# The twelve requirement-owned `Provides` seams

*Owner decision surface, commissioned in session 2026-08-23 with the ruling on
`OI-60`: "You can fix the ones that are fixable now, but then can you generate a
report of what those SRs are? … including the definition of the SR and the
interfaces."*

---

## 1. What the issue actually is

It is **not** that these seams have no consumer. Every one of the twelve names a
real far side, and eight of them name a module in this tree. The gap is on the
**provider** side, and it is structural rather than an authoring mistake.

An interface row names exactly one `owner` — the row answerable for the seam —
and that owner is id-typed and polymorphic: it may be a **design** row (`LLR-###`)
or a **requirement** row (`SR-###`). A design row carries a `module` cell; **a
requirement row does not, and should not** — a requirement states an obligation,
not a location in the source tree.

The schema the registry is migrating toward drops the `this_project` column and
recovers the providing module by following `owner → LLR → module`. That works
perfectly for the 91 rows whose owner is a design row. On these twelve, the owner
is a requirement, so there is nothing to follow: **`this_project` is the only
record anywhere in the registry of which module provides the seam.** Delete the
column on those rows and the fact is gone — with it goes the module's producer
credit in the connectivity advisory and the source end of the declared seam pair
that tells the cross-component rule "this import edge is intended".

So the decision each row needs is small and specific: **is the truthful owner a
design row inside the providing module (in which case re-point it, and the
column becomes free), or is the requirement genuinely the right owner (in which
case the column has to survive for these rows, or the fact needs another home)?**

That is a judgement per seam, not a transform, which is why it is a report and
not a commit.

### What was fixed now, and what was not

**Fixed** (the two corrections the ruling folded in):

- **`IF-031`'s owner** moved from `LLR-014` (the module holding the *consuming*
  code, `check_perf.py`) to **`SR-015`** (the requirement stating the budgets
  registry's own invariant). It was the single row in the whole registry authored
  under the reading that was *not* ruled. The reason is written on the row.
- **The ruled reading itself** is now recorded in the header of
  [`interfaces.toml`](../requirements/interfaces.toml), where an author will meet
  it: on a `Consumes` row the owner is the **provider of the medium consumed**,
  and the consumer side carries **verified** readers.

**Not done — and this is a deviation from what the ruling expected to land
today.** The ruling's option (a) was "shed `direction` only". Measured over the
live registry before any cell was touched, that shed is **not lossless yet**:

| Population | Rows | Is `direction` recoverable without the column? |
|---|---|---|
| Design-owned | 91 | **Yes on 90** — `owner → module` matches the provider-side endpoint. The one exception was `IF-031`, now corrected. |
| Requirement-owned | 44 | **No, on all 44** — the same missing-module gap this report is about, applied to the other column. |

Dropping `direction` today would read all 44 of those rows as `Provides`,
silently reversing the 32 requirement-owned `Consumes` seams in all three places
that orient from the column (the connectivity advisory's producer/consumer
credit, the dashboard's seam arrows, the architecture map's dotted edges). The ruling's
premise — that the readers can take the fact from "owner-side versus
consumer-side" instead — becomes true only **after** option (a)'s *other* clause,
the rename of `counterpart` into a consumers list, which makes this side the
provider on every row. The two clauses are ordered, not parallel, so the shed was
held and the enabling half is named as the lane's next executable slice. Nothing
in the registry was normalized to make the column look shed-able.

---

## 2. The twelve rows

Every row below is `Drafted`. "Candidate design rows" counts the `LLR` rows whose
`module` cell resolves to the providing module — the pool a re-point would choose
its owner from, or decline in favour of the requirement.

---

### IF-001 — `scripts/trace` → `scripts/check`

**Contract.** `trace.py` CLI: `--strict-integrity` exits 1 on a duplicate/
malformed id or mis-columned row; `--strict` adds orphan + IF/PB back-link
findings; `--require-verified` adds the DevStg-Impl status check; writes
`docs/test/report.md`.

**Owner — `SR-157` (Approved).** *"The delivered harness shall report every
declared spine and work-registry rule violation — broken joins, integrity and
schema faults, leftover placeholders, requirement-form findings and work-item
coherence contradictions — naming the at-fault row and cell, gating the declared
failure set at the declared gate while advisory classes never change the exit
code."*
Rationale, in brief: it realizes SN-002 (the chain is mechanically verified, not
asserted) and is deliberately **one** row because the adopter-observable contract
is one — named findings at a declared severity; *which* rules at *which*
severities is component detail for the rows below it.

**Candidate design rows in `scripts/trace` — 10:** LLR-001, LLR-002, LLR-003,
LLR-005, LLR-015, LLR-041, LLR-083, LLR-183, LLR-187, LLR-194.

**What a re-point would decide.** Ten rows decompose slices of `trace.py`
(integrity, orphans, back-links, the frame joins) and none answers for the *CLI
contract as a whole*; the choice is to elect one as the module's face or to mint
a design row for the CLI surface — this is an internal seam, so SR ownership is
the weaker reading here.

---

### IF-005 — `scripts/check_privacy` → `scripts/check`

**Contract.** `check_privacy.py` CLI: `--repo` scans the tree and exits 1 on a
secret (always-on floor) or, under `docs/privacy-check`, a gated identity/PII
class.

**Owner — `SR-017` (Approved).** *"When a session attempts to commit or push
content matching a secret pattern, the system shall refuse at the hook floor —
scanning every commit's staged diff, message and outgoing range regardless of the
privacy toggle, and naming the finding — unless the declared `secrets_scan` dial
is explicitly false."*
Rationale, in brief: realizes SN-009 — a credential that reaches a shared branch
must be treated as disclosed, so the cheap moment to catch it is before the
commit. Folding the scan into the privacy toggle was rejected: that makes the
highest-severity check opt-in alongside a preference.

**Candidate design rows in `scripts/check_privacy` — 3:** LLR-017, LLR-018,
LLR-031.

**What a re-point would decide.** The smallest candidate pool of the twelve, and
the seam is internal — one of these three plausibly answers for the CLI outright,
which would make this the cheapest row to close.

---

### IF-009 — `scripts/check_trajectory` → `scripts/check`

**Contract.** `check_trajectory.py` CLI: exits 1 on a WI id/predecessor/cycle or
an R-A coherence violation (every run), R-B..R-E under `--strict`; connectivity
coverage is warn-only.

**Owner — `SR-157` (Approved).** Same requirement as IF-001 (text above).

**Candidate design rows in `scripts/check_trajectory` — 15:** LLR-034, LLR-042,
LLR-049, LLR-067, LLR-068, LLR-075, LLR-077, LLR-084, LLR-097, LLR-158, LLR-160,
LLR-172, LLR-178, LLR-183, LLR-202.

**What a re-point would decide.** The largest pool in the set, and the honest
reading may be that no single design row *should* answer for a 4,900-line checker
— which is itself a live question elsewhere (whether `check_trajectory` is still
one checker). A re-point here is entangled with that decomposition question, so
this row is the strongest candidate for "leave it at SR tier until the module is
split".

---

### IF-011 — `scripts/gen_trajectory` → `scripts/check`

**Contract.** `gen_trajectory.py` CLI: `--check` exits 1 when root
`PROJECT_STATE.html` is stale or missing (the git as-of line is excluded from the
byte compare).

**Owner — `SR-070` (Approved).** *"The delivered generator set shall derive each
artifact it produces from the tracked registries alone — self-contained and
usable without network access, byte-stable across regeneration from unchanged
sources, and carrying a freshness contract that fails when the committed copy has
drifted from those sources — omitting a view whose source registries the adopting
repository does not carry rather than emitting an empty one."*
Rationale, in brief: one decision per row — the *integrity* of a generated
artifact and what the state view must *show* are unrelated obligations that fail
independently, and this row holds the first alone.

**Candidate design rows in `scripts/gen_trajectory` — 15:** LLR-035, LLR-051,
LLR-055, LLR-079, LLR-080, LLR-099, LLR-103, LLR-107, LLR-108, LLR-111, LLR-112,
LLR-115, LLR-117, LLR-119, LLR-130.

**What a re-point would decide.** The contract here is the **freshness** contract
specifically, not the whole generator — so the choice is narrower than the pool
suggests: which design row owns `--check`'s byte compare, rather than which owns
the dashboard.

---

### IF-013 — `scripts/check` → `external:downstream adopter`

**Contract.** `check.py` CLI: `--gate DevStg-Reqs|DevStg-Tests|DevStg-Impl|all`
with `--tier`/`--coverage`/`--lenient` runs the active gate's steps as
subprocesses and exits nonzero on any required failure (never a silent pass).

**Owner — `SR-006` (Approved).** *"The delivered harness shall run the required
steps of the gate that must next be passed (the strictness selector cached in
`docs/stage`) and fail that gate when a required tool is missing, reporting
SKIP(missing) rather than silently passing — and, on a claimed work branch (one
whose history holds a `docs/work/active/<branch>/` claim), SKIP its
generated-artifact freshness steps with a stated trunk-lane reason, generated
artifacts being trunk-only, while every non-freshness step still runs."*
Rationale, in brief: realizes SN-004 (gates enforce their bar) and SN-008 (no
false green); the sanctioned SKIP is reported, never silent.

**Candidate design rows in `scripts/check` — 4:** LLR-006, LLR-007, LLR-008,
LLR-141.

**The `WI-495` dossier's read** ([exception
dossier](2026-08-22-interface-exception-dossier.md)): **KEEP `SR-006`** — the
contract's central claim restates SR-006's requirement text almost verbatim, and
`SR-007` governs a different observable. The dossier verified that **no `LLR` row
owns `scripts/check` outright** — every design row citing the module decomposes a
narrower slice — which is exactly why the row fell back to an SR owner. It states
its recommendation as provisional only under OI-60's option (b), which was not
ruled.

**What a re-point would decide.** This is an **adopter-facing** seam: the far
side is the downstream adopter, and what the adopter is promised is the
requirement, not a module's internals. SR ownership is arguably the *correct*
reading here rather than a fallback — in which case the decision is where the
providing module gets recorded, not who owns the row.

---

### IF-014 — `scripts/bootstrap` → `external:downstream adopter`

**Contract.** `bootstrap.py` CLI: `--dest DIR [--stack/--domain/--agents/--force]`
writes the mapped kit files so the scaffold harness runs green; idempotent
without `--force`; stamps `docs/kit-version`.

**Owner — `SR-010` (Approved).** *"The delivered scaffold generator shall produce
a scaffold whose harness runs green immediately after generation."*
Rationale, in full: realizes SN-001 (a working process without hand-building
tooling) and SN-007 (the suite bootstraps a real scaffold and exercises every
script).

**Candidate design rows in `scripts/bootstrap` — 5:** LLR-009, LLR-010, LLR-011,
LLR-121, LLR-156.

**What a re-point would decide.** Adopter-facing, like IF-013, and the SR is
unusually close to the contract (both say "the scaffold runs green"). The pool is
small enough that a design-tier owner is available if the owner prefers
uniformity over the external-facing argument.

---

### IF-015 — `scripts/agent_loop` → `external:downstream adopter`

**Contract.** `agent_loop.py` CLI: `--wi` runs one claimed worker assignment,
`--interactive` launches one attached session, `--dual-plan` runs one
decomposition round; a plain launch runs DRIVE mode — claim the next ready WI in
build order, run a worker session on the claimed branch's worktree, drain the
serial merge queue, repeat — re-deriving the frontier every cycle, resuming a
parked claim on relaunch, stopping loudly on any composed refusal, never pushing.

**Owner — `SR-026` (Approved).** *"The delivered coordinator shall resume
headless with stdin closed, never blocking on a prompt: a worker resumes from its
explicit claimed assignment plus the committed trailer evidence on its branch,
and the integrator derives claim and queue state from trunk history alone — the
generated status surface never a session input."*
Rationale, in brief: realizes SN-006; an unattended run blocked on a prompt is
indistinguishable from a hung one. Two obligations an acceptance cell had carried
without a `shall` were minted as their own rows (SR-171, SR-172) rather than
deleted.

**Candidate design rows in `scripts/agent_loop` — 11:** LLR-028, LLR-037,
LLR-045, LLR-048, LLR-061, LLR-082, LLR-095, LLR-096, LLR-132, LLR-174, LLR-175.

**What a re-point would decide.** The contract is much wider than the owning
requirement (SR-026 states headless resumption; the contract states the whole
launcher surface). Either the owner is a design row that answers for the CLI, or
the row's contract is really several seams — worth noticing before choosing.

---

### IF-044 — `scripts/agent_route` → `scripts/agent_loop`

**Contract.** `agent_route.py` module/CLI: `load_registry`/`load_enabled` +
`resolve_enabled` + `parse_env` + `select(pool,tier)` honoring per-pair cooldown,
the family-keyed reviewer heterogeneity preference and tier-up-never-down;
`escalate()`/`failure_action()` the fixed win-stay/lose-shift policy;
`planner_pair()`/`planner_fallback()` the dual-plan two-hat selection — pure
selection returning the reason as data, the coordinator owning launch.

**Owner — `SR-154` (Approved).** *"When unattended work reaches integration, the
delivered loop content shall obtain each review or critique verdict the declared
policy requires from a session that did not author the work — resolved per
in-process phase and tier from the delivered agent registry's declared
(family × model × tier) rows and only while the declared consent surface that
turns managed selection on is present, drawn from a different model family
wherever one is configured, degrading only to the documented same-family mode —
with every selection logged before launch and a non-converging rework loop
escalated through the declared approval level."*
Rationale, in brief: realizes SN-026 (cross-family second opinions) and SN-024
(an author cannot judge its own output); one row because routing, scheduling,
scoring and escalation are one delivered contract.

**Candidate design rows in `scripts/agent_route` — 3:** LLR-044, LLR-072,
LLR-081.

**The `WI-495` dossier's read**: **KEEP `SR-154`** (not `SR-155`) — five of the
module's seven named call surfaces serve SR-154's general routing capability, and
only the planner pair serves SR-155's contested-planning round. The dossier
records the same no-owning-`LLR` finding for `scripts/agent_route` as for
`scripts/check`.

**What a re-point would decide.** Internal seam, three candidates — the most
tractable design-tier re-point in the set, if one of the three can honestly answer
for the module's whole selection surface.

---

### IF-053 — `scripts/schedule` → `scripts/check_trajectory`

**Contract.** The ready-frontier + deterministic-order + safety-classification
library/CLI: `ready [--explain|--format json]` and `simulate --jobs N` over the WI
registry return the ordered frontier and reason-coded dispositions; pure and
side-effect-free (never mutates the registry, spawns a worker, or touches git).

**Owner — `SR-148` (Approved).** *"The delivered loop content shall select the
work an unattended run does next from the repository's tracked registries and git
history alone, in this order: ready adjudication rows first …; then unresolved
handback records; then the earliest incomplete spine tier in SN→SR→LLR→TC order;
then implementation work after test-case layout is complete — with the eligible
set and its order deterministic, an item whose declared safety, policy or
plan-mode inputs are missing, undeclared or contradictory failing closed for that
item alone, human holds applied only from the declared approval level, nothing
admitted past a human-held stop, no prose surface and no predefined track in the
derivation, no hand-curated next-work or run-phase pointer surface shipped …, and
the status surface a session reads generated and freshness-gated rather than
hand-copied."*
Rationale, in brief: without one precedence rule the same repository can resume
into implementation while returned obligations remain unresolved; the invariant is
stated here and nowhere else so no second row can drift from it.

**Candidate design rows in `scripts/schedule` — 7:** LLR-058, LLR-059, LLR-089,
LLR-095, LLR-123, LLR-131, LLR-152.

**What a re-point would decide.** The requirement and the module are unusually
well matched (one invariant, one module), so the question is only whether the
design tier says it better than the SR does.

---

### IF-065 — `scripts/agent_common` → `scripts/agent_loop`

**Contract.** `agent_common.py` module: the shared coordinator primitives split
out of `agent_loop` — typed exit codes + END_STATES; git/head_sha wrappers; the
declared-surface reads + stop banner; the per-worktree kernel advisory lock;
worker-assignment primitives; `parse_map`; preflight; the session-log family and
the generated run-state write. `agent_loop` re-exports the historical names, so
its public surface is unchanged.

**Owner — `SR-026` (Approved).** Same requirement as IF-015 (text above).

**Candidate design rows in `scripts/agent_common` — 7:** LLR-027, LLR-029,
LLR-030, LLR-138, LLR-155, LLR-177, LLR-196.

**What a re-point would decide.** This row documents an **extraction**, not a
capability — its contract is "these primitives now live here". A design-tier owner
fits that better than a requirement does; the SR ownership looks like inheritance
from `agent_loop` rather than a considered pick.

---

### IF-076 — `scripts/trace_text` → `scripts/trace`

**Contract.** `trace_text.py` module: the spine-row TEXT layer split out of
`trace.py` — four pure predicates (rows in, findings out, no I/O) plus the row
primitives they share. `provenance_findings` and `form_findings` return gating
findings that join trace's `--strict` exit code; `ac_advisories` and
`paraphrase_advisories` return warn-only advisories. Finding **strings** are part
of the contract: three golden files assert them byte-for-byte, which is what makes
the split provably behaviour-preserving.

**Owner — `SR-157` (Approved).** Same requirement as IF-001 and IF-009.

**Candidate design rows in `scripts/trace_text` — 5:** LLR-004, LLR-133, LLR-134,
LLR-135, LLR-179.

**Also on this row.** It carries the `source` honesty valve — `trace_text`
consumes nothing by design (pure predicate layer), which is what makes the
provider-side fact the *only* endpoint fact this row has. It is therefore the row
where losing `this_project` costs the most.

**What a re-point would decide.** Like IF-065, an extraction record; five
candidates sit in the module, so a design-tier owner is available.

---

### IF-081 — `scripts/trunk_step` → `external:downstream adopter`

**Contract.** `trunk_step.py` CLI (the serial trunk lane's shared-surface steps):
`--compile-log` validates and appends `docs/log.d/` fragments to `docs/log.md` in
git add-time order (all-or-nothing, links rebased, fragments deleted); `--regen`
re-derives the generated document families in `REGEN_STEPS` order. Fail-loud: a
red trunk lane halts claiming.

**Owner — `SR-170` (Approved).** *"The delivered loop content shall write the
shared records it derives — the compiled activity log and the generated
project-state artifacts — only from the serial merge step and only against the
merged tree, never from a parallel work branch."*
Rationale, in brief: one decision per row — this row holds the **exclusive-writer**
contract alone (ordering and all-or-nothing is SR-173's, identity allocation
SR-174's), realizing SN-027's serialization guarantee where a parallel writer
would actually corrupt something.

**Candidate design rows in `scripts/trunk_step` — 4:** LLR-060, LLR-124, LLR-137,
LLR-142.

**What a re-point would decide.** Adopter-facing, and the requirement states a
*policy* (only the serial step writes) that no single module owns — so this is
the fourth row where SR ownership may be the truthful reading rather than a
fallback.

---

## 3. What the twelve add up to

**Four are adopter-facing** — `IF-013`, `IF-014`, `IF-015`, `IF-081`, whose far
side is `external:downstream adopter`. For these, what crosses the seam is a
*promise to an adopter*, and a requirement is the right thing to hold a promise.
Re-pointing them to a design row would arguably make the registry **less**
truthful, so the likely answer for this group is: keep the SR owner and keep a
provider-side endpoint cell (or find the fact another mechanical home).

**Eight are internal** — `IF-001`, `IF-005`, `IF-009`, `IF-011`, `IF-044`,
`IF-053`, `IF-065`, `IF-076`. For these, the SR owner is a *fallback* the schema
itself calls temporary ("prefer the design tier wherever a design row exists").
Three of them (`IF-005`, `IF-044`, `IF-076`) have small candidate pools and read
as ordinary re-points. Two (`IF-065` and `IF-076` — the latter in both groups)
record module **extractions**, where a design-tier owner is the natural fit,
because what such a row states is "these parts now live here", a design fact
rather than an obligation. Two (`IF-009`, `IF-011`) sit on
large modules whose own decomposition is an open question, and re-pointing them
before that question settles would just move the problem.

**Two carry a prior recommendation.** `IF-013` and `IF-044` were adjudicated in
the `WI-495` exception dossier, which recommended keeping both SR owners on the
merits *and* verified that no design row owns either module outright. That
dossier's picks stand under the ruling taken here; they would only be superseded
by a decision to re-point the twelve.

**And there is a second population, named here so it is not discovered later.**
The same missing-module gap sits on **32 requirement-owned `Consumes` rows**. They
are not in this report because their consumer side is intact and the shed does not
threaten them the same way — but when the `counterpart` column becomes a consumers
list, those 32 rows will need the same provider-side judgement these twelve need.
Whatever principle the owner sets for these twelve should be the one that answers
those thirty-two.
