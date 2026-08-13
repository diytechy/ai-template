---
name: downstream-resync
description: Use when upgrading a repo that adopted this kit to a newer kit version — open the kit's RESYNC_PACK.md, diff from the recorded kit commit, apply the entries your range contains, overwrite the kit-owned files, preserve your own, and re-stamp.
stacks: [python, node, powershell, go, rust, any]
domains: [any]
phases: [dev, release]
tags: [adopting, re-sync, kit-version, upgrade, migration]
scope: kit
---

# Downstream re-sync (upgrade an adopted repo to kit HEAD)

Pull newer kit updates into a repo that adopted this kit earlier. This is **not**
a fresh bootstrap — you merge kit changes into files you've filled in.

**`RESYNC_PACK.md` is the whole procedure; this skill only routes you to it.**
The pack carries the ordered procedure (§1), the file-by-file deviation review
over the bootstrap `MAPPING` inventory (§2), the per-change migration entries —
each anchored to the kit commit it landed at, so your recorded-SHA-to-target
range selects them (§3), the concept renames (§4), and the promotion trigger
(§5). This file deliberately repeats none of it: a rule kept in two homes drifts,
and this file's copy already did — the drift was caught by an audit within weeks,
at zero re-sync traffic. Want a specific? Open the pack. Pack wrong? Fix the pack.

**Which copy to read.** The pack is a kit reference doc
(`project-trajectory/RESYNC_PACK.md`), like `ADOPTING.md` — not scaffolded into
your repo. Read it from the kit checkout you are syncing **to**: that is the only
copy carrying the entries added since your adoption, and it is the checkout this
procedure already requires you to have open for the diff. `ADOPTING.md` §6 frames
the job and points at the same pack.

## How to run it

1. Read `docs/kit-version` — your anchor — and choose the target kit commit.
2. Work the pack's §1 top to bottom. It fixes the ORDER of moves, and in at least
   one place a wrong order is *refused* rather than resolved by precedence.
3. Where §1 sends you into §2/§3/§4, take only what your range actually contains
   — the anchors are there so you read a handful of entries, not all of them.
4. Finish on §1.4's verification, and run the **target** kit's checkers against
   your tree, not only your own: a green produced by checkers you did not update
   is the failure mode this whole procedure exists to avoid.

Nothing else belongs in this file. If you are about to write a rule here, it
belongs in the pack.
