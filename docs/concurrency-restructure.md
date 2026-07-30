# Concurrency restructure — design spec (RULED; Phases 0–4 executed)

**Branch:** `ConcurrencyTrainRewrite`. **Status:** all §9 rulings answered
2026-07-28; Phases 0–4 are **implemented** (per-phase records in §7) and the
Phase 4 acceptance proof PASSED — only Phase 5 (deletion) remains. **Goal (owner-stated):** the kit is parallel *out
of the box*, and a full restructure is acceptable. This spec replaces the bespoke
train/dispatcher machinery with git + a thin integration seam — local serial
integrator by default, forge as the optional online backend — shards the
contended surfaces, and declares the concurrency rules that were previously
implicit.

Relationship to prior records: this executes several rulings proposed in
[handoff-2026-07-28c.md](handoff-2026-07-28c.md) by *replacement* rather than
mothball — the train machinery retires because a forge does its job, not
because parallelism was abandoned. The dispatcher's measured record (19
reservations → 8 integrations → 0 gate-verified → 11 rescues) is the evidence
base; the design principle throughout is **fail closed, contend nowhere, one
home per fact**.

> **RULING markers.** Decisions were tagged `RULING-n` inline and collected in
> §9. **The owner answered all eight on 2026-07-28** — §9 records the rulings;
> the inline markers stay for traceability. v1 (pre-ruling) is the prior
> commit of this file.

---

## 1. Declared substrates and the dependency policy

### 1.1 Git is a required substrate (RULING-1: confirm)

The process has always assumed git — diffable registries, append-only log,
"ratification is a reviewed Status-change commit," reservations as refs —
without naming it. Declare it in `PROCESS.md` at the same tier as Python 3.11:
**the process requires a git repository.** No fallback story is owed to
non-git environments.

### 1.2 The integration seam — local-first, forge optional (RULING-2: revised)

One flow everywhere: **branch → change request → required checks on the
composed tree → merge.** The seam is the five operations below; *who enforces
them* is a backend choice, and the owner ruled the default is local:

| Seam operation | Local integrator (default) | GitHub backend |
|---|---|---|
| open a change request | branch appears in `docs/work/active/` | `gh pr create` |
| read check status | integrator runs the bar itself | `gh pr checks` |
| record a review verdict | verdict artifact in the branch | `gh pr review` |
| merge when green (fail-closed) | integrator refuses on red, ff on green | `gh pr merge --auto` + protection |
| composed-tree gating | serial integrator ⇒ candidate **is** the composed tree | merge queue |

- **Local integrator** — a deliberately tiny serial trunk lane on this
  machine: take the next finished branch, merge onto a candidate, run the
  required checks, fast-forward the trunk on green, refuse **loudly** on red.
  Because it is serial, composed-tree gating falls out by construction — it
  is a one-page merge queue. No network, no push, no secrets.
  `workers = 1` degenerates to the attended serial flow with **no separate
  structure** (RULING-8).
- **Forge (GitHub via `gh`)** — the same flow for repos that live online;
  enforcement moves server-side (branch protection + required checks + merge
  queue), out of any local agent's reach entirely.

**Why a PR is not just a local merge — the honest answer:** mechanically it
*is* one. A PR is a server-held request to merge a branch, with policy
attached; there is no such thing as an offline PR. The difference is **where
enforcement lives**, not what happens to the commits. Locally, the integrator
script is the enforcement point — trust equals its one page of audited,
mutation-tested code plus the rule that workers never write the trunk. On a
forge, the server refuses an un-green merge no matter what any agent does or
skips. The threat model in this repo is bugs and fail-open (the dispatcher's
`skipped → merged anyway` record), not malice — and a fail-loud one-page
integrator answers that adequately; the forge answers it structurally.
Adopters choose by where their repo lives; the artifacts and flow are
byte-identical either way.

### 1.3 Dependency policy: stdlib by default, ledger for exceptions (RULING-3)

Owner-stated: stdlib-only is nice but not mandatory; genuinely good tools may
be used and installed by dev-setup — guarded against abuse. Proposed rule:

- **Checks that ship downstream and run in adopter repos are
  stdlib-preferred, not stdlib-absolute** (owner ruling): if a genuinely
  cleaner tool exists it *may* be shipped downstream — expected rare, ideally
  never. Such an entry sits in the ledger's **exceptional tier**, because it
  makes every adopter install it; the bar is correspondingly highest.
- **Coordinator-side tooling may take dependencies**, each recorded in the
  **dependency ledger** ([dependencies.md](dependencies.md), live as of
  Phase 1): what it is, what it replaces, why hand-rolling is worse, and the
  owner ruling that admitted it.
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
  deferred/WI-280-core-decomposition.md# parked with its reason (first-class,
                                       #   as today's `deferred` status is)
  archive/WI-360-forge-seam.md         # done (moved by the closing merge)
```

Phase 2a grammar (fixed with the converter, so design and code cannot
drift): frontmatter is TOML between `+++` delimiter lines; the long
`Deliverable` record lives in the **body** under `## Deliverable` (verbatim
prose — no escaping problems by construction); filenames are
`<id>-<slug>.md` with a ≤40-char kebab slug from the title; `needs` tokens
keep the `~` soft-dependency prefix verbatim; the converter **refuses** any
status outside `done/retired/queued/deferred` (a classifier that cannot
finish is louder than a catch-all) and refuses to materialize into a
non-empty target without `--force` (no accidental second home).

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
to a spec-folder loader. **RULING-4 (ruled): no CSV at all** — neither
hand-edited nor generated. Everything the CSV provided (the DAG, the ready
frontier, status counts, SR-Refs traceability) is derived by scanning
frontmatter at run time; a tool wanting a table builds it in memory. One
encoding on disk, zero parallel homes.

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

**RULING-5 (ruled): agreed.** SR-054 flips to `Verification=Test`
(handoff-2026-07-28c §4 line 3), so this class reduces to `ordinary` plus a
periodic advisory critique; the tag survives only as a batching hint so
render-touching specs share one critique dispatch.

---

## 4. Integration and gating

- **Required checks are declared once** (`stack.ini` at the derived gate) and
  the integrator — either backend — merges only on green. A missing or empty
  check declaration is a **refusal**, never a skip (the fail-open lesson,
  stated as a contract).
- **Composed-tree gating**: the serial local integrator provides it by
  construction (§1.2); forge mode gets it from the merge queue.
- **RULING-6 (ruled)**: coordinator **bookkeeping** (claims, fragment
  compile, artifact regeneration) commits directly to the trunk — it is
  serial, content-free bookkeeping by design. **Product changes reach the
  trunk only through the integrator's merge**, made `--no-ff` so merges are
  distinguishable in history. Mechanized: a check flags any non-merge trunk
  commit that touches paths outside the bookkeeping surfaces
  (`docs/work/`, `docs/log.d/` compilation, generated artifacts).
- **RULING-7 (ruled): the config already exists** — `docs/gate-policy`,
  `docs/push-policy`, and the review-policy dial are the human-gate
  declarations. The integrator reads them and requires the corresponding
  verdict artifact (review file, critique, attestation) before merging; no
  new mechanism. The second-bot-identity question is **forge-mode only**
  (a forge account cannot approve its own PR) and is deferred until forge
  mode is used with approval-required lanes.
- **RULING-8 (ruled): there is no separate serial fallback.** The local
  integrator is not a degraded mode — it is the default backend of the one
  flow. `workers = 1` *is* serial operation, with nothing extra maintained.

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
machinery on day one). Pause is formalized in §5.6 — a capability kept, at
the checkpoints where it can be honest.

### 5.6 Pause — drain to a clean, merged stop (owner-ruled semantics)

The old `docs/pause` had the right idea at the wrong moment: its one live
failure (2026-07-26) was being *expected* to stop a mid-flight worker, which
it structurally never could. The capability survives with **one meaning**:

**Pause = stop claiming. Everything in flight finishes, integrates, and
archives.** A full stop is a *drained and unloaded* stop — a traincar always
tries to unload (merge to trunk); the pause never strands finished work on a
branch. The only thing that stops an unload is the **integrator's own
refusal** (red bar, missing required verdict) — and that is the gate
working, not the pause: broken work is never force-merged to satisfy a
drain. A pause therefore ends in exactly one of two visible states: fully
merged and quiet, or fully merged except N branches parked red — each red a
finding to work, not a limbo.

(A second scope considered in an earlier draft — holding finished branches
unmerged for inspection — is **rejected**: completed-but-unmerged work is
precisely the stranded-train pathology of the old machinery, and no use for
it survives the always-unload rule. Inspection happens on the trunk, where
every merge is a `--no-ff` commit that can be reverted.)

Form: a **tracked** file, `docs/work/pause` (TOML: `reason`, `since` — no
scope field; one meaning needs none), committed by the bookkeeping lane.
Tracked fixes three defects of the old file at once: it survives clones, the
reason is diffable history instead of a stale local note, and unpausing is
an auditable commit. The coordinator reads it before every claim; the spine
barrier (§3.2) is this same drain performed automatically — one mechanism,
two users. What no file can ever do — stop a running session — stays stated
plainly: that remains "kill the worker." Status generation surfaces
`paused since <date>: <reason>` so an open pause is a visible accruing cost,
never a forgotten one (the stale-reason lesson).

## 6. What retires, what shrinks, what remains

| Artifact | Fate |
|---|---|
| `agent_dispatch.py` train/reservation/integration half (~4k lines) | **Retires** — forge + §2.3 replace it |
| `refs/llm/*`, `out/dispatch/events.jsonl`, `docs/run-state` | **Retire** — git history and spec location replace them |
| `docs/pause` (untracked, dispatcher-scope) | **Replaced** by tracked `docs/work/pause` — drain to a clean, merged stop, §5.6 |
| `work-items.csv` | **Retires outright** (RULING-4: no generated CSV either) |
| WI-289 (compose auto-resolve), WI-343 (ref plumbing extraction) | **Moot** — the contended surfaces stop being written concurrently |
| `agent_loop.py` | **Shrinks** to: claim → branch → launch worker session → hand off to the integrator (local by default, `gh` in forge mode). No lane state machine |
| `agent_route.py` + provider dispatch (`codex`/OpenCode) | **Remains** — heterogeneous review/critique routing is the irreplaceable piece |
| `schedule.py` | **Remains**, loader swapped to spec folders; gains the §3 class rules |
| `check_trajectory.py` | **Remains**, loader swapped; minus the never-fired rules per the audit ruling |
| 36 stale worktrees, 34 `llm/*` branches, orphaned stash | **Cleaned** in migration phase 0 (diff for orphaned *files* first — 2026-07-26 lesson) |

## 7. Migration plan (each phase is itself spine-class: solo, serial)

- **Phase 0 — rulings + hygiene.** ~~Owner answers §9~~ **done 2026-07-28.**
  Remaining: clean the train residue.
- **Phase 1 — declarations.** PROCESS.md names git; dependency ledger + its
  enforcement test; the integration seam documented (both backends).
- **Phase 2 — specs as registry.**
  **2a is DONE (2026-07-28):** the converter + `tests/test_wi_convert.py`
  — the round-trip over the live registry is **cell-exact and byte-identical**
  (354 rows, all 17 columns, quoting included; the 140-cell lesson satisfied
  outright). The converter was **meta-repo tooling (`tools/wi_convert.py`)
  until 2c**: shipping it in `project-trajectory/scripts/` earlier would have
  demanded spine containment (a new SR/LLR — a barrier edit and an open window)
  for a tool whose target format the kit did not yet ship. It moved to
  `project-trajectory/scripts/wi_convert.py` at **2c-i**, the pre-flip half of
  the authority flip — see that entry below.
  **2b (loader swap), re-scoped by the consumer inventory (2026-07-28):**
  migrate only the SURVIVING consumers — `schedule.load_wis` +
  `check_trajectory.load_wis` (each keeps its OWN folder loader, drift-guard
  extended, per the F5/WI-291 pattern), `gen_trajectory` (reads via
  `schedule`; a re-point), `agent_common.load_wi_registry`, and
  `plan_artifacts` (id allocation becomes the §2.3 trunk-serial claim; its
  append-a-row becomes write-a-file-in-`queued/`). The dispatcher's write
  paths (`_rewrite_wi_rows` + 4 sites, `_union_registry`,
  `registry_rows_at`) are **not ported — they die with Phase 5**; porting
  code scheduled for deletion is waste. Step 0 of 2b: collapse the six
  copy-paste test fixture builders into one conftest helper. Design notes
  fixed now: `blocked` gets **no directory** — it is `queued/` plus a
  `blockref` frontmatter key (the only writer of `Status=blocked` is the
  retiring blocked-disposition path; readiness is the scheduler's to derive);
  and backlog-staleness/freshness must track a spec by **id, following
  renames**, or every status move silently resets its clock.
  **2b is DONE (2026-07-28):** the three F5-duplicated spec-folder readers
  (byte-identical block in `schedule`/`check_trajectory`/`agent_common`)
  emit CSV-shaped rows, so every `load_wis` and downstream consumer is
  untouched; dual-read resolves to the folder when `docs/work/` holds specs,
  else the CSV; the validator alone errors on both-present. Representation
  equivalence is proven (one fixture → CSV and folder via `wi_convert` →
  four loader outputs agree), 12 source mutations each shown RED.
  **Measured correction to the note above:** `git log --follow` ALONE does
  not preserve the clock — a pure rename still answers the rename commit;
  the working pair is `--follow --diff-filter=AM`, pinned by a four-way
  mutation test. Carried to Phase 4/5: `agent_loop.py:1636` and three
  `agent_dispatch` sites still call `schedule.load_rows` directly (empty
  registry in a folder-only tree) — the agent_loop one-word re-point is owed
  when Phase 4 shrinks it; and `schedule.classify`'s `blocked` branches are
  reachable only from the CSV home, dying with it.
  **2c-i is DONE (2026-07-29)** — the PRE-FLIP half, everything that can be
  green while the CSV is still authoritative. The converter moved to
  `project-trajectory/scripts/wi_convert.py` (history followed) and the kit now
  SHIPS the second home: `bootstrap.py` scaffolds
  `docs/work/{queued,active,deferred,archive}/` plus the inert
  `WI-000-example.md`, whose body carries the folder model's schema
  documentation translated from the CSV template's `-000` cell.
  `plan_artifacts.file_selected_wis` dual-WRITES — spec files into
  `docs/work/queued/` when the folder is the home, CSV rows otherwise, with ids
  allocated over the UNION of both homes so no transition state can mint a
  duplicate. The live round-trip proof is now representation-CONDITIONAL, and
  the agent_loop re-point carried from 2b landed.
  **One design change the scaffold forced, measured not assumed:** an example
  spec cannot decide authority. Scaffolding `WI-000-example.md` beside the CSV
  template made the folder authoritative in every fresh repo — empty registry,
  plus `two registries present` on the first check — so `spec_registry_dir`
  excludes `WI-000-*` in all three verbatim copies. It is the `-000` rule the
  kit already applies to every registry template, and it is the AUTHORITY rule
  only: `read_spec_rows` still parses the example, `load_wis` still skips it.
  **Known-red, and the FLIP commit's to fix, not this one's:**
  `check_trajectory --strict` reports `scripts/wi_convert` as an arch-map module <!-- path-ok: the arch-map MODULE label the error quoted, not a file path -->
  in no CMP-### component. Containing it is a spine edit (an LLR `Component`
  cell), which is exactly the barrier the flip commit is.
  **2c-ii — THE FLIP — is DONE (2026-07-29), solo and attended (the §3.2
  barrier, self-applied).** `docs/work/` materialized from the CSV by the
  proven converter (354 specs + the example); the CSV deleted; the CSV
  template de-scaffolded (kept as the legacy-format reference). Spine
  amendment, cell-edited with a byte-identity round-trip proven first:
  SR-050/SR-055/LLR-034/LLR-051/LLR-056 re-grounded on the folder home
  (→`Modified`), **SR-129/LLR-136/TC-129** added for the converter (→CMP-005,
  clearing the known-red), IF-023/024/053/054/061 amended to v2,
  **IF-078/IF-079** declared. **SR-054 flipped `Critique`→`Test` (RULING-5,
  executed)** — `perceptual-stale` cleared with it; the T4/T8 perceptual
  clauses become the periodic advisory critique of §4-line-3's ruling.
  Fresh-scaffold filing fixed: an absent CSV plus a scaffolded `docs/work/`
  files specs (never resurrects the CSV), mutation-proven. Historical links
  to the CSV redirected to the folder home (the WI-288/353 relink precedent);
  `check_docs` scopes `docs/work/*` out as DATA (registry records are not
  navigable prose — and its `--ignore` now uses the house spanning-glob
  semantics, regression-tested, because `Path.match` silently missed nested
  paths). The session-protocol skill (×3), PROCESS_OPTIONS' registry
  definition, README, ADOPTING's migration note and CLAUDE.md re-grounded.
- **Phase 3 — shared-surface rules — is DONE (2026-07-29), solo and attended.**
  All four §5 rules landed as code, each with its tests:
  **§5.1** — `project-trajectory/scripts/trunk_step.py --compile-log`: every
  `docs/log.d/*.md` fragment validated before any write (name shape, `## `
  heading, the three reserved section headings refused, committed-in-HEAD
  required — an uncommitted fragment is a loud error), ordered by **git
  add-time** (merge order derived from history, filename tie-break), relative
  links rebased `docs/log.d/` → `docs/`, appended via the pinned
  `append_log_summary` primitive, fragments deleted after compile,
  all-or-nothing. `bootstrap.py` scaffolds `docs/log.d/`; the worker prompt
  and the session-protocol skill route a work branch's session record to a
  fragment. **§5.2** — `check.py` learns the one branch fact the registry
  already encodes: a branch is a *work branch* iff `docs/work/active/<branch>/`
  exists (fail-closed to full checks off-git/detached/`..`); the seven
  trunk-freshness steps (`arch-map`, `trajectory-map`, `status-map`,
  `open-items`, `okf`, `ratify-fresh`, `derived-gate`) **SKIP with a stated
  §5.2 notice** there — `skills-sync`/`trajectory`/`registry-integrity` still
  run, and `resolve_gate` still reads `docs/gate` as-of-base. `stack.ini
  [generated]` now declares the complete trunk-regenerated set (gate,
  open-items, ratify, skills INDEX added); the retiring dispatcher's
  auto-resolve reads the new kinds as unknown and **parks for a hand-merge
  instead of running a wrong regenerator** — fail-closed, loud, moot at
  Phase 5. `trunk_step.py --regen` is the trunk lane's regeneration half —
  **measured deviation from the §5.2 sketch: `derive_gate` runs BEFORE the
  dashboard/status regens**, because `docs/gate` is their input, not their
  output (regenerating it last leaves both stale in one pass). This phase's
  own artifacts were regenerated by it (dogfood). **§5.4** — flat critique
  selection (`check_trajectory._latest_critique_file`) stops trusting the
  serial-number convention: latest by **git commit time** (one batched
  `git log`, 0.09 s vs 1.35 s per-path), mtime then filename as the fallback
  ladder, both naming generations accepted; the convention is now
  `docs/reviews/WI-<n>-<PHASE>.md` (PROCESS_OPTIONS), historical `NNN-` files
  untouched. **§5.6** — tracked `docs/work/pause` (TOML `reason`/`since`)
  shipped: `agent_common.tracked_pause` fails closed on malformation,
  `pause_reason` reads legacy-home-first so the retired-in-place dispatcher
  can never resume on the home swap, and `gen_trajectory._pause_pending`
  renders `Paused since <date>` in the committed-tree-pure pending region (no
  clock; the spec-folder loaders provably ignore the file). This repo's pause
  **migrated**: untracked `docs/pause` deleted, tracked file committed.
  **Spine:** SR-006/LLR-006 → `Modified` (the lane clause); SR-130/SR-131 +
  LLR-137/138/139 + TC-130/131 added (`Draft`) — the amendment **window is
  OPEN**, gate re-derived down until the sitting, brief
  `docs/ratify/2026-07-29b-phase3.md`. Bookkeeping re-stamped with reasons:
  module-size ratchet (5 modules), dupes census 203 → 213 (ten additions in
  established F5 classes + one new `link-rebase` class + the WI-347
  clique-re-pairing effect on three git-wrapper lines), smoke tier at 636 of
  its 640 ceiling (headroom noted, not re-stamped).
- **Phase 4 — the integrator — is DONE (2026-07-29), and the acceptance proof
  PASSED.** `project-trajectory/scripts/integrate.py` (CMP-004; SR-132 chain)
  is the §1.2 seam's default backend: `claim` (the §2.3 serial trunk claim —
  refusal ladder: paused / dirty / branch-exists / unsafe-name / non-ordinary
  / off-frontier — with **regeneration folded into the claim commit**, RULING-6
  applied after the first live claim was blocked by its own freshness floor),
  `integrate` (the serial queue: `--no-ff --no-commit` merge onto a reusable
  candidate worktree, the §5.1/§5.2 trunk step folded into the merge commit,
  the DECLARED bar on the composed tree read **fail-closed** — missing/empty
  declaration refuses, any SKIP in the report refuses, exit 0 alone is not
  evidence — the RULING-7 verdict gate with **git-derived freshness**
  replacing the old sha7 filename binding, ff-only trunk advance, loud park
  on red), and `audit` (RULING-6 over the queue's own `--since` window —
  **scoped**, because the unconditional form flags attended serial work;
  widening it is an owner ruling, left open deliberately). The coordinator
  shrink is realized as this new small module rather than surgery on
  `agent_loop.py`, whose train half dies wholesale at Phase 5.
  **The acceptance proof:** WI-355 and WI-346 (both keep-ruled genuine,
  disjoint modules) claimed through `integrate.py claim`, built by two
  parallel worker sessions in isolated worktrees under the full branch
  discipline (log fragments, no generated artifacts, freshness steps
  auto-skipping on the claimed branches), each independently REVIEW-A'd by a
  fresh-context session (verdicts `docs/reviews/WI-355-REVIEW-A.md` APPROVE
  f=2-minor and `WI-346-REVIEW-A.md` APPROVE f=2-minor, both at branch tip),
  then merged by the queue: **`95ff7ef` (wi-346, bar PASS 34 steps tier all)
  and `43d90ef` (wi-355, bar PASS 32 steps tier all), audit clean — product
  changes arrived by merge only, zero hand-rescues in the queue run.**
  **What the acceptance surfaced and fixed en route** (each a live refusal,
  fixed on the trunk, none papered over): the claim staled its own floor
  (Phase 4a fix: regen folds into the claim commit); `wi_convert` crashed on
  the claim's `active/<branch>/` shape — now a **drained-stop refusal by
  name** (Phase 4b; SR-129/LLR-136 → `Modified`, in this window); a
  merge-staged fragment's adding commit lives on MERGE_HEAD, not HEAD
  (Phase 4c: `added_at` retries there and only there); a refusal-parked
  candidate worktree could not be reused (Phase 4d).
  **Surfaced and FILED, not fixed** (the findings register:
  WI-357..WI-360): the closing commit un-claims its own branch on disk
  (§2.3/§5.2 collision, hit three times — the emptied claim dir left on disk
  is the standing workaround); R-D reds at merge when trunk status.md prose
  names an in-queue WI (pre-scrubbed by hand this run, `55777cc`); integrator
  unload is incomplete while a worker worktree holds the merged branch
  (`branch -d` swallowed); one unpinned lookup assertion from the REVIEW-A
  minors. Also observed working as designed: the wi-346 reviewer's verdict
  commit was blocked by the un-claim collision and the reviewer REFUSED
  `--no-verify` — the commit landed by restoring the on-disk lane signal, no
  hook bypassed anywhere in the phase.
- **Phase 5 — deletion.** The train machinery, its tests, and the dead
  surfaces leave; the audit's other approved retirements execute here too.
  **The concrete scope, compiled at the Phase 4 close so a fresh session can
  run this from the spec alone** (each item's fuller note lives where cited;
  Phase 5 is itself spine-class — solo, attended, one session where
  possible):
  1. **`agent_dispatch.py` retires whole** (§6) with its tests
     (`test_agent_loop_integrate/dispatch/train/recovery/dualplan`,
     `test_agent_dispatch_decisions` — audit each file for the non-dispatch
     helpers it also covers before deleting). With it die: `refs/llm/*`
     conventions, `out/dispatch/events.jsonl`, `docs/run-state` (+ its
     `_runstate_pending` surface in `gen_trajectory` and the run-state prose
     in PROCESS_OPTIONS), the `docs/blackout` reader if nothing else holds
     it, and `score_reviews.latest_phase_verdicts`' train-form consumers.
     `agent_route.py` + heterogeneous critique dispatch REMAIN (§6).
  2. **`agent_loop.py` shrinks or retires**: the Phase 4 coordinator lives
     in `integrate.py`, so what remains of agent_loop is the worker-session
     launch seam (`agent_session.py` is standalone) and the reviewer/critique
     prompts — decide shrink-in-place vs extract-and-delete; the train
     vocabulary in WORKER_PROMPT (`Train:`, `llm/train/`) re-grounds on the
     §2.3 claim model either way. `agent_common.pause_reason`'s legacy
     untracked-`docs/pause` half retires (agent_common:250); the root
     `agent-resume.*` launchers re-point at the new flow or leave.
  3. **The CSV registry home dies**: the dual-read in
     `schedule`/`check_trajectory`/`agent_common` collapses to folder-only
     (the F5 triplicated reader becomes the only reader;
     `tests/test_module_size_ratchet.py` entries for `agent_common` (+228 and
     +15 stamps) and `check_trajectory` re-stamp DOWN per their own comments;
     `schedule.classify`'s `blocked` branches die with the CSV);
     `wi_convert` keeps the legacy-format reference role; the
     `wi-schema-columns` census class shrinks to one home (dupes-allow:709).
  4. **Census + ratchet re-stamps that Phase 5 owns**: the `link-rebase`
     class (agent_dispatch == trunk_step) dissolves (dupes-allow:183,540);
     every `git-wrapper`/`cli` row naming agent_dispatch leaves; re-derive
     the whole census on the post-deletion tree (the WI-347 clique effect
     will re-pair survivors — classify, don't silently accept).
  5. **`[generated]`'s dual duty dissolves** (auto-resolve allowlist vs
     §5.2 trunk-regenerated set — the design smell filed at Phase 3) once
     agent_dispatch's reader is gone; reconcile `trunk_step.REGEN_STEPS`
     (6 families) against `[generated]` (10) while there.
  6. **PROCESS_OPTIONS' parallel-dispatch section rewrites** onto the
     §1.2/§2.3 model (the train-scoped verdict naming at ~:2330, the lane
     files, `docs/pause` mentions) — byte-budget-guard before/after, baseline
     re-stamp ×3 copies.
  7. **The audit's approved retirements** (handoff-2026-07-28c §3, as
     superseded by this spec's replacement approach): WI-343 is moot if
     agent_dispatch deletes (§6 table) — retire its row with that reason;
     re-examine WI-350/351/356 against the owner's audit rulings before
     grinding them.
  8. **Then the acceptance follow-ups become buildable**: WI-357 (the
     close-un-claims-lane fix — design it against the post-deletion
     loaders), WI-358, WI-359 (integrator unload/worktree GC), WI-360.
  Exit bar: full suite green on the shrunken tree, census re-derived,
  `--strict` clean, a §7 record here, and the spine amendment for whatever
  rows the deletions amend (SR-116/117/125 and friends go `retired`-shaped
  or `Modified`) — a window and a sitting, same as every phase.
  **Phase 5 is DONE (2026-07-29, solo and attended; window CLOSED — the
  sitting attested same-day, ruling in log.md's Decisions).** All eight compiled points executed, nine commits on the trunk
  lane; the mechanical test-fixture conversions ran as three parallel
  read-limited subagents on disjoint files while the production edits stayed
  serial in the one session. The record, point by point:
  1. `agent_dispatch.py` (4,042 lines) deleted whole with seven test
     modules (the six named + `test_agent_loop_migration.py`, audited
     dispatcher-only — a deviation-with-reason). Surviving coverage
     relocated first (`test_agent_common_harness.py`,
     `test_dual_plan_round.py`); `docs/run-state` + every reader, the
     `refs/llm` advisory machinery in gen_trajectory/gen_open_items, the
     commit-msg train floor (WI-282), and `agent_route`'s dead `run_state`
     keys left with it. **`docs/blackout` SURVIVES** — measured, not
     assumed: agent_loop's own session-boundary check consumes it
     independently, answering this entry's "if nothing else holds it" open
     question. The WI-286 venv-floor preflight died with its only caller —
     nothing surviving had the guarantee, so re-homing it is **WI-361**,
     not a silent port.
  2. `agent_loop.py` **shrunk in place** (the audit showed its train half
     was thin — a re-export shell): docstring + WORKER_PROMPT re-grounded
     on §2.3 (`WI:` trailer alone; `Train:`/`Base:` keyed dead machinery),
     `--train` demoted to the optional session tag defaulting to the branch
     name, the llm/train branch-equality preflight reduced to its
     fail-closed core (a worker runs on a branch), the legacy untracked
     pause half deleted (tracked `docs/work/pause` is the one home, a stray
     local file now inert by test), launchers/templates de-dispatchered
     (AGENT_JOBS gone).
  3. The CSV home died: all three F5 reader copies folder-only
     (`spec_registry_dir` deleted; a stray `work-items.csv` is the
     validator's named integrity ERROR), `blocked` derived (queued +
     blockref) in `schedule._disposition` AND — found by the fixture
     conversion, fixed rather than accepted — in `gen_trajectory._wi_status`,
     which would otherwise have silently erased the WI-272/M-2
     parked-vs-queued distinction. `plan_artifacts` files specs only;
     `build_scope_srs`/`critique_control` re-pointed off their direct CSV
     reads (silently EMPTY since the 2c flip — the census classification at
     item 4 exposed it). Ratchets re-stamped DOWN per their own scheduled
     comments (agent_common 1720→1642, check_trajectory 3122→3039).
  4. Census re-derived twice (208→181 at the deletion, reconciled again on
     the final tree): six all-dispatcher classes dissolved, one pair
     re-paired then DISSOLVED with the defect it shadowed; the unchecked
     header aggregates deleted per the WI-356 ruling; the WI-350 same-file
     majority rule retired to a Reviewer-tier enforcement-audit row after
     false-positiving on the honest shrink.
  5. `[generated]` is single-duty (§5.2 trunk-ownership declaration; the
     auto-resolve half died with its reader) in both stack.ini copies + the
     template; the REGEN_STEPS asymmetry is documented as
     ownership-vs-regenerator, deliberately not derived.
  6. PROCESS_OPTIONS' parallel-dispatch section rewrote onto the
     §1.2/§2.3 seam (166,953→161,117 bytes, −5,836 — the deletion
     dividend; baselines re-stamped ×3).
  7. WI-343 retired (moot, as §6 predicted), WI-350/351/356 retired per the
     audit rulings — each with its full record in `docs/work/archive/`.
  8. WI-357..360 remain queued (buildable, per the plan); the phase FILED
     three more: **WI-361** (venv-floor re-home), **WI-362** (the staleness
     clock is blind to a Title rename — measured at conversion), **WI-363**
     (gen_arch_map scans empty under any dot-prefixed absolute path —
     pre-existing, isolated at conversion).
  **Spine amendment (window closed at the 2026-07-29 sitting — all 26 rows
  + TC-133 blessed, G3 re-derived):** 15 dispatcher SRs superseded →
  SR-132 (the TC-099 pattern: `Superseded:` titles, Inspection, no LLRs,
  the new TC-133 + `test_phase5_supersession_rows_...` pin the map); 11
  SRs re-grounded (SR-026/057/059/060/107/108/115/116/124/125/131); 15
  LLRs + 10 TCs deleted with their machinery; IF-067 deleted, six IFs
  re-versioned, **IF-080/IF-081 declared** (integrate.py + trunk_step.py —
  clearing the two standing connectivity warns). Brief:
  `docs/ratify/2026-07-29d-phase5.md`. Residue stated honestly: the §6
  fate line "check_trajectory minus the never-fired rules" was NOT in the
  compiled scope and was not done (the audit's §4-line-6 ruling remains
  the owner's); the loop's managed review verdicts still write tag-scoped
  `NNN-` names (both naming generations accepted since §5.4); and
  `schedule.load_rows`/`cell_integrity_errors` survive with test-and-spine
  consumers only.

Phases 1–3 are valuable even if Phase 4 stalls — they de-contend the repo for
attended work as well.

## 8. Residual risks (honest list, post-design)

1. **Worker writes the trunk (local mode)** — nothing physically stops a
   buggy worker from committing to trunk on this machine; enforcement is the
   §4 mechanized check (non-merge trunk commit touching product paths = red)
   plus worktree isolation. The threat model is bugs, not malice; if that
   ever changes, forge mode is the structural answer.
2. **Same-module collisions** remain possible (§3.1 hint, not guard) —
   surfaced as ordinary merge conflicts at the integrator; cost is a rebase,
   not a deadlock.
3. **Trunk-lane bugs** — the integrator + compile step are new serial code;
   kept tiny, fail-loud, and mutation-tested before trust (the vacuous-guard
   lesson). A red trunk lane halts claiming.
4. **Secrets/identity — forge mode only.** In local mode there are none:
   everything on the machine already shares one environment (the owner's
   observation is correct — a credential available to the trunk lane is
   available to every branch worktree, so per-lane secrecy was never real
   locally). The token-scoping and second-approver-identity concerns exist
   only when the forge backend is enabled, and are deferred with it.
5. **Semantic drift between spec body and frontmatter** — two parts of one
   file, but still two encodings; the existing completion-reconciler idea
   (Done-when vs status) re-lands here as "archive move requires all
   Done-when boxes ticked," which is now a *local* check on one file.
6. **Migration-window inconsistency** — between Phases 2 and 5 both loaders
   exist; the dogfood-sync suite pins them equal until the old one deletes.

## 9. Rulings (owner, 2026-07-28)

- **RULING-1 — RULED, agree.** Git is declared a required substrate in
  PROCESS.md.
- **RULING-2 — RULED, revised: local-first.** No tunneling through GitHub.
  The seam's default backend is the local serial integrator (§1.2); GitHub is
  the optional online backend of the *same* flow for repos that live on a
  forge. A PR was never mechanically more than a merge — its added value is
  server-side enforcement, which this repo does not currently need.
- **RULING-3 — RULED, strengthened.** Stdlib *preferred* for shipped checks,
  not absolute: a genuinely cleaner tool may be forced downstream — rare,
  ideally never — via the ledger's exceptional tier. Coordinator-side
  dependencies via the ordinary ledger tier, installed by dev-setup.
- **RULING-4 — RULED: no CSV at all.** Neither hand-edited nor generated;
  all traceability derives from the TOML frontmatter scans. Two encodings of
  the registry will not coexist.
- **RULING-5 — RULED, agreed.** SR-054 flips to `Verification=Test`; the
  `render` class survives only as a batching tag (§3.3).
- **RULING-6 — RULED.** Bookkeeping (claims, compile, regeneration) commits
  directly to the trunk; product changes reach the trunk only through the
  integrator's `--no-ff` merge; mechanized by the non-merge-product-commit
  check (§4). Note the push question dissolved with RULING-2: locally there
  is no push at all, only trunk commits by the two serial lanes.
- **RULING-7 — RULED: the config already exists.** `docs/gate-policy`,
  `docs/push-policy`, and the review-policy dial are the human-gate
  declarations; the integrator enforces them. No new mechanism; the
  bot-identity question is forge-mode-only and deferred.
- **RULING-8 — RULED: killed.** There is no separate serial fallback to
  maintain — the local integrator is the default backend, and
  `workers = 1` is the serial flow.
