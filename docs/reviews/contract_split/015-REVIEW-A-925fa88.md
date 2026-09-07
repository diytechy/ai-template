# REVIEW-A — WI-619 cumulative amendment RETURN (candidate 925fa887)

Reviewer: independent, fresh context (did not author the judgment).
Reading scope: HEAD is trunk itself, so the prescribed three-dot diff against
`contract_split` is empty; the WI-619 commits 3e43db91 (selection), 84a65595
(judgment record) and 925fa887 (Approval/Dispositions + transport manifest) are
the work under review, read as `git diff 5772a835..925fa887`. Records under
docs/reviews, docs/iteration and docs/log.d were read only as the cited
evidence; the adjudicator's summary and telemetry prose were not used as input.

## What the diff does

- Selects WI-619 into the exclusive primary path (turn
  `WI-619-5772a835…`, 52-row scope, proposal spec blob 4df07cf4).
- Commits the typed judgment `014-ADJUDICATE-3e43db9.md`: 52 row findings
  (37 MEANING, 15 CLARITY), four RETURN findings R1–R4, counterpart and
  decomposition reservations, `VERDICT: MEANING rows=52`.
- Fills `## Approval` with 52 `[[decision]]` rows, all `classification =
  "return"`, every `evidence` = 84a65595, before = approved-snapshot blob,
  after = live registry blob; no impact or absorption ledger (all-return).
- Fills `## Dispositions` with one `spine` successor (supersedes WI-619,
  specref = the judgment record, needs WI-608..WI-617) carrying R2–R4 and
  the original Context verbatim.
- Copies the codex delivery manifest into the transport evidence dir and
  retitles its README. No registry, code, test or snapshot bytes change.

## Worst failure classes hunted, in order

1. Silent acceptance under an all-RETURN carrier. Drove the shipped
   `primary_turn.validate` (None at HEAD and at 925fa887) and
   `primary_approval.approval_projection`: with provenance off, outcome
   `return`, `statuses={}`, `approves={}`, 52 findings; with provenance on,
   the sole refusal is `candidate lacks its required independent review
   phases`, which is this round. `_judgment_records` binds exactly one
   record (logged commit 91735823, candidate 925fa887, model gpt-6-astra,
   invocation 821aed6d…) at the candidate's tree identity cc7b8c71…;
   `_machine_author` resolves; `_evidence_refusal` on 84a65595 is None.
2. Row findings that misname the changed cells (silent wrong content).
   Recomputed `absorption_census` over the 52-row accepted set at HEAD and
   compared each row's approved-cell set to the cells the record names:
   0 mismatches over 52 rows. The census's only out-of-scope entries are the
   nine Drafted riders the record lists (LLR-210, SR-183..186, TC-208..211).
   The 32 further Approved LLR rows whose bytes differ from the snapshot
   (LLR-035, LLR-099, LLR-200, …) differ only in traced cells
   (Module/CodeSymbol), so the 52-row scope is exactly the approved-change
   set; the Dispositions' "entire original 52-row scope" is complete.
3. RETURN findings that assert a defect that is not there. R2: verified —
   OBLIGATIONS.md:40 says "IF-091 remains intake; IF-090 remains …" while
   interfaces.toml has IF-090 owner scripts/intake (intake_after_merge ·
   mint_gap_rows · context_block) and IF-091 owner scripts/acceptance_record
   (staged amendment/drafted-row records · lane_approval_refusal); the
   Dispositions' corrected attribution matches the registry. R3: the cited
   `test_a_two_row_batch_close_peels_under_one_canonical_order` is absent
   from tests/ and no longer cited by TC-205.Evidence, as the record states.
   R4: tests/test_primary_publication.py:249-259 compares FETCH_HEAD and
   .git/objects only, while LLR-207.Detail promises "changes no primary ref,
   index or working tree"; the proof limit is real.
4. Row-finding semantics spot-checked against the snapshot→live cells:
   TC-178.Expected now refers SR-161 inspection to TC-211; SR-161.Verification
   Test→Inspection; TC-205.Level Unit→Integration with Tier Full unchanged;
   TC-161.Tier Smoke→Full; LLR-058.Title drops "deterministic traincar
   ordering"; SR-024.Rationale drops the hat.TEST-ENGINEER prefix. All match.
5. Continuation that drops an obligation. The Dispositions' copied Context
   is byte-identical to the spec's original Context (blank-line-normalised
   diff empty). `intake.parse_dispositions` yields one `spine` draft, review
   owed = True under review-policy 1; all seven `needs` are in
   docs/archive/work/complete. The spine→intake-minted-adjudication pattern is
   the one WI-612 → WI-619 already used (WI-619 was minted in 35020525).
6. Counterpart/decomposition reading. The record names each changed side
   with its counterpart (SR-026/LLR-061/TC-061, SR-174/LLR-153/TC-147 and
   LLR-154/TC-148, IF-090/IF-091, SR-178, LLR-159, IF-075, IF-124) and
   records retain-or-carry for each; LLR-167's retained criteria are judged
   as one validity contract with distinct verification purposes. Adequate
   for a zero-effect RETURN.

## Instruments (run once, summaries)

`check.py --jobs 0`: Check summary (stage DevStg-Tests, tier all) — all 12
steps PASS (smoke 60.6s, registry-integrity, derived-stage, vocabulary,
need-form, privacy, doc-navigability, design-flows, trajectory,
approval-fresh, skills-index, prompt-catalog); RESULT: PASS, exit 0.
`trace.py --strict-integrity`: `Traceability: SN=27 SR=79 LLR=192 TC=194
orphans=0 integrity=0 … drafts=17 …`, exit 0.

status.md lines 38/47 ("keep the coordinator paused", no control window)
and 52-54 (`push = "human"`) agree with docs/process.toml
(`human_approval_through = "DevStg-Needs"`, `push = "human"`).

## Findings

- [MINOR] docs/work/queued/WI-619-adjudicate-complete-combined.md:628 -> for clarity: the Dispositions say "Correct the SpecRef packet's reversed IF-090/IF-091 attribution", but the successor's own `specref` is the judgment record, not the packet; the reversed line lives at docs/reviews/wi612-authoring/OBLIGATIONS.md:40 -> name that file path in the sentence so the successor edits the right record -> @coordinator

VERDICT: APPROVE findings=1
