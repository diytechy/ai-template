+++
id = "WI-1017"
title = "The guidance says an LLR yields to a sustainable design: it may be split, merged, moved or retired"
workstream = "docs"
sr_refs = ["SR-186"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 2
planmode = "single"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1017`, cut from `refactor_again` at
`0d67302bd`, with the commit hooks on. The sample landed first, in the plan's
commit, and the guidance in the commit after it. Review: pending (the
coordinator). The specref
(`docs/plans/2026-11-11-test-tiers/HANDOFF.md`, §12.6) is cleared at close,
as a terminal row's is.

- `3d6ad6fe1`: the plan, `docs/plans/WI-1017/plan.md`, written from the
  sample and committed alone.
- `d1d221c82`: the guidance, the pin test, the RESYNC entry, the decisions
  record and the regenerated views.

### The evidence sample (Done-when 1)

**How the sample was chosen.** No case was picked by hand:

- Every entry naming an LLR or a design row in the decisions records of the
  thirteen most recent lanes that kept one (`docs/decisions/wi-971.toml`
  to `wi-997.toml`): 92 of their 145 entries.
  <!-- fig: cmd="tomllib over docs/decisions/wi-9[6-9]*.toml (wi-971 on), entries whose fields match \bLLR\b|LLR-\d+|design row" rev=0d67302bd -->
  Each was classed as a design fitted to a row (A), a row kept after the
  design moved (B), rows reshaped with the design (C), or no bearing (D).
  Entries 1 to 53 (wi-971 to wi-979) were classed by a delegated reader and
  each A and B case it reported was re-read here; entries 54 to 92 were
  classed here.
- The Deliverables of the thirteen rows built on maintenance branches since
  (WI-999 to WI-1011), which kept no decisions record.
- The 136 review verdicts of lanes wi-960 to wi-1002; 44 answer the reviewer
  brief's change-intake question by name.
  <!-- fig: cmd="ls docs/reviews/wi-9[6-9]*/*REVIEW*.md docs/reviews/wi-100*/*REVIEW*.md | wc -l; grep -l -i unsuitable over the same files | wc -l" rev=0d67302bd -->
- The two most recent handbacks (WI-828, WI-902), every LLR retirement record
  (four), WI-1015's measurement (`docs/reviews/2026-11-21-code-vs-interfaces/`),
  and one count of symbol accretion over the live LLRs.

**What it found.** The concern holds in one form. No lane changed a behaviour
to satisfy an LLR's text, and lanes did reshape rows with their design (C
below). But when the design changed shape the row set did not, and row text
was left trailing the code at the end of a lane. Of the 92 entries: 2 A, 8 B,
27 C, 55 D; the maintenance rows add one A, two B and seven C.

**A: a design fitted to the rows that exist.**

| Case | Lane | What happened | What kept the row set |
|---|---|---|---|
| A1 | WI-1007 (maint) | `trajectory_arch.py` split into five modules, and no design row minted: "a new `Drafted` row under SR-159 would be design written for a refactor". Three checks no design row binds were placed beside a bound rule rather than in modules of their own, and "one check per module" was left undone because each "needs ... a design row binding the two that have none". LLR-375 to LLR-380 were allotted and not used. | The reading that a refactor never changes the row set (§5's chart offered only rows on the existing modules; the spine questions say a refactor keeps a row true); the containment rule (a module joins a component only through a design row naming it); and the five allotted interface ids, read as a ceiling ("so the split makes at most five new modules"). |
| A2 | wi-996 D-009 | Four integrator functions tagged `LLR-368` but missing from its `code_symbol` dropped that back-link and stayed under LLR-207, "so no judged row changed". | The sitting's verdict binding the set: changing a judged row would have owed a re-sitting. Medium confidence: the functions are also LLR-207's. |
| A3 | wi-976 D-005 | A confirmed finding held because its remedy would change "LLR-360's ruled text and the spec's Done-when"; sent to a successor. | The spec's named surface and LLR-360's spec-given text. Low confidence: LLR-360 was `Drafted`, and was amended toward the better contract in the same lane (D-011). |

wi-971 D-001 states the same reading as A1 without a case: a refactor's plan
"edits traced registry cells only ... so no spine row is authored".

**B: a row kept after the design moved.**

| Case | Lane | The row | What kept it | Now |
|---|---|---|---|---|
| B1 | wi-976 D-021 | LLR-273's `module` names `adjudicate_brief.py`, which holds none of its symbols | The rule that a MINOR after the gate never moves the gated tip | Unchanged |
| B2 | wi-977 D-023 | LLR-150 says specs "moved out of `active/<branch>/`", from before one-item lanes; LLR-149 repeats a sentence | "amending a blessed row's text now would reopen its sitting", and the post-gate rule | LLR-150 unchanged |
| B3 | wi-977 D-025 | LLR-123's rationale still says "traincars" | The post-gate rule | Unchanged |
| B4 | wi-978 D-021 | LLR-362 says a fold keeps every space's maximum, where the carrier contributes only reservation-backed marks | The post-gate rule | Unchanged |
| B5 | wi-987 D-005 | LLR-118 listed the page's section 2 as SR chains only | The post-gate rule | Amended by WI-1010 |
| B6 | wi-993 D-009 | LLR-153 labels its new trigger "(d)" where its module says "(f)" | The post-gate rule ("would move a blessed cell after the gate") | Unchanged |
| B7 | wi-977 D-024 | LLR-312 lists `_the_one_claimed_spec` for a rule its detail does not state; two stale symbols elsewhere | The spec's named set of rows; traced-only cells owe no sitting | Unchanged |
| B8 | wi-977 D-014 | LLR-208's batch-era justification ("one review scope") | The spec's "unchanged on purpose" list (low confidence: the spec argues it stays true) | Unchanged |
| B9 | WI-1007 (maint) | LLR-172's detail and TC-166's method name `trajectory_arch.component_findings` after the move | "The name still resolves through the composer, so neither accepted row was amended": the accepted rows' amendment and re-acceptance avoided | Unchanged |
| B10 | WI-1001 (maint) | No LLR states the rule that an accepted automated TC no tag names is a finding; TC-428 and TC-429 verify SR-157 directly | "Whether LLR-366 is amended, or an LLR minted, is the operator's call": the builder stopped at the accepted row, as its instructions said | Unchanged |

**C: rows reshaped with the design (the counter-evidence).** 27 entries:
wi-976 (LLR-297 retired, LLR-360 minted and restated, LLR-167 and LLR-273
amended), wi-977 (the batch-to-single rewrite of LLR-058, -061, -123, -144,
-149 to -152, -161 and -207), wi-978 (LLR-362 and LLR-363 minted, split into
allocation and landing, restated), wi-982 D-004 and D-006 (LLR-360), wi-987
D-003 and D-004 (LLR-271), wi-993 D-007 (LLR-153), wi-994 D-004 (LLR-365),
wi-995 D-005, wi-996 D-006 (LLR-368, LLR-207) and wi-997 D-011 (LLR-365,
LLR-366). Seven maintenance rows: WI-1003 (LLR-374), WI-1004 (LLR-382 to
LLR-388, one per new home), WI-1005 (LLR-373), WI-1006 (LLR-370), WI-1009
and WI-1010 (LLR-118, LLR-283), WI-1011 (LLR-372). One lane paid for a
retirement: wi-976 stopped a leg and re-sat its set twice rather than keep
LLR-297.

**The other sources.**

- *Review verdicts.* Six of the 44 answers found a row unsuitable (wi-960
  LLR-269, wi-961 LLR-347, wi-963 LLR-364, wi-978 LLR-363, wi-993 LLR-153,
  wi-997 LLR-365), and each named that row's amendment as the remedy; none
  found a workaround kept for a row. The question as asked reaches one row's
  mechanism, never how the rows divide the design.
- *Retirements.* All four LLR retirement records (LLR-015, -237, -289, -297)
  follow a ruling that dropped a feature; none is a re-cut.
- *Accretion.* 48 of 345 live LLRs list more than ten symbols and 18 more than
  twenty; 62 span three or more modules (LLR-270: 80 symbols over six modules;
  LLR-336: 68 over ten).
  <!-- fig: cmd="tomllib over docs/requirements/low-level-requirements.toml [design], code_symbol split on / ; , and space, module split on ; and ," rev=0d67302bd -->
- *WI-1015's measurement.* 7 symbols LLRs name exist nowhere and 3 have moved;
  about 25 `code_symbol` cells hold prose.
- *Handbacks.* Neither WI-828 nor WI-902 bears on an LLR.

### The causes, and what changed (Done-when 2 to 5)

The sample found cases, so each named cause inside the guidance is changed
here:

1. **§5's change intake had no re-cut** (A1, wi-971 D-001). PROCESS.md §5
   now states once: "an LLR records the current design, not a commitment";
   when a sustainable design needs a different decomposition the LLRs are
   split, merged, moved or retired (`retire.py`) under their tier's acceptance
   authority, never the design bent to fit them; the parent SR keeps its
   acceptance and the enduring regression tests and parent constraints stay;
   one row's mechanism at fault is that row's amendment; moving code that
   keeps every row's stated behavior moves trace cells only, while a design
   that divides the behavior differently re-cuts the rows; keeping an
   unsuitable row, or bending the design to fit it, to avoid an acceptance act
   is a finding. The chart gains `RD` (split / merge / move / retire),
   reached from a violated row ("parent sound; design re-cut") and from a new
   scope's solution ("existing LLRs do not fit"). § numbering is unchanged.
2. **"Keep IDs where meaning remains" was silent on the other case.** The
   skill now says: where it does not, mint and retire as `docs/process.md` §4
   ("Keep or mint") and §5's design replacement say.
3. **The spine questions read a refactor as never changing the row set** (A1).
   §3's design-replacement bullet now covers "the way the rows divide the
   design" and routes it to §5 instead of restating §5's amendment route; the
   in-lane reference has a lane's change set include each LLR the design
   re-cuts.
4. **The builder tagged new code by file** (accretion; B10's stop). The
   builder agent tags a new function with the LLR whose stated behavior it
   implements (that LLR's `module` naming the file), and reports a row that no
   longer fits the design with the re-cut §5 calls for, never fitting the
   design to it; rubric K3 follows.

The readers point at the statement and restate none of it (Done-when 4):

| Reader | Where it lives |
|---|---|
| The spine-authoring skill | `project-trajectory/skills/spine-authoring/SKILL.md` and `references/in-lane.md`, with their `.claude/skills/` and `.agents/skills/` copies; its question home `project-trajectory/prompts/spine-questions.md` §3, which `adjudicate_brief.py` composes into every LLR sitting |
| The builder's instructions | `project-trajectory/prompts/worker.template.md` (the shipped worker brief) and `.claude/agents/kit-builder.md` (this repository's builder agent) |
| The reviewer prompts | `project-trajectory/prompts/reviewer.template.md` (the shipped reviewer brief; it dropped the sentence restating §5's preservation clauses) and `docs/rubrics/kit-change-review.md` K3 (the rubric `review_brief.py review --rubric` appends here) |
| The scope-critique prompt | `docs/rubrics/scope-critique.md` S5, rendered by `review_brief.py critique` into `prompts/critique.template.md`: a change that re-cuts the design names the LLRs it splits, merges, moves or retires |

Done-when 5: nothing in these homes now rewards keeping an unsuitable LLR to
avoid an acceptance act. The statement makes it a finding, the chart offers
the re-cut where it offered only rows on the existing modules, "keep IDs"
says what to do when meaning does not remain, and the builder no longer grows
the row that owns a file.

Checked against the rulings the statement must not contradict: SR-186
(accepted, not amended: a re-cut keeps each child's independent purpose);
§4's keep-or-mint rule; the review-churn plan's variant F (ruled, unbuilt: a
refactor moves traced cells and never reopens a requirement row, which
"moves trace cells only" keeps); and the operator's ruling of 2026-11-19 that
"architectural changes are permitted to keep code clean and modular".

**Causes outside the guidance: rows to file, not built here.**
(`docs/decisions/maint-wi-1017.toml` D-001 reads the coordinator's procedure
as outside this row's homes.)

1. **Row text a lane leaves stale is never filed.** The rule that a MINOR
   after the gate never moves the gated tip (`coordinator-cycle` recipes §3,
   wi-935 D-005) and the cost of re-sitting or re-accepting a row send an
   LLR's stale text to status.md's unfiled follow-ups or to nowhere (B1 to
   B9); only B5 has been fixed since. A row to file: such a follow-up is filed
   as a queued row, or rides the next lane that touches the row, so it cannot
   lapse. Its first set: LLR-273's `module`, LLR-150, LLR-123's rationale,
   LLR-362, LLR-153's label, LLR-312, and LLR-172 with TC-166.
2. **WI-1001's rule has no LLR** (B10). A row to file: amend LLR-366 or mint
   an LLR under SR-157 stating that an accepted automated TC no tag names is a
   finding (the operator's acceptance).
3. **Accepted rows are amended only by addition** (`coordinator-cycle`
   recipes, "Brief Terra to amend an accepted row by addition"). It guards
   against lost obligations, and it makes accepted rows grow (wi-977's 008 F6:
   LLR-149 repeats a sentence) where a re-cut would retire and mint. One case
   in the sample; a row to file only if the coordinator judges it worth one:
   the recipe names §5's re-cut as the alternative to appending.
4. **A module joins a component only through a design row naming it** (A1).
   Not a new row: variant F's placement on the realization removes that
   binding, and review-churn phase 3 still needs its rows (HANDOFF §12.6).

### Tests

- The pin, `tests/test_prompts.py::test_the_design_replacement_rule_has_one_home_and_every_reader_points_at_it`:
  red on the base text (the statement absent from PROCESS.md), green after.
  It rides the module's file-level tag (D-002: no spine row minted; LLR-396
  to LLR-398, TC-460 to TC-463 and IF-327 to IF-328 unused).
- The modules the change reaches, at `-n 2`: `test_prompts`,
  `test_prompts_driven`, `test_agent_loop_worker` (the golden worker prompt,
  updated), `test_agent_loop_review`, `test_review_brief`,
  `test_routing_and_prompts`, `test_adjudicate_brief`, `test_hats`,
  `test_skills_sync`, `test_dogfood_sync`,
  `test_architecture_decomposition_rubric`, `test_held_rung_doctrine`,
  `test_language_neutral_scheme`, `test_status_vocabulary_contract`,
  `test_gen_cases`, `test_spec_move`, `test_plan_filing`, `test_import_layers`,
  `test_module_size_ratchet`: `658 passed, 1 skipped in 404.37s (0:06:44)`.
  `test_bootstrap.py -k "byte_caps or size_budget or baselines"`:
  `3 passed in 11.78s`.
- `check_trajectory.py --strict`: clean; `trace.py --strict`: `orphans=0
  integrity=0`; `check_doc_refs.py`: 229 dangling, as at the base. Both
  commits passed the hook.

### Byte deltas

- `project-trajectory/PROCESS.md` 100,990 -> 101,691 (+701, watched: §5's
  statement and the chart's re-cut), re-stamped in `byte-budget-guard`.
- `project-trajectory/skills/byte-budget-guard/SKILL.md` 4,613 -> 4,610
  (390 under its 5,000 cap).
- `project-trajectory/skills/spine-authoring/SKILL.md` 19,630 -> 19,744
  (+114, uncapped); `references/in-lane.md` 5,135 -> 5,212 (+77).
- `project-trajectory/prompts/spine-questions.md` 21,623 -> 21,532 (-91);
  `reviewer.template.md` 12,058 -> 11,927 (-131); `worker.template.md`
  8,901 -> 8,935 (+34).
- `AGENTS.template.md` (9,964), `CLAUDE.md` (8,052) and `PROCESS_OPTIONS.md`
  untouched.

Left undone: the four rows above, named and not filed; the review.

## Context

Filed by hand on 2026-11-21 at the operator's direction. The operator's
concern, stated as speculation: the tooling works to maintain LLRs rather
than toward a sustainable design, which will sometimes need redesign.

What the guidance says today:

- PROCESS.md §5's change intake has a branch for it ("parent sound; LLR
  unsuitable" → amend the LLR and its verification, keep the parent's
  acceptance), and the reviewer prompt asks whether a workaround preserves
  an unsuitable LLR.
- But the spine-authoring skill says "Keep IDs where meaning remains" and
  is silent on what happens when meaning does not remain; the chart's
  "code only" path adds LLR rows on the existing modules, with no branch
  for re-decomposing (splitting, merging, moving or retiring several LLRs
  when the design changes shape); and SR-186 asks each child for an
  independent purpose without mentioning re-decomposition.
- Only 4 LLRs have retirement records since the record began. Adding code
  under existing rows needs no act, while reshaping rows needs retirement
  records and re-acceptance, so the cheaper path keeps the rows.
- WI-1015's evidence (`docs/reviews/2026-11-21-code-vs-interfaces/`) shows
  LLRs trailing the code: 33 tags on functions their LLR does not name, and
  7 named symbols that no longer exist. The rows are being maintained after
  the fact rather than redesigned with the code.

## Done-when

- [x] First, check whether the concern holds: sample recent lanes (decisions
      records, review verdicts, handbacks) for a design bent to fit an
      existing LLR, or an LLR kept when the design had changed. Record what
      was found in this row's Deliverable, each case with its lane and what
      kept the row. The sample lands first, in the same branch as the
      guidance; it is one deliverable with it.
- [x] The guidance items below land whatever the sample finds, because
      the gaps they close are in the text today (the silent "keep IDs" rule,
      the chart with no re-decomposition branch). The sample sets only how
      far the last item goes: with no case found, it is met by the statement
      and the pointers; with cases found, each named cause in the guidance
      is changed here, and a cause outside the guidance (a tool's cost, an
      act's cost) is filed as its own row rather than built in this one.
- [x] PROCESS.md §5 states once that an LLR records the current design, not
      a commitment. When a sustainable design needs a different
      decomposition, LLRs are split, merged, moved or retired (`retire.py`)
      under their tier's acceptance authority, keeping the parent SR's
      acceptance and the enduring regression tests. The change-intake chart
      gains that branch.
- [x] The spine-authoring skill, the builder's instructions and the
      scope-critique and reviewer prompts point at that statement instead of
      restating it, and "keep IDs where meaning remains" says what to do when
      it does not.
- [x] Nothing in the guidance rewards keeping an unsuitable LLR to avoid an
      acceptance act.

## Critique dispositions

Round 1 (OpenAI Sol, low, 2026-11-21; Gemini Argon timed out on the wave's
first two rows, so Sol reviewed alone;
`docs/reviews/2026-11-21-scope-critiques/WI-1017.md`): CHANGES-REQUESTED,
two findings.

- **S1 (MAJOR), the deliverable depends on the sample with no outcome
  stated: adopted.** The first Done-when item makes the sample and the
  guidance one deliverable, landing sample first. A new second item states
  that the guidance items land whatever the sample finds, since the gaps
  they close are in the text today, and that the sample sets only how far
  the last item goes; a cause outside the guidance is filed as its own row
  (S7).
- **S4 (MAJOR), `planmode` missing: adopted as `planmode = "single"`.** The
  changes reach PROCESS.md §5, a skill and prompts that scripts render, and
  depend on what the sample finds, so the plan follows the sample and
  precedes the edits (`docs/plans/WI-1017/plan.md`).
