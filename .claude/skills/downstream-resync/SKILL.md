---
name: downstream-resync
description: Use when upgrading a repo that adopted this kit to a newer kit version — walk ADOPTING.md section 6 to diff from the recorded kit commit, overwrite the kit-owned files, preserve your own, and re-stamp.
stacks: [python, node, powershell, go, rust, any]
domains: [any]
phases: [dev, release]
tags: [adopting, re-sync, kit-version, upgrade, migration]
scope: kit
---

# Downstream re-sync (upgrade an adopted repo to kit HEAD)

Pull newer kit updates into a repo that adopted this kit earlier. This is **not**
a fresh bootstrap — you merge kit changes into files you've filled in. The
authority is `docs/process.md`'s companion **`ADOPTING.md` §6**; this is the
checklist.

## 1. Make it a diff, not a guess

- Read `docs/kit-version` — the kit short-SHA + date this repo was last
  scaffolded/re-synced from — and `docs/kit-profile` — the structural choices
  (stack + omitted sections) its process docs were *generated* with.
- Choose the target kit commit. **Sync only from a committed kit state**, never a
  dirty kit tree (bootstrap stamps `<sha>-dirty` and warns — that stamp is
  unreproducible).
- Diff the recorded SHA against the target to see exactly which templates/scripts
  changed before touching anything.

## 2. Overwrite vs. preserve

- **Overwrite freely (kit-owned):** `scripts/trace.py`, `check_docs.py`,
  `check_flows.py`, `check_perf.py`, `gen_arch_map.py`, `gen_*`, the pre-commit
  hook, `pytest.ini` markers, **`check.py`**. `check.py` is take-wholesale: your
  whole toolchain — format/lint/test commands, paths, tiers, coverage, arch-map
  mode, **and any project-specific gates (`[step:<name>]` sections)** — lives in
  `docs/stack.ini`, so nothing to re-apply. (Only if this repo still carries a
  hand-added step inside a pre-`[step:]` `check.py`: move it into a
  `[step:<name>]` section in `docs/stack.ini` this once, then take the kit
  `check.py` wholesale — it survives every re-sync after.)
- **Regenerate, never raw-copy (kit-owned but generated):**
  `docs/process.md` + `docs/process-options.md` are *generated* from the kit
  masters per the recorded `docs/kit-profile` — the masters carry
  `kit-only`/`profile` markers and every permutation, so a raw copy would ship
  marker comments and sections the repo opted out of. To take the new
  versions: **delete the two files, then re-run `bootstrap.py --dest .`** — it
  re-reads `docs/kit-profile`, regenerates them with the same structural
  choices, and refreshes both stamps (ADOPTING.md §6).
- **Preserve always (yours):** every registry CSV, `stakeholder-needs.md`,
  `docs/status.md`, `docs/log.md`, `docs/plan.md` (your work plan — the kit
  seeds the block-list skeleton once), `docs/architecture.md` hand-written overview
  (regenerate only the marker blocks), `AGENTS.md` project content, `docs/gate`,
  `.gitignore`/`.gitattributes` (merge new kit lines by hand). `bootstrap.py`
  **skips existing files**, so a plain re-run won't clobber these — never run
  `--force` against a live repo without a diff pass.

## 3. Apply the migration recipes

Read the **"Migration recipes"** list in ADOPTING.md §6 for the specific changes
in your diff range (e.g. `process.md` split into `process.md` +
`process-options.md`; a legacy `UN-` → `SN-` rename keeping id numbers; a TC CSV
gaining a required `Tier` column; a `gen_release_checklist.py` function rename).
Apply only the ones your diff actually contains.

## 4. Re-stamp and verify

- Re-run bootstrap to refresh generated pieces — it also **re-stamps
  `docs/kit-version` + `docs/kit-profile`**; commit them as the **last** step,
  so the record reflects the state you landed on.
- End green: run the harness (`scripts/check.py` / `check.{sh,ps1}`) and
  `scripts/check_docs.py`; a re-sync that leaves the harness red isn't done.
