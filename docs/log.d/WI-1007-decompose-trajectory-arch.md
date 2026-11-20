## 2026-11-19 — WI-1007: trajectory_arch.py is split by the checks it holds into five modules beneath it, with no change of behaviour

Deferred open items: none.

Built on the maintenance branch `maint/wi-1007`, cut from `refactor_again` at
`af1dec169`, outside the lane workflow at the operator's direction: no claim,
no lane review rounds, commit hooks on. The parent session reviews and merges.

- **The critique.** Gemini Argon's round 1 raised two MAJORs, both adopted.
  S4: `planmode = "single"`, so the plan named the cuts before code moved.
  S5: the Context states the architectural delta, and the third Done-when
  item covers IF-263, IF-131, the new interface rows, `components.derived.toml`
  and `docs/kernel-modules-allow`.
- **What bounded the cut.** Three rules whose output had to stay the same.
  Connectivity asks every arch-map module to own an interface row and to sit
  on the far side of one, so five allotted ids allow five new modules.
  Containment asks every module to sit in a component, which only a design
  row's `module` cell gives, and this repository's knowledge packs make a
  module in no component a `--strict` finding; so the three checks no design
  row binds (the armed definition gate, seam-TC coverage, the CodeSymbol
  crosscheck) ride with the bound rule of their tier, as they did inside
  `trajectory_arch`. Seam coverage asks each new row to be cited by a test
  case, so existing ones cite them. No design row was minted.
- **The cuts.** Every function and constant moved byte for byte (85 named
  statements, each with one home, checked by a scratch AST comparison); two
  docstring phrases that said "this module's" were corrected to name the
  module meant. `arch_inputs.py` (114 SLOC): registry paths, the two dials,
  the loaders, the scan profile and `arch_inventory`. `arch_interfaces.py`
  (454): connectivity, contract bodies, seam-TC coverage and its allowlist.
  `arch_tags.py` (133): the CodeSymbol crosscheck and the test-file tag rule.
  `arch_seams.py` (156): the cross-component seam check, the kernel allowlist
  and `_SCAN_CACHE`. `arch_components.py` (241): the top view, the derivation
  record and `component_findings`. `trajectory_arch.py` (1128 to 201) is
  IF-263's composer, re-exporting the same `__all__`, and keeps the
  spec-boundary rule, whose design row (LLR-068) keeps it in CMP-006.
  `check_trajectory.py` does not change, and the process keeps one scan
  cache: `check_trajectory`, `trajectory_arch` and `arch_seams` bind one dict.
- **Behaviour unchanged, measured.** `check_trajectory.py --strict` on this
  repository at the base printed 273 lines; after the change, 272. The one
  line gone is WI-1007's own SpecRef-staleness warning, which the
  dispositions commit cleared by editing the spec. The base's scripts run
  with `--root` against the final tree print output byte-identical to the
  final scripts'.
- **Rows.** IF-316 to IF-320 are new and `Drafted`, one per module, each with
  its `Contracts:` line and `Contract IF-###:` body. IF-131's requestors are
  now the modules that import `gen_arch_map`. TC-080 cites IF-316 and IF-317,
  TC-409 and TC-410 cite IF-318, TC-067 cites IF-319, TC-049 and TC-166 cite
  IF-320 (traced `verifies`). LLR-042, LLR-049, LLR-067, LLR-172, LLR-365,
  LLR-366 and LLR-374 name the moved symbols' new modules (traced `module`);
  LLR-374's `Drafted` detail names `arch_seams.py`. Watermark IF 320.
- **Tests.** Only imports changed: `tests/test_seam_import_forms.py` loads
  `arch_seams`, whose `_SCAN_CACHE` and `gen_arch_map` it patches, and TC-080's
  re-export pin loads each rule's new home and names it. The size ratchet's
  `trajectory_arch.py` entry retires; the complexity entries re-key without a
  re-stamp. The bootstrap manifest ships the five modules.
- **RESYNC.** "The architecture rules move out of trajectory_arch into five
  modules beneath it", anchored at `af1dec169`: nothing forced, overwrite
  together.
- **Left as found.** LLR-172's detail and TC-166's method name
  `trajectory_arch.component_findings` in accepted text; the name still
  resolves through the composer, so neither was amended. The OI-130 re-score's
  `score.py` already failed its partition assertion at the base (P5 lists
  `kitlib/spine`, a kernel module since WI-1003); its `live.py` now imports
  `kitlib.spine` itself, the private alias it reached through
  `trajectory_arch` being gone.
