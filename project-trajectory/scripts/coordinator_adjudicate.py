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

A sitting ends at its committed verdict, and its act is a later adjudicator
turn taken from that verdict (WI-912; revisions 31, 32 and 36 of the
review-churn plan): `adjudicate` runs the judging turn, `act` the act turn,
which `adjudicate_act` composes from the verdict accepted at the lane's HEAD.
Under the loop marker every prompt either command launches ends with the
loop's `Loop-Session` instruction.

TEMPORARY. WI-801's `ask` becomes the one launcher for the loop and the
coordinator alike; it deletes this entry point and moves its callers and
tests to its adjudicate kind, and it must carry the `act` command with them.

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
    It reads the composed brief from F (UTF-8) and launches it on the
    enabled entry ID (a registry id, or `ROUTE@ACCOUNT`; default
    `ANTHROPIC-OPUS-STRONG@ADJUDICATOR`, the strong Anthropic route on the
    declared token account ADJUDICATOR, WI-798), which must resolve against
    `docs/agents.toml` (its route a row, its account declared for that
    route's CLI, the registry free of errors) and be named on
    `docs/agents-enabled`, as an ADJUDICATE call of brief class CLASS for
    WI-N, under that entry's account by the one launch-environment rule,
    retained where the `[adjudicator]` dial covers it, and writes and commits
    the call's session log.
    `act --verdict PATH --wi WI-N [--route ID] [--root DIR] [--timeout
    SECONDS]` runs only from a lane, as `adjudicate` does, with no
    uncommitted change in it: it composes the act brief from the verdict at
    PATH (repo-relative) and its binding as committed at the lane's HEAD,
    launches it on the enabled entry ID as `adjudicate` resolves it, under
    that entry's account by the same launch-environment rule, as an
    ADJUDICATE call for WI-N, retained where the `[adjudicator]` dial
    retains the verdict's bound class and fresh otherwise, and writes and
    commits the call's session log. It reserves no verdict path, writes no
    binding and records no outcome.
    `signin [--route ID] [--root DIR] [--retained]` prints the sign-in
    probe's reading for the account of entry ID (default the adjudicator's),
    creating nothing and making no model call: for a token account whether
    the long-lived token file its `token_file_variable` names can be read,
    never the token or its path; for a login account its own home's status
    command. With `--retained` it reads `off`, probing nothing, while the
    `[adjudicator]` dial leaves retention off.

Contract IF-284: the command's exit codes. `adjudicate` exits 0 for a valid
    verdict; 1 for a call that failed, timed out or reported an error result
    (`session_service.call_succeeded`), or a missing (still
    empty) or invalid verdict; 2, before anything launches, for a root that
    is not a lane, an unusable route, a brief file that cannot be read or
    decoded, a PATH that exists or cannot be reserved, or a launch the
    blackout window refuses (the session service admits only an
    adjudication of a work item whose claim is active there); and 7 (needs a
    human) when the launch is refused because its account cannot
    authenticate (a token that cannot be read, a login home absent or not
    signed in) or its environment conflicts. `act` exits 0 only when
    the call succeeded, HEAD then carries in full every act the verdict
    authorizes, and nothing under docs/reviews/ changed; 1 otherwise after a
    launch; 2, before anything launches, for a root that is not a lane, an
    unusable route, a lane with uncommitted changes, a verdict that is not
    accepted at HEAD, owes no act or judged a row in a state no act explains,
    or a launch the blackout window refuses; and 7 as `adjudicate`. `signin`
    exits 0.

Contract IF-285: the command's stdout readings. `adjudicate` prints the
    call's keep, its exit, and, for a call that SUCCEEDED
    (`session_service.call_succeeded`: exit 0, within its deadline, and no
    error result the CLI reported), the verdict file at PATH with its
    validity under the brief class's grammar, or that the verdict is missing
    when the call left its reservation empty; any other call prints that it
    failed and that its verdict is not read. `act` prints its keep and exit,
    then the acts still owed at HEAD after the call, the paths it changed
    under docs/reviews/, or `act: complete`; a refusal prints `act: refused:`
    and why, naming the uncommitted paths or the inconsistent row. `signin`
    prints one line
    `signin [<ACCOUNT>] <token|login>: <status>` (status `signed-in`,
    `missing` or `unknown`; `signin [-] retained: off` under `--retained` with retention off;
    an unverified Claude login appends ` (unverified)` and a line saying it
    is printed, not refused; a login account reading missing adds the
    command that provisions it), `signin [-] ambient: ambient` for an
    unqualified entry, or `signin [-] unresolved: unknown (<why>)`.

Run with Python 3.11+:  python scripts/coordinator_adjudicate.py adjudicate \\
    --brief-file out/brief.md --brief amendment --wi WI-123 \\
    --verdict docs/reviews/wi-123/verdict.md
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import adjudicate_act
    import adjudicate_brief
    import agent_brief
    import agent_common
    import agent_route
    import integrate
    import session_service
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import adjudicate_act
    import adjudicate_brief
    import agent_brief
    import agent_common
    import agent_route
    import integrate
    import session_service
from kitlib.config import utf8_console
from kitlib.git import git_out

# The coordinator's adjudicator: the strong Anthropic route (owner, 2026-10-05),
# run on the declared token account ADJUDICATOR (WI-798), whose table names the
# variable locating its long-lived token (OI-110 (b)). A repository that does
# not declare that account names its entry with --route.
# Implements: SR-231, SR-222, LLR-306, LLR-336
DEFAULT_ROUTE = "ANTHROPIC-OPUS-STRONG@ADJUDICATOR"
# The loop's default idle bound (AGENT_SESSION_IDLE_TIMEOUT), so a wedged
# call ends as the loop's would.
IDLE_TIMEOUT = 900


def resolve_route(root, entry):
    """`(registry, None)` when the enabled `entry` may launch, else `(None,
    reason)`: the entry's own enable-list line is the owner's consent to
    launch it, here as in the loop (an unqualified entry is its route id, a
    qualified one `ROUTE@ACCOUNT`). Refused, never discarded (WI-798): a
    registry error (a malformed row or account table), an agents-enabled
    that exists but cannot be read, an entry that does not resolve (its
    route not a row, its account not declared or not its CLI's), or one not
    on the enable list. The caller reads the row and account through
    `agent_route.entry_route` / `account_of`.

    Implements: SR-231, SR-222, LLR-306, LLR-336
    """
    docs = Path(root) / "docs"
    registry, errors = agent_route.load_registry(docs / "agents.toml")
    if errors:
        return None, "docs/agents.toml: {}".format("; ".join(errors))
    found, why = agent_route.resolve_entry(entry, registry)
    if why:
        return None, why
    try:
        tokens = agent_route.load_enabled(docs / "agents-enabled")
    except agent_route.EnabledUnreadable as exc:
        return None, str(exc)
    enabled, _ = agent_route.resolve_enabled(
        tokens, registry, agent_route.load_tag_rank(docs / "agents.toml")
    )
    if found != entry or found not in enabled:
        return None, "{} is not named on docs/agents-enabled".format(entry)
    return registry, None


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
    index = agent_common.worktree_index(records, root)
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
    """`(registry, prompt, None)` when the call may launch, else `(None,
    None, why)`: a lane root, an enabled entry, a readable brief, and, last,
    the verdict path reserved for this call alone (`reserve_verdict`)."""
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


def _launched(prompt):
    """The prompt as the entry point launches it: under the loop marker, with
    the loop's `Loop-Session` instruction appended
    (`agent_brief.loop_provenance_note`, "" without the marker), so one
    construction covers every prompt either command launches (WI-912, Q4).

    Implements: SR-209, LLR-306
    """
    return prompt + agent_brief.loop_provenance_note()


def _call(root, row, request, kept, prompt, env):
    """Launch `prompt` (as `_launched` makes it) on the route as the request's
    adjudication call under `kept`, in `env` (the entry's launch environment,
    `session_service.launch_env`; WI-798), and record its session log; raises
    BlackoutRefused or HooksOffRefused as `session_service.call` does.

    Implements: SR-231, LLR-306
    """
    return session_service.call(
        session_service.Call(
            root=root,
            role=request.role,
            template=row.cmd_template,
            model=row.model or row.id,
            prompt=_launched(prompt),
            provider=row.family,
            tier=row.tier,
            route_id=row.id,
            source_event="coordinator",
            attribution={"wi": request.wi},
            env=env,
            timeout=request.deadline,
            idle_timeout=IDLE_TIMEOUT,
            keep=kept,
            wi=request.wi,
        )
    )


def adjudicate(args):
    """Compose the request, plan the keep, launch and record, report.

    Implements: SR-231, LLR-306
    """
    root = Path(args.root).resolve()
    registry, prompt, why = _inputs(root, args)
    if why:
        print("adjudicate: refused: {}".format(why))
        return agent_common.EXIT_PREFLIGHT
    row = registry[agent_route.entry_route(args.route)]
    request = session_service.AdjudicationRequest(
        root=root,
        brief=args.brief,
        route=row,
        wi=args.wi,
        deadline=args.timeout,
        account=agent_route.account_of(registry, args.route),
    )
    try:
        kept = session_service.adjudication_keep(request)
        env = session_service.launch_env(root, row, request.account)
    except session_service.SigninRefused as refused:
        _release(args.verdict)
        print("adjudicate: {}".format(refused))
        return agent_common.EXIT_NEEDS_HUMAN
    print(_keep_line(kept))
    try:
        outcome = _call(root, row, request, kept, prompt, env)
    except (
        session_service.BlackoutRefused,
        session_service.HooksOffRefused,
    ) as refused:
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


# The verdict records an act turn may not write (WI-912).
REVIEWS = adjudicate_brief.ksitting.REVIEWS


def _status_paths(root, *pathspec):
    """The paths `git status` reports changed or untracked under `root`
    (limited to `pathspec`), or None when git cannot say."""
    args = ["status", "--porcelain", "--untracked-files=all"]
    out = git_out(root, args + (["--", *pathspec] if pathspec else []))
    if out is None:
        return None
    return [line[3:] for line in out.splitlines() if line.strip()]


def _act_inputs(root, args):
    """`(registry, brief, prompt, None)` when the act turn may launch, else
    `(None, None, None, why)`: a lane root, an enabled entry, a lane with no
    uncommitted change, and the act brief composed from the verdict accepted
    at HEAD (`adjudicate_act.compose_act`), which refuses a verdict that is
    not accepted there, owes no act, or judged a row in a state no act
    explains.

    Implements: SR-231, LLR-306
    """
    why = lane_refusal(root)
    registry, prompt = None, None
    if why is None:
        registry, why = resolve_route(root, args.route)
    if why is None:
        dirty = _status_paths(root)
        if dirty is None:
            why = "git cannot read the status of {}".format(root)
        elif dirty:
            why = "the lane has uncommitted changes: {}".format(", ".join(dirty))
    if why is None:
        prompt, why = adjudicate_act.compose_act(root, args.verdict, args.wi)
    if why:
        return None, None, None, why
    return registry, adjudicate_act.bound_brief(root, args.verdict), prompt, None


def _reviews_written(root, before):
    """The paths under docs/reviews/ changed since the commit `before`,
    committed or not."""
    committed = git_out(root, ["diff", "--name-only", before, "HEAD", "--", REVIEWS])
    working = _status_paths(root, REVIEWS) or []
    return sorted(set((committed or "").split()) | set(working))


def _act_report(root, args, outcome, before):
    """Print the act call's exit and what it left; 0 only when the call
    succeeded, nothing the verdict authorizes is left owed at HEAD, and
    nothing under docs/reviews/ changed, else 1.

    Implements: SR-231, LLR-306
    """
    print("act: exit {}{}".format(outcome.code, _timed(outcome)))
    call_ok = session_service.call_succeeded(outcome)
    if not call_ok:
        print("act: the call failed")
    left = adjudicate_act.left_owed(root, args.verdict)
    if left:
        print("act: owed after the call: {}".format(left))
    written = _reviews_written(root, before)
    if written:
        print("act: wrote under docs/reviews: {}".format(", ".join(written)))
    if call_ok and not left and not written:
        print("act: complete")
        return 0
    return 1


def act(args):
    """Take the act a committed, accepted verdict authorizes: compose the act
    brief from it at HEAD, plan the keep by the verdict's bound class, launch,
    and report whether the act is complete. Reserves no verdict path, writes
    no binding and records no outcome (WI-912).

    Implements: SR-231, LLR-306
    """
    root = Path(args.root).resolve()
    registry, brief, prompt, why = _act_inputs(root, args)
    if why:
        print("act: refused: {}".format(why))
        return agent_common.EXIT_PREFLIGHT
    row = registry[agent_route.entry_route(args.route)]
    request = session_service.AdjudicationRequest(
        root=root,
        brief=brief,
        route=row,
        wi=args.wi,
        deadline=args.timeout,
        account=agent_route.account_of(registry, args.route),
    )
    try:
        kept = session_service.adjudication_keep(request)
        env = session_service.launch_env(root, row, request.account)
    except session_service.SigninRefused as refused:
        print("act: {}".format(refused))
        return agent_common.EXIT_NEEDS_HUMAN
    print(_keep_line(kept))
    before = (git_out(root, ["rev-parse", "HEAD"]) or "").strip()
    try:
        outcome = _call(root, row, request, kept, prompt, env)
    except (
        session_service.BlackoutRefused,
        session_service.HooksOffRefused,
    ) as refused:
        print("act: refused: {}".format(refused))
        return agent_common.EXIT_PREFLIGHT
    return _act_report(root, args, outcome, before)


def signin(args):
    """Print the sign-in probe's reading of the adjudicator entry's account
    (`--route`, default `DEFAULT_ROUTE`; WI-798) as `signin_lines` words it.
    An entry that does not resolve reads `signin [-] unresolved: unknown`
    and says why. With `--retained`, `signin [-] retained: off` and no probe
    or resolution while the `[adjudicator]` dial
    (`session_keep.keep_config`) leaves retention off: dev-setup's reading. Nothing is run beyond the account's own status
    command, nothing is created and nothing signs in.

    Implements: SR-231, SR-222, LLR-306, LLR-336
    """
    root = Path(args.root).resolve()
    if args.retained and not session_service.session_keep.keep_config(root).enabled:
        print("signin [-] retained: off")
        return 0
    registry, why = resolve_route(root, args.route)
    if why:
        print("signin [-] unresolved: unknown ({})".format(why))
        return 0
    row = registry[agent_route.entry_route(args.route)]
    account = agent_route.account_of(registry, args.route)
    status = session_service.signin_status(root, account, row=row)
    for line in signin_lines(account, status):
        print(line)
    return 0


def signin_lines(account, status):
    """The `signin` command's lines for `account` (None: an ambient entry)
    reading `status`. First the parseable status line,
    `signin [<ACCOUNT>] <kind>: <status>`: kind `token` (whether its
    long-lived token file can be read; never the token or its path), `login`
    (its own home's status command; an unverified Claude login carries
    ` (unverified)`), or `signin [-] ambient: ambient` for the person's own
    login, which has no kit-held home. Then, for a token account, the name of
    the variable locating its token file (never the path or the token); for a
    login account reading missing, the command that provisions it (never
    run); and for an unverified one the line saying it is printed, not
    refused (D-011).

    Implements: SR-222, LLR-336
    """
    if account is None:
        return ["signin [-] ambient: {}".format(status)]
    kind = "token" if account.token_file_variable else "login"
    flag = " (unverified)" if account.unverified else ""
    lines = ["signin [{}] {}: {}{}".format(account.id, kind, status, flag)]
    if kind == "token":
        lines.append(
            "signin [{}]: token_file_variable {}".format(
                account.id, account.token_file_variable
            )
        )
    if kind == "login" and status == session_service.SIGNIN_MISSING:
        lines.append(
            "signin [{}]: provision it yourself: {}".format(
                account.id, session_service.provision_command(account)
            )
        )
    if account.unverified:
        lines.append(
            "signin [{}]: UNVERIFIED: a Claude login other than the ambient one "
            "whose login-isolation check has not passed (`verified` is empty); "
            "printed, not refused".format(account.id)
        )
    return lines


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
    run.add_argument(
        "--route",
        default=DEFAULT_ROUTE,
        help="the enabled entry: a registry id, or ROUTE@ACCOUNT",
    )
    run.add_argument("--timeout", type=int, default=session_service.DEFAULT_DEADLINE)
    run.set_defaults(handler=adjudicate)
    take = sub.add_parser(
        "act", help="take the act a committed, accepted verdict authorizes"
    )
    take.add_argument("--root", default=".")
    take.add_argument("--verdict", required=True)
    take.add_argument("--wi", required=True)
    take.add_argument(
        "--route",
        default=DEFAULT_ROUTE,
        help="the enabled entry: a registry id, or ROUTE@ACCOUNT",
    )
    take.add_argument("--timeout", type=int, default=session_service.DEFAULT_DEADLINE)
    take.set_defaults(handler=act)
    probe = sub.add_parser(
        "signin",
        help="read the adjudicator entry's account sign-in: a token account's "
        "long-lived token file (named by its token_file_variable), or a login "
        "account's own home",
    )
    probe.add_argument("--root", default=".")
    probe.add_argument(
        "--route",
        default=DEFAULT_ROUTE,
        help="the enabled entry whose account is read (default: the adjudicator's)",
    )
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
