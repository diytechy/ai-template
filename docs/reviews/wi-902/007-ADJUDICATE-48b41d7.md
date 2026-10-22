# WI-902 adjudication 007: lane checkpoint at 48b41d721 (amendment; first-approval)

This re-sits sitting 006 (item 4 of its returns). I judged the rows as they stand at `48b41d721`, reading the chains in the live registries and checking the trace homes against the code.

**What 006 returned, and what the lane changed:**
- **One home for adoption.** LLR-335 (SR-148) is now the single home of the adoption decision. Its eleven symbols back-link `SR-148, LLR-335`, and the shared handback close `_archive_one_adjudication_row` back-links both LLR-312 and LLR-335.
- **LLR-153 trimmed.** It no longer lists `kitlib/adoption.py` or the adoption symbols. Its Detail cites LLR-335 instead of restating the acceptance rules, and its SR-Refs gain SR-148 for the lineage half of title identity.
- **TC-360's Evidence** drops the two title-identity tests that TC-147 keeps.

The finding 006 raised is answered.

**Checks:**
- Every `Evidence` test named here exists.
- `check_trajectory.py --strict` is clean.
- The close calls `adoption_lineage` with no replay flag, so it applies the open-state rule (`handback.py:896`), as LLR-335 says.
- The LLR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`).

**Two advisories.** Neither blocks a row, and the lane can fold both in before it merges:
1. **Shared functions name only LLR-335.** `parse_disposition_section`, `_section_block`, `_disposition_drafts` and `_merged_dispositions` serve LLR-153's draft arms as well as LLR-335's adoption arms. They validate drafts (`_draft_refusal`), feed the drafts-mint trigger, and hold the unreadable-spec refusal that LLR-153 states. Their tags name only `SR-148, LLR-335`, and LLR-153's CodeSymbol no longer lists them. Sitting 006's "each symbol in one LLR's `CodeSymbol`" asked for this, so it is my wording, not the lane's error. A shared function should name both rows, as `_archive_one_adjudication_row` does.
2. **One LLR-335 clause is only partly tested.** LLR-335 says the adopted row's cells are never changed. `test_an_adoption_of_a_superseding_row_closes_and_sweeps` checks only that row's `Status`. A byte-identity check on the adopted spec after the close and the sweep would test the clause whole. TC-360 does not claim this check, so its text overclaims nothing.

## amendment

- [MEANING] LLR-161 Detail -> continuing partial work drafts a successor with explicit lineage, never re-opening a terminal row -> it drafts a successor or adopts an already-filed one, with explicit lineage, never re-opening a terminal row -> the adoption path is a new case of the close's continuation. Blessed: SR-144's close ritual is the right parent, and sitting 006 already blessed this text, which is unchanged since.
- [MEANING] TC-156 Method -> the handback suite checks a clean partial close, a loud missing report, a refused second close and report-path keying -> it also checks that a continuation can draft or adopt a successor without reopening the terminal row -> the test's obligation is extended. Blessed: it verifies LLR-161's new clause, and its cited test `test_an_adoption_of_a_superseding_row_closes_and_sweeps` exists. Unchanged since 006.
- [MEANING] LLR-153 Detail -> the intake mint covers three triggers, drafts minting at merge, and exact-title dedup as plain allocation suppression -> it adds: an adopts-only block allocates no id (under LLR-335's rules); exact-title dedup resolves identity and lineage together (no lineage for a draft that supersedes nothing; standing only for one same-title row with the draft's own Supersedes; any other match refuses the whole mint before any write); the one lineage operation re-points a dependent to the full successor set, accepted adoptions included; a no-op replay commits nothing; an unreadable merged spec refuses the sweep rather than being skipped -> new cases and refusals. Blessed. The upward read now holds: allocation-only dedup and "allocates no id" answer SR-174, the approval-level arms answer SR-228, and the successor-set lineage half answers SR-148, which the row now cites. Sideways, it states the mint's own arms and cites LLR-335 for adoption acceptance instead of restating it, so each decision has one home. The text matches `_standing_successors` (`intake.py:2560`).
- [MEANING] TC-147 Expected and Method -> Expected: satisfies SR-174 via LLR-153; Method: the intake suite per trigger -> Expected now names SR-174, SR-228 and SR-148 through LLR-153. Method adds: an adopts-only block allocates no id; title-identity standing versus refusal before any write; the full successor set; the no-op replay; and an unreadable merged spec refusing with nothing minted -> the claimed parents and the verification obligations both grew. Blessed: the Method is closed over LLR-153's new arms and leaves adoption acceptance to TC-360. Each new arm has a named test (`test_drafts_and_adoptions_together_hold_the_full_successor_set`, `test_a_replay_re_points_a_late_dependent_to_the_full_successor_set`, the two title-identity tests, `test_an_unreadable_merged_adjudication_spec_refuses_the_sweep`). Its Verifies matches its Expected.
- [MEANING] LLR-312 Detail -> the consolidation close resolves, plans and composes every affected spec before its first write -> it also refuses, before any write, a consolidation disposition that adopts an item -> a new refusal case. Blessed: SR-220 requires that the successor record every item it supersedes, which an adoption cannot satisfy. Unchanged since 006.
- [MEANING] TC-254 Method -> the consolidation suite's existing clauses -> it also checks that a consolidation verdict that adopts refuses the close before any write -> a new verification obligation. Blessed: it matches LLR-312's new clause, and `test_a_consolidation_verdict_that_adopts_refuses_the_close` exists. Unchanged since 006.

VERDICT: MEANING rows=6

**Aftermath:** this session re-attests all six rows on the released rung, in their own act commit:

`python project-trajectory/scripts/intake.py snapshot --reattests LLR-153,LLR-161,LLR-312,TC-147,TC-156,TC-254`

## first-approval

- [APPROVE] LLR-335 -> one shared module carries the adoption rules:
  - it parses an adoption block of exactly one well-formed WI id;
  - it reads the disposed item only from one event token in the disposition title;
  - it accepts the adopted item with distinct refusals: unloadable registry, item not open at first consumption, unreadable spec, Supersedes omitting the disposed item;
  - on replay it finds the item in any state and reads lineage only;
  - the close and the landing sweep apply the open-state rule, and a later sweep applies the lineage rule;
  - an accepted adoption joins the drafted successors' single re-point without minting, drafts still mint, and neither consumer guesses a successor or edits the adopted row.

  -> Upward, SR-148's AC (re-anchored in 006) calls for "names an already-open item that supersedes it as its successor". Sideways, it is now the single home: LLR-153 cites it instead of restating it, its symbols back-link to it, and the shared close is tagged with both it and LLR-312. Downward, TC-360 verifies every arm with a named, existing test. The one partial check is advisory 2.

  -> Ready: one decision, the right parent, no `shall`, real detail beyond its parent, and trace homes that agree.
- [APPROVE] TC-360 -> it parses valid and malformed adoption blocks, derives the disposed item from both title forms and rejects bad titles, reads the accepted, missing, closed, unreadable and non-superseding cases, and on real repositories checks the close and landing acceptance without a mint, the refused close, a drafted successor still minting, no absorption, lineage-only replay, a closed successor refused at landing, the full successor set including a late dependent, and a no-op second replay -> it verifies SR-148 and LLR-335. Its Evidence now cites only adoption tests, all of them existing, and leaves the title-identity tests to TC-147. Its Expected is a condition (open at first consumption, enduring lineage on replay, invalid lineage refused, complete successor set, no id allocated) -> ready: closed over LLR-335's arms, with no claim beyond its tests.

OUTCOME: APPROVE rows=2

**Act:** the flip of LLR-335 and TC-360 to `Approved` and `intake.py snapshot --approves "docs/requirements/low-level-requirements.toml=WI-902;docs/test/test-cases.toml=WI-902"` go in one commit, taken after the re-attestation act above.

SITTING: JUDGED kinds=amendment;first-approval
