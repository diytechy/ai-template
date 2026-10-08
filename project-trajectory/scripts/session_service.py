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
    and an optional `keep` (from `keep_for`) naming the retained session the
    call resumes or mints. `act(call, metrics=None)` returns an `Outcome` (`root`, `code`,
    `text`, `timed_out`, `stream`, `metrics`): `text` is the CLI's result as
    its adapter reads it, `stream` the whole captured output, and `metrics`
    the call's accounting, filled into a caller-owned dict so a call that
    raises is still accounted before the exception propagates; a command
    template that cannot be built raises ValueError before anything is
    accounted. `record(outcome, meta, ...)` writes one session log from the
    caller's row overlaid by the outcome's accounting, the raw stream to
    `raw_dir/raw_name` when given, and commits the log; it returns the log's
    path. `call(call)` is `act` then `record` with the standard row, recording
    even when the launch raised, and returns the `Outcome`. A call with a
    `keep` (from `plan_keep`) launches in its retained session's resume or
    mint form under its dedicated CLI home, is bookkept into that session's
    record, and retires it if its launch raises; `one_turn` bounds the call to
    one turn where the runner can. `KeepWarmer`, built by `keep_warmer(root,
    cfg)` only when the dial and keep-warm are on, is the dispatcher's
    non-blocking keep-warm (see its docstring).

Contract IF-282: the adjudication request and the sign-in probe, the surface
    the loop's route and the coordinator's entry point share.
    `AdjudicationRequest` carries `root`, the brief class `brief`, `route`
    (the registry row the caller SELECTED; None: no route), the work item
    `wi`, `role` (default ADJUDICATE), the operator's `prompt_templates`
    overrides (None: the shipped templates), and the call's wall `deadline`
    in seconds (None: 7200). `adjudication_keep(request)` returns the Keep the
    adjudication launches under, or None where the `[adjudicator]` dial does
    not cover it; its lease is the deadline plus 300 s, and its governing
    template identity covers the templates of every class the dial retains,
    so switching between retained classes does not drain the session.
    `signin_status(root, family, run=None)` returns `signed-in`, `missing` or
    `unknown` for the family's dedicated CLI home, with no model call and
    nothing created. A family in `TOKEN_VARIABLES` (ANTHROPIC) reads its
    long-lived token: signed-in exactly when the file its declared
    environment variable `AGENT_CLAUDE_TOKEN_FILE` names is present, readable
    and not empty, and missing otherwise, an unset variable included; nothing
    runs. Any other family with a dedicated home: an absent home is missing;
    otherwise its status command (`codex login status`) runs under it, and
    only its documented answers read signed-in or missing; any other answer,
    a failure or a timeout is unknown. `launch_credential(family)` returns
    `{CLAUDE_CODE_OAUTH_TOKEN: token}`, read at that launch from the declared
    file (`{}` for a family without a token), or raises `SigninRefused`. A
    covered call whose family has a dedicated home and does not read
    `signed-in` raises `SigninRefused` before any lease is taken or home
    created. Every retained launch, an adjudication on either route or a
    keep-warm ping, is prepared by `prepare_launch(root, row)` from the
    registry row its caller SELECTED (the loop's from the registry it drew
    from, the coordinator's resolved row, the warmer's own); the registry is
    not read again. It returns a `Prepared` launch from that one snapshot (its
    family, template, model and tier, which the call launches and is
    accounted as; its own declared pairs, never a merged environment; the
    credential; the home; and the ONE executable, an absolute path resolved
    there once on the `PATH` of the composed launch environment, a name with
    a directory part taken against the root). The runner-version probe
    (`cli_version(prepared)`) and the launch both run that executable and
    never resolve the command name again. The probe runs under
    `probe_env(prepared)`, the composed launch environment less the
    credential's names, so it never receives the token. It raises
    `SigninRefused` when the runner does not resolve on that `PATH`
    (`RUNNER_REFUSAL`, naming the runner and whether the `PATH` is the
    route's declared one or the ambient one), when the token cannot be read,
    or when the route declares a `COMPETING_CREDENTIALS` source (any value;
    names compared by `_name_key`, case-insensitively on Windows) or carries
    `--bare` (`refuse_competing`). A token refusal names dev-setup and the
    variable or the conflict, never the path or the token; nothing signs in,
    nothing is stripped silently, and nothing falls back to OAuth, a fresh
    session or
    the default home. `compose_env(ambient, prepared)` is the launch's
    environment, and `call.env` is not consulted: the ambient environment
    less every name the launch sets and every `COMPETING_CREDENTIALS` source
    (by `_name_key`), then the declared pairs, the home and the token, the
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
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import adjudicate_brief
    import agent_common
    import agent_route
    import agent_session
    import session_adapters
    import session_keep

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


def _redactor(keep):
    """The function that removes the exact value of every credential this
    launch carries from a text, so whatever the launched process echoes never
    reaches a renderer, log, record or result; the identity when the launch
    carries none. Exact values, not credential shapes.

    Implements: SR-227, LLR-305
    """
    values = [v for v in (keep.prepared.credential.values() if keep else ()) if v]

    def redact(text):
        for value in values:
            text = text.replace(value, "[REDACTED]")
        return text

    return redact


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


def act(call, metrics=None):
    """Launch one call and account it; see Contract IF-246.

    Implements: SR-222, LLR-269
    """
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
    minted = ""
    if call.keep is not None:
        argv, minted = session_keep.keep_argv(adapter, argv, call.keep)
    if call.one_turn:
        argv = adapter.one_turn(argv)
    env = _launch_env(call)
    redact = _redactor(call.keep)
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
):
    """Write the call's one session log and commit it; see Contract IF-246.

    The log's row is the caller's `meta` overlaid by the outcome's accounting,
    so what the service measured is never shadowed by what a role guessed; the
    transcript is the whole captured stream (redacted and bounded by the log
    writer), not a reduced result.

    Implements: SR-222, LLR-269
    """
    root = Path(outcome.root)
    row = dict(meta or {})
    row.update(outcome.metrics)
    if raw_dir is not None and raw_name:
        _write_raw(raw_dir, raw_name, outcome.stream)
    path = agent_common.write_session_log(
        Path(iter_dir) if iter_dir is not None else root / "docs" / "iteration",
        row,
        outcome.stream,
    )
    agent_common.commit_telemetry(
        root,
        session or row["invocation-id"],
        label or "{} {}".format(row.get("phase", ""), row.get("outcome", "")),
        [path],
    )
    return path


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


def call(call_):
    """`act` then `record` with the standard row; see Contract IF-246.

    The record is written even when the launch raised (a Ctrl-C in an
    attached sitting is recorded INTERRUPTED and re-raised), but not for a
    command template that could not be built, which launched nothing.

    Implements: SR-222, LLR-269
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
        _record_call(call_, outcome, metrics, word)


def _outcome_word(outcome):
    if outcome.timed_out:
        return "TIMEOUT"
    return "COMPLETED" if outcome.code == 0 else "ERROR"


def _record_call(call_, outcome, metrics, word):
    """Record one standard call, even one whose launch raised; nothing for
    a call that was never accounted (its template could not be built)."""
    if "invocation-id" not in metrics:
        return
    done = outcome or Outcome(call_.root, -1, "", False, "", metrics)
    record(done, _call_row(metrics, word))


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


def plan_keep(root, cfg, *, route, role, brief, **kw):
    """The Keep an adjudication launches under, or None: `session_keep.keep_for`
    with the runner's version read first, and only when the keep operation
    covers the call, so the off dial launches nothing extra. `route` is the
    registry row the caller SELECTED (None: no route). A covered call is
    refused first, before any lease or home exists, unless its launch
    prepares from that row (`prepare_launch`) and its family's home is signed
    in (`require_signin`). The runner's version is probed from the prepared
    launch (its executable, its environment less the credential), and the
    Keep carries the prepared launch: the selected row is what is planned
    for, probed, launched and accounted.

    Implements: SR-227, LLR-270
    """
    route_id = getattr(route, "id", "") or ""
    if route is None or not session_keep.applies(cfg, role, brief, route_id):
        return None
    prepared = prepare_launch(root, route)
    require_signin(root, prepared.family)
    return session_keep.keep_for(
        root,
        cfg,
        role=role,
        brief=brief,
        route_id=route_id,
        family=prepared.family,
        cli_version=cli_version(prepared),
        prepared=prepared,
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
    outlives. The governing template identity is not the caller's to compose:
    the keep derives it from the dial's retained set (`adjudication_keep`).

    Implements: SR-227, LLR-305
    """

    root: object
    brief: str
    route: object
    wi: str
    role: str = "ADJUDICATE"
    prompt_templates: object = None
    deadline: object = None


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
    changes. Raises SigninRefused as `plan_keep` does.

    Implements: SR-227, LLR-305
    """
    cfg = session_keep.keep_config(request.root)
    paths, texts = adjudicate_brief.governing_templates(
        cfg.retain_for, request.prompt_templates
    )
    return plan_keep(
        request.root,
        cfg,
        route=request.route,
        role=request.role,
        brief=request.brief,
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
SIGNIN_TIMEOUT = 60


class SigninRefused(Exception):
    """A retained launch refused before it starts: its family's dedicated CLI
    home is not signed in, or the probe could not tell.

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


# Each family's status command, which reads the home and calls no model, and
# its reader. A family with a dedicated home and no row here, or in
# TOKEN_VARIABLES, probes unknown.
# Implements: SR-227, LLR-305
SIGNIN_PROBES = {
    "OPENAI": (("codex", "login", "status"), _codex_signin),
}


# The families whose dedicated home authenticates with a long-lived token, and
# for each the declared environment variable naming the token FILE (OI-110
# (b), 2026-10-08: nothing about its path is tracked; dev-setup tells the owner,
# or an adopter, to set it) and the variable the CLI reads the token from in
# headless use (`claude setup-token`, 2.1.289: "Use this token by setting:
# export CLAUDE_CODE_OAUTH_TOKEN=<token>"). Such a home is never signed in
# interactively, so its probe is the token file alone.
# Implements: SR-227, LLR-305
TOKEN_VARIABLES = {"ANTHROPIC": ("AGENT_CLAUDE_TOKEN_FILE", "CLAUDE_CODE_OAUTH_TOKEN")}

# The credential sources the CLI ranks ABOVE `CLAUDE_CODE_OAUTH_TOKEN` that an
# environment can carry: the cloud-provider switches, then the bearer token and
# the API key, which `-p` always uses when present (code.claude.com/docs/en/
# authentication, "Authentication precedence", read 2026-10-08). A token
# launch leaves them out of its environment (`_launch_env`); a route that
# declares one is refused (`refuse_competing`). Settings-file sources
# (`apiKeyHelper`, a settings `env` block, a managed gateway sign-in) are not
# environment variables and are NOT covered here.
# Implements: SR-227, LLR-305
COMPETING_CREDENTIALS = (
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_VERTEX",
    "CLAUDE_CODE_USE_FOUNDRY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_API_KEY",
)


def _read_token(family):
    """`(token, problem)` for a family in TOKEN_VARIABLES: the token in the
    file its declared variable names, stripped, and "", or "" and why there is
    none (the variable unset, the file missing or unreadable, or empty). The
    problem names the variable, never the path; the token is never printed.

    Implements: SR-227, LLR-305
    """
    variable = TOKEN_VARIABLES[family][0]
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
    "keep [{family}]: refused before launch: the dedicated home reads {status} "
    "to the sign-in probe: {problem}. Run dev-setup's one-time `claude "
    "setup-token` step, keep the token in a file outside the repository, and "
    "set {variable} to that file; nothing signs in automatically, and the call "
    "never falls back to OAuth, a fresh session or the default home."
)


def _token_refusal(family, status, problem):
    """The refusal of a token family's retained launch, naming dev-setup and
    the variable, never the path or the token.

    Implements: SR-227, LLR-305
    """
    variable = TOKEN_VARIABLES[family][0]
    return SigninRefused(
        TOKEN_REFUSAL.format(
            family=family, status=status, problem=problem, variable=variable
        )
    )


COMPETING_REFUSAL = (
    "keep [{family}]: refused before launch: the route declares {names}, so the "
    "CLI would not authenticate with the long-lived token dev-setup's "
    "`claude setup-token` step provides. Remove it from the route's env or "
    "command template; nothing is stripped silently and nothing falls back."
)


def refuse_competing(family, template, declared):
    """Refuse (SigninRefused) a token family's retained launch whose route
    DECLARES a COMPETING_CREDENTIALS source (a name in its own `env` cell,
    `declared`, compared by `_name_key` whatever its value) or whose template
    carries `--bare`, which does not read the token. An ambient source is not
    the route's choice and is left out of the launch instead (`compose_env`).

    Implements: SR-227, LLR-305
    """
    competing = {_name_key(k) for k in COMPETING_CREDENTIALS}
    names = [k for k in declared if _name_key(k) in competing]
    try:
        names += ["--bare"] if "--bare" in agent_session.split_cmd(template) else []
    except ValueError:
        pass  # a template that cannot be split cannot launch either
    if names:
        raise SigninRefused(
            COMPETING_REFUSAL.format(family=family.upper(), names=", ".join(names))
        )


# Windows resolves environment variable names case-insensitively, POSIX does
# not: the one rule every comparison of names in a launch environment uses.
# Implements: SR-227, LLR-305
_CASE_INSENSITIVE = os.name == "nt"


def _name_key(name):
    """The name as the platform resolves it (`_CASE_INSENSITIVE`).

    Implements: SR-227, LLR-305
    """
    return name.upper() if _CASE_INSENSITIVE else name


@dataclass(frozen=True)
class Prepared:
    """A retained launch, validated, from ONE snapshot of its route row: the
    row's family, command template, model and tier (what the call launches
    and is accounted as), the ONE resolved `executable` both the version
    probe and the launch run (`""`: it did not resolve), its own declared
    environment pairs, the credential the CLI reads (`{}` for a family
    without a token), and the dedicated home (`{variable: path}`, or `{}`).
    Built only by `prepare_launch`; the environment parts are never stored,
    logged or shown in a repr.

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


def prepare_launch(root, row):
    """The `Prepared` launch of a retained call on `row`, or SigninRefused:
    the ONE step every retained launch (an adjudication on either route, a
    keep-warm ping) takes. `row` is the registry row the caller SELECTED; the
    registry is never read here, so that one snapshot supplies everything:
    family, template, model, tier and declared pairs (`act` launches it), and
    the executable, resolved here once or refused (`_resolve_executable`). A
    token
    family refuses a declared competing source or a `--bare` template
    (`refuse_competing`) and reads its token (`launch_credential`).

    Implements: SR-227, LLR-305
    """
    family = (row.family or "").upper()
    declared = agent_route.parse_env(row.env or "")
    credential = launch_credential(family)
    if credential:
        refuse_competing(family, row.cmd_template, declared)
    home = session_keep.dedicated_home(root, family)
    home = {home[0]: str(home[1])} if home else {}
    launch_env = _compose(os.environ, declared, home, credential)
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
    )


RUNNER_REFUSAL = (
    "keep [{family}]: refused before launch: the runner {runner!r} is not found "
    "on {source}. Install it there, or declare a PATH in the route's env that "
    "holds it; nothing launches another runner in its place."
)


def _resolve_executable(root, family, route, declared, launch_env):
    """The absolute path of the runner a `route` (its template and model)
    names, the template's first token after the argv substitution
    (`agent_session.substitute`), found on the `PATH`
    of the composed launch environment `launch_env` (None: the ambient one),
    a name with a directory part taken against `root`; SigninRefused
    (`RUNNER_REFUSAL`, naming the route's `declared` PATH or the ambient one)
    when it does not resolve or the template names none.
    The one resolution: the probe and the launch run what it returns, and
    nothing resolves the command name again.

    Implements: SR-227, LLR-305
    """
    template, model = route
    try:
        name = agent_session.substitute(agent_session.split_cmd(template)[0], model, "")
    except (ValueError, IndexError):
        name = ""
    if os.path.dirname(name):
        name = str(Path(root, name))
    path_key = _name_key("PATH")
    env = os.environ if launch_env is None else launch_env
    path = next((v for k, v in env.items() if _name_key(k) == path_key), None)
    resolved = shutil.which(name, path=path) if name else None
    if not resolved:
        own = any(_name_key(k) == path_key for k in declared)
        raise SigninRefused(
            RUNNER_REFUSAL.format(
                family=family,
                runner=name or template,
                source="the route's declared PATH" if own else "the ambient PATH",
            )
        )
    return os.path.abspath(resolved)


def probe_env(prepared):
    """The environment the runner-version probe runs under: the launch's own
    (`compose_env` over the ambient one), less every name of the launch's
    credential, which only the launch receives.

    Implements: SR-227, LLR-305
    """
    env = compose_env(os.environ, prepared)
    if env is None or not prepared.credential:
        return env
    withheld = {_name_key(k) for k in prepared.credential}
    return {k: v for k, v in env.items() if _name_key(k) not in withheld}


def compose_env(ambient, prepared):
    """The environment of a prepared launch: the ambient one, less every name
    the launch sets itself and, for a launch with a credential, every
    COMPETING_CREDENTIALS source, then the declared pairs, the home and the
    credential. Names compare by `_name_key`, so no second spelling of one
    survives; None (inherit exactly) when the launch sets nothing.

    Implements: SR-227, LLR-305
    """
    return _compose(ambient, prepared.declared, prepared.home, prepared.credential)


def _compose(ambient, declared, home, credential):
    """`compose_env` over the launch's parts, before they are a `Prepared`
    (`prepare_launch` resolves the executable on its result).

    Implements: SR-227, LLR-305
    """
    overlay = {}
    for pairs in (declared, home, credential):
        for name, value in pairs.items():
            overlay[_name_key(name)] = (name, value)
    if not overlay:
        return None
    drop = set(overlay)
    if credential:
        drop |= {_name_key(k) for k in COMPETING_CREDENTIALS}
    base = {k: v for k, v in ambient.items() if _name_key(k) not in drop}
    return {**base, **dict(overlay.values())}


def launch_credential(family):
    """`{variable: token}` the CLI of a retained `family` launch reads its
    long-lived token from, read now from the file the declared variable
    names, or `{}` for a family with no token; raises SigninRefused, naming
    dev-setup, when the token cannot be read. Nothing falls back to OAuth.

    Implements: SR-227, LLR-305
    """
    family = (family or "").upper()
    if family not in TOKEN_VARIABLES:
        return {}
    token, problem = _read_token(family)
    if problem:
        raise _token_refusal(family, SIGNIN_MISSING, problem)
    return {TOKEN_VARIABLES[family][1]: token}


def _run_status(argv, env):
    """Run a status command: `(exit code, stdout and stderr)`."""
    exe = shutil.which(argv[0]) or argv[0]
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


def signin_status(root, family, *, run=None):
    """Whether `family`'s dedicated CLI home is signed in: `signed-in`,
    `missing` or `unknown`. A family with a long-lived token
    (TOKEN_VARIABLES) is signed in exactly when the file its declared
    variable names is present, readable and not empty, and missing otherwise
    (an unset variable included); nothing runs. For any other family the home
    is resolved without being created; an absent home is missing without
    running anything; otherwise the family's status command runs under it
    (`run(argv, env)`, default a bounded subprocess); only its documented
    exit-and-output pairs read signed-in or missing, and any other answer,
    failure or timeout is unknown.

    Implements: SR-227, LLR-305
    """
    if (family or "").upper() in TOKEN_VARIABLES:
        return SIGNIN_MISSING if _read_token(family.upper())[1] else SIGNED_IN
    home = session_keep.dedicated_home(root, family)
    probe = SIGNIN_PROBES.get((family or "").upper())
    if home is None or probe is None:
        return SIGNIN_UNKNOWN
    variable, path = home
    if not path.is_dir():
        return SIGNIN_MISSING
    argv, read = probe
    try:
        code, text = (run or _run_status)(
            list(argv), {**os.environ, variable: str(path)}
        )
    except (OSError, subprocess.SubprocessError, ValueError):
        return SIGNIN_UNKNOWN
    return read(code, text or "")


SIGNIN_REFUSAL = (
    "keep [{family}]: refused before launch: the dedicated CLI home {home} "
    "reads {status} to the sign-in probe. Sign in there through dev-setup; "
    "nothing signs in automatically, and the call never falls back to a "
    "fresh session or the default home."
)


def require_signin(root, family):
    """Refuse (SigninRefused) a retained launch of `family` whose dedicated
    home the probe does not read as signed in; a family with no dedicated
    home has nothing to sign in to. A token family's refusal names its
    declared variable and dev-setup's `claude setup-token` step.

    Implements: SR-227, LLR-305
    """
    family = (family or "").upper()
    if family not in session_keep.HOME_VARIABLES:
        return
    status = signin_status(root, family)
    if status != SIGNED_IN and family in TOKEN_VARIABLES:
        problem = _read_token(family)[1] or "the token could not be confirmed"
        raise _token_refusal(family, status, problem)
    if status != SIGNED_IN:
        _variable, home = session_keep.dedicated_home(root, family)
        raise SigninRefused(
            SIGNIN_REFUSAL.format(family=family, home=home, status=status)
        )


class KeepWarmer:
    """The dispatcher's keep-warm, bounded four ways.

    - It never blocks the tick: a due ping runs on its own thread, and a tick
      while one is in flight starts no second one.
    - It never races a lane: the ping holds the route's lease
      (`session_keep.take_warm_lease`), which an adjudication waits on, and a
      ping whose session is leased to an adjudication does not run.
    - It writes the store only under the store lock (the bookkeeping `act`
      does), each write through its own temporary file.
    - It moves trunk only through the serialized telemetry path: the ping's
      thread launches and accounts, and its session log is written and
      committed later on the dispatcher's own thread, between polls, and only
      over a clean trunk — the thread that runs the merges, so never beside one.

    A due ping that cannot run says why, once per reason, through `tick`'s
    returned lines.

    Implements: SR-227, LLR-270
    """

    def __init__(
        self, root, cfg, registry, *, runner=None, clock=time.time, dirty=None
    ):
        self.root = Path(root)
        self.cfg = cfg
        self.registry = registry
        self.routes = {
            route_id
            for route_id, row in registry.items()
            if _pings_one_turn(row.cmd_template, row.model or "")
        }
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

    def _prepare(self, route_id):
        """`(prepared, reason)` for a due route's ping, asked by
        `take_warm_lease` before it takes any lease: the same `prepare_launch`
        an adjudication takes, from the row this warmer selected its routes
        from (one snapshot), its refusal the reason the ping is skipped."""
        try:
            return prepare_launch(self.root, self.registry[route_id]), ""
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
        the working tree or git."""
        metrics = {}
        outcome, word = None, "ERROR"
        try:
            outcome = act(call_, metrics)
            word = _outcome_word(outcome)
        except BaseException:  # recorded ERROR on the dispatcher's thread
            pass
        self.finished.append((call_, outcome, metrics, word))

    def _record_finished(self):
        while self.finished:
            call_, outcome, metrics, word = self.finished.pop(0)
            _record_call(call_, outcome, metrics, word)

    def finish(self, timeout=KEEPWARM_TIMEOUT + 30):
        """At the run's end: wait out a ping in flight, then record every
        finished one through the same rule the tick applies — only over a
        clean trunk. Over a dirty one the log is not written, and the reason
        is printed and returned instead, so the exit path never commits beside
        uncommitted work."""
        if self.thread is not None:
            self.thread.join(timeout)
        if not self.finished:
            return []
        if self.dirty():
            line = "keep-warm: session log not recorded (the trunk is dirty)"
            print(line, file=sys.stderr)
            self.finished.clear()
            return [line]
        self._record_finished()
        return []


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
    registry, _errors = agent_route.load_registry(Path(root) / "docs" / "agents.toml")
    warmer = KeepWarmer(root, cfg, registry)
    atexit.register(warmer.finish)  # a ping in flight is recorded at the run's end
    return warmer


def route_env(row):
    """A registry row's declared environment merged over the ambient one, or
    None to inherit it exactly — the loop's own launch rule.

    Implements: SR-227, LLR-305
    """
    pairs = agent_route.parse_env(getattr(row, "env", "") or "")
    return {**os.environ, **pairs} if pairs else None
