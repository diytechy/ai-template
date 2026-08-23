"""Bootstrap must produce a scaffold that is green out of the box."""

import ast
import re
import shutil
import subprocess

from conftest import (
    KIT,
    ROOT,
    SCRIPTS,
    load_script,
    pin_autocrlf,
    process_key,
    process_toml,
    run_py,
)


_ACTION_PINS = {
    "actions/checkout": "de0fac2e4500dabe0009e67214ff5f5447ce83dd",  # v6.0.2
    "actions/setup-python": "a309ff8b426b58ec0e2a45f0f869d46889d02405",  # v6.2.0
    "actions/upload-artifact": "043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",  # v7.0.1
}


def test_scaffold_contains_expected_files(scaffold):
    for rel in [
        "AGENTS.md",
        "CLAUDE.md",
        "GEMINI.md",
        ".gitignore",
        "pytest.ini",
        "docs/stack.ini",
        "docs/process.md",
        "docs/process-options.md",
        # WI-498 slice 5 deleted `docs/gate` (and gate.template) from the
        # scaffold surface; `docs/stage` is the derived state a scaffold ships.
        "docs/stage",
        # SN-028: the ~10 one-word policy files collapsed into ONE home. A
        # fresh scaffold ships only this; the legacy files are absent by
        # design (shipping both would be the mixed-config refusal on day one).
        "docs/process.toml",
        "docs/agents.toml",
        "docs/kit-profile",
        "docs/status.md",
        "docs/requirements/open-items.toml",
        "docs/log.md",
        "docs/plan.md",
        # WI-455 (sitting-2 decision 8): the authored Runtime flows live in
        # their own scaffolded doc; docs/architecture.md is RETIRED from the
        # scaffold surface (the structural architecture derives live).
        "docs/runtime-flows.md",
        "docs/requirements/system-requirements.toml",
        "docs/requirements/performance-budgets.csv",
        "docs/requirements/procurement.csv",
        "docs/requirements/assets.csv",
        # The last two registries onto the TOML carrier (WI-443 / OI-14 part B).
        "docs/requirements/components.toml",
        "docs/requirements/interfaces.toml",
        # WI-442: the depth-0 frame — the tier system requirements form around.
        # Scaffolded unconditionally beside interfaces.toml, and inert until its
        # `-000` rows are replaced.
        "docs/requirements/external.toml",
        # SN-036 / OI-19: the hats roster ships with CONTENT (thirteen starting
        # perspectives since WI-453), so a fresh scaffold's planner brief
        # carries questions on day one rather than a blank form.
        "docs/requirements/hats.toml",
        # docs/requirements/work-items.csv left this list at the Phase 2c flip:
        # the WI registry scaffolds as docs/work/ below (the CSV template ships
        # unscaffolded, as the legacy-format reference wi_convert migrates).
        "docs/work/queued/WI-000-example.md",
        # ...and the folder's own contract: the location->status table plus the
        # rule that keeps getting re-derived wrongly — a terminal row STAYS in
        # the registry, so docs/work/archive/ must never materialize.
        "docs/work/README.md",
        "docs/orphans-allow",
        # The six-state vocabulary (WI-384): every state that is not `queued`
        # (which the WI-000 exemplar already tracks) gets an empty directory, so
        # the states are visible in a listing — including BOTH terminals, which
        # is what removed the `disposition` attribute that told them apart.
        "docs/work/draft/.gitkeep",
        "docs/work/active/.gitkeep",
        "docs/work/deferred/.gitkeep",
        # The three terminal states live under the archive, not the active
        # workspace (WI-504, OI-55 ruled (a)): docs/work/ holds only rows still
        # in flight. `docs/archive/work/cancelled` beside `.../complete` is
        # what removed the `disposition` attribute that told the two apart;
        # SR-144's third terminal, `.../partial`, is pinned here so the
        # shipped folder set cannot quietly lose it again.
        "docs/archive/work/cancelled/.gitkeep",
        "docs/archive/work/partial/.gitkeep",
        "docs/archive/work/complete/.gitkeep",
        # The log's fragment drop-box (concurrency-restructure.md §5.1): empty,
        # marker-only — an exemplar here would be compiled into docs/log.md by
        # the first trunk step.
        "docs/log.d/.gitkeep",
        "docs/specs/README.md",
        "docs/specs/WI-000.md",
        "docs/knowledge/README.md",
        "docs/rubrics/README.md",
        "docs/rubrics/rubric-000.md",
        "docs/test/test-cases.toml",
        # The shared helper package (WI-448) — every module, because a
        # PARTIAL copy is the failure mode: the scripts import
        # `kitlib.config` / `kitlib.evidence` / `kitlib.git` / `kitlib.ladder` /
        # `kitlib.registry` / `kitlib.spine` / `kitlib.stage` / `kitlib.station`
        # by name, so a missing module ImportErrors on the scaffold's first
        # check rather than degrading. `test_the_common_package_ships_complete`
        # asserts the set EXACTLY against the kit; these nine rows are the
        # spot-check that keeps the expectation readable beside the other
        # scripts.
        "scripts/kitlib/__init__.py",
        "scripts/kitlib/config.py",
        "scripts/kitlib/evidence.py",
        "scripts/kitlib/git.py",
        "scripts/kitlib/ladder.py",
        "scripts/kitlib/registry.py",
        "scripts/kitlib/spine.py",
        "scripts/kitlib/stage.py",
        "scripts/kitlib/station.py",
        "scripts/check.py",
        "scripts/spine_rules.py",
        "scripts/derive_stage.py",
        "scripts/record_test_evidence.py",
        "scripts/check_doc_refs.py",
        "scripts/check_figures.py",
        "scripts/check_need_form.py",
        "scripts/check_privacy.py",
        "scripts/check_vendored.py",
        "scripts/check_trajectory.py",
        "scripts/schedule.py",
        "scripts/subagent_gate.py",
        "scripts/agent_route.py",
        "scripts/adjudicate_brief.py",
        "scripts/score_reviews.py",
        "scripts/gen_cases.py",
        "scripts/gen_trajectory.py",
        "scripts/traj_graph.py",
        "scripts/traj_parse.py",
        "scripts/traj_render.py",
        "scripts/traj_views.py",
        "scripts/traj_status.py",
        "scripts/traj_panels.py",
        "scripts/traj_context.py",
        "scripts/gen_open_items.py",
        "scripts/gen_components.py",
        "scripts/gen_okf.py",
        "scripts/plan_coverage.py",
        "scripts/plan_round.py",
        "scripts/plan_briefs.py",
        # ...and the roster reader it imports (SN-036 / OI-19).
        "scripts/hats.py",
        "scripts/plan_coverage_step.py",
        "scripts/plan_artifacts.py",
        "scripts/wi_convert.py",
        "scripts/trunk_step.py",
        "scripts/integrate.py",
        "scripts/run_menu.py",
        "scripts/dev-setup.cmd",
        ".githooks/pre-commit",
        ".githooks/commit-msg",
        ".githooks/pre-push",
        ".github/workflows/check.yml",
        "src/.gitkeep",
        "tests/.gitkeep",
        "README.md",
        "OWNER_SCRATCHPAD.md",
        "run.cmd",
        "run.sh",
        "run.command",
        "agent-resume.cmd",
        "agent-resume.sh",
        "agent-resume.command",
        "scripts/agent_loop.py",
        "scripts/dispatch.py",
        "scripts/lane.py",
        "scripts/handback.py",
        "scripts/intake.py",
        "scripts/census.py",
        "scripts/pending.py",
        "scripts/agent_session.py",
        "scripts/agent_common.py",
        "scripts/plan_runner.py",
    ]:
        assert (scaffold / rel).exists(), "missing from scaffold: " + rel


def test_scaffold_stack_ini_declares_generated_artifact_set(scaffold):
    # WI-235: the integrator's auto-resolution allowlist is scaffolded with the
    # kit defaults, so a fresh repo composes identically without forking kit code.
    ini = (scaffold / "docs" / "stack.ini").read_text(encoding="utf-8")
    assert "\n[generated]" in ini, "a fresh scaffold declares the generated set"
    for row in (
        "PROJECT_STATE.html = trajectory",
        "docs/okf/ = okf",
        "docs/status.md = status | <!-- BEGIN GENERATED STATUS --> "
        "| <!-- END GENERATED STATUS -->",
    ):
        assert row in ini, "scaffolded [generated] must carry the default: " + row


def test_scaffold_hats_roster_is_readable_by_the_scaffolded_reader(scaffold):
    """WI-446 / SN-036: the roster ships with CONTENT and its reader ships with
    it, so a FRESH scaffold's decomposition brief carries real questions.

    The standing lesson this pays: a scaffold-surface change is only verified by
    bootstrapping a scaffold. The file list above proves the two files ARRIVE;
    this proves they arrive USABLE — a roster that copied but did not parse, or
    parsed but selected nothing, would satisfy the list and ship a form with
    nothing behind it."""
    hats = load_script("hats")
    roster = hats.load(scaffold)
    assert len(roster) >= 3, "the scaffolded roster is a blank form"
    for hat in roster:
        # The anti-ceremony rule, checked on what an adopter actually receives.
        assert hat["asks"] and hat["listens_for"]
    # Every hat's condition is evaluable, and the always-on ones fire even for a
    # decomposition that declares no facts at all.
    assert hats.applicable(roster, {}), "no hat applies to a bare decomposition"
    block = hats.brief_block(hats.applicable(roster, {}))
    assert block != hats.NO_HATS and "listens for:" in block


def test_scaffold_stack_ini_seeds_the_lanes_dial(scaffold):
    # WI-381 (§A4.3, ruled): the TEMPLATE seeds lanes = 2 so a fresh scaffold
    # exercises the barrier/merge-slot/refresh machinery for real — while the
    # ABSENT-key-means-1 rule (tests/test_dispatch_admission.py) keeps every
    # existing adopter serial until they add the line themselves.
    ini = (scaffold / "docs" / "stack.ini").read_text(encoding="utf-8")
    assert "\n[agent-loop]" in ini
    assert "\nlanes = 2" in ini


def test_workflows_pin_actions_and_reduce_token_permissions(scaffold):
    """Meta CI and the downstream reference use immutable, least-privilege Actions."""
    workflows = [
        ROOT / ".github" / "workflows" / "test.yml",
        ROOT / ".github" / "workflows" / "canary.yml",
        scaffold / ".github" / "workflows" / "check.yml",
    ]
    for workflow in workflows:
        text = workflow.read_text(encoding="utf-8")
        assert "permissions:\n  contents: read" in text, workflow
        # EVERY `uses:` ref must be pinned to a full 40-hex commit SHA — a bare
        # `@vN`, `@main`, or an unknown unpinned action all fail (a deleted
        # action can no longer silently vacate its check).
        refs = re.findall(r"^\s*-?\s*uses:\s*(\S+)", text, flags=re.MULTILINE)
        assert refs, "no uses: refs found in {}".format(workflow)
        for ref in refs:
            action, sep, pin = ref.partition("@")
            assert sep and re.fullmatch(r"[0-9a-f]{40}", pin), (
                "action ref not pinned to a 40-hex SHA: {} in {}".format(ref, workflow)
            )
        for action, sha in _ACTION_PINS.items():
            if action in text:
                assert "{}@{}".format(action, sha) in text, workflow


_FORK_ONLY_PR_GUARD = (
    "if: github.event_name == 'push' || "
    "github.event.pull_request.head.repo.full_name != github.repository"
)


def test_meta_ci_runs_on_every_branch_push_exactly_once():
    """Hosted CI fires on ANY branch push, and no job runs twice (WI-278/OI-8).

    The regression this locks is the one the 2026-07-22 review found as M-7:
    `test.yml` triggered on `push: branches: [main]` + `pull_request`, so the
    development branch accumulated ~845 commits with **no hosted run at all** —
    a branch push only reached CI while somebody kept a PR open. Naming the
    current branch would re-lapse at the next one, so the trigger is `["**"]`
    and the `pull_request` event is narrowed to the case a push cannot see (a
    fork's PR) rather than dropped.
    """
    text = (ROOT / ".github" / "workflows" / "test.yml").read_text(encoding="utf-8")
    header, sep, jobs_block = text.partition("\njobs:\n")
    assert sep, "test.yml lost its jobs: block"

    assert re.search(r'^\s*branches: \["\*\*"\]$', header, flags=re.MULTILINE), (
        "test.yml's push trigger must cover every branch; a named-branch list "
        "(e.g. `branches: [main]`) leaves development branches uncovered"
    )
    assert re.search(r"^\s*pull_request:\s*$", header, flags=re.MULTILINE), (
        "the pull_request trigger must stay — it is the only CI a fork's PR gets"
    )

    jobs = re.findall(r"^  ([A-Za-z][\w-]*):$", jobs_block, flags=re.MULTILINE)
    assert len(jobs) >= 3, "expected at least test/smoke-budget/gate, got " + repr(jobs)
    assert jobs_block.count(_FORK_ONLY_PR_GUARD) == len(jobs), (
        "every job must carry the fork-only pull_request guard, or a same-repo "
        "PR double-runs the whole matrix (the two events carry different "
        "github.ref values, so the concurrency group cannot dedupe them); "
        "jobs={}".format(jobs)
    )


def test_agents_guide_is_canonical_and_stubs_point_at_it(scaffold):
    # AGENTS.md carries the full guide; CLAUDE.md/GEMINI.md are thin stubs that
    # point back at it (single source of truth — Thread 0a).
    agents = (scaffold / "AGENTS.md").read_text(encoding="utf-8")
    assert "How we work here (the process)" in agents  # a full-guide section
    assert "Working agreement" in agents
    for stub_name in ("CLAUDE.md", "GEMINI.md"):
        stub = (scaffold / stub_name).read_text(encoding="utf-8")
        assert "AGENTS.md" in stub, stub_name + " should point at AGENTS.md"
        # The stub must not duplicate the full guide.
        assert "Working agreement" not in stub, stub_name + " duplicates the guide"


def test_scaffold_knowledge_home_states_pack_contract(scaffold):
    knowledge = (scaffold / "docs" / "knowledge" / "README.md").read_text(
        encoding="utf-8"
    )
    assert "## Pack contract" in knowledge
    assert "## Pack index" in knowledge
    assert "[`example`](README.md)" in knowledge
    assert "retrieval dates" in knowledge
    assert "promote it through the change-intake flow" in knowledge
    assert "Packs are advisory context, never gates" in knowledge
    project_readme = (scaffold / "README.md").read_text(encoding="utf-8")
    assert "[docs/knowledge/](docs/knowledge/README.md)" in project_readme


def test_knowledge_library_is_opt_in_by_declared_domain(tmp_path):
    # The default/`any` scaffold carries only the index: curated packs become
    # durable project context, so they must never arrive as an implicit superset.
    plain = tmp_path / "plain"
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", plain], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert {p.name for p in (plain / "docs" / "knowledge").glob("*.md")} == {
        "README.md"
    }

    web = tmp_path / "web"
    proc = run_py(
        [SCRIPTS / "bootstrap.py", "--dest", web, "--domain", "web"],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    expected = {
        "README.md",
        "ui-design-systems.md",
        "web-rendering.md",
        "model-inference.md",
    }
    assert {p.name for p in (web / "docs" / "knowledge").glob("*.md")} == expected
    index = (web / "docs" / "knowledge" / "README.md").read_text(encoding="utf-8")
    for name in expected - {"README.md"}:
        assert "({})".format(name) in index
    assert "domains: [web]" in (
        web / "docs" / "knowledge" / "ui-design-systems.md"
    ).read_text(encoding="utf-8")


def test_knowledge_pack_materialization_is_write_once_and_forceable(tmp_path):
    dest = tmp_path / "repo"
    args = [SCRIPTS / "bootstrap.py", "--dest", dest, "--domain", "hardware"]
    first = run_py(args, cwd=tmp_path)
    assert first.returncode == 0, first.stdout + first.stderr
    pack = dest / "docs" / "knowledge" / "perception.md"
    pack.write_text("project-owned\n", encoding="utf-8")

    second = run_py(args, cwd=tmp_path)
    assert second.returncode == 0, second.stdout + second.stderr
    assert pack.read_text(encoding="utf-8") == "project-owned\n"

    forced = run_py([*args, "--force"], cwd=tmp_path)
    assert forced.returncode == 0, forced.stdout + forced.stderr
    assert "# Perception" in pack.read_text(encoding="utf-8")
    index = (dest / "docs" / "knowledge" / "README.md").read_text(encoding="utf-8")
    assert index.count("[perception](perception.md)") == 1


def test_agents_template_stays_within_size_budget():
    # Gemini's AGENTS.md support truncates near ~12k chars, and a downstream
    # project must still fill the Project section and add its own rules. The
    # shipped template therefore keeps >=2k of headroom; a kit thread that
    # grows it past this budget must pay by tightening elsewhere (the file's
    # own Customizing note states the same rule for downstream editors).
    size = len((KIT / "AGENTS.template.md").read_bytes())
    assert size <= 10_000, (
        "AGENTS.template.md is {} bytes; budget is 10,000 (>=2k headroom under "
        "the ~12k Gemini cap) — tighten another rule to pay for the growth".format(size)
    )


# The always-loaded docs, capped on the SAME mechanism as AGENTS.template.md
# above: a hard number and a test that fails past it. Caps rather than
# watch-only rows because the measured growth of a capped file and a watched one
# differ by orders of magnitude — the derivation, its window, and the earlier
# figures WITHDRAWN as unreproducible live in
# docs/knowledge/instruction-file-adherence.md; do not copy the numbers back
# here, since a second home is what let the withdrawn ones survive. Each cap is
# ~20-25% headroom
# over the file's size when the cap landed, so ordinary edits pass and a
# doubling does not; the owner may retune any of them (the skill's Budgets
# table is the readable statement of the same values).
BYTE_CAPS = {
    # Loaded into every agent session in this repo (project instructions).
    "CLAUDE.md": 8_500,
    # The guard against doc growth must not itself grow: it reached 24,336
    # bytes as a nested changelog before the history moved to docs/log.md.
    "project-trajectory/skills/byte-budget-guard/SKILL.md": 5_000,
}

# The neutral source's per-agent copies, pinned byte-identical by
# gen_skills_index.py --check-agents; a cap on the source must hold for the
# copy an agent actually loads.
_SKILL_COPIES = (".claude/skills", ".agents/skills")


def test_always_loaded_docs_stay_within_byte_caps():
    targets = dict(BYTE_CAPS)
    skill = "project-trajectory/skills/byte-budget-guard/SKILL.md"
    for agentdir in _SKILL_COPIES:
        copy = ROOT / agentdir / "byte-budget-guard" / "SKILL.md"
        if copy.exists():
            targets["{}/byte-budget-guard/SKILL.md".format(agentdir)] = BYTE_CAPS[skill]

    oversize = []
    for rel, cap in sorted(targets.items()):
        size = len((ROOT / rel).read_bytes())
        if size > cap:
            oversize.append("{} is {:,} bytes; cap is {:,}".format(rel, size, cap))
    assert not oversize, (
        "; ".join(oversize) + " — tighten the file (history belongs in "
        "docs/log.md, not in a nested parenthetical) or argue the cap up with "
        "the owner in the same commit; the byte-budget-guard skill's Budgets "
        "table states the same numbers and must be re-stamped with them"
    )


def test_capped_doc_baselines_match_the_real_sizes():
    """The skill's `Baseline` column is a MEASUREMENT, so measure it.

    2026-08-21 review, M-7: the guard's own row read 4,925 while the file was
    4,982 — already ~20 bytes wrong when the range opened, then grown 77 more
    without a re-stamp — and its printed headroom claim ("every other capped
    file holds 2–18%") was false about the very file it was printed in, which
    held 0.36%. Nothing tested a baseline cell against anything; the cap test
    above checks size <= cap and would happily watch the baseline drift. The
    failure that produces is the one the skill exists to prevent: an author
    follows the procedure, records "before = 4,925", adds 40 bytes, computes
    4,965, commits, and reds at 5,022.
    """
    table = ROOT / "project-trajectory" / "skills" / "byte-budget-guard" / "SKILL.md"
    rows = {}
    for line in table.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 5 and cells[0].startswith("`") and cells[0].endswith("`"):
            rel = cells[0].strip("`")
            digits = cells[2].replace(",", "")
            if digits.isdigit():
                rows[rel] = int(digits)
    assert set(rows) >= set(BYTE_CAPS), (
        "the Budgets table lost a capped row: {}".format(
            sorted(set(BYTE_CAPS) - set(rows))
        )
    )
    wrong = []
    for rel, declared in sorted(rows.items()):
        path = ROOT / rel
        if not path.is_file():
            wrong.append("{}: no such file".format(rel))
            continue
        real = len(path.read_bytes())
        if real != declared:
            wrong.append(
                "{}: table says {:,}, file is {:,}".format(rel, declared, real)
            )
    assert not wrong, (
        "; ".join(wrong) + " — re-stamp the byte-budget-guard Budgets table "
        "(source plus every tracked skill copy) in the SAME commit as the edit. "
        "A baseline nobody re-stamps is worse than none: the procedure tells the "
        "next author to compute their delta from it."
    )


def test_status_is_working_surface_history_lives_in_log(scaffold):
    # Thread 36: status.md holds only what must be performed next; the history
    # sections (Sittings, Audit log) live in the pointed-to docs/log.md,
    # headings preserved verbatim so downstream greps and the §5 prose survive.
    status = (scaffold / "docs" / "status.md").read_text(encoding="utf-8")
    for heading in ("## Sittings", "## Audit log", "## Decisions log"):
        assert heading not in status, "history section left in status.md: " + heading
    assert "log.md" in status, "status.md must point at the history log"
    assert "blocks:" in status, "Open-items format must seed the blocks: clause"
    log = (scaffold / "docs" / "log.md").read_text(encoding="utf-8")
    for heading in ("## Sittings", "## Audit log", "## Decisions log"):
        assert heading in log, "log.md must carry the history heading: " + heading
    # The sittings table moved intact, and each row names the RUNG RANGE it
    # certifies (OI-21 break 6) rather than being one row per boundary.
    assert "| Sitting | Rungs certified |" in log
    assert "| Acceptance | `DevStg-Release` (the owner's final read)" in log


def test_plan_build_cadence_surfaces(scaffold):
    # WI-1.29: the plan/build cadence's scaffold surfaces. docs/plan.md is the
    # sequenced block list (PLAN writes, BUILD executes); status.md points at
    # it (the lean resume surface names, never holds, the plan); the launcher
    # templates seed the strong-plans/cheap-executes model-map example.
    plan = (scaffold / "docs" / "plan.md").read_text(encoding="utf-8")
    assert "Plan/build" in plan  # names the process-options cadence section
    assert "B-1" in plan  # the example block a fresh repo replaces
    assert "Done-when" in plan  # every block states an observable done-when
    assert (
        "re-chunk" in plan
    )  # the bounce rule: exhausted/wrong -> re-chunk (strong tier)
    status = (scaffold / "docs" / "status.md").read_text(encoding="utf-8")
    assert "plan.md" in status, "status.md must point at the work plan"
    for launcher in ("agent-resume.sh", "agent-resume.cmd"):
        text = (scaffold / launcher).read_text(encoding="utf-8")
        assert "PLAN=<strong-model>,BUILD=<cheap-model>" in text, (
            launcher + " must seed the plan/build model-map example"
        )


def test_fresh_scaffold_passes_trace(scaffold):
    proc = run_py(["scripts/trace.py"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_scaffold_ships_no_declared_kernel_surface(scaffold):
    # OI-48 (d) / WI-494's fail-safe default, proven in a REAL scaffold rather
    # than a synthetic fixture: `docs/kernel-modules-allow` is a this-repo
    # declared surface (the `docs/provenance-allow`, `docs/if-tc-coverage-allow`
    # precedent), never bootstrap.py MAPPING material, so a fresh adopter
    # starts with NO declared kernel and therefore NO exemption — every
    # cross-component import stays fully policed until an adopter deliberately
    # declares one.
    assert not (scaffold / "docs" / "kernel-modules-allow").exists()
    check_trajectory = load_script("check_trajectory")
    assert check_trajectory.read_kernel_modules(scaffold) == {}
    assert check_trajectory.kernel_allow_parse_findings(scaffold) == []


def test_scaffold_ships_no_architecture_doc(scaffold):
    # WI-455 (sitting-2 decision 8): the structural architecture DERIVES —
    # the dashboard and checks scan the registries + source AST — so no
    # docs/architecture.md way-station is scaffolded; the authored narrative
    # ships as docs/runtime-flows.md instead (asserted in the file list).
    assert not (scaffold / "docs" / "architecture.md").exists()


def test_scaffold_stamps_kit_version(scaffold):
    # docs/kit-version records the kit commit the scaffold came from, so a later
    # re-sync is a diff against kit HEAD, not a guess (ADOPTING.md §6).
    stamp = scaffold / "docs" / "kit-version"
    assert stamp.exists(), "bootstrap must write docs/kit-version"
    text = stamp.read_text(encoding="utf-8")
    # ...and points the reader at the re-sync guidance. The stamp names the PACK
    # (the procedure's one home since OI-27) as well as the framing section: for a
    # tarball adopter with an `unknown` label this comment is the only pointer
    # they have.
    assert "RESYNC_PACK.md" in text
    assert "ADOPTING.md" in text
    # The last non-comment line is the identity: a short SHA (+ optional -dirty
    # + date) or the explicit unknown marker for a non-git kit copy.
    ident = [ln for ln in text.splitlines() if ln and not ln.startswith("#")][-1]
    assert ident.strip(), "kit-version must carry a non-empty identity line"


def test_non_git_kit_copy_warns_that_the_scaffold_has_no_resync_anchor(tmp_path):
    """The tarball adopter must be TOLD it has no anchor — loudly, exit 0 (OI-27).

    Copying `project-trajectory/` out of the repo reproduces the tarball shape
    exactly: git walks UP from the kit dir to find a checkout, so a kit sitting
    outside any repo resolves to nothing and `kit_version()` can only stamp
    `unknown`. That path used to be SILENT: the loud stamp warning fires on
    `dirty`, which the no-git branch hard-codes False, so the one adopter with
    NO anchor at all was the only one never told. Warning, not refusing — a
    tarball is a documented way in, so the exit code stays 0 and the scaffold is
    still produced; what changes is that the missing anchor is visible while the
    operator still remembers which kit they downloaded.
    """
    loose_kit = tmp_path / "tarball" / "project-trajectory"
    shutil.copytree(KIT, loose_kit)
    assert not (tmp_path / "tarball" / ".git").exists()
    dest = tmp_path / "adopter"
    dest.mkdir()

    proc = run_py([loose_kit / "scripts" / "bootstrap.py", "--dest", dest], cwd=dest)

    # Exit code UNCHANGED — this is a warning, not a gate.
    assert proc.returncode == 0, proc.stdout + proc.stderr
    stamp = (dest / "docs" / "kit-version").read_text(encoding="utf-8")
    assert "unknown (kit not a git checkout)" in stamp
    # ...and the warning is loud, on stderr, and names the consequence rather
    # than just the fact (a reader who sees "unknown" in a stamp file has to be
    # told that the documented upgrade path is what it costs them).
    assert "WARNING" in proc.stderr, (
        "the no-git stamp path must warn on stderr, not ship silently:\n" + proc.stderr
    )
    lowered = proc.stderr.lower()
    assert "no re-sync anchor" in lowered
    assert "adopting.md" in lowered, "the warning must point at the re-sync guide"


def test_tarball_kit_inside_a_foreign_repo_does_not_steal_its_anchor(tmp_path):
    """A kit extracted INSIDE someone else's git repo must stamp `unknown`.

    `git rev-parse` searches parent directories, so before the tracked-file
    probe this shape resolved to the ENCLOSING repo's HEAD — a false re-sync
    anchor pointing at a commit that never contained the kit, which is worse
    than no anchor at all (the adversarial round's finding). The kit is only
    anchored when its own files are TRACKED in the checkout rev-parse found.
    """
    foreign = tmp_path / "someones-monorepo"
    foreign.mkdir()
    env_git = ["git", "-C", str(foreign), "-c", "user.name=t", "-c", "user.email=t@t"]
    subprocess.run(env_git[:3] + ["init", "-q"], check=True)
    pin_autocrlf(foreign)  # WI-461/WI-465; see conftest.pin_autocrlf
    (foreign / "unrelated.txt").write_text("not the kit\n", encoding="utf-8")
    subprocess.run(env_git + ["add", "unrelated.txt"], check=True)
    subprocess.run(env_git + ["commit", "-qm", "foreign history"], check=True)

    loose_kit = foreign / "vendor" / "project-trajectory"
    shutil.copytree(KIT, loose_kit)  # extracted, never `git add`ed
    dest = tmp_path / "adopter"
    dest.mkdir()

    proc = run_py([loose_kit / "scripts" / "bootstrap.py", "--dest", dest], cwd=dest)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    stamp = (dest / "docs" / "kit-version").read_text(encoding="utf-8")
    assert "unknown (kit not a git checkout)" in stamp, (
        "an untracked kit inside a foreign repo must not inherit that repo's "
        "HEAD as its anchor:\n" + stamp
    )
    assert "WARNING" in proc.stderr and "no re-sync anchor" in proc.stderr.lower()


def test_kit_version_unknown_label_has_one_home():
    """The `unknown` label is a constant both return paths and the warner share.

    Three copies of the same string is how the warning came to fire on one path
    and not the other: `write_stamps` can only branch on the label it is handed,
    so the label and the branch must be the same literal by construction.
    """
    boot = load_script("bootstrap")
    src = (SCRIPTS / "bootstrap.py").read_text(encoding="utf-8")
    assert boot.KIT_VERSION_UNKNOWN == "unknown (kit not a git checkout)"
    assert src.count('"' + boot.KIT_VERSION_UNKNOWN + '"') == 1, (
        "the unknown-kit label must be written out once (KIT_VERSION_UNKNOWN); "
        "every other site refers to the constant"
    )


def test_kit_license_travels_inside_the_portable_unit():
    """The license must live where the copy-in step can reach it (WI-097/OI-4).

    Adopting the kit copies `project-trajectory/` — a LICENSE sitting only at
    this repo's root would be left behind, which is exactly the H-3 gap
    (a repo built to be copied, with no terms attached to what gets copied).
    So the kit carries its own copy, and the two must stay byte-identical or
    the copy is a silently different license.
    """
    root = (ROOT / "LICENSE").read_text(encoding="utf-8")
    kit = (KIT / "LICENSE").read_text(encoding="utf-8")
    assert "Apache License" in root and "Version 2.0" in root
    assert kit == root, (
        "project-trajectory/LICENSE has drifted from the root LICENSE — the "
        "copied kit would carry different terms from the repo it came from"
    )
    notice = (ROOT / "NOTICE").read_text(encoding="utf-8")
    assert "Apache License, Version 2.0" in notice


def test_scaffold_records_the_kit_license_and_its_scope(scaffold):
    """docs/kit-license carries the FULL text (Apache-2.0 §4(a)) plus its scope.

    A pointer to a URL would not satisfy §4(a) for anyone redistributing the
    adopting repo, and text with no scope note would read as if the kit were
    licensing the adopter's own work — which it is not.
    """
    stamp = scaffold / "docs" / "kit-license"
    assert stamp.exists(), "bootstrap must write docs/kit-license"
    text = stamp.read_text(encoding="utf-8")
    # The full instrument, not a reference to one.
    assert "TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION" in text
    assert "END OF TERMS AND CONDITIONS" in text
    assert (KIT / "LICENSE").read_text(encoding="utf-8") in text
    # ...and the scope note that keeps it from over-claiming.
    lowered = text.lower()
    assert "your own" in lowered or "are yours" in lowered, (
        "kit-license must state that the adopter's own code is not covered"
    )
    assert "docs/kit-version" in text  # the §4(b) 'what did I change' pointer

    # §4(d) attribution travels, and survives a PRIVACY-CHECKED adopting repo.
    # A real name in a scaffold is a legal requirement, not a leak, so the one
    # line carrying it is marked — and the License text itself carries none, so
    # that marker stays a single auditable exception rather than a habit.
    # (test_check_privacy's fresh-scaffold sweep is the enforcing half.)
    attribution = [ln for ln in text.splitlines() if "Copyright 2026" in ln]
    assert len(attribution) == 1, attribution
    assert "privacy-ok" in attribution[0].lower(), attribution[0]
    assert "Peter Johnson" not in (KIT / "LICENSE").read_text(encoding="utf-8"), (
        "the LICENSE instrument must keep the stock Apache appendix placeholder; "
        "real attribution belongs in NOTICE and the kit-license header"
    )


def test_scaffold_pins_hook_line_endings(scaffold):
    # The sh-based git hook breaks under Windows autocrlf without an eol=lf pin;
    # the scaffolded .gitattributes must carry that rule (friction from the pilot).
    ga = scaffold / ".gitattributes"
    assert ga.exists(), "bootstrap must scaffold .gitattributes"
    text = ga.read_text(encoding="utf-8")
    assert ".githooks/pre-commit text eol=lf" in text
    assert ".githooks/pre-push text eol=lf" in text
    # THE GLOBAL RULE, ASSERTED SINCE 2026-08-20 (the batch review's ROUND-SOL
    # MINOR-15). Five test modules rely on this line for CRLF-safety — fixture
    # trees are built by copying kit files and then diffed byte-for-byte — and
    # nothing pinned it: deleting it from the template left every hook-specific
    # assertion above green while Windows fixtures began producing CRLF diffs
    # and snapshot mismatches. The default is the load-bearing half; the
    # per-path rules below it are the exceptions.
    assert "* text=auto eol=lf" in text, (
        "the scaffolded .gitattributes must carry the global LF normalization "
        "default — the per-path hook pins do not cover the fixture trees that "
        "depend on it"
    )


def test_scaffolded_process_doc_drops_template_meta_prose(scaffold):
    # Once copied, docs/process.md *is* the process doc — the "(template)" title
    # and "Copy this into a new repo" meta-prose read wrong and are stripped.
    proc = (scaffold / "docs" / "process.md").read_text(encoding="utf-8")
    assert "# Development Process" in proc
    assert "(template)" not in proc.splitlines()[0]
    assert "Copy this into a new" not in proc


def test_readme_scaffolded_with_project_name(scaffold):
    # The README skeleton is the human front door (WI-1.12): bootstrap fills
    # the one dynamic placeholder (project name = destination folder) and the
    # skeleton points at the launchers + the ladder for the kickoff agent to
    # build out from the brief.
    readme = (scaffold / "README.md").read_text(encoding="utf-8")
    assert "{{PROJECT_NAME}}" not in readme, "placeholder must be filled"
    assert readme.splitlines()[0] == "# " + scaffold.name
    assert "run.cmd" in readme  # points at the product launchers
    assert "onboard" in readme  # points at the onboarding ladder


def test_readme_vision_tag_and_needs_pointer(scaffold):
    # Thread 37: the README's ## Vision section (anchored by the singleton
    # PROJECT-VISION: token) is the purpose fact's canonical home; the needs
    # registry points at it with a real link, so check_docs mechanically keeps
    # the pointer from dangling (test_clean_scaffold_passes exercises that).
    readme = (scaffold / "README.md").read_text(encoding="utf-8")
    assert "## Vision" in readme
    assert "PROJECT-VISION:" in readme
    needs = (scaffold / "docs" / "requirements" / "stakeholder-needs.toml").read_text(
        encoding="utf-8"
    )
    assert "](../../README.md#vision)" in needs


def test_scaffolds_owner_scratchpad(scaffold):
    # FB3: the owner scratchpad ships at the root with a loud agents-ignore header
    # and the secrets-floor caveat. It carries no placeholders, so the scaffolded
    # copy is content-identical to the kit template.
    pad = scaffold / "OWNER_SCRATCHPAD.md"
    assert pad.exists(), "bootstrap must scaffold OWNER_SCRATCHPAD.md"
    text = pad.read_text(encoding="utf-8")
    assert "For the human owner only" in text
    assert "do **NOT** read" in text  # the agents-ignore instruction
    assert "secrets floor still scans this file" in text  # not a secrets-safe zone
    template = (KIT / "OWNER_SCRATCHPAD.template.md").read_text(encoding="utf-8")
    assert text == template, "scaffolded scratchpad must match the kit template"


def test_readme_never_overwritten(tmp_path):
    # Adoption case: an existing README is the project's own front door —
    # bootstrap must skip it (same default-skip contract as every template).
    dest = tmp_path / "repo"
    dest.mkdir(parents=True)
    (dest / "README.md").write_text("my project's own readme", encoding="utf-8")
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", dest], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = (dest / "README.md").read_text(encoding="utf-8")
    assert text == "my project's own readme"


def test_resync_never_reruns_the_scaffold_initializers(tmp_path):
    # Re-sync against an adopted repo must not re-run the fresh-scaffold
    # generator initialization (initialize_generated_docs gates on this run
    # having CREATED docs/status.md — a re-sync skips existing files, so the
    # gate holds; it rode docs/architecture.md until WI-455 retired that file
    # from the scaffold surface). A sentinel open-items surface owned by the
    # adopter must survive byte-identical.
    dest = tmp_path / "adopted"
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", dest], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    sentinel = "<!-- FOREIGN GENERATOR OWNS THIS -->\n"
    (dest / "docs" / "open-items.html").write_text(sentinel, encoding="utf-8")
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", dest], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = (dest / "docs" / "open-items.html").read_text(encoding="utf-8")
    assert text == sentinel


def test_run_launchers_delegate_to_run_menu(scaffold):
    # The evaluator's rungs (WI-067): the root launchers are thin delegates to
    # scripts/run_menu.py, which reads the docs/stack.ini [run] section — the
    # duplicated RUN_CMD is retired, so the launch commands live in one place.
    # A fresh scaffold ships an inert [run]-less stack.ini (guidance + exit 1).
    assert (scaffold / "scripts" / "run_menu.py").exists()
    cmd = (scaffold / "run.cmd").read_text(encoding="utf-8")
    assert "run_menu.py" in cmd, "run.cmd must delegate to run_menu.py"
    assert "RUN_CMD" not in cmd, "the duplicated RUN_CMD must be gone"
    sh = (scaffold / "run.sh").read_text(encoding="utf-8")
    assert "run_menu.py" in sh, "run.sh must delegate to run_menu.py"
    assert "RUN_CMD" not in sh, "the duplicated RUN_CMD must be gone"
    command = (scaffold / "run.command").read_text(encoding="utf-8")
    assert "./run.sh" in command, ".command must delegate to run.sh"
    assert "RUN_CMD" not in command, ".command must not carry a third copy"
    # The shipped stack.ini has no active [run] section (commented examples
    # only), so the launcher degrades to guidance rather than launching nothing.
    ini = (scaffold / "docs" / "stack.ini").read_text(encoding="utf-8")
    assert "\n[run]" not in ini, "a fresh scaffold ships the [run] examples commented"


def test_scaffold_ships_every_policy_dial_in_one_home(scaffold):
    # SN-028: docs/process.toml carries every dial a fresh scaffold declares,
    # and each is TYPED (a bool is a bool, the reviewer count is an int) rather
    # than a one-word string every reader re-parses. Every VALUE is the one the
    # file it replaced shipped, with ONE deliberate exception carrying its own
    # ruling: WI-433 (owner 2026-08-11) ships `blackout` DISABLED
    # (`12:00-12:00`, start == end) rather than the kit author's own
    # 12:00-19:00 window, because an adopter should not inherit a
    # business-hours blackout in a timezone they did not choose. Folding a file
    # into another file is a MOVE; a default reversed inside a refactor is a
    # prior ruling overturned without its own review, and a comment is not
    # where that decision gets made — this one has a ruling, and
    # tests/test_blackout_isolation.py holds the rest of it.
    cfg = process_toml(scaffold)
    # SN-029: the gate-authority posture is the RUNG-THROUGH dial plus its two
    # orthogonal dials, not a stored enum word. The default is the conservative
    # end — WI-493 re-keyed the dial from the 0-4 ordinal to the DevStg-* rung
    # string it always meant, and `4` is now `"DevStg-Release"`.
    assert cfg["attestation"]["human_approval_through"] == "DevStg-Release"
    assert cfg["attestation"]["keep_nondependent"] is False
    assert "gate_policy" not in cfg["attestation"]
    assert cfg["attestation"]["human_approval_through"] == "DevStg-Release"
    assert cfg["policies"] == {
        "push": "human",
        "review_rounds": 1,
        "privacy_check": False,
        "secrets_scan": True,
        "privacy_review": "require",
        "guardrails": "off",
        "blackout": "12:00-12:00",
    }
    # WI-432: the six check-enablement toggles are dials here too, folded in by
    # the 2026-08-11 overturn of WI-423 — every one VISIBLE, and every one at
    # the default it had as an absent file. The two opt-in dials are the point
    # of the assertion: "key them all to on / true" made the DECLARATION
    # explicit; a `live_status = true` or `subagent_gate = "ask"` here would be
    # a behaviour flip smuggled in under a re-homing.
    assert cfg["checks"] == {
        "trajectory_check": True,
        "interfaces_check": True,
        "components_check": True,
        "okf_export": True,
        "live_status": False,
        "subagent_gate": "off",
        # WI-486 / OI-42's seventh dial, and the first NUMBER in this section:
        # the reverse back-link coverage bar. `0` is its off position, and the
        # same argument as the two opt-in dials above applies — shipping the
        # recorded 50% target here would arm a bar every fresh scaffold fails
        # on its first run.
        "backlink_coverage_min": 0,
    }
    for legacy in (
        "gate-policy",
        "push-policy",
        "review-policy",
        "privacy-check",
        "secrets-scan",
        "privacy-review",
        "guardrails-policy",
        "blackout",
        "trajectory-check",
        "interfaces-check",
        "components-check",
        "okf-export",
        "live-status",
        "subagent-gate",
    ):
        assert not (scaffold / "docs" / legacy).exists(), (
            "SN-028: docs/" + legacy + " must not ship beside docs/process.toml"
        )


def test_agent_resume_launchers_ship_inert_with_edit_slots(scaffold):
    # The work-resume counterpart of run.* (Thread 33): root agent launchers
    # over scripts/agent_loop.py, shipped inert (empty AGENT_CMD) with a
    # marked EDIT slot and an explicit consent note; .command delegates to
    # .sh so the POSIX slots live once.
    cmd = (scaffold / "agent-resume.cmd").read_text(encoding="utf-8")
    assert 'set "AGENT_CMD="' in cmd, "agent-resume.cmd must ship inert"
    assert "EDIT FOR YOUR PROJECT" in cmd
    assert "CONSENT" in cmd
    sh = (scaffold / "agent-resume.sh").read_text(encoding="utf-8")
    assert 'AGENT_CMD=""' in sh, "agent-resume.sh must ship inert"
    assert "CONSENT" in sh
    command = (scaffold / "agent-resume.command").read_text(encoding="utf-8")
    assert "./agent-resume.sh" in command, ".command must delegate to .sh"
    assert 'AGENT_CMD=""' not in command, ".command must not carry a third copy"
    engine = (scaffold / "scripts" / "agent_loop.py").read_text(encoding="utf-8")
    assert "run-state" in engine  # the engine, not a stub


def test_agents_choice_seeds_agent_resume_slots(tmp_path):
    # --agents claude seeds the launcher EDIT slots with that agent's example
    # command (the consent line: the seeded AGENT_CMD carries the bypass flag
    # the launcher header explains). The slots stay repo-owned EDIT blocks.
    dest = tmp_path / "repo"
    proc = run_py(
        [SCRIPTS / "bootstrap.py", "--dest", dest, "--agents", "claude"],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    sh = (dest / "agent-resume.sh").read_text(encoding="utf-8")
    # No {prompt} in the seeded command: prompt delivery is via stdin (WI-216).
    assert 'AGENT_CMD="claude -p --model {model}' in sh
    # Strong tier is the seeded default (driver sessions are gate-bearing);
    # cheaper phases are the model map's job.
    assert 'AGENT_MODEL="opus"' in sh
    cmd = (dest / "agent-resume.cmd").read_text(encoding="utf-8")
    assert 'set "AGENT_CMD=claude -p --model {model}' in cmd
    assert "seeded agent-resume launchers" in proc.stdout


def test_default_scaffold_leaves_agent_resume_unseeded(scaffold):
    # No agent chosen (the CI-safe default) -> the slots stay empty; the
    # launchers are discoverable but inert.
    sh = (scaffold / "agent-resume.sh").read_text(encoding="utf-8")
    assert 'AGENT_CMD=""' in sh


# RETIRED (concurrency-restructure Phase 5): the AGENT_JOBS single-home
# migration test (WI-274 / IF-068). Its whole subject — the launchers'
# `${AGENT_JOBS:-2}` dispatcher ceiling and the `[agent-loop] jobs` dial it had
# to lose to — retired with the parallel dispatcher, so the scaffolded launchers
# carry no AGENT_JOBS slot and `resolve_coordinator_dials` returns only
# (model, model_map). Nothing is left to migrate. The surviving launcher
# single-home rule (model/model-map via docs/stack.ini) is pinned by
# test_agent_loop.py::test_resolve_coordinator_dials_precedence.


def test_scaffold_text_writes_are_lf_on_every_platform(tmp_path):
    # M-15: bootstrap routes every scaffold TEXT write through _write_text_lf,
    # so a Windows bootstrap cannot emit CRLF scaffolds — above all the seeded
    # agent-resume.sh, whose CRLF shebang breaks `#!/bin/sh` (the exact trap
    # the scaffolded .gitattributes documents). One seeded launcher + one
    # generated/rewritten .md, asserted at the byte level.
    dest = tmp_path / "repo"
    proc = run_py(
        [SCRIPTS / "bootstrap.py", "--dest", dest, "--agents", "claude"],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert b"\r" not in (dest / "agent-resume.sh").read_bytes()
    # status.md is both marker-generated (.md branch) and appended to by
    # record_agent_choice — CRLF from either write site would land here.
    assert b"\r" not in (dest / "docs" / "status.md").read_bytes()


def test_dry_run_writes_nothing(tmp_path):
    proc = run_py(
        [SCRIPTS / "bootstrap.py", "--dest", tmp_path / "repo", "--dry-run"],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert not (tmp_path / "repo").exists()


def test_rerun_skips_existing_files(scaffold):
    (scaffold / "CLAUDE.md").write_text("customized", encoding="utf-8")
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", scaffold], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (scaffold / "CLAUDE.md").read_text(encoding="utf-8") == "customized"


def test_force_overwrites_existing_files(scaffold):
    # The --force direction SR-011/TC-011 claim (counterpart to the default skip):
    # a re-run WITH --force overwrites an existing, even hand-customized, kit file.
    target = scaffold / "CLAUDE.md"
    target.write_text("customized", encoding="utf-8")
    proc = run_py(
        [SCRIPTS / "bootstrap.py", "--dest", scaffold, "--force"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert target.read_text(encoding="utf-8") != "customized"


# --- Privacy-check toggle (Thread 38 -> identity/privacy reframe) --------------


def test_privacy_check_defaults_to_false(scaffold):
    # The scaffolded toggle is `false` — the privacy gate is off by default, so
    # existing adopters and default scaffolds see zero change (the always-on
    # secrets floor still runs regardless).
    assert process_key(scaffold, "policies", "privacy_check") is False


def test_privacy_check_flag_sets_toggle(tmp_path):
    # --privacy-check sets the toggle at repo creation, keeping the template's
    # explanatory header above the value.
    dest = tmp_path / "repo"
    proc = run_py(
        [
            SCRIPTS / "bootstrap.py",
            "--dest",
            dest,
            "--privacy-check",
            "true",
        ],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    policy = dest / "docs" / "process.toml"
    assert process_key(dest, "policies", "privacy_check") is True
    assert policy.read_text(encoding="utf-8").startswith("#"), "header kept"
    # KEYED-GREPPABLE (M-42): the git hooks read this exact line shape in pure
    # sh, so a Python-less box still fails closed on a declared privacy policy.
    assert "\nprivacy_check = true\n" in policy.read_text(encoding="utf-8")


def test_setup_scripts_advise_on_privacy_not_pin_identity():
    # Identity is user-owned: the setup launchers no longer set an author
    # identity. They read docs/privacy-check and advise (via check_privacy
    # --author) when a private author would be blocked; they must never touch
    # global git config.
    for name in ("setup.sh", "setup.ps1"):
        text = (KIT / "scripts" / name).read_text(encoding="utf-8")
        assert "privacy-check" in text, name + " must read the privacy toggle"
        assert "git config --global" not in text, name + " must stay repo-local"


def test_setup_scripts_enforce_the_python_311_floor():
    # The declared runtime floor must govern the scripts that create/reuse the
    # project venv, not merely documentation and CI.
    for name in ("setup.sh", "setup.ps1"):
        text = (KIT / "scripts" / name).read_text(encoding="utf-8")
        assert "sys.version_info >= (3, 11)" in text, (
            name + " does not enforce the Python 3.11 floor"
        )
        assert "Existing ./.venv" in text or "Existing .\\.venv" in text, (
            name + " does not refuse an unsupported existing venv"
        )


# --- Agent selection & the skills layer (WI-1.9) -----------------------------


def _bootstrap(tmp_path, *extra):
    dest = tmp_path / "repo"
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", dest, *extra], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return dest


def test_non_interactive_default_materializes_no_agent_layer(tmp_path):
    # The property the spec pins: run non-interactively with NO --agents flag and
    # the scaffold is the historical, agent-neutral one — no .claude/.gemini dirs,
    # no skills, no setup note. (conftest.run_py closes stdin, so the omitted-flag
    # path takes its 'none' default exactly as CI would.)
    dest = _bootstrap(tmp_path)
    assert not (dest / ".claude").exists(), "default must not materialize .claude"
    assert not (dest / ".gemini").exists(), "default must not materialize .gemini"
    status = (dest / "docs" / "status.md").read_text(encoding="utf-8")
    assert "<!-- agent-setup -->" not in status, "default must add no setup note"


def test_explicit_agents_none_matches_default(tmp_path):
    # --agents none is the same agent-neutral result, just stated explicitly.
    dest = _bootstrap(tmp_path, "--agents", "none")
    assert not (dest / ".claude").exists()
    assert not (dest / ".gemini").exists()


def test_agents_claude_materializes_kit_skills_and_inert_hook(tmp_path):
    dest = _bootstrap(tmp_path, "--agents", "claude")
    skills = dest / ".claude" / "skills"
    assert skills.is_dir(), "claude selection must materialize .claude/skills"
    # Only kit-scope skills ship downstream; the this-repo ones must NOT.
    names = {p.name for p in skills.iterdir()}
    assert {"registry-hygiene", "downstream-resync", "gate-advance"} <= names
    assert "byte-budget-guard" not in names, "this-repo skill must not ship"
    assert "session-protocol" not in names, "this-repo skill must not ship"
    # Each materialized skill keeps its neutral SKILL.md verbatim.
    assert (skills / "registry-hygiene" / "SKILL.md").exists()
    # The hook config is copied INERT (as an example), never a live settings.json.
    assert (dest / ".claude" / "settings.json.example").exists()
    assert not (dest / ".claude" / "settings.json").exists()
    # Gemini gets nothing for a claude-only selection.
    assert not (dest / ".gemini").exists()
    # The choice + date is recorded in status.md.
    status = (dest / "docs" / "status.md").read_text(encoding="utf-8")
    assert "<!-- agent-setup -->" in status
    assert "agents=`claude`" in status


def test_agents_both_materializes_for_both(tmp_path):
    dest = _bootstrap(tmp_path, "--agents", "both")
    for agent_dir in (".claude", ".gemini"):
        skills = dest / agent_dir / "skills"
        assert skills.is_dir(), agent_dir + " must get skills"
        assert (skills / "gate-advance" / "SKILL.md").exists()
        assert (dest / agent_dir / "settings.json.example").exists()


def test_domain_skills_require_matching_explicit_opt_in(tmp_path):
    for name in ("web", "hardware", "neutral"):
        (tmp_path / name).mkdir()
    web = _bootstrap(tmp_path / "web", "--agents", "claude", "--domain", "web")
    web_skills = {p.name for p in (web / ".claude" / "skills").iterdir()}
    assert "ui-accessible-component" in web_skills
    assert "ros2-perception-pipeline" not in web_skills

    hardware = _bootstrap(
        tmp_path / "hardware", "--agents", "codex", "--domain", "hardware"
    )
    hardware_skills = {p.name for p in (hardware / ".agents" / "skills").iterdir()}
    assert "ros2-perception-pipeline" in hardware_skills
    assert "ui-accessible-component" not in hardware_skills

    neutral = _bootstrap(tmp_path / "neutral", "--agents", "claude")
    neutral_skills = {p.name for p in (neutral / ".claude" / "skills").iterdir()}
    assert "ui-accessible-component" not in neutral_skills
    assert "ros2-perception-pipeline" not in neutral_skills
    assert "registry-hygiene" in neutral_skills


def test_scaffold_with_agents_still_green(tmp_path):
    # Materializing the agent layer must not break the out-of-the-box harness.
    dest = _bootstrap(tmp_path, "--agents", "both")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=dest)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=dest
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_scope_matcher_is_tag_intersection():
    boot = load_script("bootstrap")
    # `any` on an axis always matches; a specific value matches only its members.
    py_only = {"stacks": ["python"], "domains": ["any"]}
    assert boot.matches_scope(py_only, "python", "any", False)
    assert not boot.matches_scope(py_only, "go", "any", False)
    # A skipped answer ("") never filters.
    assert boot.matches_scope(py_only, "", "web", False)
    any_skill = {"stacks": ["any"], "domains": ["any"]}
    assert boot.matches_scope(any_skill, "rust", "hardware", True)


def test_select_skills_returns_only_kit_scope():
    boot = load_script("bootstrap")
    chosen = {n for n, _ in boot.select_skills("any", "any", False)}
    assert {"registry-hygiene", "downstream-resync", "gate-advance"} <= chosen
    assert "byte-budget-guard" not in chosen
    assert "session-protocol" not in chosen


def test_skills_index_is_fresh():
    # The generated INDEX.csv must match the SKILL.md files (like arch-map --check).
    proc = run_py([SCRIPTS / "gen_skills_index.py", "--check"], cwd=KIT)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_scaffold_ships_no_tracks_layer(scaffold):
    # WI-210: the parallel-tracks layer is retired outright — no scaffold
    # (and no flag) produces its files; the dispatcher's worker assignment is
    # the only lane concept.
    assert not (scaffold / "docs" / "tracks").exists()
    assert not (scaffold / "docs" / "requirements" / "id-blocks.md").exists()
    # the lock is gitignored downstream so a runtime pid file never lands
    assert "out/agent-loop.lock" in (scaffold / ".gitignore").read_text(
        encoding="utf-8"
    )


def test_strip_provenance_drops_review_anchors_keeps_prose_and_code():
    # WI-079: scaffolded scripts must not carry citations into this meta-repo's
    # docs/archive/ review docs (which do not ship). strip_provenance drops the
    # (REVIEW_GRIND_*/THREAD_*_REVIEW code) tags across every citation SHAPE
    # while leaving the surrounding prose — and never touching code.
    strip = load_script("bootstrap").strip_provenance
    cases = {
        # whole-parenthetical -> the paren and its leading space go
        "fall back to the default (REVIEW_GRIND_A A5).": "fall back to the default.",
        "posture (REVIEW_GRIND_FULL C9): the target": "posture: the target",
        # leading clause in a shared paren -> keep the prose
        "console (REVIEW_GRIND_FULL C5; verbatim across the kit).": "console (verbatim across the kit).",
        "scope (REVIEW_GRIND_A A2 — false-positive control is the point).": "scope (false-positive control is the point).",
        # trailing clause in a shared paren -> keep the prose and the ")"
        "adjacent (a gap > 1 line is a second block; REVIEW_GRIND_A A6).": "adjacent (a gap > 1 line is a second block).",
        # a citation wrapped across one comment-continuation line
        "drifted — REVIEW_GRIND_FULL\n    # C6). Change both": "drifted). Change both",
        # a whole comment line that is only the citation -> the line goes
        "no cruft behind\n    # (REVIEW_GRIND_A A7).\n    if pruned:": "no cruft behind\n    if pruned:",
        # a citation that opens a comment line before real prose
        "\n    # (THREAD_52_REVIEW.md F4). Kept recursive so": "\n    # Kept recursive so",
        # bare, "See"-introduced, wrapped onto its own comment line
        "directory explicitly. See\n# THREAD_52_REVIEW.md F5.\ntry:": "directory explicitly.\ntry:",
    }
    for src, want in cases.items():
        assert strip(src) == want, "shape not stripped cleanly:\n" + repr(strip(src))
    # Must NOT touch code identifiers or the hyphenated phase names that merely
    # LOOK like anchors (REVIEW_GRIND_[A-Z]+ excludes REVIEW_PHASES).
    for keep in (
        "frozenset(REVIEW_PHASES)",
        "Reviewer phases (REVIEW-A/REVIEW-B) fall",
    ):
        assert strip(keep) == keep


def test_scaffolded_scripts_carry_no_archive_review_anchors(scaffold):
    # The kit source DOES cite its archive review docs; the scaffolded copies
    # must not (bootstrap strips them on copy) — and must stay valid Python.
    anchor = re.compile(r"THREAD_\d+_REVIEW|REVIEW_GRIND_[A-Z]+")
    kit_hits = 0
    for src in sorted(SCRIPTS.glob("*.py")):
        kit_hits += len(anchor.findall(src.read_text(encoding="utf-8")))
        copied = scaffold / "scripts" / src.name
        if not copied.exists():
            continue  # *.template.* sources scaffold under a renamed target
        text = copied.read_text(encoding="utf-8")
        assert not anchor.search(text), "archive anchor survived in " + src.name
        compile(text, str(copied), "exec")
    assert kit_hits > 0, "kit source should still carry the provenance citations"


def test_the_common_package_ships_complete(scaffold):
    """Every module of the shared package reaches a real scaffold, and imports.

    WI-448. The sibling-import guard below answers a DIFFERENT question and
    cannot answer this one: it compares TOP-LEVEL import names, so once any
    `scripts/kitlib/*.py` row is in MAPPING the name `kitlib` reads as mapped
    and a MISSING MODULE INSIDE the package is invisible to it. Probed, not
    assumed — deleting the `config.py` row leaves that guard green.

    Per-file completeness is a MANIFEST question, so it is asked of a real
    scaffold: the copied package must hold exactly the kit's module set, and
    must actually import there. That is the standing lesson from the
    `schedule.py` omission stated for a package — a partial copy would pass
    every in-repo test, because this repo's `scripts/` holds every file, and
    would ImportError on an adopter's first check.
    """
    kit_modules = sorted(p.name for p in (SCRIPTS / "kitlib").glob("*.py"))
    assert "__init__.py" in kit_modules, "kitlib is not a package in the kit"
    shipped = sorted(p.name for p in (scaffold / "scripts" / "kitlib").glob("*.py"))
    assert shipped == kit_modules, (
        "the scaffold's copy of kitlib/ is not the kit's module set — "
        "MAPPING is missing a row (or carries a stale one): "
        "kit={} scaffold={}".format(kit_modules, shipped)
    )
    # ...and the copy is IMPORTABLE from where a shipped script sits, which is
    # the property the file list is only a proxy for. Run out of `scripts/`,
    # exactly as a scaffolded check resolves it (sys.path[0] = the script dir).
    proc = run_py(
        [
            "-c",
            "import kitlib, kitlib.config, kitlib.git, kitlib.ladder, "
            "kitlib.registry, kitlib.stage; "
            "assert kitlib.ladder.STAGE_OF == len(kitlib.ladder.STAGE_ORDER); "
            "assert kitlib.stage.FLOOR in kitlib.ladder.LADDER_RUNGS; "
            "print(kitlib.registry.spec_work_dir('docs/x.csv'))",
        ],
        cwd=scaffold / "scripts",
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_bootstrap_imports_only_the_common_package():
    """THE RULE THAT REPLACED F5, ASSERTED RATHER THAN COMMENTED.

    Owner ruling D-8 (`OI-16`) inverted its own step 2: shared helpers live in
    the shipped package and `bootstrap.py` imports FROM it. The replacing rule
    — *bootstrap imports the common package and nothing else* — had only ever
    been prose. It is load-bearing in one specific way: `bootstrap.py` is
    deliberately absent from its own MAPPING, so it must keep working from a
    bare kit checkout, and every sibling it imports becomes a load-bearing
    dependency of the installer. `kitlib` is safe to depend on precisely
    because it ships and is import-clean of the rest of `scripts/`; a second
    sibling would not be.
    """
    kit_modules = {p.stem for p in SCRIPTS.glob("*.py")} - {"bootstrap"}
    kit_modules |= {p.parent.name for p in SCRIPTS.glob("*/__init__.py")}
    tree = ast.parse((SCRIPTS / "bootstrap.py").read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            imported.add(node.module.split(".")[0])
    assert imported & kit_modules == {"kitlib"}, (
        "bootstrap.py must import the common package and nothing else "
        "(D-8/OI-16); it imports: " + ", ".join(sorted(imported & kit_modules))
    )
    # And the package must stay clean of the rest of scripts/, or the edge
    # above smuggles the whole graph into the scaffolder anyway.
    for module in sorted((SCRIPTS / "kitlib").glob("*.py")):
        mtree = ast.parse(module.read_text(encoding="utf-8"))
        for node in ast.walk(mtree):
            tops = set()
            if isinstance(node, ast.Import):
                tops = {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                tops = {node.module.split(".")[0]}
            assert not (tops & (kit_modules - {"kitlib"})), (
                "kitlib/{} imports a non-kitlib sibling: {}".format(
                    module.name, sorted(tops & kit_modules)
                )
            )


def test_every_sibling_imported_module_is_shipped_by_mapping():
    """A shipped script's sibling imports must themselves be in MAPPING.

    WI-379: `bootstrap.py`'s MAPPING decides what a fresh scaffold receives,
    and the kit's own `scripts/` dir holds every file — so a shipped module
    importing a sibling the MAPPING omits is invisible HERE and an
    ImportError THERE. It is also invisible to a downstream re-sync, because
    an already-adopted repo carries the file from an older kit; only a fresh
    scaffold reaches it. That is exactly how `schedule.py` went missing while
    `integrate.py claim` (the integration seam) and `drive.py` (the walk-away
    loop) both import it unguarded — a scaffold could not claim work at all.

    Guards the CLASS, not the instance: any future sibling extraction (WI-280
    alone added six) that forgets its MAPPING row fails here instead of in an
    adopter's repo.
    """
    # Read the MAPPING LITERAL, not the file text: a whole-file regex also
    # matches script names in docstrings and comments, which would silently
    # mark an unmapped module as mapped - a false negative on exactly the
    # module someone next mentions in prose (WI-379 review round 1).
    bootstrap_tree = ast.parse((SCRIPTS / "bootstrap.py").read_text(encoding="utf-8"))
    mapping_node = next(
        (
            node.value
            for node in bootstrap_tree.body
            if isinstance(node, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == "MAPPING" for t in node.targets)
        ),
        None,
    )
    assert mapping_node is not None, "bootstrap.py no longer defines MAPPING"
    # PACKAGES COUNT AS MODULES, BOTH SIDES OF THE COMPARISON (WI-448). Before
    # `kitlib/` this collapsed every MAPPING literal to a bare stem and globbed
    # only top-level `*.py`, so a package was invisible TWICE: `from kitlib
    # import config` yields the top-level name `kitlib`, which was in neither
    # `mapped` nor `kit_modules`, and the guard silently passed the one import
    # edge with the widest blast radius in the kit. `mapped` therefore also
    # carries the PACKAGE NAME of any `scripts/<pkg>/*.py` destination, and the
    # walk recurses so a package module's own sibling imports are checked too.
    mapped = set()
    for literal in ast.walk(mapping_node):
        if not (
            isinstance(literal, ast.Constant)
            and isinstance(literal.value, str)
            and literal.value.endswith(".py")
        ):
            continue
        parts = literal.value.split("/")
        mapped.add(parts[-1][:-3])
        if len(parts) > 2:  # scripts/<pkg>/<module>.py — the package ships too
            mapped.add(parts[-2])
    kit_modules = {p.stem for p in SCRIPTS.glob("*.py")}
    kit_modules |= {p.parent.name for p in SCRIPTS.glob("*/__init__.py")}

    missing = {}
    for path in sorted(SCRIPTS.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        owner = path.parent.name if path.parent != SCRIPTS else path.stem
        if owner == "bootstrap" or owner not in mapped:
            continue  # the scaffolder itself is not shipped; nor are kit-only tools
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                names = [node.module.split(".")[0]]
            for name in names:
                if name in kit_modules and name not in mapped:
                    missing.setdefault(name, set()).add(path.name)

    assert not missing, (
        "shipped script(s) import a sibling MAPPING omits: "
        + "; ".join(
            "{}.py <- {}".format(mod, ", ".join(sorted(who)))
            for mod, who in sorted(missing.items())
        )
    )
