## 2026-09-02 — WI-569: the WI-508 spine reseal — one clean cross-family round, and the two routed BLOCKERs ruled

Deferred open items: none — nothing in this fragment is owed to the owner; the
lane's remainder is queued as an amendment adjudication minted by this row's own
merge.

**One line:** the round the WI-508 lane never landed was drawn on current trunk
and came back `CHANGES-REQUESTED findings=2` — `TC-199`/`TC-200` stand,
`LLR-203`/`LLR-204` did not, because trunk delivered the mechanisms they still
said did not exist; the false sentences were corrected in-lane and the design
remainder handed to the amendment adjudication, and the two routed `5175065`
BLOCKERs were ruled ANNOTATE, no successor.

Worker lane `wi-569-wi-508-spine-reseal-one-clean`, integration base `2f660cb7`.
Successor to the closed `WI-508`, drafted by the `WI-568` adjudication.

### Scope as it actually stood, not as the row was minted

The row was minted carrying a baseline arm — regenerate
`docs/archive/last_approved/` under the owner's `OI-78` ruling. Two merged
predecessors removed that arm from this lane before it started, and the spec's
`## Context` already records the supersession:

- `WI-571` scoped `baseline_snapshot.copy_live` to the act, so a bare
  `intake.py snapshot` on a lane that flips no `Status` copies **zero**
  registries — this row flips none.
- `WI-572` ruled the approval act (every `Status` flip and every
  `docs/archive/last_approved/` write) the adjudicator's alone, on trunk, and
  wired a merge-slot refusal by name against any work lane performing one.

So the lane ran the two arms that remained. Nothing on the spine needed
re-sealing in any case: all four rows are cell-for-cell identical between the
round-010-approved tree `b8d57e9f` and trunk `2f660cb7` — compared by parsing
both `tomllib` and diffing the row dicts, not by eyeballing a `git diff`, since
a trailing-newline artifact makes the textual comparison lie.

### Arm 1 — the cross-family round, and what it found

Drawn on `OPENAI-SOL` (gpt-5.6-sol, `-c model_reasoning_effort=medium`), a
different model family from the author, against a hostile read-only brief that
named the four rows and the standing-claim rule and told it nothing about what
had moved on trunk. It found `WI-543`'s mechanisms itself.
`docs/reviews/wi-569-wi-508-spine-reseal-one-clean/001-REVIEW-A-2f660cb7-spine-rows.md`
— **`VERDICT: CHANGES-REQUESTED findings=2`**, scored `substance=0.667
precision=1.00 action=1.00`, tripwires none.

`TC-199`/`TC-200` **stand, no finding**: seven evidence nodes pass, `verifies`
names the LLR arm and not `SR-163`, `expected` is still true, and TC-199's
shared-node claim with TC-176 is exact (the intersection of the two `evidence`
sets is precisely the two package-direction nodes).

`LLR-203`/`LLR-204` **did not stand**. Three LLR-203 assertions are false of the
tree and one LLR-204 claim is counterfactual; each was falsified by DRIVING:

| the row's claim | driven result |
| --- | --- |
| "no cell joins an inventoried file to a requirement id … no check resolves" | 21 of 148 MAPPING rows carry a reference cell; `--mapping-purpose` reports `unresolved_reference — 0` — all 21 resolve SR → live need |
| "every arm above walks the DESTINATIONS the inventory declares, never the shipped tree" | `bootstrap.delivery_inventory()` walks 213 physical kit sources against 148 MAPPING sources and 31 exclusion rows |
| "the installer is excluded … in prose … rather than as a row in the exclusion carrier" | it is row 19 of the mechanically parsed `project-trajectory/mapping-source-exclusions` |
| LLR-204: the grammar and dial "are what the parent's join and its policy would ride" | the join rides `MAPPING_FINDING_POLICY` and the inventory's reference cell; `read_backlink_min`'s only call site is the backlink report |

fig: driven="`gen_arch_map.py --mapping-purpose --root .` at 2f660cb7 (missing_file 0 / stale_entry 0 / unresolved_reference 0 / unmapped_file 152), and `bootstrap.delivery_inventory()` called in-process at the same commit (213 / 148 / 31 / 34)"

**Deviation from spec, stated plainly.** The row asked for a round *"confirming
the four rows stand"*. It could not confirm them, and a round that must return
APPROVE is not a round. The lane corrected the false sentences in the rows' own
cells (`33aee707`) with `Status` untouched at `Approved` — a lane amends cell
text and never performs the approval act, and
`acceptance_record.lane_approval_refusal` says in as many words that an
amendment to an approved row is not one. Verified merge-legal:
`lane_approval_refusal('.', 2f660cb7, HEAD)` returns `None`.

The DESIGN half of the reviewer's remedy was deliberately **not** taken — which
row owns `resolve_requirement_reference` / `mapping_purpose_findings` /
`MAPPING_FINDING_POLICY`, whether LLR-203's `CodeSymbol` widens, where TC-204's
evidence binds. Those need the whole chain, which one work item does not hold.
It is not left on no queue, which is the exact defect this row exists to remedy:
it is stated as the standing NOT-DISCHARGED gap in LLR-203's own cell, and
`staged_spine_amendments` over `2f660cb7..HEAD` was driven to confirm the
amendment adjudication minted at this merge really does list both rows.

### Arm 2 — the two routed `5175065` BLOCKERs: ANNOTATE, no successor

Both re-verified before ruling. The brief and the returns record are both first
added by `64e9bf2a` (`git log --diff-filter=A`), so nothing immutably fixed the
question before the answers existed; the contamination of the closed five-file
input set is real, and the teams had already disclosed it themselves at the very
line the finding anchors to. Standing caveats now open
`docs/plans/2026-08-25-blind-minimal-map-brief.md` and
`…-derivation.md`, additively — the original text is unchanged, so the record
stays the record — and the brief's dangling pointer to the lane's old
`docs/work/active/` home was repointed to its terminal `partial/` spec.

A sterile re-run was refused on three grounds: it cannot repair the first defect
at all, since immutability is a property of the 2026-08-25 record and a fresh
pre-committed brief would evidence a NEW exercise; no live requirement, design
or test row cites the exercise (grepped `docs/requirements/` and `docs/test/` —
zero hits), so nothing on the spine waits on a better number; and the alignment
pass already adjudicates each divergence against the registry rather than
deferring to either return. The credit was what needed stopping.

### Bar — green, with ONE red stated rather than buried

Commit bar at every commit: `pytest -q -n auto -m smoke` 1459 passed, 8 skipped
in 23.88 s; smoke budget 21.9 s vs 60 s → within; `check_docs --stale` OK, 1233
docs / 1595 links / 0 broken; `trace.py --strict-integrity` integrity=0 with no
new spine finding.

**Full unfiltered suite on the final tree: `1 failed, 3281 passed, 25 skipped in
576.93s`.** The one failure is
`tests/test_derive_stage.py::test_this_repo_s_committed_stage_is_current`, and
it is REAL and MINE — not the pre-existing trunk red it superficially resembles.
I checked instead of assuming: the same node **passes at the integration base**
`2f660cb7` in a detached worktree, so this lane induced it.

What induced it is benign and is the trunk lane's to clear.
`docs/requirements/low-level-requirements.toml` is a DECLARED derivation input
(`kitlib/stage.py` `DECLARED_INPUTS`), and the recorded `fingerprint` is a
SHA-256 over those inputs' bytes — so amending a cell moves the hash by
construction. **The derived values themselves did not move**: `derive_stage.py
--check` reports the same `per-phase = 1=DevStg-Impl;3=DevStg-Impl;
4=DevStg-Impl;5=DevStg-LLReqs` and the same `drafted = 9` that `docs/stage`
already records. Only the input hash differs.

`docs/stage` was deliberately NOT restamped here. It is a generated artifact,
this branch may not write one, and `trunk_step.py`'s `derived-stage` step
regenerates it after the merge — which is exactly why the branch-aware bar
prints `SKIP derived-stage … generated freshness is the trunk lane's,
concurrency-restructure §5.2`. Restamping it pre-merge would compute the hash
over a tree that never exists on trunk and would collide with the trunk step.
The full suite has no such branch-awareness, so it reds; the node sits in
`conftest.SLOW_MODULES`, which is why the smoke commit bar never saw it and why
those greens were honest for what they measure.

The git hooks' `format` step SKIPPED throughout — the hook runs
`/usr/local/bin/python3`, which has no `ruff`, and this lane worktree has no
`.venv`. No Python source was changed on this lane, so nothing was left ungraded
by it.

Byte deltas on budgeted files: none — `AGENTS.template.md` and `PROCESS.md`
untouched.

The baseline arm's open item, `OI-78`, was ruled STAND by the owner on
2026-09-01, so nothing on it is owed to the owner by this lane; the lane's own
remainder is queued as an amendment adjudication that this row's merge mints.

### Rework — REVIEW-A round 002 (supervisor-drawn, `CHANGES-REQUESTED findings=5`)

Four of the five findings were reworked in-lane. No `status` cell moved, no
`intake.py snapshot` ran, nothing under `docs/archive/last_approved/` was
written; the corrections are `detail`/`title`/prose text only.

- **MAJOR — this fragment's `Deferred open items:` line was not file-level.**
  It sat at line 139, inside the last `###` section, so `gen_open_items.py
  --root . --check` exited 1 with two lane-introduced findings: *3 of 4 sections
  carry no deferral declaration* and *:139 declares OI-78 deferred, but that row
  reads `ruled`* (`open_items.toml` carries `status = "ruled"`). The declaration
  now opens the top matter above the first heading, matching
  `WI-575-llr-158-registry-bound.md`, and is widened to speak for the whole
  fragment; the `OI-78` token left the declaration and its account stays in the
  prose at the file's end, where a ruled row is not read as a deferral. The
  check now emits only the pre-existing `docs/open-items.html STALE` advisory,
  which is trunk's and is present at the lane base too.
- **MAJOR — the WI-569 Deliverable contradicted itself on `b8d57e9f`.** Its
  closing clause claimed in the present tense that all four rows *are*
  cell-for-cell identical to the round-010-approved tree, four paragraphs after
  recording that `33aee707` corrected `LLR-203` and `LLR-204`. Re-tensed to the
  moment the reseal question was ruled, with the deliberate drift stated:
  loading `low-level-requirements.toml` and `test-cases.toml` from each of
  `b8d57e9f`, `2f660cb7` and `HEAD` with `tomllib` and diffing the four rows
  cell by cell returns IDENTICAL for all four at the lane base, and at the tip
  `LLR-203 -> ['detail', 'rationale', 'title']`, `LLR-204 -> ['detail']`,
  `TC-199`/`TC-200 -> IDENTICAL`, `status` unmoved on all four.
- **MINOR, treated as required — LLR-203 mis-stated the exclusion grammar.**
  The cell wrote the carrier row as `<source> - <reason>` with a HYPHEN;
  `bootstrap._mapping_source_exclusions` partitions on the literal `" — "`
  (`bootstrap.py:2335`) and the carrier's own header says the same, so a row
  written to the cell's instruction is skipped, excludes nothing, and its source
  resurfaces as a gate-class `missing_file` finding. The cell now quotes the em
  dash inside the code span and names the separator and the failure mode
  explicitly; the surrounding prose keeps its ` - ` dashing, which is what
  caused the drift. No WI/OI citation frame entered the cell.

Finding 3 (a backticked path to `docs/reviews/WI-569-REVIEW-A.md`) is discharged
by the rollup the supervisor compiles over this rework, which makes the citation
true. Finding 5 asked that the scope extension be recorded knowingly rather
than left implicit, and it IS reworked here: the Deliverable now opens with
"A third act, taken knowingly", naming the amendment as beyond the two arms
this row was narrowed to, round 002 as the first independent read of the new
text, and the merge-minted amendment adjudication as the backstop that judges
it unprejudiced.
