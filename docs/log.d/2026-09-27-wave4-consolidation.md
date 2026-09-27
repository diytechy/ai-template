## 2026-09-27 — The fourth coordinator session: consolidate the queue, then build by group

The owner closed the previous session asking that the queue shrink rather
than grow ([the handoff](../handoff-2026-09-27-coordinator.md)). This session
consolidated first and builds one lane per group after. Arbitration:
[../reviews/2026-09-27-wave4/ARBITRATION.md](../reviews/2026-09-27-wave4/ARBITRATION.md).

**Open count at start: 50** (49 queued, 1 deferred; the handoff's 49 counts
the queued rows only).
fig: `git ls-tree --name-only HEAD docs/work/queued/ docs/work/deferred/ | grep WI- | grep -v WI-000 | wc -l` at 8aae3af3.

### The consolidation (hand trunk commit, the 2026-09-02 precedent)

The kit's census (`consolidate.census_draft`) refused to run, correctly:
three adjudication rows are queued (WI-604, WI-675, WI-676) and a
consolidation never stacks on a judgement. Its overlap signals (shared
spec, shared SRs, near titles) would also not have seen most of these
groups, which share a surface rather than a spec. So the consolidation is a
hand trunk commit, as the 2026-09-02 restructure was: each absorbed row is
archived under `docs/archive/work/restructured/` with its scope text
untouched and a one-line `Restructured into WI-<host>.` Deliverable; each
host keeps its id, names the absorbed rows in `supersedes`, states why they
are one row, and quotes their Done-when blocks verbatim; inbound hard edges
are re-pointed to the host (WI-541 and WI-545 to WI-620, WI-651's WI-634
edge to WI-638). A host is never a row whose own lineage would chain
through a restructured row (so WI-582 hosts WI-677, not the reverse).

| host | absorbs | the one surface |
|---|---|---|
| WI-582 | WI-677, WI-644 | spine text for the next batch adjudication |
| WI-672 | WI-663, WI-598, WI-619 | the suite's own honesty (one evidence-to-module join) |
| WI-656 | WI-670, WI-626, WI-658 | checker findings that lie |
| WI-651 | WI-666, WI-671 | the approval snapshot and its readers |
| WI-615 | WI-609, WI-613, WI-614, WI-556, WI-668, WI-610, WI-536 | byte-budgeted doctrine, one sitting |
| WI-620 | WI-605, WI-606, WI-551 | the session service |
| WI-621 | WI-608, WI-622 | the record a merge judges |
| WI-616 | WI-617 | absolutes: check, then sweep |
| WI-581 | WI-659, WI-570 | the claim, close and mint path |
| WI-638 | WI-634 | the assumption plan's remaining build |
| WI-657 | WI-539, WI-623, WI-624 | the complexity and readability sensors |

Differences from the handoff's proposal: the three queued adjudications
(WI-604, WI-675, WI-676) are not merged, because an amendment verdict and a
first-approval verdict have different grammars (`adjudicate_brief.VERDICT_GRAMMAR`);
they are judged in one adjudicator session and re-anchored in one act
instead. WI-659 went to the claim-path group, not the snapshot group
(it is `integrate`'s relink). WI-657 hosts the
sensors group from the "quality" triage, which cancelled nothing: every row
in it carries an owner ruling. WI-634 joined WI-638 so one builder finishes
the assumption build. WI-655 (C2 content), WI-667, WI-541, WI-545, WI-557,
WI-618 and the deferred WI-625 stay single.

Ruled on the way (arbitration ruling 1): a design row's `module` cell lists
the modules holding its `code_symbol` entries, which was WI-670's
precondition; the owner may overturn it.

**Open count after the consolidation: 21** (20 queued, 1 deferred), 29
rows absorbed.
fig: the same command after the consolidation commit.

Commit bar at the consolidation: `check_trajectory --strict` clean,
`trace --strict-integrity` 0 integrity, `trace --approve modified --check`
current, `gen_open_items --check` up to date, `check_docs --stale` 0 broken
(six links in the backlog-migration table re-pointed by hand; `spec_move`
left them), smoke 1560 passed / 3 skipped. **Seconds FAILED: 66.8 s and
67.2 s against the 60 s budget**, recorded and not re-stamped. The box was
loaded: the same tier at the parent commit 8aae3af3, in a fresh worktree
at the same minute, took 92.45 s, and it took 30.2 s at the OI-88 commit an
hour earlier. The change moves spec files and edits prose; it adds no test.
