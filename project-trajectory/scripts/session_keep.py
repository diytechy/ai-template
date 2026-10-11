#!/usr/bin/env python3
"""The session service's keep operation: adjudicator and loop reviewer session retention.

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
added, no store is written, and the launch is exactly a fresh session's. The
loop's review rounds ride the same layer under their own dial (WI-887,
`[reviewer] context_reset_pct`, also shipped 0), each kept under a `scope`
(`review_retention`), and the final reviewer is fresh unless `[reviewer]
final_reviewer` is `persisted`.

Stdlib only, Python 3.11+, Windows/POSIX. It imports `agent_common` (the
policy-file reader and git); `session_service` imports it.

Contracts: IF-247, IF-248, IF-272, IF-273 — the interface seams this module declares
(process.md §8; rows of record in docs/requirements/interfaces.toml).

Contract IF-272: `primary_out_dir(root)` returns the primary checkout's
    `out/` directory: the parent of the git common directory when that
    directory is named `.git`, else `root` itself (git unavailable, or not a
    repository).

Contract IF-273: `dir_lock(directory, wait=10.0)` is an exclusive-file
    context manager: it creates `directory`, holds `directory/.lock` (created
    exclusively; one older than two minutes is stale and taken over), yields
    `directory`, and raises StoreBusy when the lock stays held past `wait`.

Contract IF-247: the retained-session record, one JSON object per route at
    `out/adjudicator/<FAMILY>-<hash of the route id>.json` under the primary
    checkout (the git common directory's parent, else the root given), and
    one per route and scope (a loop review session, WI-887) at
    `<FAMILY>-<hash of the route id, a NUL and the scope>.json`, so the empty
    scope keeps the adjudicator's name. Its identity is `family`, `route_id`
    and, when not empty, `scope`, kept verbatim; `session_id` is the
    runner's own id, `generation` counts the sessions this route has minted,
    `state` is `active`, `draining` or `retired`, `reset_reason` says why it
    left `active`, `judged` lists the work items it has judged, `cli_version`
    is the runner's `--version` when it was minted, `lease` is `{holder,
    until}` while one call owns it, and `governing_hash`, `window`,
    `occupancy`, `pct`, `started`, `last_used` and `last_used_epoch` record
    what it was last seen under. Codex records also keep `input_total` and
    `request_prompt` as comparison baselines, `compacted` and
    `compaction_source` (reported, inferred or empty). A fresh generation has
    no prior compaction or comparison baseline. A route's first covered call
    writes a LEASE-ONLY record (`family`, `route_id` and `lease`, no session
    yet) before it launches, so a second first call meets the lease; its
    bookkeeping completes the record and its abandonment removes it.
    Every read-modify-write holds the store lock
    (`out/adjudicator/.lock`, created exclusively, stale after two minutes);
    a record is written whole through its own temporary file and a replace; a
    file that does not parse, or names another family, route or scope, reads
    as no session. Beside a record lie its pending STORE MARKERS (WI-858),
    `<record stem>.<hash of the publisher id>.mark`, one JSON object each,
    written whole without the lock: `family`, `route_id`, `scope`,
    `publisher`, `session_id`, `generation`, `published` and `kind`
    (`bookkeep` with the call's `observation`, `release`, or `retire` with
    its `reason`). A locked read applies and deletes them; a record can lag
    them until then.

Contract IF-248: the keep call surface the session service composes.
    `keep_config(root)` reads `[adjudicator]` and `[reviewer]` as a
    `KeepConfig`; `applies(cfg, role, brief, route_id, scope="")` says whether
    the operation covers a call (an adjudication with no scope, or a review
    round with one under the review dial); `keep_for(root, cfg, role=, brief=,
    family=, route_id=, wi=, rows=, cli_version=, template_paths=,
    template_texts=, lease_seconds=, lease_wait=, prepared=, scope=)` returns
    the `Keep` the call resumes or mints, holding the record's lease, or None when the layer does not apply or
    the lease stays held past `lease_wait`. Every `Keep` carries its
    `prepared` launch (the session service's `prepare_launch`), a REQUIRED
    field, so no retained launch can be built unvalidated; `keep_argv(adapter, argv, keep)` is the resume or
    mint argv; `keep_bookkeep(root, keep, minted, outcome, reported_error=,
    *, compaction=, auth_failed=)` folds a finished call in, applies the reset
    rules, releases the lease and returns the `session-gen` and `reset-reason`
    columns and, with a codex observation supplied as `compaction=`,
    `compacted` and `compaction-source`; with `auth_failed` (the runner
    refused the credential) it changes nothing but releasing the call's lease
    (`keep_release`) and returns the session's generation (blank for a mint)
    and an empty `reset-reason`. `keep_abandon(root, keep, reason)` retires
    the session of a launch that raised. `keep_release(root, keep)` releases
    the call's lease and leaves its session's record as it was (a first
    mint's lease-only record is removed). Each of the three, and
    `retire_scope`, PUBLISHES a store marker first (`publish_marker`, no
    lock) and then applies it if the store lock is had within `APPLY_WAIT`;
    otherwise the next locked read (`load_honoured`: the clock, then the
    markers in publication order, then the stale-lease rule) applies it, and
    the lockless reads fold it in (`fold_marker`) without deleting it. None
    raises StoreBusy; a deferred bookkeeping returns `reset-reason`
    `pending` and the call's own `session-gen`; a failed publication raises
    OSError.
    `take_warm_lease(root, cfg, now=, work_pending=, holder=, prepare=)`
    returns `(keep, reason)` for the next due keep-warm ping, `reason` naming
    why a due ping cannot run now; `prepare(route_id)` returns `(prepared,
    reason)` and is asked under the lock before any lease is taken, so a
    refused ping holds nothing; a prepared row whose family differs from the
    record's session is refused there too (`_prepare_warm`), and a warmed
    Keep takes the prepared row's family and home. The blackout window
    (WI-834): `take_warm_lease` returns `(None, None)` inside it, and both it
    and `keep_for` first retire a live session last used before the end of
    the most recent window that ended (or with no last use), reset reason
    `blackout` (`retire_after_blackout`), so the next call mints; a session
    another call's live lease holds is left to that call, its bookkept last
    use deciding at the next keep. A scoped record is never pinged.
    `review_retention(root, worker, phase, narrow)` returns a
    `ReviewRetention(scope, stage, pin)` for a loop review round: the
    iteration scope and stage for a narrow round; for a gating round, after
    retiring the lane's iteration session (`retire_scope`), no scope in
    fresh mode or the final scope and stage in persisted mode; and for any
    scope, the pin of its live route. `scoped_route(root, scope)` is the
    live route kept under a scope, or None. A malformed or misfiled record
    is no record to every load and scan (`_read_record`).
"""

import copy
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
from typing import NamedTuple
from pathlib import Path

try:
    import agent_common
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import agent_common

from kitlib import config as kconfig
from kitlib import verdict as kverdict

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
    """The `[adjudicator]` table, and the `[reviewer]` table's two dials
    (WI-887, `kitlib.config.reviewer_dials`). `context_reset_pct = 0` is OFF
    for adjudications, `review_reset_pct = 0` for loop review rounds; a
    `final_reviewer` of `persisted` keeps the final reviewer under its own
    scope while review retention is on.

    Implements: SR-227, LLR-270
    """

    context_reset_pct: int = 0
    retain_for: tuple = ("disposition", "amendment", "red-tc")
    keepwarm_minutes: int = 0
    reset_on_same_artifact: bool = False
    review_reset_pct: int = 0
    final_reviewer: str = kconfig.FINAL_FRESH

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
    review_pct, final = kconfig.reviewer_dials(root)
    return KeepConfig(
        context_reset_pct=_dial(table.get("context_reset_pct"), 0, 100) or 0,
        retain_for=tuple(retain) if retain_ok else default.retain_for,
        keepwarm_minutes=_dial(table.get("keepwarm_minutes"), 0, 10**6) or 0,
        reset_on_same_artifact=same if isinstance(same, bool) else False,
        review_reset_pct=review_pct,
        final_reviewer=final,
    )


def reset_pct(cfg, family, scope=""):
    """The reset percent that applies to `family`, clamped by its cap: the
    review dial for a scoped (loop review) session, else the adjudicator's."""
    dial = cfg.review_reset_pct if scope else cfg.context_reset_pct
    cap = FAMILY_RESET_CAP.get((family or "").upper())
    return min(dial, cap) if cap else dial


# --- the store: one record per route, under a lock ---------------------------


_COMMON_DIR = {}  # absolute root -> its git common directory (None: no repo)


def primary_out_dir(root):
    """The untracked `out/` directory of the PRIMARY checkout (the git common
    directory's parent, else `root` itself), so a lane's worktree, which comes
    and goes, shares one runtime store with the others and with the
    dispatcher. The one home of that lookup: the adjudicator store and the
    coordinator lease both live under it. Resolved by one git spawn per root
    and remembered for the life of the process (WI-874): a checkout's common
    directory does not move under a running operation, and every store
    access would otherwise pay the spawn again.

    Implements: SR-227, LLR-270
    """
    key = os.path.abspath(root)
    if key not in _COMMON_DIR:
        code, out = agent_common.git(
            root, "rev-parse", "--path-format=absolute", "--git-common-dir"
        )
        _COMMON_DIR[key] = Path(out.strip()) if code == 0 and out.strip() else None
    common = _COMMON_DIR[key]
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


def _store_path(root, family, route_id, scope=""):
    """One record's file: a route's, or a route's under a `scope` (WI-887).
    The route id, and a scope after it, are hashed into the name (registry
    and lane data, not trusted path segments) and kept verbatim inside. The
    EMPTY scope hashes the route id alone, the adjudicator's file name, so a
    record written before scopes existed still loads."""
    return store_dir(root) / _record_name(family, route_id, scope)


def _record_name(family, route_id, scope=""):
    """The file name a record of this identity is filed under (`_store_path`).

    Implements: SR-227, LLR-270
    """
    keyed = route_id or ""
    if scope:
        keyed += "\0" + scope
    key = hashlib.sha256(keyed.encode("utf-8")).hexdigest()[:24]
    return "{}-{}.json".format((family or "").upper(), key)


def store_load(root, family, route_id, scope=""):
    """The record of `route_id` under `scope`, or None when absent,
    unreadable, malformed or not its own: one naming another family, route or
    scope reads as no record. A corrupt store reads as "no session", and the
    next launch mints, which is always safe (retention is an optimisation,
    never a correctness input).

    Implements: SR-227, SR-239, LLR-270
    """
    path = _store_path(root, family, route_id, scope)
    return _load_path(path, family, route_id, scope)


# The record variants the store's writers produce (IF-247), declared once and
# read by the reader (`_variant`) and by `is_lease_only`; each field with its
# type. Every variant has the IDENTITY and may carry the ENVELOPE. LEASE-ONLY
# is a first call's record (`_hold`): nothing else. RETIRED-FIRST is that record
# retired before any session (`retire_stale_lease`): the RETIREMENT fields too,
# `state` retired. FULL is a session's record (`_fresh_record`): every
# RETIREMENT and SESSION field, which its consumers read, and the OPTIONAL
# fields, each of its writer's type when present: the start and use stamps
# and the occupancy `_fresh_record` and `_observe` write (an int count or the
# "" placeholder), and the compaction cursor and baselines
# `_observe_compaction` folds in (`request_prompt` null until a prompt is
# seen). A full record written before scopes (no `scope`) or compaction fields
# still is one; a field no consumer reads is free. Nested values are declared
# too: the LEASE, on any variant, as `_hold` and `take_warm_lease` write it (a
# non-empty `holder` str and a numeric `until`), and `judged`'s items, the
# work-item id strs `_observe` appends.
_IDENTITY = {"family": str, "route_id": str}


def _nonempty_str(value):
    """Whether `value` is a non-empty str (a lease holder, as its writers mint it).

    Implements: SR-239, LLR-270
    """
    return isinstance(value, str) and value != ""


_LEASE = {"holder": _nonempty_str, "until": (int, float)}
_ENVELOPE = {"scope": str, "lease": _LEASE}
_RETIREMENT = {"state": str, "reset_reason": str}
_SESSION = {
    "session_id": str,
    "generation": int,
    "governing_hash": str,
    "cli_version": str,
    "judged": [str],
}
_OPTIONAL = {
    "started": str,
    "window": (int, str),
    "occupancy": (int, str),
    "pct": (int, str),
    "last_used": str,
    "last_used_epoch": (int, float),
    "rollout_requests": int,
    "request_prompt": (int, type(None)),
    "input_total": int,
    "compaction_source": str,
    "compacted": bool,
}
LEASE_ONLY, RETIRED_FIRST, FULL_RECORD = "lease-only", "retired-first", "full"
_STATES = (STATE_ACTIVE, STATE_DRAINING, STATE_RETIRED)


def _read_record(path):
    """The record at `path`, or None: THE STORE'S ONE RECORD READER, the JSON
    trust boundary every load and scan reads through (`store_load`,
    `scoped_route`, `retire_scope`, `due_routes`), so nothing downstream
    re-decides validity. A record is returned only when it is a JSON object
    of one of the declared variants (`_variant`: lease-only, retired-first or
    full, each with every field its consumers read, typed) filed under its
    OWN name (`_record_name` of its identity). Anything else, an absent,
    unreadable, malformed or misfiled file, is no record, and a call that
    would have resumed it mints (WI-887's Trust ruling).

    Implements: SR-227, SR-239, LLR-270
    """
    try:
        record = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not _variant(record):
        return None
    own = _record_name(record["family"], record["route_id"], record.get("scope"))
    return record if Path(path).name == own else None


def _typed(record, fields, required):
    """Whether every field of `fields` present in `record` meets its spec
    (`_conforms`), and, when `required`, every one is present."""
    if required and not set(fields) <= set(record):
        return False
    return all(_conforms(record[k], t) for k, t in fields.items() if k in record)


def _conforms(value, spec):
    """Whether `value` meets one declared field spec: a type or tuple of
    types; a nested declaration (a dict, every field required); a one-item
    list, every item meeting its spec; or a predicate.

    Implements: SR-239, LLR-270
    """
    if isinstance(spec, dict):
        return isinstance(value, dict) and _typed(value, spec, True)
    if isinstance(spec, list):
        return isinstance(value, list) and all(_conforms(v, spec[0]) for v in value)
    if isinstance(spec, (type, tuple)):
        return isinstance(value, spec)
    return spec(value)


def _variant(record):
    """The declared variant a parsed record is (`LEASE_ONLY`, `RETIRED_FIRST`
    or `FULL_RECORD`), or "" for none: the reader's one shape rule.

    Implements: SR-227, SR-239, LLR-270
    """
    if not isinstance(record, dict) or not _typed(record, _IDENTITY, True):
        return ""
    if not _typed(record, _ENVELOPE, False):
        return ""
    if set(_SESSION) & set(record):
        full = _typed(record, {**_RETIREMENT, **_SESSION}, True)
        full = full and _typed(record, _OPTIONAL, False)
        return FULL_RECORD if full and record["state"] in _STATES else ""
    keys = set(record) - set(_IDENTITY) - set(_ENVELOPE)
    if not keys:
        return LEASE_ONLY
    retired = keys == set(_RETIREMENT) and _typed(record, _RETIREMENT, True)
    return RETIRED_FIRST if retired and record["state"] == STATE_RETIRED else ""


def _load_path(path, family, route_id, scope=""):
    record = _read_record(path)
    if record is None:
        return None
    same = (
        record.get("family"),
        record.get("route_id"),
        record.get("scope", ""),
    ) == ((family or "").upper(), route_id or "", scope or "")
    return record if same else None


def _write_whole(path, text):
    """Write `text` to `path` through its own temporary file and a replace."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=path.stem, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    os.replace(tmp, path)


def is_lease_only(record):
    """Whether `record` holds no session yet: only its identity and, while a
    first call mints, that call's lease (see `_hold`): the declared lease-only
    variant (`_variant`).

    Implements: SR-227, LLR-270
    """
    return _variant(record) == LEASE_ONLY


# --- the store marker: the one lockless carrier (WI-858) ---------------------------
#
# Every lease release and every bookkeeping write is PUBLISHED first, with no
# lock, as a marker beside its record, then applied under the lock if the lock
# is had within APPLY_WAIT; past that the marker stands for the next locked
# read. A marker is written once under its own name (the record's stem and a
# hash of its publisher id), applied by a locked reader and then deleted by
# that name only, so no reader drops a publication it has not applied. The
# reset decision is not in the marker: it is computed when the marker is
# applied (`fold_marker`), by the same rule for the locked reader, which saves
# it, and the lockless readers, which only decide on it.

MARKER_SUFFIX = ".mark"
BOOKKEEP, RELEASE, RETIRE = "bookkeep", "release", "retire"
# Implements: SR-227, LLR-270
APPLY_WAIT = 1.0  # seconds a producer waits for the lock to apply its marker


def _compaction_seen(value):
    """Whether `value` is a call's compaction observation as the codex
    adapter returns it (`_observe_compaction` reads it), or None for none.

    Implements: SR-227, LLR-270
    """
    return value is None or _conforms(value, _COMPACTION)


_COMPACTION = {"reported": bool, "prompts": [int], "totals": [int]}
_METRICS = {
    "ended-at": str,
    "context-used": (int, str),
    "context-window": (int, str),
    "context-pct": (int, str),
}
_OBSERVATION = {
    "minted": str,
    "usable": bool,
    "metrics": _METRICS,
    "epoch": (int, float),
    "compaction": _compaction_seen,
    "wi": str,
    "governing": str,
    "cli_version": str,
    "reset_at": int,
}
_MARKER = {
    "family": str,
    "route_id": str,
    "scope": str,
    "publisher": _nonempty_str,
    "session_id": str,
    "generation": int,
    "kind": str,
    "published": (int, float),
}
_KIND_FIELDS = {
    BOOKKEEP: {"observation": _OBSERVATION},
    RELEASE: {},
    RETIRE: {"reason": str},
}


def _marker_name(family, route_id, scope, publisher):
    """The file one publisher's marker on one record is filed under: the
    record's stem, a hash of the publisher id and `MARKER_SUFFIX`, which no
    record glob matches. Each publication has its own name.

    Implements: SR-227, LLR-270
    """
    stem = _record_name(family, route_id, scope)[: -len(".json")]
    tag = hashlib.sha256(publisher.encode("utf-8")).hexdigest()[:16]
    return "{}.{}{}".format(stem, tag, MARKER_SUFFIX)


def keep_marker(keep, kind, **payload):
    """The marker a call publishes: its record's identity, its lease holder
    as the publisher id, the session id and generation it held, the `kind`
    and that kind's `payload`.

    Implements: SR-227, LLR-270
    """
    return {
        "family": keep.family,
        "route_id": keep.route_id,
        "scope": keep.scope or "",
        "publisher": keep.holder,
        "session_id": keep.session_id,
        "generation": keep.generation,
        "kind": kind,
        **payload,
    }


def publish_marker(root, body):
    """Publish one marker WITHOUT the store lock: `body` stamped with its
    publication time, written whole (`_write_whole`) under its own name. A
    failed write raises OSError before the replace and leaves no marker (a
    leftover `*.tmp` matches no glob).

    Implements: SR-227, LLR-270
    """
    body = {**body, "published": time.time()}
    name = _marker_name(
        body["family"], body["route_id"], body["scope"], body["publisher"]
    )
    _write_whole(store_dir(root) / name, json.dumps(body, sort_keys=True))


class Pending(NamedTuple):
    """A record's markers as read (`_pending`): the well-formed ones as
    `(path, marker)` in publication order, and the paths that could not be
    read (an OSError) or were malformed.

    Implements: SR-227, LLR-270
    """

    markers: list
    unreadable: list
    malformed: list


def _pending(root, identity):
    """The markers beside the record of `identity` (`(FAMILY, route_id,
    scope)`), read and never deleted.

    Implements: SR-227, LLR-270
    """
    stem = _record_name(*identity)[: -len(".json")]
    found = Pending([], [], [])
    for path in store_dir(root).glob(stem + ".*" + MARKER_SUFFIX):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            found.unreadable.append(path)
            continue
        marker = _parse_marker(text, path, identity)
        if marker is None:
            found.malformed.append(path)
        else:
            found.markers.append((path, marker))
    found.markers.sort(key=lambda item: (item[1]["published"], item[0].name))
    return found


def _parse_marker(text, path, identity):
    """The marker `text` holds, or None when it is malformed: not a JSON
    object with every declared field of its kind, typed, or naming another
    record than `identity`, or filed under another name than its own.

    Implements: SR-227, LLR-270
    """
    try:
        marker = json.loads(text)
    except ValueError:
        return None
    if not (isinstance(marker, dict) and _typed(marker, _MARKER, True)):
        return None
    fields = _KIND_FIELDS.get(marker["kind"])
    if fields is None or not _typed(marker, fields, True):
        return None
    named = (marker["family"], marker["route_id"], marker["scope"])
    own = _marker_name(*named, marker["publisher"])
    return marker if named == identity and path.name == own else None


def fold_marker(record, marker):
    """`(record, columns)`: `record` with one marker applied, the record
    given left unchanged; None is no record. THE ONE RULE both readers
    apply: a `release` drops its publisher's lease; a `retire` retires the
    live session and generation it names, then does the same; a `bookkeep`
    lands the call's observation (`_fold_bookkeep`). A lease-only record
    left with no lease is no record (a first mint stored nothing). `columns`
    are a bookkeeping call's `session-gen`, `reset-reason` and compaction
    columns.

    Implements: SR-227, LLR-270
    """
    record = copy.deepcopy(record)
    if marker["kind"] == BOOKKEEP:
        return _fold_bookkeep(record, marker)
    if marker["kind"] == RETIRE and _names_session(record, marker):
        _retire(record, marker["reason"] or "session unusable")
    return _released(record, marker["publisher"]), {}


def fold_markers(record, markers):
    """`(record, applied)`: `fold_marker` over `markers` in order, and each
    publisher's columns.

    Implements: SR-227, LLR-270
    """
    applied = {}
    for marker in markers:
        record, applied[marker["publisher"]] = fold_marker(record, marker)
    return record, applied


def _names_session(record, marker):
    """Whether `record` is live on the session and generation `marker`
    names (a newer session on the record is not)."""
    return (
        isinstance(record, dict)
        and marker["session_id"] != ""
        and record.get("session_id") == marker["session_id"]
        and record.get("generation") == marker["generation"]
        and record.get("state") in (STATE_ACTIVE, STATE_DRAINING)
    )


def _released(record, holder):
    """`record` without `holder`'s lease; a lease-only record left with no
    lease is None.

    Implements: SR-227, LLR-270
    """
    if not isinstance(record, dict):
        return None
    if (record.get("lease") or {}).get("holder") == holder:
        record.pop("lease", None)
    return None if is_lease_only(record) and "lease" not in record else record


def _fold_bookkeep(record, marker):
    """Land a call's observation under `_landing`'s rule, decide its reset
    (`_reset_after`) and release its lease (the landed record carries it,
    by `_landing`'s rule); a marker that no longer lands releases its
    holder's lease, if still held, and is otherwise spent (inert)."""
    keep, seen = _marker_keep(marker), marker["observation"]
    landed = _landing(record, keep, seen["minted"], seen["metrics"]["ended-at"])
    if landed is None:
        moved = {"session-gen": "", "reset-reason": "store moved on"}
        return _released(record, keep.holder), moved
    columns = _observe_compaction(landed, seen["compaction"], not keep.session_id)
    _observe(landed, keep, seen["metrics"], seen["epoch"])
    _reset_after(landed, seen, keep.governing)
    landed.pop("lease", None)
    gen, reason = landed["generation"], landed["reset_reason"]
    return landed, {"session-gen": gen, "reset-reason": reason, **columns}


def _marker_keep(marker):
    """The call a bookkeeping marker stands for, as `_landing` and `_observe`
    read it (no launch: nothing prepared)."""
    seen = marker["observation"]
    return Keep(
        family=marker["family"],
        route_id=marker["route_id"],
        session_id=marker["session_id"],
        wi=seen["wi"],
        governing=seen["governing"],
        cfg=None,
        prepared=None,
        holder=marker["publisher"],
        cli_version=seen["cli_version"],
        generation=marker["generation"],
        scope=marker["scope"],
    )


def _reset_after(record, seen, governing):
    """The reset rules after a call: no session id or an unusable session
    retires at once; an occupancy at the call's dial drains."""
    if not record["session_id"]:
        _retire(record, "session id unavailable")
    elif not seen["usable"]:
        _retire(record, "session unusable")
    else:
        reason = drain_reason(record, record["pct"], seen["reset_at"], governing)
        if reason:
            record["state"], record["reset_reason"] = STATE_DRAINING, reason


class Honoured(NamedTuple):
    """One locked read (`load_honoured`): the record as it now stands, the
    one clock read its decision uses, each applied publisher's columns, and
    whether an unreadable marker held back the stale-lease rule.

    Implements: SR-227, LLR-270
    """

    record: object
    clock: float
    applied: dict
    blocked: bool


def load_honoured(root, family, route_id, scope="", holder=""):
    """The LOCKED READ of one record (callers hold `store_lock`): read the
    clock first, then list the record's markers, apply each in publication
    order, then retire an expired lease another holder than `holder` left
    (`retire_stale_lease`), so no reader retires a lease whose release was
    published before it observed the lease expired. The record is saved (or
    removed) when it changed; each applied or spent marker is then deleted
    by name. An unreadable marker is left in place and this read retires no
    expired lease; a malformed one is deleted with one stderr line.

    Implements: SR-227, LLR-270
    """
    clock = time.time()
    pending = _pending(root, ((family or "").upper(), route_id or "", scope or ""))
    before = store_load(root, family, route_id, scope)
    markers = [marker for _, marker in pending.markers]
    record, applied = fold_markers(copy.deepcopy(before), markers)
    blocked = bool(pending.unreadable)
    if not blocked:
        retire_stale_lease(record, holder, clock)
    if record is not None and record != before:
        store_save(root, record)
    elif record is None and before is not None:
        store_remove(root, before)
    _spend(pending)
    return Honoured(record, clock, applied, blocked)


def _spend(pending):
    """Delete each applied marker, and each malformed one with one stderr
    line, by its own name."""
    for path in pending.malformed:
        print(
            "keep: deleted malformed store marker {}".format(path.name), file=sys.stderr
        )
    for path in [p for p, _ in pending.markers] + pending.malformed:
        try:
            path.unlink()
        except OSError:
            pass  # left for the next locked read, which applies it again


def _folded(root, record):
    """A record read WITHOUT the lock, with its markers folded in by the
    locked reader's rule (`fold_markers`) and none deleted; an unreadable
    or malformed marker is read as absent.

    Implements: SR-227, LLR-270
    """
    if record is None:
        return None
    identity = (record["family"], record["route_id"], record.get("scope", ""))
    markers = [marker for _, marker in _pending(root, identity).markers]
    return fold_markers(record, markers)[0]


def _apply_now(root, identities):
    """Apply what a producer just published: the locked reads of
    `identities` if the lock is had within `APPLY_WAIT`, else None (the
    markers stand for the next locked read)."""
    try:
        with store_lock(root, wait=APPLY_WAIT):
            return [load_honoured(root, *identity) for identity in identities]
    except StoreBusy:
        return None


def _identity(keep):
    return (keep.family, keep.route_id, keep.scope or "")


def keep_release(root, keep):
    """Release the call's lease and leave its session's record as it was:
    the end of a call whose failure says nothing about the session (the
    runner refused its credential, or the blackout refused the launch). A
    `release` marker is published first, then applied if the lock is had
    within `APPLY_WAIT`; a first mint's lease-only record is removed, so the
    next call mints. A failed publication raises OSError.

    Implements: SR-227, LLR-270
    """
    publish_marker(root, keep_marker(keep, RELEASE))
    _apply_now(root, [_identity(keep)])


def _record_path(root, record):
    """The file a record lives in: its family, route and scope."""
    family, route_id = record["family"], record["route_id"]
    return _store_path(root, family, route_id, record.get("scope", ""))


def store_save(root, record):
    """Write a record whole: its own temporary file beside it, then a replace,
    so no reader ever sees half of one and no two writers share a temp path.
    Callers hold `store_lock`."""
    _write_whole(_record_path(root, record), json.dumps(record, sort_keys=True))


def store_remove(root, record):
    """Remove a record's file. Callers hold `store_lock`.

    Implements: SR-227, LLR-270
    """
    try:
        _record_path(root, record).unlink()
    except OSError:
        pass


def dedicated_home(root, family):
    """`(variable, path)` of the dedicated CLI home for `family` under the
    store's `home/`, WITHOUT creating it, or None for a family with no ruled
    home variable: the one path rule, read by the launch and by the sign-in
    probe, which must not leave an empty home behind.

    Implements: SR-227, LLR-305
    """
    variable = HOME_VARIABLES.get((family or "").upper())
    if not variable:
        return None
    return variable, store_dir(root) / "home" / (family or "").lower()


def dedicated_home_env(root, family):
    """The dedicated CLI home for `family` while retention is on, created if
    absent: `{variable: path}` under the store's `home/`, or `{}` for a family
    with no ruled home variable.

    Implements: SR-227, LLR-270
    """
    home = dedicated_home(root, family)
    if home is None:
        return {}
    variable, path = home
    path.mkdir(parents=True, exist_ok=True)
    return {variable: str(path)}


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
    holds, the dedicated home its launch runs under, and its `prepared`
    launch: the session service's validated environment and credential
    (`session_service.prepare_launch`), REQUIRED, so no retained launch can be
    built without that validation; never stored, logged or shown in a repr."""

    family: str
    route_id: str
    session_id: str
    wi: str
    governing: str
    cfg: KeepConfig
    prepared: object = field(repr=False)
    holder: str = ""
    cli_version: str = ""
    generation: int = 0
    home_env: dict = field(default_factory=dict)
    scope: str = ""


def _lease_held(record, holder, now):
    """The holder of a live lease someone else owns, else ""."""
    lease = record.get("lease") if isinstance(record, dict) else None
    if not isinstance(lease, dict) or lease.get("holder") in ("", holder):
        return ""
    until = lease.get("until")
    if not isinstance(until, (int, float)) or until <= now:
        return ""  # an expired lease: its holder died or overran
    return lease.get("holder") or ""


def _busy(found, holder):
    """Who holds a locked read's record (`Honoured`) against `holder`: a
    live lease's holder; while an unreadable marker holds back the
    stale-lease rule, any other holder's lease, expired or not, which may
    have been released; else "".

    Implements: SR-227, LLR-270
    """
    held = _lease_held(found.record, holder, found.clock)
    record = found.record if isinstance(found.record, dict) else {}
    lease = record.get("lease") if found.blocked and not held else None
    if isinstance(lease, dict) and lease.get("holder") not in ("", holder):
        return "an unreadable store marker"
    return held


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


def retire_after_blackout(root, record):
    """Retire a live session (active or draining) whose last use is before
    the end of the most recent blackout window that ended at or before now
    (`agent_common.blackout_at`), or that records no last use: its prompt
    cache did not outlive the window, so resuming it would replay the whole
    transcript uncached, which costs more than a fresh session reading only
    its brief. The reset reason is `blackout`, and it overrides a draining
    session's chain continuity. Nothing runs at the window's start: this is
    the lazy retirement, at the first keep call or keep-warm tick after the
    window. Returns whether it retired.

    Implements: SR-227, LLR-270
    """
    if not isinstance(record, dict):
        return False
    if record.get("state") not in (STATE_ACTIVE, STATE_DRAINING):
        return False
    last_end = agent_common.blackout_at(Path(root) / "docs").last_end_epoch
    used = record.get("last_used_epoch")
    if last_end is None or (isinstance(used, (int, float)) and used >= last_end):
        return False
    _retire(record, "blackout")
    return True


def _before_launch(cfg, record, wi, governing, version, rows):
    """The pre-launch reset rules on a live record (see `keep_for`). A
    scoped (loop review) record's every round is a clear point: the
    same-artifact guard is the adjudicator's and passes it by, and a draining
    review session retires at its next call."""
    judged = record.get("judged") or []
    scoped = bool(record.get("scope"))
    if cfg.reset_on_same_artifact and not scoped and wi in judged:
        _retire(record, "same-artifact guard")
        return
    reason = drain_reason(record, None, 0, governing, version)
    if reason:
        record["state"], record["reset_reason"] = STATE_DRAINING, reason
    clear = scoped or is_clear_point(rows, judged, wi)
    if record["state"] == STATE_DRAINING and clear:
        _retire(record, record.get("reset_reason") or "drained")


def applies(cfg, role, brief, route_id, scope=""):
    """Whether the keep operation covers this call at all, on a named route:
    an adjudication of a retained class under the adjudicator's dial, with no
    scope; or a loop review round under the review dial (WI-887), with the
    scope it is kept under. A review with no scope is never kept: it would
    share the route's adjudicator record.

    Implements: SR-227, LLR-270
    """
    if not route_id:
        return False
    if role in kverdict.REVIEW_PHASES:
        return cfg.review_reset_pct > 0 and bool(scope)
    return (
        cfg.enabled and role == "ADJUDICATE" and not scope and brief in cfg.retain_for
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
    prepared,
    scope="",
):
    """The retained session an adjudication, or a loop review round under
    `scope` (WI-887), resumes or mints, or None. The Keep carries `prepared`,
    the call's validated launch, and `scope`, which keys its record: a record
    under another scope is never resumed.

    None, touching nothing, when the layer does not apply (`applies`): the
    dial is off, the role is neither ADJUDICATE of a retained class with no
    scope nor a review round with one, or no route is named. Otherwise,
    before the launch and under the store lock:

      - a retired, absent or lease-only record mints (`session_id` "");
      - with the same-artifact guard on, a session that already judged this
        work item retires, so the rejudgement is fresh;
      - a changed governing input or runner version drains an active session;
      - a draining session retires at a clear point (`is_clear_point`, over
        the work-item `rows`) and is otherwise resumed, so a review, rework,
        re-review round trip is never cut mid-way; a scoped (review) session
        is at a clear point at every round, so it retires at once;
      - the call takes the route's lease for `lease_seconds`, so a keep-warm
        ping cannot resume the same session while it runs. On a route with no
        record it writes a lease-only record (`is_lease_only`), so a second
        first call cannot mint beside it. A lease another call holds is
        waited on up to `lease_wait` seconds; past that the adjudication runs
        unretained (None) and says why.

    Implements: SR-227, LLR-270
    """
    if not applies(cfg, role, brief, route_id, scope):
        return None
    governing = governing_hash(root, template_paths, template_texts)
    holder = role.lower() + ":" + uuid.uuid4().hex
    deadline = time.monotonic() + lease_wait
    while True:
        try:
            with store_lock(root):
                # ONE clock read per locked decision (`load_honoured` reads
                # it first): two reads could see a lease live to the retire
                # rule and free to the busy rule.
                found = load_honoured(root, family, route_id, scope, holder)
                busy = _busy(found, holder)
                if not busy:
                    return _hold(
                        root,
                        cfg,
                        found.record,
                        (family, route_id, scope, wi, governing, cli_version),
                        rows,
                        (holder, found.clock + lease_seconds),
                        prepared,
                    )
        except StoreBusy:
            busy = "the store lock"
        if time.monotonic() >= deadline:
            print(
                "keep [{}]: held by {}; this {} call runs unretained".format(
                    route_id, busy, role
                ),
                file=sys.stderr,
            )
            return None
        time.sleep(1.0)


def _hold(root, cfg, record, subject, rows, lease, prepared):
    """Apply the pre-launch rules, take the lease `(holder, until)`, and
    build the Keep. A route with no record gets a lease-only one, so the
    first mint holds the lease as every later call does."""
    family, route_id, scope, wi, governing, version = subject
    holder, until = lease
    # Live means a session to resume: a retired record, and a lease-only one
    # (no session yet, no state), mint.
    live = record is not None and record.get("state") in (STATE_ACTIVE, STATE_DRAINING)
    if live and not retire_after_blackout(root, record):
        _before_launch(cfg, record, wi, governing, version, rows)
    live = live and record.get("state") != STATE_RETIRED
    if record is None:
        record = {"family": (family or "").upper(), "route_id": route_id or ""}
        record.update({"scope": scope} if scope else {})
    record["lease"] = {"holder": holder, "until": until}
    store_save(root, record)
    return Keep(
        family=(family or "").upper(),
        route_id=route_id,
        session_id=(record.get("session_id") or "") if live else "",
        wi=wi or "",
        governing=governing,
        cfg=cfg,
        prepared=prepared,
        holder=holder,
        cli_version=version or "",
        generation=record.get("generation", 0),
        home_env=dedicated_home_env(root, family),
        scope=scope or "",
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
    scoped = {"scope": keep.scope} if keep.scope else {}
    return {
        **scoped,
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
    moved on (that record is left alone). A call's observation lands only
    while the record still carries ITS OWN lease (taken in `_hold`, expired
    or not), and a resumed call's only on the live session and generation it
    resumed. Landing drops that lease in the same whole-record write, so the
    lease is the store's record that this call is not yet consumed: a
    replayed marker (one a failed unlink left) finds no lease of its own and
    lands nothing, and an overrun call whose lease another call took over
    never touches that call's record (in flight or completed).

    Implements: SR-227, LLR-270
    """
    lease = current.get("lease") if isinstance(current, dict) else None
    if not isinstance(lease, dict) or lease.get("holder") != keep.holder:
        return None
    if keep.session_id:
        resumed = {"session_id": keep.session_id, "generation": keep.generation}
        return current if _names_session(current, resumed) else None
    prior = max(keep.generation, current.get("generation", 0))
    return _fresh_record(keep, session_id, prior, stamp)


def _unusable(outcome, reported_error):
    return outcome.code != 0 or bool(outcome.timed_out) or bool(reported_error)


def keep_bookkeep(
    root,
    keep,
    minted,
    outcome,
    reported_error=False,
    *,
    compaction=None,
    auth_failed=False,
):
    """Fold one retained call into its record and decide its reset: an
    unusable session (a non-zero exit, a timeout, an error the runner
    reported) retires at once; one whose occupancy reached the dial drains.
    Releases the lease. The call's raw observation is PUBLISHED first as a
    `bookkeep` marker (`publish_marker`), then applied if the store lock is
    had within `APPLY_WAIT` (`fold_marker` decides the reset there); under
    contention the marker stands for the next locked read, so the
    observation and the release are never lost and never raise StoreBusy.
    Returns the call's `session-gen` and `reset-reason` columns: when the
    apply was deferred, `reset-reason` is `pending` and `session-gen` the
    call's own. A call whose credential the runner refused (`auth_failed`)
    failed, but not its session: only its lease is released
    (`keep_release`), and the record stays as it was. A failed publication
    raises OSError.

    Implements: SR-227, LLR-270
    """
    if auth_failed:
        keep_release(root, keep)
        generation = keep.generation if keep.session_id else ""
        return {"session-gen": generation, "reset-reason": ""}
    seen = _observation(keep, minted, outcome, reported_error, compaction)
    publish_marker(root, keep_marker(keep, BOOKKEEP, observation=seen))
    done = _apply_now(root, [_identity(keep)])
    columns = done[0].applied.get(keep.holder) if done else None
    if columns is None:
        own = keep.generation if keep.session_id else keep.generation + 1
        return {"session-gen": own, "reset-reason": "pending"}
    return columns


def _observation(keep, minted, outcome, reported_error, compaction):
    """A finished call's raw observation, as a `bookkeep` marker carries it:
    the session id it reported, whether the session is usable, the metrics
    the bookkeeping reads, when it was used, the codex compaction
    observation, the judged work item, and the inputs and dial it ran
    under.

    Implements: SR-227, LLR-270
    """
    m = outcome.metrics
    return {
        "minted": minted or m.get("session-id") or "",
        "usable": not _unusable(outcome, reported_error),
        "metrics": {key: m.get(key, "") for key in _METRICS},
        "epoch": time.time(),
        "compaction": compaction or None,
        "wi": keep.wi or "",
        "governing": keep.governing or "",
        "cli_version": keep.cli_version or "",
        "reset_at": reset_pct(keep.cfg, keep.family, keep.scope),
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


def _observe(record, keep, m, epoch):
    """Copy one call's occupancy and use (at `epoch`) into its record."""
    for key, column in (("occupancy", "context-used"), ("window", "context-window")):
        if m.get(column, "") != "":
            record[key] = m[column]
    record["pct"] = m.get("context-pct", "")
    record["last_used"] = m["ended-at"]
    record["last_used_epoch"] = epoch
    if keep.wi and keep.wi not in record["judged"]:
        record["judged"].append(keep.wi)


def keep_abandon(root, keep, reason):
    """A retained launch raised before it could be bookkept: retire the
    session it resumed (its transcript state is unknown) and release the
    lease. The retirement is GUARANTEED: a `retire` marker naming the
    session, its generation and `reason` is published first, with no lock
    needed, and then applied if the store lock is had within `APPLY_WAIT`;
    if it is not, the next locked read of the record applies it. A mint that
    raised has no session to retire: its lease-only record is removed.

    Implements: SR-227, LLR-270
    """
    publish_marker(root, keep_marker(keep, RETIRE, reason=reason))
    _apply_now(root, [_identity(keep)])


# --- scoped records: a lane's review sessions (WI-887) ----------------------------


def _scoped_records(root, scope):
    """Every record kept under `scope`, read without the lock (whole records
    only) through the store's one reader (`_read_record`), so a malformed or
    misfiled file is no record here as everywhere, each with its pending
    markers folded in (`_folded`)."""
    found = []
    for path in sorted(store_dir(root).glob("*.json")):
        record = _read_record(path)
        if record is not None and scope and record.get("scope") == scope:
            record = _folded(root, record)
            found.extend([record] if record is not None else [])
    return found


def scoped_route(root, scope):
    """The route id of the live session kept under `scope`, or None: the
    route a lane's next review round of that scope pins, so it resumes the
    reviewer that served the round before. A record whose pending markers
    retire it pins nothing.

    Implements: SR-227, SR-239, LLR-270
    """
    for record in _scoped_records(root, scope):
        if record.get("state") in (STATE_ACTIVE, STATE_DRAINING):
            return record["route_id"]
    return None


def retire_scope(root, scope, reason):
    """Retire every live session kept under `scope`, with `reset_reason`
    `reason`: the loop retires a lane's iteration reviewer when that lane's
    gating round is drawn, so the next iteration mints. It holds no lease
    and releases none: per live record its lockless read finds, it publishes
    one `retire` marker under a fresh publisher id (`scope-retire:<uuid>`)
    naming the session id and generation it read, then applies them if the
    store lock is had within `APPLY_WAIT`; a deferred apply needs nothing
    more, since the lockless readers fold the marker. A failed publication
    raises OSError to the caller.

    Implements: SR-227, SR-239, LLR-270
    """
    identities = []
    for found in _scoped_records(root, scope):
        if found.get("state") not in (STATE_ACTIVE, STATE_DRAINING):
            continue
        identity = (found["family"], found["route_id"], scope)
        body = dict(zip(("family", "route_id", "scope"), identity))
        body.update(publisher="scope-retire:" + uuid.uuid4().hex, kind=RETIRE)
        body.update(session_id=found["session_id"], generation=found["generation"])
        publish_marker(root, {**body, "reason": reason})
        identities.append(identity)
    if identities:
        _apply_now(root, identities)


# The two stages a lane's review session is kept under; the final stage's
# name is the review-scope kind its full round records (`kverdict.FINAL`).
ITERATION, FINAL = "iteration", kverdict.FINAL


class ReviewRetention(NamedTuple):
    """What a loop review round's draw settles (`review_retention`): the
    `scope` its session is kept under ("" runs it unretained), the `stage`
    that scope was composed for (`ITERATION`, `FINAL`, or "" for none), which
    the round's recorded review scope is derived from
    (`kverdict.format_scope`), and the route ids its draw should prefer.

    Implements: SR-227, SR-239, LLR-270
    """

    scope: str = ""
    stage: str = ""
    pin: tuple = ()


def review_retention(root, worker, phase, narrow):
    """The `ReviewRetention` for one loop review round of `phase` on
    `worker`'s lane.

    The scope is `<train>@<claim base>:<phase>:<stage>`, verbatim, so no
    lane, re-claim or phase resumes another's transcript. A NARROW round
    (`narrow`) is an iteration round: it is kept under the `iteration` stage.
    A FULL round is the gating round: drawing it retires the lane's iteration
    session for the phase, and it runs unretained in fresh mode (the
    default) or under the `final` stage in persisted mode, which an
    iteration round never uses. Whatever the stage, the scope is settled
    first and its pin is composed once from it (`scoped_route`): the route of
    that scope's live session, so an iteration round and a gating round in
    persisted mode alike resume their own reviewer; an unavailable pinned
    route falls through the draw's ordinary selection. With the review dial
    off, for a lane with no readable claim base, and for a phase that is not
    a review phase, nothing is kept and nothing is touched.

    Implements: SR-227, SR-239, LLR-270
    """
    if phase not in kverdict.REVIEW_PHASES:
        return ReviewRetention()
    cfg = keep_config(root)
    claim = (worker or {}).get("claim")
    if not (cfg.review_reset_pct and claim):
        return ReviewRetention()
    lane = "{}@{}:{}".format(worker.get("train") or "", claim, phase)
    iteration = "{}:{}".format(lane, ITERATION)
    if narrow:
        stage = ITERATION
    else:
        retire_scope(root, iteration, "gating round drawn")
        persisted = cfg.final_reviewer == kconfig.FINAL_PERSISTED
        stage = FINAL if persisted else ""
    scope = "{}:{}".format(lane, stage) if stage else ""
    route = scoped_route(root, scope)
    return ReviewRetention(scope, stage, (route,) if route else ())


# --- keep-warm --------------------------------------------------------------------


def _prepare_warm(prepare, route_id, record):
    """`(prepared, reason)` for a due record's ping: the route's prepared
    launch, refused when `prepare` refuses it or when the prepared row names
    another family than the record's session, which is then never warmed
    (one family's session never runs under another family's home).

    Implements: SR-227, LLR-270
    """
    prepared, refused = prepare(route_id)
    if not refused and prepared.family != record.get("family"):
        refused = "route {} now names family {}; its {} session is not warmed".format(
            route_id, prepared.family, record.get("family")
        )
    return prepared, refused


def _warm_keep(root, cfg, record, holder, prepared):
    """The Keep a keep-warm ping launches under: the leased record's session,
    under the prepared row's family and home (`_prepare_warm` has matched
    them).

    Implements: SR-227, LLR-270
    """
    return Keep(
        family=prepared.family,
        route_id=record.get("route_id") or "",
        session_id=record.get("session_id") or "",
        wi="",
        governing=record.get("governing_hash") or "",
        cfg=cfg,
        prepared=prepared,
        holder=holder,
        cli_version=record.get("cli_version") or "",
        generation=record.get("generation", 0),
        home_env=dedicated_home_env(root, prepared.family),
    )


def keepwarm_due(record, cfg, now, work_pending):
    """Whether a keep-warm ping is due: the dial and `keepwarm_minutes` are
    on, the session is ANTHROPIC's (the only family whose prompt cache lives
    an hour; the others' live minutes and are never pinged) and active, it
    is the adjudicator's (a scoped review record is never pinged), work is
    pending, and it has been idle `keepwarm_minutes`. No ping fires inside
    the blackout window (`take_warm_lease`, owner 2026-10-05, overruling OI-69
    (c2)): a session idle across the window is retired after it instead.

    Implements: SR-227, LLR-270
    """
    if not (cfg.enabled and cfg.keepwarm_minutes > 0 and work_pending):
        return False
    if not isinstance(record, dict) or record.get("family") != "ANTHROPIC":
        return False
    if record.get("scope") or record.get("state") != STATE_ACTIVE:
        return False
    last = record.get("last_used_epoch")
    if not isinstance(last, (int, float)):
        return False
    return now - last >= cfg.keepwarm_minutes * 60


def due_routes(root, cfg, now, work_pending):
    """The route ids whose retained session is due a keep-warm ping, read
    without the lock (a read of whole records only) through the store's one
    reader (`_read_record`), each with its pending markers folded in
    (`_folded`): a malformed or misfiled record is never due, one a pending
    marker retires is never due, and a pending bookkeeping or release
    marker never makes a record skipped.

    Implements: SR-227, LLR-270
    """
    due = []
    for path in sorted(store_dir(root).glob("ANTHROPIC-*.json")):
        record = _folded(root, _read_record(path))
        if keepwarm_due(record, cfg, now, work_pending):
            due.append(record.get("route_id") or "")
    return due


def _warm_candidates(root, cfg, now, work_pending, routes):
    """The due routes a keep-warm tick may ping: none inside the blackout
    window, else `due_routes` narrowed to `routes` (None: every route).

    Implements: SR-227, LLR-270
    """
    if agent_common.blackout_at(Path(root) / "docs").inside:
        return []
    due = due_routes(root, cfg, now, work_pending)
    return [r for r in due if routes is None or r in routes]


def take_warm_lease(
    root, cfg, *, now, work_pending, holder, prepare, routes=None, lease_seconds=600
):
    """`(keep, reason)` for the next due keep-warm ping. `keep` holds the
    route's lease, so no adjudication resumes the session while the ping
    runs; `reason` names why a due ping cannot run now (the lease or the lock
    is held, or `prepare(route_id)`, which returns `(prepared, reason)` and
    is asked under the lock BEFORE any lease is taken, refused the launch:
    nothing is then held, so nothing needs releasing). `(None, None)` when
    nothing is due. With `routes`, only those route ids are considered (a
    route the registry no longer lists is never pinged).

    Inside the blackout window nothing is due. After one, a due session last
    used before the window's end is retired (`retire_after_blackout`) before
    any lease or ping, so no ping refreshes a stale session's last use. A
    session another call's live lease holds is not retired here: the lease
    is read first, under the same lock and clock read, and the session is
    left to that call, whose bookkept last use decides at the next keep
    (a due one returns the "leased to" reason).

    Implements: SR-227, LLR-270
    """
    due = _warm_candidates(root, cfg, now, work_pending, routes)
    if not due:
        return None, None
    try:
        with store_lock(root, wait=0.5):
            for route_id in due:
                # One clock read for this record's decision (`load_honoured`).
                found = load_honoured(root, "ANTHROPIC", route_id, holder=holder)
                record, clock = found.record, found.clock
                busy = _busy(found, holder)  # left to its holder
                if not busy and retire_after_blackout(root, record):
                    store_save(root, record)  # never pinged: retired
                if not keepwarm_due(record, cfg, now, work_pending):
                    continue
                if busy:
                    return None, "the session is leased to {}".format(busy)
                prepared, refused = _prepare_warm(prepare, route_id, record)
                if refused:
                    return None, refused
                record["lease"] = {"holder": holder, "until": clock + lease_seconds}
                store_save(root, record)
                return _warm_keep(root, cfg, record, holder, prepared), None
    except StoreBusy:
        return None, "the store lock is held"
    return None, None
