"""WI-427 — SN-010's universal, enforced: every DECLARED generated artifact has a
freshness enforcer, and each newly wired one can actually go RED.

SN-010 says *every* generated artifact carries a `--check` freshness contract.
That is a universal, so it is false at one counterexample — and it had two.
`project-trajectory/prompts/CATALOG.md` and `project-trajectory/skills/INDEX.csv`
are both declared generated in `docs/stack.ini`'s `[generated]` section, both
had a working `--check`, and neither `--check` was named by `check.py`, the
pre-commit hook, `ci/check.yml` or any workflow. A declared contract nothing
enforces is worse than an undeclared one: a reader concludes the artifact is
gated when it is not.

Two rules live here, and the second is the one that matters most:

  * **the census** — every `[generated]` row's kind resolves to a named
    enforcer. This is the durable guard: it catches the THIRD unwired artifact
    the day it is declared, which is how these two were found by hand.
  * **non-vacuity** — each newly wired step is driven RED against a planted
    defect. Wiring a check that cannot fail converts a visible gap into an
    invisible one, which is exactly the "green hides a skipped check" failure
    SN-008 forbids. The defect is planted in a COPY of the harness under
    `tmp_path`; the live tree is never corrupted.

The census is in test_generated_freshness_census.py, in the per-commit smoke
tier; this module keeps the tables it reads and the non-vacuity half, which
runs `check.py` as a subprocess and is registered in `tests/conftest.py`'s
`SLOW_MODULES`.
"""

import configparser
import shutil

from conftest import KIT, ROOT, SCRIPTS, load_script, run_py

STACK_INI = ROOT / "docs" / "stack.ini"
HOOK = KIT / "hooks" / "pre-commit"

# Each `[generated]` kind -> the check.py step name that holds it fresh.
WIRED = {
    "trajectory": "trajectory-map",
    "okf": "okf",
    "status": "status-map",
    # WI-498 slice 5 retired the `gate` kind (docs/gate and its three-value BAR)
    # along with its `derived-gate` enforcer; `stage` is the surviving axis.
    "stage": "derived-stage",
    "openitems": "open-items",
    "approve": "approval-fresh",
    "skillsindex": "skills-index",
    "promptcatalog": "prompt-catalog",
    "components": "component-view",
    # OI-61 ruled (a)'s second step: the argparse-derived CLI reference, which
    # is what the registry's thinned CLI `contract` cells now point at instead
    # of paraphrasing the flags by hand.
    "cli": "cli-reference",
    # OI-66 ruled (a): the module-declared interface reference, which is what a
    # thinned `contract` cell points at instead of restating what the providing
    # module already says.
    "interface-reference": "interface-reference",
    # OI-76: the hand-authored per-WI rollup died as a gate INPUT and was reborn
    # generated. The gate never reads it; a human does, which is precisely why
    # it is freshness-gated.
    "verdictrollup": "verdict-rollup",
}

# The kinds whose enforcer is NOT a check.py step, each named with its reason.
# A row lands here only when the artifact genuinely has no mechanical
# regenerator to `--check` against — never because wiring one was inconvenient.
OTHERWISE_ENFORCED = {
    # A hand-stamped, measured-and-classified BASELINE (docs/stack.ini §5.3):
    # there is no command that regenerates it, because re-deriving it would
    # blindly approve whatever the tree currently measures — which is the ratchet
    # inverted. Its enforcer is that it IS a test: tests/test_module_size_ratchet
    # re-measures every kit module against the baseline on every run.
    "linecounts": "tests/test_module_size_ratchet.py",
}

# Steps in WIRED that deliberately do NOT run in the pre-commit floor. Empty
# today, and a new entry owes the hook's own stated rule as its reason: a
# freshness check joins the floor when regenerating is one stdlib command and
# the step is vacuous for a non-adopter; one needing the product toolchain or
# gate context (tests, perf, flows) stays in check.py / CI.
HOOK_EXEMPT = frozenset()


def _generated_kinds():
    """The `[generated]` rows as {path: kind} — the §5.2 declaration itself,
    read the way check.py/integrate.py read it (interpolation off, BOM-tolerant)."""
    cp = configparser.ConfigParser(interpolation=None)
    cp.read(STACK_INI, encoding="utf-8-sig")
    rows = {}
    for path in cp.options("generated"):
        # `<kind> [| <BEGIN> | <END>]` — the marker pair is not part of the kind.
        rows[path] = cp.get("generated", path).split("|")[0].strip()
    return rows


def _plan_names(gate="all"):
    check = load_script("check")
    return {s[0] for s in check.steps(80, "full", gate)}


def _step(name, gate="all"):
    check = load_script("check")
    for step in check.steps(80, "full", gate):
        if step[0] == name:
            return step
    raise AssertionError("no step named {!r} in the built-in plan".format(name))


# --- the census: no declared generated artifact is left unenforced -----------
# The census reads only the declarations and check.py's plan, so it lives in
# test_generated_freshness_census.py, in the per-commit smoke tier.


# --- non-vacuity: each new step driven RED on a planted defect ---------------


def _kit_copy(tmp_path, *, prompts=False, skills=False):
    """A minimal COPY of the kit harness under tmp_path, so a defect can be
    planted without ever corrupting the live tree.

    Both generators resolve their artifact from their OWN location (never the
    CWD), which is what makes an isolated copy a faithful stand-in: the copied
    check.py builds its step commands from the copied scripts dir, so the whole
    step runs against the copy. `docs/` exists because check.py refuses to run
    anywhere but a repo root (WI-100).

    `kitlib/` COMES ALONG UNCONDITIONALLY (WI-448). It is the shipped
    shared-helper package `check.py` imports for the best-effort-off-git
    pattern, so a copy without it ImportErrors before the planted defect can be
    reached — the same dependency-manifest truth bootstrap's MAPPING states for
    a real scaffold, asserted here for the one fixture that assembles a partial
    scripts dir by hand rather than by bootstrapping."""
    dest = tmp_path / "project-trajectory"
    (dest / "scripts").mkdir(parents=True)
    names = ["check.py"]
    if prompts:
        names += ["gen_prompt_catalog.py", "prompts.py"]
    if skills:
        names += ["gen_skills_index.py"]
    for name in names:
        shutil.copy2(SCRIPTS / name, dest / "scripts" / name)
    shutil.copytree(SCRIPTS / "kitlib", dest / "scripts" / "kitlib")
    if prompts:
        shutil.copytree(KIT / "prompts", dest / "prompts")
    if skills:
        shutil.copytree(KIT / "skills", dest / "skills")
    (tmp_path / "docs").mkdir()
    return dest


def _run_step(kit, name, cwd):
    return run_py([kit / "scripts" / "check.py", "--run-steps", name], cwd=cwd)


def test_prompt_catalog_step_reds_when_a_template_changes(tmp_path):
    # The real failure mode: someone edits a shipped prompt template and does not
    # regenerate the catalogue, so every later `prompt-sha` lookup resolves to a
    # template that no longer exists. Green first (the copy is faithful), then
    # red on the defect, then green again once regenerated — so the step is shown
    # to track the artifact, not merely to have an opinion.
    kit = _kit_copy(tmp_path, prompts=True)
    before = _run_step(kit, "prompt-catalog", tmp_path)
    assert before.returncode == 0, before.stdout + before.stderr

    template = kit / "prompts" / "worker.template.md"
    template.write_text(
        template.read_text(encoding="utf-8") + "\nan edit that moves the digest\n",
        encoding="utf-8",
    )
    red = _run_step(kit, "prompt-catalog", tmp_path)
    assert red.returncode != 0, "a template edit must stale the catalogue"
    assert "STALE" in (red.stdout + red.stderr)

    fix = run_py([kit / "scripts" / "gen_prompt_catalog.py"], cwd=tmp_path)
    assert fix.returncode == 0, fix.stdout + fix.stderr
    after = _run_step(kit, "prompt-catalog", tmp_path)
    assert after.returncode == 0, after.stdout + after.stderr


def test_skills_index_step_reds_when_a_skill_is_added(tmp_path):
    # Same shape for the index: a SKILL.md lands and INDEX.csv is not
    # regenerated, so the applicability index an agent reads omits a skill that
    # exists.
    kit = _kit_copy(tmp_path, skills=True)
    before = _run_step(kit, "skills-index", tmp_path)
    assert before.returncode == 0, before.stdout + before.stderr

    planted = kit / "skills" / "planted-skill"
    planted.mkdir()
    (planted / "SKILL.md").write_text(
        "---\nname: planted-skill\ndescription: a skill the index never heard of\n"
        "scope: kit\n---\nbody\n",
        encoding="utf-8",
    )
    red = _run_step(kit, "skills-index", tmp_path)
    assert red.returncode != 0, "a new SKILL.md must stale INDEX.csv"
    assert "STALE" in (red.stdout + red.stderr)

    fix = run_py(
        [kit / "scripts" / "gen_skills_index.py", "--skills", kit / "skills"],
        cwd=tmp_path,
    )
    assert fix.returncode == 0, fix.stdout + fix.stderr
    after = _run_step(kit, "skills-index", tmp_path)
    assert after.returncode == 0, after.stdout + after.stderr


def test_skills_index_step_never_falls_back_to_the_cwd_default(tmp_path):
    # THE VACUOUS-PASS TRAP, pinned. `gen_skills_index.py --check` defaults
    # `--skills` to a CWD-relative `skills`, and in this kit the source lives at
    # project-trajectory/skills — so the default resolves to nothing and the
    # generator exits 0 with "no skills dir". Wiring the step that way would have
    # produced a permanently green check of nothing. The step therefore passes an
    # explicit path derived from the script's own location.
    check = load_script("check")
    cmd = _step("skills-index")[2]
    assert "--skills" in cmd, "the step must not rely on the CWD-relative default"
    assert cmd[cmd.index("--skills") + 1] == str(check._SCRIPTS.parent / "skills")
    # End-to-end, from a CWD with no `skills/` of its own: a real answer, never
    # the no-skills-dir shrug.
    kit = _kit_copy(tmp_path, skills=True)
    proc = _run_step(kit, "skills-index", tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout + proc.stderr
    assert "no skills dir" not in out, "the step read nothing and passed: " + out
    assert "index fresh" in out


def test_skills_sync_cannot_see_index_staleness(tmp_path):
    # WHY THESE ARE TWO STEPS AND NOT ONE. The wired `skills-sync` step runs
    # --check-agents, which compares hand-authored per-agent COPIES to the
    # hand-authored SOURCE and never reads INDEX.csv at all. Plant the exact
    # defect the new step catches and --check-agents stays green — different
    # inputs, different fix (gen_skills_index.py vs bootstrap.py --sync), so
    # folding them into one step would report one failure for two properties.
    kit = _kit_copy(tmp_path, skills=True)
    planted = kit / "skills" / "planted-skill"
    planted.mkdir()
    (planted / "SKILL.md").write_text(
        "---\nname: planted-skill\ndescription: x\nscope: kit\n---\nbody\n",
        encoding="utf-8",
    )
    blind = run_py(
        [
            kit / "scripts" / "gen_skills_index.py",
            "--check-agents",
            "--source",
            kit / "skills",
            "--root",
            tmp_path,
        ],
        cwd=tmp_path,
    )
    assert blind.returncode == 0, "--check-agents is not an index-freshness check"
    stale = _run_step(kit, "skills-index", tmp_path)
    assert stale.returncode != 0, "…which is exactly why skills-index is its own step"


# --- OI-31's divergence detector: where its tests live ------------------------
# The `staged-divergence` step reads THIS section's `[generated]` census (see
# check.py `_generated_census`) and asks what these freshness gates cannot — is
# the artifact on disk the one about to be committed? Its four cases live in
# tests/test_check_harness.py, with check.py's other step tests: they build real
# git repos, and this module is in the SMOKE tier, whose membership budget
# (docs/stack.ini [smoke-budget]) is a shared dial this lane did not own.
