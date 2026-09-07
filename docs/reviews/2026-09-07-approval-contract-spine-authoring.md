# 2026-09-07 — approval repair spine authoring

This is an exclusive authoring record, not an approval. It applies the surgical
amendments approved as a design in
`docs/reviews/2026-09-07-approval-contract-luna-round-3.md`, whose reviewed
contract SHA-256 is
`b5295cec53caa2078aa1ade53d9322022052637a05b9ac6775aa9f4813757105`.
No Status, snapshot, runtime file, or approval record was changed.

## Exact authored cells

Only these normative cells changed:

```text
docs/requirements/low-level-requirements.toml
LLR-140 Detail
LLR-152 Detail
LLR-153 Detail
LLR-154 Detail
LLR-158 Detail
LLR-167 Detail
LLR-207 Detail

docs/test/test-cases.toml
TC-146 Method
TC-147 Method
TC-148 Method
TC-153 Method
TC-161 Method
TC-205 Method
```

Every unlisted cell is byte-preserved, including each row's Status, Rationale,
references, tier and evidence. No CodeSymbol changed because the implementation
has not yet established an exact new callable to trace.

The exact diff is the Git worktree diff at these locations:

```text
docs/requirements/low-level-requirements.toml:1382  LLR-140 Detail
docs/requirements/low-level-requirements.toml:1526  LLR-152 Detail
docs/requirements/low-level-requirements.toml:1538  LLR-153 Detail
docs/requirements/low-level-requirements.toml:1550  LLR-154 Detail
docs/requirements/low-level-requirements.toml:1598  LLR-158 Detail
docs/requirements/low-level-requirements.toml:1709  LLR-167 Detail
docs/requirements/low-level-requirements.toml:2187  LLR-207 Detail
docs/test/test-cases.toml:1436  TC-146 Method
docs/test/test-cases.toml:1447  TC-147 Method
docs/test/test-cases.toml:1458  TC-148 Method
docs/test/test-cases.toml:1513  TC-153 Method
docs/test/test-cases.toml:1601  TC-161 Method
docs/test/test-cases.toml:2083  TC-205 Method
```

## Blob binding

```text
low-level-requirements.toml
baseline HEAD blob: e288f6f9ca2854bc6e54382c1ac79637ed083b39
authored worktree blob: 389f025681849fe080bd4bf8ba4d97e89a5fbb48

test-cases.toml
baseline HEAD blob: 738ab7eca9cb4d63c0434d4edf7a66dc344fab5d
authored worktree blob: bf1765cc6404c7451becdae7ea8e9bf5268e5eb3
```

The TOML parser accepts both authored files. A parsed before/after comparison
reports exactly the thirteen row/cell pairs above and no others.

## LLR-167 and WI-603

LLR-167 already differed from its approved snapshot before this authoring. The
new primary-turn wording is added to that same live cell; it does not discard or
silently resolve the pending change. WI-603 remains the owner of LLR-167's
amendment judgment and must compare the approved snapshot against the complete
authored `Detail` now bound by blob
`389f025681849fe080bd4bf8ba4d97e89a5fbb48`. Its existing scope, evidence and
identity remain pending; no approval is inferred from this authoring record.

## Required next act

An independent adjudicator must inspect the exact live cells, their complete
chains and this before/after binding. Runtime implementation must not begin from
these amendments until that judgment accepts them through the applicable
authority. Snapshot files remain the prior approved baseline.
