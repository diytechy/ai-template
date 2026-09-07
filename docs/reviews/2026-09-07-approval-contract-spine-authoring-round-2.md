# 2026-09-07 — approval repair spine authoring round 2

This is a narrow authoring record, not an approval. Luna's independent review
accepted the smaller RETURN resolution: an unpublishable requested approval is
returned with no accepted cells or snapshot, while a later complete-scope
reanchor remains the approval act. The clarification preserves the owner's
same-commit approval and snapshot rule and adds no publication phase.

## Exact authored cells

Only these normative cells changed in this round:

```text
docs/requirements/low-level-requirements.toml  LLR-153 Detail
docs/test/test-cases.toml                       TC-147 Method
```

The design contract gained matching explanatory and test clauses. Every other
registry cell, including Status and CodeSymbol, is preserved from round 1. No
snapshot, runtime source, queued WI, or prior review artifact changed.

The new clauses require this exact fail-direction:

- A requested approval blocked by another scoped owner's `UNJUDGED` or
  out-of-scope registry drift cannot publish accepted cells or a snapshot.
- The adjudicator may revise it to RETURN with zero accepted cells and a
  concrete reanchor or corrective continuation whose dependencies preserve the
  existing scoped owners. That RETURN closes atomically without Status or
  snapshot effects.
- Equivalence observations in the RETURN remain findings and evidence. They
  are not accepted judgment refs. The later complete-scope reanchor independently
  judges every cell before the whole-file approval and snapshot publication.
- A malformed or inconsistent projection is still a mechanical refusal and
  leaves the same pending turn for REWORK; it is not silently converted to
  RETURN.

This permits WI-605 to follow its own recorded instruction to RETURN when the
WI-601 and WI-603 judgments are unavailable, while preserving those WIs as the
owners of LLR-061 and LLR-167. A later precisely scoped reanchor can depend on
their completed work and judge the remaining whole-file absorption population.

## Blob binding

```text
APPROVAL-REPAIR-CONTRACT.md
round-1 SHA-256: b5295cec53caa2078aa1ade53d9322022052637a05b9ac6775aa9f4813757105
round-2 Git blob: 1ed651a7a13b290ef530705c555a481820cce21b
round-2 SHA-256: ee050ae995f56167a16bc0b58b50c9450c760904188ab6101f93e65582ea0968

low-level-requirements.toml
round-1 authored blob: 389f025681849fe080bd4bf8ba4d97e89a5fbb48
round-2 authored blob: c06d321c1f434b3dded889b5165379526f322a03

test-cases.toml
round-1 authored blob: bf1765cc6404c7451becdae7ea8e9bf5268e5eb3
round-2 authored blob: eb68c97f8999e9ea4cf958a856257b9826865cbd
```

Both authored registries parse as TOML. Independent judgment must review these
exact round-2 blobs before runtime implementation relies on the clarification.
