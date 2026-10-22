#!/usr/bin/env python3
"""codex_call.py — the coordinator's codex calls (a Sol review or critique, a
Terra turn) through the kit's session service.

  codex_call.py ROLE --prompt-file P --out O [--root DIR] [--wi WI-N]
      [--effort medium] [--route ENTRY] [--resume] [--timeout 7200]

  - ROLE is one of REVIEW-A, CRITIQUE (Sol) and AUTHOR (Terra; it names its
    work item with --wi). The role's enabled roster row (or the enabled
    entry --route names) gives the family, model, tier and route id; the
    launch template is this module's own (`launch_template`: the sandbox the
    retired shell wrappers used, unelevated and workspace-write, the primary
    checkout's review scratch root writable, the effort, and the prompt on
    stdin), never the row's own template.
  - Refused before launch, exit 2: an unknown role, `--resume` off AUTHOR,
    an AUTHOR turn naming no work item or one the lane does not hold
    claimed (another role's --wi is attribution only), an unreadable
    prompt, a route or launch environment that cannot be used, a bad resume carrier, and the
    service's own refusals (the blackout window, commit hooks off).
  - The change check compares the root's HEAD and uncommitted paths (each
    one's content on disk and its index state) before and after the call
    (`snapshot`, `read_span`, `judge_changes`). For Sol,
    any change is an edit except a commit that only adds standard-call
    session logs and the uncommitted logs such commits account for; for
    Terra, uncommitted changes are its output and only an undiscounted HEAD
    move is an edit. Exit 3 is an edit, its paths printed; exit 5 a check
    that could not run (git unreadable). The call runs through the service's
    own act-then-record (`session_service.call`), the check in its seam
    between the two, so its log is recorded even after an edit or a Ctrl-C,
    committed in a claimed lane or spooled outside one; exit 4 is a log whose
    commit was refused or whose spool could not be written, the log named.
    Exit 1 is a call that failed.
    Precedence after launch: 5 > 3 > 4 > 1 > 0.
  - `--resume` continues the thread of the lane's newest committed Terra log
    (`resume_carrier`, over the standard-call logs at HEAD in name order),
    refusing a missing, damaged, foreign, conflicting or newer-uncommitted
    carrier before launch, naming the log and the cause. It never reads an
    id typed into the decisions record and never starts a fresh thread in
    the carrier's place.

Stdlib only, Python 3.11+, Windows/POSIX. It imports the kit's scripts from
its own checkout, so a lane's copy runs that lane's service.
"""

import argparse
import json
import subprocess
import sys
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

KIT_SCRIPTS = Path(__file__).resolve().parents[2] / "project-trajectory" / "scripts"
if str(KIT_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(KIT_SCRIPTS))

import agent_common  # noqa: E402
import agent_route  # noqa: E402
import coordinator_adjudicate  # noqa: E402
import session_keep  # noqa: E402
import session_service  # noqa: E402
from kitlib.config import utf8_console  # noqa: E402

# Implements: SR-243, LLR-346
ROLES = ("REVIEW-A", "CRITIQUE", "AUTHOR")
# Implements: SR-243, LLR-346
ROLE_ROUTES = {
    "REVIEW-A": "OPENAI-SOL",
    "CRITIQUE": "OPENAI-SOL",
    "AUTHOR": "OPENAI-TERRA",
}
# The judge's three readings.
CLEAN, EDIT, UNABLE = "clean", "edit", "unable"
# The exit codes (the plan's decision 5).
EXIT_OK, EXIT_FAILED, EXIT_REFUSED, EXIT_EDIT, EXIT_UNRECORDED, EXIT_UNABLE = range(6)
# The loop's idle bound, so a wedged call ends as the loop's would.
IDLE_TIMEOUT = coordinator_adjudicate.IDLE_TIMEOUT
ITERATION = "docs/iteration/"
# The header fields a well-formed standard-call log carries, whatever its role.
CARRIER_FIELDS = ("role", "roster-row", "wi", "started-at")
RECOVERY = (
    " Nothing was launched. Commit or inspect the named log, or run a first "
    "turn without --resume."
)


@dataclass(frozen=True)
class Launch:
    """What a role launches: the enabled row's identity and model, and the
    declared template with its effort and scratch root filled.

    Implements: SR-243, LLR-346
    """

    route_id: str
    provider: str
    tier: str
    model: str
    template: str
    env: object = None


@dataclass(frozen=True)
class Snapshot:
    """The root as one read sees it: `head`, the HEAD commit (None when git
    cannot say), `paths`, every uncommitted or untracked path mapped to its
    content identity ("" for a path absent from disk; None when git cannot
    say), `tracked`, those of the paths HEAD already tracks (a modified or
    deleted file, never a new one), and `index`, the same paths mapped to
    their index state (`_status_entry`; None when git cannot say).

    Implements: SR-243, LLR-346
    """

    head: object
    paths: object
    tracked: frozenset = frozenset()
    index: object = field(default_factory=dict)


@dataclass(frozen=True)
class Commit:
    """One commit of the call's range: its `sha`, its `parents`, and its
    `changes`, `(status, path, blob)` triples (`diff-tree --no-renames -r`).

    Implements: SR-243, LLR-346
    """

    sha: str
    parents: tuple
    changes: tuple


@dataclass(frozen=True)
class Span:
    """The range from the before HEAD to the after HEAD: `descendant`, whether
    the after HEAD descends from the before HEAD, and `commits`, the range's
    commits (either None when git cannot say).

    Implements: SR-243, LLR-346
    """

    descendant: object
    commits: object


@dataclass(frozen=True)
class Verdict:
    """The change check's reading, CLEAN, EDIT or UNABLE, and the edited paths.

    Implements: SR-243, LLR-346
    """

    state: str
    edits: tuple = ()


@dataclass(frozen=True)
class Carrier:
    """A resumed turn's carrier: the session id it continues and the log it
    was read from, or the refusal naming the log and the cause.

    Implements: SR-243, LLR-346
    """

    session_id: str = ""
    path: str = ""
    refusal: str = ""


def parse_args(argv):
    """The command line.

    Implements: SR-243, LLR-346
    """
    p = argparse.ArgumentParser(prog="codex_call.py")
    p.add_argument("role")
    p.add_argument("--prompt-file", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--root", default=".")
    p.add_argument("--wi", default="")
    p.add_argument("--effort", default="medium")
    p.add_argument("--route", default="")
    p.add_argument("--resume", action="store_true")
    p.add_argument("--timeout", type=int, default=7200)
    return p.parse_args(argv)


# --- the route and the launch template ----------------------------------------


def scratch_root(root):
    """The review scratch root a call may write: `<checkout>.wt/review-tmp`
    beside the PRIMARY checkout of `root`, derived from the call's root and
    never from this script's location (a lane's copy runs from the lane)."""
    primary = session_keep.primary_out_dir(root).parent
    return primary.parent / (primary.name + ".wt") / "review-tmp"


def launch_template(runner, effort, scratch):
    """The declared launch template (a JSON-array command template, so no
    path or quote is re-parsed): `codex exec` under the workspace-write
    sandbox, unelevated on Windows, with `scratch` its one extra writable
    root, at `effort`, on the row's `{model}`; the prompt goes on stdin and
    the service's adapter adds `--json` and the final-message file. The
    `-c` forms are the ones `codex exec resume` also accepts.

    Implements: SR-243, LLR-346
    """
    return json.dumps(
        [
            runner,
            "exec",
            "-c",
            "model_reasoning_effort={}".format(effort),
            "-c",
            "windows.sandbox=unelevated",
            "-c",
            "sandbox_mode=workspace-write",
            "-c",
            "sandbox_workspace_write.writable_roots=['{}']".format(scratch),
            "--skip-git-repo-check",
            "--model",
            "{model}",
        ]
    )


def resolve_role(root, role, *, entry="", effort="medium"):
    """`(Launch, None)` for a role whose enabled row may launch, else `(None,
    reason)`: an unknown role, an entry the registry or the enable-list
    refuses (`coordinator_adjudicate.resolve_route`), or a launch
    environment that cannot be composed.

    Implements: SR-243, LLR-346
    """
    if role not in ROLES:
        return None, "unknown role {!r} (one of {})".format(role, ", ".join(ROLES))
    entry = entry or ROLE_ROUTES[role]
    registry, why = coordinator_adjudicate.resolve_route(root, entry)
    if why:
        return None, why
    route_id = agent_route.entry_route(entry)
    row = registry[route_id]
    try:
        env = session_service.entry_env(root, registry, entry)
    except session_service.SigninRefused as exc:
        return None, str(exc)
    runner = agent_route.route_runner(row.cmd_template, row.model)
    if not runner:
        return None, "{}: its command template names no runner".format(entry)
    template = launch_template(runner, effort, scratch_root(root))
    return Launch(route_id, row.family, row.tier or "", row.model, template, env), None


# --- the snapshots and the range ------------------------------------------------


def _git(root, *args, stdin=None):
    """`(exit code, stdout)` of one git read in `root`, unstripped, taking no
    optional lock (a status read must not contend with another call's
    commit)."""
    try:
        proc = subprocess.run(
            ["git", "--no-optional-locks", "-C", str(root), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            input=stdin,
            stdin=None if stdin is not None else subprocess.DEVNULL,
        )
    except OSError:
        return -1, ""
    return proc.returncode, proc.stdout


def _status_entry(entry):
    """`(XY, path, index state)` of one `status --porcelain=v2 -z` entry, or
    None for a shape this reader does not know. The index state is the
    entry's XY, its index and working-tree modes and its index object ids,
    so staging, unstaging or restaging a path changes it while its file on
    disk stays the same."""
    if entry.startswith("? "):
        return "??", entry[2:], "??"
    fields = entry.split(" ", 10 if entry.startswith("u ") else 8)
    if entry.startswith("1 ") and len(fields) == 9:
        return fields[1], fields[8], " ".join(fields[1:2] + fields[4:6] + fields[7:8])
    if entry.startswith("u ") and len(fields) == 11:
        return fields[1], fields[10], " ".join(fields[1:2] + fields[6:10])
    return None


def _status(root, *pathspec):
    """`[(XY, path, index state)]` of `root`'s uncommitted and untracked
    paths (`_status_entry`), or None when git cannot say."""
    code, out = _git(
        root,
        "status",
        "--porcelain=v2",
        "-z",
        "--untracked-files=all",
        "--no-renames",
        *(("--", *pathspec) if pathspec else ()),
    )
    if code != 0:
        return None
    entries = [_status_entry(entry) for entry in out.split("\0") if entry]
    return None if None in entries else entries


def _identities(root, paths):
    """`{path: identity}`: a file's blob id as git would store it, "" for a
    path absent from disk, a marker for one that is not a file; None when
    git cannot hash them."""
    found = {p: ("" if not (Path(root) / p).exists() else "not-a-file") for p in paths}
    files = [p for p in paths if (Path(root) / p).is_file()]
    if files:
        code, out = _git(root, "hash-object", "--stdin-paths", stdin="\n".join(files))
        hashes = out.split()
        if code != 0 or len(hashes) != len(files):
            return None
        found.update(zip(files, hashes))
    return found


def snapshot(root):
    """The root's HEAD and uncommitted paths with their content identities.

    Implements: SR-243, LLR-346
    """
    code, head = _git(root, "rev-parse", "--verify", "HEAD")
    head = head.strip() if code == 0 and head.strip() else None
    entries = _status(root)
    if entries is None:
        return Snapshot(head, None, index=None)
    paths = _identities(root, [path for _, path, _ in entries])
    tracked = frozenset(p for xy, p, _ in entries if xy != "??" and xy[0] != "A")
    index = {path: state for _, path, state in entries}
    return Snapshot(head, paths, tracked if paths is not None else frozenset(), index)


def _changes(root, sha):
    """The `(status, path, blob)` triples of one non-merge commit, or None."""
    code, out = _git(
        root, "diff-tree", "--no-commit-id", "--no-renames", "-r", "--raw", "-z", sha
    )
    if code != 0:
        return None
    fields = out.split("\0")
    triples = []
    for meta, path in zip(fields[0::2], fields[1::2]):
        parts = meta.split()
        if len(parts) < 5:
            return None
        triples.append((parts[4][:1], path, parts[3]))
    return tuple(triples)


def _commits(root, before, after):
    """The `Commit`s of `before..after`, or None when git cannot list them."""
    code, out = _git(root, "rev-list", "--parents", "{}..{}".format(before, after))
    if code != 0:
        return None
    commits = []
    for line in out.splitlines():
        sha, *parents = line.split()
        changes = _changes(root, sha) if len(parents) == 1 else ()
        if changes is None:
            return None
        commits.append(Commit(sha, tuple(parents), changes))
    return tuple(commits)


def read_span(root, before, after):
    """The range between two HEADs, read from git.

    Implements: SR-243, LLR-346
    """
    if before is None or after is None:
        return Span(None, None)
    if before == after:
        return Span(True, ())
    code, _ = _git(root, "merge-base", "--is-ancestor", before, after)
    if code == 1:
        return Span(False, ())
    if code != 0:
        return Span(None, None)
    return Span(True, _commits(root, before, after))


# --- the judge -------------------------------------------------------------------


def is_call_log_path(path):
    """Whether repository path `path` is a standard call's session log: a file
    directly under `docs/iteration/` with the name the service gives one."""
    if not path.startswith(ITERATION):
        return False
    name = path[len(ITERATION) :]
    return "/" not in name and session_service.is_call_log(name)


def _commit_edits(commits):
    """`(edits, added)` over the range: every commit but one that only adds
    standard-call logs is an edit (a merge included), and `added` maps each
    log a discounted commit adds to its blob."""
    edits, added = [], {}
    for c in commits:
        if len(c.parents) != 1:
            edits.append("merge commit {}".format(c.sha))
        elif c.changes and all(
            status == "A" and is_call_log_path(path) for status, path, _ in c.changes
        ):
            added.update((path, blob) for _, path, blob in c.changes)
        else:
            edits.extend(path for _, path, _ in c.changes)
            edits.extend(() if c.changes else ["empty commit {}".format(c.sha)])
    return edits, added


def _discounted(path, was, now, added, tracked):
    """Whether one uncommitted change is another call's log: a new standard-call
    log, or one waiting at the first snapshot that a discounted commit added
    unchanged."""
    if not is_call_log_path(path):
        return False
    if was is None:
        return bool(now) and path not in tracked
    return now is None and added.get(path) == was


def _status_edits(before, after, added):
    """The uncommitted changes between the two snapshots that are edits: a
    path whose file on disk or whose index state differs, unless it is
    another call's log (`_discounted`)."""
    edits = []
    for path in sorted(set(before.paths) | set(after.paths)):
        was, now = before.paths.get(path), after.paths.get(path)
        moved = was != now or before.index.get(path) != after.index.get(path)
        if moved and not _discounted(path, was, now, added, after.tracked):
            edits.append(path)
    return edits


def _unreadable(before, after, span):
    reads = (before.head, after.head, before.paths, after.paths)
    reads += (before.index, after.index)
    return any(r is None for r in reads + (span.descendant, span.commits))


def judge_changes(role, before, after, span):
    """The change check over two snapshots and the range between them: UNABLE
    when any read failed, EDIT (with the paths) for a HEAD that does not
    descend from the first, an undiscounted commit, or, for a Sol role, an
    undiscounted uncommitted change; else CLEAN.

    Implements: SR-243, LLR-346
    """
    if _unreadable(before, after, span):
        return Verdict(UNABLE)
    if not span.descendant:
        moved = "HEAD {} does not descend from {}".format(after.head, before.head)
        return Verdict(EDIT, (moved,))
    edits, added = _commit_edits(span.commits)
    if role != "AUTHOR":
        edits += _status_edits(before, after, added)
    return Verdict(EDIT, tuple(dict.fromkeys(edits))) if edits else Verdict(CLEAN)


# --- the resume carrier -----------------------------------------------------------


def _stamp(path):
    match = session_service.CALL_LOG_RE.match(path.rsplit("/", 1)[-1])
    return match.group("stamp") if match else None


def _classify(text, wis):
    """`(kind, detail)` of one standard-call log's text: `("bad", cause)` for
    an unreadable or damaged log, `("other", meta)` for a well-formed log of
    another role or lane, `("lane", meta)` for one of this lane's AUTHOR
    logs."""
    if text is None:
        return "bad", "its content cannot be read"
    meta, terminated = agent_common.log_meta_text(text)
    if not terminated:
        return "bad", "its header has no `# ---` terminator (a write cut short)"
    missing = [key for key in CARRIER_FIELDS if key not in meta]
    if missing:
        return "bad", "its header has no {}".format(", ".join(missing))
    if meta["role"] != "AUTHOR" or meta["wi"] not in wis:
        return "other", meta
    return "lane", meta


def _stamp_group(paths, logs, wis, route_id):
    """The carrier one name stamp's committed logs give, a refusal, or None
    when none of them is this lane's AUTHOR log."""
    lane = []
    for path in sorted(paths):
        kind, detail = _classify(logs[path], wis)
        if kind == "bad":
            return Carrier(refusal="{}: {}.".format(path, detail))
        if kind == "lane":
            lane.append((path, detail))
    if not lane:
        return None
    if len(lane) > 1:
        tied = ", ".join(path for path, _ in lane)
        return Carrier(refusal="{}: AUTHOR logs share one name stamp.".format(tied))
    path, meta = lane[0]
    if meta["roster-row"] != route_id:
        why = "{}: the lane's newest AUTHOR log ran on {}, not {}.".format(
            path, meta["roster-row"] or "no route", route_id
        )
        return Carrier(refusal=why)
    if not meta.get("session-id"):
        return Carrier(refusal="{}: its session-id is empty.".format(path))
    return Carrier(meta["session-id"], path)


def _newer_waiting(uncommitted, stamp, wis):
    """The refusal an uncommitted standard-call log not older than the
    carrier's stamp gives (damaged, or this lane's AUTHOR log), else ""."""
    for path, text in sorted(uncommitted.items()):
        found = _stamp(path)
        if found is None or found < stamp:
            continue
        kind, detail = _classify(text, wis)
        if kind == "bad":
            return "{}: uncommitted, and {}.".format(path, detail)
        if kind == "lane":
            return "{}: an uncommitted AUTHOR log of this lane, not older than the carrier.".format(
                path
            )
    return ""


def resume_carrier(committed, uncommitted, wis, route_id):
    """The carrier a resumed AUTHOR turn continues, from the committed
    standard-call logs at HEAD and the uncommitted ones (`{path: text}`, text
    None when unreadable), the lane's work item ids and the Terra route id.

    The committed logs are walked newest first by their name's stamp. A log
    that cannot be read or classified is refused, never stepped over (it may
    be a damaged newest carrier); a well-formed log of another role or lane
    is skipped; the first of this lane's AUTHOR logs is taken when it ran on
    the route and names its session (two under one stamp are refused); then
    an uncommitted log not older than it, damaged or this lane's AUTHOR log,
    refuses the turn.

    Implements: SR-243, LLR-346
    """
    groups = {}
    for path in committed:
        stamp = _stamp(path)
        if stamp is not None:
            groups.setdefault(stamp, []).append(path)
    for stamp in sorted(groups, reverse=True):
        carrier = _stamp_group(groups[stamp], committed, wis, route_id)
        if carrier is None:
            continue
        if carrier.refusal:
            return carrier
        refusal = _newer_waiting(uncommitted, stamp, wis)
        return Carrier(refusal=refusal) if refusal else carrier
    return Carrier(
        refusal="no committed AUTHOR session log of {} at HEAD: no thread to "
        "resume.".format(", ".join(sorted(wis)) or "this lane")
    )


class _HeadLogs(Mapping):
    """The standard-call logs at one commit, `{path: text}`, each blob read
    only when the walk reaches it (text None when it cannot be shown)."""

    def __init__(self, root, commit, paths):
        self._root, self._commit, self._paths = root, commit, list(paths)
        self._read = {}

    def __getitem__(self, path):
        if path not in self._paths:
            raise KeyError(path)
        if path not in self._read:
            code, text = _git(self._root, "show", "{}:{}".format(self._commit, path))
            self._read[path] = text if code == 0 else None
        return self._read[path]

    def __iter__(self):
        return iter(self._paths)

    def __len__(self):
        return len(self._paths)


def _committed_logs(root):
    """The standard-call logs committed at HEAD, or None when git cannot say."""
    code, head = _git(root, "rev-parse", "--verify", "HEAD")
    if code != 0:
        return None
    code, out = _git(root, "ls-tree", "--name-only", "-z", head.strip(), ITERATION)
    if code != 0:
        return None
    paths = [p for p in out.split("\0") if is_call_log_path(p)]
    return _HeadLogs(root, head.strip(), paths)


def _uncommitted_logs(root):
    """The uncommitted or untracked standard-call logs, `{path: text}` read
    from the working tree (None when unreadable), or None when git cannot
    say."""
    entries = _status(root, ITERATION)
    if entries is None:
        return None
    logs = {}
    for _, path, _ in entries:
        if is_call_log_path(path):
            try:
                logs[path] = (Path(root) / path).read_text(
                    encoding="utf-8", errors="replace"
                )
            except OSError:
                logs[path] = None
    return logs


def read_carrier(root, route_id):
    """The carrier a resumed turn at `root` continues, read from the lane's
    committed logs at HEAD and its uncommitted ones (`resume_carrier`).

    Implements: SR-243, LLR-346
    """
    wis = session_service.lane_wis(root)
    if not wis:
        return Carrier(refusal="{} is not a claimed lane.".format(root))
    committed, uncommitted = _committed_logs(root), _uncommitted_logs(root)
    if committed is None or uncommitted is None:
        return Carrier(refusal="git cannot list the session logs in {}.".format(root))
    return resume_carrier(committed, uncommitted, wis, route_id)


# --- the call ------------------------------------------------------------------------


def _prepare(root, args):
    """`((launch, prompt, resume id), None)`, or `(None, why)` for a call
    refused before launch."""
    if args.resume and args.role != "AUTHOR":
        return None, "--resume applies to an AUTHOR turn only"
    why = work_item_refusal(root, args.role, args.wi)
    if why:
        return None, why
    launch, why = resolve_role(root, args.role, entry=args.route, effort=args.effort)
    if why:
        return None, why
    try:
        prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return None, "the prompt {} cannot be read: {}".format(args.prompt_file, exc)
    resume = ""
    if args.resume:
        carrier = read_carrier(root, launch.route_id)
        if carrier.refusal:
            return None, "the resume carrier: " + carrier.refusal + RECOVERY
        resume = carrier.session_id
    return (launch, prompt, resume), None


def work_item_refusal(root, role, wi):
    """Why an AUTHOR turn may not launch for work item `wi` at `root` ("" when
    it may): it names none, or one the lane does not hold claimed
    (`session_service.lane_wis`), whose log the next resumed turn would skip
    as another lane's. Another role's work item is attribution only.

    Implements: SR-243, LLR-346
    """
    if role != "AUTHOR":
        return ""
    if not wi:
        return "an AUTHOR turn names its work item (--wi)"
    wis = session_service.lane_wis(root)
    if wi in wis:
        return ""
    held = ", ".join(sorted(wis)) or "none: {} is not a claimed lane".format(root)
    return (
        "the AUTHOR turn's work item {} is not one this lane holds claimed ({})".format(
            wi, held
        )
    )


def _service_call(root, args, launch, prompt, resume):
    """The service's `Call` for this launch."""
    return session_service.Call(
        root=root,
        role=args.role,
        template=launch.template,
        model=launch.model,
        prompt=prompt,
        provider=launch.provider,
        tier=launch.tier,
        route_id=launch.route_id,
        source_event="coordinator",
        attribution={"wi": args.wi},
        env=launch.env,
        timeout=args.timeout,
        idle_timeout=IDLE_TIMEOUT,
        resume=resume,
    )


@dataclass
class Called:
    """What one call through the service left: the `outcome` (None when the
    launch raised), the change check's `verdict` (None for a call refused
    before anything was accounted), the record's `report`, and `raised`, the
    text of what raised ("" for nothing).

    Implements: SR-243, LLR-346
    """

    outcome: object = None
    verdict: object = None
    report: dict = field(default_factory=dict)
    raised: str = ""


def run_call(root, args, launch, prompt, resume, before):
    """One call through the service's act-then-record (`session_service.call`),
    the change check run in its seam between the two, so the check reads the
    root before the call's own log is written and every recorded call is
    checked. A KeyboardInterrupt propagates, the call recorded INTERRUPTED.

    Implements: SR-243, LLR-346
    """
    called = Called()

    def check(outcome):
        called.outcome = outcome
        after = snapshot(root)
        span = read_span(root, before.head, after.head)
        called.verdict = judge_changes(args.role, before, after, span)

    service_call = _service_call(root, args, launch, prompt, resume)
    try:
        session_service.call(service_call, between=check, report=called.report)
    except Exception as exc:  # a refusal, a raised launch, or a failed record
        called.raised = str(exc)
        if called.verdict is not None and not called.report:
            why = "the log cannot be recorded: {}".format(exc)
            called.report.update(path=None, spooled=False, committed=False, refusal=why)
    return called


def _write_out(out, text):
    """Write the call's final text to `out`; the error text, or ""."""
    try:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(text or "", encoding="utf-8", newline="\n")
    except OSError as exc:
        return "the out path {} cannot be written: {}".format(out, exc)
    return ""


def exit_code(verdict, report, succeeded):
    """The exit code after launch, by precedence 5 > 3 > 4 > 1 > 0.

    Implements: SR-243, LLR-346
    """
    if verdict.state == UNABLE:
        return EXIT_UNABLE
    if verdict.state == EDIT:
        return EXIT_EDIT
    if not (report.get("committed") or report.get("spooled")):
        return EXIT_UNRECORDED
    return EXIT_OK if succeeded else EXIT_FAILED


def _log_line(report):
    if report.get("committed"):
        state = "committed"
    elif report.get("spooled"):
        state = "spooled"
    else:
        state = "NOT COMMITTED: {}".format(report.get("refusal") or "no record")
    return "codex_call: log {} {}".format(report.get("path") or "(none)", state)


def _report(verdict, report, out, failure):
    """Print what the call left: the check, the log and the out path."""
    if verdict.state == UNABLE:
        print("codex_call: the change check could not run (git could not answer)")
    for path in verdict.edits:
        print("codex_call: EDIT {}".format(path))
    print(_log_line(report))
    if failure:
        print("codex_call: " + failure)
    print("codex_call: out {}".format(out))


def main(argv=None):
    """Run one coordinator codex call; the exit code is the outcome.

    Implements: SR-243, LLR-346
    """
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = Path(args.root).resolve()
    prepared, why = _prepare(root, args)
    if why:
        print("codex_call: refused before launch: {}".format(why))
        return EXIT_REFUSED
    launch, prompt, resume = prepared
    print(
        "codex_call: {} on {} ({}), effort {}{}".format(
            args.role,
            launch.route_id,
            launch.model,
            args.effort,
            ", resuming {}".format(resume) if resume else "",
        )
    )
    before = snapshot(root)
    if before.head is None or before.paths is None:
        print(
            "codex_call: the change check could not run: git cannot read {}".format(
                root
            )
        )
        return EXIT_UNABLE
    called = run_call(root, args, launch, prompt, resume, before)
    if called.verdict is None and not called.report:
        print("codex_call: refused before launch: {}".format(called.raised))
        return EXIT_REFUSED
    code = _finish(args.out, called)
    print("codex_call: exit {}".format(code))
    return code


def _finish(out, called):
    """Write the out path, print what the call left, and return its exit
    code; a recorded call whose check never ran reads as unable."""
    verdict = called.verdict or Verdict(UNABLE)
    outcome = called.outcome
    failure = _write_out(out, outcome.text if outcome is not None else "")
    if outcome is None:
        failure = failure or "the launch raised: {}".format(called.raised)
    elif not session_service.call_succeeded(outcome):
        failure = failure or "the call failed (exit {})".format(outcome.code)
    _report(verdict, called.report, out, failure)
    return exit_code(verdict, called.report, not failure)


if __name__ == "__main__":
    utf8_console()
    sys.exit(main())
