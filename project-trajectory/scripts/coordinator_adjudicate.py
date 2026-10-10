#!/usr/bin/env python3
"""The coordinator's adjudication entry point: one retained session, the loop's.

A coordinator working from an interactive session runs its adjudications
through here rather than starting a fresh subagent for each: the call goes
through the session service's keep operation and the same `out/adjudicator/`
record as the loop's adjudications, so the coordinator's verdicts come from
one retained session that keeps the spine and the briefs it has read. This
module is a thin caller: the adjudication request is composed by the step the
loop uses (`session_service.AdjudicationRequest`, `adjudication_keep`, which
also derives the governing template identity), and the launch and the
session log by `session_service.call`.

TEMPORARY. WI-801's `ask` becomes the one launcher for the loop and the
coordinator alike; it deletes this entry point and moves its callers and
tests to its adjudicate kind.

Stdlib only, Python 3.11+, Windows/POSIX.

Contracts: IF-283, IF-284, IF-285 — the interface seams this module declares
(process.md §8; rows of record in docs/requirements/interfaces.toml).

Contract IF-283: the coordinator's adjudication command line, its arguments.
    `adjudicate --brief-file F --brief CLASS --wi WI-N --verdict PATH
    [--route ID] [--root DIR] [--timeout SECONDS]` runs only from a lane:
    DIR must be a linked worktree (not the primary checkout) on a branch that
    holds a claim under `docs/work/active/<branch>/`, so the session log's
    commit rides the lane and never lands on trunk. PATH must not exist: its
    missing parent directories are created, then it is created empty and
    exclusively before the launch, so no other call can claim it, and only
    what this call's session writes into it is read; a call refused before
    its launch removes it (the directories stay), and one that launched
    leaves it, written or empty, for inspection.
    It reads the composed brief from F (UTF-8) and launches it on the route
    (default `ANTHROPIC-OPUS-STRONG`), which must be a row of
    `docs/agents.toml` named on `docs/agents-enabled`, as an ADJUDICATE call
    of brief class CLASS for WI-N, retained where the `[adjudicator]` dial
    covers it, and writes and commits the call's session log.
    `signin [--family F] [--root DIR] [--retained]` prints the sign-in
    probe's reading for family F (default ANTHROPIC), creating nothing and
    making no model call; for ANTHROPIC the reading is whether the long-lived
    token file the `AGENT_CLAUDE_TOKEN_FILE` environment variable names can
    be read, never the token or its path. With `--retained` it reads `off`,
    probing nothing, while the `[adjudicator]` dial leaves retention off.

Contract IF-284: the command's exit codes. `adjudicate` exits 0 for a valid
    verdict; 1 for a call that failed, timed out or reported an error result
    (`session_service.call_succeeded`), or a missing (still
    empty) or invalid verdict; 2, before anything launches, for a root that
    is not a lane, an unusable route, a brief file that cannot be read or
    decoded, a PATH that exists or cannot be reserved, or a launch the
    blackout window refuses (the session service admits only an
    adjudication of a work item whose claim is active there); and 7 (needs a human) when the retained launch is refused
    because its dedicated CLI home is not signed in. `signin` exits 0.

Contract IF-285: the command's stdout readings. `adjudicate` prints the
    call's keep, its exit, and, for a call that SUCCEEDED
    (`session_service.call_succeeded`: exit 0, within its deadline, and no
    error result the CLI reported), the verdict file at PATH with its
    validity under the brief class's grammar, or that the verdict is missing
    when the call left its reservation empty; any other call prints that it
    failed and that its verdict is not read. `signin` prints the sign-in probe's reading: `signed-in`,
    `missing` or `unknown`, or `off` under `--retained` with retention off.

Run with Python 3.11+:  python scripts/coordinator_adjudicate.py adjudicate \\
    --brief-file out/brief.md --brief amendment --wi WI-123 \\
    --verdict docs/reviews/wi-123/verdict.md
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import adjudicate_brief
    import agent_common
    import agent_route
    import integrate
    import session_service
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import adjudicate_brief
    import agent_common
    import agent_route
    import integrate
    import session_service
from kitlib.config import utf8_console

# The coordinator's adjudicator: the strong Anthropic route (owner, 2026-10-05).
# Implements: SR-231, LLR-306
DEFAULT_ROUTE = "ANTHROPIC-OPUS-STRONG"
# The loop's default idle bound (AGENT_SESSION_IDLE_TIMEOUT), so a wedged
# call ends as the loop's would.
IDLE_TIMEOUT = 900


def resolve_route(root, route_id):
    """`(row, None)` for an enabled registry row, else `(None, reason)`: the
    enable-list is the owner's consent to launch a route, here as in the loop.

    Implements: SR-231, LLR-306
    """
    docs = Path(root) / "docs"
    registry, _errors = agent_route.load_registry(docs / "agents.toml")
    row = registry.get(route_id)
    if row is None:
        return None, "{} is not a row in docs/agents.toml".format(route_id)
    enabled, _ = agent_route.resolve_enabled(
        agent_route.load_enabled(docs / "agents-enabled"), registry
    )
    if route_id not in enabled:
        return None, "{} is not named on docs/agents-enabled".format(route_id)
    return row, None


def _worktree_index(records, root):
    """The index of `root` among git's worktree records (0 is the primary
    checkout), or None when it is not the top of one."""
    want = os.path.normcase(str(Path(root).resolve()))
    for index, (path, _branch) in enumerate(records):
        if path and os.path.normcase(str(Path(path).resolve())) == want:
            return index
    return None


def lane_refusal(root):
    """Why `root` is not a lane, or None. A lane is a linked worktree (never
    the primary checkout, whose session-log commit would land on trunk and
    fail the integrator's audit) on a branch whose committed tree still holds
    a claim under `docs/work/active/<branch>/`. Read through git's worktree
    records (`agent_common.worktree_records`) and the integrator's claim
    reader (`integrate.claimed_ids_on_branch`).

    Implements: SR-231, LLR-306
    """
    records = agent_common.worktree_records(root)
    index = _worktree_index(records, root)
    if index is None:
        return "{} is not the top of a git worktree".format(root)
    if index == 0:
        return (
            "{} is the primary checkout: run from the lane's worktree, so the "
            "session log's commit rides the lane and not trunk".format(root)
        )
    branch = records[index][1]
    if not branch:
        return "{} has a detached HEAD, not a lane branch".format(root)
    if not integrate.claimed_ids_on_branch(root, branch):
        return "branch {0} holds no claim under docs/work/active/{0}/".format(branch)
    return None


def reserve_verdict(path):
    """Take exclusive ownership of the verdict path, or say why not: its
    missing parent directories are created (a work item's first verdict
    names a review directory that does not exist yet), then the path is
    created empty with O_CREAT|O_EXCL, so of two calls naming it only one can
    hold it, and a verdict read afterwards from a non-empty file was written
    into this call's reservation. None when reserved.

    Implements: SR-231, LLR-306
    """
    path = Path(path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:  # a parent that is a file, or not creatable
        return "the verdict path {} cannot be reserved: {}".format(path, exc)
    try:
        fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return (
            "the verdict path {} already exists or is reserved by another "
            "call; name a fresh one".format(path)
        )
    except OSError as exc:
        return "the verdict path {} cannot be reserved: {}".format(path, exc)
    os.close(fd)
    return None


def bind_requested(path, brief, prompt):
    """Bind what this sitting was asked beside its verdict, or say why not:
    `kitlib.sitting.requested_path(path)` is created exclusively holding the
    brief class and its requested kinds (a combined brief's, read off its one
    `SITTING:` line; a dispute brief's finding ids, off its `DISPUTE:` line;
    a single-kind brief's own class). A separate file, so the
    adjudicator's rewrite of the verdict cannot change what the verdict is
    judged against (WI-841 round 10). None when bound.

    Implements: SR-232, LLR-310
    """
    try:
        kinds = adjudicate_brief.bind_pending(path, brief, prompt, exclusive=True)
    except OSError as exc:
        return "the verdict binding for {} cannot be written: {}".format(path, exc)
    if not kinds:
        return (
            "the {} brief names nothing to judge (a combined brief's kinds on a "
            "`SITTING:` line, a dispute brief's findings on a `DISPUTE:` "
            "line)".format(brief)
        )
    return None


def _release(path, bound=True):
    """Remove the files THIS call created and nothing else: its reservation
    when nothing was written into it, and its binding only when `bound` (this
    call wrote it). A reservation refused because a binding already existed
    leaves that binding, which another call owns (WI-841 round 13)."""
    try:
        if os.path.getsize(path) == 0:
            os.remove(path)
            if bound:
                os.remove(adjudicate_brief.ksitting.requested_path(path))
    except OSError:
        pass


def _inputs(root, args):
    """`(row, prompt, None)` when the call may launch, else `(None, None,
    why)`: a lane root, an enabled route, a readable brief, and, last, the
    verdict path reserved for this call alone (`reserve_verdict`)."""
    why = lane_refusal(root)
    row, prompt = None, None
    if why is None:
        row, why = resolve_route(root, args.route)
    if why is None:
        try:
            prompt = Path(args.brief_file).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            why = "the brief file cannot be read: {}".format(exc)
    if why is None:
        why = reserve_verdict(args.verdict)
    if why is None:
        why = bind_requested(args.verdict, args.brief, prompt)
        if why:
            _release(args.verdict, bound=False)
    return (None, None, why) if why else (row, prompt, None)


def _keep_line(kept):
    if kept is None:
        return "keep: none (the dial does not retain this call); a fresh session"
    if kept.session_id:
        return "keep: resuming {} (generation {})".format(
            kept.session_id, kept.generation
        )
    return "keep: minting a retained session"


def _report(outcome, brief, verdict, kinds=()):
    """Print the call's exit and the verdict; 0 for a valid verdict, else 1.
    A call that exited non-zero, timed out or reported an error result
    (`session_service.call_succeeded`) has failed whatever file is at the
    verdict path, which is then not read. A combined sitting's verdict is
    judged against `kinds`, the kinds its composed brief requested."""
    print("adjudicate: exit {}{}".format(outcome.code, _timed(outcome)))
    if not session_service.call_succeeded(outcome):
        print("adjudicate: the call failed; its verdict is not read")
        return 1
    path = Path(verdict)
    if not path.is_file() or path.stat().st_size == 0:
        print("adjudicate: verdict missing: the call wrote nothing to {}".format(path))
        return 1
    refusal = adjudicate_brief.verdict_refusal(brief, verdict, kinds=kinds)
    if path.is_file():
        print("--- verdict {} ---".format(path))
        print(path.read_text(encoding="utf-8", errors="replace").rstrip())
        print("--- end verdict ---")
    print("adjudicate: verdict {}".format(refusal or "valid"))
    return 1 if refusal else 0


def _timed(outcome):
    return " (timed out)" if outcome.timed_out else ""


def adjudicate(args):
    """Compose the request, plan the keep, launch and record, report.

    Implements: SR-231, LLR-306
    """
    root = Path(args.root).resolve()
    row, prompt, why = _inputs(root, args)
    if why:
        print("adjudicate: refused: {}".format(why))
        return agent_common.EXIT_PREFLIGHT
    env = session_service.route_env(row)
    request = session_service.AdjudicationRequest(
        root=root,
        brief=args.brief,
        route=row,
        wi=args.wi,
        deadline=args.timeout,
    )
    try:
        kept = session_service.adjudication_keep(request)
    except session_service.SigninRefused as refused:
        _release(args.verdict)
        print("adjudicate: {}".format(refused))
        return agent_common.EXIT_NEEDS_HUMAN
    print(_keep_line(kept))
    try:
        outcome = session_service.call(
            session_service.Call(
                root=root,
                role=request.role,
                template=row.cmd_template,
                model=row.model or row.id,
                prompt=prompt,
                provider=row.family,
                tier=row.tier,
                route_id=row.id,
                source_event="coordinator",
                attribution={"wi": args.wi},
                env=env,
                timeout=args.timeout,
                idle_timeout=IDLE_TIMEOUT,
                keep=kept,
                wi=args.wi,
            )
        )
    except session_service.BlackoutRefused as refused:
        _release(args.verdict)
        print("adjudicate: refused: {}".format(refused))
        return agent_common.EXIT_PREFLIGHT
    kinds = adjudicate_brief.requested_for(args.brief, prompt)
    code = _report(outcome, args.brief, args.verdict, kinds)
    # The route that ran the call RECORDS its acceptance (WI-841 rounds 11,
    # 12): `record_outcome` judges the verdict itself and takes the call's
    # success, so a failed or timed-out call is recorded failed.
    call_ok = session_service.call_succeeded(outcome)
    adjudicate_brief.record_outcome(
        root, args.verdict, args.brief, kinds, call_ok, args.wi
    )
    return code


def signin(args):
    """Print the sign-in probe's reading of a family's dedicated home (for
    Claude, whether its long-lived token file can be read; never the token).
    With `--retained`, `off` and no probe while the `[adjudicator]` dial
    (`session_keep.keep_config`) leaves retention off: dev-setup's reading.

    Implements: SR-231, LLR-306
    """
    family = args.family.upper()
    root = Path(args.root).resolve()
    if args.retained and not session_service.session_keep.keep_config(root).enabled:
        status = "off"
    else:
        status = session_service.signin_status(root, family)
    print("signin [{}]: {}".format(family, status))
    return 0


def _parser():
    parser = argparse.ArgumentParser(
        description="The coordinator's adjudication through the retained session."
    )
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("adjudicate", help="run one adjudication")
    run.add_argument("--root", default=".")
    run.add_argument("--brief-file", required=True)
    run.add_argument(
        "--brief", required=True, choices=sorted(adjudicate_brief.BRIEF_PROMPTS)
    )
    run.add_argument("--wi", required=True)
    run.add_argument("--verdict", required=True)
    run.add_argument("--route", default=DEFAULT_ROUTE)
    run.add_argument("--timeout", type=int, default=session_service.DEFAULT_DEADLINE)
    run.set_defaults(handler=adjudicate)
    probe = sub.add_parser(
        "signin",
        help="read a dedicated home's sign-in; Claude's is its long-lived token, "
        "read from the file the AGENT_CLAUDE_TOKEN_FILE env var names",
    )
    probe.add_argument("--root", default=".")
    probe.add_argument("--family", default="ANTHROPIC")
    probe.add_argument(
        "--retained",
        action="store_true",
        help="read `off` while the [adjudicator] dial leaves retention off",
    )
    probe.set_defaults(handler=signin)
    return parser


def main(argv=None):
    """The command line; see Contracts IF-283, IF-284 and IF-285.

    Implements: SR-231, LLR-306
    """
    args = _parser().parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    utf8_console()
    sys.exit(main())
