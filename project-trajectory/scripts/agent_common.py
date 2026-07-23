#!/usr/bin/env python3
"""Shared coordinator primitives, extracted VERBATIM from agent_loop.py
(WI-218 slice C — a file split, not a rewrite; behaviors and WI history
unchanged). The worker loop (agent_loop) and the parallel dispatcher/
integrator (agent_dispatch) both stand on this layer:

  - the typed exit codes + `END_STATES`;
  - `git`/`head_sha`/`head_sha_full` and the dirty-tree family (owner-only
    scratchpad exemption, WI-203);
  - the declared-surface reads — `read_declared`, `pause_reason`, the WI-148
    blackout window — and the stop banner + Current State excerpt;
  - the per-worktree coordinator lock (kernel advisory lock; the held
    descriptor lives HERE, in this module's `_LOCK_FD`, so every caller
    shares one lock namespace);
  - worker-assignment primitives (`WI_TOKEN_RE`, `TRAIN_BRANCH_PREFIX`,
    `sanitize_train`, `parse_wi_list`, `load_wi_registry`, `train_evidence`)
    and the small CSV/ref readers;
  - `parse_map`, `preflight` (launchability refusal, SR-027), and the
    session-log family (size-bounded logs, the regenerated iteration index,
    the telemetry commit) + the generated run-state write.

agent_loop re-exports the names it historically exposed, so its public
surface is unchanged. Stdlib only, Python 3.11+, Windows/POSIX.

Contracts: IF-037, IF-065 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import csv
import datetime
import errno
import os
import re
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

# Sibling scripts (the WI-218 split): preflight validates the AGENT_CMD
# template through the headless session layer. The guard covers an in-process
# import (a test) whose sys.path doesn't yet carry scripts/ — the same
# sanctioned-sibling-import idiom agent_loop uses.
try:
    from agent_session import build_argv
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from agent_session import build_argv
# Size bounds for the tracked per-session log (the Q13d "size-bounded" cap):
# the head shows how the session started, the capped tail how it ended — the
# part that explains the outcome. The raw unbounded stream goes to the
# gitignored out/run-logs/ for local debugging.
LOG_HEAD_LINES = 60


LOG_TAIL_LINES = 400


LOG_MAX_BYTES = 65536


# The end states docs/run-state may carry (one word, tracked like docs/gate;
# anything else — including the file being absent — reads RUNNING). The file
# is dispatcher-GENERATED (spec §10; the serial driver that used to read it
# back is retired, WI-210). NEEDS-HUMAN may carry one `ask: <one-line ask>`
# line after the state word — the concrete human act the stop banner
# headlines (WI-127). Every state reader takes only the first declared line,
# so the extra line is invisible to them.
END_STATES = ("DONE", "BLOCKED", "NEEDS-HUMAN")


EXIT_DONE = 0


EXIT_PREFLIGHT = 2


EXIT_BLOCKED = 3


EXIT_STALL = 4


EXIT_WAITING = 5


EXIT_BUDGET = 6


EXIT_NEEDS_HUMAN = 7


EXIT_PAUSED = 8


# A worker whose §7 continuation re-check refuses the next constituent ends
# its train EARLY (WI-183, SR-062): built/blocked evidence stands, and the
# dispatcher transactionally releases the unstarted constituents' reservations.
EXIT_TRAIN_END = 10


# The FB3 owner-only path(s): OWNER_SCRATCHPAD.md is free-form owner notes the
# human edits continuously (check_docs.py drops it from doc discovery the same
# way — check_docs.SCRATCHPAD). Because it is tracked and perpetually edited, an
# owner-only-dirty tree is NOT interrupted-session residue: it must not fire the
# WI-076 resume note or flip the done detection (WI-203). Mirrored, not imported
# — importing the doc-checker into the coordinator would add a CMP-004→CMP-001
# edge + an IF seam for one fixed filename; the name is a bootstrap contract
# (test_bootstrap asserts the scaffold ships it), so the mirror cannot drift.
OWNER_ONLY_PATHS = ("OWNER_SCRATCHPAD.md",)


def read_declared(path, default):
    """Read a one-word declared-policy file (docs/gate, docs/run-state, …):
    the first non-empty, non-comment line — the same rule the git hooks and
    check_privacy.py apply — or `default` when absent/empty."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return default
    for ln in lines:
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            return ln
    return default


# The coordinator dials that live once in docs/stack.ini [agent-loop] instead of
# being duplicated across the agent-resume.{cmd,sh,command} launchers (IF-068,
# WI-274 part B). Each maps a stack.ini key to the AGENT_* env slot it now backs.
AGENT_LOOP_DIALS = ("jobs", "model", "model-map")


def read_agent_loop_config(docs):
    """The declared coordinator dials — the ``[agent-loop]`` section of
    ``docs/stack.ini`` (IF-068, WI-274). Returns a dict of the present dial keys
    (``jobs`` / ``model`` / ``model-map``) with surrounding whitespace stripped;
    an empty value, absent key/section/file, or an unreadable/malformed stack.ini
    all yield ``{}`` for that key (fail-soft — the AGENT_* env slots and the
    built-in defaults still apply, so a repo without the section behaves exactly
    as before, never-breaking).

    This is the DECLARED-FILE tier of the coordinator-dial precedence
    ``CLI flag > AGENT_* env > declared file > built-in default`` that
    ``agent_loop.main`` applies (so a one-dial owner change edits ONE file, not
    the same value in three launchers)."""
    import configparser

    cp = configparser.ConfigParser(interpolation=None)
    try:
        # An absent file -> cp.read returns [] (no exception); a present but
        # malformed/non-UTF-8 file degrades to {} rather than crashing the loop.
        if not cp.read(str(Path(docs) / "stack.ini"), encoding="utf-8"):
            return {}
    except (configparser.Error, OSError, ValueError, UnicodeDecodeError):
        return {}
    if not cp.has_section("agent-loop"):
        return {}
    out = {}
    for key in AGENT_LOOP_DIALS:
        if cp.has_option("agent-loop", key):
            val = cp.get("agent-loop", key).strip()
            if val:
                out[key] = val
    return out


def resolve_coordinator_dials(args, docs):
    """``(model, model_map, jobs_opt)`` for the coordinator, each resolved by the
    IF-068 precedence ``CLI flag > AGENT_* env > declared file > built-in
    default`` (WI-274 part B). ``args.model``/``args.model_map``/``args.jobs`` are
    ``None`` when their flag was not passed; an empty env or declared value falls
    through (the launchers' "empty slot = default" convention, so the env path
    keeps working unchanged). ``jobs_opt`` is ``None`` when nothing set it — the
    caller then applies the §6 two-worker default. Kept OUT of ``agent_loop.main``
    so that hot function's complexity does not grow (the ratchet's escape hatch)."""
    dials = read_agent_loop_config(docs)
    model = (
        args.model
        if args.model is not None
        else (os.environ.get("AGENT_MODEL") or dials.get("model", ""))
    )
    model_map = (
        args.model_map
        if args.model_map is not None
        else (os.environ.get("AGENT_MODEL_MAP") or dials.get("model-map", ""))
    )
    jobs_opt = (
        args.jobs
        if args.jobs is not None
        else (os.environ.get("AGENT_JOBS", "").strip() or dials.get("jobs", "") or None)
    )
    return model, model_map, jobs_opt


def pause_reason(lane):
    """A declared **graceful-pause** request (WI-147): the `docs/pause` file
    present = pause the loop at the next session boundary. Returns the free-form
    reason (the file's first non-comment line, `""` when it carries none) or
    `None` when the file is absent. The file is the whole contract — presence
    pauses, deleting it resumes — so `run-state` is deliberately left untouched
    (a resume is one act: delete the file and re-launch). Per-lane like
    run-state, so a track pauses only its own coordinator."""
    path = lane / "pause"
    if not path.is_file():
        return None
    return read_declared(path, "")


# --- WI-148: weekday blackout window ------------------------------------------
# A declared `docs/blackout` policy: first non-comment line `HH:MM-HH:MM` (UTC),
# active Mon–Fri. Inside the window the coordinator starts no new session (the
# in-flight one already wrapped, the same graceful semantic as docs/pause) — it
# waits out the window, then resumes automatically, so a single walk-away launch
# survives the blackout. An absent/empty/malformed file, or `start == end`,
# disables it (byte-identical to a repo that never had the file — never-breaking);
# a fresh scaffold ships the 12:00–19:00 default so the owner's "always on"
# blackout is honored by the scaffold, not a hidden built-in.
BLACKOUT_RE = re.compile(r"^\s*(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})\s*$")


def parse_blackout(line):
    """Parse a `HH:MM-HH:MM` blackout line into `(start_min, end_min)` — minutes
    past UTC midnight — or `None` when absent/empty/malformed (an out-of-range
    hour or minute is malformed). Deliberately does NOT apply the `start == end`
    disable rule; the caller (blackout_wake) does, so the parse and the policy
    stay separately testable."""
    m = BLACKOUT_RE.match(line or "")
    if not m:
        return None
    sh, sm, eh, em = (int(g) for g in m.groups())
    if sh > 23 or eh > 23 or sm > 59 or em > 59:
        return None
    return (sh * 60 + sm, eh * 60 + em)


def blackout_wake(line, now):
    """Seconds until the current UTC weekday blackout window ends, or `None` when
    a new session is NOT blacked out at `now` — the file is absent/empty/
    malformed, the window is disabled (`start == end`), it is the weekend (the
    window is Mon–Fri only), or `now` falls outside the window. The window is
    half-open `[start, end)`: a session starting exactly at `end` is already
    clear (so 12:00–19:00 blocks 12:00 through 18:59 and releases at 19:00). A
    window whose start is after its end wraps past UTC midnight, honored on its
    start weekday. `now` is a naive UTC datetime (datetime.utcnow())."""
    win = parse_blackout(line)
    if win is None:
        return None
    start, end = win
    if start == end:
        return None  # the disable form
    if now.weekday() >= 5:  # Sat/Sun — the window is weekdays only
        return None
    minute = now.hour * 60 + now.minute
    inside = start <= minute < end if start < end else (minute >= start or minute < end)
    if not inside:
        return None
    wake = now.replace(hour=end // 60, minute=end % 60, second=0, microsecond=0)
    if wake <= now:  # a wrap window's end is tomorrow morning
        wake += datetime.timedelta(days=1)
    return int((wake - now).total_seconds())


# --- WI-261: blackout pause feedback (banner + countdown heartbeat) --------------
# The window SEMANTICS live in blackout_wake above; these render the WAIT so a
# walk-away launch reads as deliberately paused, not hung. All three are pure /
# injectable so the terminal feedback is testable without a real multi-second
# sleep. The scaffold's default cadence between countdown heartbeats (seconds).
BLACKOUT_HEARTBEAT_SEC = 300


def _fmt_hms(seconds):
    """Whole seconds as a compact `Hh Mm Ss`, dropping leading zero units but
    always keeping seconds: 25200 -> '7h 0m 0s', 90 -> '1m 30s', 45 -> '45s'."""
    seconds = int(seconds)
    hours, rem = divmod(seconds, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return "{}h {}m {}s".format(hours, minutes, secs)
    if minutes:
        return "{}m {}s".format(minutes, secs)
    return "{}s".format(secs)


def blackout_banner(window, resume_at, wake_seconds, policy_file="docs/blackout"):
    """The multi-line terminal banner shown when the coordinator holds a NEW
    session for the declared blackout window (WI-261). Pure: names the policy
    file, the raw `HH:MM-HH:MM` UTC `window`, its weekday-only scope, the resume
    time (`resume_at`, a naive UTC datetime), and how long the wait is
    (`wake_seconds`), so an unattended launch reads as deliberately WAITING, not
    hung. Returns the banner as one string (no trailing newline)."""
    bar = "=" * 70
    return "\n".join(
        [
            bar,
            "agent_loop: BLACKOUT — holding; no new session starts yet.",
            "  policy file : {}".format(policy_file),
            "  window      : {} UTC  (weekday-only, Mon–Fri; weekends run)".format(
                (window or "").strip()
            ),
            "  resuming at : {} UTC  (in ~{})".format(
                resume_at.strftime("%H:%M"), _fmt_hms(wake_seconds)
            ),
            "  honored by  : the agent-resume -> agent_loop path (waits in place)",
            "The loop is WAITING, not hung; it resumes automatically.",
            bar,
        ]
    )


def blackout_countdown_line(remaining_seconds, resume_at):
    """One countdown-heartbeat line emitted every BLACKOUT_HEARTBEAT_SEC while
    waiting out a blackout, so an unattended launch visibly ticks down rather
    than looking hung (WI-261). Pure: names the remaining wait and the UTC resume
    time (`resume_at`, a naive UTC datetime)."""
    return "agent_loop: blackout — ~{} remaining, resuming {} UTC.".format(
        _fmt_hms(remaining_seconds), resume_at.strftime("%H:%M")
    )


def blackout_wait(
    wake_seconds, window, resume_at, emit, sleep, interval=BLACKOUT_HEARTBEAT_SEC
):
    """Emit the blackout banner, then wait `wake_seconds` in `interval`-second
    steps, emitting a countdown heartbeat after each step (never a redundant one
    at zero, where the loop resumes). `emit(line)` prints a line and
    `sleep(secs)` waits — both injected so the feedback is deterministic under
    test with a captured `emit` and a no-op `sleep` (no real multi-second delay).
    The WAIT itself is unchanged: the total time slept is exactly `wake_seconds`
    (an interval <= 0 degenerates to a single full-length sleep, never a spin)."""
    emit(blackout_banner(window, resume_at, wake_seconds))
    remaining = int(wake_seconds)
    while remaining > 0:
        step = interval if 0 < interval < remaining else remaining
        sleep(step)
        remaining -= step
        if remaining > 0:
            emit(blackout_countdown_line(remaining, resume_at))


# --- WI-181: explicit worker assignment (SR-060) --------------------------------
# A worker is one agent_loop process driving one dispatcher-assigned traincar on
# one llm/train/<id> branch in one worktree. Its inputs are explicit CLI
# arguments (never a lane file) and its result is committed evidence read back
# through git trailers — the durable channel recovery reconstructs from (spec
# §6/§11).

# The branch namespace a train builds on. The dispatcher (Slice D) creates these.
TRAIN_BRANCH_PREFIX = "llm/train/"


WI_TOKEN_RE = re.compile(r"^WI-\d+$")

# The terminal work-item Statuses — no further build is owed (WI-267). Mirrors
# check_trajectory.TERMINAL_STATUSES, kept inline here rather than imported: the
# F5 self-contained-script rule keeps agent_common stdlib-only (it never pulls a
# sibling engine). A worker must never build a WI in either state.
TERMINAL_STATUSES = ("done", "retired")


def sanitize_train(name):
    """A train id becomes a branch segment, a log-file prefix, and a reviews/
    subdirectory, so restrict it to a safe slug (alnum + `.`/`-`/`_`, starts
    alphanumeric) — `--train` can then never traverse the tree. Returns the
    name or raises ValueError (preflight surfaces the message)."""
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name or ""):
        raise ValueError(
            "train id {!r} must be a slug matching [A-Za-z0-9][A-Za-z0-9._-]* "
            "(starts alphanumeric; no path separators)".format(name)
        )
    return name


def parse_wi_list(spec):
    """The ordered assigned-WI list from a `;`/`,`/whitespace-joined --wi value.
    Raises ValueError on an empty list, a malformed token, or a duplicate —
    a broken assignment must fail preflight, never half-run."""
    out = []
    for tok in re.split(r"[;,\s]+", (spec or "").strip()):
        if not tok:
            continue
        if not WI_TOKEN_RE.match(tok):
            raise ValueError(
                "--wi token {!r} is not a WI-### id (got --wi {!r})".format(tok, spec)
            )
        if tok in out:
            raise ValueError("--wi names {} twice".format(tok))
        out.append(tok)
    if not out:
        raise ValueError("--wi carries no WI-### id (got {!r})".format(spec))
    return out


def load_wi_registry(root):
    """{WI-ID: raw row dict} from the worktree's tracked WI registry — the
    checked-out copy on the train branch, so a worker reads the same registry
    state its base commit fixed. Malformed/duplicate ids are skipped (the
    validator's finding, not the worker's crash)."""
    rows = _read_csv_rows(root / "docs" / "requirements" / "work-items.csv")
    out = {}
    for r in rows:
        wid = (r.get("WI-ID") or "").strip()
        if WI_TOKEN_RE.match(wid) and wid not in out:
            out[wid] = r
    return out


# The trailer-evidence log format (shared by the worker- and dispatcher-side
# readers). The leading "T" sentinel keeps the first field intact through
# git()'s stdout .strip() — a commit whose WI field is empty would otherwise
# lose its leading tab and shift every field left.
TRAILER_EVIDENCE_FMT = (
    "T%x09"
    "%(trailers:key=WI,valueonly,separator=;)%x09"
    "%(trailers:key=Blocked-WI,valueonly,separator=;)%x09"
    "%(trailers:key=BlockRef,valueonly,separator=;)"
)


def latest_trailer_evidence(log_out):
    """Fold a newest-first trailer log (TRAILER_EVIDENCE_FMT) into
    (built:set, blocked:map) where each WI is claimed by its LATEST trailer
    ONLY — the two buckets are disjoint. A newer `WI:` completion supersedes an
    older `Blocked-WI:` for the same id (a CURED blocker), and a newer
    `Blocked-WI:` supersedes an older `WI:` (the block is newer truth). `git
    log` emits newest-first, so the FIRST commit that names a WI (in either
    trailer) fixes its verdict; within one commit a completion wins. `blocked`
    maps a still-blocked WI to its committed BlockRef ('' when omitted)."""
    built, blocked, seen = set(), {}, set()
    for line in log_out.splitlines():
        parts = (line.split("\t")[1:] + ["", "", ""])[:3]
        for tok in (x.strip() for x in parts[0].split(";")):
            if WI_TOKEN_RE.match(tok) and tok not in seen:
                seen.add(tok)
                built.add(tok)
        refs = [t.strip() for t in parts[2].split(";")]
        for j, tok in enumerate(t.strip() for t in parts[1].split(";")):
            if WI_TOKEN_RE.match(tok) and tok not in seen:
                seen.add(tok)
                blocked[tok] = refs[j] if j < len(refs) else ""
    return built, blocked


def train_evidence(root, base):
    """(built, blocked) read from the train branch's committed trailers in
    base..HEAD: `built` is the set of WI ids whose LATEST trailer is the `WI:`
    completion; `blocked` maps a still-blocked `Blocked-WI:` id to its
    `BlockRef:` value (empty string when the commit omitted one). Per WI the
    newest trailer wins, so a resumed worker whose gate now passes supersedes
    its own earlier block by committing `WI:` (WI-239). This is the worker's
    one result channel — recovery reconstructs the same facts from git alone."""
    code, out = git(
        root, "log", "--format=" + TRAILER_EVIDENCE_FMT, "{}..HEAD".format(base)
    )
    if code != 0:
        return set(), {}
    return latest_trailer_evidence(out)


def _clip(text, limit):
    """Bound a prompt block: head lines up to `limit`, with an elision marker."""
    lines = (text or "").splitlines()
    if len(lines) <= limit:
        return "\n".join(lines)
    return "\n".join(lines[:limit] + ["… ({} more lines)".format(len(lines) - limit)])


# The per-worktree coordinator lock is a kernel ADVISORY lock (fcntl.flock on
# POSIX, msvcrt.locking on Windows) held on out/agent-loop.lock for this
# process's lifetime. The OS releases it automatically when the process exits —
# INCLUDING a crash or SIGKILL — so there is no stale-pid file to reason about
# and no PID-reuse hazard: the freed lock is simply available to the next run.
# The pid/host/stamp written into the file are human-readable DIAGNOSTICS only,
# never the liveness signal. The held descriptor lives in a module global so it
# (and thus the lock) stays open until release_lock / process exit.
_LOCK_FD = None


def _host():
    """This machine's name, for the lock file's human-readable diagnostics."""
    try:
        return socket.gethostname()
    except OSError:
        return ""


# On Windows the CRT lock is MANDATORY — it blocks other processes from reading
# the locked bytes — so we lock a single byte far beyond any real content. The
# human-readable diagnostics in bytes 0..N stay readable (e.g. git staging this
# file if a repo forgot to gitignore out/), while two coordinators still contend
# on the same byte range. POSIX flock is advisory and whole-descriptor, so it
# needs no offset games.
_WIN_LOCK_OFFSET = 1 << 40


def _take_os_lock(fd):
    """Take a non-blocking exclusive advisory lock on `fd`, raising OSError when
    another process already holds it. Platform-split, stdlib only."""
    if os.name == "nt":
        import msvcrt

        os.lseek(fd, _WIN_LOCK_OFFSET, os.SEEK_SET)
        try:
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        finally:
            os.lseek(fd, 0, os.SEEK_SET)
    else:
        import fcntl

        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)


# Errnos that mean "this filesystem cannot do advisory locks" (a network / exotic
# mount — flock returns these) as opposed to "the lock is held" (EWOULDBLOCK /
# EAGAIN / EACCES). On these we degrade to a warning instead of failing closed;
# every other error stays a refusal, so an unknown failure never silently drops
# the guard (fail-safe). Built via getattr so a name absent on a platform is just
# skipped.
_UNSUPPORTED_LOCK_ERRNOS = frozenset(
    getattr(errno, name)
    for name in ("ENOLCK", "ENOSYS", "EOPNOTSUPP", "ENOTSUP")
    if hasattr(errno, name)
)


def _read_holder(lock_path):
    """The holder's diagnostic line (pid host stamp) for an error message, or ''
    — best-effort; a mandatory Windows lock may block the read, which is fine."""
    try:
        return lock_path.read_text(encoding="utf-8").strip().replace("\n", " ")
    except OSError:
        return ""


def acquire_lock(lock_path):
    """Take the per-worktree coordinator lock, or return an error string.

    Prevents two coordinators grinding the same checkout — a double-launch or a
    cron overlap — the one collision the branch guard can't catch (both would
    sit on the same llm/<track> branch in one worktree). The lock is a kernel
    advisory lock the OS grants atomically and releases on exit *or crash*, so a
    dead run never wedges the next one (no pid reasoning, no timer). Cross-host
    on a shared filesystem is best-effort only: flock over NFS is unreliable, so
    this guards one checkout on one host — the common and important case. A
    filesystem that cannot lock at all (ENOLCK/ENOTSUP) degrades to a warning and
    runs unguarded rather than fail-closed on a legitimate run."""
    global _LOCK_FD
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_RDWR | os.O_CREAT
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY  # keep the diagnostic newlines untranslated on Windows
    fd = os.open(str(lock_path), flags, 0o644)
    try:
        _take_os_lock(fd)
    except OSError as exc:
        if os.name != "nt" and exc.errno in _UNSUPPORTED_LOCK_ERRNOS:
            # This filesystem cannot do advisory locks (a network / exotic mount).
            # Degrade to a warning and proceed WITHOUT the guard rather than block
            # a legitimate run: the single-checkout guarantee is only lost on a
            # mount that never supported it, and the branch guard + git history
            # still backstop. Keep fd open (diagnostics written below) so the file
            # still records who is here.
            print(
                "agent_loop: WARNING - {} is on a filesystem that does not "
                "support advisory locks (errno {}); running WITHOUT the "
                "one-coordinator-per-checkout guard.".format(lock_path, exc.errno),
                file=sys.stderr,
            )
        else:
            os.close(fd)
            return (
                "another coordinator holds {} — refusing to run two in one "
                "worktree (held by: {}). It clears itself when that run exits; "
                "wait for it, or delete the file only if you are sure that run "
                "is gone.".format(lock_path, _read_holder(lock_path) or "unknown")
            )
    # We hold the lock: overwrite the diagnostics (a crashed predecessor may have
    # left its own). Best-effort — the OS lock, not this content, is the guard.
    try:
        os.ftruncate(fd, 0)
        os.write(
            fd,
            "{}\n{}\n{}\n".format(
                os.getpid(), _host(), time.strftime("%Y-%m-%d %H:%M:%S")
            ).encode("utf-8"),
        )
    except OSError:
        pass
    _LOCK_FD = fd
    return None


def release_lock(lock_path=None):
    """Drop the coordinator lock: closing the descriptor releases the OS lock.
    Idempotent, and a no-op if we never held it; the OS would release on exit
    regardless (the crash path relies on exactly that). `lock_path` is accepted
    for the atexit call signature but unused — the held descriptor is the
    authority, so a reclaimed-then-exited predecessor never disturbs a successor."""
    global _LOCK_FD
    if _LOCK_FD is not None:
        try:
            os.close(_LOCK_FD)
        except OSError:
            pass
        _LOCK_FD = None


def parse_map(spec):
    """Parse a KEY=value phase map — shared by --model-map/--cmd-map/--prompt-map/
    --tier-map/--prefer-map: "P0=model-a,G3=model-b" -> {"P0": "model-a",
    "G3": "model-b"}."""
    mapping = {}
    for pair in (spec or "").replace(";", ",").split(","):
        pair = pair.strip()
        if not pair:
            continue
        if "=" not in pair:
            raise ValueError("--model-map entry without '=': {}".format(pair))
        phase, _, model = pair.partition("=")
        mapping[phase.strip()] = model.strip()
    return mapping


_SPLIT_RE = re.compile(r"[;,\s]+")


def _read_csv_rows(path):
    """CSV rows of `path` as dicts, or [] (absent/unreadable). utf-8-sig so an
    Excel-written BOM can't rename the first header key (a BOM'd
    work-items.csv split the dispatcher's and the worker's view of the same
    registry, and a BOM'd system-requirements.csv silently vacated the
    critique gate — repo-review 2026-07-21 M-23); errors=replace so a stray
    byte degrades, never crashes (the declared-reader idiom). A real file
    handle (newline="") also keeps quoted multi-line cells parseable, unlike
    the old splitlines() feed."""
    try:
        with Path(path).open(newline="", encoding="utf-8-sig", errors="replace") as fh:
            return list(csv.DictReader(fh))
    except OSError:
        return []


def _refs(cell):
    return [t for t in _SPLIT_RE.split((cell or "").strip()) if t]


def git(root, *args):
    """Run git in the repo; returns (returncode, text).

    On success `text` is stdout-stripped and byte-identical to the raw call —
    every success-path caller parses stdout (`rev-parse`, `status --porcelain`,
    trailer reads). But git reports hook rejections and fatal errors on STDERR,
    so on a NONZERO exit the stripped stderr is appended to stdout (newline-joined
    when both are non-empty); otherwise every failure detail a failed call feeds
    a park/quarantine reason (via `_failure_tail`) would be blank (WI-233)."""
    proc = subprocess.run(
        ["git", "-C", str(root)] + list(args),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,
    )
    out = (proc.stdout or "").strip()
    if proc.returncode != 0:
        err = (proc.stderr or "").strip()
        if err:
            out = out + "\n" + err if out else err
    return proc.returncode, out


# WI-240: the harness/hook banner shape a structured failure prints — a
# `=== <step> : <cmd> ===` banner per step, then that step's output, then a
# `  {STATUS}  <step>  <detail>` line (check.py --run-steps / the check summary).
_FAILTAIL_FAIL_RE = re.compile(r"^\s*FAIL\s")
_FAILTAIL_BANNER_RE = re.compile(r"^\s*=== ")


def _failure_tail(out, budget=600):
    """The FAILING part of a harness/git output, bounded to `budget` chars.

    Park/quarantine/journal details once kept only the leading 200 chars — the
    HEAD — so a multi-step hook failure journaled the FIRST (passing) banner and
    cut the actual error (the WI-229 blocked-disposition loop: three runs of
    `disposition commit failed: === derived-gate : ...python.exe ...` while the
    real `check_trajectory: ERROR - blocked-ref ...` / `  FAIL  trajectory` was
    off the end). This prefers the LAST `  FAIL  <step>` block — that step's
    `=== <step> :` banner through its FAIL line — else the TAIL of the output;
    always tail-bounded, so the error survives even when the banner is long."""
    text = (out or "").rstrip()
    if not text:
        return ""
    lines = text.splitlines()
    fail_idx = None
    for i, line in enumerate(lines):
        if _FAILTAIL_FAIL_RE.match(line):
            fail_idx = i
    if fail_idx is None:
        return text[-budget:].lstrip()
    start = 0
    for j in range(fail_idx - 1, -1, -1):
        if _FAILTAIL_BANNER_RE.match(lines[j]):
            start = j
            break
    block = "\n".join(lines[start : fail_idx + 1])
    return block[-budget:].lstrip()


def head_sha(root):
    """Short HEAD sha, or None on a zero-commit repo (guarded rev-parse)."""
    code, out = git(root, "rev-parse", "--short", "HEAD")
    return out if code == 0 and out else None


def working_tree_dirty(root):
    """The `git status --porcelain` lines — one per uncommitted path (a rename is
    a single 'R  old -> new' entry, an untracked file a single '?? path' entry),
    or [] on a clean tree or a non-repo. Read through git() (text,
    errors=replace) so an odd byte in a path degrades rather than crashes (the
    sibling encoding-safe idiom). Used once at loop start to surface
    interrupted-session residue (WI-076)."""
    code, out = git(root, "status", "--porcelain")
    if code != 0:
        return []
    return [ln for ln in out.splitlines() if ln.strip()]


def _porcelain_path(line):
    """The repo-relative path a `git status --porcelain` line names — the
    destination side of a rename/copy (`R  old -> new`), surrounding quotes
    stripped — used to match a dirty line against OWNER_ONLY_PATHS. Splits the
    XY status token off the front rather than assuming a fixed column width (a
    leading blank status column may or may not survive to here)."""
    body = line.strip()
    if " -> " in body:
        return body.split(" -> ", 1)[1].strip().strip('"')
    parts = body.split(None, 1)  # status token, then the path
    return (parts[1] if len(parts) == 2 else body).strip().strip('"')


def substantive_working_tree_dirty(root):
    """`working_tree_dirty` minus the FB3 owner-only paths (OWNER_ONLY_PATHS) —
    the view the loop's WI-076 resume note (loop start) and done detection use,
    so a tree whose ONLY changes are the owner scratchpad (perpetually edited,
    never the loop's or a worker's deliverable) reads clean and the interrupted-
    residue signal fires only on genuine residue. The raw primitive stays
    available for a caller that wants every uncommitted path (WI-203)."""
    return [
        ln
        for ln in working_tree_dirty(root)
        if _porcelain_path(ln) not in OWNER_ONLY_PATHS
    ]


def current_state_excerpt(status_path, max_lines=40):
    """The '## Current State' section of a status.md — the root dispatcher's or
    a track lane's own — the pending asks a stopping coordinator must surface in
    its exit banner."""
    try:
        lines = status_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return "({} not found — no asks to surface)".format(status_path)
    section, collecting = [], False
    for ln in lines:
        if ln.startswith("## "):
            if collecting:
                break
            collecting = ln.strip().lower().startswith("## current state")
            continue
        if collecting:
            section.append(ln)
    if not section:
        return "({} has no '## Current State' section)".format(status_path)
    section = [ln for ln in section if ln.strip()][:max_lines]
    return "\n".join(section)


def bounded_transcript(output):
    """Head + capped tail of a session transcript (the tracked-log bound)."""
    lines = output.splitlines()
    if len(lines) > LOG_HEAD_LINES + LOG_TAIL_LINES:
        elided = len(lines) - LOG_HEAD_LINES - LOG_TAIL_LINES
        lines = (
            lines[:LOG_HEAD_LINES]
            + [
                "",
                "[... {} line(s) elided — full stream in out/run-logs/ ...]".format(
                    elided
                ),
                "",
            ]
            + lines[-LOG_TAIL_LINES:]
        )
    text = "\n".join(lines)
    encoded = text.encode("utf-8", "replace")
    if len(encoded) > LOG_MAX_BYTES:
        keep = LOG_MAX_BYTES // 2
        text = (
            encoded[:keep].decode("utf-8", "ignore")
            + "\n[... byte cap hit — full stream in out/run-logs/ ...]\n"
            + encoded[-keep:].decode("utf-8", "ignore")
        )
    return text


_SECRET_RES = (
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._\-]{25,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
)


def redact_secrets(text):
    """Best-effort redaction of well-known credential shapes, applied before a
    transcript is committed to tracked history (docs/iteration/*.log): a CLI
    auth error echoing a key otherwise lands in permanent history with only
    push-policy between it and publication (repo-review 2026-07-21 M-19).
    Deliberately imperfect — unknown token shapes pass through, and the raw
    unredacted stream stays in gitignored out/run-logs/ for debugging."""
    hits = 0
    for rx in _SECRET_RES:
        text, n = rx.subn("[REDACTED]", text)
        hits += n
    return text, hits


def write_session_log(iter_dir, meta, transcript):
    """Write the tracked, size-bounded per-session log: a `# key: value`
    metadata header (what the index is regenerated from) + the transcript
    (credential shapes redacted — see redact_secrets)."""
    transcript, redacted = redact_secrets(transcript)
    iter_dir.mkdir(parents=True, exist_ok=True)
    header = ["# agent-loop session log — written by scripts/agent_loop.py"]
    for key in (
        "session",
        "date",
        "train",
        "base",
        "phase",
        "wi",
        "model",
        "guardrails",
        "outcome",
        "commits",
        "tokens",
        "cost-usd",
        "wall-secs",
        "api-secs",
        "turns",
        "ttft-secs",
        "cache-read",
        "cache-create",
        "effort",
        "fast",
        "prompt-chars",
        "exit-code",
    ):
        header.append("# {}: {}".format(key, meta.get(key, "")))
    if redacted:
        header.append("# redacted: {} credential-shaped token(s)".format(redacted))
    header.append("# ---")
    # A worker's log name is prefixed with its train id (WI-181): two parallel
    # workers' committed session logs must never collide at integration.
    name = "{}-{}.log".format(meta["session"], meta["stamp"])
    if meta.get("train"):
        name = "{}-{}".format(meta["train"], name)
    path = iter_dir / name
    path.write_text(
        "\n".join(header) + "\n" + bounded_transcript(transcript) + "\n",
        encoding="utf-8",
    )
    return path


def read_log_meta(path):
    """Parse the `# key: value` metadata header of one session log."""
    meta = {}
    try:
        with open(str(path), encoding="utf-8", errors="replace") as fh:
            for _ in range(32):
                line = fh.readline()
                if not line or line.startswith("# ---"):
                    break
                m = re.match(r"#\s*([\w-]+):\s*(.*)", line)
                if m:
                    meta[m.group(1)] = m.group(2).strip()
    except OSError:
        pass
    return meta


def per_turn_pace(meta):
    """API seconds per turn from a log's header meta — the like-for-like speed
    number across sessions of different lengths (a 100-turn build and a
    25-turn review compare honestly here, not on wall time). Empty when either
    field is absent (pre-WI-119 logs, errored sessions)."""
    try:
        api, turns = float(meta.get("api-secs", "")), float(meta.get("turns", ""))
    except ValueError:
        return ""
    return "{:.1f}".format(api / turns) if turns else ""


def per_turn_context(meta):
    """Average context carried per turn (cache-read tokens / turns, humanized
    to k) — the "how much is it re-reading every step" complexity number the
    per-session totals hide. Empty when the fields are absent."""
    try:
        read, turns = float(meta.get("cache-read", "")), float(meta.get("turns", ""))
    except ValueError:
        return ""
    return "{:.0f}k".format(read / turns / 1000.0) if turns else ""


def regenerate_index(docs_dir):
    """Rebuild docs/iteration_index.md from the docs/iteration/*.log metadata
    headers — generated, never hand-maintained (the kit's standing rule), so
    it survives manual log pruning and answers "which session did this"."""
    iter_dir = docs_dir / "iteration"
    rows = []
    for log in sorted(iter_dir.glob("*.log")):
        meta = read_log_meta(log)
        if not meta.get("session"):
            continue
        rows.append(
            "| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} "
            "| [{}](iteration/{}) |".format(
                meta.get("session", ""),
                meta.get("date", ""),
                meta.get("phase", "") or "—",
                meta.get("wi", "") or "—",
                meta.get("model", "") or "—",
                meta.get("outcome", ""),
                meta.get("commits", "") or "—",
                meta.get("tokens", "") or "—",
                meta.get("cost-usd", "") or "—",
                meta.get("wall-secs", "") or "—",
                meta.get("api-secs", "") or "—",
                meta.get("turns", "") or "—",
                per_turn_pace(meta) or "—",
                per_turn_context(meta) or "—",
                log.name,
                log.name,
            )
        )
    text = (
        "# Iteration index\n\n"
        "_Generated by `scripts/agent_loop.py` from the `docs/iteration/*.log`\n"
        "metadata headers — regenerated every session, never hand-edited. The\n"
        "collated human-review record is `log.md`; this index is the quick\n"
        '"which session did this" pointer (process-options.md "Unattended\n'
        'operation")._\n\n'
        "| # | Date | Phase | WI | Model | Outcome | Commits | Tokens | Cost USD "
        "| Wall s | API s | Turns | s/turn | Ctx/turn | Log |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
        + "\n".join(rows)
        + "\n"
    )
    (docs_dir / "iteration_index.md").write_text(text, encoding="utf-8")


def commit_telemetry(root, session, label, paths):
    """Commit the coordinator's own bookkeeping in its own `telemetry:` commit,
    right after it is written — so it never rides the next session's work commit
    or dangles in the tree (WI-137, the session-021 defect-shape). Stages only
    the named bookkeeping paths (the iteration log + regenerated index, the
    review scoreboard); the reviewer's verdict files commit themselves. Honors
    the hooks and is best-effort: nothing staged, or a hook veto, leaves the
    files in the tree exactly as before — never fatal, so the fix can only help
    (a walk-away run that today dangles telemetry keeps working either way)."""
    rels = []
    for p in paths:
        try:
            rels.append(os.path.relpath(str(p), str(root)))
        except ValueError:
            continue  # a path on another drive (Windows) — skip, never crash
    if not rels:
        return
    code, out = git(root, "status", "--porcelain", "--", *rels)
    if code != 0 or not out.strip():
        return  # unchanged bookkeeping — no empty commit
    code, staged = git(root, "diff", "--cached", "--name-only", "--", *rels)
    pre_staged = set(staged.splitlines()) if code == 0 else set()
    git(root, "add", "--", *rels)
    msg = "telemetry: session {} {}".format(session, label)
    code, out = git(root, "commit", "-q", "-m", msg, "--", *rels)
    if code != 0:
        # "Exactly as before" covers the index too: a veto must not leave the
        # bookkeeping staged for the next session's work commit to swallow.
        # Unstage only what this add staged; anything already staged stays.
        fresh = [r for r in rels if r.replace(os.sep, "/") not in pre_staged]
        if fresh:
            git(root, "reset", "-q", "--", *fresh)
        print(
            "agent_loop: telemetry commit skipped (session {}): {}".format(
                session, _failure_tail(out) or "hook veto or nothing staged"
            ),
            file=sys.stderr,
        )


def next_session_number(iter_dir, train=None):
    """Next NNN, continuing across coordinator restarts. A worker's numbering
    is scoped to its train prefix (WI-181) — parallel session numbers cannot
    collide because the (train, session) pair is the aggregation key."""
    pattern = re.compile(r"{}-(\d+)-".format(re.escape(train)) if train else r"(\d+)-")
    highest = 0
    if iter_dir.is_dir():
        for log in iter_dir.glob("*.log"):
            m = pattern.match(log.name)
            if m:
                highest = max(highest, int(m.group(1)))
    return highest + 1


def _iter_dir_list(iter_dirs):
    """Normalize the phase_draw_ordinal argument to a list of Paths — a single
    Path/str (the attended single-dir case) or an already-assembled iterable
    (the cross-train `draw_iter_dirs` list)."""
    if isinstance(iter_dirs, (str, Path)):
        return [Path(iter_dirs)]
    return [Path(d) for d in iter_dirs]


def phase_draw_ordinal(iter_dirs, phase):
    """The 0-based CROSS-TRAIN draw ordinal for `phase` (WI-263, repo-review
    M-31): how many PRIOR sessions — across EVERY train, not just this one —
    already ran this exact phase, counted from the durable session-log
    `# phase:` headers and de-duplicated by log filename across `iter_dirs`.
    This keys the weighted-rotation draw so each phase advances its OWN rotation
    (the global per-train session counter strides — a round is BUILD + REVIEW-A +
    REVIEW-B [+ CRITIQUE] — and would alias against the weight sum, starving
    weight-1 candidates) AND so the long-run provider frequency converges to the
    declared weights ACROSS trains (advertised weight 4 drawn ~4x as often — true
    across trains, not only within one multi-round train). WI-236 counted only
    THIS train's prefix, so a freshly minted train drew slot 0 deterministically
    and the weights were inert across trains (M-31); the caller now passes the
    durable aggregate — the PRIMARY worktree's committed docs/iteration plus this
    worker's own in-flight logs (see `draw_iter_dirs`). Reads existing state only
    (the logs already record the phase); no new durable store, no randomness.
    Empty phase / absent dirs -> 0 (the first draw)."""
    if not phase:
        return 0
    seen = set()
    count = 0
    for iter_dir in _iter_dir_list(iter_dirs):
        if not iter_dir.is_dir():
            continue
        for log in iter_dir.glob("*.log"):
            # De-dup by filename: the same committed log can appear in both the
            # primary aggregate and the local worktree (a train branched from the
            # development checkout carries its history); a session's log name is
            # unique ((train, session, stamp)), so first sighting counts it once.
            if log.name in seen:
                continue
            seen.add(log.name)
            if read_log_meta(log).get("phase", "") == phase:
                count += 1
    return count


def primary_worktree_root(root):
    """The MAIN (primary) worktree of `root`'s repo — the FIRST entry of
    `git worktree list --porcelain`, which git always lists ahead of the linked
    worktrees (WI-263). A dispatched worker runs agent_loop inside a linked TRAIN
    worktree; this is how it reaches the durable cross-train iteration aggregate
    that lives on the primary checkout. Returns a Path, or None when git can't
    answer (not a repo, git missing) — the caller then falls back to its local
    dir, so a draw never crashes."""
    code, out = git(root, "worktree", "list", "--porcelain")
    if code != 0:
        return None
    for line in out.splitlines():
        if line.startswith("worktree "):
            path = line[len("worktree ") :].strip()
            return Path(path) if path else None
    return None


def draw_iter_dirs(root, local_iter_dir):
    """The iteration directories `phase_draw_ordinal` must union for a cross-train
    draw (WI-263, repo-review M-31). The old draw filtered same-phase logs by this
    train's own filename PREFIX, so the ordinal counted only the current train and
    reset every train — the declared weights never materialized across trains. A
    train branches from `integration_head`, so its LOCAL `docs/iteration` (in the
    linked worktree) already carries prior INTEGRATED trains' logs; dropping the
    prefix filter counts those. But the local dir is frozen at the branch base, so
    it MISSES a sibling train that integrates mid-flight (past this base), and the
    first-ever trains have no prior logs at all. The DURABLE cross-train aggregate
    that closes both gaps is the PRIMARY worktree's committed `docs/iteration` —
    the development checkout every INTEGRATED train's logs land on disk in
    (materialized by `publish_integration` -> `_sync_worktree`). Return that
    primary dir FIRST (its committed history is the authority for the filename
    de-dup) plus the local dir, whose not-yet-integrated in-flight logs keep the
    WITHIN-train rotation advancing between integrations. When the primary IS this
    root (an attended single-repo run, no linked worktree) the two coincide and
    only the one dir is returned."""
    local = Path(local_iter_dir)
    primary = primary_worktree_root(root)
    if primary is None:
        return [local]
    shared = primary / "docs" / "iteration"
    if _same_dir(shared, local):
        return [local]
    return [shared, local]


def _same_dir(a, b):
    """Whether two paths name the same directory, tolerant of symlinks and a
    not-yet-created dir (macOS /tmp -> /private/tmp; a fresh worktree). A wrong
    answer is only a lost optimization — `phase_draw_ordinal` de-dups by filename
    regardless — so any error just answers "different"."""
    try:
        return a.resolve() == b.resolve()
    except OSError:
        return a == b


def preflight(root, template, args):
    """Refuse to start iteration 1 on a broken footing. Returns the list of
    failures (empty = go)."""
    failures = []
    if not template.strip():
        failures.append(
            "no agent command wired yet: fill the AGENT_CMD slot in "
            "agent-resume.cmd + agent-resume.sh (or pass --agent-cmd / set "
            "the AGENT_CMD env var). Example:\n"
            "    claude -p --model {model} --output-format json "
            "--dangerously-skip-permissions\n"
            "  (no {prompt} = the prompt is piped to the CLI's stdin — immune "
            "to OS command-line caps and Windows batch-shim shell re-parsing; "
            "a .cmd/.bat shim with {prompt} is refused, so use stdin or a "
            "native executable).\n"
            "  The permission-bypass flag is YOUR consent to unattended "
            "edits; leave it out to be prompted."
        )
        return failures  # nothing else is checkable without a command
    try:
        argv, _ = build_argv(template, "model", "prompt")
    except ValueError as exc:
        failures.append("cannot parse AGENT_CMD: {}".format(exc))
        return failures
    exe = argv[0]
    if not (shutil.which(exe) or Path(exe).exists()):
        failures.append(
            "agent CLI not found: {!r} is not on PATH. Install it (or fix "
            "AGENT_CMD), then re-run.".format(exe)
        )
    code, _ = git(root, "rev-parse", "--git-dir")
    if code != 0:
        failures.append(
            "{} is not a git repository — the loop reads commits as its "
            "progress signal.".format(root)
        )
    else:
        enabled = (
            read_declared(root / "docs" / "privacy-check", "false").lower() == "true"
        )
        if enabled:
            # Single-source the exempt allowlist: let check_privacy.py judge the
            # author email (it self-skips when the gate is off, so this fails
            # only on a genuinely private author on a privacy-checked repo).
            proc = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).resolve().parent / "check_privacy.py"),
                    "--root",
                    str(root),
                    "--author",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            if proc.returncode != 0:
                failures.append(
                    "privacy-check author identity violated: an unattended run "
                    "would commit every session under a private identity. "
                    + (proc.stderr or proc.stdout or "").strip()
                )
    # --- worker assignment preflight (WI-181, SR-060) -----------------------
    wi_spec = getattr(args, "wi", None)
    train = getattr(args, "train", None)
    if bool(wi_spec) != bool(train):
        failures.append(
            "--wi and --train come as a pair (the dispatcher's explicit "
            "assignment); got {}".format(
                "--wi without --train" if wi_spec else "--train without --wi"
            )
        )
    if (wi_spec or train) and getattr(args, "interactive", False):
        failures.append(
            "--wi/--train is an unattended worker assignment; it cannot be "
            "combined with --interactive."
        )
    if wi_spec and train and not failures:
        try:
            assigned = parse_wi_list(wi_spec)
            sanitize_train(train)
        except ValueError as exc:
            failures.append(str(exc))
        else:
            expected = TRAIN_BRANCH_PREFIX + train
            code, branch = git(root, "branch", "--show-current")
            if code != 0 or not branch:
                # Detached HEAD / unreadable branch: the lane cannot be
                # confirmed, so a worker must fail CLOSED (the track guard's
                # rule) — never build a train from an unverifiable checkout.
                failures.append(
                    "worker assignment for train {!r} requires branch {!r}, "
                    "but this worktree's branch could not be determined "
                    "(detached HEAD, or git older than 2.22).".format(train, expected)
                )
            elif branch != expected:
                failures.append(
                    "worker assignment for train {!r} must run on its train "
                    "branch {!r}, but this worktree is on {!r} — the "
                    "dispatcher creates the branch and leases the worktree "
                    "(docs/specs/parallel-wi-dispatch.md §6).".format(
                        train, expected, branch
                    )
                )
            wi_rows = load_wi_registry(root)
            for wid in assigned:
                row = wi_rows.get(wid)
                if row is None:
                    failures.append(
                        "assigned {} is not in docs/requirements/"
                        "work-items.csv on this branch — a worker never "
                        "builds an untracked WI.".format(wid)
                    )
                elif (row.get("Status") or "").strip().lower() in TERMINAL_STATUSES:
                    # WI-267: a WI RETIRED mid-assignment is terminal too — a
                    # worker must never build a WON'T-BUILD row. The scheduler
                    # never freshly dispatches a retired WI, but an owner can
                    # retire one already leased to a worker; this closes that
                    # narrow mid-flight race the done-only check missed.
                    status = (row.get("Status") or "").strip().lower()
                    failures.append(
                        "assigned {} is already {} — a terminal status "
                        "(done/retired); a stale assignment, so the dispatcher "
                        "must re-derive the frontier.".format(wid, status)
                    )
    return failures


def stop_banner(status_path, label, detail=""):
    print("\n=== coordinator stopping: {} ===".format(label))
    if detail:
        print(detail)
    print("--- pending state ({} Current State) ---".format(status_path))
    print(current_state_excerpt(status_path))
    print(
        "--- end-of-run evidence: {0} | {1} | {2} ---".format(
            status_path,
            status_path.parent / "log.md",
            status_path.parent / "iteration_index.md",
        )
    )


def _utf8_console():
    """Emit UTF-8 whatever the OS console codepage is (bootstrap.py's guard):
    session transcripts echoed into findings can carry any characters."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def _write_runstate(docs, state, ask=""):
    """The dispatcher-generated root run-state (spec §10; SR-059's generation
    half): RUNNING | NEEDS-HUMAN (+ ask) | BLOCKED | DONE. Generated only by
    the dispatcher/integrator — never by a worker."""
    try:
        (docs / "run-state").write_text(
            state + ("\nask: " + ask if ask else "") + "\n", encoding="utf-8"
        )
    except OSError:
        pass


def head_sha_full(root):
    """Full HEAD sha (reservation bases are exact, never abbreviated)."""
    code, out = git(root, "rev-parse", "HEAD")
    return out if code == 0 else ""
