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


def _collected_smoke_count():
    """The true count of tests the `-m smoke` commit bar collects, measured by an
    INDEPENDENT collect-only run — deterministic and invocation-independent (it
    does not depend on how the outer suite was invoked). `--co` collects but runs
    nothing, so this cannot recurse into itself."""
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "--co", "-q", "-m", "smoke"],
        cwd=str(ROOT),
        capture_output=True,
        encoding="utf-8",
    )
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
