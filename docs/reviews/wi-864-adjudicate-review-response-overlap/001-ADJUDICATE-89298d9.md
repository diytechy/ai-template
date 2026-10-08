# ADJUDICATE — WI-864 — review-response overlap at 89298d9

Independent adjudication of the eight rows the owner chose on 2026-10-08:
WI-805, WI-811, WI-847, WI-848, WI-852, WI-853, WI-854 and WI-860 (digests
`af015cc7e32a|a4596ff3f7d5`, unchanged when judged). The owner's question was
whether these rows guard against the same thing from several directions.

Disclosure. Besides the brief I read:

- the owner's ruling (`docs/log.d/2026-10-08-owner-ruling-review-threat-model.md`);
- WI-861 as cancelled into WI-811;
- WI-856;
- WI-855's three sittings (`docs/reviews/wi-855-adjudicate-queue-overlap-2042/`);
- WI-848's drafts (`docs/plans/2026-10-07-wi841-retro/drafts/coordinator-cycle/`);
- the untracked coordinator brief templates in
  `C:/Projects/ai-template.wt/coordinator-tools/` (`sol-review-prompt` and
  `review-prompt`);
- `plan_coverage.py`'s findings input;
- the close path (`consolidate.parse_verdict`, `reconcile_refusal`,
  `close_refusal` and `edged_text`).

HEAD stayed at 89298d9 throughout.

**The owner's question.** These rows are not one guard written several times.
They are one pipeline, cut into stages, and each stage is its own decision:

- WI-852 and WI-860 shape what a reviewer reports: WI-852 asks for failure
  classes, and WI-860 bounds the scope with the threat model.
- WI-853 requires each reported finding to be covered by the rework plan.
- WI-811 sends a contested or repeated finding to the adjudicator.
- WI-805 replans and escalates a builder that keeps failing.
- WI-847 makes a round cheaper.
- WI-848 writes the coordinator's procedure down.

WI-854 is outside the theme. It judges spine rows, not review findings, and
nothing in this cluster collides with it.

The real risk is textual. Four facts each have, or would get, two homes:

- **The threat model.** The coordinator-tools templates restate it today
  under ruling rule 3, and WI-860 makes PROCESS.md §6 its one home.
- **The scope-critique questions.** WI-848's draft §1 lists them, and WI-852
  puts them in a rubric.
- **The sweep table.** WI-848's draft describes it, and WI-853 makes it a
  checked plan grammar.
- **"A resolved dispute counts as covered".** Both WI-853 and WI-811 state it.

The fourth is one gate fed by two producers, and WI-855 already judged it
that way. The order WI-853, then WI-805, then WI-811 makes the producer
conform to the gate, and this sitting does not re-litigate it. The first
three are settled by order, not by consolidation.

**Shape 1, contradiction with the spine: none.**

- WI-847 keeps the merge-gating review fresh, which agrees with SR-154 and
  with WI-811's amendment that the final review is never an authoring
  session.
- WI-852 and WI-854 extend SR-146's strict-slot render to the coordinator
  and to a composed home. They do not relax it.
- WI-811's final resolution amends SR-154 itself, in the third position
  after WI-805.

One composition at the third CR round is recorded below as a MINOR finding.

**Shape 3, already answered: none.**

- WI-861 is already folded into WI-811, and nothing here re-absorbs it.
- No row in the cluster is an earlier consolidation's successor.
- WI-855 judged the other seven rows and kept each one separate. The new
  facts are WI-860, the ruling's interim text and WI-861's fold. None of them
  merges two rows into one decision.

**Consolidation: none.** Every row is independently landable. The retro's
reconciliation (§8.1) cut WI-852 from WI-801 and WI-853 from WI-805 on
purpose, and those cuts stand.

**Shape 2, scope overlap: five collisions.**

- [MAJOR] WI-852 -> WI-852 retires the coordinator-tools brief templates
  that WI-848's draft recipes are built on:
  - the recipes fill `$TOOLS/sol-review-prompt.template.md` through
    `mkprompt.py`;
  - they say "Rendering through `prompts.py` ... follow-up work, not live
    gates";
  - the draft §1 restates the two scope-critique questions that WI-852 moves
    into a rubric under `docs/rubrics/`.

  WI-852 is claimable now, and WI-848 becomes claimable once WI-846 lands.
  If both are in flight, neither builder sees the other's text. WI-848's
  reconciliation clause covers only rows that have already landed. A skill
  that lands first is outside WI-852's reviewed range, so the procedure
  would keep naming retired templates and a second copy of the questions.
  -> add the edge WI-848 needs WI-852. WI-848's existing reconciliation
  clause then lands the skill pointing at the rendered briefs and the
  rubric. Nothing waits on WI-848, so only WI-848 is delayed.
- [MAJOR] WI-853 -> WI-848's draft says wiring `plan_coverage.py --findings`
  is "follow-up work, not live gates". WI-853 makes that check the live
  dispatch gate and gives the sweep table its checked grammar. The two rows
  collide in the same way as the previous finding. -> add the edge WI-848
  needs WI-853. The skill then states the gate as live and points at that
  grammar instead of holding a second copy of the table. WI-853 builds the
  table's columns from its own Done-when, which lists them.
- [MINOR] WI-860 -> WI-848's draft predates the 2026-10-08 ruling. Its
  review steps carry neither rule 1 nor rule 3's interim procedure:
  - state the out-of-scope class in every reviewer prompt;
  - apply rule 1;
  - record each dismissal in `docs/decisions/<branch>.toml`.

  Its reconciliation clause names rows, not rulings. -> add the edge WI-848
  needs WI-860, so the skill links PROCESS.md §6 instead of restating it.
  The coordinator should also give WI-848 this Done-when bullet by hand:
  "The coordinator-cycle review steps carry the 2026-10-08 ruling (`docs/log.d/2026-10-08-owner-ruling-review-threat-model.md`):
  rule 1 by a link to PROCESS.md §6's review threat model, and rules 2 and 3
  as the procedure that holds until WI-811 lands (the coordinator applies
  rule 1 to each review, records each dismissal in the lane's decisions
  record, and sends a contested or third-round finding to the adjudicator)."
- [MAJOR] WI-860 -> WI-852 and WI-860 edit one clause of one shipped
  template from opposite directions:
  - The coordinator-tools templates that WI-852 retires carry the threat
    model verbatim, under "Out of scope: the review threat model (owner
    ruling, 2026-10-08)".
  - WI-852's Done-when moves whatever those templates carry that the kit
    templates lack "into the fill values or the kit templates".
  - WI-860 makes PROCESS.md §6 the one home and has `prompts/reviewer.template.md`
    link to it, not restate it.

  If WI-852 lands first or alongside, it puts a second home of the threat
  model into the shipped reviewer template or a fill value, and WI-860 must
  then find it and remove it. -> WI-852 needs WI-860. WI-860 is a small
  docs row that is claimable now, so this delays WI-852, and through it
  WI-847 and WI-801, by one medium build. This sitting cannot enact the
  edge: WI-852 has no `needs` line, `consolidate.edged_text` returns None,
  and `handback._enact_plan` would refuse the whole verdict (WI-856 is
  still open). The coordinator adds `needs = ["WI-860"]` to WI-852 by hand
  before claiming either row, or lands WI-856 first.
- [MAJOR] WI-852 -> WI-853's shared step turns "a review verdict's finding
  lines" into the `F#` clauses `plan_coverage.py --findings` reads, for both
  the loop and the coordinator. Until WI-852 lands, the coordinator's
  reviews are in a hand format: the first line is `<sha> SOUND` or
  `<sha> NOT YET SOUND`, followed by BLOCKER, MAJOR and MINOR sections. They
  are not kit round files with kit finding lines. If WI-853 is built first,
  its coordinator half has two choices. It can parse that second grammar,
  which WI-852 then retires (a legacy path, against the owner's 2026-10-03
  no-fallback rule). Or it can leave the coordinator half untestable.
  -> WI-853 needs WI-852. This costs WI-805 nothing, because WI-805 already
  waits on WI-852 through WI-804 and WI-801. This edge cannot be enacted
  either, because WI-853 has no `needs` line. The coordinator adds
  `needs = ["WI-852"]` to WI-853 by hand, with the same timing as the
  previous edge.
- [MINOR] WI-805 / WI-811 -> two rules act at the third CHANGES-REQUESTED.
  WI-805's ladder says "a third CR tiers up" (LLR-081). WI-811's bullet
  absorbed from WI-861 says "any finding class reaching its third review
  round goes to the dispute sitting before another build round". These are
  not a contradiction: WI-811 is ordered after WI-805 and amends SR-154
  after it. But the WI-861 bullet is worded for the coordinator's entry
  point. A loop that tiers up at the third CR without a sitting would keep
  building blind against the very finding that ruling rule 2 sends to the
  adjudicator. -> WI-811's builder states in its rows that, in the loop
  too, the third-round sitting comes before WI-805's tier-up build, and
  the tier-up build answers only upheld findings. This is the LLR-081
  amendment WI-811 shares with WI-805. No edge is needed, because WI-811
  already waits on WI-805.
- [MINOR] WI-811 -> once WI-848 lands, WI-811's dispute class replaces the
  skill's iterate step 7 ("A dispute goes to the adjudicator") and its
  recipes. WI-811 is ordered long after WI-848, so it is the row that lands
  second. -> WI-811's builder updates `coordinator-cycle`, as CLAUDE.md's
  this-repo skill rule already requires. No edge is needed.

OUTCOME: QUEUE-WITH-EDGE needs=WI-848 absorbs=-
