# 2026-09-07 — approval repair spine authoring round 3

This is the final narrow authoring record before independent exact judgment. It
grants no approval. It clarifies the existing blank-Brief adjudication route and
the existing Git author/committer distinction; it creates no actor registry,
route field, legacy adjudication worker path, or new lifecycle phase.

## Exact authored cells

Only these normative cells changed in this round:

```text
docs/requirements/low-level-requirements.toml  LLR-167 Detail
docs/test/test-cases.toml                       TC-161 Method
```

Every other registry cell is preserved from round 2, including all Status and
CodeSymbol values. SR-140, LLR-173 and TC-167 are unchanged. No snapshot,
runtime source, queued WI, or prior review artifact changed. WI-603 remains the
owner of the complete pending LLR-167 before/after delta.

The authored route has these exact boundaries:

- A blank-Brief adjudication receives a generic primary judgment assignment
  bound to turn, queued WI, base, candidate and scope and naming its verdict
  path. It carries no claim, branch, model-side close or snapshot instruction.
- A declared Brief whose assembler fails remains HELD. It never falls through
  to the blank-Brief assignment.
- Ordinary non-adjudication work retains its worker assignment. There is no
  retained legacy adjudication-worker context.
- Automatic publication derives the canonical machine Git author only from the
  actual committed ADJUDICATE log's provider, roster row, model, session id and
  invocation identity bound to the turn. Ambient or configured Git identity is
  not evidence, and an automatic human-looking identity refuses and surfaces.
  A real human remains author only through the existing manual primary path
  with the actual human act bound. The coordinator remains committer.

## Blob binding

```text
APPROVAL-REPAIR-CONTRACT.md
round-2 SHA-256: ee050ae995f56167a16bc0b58b50c9450c760904188ab6101f93e65582ea0968
round-3 Git blob: d8f8263553f4aa8ea04c6908834758b3f425ef3c
round-3 SHA-256: 89f61c67cab0a8dcfbb3cf05bad615ee58b94fca3b7b7cbcc4ceab586751cc42

low-level-requirements.toml
round-2 authored blob: c06d321c1f434b3dded889b5165379526f322a03
round-3 authored blob: e819616aa75be76fc84d6cfbf063551d92b7f5ef

test-cases.toml
round-2 authored blob: eb68c97f8999e9ea4cf958a856257b9826865cbd
round-3 authored blob: 354a27de0df76fa86c195d023d7b835bdd25d4d6
```

Both registries parse as TOML. Independent judgment must review these exact
round-3 identities and the combined WI-603 LLR-167 delta before implementation
relies on the amended cells.
