"""WI-921: every built-in check step is classified for the commit floor.

A step registered in `check.py` that no commit runs is a gap nothing reports:
WI-913's `plan-gate` and WI-841's `done-when-blessed` were each registered and
never selected by the shipped hook, so the hold each promised never held a
commit. This census closes that class. Every name `check.steps()` returns (the
built-in set, pinned inside `BUILTIN_STEP_NAMES` by tests/test_stack_profile.py)
is exactly one of:

  * in the hook's batched floor (its one `--run-steps` line);
  * run by the hook by name (`--run-step`: `format`);
  * listed below as not run at commit, with a one-line reason citing where the
    kit states it, or, where no text states it, the reason read from the step.

A new step in none of them, a name in two, or a listed name that is not a step
fails here, in the smoke tier, at the commit that registered it. In process:
the hook is read as text and `steps()` is called, nothing is spawned.
"""

from conftest import KIT, hook_check_lines, load_script

HOOK = KIT / "hooks" / "pre-commit"

# The hook header's rule, cited below as GATE-SCOPED: "the full gate bar
# (placeholder rejection, schema checks, tests, coverage) is gate-scoped and
# lives in check.py / CI ... they would block legitimate early-stage commits".
# The FLOOR RULE is the one the hook states at `trajectory-map`: a check joins
# the floor when regenerating is one stdlib command and it is vacuous for a
# non-adopter; "checks needing the product toolchain or gate context (tests,
# perf, flows) stay in check.py / CI".
NOT_AT_COMMIT = {
    "tests+coverage": "runs the product's test suite under coverage: the "
    "toolchain and gate context the floor rule keeps in check.py / CI "
    "(hook header: tests and coverage are gate-scoped).",
    "traceability": "trace.py --strict's orphan check is a gate criterion that "
    "must never block an early commit (the hook's registry-integrity entry); "
    "ruling 6 (docs/plans/2026-10-11-review-churn/README.md) runs it after each "
    "build, never in the commit hook.",
    "privacy": "the tracked-tree sweep for what slipped in before the gate was "
    "enabled or past --no-verify (its step comment); the hook scans the staged "
    "content itself, in its step 3.",
    "perf-budgets": "compares the metrics the product's harness measured: perf "
    "is named by the floor rule as staying in check.py / CI.",
    "design-flows": "the runtime-flow diagrams, required from the DevStg-Tests "
    "rung: flows are named by the floor rule as staying in check.py / CI.",
    "assumption-evidence": "the release-rung check, listed after the harness whose "
    "results it reads (its step comment): gate context, under the floor rule.",
    "lint": "the product linter from the declared toolchain: a product-toolchain "
    "check, gate-scoped (hook header) and kept in check.py / CI by the floor rule.",
    "vocabulary": "a whole-tree retired-vocabulary scan whose severity rises with "
    "the rung (its step comment): gate-scoped (hook header).",
    "need-form": "a form heuristic over the approved need prose, warn-first always "
    "(its step comment): gate-scoped (hook header).",
    "doc-navigability": "a whole-tree link and orphan check with a git-history "
    "staleness heuristic (its step comment): gate-scoped (hook header).",
    "backlink-coverage": "the share of LLR rows named by an Implements: line in "
    "source, from the Impl rung, report-only as shipped (its step comment): "
    "gate-scoped (hook header).",
    "test-first": "reads approval and Implements: order from history, warn-only "
    "always (its step comment): gate-scoped (hook header).",
    "assumption-gate": "the assumption gate's requirement question from the "
    "Boundary rung, advisory unless [checks] assumption_gate is set (its step "
    "comment): gate-scoped (hook header).",
    "crossing-allocation": "the assumption gate's crossing allocation from the "
    "Boundary rung, advisory unless [checks] assumption_gate is set (its step "
    "comment): gate-scoped (hook header).",
    "interface-allocation": "the assumption gate's interface allocation from the "
    "Arch rung, advisory unless [checks] assumption_gate is set (its step "
    "comment): gate-scoped (hook header).",
}


def census(names, floor, by_name, listed):
    """The census's findings, one line each, [] when every step is classified
    exactly once: a step in no class, a name in two (or twice in one), and a
    listed name that is not a step."""
    steps = set(names)
    classes = {}
    for label, members in (
        ("the batched floor", floor),
        ("run by name", by_name),
        ("not run at commit", listed),
    ):
        for name in members:
            classes.setdefault(name, []).append(label)
    findings = [
        "{}: a built-in step in no class (floor, by name, or not at commit)".format(n)
        for n in sorted(steps - classes.keys())
    ]
    for name, where in sorted(classes.items()):
        if len(where) > 1:
            findings.append("{}: classified more than once: {}".format(name, where))
        if name not in steps:
            findings.append("{}: classified, but not a built-in step".format(name))
    return findings


def _live():
    check = load_script("check")
    names = [s[0] for s in check.steps(80, "full", "all")]
    floor, by_name = hook_check_lines(HOOK)
    return names, floor, by_name


def test_every_built_in_step_is_classified_exactly_once():
    names, floor, by_name = _live()
    assert census(names, floor, by_name, NOT_AT_COMMIT) == []
    assert by_name == ["format"]
    assert all(len(r.splitlines()) == 1 and r.strip() for r in NOT_AT_COMMIT.values())


# The three faults, each over a small census of its own: they test the census
# function, so they pass whatever the live hook says.
_NAMES = ["fresh-a", "fresh-b", "format", "heavy"]
_FLOOR = ["fresh-a", "fresh-b"]
_LISTED = {"heavy": "gate-scoped"}


def test_an_unclassified_step_fails_the_census():
    assert census(_NAMES, _FLOOR, ["format"], _LISTED) == []
    findings = census(_NAMES + ["new-step"], _FLOOR, ["format"], _LISTED)
    assert findings == [
        "new-step: a built-in step in no class (floor, by name, or not at commit)"
    ]


def test_a_name_in_two_classes_fails_the_census():
    listed = dict(_LISTED, format="also listed")
    findings = census(_NAMES, _FLOOR, ["format"], listed)
    assert findings == [
        "format: classified more than once: ['run by name', 'not run at commit']"
    ]


def test_a_listed_name_that_is_not_a_step_fails_the_census():
    listed = dict(_LISTED, retired="no such step")
    assert census(_NAMES, _FLOOR, ["format"], listed) == [
        "retired: classified, but not a built-in step"
    ]
