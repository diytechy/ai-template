# Concurrency restructure — design spec (DRAFT, owner rulings pending)

**Branch:** `ConcurrencyTrainRewrite`. **Status:** draft for owner review; nothing
here is implemented. **Goal (owner-stated):** the kit is parallel *out of the
box*, and a full restructure is acceptable. This spec replaces the bespoke
train/dispatcher machinery with git + a thin forge seam, shards the contended
surfaces, and declares the concurrency rules that were previously implicit.

Relationship to prior records: this executes several rulings proposed in
[handoff-2026-07-28c.md](handoff-2026-07-28c.md) by *replacement* rather than
mothball — the train machinery retires because a forge does its job, not
because parallelism was abandoned. The dispatcher's measured record (19
reservations → 8 integrations → 0 gate-verified → 11 rescues) is the evidence
base; the design principle throughout is **fail closed, contend nowhere, one
home per fact**.

> **RULING markers.** Decisions the owner must make are tagged `RULING-n`
> inline and collected in §9. Everything else is proposed as written.

---

## 1. Declared substrates and the dependency policy

### 1.1 Git is a required substrate (RULING-1: confirm)

The process has always assumed git — diffable registries, append-only log,
"ratification is a reviewed Status-change commit," reservations as refs —
without naming it. Declare it in `PROCESS.md` at the same tier as Python 3.11:
**the process requires a git repository.** No fallback story is owed to
non-git environments.

### 1.2 The forge seam (RULING-2: GitHub as reference)

Orchestration control moves to a *forge*: the layer providing pull requests,
required status checks, and a merge queue. The kit declares a **thin seam** —
five operations — and ships one reference implementation (GitHub via `gh`):

| Seam operation | GitHub reference |
|---|---|
| open a change request for a branch | `gh pr create` |
| read its check status | `gh pr checks` |
| record a review verdict | `gh pr review` |
| merge when green (fail-closed) | `gh pr merge --auto` + branch protection |
| composed-tree gating | merge queue (repo setting) |

Fail-closed is structural here: a **required** check that has not passed
blocks the merge. The dispatcher's `skipped (no declared test command)` →
merge-anyway failure class is not fixable in this model — it is unrepresentable.

Adopters on another forge (GitLab, Gitea) implement the same five operations;
adopters with no forge get the degraded serial mode in §5.4.

### 1.3 Dependency policy: stdlib by default, ledger for exceptions (RULING-3)

Owner-stated: stdlib-only is nice but not mandatory; genuinely good tools may
be used and installed by dev-setup — guarded against abuse. Proposed rule:

- **Checks that ship downstream and run in adopter repos stay stdlib** — the
  original portability argument holds for them (`trace.py`, `check.py`,
  `check_docs.py`, …).
- **Coordinator-side tooling may take dependencies**, each recorded in a
  **dependency ledger** (`docs/dependencies.md`): what it is, what it
  replaces, why hand-rolling is worse, and the owner ruling that admitted it.
  Installed by `setup.{sh,ps1}`; CI installs from the same list.
- Enforcement: a test scans coordinator-module imports against the ledger and
  fails on an undeclared dependency. Adding a row is a reviewed, owner-ruled
  edit — that is the abuse guard: not "no dependencies," but "no *unargued*
  dependencies."
- `gh` is a system binary, not a Python package; it enters the ledger with the
  same entry discipline.

The lesson this encodes: applying the stdlib rule to the *orchestrator* is
what forced `agent_dispatch.py` to hand-roll a forge in 4,042 lines.

---

## 2. Work items: specs are the registry

### 2.1 One file per work item; status is location

`work-items.csv` retires. Each work item is one Markdown spec file whose
**directory encodes its status**:

```
docs/work/
  queued/WI-360-forge-seam.md          # filed, unclaimed
  active/<branch>/WI-360-forge-seam.md # claimed by that branch
  archive/WI-360-forge-seam.md         # done (moved by the closing PR)
```

Moves in distinct paths never conflict; two branches claiming the same spec
produce a visible move/move conflict — the reservation collision surfaced by
git itself instead of prevented by CAS refs. The `retired` disposition keeps
its honesty: retirement is a move to `archive/` with a `disposition = "retired"`
frontmatter field and the reason in the body, never deletion.

### 2.2 Frontmatter carries what the CSV row carried

TOML frontmatter (parsed with stdlib `tomllib`, 3.11+ — no dependency needed):

```toml
id = "WI-360"
title = "Forge seam: gh reference implementation"
class = "ordinary"          # ordinary | spine | render (see §3)
priority = 1
needs = ["WI-358"]          # predecessor ids
sr_refs = ["SR-0xx"]
modules = ["project-trajectory/scripts/forge.py"]  # declared touch-set (§3.1)
verification = "Test"
```

**One home per fact is preserved**: mutable state (status) lives in location;
immutable-ish metadata lives in frontmatter; narrative lives in the body. The
scheduler, `check_trajectory`'s DAG validation, and the dashboard all switch
to a spec-folder loader. If a tabular view is still wanted, `work-items.csv`
may survive as a **generated** artifact (RULING-4) — derived, never edited.

### 2.3 The claim protocol (serial, on the trunk)

1. Coordinator commits the move `queued/ → active/<branch>/` **on the trunk**.
2. Coordinator cuts the worker branch *from that commit*.
3. Worker builds; the closing PR itself contains the move
   `active/<branch>/ → archive/`.

Claims are atomic and race-free because step 1 is a serial trunk commit; with
multiple coordinators, push rejection on the trunk is the compare-and-swap.
This replaces `refs/llm/reservations/` entirely, and replaces
`out/dispatch/events.jsonl` with plain git history. Id allocation happens at
filing time on the trunk (serial), eliminating the next-id race.

---

## 3. Concurrency classes

Declared per-spec in `class =`; the coordinator schedules by class.

### 3.1 `ordinary` — parallel

Runs concurrently. The coordinator does not co-schedule two specs whose
declared `modules` touch-sets overlap; overlaps that slip through surface as
normal PR conflicts and are the worker's to resolve by rebasing. The
touch-set is a scheduling *hint*, honestly labeled — not a guard, so it
cannot be a vacuous one.

### 3.2 `spine` — a barrier, not a lane (owner-ruled semantics)

**A spine work item excludes ALL other work, not just other spine work.**
Sequence: the coordinator stops claiming; active branches merge or park; the
spine traincar runs **solo, in a single session**; it merges; claiming
resumes. Spine surfaces (the explicit list, kept in the spec schema doc):
`stakeholder-needs.md`, `system-requirements.csv`,
`low-level-requirements.csv`, `test-cases.csv`, `interfaces.csv`, the process
docs, and this schema itself.

This is stronger than the current scheduler's behavior (which serializes
spine WIs against each other), and it is what makes the model clean: **no
worker can be mid-flight when requirements change**, so the "built against
amended requirements" staleness class is not mitigated — it is
*unrepresentable*, the same way the forge makes fail-open unrepresentable.
The residue is only work *already merged* before the spine change, and that
is the existing re-attestation flow's job, unchanged: the spine WI's own
Done-when includes reconciling affected rows (`Modified` status, sitting,
re-derive). The cost is a drain — acceptable because spine changes are rare
by design, and the drain doubles as the natural moment for the trunk
regeneration pass (§5.2).

### 3.3 `render` — per the pending critique-gate ruling

If SR-054 flips to `Verification=Test` (handoff-2026-07-28c §4 line 3), this
class reduces to `ordinary` plus a periodic advisory critique, and the
class exists only as a scheduling tag for batching. If the standing gate
stays, render specs inherit the batch-attended rule. (RULING-5 — already on
the audit checklist; restated here because it decides whether this class
exists.)

---

## 4. Integration and gating

- **Branch protection on the trunk**: required checks = `check.py` at the
  derived gate + the test tier the gate demands. Nothing merges un-gated —
  including coordinator commits? No: trunk claim/compile commits are direct
  pushes by design (they are serial bookkeeping, not product change) —
  **RULING-6**: confirm this split, or route even bookkeeping through PRs at
  the cost of latency.
- **Merge queue on**: every PR is verified against the composed tree before
  landing. This *is* gated parallel integration; no kit code implements it.
- **Auto-merge**: a worker's publish step is `git push` + `gh pr create` +
  `gh pr merge --auto`. The PR then lands itself when green.
- **Human gates map to forge requirements**: autonomous lanes rely on
  required checks only; lanes the gate-policy marks human additionally
  require a review approval. Note the forge constraint: an identity cannot
  approve its own PR, so autonomous-with-approval lanes need a second (bot)
  identity — or stay checks-only (RULING-7).
- **Degraded serial mode (no forge)**: a one-page script — merge branch into
  an integration branch, run the bar, fast-forward trunk on green, refuse on
  red. Serial only; documented as the floor, not the product. This preserves
  an offline story at ~1% of the dispatcher's size (RULING-8: keep or drop).

## 5. Shared-surface rules (the residual contention, each with its rule)

### 5.1 The log: fragments, compiled serially

`docs/log.md` stays append-only and single — but **no work branch writes it**.
Each branch writes `docs/log.d/<WI-id>-<slug>.md` (unique name → conflict-free
by construction). A serial trunk step (coordinator or post-merge Action)
appends fragments to `log.md` in merge order and deletes them. Merge order is
derived from git history, not asserted. The PR timeline absorbs the
mechanical record (what ran, what passed, who approved); fragments carry the
narrative the log is valued for. Hand-merging the log ends entirely.

### 5.2 Generated artifacts: trunk-only

Work branches **never commit** generated artifacts (`PROJECT_STATE.html`,
arch map, `status.md` generated block, `docs/gate`, `open-items.html`,
`INDEX.csv`). The trunk regenerates them after each merge (same serial step
as 5.1); freshness gates run on the trunk lane only. This deletes the single
largest cause of train merge conflicts. Branch-local checks that *read*
generated artifacts read them as-of-base, which is correct: the composed-tree
check re-derives at the queue.

### 5.3 Stamps and ratchets

Whatever survives the audit's ratchet rulings is re-derived or re-stamped in
the trunk step, never hand-carried on work branches (the module-size ratchet
was re-stamped three times on one row across one train's life — that pattern
ends here).

### 5.4 Review/critique artifacts

Branch-scoped names (`docs/reviews/<WI-id>-A.md`), not serial counters — the
`131-REVIEW-A` numbering is a next-number race under concurrency.

### 5.5 The trunk lane itself

The compile/regenerate step is the one deliberately serial actor. Its rules:
it must be tiny, it must be idempotent, and **its failures block loudly** —
a red trunk lane halts claiming (the fail-open lesson applied to the new
machinery on day one). `docs/pause` retires; "pause" becomes the coordinator
flag that stops claiming — which, unlike the file, cannot fail to stop a
worker, because workers are branch-local and land only through the queue.

## 6. What retires, what shrinks, what remains

| Artifact | Fate |
|---|---|
| `agent_dispatch.py` train/reservation/integration half (~4k lines) | **Retires** — forge + §2.3 replace it |
| `refs/llm/*`, `out/dispatch/events.jsonl`, `docs/run-state`, `docs/pause` | **Retire** — git history, PR state, coordinator flag |
| `work-items.csv` | **Retires** (or becomes generated — RULING-4) |
| WI-289 (compose auto-resolve), WI-343 (ref plumbing extraction) | **Moot** — the contended surfaces stop being written concurrently |
| `agent_loop.py` | **Shrinks** to: claim → branch → launch worker session → publish via `gh`. No lane state machine |
| `agent_route.py` + provider dispatch (`codex`/OpenCode) | **Remains** — heterogeneous review/critique routing is the irreplaceable piece |
| `schedule.py` | **Remains**, loader swapped to spec folders; gains the §3 class rules |
| `check_trajectory.py` | **Remains**, loader swapped; minus the never-fired rules per the audit ruling |
| 36 stale worktrees, 34 `llm/*` branches, orphaned stash | **Cleaned** in migration phase 0 (diff for orphaned *files* first — 2026-07-26 lesson) |

## 7. Migration plan (each phase is itself spine-class: solo, serial)

- **Phase 0 — rulings + hygiene.** Owner answers §9. Clean the train residue.
- **Phase 1 — declarations.** PROCESS.md names git; dependency ledger + its
  enforcement test; forge seam documented.
- **Phase 2 — specs as registry.** Converter generates one spec file per
  existing CSV row (mechanical; frontmatter from columns); loaders in
  `schedule.py` / `check_trajectory.py` / `gen_trajectory.py` switch to the
  folder; CSV becomes generated or is deleted. *The converter is proven by a
  byte-exact round-trip before the CSV is demoted* (the 140-cell lesson).
- **Phase 3 — shared-surface rules.** `log.d/` fragments + trunk compile;
  generated-artifacts-trunk-only; branch-scoped review names.
- **Phase 4 — forge wiring.** Branch protection, required checks, merge
  queue, `gh`-based publish; the shrunken coordinator; first parallel batch
  of two `ordinary` WIs run end-to-end as the acceptance proof (the proof the
  mothball proposal wanted, now against the new machinery: **the journal
  must show the composed-tree check running, and zero hand-rescues**).
- **Phase 5 — deletion.** The train machinery, its tests, and the dead
  surfaces leave; the audit's other approved retirements execute here too.

Phases 1–3 are valuable even if Phase 4 stalls — they de-contend the repo for
attended work as well.

## 8. Residual risks (honest list, post-design)

1. **Forge dependence** — GitHub outage or rate limits halt integration (not
   building). Mitigation: the §4 degraded serial mode, if kept.
2. **Same-module collisions** remain possible (§3.1 hint, not guard) —
   surfaced as PR conflicts; cost is a rebase, not a deadlock.
3. **Trunk-lane bugs** — the compile step is new serial code; kept tiny,
   fail-loud, and mutation-tested before trust (the vacuous-guard lesson).
4. **Secrets/identity for autonomous lanes** — worker agents need push +
   `gh` credentials; scope tokens per-lane; the approval-identity question is
   RULING-7.
5. **Semantic drift between spec body and frontmatter** — two parts of one
   file, but still two encodings; the existing completion-reconciler idea
   (Done-when vs status) re-lands here as "archive move requires all
   Done-when boxes ticked," which is now a *local* check on one file.
6. **Migration-window inconsistency** — between Phases 2 and 5 both loaders
   exist; the dogfood-sync suite pins them equal until the old one deletes.

## 9. Rulings needed

- **RULING-1** — git declared as a required substrate in PROCESS.md.
- **RULING-2** — GitHub/`gh` as the reference forge; seam kept thin enough to
  swap.
- **RULING-3** — the dependency ledger policy as stated (stdlib for shipped
  checks; argued, owner-ruled entries for coordinator tooling).
- **RULING-4** — `work-items.csv`: delete outright, or keep as a generated
  view for the dashboard.
- **RULING-5** — the SR-054 critique-gate flip (already on the audit
  checklist; decides whether the `render` class exists).
- **RULING-6** — trunk bookkeeping commits (claims, compile) as direct pushes
  vs PRs-for-everything.
- **RULING-7** — autonomous lanes: checks-only, or approval-required with a
  second bot identity.
- **RULING-8** — keep the one-page no-forge serial fallback, or declare the
  forge required.
