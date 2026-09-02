## 2026-09-01 — WI-571 rework: Review-A round 004 transition scope

Review-A round 004 found that the first scoped implementation treated every
Status difference as an authorising flip. This session corrects that at the
single maturity boundary: only a transition into an approval claim (and a new
approved row) authorises a copied registry. The regression pairs an
`Approved` → `Drafted` row with an unrelated approved amendment and proves the
copy is refused and the snapshot stays untouched. This record is started before
the correction's broad verification; its final check results are appended below.

Deferred open items: OI-78 remains explicitly unruled; this correction only
keeps future snapshot acts within their stated authority.

Verification: `tests/test_baseline_snapshot.py`, `test_module_size_ratchet.py`,
`test_trace_briefs.py`, and `test_intake.py` — **112 passed**. The full
`.venv/bin/python -m pytest -q -n auto` completed with the already-known 12
unrelated failures in docs/check-harness/integration/work-registry surfaces;
the snapshot module is not among them. The smoke tier likewise remained
`1452 passed, 8 skipped, 1 failed`: the pre-existing drained-worktree
`test_wi_convert` redirect-stub failure. `check_docs --stale` remains red only
on the pre-existing broken `docs/log.md` WI-572 link; root coordination truth
is outside this claimed lane. `check_smoke_budget.py --mode enforce` reran that
same smoke tier; its timing budget was not breached.

## 2026-09-01 — WI-571 rework: review A (61180ab, CHANGES-REQUESTED, 2 MINOR)

Addressed both findings of `docs/reviews/wi-571-the-snapshot-copies-only-what/002-REVIEW-A-61180ab.md`.

- **[MINOR] baseline_snapshot.py — a Status-move-only refresh wrote no stamp.**
  `copy_live` recorded the approval stamp only `if approves:`, so a refresh
  authorised by a `Status` move alone copied its registry but left the act
  unauditable in the prose stamp the new contract promises. FIX: `_refresh_targets`
  now returns `(targets, first_signing)` and `copy_live` stamps EVERY non-seed
  refresh that copied a registry, passing `approves or {}` so the per-registry
  reason reads `Status move` when no ref named it. The seed and a refresh that
  copied nothing (traced-only re-point) still write no line. README prose and the
  `_record_approval`/`_refresh_targets` docstrings updated to match; new test
  `test_a_STATUS_MOVE_refresh_is_STAMPED_as_a_Status_move` drives it red→green.
- **[MINOR] WI-569 triage claimed a bare snapshot would copy the LLR rows.** The
  triage note asserted this row's approval commit *flips* `LLR-203`/`LLR-204`, but
  the same spec states both are already `Approved` (the KEPT `580df781` flip) and
  the successor only CONFIRMS them, so under the scoped copy a bare `intake.py
  snapshot` moves no `Status` and copies ZERO registries. FIX: corrected the
  triage to say a bare run copies nothing (the LLR rows are already sealed
  byte-identical, so no spine reseal is needed), and to re-seal any registry
  deliberately the row must NAME it with `--approves`.

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
Two-line CLI edge (parse call + the scoped success banner); intake baseline
1177→1179 in the ratchet, reason recorded there. The scope logic lives in
`baseline_snapshot` (386 SLOC, ample headroom under the 1000 threshold).

**C901:** `copy_live`'s scope decision was extracted to `_refresh_targets` so
the writer's branch count stays under the cyclomatic bar (the full-suite run
caught `copy_live` at 11; the extract drops it well below, no ratchet edit).

**Full suite** (`.venv/bin/python -m pytest -q -n auto`, this box): after the
extract, `3239 passed, 23 skipped` across the files this WI touches and their
neighbours; the 11 residual failures in the whole-repo run are pre-existing and
NOT this WI's — 10 are the ruff-0.16 `I001` skew in the scaffolded demo's
`src`/`tests` (`bootstrap.py`, the demo generator, is untouched here, so the
demo lint result is identical on the integration base) and 1 is a broken link
in `docs/log.md` (`log.d/plans/2026-09-01-approval-act-adjudicator-only.md`,
WI-572's plan) that is present at base `78bcea28` and lives in root
coordination truth this branch must not edit. `test_baseline_snapshot.py` (47),
`test_trace_briefs.py`, `test_module_size_ratchet.py`,
`test_complexity_ratchet.py`, `test_intake.py` all green.

**Smoke tier** (`-m smoke`, the commit bar): `1452 passed, 8 skipped`, wall
21.4s vs the 60s budget (`scripts/check_smoke_budget.py --mode enforce` →
within). ONE pre-existing failure, NOT this WI's:
`test_wi_convert.py::test_the_live_registry_round_trips_in_whichever_home_is_authoritative`.
`wi_convert.read_specs` requires every `*.md` inside a status subdirectory of
`docs/work/` to parse as a spec, but `docs/work/cancelled/README.md` is a
no-frontmatter redirect stub ("this directory moved — cancelled/ now lives under
the archive"), so the converter chokes on it whenever the tree is DRAINED (no
in-flight `active/<branch>/` claim). The base commit `78bcea28` carries this
WI's own claim, so there the converter takes the `drained-stop` branch and the
test passes; the FULL-suite run above (on the checkpoint, claim still in flight)
passed it for the same reason. Closing this row drains the claim and re-exposes
the pre-existing state — VERIFIED identical at trunk `b8db16fd` (the claim's
parent, before this WI existed): `active/` empty, `cancelled/README.md` present,
`wi_convert.to_csv` raises the same "does not start with a +++ frontmatter
fence" `ConvertError`. Out of scope here (it is the `docs/work/cancelled/`
coordination tree and the converter's status-subdir README rule, neither this
WI's product surface); surfaced for the trunk lane / owner rather than fixed
inline — the redirect stub wants either deletion (cancelled/ is fully archived)
or a converter exclusion for status-subdir READMEs, which is its own row.

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
