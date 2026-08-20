"""WI-281 — the smoke commit bar stays a smoke test (its membership ratchet).

The per-commit bar runs `-m smoke`; WI-122 keeps that tier OPT-OUT (a new test
is in the bar by default). WI-281 gave the tier a BUDGET — the bar must answer
"is it basically alive?" in <= 60 s wall — and split the budget item in two,
because a wall-clock assert is machine-/core-count-dependent and flaky:

  * this DETERMINISTIC ratchet budgets what does not vary by machine — smoke-tier
    MEMBERSHIP (the collected-count) — and BITES when the tier grows back toward
    the full suite (the regression this exists to catch);
  * the noisy wall-clock check lives in scripts/check_smoke_budget.py: its local
    default is report-only `--mode warn`, while CI deliberately invokes
    `--mode enforce` to fail a budget breach. It is not a hard assert here.

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
import subprocess
import sys

from conftest import ROOT

STACK_INI = ROOT / "docs" / "stack.ini"


def _budget(option):
    """A declared [smoke-budget] value from docs/stack.ini (the single source of
    truth shared with scripts/check_smoke_budget.py). Mirrors check.py's parser:
    interpolation=None so a `%` needs no escaping, utf-8-sig for a Notepad BOM."""
    cp = configparser.ConfigParser(interpolation=None)
    cp.read(STACK_INI, encoding="utf-8-sig")
    return int(cp["smoke-budget"][option])


def _run_pytest_collect(cwd, *extra_args):
    """A `python -m pytest --co -q` collect-only run against `cwd`, with the
    child interpreter forced into UTF-8 mode (`-X utf8`).

    M-01 (repo review 2026-08-19): without that flag, a pipe-connected child's
    stdout/stderr default to the AMBIENT locale encoding — cp1252 on a stock
    Windows box — not UTF-8. Collection can print non-ASCII (conftest's own
    missing-POSIX-shell banner uses an en dash) before a single test runs, so
    the child would emit a cp1252 byte this call's `encoding="utf-8"` decode
    cannot read. That decode error kills the pipe's READER THREAD — the
    exception is raised inside the thread, not here, so it never surfaces as a
    catchable error — and leaves the crashed stream (`proc.stdout` or
    `.stderr`) `None`; a caller that assumes a string then dies on
    `AttributeError` for reasons that have nothing to do with the tests
    themselves. `-X utf8` makes the child's own text streams UTF-8 by
    construction, so whatever it prints always matches this decode."""
    return subprocess.run(
        [sys.executable, "-X", "utf8", "-m", "pytest", "--co", "-q", *extra_args],
        cwd=str(cwd),
        capture_output=True,
        encoding="utf-8",
    )


def _collected_smoke_count():
    """The true count of tests the `-m smoke` commit bar collects, measured by an
    INDEPENDENT collect-only run — deterministic and invocation-independent (it
    does not depend on how the outer suite was invoked). `--co` collects but runs
    nothing, so this cannot recurse into itself."""
    proc = _run_pytest_collect(ROOT, "-m", "smoke")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # `-q --co` prints one node id (containing "::") per collected item.
    return sum(1 for line in proc.stdout.splitlines() if "::" in line)


def _within_budget(count, ceiling):
    """The ceiling is INCLUSIVE: at the line is fine, one past it bites."""
    return count <= ceiling


def test_smoke_tier_stays_within_its_membership_budget():
    ceiling = _budget("max-tests")
    count = _collected_smoke_count()
    assert _within_budget(count, ceiling), (
        "smoke tier collects {} tests, over its {}-test membership budget "
        "(docs/stack.ini [smoke-budget] max-tests). The per-commit bar must stay "
        "a smoke test (<= {} s wall). If a heavy subprocess/scaffold module "
        "slipped back into the bar, re-tier it into conftest.SLOW_MODULES; if "
        "this is legitimate in-process growth, re-stamp max-tests with the reason "
        "in the WI/session log."
    ).format(count, ceiling, _budget("seconds"))


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


def test_nested_collection_survives_a_non_utf8_console_byte(tmp_path):
    # M-01 regression (repo review 2026-08-19): a collected module that prints
    # a character during collection — exactly what conftest's own
    # missing-POSIX-shell banner does with an en dash — must not crash the
    # collect-only run `_collected_smoke_count` depends on. No explicit
    # encoding is forced here: on a stock Windows box a pipe-connected child's
    # default IS cp1252, which is the real trigger this test measures against;
    # `_run_pytest_collect`'s `-X utf8` is what keeps the child's own default
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
    proc = _run_pytest_collect(tmp_path)
    assert proc.stdout is not None and proc.stderr is not None, (
        "a decode failure killed a reader thread — proc.stdout={!r} "
        "proc.stderr={!r}".format(proc.stdout, proc.stderr)
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "test_x.py::test_x" in proc.stdout
