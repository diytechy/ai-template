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
a fresh bootstrap — you merge kit changes into files you've filled in.

**`ADOPTING.md` §6 is the authority; this skill is the ORDER, not the content.**
It gives you the sequence of moves and the traps in each one, and sends you to §6
for every actual rule — which files to overwrite, which to preserve, and the
per-change migration recipes. It deliberately does **not** repeat those lists.
That is not tidiness: a recipe kept in two homes drifts, and this file's copy
already did (OI-27 caught it stale within weeks, at zero re-sync traffic). If you
find yourself wanting the specifics, open §6 — and if §6 is wrong, fix §6.

Where §6 lives: it is a kit reference doc (`project-trajectory/ADOPTING.md`), not
a scaffolded one, so read it in the **kit checkout you are re-syncing from** —
the one you are diffing against, which you already need for this procedure.

## 1. Make it a diff, not a guess

- Read `docs/kit-version` — the kit short-SHA + date this repo was last
  scaffolded/re-synced from — and `docs/kit-profile` — the structural choices
  (stack + omitted sections) its process docs were *generated* with.
- **If the stamp reads `unknown (kit not a git checkout)`** the repo was
  scaffolded from a tarball and has **no anchor**: there is no recorded commit to
  diff from. Don't guess a range — reconstruct it from artifacts (which scripts
  and docs the repo actually has), treat the whole of §6 as potentially
  applicable, and re-stamp honestly at the end.
- Choose the target kit commit. **Sync only from a committed kit state**, never a
  dirty kit tree (bootstrap stamps `<sha>-dirty` and warns — that stamp is
  unreproducible).
- Diff the recorded SHA against the target to see exactly which templates/scripts
  changed before touching anything.
- While the diff is open, recheck the **new capability surface** across the
  range — new/updated skills (`skills/INDEX.csv`), opt-in layers added to
  process-options.md, new vendorable packs (guardrails / efficiency /
  knowledge) — §6 "Re-weigh the opt-in layers".

## 2. Sort the changed files, then move them

Read §6 **"What to overwrite vs preserve"** and sort your diff into its four
classes: *overwrite freely* (kit-owned), *regenerate, never raw-copy* (kit-owned
but generated from your `docs/kit-profile`), *overwrite then re-apply your dials*
(kit-owned but hand-edited), and *preserve always* (yours). The membership lists
are §6's and change with the kit — read them there, per re-sync.

Two traps worth naming up front, because they are the ones that bite mid-move:

- **A plain `bootstrap.py --dest .` re-run is ADD-ONLY.** It skips every existing
  file, so it brings in what is *new* and updates *nothing* you already have —
  and it never deletes a script the kit has since retired. It is the safe first
  move, not the whole move: everything in the *overwrite* and *regenerate*
  classes is still on you afterwards. `--force` is the opposite extreme
  (overwrites everything, resets every dial) — never aim it at a live repo
  without a diff pass.
- **Set-together files.** Some kit-owned files only work as a set — take a newer
  hook with an older `check.py` and every commit fails on a step that doesn't
  exist. §6 flags each of these where it lists the file.

## 3. Apply the migration recipes for your range

§6 **"Migration recipes for specific kit changes"** is the single home for these.
Work through it and apply **only** the recipes your diff range actually contains
— each one names the change it belongs to and its date/WI. Recipes cover things a
file copy cannot: registry conversions, renamed or deleted scripts you must
remove by hand, config folds, and state you must reconcile before a derived value
is trustworthy.

Order matters in one place: if this repo still carries the **legacy one-word
policy files** under `docs/`, fold them into `docs/process.toml` **before running
anything else** (running with both homes live is refused, not resolved by
precedence). §6 "One policy home" has the command and the type changes.

## 4. Re-stamp and verify

- Re-run bootstrap to refresh generated pieces — it also **re-stamps
  `docs/kit-version` + `docs/kit-profile`**; commit them as the **last** step,
  so the record reflects the state you landed on.
- Refresh any materialized per-agent skills from source (`bootstrap.py --dest .
  --sync`) — a drifted copy is a gate finding.
- End green: run the harness (`scripts/check.py` / `check.{sh,ps1}`) and
  `scripts/check_docs.py`; a re-sync that leaves the harness red isn't done.
- **A green here is only as new as your checkers.** If step 2 left any kit-owned
  script un-updated, the repo is being judged by the OLD one — which cannot see
  what the new kit refuses. Measured on a three-week range: an add-only re-sync
  leaves the spine registries under BOTH carriers, a state the current kit
  hard-refuses, and the surviving old `trace.py` passes it. Before believing the
  green, run the TARGET kit's `trace.py`/`check.py` against your tree
  (`python <kit>/scripts/trace.py --strict` from your repo root); a disagreement
  between the two is the list of moves step 2 still owes.
