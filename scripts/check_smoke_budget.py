#!/usr/bin/env python3
"""The smoke tier's budget step: run the tier once, meter its own CPU seconds.

The per-commit smoke tier (docs/stack.ini [tiers] smoke) answers "is it
basically alive?", not "re-run most of the full suite". This step runs it once
and reports two readings against two limits declared in docs/stack.ini
[smoke-budget]:

  * `cpu-seconds`, the budget: the CPU seconds the tier's own processes used,
    user plus system, its xdist workers and their children included. Other
    load on the box moves it far less than it moves wall time, which is why
    it is the budget: two concurrent tier runs beside it raised it about 26%
    while nearly doubling its wall time, and that loaded rise is what the
    stamped value's 25% margin over the highest loaded reading was sized
    against (docs/stack.ini [smoke-budget] holds the readings).
  * `wall-seconds`, a looser cap on the tier's wall time, so a tier that
    sleeps or hangs for minutes is still caught.

It also validates `max-tests`, the tier's membership ceiling, in both modes,
so one broken key refuses every caller alike. A missing or broken key exits
2, naming the file and the key, before any tier runs; there is no default.

THE METERS. On Windows the step creates an unnamed job and joins it before
the spawn (kitlib.winjob), so every tier process is born in the job; the
reading is the job's user plus kernel time after the tier exits, minus the
same sum just before the spawn. Exited processes, orphans and nested jobs
count. Anywhere `resource` imports, the reading is the change in
`getrusage(RUSAGE_CHILDREN)` across the run, with nothing else started
meanwhile. That counts only descendants their parents waited for: a process
orphaned before it ends is outside the reading, a stated under-count. Any
other platform, or a job that cannot be made or joined, exits 2. There is no
wall-only verdict.

NO OUTSIDE PROCESS ADDS CPU. The tier runs with PYTEST_CPU_CAP_JOB=private,
so the root conftest caps it in an unnamed job, at the same rate and
priority, instead of the shared named one. Another process cannot open an
unnamed job by name and join it, so it cannot burn inside the step's job.

THE COUNT. In enforce mode, the run menu's audit (docs/stack.ini [run] audit),
the step also counts the tier against `max-tests` once the reading has
stopped, so the count is outside it: the test node ids a collect-only
`-m smoke` run from the repository root collects. tests/test_smoke_budget.py's
membership ratchet counts through the same function. A collect-only run that
exits nonzero, or that yields no node id, is a failed count, never a pass.
Warn mode does not count: the bars judge membership through the ratchet,
which runs inside the tier.

THE MODES AND THE EXITS. `--mode warn` (the default) prints a WARN line for a
limit over and exits 0; `--mode enforce` exits 1 for it, a count over
`max-tests` included. In both modes a red tier exits with its own code, the
verdict line still printed, and a green tier whose reading (or, in enforce
mode, whose count) failed exits 2. Callers test only for nonzero; the lines
name the cause.

THE CALLERS. Every bar runs warn mode, so no bar fails on the tier's seconds:
docs/stack.ini [run] smoke (the commit bar, which [bars] review runs through
the run menu), the [step:smoke] harness step, and the CI workflow's
smoke-budget job. Only the run menu's audit, [run] audit, runs enforce mode,
by hand and at phase close; a breach there is filed as a re-tier row.

Usage:
  python scripts/check_smoke_budget.py [--mode warn|enforce]

Stdlib-only, cross-platform (a meta-repo dev/CI tool, like scripts/dev-setup).
"""

import argparse
import importlib
import math
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "project-trajectory/scripts"))
from kitlib import config as _kitconfig  # noqa: E402

STACK_INI = ROOT / _kitconfig.STACK_INI
SECTION = "smoke-budget"
# How many of a failed collect-only run's last output lines a failed count
# carries: enough for a collection error's traceback end, not the whole log.
COUNT_TAIL_LINES = 20


class Refusal(Exception):
    """A missing or broken declared value or meter: exit 2, no tier run."""


class CountFailed(Exception):
    """The tier's collect-only count exited nonzero or found no node id."""


class Limits(NamedTuple):
    cpu_seconds: float
    wall_seconds: float
    max_tests: int


class Reading(NamedTuple):
    """One tier run: its CPU seconds (None when the meter failed), the
    failure's cause, its wall seconds and its exit code."""

    cpu: object
    failure: object
    wall: float
    code: int


class Count(NamedTuple):
    """The tier's test count (None when the count failed) and the failure's
    cause."""

    tests: object
    failure: object


_KEYS = (("cpu-seconds", float), ("wall-seconds", float), ("max-tests", int))


def _profile():
    # The parse is kitlib.config.read_stack_ini's, the one check.py reads
    # through. An absent profile reads None, and an unreadable or malformed
    # one raises: the budget has no default to fall back to.
    return _kitconfig.read_stack_ini(STACK_INI)


def _where():
    try:
        return STACK_INI.relative_to(ROOT).as_posix()
    except ValueError:
        return str(STACK_INI)


def _positive(section, key, kind):
    raw = section.get(key)
    if raw is None:
        raise Refusal("{} [{}] has no {} key".format(_where(), SECTION, key))
    try:
        value = kind(raw.strip())
    except ValueError:
        value = None
    if value is None or not math.isfinite(value) or value <= 0:
        raise Refusal(
            "{} [{}] {} = {!r} is not a positive number".format(
                _where(), SECTION, key, raw
            )
        )
    return value


def declared_limits(cp):
    """The three declared limits, validated: positive and finite, max-tests
    an integer. Raises Refusal naming the file and the key."""
    if cp is None:
        raise Refusal("{} is absent; [{}] cannot be read".format(_where(), SECTION))
    if not cp.has_section(SECTION):
        raise Refusal("{} has no [{}] section".format(_where(), SECTION))
    section = cp[SECTION]
    return Limits(*(_positive(section, key, kind) for key, kind in _KEYS))


def _read_limits():
    try:
        cp = _profile()
    except _kitconfig.StackIniError as exc:
        raise Refusal("{} cannot be read: {}".format(_where(), exc)) from exc
    return cp, declared_limits(cp)


class _JobMeter:
    """Windows: the CPU seconds of an unnamed job this process joins."""

    name = "windows-job"

    def start(self):
        from kitlib import winjob

        self._winjob = winjob
        self._job = winjob.create_joined_job()
        self._before = winjob.job_cpu_seconds(self._job)

    def stop(self):
        return self._winjob.job_cpu_seconds(self._job) - self._before


class _RusageMeter:
    """POSIX: the reaped children's CPU seconds, from getrusage."""

    name = "getrusage"

    def __init__(self, resource):
        self._resource = resource

    def _children(self):
        usage = self._resource.getrusage(self._resource.RUSAGE_CHILDREN)
        return usage.ru_utime + usage.ru_stime

    def start(self):
        self._before = self._children()

    def stop(self):
        return self._children() - self._before


def select_meter(platform=sys.platform):
    """The CPU meter for `platform`; a Refusal where there is none."""
    if platform == "win32":
        return _JobMeter()
    try:
        resource = importlib.import_module("resource")
    except ImportError as exc:
        raise Refusal(
            "no CPU meter on {}: no job objects and no resource module".format(platform)
        ) from exc
    return _RusageMeter(resource)


def smoke_argv(cp):
    """The declared smoke command: [product] test + the [tiers] smoke selector,
    with {py} bound to this interpreter — so this runs exactly the bar sessions
    run (`python -m pytest -q -n auto -m smoke`), read from the single source."""
    test = cp.get("product", "test", fallback="{py} -m pytest -q -n auto")
    tier = cp.get("tiers", "smoke", fallback="-m smoke")
    argv = shlex.split(test) + shlex.split(tier)
    return [sys.executable if tok == "{py}" else tok for tok in argv]


def tier_env():
    """The tier's environment: this one, with the root conftest's cap in a
    private job that no other process can join by name."""
    return dict(os.environ, PYTEST_CPU_CAP_JOB="private")


def run_tier(cmd, env):
    """Run the tier once and return its exit code."""
    return subprocess.run(cmd, cwd=str(ROOT), env=env).returncode


def measure(cmd, meter):
    """Run the tier once under the meter. A meter that cannot start is a
    Refusal, raised before the spawn; one that cannot stop is a failed
    reading, recorded, not raised."""
    print("running: " + " ".join(shlex.quote(c) for c in cmd), flush=True)
    env = tier_env()
    try:
        meter.start()
    except OSError as exc:
        raise Refusal("the CPU meter could not start: {}".format(exc)) from exc
    start = time.perf_counter()
    code = run_tier(cmd, env)
    wall = time.perf_counter() - start
    try:
        return Reading(meter.stop(), None, wall, code)
    except OSError as exc:
        return Reading(None, str(exc), wall, code)


def _run_pytest_collect(cwd, *extra_args, run=subprocess.run):
    """A `python -m pytest --co -q` collect-only run against `cwd`, with the
    child interpreter forced into UTF-8 mode (`-X utf8`).

    Without that flag, a pipe-connected child's stdout/stderr default to the
    AMBIENT locale encoding — cp1252 on a stock Windows box — not UTF-8.
    Collection can print non-ASCII (conftest's own missing-POSIX-shell banner
    uses an en dash) before a single test runs, so the child would emit a
    cp1252 byte this call's `encoding="utf-8"` decode cannot read. That decode
    error kills the pipe's READER THREAD — the exception is raised inside the
    thread, not here, so it never surfaces as a catchable error — and leaves
    the crashed stream (`proc.stdout` or `.stderr`) `None`; a caller that
    assumes a string then dies on `AttributeError` for reasons that have
    nothing to do with the tests themselves. `-X utf8` makes the child's own
    text streams UTF-8 by construction, so whatever it prints always matches
    this decode."""
    return run(
        [sys.executable, "-X", "utf8", "-m", "pytest", "--co", "-q", *extra_args],
        cwd=str(cwd),
        capture_output=True,
        encoding="utf-8",
    )


def count_smoke_tier(run=subprocess.run):
    """The smoke tier's test count: the node ids (one `::` line each under
    `-q --co`) a collect-only `-m smoke` run from the repository root
    collects. Deterministic and independent of how any outer run was invoked.
    Raises CountFailed on a nonzero exit, a run that cannot start, or no id.
    A nonzero exit's message ends with the last lines of the run's output,
    where a module that failed to import names its error."""
    try:
        proc = _run_pytest_collect(ROOT, "-m", "smoke", run=run)
    except OSError as exc:
        raise CountFailed("the collect-only run could not start: {}".format(exc))
    if proc.returncode != 0:
        output = (proc.stdout or "") + (proc.stderr or "")
        tail = "\n".join(output.splitlines()[-COUNT_TAIL_LINES:])
        raise CountFailed(
            "the collect-only run exited {}; its output ended:\n{}".format(
                proc.returncode, tail
            )
        )
    count = sum(1 for line in (proc.stdout or "").splitlines() if "::" in line)
    if count == 0:
        raise CountFailed("the collect-only run collected no node id")
    return count


def take_count(mode):
    """The audit's count, in enforce mode only; None in warn mode, which
    never starts the counter."""
    if mode != "enforce":
        return None
    try:
        return Count(count_smoke_tier(), None)
    except CountFailed as exc:
        return Count(None, str(exc))


def _annotate(level, message):
    """A GitHub Actions annotation when running in CI; harmless plain text else."""
    if os.environ.get("GITHUB_ACTIONS"):
        print("::{}::{}".format(level, message))


def _overs(reading, limits, count=None):
    """(key, message) for each limit the reading, or the count, is over."""
    overs = []
    if reading.cpu is not None and reading.cpu > limits.cpu_seconds:
        overs.append(("cpu-seconds", "CPU", reading.cpu, limits.cpu_seconds))
    if reading.wall > limits.wall_seconds:
        overs.append(("wall-seconds", "wall", reading.wall, limits.wall_seconds))
    messages = [
        (
            key,
            "smoke tier {} {:.1f} s is over {} = {:g} ({} [{}]). Re-tier a heavy "
            "module into conftest.SLOW_MODULES, or re-stamp the value with the "
            "reason in the log.".format(what, value, key, limit, _where(), SECTION),
        )
        for key, what, value, limit in overs
    ]
    if count is not None and (count.tests or 0) > limits.max_tests:
        messages.append(
            (
                "max-tests",
                "smoke tier count {} tests is over max-tests = {} ({} [{}]). "
                "Re-tier a heavy module into conftest.SLOW_MODULES, or "
                "re-stamp the value with the reason in the log.".format(
                    count.tests, limits.max_tests, _where(), SECTION
                ),
            )
        )
    return messages


def _count_line(count, limits):
    if count.tests is None:
        return "smoke tier count FAILED ({}); max-tests {}".format(
            count.failure, limits.max_tests
        )
    return "smoke tier count: {} tests vs {} max-tests -> {}".format(
        count.tests,
        limits.max_tests,
        "OVER" if count.tests > limits.max_tests else "within",
    )


def _verdict_line(reading, limits, meter, overs):
    if reading.cpu is None:
        cpu = "CPU reading FAILED ({})".format(reading.failure)
    else:
        cpu = "CPU {:.1f} s vs {:g} s cpu-seconds".format(
            reading.cpu, limits.cpu_seconds
        )
    return "smoke budget: {}; wall {:.1f} s vs {:g} s wall-seconds; meter {}; {} logical CPUs -> {}".format(
        cpu,
        reading.wall,
        limits.wall_seconds,
        meter.name,
        os.cpu_count(),
        "OVER" if any(key != "max-tests" for key, _ in overs) else "within",
    )


def report(reading, limits, meter, mode, count=None):
    """Print the verdict (and, in enforce mode, the count) and return the exit
    code, in precedence order: a red tier's own code, then 2 for a failed
    reading or count, then 1 for an enforced limit over, else 0."""
    overs = _overs(reading, limits, count)
    print(_verdict_line(reading, limits, meter, overs), flush=True)
    if count is not None:
        print(_count_line(count, limits), flush=True)
    for _, message in overs:
        if mode == "enforce":
            _annotate("error", message)
            print("FAIL (enforce): " + message, file=sys.stderr)
        else:
            _annotate("warning", message)
            print("WARN: " + message)
    if reading.code != 0:
        print(
            "note: smoke tier exited {} (test failures are not a budget "
            "breach; fix them separately)".format(reading.code),
            file=sys.stderr,
        )
        return reading.code
    if reading.cpu is None or (count is not None and count.tests is None):
        return 2
    return 1 if overs and mode == "enforce" else 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Run the smoke tier once; judge its CPU seconds and wall time."
    )
    ap.add_argument(
        "--mode",
        choices=("warn", "enforce"),
        default="warn",
        help="warn (default): report a limit over; enforce (the audit): also "
        "count the tier against max-tests, and exit 1 on any limit over.",
    )
    args = ap.parse_args(argv)
    try:
        cp, limits = _read_limits()
        meter = select_meter()
        reading = measure(smoke_argv(cp), meter)
    except Refusal as exc:
        print("smoke budget: REFUSED: {}".format(exc), file=sys.stderr)
        return 2
    return report(reading, limits, meter, args.mode, take_count(args.mode))


if __name__ == "__main__":
    sys.exit(main())
