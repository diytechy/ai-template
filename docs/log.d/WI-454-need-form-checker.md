## 2026-08-14 — WI-454: SN-033's need-form checker lands warn-first, while the tier is clean

One line: the check SN-033's ratified acceptance commissions now exists —
[`check_need_form.py`](../../project-trajectory/scripts/check_need_form.py)
reports the row and the offending phrase for any SN `need` cell carrying an
internal path, implementation-only identifier or process citation — landed
deliberately while the tier is measured clean (0 findings over 27 need cells),
so the SR re-tier's churn inherits a locked-in state where the first row to
dirty the tier is the one that reports.

- **Deliverables.** The checker (stdlib, `spine_carrier.load_needs` sibling
  read, need cells only per SN-033's own exemption); the `need-form` step in
  [`check.py`](../../project-trajectory/scripts/check.py)'s table at every bar
  **warn-first always** (no `--strict` promotion — gating needs an owner
  ruling, recorded in the wiring comment); the reviewed exception list
  `docs/need-form-allow` (`<token> — <reason>` lines, separator required so a
  malformed entry can only fail loud, **ships empty** — not scaffolded);
  9 in-process smoke tests
  ([`tests/test_check_need_form.py`](../../tests/test_check_need_form.py));
  scaffold registration (bootstrap MAPPING + manifest, kit README row,
  `test_bootstrap` list, `BUILTIN_STEP_NAMES`); the spine chain SR-150
  (Planned, SN-033's **first** coverage — SN orphans 10 → 9) → LLR-170
  (Draft, CMP-007) → TC-164 (Draft, Smoke) with IF-121 (Provides, the CLI
  contract incl. the never-strict posture) + IF-122 (Consumes, the carrier
  read), all Draft/Planned — **no re-attest window**. Spec closed to
  [`work/complete/`](../work/complete/WI-454-sn-033-need-form-checker.md).
- **The §6 item-16 rider, executed.** Its *SN comment block* stray rides this
  registry touch per §6.0: the OI-18 dissolution deleted the Edge-case rows
  and left the header prose declaring an empty section — the comment block in
  [`stakeholder-needs.toml`](../requirements/stakeholder-needs.toml) now
  records the deletion instead of inviting rows into a tier the dissolution
  closed. Item 16's *other* stray (IF-064's inline SN-016) rides the
  `external.toml` schema row per §6.0 and was not touched.
- **Deviations / finds, stated plainly.** (1) Two heuristic scope calls the
  spec's classes forced, both documented in the docstring and pinned by
  tests: `SN-###` is **not** a process citation (the live SN-025 need hands
  its launcher clause to SN-034 by id — a stakeholder-tier cross-reference),
  and a single-slash dot-free token is **not** a path (live English pairs
  `subjective/perceptual` in SN-024, `requirement/test` in SN-029). Without
  both, the "live registry clean" acceptance is unmeetable against the
  ratified text as written. (2) Minting IF-121/122 exposed a real hole:
  `trace._offspine_ids` read only `open-items.toml`, so the **IF and CMP
  watermark spaces went vacuous** at the WI-443 CSV→TOML conversion — ids
  above the mark drew no finding, the OI-26 defect class the function's own
  docstring records. Re-armed with two registry rows (trace.py ratchet
  3938 → 3947, reviewed); `--bump-ids` then recorded SR=150 LLR=170 TC=164
  IF=122. (3) `docs/gate` regenerated **on the branch** — basis tracks the
  new rows, value unchanged at DevBar-Reqs (the WI-392/393 precedent;
  `test_derive_gate` requires the committed cache to track the spine).
  (4) No RESYNC_PACK entry: additive and warn-first, nothing for an adopter
  to migrate (the check_figures/check_doc_refs precedent — check_vocab's
  entry documented the vocabulary *break*, not the script's existence).
  (5) The two `IF-121/122 … no script declares it` WARNs are the arch-map
  lag; the `Contracts:` line ships in the script and the map regenerates on
  the trunk at merge (the WI-392 precedent). Follow-up surfaced, not filed:
  CMP-007's notes cell says "the 8 check_* lints" — a count this landing
  makes stale, left untouched because the row is provisional with owner
  ratification owed.
- **Byte budgets:** none of the budgeted docs (AGENTS.template.md,
  PROCESS.md, PROCESS_OPTIONS.md) were touched.
- **Measured on the build commit 790a253a (clean tree):** module suite
  9 passed in 0.37s
  <!-- fig: cmd=".venv/bin/python -m pytest -q tests/test_check_need_form.py" rev=790a253a -->;
  smoke tier 1123 passed / 7 skipped in 32.81s
  <!-- fig: cmd=".venv/bin/python -m pytest -q -n auto -m smoke" rev=790a253a -->
  (membership within the 1150 ceiling, no re-stamp); full unfiltered suite
  **2484 passed / 11 skipped** in 0:07:02
  <!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=790a253a -->;
  `trace.py` rc=0, `check_trajectory.py --strict` rc=0, live checker run
  clean over 27 need cells
  <!-- fig: cmd=".venv/bin/python project-trajectory/scripts/check_need_form.py --root ." rev=790a253a -->.
