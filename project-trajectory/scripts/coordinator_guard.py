#!/usr/bin/env python3
"""The coordinator context guard: stop new lanes at a context threshold, close
out, hand off, and relaunch at session end (WI-822; docs/specs/WI-822.md).

An interactive Claude Code coordinator session grows its context over many
lanes, and compaction then degrades it. This module is the whole guard:

- **the occupancy reader** (`read_occupancy`): the newest valid assistant
  `usage` after the transcript's last compaction boundary, on the live branch,
  read from the transcript's TAIL only (transcripts reach tens of MB);
- **the lease** (`take`, `release`, `clear`, `hand_back`): one record naming
  the one coordinator session, under the primary checkout's untracked
  `out/coordinator/`. It passes in exactly three ways: to the relaunched
  successor at its `SessionStart`, by the holder's recorded hand-back naming
  the handoff it closed with (freeing it for the next session's take), or by
  the owner's recorded release of a holder that has gone. Time never
  transfers it;
- **the drain latch** (`latch_reading`): the first reading at or above the
  declared threshold latches drain mode in the lease, and only the successor's
  take, the holder's hand-back (which frees the lease with it) or the owner's
  recorded clear or release unlatches it;
- **the admission boundary** (`claim_refusal`): the work-item claim calls it on
  every route except the live dispatcher's;
- **the hook entry point** (`hook`): one CLI dispatching on the event name the
  hook input carries;
- **the relaunch** (`request_relaunch`, `session_end`, `launch_detached`): a
  request written atomically, acquired by rename at the holder's exit, and
  launched detached through the repo's launcher in the declared repo root;
- **the blackout close-down** (`window_refusal`, `on_blackout`,
  `launch_reason`, `blackout_session_end`, `window_check`; WI-834): inside
  the declared blackout window every claim is refused, the main session's
  launches are denied, it is told to close down, and no relaunch is requested
  or launched, whatever the context guard's dial says;
- **the hooks opt-in** (`hooks_state`, `enable_hooks`): dev-setup's consented
  switch from the inert hook config to the project settings.

SHIPPED OFF. At `[coordinator] context_guard_pct = 0` the context guard's
entry points return before reading or writing its state: claims behave as
without the guard and the hooks print nothing, except inside an open blackout
window (`[policies] blackout`), which the claim and the hooks act on at any
dial.

The Claude Code facts this relies on are version-dependent claims, read from
its hooks reference and from transcripts of 2.1.285: the hook input fields
(`hook_event_name`, `session_id`, `transcript_path`, `agent_id` on a
subagent's call, `reason` on SessionEnd, `trigger` on PreCompact),
`hookSpecificOutput.additionalContext`, the session id a Bash child sees in
`CLAUDE_CODE_SESSION_ID`, and the transcript's record shapes. Supervision, not
security: a session that can edit files can remove a hook.

Stdlib only, Python 3.11+, Windows/POSIX.

Contracts: IF-271, IF-274, IF-275, IF-277, IF-278, IF-279, IF-280, IF-281 —
the interface seams this module declares (process.md §8; rows of record in
docs/requirements/interfaces.toml).

Contract IF-271: `claim_refusal(root, env=None)` returns the refusal text,
    naming the reason, or None when a guarded claim may proceed. It asks
    `window_refusal(root)` first, before the dial: inside the blackout window
    it refuses, naming the window's UTC end, at any dial. Outside the window
    it returns None while `[coordinator] context_guard_pct` is 0, and
    otherwise the context guard's decision. The caller's session is read from
    `CLAUDE_CODE_SESSION_ID` in `env` (default the process environment). The
    live dispatcher's claim calls `window_refusal` alone: it is exempt from
    the context guard, not from the window.

Contract IF-274: the hook's stdin is one JSON object carrying
    `hook_event_name`, `session_id` and `transcript_path`, with `agent_id`,
    `reason` and `trigger` where the event provides them, and on PreToolUse
    `tool_name` and `tool_input` (a shell tool's `command`). Stdin that does
    not parse is reported on stderr and answered with nothing; the exit is 0.

Contract IF-275: a hook response is one line of JSON on stdout,
    `hookSpecificOutput` with `hookEventName` and `additionalContext`, printed
    only when the guard has context to add; otherwise nothing is printed.
    Inside the blackout window a main session's PreToolUse for a new `Agent`,
    a `SendMessage`, or a `Bash` or `PowerShell` command naming a model CLI
    as a command word (the line read with that shell's quoting) is refused:
    `permissionDecision` `deny` with its `permissionDecisionReason`. So is a
    shell command line that cannot be read (an unclosed quote, substitution
    or here-string), naming why. The hook refuses nothing else and always
    exits 0.

Contract IF-277: our reading of the agent CLI's process environment, stated
    here because the CLI's documentation is not ours. A Bash child of a
    Claude Code session sees that session's id in `CLAUDE_CODE_SESSION_ID`,
    and a hook process sees the project root in `CLAUDE_PROJECT_DIR`. The
    guard takes the caller's session from the first (an explicit `--session`
    wins) and its default `--root` from the second (else `.`). An absent
    session id is an unnamed caller, which a guarded claim refuses.

Contract IF-278: `PT_COORDINATOR_TAKE` carries the successor token. A
    launcher sets it for the session it starts; at that session's
    `SessionStart` the guard takes the lease only when the token matches
    the successor token the lease recorded at the relaunch. An absent token
    takes nothing; a mismatched one takes nothing and is recorded as a
    refused take.

Contract IF-279: the guard starts a launcher, detached, as
    `coordinator-relaunch.{cmd,sh} REPO_ROOT PROMPT_FILE TOKEN`: the
    declared repo root, a prompt file holding the handoff's session prompt,
    and the successor token. The POSIX launcher reads the prompt file
    itself; the Windows launcher passes it back as
    `coordinator_guard.py exec-claude --prompt-file PROMPT_FILE`, which runs
    `claude` with the prompt as its one argument and exits with claude's
    code. A launcher that exits non-zero within the grace period is a
    failed launch, and the request is restored.

Contract IF-280: the command line is `coordinator_guard.py [--root ROOT]`
    with one of `hook`, `status`, `take [--session S] [--transcript T]`,
    `release --reason R`, `clear --reason R`,
    `request-relaunch --handoff H [--session S]`,
    `handback --handoff H [--session S]`, `window-check`, or
    `hooks --example E [--enable]`, which prints `none`, `on` or `off` for
    the guard hooks the inert config E registers against the machine-local
    `.claude/settings.local.json`, merging them in first with `--enable`,
    each bound to the interpreter the command runs on.

Contract IF-281: the command line's exit code is 0 on success and 1 on a
    refusal, whose reason goes to stderr after "coordinator guard: "; a
    usage error exits 2; `hook` always exits 0. `window-check` exits 1 inside
    the blackout window and 0 outside it; `hooks` exits 1 only when a
    settings file does not parse.

Runtime state (internal, no seam: only this module reads or writes it, and
    every other reader goes through IF-271): `out/coordinator/` under the
    primary checkout holds
    `lease.json`, `events.jsonl` (one JSON event per line, appended),
    `relaunch.json`, consumed and refused request files
    (`relaunch.<token>.consumed`, `relaunch.<token>.refused`), prompt files
    (`relaunch-prompt.<token>.txt`) and the directory lock `.lock`. Lease and
    request records are whole-file atomic writes; a request is acquired by
    renaming it; the directory lock serializes every read-modify-write.
"""

import argparse
import json
import os
import re
import secrets
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

try:
    import agent_common
    import agent_route
    import session_keep
    from kitlib import guard_hooks, shell_line
    from kitlib.observation import write_atomic
except ImportError:  # pragma: no cover - in-process import from elsewhere
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import agent_common
    import agent_route
    import session_keep
    from kitlib import guard_hooks, shell_line
    from kitlib.observation import write_atomic

SECTION = "coordinator"
DEFAULT_WINDOW = 200_000
SESSION_ENV = "CLAUDE_CODE_SESSION_ID"
TAKE_ENV = "PT_COORDINATOR_TAKE"
# SessionEnd reasons that are a true exit. `clear` and `resume` end a session
# id without ending the coordinator, so they never launch.
EXIT_REASONS = frozenset({"logout", "prompt_input_exit", "other"})
MONITORED = frozenset(
    {"PreToolUse", "PostToolUse", "PostToolUseFailure", "UserPromptSubmit", "Stop"}
)
# A latched session is reminded on every REMINDER_EVERY-th monitored event.
REMINDER_EVERY = 20
# The transcript tail read first, and the most ever read for one reading.
TAIL_BYTES = 256 * 1024
MAX_TAIL_BYTES = 8 * 1024 * 1024
# The characters a path may hold and still be written unquoted, so one command
# line runs as typed in Bash and in PowerShell alike.
_PLAIN_PATH = re.compile(r"^[A-Za-z0-9_./:-]+$")


def _guard_command(args):
    """The guard command the instructions below tell the session to run, as
    text that runs as typed in each supported shell (round 035 F1): on the
    interpreter this hook runs on, never a bare `python` that PATH may
    resolve below the 3.11 floor (round 016 F2, decision D-019), and on this
    file's own path, so it runs from any working directory and in a scaffold.
    Plain paths give one line for both shells; any other path gives the Bash
    and the PowerShell lines side by side, each quoted for its shell."""
    paths = [Path(sys.executable).as_posix(), Path(__file__).resolve().as_posix()]
    if all(_PLAIN_PATH.match(p) for p in paths):
        return "`{} {} {}`".format(paths[0], paths[1], args)
    bash = " ".join("'{}'".format(p.replace("'", "'\\''")) for p in paths)
    pwsh = " ".join("'{}'".format(p.replace("'", "''")) for p in paths)
    return "`{} {}` (Bash) or `& {} {}` (PowerShell)".format(bash, args, pwsh, args)


# The opening both drain texts share, so the blackout close-down can tell the
# context guard's drain instruction from its other output.
DRAIN_MARK = "COORDINATOR CONTEXT GUARD"
INSTRUCTION = (
    DRAIN_MARK + ": this session's context reached {pct:.1f}% of its "
    "declared window (threshold {threshold}%), and drain mode is latched. "
    "Work-item claims now refuse. Close out now, following the session-protocol "
    "skill's coordinator close-out: (1) start no new claims or lanes; (2) bring "
    "every in-flight row to a safe point: land it, close it, or leave it "
    "committed on its lane and recorded; (3) write docs/status.md, a handoff "
    "with its session prompt, and a log fragment; (4) request the relaunch: "
    "{command}, then end the session. "
    "The next session starts from the handoff when this one exits."
)
REMINDER = (
    DRAIN_MARK + " reminder: drain mode is latched ({pct:.1f}%). No new "
    "claims; finish the close-out and request the relaunch."
)
# The close-down inside the blackout window (WI-834), told at SessionStart and
# on the monitored events, whether or not the context guard is on.
BLACKOUT_INSTRUCTION = (
    "BLACKOUT WINDOW: the declared blackout window {window} UTC is open until "
    "{end} UTC. Keep usage to a minimum: no work item is claimed, no new "
    "subagent, resumed subagent or model CLI starts here, and no relaunch is "
    "requested. Close down, following the session-protocol skill's coordinator "
    "close-out (the blackout case): (1) bring each open lane to its pause point, "
    "the last finished step whose evidence is committed, using a wrap-up "
    "adjudication of an active claim where a step needs it (the session "
    "service admits that one call); a lane whose next step is a review, rework "
    "or any launch the window refuses stops there; (2) write the handoff naming "
    "each lane and its next obligation; (3) end the session. The owner resumes "
    "after the window."
)
BLACKOUT_DENIAL = (
    "BLACKOUT WINDOW: {what} is refused until {end} UTC (the declared window "
    "{window} UTC). Close down instead: bring each open lane to its pause point, "
    "write the handoff naming each lane and its next obligation, and end the "
    "session."
)


# --- dials -------------------------------------------------------------------


@dataclass(frozen=True)
class GuardConfig:
    """The declared `[coordinator]` dials: the drain threshold in percent (0 is
    off) and the context window in tokens.

    Implements: SR-229, LLR-300
    """

    threshold: int = 0
    window: int = DEFAULT_WINDOW

    @property
    def enabled(self):
        return self.threshold > 0


def _int_dial(value, low, high):
    ok = isinstance(value, int) and not isinstance(value, bool)
    return value if ok and low <= value <= high else None


def guard_config(root):
    """The `[coordinator]` table as a GuardConfig. An absent table or a value
    outside its type or range reads as the default, so a malformed threshold
    leaves the guard OFF and a malformed window keeps the standard one.

    Implements: SR-229, LLR-300
    """
    table = agent_common.process_config(Path(root) / "docs").get(SECTION)
    table = table if isinstance(table, dict) else {}
    threshold = _int_dial(table.get("context_guard_pct"), 0, 100) or 0
    window = _int_dial(table.get("context_window_tokens"), 1, 10**9)
    return GuardConfig(threshold=threshold, window=window or DEFAULT_WINDOW)


# --- occupancy ---------------------------------------------------------------


@dataclass(frozen=True)
class Occupancy:
    """One reading. `tokens` and `pct` are None when it is unknown; `note`
    says why, or flags a window the reading does not fit.

    Implements: SR-229, LLR-300
    """

    tokens: int | None
    pct: float | None
    note: str = ""

    @property
    def known(self):
        return self.pct is not None

    def as_dict(self):
        return {"tokens": self.tokens, "pct": self.pct, "note": self.note}


def _tail_records(path, size):
    """The parsed JSON records of the last `size` bytes of `path`, and
    whether the read reached the start of the file. A partial first line and
    any line that does not parse are skipped."""
    with open(path, "rb") as handle:
        handle.seek(0, os.SEEK_END)
        end = handle.tell()
        start = max(0, end - size)
        handle.seek(start)
        data = handle.read()
    lines = data.split(b"\n")
    if start > 0:
        lines = lines[1:]
    records = []
    for line in lines:
        try:
            record = json.loads(line.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            continue
        if isinstance(record, dict):
            records.append(record)
    return records, start == 0


def _is_boundary(record):
    return record.get("type") == "system" and record.get("subtype") == (
        "compact_boundary"
    )


def _usage_tokens(record):
    """The occupancy one assistant record states, or None when it states none
    validly: a synthetic reply, a missing or non-integer field, or a zero
    total (a reading is never 0%)."""
    message = record.get("message")
    if record.get("type") != "assistant" or not isinstance(message, dict):
        return None
    usage = message.get("usage")
    if not isinstance(usage, dict) or message.get("model") == "<synthetic>":
        return None
    keys = ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")
    values = [usage.get(k, 0 if k != "input_tokens" else None) for k in keys]
    if any(_int_dial(v, 0, 10**12) is None for v in values):
        return None
    total = sum(values)
    return total or None


def _live_tip(records):
    """The newest main-chain record: the live branch's tip."""
    for record in reversed(records):
        if record.get("uuid") and not record.get("isSidechain"):
            return record
    return None


def _walk(records, whole):
    """Walk the live branch back from its tip. Returns `(tokens, note)`, or
    `(None, "more")` when the chain leaves the records read."""
    by_uuid = {r["uuid"]: r for r in records if r.get("uuid")}
    record = _live_tip(records)
    if record is None:
        return (None, "no records") if whole else (None, "more")
    while record is not None:
        if _is_boundary(record):
            return None, "no usage since the last compaction"
        tokens = _usage_tokens(record)
        if tokens is not None:
            return tokens, ""
        parent = record.get("parentUuid")
        if parent is None:
            return None, "no usage in the transcript"
        record = by_uuid.get(parent)
    return (None, "the live branch is broken") if whole else (None, "more")


def read_occupancy(transcript, window, tail_bytes=TAIL_BYTES, max_bytes=MAX_TAIL_BYTES):
    """Occupancy of `transcript` against `window` tokens: the newest valid
    assistant usage after the last compaction boundary on the live branch,
    counting input, cache-read and cache-creation tokens. Reads the tail,
    doubling it until the walk resolves or `max_bytes` is reached. No valid
    usage reads as unknown, never 0%. A total above the window is reported as
    a window mismatch, with its percent.

    Implements: SR-229, LLR-300
    """
    if not transcript:
        return Occupancy(None, None, "no transcript recorded")
    size = tail_bytes
    while True:
        try:
            records, whole = _tail_records(transcript, size)
        except OSError as exc:
            return Occupancy(None, None, "transcript unreadable: {}".format(exc))
        tokens, note = _walk(records, whole)
        if note != "more":
            break
        if size >= max_bytes:
            return Occupancy(None, None, "no usage within the tail read")
        size *= 2
    if tokens is None:
        return Occupancy(None, None, note)
    pct = 100.0 * tokens / window  # unrounded: admission compares this
    note = "window mismatch: usage exceeds the declared window" if pct > 100 else ""
    return Occupancy(tokens, pct, note)


# --- the lease store -----------------------------------------------------------


def lease_dir(root):
    """`out/coordinator/` under the primary checkout.

    Implements: SR-229, LLR-300
    """
    return session_keep.primary_out_dir(root) / SECTION


def _lease_path(directory):
    return Path(directory) / "lease.json"


def _request_path(directory):
    return Path(directory) / "relaunch.json"


def _load(directory):
    """The lease record; an absent or unreadable one reads as free."""
    try:
        data = json.loads(_lease_path(directory).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _save(directory, lease):
    write_atomic(_lease_path(directory), json.dumps(lease, indent=2) + "\n")


def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def record_event(directory, kind, **fields):
    """Append one event to `events.jsonl`: every take, release, hand-back,
    clear, latch, compaction, refused request and launch is recorded there.

    Implements: SR-229, LLR-300
    """
    entry = {"at": _now(), "event": kind}
    entry.update(fields)
    with open(
        Path(directory) / "events.jsonl", "a", encoding="utf-8", newline="\n"
    ) as handle:
        handle.write(json.dumps(entry) + "\n")


def _holder_line(lease):
    return "session {} (taken {})".format(lease.get("holder"), lease.get("taken_at"))


def take(root, session_id, transcript=None):
    """The explicit take: record `session_id` as the coordinator when no
    session holds the lease. Returns None, or the refusal.

    Implements: SR-229, LLR-300
    """
    if not session_id:
        return "no session id: run it from the session, or pass --session"
    with session_keep.dir_lock(lease_dir(root)) as directory:
        lease = _load(directory)
        if lease.get("holder") == session_id:
            return None  # already held: a re-take never unlatches
        if lease.get("holder"):
            return (
                "the coordinator lease is held by {}; the owner releases it: {}".format(
                    _holder_line(lease), _guard_command('release --reason "<why>"')
                )
            )
        _install(directory, lease, session_id, transcript, root, "take")
    return None


def _install(directory, lease, session_id, transcript, root, how):
    """Make `session_id` the holder, unlatched: the explicit take of a free
    lease, or the successor's take."""
    lease.update(
        holder=session_id,
        transcript=transcript,
        repo_root=str(Path(root).resolve()),
        taken_at=_now(),
        draining=False,
        latched_at=None,
        latched_pct=None,
        since_reminder=0,
        successor_token=None,
    )
    _save(directory, lease)
    record_event(directory, how, session=session_id, transcript=transcript)


def release(root, reason):
    """The owner's release: frees the lease, recorded with `reason`.

    Implements: SR-229, LLR-300
    """
    if not reason:
        return "a release names its reason (--reason)"
    with session_keep.dir_lock(lease_dir(root)) as directory:
        lease = _load(directory)
        _save(directory, {})
        record_event(directory, "release", reason=reason, was=lease.get("holder"))
    return None


def clear(root, reason):
    """The owner's clear: unlatches drain mode, recorded with `reason`.

    Implements: SR-229, LLR-300
    """
    if not reason:
        return "a clear names its reason (--reason)"
    with session_keep.dir_lock(lease_dir(root)) as directory:
        lease = _load(directory)
        if not lease.get("holder"):
            return "no coordinator lease is held"
        lease.update(draining=False, latched_at=None, latched_pct=None)
        _save(directory, lease)
        record_event(directory, "clear", reason=reason, holder=lease["holder"])
    return None


# --- the latch -----------------------------------------------------------------


def latch_reading(directory, lease, cfg):
    """Read the holder's transcript and latch drain mode when the reading is
    at or above the threshold. Returns `(reading, latched_now)`; saves the
    lease. The caller holds the lock.

    Implements: SR-229, LLR-300
    """
    reading = read_occupancy(lease.get("transcript"), cfg.window)
    lease["last_occupancy"] = dict(reading.as_dict(), at=_now())
    latched_now = False
    if reading.known and reading.pct >= cfg.threshold and not lease.get("draining"):
        lease.update(draining=True, latched_at=_now(), latched_pct=reading.pct)
        lease["since_reminder"] = 0
        latched_now = True
        record_event(directory, "latch", pct=reading.pct, tokens=reading.tokens)
    _save(directory, lease)
    return reading, latched_now


def window_refusal(root):
    """The blackout window's claim refusal, or None: inside the window
    (`agent_common.blackout_at`, read at this call) every claim is refused,
    naming the window's UTC end, on every route, the live dispatcher's
    included, whatever the context guard's dial says.

    Implements: SR-229, LLR-300
    """
    blackout = agent_common.blackout_at(Path(root) / "docs")
    if not blackout.inside:
        return None
    return (
        "coordinator guard: the blackout window {} UTC is open until {} UTC; no "
        "work item is claimed inside it, on any route. Claim after it ends.".format(
            blackout.window, blackout.end.strftime("%Y-%m-%d %H:%M")
        )
    )


def claim_refusal(root, env=None):
    """The admission boundary the work-item claim calls on every route but the
    live dispatcher's: None when the claim may proceed, else the refusal.
    The blackout window is asked first (`window_refusal`), before the context
    guard's dial, so it refuses with the guard off. Then, with the guard on,
    it refuses when no lease is held, when the caller's session is not the
    holder, and when drain mode is latched, reading the holder's transcript
    itself first so admission never depends on a hook having run.

    Implements: SR-229, LLR-300
    """
    refusal = window_refusal(root)
    if refusal:
        return refusal
    cfg = guard_config(root)
    if not cfg.enabled:
        return None
    env = os.environ if env is None else env
    with session_keep.dir_lock(lease_dir(root)) as directory:
        lease = _load(directory)
        refusal = _ownership_refusal(lease, env.get(SESSION_ENV))
        if refusal is None and not lease.get("draining"):
            latch_reading(directory, lease, cfg)
        if refusal is None and lease.get("draining"):
            refusal = _draining_refusal(lease, cfg)
    return refusal


def _ownership_refusal(lease, session_id):
    if not lease.get("holder"):
        return (
            "coordinator guard: no coordinator lease is held, and claims need "
            "one while [coordinator] context_guard_pct is on. Take it from "
            "the coordinator session: {}".format(_guard_command("take"))
        )
    if session_id != lease["holder"]:
        return (
            "coordinator guard: the coordinator lease is held by {}, not by "
            "this caller (session {}); only the coordinator claims. The owner "
            "releases a lease whose session has ended: {}"
        ).format(
            _holder_line(lease),
            session_id or "unknown",
            _guard_command('release --reason "<why>"'),
        )
    return None


def _draining_refusal(lease, cfg):
    return (
        "coordinator guard: drain mode is latched (since {}, at {:.1f}% of the "
        "declared window; threshold {}%). No new claims: close out, hand off "
        "and request the relaunch (the session-protocol skill's coordinator "
        "close-out)".format(
            lease.get("latched_at"), lease.get("latched_pct"), cfg.threshold
        )
    )


# --- the hook entry point ------------------------------------------------------


def _context(event, text):
    return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}


def _is_holders_call(lease, payload):
    """True only for the holder session's own call: not a subagent's, and on
    the holder's transcript."""
    if payload.get("agent_id") or payload.get("session_id") != lease.get("holder"):
        return False
    recorded = lease.get("transcript")
    return not recorded or _same_path(recorded, payload.get("transcript_path"))


def _same_path(a, b):
    """One file, however its path is spelled (case and separators on Windows)."""
    norm = lambda p: os.path.normcase(os.path.abspath(p))  # noqa: E731
    return bool(a and b) and norm(a) == norm(b)


def _instruction(pct, threshold):
    """The drain instruction, naming the request-relaunch command."""
    return INSTRUCTION.format(
        pct=pct,
        threshold=threshold,
        command=_guard_command("request-relaunch --handoff <path>"),
    )


def on_monitored(root, cfg, payload):
    """A tool, failed-tool, prompt or stop event: measure the holder's
    transcript, latch on a crossed threshold, and say so once at the latch,
    then every REMINDER_EVERY-th event while latched.

    Implements: SR-229, LLR-300
    """
    event = payload.get("hook_event_name")
    with session_keep.dir_lock(lease_dir(root)) as directory:
        lease = _load(directory)
        if not _is_holders_call(lease, payload):
            return None
        if not lease.get("transcript"):
            lease["transcript"] = payload.get("transcript_path")
        was_draining = bool(lease.get("draining"))
        reading, latched_now = latch_reading(directory, lease, cfg)
        if latched_now:
            return _context(event, _instruction(reading.pct, cfg.threshold))
        if not was_draining:
            return None
        lease["since_reminder"] = int(lease.get("since_reminder") or 0) + 1
        due = lease["since_reminder"] >= REMINDER_EVERY
        if due:
            lease["since_reminder"] = 0
        _save(directory, lease)
    return (
        _context(event, REMINDER.format(pct=lease.get("latched_pct"))) if due else None
    )


def on_session_start(root, cfg, payload, env):
    """The successor's take: a session launched by the relaunch carries the
    lease's successor token in its environment and takes the lease, which
    clears the latch. The holder's own resumed start keeps the latch and is
    told again.

    Implements: SR-229, LLR-300
    """
    session_id = payload.get("session_id")
    token = env.get(TAKE_ENV)
    with session_keep.dir_lock(lease_dir(root)) as directory:
        lease = _load(directory)
        pending = lease.get("successor_token")
        if token and pending and secrets.compare_digest(token, pending):
            _install(
                directory,
                lease,
                session_id,
                payload.get("transcript_path"),
                root,
                "take-successor",
            )
            return _context(
                "SessionStart", "You hold the coordinator lease (relaunched successor)."
            )
        if token:
            record_event(
                directory, "take-refused", session=session_id, reason="token mismatch"
            )
        if session_id != lease.get("holder") or payload.get("agent_id"):
            return None
        lease["transcript"] = payload.get("transcript_path") or lease.get("transcript")
        _save(directory, lease)
        if lease.get("draining"):
            return _context(
                "SessionStart",
                _instruction(lease.get("latched_pct"), cfg.threshold),
            )
    return None


def on_pre_compact(root, cfg, payload):
    """Compaction telemetry: the trigger, the occupancy and the guard state,
    recorded on the lease and in the event log. Never a recovery path.

    Implements: SR-229, LLR-300
    """
    with session_keep.dir_lock(lease_dir(root)) as directory:
        lease = _load(directory)
        if not _is_holders_call(lease, payload):
            return None
        reading = read_occupancy(lease.get("transcript"), cfg.window)
        entry = {
            "at": _now(),
            "trigger": payload.get("trigger"),
            "occupancy": reading.as_dict(),
            "last_occupancy": lease.get("last_occupancy"),
            "draining": bool(lease.get("draining")),
            "relaunch_requested": _request_path(directory).exists(),
        }
        entry["class"] = classify_compaction(entry, cfg)
        lease.setdefault("compactions", []).append(entry)
        _save(directory, lease)
        record_event(
            directory, "compaction", **{k: v for k, v in entry.items() if k != "at"}
        )
    return None


def classify_compaction(entry, cfg):
    """The handoff's classification of one compaction: during a drain, a
    manual compaction, or a missed threshold (auto-compaction before the latch).

    Implements: SR-229, LLR-300
    """
    if entry.get("draining"):
        return "during-drain"
    if entry.get("trigger") == "manual":
        return "manual"
    return "missed-threshold"


def hook(payload, root, env=None, launch=None):
    """One hook call: the output dict to print, or None. A no-op when the
    guard is off and no blackout window is open; inside an open window the
    blackout close-down runs whatever the guard's dial says (`on_blackout`).

    Implements: SR-229, LLR-300
    """
    cfg = guard_config(root)
    if not isinstance(payload, dict):
        return None
    blackout = agent_common.blackout_at(Path(root) / "docs")
    if blackout.inside:
        return on_blackout(root, cfg, payload, blackout, env)
    if not cfg.enabled:
        return None
    if payload.get("hook_event_name") == "SessionEnd":
        session_end(root, payload, launch=launch)
        return None
    return _guard_event(root, cfg, payload, os.environ if env is None else env)


def _guard_event(root, cfg, payload, env):
    """The context guard's own handling of a tool, prompt, stop, start or
    compaction event (not SessionEnd)."""
    event = payload.get("hook_event_name")
    if event in MONITORED:
        return on_monitored(root, cfg, payload)
    if event == "SessionStart":
        return on_session_start(root, cfg, payload, env)
    if event == "PreCompact":
        return on_pre_compact(root, cfg, payload)
    return None


# --- the blackout window: the coordinator's close-down (WI-834) ----------------


def on_blackout(root, cfg, payload, blackout, env=None):
    """One hook call inside the blackout window, guard on or off. SessionEnd
    cancels the ending session's pending relaunch and launches nothing. Every
    other event runs the context guard's handling first when it is on (the
    latch is unchanged), then, for the main session (not a subagent), adds
    the close-down: PreToolUse denies a launch (`launch_reason`), SessionStart
    tells the close-down, and the monitored events tell it at the window's
    first event and then every REMINDER_EVERY-th. A context-guard drain text
    (it asks for a relaunch) is replaced by the close-down, told on that
    event, while its latch stays recorded (round 035 F2). Nothing is latched
    for the window: its drain is the clock's, so nothing is cleared after it.

    Implements: SR-229, SR-230, LLR-300, LLR-301
    """
    if payload.get("hook_event_name") == "SessionEnd":
        blackout_session_end(root, payload)
        return None
    env = os.environ if env is None else env
    guarded = _guard_event(root, cfg, payload, env) if cfg.enabled else None
    if payload.get("agent_id"):
        return guarded
    drain = _is_drain(guarded)
    if drain:  # the latch is recorded; the window's close-down replaces its text
        guarded = None
    return _combine(guarded, _close_down(root, payload, blackout, drain))


def _is_drain(output):
    """True when a context guard hook output is its drain instruction or
    reminder, which asks for the relaunch the window refuses."""
    spec = (output or {}).get("hookSpecificOutput") or {}
    return str(spec.get("additionalContext") or "").startswith(DRAIN_MARK)


def _close_down(root, payload, blackout, tell=False):
    """The main session's close-down output for one event, or None; `tell`
    tells it whatever the reminder cadence (in place of a drain text)."""
    event = payload.get("hook_event_name")
    end = blackout.end.strftime("%Y-%m-%d %H:%M")
    if event == "PreToolUse":
        what = launch_reason(root, payload)
        if what:
            return _deny(
                BLACKOUT_DENIAL.format(what=what, end=end, window=blackout.window)
            )
    told = (
        tell
        or event == "SessionStart"
        or (event in MONITORED and _reminder_due(root, payload, blackout))
    )
    if not told:
        return None
    return _context(event, BLACKOUT_INSTRUCTION.format(window=blackout.window, end=end))


def _deny(reason):
    """A PreToolUse refusal of the tool call."""
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def _combine(first, second):
    """One hook response from two: the second's decision kept, and the two
    `additionalContext` texts joined."""
    if not first or not second:
        return first or second
    out = dict(second["hookSpecificOutput"])
    texts = [
        o["hookSpecificOutput"].get("additionalContext")
        for o in (first, second)
        if o["hookSpecificOutput"].get("additionalContext")
    ]
    if texts:
        out["additionalContext"] = "\n\n".join(texts)
    return {"hookSpecificOutput": out}


def _reminder_due(root, payload, blackout):
    """True at the main session's first monitored event inside this window
    and every REMINDER_EVERY-th after it: a cadence keyed by the window's end,
    so a later window starts afresh and nothing needs clearing."""
    session = payload.get("session_id") or ""
    end = blackout.end.isoformat()
    with session_keep.dir_lock(lease_dir(root)) as directory:
        path = Path(directory) / "blackout-told.json"
        try:
            told = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            told = {}
        told = {
            k: v
            for k, v in (told.items() if isinstance(told, dict) else ())
            if isinstance(v, dict) and v.get("end") == end
        }
        count = int(told.get(session, {}).get("count") or 0)
        told[session] = {"end": end, "count": count + 1}
        write_atomic(path, json.dumps(told, indent=2) + "\n")
    return count % REMINDER_EVERY == 0


# The tools a main session starts or resumes another model with.
LAUNCH_TOOLS = {"Agent": "a new subagent", "SendMessage": "a message to a subagent"}
# The shell tools, each read with its own shell's quoting (`shell_line`).
SHELL_TOOLS = {"Bash": "posix", "PowerShell": "powershell"}
_ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
# A PowerShell assignment operator (`=` `+=` `-=` `*=` `/=` `%=` `??=`). An
# assignment is recognised by its operator, never by its target's shape, so
# property, index, typed, scoped and any other target form is covered (round
# 016 F1 and round 018 F1, decision D-020).
_PS_OPERATOR = re.compile(r"(?:[-+*/%]|\?\?)?=")
_EXECUTABLE_SUFFIXES = (".exe", ".cmd", ".bat", ".com", ".ps1")
# Option words of `timeout` and `env` that take the next word as their value
# (env's split string is read by `_split_string`).
_OPTION_ARGS = {
    "timeout": frozenset({"-s", "-k", "--signal", "--kill-after"}),
    "env": frozenset({"-u", "-C", "--unset", "--chdir"}),
}
# Shell grammar words that stand before a command and are never one, each
# mapped to its shape (round 028 F1, decision D-025): the option words it
# takes, and the openers before which one word is its NAME. Bash's
# `time [-p] [--] pipeline`; `coproc [NAME] compound-command`, the NAME
# taken before every compound-command opener (round 030 F1, D-026; the
# reader splits at `(`, so `coproc NAME ( ... )` reads NAME and its body as
# its own simple command), and `coproc` before a simple command.
_NO_SHAPE = (frozenset(), frozenset())
_GRAMMAR_WORDS = {
    "time": (frozenset({"-p", "--"}), frozenset()),
    "coproc": (
        frozenset(),
        frozenset({"{", "while", "until", "if", "for", "select", "case", "[[", "(("}),
    ),
    **dict.fromkeys(
        ("!", "{", "}", "if", "then", "else", "elif", "do", "while", "until"),
        _NO_SHAPE,
    ),
}


def launch_reason(root, payload):
    """What a main session's tool call would launch, or None: a new `Agent`
    call, a `SendMessage`, or a `Bash` or `PowerShell` command naming a model
    CLI as any command word (`command_words`, read with that shell's
    quoting). The CLI names are the executables of `docs/agents.toml`'s
    `cmd_template` cells (`model_clis`), never a hand-kept list. A command
    line the hook cannot read is refused too, naming why (decision D-010 in
    docs/decisions/wi-834.toml). Script wrappers are not inspected: a
    coordinator launch script calls `window-check` itself.

    Implements: SR-229, LLR-300
    """
    tool = payload.get("tool_name")
    if tool in LAUNCH_TOOLS:
        return LAUNCH_TOOLS[tool]
    tool_input = payload.get("tool_input")
    if tool not in SHELL_TOOLS or not isinstance(tool_input, dict):
        return None
    command = str(tool_input.get("command") or "")
    try:
        words = set(command_words(command, SHELL_TOOLS[tool]))
    except shell_line.Unreadable as unreadable:
        return "a {} command line the hook cannot read ({}); rewrite it".format(
            tool, unreadable
        )
    named = sorted(words & model_clis(root))
    return "the model CLI {}".format(named[0]) if named else None


def model_clis(root):
    """The command names of the executables `docs/agents.toml`'s
    `cmd_template` cells start with (every row, enabled or not), read by the
    kit's one template reader (`split_cmd`: the shell-string or JSON-array
    form). A template that reader refuses launches nothing through the kit
    and names nothing here.

    Implements: SR-229, LLR-300
    """
    rows, _errors = agent_route.load_registry(Path(root) / "docs" / "agents.toml")
    names = set()
    for row in rows.values():
        try:
            argv = agent_common.split_cmd(row.cmd_template or "")
        except ValueError:
            continue
        if argv:
            names.add(command_name(argv[0]))
    names.discard("")
    return names


def command_name(word):
    """An unquoted command word as a name: its directory and an executable
    suffix dropped, lowercased (`C:/bin/codex.exe` reads `codex`).

    Implements: SR-229, LLR-300
    """
    base = re.split(r"[\\/]", word)[-1].lower()
    for suffix in _EXECUTABLE_SUFFIXES:
        if base.endswith(suffix):
            return base[: -len(suffix)]
    return base


def command_words(command, dialect="posix"):
    """The command word of every simple command of a shell command line
    (`kitlib.shell_line.segments`, the one reading of it), read past
    `VAR=value` assignments, the shell's grammar words and the `timeout` and
    `env` prefixes (with their options, `timeout`'s duration and env's split
    string). Raises `shell_line.Unreadable`. Scripts are not read into.

    Implements: SR-229, LLR-300
    """
    found = shell_line.segments(command, dialect)
    if dialect == "powershell":
        found = [_invoked(_assigned(words)) for words in found]
    names = (_segment_command(words) for words in found)
    return [name for name in names if name]


def _assigned(words):
    """A PowerShell statement's words past a leading assignment: the
    right-hand side, read as a command (`$r = claude -p x` runs `claude`), or
    none when it opens with a value (a quoted string, or a variable that is
    not itself an assignment). A statement is an assignment when its first
    word is unquoted and starts with `$` or `[` and an unquoted assignment
    operator follows (standalone, or written against a word); any other
    statement's words are returned unchanged.

    Implements: SR-229, LLR-300
    """
    first = words[0] if words else ""
    if first[:1] not in ("$", "[") or first.opens_quoted:
        return words
    for i, word in enumerate(words):
        end = _operator_end(word)
        if end is not None:
            return _right_hand(_tail(word, end), words[i + 1 :])
    return words


def _invoked(words):
    """A PowerShell statement's words past a leading dot invocation operator:
    an unquoted `.` word, like `&` (a boundary the reader already splits
    at), makes the next word the command (`. claude -p x`). A quoted `'.'`
    is data. Wrappers that take a command as an argument stay outside the
    coverage (round 024 F1, dispute 025, decision D-024).

    Implements: SR-229, LLR-300
    """
    if words and words[0] == "." and not words[0].spans:
        return words[1:]
    return words


def _operator_end(word):
    """Where the first assignment operator in `word` none of whose characters
    was quoted ends, or None: `$h['answer']=x` holds one, `$h['a=b']` none."""
    for found in _PS_OPERATOR.finditer(word):
        if not any(word.quoted(i) for i in range(found.start(), found.end())):
            return found.end()
    return None


def _tail(word, at):
    """`word` from offset `at`, its quoted spans kept."""
    tail = shell_line.Word(word[at:])
    tail.spans = tuple(
        (max(start - at, 0), end - at)
        for start, end in word.spans
        if end > at or start >= at
    )
    return tail


def _right_hand(head, after):
    """An assignment's right-hand side as a command: `head` (the part written
    against the operator, when any) then `after`. None when it opens with a
    quoted string, or with a variable that is not itself an assignment (a
    chained `$a = $b = claude` runs `claude`)."""
    words = ([head] if head else []) + after
    if not words or words[0].opens_quoted:
        return []
    if words[0].startswith("$"):
        chained = _assigned(words)
        return [] if chained is words else chained
    return words


def _segment_command(words):
    """The command one simple command's words run, past assignments,
    grammar words with their shapes (`_past_grammar`) and prefixes."""
    i = 0
    while i < len(words):
        name = command_name(words[i])
        if name in _GRAMMAR_WORDS:
            i = _past_grammar(words, i, name)
        elif _ASSIGNMENT.match(words[i]) or not name:
            i += 1
        elif name in _OPTION_ARGS:
            i, split = _past_prefix(words, i + 1, name)
            if split is not None:
                return _segment_command(["env"] + split + words[i:])
        else:
            return name
    return None


def _past_grammar(words, i, name):
    """The index past the grammar word `name` at `i` and the words its
    declared shape (`_GRAMMAR_WORDS`) gives it: its options, then a NAME
    when the word after that opens a compound command (`coproc NAME {`)."""
    options, name_before = _GRAMMAR_WORDS[name]
    i += 1
    while i < len(words) and words[i] in options:
        i += 1
    if i + 1 < len(words) and words[i + 1] in name_before:
        i += 1
    return i


def _past_prefix(words, i, prefix):
    """`(index, split)`: the index past `prefix`'s options (and `timeout`'s
    duration), or past env's split string with that string's words."""
    while i < len(words) and words[i].startswith("-"):
        if words[i] == "--":
            i += 1
            break
        split = _split_string(words, i) if prefix == "env" else None
        if split is not None:
            return split
        i += 2 if words[i] in _OPTION_ARGS[prefix] else 1
    if prefix == "timeout" and i < len(words):
        i += 1  # the duration
    return i, None


def _split_string(words, i):
    """`env -S STRING` (`-SSTRING`, `--split-string[=]STRING`): the index
    past it and STRING's words, which env reads as more of its own
    arguments; else None."""
    word = words[i]
    if word in ("-S", "--split-string"):
        string, i = (words[i + 1] if i + 1 < len(words) else ""), i + 2
    elif word.startswith("--split-string="):
        string, i = word.partition("=")[2], i + 1
    elif word.startswith("-S"):
        string, i = word[2:], i + 1
    else:
        return None
    found = shell_line.segments(string)
    return i, (found[0] if found else [])


def blackout_session_end(root, payload):
    """At the main session's true exit inside the blackout window: its own
    pending relaunch request is cancelled, renamed
    `relaunch.<token>.cancelled` and recorded as `blackout`; no successor
    starts. Returns True when one was cancelled.

    Implements: SR-230, LLR-301
    """
    if payload.get("reason") not in EXIT_REASONS or payload.get("agent_id"):
        return False
    session_id = payload.get("session_id")
    with session_keep.dir_lock(lease_dir(root)) as directory:
        if not session_id or not _own_request_pending(directory, session_id):
            return False
        cancelled = Path(directory) / "relaunch.{}.cancelled".format(
            secrets.token_hex(16)
        )
        os.replace(_request_path(directory), cancelled)
        record_event(
            directory, "relaunch-cancelled", reason="blackout", session=session_id
        )
    return True


def window_check(root):
    """The `window-check` subcommand, for a coordinator launch script that
    starts a model outside the session service: the refusal inside the
    blackout window (exit 1), else None (exit 0). A service-backed entry
    point does not call it; the service's admission governs it.

    Implements: SR-229, LLR-300
    """
    blackout = agent_common.blackout_at(Path(root) / "docs")
    if not blackout.inside:
        return None
    return "the blackout window {} UTC is open until {} UTC; no model starts".format(
        blackout.window, blackout.end.strftime("%Y-%m-%d %H:%M")
    )


# --- the relaunch ----------------------------------------------------------------


def session_prompt(handoff):
    """The handoff's session prompt: the first fenced block under a
    `Session prompt` heading, or None.

    Implements: SR-230, LLR-301
    """
    try:
        lines = Path(handoff).read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return None
    under = fenced = False
    body = []
    capturing = False
    for line in lines:
        if line.startswith("```"):
            if fenced and capturing:
                return "\n".join(body).strip() or None
            fenced, capturing = not fenced, under and not fenced
        elif fenced:
            if capturing:
                body.append(line)  # a `#` line inside a fence is its text
        elif line.startswith("#"):
            under = "session prompt" in line.lower()
    return None


def _promptless(handoff):
    """The refusal of a handoff with no session prompt, or None."""
    if session_prompt(handoff):
        return None
    return "{} carries no session prompt (a fenced block under a 'Session prompt' heading)".format(
        handoff
    )


def _not_holder(lease, session_id, act):
    """The refusal of a caller that is not the lease holder, or None."""
    if session_id and lease.get("holder") == session_id:
        return None
    return "only the lease holder {} (holder: {}, caller: {})".format(
        act, lease.get("holder"), session_id
    )


def request_relaunch(root, handoff, session_id):
    """Write the relaunch request for the holder: its session id, the repo
    root, the handoff and the creation time, atomically. Returns None, or the
    refusal.

    Inside the blackout window no request is written: the close-down ends the
    session instead (`window_check`).

    Implements: SR-230, LLR-301
    """
    refusal = window_check(root)
    if refusal:
        return "{}: no relaunch is requested inside it; write the handoff and end the session".format(
            refusal
        )
    handoff = Path(handoff).resolve()
    refusal = _promptless(handoff)
    if refusal:
        return refusal
    with session_keep.dir_lock(lease_dir(root)) as directory:
        lease = _load(directory)
        refusal = _not_holder(lease, session_id, "requests the relaunch")
        if refusal:
            return refusal
        request = {
            "session_id": session_id,
            "repo_root": lease.get("repo_root") or str(Path(root).resolve()),
            "handoff": str(handoff),
            "created": _now(),
        }
        write_atomic(_request_path(directory), json.dumps(request, indent=2) + "\n")
        record_event(directory, "relaunch-requested", **request)
    return None


def _own_request_pending(directory, session_id):
    """True when the relaunch request on file is `session_id`'s own; an
    absent, unreadable or another session's request is not."""
    try:
        request = json.loads(_request_path(directory).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return isinstance(request, dict) and request.get("session_id") == session_id


def hand_back(root, handoff, session_id):
    """The holder's hand-back at its close-out: frees the lease, its latch
    with it, recorded with the handoff it closed with, so the next session's
    take succeeds. Refuses another caller first, whatever handoff it names
    (the owner releases a holder that has gone), then a handoff with no
    session prompt, then the holder's own pending relaunch request (its
    successor takes the lease at its start). A previous holder's request
    never blocks it: it is left for session_end's foreign-request refusal.
    Returns None, or the refusal; with the guard off it returns before
    reading or writing.

    Implements: SR-229, LLR-300
    """
    if not guard_config(root).enabled:
        return None
    handoff = Path(handoff).resolve()
    promptless = _promptless(handoff)  # read before the lock, reported after
    with session_keep.dir_lock(lease_dir(root)) as directory:
        lease = _load(directory)
        refusal = _not_holder(lease, session_id, "hands the lease back")
        if refusal:
            return "{}; the owner releases a lease whose holder has gone: {}".format(
                refusal, _guard_command('release --reason "<why>"')
            )
        if promptless:
            return promptless
        if _own_request_pending(directory, session_id):
            return (
                "a relaunch is requested: end the session, and the relaunched "
                "successor takes the lease at its start"
            )
        _save(directory, {})
        record_event(
            directory,
            "handback",
            session=session_id,
            handoff=str(handoff),
            was_draining=bool(lease.get("draining")),
        )
    return None


def _request_problem(request, session_id, lease):
    if not isinstance(request, dict):
        return "the request does not parse"
    if request.get("session_id") != session_id:
        return "the request is from session {}, not the ending holder {}".format(
            request.get("session_id"), session_id
        )
    if request.get("repo_root") != lease.get("repo_root"):
        return "the request names repo {}, not this repo {}".format(
            request.get("repo_root"), lease.get("repo_root")
        )
    if not session_prompt(request.get("handoff") or ""):
        return "the request's handoff {} is missing or has no session prompt".format(
            request.get("handoff")
        )
    return None


def _acquire(directory, token):
    """Take the request by renaming it to a consumed name: of two concurrent
    handlers exactly one finds it. Returns `(consumed path, request)` or None."""
    consumed = Path(directory) / "relaunch.{}.consumed".format(token)
    try:
        os.rename(_request_path(directory), consumed)
    except OSError:
        return None
    try:
        request = json.loads(consumed.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        request = None
    return consumed, request


def session_end(root, payload, launch=None):
    """At the holder's true exit, launch the successor for the holder's own
    request, once. Returns True when it launched. The store lock is held from
    the acquisition to the launch's confirmation or restoration, so restoring
    never waits on the lock (decision D-014).

    Implements: SR-230, LLR-301
    """
    if payload.get("reason") not in EXIT_REASONS or payload.get("agent_id"):
        return False
    session_id = payload.get("session_id")
    token = secrets.token_hex(16)
    with session_keep.dir_lock(lease_dir(root)) as directory:
        lease = _load(directory)
        if not session_id or lease.get("holder") != session_id:
            return False
        acquired = _acquire(directory, token)
        if acquired is None:
            return False
        consumed, request = acquired
        problem = _request_problem(request, session_id, lease)
        if problem:
            os.replace(consumed, consumed.with_suffix(".refused"))
            record_event(directory, "relaunch-refused", reason=problem)
            print("coordinator guard: relaunch refused: " + problem, file=sys.stderr)
            return False
        return _launch_or_restore(directory, lease, consumed, request, token, launch)


def _restore(directory, consumed, prompt_file, exc):
    """Undo an acquisition whose launch was not confirmed: the request goes
    back first (so it is never stranded), then the successor token is cleared
    and the prompt file removed, best effort, and the failure is reported.
    The caller holds the lock it acquired the request under."""
    os.replace(consumed, _request_path(directory))
    try:
        lease = _load(directory)
        if lease.get("successor_token"):
            lease["successor_token"] = None
            _save(directory, lease)
        record_event(directory, "launch-failed", reason=str(exc))
    except OSError as cleanup:
        print("coordinator guard: cleanup failed: {}".format(cleanup), file=sys.stderr)
    prompt_file.unlink(missing_ok=True)
    print(
        "coordinator guard: relaunch failed, request restored: {}".format(exc),
        file=sys.stderr,
    )


def _launch_or_restore(directory, lease, consumed, request, token, launch):
    """Save the successor token, write the prompt file and run the launch,
    under the lock the request was acquired with. Every failure, of any
    exception type, from the token save to a confirmed launch puts the
    request back, removes the successor token and the prompt file, and
    reports: one restoration route, which never reacquires the lock."""
    prompt_file = Path(directory) / "relaunch-prompt.{}.txt".format(token)
    try:
        lease["successor_token"] = token
        _save(directory, lease)
        prompt_file.write_text(
            session_prompt(request["handoff"]), encoding="utf-8", newline="\n"
        )
        (launch or launch_detached)(Path(request["repo_root"]), prompt_file, token)
    except Exception as exc:  # noqa: BLE001 - any failure before confirmation restores
        _restore(directory, consumed, prompt_file, exc)
        return False
    record_event(
        directory,
        "launched",
        handoff=request["handoff"],
        repo_root=request["repo_root"],
    )
    return True


# Popen creation flags for a new console window, detached from the hook's.
_NEW_CONSOLE = 0x10 | 0x200  # CREATE_NEW_CONSOLE | CREATE_NEW_PROCESS_GROUP


def launch_command(repo_root, prompt_file, token, os_name=None):
    """`(launcher, command, Popen keywords)` for this platform: the repo's
    `.cmd` on Windows (the command is one command line for cmd), its POSIX
    sibling elsewhere (an argv), run in `repo_root` with the prompt file and
    the successor token.

    Implements: SR-230, LLR-301
    """
    os_name = os.name if os_name is None else os_name
    repo_root = Path(repo_root)
    args = [str(repo_root), str(prompt_file), token]
    if os_name == "nt":
        launcher = repo_root / "scripts" / "coordinator-relaunch.cmd"
        # One command line, not an argv: `cmd /s /c "<line>"` strips exactly
        # the outer quote pair and runs the rest, so a quoted launcher path and
        # quoted arguments survive a root with spaces (a Windows path cannot
        # contain a quote). No standard-handle redirection: the new console's
        # own handles are the interactive successor's stdin, stdout and stderr.
        line = " ".join('"{}"'.format(part) for part in [str(launcher)] + args)
        return (
            launcher,
            'cmd /d /s /c "{}"'.format(line),
            {"creationflags": _NEW_CONSOLE},
        )
    launcher = repo_root / "scripts" / "coordinator-relaunch.sh"
    # The POSIX launcher opens its own terminal; its own streams carry nothing.
    quiet = {
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "start_new_session": True,
    }
    return launcher, ["sh", str(launcher)] + args, quiet


# How long a started launcher is watched before its launch counts as
# confirmed: a launcher that fails exits at once; one that works keeps running
# (Windows: claude runs in it) or exits 0 having opened a terminal (POSIX).
LAUNCH_GRACE_SECONDS = 5.0


def launch_detached(
    repo_root,
    prompt_file,
    token,
    popen=subprocess.Popen,
    os_name=None,
    grace=LAUNCH_GRACE_SECONDS,
):
    """Start the launcher detached in `repo_root` and confirm it. Raises
    OSError when it cannot start (a missing launcher included) or exits
    non-zero within `grace` seconds; still running, or exited 0, confirms.

    Implements: SR-230, LLR-301
    """
    launcher, argv, extra = launch_command(repo_root, prompt_file, token, os_name)
    if not launcher.is_file():
        raise OSError("launcher not found: {}".format(launcher))
    process = popen(argv, cwd=str(repo_root), close_fds=True, **extra)
    try:
        code = process.wait(timeout=grace)
    except subprocess.TimeoutExpired:
        return
    if code != 0:
        raise OSError("launcher {} exited {}".format(launcher.name, code))


def exec_claude(prompt_file, run=subprocess.call):
    """The Windows launcher's last step: run `claude` with the prompt as its
    one argument (Python quotes it, which a `.cmd` cannot do safely).

    Implements: SR-230, LLR-301
    """
    prompt = Path(prompt_file).read_text(encoding="utf-8")
    return run(["claude", prompt])


# --- the hooks opt-in (WI-834 part D) ----------------------------------------------


def _read_json(path):
    """A JSON object from `path`: {} when absent; ValueError when unreadable."""
    path = Path(path)
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("{} is not a JSON object".format(path))
    return data


def _local_settings(root):
    """The machine-local Claude Code settings the opt-in writes: their hook
    commands name this machine's interpreter, so they never go in the
    committed `.claude/settings.json` (decision D-019)."""
    return Path(root) / ".claude" / "settings.local.json"


def _guard_plan(example, interpreter):
    """`(wanted, shapes)`: the inert example's guard hook groups bound to
    `interpreter` (`{event: [group, ...]}`), and the guard's own command
    shapes, the one definition of what the opt-in owns (`kitlib.guard_hooks`)."""
    found = guard_hooks.guard_groups(_read_json(example))
    wanted = {
        e: [guard_hooks.bind(g, interpreter) for g in gs] for e, gs in found.items()
    }
    return wanted, guard_hooks.command_shapes(found)


def hooks_state(root, example, interpreter=None):
    """`none` when the inert config `example` registers no guard hook, `on`
    when the machine-local settings already are what switching on would make
    them (`kitlib.guard_hooks.merged`, bound to `interpreter`, this process's own by default),
    else `off`.

    Implements: SR-229, LLR-300
    """
    wanted, shapes = _guard_plan(example, interpreter or sys.executable)
    if not wanted:
        return "none"
    live = _read_json(_local_settings(root)).get("hooks") or {}
    return "on" if guard_hooks.merged(live, wanted, shapes) == live else "off"


def enable_hooks(root, example, interpreter=None):
    """Switch the coordinator's hooks on: every guard hook group the inert
    config `example` registers, bound to `interpreter` (this process's own
    by default: the floor-resolved one dev-setup runs this on), is merged
    into the machine-local `.claude/settings.local.json` (`guard_hooks.merged`: only
    the guard's own commands are replaced; every other command, group and
    setting is kept). The committed `.claude/settings.json` is never
    written. Idempotent.

    Implements: SR-229, LLR-300
    """
    path = _local_settings(root)
    settings = _read_json(path)
    wanted, shapes = _guard_plan(example, interpreter or sys.executable)
    settings["hooks"] = guard_hooks.merged(settings.get("hooks") or {}, wanted, shapes)
    path.parent.mkdir(parents=True, exist_ok=True)
    write_atomic(path, json.dumps(settings, indent=2) + "\n")


def _hooks_main(root, example, enable):
    """`hooks`: print `none`, `on` or `off`, switching them on first with
    `--enable` (a `none` example changes nothing)."""
    try:
        if enable and hooks_state(root, example) == "off":
            enable_hooks(root, example)
        print(hooks_state(root, example))
    except ValueError as exc:
        return "the hook settings do not parse: {}".format(exc)
    return 0


# --- CLI -------------------------------------------------------------------------


def _hook_main(root):
    try:
        payload = json.loads(sys.stdin.read() or "{}")
        output = hook(payload, root)
    except Exception as exc:  # noqa: BLE001 - a broken hook must not wedge the tools
        print("coordinator guard: hook error: {}".format(exc), file=sys.stderr)
        return 0
    if output:
        print(json.dumps(output))
    return 0


def _status(root):
    cfg = guard_config(root)
    lease = _load(lease_dir(root))
    reading = read_occupancy(lease.get("transcript"), cfg.window) if lease else None
    print(
        json.dumps(
            {
                "config": cfg.__dict__,
                "lease": lease,
                "occupancy": reading.as_dict() if reading else None,
            },
            indent=2,
        )
    )
    return 0


def _parser():
    parser = argparse.ArgumentParser(description="The coordinator context guard.")
    parser.add_argument(
        "--root", default=None, help="repo root (default: CLAUDE_PROJECT_DIR, else .)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("hook", help="one Claude Code hook call (JSON on stdin)")
    sub.add_parser("status", help="print the lease and the holder's occupancy")
    p = sub.add_parser("take", help="take a free lease for this session")
    p.add_argument("--session", default=None)
    p.add_argument("--transcript", default=None)
    for name in ("release", "clear"):
        p = sub.add_parser(name, help="the owner's {} (recorded)".format(name))
        p.add_argument("--reason", required=True)
    p = sub.add_parser("request-relaunch", help="request the relaunch from a handoff")
    p.add_argument("--handoff", required=True)
    p.add_argument("--session", default=None)
    p = sub.add_parser("handback", help="the holder hands the lease back at close-out")
    p.add_argument("--handoff", required=True)
    p.add_argument("--session", default=None)
    p = sub.add_parser("exec-claude", help=argparse.SUPPRESS)
    p.add_argument("--prompt-file", required=True)
    sub.add_parser(
        "window-check",
        help="exit 1 inside the blackout window (a coordinator launch script's check)",
    )
    p = sub.add_parser(
        "hooks", help="report, or switch on, the coordinator's Claude Code hooks"
    )
    p.add_argument("--example", required=True, help="the inert hook config")
    p.add_argument("--enable", action="store_true")
    return parser


def main(argv=None):
    """The guard's command line: dispatch one operation and map a refusal to
    exit 1 with its reason on stderr.

    Implements: SR-230, LLR-301
    """
    args = _parser().parse_args(argv)
    root = Path(args.root or os.environ.get("CLAUDE_PROJECT_DIR") or ".").resolve()
    session = getattr(args, "session", None) or os.environ.get(SESSION_ENV)
    actions = {
        "hook": lambda: _hook_main(root),
        "status": lambda: _status(root),
        "take": lambda: take(root, session, args.transcript),
        "release": lambda: release(root, args.reason),
        "clear": lambda: clear(root, args.reason),
        "request-relaunch": lambda: request_relaunch(root, args.handoff, session),
        "handback": lambda: hand_back(root, args.handoff, session),
        "exec-claude": lambda: exec_claude(args.prompt_file),
        "window-check": lambda: window_check(root),
        "hooks": lambda: _hooks_main(root, args.example, args.enable),
    }
    result = actions[args.cmd]()
    if isinstance(result, str):
        print("coordinator guard: " + result, file=sys.stderr)
        return 1
    return result or 0


if __name__ == "__main__":
    sys.exit(main())
