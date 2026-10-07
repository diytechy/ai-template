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
    `AdjudicationRequest` carries `root`, the brief class `brief`, `family`,
    `route_id`, the work item `wi`, the route's command `template` and launch
    `env`, `role` (default ADJUDICATE), the operator's `prompt_templates`
    overrides (None: the shipped templates), and the call's wall `deadline`
    in seconds (None: 7200). `adjudication_keep(request)` returns the Keep the
    adjudication launches under, or None where the `[adjudicator]` dial does
    not cover it; its lease is the deadline plus 300 s, and its governing
    template identity covers the templates of every class the dial retains,
    so switching between retained classes does not drain the session. `signin_status(root,
    family, run=None)` returns `signed-in`, `missing` or `unknown` for the
    family's dedicated CLI home, resolved without being created, with no
    model call: an absent home is missing; otherwise the family's status
    command (`claude auth status`, `codex login status`) runs under it, and
    only its documented answers read signed-in or missing: any other answer,
    a failure or a timeout is unknown. A covered call whose
    family has a dedicated home and does not read `signed-in` raises
    `SigninRefused`, naming dev-setup, before any lease is taken or home
    created; nothing signs in and nothing falls back to a fresh session.
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
from dataclasses import dataclass, field
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


def _launch(call, argv, stdin_input, env):
    """Run the prepared argv through the call's launch."""
    if call.attached:
        runner = call.runner or run_attached
        return runner(argv, call.root, call.timeout, stdin_input=stdin_input)
    runner = call.runner or run_session
    return runner(
        argv,
        call.root,
        call.timeout,
        env=env,
        on_line=call.on_line,
        stdin_input=stdin_input,
        idle_timeout=call.idle_timeout,
    )


def _launch_env(call):
    """The environment the call launches under: the call's own, or None to
    inherit the ambient one exactly; a retained call adds its dedicated CLI
    home over whichever it is."""
    home = call.keep.home_env if call.keep is not None else {}
    if not home:
        return call.env
    return {**(os.environ if call.env is None else call.env), **home}


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
    argv, stdin_input = agent_session.build_argv(call.template, call.model, call.prompt)
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
    metrics.update(_identity(call))
    started = time.monotonic()
    try:
        code, stream, timed_out = _launch(call, argv, stdin_input, env)
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
    text = adapter.final_text(stream, scratch, code)
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


def cli_version(template, env=None):
    """The runner's `--version` line for a route's command template, or ""
    when it cannot be read. Read once per retained launch (never at the off
    dial), so a runner upgraded under a retained session drains it.

    Implements: SR-227, LLR-270
    """
    try:
        exe = agent_session.split_cmd(template)[0]
    except (ValueError, IndexError):
        return ""
    resolved = shutil.which(exe) or exe
    try:
        proc = subprocess.run(
            [resolved, "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
            env=env,
            stdin=subprocess.DEVNULL,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    lines = [ln.strip() for ln in (proc.stdout or "").splitlines() if ln.strip()]
    return lines[0] if proc.returncode == 0 and lines else ""


def plan_keep(root, cfg, *, template, env=None, role, brief, route_id, family, **kw):
    """The Keep an adjudication launches under, or None: `session_keep.keep_for`
    with the runner's version read first, and only when the keep operation
    covers the call, so the off dial launches nothing extra. A covered call
    whose family runs under a dedicated CLI home is refused first, before any
    lease or home exists, unless that home is signed in (`require_signin`).

    Implements: SR-227, LLR-270
    """
    if not session_keep.applies(cfg, role, brief, route_id):
        return None
    require_signin(root, family)
    return session_keep.keep_for(
        root,
        cfg,
        role=role,
        brief=brief,
        route_id=route_id,
        family=family,
        cli_version=cli_version(template, env),
        **kw,
    )


# --- the adjudication request: one composition for every route -------------------


@dataclass(frozen=True)
class AdjudicationRequest:
    """What an adjudication's keep is planned from, composed alike on the
    loop's route and the coordinator's: the brief class, the family and route,
    the work item, the operator's `prompt_templates` overrides (keyed by prompt
    key; None or empty: the shipped templates), and the call's wall `deadline`
    in seconds (None: the default session wall), which the lease outlives.
    The governing template identity is not the caller's to compose: the keep
    derives it from the dial's retained set (`adjudication_keep`).

    Implements: SR-227, LLR-305
    """

    root: object
    brief: str
    family: str
    route_id: str
    wi: str
    template: str
    env: object = None
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
        template=request.template,
        env=request.env,
        role=request.role,
        brief=request.brief,
        family=request.family,
        route_id=request.route_id,
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


def _claude_signin(code, text):
    """`claude auth status` prints one JSON object: signed in is exit 0 with
    `loggedIn` true, signed out is exit 1 with `loggedIn` false. Any other
    combination, or output that is not that object alone, is unknown.
    """
    try:
        state = json.loads(text.strip())
    except ValueError:
        return SIGNIN_UNKNOWN
    logged = state.get("loggedIn") if isinstance(state, dict) else None
    if not isinstance(logged, bool):  # 1 must not read as True
        return SIGNIN_UNKNOWN
    return _CLAUDE_READINGS.get((code, logged), SIGNIN_UNKNOWN)


# The documented (exit code, `loggedIn`) pairs; every other pair is unknown.
_CLAUDE_READINGS = {(0, True): SIGNED_IN, (1, False): SIGNIN_MISSING}


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
# its reader. A family with a dedicated home and no row here probes unknown.
# Implements: SR-227, LLR-305
SIGNIN_PROBES = {
    "ANTHROPIC": (("claude", "auth", "status"), _claude_signin),
    "OPENAI": (("codex", "login", "status"), _codex_signin),
}


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
    `missing` or `unknown`. The home is resolved without being created; an
    absent home is missing without running anything; otherwise the family's
    status command runs under it (`run(argv, env)`, default a bounded
    subprocess); only its documented exit-and-output pairs read signed-in or
    missing, and any other answer, failure or timeout is unknown.

    Implements: SR-227, LLR-305
    """
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
    home has nothing to sign in to.

    Implements: SR-227, LLR-305
    """
    family = (family or "").upper()
    if family not in session_keep.HOME_VARIABLES:
        return
    status = signin_status(root, family)
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
        self.routes = set()
        for route_id, row in registry.items():
            try:
                argv, _ = agent_session.build_argv(
                    row.cmd_template, row.model or "", KEEPWARM_PROMPT
                )
            except ValueError:
                continue  # A route that cannot launch cannot be pinged.
            if session_adapters.adapter_for(argv).bounds_one_turn():
                self.routes.add(route_id)
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

    def _start(self, keep):
        row = self.registry[keep.route_id]
        call_ = Call(
            root=self.root,
            role="KEEP-WARM",
            template=row.cmd_template,
            model=row.model or "",
            prompt=KEEPWARM_PROMPT,
            provider=row.family,
            tier=row.tier,
            route_id=row.id,
            source_event="keep-warm",
            env=route_env(row),
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
