# Knowledge packs (`docs/knowledge/`)

A **knowledge pack** preserves project-specific findings that should outlive the
session or work item that produced them. Use one Markdown file per topic; its
filename (without `.md`) is the label that a component registry's `Knowledge`
cell may reference.

## Pack contract

A pack records only context the requirement registries cannot hold: evidence,
decision rationale, vendor or tool quirks, failed approaches worth avoiding, and
external references with retrieval dates. Link to `SN-`, `SR-`, `LLR-`, `TC-`,
`IF-`, or `CMP-` ids instead of restating their facts, and link to generated
architecture views instead of copying them.

Packs are advisory context, never gates. When a finding becomes a rule,
constraint, or requirement, promote it through the change-intake flow in
[`process.md`](../process.md) so the requirement spine remains authoritative;
keep the rationale and evidence trail in the pack.

A durable module description is the component row plus its `Knowledge` and
`DetailDoc` references. Do not create a parallel component specification inside
this directory. The optional research-track workflow is described in
[`process-options.md`](../process-options.md).

## Pack index

Add every pack here so documentation checks can discover it.

| Label | Topic | Components | Last reviewed |
|---|---|---|---|
| [`example`](README.md) | Replace label and target with the pack file | `CMP-000` | YYYY-MM-DD |
