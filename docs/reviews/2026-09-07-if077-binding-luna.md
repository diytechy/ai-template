# IF-077 binding review — 2026-09-07

Decision: **APPROVE** the physical binding update.

`primary_turn._definition` imports and calls the existing
`check_docs.blank_fenced` API to obtain line-preserving text with fenced code
hidden before recognizing `## Approval` and `## Dispositions` headings. This
prevents a fenced `##` comment from changing the proposal definition while
preserving the existing line and section behavior.

IF-077 remains owned by `scripts/check_docs`, with its existing `version =
"v1"`, `status = "Drafted"`, component and contract meaning unchanged. The
physical requestor addition is `scripts/primary_turn`; the data description
now names the already-used `blank_fenced` operation. The live interface file
SHA-256 at review is
`5db6d8aede6ec3c1e55a467fda0139568b3699f52ffa6698981ef8f439d269c3`.

This is an implementation trace binding only. It grants no approval waiver,
does not alter authority or scope, and does not approve any live registry or
snapshot cell.
