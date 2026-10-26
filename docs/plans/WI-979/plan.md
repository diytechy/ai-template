# WI-979 implementation plan — architectural decomposition, text

Planner: fresh Claude Opus session, 2026-10-25. Read: the spec
`docs/work/active/wi-979/WI-979-arch-decomposition-text.md`, its `specref`
(review-churn plan item 12), the W3 dry-run record (`w3-dry-run/README.md`,
`rubric-draft.md`, `dry-run.md` §"Rubric assessment" and §"Missing questions
that changed the answer"), SR-186, SR-165, TC-166, TC-211, IF-035, IF-262,
IF-019, IF-254, IF-097, IF-098, and every file and test named below. Nothing
in the lane was changed.

## Architectural delta

DELTA: none

Each of the four clauses, checked against what the change touches:

- **A state:** none. No script gains a mode or a lifecycle state; all six
  deliverables are text a session reads.
- **A value in a domain:** none. The MAPPING gains one row and the skill set
  one member. Both are open member lists (IF-262's `data` cell and IF-035's
  form are unchanged), not closed domains. The `## 4.` section uses the
  closed tier set (`LLR`) as it stands.
- **An output depending on a new input:** none. `adjudicate_brief.tier_questions`
  reads the same home file and composes it under the same tiers rule, so an
  LLR brief carries one more section of a file it already reads.
  `review_brief.render_plan` fills the same template. No script reads the
  new rubric or the skill. Only critic, adjudicator and planner sessions do,
  as judgement guidance.
- **A new boundary:** none. No new channel or endpoint. The rubric is seeded
  through the existing scaffold mapping (IF-262), and the skill ships through
  the existing skill directory seam (IF-035).

This matches the spec's S5 answer.

## Plan

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Ship the rubric: template, seeded copy, MAPPING row, dogfood pin, scaffold expectation, README link | D1; D2; D3; D4; SR-186; SR-165 | IF-262 (one MAPPING row added; form unchanged) | |
| P2 | The `architecture-decomposition` skill, INDEX.csv, and this repo's two materialized copies | D5; D6; SR-186 | IF-035 (one skill added); IF-019 (INDEX.csv regenerated); IF-254 (`--check` floor) | P1 |
| P3 | `spine-questions.md` §4 (DevStg-Arch) pointing at the rubric | D7; SR-186 | IF-097 (SPINE_QUESTIONS home composed by the briefs; grammar unchanged); IF-098 (catalogue digest) | P1 |
| P4 | This repo's plan and scope rubrics point at the shared rubric and skill | D8; D9; SR-186 | no interface — this repo's own rubric prose, read by critic sessions; no script parses an anchor | P1; P2 |
| P5 | The single-plan brief names the skill beside the delta question; regenerate CATALOG.md | D10; SR-186 | IF-097 (PLAN-SINGLE template); IF-098 (catalogue row digest) | P2; P3 |
| P6 | One RESYNC_PACK.md entry for the whole change | D11; D12; D13; D14; D15; D16 | no interface — kit reference prose; `check_resync` reads only its heading grammar, which is unchanged | P1; P2; P3; P5 |
| P7 | Land-tip verification: commit bar, strict lints, generators, the touched slow modules, a temp scaffold | D17; SR-186; SR-165; TC-166 | IF-262; IF-035; IF-254 (run, not changed) | P1; P2; P3; P4; P5; P6 |

Excludes: TC-211 — it is SR-186's Release-trigger manual Inspection (`trigger = "release"`, `min_work_items = 10`) of the decomposition-proportionality procedure and its rubric. This item changes neither the procedure, nor `docs/rubrics/decomposition-proportionality.md`, nor SR-186, so the inspection keeps its release cadence and is not re-run in this lane.

TC-166 (SR-165, trace.py's component-registry derivation-record pass) is
cited by P7 as an unchanged-regression run. This item changes no script it
drives.

## Build order and commits

The spec's S1 sets the order: the rubric first, then the skill, then the
pointers, because a pointer that lands before its target is a broken link.
`scripts/check_resync.py` judges the range from the trunk base to the working
tree, and every row from P1 on touches a shipped file. So **either land the
lane as one commit after P6**, or add P6's entry heading in the first commit
and finish its body at P6. Write every new or edited file with LF endings: the
two byte-pins (dogfood boilerplate and `--check-agents`) compare bytes.

---

## P1 — The rubric

**Files.**

- New `project-trajectory/rubrics/architecture-decomposition.template.md`,
  written from `docs/plans/2026-10-11-review-churn/w3-dry-run/rubric-draft.md`
  with the edits below.
- New `docs/rubrics/architecture-decomposition.md`, a byte-identical copy.
- `project-trajectory/scripts/kitlib/bootstrap_manifest.py`: one MAPPING row,
  placed directly after the two existing rubric rows under their comment:
  `("rubrics/architecture-decomposition.template.md", "docs/rubrics/architecture-decomposition.md", "SR-186"),`.
  The third element is SR-163's purpose reference. SR-186 is Approved under
  SN-012, so the row adds no `unmapped_file` warning.
- `tests/test_dogfood_sync.py` `BOILERPLATE_COPIES`: add
  `"docs/rubrics/architecture-decomposition.md": "project-trajectory/rubrics/architecture-decomposition.template.md"`.
- `tests/test_bootstrap.py` `test_scaffold_contains_expected_files`: add
  `"docs/rubrics/architecture-decomposition.md"` after `docs/rubrics/rubric-000.md`.
- **One sentence in `project-trajectory/rubrics/README.template.md`**, and the
  same bytes in `docs/rubrics/README.md` (pinned byte-identical today). This
  file is not in the spec's list, and the sentence is needed for a reason the
  spec did not foresee. `tests/test_profile.py::test_default_scaffold_is_fully_green_including_warnings`
  requires **zero** check_docs WARN lines on a fresh scaffold. A seeded
  `docs/rubrics/architecture-decomposition.md` that nothing links to would be
  reported as an orphan there. Today the scaffold reaches `rubric-000.md` only
  through the README's link. Suggested text, after the "Shape" list: "The kit
  also seeds one shared rubric, `[architecture-decomposition.md](architecture-decomposition.md)`:
  the bar a component scope's decomposition is judged against at `DevStg-Arch`,
  when a work item's plan answers its architectural-delta question, and in an
  audit." It links the rubric and names no record id.

**Edits to the draft.**

1. *References read correctly for an adopter (D4).* At
   `docs/rubrics/architecture-decomposition.md`:
   - Every `[README](../../../rubrics/README.md)` becomes `[README](README.md)`,
     the sibling. It resolves in this repo, in a scaffold, and nowhere else.
   - Every other reference stays prose, as `rubrics/README.template.md`
     already writes them: `process.md §3` / `§4` / `§5` / `§6` / `§8`,
     `process-options.md` "(d2) Record the stopping boundary", and
     `prompts/spine-questions.md` §3 "Record the stopping boundary". Prose is
     used because `docs/process.md` does not exist in this repo, so a markdown
     link to it would break `check_docs` here. In a scaffold those are the
     MAPPING destinations.
   - Before landing, check each quoted title in its section:
     "Decompose, don't paraphrase" (PROCESS.md §3), "Review threat model"
     (§6), the requirements-before-architecture and recursion text (§4), one
     row per owner, far side and kind (§8), "(d2) Record the stopping boundary"
     (PROCESS_OPTIONS.md), and "Record the stopping boundary" (spine-questions §3).
   - The rubric names no record id (`WI-`, `SR-`, `LLR-`, `TC-`, `IF-`, `OI-`,
     `CMP-` followed by digits), no `docs/plans/` path and no "W3". CLAUDE.md
     forbids a token that means nothing in an adopter's repo.
2. *The five clarifications (D2)*, each written into the anchor that asks it.
   No `B5` is added.

   | # | Clarification | Anchor | Text the anchor gains (substance; builder words it) |
   |---|---|---|---|
   | 1 | ownership / allocation model | **A6** | Before judging a boundary, state the scope's ownership model for a file that several components' rows name: one implementation owner, several obligation allocations, or a declared kernel role. Requirement allocation is not implementation ownership. |
   | 2 | invariants a cut must preserve | **A7** (costs) | Each candidate states which invariants it preserves, and how: transaction scope, lock order, failure and retry ownership, durable effects. A cut that breaks one carries that as a cost, not as a stage-split objection. |
   | 3 | evidence: audit vs fresh design | **A4** (main); echoed in **A7** and **A8** | A4: each table cell names its evidence, and a blank says whether it means proven independence or unknown. An audit may rely on generated reports of the scope as built. A fresh design has the requirements and proposed interfaces only. A question the supplied evidence cannot answer is recorded as *not supplied* or *not assessable*, never read as a defect. A7: a comparison the evidence cannot settle ends in *insufficient evidence for approval*, with the missing evidence named. A8: the record's "remaining uncertainty" field (row 3 of D3 below). |
   | 4 | cost of enforceability and migration | **A7** (costs) | The access constraints that make the boundary hold, and the boundary tests that establish them. A migration plan wherever approved rows or tests would change. A file move is counted only when needed. |
   | 5 | what counts as one interface or one case | **A7** (costs); one clause in **A4** | A7: existing rows the cut newly crosses, new endpoint crossings, shared schema definitions and new semantic surfaces are counted separately, and the unknown remainder is stated. A4: a case count multiplies input choices; an import count or an interface-row count is never a case count. |

3. *A8's two descent rules (D3).* Rename A8's lead from "under the
   state-or-source test" to something that covers both rules. Then split the
   body:
   - **Requirement (obligation) descent:** tests 1 to 4 kept as drafted, as
     the rule for obligations.
   - **Component descent:** a component leaf stops when no information-hiding
     cut pays its way after the A1/A4/A7 comparison. Sub-decisions that are
     testable on their own do not by themselves force a cut.
   - **The stopping record** names the candidate children, the evidence, the
     remaining uncertainty and what would trigger a revisit, plus, for an
     obligation, the test that stopped it. A leaf without a record, or one
     citing a rule that does not hold, is a finding (kept from the draft).
4. Everything else is kept as drafted: A1–A3, A5, B1–B4, Terms, Intent and
   Verdict, apart from the README link fix. The spec puts the dry run's other
   anchor edits out of scope.

**Tests added (each fails before the change).**

- New `tests/test_architecture_decomposition_rubric.py`. It runs in-process
  in the smoke tier: not in `SLOW_MODULES`, and it reads files plus
  `load_script("bootstrap").mapping_entries()`.
  - `test_each_clarification_is_asked_in_its_anchor`: slice the template
    between consecutive `**A#` / `**B#` heads. Assert each anchor's key
    phrases from the table above sit in that anchor's slice: A6 "implementation
    owner" + "obligation allocation" + "kernel"; A7 "transaction scope" +
    "lock order" + "retry" + "durable effect", "access constraint" +
    "migration plan", "new endpoint crossing" + "shared schema" +
    "unknown remainder", "insufficient evidence for approval"; A4 "not supplied"
    + "not assessable". *Fails before:* the file does not exist.
  - `test_no_failure_pattern_is_added_for_them`: the set of `**B#` heads is
    exactly {B1, B2, B3, B4}.
  - `test_a8_separates_requirement_descent_from_component_descent`: the A8
    slice holds the four tests, the component rule's words "information-hiding
    cut" + "A1/A4/A7", and the four record fields "candidate children",
    "evidence", "remaining uncertainty", "revisit".
  - `test_references_read_in_an_adopters_repo`:
    - every markdown link target in the template is `README.md`;
    - the template holds no record-id regex match and no `docs/plans/`;
    - each `process.md §N "…"` quote occurs in that § of
      `project-trajectory/PROCESS.md`, and each `prompts/spine-questions.md`
      §3 and `process-options.md` quote occurs in its file;
    - `docs/process.md`, `docs/process-options.md` and
      `prompts/spine-questions.md` are MAPPING destinations, so the prose
      names paths an adopter has.
  - `test_the_manifest_seeds_it_once_with_its_purpose`: `mapping_entries()`
    holds `("rubrics/architecture-decomposition.template.md",
    "docs/rubrics/architecture-decomposition.md", "SR-186")`. This is the
    in-process pin of the scaffold destination; `test_bootstrap` is slow.
- `test_dogfood_sync.py::test_dogfooded_boilerplate_matches_template[docs/rubrics/architecture-decomposition.md-…]`
  (new parametrize case). *Fails before:* both files are missing.
- `test_bootstrap.py::test_scaffold_contains_expected_files` (slow; run in P7).
  *Fails before:* the scaffold lacks the destination.
- `test_profile.py::test_default_scaffold_is_fully_green_including_warnings`
  (existing, slow) is the guard for the README sentence. Without it, the
  orphan WARN reds this test.

## P2 — The skill

**Files.**

- New `project-trajectory/skills/architecture-decomposition/SKILL.md`.
  Frontmatter, in the house shape (`deep-module-design` is the model):
  - `name: architecture-decomposition`
  - `description:` a "Use when …" sentence that triggers on **planning a
    work item** (answering its architectural-delta question) and on
    **`DevStg-Arch`** (breaking down a component scope), and names the four
    steps. It must be at least `DESCRIPTION_FLOOR` (100) characters.
  - `stacks: [any]`, `domains: [any]`, `phases: [dev, gate]`
  - `tags: [architecture, decomposition, interfaces, components, planning]`
  - `scope: kit`

  `[any]`/`[any]` makes `bootstrap.select_skills` pick it for every
  scaffold, so every `--agents` choice materializes it. P5 relies on that.
- Body: **When to use** (the two moments plus an audit), then a four-step
  **Procedure**. Each step cites the rubric's anchor ids and the rubric path
  `docs/rubrics/architecture-decomposition.md`, and restates no anchor:
  1. **Name the mode classes** (A2). Record them, with their transitions, as
     the scope's state flow in `docs/runtime-flows.md`.
  2. **State each boundary's value domain** (A3, A6). Record it in the
     boundary interface row's form in `docs/requirements/interfaces.toml`.
  3. **Tabulate output against input dependencies** (A4). Record the table
     beside the scope's flow in `docs/runtime-flows.md`, or, when planning,
     in the plan.
  4. **Apply A8's two descent tests**: requirement descent for obligations,
     and component descent after comparing candidate cuts under A1, A4 and
     A7. Record the result in the existing scoped decomposition or review
     record (process-options.md "(d2)"). Where the component layer keeps one,
     that is the component registry's partition record.

  Then a **When planning a work item** paragraph. Each step's result answers
  one clause of the delta question: a new mode class or transition is "add a
  state", a new case in a domain is "add a value", a new table cell is "a new
  input", a new boundary interface is "cross a new boundary". The plan writes
  its `DELTA:` line from them, and carries a `within` change as rows. Add one
  sentence saying each output goes **only to a home that already exists**,
  never a new file or field. A pointer to the **`deep-module-design`** skill
  covers the code level below a component's boundary. The body names no
  record id of this repo.
- Regenerate `project-trajectory/skills/INDEX.csv` with
  `python project-trajectory/scripts/gen_skills_index.py`.
- Byte-copy the skill directory to `.claude/skills/architecture-decomposition/`
  and `.agents/skills/architecture-decomposition/` with a plain byte copy.
  **Not** `bootstrap.py --agents`: that would also materialize every other
  matching `scope: kit` skill this repo deliberately does not carry. Also not
  `--sync`, which refreshes only skills already present. Then
  `gen_skills_index.py --check-agents` must be clean.

**Tests added.**

- `tests/test_skills_index.py::test_architecture_decomposition_skill_walks_four_steps_and_cites_the_rubric`,
  in the shape of the existing `gate-advance` and `downstream-resync` pins:
  - frontmatter `scope == "kit"`, and the description contains "planning a
    work item" and "DevStg-Arch";
  - the body cites `docs/rubrics/architecture-decomposition.md`, A2, A3, A4
    and A8, and `deep-module-design`, and names `docs/runtime-flows.md` and
    `docs/requirements/interfaces.toml` as its homes;
  - **no restatement:** for every `**A# — <title>.**` head in the rubric
    template, `<title>` is not in the body, and neither is any of A8's four
    test labels ("A describable state", "An invented number", "A paraphrase",
    "No pass/fail of its own");
  - no record-id regex match in the body;
  - `architecture-decomposition` is among `bootstrap.select_skills(None, None, False)`'s
    names.

  *Fails before:* the file is absent.
- Existing tests that now cover the new skill:
  `test_every_skill_frontmatter_is_valid`, `test_index_row_count_matches_skill_dirs`
  and `test_every_shipped_description_clears_the_floor`. The last one reds
  for a description under 100 characters.

## P3 — `spine-questions.md` §4

**File.** `project-trajectory/prompts/spine-questions.md`: append after §3,
with §0–§3 untouched:

```
## 4. At DevStg-Arch — a component scope's decomposition
<!-- tiers: LLR -->

- **Judge the scope's decomposition against `docs/rubrics/architecture-decomposition.md`**, citing its anchor ids; this section restates none of them.
```

The bullet is one physical line, the "single line" D7 asks for. The tier is
`LLR` because `DevStg-Arch` has no approval act of its own. The first LLR
sitting at a scope is the act its output feeds (item 12, "When the critique
runs"). Add one maintainer-note sentence in the stripped header saying so.
Then regenerate `project-trajectory/prompts/CATALOG.md` with
`python project-trajectory/scripts/gen_prompt_catalog.py`, because the
fragment digest changes.

**Tests (amended; each fails before).**

- `tests/test_adjudicate_brief.py`:
  - Add `_ARCH_HEAD = "## 4. At DevStg-Arch"` to `_heads`.
  - The first-approval (LLR) and combined-section tests now expect
    `[_EVERY_HEAD, _LLR_HEAD, _ARCH_HEAD]`.
  - The amendment test keeps `[_EVERY_HEAD, _SR_HEAD]` and
    `[_EVERY_HEAD, _SN_HEAD]`, so §4 is shown absent from SR and SN briefs.
  - *Fails before:* the LLR brief has no §4.
- `tests/test_prompts.py::test_the_arch_section_points_at_the_rubric_and_restates_nothing`
  (new):
  - the home's `## ` heads, in order, start `## 0.`, `## 1.`, `## 2.`,
    `## 3.`, `## 4.`, so sections 0–3 keep their numbers;
  - §4's tiers line is exactly `<!-- tiers: LLR -->`;
  - its body has exactly one non-blank line, and that line names
    `docs/rubrics/architecture-decomposition.md`;
  - `adjudicate_brief.tier_questions({"LLR"})` contains it and
    `tier_questions({"SR"})` does not.
- The existing catalogue freshness step (`gen_prompt_catalog.py --check`)
  reds until the catalogue is regenerated.

## P4 — This repo's plan and scope rubrics

**Files.**

- `docs/rubrics/plan-decomposition.md`: after `**G4 — Coherent DAG.**`, add
  `**G5 — The delta answer holds against the shared rubric.**`. It judges a
  single plan's `DELTA:` line against
  `[architecture-decomposition](architecture-decomposition.md)`. Each of
  these is a G5 finding, citing the rubric anchor it rests on:
  - a `none` that a row contradicts: the row adds a mode class (A2), a
    domain case (A3), a dependency cell (A4) or a boundary interface (A6);
  - a `within` whose rows do not carry the interface and domain edits;
  - a `beyond` that plans around the refactor.

  The planner's procedure is the `architecture-decomposition` skill. The
  "Second use: a single plan" paragraph and its delta sentence stay
  byte-for-byte.
- `docs/rubrics/scope-critique.md` S5: the existing three sentences stay
  verbatim. Append one sentence: "Judge the answer against
  `[architecture-decomposition](architecture-decomposition.md)`; the
  `architecture-decomposition` skill is the author's procedure for it."

**Tests.**

- `tests/test_review_brief.py::test_the_scope_rubric_names_every_registry_the_critique_brief_renders`
  (extended):
  - the S5 slice (`**S5 —` to `**S6 —`) contains the original question
    verbatim, from "Does the WI add a state" to "filed on trunk before the
    claim.";
  - it also contains `](architecture-decomposition.md)` and
    "`architecture-decomposition` skill".

  *Fails before:* no pointer.
- `tests/test_plan_pass.py::test_the_plan_rubric_judges_the_delta_line_against_the_shared_rubric`
  (new):
  - `docs/rubrics/plan-decomposition.md` has a `**G5 —` head whose slice
    links `architecture-decomposition.md` and names `DELTA:`;
  - the existing sentence "does the work item add a state, add a value to a
    domain, make an output depend on a new input, or cross a new boundary,
    and if so does the plan carry the change within its scope?" is still
    present (whitespace-flattened).

  *Fails before:* no G5.

## P5 — The single-plan brief names the skill

**File.** `project-trajectory/prompts/plan-single.template.md`: one new line
directly after the "THE ARCHITECTURAL-DELTA QUESTION. Answer it …" paragraph,
before its two outcome bullets. The question's wording is untouched. The
line names the skill by the path each agent's copy has:

> Answer it by following the `architecture-decomposition` skill: `.claude/skills/architecture-decomposition/SKILL.md`, or the same file under `.agents/skills/` or `.gemini/skills/` for your agent.

- The line has no braces, so `prompts.fill`'s seven slots are unchanged.
- It names no record id.
- The `.claude/` and `.agents/` paths both resolve in this repo after P2.
  In a scaffold, the selected agent's directory holds the copy, because P2
  makes `select_skills` choose the skill for every scope.
- Extend the dispatcher note "DO NOT RE-WRAP the delta question" with one
  clause saying the skill line beside it is pinned too.
- Regenerate `prompts/CATALOG.md`: the PLAN-SINGLE digest changes.

**Tests.**

- `tests/test_plan_pass.py::test_the_shipped_planner_template_names_no_skill_and_no_row_of_this_repo`
  is **amended** and renamed
  `…_names_the_architecture_skill_by_its_agent_paths_and_no_row_of_this_repo`.
  - Drop `assert "skill" not in raw.lower()`. WI-913's spec states the
    reason it was written: "It names no skill: item 12's text lane (P6) adds
    that one line." This item is that lane.
  - In its place, assert that `architecture-decomposition/SKILL.md` and
    every `skills_dir` in `bootstrap.AGENTS` appear in the raw template.
  - Assert that the skill line falls after the `DELTA_QUESTION` text and
    before `DELTA: none`.
  - Assert that `ROOT / ".claude/skills/architecture-decomposition/SKILL.md"`
    exists.
  - Keep the existing `DELTA_QUESTION` and no-record-id assertions.

  *Fails before:* no skill is named.
- `test_the_planner_brief_carries_the_clauses_the_contract_and_the_delta_question`
  gains `assert "architecture-decomposition/SKILL.md" in text`, so the
  rendered brief carries the line. Its `DELTA_QUESTION` pin is unchanged and
  must still pass. So must the revision-mode test's.
- `test_the_planner_template_is_in_the_generated_catalogue` and the
  `prompt-catalog` freshness step hold after regeneration.

## P6 — The RESYNC entry

**File.** `project-trajectory/RESYNC_PACK.md`: one entry, appended as the
last `###` before `## 5. Promotion`, so the landing-order test holds. The
heading is
`### The architecture-decomposition rubric and skill, and pointers to them [since <base>]`,
where `<base>` is the lane's trunk base: the `git merge-base` of `HEAD` and
the trunk named in `docs/process.toml` `[policies] trunk`, abbreviated like
its neighbours. Then the standard "*(Anchored at the preceding commit …)*"
line. If the lane is rebased before landing, re-anchor it.

- **What changed:** the seeded rubric; the kit skill; `spine-questions.md`
  §4 (composed into LLR briefs); the single-plan brief's skill line; the
  one-sentence link in the rubric README template.
- **What to do**, one bullet per D12–D16, plus the two mechanical steps:
  - D12: a plain add-only `bootstrap.py --dest .` re-run seeds
    `docs/rubrics/architecture-decomposition.md`, which is yours from then
    on. Add the README template's one-sentence link to your own
    `docs/rubrics/README.md`, or check_docs reports the new rubric as an
    orphan.
  - D13: `bootstrap.py --dest . --agents <yours>` materializes the skill.
    (`--sync` refreshes only skills you already carry.)
  - D14: `prompts/plan-single.template.md` and `prompts/spine-questions.md`
    are kit-owned and are overwritten. Then run
    `python scripts/gen_prompt_catalog.py` (§1.3 step 3).
  - D15: if you keep your own scope or plan rubric, you may add the two
    pointers (S5-style and G5-style) in your own words.
  - D16: nothing migrates. No setting, registry or check changes.
- **Kit-owned files — overwrite:** `scripts/kitlib/bootstrap_manifest.py`,
  `prompts/plan-single.template.md`, `prompts/spine-questions.md`,
  `prompts/CATALOG.md` (regenerate) and `skills/INDEX.csv` (regenerate).

**Tests.** None added. The instruments are `scripts/check_resync.py`, which
is in the commit bar and refuses this change without an entry anchored at
the base (it fails before P6), and `tests/test_resync_pack.py`: the anchor
grammar, a real commit, landing order, and no `Reserved:` heading left.

## P7 — Verification on the landing tip

Run in the foreground, in batches under the 10-minute tool cap, and paste
the real output:

1. `run.cmd smoke` (or `python project-trajectory/scripts/run_menu.py smoke`)
   must be green. It includes `trace.py --strict`, `check_trajectory.py --strict`,
   `check_docs.py --root . --stale`, `check_resync.py` and the smoke tier,
   which holds the new and amended in-process tests. Also run
   `python project-trajectory/scripts/trace.py --strict` and
   `python project-trajectory/scripts/check_trajectory.py --strict` on their
   own on the landing tip (D17).
2. `python project-trajectory/scripts/gen_skills_index.py --check`, then
   `… --check-agents`, then `python project-trajectory/scripts/gen_prompt_catalog.py --check`.
   All must be clean.
3. `python project-trajectory/scripts/check_doc_refs.py --strict`: no
   dangling reference. `prompts/spine-questions.md` in the seeded copy reads
   as kit-relative and untraced, not dangling.
4. The slow modules this item touches, by name:
   `python -m pytest -q tests/test_bootstrap.py tests/test_profile.py tests/test_dual_plan_round.py`.
   The last one writes a plan-decomposition rubric fixture, so it is a
   regression check only.
5. TC-166, unchanged: `python -m pytest -q tests/test_components_registry.py`.
6. A temp scaffold **outside the repo**:
   - `python project-trajectory/scripts/bootstrap.py --dest <tmp> --agents claude,codex`;
   - confirm `<tmp>/docs/rubrics/architecture-decomposition.md`,
     `<tmp>/.claude/skills/architecture-decomposition/SKILL.md` and
     `<tmp>/.agents/skills/architecture-decomposition/SKILL.md` exist;
   - `python scripts/check_docs.py --ignore docs/test/report.md` in `<tmp>`
     prints no WARN and no FAIL (re-checking P1's D4 in a real scaffold,
     and the orphan guard);
   - the plan-single path named for each agent resolves there.
7. Smoke membership: `python -m pytest -m smoke --collect-only -q`. Its
   count stays under `[smoke-budget] max-tests`; P1, P2 and P3 add about
   eight in-process tests.

## Found on the way (surfaced, not fixed here)

- `project-trajectory/skills/spine-authoring/SKILL.md` §"1–3" lists the
  home's sections as "§0 … §1 … §2 … §3 at LLR and TC". After P3 that list
  omits §4. Changing it touches a further shipped skill and its two copies,
  outside this item's file list. The coordinator should decide: a one-clause
  follow-up, or accept that the list is not exhaustive.
- `docs/rubrics/plan-decomposition.md`'s first three anchor ids read
  `DevStg-Reqs`, `DevStg-Tests` and `DevStg-Impl` where `G1`–`G3` belong,
  next to `G4` (the arbiter example cites "anchored DevStg-Tests"). The
  shipped `rubrics/README.template.md` likewise says "Numbered good anchors
  (`DevStg-Reqs`, `DevStg-Tests`, …)". Both look like damage from a global
  rename. P4's new anchor is named `G5` to follow G4. The repair is its own
  row.
