## 2026-08-14 — The depth-0 frame becomes rows; `Stability` retires; rung 1 re-keys

**Why.** Sitting 2 locked the frame — 5 entities · 6 crossings · 3 relationships
— and ruled the registry shape around it (decisions 3/4/5/12,
[§1R.5](../plans/2026-08-13-sitting-2-boundary-and-context.md#1r5-the-registry-shape-around-them-decisions-345-as-ruled)).
Nothing downstream could start without it: the SR re-tier campaign needs
machine-resolvable crossing ids, and SN-037's checker needs an SR-side column
that did not exist. This row is that schema.

**What changed.** [`docs/requirements/external.toml`](../requirements/external.toml)
holds the frame in three tiers on one path — `[entity.EXT-###]`,
`[boundary.B-##]`, `[relationship.REL-###]` — shipped as
[`registries/external.template.toml`](../../project-trajectory/registries/external.template.toml)
and scaffolded by `bootstrap.py`. The carrier needed no loader change: keying
registries by ID COLUMN rather than by path already made a three-tier file work.
`Stability` retired for `Approval` across all 113 IF rows and
`derive_gate.boundary_incomplete` re-keyed onto crossing approval **in the same
commit**, because `_maturity` maps an unrecognized value to DRAFTED — the split
would have pinned rung 1 open forever on a deleted column, giving the right
stage for the wrong reason. `trace.py` gained the frame's resolution rules as
their own `--strict` failure class, and SN-037's SR→boundary rule on a new
`SR.BIF-Refs`.

**Row ids are `B-##`, not `BIF-###`** — a deviation from §1R.5's sketch that
resolves a contradiction inside the source. §1R.2's locked table, §3R and this
WI's own tie-back examples all write `B-01`…`B-07`; v1's `BIF-001`…`BIF-031` are
a different set of 31 crossings still cited by id in the archive, so that prefix
would recycle live ids onto new meanings.

**Both ambiguities resolved, stated not assumed.** Rung 1 gates on crossing
**approval**, not realization coverage: 13u says approval, §1R.5 adds "every BIF
realized", and realization is decision 6 — deferred by ruling, and not
hypothetically, since four of six crossings are realized by no IF row today. The
approval vocabulary ships **provisional** (`draft` | `approved`) with its D-9
migration written into the registry header rather than waiting on sitting 3,
which the campaign sits downstream of.

**Every row lands `draft`, all 113 IF rows included** — a deliberate non-claim.
`Stable` was a maturity assertion; `approved` is a ratification one, and mapping
one onto the other would have manufactured 108 approvals nobody signed. Flip
authority is in both registries' prose (`human_ratification_through` covers the
spine tiers only) and pinned by a test that reds if anything but a ratification
sets one.

**FINDING — decisions 4 and 8 are in tension, and one clause is HELD.** §1R.5
rules that an IF row sheds `direction` and `counterpart`. Those two columns are
the sole input to the dashboard's How-SW seam graph and its containerized
component drill, and the second is **ratified work**: SR-091, "shall attach IF
seams to visible block input/output ports and aggregate cross-container seams to
container boundaries", Verification = Test. Decision 8 makes
`PROJECT_STATE.html` the one home for architecture in the same sitting decision 4
deletes what it draws from. The full shed was implemented first and measured — 41
tests red, 30 of them the dashboard failing to render at all — so the columns are
held, their deletion bound to WI-455, and the reason written into the registry
header, the carrier, the migrator and the checker. Side effect recorded as a
watched defect: `direction` now means two things across two tiers (D-3), which
closes itself when WI-455 lands the deletion; renaming the boundary column is the
fix if WI-455 slips. **Sitting 3 owes the sequencing call.**

**FINDING — two checks would have become tautologies if copied forward.** The
seam-TC citation rule had already been re-keyed once off a column whose values
marked exactly the rows that passed it; `Approval == "approved"` would have
rebuilt that (every row reads `draft`), so it now arms on every real IF row and
the maturity column drops out of the rule. WI-191's anti-duplication rationale
arm is **retired, not re-keyed**: its input meant "proposed, not yet pinned by a
second consumer", `draft` means "not yet ratified", and the swap would have taken
its arming set from ~4% to 100% at a severity that errors under `--strict`. Both
removals are pinned by tests asserting the removal, so neither drifts back
half-fed. **Sitting 3 owes a value meaning "proposed" if the forced
anti-duplication search is worth keeping.**

**FINDING — WI-452's `SpecRef` anchor is dangling on trunk**, pre-existing and
not this row's: `check_trajectory --strict` errors R-E on
`#55-wi-452--llr-165-resync-helper-resurface`, which names no heading in the
sitting-2 plan. WI-452 is on the ready frontier and `integrate.py claim` refuses
a spec with no in-repo-resolving SpecRef, so this blocks that claim.

**Verification.** Full suite `pytest -q -n auto`: **2472 passed, 11 skipped**
(7:30). Smoke `-m smoke`: **1112 passed, 7 skipped** (32 s). `check_docs --stale`:
402 docs, 1183 links, **0 broken**. The re-key demonstrated both ways, not
asserted: crossings `draft` → `stage=DevStg-Boundary`; all six flipped to
`approved` → the rung releases. A throwaway `bootstrap.py --dest` scaffold
scaffolds `external.toml`, runs `trace.py --strict` clean and reads
`stage=DevStg-Needs`, so inert `-000` rows hold nobody at the boundary rung.
Ratchets re-stamped deliberately in both directions: `trace.py` 3678 → 3917,
`bootstrap.py` 2834 → 2844, `check_trajectory.py` 4115 → 4120,
`interface_findings` 22 → 13, `build_dependency_diagram` deleted from the
complexity census.

**Deviations from spec.** One clause held (`direction`/`counterpart`, above) and
one id-shape deviation (`B-##`, above). Both are recorded in
[WI-442](../work/complete/WI-442-oi-28-seeds-landed-on-the-spine.md)'s Deliverable.
No byte-budgeted file was touched.
