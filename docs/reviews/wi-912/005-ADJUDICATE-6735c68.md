# WI-912 adjudication 005: lane checkpoint at 6735c6832 (amendment; first-approval)

I judged the rows on the text at `6735c6832`, reading their chains in the live registries and checking the trace homes against the code. The SR, LLR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`). This sitting records the verdict only; the acts it authorizes are a later act turn.

**What I checked:**
- **Tests:** every `Evidence` test of TC-161, TC-192, TC-308, TC-321, TC-322 and TC-368 exists, and every test a Method names is in its Evidence.
- **Tiers:** TC-321's evidence includes `test_coordinator_act`, which `tests/conftest.py` lists in `SLOW_MODULES`, so its move to `Full` is honest. TC-368 cites only fast evidence and stays `Smoke`.
- **Code:** all 26 of LLR-338's `CodeSymbol` entries exist in `adjudicate_act.py`, and its functions back-link LLR-338.
- **Checks:** `check_trajectory.py --strict` is clean. `trace.py --strict` raises only SR-231's "unclassified" advisory, which concerns its `DA-Refs` and `Delivered-With`, cells this amendment did not touch.

**Three advisories.** None blocks a row:
1. **Stray SR-146 tag.** `adjudicate_act.act_values` and `compose_act` back-link `SR-231, SR-146, LLR-338`, but LLR-338's SR-Refs are SR-231 and SR-232. Either drop SR-146 from those tags or argue it into LLR-338's SR-Refs, so the trace homes agree.
2. **SR-231's new sentences are indicative.** "From a claimed lane, it takes only an act..." and "the act turn's success is the completion contract stated in the acceptance criteria" sit outside the row's one `shall`. The obligation is clear and observable, and the AC that gives the completion contract is verified by TC-321 and TC-368. WI-913's D-008 precedent would fold it in as a second predicate under the one `shall`.
3. **An unclear "it" in LLR-167's addition.** "a released-rung MEANING verdict it blesses" uses "it" without a clear referent. The judging adjudicator is meant, and naming it would close the reading.

## amendment

- [MEANING+BLESS] LLR-167 Detail -> the brief router composes each declared brief strictly, holds on refusal, renders amendment before/after within scope, and composes tier questions from one home; the first-approval brief derives the `--approves` argument and forbids stopping before the approval commit -> the same, plus: judging briefs order no act; a first-approval brief derives no approval-registry token or per-token row map; amendment aftermath identifies each verdict's mark for a later turn (CLARITY re-anchored, naming its verdict on a held rung; a blessed released-rung MEANING marked `MEANING+BLESS`; a held MEANING recommended to the owner) -> the brief's obligations changed: it no longer orders the act or derives its tokens. Blessed: it is the judging half of SR-231's split into a judging turn and an act turn, verified by `test_no_judging_brief_orders_an_act`. See advisory 3.
- [MEANING+BLESS] TC-161 Expected and Method -> Expected was the bare "Satisfies SR-146"; Method asserted the derived `--approves` command and the session-owned re-attestation arms -> Expected now states that judging briefs order no act and name the later act turn; Method asserts no snapshot command, no "BY YOU" and no Status flip, plus the act-turn citation, and defers command quoting to TC-368 and completion to TC-321 -> the verification obligations were replaced. Blessed: it is closed over LLR-167's new arm and hands the act half to the TCs that own it.
- [MEANING+BLESS] TC-192 Method -> catalogue freshness and question-home staleness -> it adds that the act brief is a shipped prompt with six strict slots, fills in full and refuses a fill missing one -> a new verification obligation. Blessed: the act brief is a new shipped prompt, and the catalogue TC is where shipped prompts are pinned.
- [MEANING+BLESS] TC-308 Method -> an assumption-only first-approval brief shows a test-registry token and no assumption-registry token -> it shows no registry token at all -> a changed assertion. Blessed: it follows from LLR-167's "derives no approval-registry token".
- [MEANING+BLESS] LLR-305 Detail -> REVIEW identity is the once-resolved reviewer template, and ADJUDICATE keeps the retained-class identity -> it adds that the governing identity of a retained set holding amendment, first-approval or combined also covers the act brief, by its override text or else its shipped text -> a new identity input. Blessed: a retained adjudicator that later takes acts must drain when the act brief changes. TC-322 verifies it.
- [MEANING+BLESS] TC-322 Method -> the retained-class identity cases -> it adds that the act brief joins each actable retained class's identity, and joins no other class -> a new verification obligation. Blessed: it is closed over LLR-305's addition, and its named test exists.
- [MEANING+BLESS] LLR-306 Detail -> the coordinator entry point's judging turn (claimed lane, exclusive reservation, validated verdict, recorded outcome) -> it adds an act invocation: from a clean claimed lane, it derives the later-turn brief from the verdict and binding committed at HEAD; plans retention by that class; launches and logs without reserving a verdict or recording an outcome; refuses before launch on lane, route, dirty-tree or derivation inputs, naming each; succeeds only when no authorized act is left owed and no verdict record changed; appends loop provenance under the marker; and the judging turn's freshness conditions apply only to judging -> a new command arm and its contract. Blessed: it decomposes SR-231's amended acceptance. TC-321's `test_coordinator_act` cases verify each arm. It names no new carrier.
- [MEANING+BLESS] TC-321 Expected, Method and Tier -> the judging-turn outcomes at Smoke -> it adds the act turn: pre-launch refusals with no launch or change; amendment before first approval; success only with every act taken and verdict records unchanged; byte-identical briefs for retained and fresh turns; a dirty interrupted turn discarded and rerun; a combined rerun listing only first approval; provenance only under the marker; and the tier moves to Full -> new obligations, and a tier under which evidence could leave the commit floor. Blessed: it is closed over LLR-306's act arm, its tests exist, and `Full` is honest.
- [MEANING+BLESS] SR-231 Requirement, AcceptanceCriteria and Rationale -> the entry point runs only from a claimed lane and reads success only from a verdict its own call wrote in its deadline -> it adds that from a claimed lane it takes only an act an accepted current verdict authorizes. The AC states the act turn's pre-launch refusals (an unaccepted verdict, one owing no act, an unexplained row state, uncommitted changes), that it reserves no verdict and writes no binding or outcome, that it is retained only where the class is retained, and that it succeeds only when the call succeeds, every authorized act is taken and verdict records are unchanged. The judging conditions are scoped to the judging turn. The Rationale adds why only an accepted committed verdict authorizes an act -> a new obligation. Blessed:
  - SN-025's attributable, current adjudication evidence now extends to the act that evidence authorizes.
  - The AC is observable and verified by TC-321 and TC-368.
  - It names no file.
  - See advisory 2 on form.
- [MEANING+BLESS] LLR-310 Detail -> the combined sitting, review-line and binding rules, with merge-time authorization by accepted rulings -> it adds that an amendment verdict's `- [MEANING+BLESS]` row tag reads MEANING to every rulings reader, and that a dedicated reader returns only rows so marked, treating an unmarked row or one also tagged MEANING or CLARITY as not blessed -> a new grammar element and reader. Blessed: it is the one parser that every consumer shares, now carrying the mark the act turn needs, and it fails closed on ambiguity. TC-368's three bless-mark tests verify it.

VERDICT: MEANING rows=10

**For the later act turn:** all ten rows are marked `[MEANING+BLESS]` on a released rung, so the act turn re-attests each one. No row is held, and no row is returned.

## first-approval

- [APPROVE] LLR-338 -> from an accepted verdict and its binding as committed at a revision, derive every authorized act the committed registries and records do not yet carry in full:
  - released APPROVE; CLARITY on either rung, naming the verdict when held; blessed MEANING on a released rung only;
  - nothing for RETURN, unmarked or held MEANING, held APPROVE or Done-when;
  - owed-or-taken read from status and the whole-row copy, refusing an unrecognized state or an unmatched tier by row;
  - refusal of uncommitted, unbound, unaccepted or invalid verdicts, of a class with no act, of exhausted acts and of a missing approval record;
  - amendment listed before first approval, with a brief filled whole or not at all;
  - a retirement owed while recorded and taken once absent (no act when held), and a first approval of an absent row refused;
  - each row's arm taken from the one held-rung policy.

  -> **Upward,** SR-231's amended AC (an act turn takes only what an accepted verdict authorizes, and succeeds only when all of it is taken) and SR-232's per-kind scope (amendment before first approval, neither acting on the other's scope) both call for exactly this derivation. **Sideways,** it is the act-side counterpart of LLR-167 (which now orders no act) and LLR-306 (which launches it), and it reads LLR-310's bless reader rather than re-parsing. **Downward,** TC-368 verifies every arm with a named, existing test.

  -> Ready: one decision, the right parents, no `shall`, no carrier named, and refusals that are each observable. The stray SR-146 back-link is advisory 1.
- [APPROVE] TC-368 -> exercise bless-mark parsing and committed-verdict derivation on real git fixtures across accepted, unreadable, mixed, held, interrupted, inconsistent and completed states; fill the act brief and inspect its commands; assert two-registry token coverage, one listing per row, retirement listed with re-attestations and leaving nothing owed once taken through the snapshot writer, no act for a held retirement, refusals for an absent first approval, a missing approval record, a row no compared tier holds and an out-of-root verdict, and each row's arm pinned against the held-rung policy for every ruling and rung -> it verifies SR-231, SR-232, LLR-338, LLR-310 (the bless reader) and IF-296. Its 29 named tests all exist and are fast, so `Smoke` is honest. Its Expected is a condition, not an instrument -> Ready: closed over LLR-338's arms and LLR-310's bless addition, with no claim beyond its tests.

OUTCOME: APPROVE rows=2

**For the later act turn:** LLR-338 and TC-368 are approved. Flip both to `Approved` and anchor the LLR and TC registries.

SITTING: JUDGED kinds=amendment;first-approval
