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
