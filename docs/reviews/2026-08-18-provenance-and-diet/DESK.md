# 2026-08-18 review round — desk disposition

**Scope reviewed:** the day's six commits, `ff03d323..4e9a5c8a` — okf-off,
spine+scripts hardening, the doc diet + byte caps, the WI-455 architecture
retirement merge, the artifact-voice rule reaching the need tier, and the
provenance ruling.

**Reviewers:** two rounds, independent and cross-family.

| Round | Reviewer | Verdict | Filed |
|---|---|---|---|
| External | GPT-5.6 Sol via `codex`, medium effort, read-only sandbox | REJECT — 5 MAJOR, 2 MINOR | [ROUND-SOL.md](ROUND-SOL.md) |
| Internal | Claude Opus, adversarial brief, execution permitted | 8 MAJOR, 15 MINOR | this file |

Two findings were reported independently by both reviewers (the unstamped
RESYNC entries; the kit shipping text that teaches the repealed rule — each
found a different instance). The internal round reproduced the full suite
independently: `2578 passed, 10 skipped`, matching the claim under review.

## Disposition

**Applied — 23.** M1 the flows gate matching a document TITLE (a gate that
could not fail, shipping downstream); M2 a detector arm at 100% false-positive
whose commit claimed 0 of 319; M3 cell-granular suppression hiding 67
unadjudicated tokens while the report asserted none existed; M4 the sweep
using the detector as its definition of done, leaving 33 bare edit verbs; M5
three RESYNC entries with no landing anchor; M6 a log fragment claiming a green
the committed tree did not carry; M7 and Sol-F1 the repealed permission
surviving in the shipped worklist and in a test that pinned it; M8 the `13v`
waiver marker, itself a decision id, mandated into the cell the rule bans
decision ids from; Sol-F2 CMP and EXT swept but unguarded; Sol-F4 the
architecture-retirement residue in PROCESS.md; N1 a gating message naming a
retired carrier; N2 path suppression on one date arm only; N3 this repo's own
letter-suffixed ruling stamps invisible to the detector; N4 an undisclosed
deferral; N5 two SN rewrites that deleted the reasoning with the citation —
the named failure mode of the rule being applied; N6 two stale capped
baselines; N7 a file parked at its cap with nothing recording it; N8 an orphan
glob dropped as an undisclosed side effect; N10 screenshot tooling broken by
the absent Knowledge tab; N11 an incomplete reversal recipe; N12 two registry
templates missing the charter the ruling extended to them; N13 a PowerShell
port still defaulting to the deleted architecture doc; N14 the caps'
justifying figures unreproducible.

**Refuted in part — 1.** Sol-F5 claimed no populated TOML-spine OKF path is
exercised anywhere. Its reading of `tests/test_gen_okf.py` is correct — that
module's fixtures write the legacy CSV carrier — but the reviewer ran
read-only and could not observe that two dashboard tests drive
`gen_okf.emit()` over this repo's live TOML registries. The gap is real and
narrower than filed: bundle determinism and staleness are exercised only on
the legacy carrier.

**Found while fixing, in neither review — 2.** Two Reserved entries and the
architecture-retirement entry had been appended *below* the pack's closing
section, outside the bodies the anchor grammar, the landing-order test and the
operator worklist all read — well-formed and unreachable. And the flows fix
exposed a second face of M1: requirement ids cited *outside* the flows section
were being validated as if inside it (40 → 37 on the unchanged document).

**Deferred to the sitting — the standing carve-outs.** The open-question
markers remain allow-listed and still owe open-item rows; the three living
rows citing archived specs remain blocked on the `docs/cmp/` ruling; eight
citation frames in IF/LLR/TC cells outside the detector lane's scope are
recorded as a worklist in its log fragment.

## The lesson worth keeping

The sweep was validated by the detector it was co-designed with, and the
detector's own false-positive rate was reported without being measured. A
cleanup graded by the instrument built alongside it proves nothing about the
population it claims to have cleaned — which is the same circularity the
enforcement audit exists to break. The instrument needs an adversary, and the
adversary needs to be able to run it.
