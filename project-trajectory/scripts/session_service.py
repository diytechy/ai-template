#!/usr/bin/env python3
"""The session service: the one path every model call takes (act, keep, record).

Every model call the kit makes — a worker's build, both review legs, a critic,
an adjudicator, a dual-plan hat, a route's liveness probe, a hands-on sitting —
goes through here, and a role differs only in the data it hands over (brief,
route, tier, environment), never in launch or logging code of its own. That
is the whole point: when each role kept its own launch and logging path, a
usage fix landed in one of them and not the others, and the codex route
recorded no usage at all.

  - `act` launches one call: it builds the argv from the route's command
    template (`agent_session.build_argv`), lets the launched CLI's adapter
    (`session_adapters`) add its structured-output flags, runs it headless
    (`agent_session.run_session`) or attached to the terminal, reads the final
    text back through the adapter, and accounts it — identity, timing, the
    usage record and the context occupancy of the latest request.
  - `record` is the one writer: it writes the call's session log (the tracked
    `docs/iteration/*.log`, through `agent_common.write_session_log`), keeps
    the raw stream where the caller asks for it, and commits the log in its
    own telemetry commit. A worker hands it the row it composed; every other
    call gets the standard row from `call`, which is `act` then `record`.
  - `keep` is the retention operation (resume by id, keep warm, reset) that
    rides `act` and `record` rather than launching or logging anything itself;
    its rules and its store are `session_keep`'s.

Stdlib only, Python 3.11+, Windows/POSIX. A coordinator-layer module: it
imports its siblings `agent_common`, `agent_session` and `session_adapters`
(and `adjudicate_brief` for the brief classes' template identity),
and `agent_loop` and `plan_runner` import it.

Contracts: IF-246, IF-282 — the interface seams this module declares
(process.md §8; rows of record in docs/requirements/interfaces.toml).

Contract IF-246: the session service's call surface. `Call` is the data a role
    hands over: `root`, `role`, the route's command `template` with `model` and
    `prompt`, the route's `provider`, `tier`, `route_id`, `source_event` and
    `attempt_id`, any further log `attribution`, the launch `env`, the wall
    `timeout` and `idle_timeout`, the console `on_line` renderer, `attached`
    for a hands-on sitting, an optional `runner` standing in for the launch,
    an optional `keep` (from `keep_for`) naming the retained session the
    call resumes or mints, and `wi`, the work item an adjudication is for,
    carried apart from the keep. `act(call, metrics=None)` returns an `Outcome` (`root`, `code`,
    `text`, `timed_out`, `stream`, `metrics`): `text` is the CLI's result as
    its adapter reads it, `stream` the whole captured output, and `metrics`
    the call's accounting, filled into a caller-owned dict so a call that
    raises is still accounted before the exception propagates; a command
    template that cannot be built raises ValueError before anything is
    accounted. `resume`, a thread id, launches the call in its CLI's resume
    form with no retained session and accounts it `session-mode = resumed`;
    a call naming both `keep` and `resume` raises ValueError before anything
    is accounted. `record(outcome, meta, ..., report=None)` writes one session
    log from the caller's row overlaid by the outcome's accounting, and the
    raw stream to `raw_dir/raw_name` when given. Where the log goes is derived
    from the root alone (`lane_branch`): in a claimed lane, a linked worktree
    on a branch whose own committed tree or trunk's still holds a claim under
    `docs/work/active/<branch>/` (trunk's covers a lane closed under
    close-first and not yet merged), it is written to `docs/iteration/` and
    committed; from any other root (the primary checkout on any branch, a
    detached HEAD, a branch neither readable tree shows claimed, or a root
    whose worktree records cannot be read; a claim read that cannot be read
    adds no claim) it is written to the primary checkout's spool,
    `out/sessions/spool/` (`spool_dir`), and nothing is committed; a spool that cannot be written raises OSError. It returns
    the log's path and fills a caller-owned `report` dict with `path`,
    `spooled`, `committed` and the telemetry commit's `refusal` text ("" for
    none), so a refused commit is never read as success. `lane_wis(root)`
    returns the lane's claimed work item ids on either tree. A standard call's
    log is named `call_<invocation id>-<YYYYmmdd>-<HHMMSS>.log`, which
    `is_call_log(name)` accepts and no gate-log name matches. `call(call,
    between=None, report=None)` is `act` then `record` with the standard
    row, recording even when the launch raised (a Ctrl-C recorded
    INTERRUPTED), and returns the `Outcome`; a caller's `between` is called
    with the Outcome (None when the launch raised) after `act` and before the
    log is written, for every call that is recorded, and `report` is the
    caller-owned dict `record` fills. A call with a
    `keep` (from `plan_keep`) launches in its retained session's resume or
    mint form under its account's home (none for an ambient entry), is bookkept into that session's
    record, and retires it if its launch raises; `one_turn` bounds the call to
    one turn where the runner can. `KeepWarmer`, built by `keep_warmer(root,
    cfg)` only when the dial and keep-warm are on, is the dispatcher's
    non-blocking keep-warm (see its docstring). Inside the blackout window
    (`agent_common.blackout_at`) `act`, and so `call`, raises
    `BlackoutRefused` before anything is built, accounted, recorded or
    launched, for every call but one whose role is ADJUDICATE and whose `wi`
    has an active claim in the primary checkout's registry; a refused
    retained call's lease is released. `through_blackout(launch)` is the
    loop's handling: it waits the window out and retries the launch. In a
    checkout whose commit floor is inactive (its commit hooks are not on,
    `kitlib.commit_hooks`), `act`, and so `call`, raises `HooksOffRefused`
    first, for every call, the same way: before anything is built,
    accounted, recorded or launched, a refused retained call's lease
    released; it is not a `BlackoutRefused`, so `through_blackout` does not
    wait it out.

Contract IF-282: the adjudication request and the sign-in probe, the surface
    the loop's route and the coordinator's entry point share.
    `AdjudicationRequest` carries `root`, the brief class `brief`, `route`
    (the registry row the caller SELECTED; None: no route), the work item
    `wi`, `role` (default ADJUDICATE), the operator's `prompt_templates`
    overrides (None: the shipped templates), the call's wall `deadline`
    in seconds (None: 7200), the `scope` a loop review round is kept under
    ("" for an adjudication; WI-887), and the `account` its entry names
    (None: the ambient login; WI-798). `adjudication_keep(request)` returns the
    Keep the call launches under, or None where the `[adjudicator]` dial (or,
    for a review round, the `[reviewer]` dial) does not cover it; its lease is the deadline plus 300 s, and its governing
    template identity covers the templates of every class the dial retains,
    so switching between retained classes does not drain the session, or,
    for a review round, the reviewer template its brief is built from.
    `signin_status(root, account, row=None, env=None, run=None)` reads an
    account's readiness from its own source only, with no model call and
    nothing created (WI-798): `ambient` for an ambient entry (no account; no
    kit-held home and no sign-in gate); for a token account (one declaring a
    `token_file_variable`, OI-110 (b)) `signed-in` exactly when the file that
    variable names is present, readable and not empty, else `missing` (an
    unset variable included), nothing run; for a login account `missing`
    when its home is absent, else its CLI's status command (`claude auth
    status`, `codex login status`) run under the launch's composed
    environment less the credential, only its documented answers reading
    `signed-in` or `missing`, any other answer, failure or timeout
    `unknown`. `launch_credential(account)` returns `{<the CLI's token
    variable>: token}` (claude `CLAUDE_CODE_OAUTH_TOKEN`), read at that
    launch from the account's declared file (`{}` for an ambient entry or a
    login account), or raises `SigninRefused`. A covered call whose account
    does not read `signed-in` raises `SigninRefused` before any lease is
    taken. THE ONE LAUNCH-ENVIRONMENT RULE (`_launch_parts`, composed once per
    call): the ambient environment, then the route's declared env, then the
    account's declared env, then the account home's variables
    (`session_adapters.home_env` over `session_keep.account_home`), then the
    credential; a name both the route's and the account's env declare, or a
    route env declaring its CLI's home variable under an account, is refused
    before launch. Every launch site takes it: an unretained launch through
    `launch_env(root, row, account)` / `entry_env(root, registry, entry)`,
    a retained one through `prepare_launch`, and the version and sign-in
    probes and keep-warm through the prepared launch. The kit creates a
    token account's home, empty, never a login account's: an absent login
    home refuses the launch naming the command that provisions it
    (`provision_command`). Every retained launch, an adjudication on either
    route or a keep-warm ping, is prepared by `prepare_launch(root, row,
    account)` from the registry row and account its caller SELECTED (the
    loop's from the registry it drew from, the coordinator's resolved entry,
    the warmer's own); the registry is not read again. It returns a
    `Prepared` launch from that one snapshot (its
    family, template, model and tier, which the call launches and is
    accounted as; the route's and the account's declared pairs, never a
    merged environment; the credential; the account home; and the ONE
    executable, an absolute path resolved
    there once on the `PATH` of the composed launch environment, a name with
    a directory part taken against the root). The runner-version probe
    (`cli_version(prepared)`) and the launch both run that executable and
    never resolve the command name again. The probe runs under
    `probe_env(prepared)`, the composed launch environment less the
    credential's names, so it never receives the token. It raises
    `SigninRefused` when the runner does not resolve on that `PATH`
    (`RUNNER_REFUSAL`, naming the runner and whether the `PATH` is the
    route's declared one or the ambient one), when the token cannot be read,
    or when the route or the declared account declares a source its CLI
    ranks above the account's own (`COMPETING_CREDENTIALS[cli]`, any value;
    names compared by `agent_route.env_name_key`, case-insensitively on
    Windows) or a token account's template carries `--bare`
    (`refuse_competing`). A token refusal names dev-setup and the
    variable or the conflict, never the path or the token; nothing signs in,
    nothing is stripped silently, and nothing falls back to OAuth, the
    ambient login, a fresh session or another account's home.
    `compose_env(ambient, prepared)` is a retained launch's
    environment, and `call.env` is not consulted: the ambient environment
    less every name the launch sets and, under a declared account, every
    source its CLI ranks above the account's own home or token
    (`COMPETING_CREDENTIALS[cli]`, by `agent_route.env_name_key`; an ambient
    entry withholds none), or, for a CLI whose sources are open-ended
    (opencode), only its declared base (`BASE_ENVIRONMENT[cli]`) and the
    kit's own names (`KIT_INHERITED`), then the route's and the account's declared pairs, the home and the token, the
    launch's one environment credential. The redaction removes every
    verbatim occurrence of the credential's exact value from each physical
    output line and from the captured stream, before the result, the usage,
    the session log, the raw log or the retention record reads it. An
    occurrence the launched process writes in another representation
    (escaped, encoded, or split across lines) is not removed: no standard
    encoder produces one for the token's ASCII characters (Python's
    `json.dumps` and Node's `JSON.stringify` leave them unescaped), so only
    the launched process can emit one by its own choice, and it already holds
    the token (the bound below). BOUNDS, not covered: credential sources the
    CLI reads from settings files (`apiKeyHelper`, a settings `env` block, a
    managed gateway sign-in); and the launched process itself, which holds
    the token as it held the OAuth credential file in that home before, so
    its own transcript in the home and its tool subprocesses can see it.
"""

import atexit
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import uuid
from dataclasses import dataclass, field, replace
from pathlib import Path

try:
    import adjudicate_brief
    import agent_common
    import agent_route
    import agent_session
    import session_adapters
    import session_keep
    from kitlib import commit_hooks
    from kitlib import provenance
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import adjudicate_brief
    import agent_common
    import agent_route
    import agent_session
    import session_adapters
    import session_keep
    from kitlib import commit_hooks
    from kitlib import provenance

# The headless launch. Bound here so a test replaces the launch of every call
# in one place (`monkeypatch.setattr(session_service, "run_session", ...)`).
run_session = agent_session.run_session


@dataclass
class Call:
    """The data one model call differs by. A role supplies these and nothing
    else; the service owns everything that launches and records.

    Implements: SR-222, LLR-269
    """

    root: object
    role: str
    template: str = ""
    model: str = ""
    prompt: str = ""
    provider: str = ""
    tier: str = ""
    route_id: str = ""
    source_event: str = ""
    attempt_id: str = ""
    attribution: dict = field(default_factory=dict)
    env: object = None
    timeout: object = None
    idle_timeout: object = None
    on_line: object = None
    attached: bool = False
    runner: object = None
    keep: object = None
    one_turn: bool = False
    wi: str = ""
    # A thread id the call resumes WITHOUT a retained session (the
    # coordinator's authoring turn); never together with `keep`.
    resume: str = ""


@dataclass
class Outcome:
    """What one call returned and how it was accounted."""

    root: object
    code: int
    text: str
    timed_out: object
    stream: str
    metrics: dict


def call_succeeded(outcome):
    """Did the call itself succeed? From its real failure signals, never its
    displayed outcome or a commit's presence: exit 0, no timeout, and no
    error result the CLI reported (`is_error` in its JSON result). The ONE
    derivation both adjudication routes hand `adjudicate_brief.record_outcome`
    (WI-841 round 13): the loop's and the coordinator's calls are both an
    `Outcome`.

    Implements: SR-232, LLR-310
    """
    data = agent_session.parse_json_result(outcome.text or "")
    return outcome.code == 0 and not outcome.timed_out and not data.get("is_error")


def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def run_attached(argv, root, _timeout, *, stdin_input=None):
    """The launch for a hands-on sitting: stdio stays the terminal's, so
    nothing is captured. A `{prompt}` template leaves stdin to the person; a
    template without one pipes the prompt in, then the CLI proceeds (text
    mode is load-bearing: a str input on a binary pipe is a TypeError)."""
    if stdin_input is None:
        proc = subprocess.run(argv, cwd=str(root))
    else:
        proc = subprocess.run(argv, cwd=str(root), input=stdin_input, text=True)
    return proc.returncode, "", False


def _launch(call, argv, stdin_input, env, redact):
    """Run the prepared argv through the call's launch; each live line reaches
    the call's renderer through `redact` (`_redactor`)."""
    if call.attached:
        runner = call.runner or run_attached
        return runner(argv, call.root, call.timeout, stdin_input=stdin_input)
    runner = call.runner or run_session
    shown = call.on_line
    return runner(
        argv,
        call.root,
        call.timeout,
        env=env,
        on_line=None if shown is None else (lambda line: shown(redact(line))),
        stdin_input=stdin_input,
        idle_timeout=call.idle_timeout,
    )


def _as_prepared(call):
    """A retained call as its prepared route snapshot launches it: family,
    template, model and tier from `call.keep.prepared`, whatever copy of the
    row the caller held; any other call unchanged.

    Implements: SR-227, LLR-305
    """
    if call.keep is None:
        return call
    p = call.keep.prepared
    return replace(
        call, provider=p.family, template=p.template, model=p.model, tier=p.tier
    )


def _runner_argv(call, argv):
    """`argv` with a retained call's runner replaced by its prepared
    `executable`, the one the version probe ran; any other call unchanged.

    Implements: SR-227, LLR-305
    """
    if call.keep is None or not argv:
        return argv
    return [call.keep.prepared.executable, *argv[1:]]


def _launch_env(call):
    """The environment the call launches under: the call's own, or None to
    inherit the ambient one exactly. A retained call launches under its
    prepared environment alone (`compose_env` over the ambient one), and
    `call.env` is not consulted.

    Implements: SR-227, LLR-305
    """
    if call.keep is None:
        return call.env
    return compose_env(os.environ, call.keep.prepared)


def _redactor(keep, env=None):
    """The function that removes the exact value of every credential this
    launch carries from a text, so whatever the launched process echoes never
    reaches a renderer, log, record or result; the identity when the launch
    carries none. A retained launch's credential is its prepared one; an
    unretained launch's is any token variable (`session_adapters.
    TOKEN_VARIABLES`) its environment `env` sets, as a token account's does.
    Exact values, not credential shapes.

    Implements: SR-227, LLR-305
    """
    values = list(keep.prepared.credential.values()) if keep else []
    names = session_adapters.TOKEN_VARIABLES.values()
    values += [env[name] for name in names if keep is None and env and name in env]
    values = [v for v in values if v]

    def redact(text):
        for value in values:
            text = text.replace(value, "[REDACTED]")
        return text

    return redact


def _resumes(call):
    """Whether the call continues an existing thread: a retained session
    holding one, or an unretained `resume`."""
    return bool((call.keep and call.keep.session_id) or call.resume)


def _identity(call):
    """The accounting a call carries before it runs: who asked, on which
    route, for which model."""
    row = {
        "invocation-id": uuid.uuid4().hex,
        "started-at": _now(),
        "role": call.role,
        "source-event": call.source_event,
        "attempt-id": call.attempt_id,
        "provider": call.provider or "",
        "tier": call.tier or "",
        "roster-row": call.route_id or "",
        "gen_ai.request.model": call.model or "",
        # WI-887's audit columns: whether the session was minted fresh or
        # resumed, and the scope it is kept under. No gate reads them.
        "session-mode": "resumed" if _resumes(call) else "fresh",
        "keep-scope": call.keep.scope if call.keep else "",
    }
    row.update(call.attribution)
    return row


def _status(usage):
    """`usage-source`/`usage-status` from a usage record: known when both
    input and output were reported, partial when anything was, else
    unavailable — so a blank never reads as a zero."""
    counts = [usage.get(k, "") for k in session_adapters.USAGE_COUNT_KEYS]
    reported = [c for c in counts if c != ""] or usage.get("cost-usd", "") != ""
    both = (
        usage.get("gen_ai.usage.input_tokens", "") != ""
        and usage.get("gen_ai.usage.output_tokens", "") != ""
    )
    return {
        "usage-source": "reported" if reported else "unknown",
        "usage-status": "known" if both else ("partial" if reported else "unavailable"),
    }


def _timeout_kind(timed_out):
    """The deadline that ended the call: `idle`, `wall`, or "" for none."""
    if isinstance(timed_out, str):
        return timed_out
    return "wall" if timed_out else ""


def _one_thread(call):
    """Refuse a call that names its thread twice: a retained session (`keep`)
    and an unretained `resume`. Raises ValueError.

    Implements: SR-243, LLR-269
    """
    if call.resume and call.keep is not None:
        raise ValueError(
            "session service: a call resumes a retained session or an unretained "
            "thread, never both (keep and resume {!r})".format(call.resume)
        )


def _thread_argv(call, adapter, argv):
    """`(argv, minted_id)`: a retained call's resume or mint form
    (`session_keep.keep_argv`), an unretained `resume`'s resume form, or the
    argv unchanged for a fresh unretained call.

    Implements: SR-243, LLR-269
    """
    if call.keep is not None:
        return session_keep.keep_argv(adapter, argv, call.keep)
    if call.resume:
        return adapter.resume(argv, call.resume), ""
    return argv, ""


def act(call, metrics=None):
    """Launch one call and account it; see Contract IF-246. In a checkout
    whose commit hooks are not on (`kitlib.commit_hooks`), a call raises
    HooksOffRefused, and inside the blackout window a call the window does
    not admit (`launch_refusal`) raises BlackoutRefused: either before
    anything is built, accounted or launched, and a retained call's lease is
    released first (`keep_release`, which does not raise on store-lock
    contention).

    A call naming both a retained session (`keep`) and an unretained
    `resume` then raises ValueError, before anything is accounted.

    Implements: SR-222, SR-229, SR-243, LLR-269
    """
    hooks_off = commit_hooks.hooks_refusal(call.root)
    refused = _refused_launch(call, hooks_off)
    if refused is not None:
        if call.keep is not None:
            session_keep.keep_release(call.root, call.keep)
        raise refused
    _one_thread(call)
    metrics = {} if metrics is None else metrics
    call = _as_prepared(call)
    argv, stdin_input = agent_session.build_argv(call.template, call.model, call.prompt)
    argv = _runner_argv(call, argv)
    adapter = (
        session_adapters.PlainAdapter()
        if call.attached
        else session_adapters.adapter_for(argv)
    )
    argv, scratch = adapter.prepare(argv)
    argv, minted = _thread_argv(call, adapter, argv)
    if call.one_turn:
        argv = adapter.one_turn(argv)
    env = _launch_env(call)
    redact = _redactor(call.keep, env)
    metrics.update(_identity(call))
    started = time.monotonic()
    try:
        code, stream, timed_out = _launch(call, argv, stdin_input, env, redact)
    except BaseException as exc:
        # BaseException, not Exception: a Ctrl-C in an attached sitting must
        # leave a record with its wall-secs and ended-at filled.
        adapter.final_text("", scratch, -1)  # remove the adapter's scratch file
        if call.keep is not None:
            session_keep.keep_abandon(call.root, call.keep, "session unusable")
        metrics.update(adapter.usage(""))
        metrics.update(_status({}))
        metrics.update(
            {
                "ended-at": _now(),
                "wall-secs": int(round(time.monotonic() - started)),
                "exit-code": "",
                "timeout": "",
                "error": type(exc).__name__,
            }
        )
        raise
    stream = redact(stream)  # before anything reads, keeps or shows it
    text = redact(adapter.final_text(stream, scratch, code))
    usage = adapter.usage(stream)
    session_id, used, window, pct = adapter.context(
        stream,
        os.environ if env is None else env,
        usage["gen_ai.conversation.id"],
    )
    metrics.update(usage)
    metrics.update(_status(usage))
    metrics.update(
        {
            "ended-at": _now(),
            "wall-secs": int(round(time.monotonic() - started)),
            "exit-code": code,
            "timeout": _timeout_kind(timed_out),
            "session-id": session_id or usage["gen_ai.conversation.id"],
            "context-used": used,
            "context-window": window,
            "context-pct": pct,
        }
    )
    outcome = Outcome(call.root, code, text, timed_out, stream, metrics)
    if call.keep is not None:
        metrics.update(
            session_keep.keep_bookkeep(
                call.root,
                call.keep,
                minted,
                outcome,
                reported_error=session_adapters.reported_error(stream),
                auth_failed=session_adapters.auth_failed(stream),
                compaction=adapter.compaction(
                    stream, os.environ if env is None else env, metrics["session-id"]
                ),
            )
        )
    return outcome


# --- the blackout window at the launch boundary (WI-834) ---------------------------


class BlackoutRefused(Exception):
    """A launch the blackout window refuses, carrying the window as read at
    the refusal (`blackout`, an `agent_common.blackout_at` answer). The loop
    waits it out and retries (`through_blackout`); the coordinator's route
    reports it.

    Implements: SR-237, LLR-317
    """

    def __init__(self, blackout, role):
        self.blackout = blackout
        window, end = blackout.window, blackout.end
        super().__init__(
            "session service: the blackout window {} UTC is open until {} UTC; a "
            "{} launch is refused inside it (only a wrap-up adjudication of a work "
            "item whose claim is active starts a session there)".format(
                window, end.strftime("%Y-%m-%d %H:%M"), role or "model"
            )
        )


# --- the commit hooks at the launch boundary (WI-926) -------------------------


class HooksOffRefused(Exception):
    """A launch refused because the checkout's commit hooks are not on,
    carrying the check's refusal text. Not a BlackoutRefused: there is no
    window to wait out, so `through_blackout` lets it propagate and every
    route reports it.

    Implements: SR-240, LLR-340
    """


def _refused_launch(call, hooks_off):
    """The refusal `act` raises, or None: a HooksOffRefused carrying the
    commit-hooks check's text `hooks_off` when it is not None, else the
    blackout window's answer (`launch_refusal`).

    Implements: SR-240, LLR-340
    """
    if hooks_off is not None:
        return HooksOffRefused("session service: " + hooks_off)
    return launch_refusal(call)


def claim_active(root, wi):
    """Whether work item `wi`'s claim is `active` in the PRIMARY checkout's
    registry: a lane's own checkout is not enough, because the close-first
    rule moves its spec before the final verdict.

    Implements: SR-237, LLR-317
    """
    primary = session_keep.primary_out_dir(root).parent
    row = agent_common.load_wi_registry(primary).get(wi) or {}
    return (row.get("Status") or "").strip().lower() == "active"


def launch_refusal(call):
    """BlackoutRefused for a call launched inside the blackout window, or
    None. Every caller is refused there but one: a call whose role is
    ADJUDICATE for a named work item (`call.wi`, carried apart from the keep,
    so the rule holds with retention off) whose claim is active
    (`claim_active`). Claims are refused inside the window on every route, so
    an active claim is a lane claimed before it. Derived from the role and the
    registry; no caller selects it.

    Implements: SR-237, LLR-317
    """
    blackout = agent_common.blackout_at(Path(call.root) / "docs")
    if not blackout.inside:
        return None
    if call.role == "ADJUDICATE" and call.wi and claim_active(call.root, call.wi):
        return None
    return BlackoutRefused(blackout, call.role)


def through_blackout(launch, emit=print, sleep=time.sleep):
    """`launch()`, and while the blackout window refuses it, the window waited
    out (`agent_common.blackout_wait`: a banner and a countdown) and the
    launch retried: the loop's handling of the launch boundary, on every loop
    route (a worker session, the interactive sitting, a recovery probe, a
    dual-plan round).

    Implements: SR-237, LLR-317
    """
    while True:
        try:
            return launch()
        except BlackoutRefused as refused:
            b = refused.blackout
            agent_common.blackout_wait(
                max(1, b.wake_seconds), b.window, b.end, emit, sleep
            )


def _write_raw(raw_dir, name, stream):
    """The raw captured stream, untracked beside the tracked log: a debugging
    convenience, never load-bearing, so a filesystem failure is swallowed."""
    try:
        Path(raw_dir).mkdir(parents=True, exist_ok=True)
        (Path(raw_dir) / name).write_bytes(stream.encode("utf-8", "replace"))
    except OSError:
        pass


def record(
    outcome,
    meta=None,
    *,
    iter_dir=None,
    raw_dir=None,
    raw_name=None,
    session=None,
    label=None,
    report=None,
):
    """Write the call's one session log and commit it in a lane, or spool it
    outside one; see Contract IF-246.

    The log's row is the caller's `meta` overlaid by the outcome's accounting,
    so what the service measured is never shadowed by what a role guessed; the
    transcript is the whole captured stream (redacted and bounded by the log
    writer), not a reduced result. Where it goes is derived from the root
    alone (`lane_branch`): in a claimed lane it is written under `iter_dir`
    (default `docs/iteration/`) and committed; anywhere else it is written to
    the primary checkout's spool (`spool_dir`; `iter_dir` is ignored) and
    nothing is committed, and a spool that cannot be written raises OSError.
    A caller-owned `report` dict is filled with the log's `path`, whether it
    was `spooled` or `committed`, and the commit's `refusal` text ("" for
    none).

    Implements: SR-222, SR-243, LLR-269
    """
    root = Path(outcome.root)
    row = dict(meta or {})
    row.update(outcome.metrics)
    if raw_dir is not None and raw_name:
        _write_raw(raw_dir, raw_name, outcome.stream)
    spooled = lane_branch(root) is None
    if spooled:
        target = spool_dir(root)
    elif iter_dir is not None:
        target = Path(iter_dir)
    else:
        target = root / "docs" / "iteration"
    path = agent_common.write_session_log(target, row, outcome.stream)
    refusal = ""
    if not spooled:
        label = label or "{} {}".format(row.get("phase", ""), row.get("outcome", ""))
        refusal = agent_common.commit_telemetry(
            root, session or row["invocation-id"], label, [path]
        )
    if report is not None:
        report.update(
            path=path,
            spooled=spooled,
            committed=not spooled and not refusal,
            refusal=refusal or "",
        )
    return path


def spool_dir(root):
    """The directory a call recorded outside a claimed lane writes its log
    to: `out/sessions/spool/` of the primary checkout, machine-local and
    untracked.

    Implements: SR-243, LLR-269
    """
    return session_keep.primary_out_dir(root) / "sessions" / "spool"


def _lane_claims(root):
    """`(branch, ids)` for a root that is a linked worktree on a branch, or
    None. The ids are those the branch's own committed tree holds under
    `docs/work/active/<branch>/` (`integrate.claimed_ids_on_branch`), united
    with those trunk's committed tree still holds there (a lane closed under
    close-first and not yet merged). An unreadable read adds no id, and an
    undeclared trunk adds none from trunk.
    """
    import integrate  # deferred: a heavy import only a record's lane read needs

    records = agent_common.worktree_records(root)
    index = agent_common.worktree_index(records, root)
    # None: not the top of a worktree; 0: the primary checkout; no branch: detached
    if not index or not records[index][1]:
        return None
    branch = records[index][1]
    ids = set(integrate.claimed_ids_on_branch(root, branch) or ())
    try:
        trunk = agent_common.trunk_name(root)
    except agent_common.TrunkUndeclared:
        return branch, ids
    trunk_ref, folder = "refs/heads/" + trunk, integrate.ACTIVE + "/" + branch
    for path in integrate._branch_tree_paths(root, trunk_ref, folder) or ():
        wid = integrate._spec_id(path.rsplit("/", 1)[-1])
        if wid is not None:
            ids.add(wid)
    return branch, ids


def lane_branch(root):
    """The branch of the claimed lane `root` is the top of, or None. A lane
    is a linked worktree on a branch whose committed tree, or trunk's, holds
    a claim under `docs/work/active/<branch>/`; the primary checkout (on any
    branch), a detached HEAD, a root that is not the top of a worktree, and a
    branch neither readable tree shows claimed (a claim read that cannot be
    read adds no claim) are not.

    Implements: SR-243, LLR-269, LLR-346
    """
    claims = _lane_claims(root)
    return claims[0] if claims and claims[1] else None


def lane_wis(root):
    """The work item ids the lane at `root` holds claimed, on its branch's
    tree or on trunk's; empty outside a lane.

    Implements: SR-243, LLR-269, LLR-346
    """
    claims = _lane_claims(root)
    return set(claims[1]) if claims else set()


# The name `_call_row` gives a standard call's log, as the log writer spells
# it: `call_<invocation id>-<YYYYmmdd>-<HHMMSS>.log`. No gate-log name
# (`kitlib.verdict.SESSION_LOG_RE`) has this shape.
CALL_LOG_RE = re.compile(r"^call_[0-9a-f]{32}-(?P<stamp>\d{8}-\d{6})\.log$")


def is_call_log(name):
    """Whether the file name `name` is a standard call's session log, the
    name `_call_row` gives.

    Implements: SR-243, LLR-269, LLR-346
    """
    return CALL_LOG_RE.match(name) is not None


def _call_row(metrics, word):
    """The standard row for a call no worker composed a row for."""
    return {
        "session": "call_" + metrics["invocation-id"],
        "stamp": time.strftime("%Y%m%d-%H%M%S"),
        "date": time.strftime("%Y-%m-%d %H:%M"),
        "model": metrics.get("gen_ai.request.model", ""),
        "phase": metrics.get("role", ""),
        "outcome": word,
    }


def call(call_, *, between=None, report=None):
    """`act` then `record` with the standard row; see Contract IF-246.

    The record is written even when the launch raised (a Ctrl-C in an
    attached sitting is recorded INTERRUPTED and re-raised), but not for a
    command template that could not be built, which launched nothing.
    `between`, when given, is the caller's one seam between the two: it is
    called with the Outcome (None when the launch raised) after `act` and
    before the log is written, for every call that is recorded; the record
    is written even when it raises. `report` is handed to `record`.

    Implements: SR-222, SR-243, LLR-269
    """
    metrics = {}
    outcome = None
    word = "ERROR"
    try:
        outcome = act(call_, metrics)
        word = _outcome_word(outcome)
        return outcome
    except KeyboardInterrupt:
        word = "INTERRUPTED"
        raise
    finally:
        _record_call(call_, outcome, metrics, word, between=between, report=report)


def _outcome_word(outcome):
    if outcome.timed_out:
        return "TIMEOUT"
    return "COMPLETED" if outcome.code == 0 else "ERROR"


def _record_call(call_, outcome, metrics, word, *, between=None, report=None):
    """Record one standard call, even one whose launch raised; nothing for
    a call that was never accounted (its template could not be built). A
    caller's `between` runs first, given the outcome (None when the launch
    raised)."""
    if "invocation-id" not in metrics:
        return
    try:
        if between is not None:
            between(outcome)
    finally:
        done = outcome or Outcome(call_.root, -1, "", False, "", metrics)
        record(done, _call_row(metrics, word), report=report)


# --- keep: adjudicator session retention through act and record -----------------
#
# The rules and the store are session_keep's; what lives here is only what
# launches or records: the runner's version read the drift rule compares, and
# the keep-warm ping, which is an ordinary call made off the dispatcher's tick.

KEEPWARM_PROMPT = "ack"
KEEPWARM_TIMEOUT = 300


def cli_version(prepared):
    """The `--version` line of the `prepared` launch's runner, or "" when it
    cannot be read. Read once per retained launch (never at the off dial), so
    a runner upgraded under a retained session drains it. It runs the one
    executable the launch runs (`prepared.executable`), under the launch's
    environment with the credential withheld (`probe_env`), so its output
    cannot carry the token.

    Implements: SR-227, LLR-270
    """
    try:
        proc = subprocess.run(
            [prepared.executable, "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
            env=probe_env(prepared),
            stdin=subprocess.DEVNULL,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    lines = [ln.strip() for ln in (proc.stdout or "").splitlines() if ln.strip()]
    return lines[0] if proc.returncode == 0 and lines else ""


def plan_keep(root, cfg, *, route, role, brief, scope="", account=None, **kw):
    """The Keep an adjudication, or a loop review round under `scope`
    (WI-887), launches under, or None: `session_keep.keep_for` with the
    runner's version read first, and only when the keep operation covers the
    call, so the off dial launches nothing extra. `route` is the
    registry row the caller SELECTED (None: no route) and `account` the
    declared account its entry names (None: the ambient login). A covered
    call is refused first, before any lease exists, unless its launch
    prepares from that row and account (`prepare_launch`) and its account
    reads signed in (`require_signin`). The runner's version is probed from
    the prepared launch (its executable, its environment less the
    credential), and the Keep carries the prepared launch and is keyed by the
    account: the selected entry is what is planned for, probed, launched and
    accounted.

    Implements: SR-222, SR-227, LLR-270, LLR-336
    """
    route_id = getattr(route, "id", "") or ""
    if route is None or not session_keep.applies(cfg, role, brief, route_id, scope):
        return None
    prepared = prepare_launch(root, route, account)
    require_signin(root, prepared)
    return session_keep.keep_for(
        root,
        cfg,
        role=role,
        brief=brief,
        route_id=route_id,
        family=prepared.family,
        cli_version=cli_version(prepared),
        prepared=prepared,
        scope=scope,
        account=account.id if account is not None else "",
        **kw,
    )


# --- the adjudication request: one composition for every route -------------------


@dataclass(frozen=True)
class AdjudicationRequest:
    """What an adjudication's keep is planned from, composed alike on the
    loop's route and the coordinator's: the brief class, the `route` (the
    registry row the caller SELECTED, whose family, template, model and
    declared environment everything downstream reads; None: no route), the
    work item, the operator's `prompt_templates` overrides (keyed by prompt
    key; None or empty: the shipped templates), and the call's wall
    `deadline` in seconds (None: the default session wall), which the lease
    outlives, the `scope` a loop review round is kept under ("" for an
    adjudication; WI-887), and the `account` the selected entry names (an
    `agent_route.Account`; None: the person's ambient login; WI-798). The governing template identity is not the
    caller's to compose: the keep derives it from the dial's retained set,
    or a review round's own reviewer template (`adjudication_keep`).

    Implements: SR-227, LLR-305
    """

    root: object
    brief: str
    route: object
    wi: str
    role: str = "ADJUDICATE"
    prompt_templates: object = None
    deadline: object = None
    scope: str = ""
    account: object = None


# The session wall a request with no deadline is bounded by, and how long the
# lease outlives the wall, so a call is never resumed under while it runs.
DEFAULT_DEADLINE = 7200
LEASE_MARGIN = 300


def adjudication_keep(request):
    """The Keep the request's adjudication launches under, or None: the
    repository's `[adjudicator]` dial, the work-item registry for the clear
    point, and a lease tied to the call's deadline, handed to `plan_keep`.
    The governing template identity covers every class the dial retains
    (`adjudicate_brief.governing_templates` over `retain_for`, under the
    request's overrides), so a retained session judges every retained class
    under one identity and drains only when a template, or an override,
    changes; a loop review round's identity is its own reviewer template, by
    the request's role (WI-887). Raises SigninRefused as `plan_keep` does.

    Implements: SR-227, LLR-305
    """
    cfg = session_keep.keep_config(request.root)
    paths, texts = adjudicate_brief.governing_templates(
        cfg.retain_for, request.prompt_templates, request.role
    )
    return plan_keep(
        request.root,
        cfg,
        route=request.route,
        role=request.role,
        brief=request.brief,
        scope=request.scope,
        account=request.account,
        wi=request.wi,
        rows=agent_common.load_wi_registry(request.root),
        template_paths=paths,
        template_texts=texts,
        lease_seconds=(request.deadline or DEFAULT_DEADLINE) + LEASE_MARGIN,
    )


# --- the sign-in probe and the refusal -------------------------------------------

SIGNED_IN = "signed-in"
SIGNIN_MISSING = "missing"
SIGNIN_UNKNOWN = "unknown"
SIGNIN_AMBIENT = "ambient"
SIGNIN_TIMEOUT = 60


class SigninRefused(Exception):
    """A launch refused before it starts: its account cannot authenticate (a
    token that cannot be read, a login home that is absent or does not read
    signed in), its environment conflicts, its account home cannot be placed,
    or its runner does not resolve.

    Implements: SR-227, LLR-305
    """


def _codex_signin(code, text):
    """`codex login status` (0.160.1) answers with exactly one line on
    stderr: `Logged in using <method>` at exit 0, or `Not logged in` at exit
    1. The whole response is read: besides blank lines, only codex's own
    PATH-alias warning (printed for a home under the system temporary
    directory) may precede it. Any other line, a second answer, or another
    exit code is unknown.
    """
    lines = [
        line.rstrip()
        for line in text.splitlines()
        if line.strip() and not line.startswith(_CODEX_WARNING)
    ]
    if len(lines) != 1:
        return SIGNIN_UNKNOWN
    if code == 0 and _CODEX_SIGNED_IN.fullmatch(lines[0]):
        return SIGNED_IN
    if code == 1 and lines[0] == "Not logged in":
        return SIGNIN_MISSING
    return SIGNIN_UNKNOWN


# The one warning codex 0.160.1 prints ahead of its answer (observed under a
# home in the system temporary directory), and its signed-in line.
_CODEX_WARNING = "WARNING: proceeding, even though we could not create PATH aliases"
_CODEX_SIGNED_IN = re.compile(r"Logged in using \S.*")


def _claude_signin(code, text):
    """`claude auth status` (2.1.296) answers with exactly one JSON object
    whose `loggedIn` is a boolean: true at exit 0, false at exit 1 (an empty
    home read `"loggedIn": false` at exit 1, the ambient login `true` at exit
    0, on this box 2026-10-11). Anything else is unknown.

    Implements: SR-222, LLR-336
    """
    try:
        data = json.loads(text)
    except ValueError:
        return SIGNIN_UNKNOWN
    logged = data.get("loggedIn") if isinstance(data, dict) else None
    if code == 0 and logged is True:
        return SIGNED_IN
    if code == 1 and logged is False:
        return SIGNIN_MISSING
    return SIGNIN_UNKNOWN


# Each CLI's status command, which reads the home and calls no model, and its
# reader. A login account of a CLI with no row here probes unknown.
# Implements: SR-222, LLR-336
SIGNIN_PROBES = {
    "codex": (("codex", "login", "status"), _codex_signin),
    "claude": (("claude", "auth", "status"), _claude_signin),
}

# Each CLI's sign-in command, which a person runs under the account home's
# variables to provision a login account (`provision_command`). The kit never
# runs it.
# Implements: SR-222, LLR-336
LOGIN_COMMANDS = {
    "claude": "claude auth login",
    "codex": "codex login",
    "opencode": "opencode auth login",
    "gemini": "gemini",
}


def provision_command(account):
    """How a person signs `account` in under its own home, in prose: each
    home variable with its value quoted, then the sign-in command
    (`with CODEX_HOME set to "<home>", run `codex login``), or "" when its
    home cannot be placed. It holds no shell syntax, so it reads the same to
    every shell; the one text the refusals, the `signin` command and
    dev-setup show. Never run by the kit.

    Implements: SR-222, LLR-336
    """
    home = session_keep.account_home(account.id)
    if home is None:
        return ""
    pairs = session_adapters.home_env(account.cli, home)
    variables = " and ".join('{} set to "{}"'.format(k, v) for k, v in pairs.items())
    login = LOGIN_COMMANDS.get(account.cli, account.cli)
    return "with {}, run `{}`".format(variables, login)


# Per CLI, the environment credential sources it ranks ABOVE the credential a
# declared account selects (the login in the account's own home, or its
# long-lived token). A qualified launch, and its probes, leave every one out
# of the environment they inherit and carry only the account's own source
# (`_compose`); an account or a qualified route env that declares one is
# refused (`refuse_competing`). An ambient entry is untouched. Sources:
# - claude: the cloud-provider switches, then the bearer token and the API
#   key, which `-p` always uses when present (code.claude.com/docs/en/
#   authentication, "Authentication precedence", read 2026-10-08), and the
#   long-lived token, which outranks a login in the home (a token account
#   re-adds its own from its file), and the named profile and federation
#   rule, which rank above `/login` ("Anthropic profiles and federation
#   credentials": "unset ANTHROPIC_PROFILE, or unset either federation
#   variable", read 2026-10-11);
# - gemini: every variable Gemini CLI's `getAuthTypeFromEnv` reads to select
#   a non-login auth type when the home configures none (headless:
#   `configuredAuthType || getAuthTypeFromEnv()`, packages/cli/src/
#   validateNonInterActiveAuth.ts), in packages/core/src/core/
#   contentGenerator.ts (github.com/google-gemini/gemini-cli, main, read
#   2026-10-11): Vertex, the gateway, the API key and compute ADC; plus the
#   Vertex credentials `createContentGeneratorConfig` and the authentication
#   docs (geminicli.com/docs/get-started/authentication) name. Not withheld:
#   `GOOGLE_GENAI_USE_GCA` (it selects the home login itself) and
#   `GOOGLE_CLOUD_PROJECT`/`_LOCATION` (they select nothing, and an
#   organisation's Google login reads the project too);
# - codex: the per-CLI authentication table of the WI-788 design,
#   docs/plans/2026-10-04-wi788-design/2-sessions-routing-accounts.md
#   ("Auth and account", read 2026-10-04). It names codex's source only as
#   "API key", so codex's are that provider's conventional variables.
# - opencode: `OPENCODE_AUTH_CONTENT`, which its `Auth.all` reads in place of
#   the home's `auth.json` (opencode-ai 1.18.30, read 2026-10-20), so it is
#   refused when a route or account declares it. Its other sources are
#   open-ended, so a qualified opencode launch inherits nothing outside
#   `BASE_ENVIRONMENT` rather than withholding a list.
# Settings-file sources (`apiKeyHelper`, a settings `env` block, a managed
# gateway sign-in) are not environment variables and are NOT covered here.
# Implements: SR-227, LLR-305
COMPETING_CREDENTIALS = {
    "claude": (
        "CLAUDE_CODE_USE_BEDROCK",
        "CLAUDE_CODE_USE_VERTEX",
        "CLAUDE_CODE_USE_FOUNDRY",
        "ANTHROPIC_AUTH_TOKEN",
        "ANTHROPIC_API_KEY",
        session_adapters.TOKEN_VARIABLES["claude"],
        "ANTHROPIC_PROFILE",
        "ANTHROPIC_FEDERATION_RULE_ID",
    ),
    "codex": ("CODEX_API_KEY", "OPENAI_API_KEY"),
    "gemini": (
        "GOOGLE_GENAI_USE_VERTEXAI",
        "GOOGLE_GEMINI_BASE_URL",
        "GEMINI_API_KEY",
        "CLOUD_SHELL",
        "GEMINI_CLI_USE_COMPUTE_ADC",
        "GOOGLE_API_KEY",
        "GOOGLE_APPLICATION_CREDENTIALS",
    ),
    "opencode": ("OPENCODE_AUTH_CONTENT",),
}

# The ambient variables a qualified launch of a CLI with no withheld list
# inherits, beside the kit's own (`KIT_INHERITED`), and nothing else: none is
# a credential. opencode's credential sources are open-ended, so no list of
# them can be complete (opencode-ai
# 1.18.30, its provider loader and `Auth.all`, read 2026-10-20): every
# provider in its model catalog, fetched and refreshed hourly, loads from the
# first set variable of that provider's `env` names; each provider SDK reads
# its own default key even when the configuration empties that list; and
# `OPENCODE_AUTH_CONTENT` replaces the home's `auth.json`. So the launch
# starts from the platform's path, system and user directories, temporary
# directory, terminal and locale, and the network-transport variables a proxy
# or a CA bundle needs; then the route's and the account's declared pairs and
# the account home (`_compose`). Anything else it needs, a provider key
# included, is declared on the route or the account. Names compare by
# `agent_route.env_name_key`. An unqualified entry inherits the ambient
# environment unchanged.
# Implements: SR-222, LLR-336
BASE_ENVIRONMENT = {
    "opencode": (
        "PATH",
        "PATHEXT",
        "SYSTEMROOT",
        "SYSTEMDRIVE",
        "WINDIR",
        "COMSPEC",
        "PROGRAMDATA",
        "PROGRAMFILES",
        "PROGRAMFILES(X86)",
        "PROGRAMW6432",
        "COMMONPROGRAMFILES",
        "ALLUSERSPROFILE",
        "PUBLIC",
        "HOME",
        "USERPROFILE",
        "HOMEDRIVE",
        "HOMEPATH",
        "APPDATA",
        "LOCALAPPDATA",
        "USER",
        "USERNAME",
        "LOGNAME",
        "SHELL",
        "XDG_CONFIG_HOME",
        "XDG_CACHE_HOME",
        "XDG_STATE_HOME",
        "XDG_RUNTIME_DIR",
        "TEMP",
        "TMP",
        "TMPDIR",
        "TERM",
        "COLORTERM",
        "NO_COLOR",
        "LANG",
        "LANGUAGE",
        "LC_ALL",
        "LC_CTYPE",
        "LC_MESSAGES",
        "TZ",
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "NO_PROXY",
        "http_proxy",
        "https_proxy",
        "no_proxy",
        "SSL_CERT_FILE",
        "SSL_CERT_DIR",
        "NODE_EXTRA_CA_CERTS",
    ),
}


# The kit-owned variables every launch inherits, whatever its account's base
# keeps: each is named by the module that owns it, never copied here, and
# none is a credential. The loop marker is set in the loop's own process
# (`provenance.mark_loop_process`), and the commit floors a child's commits
# run read it to tell the loop's commits from a person's. A new kit variable
# a child must inherit joins this tuple by its owner's constant.
# Implements: SR-222, LLR-336
KIT_INHERITED = (provenance.LOOP_SESSION_ENV,)


def _read_token(variable):
    """`(token, problem)` for a token account: the token in the file its
    declared environment variable `variable` names (OI-110 (b): the variable
    is the account's `token_file_variable`), stripped, and "", or "" and why
    there is none (the variable unset, the file missing or unreadable, or
    empty). The problem names the variable, never the path; the token is
    never printed.

    Implements: SR-227, LLR-305
    """
    path = os.environ.get(variable, "").strip()
    if not path:
        return "", "{} is unset".format(variable)
    try:
        token = Path(path).read_text(encoding="utf-8").strip()
    except (OSError, ValueError):
        return "", "the file {} names is missing or unreadable".format(variable)
    if not token:
        return "", "the file {} names is empty".format(variable)
    return token, ""


TOKEN_REFUSAL = (
    "launch [{account}]: refused before launch: the account's long-lived token "
    "reads {status} to the sign-in probe: {problem}. Run dev-setup's one-time "
    "`claude setup-token` step, keep the token in a file outside the "
    "repository, and set {variable} to that file; nothing signs in "
    "automatically, and the call never falls back to OAuth, the ambient "
    "login, a fresh session or another account's home."
)


def _token_refusal(account, status, problem):
    """The refusal of a token account's launch, naming dev-setup and the
    variable, never the path or the token.

    Implements: SR-227, LLR-305
    """
    return SigninRefused(
        TOKEN_REFUSAL.format(
            account=account.id,
            status=status,
            problem=problem,
            variable=account.token_file_variable,
        )
    )


COMPETING_REFUSAL = (
    "launch [{account}]: refused before launch: the route or the account "
    "declares {names}, so the CLI would not authenticate with {source}. "
    "Remove it from the env or the command template; nothing is stripped "
    "silently and nothing falls back."
)
_TOKEN_SOURCE = "the long-lived token dev-setup's `claude setup-token` step provides"
_LOGIN_SOURCE = "the login in its own home"


def refuse_competing(account, template, declared):
    """Refuse (SigninRefused) a declared account's launch whose route or
    account DECLARES a source its CLI ranks above the account's own
    (`COMPETING_CREDENTIALS[account.cli]`, a name in `declared`, their env
    cells together, compared by `agent_route.env_name_key` whatever its
    value), or, for a token account, whose template carries `--bare`, which
    does not read the token. An ambient source is not the route's choice and is left out of the
    launch instead (`_compose`).

    Implements: SR-227, LLR-305
    """
    competing = {
        agent_route.env_name_key(k) for k in COMPETING_CREDENTIALS.get(account.cli, ())
    }
    names = [k for k in declared if agent_route.env_name_key(k) in competing]
    try:
        bare = "--bare" in agent_session.split_cmd(template)
    except ValueError:
        bare = False  # a template that cannot be split cannot launch either
    token = bool(account.token_file_variable)
    names += ["--bare"] if bare and token else []
    if names:
        raise SigninRefused(
            COMPETING_REFUSAL.format(
                account=account.id,
                names=", ".join(names),
                source=_TOKEN_SOURCE if token else _LOGIN_SOURCE,
            )
        )


@dataclass(frozen=True)
class Prepared:
    """A retained launch, validated, from ONE snapshot of its route row and
    its account: the row's family, command template, model and tier (what
    the call launches and is accounted as), the ONE resolved `executable`
    both the version probe and the launch run, the route's own declared
    environment pairs, the credential the CLI reads (`{}` unless the account
    authenticates with a token), the account home (`{variable: path}`, `{}`
    for an ambient entry), the account's own declared pairs and the account
    (None: the person's ambient login). Built only by `prepare_launch`; the
    environment parts are never stored, logged or shown in a repr.

    Implements: SR-227, LLR-305
    """

    family: str
    template: str
    model: str
    tier: str
    executable: str
    declared: dict = field(repr=False)
    credential: dict = field(repr=False)
    home: dict = field(repr=False)
    account_env: dict = field(default_factory=dict, repr=False)
    account: object = field(default=None, repr=False)


CONFLICT_REFUSAL = (
    "launch [{account}]: refused before launch: {why}; neither side silently "
    "overrides the other, and nothing falls back to the ambient login."
)
NO_CONFIG_DIR_REFUSAL = (
    "launch [{account}]: refused before launch: the user configuration "
    "directory account homes live under cannot be resolved (%APPDATA% on "
    "Windows; $XDG_CONFIG_HOME, else ~/.config, on POSIX); nothing falls back "
    "to a checkout-local home or the ambient login."
)
SIGNIN_REFUSAL = (
    "launch [{account}]: refused before launch: the account home {home} reads "
    "{status} to the sign-in probe. Sign it in there yourself: {provision}. "
    "Nothing signs in automatically, and the call never falls back to the "
    "ambient login, a fresh session or another account's home."
)


def _launch_parts(root, row, account):
    """`(declared, account_env, home, credential)` of a launch on `row` under
    `account` (None: the person's ambient login): THE ONE LAUNCH-ENVIRONMENT
    RULE's parts (WI-798), composed in that order over the ambient
    environment (`_compose`) by every launch site, the version and sign-in
    probes and keep-warm. An ambient entry has its route's declared pairs
    only: no kit-held home and no credential. A qualified entry is refused
    when its route and account conflict (`agent_route.qualifier_problem`),
    when its home cannot be placed, when its token cannot be read or a
    source its CLI ranks above the account's own is declared
    (`refuse_competing`), or when it is a login account whose home is
    absent (naming the provisioning command). The kit creates a token
    account's home, empty, and never a login account's.

    Implements: SR-222, LLR-336
    """
    declared = agent_route.parse_env(row.env or "")
    if account is None:
        return declared, {}, {}, {}
    why = agent_route.qualifier_problem(row, account, account.id)
    if why:
        raise SigninRefused(CONFLICT_REFUSAL.format(account=account.id, why=why))
    path = session_keep.account_home(account.id)
    if path is None:
        raise SigninRefused(NO_CONFIG_DIR_REFUSAL.format(account=account.id))
    account_env = agent_route.parse_env(account.env)
    credential = launch_credential(account)
    refuse_competing(account, row.cmd_template, {**declared, **account_env})
    if credential:
        path.mkdir(parents=True, exist_ok=True)  # holds no credential: kit-made
    elif not path.is_dir():
        raise SigninRefused(
            SIGNIN_REFUSAL.format(
                account=account.id,
                home=path,
                status=SIGNIN_MISSING,
                provision=provision_command(account),
            )
        )
    home = session_adapters.home_env(account.cli, path)
    return declared, account_env, home, credential


def prepare_launch(root, row, account=None):
    """The `Prepared` launch of a retained call on `row` under `account`
    (None: the ambient login), or SigninRefused: the ONE step every retained
    launch (an adjudication on either route, a keep-warm ping) takes. `row`
    is the registry row the caller SELECTED; the registry is never read here,
    so that one snapshot supplies everything: family, template, model, tier
    and declared pairs (`act` launches it), the account's parts
    (`_launch_parts`), and the executable, resolved here once or refused
    (`_resolve_executable`).

    Implements: SR-227, LLR-305
    """
    family = (row.family or "").upper()
    declared, account_env, home, credential = _launch_parts(root, row, account)
    launch_env = _compose(os.environ, declared, account_env, home, credential, account)
    model = row.model or row.id
    return Prepared(
        family=family,
        template=row.cmd_template,
        model=model,
        tier=row.tier or "",
        executable=_resolve_executable(
            root, family, (row.cmd_template, model), declared, launch_env
        ),
        declared=declared,
        credential=credential,
        home=home,
        account_env=account_env,
        account=account,
    )


def launch_env(root, row, account=None):
    """The environment an UNRETAINED launch on `row` under `account` runs
    under, by the one rule (`_launch_parts`, `_compose`), or None to inherit
    the ambient one exactly; raises SigninRefused as `_launch_parts` does.

    Implements: SR-222, LLR-336
    """
    return _compose(os.environ, *_launch_parts(root, row, account), account)


def entry_env(root, registry, entry):
    """`launch_env` for an enabled `entry` of `registry`: its route row and
    its account, resolved once here (`agent_route.account_of`).

    Implements: SR-222, LLR-336
    """
    row = registry[agent_route.entry_route(entry)]
    return launch_env(root, row, agent_route.account_of(registry, entry))


RUNNER_REFUSAL = (
    "keep [{family}]: refused before launch: the runner {runner!r} is not found "
    "on {source}. Install it there, or declare a PATH in the route's env that "
    "holds it; nothing launches another runner in its place."
)


def _resolve_executable(root, family, route, declared, launch_env):
    """The absolute path of the runner a `route` (its template and model)
    names (`agent_route.route_runner`, the launcher's own parse of the
    template, which also names the route's CLI), found on the `PATH`
    of the composed launch environment `launch_env` (None: the ambient one),
    a name with a directory part taken against `root`; SigninRefused
    (`RUNNER_REFUSAL`, naming the route's `declared` PATH or the ambient one)
    when it does not resolve or the template names none.
    The one resolution: the probe and the launch run what it returns, and
    nothing resolves the command name again.

    Implements: SR-227, LLR-305
    """
    template, model = route
    name = agent_route.route_runner(template, model)
    if os.path.dirname(name):
        name = str(Path(root, name))
    path_key = agent_route.env_name_key("PATH")
    env = os.environ if launch_env is None else launch_env
    path = next(
        (v for k, v in env.items() if agent_route.env_name_key(k) == path_key), None
    )
    resolved = shutil.which(name, path=path) if name else None
    if not resolved:
        own = any(agent_route.env_name_key(k) == path_key for k in declared)
        raise SigninRefused(
            RUNNER_REFUSAL.format(
                family=family,
                runner=name or template,
                source="the route's declared PATH" if own else "the ambient PATH",
            )
        )
    return os.path.abspath(resolved)


def probe_env(prepared):
    """The environment the runner-version and sign-in probes run under: the
    launch's own (`compose_env` over the ambient one), less every name of the
    launch's credential, which only the launch receives.

    Implements: SR-227, LLR-305
    """
    env = compose_env(os.environ, prepared)
    if env is None or not prepared.credential:
        return env
    withheld = {agent_route.env_name_key(k) for k in prepared.credential}
    return {k: v for k, v in env.items() if agent_route.env_name_key(k) not in withheld}


def compose_env(ambient, prepared):
    """The environment of a prepared launch: the ambient one, less every name
    the launch sets itself and, for a declared account, every source its CLI
    ranks above the account's own (`COMPETING_CREDENTIALS`) or everything
    outside its CLI's declared base (`BASE_ENVIRONMENT`) and the kit's own
    names (`KIT_INHERITED`), then the route's declared pairs, the account's, the account home and the credential.
    Names compare by `agent_route.env_name_key`, so no second spelling of one
    survives; None (inherit exactly) when the launch sets nothing.

    Implements: SR-227, LLR-305
    """
    return _compose(
        ambient,
        prepared.declared,
        prepared.account_env,
        prepared.home,
        prepared.credential,
        prepared.account,
    )


def _compose(ambient, declared, account_env, home, credential, account):
    """`compose_env` over the launch's parts, before they are a `Prepared`
    (`prepare_launch` resolves the executable on its result). The selected
    `account` (None: the ambient login) owns what is inherited
    (`_ambient_base`): a declared account inherits no ambient source its CLI
    ranks above its own home or token, or only its CLI's declared base, and
    carries only its own credential; an ambient entry inherits the ambient
    environment unchanged.

    Implements: SR-222, SR-227, LLR-305, LLR-336
    """
    overlay = {}
    for pairs in (declared, account_env, home, credential):
        for name, value in pairs.items():
            overlay[agent_route.env_name_key(name)] = (name, value)
    if not overlay:
        return None
    base = {
        k: v
        for k, v in _ambient_base(ambient, account).items()
        if agent_route.env_name_key(k) not in overlay
    }
    return {**base, **dict(overlay.values())}


def _ambient_base(ambient, account):
    """The part of the `ambient` environment a launch under `account` (None:
    the ambient login) starts from: all of it for an ambient entry; for a
    declared account of a CLI with a `BASE_ENVIRONMENT`, only those names and
    the kit's own (`KIT_INHERITED`); otherwise all of it less every source its
    CLI ranks above the account's own home or token (`COMPETING_CREDENTIALS`).
    Names compare by `agent_route.env_name_key`.

    Implements: SR-222, LLR-336
    """
    if account is None:
        return ambient
    key = agent_route.env_name_key
    kept = BASE_ENVIRONMENT.get(account.cli)
    if kept is not None:
        names = {key(k) for k in (*kept, *KIT_INHERITED)}
        return {k: v for k, v in ambient.items() if key(k) in names}
    withheld = {key(k) for k in COMPETING_CREDENTIALS.get(account.cli, ())}
    return {k: v for k, v in ambient.items() if key(k) not in withheld}


def launch_credential(account):
    """`{variable: token}` the CLI of a launch under `account` reads its
    long-lived token from, read now from the file the account's declared
    `token_file_variable` names, or `{}` for an ambient entry or a login
    account; raises SigninRefused, naming dev-setup, when the token cannot be
    read. Nothing falls back to OAuth.

    Implements: SR-227, LLR-305
    """
    if account is None or not account.token_file_variable:
        return {}
    token, problem = _read_token(account.token_file_variable)
    if problem:
        raise _token_refusal(account, SIGNIN_MISSING, problem)
    return {session_adapters.TOKEN_VARIABLES[account.cli]: token}


def _run_status(argv, env):
    """Run a status command: `(exit code, stdout and stderr)`."""
    path = (env or os.environ).get("PATH")
    exe = shutil.which(argv[0], path=path) or argv[0]
    proc = subprocess.run(
        [exe, *argv[1:]],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=SIGNIN_TIMEOUT,
        env=env,
        stdin=subprocess.DEVNULL,
    )
    return proc.returncode, (proc.stdout or "") + "\n" + (proc.stderr or "")


def signin_status(root, account, *, row=None, env=None, run=None):
    """Whether `account` can authenticate, read from its own source only:
    `signed-in`, `missing` or `unknown`, or `ambient` for an ambient entry
    (None), which has no kit-held home and no sign-in gate. A token account
    is signed in exactly when the file its `token_file_variable` names is
    present, readable and not empty, and missing otherwise (an unset
    variable included); nothing runs. A login account's home is resolved
    without being created; an absent home is missing without running
    anything; otherwise its CLI's status command runs under `env` (default:
    the launch environment of `row` under the account, `launch_env`, with no
    `row` the account's CLI with no route env; a launch refusal reads
    unknown;
    `run(argv, env)`, default a bounded subprocess); only its documented
    exit-and-output pairs read signed-in or missing, and any other answer,
    failure or timeout is unknown. Nothing is created and no model is called.

    Implements: SR-222, SR-227, LLR-305, LLR-336
    """
    if account is None:
        return SIGNIN_AMBIENT
    if account.token_file_variable:
        missing = _read_token(account.token_file_variable)[1]
        return SIGNIN_MISSING if missing else SIGNED_IN
    home = session_keep.account_home(account.id)
    probe = SIGNIN_PROBES.get(account.cli)
    if home is None or probe is None:
        return SIGNIN_UNKNOWN
    if not home.is_dir():
        return SIGNIN_MISSING
    if env is None:
        bare = agent_route.Model("", "", "", "", "", account.cli)
        try:
            env = launch_env(root, row or bare, account)
        except SigninRefused:
            return SIGNIN_UNKNOWN
    argv, read = probe
    try:
        code, text = (run or _run_status)(list(argv), env)
    except (OSError, subprocess.SubprocessError, ValueError):
        return SIGNIN_UNKNOWN
    return read(code, text or "")


def require_signin(root, prepared):
    """Refuse (SigninRefused) a retained launch whose account the probe does
    not read as signed in, run under the prepared launch's own environment
    less its credential (`probe_env`); an ambient entry has nothing to sign
    in to. A token account's refusal names its declared variable and
    dev-setup's `claude setup-token` step; a login account's names the
    command that provisions its home. An unverified login account is
    printed (`agent_route.unverified_lines`), never refused here.

    Implements: SR-222, SR-227, LLR-305, LLR-336
    """
    account = prepared.account
    if account is None:
        return
    status = signin_status(root, account, env=probe_env(prepared))
    if status != SIGNED_IN and account.token_file_variable:
        problem = _read_token(account.token_file_variable)[1]
        raise _token_refusal(
            account, status, problem or "the token could not be confirmed"
        )
    if status != SIGNED_IN:
        raise SigninRefused(
            SIGNIN_REFUSAL.format(
                account=account.id,
                home=session_keep.account_home(account.id),
                status=status,
                provision=provision_command(account),
            )
        )


class KeepWarmer:
    """The dispatcher's keep-warm, bounded four ways.

    - It never blocks the tick: a due ping runs on its own thread, and a tick
      while one is in flight starts no second one.
    - It never races a lane: the ping holds the route's lease
      (`session_keep.take_warm_lease`), which an adjudication waits on, and a
      ping whose session is leased to an adjudication does not run.
    - It writes a record only under the store lock, each write through its
      own temporary file; the ping's bookkeeping (`act`) publishes its store
      marker first, so a held lock defers it to the next locked read and
      never raises.
    - It moves trunk only through the serialized telemetry path: the ping's
      thread launches and accounts, and its session log is written and
      committed later on the dispatcher's own thread, between polls, and only
      over a clean trunk — the thread that runs the merges, so never beside one.

    A due ping that cannot run says why, once per reason, through `tick`'s
    returned lines.

    Implements: SR-227, LLR-270
    """

    def __init__(
        self,
        root,
        cfg,
        registry,
        *,
        entries,
        runner=None,
        clock=time.time,
        dirty=None,
    ):
        self.root = Path(root)
        self.cfg = cfg
        self.registry = registry
        self.routes = _warm_routes(registry, entries)
        self.runner = runner
        self.clock = clock
        self.dirty = dirty or (
            lambda: agent_common.substantive_working_tree_dirty(root)
        )
        self.thread = None
        self.finished = []
        self.last_said = None

    def tick(self, work_pending):
        """One dispatcher tick: record a finished ping, else start a due one.
        Returns the lines to log (skips and holds, each said once)."""
        lines = []
        if self.thread is not None and not self.thread.is_alive():
            self.thread.join()
            self.thread = None
        if self.finished:
            if self.dirty():
                self._raise_unended()  # the stop never waits on the hold
                lines.append("keep-warm: session log held (the trunk is dirty)")
                return self._once(lines)  # one ping at a time, until recorded
            self._record_finished()
        if self.thread is not None:
            if session_keep.due_routes(self.root, self.cfg, self.clock(), work_pending):
                lines.append("keep-warm: skipped (a ping is in flight)")
            return self._once(lines)
        keep, reason = session_keep.take_warm_lease(
            self.root,
            self.cfg,
            now=self.clock(),
            work_pending=work_pending,
            holder="keep-warm:" + uuid.uuid4().hex,
            prepare=self._prepare,
            routes=self.routes,
        )
        if reason:
            lines.append("keep-warm: skipped ({})".format(reason))
        elif keep is not None:
            self._start(keep)
        return self._once(lines)

    def _once(self, lines):
        """Each line once while it stays true, so a held state is not repeated
        every half-second tick."""
        said = tuple(lines)
        if said == self.last_said:
            return []
        self.last_said = said
        return lines

    def _prepare(self, route_id, account):
        """`(prepared, reason)` for a due entry's ping, asked by
        `take_warm_lease` before it takes any lease: the same `prepare_launch`
        an adjudication takes, from the row and account this warmer selected
        its entries from (one snapshot), its refusal the reason the ping is
        skipped."""
        row = self.registry[route_id]
        found = getattr(self.registry, "accounts", {}).get(account) if account else None
        if account and found is None:
            return None, "account {} is no longer declared".format(account)
        try:
            return prepare_launch(self.root, row, found), ""
        except SigninRefused as refused:
            return None, str(refused)

    def _start(self, keep):
        p = keep.prepared
        call_ = Call(
            root=self.root,
            role="KEEP-WARM",
            template=p.template,
            model=p.model,
            prompt=KEEPWARM_PROMPT,
            provider=p.family,
            tier=p.tier,
            route_id=keep.route_id,
            source_event="keep-warm",
            timeout=KEEPWARM_TIMEOUT,
            keep=keep,
            one_turn=True,
            runner=self.runner,
        )
        self.thread = threading.Thread(target=self._ping, args=(call_,), daemon=True)
        self.thread.start()

    def _ping(self, call_):
        """The ping's thread: launch and account only. Nothing here touches
        the working tree or git. A `TreeNotEnded` rides with the finished
        call to the dispatcher's thread, which raises it; any other failure
        is a recorded ERROR.

        Implements: SR-227, SR-238, LLR-270
        """
        metrics = {}
        outcome, word, unended = None, "ERROR", None
        try:
            outcome = act(call_, metrics)
            word = _outcome_word(outcome)
        except agent_session.TreeNotEnded as exc:
            unended = exc
        except BaseException:  # recorded ERROR on the dispatcher's thread
            pass
        self.finished.append((call_, outcome, metrics, word, unended))

    def _record_finished(self):
        """Record each finished call, then raise a carried `TreeNotEnded`;
        a failed recording rides as its context and never replaces it.

        Implements: SR-227, SR-238, LLR-270
        """
        while self.finished:
            call_, outcome, metrics, word, unended = self.finished.pop(0)
            try:
                _record_call(call_, outcome, metrics, word)
            finally:
                if unended is not None:
                    raise unended

    def _raise_unended(self):
        """Over a dirty trunk: raise a carried `TreeNotEnded` unrecorded, so
        the hold on the session log never defers the stop.

        Implements: SR-227, SR-238, LLR-270
        """
        for *_, unended in self.finished:
            if unended is not None:
                raise unended

    def finish(self, timeout=KEEPWARM_TIMEOUT + 30):
        """At the run's end: wait out a ping in flight, then record every
        finished one through the same rule the tick applies — only over a
        clean trunk. Over a dirty one the log is not written, and the reason
        is printed and returned instead, so the exit path never commits beside
        uncommitted work. A carried `TreeNotEnded` is raised either way, after
        the recording over a clean trunk, unrecorded over a dirty one.

        Implements: SR-227, SR-238, LLR-270
        """
        if self.thread is not None:
            self.thread.join(timeout)
        if not self.finished:
            return []
        if self.dirty():
            line = "keep-warm: session log not recorded (the trunk is dirty)"
            print(line, file=sys.stderr)
            self._raise_unended()
            self.finished.clear()
            return [line]
        self._record_finished()
        return []


def _warm_routes(registry, entries):
    """The `(route_id, account)` entries a keep-warm may ping: each enabled
    entry whose route is a row of `registry` its runner can bound to one
    turn and whose account, if it names one, is declared there (WI-798: a
    record whose entry is no longer enabled, or whose account no longer
    resolves, is never pinged).

    Implements: SR-222, SR-227, LLR-270, LLR-336
    """
    routes = set()
    for entry in entries:
        route_id = agent_route.entry_route(entry)
        account = agent_route.entry_account(entry)
        row = registry.get(route_id)
        declared = not account or account in getattr(registry, "accounts", {})
        if (
            row is not None
            and declared
            and _pings_one_turn(row.cmd_template, row.model or "")
        ):
            routes.add((route_id, account))
    return routes


def _pings_one_turn(template, model):
    """Whether a route's runner can be bounded to one turn, so it may be
    pinged (claude's); a template that cannot be built cannot be pinged.

    Implements: SR-227, LLR-270
    """
    try:
        argv, _ = agent_session.build_argv(template, model, KEEPWARM_PROMPT)
    except ValueError:
        return False
    return session_adapters.adapter_for(argv).bounds_one_turn()


def keep_warmer(root, cfg):
    """The run's KeepWarmer, or None — and so no thread, no store read and no
    ping — unless the dial and `keepwarm_minutes` are both on.

    Implements: SR-227, LLR-270
    """
    if not cfg.enabled or cfg.keepwarm_minutes <= 0:
        return None
    docs = Path(root) / "docs"
    registry, _errors = agent_route.load_registry(docs / "agents.toml")
    try:
        tokens = agent_route.load_enabled(docs / "agents-enabled")
    except agent_route.EnabledUnreadable as exc:
        print("keep-warm: off ({})".format(exc), file=sys.stderr)
        return None
    entries, _ = agent_route.resolve_enabled(
        tokens, registry, agent_route.load_tag_rank(docs / "agents.toml")
    )
    warmer = KeepWarmer(root, cfg, registry, entries=entries)
    atexit.register(warmer.finish)  # a ping in flight is recorded at the run's end
    return warmer
