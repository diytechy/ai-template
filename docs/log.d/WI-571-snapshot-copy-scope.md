## 2026-09-01 — WI-571: the snapshot copies only what the act authorises

Scoped `baseline_snapshot.copy_live` to the registries an approval act actually
authorises, closing the whole-tree re-seal that dragged off-spine drift into
`docs/archive/last_approved/` on every spine-only approval (the problem the
plan `docs/plans/2026-09-01-snapshot-copy-scope.md` measures from OI-78).

**What changed (`project-trajectory/scripts/baseline_snapshot.py`):**

- `copy_live` no longer iterates all seven `SNAPSHOTTED` registries on a
  refresh. It computes the AUTHORISED set — every registry a `--approves` ref
  names, plus every registry an approving `Status` move happened in (a flip on
  an existing row, or a new row arriving already `Approved`) — and copies only
  those. Every other registry keeps its existing snapshot bytes. The seed path
  (`--seed`) still copies the whole tree once, and an unreadable record is still
  re-mirrored wholesale as the repair path.
  - This is safe against BOTH mirror rules because each is pinned to the file
    it judges: `staged_snapshot_findings` only checks snapshot files IN the
    commit, and `committed_snapshot_findings` compares each snapshot file to
    live AT ITS OWN WRITING COMMIT — so an untouched registry stays green
    forever. "An untouched file is not written" (plan done-when 1).
- `--approves` is now a NAMED list: `parse_approves` turns a `;`-joined
  `REGISTRY=REF` value into `{registry rel: ref}`, and `resolve_registry`
  resolves a token by rel / filename / carrier-less stem. A ref mutes
  `refresh_refusal` for the ONE registry it names and no other (the secondary
  widening the plan's §1 records: `if approves: return ""` muted all seven).
- `_record_approval` records the act's SCOPE into the prose stamp — the
  registries copied and, for each, whether a ref named it or a Status move
  authorised it — so the next reader of `README.md` sees the act's scope, not a
  whole-tree claim (plan done-when 3). Still prose, still parsed by nothing.

**CLI (`intake.py`):** `--approves` metavar/help move to `REGISTRY=REF`
(`;`-joined); `_cmd_snapshot` parses through `baseline_snapshot.parse_approves`.
Net-zero SLOC in intake (parsing lives in `baseline_snapshot`, which has ample
headroom under the 1000-SLOC threshold; intake sits exactly on its 1177
baseline).

**Tests (`tests/test_baseline_snapshot.py`, `tests/test_trace_briefs.py`):**
existing `--approves` callers moved to the named-dict form; new red→green tests
for the scope: a spine flip with off-spine drift present leaves the off-spine
snapshot bytes untouched and the census intact; a named ref copies exactly its
registry and mutes only its gate; the seed still copies all; the mirror
invariant stays green across a scoped act.

**Deferred open items:** OI-78 is NOT ruled here — the rows already absorbed at
`580df781` stay absorbed until the owner rules; this row stops the NEXT act from
absorbing more (plan §2). The queued reseal row `WI-569`'s spec `## Context` is
updated here (triage, not a spine act) to record that, after this lands, its
regeneration re-seals only the four spine rows and the off-spine census survives
to its own review.

**fig: the 9-of-21 history figure** is `git log --format=%h --
docs/archive/last_approved` read at `6000ec9c` (the plan §1 provenance): 9 of
the 21 snapshot commits before `580df781` wrote off-spine files while only spine
`Status` moved.
