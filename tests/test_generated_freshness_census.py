"""The census half of WI-427: every declared generated artifact has a
freshness enforcer, and every wired enforcer is a real step in the commit floor.

Split out of `test_generated_freshness_wiring.py`, verbatim. That module keeps
the declaration tables this census reads and the non-vacuity half, which copies
the harness under `tmp_path` and runs `check.py` as a subprocess per case, so it
is registered in `tests/conftest.py`'s `SLOW_MODULES`. Every case here reads the
declarations and `check.py`'s step plan in-process, so the census, the durable
guard that catches the next unwired artifact the day it is declared, stays in
the per-commit smoke tier.
"""

from conftest import KIT, load_script
from test_generated_freshness_wiring import (
    HOOK,
    HOOK_EXEMPT,
    OTHERWISE_ENFORCED,
    WIRED,
    _generated_kinds,
    _plan_names,
    _step,
)


def test_every_declared_generated_artifact_has_an_enforcer():
    # The rule SN-010 states, mechanized. A new `[generated]` row must gain an
    # enforcer in the same breath: either a check.py step (add it to WIRED) or,
    # for an artifact with no mechanical regenerator, a named non-step enforcer
    # (add it to OTHERWISE_ENFORCED with its reason). Failing here is not a
    # request to edit this table — it is the finding.
    kinds = _generated_kinds()
    assert kinds, "docs/stack.ini [generated] parsed empty — the census read broke"
    unenforced = {
        path: kind
        for path, kind in kinds.items()
        if kind not in WIRED and kind not in OTHERWISE_ENFORCED
    }
    assert not unenforced, (
        "declared generated with NO freshness enforcer (SN-010 is a universal, "
        "so one of these makes it false): " + str(unenforced)
    )
    # And the reverse, so this table cannot rot into a claim about rows that no
    # longer exist (the way a stale allowlist outlives its subject).
    declared = set(kinds.values())
    stale = (set(WIRED) | set(OTHERWISE_ENFORCED)) - declared
    assert not stale, (
        "this table names kinds docs/stack.ini no longer declares: "
        + str(sorted(stale))
    )


def test_the_cli_reference_path_has_one_spelling_in_three_places():
    # THREE readers name this one file — the `[generated]` declaration (what the
    # trunk owns), `check.py`'s freshness step (what gates it) and
    # `trunk_step.py`'s regen row (what fixes it) — and they cannot import one
    # another: `check.py` and `trunk_step.py` are standalone-copied scripts. So
    # the constant is duplicated by design and pinned here instead, which is the
    # duplicated-policy rule applied to a path. Drift would not be silent (the
    # step would red while the regen wrote elsewhere), but it would be
    # baffling, and this says so in one line.
    check = load_script("check")
    trunk = load_script("trunk_step")
    assert check.CLI_REFERENCE_DOC == trunk.CLI_REFERENCE_REL
    assert check.CLI_REFERENCE_DOC in _generated_kinds()


def test_every_wired_enforcer_is_a_real_step_and_runs_in_the_commit_floor():
    # Naming a step is not wiring it: the name must resolve in check.py's
    # built-in plan (a typo would otherwise "enforce" nothing), and — unless
    # explicitly exempted — must be in the hook's batched --run-steps line, so a
    # stale artifact blocks at the commit that staled it rather than in CI.
    plan = _plan_names()
    check = load_script("check")
    hook_text = HOOK.read_text(encoding="utf-8")
    run_steps_line = [
        ln
        for ln in hook_text.splitlines()
        if "--run-steps" in ln and "check.py" in ln and not ln.lstrip().startswith("#")
    ]
    assert len(run_steps_line) == 1, "expected exactly one batched --run-steps call"
    floor = set(run_steps_line[0].split("--run-steps")[1].strip().split(","))
    for kind, step in sorted(WIRED.items()):
        assert step in plan, "{}: no step named {!r} in the plan".format(kind, step)
        assert step in check.BUILTIN_STEP_NAMES, (
            "{}: {!r} is not shadow-guarded".format(kind, step)
        )
        if step not in HOOK_EXEMPT:
            assert step in floor, "{}: {!r} is absent from the hook floor".format(
                kind, step
            )


def test_the_two_new_steps_gate_at_every_rung():
    # The gate-set decision, pinned. These two are NOT the {DevStg-Impl} doc-freshness
    # family: that family is DevStg-Impl-only because those views are of the project's own
    # evolving spine and churn while the plan forms. These index the APPARATUS
    # (the loop's prompt templates, the skill library) — kit source that does not
    # move as a downstream plan matures — and their consumers (session forensics,
    # an agent choosing a skill) are live from the first session. Concretely: this
    # kit's own effective stage sits low while its approval window is open,
    # so an Impl-threshold step would not run in the kit's own CI at all for the
    # window's whole duration, which is the gap re-created rather than closed.
    #   The tag was a three-bar membership set and is now the LOWEST RUNG
    # (WI-498 slice 2), which says the same thing more directly: there is no
    # rung from which these two do not apply.
    for name in ("skills-index", "prompt-catalog"):
        assert _step(name)[3] == "DevStg-Needs", name


def test_the_reference_ci_inherits_new_steps_without_editing_it():
    # ci/check.yml is a SINGLE entry point: it runs `check.py` and never restates
    # a step, so a step added to the built-in table is inherited for free. Pinned
    # rather than assumed — if CI ever grew a hand-listed step set, this row's
    # "no CI change needed" finding would silently stop being true.
    ci = (KIT / "ci" / "check.yml").read_text(encoding="utf-8")
    invocations = [ln.strip() for ln in ci.splitlines() if "check.py" in ln]
    assert invocations, "ci/check.yml no longer invokes check.py"
    assert not any("--run-step" in ln for ln in invocations), (
        "ci/check.yml now enumerates steps by name; adding a built-in step is no "
        "longer free and this WI's CI finding needs revisiting: " + str(invocations)
    )
