# redesign-authoring-closure — adversarial review

Requested route: Opus 5, high; declared CLI stream-json pattern.

Subject SHA256: `fde13e7ba27d4e3a91dc0d983868b57bd7ff9551b2a8fe967487ea55ecb66af2`

Tracked invocation: [session log](../iteration/call_9bbbb1b369b747398584091107eba858-20260906-111724.log).

Review uses supplied source with tools disabled. It is an independent
assessment, not a requirement approval or a test execution.

## Closure review — 21 authoring findings

No tests run; I read only the supplied records and LIVE cells and claim no result.

**Closed on the supplied evidence (16 of 21):** 1 (LLR-048 `sr_refs` back to `["SR-154"]`), 2 (SR-162 transient half stripped, durable boundary kept), 3 at the SR tier (SR-184 AC now rejects a TC-copied rubric), 4/13 (SN-007 acceptance carries the declared bar + scaffold/every-script promise only), 5/6 (procedures in durable `docs/test/inspection-procedures.md`; `method`→procedure, `evidence`→explicitly-pending result), 7/20 (reviewer prompt preserves parent acceptance/approval and requires child re-attestation; "behavioral regression tests" used in PROCESS and prompt), 8 (intro's "that classification, not the fix, is step 1" restored and aligned to node `C`; `D` follows), 9 (add-only preservation distinguished from operator restore/merge + conversion; nothing attributed to `--force`), 10/19 (SN-007/SN-026/SR-162 named as re-attest debt; H1/H4 read as authored), 11/12 (SR-186 binds what the process requires and records; both re-homed AC clauses gone — the retained "while retaining the required tiers" reads as a non-derogation limit, not a second home), 14, 15 (verified against `hats.toml`: `legal`→LEGAL, `personal-data`→DATA-PROTECTION, and the composer declares a need's own `tags`), 16, 17 (PERFORMANCE dropped; remaining cells match `listens_for`), 21's `aspect` and O1–O6 answers.

### Still open

- [MAJOR] `docs/test/test-cases.toml` TC-209 `expected`/`method` -> the finding-3 fix landed only at SR-184; the TC's abnormal arm still enumerates *missing* reviewer/rubric/intent/anchor, and `expected` reads "each missing required field is found" — a rubric that names its sources but was copied from the verifying TC passes -> add that present-but-underived case to the method's abnormal enumeration and to `expected` -> @owner
- [MAJOR] `docs/test/inspection-procedures.md` §H5 + TC-211 `expected` -> the counterexample ("a child that only paraphrases or duplicates") is constructed and then never adjudicated: the procedure's next sentence states the *normal* obligation ("Record why further splitting stops…") and `expected` requires only that the record state the stopping reason. SR-186's first AC clause has no failure outcome -> add "a child within a required tier with no independent decision or verification purpose is an Inspection finding" to both -> @owner
- [MINOR] `docs/test/test-cases.toml` TC-210 `method` -> `#h3-inspection-procedure-requirement-interface-change` does not resolve; GitHub drops `/` outright, so the heading "H3 Inspection procedure requirement/interface change" slugs to `…procedure-requirementinterface-change` -> reword the heading to "requirement and interface change" and update the cell (H2/H5 and all three result anchors are correct); while there, confirm `README.md#project-vision` resolves for the P0 record's O1–O6 link -> @owner
- [MINOR] `DECOMPOSITION-AMENDMENTS.md`, closing paragraph -> "The final authoring review's corrections are applied here as an unapplied patch" is self-contradictory and false against the LIVE rows, which already carry every correction -> "…are applied to the live rows and to this record; no Status or approval snapshot is changed" -> @owner
- [MINOR] `P0-ADOPTER-REVALIDATION-REVIEW.md` fixture basis -> "plus the continuation changes" is still un-re-derivable, and the deferral is recorded only in the dispositions file, not where the claim lives -> add one clause noting the source stamp is owed by the follow-on commit -> @owner

None of these adds a form, schema, field, or checker; all five are edits to existing cells.

VERDICT: CHANGES-REQUESTED findings=5
