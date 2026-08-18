# Retired gate vocabulary — the `G*` tags

**History, not a working surface.** The `G0` / `G1` / `G2` / `G3` / `G-Release` /
`G-Final` gate tags retired with the eight-rung stage ladder (OI-21, ruled
2026-08-13; the `DevBar-*` prefix that briefly replaced them retired in turn on
2026-08-18, leaving one vocabulary — `DevStg-<Label>` — with the verb carrying
the axis). The live rule lives in
[`../../project-trajectory/PROCESS.md`](../../project-trajectory/PROCESS.md) §4
"The stage ladder"; this file holds the retirement's *record* — the translation
table and the never-reword rule — which the load-bearing core pointed at rather
than carried, once the ladder itself was the thing a reader needed.

Moved out of `PROCESS.md` §4 on **2026-08-18**. Read-side behaviour is unchanged
and is enforced by code, not by this page: `check.py --gate G2` is still accepted
and warns, and `check_vocab.py` still refuses the tags in authored surfaces.

## What survives, and where

The tags survive **only** as read-side aliases, so an adopter's hooks, their
`stack.ini` `gates=` values and their work-item `bar:` values keep working across
a re-sync. The alias table is `check.py`'s; the refusal is `check_vocab.py`'s;
`check_vocab.py`'s own declaration sites carry an explicit
`check_vocab: allow-file` / `check_vocab: allow` marker rather than being guessed
at.

## Translating a historical record

Translate historical records rather than rewriting them:

| Retired tag | Reads as, on the eight-rung ladder |
|---|---|
| `G1` | the `DevStg-Needs` … `DevStg-Reqs` range |
| `G2` | `DevStg-Arch` … `DevStg-Tests` |
| `G3` | `DevStg-Impl` |
| `G-Release` | the `DevStg-Release` rung |
| `G-Final` | the owner's final read (`final_review`, its own dial) |

**Attestations are never re-worded.** A sign-off that recorded a named human
certifying `G1` recorded exactly that, and rewriting it would make the record
claim something was signed that was not. That is why `docs/archive/`,
`docs/log.md`, `docs/ratify/`, the iteration logs and the closed work-item specs
are all carve-outs in `check_vocab.EXEMPT_GLOBS`: a reader searching their own
history needs the vocabulary that history was written in.
