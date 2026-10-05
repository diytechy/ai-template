#!/usr/bin/env python3
"""The coordinator context guard: stop new lanes at a context threshold, close
out, hand off, and relaunch at session end (WI-822; docs/specs/WI-822.md).

An interactive Claude Code coordinator session grows its context over many
lanes, and compaction then degrades it. This module is the whole guard:

- **the occupancy reader** (`read_occupancy`): the newest valid assistant
  `usage` after the transcript's last compaction boundary, on the live branch,
  read from the transcript's TAIL only (transcripts reach tens of MB);
- **the lease** (`take`, `release`, `clear`): one record naming the one
  coordinator session, under the primary checkout's untracked
  `out/coordinator/`. It passes in exactly two ways: to the relaunched
  successor at its `SessionStart`, or by the owner's recorded release. Time
  never transfers it;
- **the drain latch** (`latch_reading`): the first reading at or above the
  declared threshold latches drain mode in the lease, and only the successor's
  take or the owner's recorded clear unlatches it;
- **the admission boundary** (`claim_refusal`): the work-item claim calls it on
  every route except the live dispatcher's;
- **the hook entry point** (`hook`): one CLI dispatching on the event name the
  hook input carries;
- **the relaunch** (`request_relaunch`, `session_end`, `launch_detached`): a
  request written atomically, acquired by rename at the holder's exit, and
  launched detached through the repo's launcher in the declared repo root.

SHIPPED OFF. At `[coordinator] context_guard_pct = 0` every entry point returns
before reading or writing anything: claims behave exactly as without the guard
and the hooks print nothing.

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

Contract IF-271: `claim_refusal(root, env=None)` returns None when a guarded
    claim may proceed, and always while `[coordinator] context_guard_pct` is
    0; otherwise it returns the refusal text, naming the reason. The caller's
    session is read from `CLAUDE_CODE_SESSION_ID` in `env` (default the
    process environment). The live dispatcher's claim does not call it.

Contract IF-274: the hook's stdin is one JSON object carrying
    `hook_event_name`, `session_id` and `transcript_path`, with `agent_id`,
    `reason` and `trigger` where the event provides them. Stdin that does not
    parse is reported on stderr and answered with nothing; the exit is 0.

Contract IF-275: a hook response is one line of JSON on stdout,
    `hookSpecificOutput` with `hookEventName` and `additionalContext`, printed
    only when the guard has context to add; otherwise nothing is printed. The
    hook never refuses a tool call and always exits 0.

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
    `release --reason R`, `clear --reason R` or
    `request-relaunch --handoff H [--session S]`.

Contract IF-281: the command line's exit code is 0 on success and 1 on a
    refusal, whose reason goes to stderr after "coordinator guard: "; a
    usage error exits 2; `hook` always exits 0.

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
import secrets
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

try:
    import agent_common
    import session_keep
    from kitlib.observation import write_atomic
except ImportError:  # pragma: no cover - in-process import from elsewhere
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import agent_common
    import session_keep
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
GUARD = "python project-trajectory/scripts/coordinator_guard.py"

INSTRUCTION = (
    "COORDINATOR CONTEXT GUARD: this session's context reached {pct:.1f}% of its "
    "declared window (threshold {threshold}%), and drain mode is latched. "
    "Work-item claims now refuse. Close out now, following the session-protocol "
    "skill's coordinator close-out: (1) start no new claims or lanes; (2) bring "
    "every in-flight row to a safe point: land it, close it, or leave it "
    "committed on its lane and recorded; (3) write docs/status.md, a handoff "
    "with its session prompt, and a log fragment; (4) request the relaunch: "
    "`" + GUARD + " request-relaunch --handoff <path>`, then end the session. "
    "The next session starts from the handoff when this one exits."
)
REMINDER = (
    "COORDINATOR CONTEXT GUARD reminder: drain mode is latched ({pct:.1f}%). No new "
    "claims; finish the close-out and request the relaunch."
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
    """Append one event to `events.jsonl`: every take, release, clear, latch,
    compaction, refused request and launch is recorded there.

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
                    _holder_line(lease), GUARD + ' release --reason "<why>"'
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


def claim_refusal(root, env=None):
    """The admission boundary the work-item claim calls on every route but the
    live dispatcher's: None when the claim may proceed, else the refusal.
    Refuses when no lease is held, when the caller's session is not the
    holder, and when drain mode is latched, reading the holder's transcript
    itself first so admission never depends on a hook having run.

    Implements: SR-229, LLR-300
    """
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
            "the coordinator session: {} take".format(GUARD)
        )
    if session_id != lease["holder"]:
        return (
            "coordinator guard: the coordinator lease is held by {}, not by "
            "this caller (session {}); only the coordinator claims. The owner "
            'releases a lease whose session has ended: {} release --reason "<why>"'
        ).format(_holder_line(lease), session_id or "unknown", GUARD)
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
            return _context(
                event, INSTRUCTION.format(pct=reading.pct, threshold=cfg.threshold)
            )
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
                INSTRUCTION.format(
                    pct=lease.get("latched_pct"), threshold=cfg.threshold
                ),
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
    guard is off.

    Implements: SR-229, LLR-300
    """
    cfg = guard_config(root)
    if not cfg.enabled or not isinstance(payload, dict):
        return None
    env = os.environ if env is None else env
    event = payload.get("hook_event_name")
    if event in MONITORED:
        return on_monitored(root, cfg, payload)
    if event == "SessionStart":
        return on_session_start(root, cfg, payload, env)
    if event == "PreCompact":
        return on_pre_compact(root, cfg, payload)
    if event == "SessionEnd":
        session_end(root, payload, launch=launch)
    return None


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


def request_relaunch(root, handoff, session_id):
    """Write the relaunch request for the holder: its session id, the repo
    root, the handoff and the creation time, atomically. Returns None, or the
    refusal.

    Implements: SR-230, LLR-301
    """
    handoff = Path(handoff).resolve()
    if not session_prompt(handoff):
        return "{} carries no session prompt (a fenced block under a 'Session prompt' heading)".format(
            handoff
        )
    with session_keep.dir_lock(lease_dir(root)) as directory:
        lease = _load(directory)
        if not session_id or lease.get("holder") != session_id:
            return "only the lease holder requests the relaunch (holder: {}, caller: {})".format(
                lease.get("holder"), session_id
            )
        request = {
            "session_id": session_id,
            "repo_root": lease.get("repo_root") or str(Path(root).resolve()),
            "handoff": str(handoff),
            "created": _now(),
        }
        write_atomic(_request_path(directory), json.dumps(request, indent=2) + "\n")
        record_event(directory, "relaunch-requested", **request)
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
    p = sub.add_parser("exec-claude", help=argparse.SUPPRESS)
    p.add_argument("--prompt-file", required=True)
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
        "exec-claude": lambda: exec_claude(args.prompt_file),
    }
    result = actions[args.cmd]()
    if isinstance(result, str):
        print("coordinator guard: " + result, file=sys.stderr)
        return 1
    return result or 0


if __name__ == "__main__":
    sys.exit(main())
