# 2026-09-07 — approval impact carrier clarification

This is a design-only authoring record, not an approval. The impact schema's
general candidate-blob rule is impossible for the selected queued spec because
that spec contains the rule's own `source_blob` value in `## Approval`.

The exact clarification uses the immutable `proposal_spec_blob` for that one
selected-spec `(id, path)` pair. Primary validation proves the proposal's
frontmatter and definition outside the two judgment sections are unchanged;
the final review separately binds the actual candidate sections. Every other
tracked pair still uses its reviewed-candidate blob, and the selected-spec pair
remains in the complete census.

No live LLR or TC cell required amendment: their governing obligations require
complete tracked-use census and exact candidate binding but do not prescribe
the per-path `source_blob` representation. No runtime, snapshot, Status,
approval payload, queued WI, or prior review artifact changed here.

The independently reviewed design before this clarification had SHA-256
`89f61c67cab0a8dcfbb3cf05bad615ee58b94fca3b7b7cbcc4ceab586751cc42`.
Independent judgment must review the new exact design hash reported with this
artifact before implementation relies on the exception.
