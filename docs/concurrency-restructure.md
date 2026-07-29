# Concurrency restructure — design spec (DRAFT, owner rulings pending)

**Branch:** `ConcurrencyTrainRewrite`. **Status:** draft for owner review; nothing
here is implemented. **Goal (owner-stated):** the kit is parallel *out of the
box*, and a full restructure is acceptable. This spec replaces the bespoke
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

### 5.6 Pause — a station-boundary control (owner-raised, kept)

The old `docs/pause` had the right idea at the wrong moment: its one live
failure (2026-07-26) was being *expected* to stop a mid-flight worker, which
it structurally never could. The capability survives, redefined at the two
boundaries the serial lanes actually control — a traincar is affected only
**at the station**, never on the track:

- **`scope = "claims"`** — no new departures. In-flight traincars finish,
  integrate, and archive normally. This is the default pause, and the spine
  barrier (§3.2) is this same scope applied automatically during a drain —
  one mechanism, two users.
- **`scope = "integrate"`** — departures already out complete their build
  but **hold at the platform**: nothing merges to trunk until resumed.
  The inspect-before-anything-lands mode.

Form: a **tracked** file, `docs/work/pause` (TOML: `scope`, `reason`,
`since`), committed by the bookkeeping lane. Tracked fixes three defects of
the old file at once: it survives clones, the reason is diffable history
instead of a stale local note, and unpausing is an auditable commit. Both
serial lanes read it before acting, so enforcement sits exactly where the
control is real. What no file can ever do — stop a running session — stays
stated plainly: that remains "kill the worker." Status generation surfaces
`paused (scope) since <date>: <reason>` so an open pause is a visible
accruing cost, never a forgotten one (the stale-reason lesson).

## 6. What retires, what shrinks, what remains

| Artifact | Fate |
|---|---|
| `agent_dispatch.py` train/reservation/integration half (~4k lines) | **Retires** — forge + §2.3 replace it |
| `refs/llm/*`, `out/dispatch/events.jsonl`, `docs/run-state` | **Retire** — git history and spec location replace them |
| `docs/pause` (untracked, dispatcher-scope) | **Replaced** by tracked `docs/work/pause` with declared scope — §5.6 |
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
- **Phase 2 — specs as registry.** Converter generates one spec file per
  existing CSV row (mechanical; frontmatter from columns); loaders in
  `schedule.py` / `check_trajectory.py` / `gen_trajectory.py` switch to the
  folder; CSV becomes generated or is deleted. *The converter is proven by a
  byte-exact round-trip before the CSV is demoted* (the 140-cell lesson).
- **Phase 3 — shared-surface rules.** `log.d/` fragments + trunk compile;
  generated-artifacts-trunk-only; branch-scoped review names.
- **Phase 4 — the integrator.** Build the local integrator lane (the one-page
  serial merge queue) + the shrunken coordinator; wire the forge backend only
  if/when this repo goes online. First parallel batch of two `ordinary` WIs
  run end-to-end as the acceptance proof (the proof the mothball proposal
  wanted, now against the new machinery: **the trunk history must show the
  composed-tree check running on every merge, and zero hand-rescues**).
- **Phase 5 — deletion.** The train machinery, its tests, and the dead
  surfaces leave; the audit's other approved retirements execute here too.

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
