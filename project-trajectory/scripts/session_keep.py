#!/usr/bin/env python3
"""The session service's keep operation: adjudicator session retention.

The retention layer OI-69 ruled (the plan of record is
docs/plans/2026-08-29-adjudicator-session-retention-plan.md): a retained
TRANSCRIPT that a bounded headless process replays through its runner's resume
form, never a daemon, a long-lived process or an open stdin, so an unattended
run still cannot wedge on a prompt. This module is the layer's state and its
rules: the `[adjudicator]` table, the per-route record and its lock and lease,
the pre-launch reset rules, the post-call bookkeeping and the keep-warm
schedule. It launches nothing and records nothing: every retained call is an
ordinary call through the session service's act and record steps, which ask
this module what to resume and tell it what happened.

SHIPPED INERT. At `[adjudicator] context_reset_pct = 0`, `keep_for` returns
None before reading or writing anything, so no id is minted, no resume flag is
added, no store is written, and the launch is exactly a fresh session's.

Stdlib only, Python 3.11+, Windows/POSIX. It imports `agent_common` (the
policy-file reader and git); `session_service` imports it.

Contracts: IF-247, IF-248 — the interface seams this module declares
(process.md §8; rows of record in docs/requirements/interfaces.toml).

Contract IF-247: the retained-session record, one JSON object per route at
    `out/adjudicator/<FAMILY>-<hash of the route id>.json` under the primary
    checkout (the git common directory's parent, else the root given). Its
    identity is `family` and `route_id`, kept verbatim; `session_id` is the
    runner's own id, `generation` counts the sessions this route has minted,
    `state` is `active`, `draining` or `retired`, `reset_reason` says why it
    left `active`, `judged` lists the work items it has judged, `cli_version`
    is the runner's `--version` when it was minted, `lease` is `{holder,
    until}` while one call owns it, and `governing_hash`, `window`,
    `occupancy`, `pct`, `started`, `last_used` and `last_used_epoch` record
    what it was last seen under. Codex records also keep `input_total` and
    `request_prompt` as comparison baselines, `compacted` and
    `compaction_source` (reported, inferred or empty). A fresh generation has
    no prior compaction or comparison baseline.
    Every read-modify-write holds the store lock
    (`out/adjudicator/.lock`, created exclusively, stale after two minutes);
    a record is written whole through its own temporary file and a replace; a
    file that does not parse, or names another route, reads as no session.

Contract IF-248: the keep call surface the session service composes.
    `keep_config(root)` reads `[adjudicator]` as a `KeepConfig`; `applies(cfg,
    role, brief, route_id)` says whether the operation covers a call;
    `keep_for(root, cfg, role=, brief=, family=, route_id=, wi=, rows=,
    cli_version=, template_paths=, template_texts=, lease_seconds=,
    lease_wait=)` returns the `Keep` an adjudication resumes or mints, holding
    the route's lease, or None when the layer does not apply or the lease stays
    held past `lease_wait`; `keep_argv(adapter, argv, keep)` is the resume or
    mint argv; `keep_bookkeep(root, keep, minted, outcome)` folds a finished
    call in, applies the reset rules, releases the lease and returns the
    `session-gen` and `reset-reason` columns and, with a codex observation
    supplied as `compaction=`, `compacted` and `compaction-source`;
    `keep_abandon(root, keep,
    reason)` retires the session of a launch that raised, through a tombstone
    (`<record>.retire`, written whole without the lock) that every locked read
    applies first (`load_honoured`) when the lock cannot be had at once;
    `take_warm_lease(root,
    cfg, now=, work_pending=, holder=)` returns `(keep, reason)` for the next
    due keep-warm ping, `reason` naming why a due ping cannot run now.
"""

import hashlib
import json
import os
import re
import sys
import tempfile
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path

try:
    import agent_common
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import agent_common

STATE_ACTIVE = "active"
STATE_DRAINING = "draining"
STATE_RETIRED = "retired"

# The per-family reset ceiling: codex compacts on its own at about 90% of its
# window, so a dial above 85 is clamped there and codex's compaction stays the
# backstop; claude and opencode leave their provider compaction above the dial.
# Implements: SR-227, LLR-270
FAMILY_RESET_CAP = {"OPENAI": 85}

# The governing inputs whose change drains a retained session: a judgement is
# stale when the rules it judges under changed, not when HEAD moved. The agent
# guides and the policy file, the skills a runner loads from the repository,
# and (from the caller) the adjudication template the brief is composed from.
# Implements: SR-227, LLR-270
GOVERNING_INPUT_FILES = ("CLAUDE.md", "AGENTS.md", "GEMINI.md", "docs/process.toml")
# Implements: SR-227, LLR-270
GOVERNING_INPUT_GLOBS = (".claude/skills/*/SKILL.md", ".agents/skills/*/SKILL.md")

# The dedicated CLI home per family, used only while retention is on (OI-69
# (e1)): the working directory still supplies what the kit mandates, and what
# moves is the user layer, so a retained transcript never mixes with a
# person's own sessions. Credentials are provisioned into it by a person.
# Implements: SR-227, LLR-270
HOME_VARIABLES = {"ANTHROPIC": "CLAUDE_CONFIG_DIR", "OPENAI": "CODEX_HOME"}

_LOCK_STALE_SECONDS = 120


@dataclass(frozen=True)
class KeepConfig:
    """The `[adjudicator]` table. `context_reset_pct = 0` is OFF.

    Implements: SR-227, LLR-270
    """

    context_reset_pct: int = 0
    retain_for: tuple = ("disposition", "amendment", "red-tc")
    keepwarm_minutes: int = 0
    reset_on_same_artifact: bool = False

    @property
    def enabled(self):
        return self.context_reset_pct > 0


def _dial(value, low, high):
    """An int dial within [low, high], else None (a bool is not a dial)."""
    ok = isinstance(value, int) and not isinstance(value, bool)
    return value if ok and low <= value <= high else None


def keep_config(root):
    """The repository's `[adjudicator]` table as a `KeepConfig`. An absent
    table, and any value outside its type or range, reads as that field's
    default, so a malformed dial can only leave the layer OFF.

    Implements: SR-227, LLR-270
    """
    table = agent_common.process_config(Path(root) / "docs").get("adjudicator")
    table = table if isinstance(table, dict) else {}
    default = KeepConfig()
    retain = table.get("retain_for")
    retain_ok = isinstance(retain, list) and all(isinstance(x, str) for x in retain)
    same = table.get("reset_on_same_artifact")
    return KeepConfig(
        context_reset_pct=_dial(table.get("context_reset_pct"), 0, 100) or 0,
        retain_for=tuple(retain) if retain_ok else default.retain_for,
        keepwarm_minutes=_dial(table.get("keepwarm_minutes"), 0, 10**6) or 0,
        reset_on_same_artifact=same if isinstance(same, bool) else False,
    )


def reset_pct(cfg, family):
    """The reset percent that applies to `family`, clamped by its cap."""
    cap = FAMILY_RESET_CAP.get((family or "").upper())
    return min(cfg.context_reset_pct, cap) if cap else cfg.context_reset_pct


# --- the store: one record per route, under a lock ---------------------------


def primary_out_dir(root):
    """The untracked `out/` directory of the PRIMARY checkout (the git common
    directory's parent, else `root` itself), so a lane's worktree, which comes
    and goes, shares one runtime store with the others and with the
    dispatcher. The one home of that lookup: the adjudicator store and the
    coordinator lease both live under it."""
    code, out = agent_common.git(
        root, "rev-parse", "--path-format=absolute", "--git-common-dir"
    )
    common = Path(out.strip()) if code == 0 and out.strip() else None
    base = common.parent if common is not None and common.name == ".git" else root
    return Path(base) / "out"


def store_dir(root):
    """Where retained sessions are recorded: `out/adjudicator/` under the
    PRIMARY checkout (`primary_out_dir`). Per-clone runtime state, ignored
    with the rest of `out/`."""
    return primary_out_dir(root) / "adjudicator"


class StoreBusy(Exception):
    """The store lock stayed held past the wait."""


@contextmanager
def store_lock(root, wait=10.0):
    """Hold the store lock for one read-modify-write. The lock is a file
    created exclusively, so it excludes other processes (a lane's worker and
    the dispatcher) as well as threads; one left behind by a killed holder is
    stale after two minutes and taken over. Raises StoreBusy past `wait`.

    Implements: SR-227, LLR-270
    """
    with dir_lock(store_dir(root), wait) as directory:
        yield directory


@contextmanager
def dir_lock(directory, wait=10.0):
    """Hold `directory/.lock` for one read-modify-write: the store lock's
    mechanism, shared by every per-clone runtime store under `out/`. Creates
    the directory; raises StoreBusy past `wait`."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / ".lock"
    deadline = time.monotonic() + wait
    while not _try_lock(path):
        if time.monotonic() >= deadline:
            raise StoreBusy(str(path))
        time.sleep(0.05)
    try:
        yield directory
    finally:
        try:
            path.unlink()
        except OSError:
            pass


def _try_lock(path):
    """Create the lock file, clearing a stale one; True when it is ours."""
    try:
        fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        try:
            if time.time() - path.stat().st_mtime > _LOCK_STALE_SECONDS:
                path.unlink()
        except OSError:
            pass
        return False
    os.write(fd, str(os.getpid()).encode("ascii"))
    os.close(fd)
    return True


def _store_path(root, family, route_id):
    """One route's record file. The route id is hashed into the name (it is
    registry data, not a trusted path segment) and kept verbatim inside."""
    key = hashlib.sha256((route_id or "").encode("utf-8")).hexdigest()[:24]
    return store_dir(root) / "{}-{}.json".format((family or "").upper(), key)


def store_load(root, family, route_id):
    """The route's record, or None when absent, unreadable or not its own —
    a corrupt store reads as "no session", and the next launch mints, which
    is always safe (retention is an optimisation, never a correctness input).

    Implements: SR-227, LLR-270
    """
    return _load_path(_store_path(root, family, route_id), family, route_id)


def _load_path(path, family, route_id):
    try:
        record = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(record, dict):
        return None
    same = (record.get("family"), record.get("route_id")) == (
        (family or "").upper(),
        route_id or "",
    )
    return record if same else None


def _write_whole(path, text):
    """Write `text` to `path` through its own temporary file and a replace."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=path.stem, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    os.replace(tmp, path)


def _tombstone_path(root, family, route_id):
    return _store_path(root, family, route_id).with_suffix(".retire")


def write_tombstone(root, keep, reason):
    """Mark a retained session for retirement WITHOUT the store lock: a file
    beside the route's record, written whole, naming the session, the reason
    and the lease holder. Every locked read of the record honours it before
    anything else (`load_honoured`), and the lockless keep-warm read skips a
    marked record, so a session whose launch failed is retired even when the
    lock could not be had at the moment of failure.

    Implements: SR-227, LLR-270
    """
    body = {"session_id": keep.session_id, "reason": reason, "holder": keep.holder}
    _write_whole(_tombstone_path(root, keep.family, keep.route_id), json.dumps(body))


def load_honoured(root, family, route_id):
    """`store_load`, with a pending tombstone applied: the session it names
    is retired, the holder's lease dropped, the record saved and the
    tombstone removed. Callers hold `store_lock`.

    Implements: SR-227, LLR-270
    """
    record = store_load(root, family, route_id)
    path = _tombstone_path(root, family, route_id)
    try:
        tomb = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return record
    if isinstance(record, dict) and isinstance(tomb, dict):
        if tomb.get("session_id") and record.get("session_id") == tomb["session_id"]:
            _retire(record, tomb.get("reason") or "session unusable")
        if (record.get("lease") or {}).get("holder") == tomb.get("holder"):
            record.pop("lease", None)
        store_save(root, record)
    try:
        path.unlink()
    except OSError:
        pass
    return record


def store_save(root, record):
    """Write a record whole: its own temporary file beside it, then a replace,
    so no reader ever sees half of one and no two writers share a temp path.
    Callers hold `store_lock`."""
    path = _store_path(root, record["family"], record["route_id"])
    _write_whole(path, json.dumps(record, sort_keys=True))


def dedicated_home_env(root, family):
    """The dedicated CLI home for `family` while retention is on, created if
    absent: `{variable: path}` under the store's `home/`, or `{}` for a family
    with no ruled home variable.

    Implements: SR-227, LLR-270
    """
    variable = HOME_VARIABLES.get((family or "").upper())
    if not variable:
        return {}
    home = store_dir(root) / "home" / (family or "").lower()
    home.mkdir(parents=True, exist_ok=True)
    return {variable: str(home)}


# --- the rules ------------------------------------------------------------------


def governing_hash(root, template_paths=(), template_texts=()):
    """A digest of the governing inputs: the agent guides, the policy file,
    the skills the runners load from the repository, and the adjudication
    templates the caller names. A missing file adds nothing; each file enters
    under its path, so a rename is a change; an operator's override text for a
    template enters as text.

    Implements: SR-227, LLR-270
    """
    root = Path(root)
    paths = [root / rel for rel in GOVERNING_INPUT_FILES]
    for pattern in GOVERNING_INPUT_GLOBS:
        paths.extend(root.glob(pattern))
    paths.extend(Path(p) for p in template_paths)
    digest = hashlib.sha256()
    for path in sorted(set(paths), key=str):
        try:
            data = path.read_bytes()
        except OSError:
            continue
        try:
            name = os.path.relpath(path, root)
        except ValueError:  # another drive on Windows
            name = str(path)
        digest.update(name.replace(os.sep, "/").encode("utf-8"))
        digest.update(b"\0" + data + b"\0")
    for text in template_texts:
        digest.update(b"override\0" + text.encode("utf-8", "replace") + b"\0")
    return digest.hexdigest()


def drain_reason(record, pct, reset_at, governing_now, version_now=""):
    """Why an ACTIVE session should drain, or None: it crested the dial, the
    inputs it judges under changed, or its runner's version is no longer the
    one it was minted under. Draining is not closing: the session keeps being
    resumed for its own chains until a clear point.

    Implements: SR-227, LLR-270
    """
    if not isinstance(record, dict) or record.get("state") != STATE_ACTIVE:
        return None
    if reset_at and isinstance(pct, int) and pct >= reset_at:
        return "crest {}% >= {}%".format(pct, reset_at)
    stored = record.get("governing_hash") or ""
    if governing_now and stored and stored != governing_now:
        return "governing-inputs changed"
    minted = record.get("cli_version") or ""
    if version_now and minted and version_now != minted:
        return "cli version {} -> {}".format(minted, version_now)
    return None


_WI = re.compile(r"WI-\d+")


def lineage(wid, rows):
    """`wid` and every work item it descends from: the closure of its
    Predecessors and Supersedes links through the registry `rows`, so an
    adjudication, the worker it sent back, and the re-adjudication naming
    only that worker are one chain. A cycle ends where it closes.

    Implements: SR-227, LLR-270
    """
    seen, todo = set(), [wid]
    while todo:
        item = todo.pop()
        if item in seen:
            continue
        seen.add(item)
        row = (rows or {}).get(item) or {}
        for column in ("Predecessors", "Supersedes"):
            todo.extend(_WI.findall(str(row.get(column) or "")))
    return seen


def _related(wid, rows, judged):
    """Whether work item `wid` belongs to a chain the session is inside:
    its lineage holds an item the session judged."""
    return bool(lineage(wid, rows) & set(judged))


def chain_pending(rows, judged, current):
    """The work items that keep a draining session's chains open: a queued
    adjudication, or a lane out on work (status `active`), that belongs to a
    chain the session judged — other than `current`, the one being launched.

    Implements: SR-227, LLR-270
    """
    pending = []
    for wid, row in sorted((rows or {}).items()):
        if wid == current or not _related(wid, rows, judged):
            continue
        status = (row.get("Status") or "").strip().lower()
        adjudication = (row.get("SafetyClass") or "").strip().lower() == "adjudication"
        if status == "active" or (status == "queued" and adjudication):
            pending.append(wid)
    return pending


def is_clear_point(rows, judged, current):
    """A draining session may be retired now: the adjudication being launched
    continues none of its chains, no queued adjudication belongs to one, and
    no lane is out on work that belongs to one — the adjudicator is waiting on
    workers with nothing of its own pending.

    Implements: SR-227, LLR-270
    """
    if current and _related(current, rows, judged):
        return False
    return not chain_pending(rows, judged, current)


@dataclass
class Keep:
    """One call's hold on a retained session: which route, the session it
    resumes (an empty `session_id` mints), what it judges, the lease it
    holds, and the dedicated home its launch runs under."""

    family: str
    route_id: str
    session_id: str
    wi: str
    governing: str
    cfg: KeepConfig
    holder: str = ""
    cli_version: str = ""
    generation: int = 0
    home_env: dict = field(default_factory=dict)


def _lease_held(record, holder, now):
    """The holder of a live lease someone else owns, else ""."""
    lease = record.get("lease") if isinstance(record, dict) else None
    if not isinstance(lease, dict) or lease.get("holder") in ("", holder):
        return ""
    until = lease.get("until")
    if not isinstance(until, (int, float)) or until <= now:
        return ""  # an expired lease: its holder died or overran
    return lease.get("holder") or ""


def retire_stale_lease(record, holder, now):
    """Retire a session whose lease EXPIRED without being released. A lease
    is released by the call that took it when that call is bookkept or
    abandoned, so an expired one means its holder is still running past its
    lease or crashed; the transcript's state is unknown, and resuming it
    could put two calls on one session. So it is never reused: it is retired
    (the next launch mints fresh) and the stale lease dropped. Returns
    whether the record changed.

    Implements: SR-227, LLR-270
    """
    lease = record.get("lease") if isinstance(record, dict) else None
    if not isinstance(lease, dict) or lease.get("holder") in ("", holder):
        return False
    until = lease.get("until")
    if isinstance(until, (int, float)) and until > now:
        return False
    if record.get("state") != STATE_RETIRED:
        _retire(record, "lease expired unreleased")
    record.pop("lease", None)
    return True


def _retire(record, reason):
    record["state"] = STATE_RETIRED
    record["reset_reason"] = reason


def _before_launch(cfg, record, wi, governing, version, rows):
    """The pre-launch reset rules on a live record (see `keep_for`)."""
    judged = record.get("judged") or []
    if cfg.reset_on_same_artifact and wi in judged:
        _retire(record, "same-artifact guard")
        return
    reason = drain_reason(record, None, 0, governing, version)
    if reason:
        record["state"], record["reset_reason"] = STATE_DRAINING, reason
    if record["state"] == STATE_DRAINING and is_clear_point(rows, judged, wi):
        _retire(record, record.get("reset_reason") or "drained")


def applies(cfg, role, brief, route_id):
    """Whether the keep operation covers this call at all: the dial is on,
    it is an adjudication of a retained class, and a route is named.

    Implements: SR-227, LLR-270
    """
    return (
        cfg.enabled
        and role == "ADJUDICATE"
        and bool(route_id)
        and brief in cfg.retain_for
    )


def keep_for(
    root,
    cfg,
    *,
    role,
    brief,
    family,
    route_id,
    wi,
    rows=None,
    cli_version="",
    template_paths=(),
    template_texts=(),
    lease_seconds=7500,
    lease_wait=120.0,
):
    """The retained session an adjudication resumes or mints, or None.

    None, touching nothing, when the layer does not apply: the dial is off,
    the role is not ADJUDICATE, the brief is not a retained class, or no route
    is named. Otherwise, before the launch and under the store lock:

      - a retired or absent record mints (`session_id` "");
      - with the same-artifact guard on, a session that already judged this
        work item retires, so the rejudgement is fresh;
      - a changed governing input or runner version drains an active session;
      - a draining session retires at a clear point (`is_clear_point`, over
        the work-item `rows`) and is otherwise resumed, so a review, rework,
        re-review round trip is never cut mid-way;
      - the call takes the route's lease for `lease_seconds`, so a keep-warm
        ping cannot resume the same session while it runs. A lease another
        call holds is waited on up to `lease_wait` seconds; past that the
        adjudication runs unretained (None) and says why.

    Implements: SR-227, LLR-270
    """
    if not applies(cfg, role, brief, route_id):
        return None
    governing = governing_hash(root, template_paths, template_texts)
    holder = "adjudicate:" + uuid.uuid4().hex
    deadline = time.monotonic() + lease_wait
    while True:
        try:
            with store_lock(root):
                record = load_honoured(root, family, route_id)
                # ONE clock read per locked decision: two reads could see a
                # lease live to the retire rule and free to the busy rule.
                clock = time.time()
                retire_stale_lease(record, holder, clock)
                busy = _lease_held(record, holder, clock)
                if not busy:
                    return _hold(
                        root,
                        cfg,
                        record,
                        (family, route_id, wi, governing, cli_version),
                        rows,
                        (holder, clock + lease_seconds),
                    )
        except StoreBusy:
            busy = "the store lock"
        if time.monotonic() >= deadline:
            print(
                "keep [{}]: held by {}; this adjudication runs unretained".format(
                    route_id, busy
                ),
                file=sys.stderr,
            )
            return None
        time.sleep(1.0)


def _hold(root, cfg, record, subject, rows, lease):
    """Apply the pre-launch rules, take the lease `(holder, until)`, and
    build the Keep."""
    family, route_id, wi, governing, version = subject
    holder, until = lease
    live = record is not None and record.get("state") != STATE_RETIRED
    if live:
        _before_launch(cfg, record, wi, governing, version, rows)
        live = record.get("state") != STATE_RETIRED
    if record is not None:
        record["lease"] = {"holder": holder, "until": until}
        store_save(root, record)
    return Keep(
        family=(family or "").upper(),
        route_id=route_id,
        session_id=(record.get("session_id") or "") if live else "",
        wi=wi or "",
        governing=governing,
        cfg=cfg,
        holder=holder,
        cli_version=version or "",
        generation=(record or {}).get("generation", 0),
        home_env=dedicated_home_env(root, family),
    )


def keep_argv(adapter, argv, keep):
    """`(argv, minted_id)`: the resume form when the keep holds a session,
    else the mint form (claude takes a pre-minted id; the others report the
    id they chose in their output).

    Implements: SR-227, LLR-270
    """
    if keep.session_id:
        return adapter.resume(argv, keep.session_id), ""
    return adapter.mint(argv)


def _fresh_record(keep, session_id, prior, stamp):
    return {
        "family": keep.family,
        "route_id": keep.route_id,
        "session_id": session_id or "",
        "generation": prior + 1,
        "started": stamp,
        "governing_hash": keep.governing,
        "cli_version": keep.cli_version,
        "window": "",
        "occupancy": "",
        "pct": "",
        "judged": [],
        "state": STATE_ACTIVE,
        "reset_reason": "",
    }


def _landing(current, keep, session_id, stamp):
    """The record this call's observation lands on, or None when the store
    moved on to another session while the call ran (that one is left alone)."""
    if keep.session_id:
        ours = (
            isinstance(current, dict) and current.get("session_id") == keep.session_id
        )
        return current if ours else None
    live = isinstance(current, dict) and current.get("state") != STATE_RETIRED
    if live and _lease_held(current, keep.holder, time.time()):
        return None
    prior = max(keep.generation, (current or {}).get("generation", 0))
    return _fresh_record(keep, session_id, prior, stamp)


def _unusable(outcome, reported_error):
    return outcome.code != 0 or bool(outcome.timed_out) or reported_error


def keep_bookkeep(
    root, keep, minted, outcome, reported_error=False, *, compaction=None
):
    """Fold one retained call into its record, under the store lock, and
    decide its reset: an unusable session (a non-zero exit, a timeout, an
    error the runner reported) retires at once; one whose occupancy reached
    the dial drains. Releases the lease. Returns the call's `session-gen` and
    `reset-reason` columns.

    Implements: SR-227, LLR-270
    """
    m = outcome.metrics
    with store_lock(root):
        current = load_honoured(root, keep.family, keep.route_id)
        record = _landing(
            current, keep, minted or m.get("session-id", ""), m["ended-at"]
        )
        if record is None:
            return {"session-gen": "", "reset-reason": "store moved on"}
        compaction_columns = _observe_compaction(
            record, compaction, not keep.session_id
        )
        _observe(record, keep, m)
        if not record["session_id"]:
            _retire(record, "session id unavailable")
        elif _unusable(outcome, reported_error):
            _retire(record, "session unusable")
        else:
            reason = drain_reason(
                record, record["pct"], reset_pct(keep.cfg, keep.family), keep.governing
            )
            if reason:
                record["state"], record["reset_reason"] = STATE_DRAINING, reason
        record.pop("lease", None)
        store_save(root, record)
    return {
        "session-gen": record["generation"],
        "reset-reason": record["reset_reason"],
        **compaction_columns,
    }


def _observe_compaction(record, observation, fresh):
    """Infer only from new rollout requests, never exec turn sums. The
    cursor excludes old requests; a legacy record first learns a baseline.

    Implements: SR-227, LLR-290
    """
    if not observation:
        return {}
    prompts = observation["prompts"]
    cursor = record.get("rollout_requests")
    previous = record.get("request_prompt") if cursor is not None else None
    requests = prompts[(cursor or 0) :] if fresh or cursor is not None else []
    pair = ([previous] if previous is not None else []) + requests
    inferred = any(current < prior for prior, current in zip(pair, pair[1:]))
    if prompts:
        record["request_prompt"] = prompts[-1]
        record["rollout_requests"] = len(prompts)
    else:
        record.setdefault("request_prompt", None)
    if observation["totals"]:
        record["input_total"] = observation["totals"][-1]
    source = record.get("compaction_source", "")
    if observation["reported"]:
        source = "reported"
    elif inferred and not source:
        source = "inferred"
    record["compaction_source"] = source
    record["compacted"] = bool(source)
    return {"compacted": bool(source), "compaction-source": source}


def _observe(record, keep, m):
    """Copy one call's occupancy and use into its record."""
    for key, column in (("occupancy", "context-used"), ("window", "context-window")):
        if m.get(column, "") != "":
            record[key] = m[column]
    record["pct"] = m.get("context-pct", "")
    record["last_used"] = m["ended-at"]
    record["last_used_epoch"] = time.time()
    if keep.wi and keep.wi not in record["judged"]:
        record["judged"].append(keep.wi)


def keep_abandon(root, keep, reason):
    """A retained launch raised before it could be bookkept: retire the
    session it resumed (its transcript state is unknown) and release the
    lease. The retirement is GUARANTEED: a tombstone is written first, with no
    lock needed, and then applied at once if the store lock can be had; if it
    cannot, the next locked read of the record applies it. A mint that raised
    stored nothing, so there is nothing to retire.

    Implements: SR-227, LLR-270
    """
    write_tombstone(root, keep, reason)
    try:
        with store_lock(root, wait=1.0):
            load_honoured(root, keep.family, keep.route_id)
    except StoreBusy:
        pass  # the tombstone stands; the next locked read honours it


# --- keep-warm --------------------------------------------------------------------


def keepwarm_due(record, cfg, now, work_pending):
    """Whether a keep-warm ping is due: the dial and `keepwarm_minutes` are
    on, the session is ANTHROPIC's (the only family whose prompt cache lives
    an hour; the others' live minutes and are never pinged) and active, work
    is pending, and it has been idle `keepwarm_minutes`. The ping fires
    through the blackout: the daily window never reaches the break-even count
    of pings.

    Implements: SR-227, LLR-270
    """
    if not (cfg.enabled and cfg.keepwarm_minutes > 0 and work_pending):
        return False
    if not isinstance(record, dict) or record.get("family") != "ANTHROPIC":
        return False
    if record.get("state") != STATE_ACTIVE:
        return False
    last = record.get("last_used_epoch")
    if not isinstance(last, (int, float)):
        return False
    return now - last >= cfg.keepwarm_minutes * 60


def due_routes(root, cfg, now, work_pending):
    """The route ids whose retained session is due a keep-warm ping, read
    without the lock (a read of whole records only)."""
    due = []
    for path in sorted(store_dir(root).glob("ANTHROPIC-*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if path.with_suffix(".retire").exists():
            continue  # marked for retirement: never pinged
        if keepwarm_due(record, cfg, now, work_pending):
            due.append(record.get("route_id") or "")
    return due


def take_warm_lease(
    root, cfg, *, now, work_pending, holder, routes=None, lease_seconds=600
):
    """`(keep, reason)` for the next due keep-warm ping. `keep` holds the
    route's lease, so no adjudication resumes the session while the ping
    runs; `reason` names why a due ping cannot run now (the lease or the lock
    is held). `(None, None)` when nothing is due. With `routes`, only those
    route ids are considered (a route the registry no longer lists is never
    pinged).

    Implements: SR-227, LLR-270
    """
    due = [
        r
        for r in due_routes(root, cfg, now, work_pending)
        if routes is None or r in routes
    ]
    if not due:
        return None, None
    try:
        with store_lock(root, wait=0.5):
            for route_id in due:
                record = load_honoured(root, "ANTHROPIC", route_id)
                clock = time.time()  # one read for this record's decision
                if retire_stale_lease(record, holder, clock):
                    store_save(root, record)  # never pinged: retired
                if not keepwarm_due(record, cfg, now, work_pending):
                    continue
                busy = _lease_held(record, holder, clock)
                if busy:
                    return None, "the session is leased to {}".format(busy)
                record["lease"] = {"holder": holder, "until": clock + lease_seconds}
                store_save(root, record)
                return (
                    Keep(
                        family="ANTHROPIC",
                        route_id=route_id,
                        session_id=record.get("session_id") or "",
                        wi="",
                        governing=record.get("governing_hash") or "",
                        cfg=cfg,
                        holder=holder,
                        cli_version=record.get("cli_version") or "",
                        generation=record.get("generation", 0),
                        home_env=dedicated_home_env(root, "ANTHROPIC"),
                    ),
                    None,
                )
    except StoreBusy:
        return None, "the store lock is held"
    return None, None
