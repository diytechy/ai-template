+++
id = "WI-979"
title = "Architectural decomposition, text: the shared rubric with the W3 dry run's five clarifications and the requirement-versus-component descent split, the architecture-decomposition skill, and four one-line pointers to them"
workstream = "process"
sr_refs = ["SR-186", "SR-165"]
specref = "docs/plans/2026-10-11-review-churn/README.md#12-architectural-decomposition-encouraged-at-three-moments"
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
+++

## Context

This row is the text half of the review-churn plan's item 12, filed as the
queue's P6 from the W3 dry-run record
(`docs/plans/2026-10-11-review-churn/w3-dry-run/README.md`). The rubric
draft (`rubric-draft.md`, anchors A1 to A8, patterns B1 to B4) passed item
12's test. A cross-family critic used it to argue three candidate cuts of W3
from evidence and rejected a split along Flow 4's stages (`dry-run.md`).
This row ships the corrected rubric.

**Anchor.** SR-186 (Approved, "Proportionate requirement decomposition",
SN-012): each extra child carries an independent decision, and the stopping
decision is recorded. The rubric's A8 is the judgement behind that record.
SR-165 (Approved, SN-040): a component partition is explained by the
candidates it weighed. A7 judges that comparison. Neither row changes.
SR-146 (the prompt and fragment) and SR-112 (the skill copies) are touched,
not changed.

**The five clarifications** come from the dry run's "missing questions that
changed the answer". Each one clarifies anchors A4, A6, A7 or A8. None adds
a failure pattern:
1. the ownership or allocation model for a file that several components'
   rows name (one implementation owner, several obligation allocations, or a
   declared kernel role);
2. the invariants a cut must preserve: transaction scope, lock order,
   failure and retry ownership, durable effects;
3. the evidence that is enough for an audit versus a fresh design, with
   explicit "not supplied" and "not assessable" outcomes, and room for
   "insufficient evidence for approval";
4. the cost of enforceability and migration: access constraints, the
   boundary tests that establish them, and a migration plan wherever
   approved rows or tests would change;
5. what counts as one interface or one case: existing rows, new endpoint
   crossings, shared schema definitions and new semantic surfaces are each
   counted separately, and the unknown remainder is stated.

**The A8 distinction.** The four descend tests stop *requirement*
(obligation) descent. They give no cost-based stop for *component* descent.
A component can contain sub-decisions that are testable on their own and
still rightly stay one component, because a cut would cost more than the
isolation it buys. A8 therefore splits in two:
- tests 1 to 4 stay as the rule for obligations;
- a component leaf stops when no information-hiding cut pays its way after
  the A1/A4/A7 comparison. Its record names the candidate children, the
  evidence, the remaining uncertainty and what would trigger a revisit.

**Files touched** (shipped = kit-owned or kit-seeded):
- `project-trajectory/rubrics/architecture-decomposition.template.md` (new,
  shipped), plus one row in
  `project-trajectory/scripts/kitlib/bootstrap_manifest.py`'s MAPPING that
  seeds it to `docs/rubrics/architecture-decomposition.md`, the adopter's
  once seeded (as `docs/rubrics/README.md` is); this repo's copy is pinned
  in `tests/test_dogfood_sync.py`. Seeded, not under the skill directory, so
  an adopter with no agent skills still has the bar.
- `project-trajectory/skills/architecture-decomposition/SKILL.md` (new,
  shipped, `scope: kit`), the generated
  `project-trajectory/skills/INDEX.csv`, and this repo's copies under
  `.claude/skills/` and `.agents/skills/`.
- `project-trajectory/prompts/spine-questions.md` (shipped fragment),
  `project-trajectory/prompts/plan-single.template.md` (shipped), and the
  generated `prompts/CATALOG.md`.
- `docs/rubrics/scope-critique.md` and `docs/rubrics/plan-decomposition.md`
  (this repo's own; adopters keep their own if they have them).
- `project-trajectory/RESYNC_PACK.md` (one entry).

**Out of scope.** Item 12's builds, after item 11, in a later build row
filed on trunk:
- one `run.cmd audit` with its `arch` and `hats` parts, in the run-menu
  template;
- checks A and C;
- the depth-0 gate (the first LLR sitting refuses without a critique verdict
  for that scope);
- the critique at every second level and the whole-tree critique at
  DevStg-Tests entry.

Also out (not in P6's stated scope):
- the Architect role in PROCESS.md section 1 (ruled in revision 35);
- a matching line in `dual-plan-planner.template.md`;
- the dry run's other proposed anchor edits (A1, A2, A3, A5, B1 to B4);
- item 11's terms in the spine-authoring rubric.

## Scope answers

**S1.** There are six deliverables. Every one except the rubric cites the
rubric. They are kept as one row with one RESYNC entry, as the plan's
"Downstream" paragraph sets out. A pointer that lands before its target is a
broken link, so the order inside the row is: the rubric, then the skill,
then the four pointers.

**S2.** No file gains authority over a hold, an act or a gate: each is
guidance a critic or planner reads. The depth-0 gate that would give the
rubric authority is item 12's build. No `## Trust` section.

**S3.** The row makes no promise over an input space. The rubric's anchors
are a closed list. The new fragment section uses the existing tiers grammar
(the closed tier set), and the brief's composition rule does not change.

**S4.** `planmode = "single"`: the row touches two interface seams, the
skill directory (IF-035), where it adds a skill, and the scaffold mapping
(IF-262), where it adds a seeded destination, and the five rubric
clarifications and two descent rules are judgements no cheap check fully
specifies, so it plans in its lane first. Neither seam's form changes.

**S5.** None of the four. No state; no domain value (the seeded files and
the skill set are open member lists, not closed domains); no new input (the
briefs compose the same files); no new boundary.

**S6.** `needs` is empty: B1 (WI-911, S5) and the plan gate (WI-913, the
single-plan prompt) have landed, the dry run is recorded and F-call 6 is
ruled (revision 35). WI-976 (active, §2(c3)) and WI-978 (queued, §0) edit
other sections of `spine-questions.md`: a merge order, not an edge. No new
third-party dependency.

## Critique dispositions

Scope critique round 1 (Codex Sol at medium, 2026-10-25, headless leg 22;
CHANGES-REQUESTED, findings=1):

- F1 (MAJOR, S4 frontmatter and Scope answers): adopted — "planmode =
  \"single\"", and S4 now reads "the row touches two interface seams, the
  skill directory (IF-035), where it adds a skill, and the scaffold mapping
  (IF-262), where it adds a seeded destination ...". The deliverable scope
  is unchanged.

## Done-when

- [ ] `project-trajectory/rubrics/architecture-decomposition.template.md`
  holds the rubric, written from `rubric-draft.md`, and one MAPPING row
  seeds it to `docs/rubrics/architecture-decomposition.md`. This repo's copy
  is byte-identical and pinned in `BOILERPLATE_COPIES`. The scaffold test
  sees the new destination.
- [ ] The rubric's A4, A6, A7 and A8 carry the five clarifications above,
  each one findable in the anchor that asks it. No B pattern is added for
  them.
- [ ] The rubric's A8 separates requirement descent (tests 1 to 4) from
  component descent (no information-hiding cut pays its way after the
  A1/A4/A7 comparison), and its stopping record names the candidate
  children, the evidence, the remaining uncertainty and what would trigger a
  revisit.
- [ ] The rubric's references read correctly in an adopter's repo
  (`process.md` §N, `prompts/spine-questions.md` §3, its sibling
  `README.md`), and `check_docs` finds no broken link.
- [ ] `project-trajectory/skills/architecture-decomposition/SKILL.md` is
  `scope: kit` and walks four steps: name the mode classes, state each
  boundary's value domain, tabulate output against input dependencies, and
  apply A8's two descent tests. It records each output only in a home that
  already exists. It cites the rubric's anchors without restating them and
  points to `deep-module-design` for the code level. Its `description`
  triggers on planning a work item and on DevStg-Arch, and clears the
  description floor. `INDEX.csv` is regenerated.
- [ ] The skill is materialized into this repo's `.claude/skills/` and
  `.agents/skills/`, and `gen_skills_index.py --check-agents` is clean.
- [ ] `spine-questions.md` gains `## 4.` (DevStg-Arch) with an `LLR` tiers
  line and a single line that points the adjudicator at the rubric. Sections
  0 to 3 keep their numbers.
- [ ] `plan-decomposition.md` gains an anchor that judges the plan's
  `DELTA:` answer against the shared rubric, so a delta finding has an
  anchor id to cite. The existing delta paragraph keeps its wording.
- [ ] S5 in `scope-critique.md` gains one sentence pointing at the rubric
  and the skill. The question's own words are unchanged.
- [ ] `plan-single.template.md` gains one line beside the delta question
  naming the skill, by a path that resolves in this repo and in a scaffold
  with an agent selected. `test_plan_pass`'s `DELTA_QUESTION` pin holds, and
  `prompts/CATALOG.md` is regenerated.
- [ ] One RESYNC entry covers what an adopter does:
  - the add-only re-run seeds the rubric, which is theirs from then on;
  - `bootstrap.py --agents <yours>` materializes the skill;
  - `plan-single` and `spine-questions` are kit-owned and are overwritten;
  - an adopter with its own scope or plan rubric may add the pointers in its
    own words;
  - nothing migrates.
- [ ] `run.cmd smoke` is green, and `trace.py --strict` and
  `check_trajectory.py --strict` are clean on the landing tip.
