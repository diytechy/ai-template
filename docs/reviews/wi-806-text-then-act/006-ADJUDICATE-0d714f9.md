# 006 — ADJUDICATE (independent, Claude Opus) — WI-806 amended approved rows at `0d714f9b`

Adjudicator: independent Claude Opus, the adjudicator of 003 and 004. I wrote
none of WI-806's code or rows. This is the fresh ruling 004 required on the
landed amendment text. Anchors: `docs/archive/last_approved/`, LLR and TC as
last copied on trunk `7db81c98` (WI-822's act 33 re-copied both registries, and
LLR-173, LLR-245 and TC-173 read there as at `7e001ccc`). The basis shared with
the first approval is in `005-ADJUDICATE-0d714f9.md`.

## Basis (probed, not trusted)

- **The landed text equals the bytes 004 would bless.** By script at
  `0d714f9b`:
  - LLR-173 `detail` and TC-173 `method` and `evidence` equal 004's fenced
    blocks.
  - LLR-173 `rationale` and LLR-245 `detail` are unchanged since 004 ruled
    them, and both are 002's replacements byte for byte.
  - TC-173 `expected` and `verifies` (`SR-179;LLR-178;SR-140;LLR-302`) are as
    ruled.
  - No `Status` cell moved, and TC-173 reads `Approved`.
- **TC-173's evidence is complete and live.** All 25 cited nodes exist. The
  added node is the owed test, which kills M15 (005), so every clause of (f)
  now has a node that kills its mutant. That includes:
  - the record-path half of "judged by what neither parent carried";
  - the stale-message clause, which now matches its cited test: an abandoned
    squash exempts a direct commit staging the tip's own registries and record,
    judges plainly one staging any other spine text, and is gone after the next
    commit.
- **LLR-173's pointer now covers every commit LLR-302 admits.** "Except for the
  root and a commit that LLR-302's squash exemption admits" includes the
  abandoned-squash commit that 004 found the old phrase left out.
- **LLR-245** was blessed in 004 and is unchanged. The code it describes is
  unchanged since 004 (`baseline_snapshot.py` has an empty diff over
  `44c9ddfd..0d714f9b`).
- **LLR-298** changed only a traced cell (`code_symbol`). It is not drift and
  owes no act, as 004 ruled.

## Rulings

- [MEANING] LLR-173 detail -> before: the record's copy contract, the unanchored rule, three refusals, a git-derived stamp and SR-140's two record fields, with no ordering of text against the act -> after: the approval-act rows' text the copy records was committed before the act that writes the copy, which changes only Status and adds or removes none, except for the root and a commit LLR-302's squash exemption admits; the off-spine registries are outside that ordering -> MEANING: a copy taken in an amend-plus-flip commit satisfied the old text and fails the new. The `rationale` change is clarity. **Blessed:** the text is true of the code and points at LLR-302 for its enforcement and exceptions, without restating them. Re-attested in the act.
- [MEANING] LLR-245 detail -> before: absorbed rows minus the rows the act flips minus the rows named by --reattests -> after: absorbed rows (a copy claiming approval whose approved cells moved or whose row live dropped; a flipped row's copy reads below approval, so it is never absorbed) minus the rows named by --reattests -> MEANING, as 002 and 004 ruled. **Blessed** as 004 ruled. Re-attested in the act.
- [MEANING] TC-173 method/evidence -> before: the mirror-invariant suite, (a) to (e), verifying SR-179 via LLR-178 -> after: adds (f), the text-then-act suite (two-tree refusal, merges judged by what neither parent carried, a record only one parent wrote not the merge's own, the content-verified squash exemption and its abandoned-squash residue, unreadable parent and diff, root), verifying LLR-302 too -> MEANING (a new acceptance condition and a newly verified row). **Blessed:** every clause is a condition a cited node observes, and every LLR-302 clause has a killing node. Re-attested in the act.

## Aftermath (taken in the lane, uncommitted; the coordinator commits it after the verdicts)

LLR and TC sit on a rung the declared gate authority releases, so the
re-attestations are mine. In one act commit that changes only `Status`:

- LLR-302 flips `Drafted` -> `Approved` (005);
- LLR-173, LLR-245 and TC-173 are re-attested, naming this verdict.

The test-cases registry enters scope through TC-173's re-attestation.

```text
python project-trajectory/scripts/intake.py snapshot --approves "docs/requirements/low-level-requirements.toml=WI-806" --reattests LLR-173,LLR-245,TC-173 --verdict docs/reviews/wi-806-text-then-act/006-ADJUDICATE-0d714f9.md
```

VERDICT: MEANING rows=3
OUTCOME: APPROVE rows=3
