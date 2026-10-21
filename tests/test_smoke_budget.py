"""WI-281 — the smoke commit bar stays a smoke test (its membership ratchet).

The per-commit bar runs `-m smoke`; WI-122 keeps that tier OPT-OUT (a new test
is in the bar by default). WI-281 gave the tier a BUDGET — the bar must answer
"is it basically alive?" — and split the budget item in two, because a timing
assert is machine-/core-count-dependent and flaky:

  * this DETERMINISTIC ratchet budgets what does not vary by machine — smoke-tier
    MEMBERSHIP (the collected-count) — and BITES when the tier grows back toward
    the full suite (the regression this exists to catch);
  * the tier's CPU seconds and wall time are metered by
    scripts/check_smoke_budget.py, which every bar and CI run in warn mode
    (reported, never failed on) and the run menu's audit runs in enforce mode.
    They are not a hard assert here.

This is a growth SENSOR with headroom (the test_dashboard_size_budget idiom), not
an exact freeze: new in-process unit tests SHOULD accrue into the bar (that is
the WI-122 opt-out intent) and are cheap. It fails only if the smoke tier
balloons past the generous ceiling declared in docs/stack.ini [smoke-budget] —
the signature of a heavy subprocess/scaffold module un-slowed
(conftest.SLOW_MODULES) or the bar accreting back toward 79% of the suite. When
it fails: re-tier the offending module to slow, OR — if the growth is legitimate
in-process units — re-stamp max-tests in docs/stack.ini with the reason in the
WI/session log, never silently.
"""

import configparser

from conftest import ROOT, load_script

STACK_INI = ROOT / "docs" / "stack.ini"

# The tier's count has one home, the budget step's, so this ratchet and the
# run menu's audit cannot count differently: the test node ids an independent
# collect-only `-m smoke` run from the repository root collects. `--co`
# collects but runs nothing, so the ratchet cannot recurse into itself.
STEP = load_script("check_smoke_budget", ROOT / "scripts")
smoke_count = STEP.count_smoke_tier


def _budget(option):
    """A declared [smoke-budget] value from docs/stack.ini (the single source of
    truth shared with scripts/check_smoke_budget.py). Mirrors check.py's parser:
    interpolation=None so a `%` needs no escaping, utf-8-sig for a Notepad BOM."""
    cp = configparser.ConfigParser(interpolation=None)
    cp.read(STACK_INI, encoding="utf-8-sig")
    return int(cp["smoke-budget"][option])


def _within_budget(count, ceiling):
    """The ceiling is INCLUSIVE: at the line is fine, one past it bites."""
    return count <= ceiling


def test_smoke_tier_stays_within_its_membership_budget():
    ceiling = _budget("max-tests")
    count = smoke_count()
    assert _within_budget(count, ceiling), (
        "smoke tier collects {} tests, over its {}-test membership budget "
        "(docs/stack.ini [smoke-budget] max-tests). The per-commit bar must stay "
        "a smoke test. If a heavy subprocess/scaffold module "
        "slipped back into the bar, re-tier it into conftest.SLOW_MODULES; if "
        "this is legitimate in-process growth, re-stamp max-tests with the reason "
        "in the WI/session log."
    ).format(count, ceiling)


def test_membership_ratchet_bites_past_the_ceiling():
    # Bite-proof: the sensor FAILS the moment the tier exceeds its ceiling — the
    # regression it exists to catch (a heavy subprocess/scaffold module un-slowed
    # back into the bar, e.g. re-adding test_agent_loop's ~113 tests or
    # test_gen_trajectory's ~98). Proves the guard's teeth without a real (and
    # self-defeating) re-tier, via the same comparison the live assertion applies.
    ceiling = _budget("max-tests")
    assert _within_budget(ceiling, ceiling)  # exactly at the line: ok
    assert _within_budget(ceiling - 1, ceiling)
    assert not _within_budget(ceiling + 1, ceiling)  # one past the line: bites


def test_the_declared_commit_bar_runs_the_strict_lints_before_its_budget():
    # This repo's one declared commit-bar command, docs/stack.ini [run] smoke,
    # runs both strict lints, the docs staleness check and the RESYNC entry
    # check first, then the budget check in warn mode, whose own metered run is
    # the bar's only smoke-tier run: a red tier fails the bar, and its seconds
    # are reported, never failed on. A lint red stops the bar before the tier
    # runs. A chain that dropped a step, moved the budget check ahead of the
    # lints, or ran the tier a second time would let a build round's bar skip a
    # check or pay for the tier twice.
    cp = configparser.ConfigParser(interpolation=None)
    cp.read(STACK_INI, encoding="utf-8-sig")
    steps = [step.strip() for step in cp["run"]["smoke"].split("&&")]
    assert steps == [
        "python project-trajectory/scripts/trace.py --strict",
        "python project-trajectory/scripts/check_trajectory.py --strict",
        "python project-trajectory/scripts/check_docs.py --root . --stale",
        "python scripts/check_resync.py",
        "python scripts/check_smoke_budget.py --mode warn",
    ]
    tier_steps = [
        step
        for step in steps
        if "pytest" in step or step.startswith("python scripts/check_smoke_budget.py")
    ]
    assert tier_steps == [steps[-1]]


def test_nested_collection_survives_a_non_utf8_console_byte(tmp_path):
    # M-01 regression (repo review 2026-08-19): a collected module that prints
    # a character during collection — exactly what conftest's own
    # missing-POSIX-shell banner does with an en dash — must not crash the
    # collect-only run the step's `count_smoke_tier` depends on. No explicit
    # encoding is forced here: on a stock Windows box a pipe-connected child's
    # default IS cp1252, which is the real trigger this test measures against;
    # `STEP._run_pytest_collect`'s `-X utf8` is what keeps the child's own default
    # UTF-8 regardless. Before that flag existed, this reproduced the exact
    # defect on a real Windows checkout: the reader thread died decoding byte
    # 0x96, and `proc.stdout` came back `None`.
    (tmp_path / "conftest.py").write_text(
        "def pytest_sessionstart(session):\n"
        '    print("missing-shell banner \\u2013 stub")\n',
        encoding="utf-8",
    )
    (tmp_path / "test_x.py").write_text(
        "def test_x():\n    assert True\n", encoding="utf-8"
    )
    proc = STEP._run_pytest_collect(tmp_path)
    assert proc.stdout is not None and proc.stderr is not None, (
        "a decode failure killed a reader thread — proc.stdout={!r} "
        "proc.stderr={!r}".format(proc.stdout, proc.stderr)
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "test_x.py::test_x" in proc.stdout
