+++
id = "WI-976"
title = "The perspective-record sidecar retires and the 2026-09-06 SN-036 ruling applies here: an SN to SR round's sitting and author briefs carry the applicable hats' questions, and the sitting's verdict names each hat's outcome"
workstream = "process"
sr_refs = ["SR-161", "SR-186"]
specref = "docs/plans/2026-10-11-review-churn/README.md#14-retire-the-perspective-record-sidecar-apply-the-2026-09-06-hat-ruling-here"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
+++

## Context

Filed by hand in headless leg 19 (2026-10-25) from the review-churn plan's
item 14, the queue's row P3 (`docs/handoff-2026-10-11-attended-coordinator.md`):
"retire the perspective-record sidecar, the SN-036 ruling's four row acts,
the hat questions in the SN -> SR briefs. One sitting, one owner act.
Before item 5's migration and the FileBackup re-sync." A planner-drafter
read the plan's item 14 and its rulings and confirmed them against trunk at
`2695213c6`.

The rulings behind it: the owner's direction of 2026-10-13 (revision 21:
the 2026-09-06 SN-036 ruling stands); revision 22 (wire the hat questions
into the coordinator's briefs, and delete the existing sidecar); revision
23 (the hat block only for decomposition rounds); revision 24 (the hats
apply when a need is decomposed into SRs); revision 25 (SAFETY leaves this
repo's roster); revision 30 (SR-161's title, the slot grammar); revision 31
(`contract_split` is read only at its tip, `961f9e47`). The ruling's own
text is the 2026-09-06 fragment added at `f6c7360f`
(`docs/log.d/2026-09-06-sn036-owner-ruling.md` there); at the tip it is
folded into `contract_split`'s `docs/log.md`, under "2026-09-06 — SN-036 /
SR-161 owner ruling: review pass, not a guard", and closes: "Do NOT build
`hats_no_finding`, a sidecar record, or a coverage check."

**Anchor.** SR-161 (Approved), under SN-036 (Approved). SR-186, the other
SR that TC-211 verifies, does not change.

**What exists today (verified on trunk at filing).**

- The tool: the roster reader `project-trajectory/scripts/hats.py` has a
  `record` subcommand (its record section, its docstring and usage lines),
  tested by `tests/test_hats_record.py`; nothing outside these two files
  calls a record symbol, and no hook, CI workflow or `check.py` step runs
  it (warn-first).
- The rows: LLR-297 and TC-312 (both Approved); LLR-183's detail ("The
  machine-readable half of the perspective record" ... "the no-finding half
  is a per-decomposition artifact, built under LLR-297"); TC-211's `inputs`
  naming the sidecar; SR-161's requirement, acceptance and `coincident`
  asking for the record; SN-036's acceptance ("a machine-readable record",
  "a check reports"); IF-133's `data` cell listing `load`, which only the
  record's spine index calls.
- The instructions that ask for the record: PROCESS.md section 1's sentence
  "Each decomposition also leaves a perspective record beside it";
  `project-trajectory/prompts/spine-questions.md` (c3); the template
  roster's "THE PER-DECOMPOSITION RECORD" paragraph; this repo's roster's
  "WHAT IS NOT BUILT YET" paragraph; the RESYNC entry "The
  per-decomposition perspective record [since 9233772b]".
- The generated pages that show it: `docs/cli-reference.md`,
  `docs/requirements/components.derived.toml`, `docs/test/report.md`.

**What the plan's evidence missed (found at filing; each joins this row's
scope).**

- **Seven sidecars, not one.** Beside
  `docs/ai-template-redesign-2026-09-05-codex/DECOMPOSITION-AMENDMENTS.perspectives.toml`,
  the spine author wrote six between 2026-10-21 and 10-23, under
  `docs/plans/WI-850/` (two), `WI-957/`, `WI-958/`, `WI-960/` and `WI-961/`.
- **In practice it is a hold.** The coordinator recipe tells lanes to write
  the record "until plan item 14 retires the sidecar" (the
  `coordinator-cycle` recipes, three copies), and first-approval sittings
  have returned derived SRs for lacking one (wi-957 sitting 003, wi-958
  sitting 005, wi-960 sitting 005). No code gates on the record; a sitting
  reading (c3) and SR-161 does.
- **TC-211's rubric and procedure ask for it too:**
  `docs/rubrics/decomposition-proportionality.md` anchors R1 and B1, and
  `docs/test/inspection-procedures.md` (the proportionality procedure, its
  result section, still reading INCOMPLETE 2026-09-06 although the
  2026-10-03 pass is on record, and the closing paragraph of "Bounded
  abnormal inputs").
- **Removing SAFETY changes tests:** the roster tests pin one name list for
  both rosters and read SAFETY from the live roster, and the roster header
  counts "Sixteen hats today".
- **The coordinator's sittings are combined sittings,** composed section by
  section through each kind's assembler, so a slot in the two templates
  reaches them, and one sitting can compose both kinds.
- **The author prompt has no path for a computed block:** the coordinator's
  prompt filler only substitutes literal values, and the prompt tests pin
  the spine-author template's slot set.
- **An amended need is not reached today:** the planner briefs'
  applicability function reaches needs only through the row's SR-Refs and
  a SpecRef naming one SN, so a round that amends a need must pass that
  need in as a parent context.
- **Composed sitting briefs are not committed** (a lane commits only the
  verdict and its binding), while TC-211's procedure reads the sample's
  brief.
- **No `contract_split` wording exists for SR-161's `coincident` cell**
  (WI-655 added those cells here after the split), so that rewrite is this
  lane's own text.

**Deliverables and landing order (S1).** One row, kept whole on the owner's
direction ("one sitting, one owner act"), in this lane order:

1. The ruling record: a log fragment carrying the 2026-09-06 decision, its
   four acts and its closing line, citing `f6c7360f` and `contract_split`'s
   `docs/log.md` heading, plus the 2026-10-13 direction and the revision 25
   SAFETY ruling. SN-036's act cites this fragment directly, with no open
   item.
2. The spine change set, authored at the intent turn: SN-036, SR-161,
   LLR-183, TC-178 and TC-211 amended; LLR-297 and TC-312 retired; one new
   LLR under SR-161 and one TC for the sitting brief's hat block; IF-133's
   `data` cell amended.
3. The retirement: code, tests, records, instructions, generated pages, and
   SAFETY in this repo's roster.
4. The hat block in the two sitting templates' composition and in the
   spine-author prompt.
5. TC-211's re-judge against this lane's own checkpoint sitting, an SN to
   SR round (SN-036 is amended) and the first round to use deliverable 4.
6. SN-036's act, which is the owner's (Done-when, "The owner-held step").

Deliverables 3 to 5 hang from SR-161's amended text, which the one sitting
judges, and 5's sample is 4's first use. A split would add a second sitting
and, between its landings, leave Approved SR-161 asking for a record that
no longer exists, or stating a brief the coordinator's path does not
compose.

**Authority (S2).** No deliverable gives a file authority over a hold, an
act or a gate, so no `## Trust` section is owed: the retirement removes a
warn-first tool whose report was a sitting's reading, not a file's
authority; the hat block adds text to a brief whose outcome lines no code
reads (a missing outcome is a review finding, never a check); the acts take
the existing snapshot route from verdicts whose trust is already ruled; and
TC-211's result goes through the existing observation writer.

**Planning (S4).** `single`: the row touches several script families (the
roster reader, the sitting-brief composer, the planner briefs'
applicability function, the coordinator's prompt filler) and promises
behaviour over an input space (which judged sets are decomposition rounds,
and which templates declare the slot). `dual` is not needed.

**Architectural delta (S5).** The sitting brief's output comes to depend on
the hats roster and the parent needs' tags, through a call inside CMP-008
(the adjudicator-brief composer calls the planner briefs' applicability
function, with no import cycle); the coordinator's author prompt gains the
same block; the sidecar files, as a kind of state, and IF-133's `load`
leave. No new state, domain value or boundary crossing.

**Dependencies (S6).** No `needs`: B1's rubric anchors and the sitting
briefs' verdict/act split, the plan gate a `single` row waits on, and P9's
headless marking and lane-mode rule have all landed. Two rows come after
it: item 5's migration (not yet filed; its rows carry WI-976 in their
`needs` when filed, so LLR-297's cells are never migrated), and the
owner's FileBackup re-sync (OI-98, with WI-684 behind it), which the
handoff asks the owner to hold until this row lands, so the one known
adopter never receives the record (coordinator-2026-10-25 D-003). This row changes the sitting
briefs the cycle runs on, so it lands alone (revision 37).

**Proposed row text** (the target meaning the sitting judges; it names no
file or code):

- **SN-036 `acceptance`**, verbatim from `contract_split`: "Each
  decomposition round is reviewed against every applicable declared
  perspective, and the review record names each perspective and its
  outcome. The record demonstrates coverage and provenance; an independent
  review judges whether the resulting requirements are adequate." `need` and
  `why` unchanged.
- **SR-161:** title "Each decomposition round is reviewed against its
  applicable perspectives"; requirement and acceptance criteria
  `contract_split`'s; verification Inspection; rationale `contract_split`'s,
  naming the ruling by its dates (2026-09-06, re-affirmed 2026-10-13), never
  by its log path; `coincident`: "The need asks that each decomposition
  round is reviewed against every applicable declared perspective; the
  sitting's review record naming each perspective's outcome is that
  outcome, and whether the resulting requirements are adequate is left to
  independent review, as the need states."
- **LLR-183 `detail`:** `contract_split`'s opening ("The row-level
  provenance part of perspective review") and closing clause
  ("Per-decomposition coverage is discharged by the existing review path
  ... Hat-Refs retain their narrower role of identifying the hats that
  raised a row ..."); the rest is this branch's text, traced cells
  unchanged.
- **New LLR** (contract voice): a sitting brief composed for a
  decomposition round carries the question of every declared perspective
  applicable to the round and asks the verdict to name one outcome per
  perspective; a round is a decomposition round when its judged rows
  include a system requirement awaiting its first approval, or an approved
  stakeholder need whose text is amended, and any other judged set carries
  no perspective question; the applicable set is the union of the
  perspectives whose condition holds for each of the round's parent needs
  (each amended need, and each need a judged system requirement names),
  each need widened by the work item's declared tags and evaluated alone;
  the questions fill the perspective slot only where the sitting's template
  declares it, and a template that declares none composes unchanged; a
  sitting composing several judgement kinds carries them once; an absent
  roster yields the roster's no-perspective line, and a roster that exists
  and cannot be read refuses the composition, naming the roster.

**Unchanged, on purpose:** `Hat-Refs` (LLR-183, LLR-202; TC-178, TC-198)
and the planner's `{{HAT_QUESTIONS}}` path; whether LLRs keep the
`hat_refs` cell (the plan's separate question); the places that say
"perspective record" but mean `Hat-Refs`; and historical records (reviews,
decisions, logs, handoffs, call logs, the archive, closed specs).

**The six lane-authored sidecars** (a call the plan did not answer): the
ruling deleted the one record a builder wrote after the fact; these six
were written by the spine author and landed sittings cite them. This spec's
default: they stay, as inert lane records under `docs/plans/`, outside the
live surface (coordinator-2026-10-25 D-003, for the owner to confirm or
overrule).

## Done-when

**The ruling record**
- [ ] The log fragment of deliverable 1 is committed before any row text
  changes.

**The spine** (judged at one checkpoint sitting, top-down)
- [ ] SN-036, SR-161, LLR-183, TC-178 and TC-211 carry `contract_split`'s
  meaning, SR-161's rationale and `coincident` aside, as proposed above:
  TC-178's `expected` is split (LLR-183's `Hat-Refs` mechanics here,
  SR-161's acceptance inspected by TC-211); TC-211 verifies SR-161 and
  SR-186, inspects one actual completed decomposition review record, and
  its `inputs` name that record and its brief and no sidecar, its other
  cells staying.
- [ ] LLR-297 and TC-312 are retired, each with its retirement record, at
  the sitting that rules those amendments.
- [ ] One new LLR under SR-161 states the sitting brief's hat block, and one
  TC verifies it.
- [ ] IF-133's `data` cell no longer lists `load`.
- [ ] `docs/test/inspection-procedures.md` takes `contract_split`'s
  proportionality procedure and its "missing perspective outcome" abnormal
  input; the 2026-09-06 INCOMPLETE result stays as history.
- [ ] `docs/rubrics/decomposition-proportionality.md` R1 and B1 ask for the
  review record's outcomes, not a record producer.

**The retirement**
- [ ] The roster reader's `record` command and its test module are removed,
  with every symbol, import and docstring line only they used.
- [ ] `DECOMPOSITION-AMENDMENTS.perspectives.toml` and its pointer paragraph
  in `DECOMPOSITION-AMENDMENTS.md` go.
- [ ] No instruction asks for the record: PROCESS.md section 1's record
  sentence goes; `spine-questions.md` (c3) becomes the ruling's rule (the
  review record names each applicable hat's outcome, and a missing outcome
  is a review finding, never a coverage gate); both roster headers state
  the same rule, and `docs/requirements/hats.toml`'s "WHAT IS NOT BUILT
  YET" paragraph goes; the coordinator recipe's perspective-record line
  goes, in all three copies.
- [ ] SAFETY leaves `docs/requirements/hats.toml`, citing the revision 25
  ruling: its header count and its open SAFETY call close, the shipped
  template keeps SAFETY, and the live and template name pins in the roster
  tests split to match.
- [ ] No live surface names the sidecar or the `record` command. Live:
  `project-trajectory/`, `scripts/`, `tests/`, `.claude/skills/`,
  `.agents/skills/`, `CLAUDE.md`, `AGENTS.md`, `docs/requirements/`,
  `docs/test/`, `docs/rubrics/` and the generated pages. Not live: the
  superseded RESYNC entry, and records (`docs/reviews/`, `docs/decisions/`,
  `docs/log.md`, `docs/log.d/`, `docs/handoff-*`, `docs/plans/`,
  `docs/iteration/`, `docs/archive/`, closed specs).

**The hat block** (a closed input space; anything outside it gets the
default)
- [ ] A sitting is a decomposition round exactly when its judged set holds
  an SR awaiting first approval or an amended SN; every other judged set
  (LLR, TC and IF rows, SR amendments, Done-when changes and every other
  brief class) gets no hat questions.
- [ ] Applicability is computed from the roster for each parent need (each
  amended SN, and the SN each judged SR names), widened by the work item's
  tags and never merged across sibling needs, the rule the dual-plan
  planner already uses; it is never hand-written.
- [ ] `adjudicate-first-approval.template.md` and
  `adjudicate-amendment.template.md` each declare an optional single-brace
  hat slot; the composer supplies it only where the template declares it,
  so an overridden template without it composes unchanged; outside a
  decomposition round the slot says so.
- [ ] A combined sitting carries the questions once, and its verdict names
  each hat's outcome once.
- [ ] An absent roster yields the opt-out line, and a malformed roster
  refuses the composition by name.
- [ ] The verdict's hat outcome lines are neither row-ruling lines nor
  machine lines: a verdict carrying them parses to the same rulings as one
  without them.
- [ ] The spine-author prompt (`scripts/coordinator/terra-spine-prompt.template.md`)
  carries the same block, computed from the lane's work item, for a turn
  whose change set adds an SR under a need or amends a need; any other
  turn gets a line saying it is no decomposition round; the
  `coordinator-cycle` skill's dispatch step and the recipe name the slot.
- [ ] Tests cover each state above, and the prompt slot pins follow.

**TC-211**
- [ ] This lane's checkpoint sitting is the sample: composed with the block,
  its brief committed beside its verdict, its verdict naming each
  applicable hat's outcome.
- [ ] After the acts, a fresh session that wrote none of the rows, the brief
  or the verdict inspects it under the amended procedure; its result is
  recorded through the kit's observation writer and in the procedure's
  result section.

**The owner-held step**
- [ ] One step is the owner's: SN-036's re-attestation act, through the
  needs-only snapshot route, in text-then-act order
  (`intake.py snapshot --approves stakeholder-needs=<the fragment> --reattests SN-036`),
  naming the sitting's verdict where the route asks for it, taken attended
  in the lane, after a re-claim if a headless leg marked the lane.
- [ ] A headless leg brings the lane to that act and stops: it commits the
  verdict, takes every other act, and records the command and its evidence
  in the lane's decisions record and under the handoff's "For the owner".
  It never takes the act.
- [ ] The lane does not land before the act. If the owner returns SN-036's
  text, it is reworked and re-sat alone, with any row whose meaning follows
  it.

**Shipping and the bar**
- [ ] One RESYNC entry, superseding the 9233772b entry: the `record` command
  is gone and an adopter's script calling it fails; existing
  `.perspectives.toml` files are inert notes; the two sitting templates
  gain an optional hat slot, and an overridden template without it
  composes unchanged; the roster template's header changed, so a preserved
  roster's header comment is stale.
- [ ] The generated pages and the prompt catalogue are regenerated, and the
  `byte-budget-guard` skill reports PROCESS.md's delta and restamps its
  row.
- [ ] The commit bar is green, and both strict lints are clean on the
  landing tip.
