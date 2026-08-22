## 2026-08-22 — WI-494: the declared-kernel seam exemption, OI-48's reuse provision executed

Deferred open items: none — the discovered `by_stem` classification gap
(below) is recorded as a finding rather than filed as a new OI, since fixing
it is mechanical (a `check_trajectory._classifiable_edges` indexing change)
and owes no owner decision the way OI-48 itself did.

**Why.** OI-48 asked which component owns `scripts/kitlib/`, the shared
helper package WI-448 built: the package is imported from all four
CMP-006..009 components, so `LLR-181` landed with a four-way `Component` tag
that was honest about usage and silent about ownership — and, as a side
effect, suppressed the cross-component seam rule on every one of the
package's edges. Ruled (d) 2026-08-21, generalised by the owner's own
follow-through question into a REUSE PROVISION: one owning component, plus a
declared shared-kernel LIST (never a `kitlib` hardcode) that any future
reused module can join the same way.

**What shipped.**

- **One owning component, measured.** `LLR-181`'s four-way tag collapses to
  `CMP-006` alone. The recorded closest-fit measurement: over `LLR-181`'s own
  four modules, `registry.py` is 304 of 572 lines (53%) — the clear
  plurality <!-- fig: cmd="wc -l project-trajectory/scripts/kitlib/__init__.py project-trajectory/scripts/kitlib/config.py project-trajectory/scripts/kitlib/git.py project-trajectory/scripts/kitlib/registry.py" rev=ce479c28 -->,
  confirming the ruling's "the registry reader is the package's bulk".
  `docs/requirements/components.toml` `CMP-006`'s notes rewritten from "open"
  to settled.
- **`LLR-182` (`kitlib/station.py`) reconciled — tag STAYS `CMP-008`, kernel
  declaration does NOT cover it.** Neither of the ruling's two literal
  branches: the repo already carries a declared, policed seam (`IF-093`,
  `scripts/traj_panels -> scripts/kitlib/station`) authored alongside
  `LLR-182` for exactly this module's one real cross-component edge — the
  WI-483 program's own Context calls it a "worked data point" for OI-48 that
  the ruling was asked not to pre-empt. Folding it into the kernel list would
  silence an edge deliberately kept visible, for no benefit: unlike
  config/git/registry/ladder/stage (real multi-consumer reuse across all
  four components), station.py has exactly one cross-component consumer,
  already governed by a normal seam. `LLR-182` and the wi448/wi483 lane
  specs' Context text are corrected to record this rather than leave it
  silent.
- **`LLR-184`/`LLR-185`** already carried the ruled `CMP-006` tag; `LLR-184`'s
  rationale is corrected (it stated the ownership question as still open).
  `LLR-186` confirmed NOT kitlib-homed (its own rationale says so) — untouched.
- **The declared kernel LIST: `docs/kernel-modules-allow`**, new, the
  `docs/provenance-allow`/`docs/if-tc-coverage-allow` `*-allow` idiom (a
  `[checks]`-side TOML list was priced and declined — those two files are
  already "per-entry recorded reason" surfaces, `docs/process.toml [checks]`
  is dials). NOT bootstrap-shipped (the `provenance-allow` precedent, not
  `orphans-allow.template`'s): a fresh adopter starts with no declared
  kernel, no exemption. Six entries — every kitlib module the package's real
  reuse touches, `station.py` deliberately absent with the header explaining
  why. Grammar: `<module path> — <reason>`, reason REQUIRED (OI-41 ARM
  precedent, hard at birth) — a malformed entry declares nothing (fail-safe:
  no exemption) and is reported (`kernel_allow_parse_findings`, WARN plain /
  ERROR `--strict`, shares `components_check`).
- **`cross_component_findings` learns the exemption**
  (`project-trajectory/scripts/check_trajectory.py`): `_cross_component_scan`
  gains a third, earlier exit — an edge whose DESTINATION is a declared
  kernel module is not a seam, neither the hard finding nor the
  multi-membership advisory. One-directional (keyed on the destination only,
  so an edge OUT of a kernel module stays fully policed); kitlib's own
  outward direction is additionally caught by the pre-existing
  `tests/test_bootstrap.py` static test (WI-448), untouched. The
  multi-membership advisory (WI-440) is otherwise unchanged and stays live
  for undeclared candidates.
- **Tests.** Seven new cases in `tests/test_trajectory_arch.py` (declared
  destination is silent; undeclared module in a non-empty allow-file still
  fires; absent file exempts nothing; one-directional; a kernel module with a
  residual multi-tag is not also advised about; a no-reason entry and an
  empty-reason entry are both dropped-and-reported; the hygiene finding
  shares `components_check`), plus one scaffold-verify case in
  `tests/test_bootstrap.py` bootstrapping a REAL scaffold and confirming it
  ships no `docs/kernel-modules-allow` and reads as empty there. `TC-067`
  (verifies `LLR-067`) gains all twelve node ids in `evidence`, its
  `method`/`expected` reworded; `LLR-067`'s own `detail` cell amended to name
  the new silent case. No new spine row minted — this rides `LLR-067` the
  way the multi-membership advisory already does, unclaimed.

**DISCOVERED, NOT FIXED — banked as a finding.** Measuring the live repo
before and after this WI's edits shows **zero** cross-component
findings/advisories for any kitlib edge, in either state — not because
suppression worked as designed, but because none of kitlib's real import
edges reach classification at all.
`gen_arch_map.internal_imports` records a package-submodule import (`from
kitlib import registry`) as the qualified stem `kitlib.registry`, while
`_classifiable_edges`'s `by_stem` index is built from only the last path
segment (`registry`) — so `by_stem.get("kitlib.registry")` never resolves and
the edge is silently unclassifiable, for every kitlib importer. Confirmed
live: `scripts/traj_panels` (CMP-009) importing `kitlib.station` (CMP-008,
single-tagged, disjoint) produces neither a finding nor an advisory today,
though the rule's own contract says it should (were `IF-093` absent). This is
orthogonal to OI-48 — a `by_stem` indexing gap that predates and outlives the
four-way tag, affecting any multi-file internal package (kitlib is the only
one in this tree today) — so it is recorded here rather than patched inline
(CLAUDE.md: edit conservatively, flag a design smell separately). The
exemption this WI built is independently verified correct (synthetic
fixtures where `by_stem` resolves cleanly, plus the real-scaffold absence
case) but has no visible effect on this repo's live checker output today,
because the edges it would exempt never reach the rule regardless of tag
shape. Recommendation for the owner: a follow-up WI to widen `by_stem` to
also index the qualified `pkg.submodule` form.

**Registry mechanics.** All three touched registries (`low-level-
requirements.toml`, `test-cases.toml`, `components.toml`) are `Approved`
rows amended under the DevStg-Needs dial (SR/LLR/TC edits proceed under
ordinary review). `Component` is a TRACED cell (`check_trajectory.
SPINE_TRACED_CELLS`) so the tag moves needed no authorisation; `Rationale`/
`Detail`/`Method`/`Expected` are RATIFIED, so `intake.py snapshot
--approves "OI-48 (d), 2026-08-21 -- docs/log.d/2026-08-21-owner-rulings-oi48-52.md"`
recorded the amendment against the ruling that authorised it — `baseline_
snapshot.refresh_refusal` clean afterward. First pass through this cited
citation frames (`WI-494`, `OI-48`, dates, edit-verb stamps) inline in the
five amended cells — `trace.py`'s stand-alone rule caught it
(`FINDING (spine stand-alone)`, warn-only by owner ruling but real): a
living spine cell states the system, never its own history. Reworded all
five to timeless prose with no citation tokens, re-ran the snapshot refresh
once more against the corrected text (the duplicate same-day stamp line this
produced in `docs/archive/last_approved/README.md` is manually deduplicated
to one entry, noted as such — nothing parses that file).

**A second, real miss caught only by the full suite:** the first hand-edit
of `docs/status.md` named `WI-494` twice, past tense, inside the two lane
bullets — and `docs/status.md` is forward-only: once this WI's registry
`Status` reads `done`, ANY token naming it in the hand-authored prose is the
`WI-200` finding (`tests/test_trajectory.py::
test_forward_only_unit_over_the_real_meta_repo`), not just the generated
frontier block. Both bullets reworded to describe the ruling's execution
without citing the id; the closed id lives only in this fragment and in
`docs/work/complete/`.

**Environment note, banked as a finding rather than fixed:** this box's `C:`
free space read ~22.9 GB at session start but was down to **~190 MB** by the
second full-suite attempt — nowhere near pytest's own basetemp (measured
negligible, ~1100 near-empty `tmp*` dirs, no cleanup needed) and not
attributable to this WI's diff. The first ENOSPC run's ~2,700 `E` collect/
teardown errors were the disk-full artifact the standing rule warns about,
not real failures — confirmed by re-running the identical suite, unchanged,
with `--basetemp` redirected to `D:` (~188 GB free on this box) once the
`status.md` fix landed: clean pass, no batching needed once temp writes had
room. The underlying low-disk condition is a box property, not a repo one;
recorded here as the one-machine-humility rule asks, not investigated
further (out of this WI's scope).

**Gates** (Windows, `-n auto`; PATH carries Git for the smoke/full suites),
real output, none sanctioned:

- `python -m pytest -q -n auto -m smoke`: **1368 passed, 5 skipped in 59.28s**
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=ce479c28 -->
  (under the WI-281 60s budget).
- `python project-trajectory/scripts/check_docs.py --root . --stale`: OK —
  1001 doc(s), 1341 intra-repo link(s), 0 broken (1 pre-existing orphan
  warning, `docs/test/report.md`, unrelated to this diff).
- `python project-trajectory/scripts/check_trajectory.py --root . --strict`:
  clean, exit 0 (506 work items, graph acyclic; pre-existing warns only —
  the shared-spec-of-record advisories and one Title-length warn, none
  touching this WI's rows).
- `python project-trajectory/scripts/trace.py --root . --strict
  --strict-integrity`: exit 1, but ENTIRELY on pre-existing, untouched state
  — 10 `FINDING (orphan)` lines over SR-151/152/160/162/163 and five more
  (`system-requirements.toml` carries zero diff in this WI; this is the
  known-open, unrelated "trajectory gating red" `docs/status.md` already
  names). Zero `FINDING (spine stand-alone)` lines — the provenance cleanup
  above closed that class for every cell this WI touched; the one surviving
  `WARNING (advisory)` on `LLR-181` Rationale is 100% pre-existing text
  (`OI-16`/`D-8`/2026-08-13/2026-08-12) this WI did not author.
- `python project-trajectory/scripts/derive_stage.py --root . --check`:
  up to date (`DevStg-Arch`) after one `derive_stage.py` regen (fingerprint
  refresh only — every derived value identical before/after).
- `python -m pytest -q -n auto` (full, unfiltered): **2847 passed, 14 skipped
  in 1138.11s (0:18:58)**, `--basetemp` on `D:` per the environment note
  above <!-- fig: cmd="python -m pytest -q -n auto --basetemp=/d/pytest-tmp-wi494" rev=ce479c28 -->
  — single foreground process, not batched (the box's C: constraint was
  worked around by relocating temp writes, not by lowering `-n`).

**One ratchet re-stamped, reviewed, reason in place:** `check_trajectory.py`
module size, 4496 -> 4631 lines (+135) — the declared-kernel reader/parser/
hygiene-finding trio, the third exit in `_cross_component_scan`, and the
docstring updates recording the new silent case. `tests/
test_module_size_ratchet.py`'s baseline dict carries the full reason inline,
the same convention every prior bump on this module used.
