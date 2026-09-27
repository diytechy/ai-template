# Arbitration — the third build wave (2026-09-26/27)

The wave that carries out the owner's 2026-09-26 rulings (OI-82, OI-86 to
OI-94) and the second wave's filed drafts. Builders work in their own
worktrees; codex Sol reviews each commit read-only (the `sol-*.md` files
beside this one, prompts reproducible from
[the wave-2 record](../2026-09-26-assumption-tier-wave2/ARBITRATION.md)'s
form). The coordinator rules where a builder and Sol disagree, or where it
disagrees with Sol, citing the governing text. Rulings a Fable arbiter makes
are marked as such.

1. **WI-653 — no dispute.** Sol: SOUND, no findings.

2. **WI-665 — SOL, both findings.** The Done-when asks only that the seven
   modules collect alone, but the defect is collection-order dependent, so
   nothing in the suite would notice it coming back. The ruling is a subprocess
   regression that collects one affected module alone, in a slow module, and
   shown red. It runs serially, which reproduces the defect as `-n 2` does at
   less cost. The builder brief's own rule is that position 0 matters (`import
   trace` must bind the kit's `trace.py`), so the helper has to guarantee it
   rather than only test membership. Both are fixed in one follow-up commit.

   **Correction, by the builder's evidence.** The coordinator's instruction
   to run the regression serially was wrong. A serial run does not reproduce
   the defect: `pytest_sessionstart` calls `load_script("agent_common")` on
   the controller before collection, and xdist workers skip that hook. The
   builder showed `4 passed` serially and `1 error` at `-n 2` on the unfixed
   conftest, and wrote the test at `-n 1`. Sol's fix round (`sol-wi665-fix.md`)
   confirmed the claim and judged 614b0ac1 SOUND.

3. **WI-654's pre-adoption failure — SOL.** The builder made only the
   neither-cell advisory wait for adoption, and kept a `bridged_by` naming an
   undeclared assumption failing before it. Its reason: a pointer into
   nothing is wrong wherever it is written. The governing text is OI-94's
   ruled option (b), "one adoption rule across the tier", with the
   recommendation "one adoption rule for the whole tier". SR-193 and SR-194
   make their undeclared-citation failure vacuous before adoption, and before
   adoption every named assumption is necessarily undeclared. Keeping the
   failure would therefore keep the rule live, which is not the ruled
   vacuity. Ruling: the whole bridging rule is vacuous until the first real
   assumption row, and the exception comes out of the three amended cells.
   The builder's LLR-224 finding, which Sol confirmed, is folded into the same
   follow-up: its `detail` says "absent" where the shared predicate reads "no
   real row". It is amended in place so WI-664's joint adjudication judges it
   with the rest.

4. **WI-652's first round — split three ways.**
   - (i) *Quiet measurement, figures and log — INTEGRATOR.* Sol held the item
     incomplete because the three quiet runs, the CLAUDE.md and skill figures
     and the log rationale were missing. The coordinator had reserved those
     for landing, because a quiet measurement cannot be taken while builders
     share the box. So they are the landing's duty, not a builder defect, and
     the item does not close until they are done.
   - (ii) *Approved Smoke evidence moved slow-only — SOL, in part.* The
     governing text is D31 (spine map §6): each Smoke test case sits in a fast
     in-memory module. The builder brief defines fast as no scaffold, no
     subprocess and no git. An approved row's `tier` cell must stay true, so
     each affected case either keeps fast evidence for its in-memory clauses
     (moving the traced `evidence` pointer), or has its `tier` amended to Full
     in place for WI-664's joint adjudication where a clause inherently drives
     git or a subprocess. The thirteen older mismatches predate this item and
     are filed separately.
   - (iii) *Representativeness — SOL.* This is the owner's stated condition
     on OI-92 (b). The seven scripts left with no per-commit exercise keep
     cheap direct pins for their pure seams.

   WI-652's fix round (`sol-wi652-fix.md`): SOUND. Six test cases have their
   `tier` amended from Smoke to Full in place (TC-135, TC-170, TC-164, TC-178,
   TC-192, TC-206), left Approved for the joint adjudication. TC-157 and
   TC-245 keep fast evidence and stay Smoke.

5. **WI-662 — no dispute.** Sol: SOUND.

6. **WI-660's parse-failure fallback — SOL.** The builder kept one fallback:
   an unparseable `.toml` needs text is read by the markdown heading scan. Its
   argument was that this only over-reports drafts, and that `load_needs`
   refuses the file on the same run. The Done-when says "no text-based carrier
   guess remains on that path", and the fallback is exactly such a guess.
   Sol also showed the safety argument fails on one path: `spine_rules.load_spine`
   never calls `load_needs`. There, malformed TOML carrying an SN id without a
   markdown draft heading yields an id and no draft, which can raise the
   derived stage. Ruling: dispatch strictly by carrier and fail closed on a
   parse failure, with a refusal pinned through the stage path. Sol's minor
   finding (`needs_from_text` keeps the same sniff) is its own item.

7. **WI-664's first round — SOL, both findings.** TC-137, which received
   TC-144's scratchpad clause, still says a stranded claim stops the run and
   that NEEDS-HUMAN exits 7 with the claim parked. LLR-143 says the same.
   `tests/test_dispatch.py` pins the reverse. The contradiction predates this
   item, but TC-137 is now one of WI-669's amended rows, and an adjudicator
   bound to bless only text true of the code would return it. The cheaper
   route is to amend LLR-143 and TC-137 to the tested behaviour now and add
   LLR-143 to WI-669. LLR-140's rewritten claim clause claimed "before
   anything is written" (the helper creates its scratch worktree first) and
   transcribed IF-186's steps. It is cut to the claim-specific scope and
   cites IF-186 for the rest.

   WI-664's second round found one more stale TC-137 clause, the old
   candidate bar that the refresh bar has replaced. The coordinator asked for
   a clause-by-clause pass over TC-137 and LLR-143 against `dispatch.py`, and
   it corrected six more clauses. The third round (`sol-wi664-fix2.md`) was
   SOUND. WI-660's fix round (`sol-wi660-fix.md`) was SOUND.

8. **WI-649's first round — SOL, both findings.** The new PROCESS.md §4
   paragraph named the loop-trailer refusal as the enforcer of the whole
   rule. The trailer only marks loop commits. The held-status refusal is a
   separate, marker-dependent step, and nothing authenticates an attended
   session's recorded delegation. The ruling OI-86 records accepted that risk
   ("even if it inherently incurs risk"), so the doctrine must say which half
   is mechanical and which is review-enforced, not imply one mechanism for
   both. The existing once-per-file test matches only legacy phrases, so a
   small pin now holds the new statement to one home, with the others only
   pointing at it.

   WI-649's fix round raised one major, split two ways. SOL: AGENTS.template.md
   carries a §4 pointer and was missing from the pin's pointer homes, so
   deleting that pointer went unseen. INTEGRATOR: Sol also asked the pin to
   catch a paraphrased restatement. Phrase-pinning is the kit's standing
   method (`test_gate_policy` does the same), and a detector that no
   paraphrase could slip past cannot be built honestly. A reworded
   restatement is for review to catch.

9. **WI-661 — SOL, all three.** A message that knows the row must print it.
   A literal `--reattests <ROW-ID>` pasted from `intake.py`'s refusal is
   itself refused by `parse_reattests`. The two off-spine census notes, which
   say a copy happens only on a Status move or `--approves`, became false the
   day `--reattests` also copied. The acceptance-record mirror findings still
   send a user to a bare `snapshot` that refuses. The tests now assert that
   each false sentence is gone as well as that the new one is present.

10. **WI-577 — SOL, all four.**
    - The `.agents` skill copy was stale. The branch also needs a rebase onto
      WI-649's ledger.
    - The brief's heading still promised that every row owes a human act.
    - Released-rung re-attestation, which the approval-act plan's §2a
      requires, was never exercised by a test.
    - IF-224 was allowlisted instead of cited. The builder's reason, that no
      spine row states this rendering, is the gap itself. The standing rule
      is never to sanction a check to green a step. So an approved test case
      covering the brief cites it, or a Drafted design row and test case state
      the ruled rendering and go to a first-approval adjudication.

11. **WI-669's adjudication, cross-reviewed — SOL on the defect, INTEGRATOR on
    the remedy.** An independent Fable adjudicator ruled all 25 amended rows
    MEANING and blessable, having run 689 targeted tests, and re-anchored
    them. Sol found that SR-209's chain is inconsistent. Its blessed
    acceptance states wave-2 ruling 4's lane-ownership rule: a person's commit
    in a loop lane is judged. Its `requirement` sentence still scopes the rule
    to "a commit the unattended loop creates", and TC-242 still expects a
    non-loop commit to pass. Narrowing SR-209 back would contradict ruling 4
    and the built code. The blessed acceptance is true of the code, so the
    re-anchor stands. The defect is in the rows around it, and the kit's
    ordinary amendment route fixes that: WI-673 amends SR-209's requirement
    and rationale and TC-242, and files their own adjudication. Holding the
    other 24 rows back would also hold the C1 sitting, for a defect none of
    them carries.

12. **WI-661's fix round — SOL, all four, correcting the coordinator.**
    Ruling 9 told the builder to print the known row id in `intake.py`'s
    refusal. The refused row can be Drafted, and a Drafted row is approved by
    a Status change, not re-attested, so the message now picks its remedy by
    the row's status. The prescribed `--approves` argument must be the
    canonical registry token the resolver accepts, because a CSV carrier's
    path is refused. The census names a move INTO approval, or a row arriving
    approved, as the trigger; a de-approval never copies.

13. **WI-577's fix round — SOL.** The follow-up drafted LLR-259 and TC-252,
    and both said the brief at a default dial is "unchanged". The title and
    instruction now change at every level. The true invariant is that no
    collapsed block renders and every owing chain stays in the owner's
    section.
    WI-577's third round (`sol-wi577-fix2.md`) was SOUND.

14. **WI-661's third round — INTEGRATOR on the one minor.** Sol found the
    census test's comment claiming each copy trigger is driven, with no
    citation for `--approves` or `--reattests`. Both are driven already, in
    `test_an_explicit_APPROVES_ref_authorises_it_and_is_RECORDED` and in
    `test_an_AMEND_PLUS_FLIP_authorises_ITS_OWN_row_and_no_other`, which
    asserts the copied bytes. The integrator added the citations at landing
    rather than duplicating those tests.

15. **WI-643, the C1 sitting commit, first round — split.** It was made by
    the owner's Fable stand-in under the recorded delegation.
    - (i) *STK-01..04 absent from `acts.toml`'s approved rows — SOL on the
      gap, INTEGRATOR on the remedy.* The ledger row-records only the tiers
      in `baseline_snapshot.SNAPSHOT_TIERS`, which lacks the stakeholder
      tier, as it lacks the need tier (OI-91 funded WI-651 for the latter).
      Adding a tier is a build, not a sitting act. WI-651 is extended to the
      stakeholder tier. The sitting's STK approvals are recorded in the
      stamp's ref and in the Decisions entry.
    - (ii) *The REL growth floor lowered 1 -> 0 — SOL.* That weakened a
      ratchet so the ruled frame would pass. The locked tier is exempted, and
      the exact-one pin in `tests/test_external_frame.py` stands guard.
    - (iii) *An added "two systems of interest" header paragraph — SOL.* A
      sitting writes only the signed text or a disclosed reconciliation.
    - (iv) *Log fragment and derived views — INTEGRATOR.* They were reserved
      to the integrator by instruction.
    - (v) *Stale `test_intake` docstrings — SOL.*

16. **WI-643's second round — split.** Sol held that two header additions
    exceed §1.3's signed text.
    - SOL on the `mediates` entry's added sentence ("Its one reader… grants
      no authority"). It is true, but it is not signed.
    - INTEGRATOR on the FLIP AUTHORITY rewrite. Package §4 says both
      comments that paraphrase the old dial "are rewritten in the same commit
      to point at the dial instead of restating it", and deleting §1.3's
      sentence bare would leave a broken sentence. A pointer to the dial is
      exactly what the owner accepted.
    The act is re-taken once more, so the ledger holds one act for the
    sitting.

17. **WI-650 — SOL, both.** Association-aware dating reads design rows'
    SR-Refs from history. So the unreadable-history guard must cover the
    design registry, or an LLR registry still on an older carrier silently
    drops the test cases it would reach. That is a pass by omission, which
    SR-217's "unreadable history never passes" forbids. The kit README's row
    describing the check is updated to match. The builder placed the owner's
    addition (the not-approved warning) as an SR-217 clause, not a derived
    row, arguing that SN-042's acceptance already covers a never-approved
    test case. Sol raised no objection, and the coordinator agrees.

18. **WI-673 — SOL.** SR-209's rationale kept a sentence from before the
    floor existed: trailers "today appear on some of its commits and nothing
    checks them". It is false now, and an amended row is judged whole, so the
    sentence is made counterfactual. The fix is one sentence in a row that
    WI-676's independent adjudicator judges next. The coordinator takes that
    judgement as the confirmation round rather than running a separate Sol
    round.
