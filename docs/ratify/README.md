# Re-attestation briefs — and the retired vocabulary they preserve

This directory splits into a live surface and a history (WI-503):

- **`CURRENT.md`** is the one file `trace.py --ratify modified` ever
  regenerates (`--out docs/ratify/CURRENT.md`), and the harness's
  `ratify-fresh` step freshness-gates it — a stale `CURRENT.md` is what a
  human is about to attest FROM, so the gate fails closed.
- **`<date>-<slug>.md`** files are **IMMUTABLE once minted**: `trace.py
  --mint-ratify-brief SLUG` copies `CURRENT.md` to a dated name at the
  moment of a sitting, and never touches an existing one again. The
  `ratify-immutable` harness step refuses any STAGED commit that modifies or
  deletes an already-committed dated brief — a plain add of a brand-new name
  is the only change it permits. A dated brief is the record of what a human
  actually read when they signed; rewriting it in place (the pre-WI-503
  defect — one file rewritten ten times, never about the WI it was named
  for) defeats the one thing it exists to do.

Every brief quotes registry cells **byte-for-byte at a pinned baseline** so an
owner can see exactly what changed between the attested revision and the
working tree.

**RETIRED VOCABULARY, PRESERVED VERBATIM (OI-21, ruled 2026-08-13).** OI-21
retired the `G0`/`G1`/`G2`/`G3`/`G-Release`/`G-Final` tags for the eight-rung
stage ladder, and every live authored surface converted. **These briefs did
not**, and this directory is a declared carve-out in
[`check_vocab.py`](../../project-trajectory/scripts/check_vocab.py):

- A brief is a **quote**. Rewriting the vocabulary inside a byte-for-byte quote
  makes it misquote, which defeats the one thing the brief exists to do.
- A brief records a boundary a **named human** was asked to bless under the name
  it had at the time.

Read a retired tag through the translation (`docs/process.md` §4 states it
canonically):

| retired tag | the ladder today |
|---|---|
| `G1` | the `DevBar-Reqs` bar — rungs `DevStg-Needs` … `DevStg-Reqs` |
| `G2` | the `DevBar-Tests` bar — rungs `DevStg-Arch` … `DevStg-Tests` |
| `G3` | the `DevBar-Release` bar — rung `DevStg-Impl` |
| `G0` | `DevBar-Below`, the internal below-the-floor sentinel (never a bar) |
| `G-Release` | the `DevStg-Release` rung |
| `G-Final` | the owner's final read (`final_review`), which is its own dial |

The same carve-out covers [`docs/log.md`](../log.md)'s dated sign-off and
ratification entries, and [`docs/archive/`](../archive/README.md).
