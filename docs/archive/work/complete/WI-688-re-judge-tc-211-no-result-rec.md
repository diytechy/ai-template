+++
id = "WI-688"
title = "re-judge TC-211: no result recorded [sha256:aa064ee9542c] at merge 77fb093"
workstream = "process"
sr_refs = ["SR-186"]
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "rejudge"
adjudicates = ["TC-211"]
+++

## Deliverable

TC-211 **RECORDED pass** (`docs/test/observations/TC-211.2026-10-03T210347Z.toml`), after the SR-161 producer it was waiting on was built. The S11 in-lane cycle ran end to end:

1. **Build (steps 1-2).** A Claude Opus builder wrote a design note, which the coordinator approved, and then built it. `hats.py record` writes a per-decomposition `<stem>.perspectives.toml`:
   - applicability and production are derived;
   - a no-finding is authored;
   - `--check` reports MISSING, STALE and CONFLICT. It is warn-first, `--strict` exits 1, and no gate means no adopter migration.

   It also wrote the record for the SR-184/185/186 decomposition TC-211 inspects. New rows: LLR-297 and TC-312. Amended: LLR-183's last clause, TC-211's `inputs` and IF-133's data cell.
2. **Review and fix rounds, in the lane.**
   - Codex Luna's MAJOR: authorship was not enforced. Fixed in fix round 1.
   - An independent Opus adjudicator returned LLR-297 and TC-312: 12 of 14 mutations survived the tests. Fixed in fix round 2 with byte-exact cells and 10 test cases; all mutations are now caught.
   - Luna's final-review MAJOR: TC-211's undeclared inputs. A one-cell coordinator fix.
3. **Acts in the lane.**
   - Act 26: LLR-297 and TC-312 approved; LLR-183 re-attested (CLARITY).
   - Act 27: TC-211 re-attested (MEANING, blessed).
4. **Judge (step 3) through the kit's own session path.** `agent_loop --wi WI-688` ran OPENAI-TERRA (gpt-5.6-terra), cross-family, in 301 s. Its verdict is at `docs/reviews/wi-688/001-ADJUDICATE-9e260e1.md`, and the session log is `docs/iteration/wi-688-001-20261003-160206.log`, which feeds WI-541's occupancy measurement.

Reviews: `docs/reviews/2026-10-03-wave9/luna-wi688-r1.md` and `luna-wi688-final.md`. Verdicts 002-004 are under `docs/reviews/wi-688-re-judge-tc-211-no-result-rec/`.

## Context

The merge checkpoint at 77fb093 found observation test case TC-211 due for re-judging.

- What changed: no result has been recorded for it.
- Method: Follow the decomposition proportionality inspection in docs/test/inspection-procedures.md#decomposition-proportionality-inspection; inspect the complete chain and an extra paraphrasing child.
- Expected: A child within a required tier with no independent decision or verification purpose is an Inspection finding; otherwise the review records that independent value and why further splitting stops.
- Declared inputs: docs/test/inspection-procedures.md; SR-186
- Result lifetime: 90 days
- Latest result: none
- Inputs digest at 77fb093: sha256:aa064ee9542c8e0a739956123890095f8f44aa74e05f96bcc41f96c70c2ca7fb

The check that filed this hashed the declared inputs and ran no model. Re-judge the case by its Method and record the result with `python scripts/record_observation.py --tc TC-211 --outcome pass|fail --by "<who or what observed>"`.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- TC-211 -> docs/test/inspection-procedures.md#decomposition-proportionality-inspection-result
Judged 2026-09-28 (`docs/reviews/wi-688-re-judge-tc-211-no-result-rec/001-ADJUDICATE-fe96ec6.md`, confirmed by Codex Sol): `OUTCOME: NEEDS-JUDGEMENT result=-`. Both of the Expected's clauses hold on the half of the sample that exists. The Method also reads the decomposition's SR-161 applicability or no-finding record, which LLR-183 states is not yet produced. The owed act is to ship the SR-161 producer, produce the record for this decomposition, re-run the procedure over the complete sample, and record. This row stays open so that the merge checkpoint does not re-mint it (wave-5 ruling 31). Folded (the adjudicator's finding, upheld by Sol): `docs/test/inspection-procedures.md` hand-restates earlier results inside a declared input, while `docs/test/observations/` is the one writer; a hand refresh of that prose stales the records it reports. Whoever re-runs this procedure replaces the result prose with a pointer to the observation records, and re-records the cases that file's change stales.


## Scope folded 2026-09-30 (owner: "fold it into WI-688")

The owed act above names an SR-161 producer that no row builds (LLR-183 records
it "NOT DISCHARGED": the per-decomposition artifact does not exist). That build
is this row's scope, not a separate row. Order:

1. Ship the SR-161 producer: a decomposition round writes a machine-readable
   perspective record beside its artifacts, distinguishing not-applicable from
   considered-with-no-finding, and an applicable declared perspective missing
   from it is reported (SR-161's acceptance criteria). Amend LLR-183 (and its
   TC) for the half it declares undischarged; those are Drafted amendments and
   follow the artifact adjudication route. Keep the scope proportional to the
   missing obligation.
2. Produce the record for the decomposition TC-211 inspects.
3. Re-run the proportionality inspection over the complete sample, replace the
   result prose in `docs/test/inspection-procedures.md` with a pointer to
   `docs/test/observations/`, and record with `record_observation.py`.

`safety_class` stays `adjudication`; the build step (1) is ordinary work inside
it, so the claimant should treat steps 1 to 2 as a build and step 3 as the judge.

## Carried from status.md at the claim (2026-10-03)

Follow the existing artifact adjudication route for the Drafted amendments; passing an
Inspection does not approve its requirement. Keep the scope proportional to the
missing obligation. Under the owner's S11 direction (2026-10-03), an adjudication
return on this lane is fixed inside the lane and re-judged, not minted as a follow-up
row. A redundant amendment row the landing sweep then mints (the re-mint trap) is
closed by citing the act.
