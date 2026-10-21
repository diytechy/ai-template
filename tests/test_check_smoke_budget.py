"""The smoke tier's budget step (scripts/check_smoke_budget.py), in process.

The step runs the declared smoke tier once and reports two readings against
two declared limits in docs/stack.ini [smoke-budget]: the tier's own CPU
seconds against `cpu-seconds`, and its wall time against `wall-seconds`. It
also validates `max-tests`, so one broken key refuses every caller alike.

In enforce mode, the run menu's audit, it also counts the tier against
`max-tests` after the reading stops, through the one counting function the
membership ratchet in tests/test_smoke_budget.py uses.

Every case here drives `main(argv)` with four stand-ins, so nothing joins a
real job and no real suite runs: a tier (`run_tier` replaced by a recorder, or
`smoke_argv` by an interpreter command that exits N), a meter (`select_meter`
replaced by a fixed reading), a counter (`count_smoke_tier` replaced by a
fixed count), and the limits (a temporary stack.ini). The real meters are read
in tests/test_smoke_budget_meter.py, a slow module, because the Windows meter
joins its process to a job for good.
"""

import configparser
import functools
import os
import shlex
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest
from conftest import ROOT, load_script

SCRIPT = ROOT / "scripts" / "check_smoke_budget.py"

LIMITS = {"cpu-seconds": "900", "wall-seconds": "600", "max-tests": "3000"}


def _load_step():
    """A fresh instance of the step, so one case's stand-ins never reach
    another's."""
    return load_script(SCRIPT.stem, SCRIPT.parent)


class FakeMeter:
    """A meter whose reading is fixed, or whose start or stop fails."""

    name = "fake-meter"

    def __init__(self, reading=1.0, start_error=None, stop_error=None, events=None):
        self.reading = reading
        self.start_error = start_error
        self.stop_error = stop_error
        self.started = False
        self.events = events if events is not None else []

    def start(self):
        if self.start_error is not None:
            raise self.start_error
        self.started = True
        self.events.append("meter start")

    def stop(self):
        self.events.append("meter stop")
        if self.stop_error is not None:
            raise self.stop_error
        return self.reading


class FakeCounter:
    """A smoke-tier counter whose count is fixed, or that fails with the
    step's own CountFailed and `error` as its cause."""

    def __init__(self, count=10, error=None, events=None):
        self.count = count
        self.error = error
        self.calls = 0
        self.events = events if events is not None else []
        self.step = None

    def __call__(self):
        self.calls += 1
        self.events.append("count")
        if self.error is not None:
            raise self.step.CountFailed(self.error)
        return self.count


def _write_limits(path, values=LIMITS, section=True):
    lines = ["[smoke-budget]"] if section else ["[other]"]
    lines += ["{} = {}".format(key, value) for key, value in values.items()]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _stand_in(
    monkeypatch,
    tmp_path,
    code=0,
    meter=None,
    values=LIMITS,
    sleep=0.0,
    platform=None,
    counter=None,
):
    """The step with a recorded tier, a stood-in counter, a stood-in meter (or
    its real meter choice for `platform`) and a temporary stack.ini; returns
    the module and the tier's recorded calls."""
    step = _load_step()
    real_select = step.select_meter
    ini = tmp_path / "stack.ini"
    _write_limits(ini, values)
    monkeypatch.setattr(step, "STACK_INI", ini)
    counter = counter if counter is not None else FakeCounter()
    counter.step = step
    monkeypatch.setattr(step, "count_smoke_tier", counter)
    calls = []
    events = meter.events if meter is not None else []

    def run_tier(cmd, env):
        calls.append((cmd, env))
        events.append("tier")
        if sleep:
            time.sleep(sleep)
        return code

    monkeypatch.setattr(step, "run_tier", run_tier)
    if platform is not None:
        monkeypatch.setattr(
            step, "select_meter", functools.partial(real_select, platform)
        )
        return step, calls
    chosen = meter if meter is not None else FakeMeter()
    monkeypatch.setattr(step, "select_meter", lambda: chosen)
    return step, calls


@pytest.mark.parametrize("mode", ["warn", "enforce"])
def test_within_both_limits_exits_zero_in_both_modes(
    monkeypatch, tmp_path, capsys, mode
):
    step, calls = _stand_in(monkeypatch, tmp_path)
    assert step.main(["--mode", mode]) == 0
    out, err = capsys.readouterr()
    assert "-> within" in out
    assert "WARN" not in out and "FAIL" not in err
    assert len(calls) == 1


def _over(key):
    """A meter and limits that put one reading over its key's limit."""
    if key == "cpu-seconds":
        return {"meter": FakeMeter(reading=1000.0)}
    return {"values": dict(LIMITS, **{"wall-seconds": "0.001"}), "sleep": 0.05}


@pytest.mark.parametrize("key", ["cpu-seconds", "wall-seconds"])
def test_over_a_limit_fails_enforce_naming_it(monkeypatch, tmp_path, capsys, key):
    step, _ = _stand_in(monkeypatch, tmp_path, **_over(key))
    assert step.main(["--mode", "enforce"]) == 1
    out, err = capsys.readouterr()
    assert "-> OVER" in out
    fail = [line for line in err.splitlines() if line.startswith("FAIL (enforce):")]
    assert len(fail) == 1 and key in fail[0], err


@pytest.mark.parametrize("key", ["cpu-seconds", "wall-seconds"])
def test_over_a_limit_warns_and_passes_in_warn_mode(monkeypatch, tmp_path, capsys, key):
    step, _ = _stand_in(monkeypatch, tmp_path, **_over(key))
    assert step.main(["--mode", "warn"]) == 0
    out, err = capsys.readouterr()
    assert "-> OVER" in out
    warn = [line for line in out.splitlines() if line.startswith("WARN:")]
    assert len(warn) == 1 and key in warn[0], out
    assert "FAIL" not in err


@pytest.mark.parametrize("mode", ["warn", "enforce"])
def test_a_red_tier_exits_with_its_own_code_and_the_verdict_line(
    monkeypatch, tmp_path, capsys, mode
):
    # The real tier runner, over an interpreter command that exits 3.
    step = _load_step()
    ini = tmp_path / "stack.ini"
    _write_limits(ini)
    monkeypatch.setattr(step, "STACK_INI", ini)
    tier = [sys.executable, "-c", "import sys; sys.exit(3)"]
    monkeypatch.setattr(step, "smoke_argv", lambda cp: tier)
    monkeypatch.setattr(step, "select_meter", lambda: FakeMeter())
    monkeypatch.setattr(step, "count_smoke_tier", FakeCounter())
    assert step.main(["--mode", mode]) == 3
    out, err = capsys.readouterr()
    assert "smoke budget: CPU 1.0 s" in out
    assert "note: smoke tier exited 3" in err


def test_a_red_tier_with_a_failed_reading_names_both(monkeypatch, tmp_path, capsys):
    meter = FakeMeter(stop_error=OSError("the query failed"))
    step, _ = _stand_in(monkeypatch, tmp_path, code=3, meter=meter)
    assert step.main(["--mode", "enforce"]) == 3
    out, err = capsys.readouterr()
    assert "CPU reading FAILED (the query failed)" in out
    assert "note: smoke tier exited 3" in err


@pytest.mark.parametrize("mode", ["warn", "enforce"])
def test_a_green_tier_with_a_failed_reading_exits_two(
    monkeypatch, tmp_path, capsys, mode
):
    meter = FakeMeter(stop_error=OSError("the query failed"))
    step, _ = _stand_in(monkeypatch, tmp_path, meter=meter)
    assert step.main(["--mode", mode]) == 2
    out, _ = capsys.readouterr()
    assert "CPU reading FAILED (the query failed)" in out


_BROKEN = [
    pytest.param(key, value, mode, id="{}-{}-{}".format(key, label, mode))
    for key in LIMITS
    for label, value in [
        ("absent", None),
        ("blank", ""),
        ("text", "abc"),
        ("zero", "0"),
        ("negative", "-5"),
    ]
    for mode in ("warn", "enforce")
]


@pytest.mark.parametrize("key, value, mode", _BROKEN)
def test_a_broken_key_refuses_before_the_tier_starts(
    monkeypatch, tmp_path, capsys, key, value, mode
):
    values = dict(LIMITS)
    if value is None:
        del values[key]
    else:
        values[key] = value
    meter = FakeMeter()
    step, calls = _stand_in(monkeypatch, tmp_path, meter=meter, values=values)
    assert step.main(["--mode", mode]) == 2
    _, err = capsys.readouterr()
    assert "stack.ini" in err and key in err, err
    assert calls == [] and not meter.started


@pytest.mark.parametrize("mode", ["warn", "enforce"])
@pytest.mark.parametrize("broken", ["section", "file"])
def test_an_absent_section_or_file_refuses_before_the_tier_starts(
    monkeypatch, tmp_path, capsys, broken, mode
):
    step, calls = _stand_in(monkeypatch, tmp_path)
    if broken == "section":
        _write_limits(step.STACK_INI, section=False)
    else:
        step.STACK_INI.unlink()
    assert step.main(["--mode", mode]) == 2
    _, err = capsys.readouterr()
    assert "stack.ini" in err, err
    if broken == "section":
        assert "[smoke-budget]" in err, err
    assert calls == []


def test_a_platform_without_resource_refuses_before_the_tier_starts(
    monkeypatch, tmp_path, capsys
):
    step, calls = _stand_in(monkeypatch, tmp_path, platform="plan9")
    monkeypatch.setitem(sys.modules, "resource", None)
    assert step.main(["--mode", "warn"]) == 2
    _, err = capsys.readouterr()
    assert "plan9" in err, err
    assert calls == []


def test_a_job_that_cannot_be_made_refuses_before_the_tier_starts(
    monkeypatch, tmp_path, capsys
):
    from kitlib import winjob

    def refuse():
        raise OSError("no job for this process")

    monkeypatch.setattr(winjob, "create_joined_job", refuse)
    step, calls = _stand_in(monkeypatch, tmp_path, platform="win32")
    assert step.main(["--mode", "enforce"]) == 2
    _, err = capsys.readouterr()
    assert "no job for this process" in err, err
    assert calls == []


def test_the_verdict_line_names_cpu_wall_meter_and_cpu_count(
    monkeypatch, tmp_path, capsys
):
    step, _ = _stand_in(monkeypatch, tmp_path, meter=FakeMeter(reading=12.3))
    assert step.main(["--mode", "warn"]) == 0
    out, _ = capsys.readouterr()
    verdict = [line for line in out.splitlines() if line.startswith("smoke budget:")]
    assert len(verdict) == 1, out
    line = verdict[0]
    assert "CPU 12.3 s vs 900 s cpu-seconds" in line
    assert "vs 600 s wall-seconds" in line
    assert "meter fake-meter" in line
    assert "{} logical CPUs".format(os.cpu_count()) in line


def test_elapsed_is_refused_as_an_unknown_argument(capsys):
    step = _load_step()
    with pytest.raises(SystemExit) as exc:
        step.main(["--elapsed", "5"])
    assert exc.value.code == 2
    _, err = capsys.readouterr()
    assert "unrecognized arguments: --elapsed" in err


def test_the_tier_runs_under_the_private_cap_job(monkeypatch, tmp_path):
    step, calls = _stand_in(monkeypatch, tmp_path)
    assert step.main(["--mode", "warn"]) == 0
    assert len(calls) == 1
    _, env = calls[0]
    assert env["PYTEST_CPU_CAP_JOB"] == "private"


# --- The audit's count: the tier's test count against max-tests, enforce only.


@pytest.mark.parametrize("count, code", [(3000, 0), (3001, 1)])
def test_a_count_at_max_tests_passes_and_one_past_fails(
    monkeypatch, tmp_path, capsys, count, code
):
    # LIMITS declares max-tests = 3000; the ceiling is inclusive.
    step, _ = _stand_in(monkeypatch, tmp_path, counter=FakeCounter(count))
    assert step.main(["--mode", "enforce"]) == code
    out, err = capsys.readouterr()
    verdict = "within" if code == 0 else "OVER"
    assert (
        "smoke tier count: {} tests vs 3000 max-tests -> {}".format(count, verdict)
        in out
    ), out
    fail = [line for line in err.splitlines() if line.startswith("FAIL (enforce):")]
    if code == 0:
        assert fail == [], err
    else:
        assert len(fail) == 1 and "max-tests" in fail[0], err


@pytest.mark.parametrize(
    "cause",
    [
        "the collect-only run exited 1",
        "the collect-only run collected no node id",
    ],
)
def test_a_failed_or_empty_count_exits_two(monkeypatch, tmp_path, capsys, cause):
    step, _ = _stand_in(monkeypatch, tmp_path, counter=FakeCounter(error=cause))
    assert step.main(["--mode", "enforce"]) == 2
    out, _ = capsys.readouterr()
    assert "smoke tier count FAILED ({})".format(cause) in out, out


def test_a_red_tier_over_max_tests_keeps_its_code_and_names_the_count(
    monkeypatch, tmp_path, capsys
):
    step, _ = _stand_in(monkeypatch, tmp_path, code=3, counter=FakeCounter(3001))
    assert step.main(["--mode", "enforce"]) == 3
    out, err = capsys.readouterr()
    assert "smoke tier count: 3001 tests vs 3000 max-tests -> OVER" in out, out
    fail = [line for line in err.splitlines() if line.startswith("FAIL (enforce):")]
    assert len(fail) == 1 and "max-tests" in fail[0], err
    assert "note: smoke tier exited 3" in err


def test_warn_mode_never_starts_the_counter(monkeypatch, tmp_path, capsys):
    counter = FakeCounter(5000)
    step, _ = _stand_in(monkeypatch, tmp_path, counter=counter)
    assert step.main(["--mode", "warn"]) == 0
    out, _ = capsys.readouterr()
    assert counter.calls == 0
    assert "smoke tier count" not in out


def test_the_count_runs_after_the_reading_stops(monkeypatch, tmp_path):
    events = []
    meter = FakeMeter(events=events)
    counter = FakeCounter(events=events)
    step, _ = _stand_in(monkeypatch, tmp_path, meter=meter, counter=counter)
    assert step.main(["--mode", "enforce"]) == 0
    assert events == ["meter start", "tier", "meter stop", "count"]


@pytest.mark.parametrize(
    "returncode, stdout, expected",
    [
        (0, "tests/test_a.py::test_one\ntests/test_a.py::test_two\n\n2 tests\n", 2),
        (1, "tests/test_a.py::test_one\nERROR collecting\n", None),
        (0, "\nno tests collected\n", None),
    ],
    ids=["two-ids", "nonzero", "no-ids"],
)
def test_the_count_reads_node_ids_from_a_collect_only_run(returncode, stdout, expected):
    step = _load_step()
    seen = []

    def run(cmd, **kwargs):
        seen.append((cmd, kwargs))
        return SimpleNamespace(returncode=returncode, stdout=stdout, stderr="")

    if expected is None:
        with pytest.raises(step.CountFailed):
            step.count_smoke_tier(run=run)
    else:
        assert step.count_smoke_tier(run=run) == expected
    cmd, kwargs = seen[0]
    assert cmd == [sys.executable, "-X", "utf8", "-m", "pytest", "--co", "-q"] + [
        "-m",
        "smoke",
    ]
    assert kwargs["cwd"] == str(ROOT)


def test_a_failed_count_carries_the_tail_of_the_collect_runs_output():
    # A tier module that fails to import is reported by the collect-only run
    # on its own output; the failed count must carry that text, not only the
    # exit code, and its tail, not a whole collection log.
    step = _load_step()
    head = "".join("tests/test_a.py::test_{}\n".format(n) for n in range(200))
    stderr = "ERROR collecting tests/test_b.py\nImportError: no module named 'gone'\n"

    def run(cmd, **kwargs):
        return SimpleNamespace(returncode=2, stdout=head, stderr=stderr)

    with pytest.raises(step.CountFailed) as caught:
        step.count_smoke_tier(run=run)
    message = str(caught.value)
    assert "exited 2" in message
    assert "ImportError: no module named 'gone'" in message
    assert "tests/test_a.py::test_0\n" not in message


def test_the_ratchet_and_the_step_count_through_one_function():
    import test_smoke_budget as ratchet

    assert Path(ratchet.STEP.__file__).resolve() == SCRIPT.resolve()
    assert ratchet.smoke_count is ratchet.STEP.count_smoke_tier
    assert not hasattr(ratchet, "_collected_smoke_count")
    assert not hasattr(ratchet, "_run_pytest_collect")


def _stack_ini():
    """The real docs/stack.ini, parsed as the run menu reads it."""
    cp = configparser.ConfigParser(interpolation=None)
    cp.read(ROOT / "docs" / "stack.ini", encoding="utf-8-sig")
    return cp


def _audit_argv():
    """The [run] audit action's step, read from the real docs/stack.ini."""
    return [step.strip() for step in _stack_ini()["run"]["audit"].split("&&")]


def test_the_audit_runs_the_step_in_enforce_mode():
    assert _audit_argv() == ["python scripts/check_smoke_budget.py --mode enforce"]


@pytest.mark.parametrize("key", ["cpu-seconds", "wall-seconds", "max-tests"])
def test_the_audit_fails_over_each_limit_naming_its_key(
    monkeypatch, tmp_path, capsys, key
):
    (step_line,) = _audit_argv()
    argv = shlex.split(step_line)
    assert argv[:2] == ["python", "scripts/check_smoke_budget.py"]
    over = {"counter": FakeCounter(3001)} if key == "max-tests" else _over(key)
    step, _ = _stand_in(monkeypatch, tmp_path, **over)
    assert step.main(argv[2:]) == 1
    _, err = capsys.readouterr()
    fail = [line for line in err.splitlines() if line.startswith("FAIL (enforce):")]
    assert len(fail) == 1 and key in fail[0], err


# --- The bars: no bar fails on the tier's seconds, and a red tier fails each.

BARS = ["commit", "review"]


def _bar_budget_argv(bar):
    """The budget step's arguments in one bar's command, read from the real
    docs/stack.ini. The commit bar is [run] smoke; the review bar runs the run
    menu's smoke action, so it resolves to the same line."""
    cp = _stack_ini()
    if bar == "review":
        assert cp["bars"]["review"].strip() == (
            "python project-trajectory/scripts/run_menu.py smoke"
        )
    steps = [step.strip() for step in cp["run"]["smoke"].split("&&")]
    (budget,) = [step for step in steps if "scripts/check_smoke_budget.py" in step]
    argv = shlex.split(budget)
    assert argv[:2] == ["python", "scripts/check_smoke_budget.py"]
    return argv[2:]


@pytest.mark.parametrize("bar", BARS)
def test_neither_bar_fails_on_seconds(monkeypatch, tmp_path, capsys, bar):
    argv = _bar_budget_argv(bar)
    step, calls = _stand_in(
        monkeypatch,
        tmp_path,
        meter=FakeMeter(reading=1000.0),
        values=dict(LIMITS, **{"wall-seconds": "0.001"}),
        sleep=0.05,
    )
    assert step.main(argv) == 0
    out, err = capsys.readouterr()
    warn = [line for line in out.splitlines() if line.startswith("WARN:")]
    assert len(warn) == 2, out
    assert "cpu-seconds" in warn[0] and "wall-seconds" in warn[1], out
    assert "FAIL" not in err, err
    assert len(calls) == 1


@pytest.mark.parametrize("bar", BARS)
def test_a_red_tier_still_fails_each_bar(monkeypatch, tmp_path, capsys, bar):
    argv = _bar_budget_argv(bar)
    step, _ = _stand_in(monkeypatch, tmp_path, code=3)
    assert step.main(argv) == 3
    _, err = capsys.readouterr()
    assert "note: smoke tier exited 3" in err, err


def _ci_budget_runs():
    """The `run:` lines that call the budget step in the CI workflow's
    smoke-budget job, found by text: the job's block runs from its key to the
    next two-space-indented key."""
    path = ROOT / ".github" / "workflows" / "test.yml"
    lines = path.read_text(encoding="utf-8").splitlines()
    runs = []
    for line in lines[lines.index("  smoke-budget:") + 1 :]:
        stripped = line.strip()
        if line[:3] != "   " and stripped and not stripped.startswith("#"):
            break
        if stripped.startswith("run:") and "check_smoke_budget.py" in stripped:
            runs.append(stripped[len("run:") :].strip())
    return runs


def _caller_commands(caller):
    if caller == "step:smoke":
        return [_stack_ini()["step:smoke"]["command"].strip()]
    return _ci_budget_runs()


@pytest.mark.parametrize("caller", ["step:smoke", "ci-smoke-budget-job"])
def test_every_other_caller_runs_warn_mode(caller):
    commands = _caller_commands(caller)
    assert commands, caller
    for command in commands:
        assert "scripts/check_smoke_budget.py --mode warn" in command, command
        assert "--mode enforce" not in command, command
