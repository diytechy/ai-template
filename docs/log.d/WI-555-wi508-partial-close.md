## 2026-09-01 — WI-555: convert the wi508 complete-close to a partial handback

Executes `OI-71` (RULED 2026-08-31, option (c)): the 43-commit wi508 lane
(`origin/wi508-architectural-remap-HELD-for-owner-verdict`, pushed to origin
2026-08-31) self-closed **complete** on its own branch, so the integrator reads
`merged` and the verdict gate demands a fresh APPROVE. The owner ruled the lane
closes **partial** through the kit's own path, performed MANUALLY as the special
case its history makes it — nothing discarded, the evidence preserved in
history, a successor re-lands the reviewed spine content from a preserved record.

### The mechanics, measured before touching anything

- Held branch has no LOCAL ref — only `origin/wi508-architectural-remap-HELD-for-owner-verdict`.
  The claim directory `docs/work/active/wi508-architectural-remap/` is still on
  trunk (the phantom head), so `_claimed_specs` resolves the claim; the branch
  name must be `wi508-architectural-remap` for `lane_worktree` to match.
- On the branch the spec sits in `docs/archive/work/complete/` (self-closed);
  `branch_outcomes` therefore reads `complete`. `close_partial` moves
  `active/<branch>/<name>` → `docs/work/partial/<name>`, so the source must be
  restored to `active/` first — the ruling's "revert the close (or re-perform
  into partial/)".
- Merge base `ff29fef8`; at that base the spec was in
  `active/wi508-architectural-remap/`. Trial merge conflicts are six generated /
  record artifacts only (handoff §1.4); the two authored spine files auto-merge.
- `needs = WI-554` because the merge regenerates `docs/ratify/CURRENT.md` and
  round 019's two trunk-side renderer defects (fixed by WI-554) would re-red it.

### The conversion sequence (executed from the trunk root `../../ai-template`)

1. Create local `wi508-architectural-remap` at the origin HELD ref (the
   "rename back" — the ref now matches the trunk claim; a finished branch).
2. Restore the spec `active/wi508-architectural-remap/` on the branch
   (undo the self-close), commit → branch now reads no-outcome (still claimed).
3. `handback.close_partial` writes the immutable report under `docs/handbacks/`,
   moves the spec to the terminal `docs/work/partial/`, commits on the branch —
   the outcome now reads `partial`, no verdict owed. Split left to the
   adjudicator (keep/discard is the disposition row's call, WI-540 precedent).
4. `integrate.py integrate` merges the partial-close lane; the six generated /
   record conflicts resolved by the precedented remedy (take trunk's generated
   side; splice `log.md`); `docs/ratify/CURRENT.md` regenerated on trunk.
5. Post-merge intake mints the disposition row from the report; the phantom head
   clears (the merge moves the claim out of trunk's `active/`).

<!-- Outcome recorded below as the sequence completes. -->
