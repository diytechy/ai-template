+++
id = "WI-494"
title = "The declared-kernel seam exemption with a reuse provision (OI-48 ruled (d), 2026-08-21)"
specref = ""
workstream = "scripts"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "spine"
priority = 3
+++

## Deliverable

Executed in full: one owning component, the declared kernel LIST as a reuse
provision, and the `cross_component_findings` exemption, all measured against
the live repo rather than assumed.

**One owning component, measured.** `LLR-181`'s four-way `Component` tag
(`CMP-006;CMP-007;CMP-008;CMP-009`) collapses to `CMP-006` alone. The
recorded closest-fit measurement, run at execution: over `LLR-181`'s own
four modules (`__init__.py` 93 + `config.py` 121 + `git.py` 54 +
`registry.py` 304 = 572 lines), `registry.py` is 304/572 (53%) — the clear
plurality, confirming the ruling's own "the registry reader is the package's
bulk" — <!-- fig: cmd="wc -l project-trajectory/scripts/kitlib/__init__.py project-trajectory/scripts/kitlib/config.py project-trajectory/scripts/kitlib/git.py project-trajectory/scripts/kitlib/registry.py" rev=ce479c28 -->
recorded on `LLR-181`'s `rationale` cell. `docs/requirements/components.toml`
`CMP-006`'s notes are rewritten to state ownership as settled rather than
open.

**`LLR-182` (`kitlib/station.py`) reconciled — the tag STAYS, unmoved, and
is NOT added to the kernel declaration.** This is neither of the ruling's two
literal branches ("the kernel declaration covers it or the tag moves"): the
repo already carries a third, better-fitting answer the ruling's own drafting
did not have in view. `docs/requirements/interfaces.toml` `IF-093`
(`scripts/traj_panels -> scripts/kitlib/station`) is a declared, POLICED seam
authored alongside `LLR-182` for exactly this module's one real
cross-component edge — the WI-483 program's own Context record calls it "a
worked data point" for `OI-48` that the ruling was asked not to pre-empt.
Folding `station.py` into the kernel list would silence an edge its own
design deliberately kept visible, for no benefit; unlike `config`/`git`/
`registry`/`ladder`/`stage` (real multi-consumer reuse across all four
components), `station.py` has exactly one cross-component consumer and it is
already governed by a normal seam. Both `LLR-182`'s and the wi448/wi483 lane
specs' Context text are corrected to record this rather than leaving it
silent.

**`LLR-184`/`LLR-185` (`ladder.py`/`stage.py`)** already carried the single
`CMP-006` tag the ruling names — no tag change — but `LLR-184`'s rationale
stated the ownership question as still open; corrected to record the ruling.
`LLR-185` made no such claim and is untouched. **`LLR-186`
(`derive_stage.py`) is confirmed NOT kitlib-homed** (its own rationale states
it deliberately stays out of the package) — out of scope, unchanged.

**The declared kernel LIST: `docs/kernel-modules-allow`, a new file** — the
`docs/provenance-allow` / `docs/if-tc-coverage-allow` `*-allow` idiom, chosen
over a `[checks]`-side TOML list because those two precedents are exactly
"per-entry recorded reason" surfaces already, while `docs/process.toml
[checks]` carries dials, not reasoned prose. NOT shipped via `bootstrap.py`
`MAPPING` (the `provenance-allow`/`if-tc-coverage-allow` precedent, not the
`orphans-allow.template` one): a fresh adopter starts with no declared
kernel and therefore no exemption, which is the fail-safe default the Tests
below prove in a real scaffold. Six entries, one per kitlib module the
package's real reuse touches (`__init__.py`, `config.py`, `git.py`,
`registry.py`, `ladder.py`, `stage.py`), each with its own recorded reason;
`station.py` is deliberately absent, with the file's own header explaining
why. Grammar: `<module path> — <reason>` (the `provenance-allow` em-dash
idiom); a reason is REQUIRED (OI-41 ARM precedent — hard at birth, no
bare-baseline exception the way the seeded `if-tc-coverage-allow` has one) —
a line with no separator, or an empty module/reason, declares nothing
(`_parse_kernel_allow`/`read_kernel_modules` in
`project-trajectory/scripts/check_trajectory.py`) and is reported by
`kernel_allow_parse_findings` (WARN plain, ERROR under `--strict`, sharing
`component_findings`' `[checks] components_check` opt-out).

**`cross_component_findings` learns the exemption.** `_cross_component_scan`
gains a third, EARLIER exit ahead of the existing seam-coverage and overlap
checks: an edge whose DESTINATION resolves into `read_kernel_modules` is not
a seam at all — neither the hard finding nor the multi-membership advisory
(a declared-kernel module is a settled candidate, so advising about it again
would be noise). One-directional by construction — keyed on `dst_n` only, so
an edge OUT of a kernel module stays exactly as policed as before; kitlib's
own outward direction is additionally caught by the pre-existing dedicated
static test in `tests/test_bootstrap.py` (WI-448), which this exemption does
not touch or replace. The multi-membership advisory (WI-440) is otherwise
untouched and stays live for undeclared candidates.

**Tests** (`tests/test_trajectory_arch.py`, following the suite's existing
`_cross_cmp_repo`/`_overlap_repo` synthetic-fixture idiom): a declared
kernel destination is silent under `--strict` (finding and advisory both);
an undeclared module in a non-empty allow-file still fires (fail-safe, and
"still fully live for every other edge"); an absent allow-file exempts
nothing; the exemption is one-directional (declaring the SOURCE does not
exempt its own outbound edge); a declared kernel module still carrying a
residual multi-tag is not also advised about; an allow-file entry with no
separator, or with an empty reason, is dropped AND reported, sharing the
components_check opt-out. **Scaffold-verify**
(`tests/test_bootstrap.py::test_scaffold_ships_no_declared_kernel_surface`):
a real `bootstrap.py`-produced scaffold carries no
`docs/kernel-modules-allow`, and `read_kernel_modules`/
`kernel_allow_parse_findings` both read it as empty there — the fail-safe
default proven on the real artifact, not only a synthetic fixture.
`docs/test/test-cases.toml` `TC-067` (which verifies `LLR-067`, the row
`cross_component_findings` itself implements) gains all twelve new
node ids in its `evidence`, and its `method`/`expected` are reworded to
state the exemption; `LLR-067`'s own `detail` cell is amended to name the
new silent case. No new spine row is minted for the exemption — it rides
`LLR-067` the same way the multi-membership advisory (WI-440) already does,
unclaimed by a dedicated row.

**DISCOVERED, NOT FIXED — banked as a finding rather than folded into this
WI's scope (CLAUDE.md: edit conservatively; flag a design smell separately
rather than fixing it inline).** Measuring the live repo before AND after
this WI's edits (`check_trajectory._cross_component_scan(Path("."))`) shows
**zero** findings or advisories for any kitlib edge, in either state — not
because the four-way tag's suppression is working as designed, but because
none of kitlib's real import edges reach classification at all.
`gen_arch_map.internal_imports` deliberately records a package-submodule
import (`from kitlib import registry`) as the QUALIFIED stem `kitlib.registry`
(its own docstring: "the real dependency is the submodule"), while
`_classifiable_edges`' `by_stem` index is built from only the LAST path
segment (`registry`) — so `by_stem.get("kitlib.registry")` never resolves,
`len(targets) != 1`, and the edge is silently treated as an unclassifiable
stem for every single kitlib importer (confirmed live: `scripts/traj_panels`
(`CMP-009`) importing `kitlib.station` (`CMP-008`, single-tagged, no overlap)
produces neither a finding nor an advisory today, though it should be a hard
finding under the rule's own stated contract were `IF-093` absent). This is a
pre-existing gap in `_classifiable_edges`, orthogonal to OI-48 and to any
package other than kitlib (the only multi-file internal package in this
tree) — fixing it is a `by_stem` indexing change with its own blast radius
(every package-style import in any adopter's tree), not a kernel-declaration
question, so it is recorded here rather than patched inline. The exemption
built by this WI is independently verified correct (synthetic fixtures where
`by_stem` resolves cleanly, and the real-scaffold absence case), but has NO
visible effect on this repo's live checker output today, because the edges
it would exempt are not reaching the rule in the first place — for either the
four-way tag this WI removed or the single kernel-declared tag it replaced
it with. **Recommendation for the owner:** a follow-up OI/WI to widen
`by_stem` to also index the qualified `pkg.submodule` form so package-style
imports classify correctly everywhere, not only for kitlib.

## Context

Executes OI-48's ruling (d), generalised by the owner's own follow-through
question into a REUSE PROVISION. The operative shape, from the ruling:

- **One owning component for `scripts/kitlib/`.** The recorded closest-fit
  analysis points at `CMP-006` (the registry reader is the package's bulk);
  measure at execution and record the tag with reasoning on the row.
  `LLR-181`'s four-way `Component` tag collapses to the owning component
  (traced cell). Reconcile `LLR-182`'s single-tag `CMP-008` choice for
  `kitlib/station.py` with the ruled ownership — either the kernel
  declaration covers it or the tag moves; record which and why.
- **A declared kernel LIST, not a `kitlib` hardcode.** A new declared
  surface (home per the ruling: a small declared file or a `[checks]`-side
  declaration — pick the one consistent with the repo's declared-surface
  conventions and record why) listing kernel modules, one per entry, each
  with a recorded reason. Any future shared module whose consumers span
  components takes the same declared path; an addition is a deliberate
  recorded act. This is the owner's reuse provision: the same
  multiple-seams-into-multiple-components shape recurs for any reused
  module, so the mechanism must not be special-cased to kitlib.
- **`cross_component_findings` learns the exemption:** an import edge INTO
  a declared kernel module is not a seam finding. The rule stays fully live
  for every other edge — including edges OUT of a kernel module (kitlib
  importing a non-kitlib sibling is already refused by the WI-448 rule
  test; keep both directions covered).
- **The multi-membership advisory stays live** so future kernel candidates
  keep surfacing rather than being silently exempted.

Tests: the exemption bites only for declared entries (an undeclared shared
module still warns); an entry without a reason is refused or warned per the
allow-file grammar conventions (OI-41 ARM precedent); the seam rule still
fires on a planted non-kernel cross-component import. Scaffold-verify: the
checker ships; bootstrap a real scaffold and confirm the declared surface's
absence means no exemption (fail-safe default).

Sequencing: this row unblocks the wi448 consolidation slices (each adds
importers) and settles the question the wi483 lane kept open by choosing a
single-tag LLR-182. Both lane specs cite OI-48 as the gate — update their
Context lines at close.
