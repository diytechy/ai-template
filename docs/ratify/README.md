# Re-attestation briefs — and the retired vocabulary they preserve

The `*.md` files beside this one are **generated** by `trace.py --ratify` and
freshness-gated by the harness's `ratify-fresh` step. They quote registry cells
**byte-for-byte at a pinned baseline** so an owner can see exactly what changed
between the attested revision and the working tree.

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
