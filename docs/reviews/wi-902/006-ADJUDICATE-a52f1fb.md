# WI-902 adjudication 006: lane checkpoint at a52f1fbbf (amendment; first-approval)

Judged on the cells the brief showed, with the chains read in the live registries at `a52f1fbbf`. I checked the code only where a trace home (`Module`, `CodeSymbol`, `Implements:` back-links, `Evidence`) bears on a row. Every test the arms map and the TC `Evidence` cells name exists. The LLR, SR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`), so every act below is this session's.

One finding drives most of this verdict. The adoption arms have two LLR homes, and the code points at the wrong one:

- **LLR-153 (Approved, amended)** now states the adoption sweep: the landing rule versus the replay rule, the re-point join, and the adoption refusals. It also carries these in its trace cells: `Module` includes `kitlib/adoption.py`, and `CodeSymbol` includes `parse_block/disposed_id/row_refusal/_hits/parse_disposition_section/adoption_lineage/_disposition_drafts/_merged_dispositions/_landed_before`. Every one of those functions back-links `Implements: SR-174, LLR-153`. But LLR-153's parents are SR-174 (identity allocated at most once) and SR-228 (held-rung CLARITY re-attestation). Neither calls for adoption acceptance, a replay rule or a needs re-point.
- **LLR-335 (Drafted, new)** traces to SR-148, whose amended AC is the clause that does call for adoption. Its Detail restates the same landing/replay rule and the same re-point join. Nine of its ten `CodeSymbol` entries are already LLR-153's, and the tenth, `_archive_one_adjudication_row`, is LLR-312's. No `Implements:` line anywhere in `project-trajectory/scripts` or `tests` names LLR-335.

So the one decision is stated twice, under two different SR chains. The row with the right parent is the one no code claims, and the row the code claims has parents that do not ask for it. In a kit whose product is traceability, this is a false chain (adoption code reads as implementing "identity allocated once"), not a style point.

## amendment

- [MEANING] SR-148 AcceptanceCriteria -> processing an unresolved handback either resolves the record or mints a provenance-linked successor exactly once -> it may also name an already-open item that supersedes the record as its successor -> the change adds a third accepted outcome. An implementation that refused an adopted successor satisfied the old AC and fails the new one. I would bless it: the clause extends the sentence that already homes handback processing, and it states an observable condition. Re-anchored below.
- [MEANING] LLR-161 Detail -> continuing partial work drafts a successor with explicit lineage -> it drafts a successor or adopts an already-filed one, with explicit lineage -> the adoption path is a new case of the close's continuation. I would bless it: SR-144's close ritual is the right parent for "the close may continue through an existing successor". Its anchor is blocked, see the aftermath.
- [MEANING] TC-156 Method -> the handback suite checks a clean partial close, a loud missing report, a refused second close and report-path keying -> it also checks that a continuation drafts or adopts a successor without reopening the terminal row -> the test's obligation is extended. I would bless it: it verifies exactly LLR-161's new clause, and `test_an_adoption_of_a_superseding_row_closes_and_sweeps` exists. Its anchor is blocked, see the aftermath.
- [MEANING] LLR-153 Detail -> the intake mint covers three triggers, drafts minting at merge, and exact-title dedup as plain allocation suppression -> it adds: an adopts-only block that mints nothing; the landing sweep's open-state acceptance against the replay's any-state lineage acceptance; the adoption's re-point of inbound hard needs together with drafted successors; exact-title dedup resolving identity and lineage together, refusing before any write; a no-op replay committing nothing; and the adoption and unreadable-spec refusals -> new behaviour, cases and refusals. I would NOT bless it as it stands, because the upward read fails. The adoption arms answer SR-148's new clause, but LLR-153 traces only to SR-174 and SR-228, neither of which asks for them. The same arms are restated in LLR-335 under SR-148 (see the finding above). The fix touches LLR-153 either way: it gains SR-148 in its SR-Refs, or it hands the adoption arms to LLR-335 and cites it. The text is accurate to the code at `intake.py:2560` (`_standing_successors`); the defect is where it sits. The re-home goes through the Dispositions draft below. I recommend that the title-identity/allocation half stay here under SR-174.
- [MEANING] TC-147 Method -> the intake suite checks each trigger, dedup idempotence, the context block and the dial arms -> it also checks landing-versus-replay adoption acceptance, the full successor set (late dependents included), the no-op replay, title-identity refusal and the adoption refusals -> new verification obligations. I would NOT bless it as it stands. It verifies the adoption arms through LLR-153's chain to SR-174 and SR-228, so it carries the same false chain. Its adoption clauses also duplicate TC-360's. It should be re-sat with LLR-153 once the adoption decision has one home.
- [MEANING] LLR-312 Detail -> the consolidation close resolves, plans and composes every affected spec before its first write -> it also refuses, before any write, a consolidation disposition that adopts an item -> a new refusal case. I would bless it: SR-220 requires that the successor record every item it supersedes, and an adoption carries no `supersedes` that the absorption could reconcile, so the refusal protects that obligation. Its anchor is blocked, see the aftermath.
- [MEANING] TC-254 Method -> the consolidation suite's existing clauses -> it also checks that a consolidation verdict that adopts refuses the close before any write -> a new verification obligation. I would bless it: it matches LLR-312's new clause one for one, and `test_a_consolidation_verdict_that_adopts_refuses_the_close` exists. Its anchor is blocked, see the aftermath.

VERDICT: MEANING rows=7

### Aftermath (taken after this verdict commits)

- **Re-attested by this session:** SR-148, in its own act commit: `python project-trajectory/scripts/intake.py snapshot --reattests SR-148`. It is the only drifted row in `system-requirements.toml`.
- **Blessed as they stand but left unanchored:** LLR-161 and LLR-312. LLR-153's drift holds `low-level-requirements.toml`, and the copy takes the registry whole.
- **Blessed as they stand but left unanchored:** TC-156 and TC-254. TC-147's drift holds `test-cases.toml` in the same way.
- **Not blessed, not anchored:** LLR-153 and TC-147. They go back through the draft below.

The coordinator should put all of these into one re-sitting with the returned first-approval rows, and the act there names them together.

## Returns answered in the lane

Answered in the lane (coordinator, 2026-10-11 leg 03): Terra's rework of items 1-3 and the coordinator's `Implements:` retags, re-sat together at the next sitting (item 4). No row is minted from this draft.

```toml
title = "WI-902 spine rework: give the disposition adoption one requirement home under SR-148 (answer checkpoint 006)"
workstream = "process"
sr_refs = ["SR-148", "SR-174"]
needs = ["WI-902"]
safety_class = "ordinary"
buildtier = "medium"
```

Spine and trace text only. No behaviour change is called for, and the code at `a52f1fbbf` is what the rows should describe.

1. **Choose one home for the adoption decision.** This covers the adoption block's parse, the disposed-id read, the open-state acceptance against the replay's lineage acceptance, the distinct refusals, and the join of an accepted adoption into the re-point pass. I recommend LLR-335: it has the SR-148 parent, and its Rationale (one shared validator for both consumers) is a decision no other row states.
   - That row's `CodeSymbol` lists those symbols.
   - LLR-153's `Module` and `CodeSymbol` stop listing them.
   - Their `Implements:` lines name `SR-148, LLR-335`.
   - LLR-153's Detail keeps what is the mint's own (an adopts-only block allocates no id; title identity and lineage resolved together, refusing before any write; a no-op replay commits nothing) and cites LLR-335 for the acceptance rules instead of restating them.

   The alternative, if the author keeps the sweep arms in LLR-153: add SR-148 to LLR-153's SR-Refs and narrow LLR-335 to the shared-validator decision alone. Either way, each rule is stated once, and each symbol sits in one LLR's `CodeSymbol` with a back-link that names that LLR.
2. **Make sure each arm's parent calls for it.** The lineage half of title identity (a standing successor kept in the successor set under the draft's intended lineage) answers SR-148, not SR-174. Whichever row states it traces to SR-148.
3. **Have each arm verified by one TC in the chain that homes it.**
   - TC-147 keeps the mint's own arms.
   - TC-360 keeps the adoption arms.
   - TC-360's `Evidence` drops `test_a_title_match_off_the_drafts_lineage_refuses_the_mint` and `test_a_drafts_title_match_on_its_own_lineage_stays_standing`, unless its home row comes to state title identity. TC-147 already cites both.
4. **Re-sit together:** LLR-153, TC-147, LLR-335 and TC-360, plus LLR-161, LLR-312, TC-156 and TC-254. This sitting blesses the last four as they stand; they are unanchored only because LLR-153 and TC-147 hold their registries. Then one act re-attests the amended rows and first-approves the new ones.

## first-approval

- [RETURN] LLR-335 -> one shared module parses the adoption block, reads the disposed id from the disposition title's one event token, and accepts the adopted item with distinct refusals (open-state at first consumption, lineage-only on replay); the close and the landing sweep apply the open-state rule and a later sweep the lineage rule; an accepted adoption joins the drafted successors' re-point without minting or editing the adopted row -> its chain upward is sound, because SR-148's amended AC calls for naming an already-open superseding item as the successor. Sideways it is not. Its landing/replay and re-point arms are stated again in the amended LLR-153. Nine of its ten `CodeSymbol` entries and its `kitlib/adoption.py` Module are already LLR-153's. Its tenth symbol is LLR-312's. No `Implements:` line names LLR-335; `kitlib/adoption.py`'s four functions back-link `SR-174, LLR-153` -> not ready. Approving it now would bless a second home for a decision whose trace homes point elsewhere. Its own decision (one validator that both consumers read) is real and worth keeping as the single home. The follow-up is the one `## Dispositions` draft under `## amendment` above, so that a single row answers both sections and nothing is minted twice.
- [RETURN] TC-360 -> parse valid and malformed adoption blocks; derive the disposed item from both title forms and reject bad ones; read the accepted, missing, closed, unreadable and non-superseding cases; check close, landing and replay behaviour on real repositories, the full successor set, a late dependent and a no-op replay -> it verifies SR-148 and LLR-335, and every test it cites exists -> not ready. Its row LLR-335 is returned above, and a returned row withholds its TC. Its `Evidence` also cites `test_a_title_match_off_the_drafts_lineage_refuses_the_mint` and `test_a_drafts_title_match_on_its_own_lineage_stays_standing`. Those verify LLR-153's exact-title identity rule, a claim that neither TC-360's Method, its Expected nor LLR-335 makes, and TC-147 already cites both. It should be re-sat with LLR-335 under the same draft.

OUTCOME: RETURN rows=2

No approval act follows: every row in this section is returned, so no Status is flipped and no `--approves` snapshot is taken.

SITTING: JUDGED kinds=amendment;first-approval
