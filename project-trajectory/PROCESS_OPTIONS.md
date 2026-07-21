# Process Options — the opt-in layers

Companion to [`process.md`](process.md), which carries the load-bearing **core**
every project reads. This file expands the **opt-in layers** that doc summarizes,
each with an **applies-when** so a small project can tell at a glance whether it
needs the layer at all. Nothing here is required for the minimum profile (a
standalone one-module project — see the core doc's header); skip any section whose
applies-when doesn't match your scope.

Section headings mirror the core-doc sections that point here.

## Applies-when index

Scan this table once, then read only the sections whose trigger matches your
scope — **skip a layer if its "applies when" doesn't fit** (nothing here is
required for the minimum profile). Rows are in document order; each maps to the
`##` section of the same name below.

| Layer | Applies when — skip the section if not | What it adds |
|---|---|---|
| Proportionality doctrine | **always** — the mindset that frames how hard every layer below is applied | nothing (tells you when *not* to reach for machinery) |
| Derived gate model | **always**, once you use gates — the default: the gate is computed from artifact states, not declared | `docs/gate` (generated) + `derive_gate.py` |
| Phased delivery | a roadmap ships phase 1 before 2/3 (a single-shot deliverable skips it) | a `Phase` on every ratified SR/LLR/TC + a derived current phase + a per-phase gate |
| Lifecycle phase | install/startup/steady-state requirements are easy to miss (most non-trivial products) | lifecycle tags on SRs |
| Gate authority levels | a repo declares a non-default `docs/gate-policy` | `docs/gate-policy` + an attestation / deviation register |
| Agent iteration branch & sync | you want agent-driven work to land as curated, reviewable history | a branch + sync cadence, wired into hooks |
| Unattended operation | a coordinator grinds work from one entry point while nobody watches | `agent_loop.py`, `docs/run-*`, `agents.csv`, the launchers |
| Critique verification & the critique loop | a requirement's acceptance is **subjective** | a critique round + `Attest`/critique TCs |
| Dual-plan decomposition | a goal is design-shaping enough that one planner's WI decomposition should not go unchallenged | two rival plans + a coverage diff + one critique round + an arbiter verdict (`docs/plans/`) |
| Tier-conditional guardrails | an unattended run maps different model tiers to different phases | `docs/guardrails-policy` |
| Enforcement audit | your process outgrew one reader's head and you want to know which rules actually bind | `docs/enforcement-audit.md` |
| §7 boundary notes | onboarding contributors, wiring a workstation, or a contested tooling boundary | prose (setup-script + boundary calls) |
| Skills layer | an AI agent works the repo and you want it to load reusable skills | `skills/` + a per-agent fan-out |
| Trajectory / work-items layer | you want to track **how** work executes — cross-track order, %-complete | `work-items.csv` + `PROJECT_STATE.html` + `gen_trajectory.py` |
| Commit identity & privacy | you must keep a real, contactable identity out of published commits | `docs/privacy-check` + commit-identity config |
| §8 purchased parts | the product incorporates purchased/external parts it buys rather than builds | a parts registry (`PB`/`PART`) |
| Binary assets | the project ships unavoidably-binary deliverables (art, audio, video) | an assets registry (provenance / license / hash) |
| Intra-repo interfaces & the architecture graph | more than one module, and you want the arch view to show how they connect | an `IF-###` seam registry + the `architecture.md` graph |
| Component layer | you want a durable home for set-grained knowledge & lifecycle (a subsystem, an assembly) | a `CMP` component registry |
| Research track & knowledge packs | findings must outlive their research session, or a spec rests on a load-bearing unknown | `WI` research rows + `docs/knowledge/` packs |
| §9 NFR checklist | deciding which non-functional concerns a project must consider at G1 | an NFR checklist |
| §9 perf comparator | you have captured `PB-###` budgets you want tracked over time | a perf comparator over `PB` rows |
| §10 several modules, one repo | a repo grows distinct sub-systems that still build and release as one (scale rung 2) | a module map |
| Parallel tracks (multi-lane operation) | one repo runs many WIs concurrently — the dispatcher/worker model (the track-lane machinery is retired, WI-210) | worker assignments + the integration ref |

**Byte budget.** This file is **byte-watched** the way [`process.md`](process.md)
is: its baseline lives in the `byte-budget-guard` skill, and any growth must be
**flagged** with a byte delta + reason in the session/WI log — so the opt-in
surface can't bloat silently the way the core is protected from. The **split**
of the two spec-sized layers (Unattended operation, Trajectory) into their own
reference docs is **deferred** until the file's size actually forces it.

---

## Proportionality doctrine

*Referenced from PROCESS.md header ("Proportionality") and §3 "Right-sizing".*
**Applies always** — this is the philosophy that frames how hard every other
layer is applied; it is opt-in only in the sense that it tells you when to *not*
reach for machinery.

The core is the process's own guardrail against turning a sustainability tool
into a straitjacket. Four points, one voice:

- **(a) The tracked-artifact ideal, not an entry gate.** The whole method is
  built to perform change management and transparency **where possible**: a
  text-representable, line-diffable, mechanically-checkable artifact is the
  **ideal** it reaches for. But some work genuinely can't produce one, and that
  is not a disqualification. When the artifact itself can't be diffed, **track
  *about* it in text** — provenance, license, version, a content hash (§8
  "Binary assets") — so the *record* is change-tracked even when the *asset*
  isn't. The ideal is a direction, not an admission ticket.
- **(b) Attestation is the honest floor — and honestly trust-based.** Where
  verification cannot be mechanized, the floor is a **recorded human
  attestation**: a named person's recorded judgment that the acceptance
  criterion is met (a playtest, a creative review, a physical action). Be honest
  about what this is: **the box can be checked without the work having
  happened.** Attestation is trust; a mechanized check is proof. The process does
  **not** pretend they are equivalent — its job is to make the attestation
  **explicit** (a real verification kind, not a silent "Verified"), **named** (who
  attested), and **auditable** (when, against which criterion), so a reader can
  always see how much of the project rests on trust. That is the `Attest`
  verification kind (§4) and the "attested vs mechanized" split in the trace
  report.
- **(c) Over-aggressive traceability is a failure mode.** Traceability founds
  sustainability — *and* pushed past what a scope earns, it becomes an overly
  complex, overly constrained process that bogs development down. The balance is
  the whole game. **Right-sizing the traceability is the process working, not a
  compromise of it.** A gate that demands fine-grained decomposition of work no
  script can verify isn't more rigorous; it is theater that trades real velocity
  for the *appearance* of control. Reach for the lightest structure that keeps
  key items from being missed or silently broken.
- **(d) For creative/subjective domains, fly high.** Story, music, artwork,
  voice acting, level design — mostly binary, mostly subjectively verified. Here
  the `SN→SR→LLR→TC` spine's value is at **high altitude**: use `SN→SR` to
  ensure nothing key is **missed or silently broken** as development moves
  forward (the through-line of a story, the mood targets of a soundtrack, the
  cast a script needs). **Descend to LLR/TC granularity only where a mechanized
  check earns its keep** — a save-file schema, an audio-loudness bound, a
  build-size budget — and stop there. Decomposing a subjective judgment ("is this
  scene moving?") into finer rows a script still can't check adds process weight
  with no verification return; mark it `Attest` and move on.
- **(e) Decision-surfacing rate is a setup dial, not a constant.** How often the
  driver pauses for the human to **ratify a decision** is project-specific:
  calibrate it **at project setup** on the same risk axis as review-depth triage
  (PROCESS.md §6) and record the setting in `AGENTS.md` (Project section). In
  specialized or high-consequence domains — where safety is a risk even an
  *ancillary* one, money, privacy, anything irreversible — surface decisions
  **often**: bring even medium calls to the human to ratify. In low-risk domains
  (creative content is the archetype), where a wrong call is cheap to revert and
  carries little tech debt, a **confident** agent may decide **autonomously** —
  and the non-negotiable price of that autonomy is that every autonomous
  decision is **recorded** (an *Assumptions* / Open-items entry in `status.md`,
  moved to `log.md`'s *Decisions log* once ratified — the call, the alternatives
  passed over, why; PROCESS.md §5) so it stays visible,
  auditable, and cheaply revertible. The dial moves *how often you ask*, never
  the fixed points: gates still close only per the declared gate authority
  (§4), and a requirement
  **contradiction** still routes as a finding to its owner — an unrecorded
  autonomous decision is a *silent* one, which no dial setting permits.

## Derived gate model

*Referenced from PROCESS.md §4/§7.* The gate is **computed from the artifact
states, not declared** — SSOT applied to the gate itself. This section is the
working summary; the kit's full design + rationale is its own ratified design
spec (`docs/specs/derived-gate-model.md` in the kit's meta-repo — not shipped
downstream).

**The gate is derived.** `docs/gate` is a **generated** file:
`scripts/derive_gate.py` computes the active gate from the spine and caches it (a
`# basis:` derivation + a compute date, then the value on the first non-comment
line, so `check.py`'s `resolve_gate()` reads it unchanged). **The repo is at gate
G iff every in-scope SN/SR/LLR/TC meets G's bar.** You never hand-edit the line;
you ratify artifacts and regenerate (`python scripts/derive_gate.py`). The
`derived-gate` step (`derive_gate.py --check`, a pre-commit floor + every gate)
guards the cache against rot — a ratification that moved the states but not the
cache fails loudly. **Hybrid:** the cache means the gate is known on checkout with
no recompute; a legacy hand-set `docs/gate` with no `# basis:` line is accepted
**value-only** until a one-time `derive_gate.py` migration (so an adopter upgrades
without a red day).

**Artifact states (no new column).** Maturity is read from existing structure,
gated by one `Draft` bit:

- **SR / LLR / TC** — the open-vocab `Status` gains a leading **`Draft`**:
  `Draft` → `Planned`/… → `Verified`. Per-artifact gate: an SR is **G0** while
  `Draft`, **G1** once ratified (Status past `Draft`), **G2** once decomposed (its
  LLR — unless the Verification is LLR-exempt Analysis/Inspection/Attest — plus a
  TC), **G3** once `Verified`. An LLR/TC caps only when `Draft`; once present its
  own Status doesn't gate G3 — the SR's `Verified` drives that, matching
  `trace.py --require-verified` (which checks SRs, not LLR/TC status), so a repo
  whose LLRs read `Implemented` still reaches G3.
- **SN** — maturity is **section-as-state**: an SN under a stakeholder-needs.md
  heading whose text contains **"draft"** (`## Draft needs (unratified)`) is Draft
  (G0); SNs under any other heading are ratified (G1). No new column — the section
  *is* the state.

The **ratification date is git-derived** — the commit that moved the `Status` (or
the SN section). No new field.

**Draft artifacts live in the live spine.** A `Draft` SR/LLR/TC and a Draft SN are
**exempt from the child-completeness orphan rules** (`trace.py`): a Draft SR needs
no LLR/TC, a Draft LLR no TC, a Draft SN no SR — so a requirement is **drafted in
the live registry before it is decomposed**. This **retires the `-000` /
off-spine workaround** for requirement-first work. Parent-linkage + integrity
still apply (a Draft SR still links an SN; ids stay unique/well-formed), and a
Draft SR is skipped by the G3 Verified criterion (it is pre-ratification).

**Ratification = a reviewed Status-change commit.** Closing a gate is no longer a
marker bump: the acceptor **marks a batch of artifacts ratified** (`Draft`→
`Planned`, or an SN section move) **in a reviewed commit** — that commit *is* the
sign-off, and the gate derives from it (`gate-advance` skill). It composes with
the gate-authority levels (below): `attended` ratifies each batch; `single-ratify`
ratifies the batch once at its `[phase]-[g2]` close (one review per phase gate);
`autonomous` on a fresh-context reviewer's recorded verdict. An agent may make the
ratifying commit, governed by the level.

**Phase = a derived detector + a committed anchor.** The derived gate **dropping
below a phase's last-closed level** — new or reopened content entered — is the
*signal* that a new phase is due; `check_trajectory` warns "open a `[phase]-[g*]`"
(warn-first). But phase **identity + membership** live in a committed
**`[phase]-[g*]` work item** — a WI whose Title carries the `[<phase>]-[g<N>]` tag
— not a git-history walk (which a rebase/squash moves and which carries no
membership). `[phase]-[g1]` is the requirement-structuring batch; `[phase]-[g2]`
the decomposition + TC batch; its predecessor is the prior phase's close.

**Parallel for pre-dev, series for dev.** A phase's requirement work is a **batch,
in parallel** — draft + ratify all the new/reopened SN/SR together, which is
exactly where "this also modifies SR-12" and other conflicts surface in one review
— then each work item runs **G2 → G3 in series** (the per-WI vertical slice):

```
Phase N:  [phase-N-g1]  draft+ratify ALL new/reopened SN/SR   (parallel, batch review)
              │
          [phase-N-g2]  decompose to LLR/TC, all Planned      (parallel, batch review)
              │
          WI-a ─ G2→G3 ─┐
          WI-b ─ G2→G3 ─┤  (series, per-WI vertical slices)
          WI-c ─ G2→G3 ─┘
```

A reopen during a later phase's g1 revs the phase: the affected verified artifact
returns to `Draft`/`Planned`, the derived gate for that phase drops, and the batch
review sees it alongside the new work. (One sanctioned relaxation of the series
rule: a run of *independent, off-spine* dev slices may batch into one BUILD
session + one review round — "Dev-slice batching" under Unattended operation;
spine-touching slices always stay per-slice.) Within a phase the derived gate only rises
(draft → ratify → decompose → verify), so a **drop from a closed level is an
unambiguous boundary** — the detection is robust; the committed anchor just makes
membership legible and durable.

## Phased delivery

*Referenced from PROCESS.md §4.* **Applies when** a roadmap ships phase 1 before
2/3; a single-shot deliverable skips it. Builds on the **Derived gate model**
above: just as the gate is computed from artifact states, the project's **current
phase is derived** — the highest phase any ratified spine row carries — so a scope
change (a new ratified SN/SR/LLR/TC) surfaces as a phase bump, never a hand-set marker.

A roadmap that ships phase 1 before 2/3 needs gates that close *per phase* without
dishonesty. **Every ratified SR/LLR/TC carries the `Phase` it was ratified in** — a
bare integer (`1`, `2`, `3`…); an SN's phase is *derived* as the minimum phase of its
referencing SRs (no `stakeholder-needs.md` schema change). `Phase` is a free-form
string: bare integers are the recommended convention, but a downstream repo that kept
`vN` labels still works everywhere — the `--phase` filter matches literally, while the
derived-max and the completeness rule **digit-parse** (`v2` → 2, `2` → 2, the same
parse `derive_gate` uses), so a `vN` registry arms the rule and passes it. Semantics:

- **A blank `Phase` is legal only on a pre-ratification (`Draft`) row.** A ratified
  SR/LLR/TC (Planned/Verified) — and transitively a ratified SN — must carry a Phase
  that digit-parses to a number, or `trace.py --strict-schema` reports a schema
  finding. The rule is **vacuous until ≥1 artifact is phased** (the same arming idiom
  the component checks use), so a fully-blank downstream registry stays green: the
  rule is unarmed and the `--phase` filter treats blank as always-in-scope — exactly
  what "blank = every phase" bought before the phase model.
- **Traceability is phase-blind.** Every SR keeps its LLR + TC rows from G2 on,
  whatever its phase — decomposition is cheap and pins the design. An LLR's Phase is
  its parent SR's; a TC's is the max over what it verifies.
- **The G3 Verified criterion is phase-scoped.** `check.py --gate G3 --phase 1`
  (cumulative for later closures: `--phase 1,2`) requires Verified only for
  in-scope SRs; out-of-scope SRs are listed in the trace report as
  **phase-deferred** — an explicit, recorded exemption, never a silent skip. **The
  foundation (minimum) phase is always in scope** — never phase-deferred — so
  foundation requirements ride every delivery filter (what blank bought before).
- **G-Release is phase-scoped the same way:** `gen_release_checklist.py --phase 1`
  includes only in-scope human items and the release-tier/manual TCs verifying
  them, plus the always-in-scope foundation.
- Later phases re-enter at G1/G2 as requirement increments and close their own
  G3/G-Release with the grown phase list.
- **A project already at G3 that takes on new scope: the derived gate handles it.**
  New scope enters as **`Draft` SN/SR in the live spine** — the `-000` / off-spine
  placeholder workaround is **retired** by the derived gate model above. The new
  drafts sit at G0, so the derived **per-phase** gate for the new phase drops (the
  `[phase]-[g*]` signal) while the shipped phase stays at its level; the shipped
  set still closes at G3 with `check.py --gate G3 --phase <shipped>` (per-phase
  scoping, not a marker rewind — rewinding would discard the closed phase's
  attestation). Traceability is phase-blind, so a new-phase SR still reaches
  **G2-completeness (LLR + TC)** before it is *Verified* — but it no longer waits
  off-spine to be *drafted*: it is a live `Draft` row from the start (its Phase may
  stay blank while `Draft` and takes its number at ratification). Only *Verified*
  and *G-Release* defer by phase; the new phase's SRs read phase-deferred until
  their own G3.

## Lifecycle phase

*Referenced from PROCESS.md §4.* **Applies when** install/startup/steady-state
requirements are easy to miss — i.e. most non-trivial products; a pure library
with no runtime lifecycle can leave the tag blank.

Distinct from the delivery `Phase` (which is *when we ship it* — v1/v2), a
requirement also has a **lifecycle phase**: *at what point in the running
product's lifetime must this hold, and how often?* Naming it stops the perennial
miss of writing only steady-state requirements and discovering the install/setup
ones late. Capture it as an **optional `Lifecycle` tag** on an SN/SR (a column or
inline tag, mirroring `Area`; blank = unspecified, treat as **Runtime**) — use the
distinct name `Lifecycle`, never overload the delivery `Phase` column. The default
vocabulary is an **open, project-named set** (extend it per scope like `Area`; it
is **not** a fixed enum):

- **Provision** (ready) — must hold *before the process can run at all*: install,
  dependencies/runtime present, infra provisioned.
- **Startup** (set) — established *once per launch, before it serves*: load +
  validate config, run migrations, open the initial pool, allocate fixed
  resources, readiness probe.
- **Runtime** (go) — steady-state serving, *including recurring acquisition*:
  handle requests, reconnect on drop, per-request alloc, dynamic config reload.

Optional **Shutdown**/**Teardown**, **Upgrade**/**Rollback**, **Recovery** extend
the set when the scope needs them.

- **Discriminate by *when / how often*, not by the word "setup"** — almost
  everything readies *something*. Opening the connection pool *at boot* is Startup;
  reconnecting *mid-operation* is Runtime; a fixed buffer at launch is Startup,
  per-request alloc is Runtime. **One capability legitimately spans phases** — that
  is the payoff: a DB feature yields *provision the DB* (Provision) → *open the
  pool + migrate at boot* (Startup) → *reconnect on drop* (Runtime), and people
  usually write only the Runtime one.
- **Configuration straddles Provision↔Startup, app-dependently.** Config is
  **Provision** when it *must pre-exist* and the app has no way to obtain it at
  launch; it is **Startup** when the app *can* obtain/validate it at launch (a
  first-run wizard, a clear error, or a default fallback). Capture both the
  *definition* (where the config lives) and the *launch behavior when it is
  missing*.
- **Keep one axis.** Dependencies and config are *subjects*, not phases — a
  dependency is required at Provision but used at Runtime; config must exist at
  Provision, is loaded at Startup, may reload at Runtime. The `Lifecycle` tag on
  the concrete requirement already places it; don't add a second "kind" axis.

## Gate authority levels

*Referenced from PROCESS.md §4.* **Applies when** a repo declares a
non-default `docs/gate-policy` — i.e. wants gates accepted by something other
than a per-gate human pause. The default **`attended`** level needs none of
this section — it is exactly the §4/§5 flow. Generalized
from a field adoption's ratified deviation register (the NotHomeWrecker
prototype), which remains this layer's worked reference.

**Selection.** The level is chosen **before the kit is ported** — by the
owner, with an agent recommendation from the project brief
(`bootstrap.py --gate-policy`, or interactively at scaffold time;
KICKOFF_PROMPT.md carries the recommendation step). Calibrate on the §6
risk axis: safety, money, privacy, or irreversibility ⇒ `attended`; low-risk
creative/tooling scopes are `autonomous`-eligible. Changing the level later is
a reviewed commit that edits `docs/gate-policy` and the register below.

**The deviation register (`docs/gate-policy.md`).** The kit-owned process doc
is never edited per-repo (it is overwritten on re-sync); a non-default level
lives in a repo-local register that *amends* it: a table of `process.md`
clause → standard behavior → this repo's behavior, ratified by the owner,
with the fixed points at the bottom that nothing overrides. Where the two
disagree, the register wins — except the fixed points. `bootstrap.py`
scaffolds the skeleton pre-filled for the chosen level.

**Machine surface: none beyond the two files.** `check.py`/`trace.py` behave
identically at every level — authority is *who accepts*, not what runs. The
harness is the bar everywhere; a red check is a red check.

### The three levels

- **`attended`** *(default)* — a human approves each gate (G1/G2/G3/G-Release)
  and G-Final. The standard §4/§5 flow; nothing else in this section applies.
- **`single-ratify`** — the driver advances through G1+G2 with LLM-gate review
  (below), **queuing every human call** instead of pausing: each becomes a
  `Needs <human>` Open-items bullet in `status.md` plus, where the driver had
  to proceed, a provisional decision. At the **ratification point — fixed at
  G2 close** — the human reviews the accumulated list + gate evidence in one
  sitting and ratifies or amends (ratified decisions move to `log.md`'s
  Decisions log, §5); G3→G-Release then run under `autonomous` rules. G-Final
  stays human. *Why G2 close:* every requirement/design ambiguity is resolved
  exactly once, over cheap artifacts (registries and docs, not code), before
  the expensive autonomous implementation stretch. An adopting repo *may*
  relocate the ratification point by amending its own register — the kit does
  not parameterize it. **Post-ratification questions route by revert-cost**,
  never a mid-run pause (the ratifier accepted bounded risk; momentum is the
  level's value): LOW → decide + record in the Decisions log; MEDIUM/HIGH →
  the Blocked register.
- **`autonomous`** — every gate except G-Final closes on the LLM-gate verdict;
  mid-run human escalation is replaced by the Blocked register, ask-the-human
  by the Decisions log (HIGH revert-cost decisions get an independent
  peer-tier second opinion *before* execution), human `Attest` by LLM-Attest.
  The **gate-closure** reviewer tier is the strong-model floor (§6 tiering) and
  is never delegated down. (This floor governs a **gate advance** only. The
  cheaper *iteration-loop* reviewers the coordinator schedules between builds
  are deliberately cheap-but-heterogeneous — see "Unattended operation" ->
  the routing/escalation subsection; a weak-but-different-family review is a
  useful uncorrelated draw, where a weak *gate* verdict is not.)

### The LLM-gate verdict protocol

A gate closes only on the verdict of an **independent LLM reviewer**:

- **Fresh context** — a separately spawned agent that did *not* drive the work
  it reviews; it gets the gate's §4 criteria, the §6 adversarial framing (hunt
  for defects, stubs, spec drift, untested claims — never rubber-stamp), and
  pointers to the artifacts, and re-derives its own view.
- **Runs the harness itself** — the reviewer executes `check.py`/`trace.py`
  and quotes real output; a verdict citing a run it didn't perform is invalid.
- **Verdict recorded** in `log.md` per §5, extended with `Model: <model id>`
  and `Role: LLM-GATE`; the Gate Sign-offs acceptor column reads `LLM-GATE`.
  APPROVE → the driver makes the **ratifying Status-change commit** (and
  regenerates `docs/gate` via `derive_gate.py`), citing the verdict block (the
  verdict is the review of record — this is the `autonomous` ratification the
  "Derived gate model" describes). CHANGES-REQUESTED → findings route to their
  owner hats; re-review up to `MAX_ROUNDS`, then the Blocked register.

### The Blocked register (replaces mid-run escalation)

When a finding survives `MAX_ROUNDS`, a call is MEDIUM/HIGH revert-cost after
ratification, or a step is impossible without the owner (a purchase, an
account, a physical action): record it under **Blocked** in `status.md` —
what, why, rounds spent, the driver's best-judgment recommendation — and
**continue with independent work**. Every Blocked item surfaces prominently
in the end-of-run report; a block that gates the deliverable itself downgrades
it honestly (partial + explanation), never silently.

### The Decisions log (replaces ask-the-human)

Where the process says *ask / pause / solicit clarification*, an autonomous
driver decides and appends to the `log.md` Decisions log (§5): what was
chosen, why, the alternatives, `Revert cost: LOW|MEDIUM|HIGH`, `Model:`. A
decision is never a license to expand scope — one that would contradict a
ratified owner decision is a Blocked item, not a new decision.

### LLM-Attest (replaces human Attest at `autonomous`)

For subjective judgments that must not fake being tests: the TC records
`Attest` with **which model** attested, when, and the one-line judgment —
reported in the attested-vs-mechanized split as *machine* attestation, never
disguised as `Test`. G-Final is where the owner's eyes replace these.

## Agent iteration branch & sync

*Referenced from PROCESS.md §3 ("Commit cadence") and §7 ("Push authority").*
**Applies when** a repo wants agent-driven work to land as curated, reviewable
history — and, on a privacy-checked repo (`docs/privacy-check` = `true`),
wants privacy to be **structural** rather than filtered at publish time.
This is the heaviest ritual in the kit: opt in deliberately. A repo without
agent-driven work skips the whole layer and pays nothing. (The
`docs/push-policy` file below ships in every scaffold regardless — declared
push authority is useful even without the branch discipline.)

**The model.** The agent never commits to the development branch. All agent
work happens on an **iteration branch — `llm/{branch}`** (slash namespacing
groups every agent branch under one prefix in git tooling): the pre-commit
floor runs there per commit, cheap and unchanged, and the §3 commit-often
cadence lives there, where granularity is free. What lands on the development
branch is scrubbed and curated **by construction** — the branch a human pushes
never contained the leak or the noise. Hooks cannot carry this guarantee
(they are per-clone and tool-circumventable: a user pushing with a different
tool may never hit them); the branch structure can.

**Sync points.** A sync runs when the work reaches an end state: everything
remaining is Blocked (the Blocked register, "Gate authority levels" above), a
gate closes, or the project's scope is complete. Five steps:

1. **Backup.** Snapshot the iteration history first — a dated backup ref,
   e.g. tag `backup/llm-<branch>-<YYYYMMDD>` — so a failed reintegration can
   never lose work. Retire it once the sync lands.
2. **Scrub** *(privacy-checked repos only — `docs/privacy-check` = `true`).*
   A separate fresh-context agent walks every commit since divergence —
   diffs, **commit messages**, and any committed session/iteration logs —
   removing or anonymizing PII via history rewrite, with the deterministic
   privacy lint (`scripts/check_privacy.py --range`, "Commit identity &
   privacy" below) as its base pass over the leg's history. The rewrite stamps a **`Scrubbed:`**
   trailer on each rewritten commit so later checks can tell scrubbed history
   from raw. Rewriting is confined to the iteration branch *before* landing —
   never the development branch; step 1 is the net. When the scrub agent
   **can't run** at a sync point, the sync **fails closed**: it waits, and
   nothing lands unscrubbed — a missing tool is never a pass at the one
   boundary that matters.
3. **Optional push of the iteration branch** — only if `docs/push-policy`
   allows agent pushes; preserves the granular (scrubbed) history remotely
   for backup and forensics.
4. **Collate.** A separate agent reorganizes the leg's commits into
   **categorical commits** — Conventional-Commit style with optional scope
   (`feat(addon):` / `fix(biome):` / `perf(noise):` / `docs:` / `build:`) —
   each a coherent, reviewable, why-and-impact-shaped change. Many tiny green
   commits in; few subject-shaped commits out. **The type list is a default
   vocabulary, never a restriction:** a project renames or extends the types
   to fit its domain, and nothing lints the exact set.
5. **Land.** The collated commits go onto the development branch as a
   rebase/cherry-pick — dev history stays linear, no merge bubbles; a
   conflict during landing is a **Blocked item**, never a silent
   force-through. After landing, the iteration branch resets onto the new dev
   head for the next leg. The human pushes at their leisure (the default
   policy) — or the agent does, iff the policy says so. **Landing is not a
   stopping point:** under an autonomous gate authority the loop syncs and
   rolls straight into the next leg — unpushed landed legs accumulate, and
   the human may push several at once; the run pauses only when intervention
   is *required*, never merely because a sync happened.

**Push authority is a declared policy — `docs/push-policy`** (one word,
tracked like `docs/gate`; scaffolded `human` in every repo):

- **`human`** *(default)* — the agent **never pushes, even if asked
  mid-session**; it prepares the branch and requests the push. Publication is
  a deliberate human act, immune to hook/tool circumvention by construction;
  the human is a cheap bottleneck, because pushing is rare and takes seconds.
- **`agent-iteration`** — the agent may push only the *scrubbed iteration
  branch* (remote backup + visibility); the development branch stays
  human-pushed.
- **`agent`** — full delegation: the agent may push the development branch
  after a landed sync, still gated by the sync ritual.

The policy is a **process rule** honored by agent drivers and any unattended
coordinator — hooks can only *assist* per-clone, which is exactly why the
authority is structural, not hook-based. Change the value in a reviewed
commit, like `docs/gate`.

**Why this beats a push-time filter (recorded).** (1) A structural model
cannot be circumvented by pushing with a different tool — the branch the user
pushes never contained the leak. (2) It solves add-then-strip *by
construction* (raw history never reaches the published branch), where a
diff-of-final-tree check would miss a leak added in one commit and removed in
a later one — it still ships in history. (3) It reconciles commit-often with
readable history — the classic feature-branch / curated-integration pattern,
with agents doing the curation.

**Two histories, one authority.** The granular iteration branch and the
curated development branch can confuse a reader: the **development branch is
authoritative**. Because scrub and collation rewrite iteration SHAs,
`status.md`/`log.md` entries cite **stable ids** — OI-n, gate names, dates —
never iteration-branch commit SHAs (the log template states the rule).
Optionally add the `llm/**` pattern to the CI triggers (the shipped
`check.yml` does) so the process floor runs remotely on the iteration branch
too.

## Unattended operation (walk-away runs)

*Referenced from PROCESS.md §4 ("gate authority").* **Applies when** a repo
wants a coordinator to grind work from a single entry point while nobody
watches. The loop runs under **every** gate authority level — what differs is
where it stops: fully walk-away under `autonomous` (or `single-ratify` after
its ratification point), while an `attended` repo's run grinds the in-gate
work and stops *at* each human act with the ask stated, rather than being
refused or, worse, inferring its way past. Generalized from a field adoption's
proven coordinator (the NotHomeWrecker `trigger.ps1`), which
`scripts/agent_loop.py` supersedes — the protocol here is agent-neutral repo
text, so a downstream can build its own coordinator against it.

**The model.** The coordinator **is the parallel dispatcher** (WI-210 — one
engine, one selection path; "Parallel tracks" below has the mechanics):
reconcile owned trains → gate → build-out. It derives the ready WI frontier
from the registry, reserves traincars, and runs **fresh headless worker
sessions** — repo text is the only memory (§7 boundary notes, "Repo text is
the durable agent memory layer"); each session builds its **explicit
assignment** (the WI row + SpecRef + predecessor context + train diff), never
a "resume from `status.md`" prompt — until the queue drains, a stall guard
trips (N consecutive sessions without a commit), or an iteration budget
ceiling hits. Work happens on `llm/train/<id>` branches (never the development
branch), integration is serialized and honors `docs/push-policy` — under the
default `human` the coordinator never pushes, even if asked. At worker start a
dirty worktree (residue from an interrupted run) is surfaced into the first
session's prompt as a reconcile instruction; stash/rollback is deliberately
*not* automated — that judgment belongs to the session.

**The judgment duties, stated once** (WI-210 re-homed them here when the
serial resume driver — the loop that read `status.md`/`run-state` back as its
control input — was retired):

- **Intake/triage of new scope** belongs to the **human + the gate-stage
  sessions**: new WIs enter the registry at planning/ratification (or through
  a dual-plan round's filed children), never by a session inventing scope
  mid-run.
- **Drained-queue handling** is the dispatcher's **end-state banner** — the
  run reports what integrated, what needs attention, and what remains queued.
- **NEEDS-HUMAN surfacing** is the **generated** root `docs/run-state`
  (dispatcher/integrator-written, spec §10): `RUNNING`/`DONE`/`BLOCKED`/
  `NEEDS-HUMAN`, with `NEEDS-HUMAN` carrying one `ask: <one-line ask>` line
  the stop banner headlines. **A wrong DONE is a false green** (§4); a worker
  never writes the file — its exit code and committed trailers are its whole
  result channel.
- **The resume-from-`status.md` prompt is retired** with the path:
  `status.md` is a generated snapshot for humans, never a session's input.

**Optional `docs/pause`** (presence = pause requested; content = a free-form
reason): a **graceful** walk-away stop honored at the *next session boundary* —
the in-flight session finishes and commits normally, then the coordinator stops
(exit 8) with a banner naming the file, **never a mid-session kill**. A launch
with the file present starts no work; **deleting the file and re-launching
resumes** — the file is the whole contract, so `run-state` is left untouched and
resuming is a single act. Under the dispatcher, `docs/pause` stops **new
reservations** at the next boundary while in-flight workers finish their safe
boundary (workers themselves ignore it); absent = not paused, so an adopter
who never creates it pays nothing.

**Optional `docs/blackout`** (first line `HH:MM-HH:MM`, UTC, Mon–Fri): a
recurring window inside which the coordinator starts **no new session** — the
same next-boundary graceful semantic as `docs/pause`, but temporal and
self-clearing. The in-flight session wraps normally, then the loop **waits the
window out and resumes automatically**, so one walk-away launch survives a daily
blackout (unlike `pause`, no re-launch needed). The window is half-open
`[start, end)` — 12:00–19:00 blocks 12:00 through 18:59 and releases at 19:00.
`start == end` disables, and so does deleting the file (absent = disabled,
byte-identical to before); the scaffold ships a **12:00–19:00** default so a
fresh repo gets it without a hidden built-in.

**The phase (in-process routing state).** The coordinator routes each session's
model tier (§6 tiering, mapped per phase) from the phase it is driving. This was
a tracked `docs/run-phase` file; it is **retired** (WI-180) — a repo-global phase
pointer does not survive the move to parallel dispatch, where a build-out lane
routes from its own activity and a `{phase}-{gate}` branch name (the
parallel-dispatch plan, §10). The phase
is now in-process runtime state (review/critique queues + the `BUILD` default);
phase names stay free-form, the named convention below `PLAN`/`BUILD`.

**Plan/build cadence (the bounce).** *Applies when the trajectory /
work-items layer is **not** enabled* — enabling `work-items.csv` + `SpecRef`
**supersedes `docs/plan.md`**: a WI row + its spec-of-record carry the same
content mechanized (`Predecessors` = the sequencing, `BuildTier` = the tier
hint, the spec's Done-when = the observable done-when, R-E gates the hand-off
exists), so running both would keep two "what's next and how" surfaces
(WI-252; delete or never scaffold `docs/plan.md` in that case). On the
zero-tooling rung the cadence stands: the §6 tiering doctrine — *strong model
plans, cheaper model executes, safe because of the gates*. A **PLAN** session
(strong tier) writes or repairs **`docs/plan.md`**: sequenced blocks, each one
coherent deliverable + its tests with an observable done-when, a size class, and
a §6 tier hint. Each **BUILD** session (cheaper tier) executes the next block —
and only it — and, when it finds the plan exhausted or *wrong* (a §5 finding,
never a silent rework), re-chunks `docs/plan.md` before continuing (re-planning
belongs on the strong tier). The coordinator's model map ties the tier to the
phase: `AGENT_MODEL_MAP="PLAN=<strong-model>,BUILD=<cheap-model>"`. The mechanized
bounce — a stop that forces re-planning onto the strong tier — rode the retired
`run-phase` file; under parallel dispatch it becomes the dispatcher's
activity-routing (Slices D–H, in development). On a small scope the cadence
collapses to plan-and-build in one session. The plan
file is the **compressed hand-off**: fresh sessions have no chat memory, and a
block spec is far cheaper to reload than the exploration that produced it — the
strong tier pays the exploration cost once, every cheap session after reloads
only the spec. `status.md` stays the lean resume surface, naming the current
block; finished blocks are logged and pruned.

**Per-phase effort (a sibling knob to the model map).** Just as `AGENT_MODEL_MAP`
routes a *model* per phase, reasoning *effort* can be tiered per phase — a
grep-and-summarize phase is not a crash-debug phase. Two cautions, both
evidenced (effortmining, ~450 pre-registered runs on `claude-opus-4-8`): **(1)
cheap is not free** — at low effort a model does not merely skim, it
*fabricates* (an invented ticket id in the published runs), so route hard work
*up* a tier, never down to save tokens on a task that will hallucinate; **(2)**
the knob that actually bites is **agent-frontmatter effort**, not a prompt-level
cue (a subagent inherits its frontmatter `effort`; `/effort`-style prose in the
task is ignored) — so per-phase effort is set the same way per-phase models are
(a phase-specific agent file / command template), and kept **thin and
replaceable**, since native per-spawn effort will likely obsolete the workaround.

**Sizing the blocks** — the judgment the PLAN phase owns; it cannot be
mechanized, but it can be steered:

- **A block = one coherent deliverable + its tests**, sized for one session.
  *Deep* work (design, a debug loop) gets a solo block — it exhausts context by
  reasoning; *wide mechanical* work (a rename, a sweep) gets a solo block for
  the opposite reason — it exhausts context by breadth; cheap prose/config
  edits get **clubbed** into one block rather than paying a session's
  context-reload tax each.
- **Too small** reads as sessions ending trivially — one small commit, budget
  barely touched — while each fresh session re-pays the full context reload:
  merge the next blocks. **Too big** reads as timeouts, stall-guard trips, or a
  session ending mid-block with no commit: split.
- **The sizing loop has a sensor**: `iteration_index.md` records tokens, cost,
  wall/API seconds, turns, per-turn pace and context volume, outcome, and
  commit range per session (the log header additionally carries boot latency,
  cache read/create volumes, the effort/fast-mode dials, and prompt size). A
  PLAN session reads the recent rows before re-chunking and coarsens or splits
  against the evidence, not a guess.

The cadence needs no coordinator to be useful — an attended human alternating
"plan on the strong tier, execute on the cheap one" across hands-on sessions is
the same protocol with a person as the model map.

**The reviewer dial + cross-provider routing (`docs/review-policy` +
`AGENT_CMD_MAP`).** `docs/review-policy` declares how many independent
fresh-context review verdicts a completed work item gets before the integrator
accepts it — **`0 | 1 | 2`, default `1`** (the file's comment block carries the
full semantics). Floors sit *above* the dial: a gate advance under
`gate-policy: autonomous` always needs ≥1 recorded verdict, and a WI touching
the spine registries recommends `2`. Two reviewers split **charters**, never
duplicate coverage — A = method/risk/corner cases, B = process/trace/prose —
because two samples of one model share blind spots; for the same reason
**cross-provider is the recommended `2` pairing**, and `AGENT_CMD_MAP` (or
`--cmd-map`) makes it first-class: a per-phase *command-template* map in the
`--model-map` syntax (`AGENT_CMD_MAP="REVIEW-B=gemini -p {prompt}"`), matched
against the in-process phase — whose keys are free-form, so `REVIEW-A`/`REVIEW-B`
phases just work — falling back to the single `AGENT_CMD`. (A template that
itself needs `,`/`;` routes through a thin dispatcher wrapper instead.) In
managed mode the loop **schedules the review round** automatically after a
committing build (the reviewer dial sets how many); the loop surfaces the dial
in its banner but never enforces it — the harness pass is the entry ticket,
the recorded verdict is the value. A reviewer is **independent** (no shared
transcript with the implementer; input = the diff + the WI + the TCs), treats
the implementation report as a set of **claims** and re-runs the checks it
asserts rather than trusting them (believe nothing unobserved), and
fixes directly only what lies within the WI's own declared scope — anything
else is *filed as a finding* for the integrator. Reviewer B's process/trace
charter includes one codename check: a **session-local codename in a durable
cell** — a `work-items.csv`/SR/LLR/TC row or a `docs/specs/` file, as opposed to
a `log.md` entry — is filed as a finding (the codename-discipline rule stated
under "Trajectory / work-items"). The charter also files a knowledge pack that
restates a registry fact instead of linking its id. Related tripwire: the
coordinator warns (never blocks) when a lane's `status.md` outgrows one screen
(`AGENT_STATUS_WARN_BYTES`, default 8192, `0` silences) — every session
inherits that resume surface, so pruning it is the integrator's charter,
with evidence living in `log.md` and the iteration logs.

**Heterogeneous scheduling — model routing, reviewer dispatch, and the
escalation policy (`docs/agents.csv` + `docs/agents-enabled`; WI-059).** The
reviewer dial above is *surfaced* by default; when a repo opts into managed
routing the loop *enforces* it — a committing build schedules the reviewer
round(s) before the next build. This is the S8 layer, and it stays stdlib,
consent-explicit (no silent model swap), and never-breaking: **absent the
enable-list, the loop keeps exactly today's single `AGENT_CMD`/`AGENT_MODEL`
behavior**, so a fresh scaffold pays nothing.

- **A model registry, not a catalog — `docs/agents.csv`, the pair-row model.**
  Columns `Id,Family,Model,Version,Tier,CmdTemplate,Env,Notes`, and **one row =
  one (model × route) pair** — this model, reached this way ("pairs now, factor
  later"). The split is **identity vs access**:
    - *Identity* — **`Family`** (who trained it — the heterogeneity + scorer
      corroboration key, *never* how the model is reached), **`Model`** (the
      provider's line identity, INCLUDING `-pro`/`-flash`/`-codex` tokens — those
      are a separately-billed *model line*, not a maturity tag), **`Version`**
      (the *comparable* token only: a dotted numeric like `4.8`, a date stamp, or
      a maturity tag — moving vendor aliases like `chat-latest` never live here).
    - *Access* — **`CmdTemplate`** (`{model}`/`{prompt}` slots) + **`Env`**
      (`KEY=value;KEY2=value2`, merged over the inherited environment at launch;
      **an empty `Env` = the ambient environment = today's behavior**). A
      template that **omits `{prompt}`** has its prompt **piped to the CLI's
      stdin** (written then closed — never an interactive wait), immune to the
      OS command-line caps a brief-sized prompt-in-argv dies on (Windows: 8191
      chars under a `.CMD` shim, ~32767 via CreateProcess) — keep `{prompt}`
      only for a CLI with no stdin prompt path; a codex session additionally
      gets `-o/--output-last-message` injected and read back as the session
      result (codex echoes the prompt into stdout). `Env` is
      the declarative fix for every env-only selector — `CLAUDE_CONFIG_DIR`,
      `CODEX_HOME`, `ANTHROPIC_BASE_URL`, `GEMINI_API_KEY` — which a bare
      `CmdTemplate` (launched `argv`-only, no shell) can't carry.
  The table itself **is the allow matrix** — a (model × route) pair is usable iff
  its row was written, keeping consent explicit (no `Serves` patterns that would
  silently allow a future model). The `Id` is a free-form unique **join key,
  never parsed** (charset: uppercase + digits + hyphen + dot). **`Provider` is
  retired** in favor of `Family`; a legacy registry with a `Provider` column and
  no `Family` reads Provider as Family — never-breaking. Cooldown stays **per row
  id = per access path**, so an account outage or router failure cools only that
  path. The kit ships example rows for the verified headless shapes (`claude -p`
  / `codex exec` / `gemini -p`) and **vendors no model catalog** — richer data is
  a documented pointer to the maintained community registries (models.dev
  `api.json`; LiteLLM's model-prices JSON), never a copy.
- **Account rows and router rows are just more pairs.** A **second paid plan**
  with one provider = a **second pair row** with a distinct id (suffix style,
  `…-ACCT2`), the *same* `Family`, and its own `Env` account selector — so its
  quota pool cools independently by construction. A **third-party router** = a
  pair row whose `Env` points its CLI at the router (`ANTHROPIC_BASE_URL`); it
  shares the native model's `Family`, so it is **not** a diverse reviewer from
  its native sibling (a router is access, not identity). Two safety notes carried
  from the research: **pin LiteLLM away from the known-malicious PyPI builds
  `1.82.7`/`1.82.8`**; and **Gemini OAuth accounts share one credentials file and
  race on token refresh** — multi-account Gemini must use API keys or be
  serialized (Claude/Codex config dirs are token-isolated and concurrent-safe).
  *The recorded revisit trigger (the "factor later" half):* once one route's
  command/env text repeats across enough pair rows that editing it is
  error-prone, factor the route definitions into a named-preset file the pair
  rows reference — the rows stay the explicit allow matrix, only the text gets
  deduplicated.
- **Version-less resolution (newest-in-line, offline & deterministic).** An
  `agents-enabled` token that exactly matches a row `Id` resolves to it;
  otherwise it resolves over rows whose normalized `Family`-`Model` matches
  (column-keyed — the id is never parsed) — **intra-line only** (it never crosses
  a model line, keeping the "different model vs. newer version" trap closed).
  Among those: newest by **dotted-numeric tuple**, then a **maturity-rank
  tiebreak** (GA/untagged > `preview` > `beta` > `exp`, a fixed vocabulary with a
  per-registry override — a `# tag-rank: …` comment line in `agents.csv` or the
  `AGENT_TAG_RANK` env knob), then a **date-stamp** final tiebreak; `preview`/
  `exp` rows are skipped unless explicitly named or the only candidate, and
  equal-key route pairs fall to **registry row order**. "Newest" is computed only
  over rows present in the registry — no network, fully deterministic.
- **Routing = an enable-list + availability.** `docs/agents-enabled` lists, in
  **preference order**, the registry ids (or version-less `Family-Model` tokens,
  resolved above) this repo may use — the consent surface, and the switch that
  turns managed routing on (it is deliberately *not* scaffolded; absence =
  routing off). Per session the loop selects from that pool by the phase's tier
  (`AGENT_TIER_MAP`/`--tier-map`, else the built-in phase->tier defaults —
  iteration reviewers default to a cheaper tier). An optional per-phase
  `AGENT_PREFER_MAP`/`--prefer-map` (for example `BUILD=OPENAI-SOL`) moves one
  enabled id ahead of that list **within the resolved tier only**; an unknown,
  disabled, wrong-tier, or cooling id falls through to enable-list order, and
  absence preserves that order byte-for-byte. For *proportional* preference
  rather than a single pin, an enabled id may carry per-phase **draw weights** —
  `<ID>[ <PHASE>=<int>]…` after whitespace (e.g. `OPENAI-TERRA  REVIEW=4`;
  `PHASE` ∈ BUILD|REVIEW|CRITIQUE|DESIGN-CHECK, `REVIEW` covering both reviewer
  legs; unannotated = weight 1 everywhere, byte-identical to before) — and draws
  then follow a **deterministic weighted rotation** over the *legal* remainder,
  keyed on the **per-phase draw ordinal** (the count of prior same-phase sessions
  on the train, read from the durable session logs — NOT the global session
  counter, which strides across phases and would alias against the weight sum;
  no randomness), renormalizing when a model cools. A pin still wins its phase
  outright; a weight can never force a same-family review, a weaker tier, or a
  disabled id; `PHASE=0` is fallback-only (drawn only as the sole legal
  candidate); a conflicting redeclaration of an id, or any malformed annotation,
  fails preflight naming the line (the file is the consent surface). The
  **family**-heterogeneity rules
  still win for reviewers and critics; a model whose session fails to start or stalls
  goes on **cooldown** (the rate-limit backoff, generalized per-model,
  `AGENT_COOLDOWN_SECONDS`) and is retried; when no enabled model of the
  preferred tier is available the loop walks the **next tier up — never a weaker
  one**, and pages rather than silently downgrade. **Every selection and
  cooldown is logged before launch** (consent = the enabled set + these declared
  rules). Failure context rides the registry's `Notes` column: the page-human
  banner renders the enabled pool per row (tier, family, cooling state, Notes),
  and a cooled or preflight-failed row's Notes is echoed at the failure point —
  put the provider's install/sign-in hint there (e.g. `opencode auth login`),
  so an exhausted pool says what to *do*, not just that it paged.
- **Per-WI build tier (a `BuildTier` column; WI-126).**
  Tier is otherwise per-*phase*, so a docs-only WI and a spine-critical engine WI
  both ride the BUILD default. An **optional `BuildTier` column** on
  `work-items.csv` (`strong|medium|quick`, legacy `weak` reads as `quick`;
  empty/absent = the phase default) names a WI's *starting* build tier. The
  dispatcher reads it **directly from the reserved WI's row** (the
  parallel-dispatch plan, §10); the
  hand-curated `docs/next-wi` pointer that once carried it is **retired** (WI-180,
  with its `;`-batch and gate-first advisories). It **composes with
  tier-up-never-down**: the column sets where a build *starts*; a contested review
  still escalates above it, so it never caps escalation. **Set the tier while
  filing or triaging the WI:** `quick` for mechanical, off-spine work, `medium` by
  default, `strong` only for design-shaping or spine-touching changes — a
  deliberate planner decision, never a mid-loop downgrade.
  **Traincar batching (WI-133 → the scheduler).** Independent, off-spine dev
  slices that once rode a `;`-joined `docs/next-wi` batch now cluster into a
  **traincar** — one branch, one Build pass per WI, one review round over the
  combined diff — packed by `schedule.py` (the scheduler contract) and dispatched
  by the parallel dispatcher (Slices A/D). The single-review amortization and the
  off-spine-only rule are unchanged; the mechanism moves from a driver-curated
  file to the registry-derived frontier.
  **Review rework carry-forward (WI-170).** When a managed review merges to
  `CHANGES-REQUESTED`, the coordinator records the reviewed BUILD scope in
  `docs/rework-wi` and reworks it before taking new work (its prompt, telemetry
  label, and BuildTier lookup all follow it), so a build that already advanced
  cannot orphan its findings. It stays durable through further review rounds and
  coordinator restarts; only an `APPROVE` of that scope clears it. Under parallel
  dispatch this becomes assignment-scoped dispatcher state (§8 of the dispatch
  plan).
- **Reviewer independence (the evidence-backed core).** Reviewers are fresh
  sessions, **two families, at least one differing from the implementer's —
  *preferred, not required*** (family = who trained the model, so a router-fronted
  row is not diverse from its native sibling). The reviewer prompt gets the diff + the
  requirement surface and **never the implementer's self-assessment** (leaking
  it collapses finding rates several-fold); it ships as an embedded **redacted
  reviewer prompt**, overridable per phase with a prompt-template **file** via
  `--prompt-map`/`AGENT_PROMPT_MAP` (each entry preflighted like
  `AGENT_CMD_MAP`). **No debate rounds** — independent parallel reviews,
  mechanically merged (CHANGES-REQUESTED if any reviewer requests changes).
  **Degraded availability is ruled legal:** when only one family responds,
  two independent *same-family* sessions review — fresh context is the
  invariant, family diversity best-effort (the scorer already weights
  cross-family corroboration above same-family). Verdicts are **repo files**
  (`docs/reviews/NNN-<PHASE>.md`) in the `log.md` block format plus one machine
  line: `VERDICT: APPROVE|CHANGES-REQUESTED findings=N`.
- **The substance scorer (`scripts/score_reviews.py`) is advisory.** It scores a
  verdict block by confirmed-finding rate, cross-reviewer corroboration
  (cross-family weighted up), anchored-finding precision (anchors must resolve;
  capped), and actionability. **Severity hygiene and the anti-gaming tripwires
  are gates, never scores; length never scores positively.** The tripwires
  (finding-cap pinning / count gaming, near-duplicate review text, an
  implementer diff touching a review or policy path, mass finding-rejection) are
  **non-scored hard stops** that page the human. The scoreboard is one small
  decayed-tally text file (`docs/reviews/scoreboard.txt`: per-provider substance
  + the round history) — the declared policy picks, nothing auto-optimizes.
- **A fixed escalation policy, not a learned router** (per-project sample sizes
  are far too small for a bandit): **win-stay/lose-shift** — the higher-substance
  family becomes the next round's primary feedback source only on a **margin
  >= 2**; the implementer's family **swaps after 2 consecutive failed review
  gates**; the tier rises **only after the swap also fails**; and the loop
  **pages the human** on 2 top-tier failures (the shared-failure regime — the
  spec is wrong, not the model), on opposite verdicts twice running, or on any
  tripwire. The constants ship as legible **per-repo-overridable defaults**
  (`AGENT_ROUTE_MARGIN`, `AGENT_ROUTE_SWAP_AFTER`, `AGENT_ROUTE_PAGE_TOP_TIER_FAILS`)
  — calibration values, not spine facts.
- **Failure semantics follow `docs/gate-policy`.** On a page-the-human condition
  the causing WI **and its hard-edge dependents pause** in every mode; the mode
  decides what happens around that — **attended:** start nothing new, let
  in-flight sessions close out, then the loop stops `NEEDS-HUMAN` and alerts;
  **single-ratify:** keep working non-dependent WIs to completion, surface the
  block for ratification; **autonomous:** schedule a fresh **design-check
  session** (different provider, strong tier) to rule grind-through vs. genuine
  redesign, document every assumption, and continue — a redesign verdict
  re-enters the change-intake flow (process.md §5).

**Session discipline.**

- **Commit every session** — the stall guard makes an empty session an abort
  signal; even a Blocked-register entry or a recorded decision is a commit
  (§3 commit cadence).
- **No elevation, no interactive tools** — a step that truly needs admin
  rights or a TTY is a Blocked item, never a prompt nothing will answer.
- **Keep `status.md` lean across iterations** — each session appends its
  evidence (verdicts, decisions, session summary) to `log.md` (§5) and leaves
  `status.md` holding only the resume point + open/blocked items, so the next
  fresh session's context reload stays cheap.
- **End-of-run evidence:** `status.md` Current State + Blocked register;
  verdicts + Decisions in `docs/log.md`; a clean tree.

**Iteration logs are tracked, indexed repo artifacts.** The coordinator writes
each session's log to `docs/iteration/NNN-<stamp>.log` — size-bounded (head +
capped tail of the transcript) so forensic detail survives machine death and
travels with the repo; the raw unbounded stream may additionally go to the
gitignored `out/run-logs/` for local debugging, and is echoed **live** to the
coordinator console as it arrives (compact one-line renderings for a
stream-json CLI's events; `--no-session-echo` silences the console, never the
capture; `--live-status` / a `docs/live-status` toggle upgrades the scroll to
one in-place status line per workstream when stdout is a TTY, a pipe/CI log
keeping the append-only scroll) — and regenerates
`docs/iteration_index.md`: one row per session (number, date, phase, the WI it
claimed, model/tier, outcome, commit range, tokens, cost, wall/API seconds,
turns, per-turn pace + context volume, log link), generated and never
hand-edited. **The coordinator commits this bookkeeping in its own
`telemetry:` commit the moment it writes it** — so the log + index (and the
review scoreboard) never ride the next session's *work* commit or dangle in
the tree; it is best-effort (a hook veto leaves the files in place, as before).
`docs/log.md` stays the *collated* human-review layer above it.
On an privacy-checked repo the logs ride the iteration branch and pass its scrub
with everything else.

**Limits are handled reactively.** Plan-usage state is not scriptable, so the
coordinator cannot preflight remaining budget: a limit-hit session returns a
machine-parseable "…limit · resets <time>" message, and the coordinator backs
off — sleeps until the reset (bounded) or exits with a WAITING banner naming
the resume time. Both am/pm and 24-hour reset clocks parse (the wording is
locale-dependent); an unrecognized wording sleeps a bounded fallback
(`--limit-retry-fallback`, default one hour) rather than killing the run.
**Limit-hit sessions never count toward the stall guard** —
three throttled sessions are not a stall, and the NHW original misread
exactly that.

**A failed session is not a work stall.** A session that errored *before it
could work* — the CLI reported an error result, or it could not be launched (a
retired model, expired auth, a broken CLI) — is logged with the `ERROR` outcome,
distinct from `NO-COMMIT` (a healthy session that simply idled). It still counts
toward the stall guard, but when a whole stall run was `ERROR`s the abort banner
names an **unavailable agent**, not a stuck task, and points at the fix — an
unsupported model is repointed by hand (`--model` / the model map). Auto-fallback
to a substitute model is deliberately **not** done: the human consented to a
specific tier, and a silent swap could run an unlisted (unguarded) model.

**Consent is unmissable.** Unattended mode passes the agent CLI's
permission-bypass flag. The human consents by (1) filling the launcher's
`AGENT_CMD` slot, (2) declaring the gate policy, and (3) running it — and the
loop banner and README say so plainly. git + CI remain the enforcement floor.
The coordinator's preflight refuses to start iteration 1 while
`docs/privacy-check` is on and the configured git author email is not exempt
(an unattended run under a private identity is the history-leak disaster case)
or the agent CLI is missing —
report and nonzero exit, never a hang.

**The shipped engine + launchers.** `scripts/agent_loop.py` (stdlib-only, one
implementation for every platform, tested in the kit suite against a fake
agent command) is the loop above; root `agent-resume.{cmd,sh,command}` are its
double-click wrappers, scaffolded like `run.*` and **inert** until the
`AGENT_CMD` slot is filled (guidance + nonzero exit). `--interactive` boots a
single hands-on session at the mapped tier instead of the loop. A repo that
doesn't want the entry point deletes the launchers; the protocol stands alone.

## Critique verification & the critique loop

*Referenced from the "Unattended operation" layer above.* **Applies when** a
requirement's acceptance is **subjective** — "a realistic-looking render", an
artifact comparison with no crisp measurable interface. The implementer session
cannot judge its own output (a real project shipped awkward render artifacts
because "the agent didn't know how to judge it, it just shipped it"), and the
original TC may have been lax. `Critique` gives another agent a **different hat**:
an independent critical eye that says *where and why* something isn't good enough
and drives rework toward a written bar. Built on the S8 chassis (fresh sessions,
redacted prompts, verdict files, `gate-policy`-keyed escalation).

- **`Critique` is a first-class Verification value** (PROCESS.md §4). A perceptual
  TC declares `Verification=Critique`; its `Method` names the critique procedure and
  its `Parameters` name a **rubric** (`docs/rubrics/<name>.md`) plus the **artifact
  recipe** (the command/steps that produce the render/output under judgment). The
  `CRITIQUE` leg is its mechanization; human **`Attest`** stays a distinct, unmixed
  value — that separation is the point of the ruling.
- **The rubric derives from the SN/SR intent, never the TC** — the inversion that
  catches a lax TC instead of inheriting it. A rubric carries **numbered good
  (`G#`) and bad (`B#`) anchors** — definite, citable entries, TC-style. The
  reference **builds over time**: a critique finding that names a new failure mode
  is added as a new `B#` anchor at rework, so the next round judges against the
  **accumulated** reference, and every verdict **cites anchor ids** (what makes
  rounds comparable across sessions). See [`docs/rubrics/`](rubrics/README.md).
- **Redaction by construction.** The critic gets the rubric + the SN/SR intent +
  the artifact recipe and **never the implementer's self-assessment** (`status.md`,
  `log.md`, the session transcript) — the same rule the reviewer prompt follows.
  It ships as an embedded `CRITIQUE_PROMPT`, overridable per phase with a
  prompt-template **file** via `--prompt-map`/`AGENT_PROMPT_MAP` under the
  `CRITIQUE` key. The critic is provider-heterogeneous from the implementer when
  available (`agent_route`), strong-tier by default.
- **The optimization loop, bounded.** BUILD → CRITIQUE → rework, iterating until
  `APPROVE` or the budget (`AGENT_CRITIQUE_MAX`, default **3**, env-overridable
  like the S8 knobs) trips the `gate-policy` page-the-human path. A WI row may
  override that run-wide default with `CritiqueBudget=n|inf` (`inf` means iterate
  until `APPROVE`) and set `CritiqueExhaustion=move-on|block`; absent/invalid cells
  preserve the global default + move-on, while `block` forces `NEEDS-HUMAN` under
  every gate policy. `inf` remains bounded operationally by `--max-iterations`,
  the per-session CLI limits, and the declared pause/blackout controls. In a
  batched build, `inf` and `block` win; otherwise the largest budget wins. The trigger is a
  committing build whose WI touches a `Critique` SR (read straight off the spine);
  absent an enable-list or any `Critique` SR, nothing changes.
- **The lax-TC ratchet.** A `CRITIQUE` round that returned CHANGES-REQUESTED and
  then closes the WI with **no change to the validation chain — the TC prose, the
  test logic, or the rubric file** — trips the warn-first no-validation-delta check
  (`check_trajectory --staged`): the fix must land in the chain, not just the
  artifact. This is the specific mechanism that stops "shipped it because nothing
  judged it" from recurring.
- **The arbiter split.** Working default: **the critic gates iteration; the human
  owns acceptance.** A critic `APPROVE` ends rework; gate closure still carries the
  human `Attest` (the strong-model floor and the attested-vs-mechanized split
  stand). Under `gate-policy: autonomous` the critic verdict closes
  iteration-level acceptance and the recorded-verdict rules govern the gate as they
  do today. (This does not contradict the S8 "no LLM-judge tiebreaker" ruling —
  that ruled out an LLM arbitrating between *reviewers' scores*; here the quality
  itself is perceptual and an LLM eye is the only mechanizable instrument.)
- **The multimodal caveat.** Image-capable CLIs read local renders/screenshots
  natively from the recipe's paths; **capability varies per model** — note it in
  the registry `Notes`, and a text-only model runs a **degraded text-proxy
  critique** (it judges the description/output text and says so). Honest
  degradation, never a silent pass.

## Dual-plan decomposition

**Applies when** a goal deserves adversarial pressure on its WI decomposition
*before* build — it declares an **optimization target that resists a
measurable budget** (a captured `PB-###` + `check_perf` stays the first
preference: the harness is a better adversary than a second opinion), the
decomposition plausibly spans **two or more modules or any IF seam**, or the
scope is design-shaping (`strong`-tier). One declared trigger at filing time,
like `BuildTier` — never a vibe call mid-loop. Single-planner filing stays the
norm; this layer fires only on its applies-when.

**Why select-and-port — never merge, never debate-to-consensus.** Peer LLMs
iterating on each other's feedback conform rather than challenge (measured
sycophantic conformity; "consensus collapse" can eliminate a correct answer
already on the table), gains concentrate in round 1 and drift past 2–3, and
plan *fusion* is unpublished — naive union of two WI DAGs yields incoherent
predecessors and duplicated scope. What does hold up: independent generation
with real cross-family diversity, a judge *separate* from the generators that
judges **artifacts, not conversations**, rubric anchoring over bare
"which is better", and externally computed feedback. Evidence:
`docs/knowledge/co-planning.md` in the kit's home repo (retrieved 2026-07-16).
**Transfer caveat:** that literature benchmarks QA/math/code with objective
verifiers, not plan artifacts — this protocol is the best-supported
extrapolation, not a proven design.

The protocol rides the S8 chassis (fresh sessions, redacted prompts, verdict
files, `agent_route` family heterogeneity, budgets) — **no new engine**:

1. **Two independent planners,** different model families where available (two
   samples of one family share blind spots; the reviewers'
   degraded-availability rule applies — fresh sessions are the invariant,
   family diversity best-effort), given **identical redacted briefs**: the
   goal brief + the SR surface + the IF registry — never each other's output,
   never the driver's self-assessment.
2. **The commensurability contract.** The goal brief declares numbered clauses
   (`C1:` …). Each plan is a table of proposed WI rows
   (`Plan-WI | Title | Covers | Interfaces | Predecessors`): every row cites
   the clauses/`SR-###` it covers and the `IF-###` it acts on — existing ids,
   `Proposed:` plus a nearest-existing-IF rationale (the same rule specs
   follow), or the intra-module escape. This is what makes rival plans
   mechanically comparable.
3. **Mechanical coverage pre-pass:** `plan_coverage.py` (stdlib) computes each
   plan's clause coverage, flags unresolvable clause/SR/IF refs, `Proposed:`
   seams missing a rationale, and predecessor cycles, and emits the pairwise
   coverage diff — the external, checkable signal that makes the one critique
   round work.
4. **One rubric-anchored cross-critique round — hard cap n=1.** Each plan is
   critiqued by the *other* family against the plan rubric
   (`docs/rubrics/<name>.md`: solvability / completeness / non-redundancy
   anchors plus the seam-duplication anchor) and the coverage report. One
   revision each. No further rounds, ever.
5. **Arbiter select-and-port.** A fresh session, third family where available
   (an arbiter sharing a family with a planner is recorded and mitigated —
   self-preference bias): **provenance-anonymized, position-swapped** pairwise
   comparison — run the arbiter prompt twice with the plan order swapped; the
   verdicts must agree, disagreement is a position-bias page-the-human —
   against the rubric + the coverage report + the owner's original prompt,
   warned that **more WIs ≠ better** (verbosity bias). It selects **one** plan
   and **ports named loser-WIs** that close coverage gaps, each port a cited
   delta in the verdict file. Never a merge. (The S8 "no LLM-judge tiebreaker
   between reviewer scores" ruling stands — this arbiter compares *plans*.)
6. **Artifacts are repo files:** one round directory `docs/plans/DP-NNN-<slug>/`
   (goal brief, both plans and revisions, critiques, `coverage.md`,
   `verdict.md` with the ports), the verdict summarized in `log.md`. The
   selected plan's rows are then filed as real WIs through normal intake.
7. **Acceptance:** human `Attest` closes the round per the gate philosophy;
   under `gate-policy: autonomous` the recorded-verdict rules govern, as they
   do for the critique loop.

The three hat prompts ship as kit templates —
`prompts/dual-plan-{planner,critic,arbiter}.template.md`, copied in when the
layer is opted into (not scaffolded by default) — with the redaction,
anonymization, position-swap, and anti-verbosity instructions **embedded in
the prompt files**, so the safeguards ride the artifacts, not session memory.
The coordinator runs the round unattended: `agent_loop --dual-plan <WI>` over
a queued WI whose registry row declares **`PlanMode=dual`** (the trigger is
declared at filing, never by flag; the worker path refuses a dual row as a
direct BUILD, fail-closed). The manual protocol above remains the fallback —
and the stronger-isolation option (empty-cwd sessions).

**SELECT disposition fails closed on registry validation.** The filed child
rows and their generated OKF/dashboard views are one atomic transaction. If a
present generator rejects the new registry, the integration ref does not move:
the dispatcher returns the generator/validator tail, quarantines the WI through
the normal error path, and salvages `docs/plans/DP-*` evidence to
`out/dispatch/salvage/<train>/`. Committing evidence with stale views is not a
portable fallback — the shipped freshness hook would reject it — and bypassing
the hook would make a known-invalid registry authoritative.

## Tier-conditional guardrails

*Referenced from the "Unattended operation" layer above.* **Applies when** an
unattended run maps **different model tiers to different phases** (the
`--model-map` servo keyed on the in-process phase) and you want the weaker tier to operate
more procedurally — extra plan/verify/reference-sweep discipline — while a
frontier tier plans unguarded. This is an **accelerator, not a gate**: it never
blocks a run, and a repo that leaves it off is unchanged.

**The insight.** A set of always-on "guardrail" instructions (an event-phrased
routing table + a few iron rules) can make a mid-tier model behave closer to a
frontier one, but the same rules are ritual noise under a frontier model. The
only thing that must be tier-conditional is that **always-on core**; on-demand
playbooks can sit permanently on disk for every tier, because a session never
told to route to them never reads them. So the coordinator — the one place that
already knows each session's resolved model — injects the core only when it
should, mutating **nothing** in the workspace.

**The mechanism.**
- **Content is vendored, not shipped by the kit** (one staleness hop, no
  third-party redistribution). A repo copies an upstream guardrails set
  **verbatim** under `docs/guardrails/` — `core.md` is the whole upstream
  always-on file; its `BEGIN/END KIT CORE` block is what gets injected (the
  whole file if it carries no such markers). Playbooks (`PLAN.md`, `CODE.md`, …)
  sit beside it so the core's routing table resolves.
- **`docs/guardrails-policy`** (same first-line parse as every declared-policy
  file; absent = `off`, not scaffolded). The value is case-insensitive:
  - `off` → never inject; `all` → every session.
  - `<sub> [<sub> …]` — an **allowlist** of model substrings: guard when the
    model matches any (e.g. `opus sonnet`). Name the weaker tier(s).
  - `all except <sub> [<sub> …]` — a **denylist**: guard everything *except*
    models matching a listed substring (e.g. `all except fable`). Name your
    **frontier** model, and a newly added quick tier is guarded automatically —
    the more rot-resistant form.
  The token is necessarily per-repo (it names a model in *this* repo's map, not
  a shared list); if it would guard none of the run's configured models — a
  stale/mistyped allowlist, or an `all except` covering every model — the
  coordinator warns at startup that the guard is inert (it still runs,
  unguarded). A single-tier repo that wants no naming uses `all`.
  - **Recommended value once you vendor: `all except <your frontier model>`**
    (e.g. `all except fable`) — guard every tier *but* the strongest, so adding
    a weaker tier later needs no policy edit. This is a *recommendation*, not the
    code default: absent stays `off`, because an active default would fire the
    "core absent" warning every session in the vast majority of repos that never
    vendor guardrails, and hard-coding a frontier model name into the kit is the
    very model-name rot the per-repo token avoids. Set it when you opt in.
- **Injection is local-only.** `scripts/agent_loop.py` prepends the vendored
  core to the session prompt when the policy selects that session's model —
  read from the **local vendored copy, never fetched at launch** (remote text
  into an agent's instructions is a supply-chain surface; the pin + a reviewed
  re-vendor commit are the control). A selected-but-absent core warns once and
  runs without it. Each session log records `guardrails: on/—` for audit.
- **Drift is caught, not auto-fixed.** `docs/guardrails/UPSTREAM` pins the raw
  base URL + commit and maps each vendored file to its upstream path;
  `scripts/check_vendored.py` hash-compares against the pin and **warns**
  (network-gated: a clean skip offline, so it never blocks CI). Updating is a
  human-reviewed re-copy that bumps the commit — never automatic. It is
  deliberately **not** wired into `check.py` (the gate stays hermetic).

**A reference upstream.** A worked example of a vendorable set is the Guardrails
Kit ([`TheColliny/FableClaudeMDForOpus`](https://github.com/TheColliny/FableClaudeMDForOpus)):
an event-phrased routing table + iron rules delimited by `BEGIN/END KIT CORE`
markers (in its `CLAUDE.md`) with `docs/guardrails/{PLAN,CODE,DEBUG,VERIFY,
EFFICIENCY,SESSION,TRAPS}.md` playbooks beside it — the exact core-plus-playbooks
shape this layer injects. To adopt it, vendor that `CLAUDE.md` as
`docs/guardrails/core.md` (the markers travel with it, so only that block is
injected) and the playbooks unchanged, then pin the source so drift is caught:

```
# docs/guardrails/UPSTREAM
base = https://raw.githubusercontent.com/TheColliny/FableClaudeMDForOpus/<commit>
docs/guardrails/core.md = CLAUDE.md
docs/guardrails/PLAN.md = docs/guardrails/PLAN.md
```

and set the recommended `guardrails-policy: all except <your frontier model>`.
(It is agent-behavior *content*, adapted independently — never redistributed by
this kit; the pin + a reviewed re-vendor commit are the supply-chain control.)

**A related opt-in — efficiency packages.** The same vendor-and-pin discipline
suits *token-efficiency* agent packages (orthogonal to the guardrails core: they
shape output verbosity and tool-output cost, not tier-conditional routing) — a
worked example is [`JayPokale/RDXmin`](https://github.com/JayPokale/RDXmin) (a
YAGNI output-ladder ruleset + a `PostToolUse` scrub/elide/dedup tool-output
compressor). Vendor one, or fold its ideas into your own package; **weigh it at
kit adoption and at each re-sync** (the adoption guide flags both moments).

**A related opt-in — design-system packages.** **Applies when** the product has
a UI/design-system need. [`jrpease/throughline`](https://github.com/jrpease/throughline)
is a worked, vendorable package for design tokens, component libraries, and
visual-regression tooling. Its manifest and gates complement this process; keep
`check.py` as the downstream's single gate runner rather than competing runners.

**The boundary.** Guardrails govern *in-session agent mechanics*; the process
(gates, traceability, the honest-gate rule) governs *artifacts*. A guardrail
never relaxes a gate, and the honest-gate rule still owns every `run-state`.
The meta-repo dogfoods the mechanism (tests) but runs the policy **off** — its
own sessions are frontier-tier, so there is nothing to guard.

## Enforcement audit — which file enforces this rule tomorrow?

**Applies when** your working agreement or process has grown past what one
reader holds in their head and you want to know which rules actually bind.
Written rules decay — context resets, the next model is weaker, goodwill can't
be assumed — so this audit asks one question of every behavioral rule: *which
file enforces it tomorrow, when nobody is being careful?* Each rule is
classified by the **strongest** mechanism that holds it up:

- **Harness** — a deterministic check at a lifecycle event (a git hook, a
  `check.py`/`trace.py` step, CI). The script decides; the rule cannot be
  forgotten. Strongest, and the default home for anything mechanizable.
- **Test** — a regression net (`tests/`): a bar checkable only by executing
  against a fixture. The enforcer for behaviors that are outcome, not syntax.
- **Reviewer** — delegated to an independent reviewer charter (the reviewer
  dial above), which gains a perspective a hook can't: judgment on method,
  risk, and prose.
- **Prose** — kept in the always-loaded guide because it shapes every decision
  and no mechanism can capture the judgment (e.g. "ask one good question").
  Only as strong as compliance — so reserved for what genuinely can't be
  mechanized, never a hiding place for a rule that *could* be a check.

The bar is **honesty**: a rule with no enforcer is either rewritten into one of
the classes above or flagged plainly as unbacked — **zero unenforceable rules
without a stated reason**. Recording the result as a short table in `docs/`
(one row per rule → its primary enforcer + the file) turns "we have rules" into
"here is where each one bites," and surfaces the gaps worth closing — an
Inspection that should be a Test, a guide rule no hook backs. (The meta-repo
dogfoods this over its own working agreement; a live example finding it caught
was the stdlib-only rule, promoted from an Inspection to a real test.)

## §7 boundary notes

*Referenced from PROCESS.md §7.* These three notes draw lines around what the kit
is and isn't; a small project can read the one-line summaries in §7 and come here
only if a boundary is contested. **Applies when** onboarding contributors, wiring
a developer workstation, or deciding whether to add an external measurement or
agent-runtime tool.

**A third toolchain layer — the developer workstation.** The two check layers (§7)
cover what the *project* needs to pass its own gates. A third, often-conflated
concern is what a **human** needs to view, render, edit, and run any of it at all:
a language/runtime, `git`, an **offline** Markdown+Mermaid renderer (e.g. VS
Code's preview, or `@mermaid-js/mermaid-cli`), and optionally an IDE or a
domain-specific viewer (CAD/image/publication tooling). "No required tools" was
always a claim about the **process** layer (stdlib only); it never meant a human
needs nothing. Naming this third layer resolves the conflation between
"procurement for the product" and "procurement for developing the product."

**The onboarding ladder — Provision-for-development, applied to the act of
developing itself.** A fresh contributor's path to a running checkout mirrors the
§4 lifecycle phases, one level up:

```
Stage 0           →  dev-setup       →  setup          →  check
get git + repo        workstation        product deps      run gates
(pre-clone)           (post-clone)       (venv/tools)       (exists)
```

`Stage 0` and `dev-setup` provision the **developer workstation** above (rare,
once per contributor); `setup` provisions the **product toolchain** (recurs per
clone/CI run); `check` is the **process** floor that already exists. Each rung is
an optional, readable, **consent-first** helper — never a silent or compiled
installer — so a contributor (including a non-code one, whose deliverable is still
a reviewable git change) can go from a bare machine to an editable, testable
checkout without needing prior git literacy.

**The pre-commit floor is wired from `dev-setup`, not only `setup`** (WI-1.42).
Enabling the git-hook process floor (`git config core.hooksPath .githooks`) is
universal (every committer wants it, including a non-code one), zero-dependency,
and reversible — so `dev-setup --baseline` wires it, and `setup` wires it too
(idempotent), meaning a contributor is protected from the rung they actually run
rather than only if they reach `setup`. A code contributor's `dev-setup` also
offers to chain into `setup` for the product toolchain, so onboarding is one
command; a non-code role is not asked. The shipped `hooks/pre-commit` finds the
harness at `scripts/` by default; a repo whose harness lives elsewhere (the kit's
own meta-repo, under `project-trajectory/scripts/`) points it there with
`KIT_SCRIPTS_DIR` and a two-line wrapper, so one shipped hook fits any layout.

**The evaluator's rungs — README + run launchers.** The ladder above serves the
*contributor*; a project also has *evaluators* — the stakeholder, a tester, the
future you — whose path is shorter: understand it, then run it. Two artifacts
serve that path, both scaffolded by bootstrap:

- **`README.md` is the human front door and exists from day one.** Bootstrap
  lays down a skeleton (project name filled from the folder; everything else a
  marked fill-in) and the kickoff agent **builds it out from the project brief**
  — purpose, how to run it, how to get started. An adopted repo keeps its own
  README (bootstrap never overwrites); retrofit the run/getting-started pointers
  into it instead (ADOPTING.md §1).
- **Root `run.{cmd,sh,command}` launchers — one double-clickable start per
  platform the project supports** (the PROJECT BRIEF's "Supported platforms"
  line). Ease of access is a requirement of its own: the launch command may be
  obvious, and it may be documented in the README, but *recall is still the
  enemy* — a launcher turns "remember the incantation" into "open the folder and
  click". A project rarely has just one thing to run — *serve the app and open
  its page* versus *build the ISO and launch the burner* — so the launchers
  present a **capability menu**. Capabilities are declared **once**, in
  `docs/stack.ini`'s `[run]` section: one `<name> = <command>` line per
  capability plus an optional `<name>.desc = <one line>`, each command a full
  shell line (a multi-step capability lives in a project script named here once).
  Each launcher is a thin delegate to `scripts/run_menu.py`, which reads that
  section — no args = a numbered interactive menu, `run.sh <name>` = a direct
  launch (exit code passed through), `run_menu.py --list` = a stable
  `name<TAB>desc` machine listing (the agent surface). The launch command lives
  in exactly one place (the duplicated `RUN_CMD` is retired); `run.command`
  delegates to `run.sh` so macOS costs no extra copy. They ship **inert** — an
  absent or empty `[run]` section prints guidance and exits nonzero, the same
  always-scaffolded-inert stance as the optional registries — and a pure library
  deletes them and describes usage in the README instead.

**Offline-render principle.** Legibility artifacts (the Mermaid diagrams, the
trace HTML map, the code map) must render with **local, offline** tooling — never a
cloud rendering service — the same reason the kit chose Mermaid-in-Markdown (§3) in
the first place. Point contributors at a local renderer; reach for a Kroki/PlantUML
*container* only if a project genuinely outgrows Mermaid.

**The kit generates legibility; it does not score it.** The harness *builds* the
traced spine, the committed code map, and the gates, so a repo scaffolded from this
kit should score well **by construction**. *Measuring* that legibility over time
(AI-readiness, complexity/churn dashboards, doc-navigability scores) is a separate,
deliberately **external** concern — run an **external readiness assessor** (e.g. a
deterministic codebase-scoring tool) as **optional downstream tooling**, never a
kit dependency. This is the same stance the kit takes on `ruff`/`pytest`: it names
the gate; the project picks the tool. Generate here; measure there.

**The kit is a spec; a turnkey agent-runtime harness is a different layer.** This
kit is a stack-agnostic, stdlib, agent-neutral process **spec** you copy into a
repo. A **turnkey agent-runtime harness** — e.g. an `npx`/Node-installed engine
shipping skills/agents/hooks/MCP for one tool, with deterministic verification
gates, model-tiered subagents, and a project-context layer — is a different,
installed **product** a downstream shop may run *in addition*. They **compose** (a
repo scaffolded from this kit can be driven by such a harness) but neither depends
on the other: a runtime harness is optional, tool-specific, downstream tooling,
never a kit dependency. Its "back every verdict with a deterministic gate" stance
is the same one §6 already takes — the philosophical fit is real, the dependency
isn't.

**Repo text is the durable agent memory layer.** An agent session starts cold;
**re-reading `AGENTS.md` + `docs/status.md` + the code map is the context reload**,
not a custom memory tool. The kit's committed artifacts already form the
agent-neutral, reviewable memory layer: `status.md` *Current State* (cheap
context reload, §6), `AGENTS.md` (guide re-read every session), the generated
code map (layout without re-deriving it), the registries (requirement + interface
truth), `docs/gate` (current bar). **Agent-native memory tools** — e.g. auto-memory
dirs, MCP memory servers, `.planning/`-style context layers — are a legitimate and
optional *scratch* space for a session's working notes; they are **not** the home
for any load-bearing fact. Why: agent memory is per-session, per-host, and often
per-tool; it is invisible to other agents and humans, unreviewable, and silently
erodes the single-source-of-truth discipline the kit is built on.

**The promote rule.** When a working note ripens into something durable — a
decision, a constraint, a gotcha, an assumption confirmed — **promote it into the
repo**: record a decision in `status.md` *Open items* (ratified: `log.md`'s
*Decisions log*), add a
constraint to `status.md`'s constraints block, update `AGENTS.md` if it changes
how contributors should behave, or amend the relevant registry row. This is the
flip side of the *Assumptions* log (§4, Thread 3): an unattended assumption is
logged to `status.md` so a human can confirm or revert it; a confirmed finding is
committed into the appropriate artifact and drops out of the assumptions list.

**No agent-memory tooling is installed or required.** Dev-setup provisions the
*workstation* (§7 "Onboarding ladder"), not the agent runtime; the kit does not
install, scaffold, or depend on any memory tool. A larger repo makes the committed
layer matter *more* (keep `status.md` *Current State* tight so re-reads stay
cheap), and a query-time semantic index (§7 map-vs-index note) can help chase
references across a large tree — but both are optional, downstream, and orthogonal
to the promote rule.

**The owner scratchpad is human scratch, not a working surface.** Bootstrap
scaffolds a root `OWNER_SCRATCHPAD.md` — the human owner's counterpart to the
agent scratch above: free-form notes that may be old, contradictory, augmented, or
half-formed. **LLM agents must not read, index, summarize, cite, or act on it**;
its own loud header says so and is the primary defense (the meta repo's `CLAUDE.md`
carries the same one-liner). Nothing there is a requirement, ruling, or working
surface — those stay `docs/status.md`, the registries, and `docs/log.md`.
`check_docs.py` exempts the file entirely (links, orphans, stale hints — owner
notes never gate a commit); the always-on secrets floor still scans it, so it is
not a secrets-safe zone. A repo that doesn't want it just deletes it.

## Skills layer

*Referenced from PROCESS.md §7 "boundary notes".* **Applies when** a repo will be
worked by an AI agent (Claude Code, Gemini CLI, …) and you want that agent to load
this repo's repeatable procedures as first-class, on-demand **skills**. Skip it for
a repo with no agent — nothing here is required, and the gates never read a skill.

A **skill** is a small, focused capability — a procedure grounded in this repo's
actual commands and files — that an agent loads on demand to work faster and more
correctly. Skills are **opt-in accelerators, not process gates** (the
Proportionality doctrine applied to tooling): the gates, the traceability spine,
and the git/CI floor are the bar; a skill only helps an agent clear it. The full
contract lives in the kit's `skills/README.md`; the shape:

- **Neutral source → per-agent materialization.** The kit ships skills as
  agent-neutral `skills/<name>/SKILL.md` files. `bootstrap.py --agents
  claude|gemini|both|none` materializes the selected agent's skills into its native
  location (Claude Code `.claude/skills/<name>/SKILL.md`; Gemini CLI
  `.gemini/skills/<name>/SKILL.md`) — both read the same Agent-Skills `SKILL.md`
  frontmatter, so materialization is a straight copy. `none` (the non-interactive
  default) materializes nothing, preserving the agent-neutral scaffold; run
  interactively and bootstrap **asks**. `AGENTS.md` stays the canonical guide
  whichever agent is chosen.
- **The optional hook config is copied inert.** The chosen agent's
  `agent-hooks/*.settings.json` is copied as `settings.json.example`, **never** a
  live `settings.json` — the scaffold must not silently install a `Stop` hook that
  runs commands. Enforcement stays in git + CI (`agent-hooks/README.md`); activating
  the example is the user's explicit choice.
- **Applicability schema + generated index.** Each `SKILL.md` frontmatter carries
  `stacks`/`domains`/`phases`/`tags` (+ a `scope` of `kit` or `this-repo`) so a
  skill's fit is machine-readable. `scripts/gen_skills_index.py` regenerates
  `skills/INDEX.csv` (one row per skill) as the cheap scan surface, with `--check`
  as the freshness gate — the same "generated, don't hand-maintain" stance as the
  code map. At setup bootstrap asks up to three scope questions (stack? domain?
  binary/hardware?) and selects the `kit`-scope skills whose tags **intersect** the
  answers — a trivial set-intersection, no engine. The **metadata convention is the
  deliverable**, so a later tool can match/fetch smarter without redesign.
- **The per-agent copies are a checked, generated fan-out (S7).** `.claude/skills/`,
  `.gemini/skills/`, and `.agents/skills/` (Codex, `--agents codex`) are just
  different directories holding **byte-identical** copies of the one neutral
  `skills/` source — needed only because agent skill *locations* don't
  standardize. Materialization stays write-once (never clobbers project content);
  `bootstrap.py --sync` is the deliberate refresh that force-overwrites **only**
  each `<agent>/skills/<name>/` subtree from source (edit source → re-materialize
  in one command). `gen_skills_index.py --check-agents` is the **drift gate** —
  every per-agent copy byte-identical to source — wired into the pre-commit floor
  + G3 like the arch-map/OKF freshness steps: a drifted copy **fails** with a
  one-command fix, and it is vacuous for a repo with no neutral source or no
  per-agent dir. Only skills that a per-agent dir already carries are compared, so
  a scope-matched subset is fine. The copies are **tracked + gated** (the kit's
  idiom for committed generated artifacts — a fresh clone has working skills
  before setup runs). **Tenability constraint:** this verbatim fan-out holds only
  while **skill frontmatter stays agent-neutral**. The day a skill needs an
  agent-specific field, materialization gains a per-agent transform (map/strip
  fields) and the tracking model flips to **gitignore + regenerate-on-setup** —
  tracking *transformed* artifacts invites the hand-edits the kit exists to
  prevent. Deferred until a real need earns it.
- **Future external sources plug in here.** `skills/README.md` documents the
  contract (naming, the frontmatter shape, the neutral-source landing zone,
  trust/review) for how a later tool would fetch remote/community skills — they land
  in the same `skills/` source layout and materialize via the same path, never
  written straight into an agent dir bypassing the index.

## Trajectory / work-items layer

*Builds on PROCESS.md §7 (the harness contract + the offline-render
principle).* **Applies when** a project wants to track **how** its work executes —
cross-track order, which deliverable gates which, %-complete — as a
machine-readable registry, and/or a generated dashboard over it. Uniquely in this
file the layer is **opt-out, not opt-in**: it is on by default but **vacuous**, so
a repo that never adds a work item pays nothing (see the opt-out below).

**What it adds over the spine.** The `SN→SR→LLR→TC` spine answers *what must be
true*. It does not carry the **execution "how"**: the order work runs in, where
independent tracks meet, which task is in flight, how far along the whole is. A
**work item** (`WI-###`) fills that gap — a unit of *doing*, not of *truth*:

- it **delivers** one or more SRs (`SR-Refs`) — the thread back to the spine;
- it belongs to a **workstream** — a mutable grouping category of related work
  (`scripts`, `docs`, a subsystem). *Not* a "track": that word named the
  retired parallel-execution lane (this file, "Parallel tracks"; WI-210) — the
  legacy `Track` CSV header is still read as `Workstream`;
- it **depends on** predecessor work items (`Predecessors`) — the edges of a DAG.
  A bare id is a **hard** edge (a real technical blocker: drives readiness,
  ranking, and the acyclicity rule); a `~`-prefixed id (`~WI-013`) is a **soft**
  edge (advisory ordering — must resolve, never blocks, dashed in the render);
- it moves through a **lifecycle**: `queued → active → done`; `deferred` parks
  intentionally postponed work and `blocked` parks work on a named `BlockRef`.

A WI is the machine-readable *how* beneath an SR's *what*. Plans and discussion
retain the *why*; the registry complements rather than replaces that narrative.
Enabling this layer **supersedes the plan/build cadence's `docs/plan.md`**
("Unattended operation" → *Plan/build cadence*; WI-252): the WI DAG + specs
*are* the plan — one "what's next and how" surface, never two.

**Registry.** `docs/requirements/work-items.csv`, columns
`WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable,SpecRef`.
Off-spine and optional like `procurement.csv` / `assets.csv`: `trace.py` does not
read `WI-` ids — the trajectory tooling owns them. `Status ∈
{queued,active,done,deferred,blocked}`; `deferred` is queued-but-not-next, while
`blocked` requires the optional `BlockRef` column to name what must clear. An
unknown status lints. `SR-Refs` / `Predecessors` are `;`-joined id lists; the
`-000` example row is inert. A legacy CSV without `SpecRef` reads it as empty.

**Validation** — `check_trajectory.py`, wired as the `trajectory` gate step from
G2. Every `Predecessors` id (hard or soft) resolves to a real work item and the
graph is **acyclic over its hard edges** — both **errors** (a trajectory that
depends on itself can never start); a cycle that closes only through soft
edges is a **warning** (conflicting ordering hints, not a blocker); every `SR-Refs` id exists in the SR registry — a **warning**, since a
draft SR referenced ahead of its row is legitimate; `WI-###` id shape and
uniqueness — integrity, like `trace.py`.

**The SSOT model (registry-authoritative).** `status.md` and `work-items.csv`
used to compete — both carried work descriptions, and they drifted. The model
makes the registry authoritative: **the WI `Deliverable` is backward-only** (what
shipped) and the forward bridge is a per-WI **`SpecRef`** that lives while the WI
is open and clears at close. `check_trajectory.py` mechanizes three rules over the
registry (warn-first at the commit floor; `--strict` gates R-E/R-F at G2+):

- **R-A** — a WI's `Deliverable` is non-empty **iff** `Status = done`; an open WI
  (queued/active/deferred/blocked) has an **empty** Deliverable. A **hard error at every
  run** (no flag): a commit is the agent handoff point, so an incoherent WI state
  launches the next session into the wrong item. This is the pre-commit floor.
- **R-E** — every **open** WI has a non-empty **`SpecRef`** resolving to an
  in-repo target (`docs/specs/WI-###.md` or a `doc#anchor`; the path part must
  exist). Deeper anchor/path validation rides `check_doc_refs.py`'s path tier.
- **R-F** (WI-251) — the close side R-E leaves unstated: a **done** WI's
  `SpecRef` is **empty**, and every live `docs/specs/` file (scaffold
  README/`-000` exemplars excluded) is cited by ≥1 **open** WI — otherwise it
  belongs in `docs/archive/specs/`. Prose-only close ritual is skipped by
  autonomous agents; whether durable spec content was absorbed *before*
  archiving stays a reviewer-tier judgment (the honest gap).

A placeholder-only/absent registry stays vacuous for all three.

**Generated status (the integrator-owned snapshot; WI-180).** `status.md` is not
an agent resume surface authored session-to-session. Under parallel dispatch it
becomes an **integrator-generated reference snapshot** — regenerated only on the
integration branch after a successful integration and gated by generated
freshness (like `PROJECT_STATE.html`), never written on a worker branch. It
carries only: the derived gate/bar pointers; queued/deferred/blocked counts + a
link to the WI dashboard; pending `Needs <human>` items linked to
`open-items.md`; the last integrated train + integration-queue summary; and
project scope/constraints whose canonical homes are linked, not copied. The
former **R-B/R-C/R-D** rules — every open WI repeated as a token in `status.md` —
are **retired** (WI-180): a generated snapshot needs no registry copy to
cross-check, and the generator + its freshness `--check` land with the
dispatcher/integrator (the parallel-dispatch plan, §10, Slices D/F).

**The owner decision surface (`docs/open-items.md`) + the status-surface
lint.** The Needs-\<human> bullets in `status.md` stay **one-liners** (id +
one-line recommendation), or the blackboard re-bloats; the *depth* of each
pending decision — blast radius, options with pros/cons, the driver's
recommendation — lives in **`docs/open-items.md`** (scaffolded from
`OPEN_ITEMS.template.md`), one `## OI-N` section per pending decision, so the
owner reviews **one file with all context**. Lifecycle: a section lives there
only while pending — the ruling appends to `log.md`'s Decisions and the
section is deleted (`work-items.csv` = tracking, `open-items.md` = pre-ruling
analysis, `log.md` = post-ruling record; no third source of truth).
`check_docs.py` warns — **structure only, never the exit code** (content
quality is reviewer-class, and gate promotion is this layer's un-defer trigger
for a spine SR): **S-1** `status.md` over its line budget (default 120;
`docs/status-lint` overrides with an integer, `off` disables S-1..S-3);
**S-2** the Open-items marker must precede `## Scope`; **S-3** every
Needs-\<human> `OI-N` has a section in `open-items.md` and every section id
appears in `status.md`. S-3 is vacuous without `open-items.md` — the surface
is optional; delete the file to opt out.

**Spec-of-record (`SpecRef` + `docs/specs/`).** A queued WI whose only description
is its title is not implementable, and nothing used to check that an open WI named
a reachable spec. `SpecRef` fixes that: a spec-of-record lives in
[`docs/specs/`](specs/README.md) (a per-WI `WI-###.md`, or a shared
**multi-WI effort** doc addressed by `#anchor`) while the WI is open, and is **archived at
close** to `docs/archive/specs/` with the close date appended and the WI it was
attributed to noted (git keeps the history; the `Deliverable` + `log.md` carry the
summary). Every spec ships a **Done-when checklist**, so a half-complete WI's
frontier is its **first unticked box**, not prose discipline (ticks are transient
working state). A shared effort doc archives when its **last** open WI closes;
R-F (above) mechanizes both close-side halves.

**Specs act on declared interface boundaries (WI-191).** A spec whose WIs act
across a module boundary carries an **`## Interfaces` section** citing each seam
as an `IF-###` that resolves in `interfaces.csv` — the one seam home (§8), so a
spec never sketches its own near-duplicate. A **new** seam is filed as a
`Status=Proposed` row *at filing*, its citation naming the **nearest existing**
IF and why it does not suffice: the forced search is the anti-duplication
mechanism — search before you invent, because a seam defined before a second
consumer exists tends to be wrong, bypassed, and re-invented, so the rule forces
*search*, never early invention. Scope is §8's: seams *between* modules (or
repos/external actors), never intra-module ceremony — a single-module WI states
that in the section in one line and cites nothing, and single-module standalone
projects skip §8 entirely. **Mechanized** (`check_trajectory`, warn-first /
ERROR under `--strict`, **vacuous-until-armed** — only a spec carrying the
section is checked): every cited IF resolves, and a cited Proposed seam carries
a non-empty rationale. **The honest gap is reviewer-tier:** whether a rationale
truly names the nearest seam, and whether a Proposed contract near-duplicates an
existing one, is a judgment call (`check_dupes`' token windows work on code, not
contract prose) — recorded in `enforcement-audit.md` with a plan/spec
critique-rubric anchor (`docs/rubrics/spec-interface-hygiene.md` **B1**, which
WI-190's plan rubric imports).

**No-validation-delta warn.** A rework WI that addresses a prior failure but
changes neither the TC prose (`docs/test/test-cases.csv`) nor the test logic
(files under the declared tests dir) warns (`--staged`, warn-first): the same
failure can recur because the fix landed in the code, not the validation chain.

**Codename discipline (durable references).** Every durable reference in a
registry or spec is a `WI-`/`SR-`/`LLR-`/`TC-` id or an in-repo path — **never a
session-local codename**. Review-finding labels, phase nicknames, and
"the grind"-style shorthand belong in a `log.md` session entry (ephemeral
narrative), but not in `work-items.csv`, the SR/LLR/TC registries, or
`docs/specs/`: a codename resolves only by spelunking archived docs, while an id
or path resolves mechanically. This stays a **writing rule + reviewer-B
checklist item**, not a mechanical lint — a naive `[A-Z]\d+`-shaped matcher
would false-positive on `G3`, `SR-###`, and the like, so a narrow lint waits
until a real recurring pattern earns it.

**Phase cadence.** Any batch of spine-touching work headed for the same
re-attestation should land as **one phase** — batch the changes so a **single
owner sitting** covers each re-attestation, rather than paying for several. A
phase's spec is one shared `docs/specs/` doc with a `#anchor` per WI. **Its
cadence:** mid-phase WI sessions end at the **commit bar** (the pre-commit
hook floor + the project's test command + `check_docs --stale`), not the full
gate; the full `check.py --gate <gate>` runs **once at phase close** (the
coordinating close), and CI runs the gate job on every push regardless — a
mid-phase regression is still caught by the per-commit suite run. Test-impact
selection ("run only the relevant tests") is **rejected**: a missed transitive
dependency passes silently and the coverage floor breaks, so the sanctioned
cheap per-commit layer for a slow suite is the declared **smoke** tier
(`stack.ini [tiers]` — `pytest -m smoke` per commit, full tier at gates), not a
guessed subset. A WI's phase is **derived** from the delivery `Phase` of the SRs
it delivers (§4 "Phased delivery"), and the When-view dashboard tiers the WI DAG
by **phase ⊃ workstream ⊃ work-item** — there is no separate grouping column.

**Whole-registry contradiction audit (WI-206).** The per-commit reviewer sweep is change-scoped — it checks each new SN/SR/TC row against the whole registry as it lands (inductive pairwise coverage), but never re-audits **old-vs-old** drift between rows that both predate it. *Applies when* the registry is mature enough for that to bite (>= 2 closed phases or >= 30 SRs). *Occasion:* at **phase close** (with the gate bar) and **before G-Final**. *Execution:* one independent fresh-context session, redacted to the registries + `docs/rubrics/registry-contradiction-audit.md`, writing a recorded `docs/reviews/NNN-AUDIT.md` verdict. *Disposition:* findings route as WIs through change-intake; the audit never edits the spine. Per-commit coverage stays the change-scoped reviewer sweep — unchanged.

**Parallel test execution.** Running the suite across cores is a **`docs/stack.ini`
concern**, not a process rule: append `-n auto` to `[product] test` and the harness,
gate, and CI all parallelize with [pytest-xdist](https://pytest.dev). It is the
right lever for a slow suite because test-impact selection is **rejected** (above),
so the sanctioned speed-ups are the **smoke** tier per commit and **parallel
execution** at the gate. The kit's **template** ships the plain command with the
`-n auto` line **commented** — opting in is a knowing act, since a suite with
order-dependent or shared-mutable-state tests may not be xdist-safe (each xdist
worker is a separate process; only filesystem writes to shared, non-`tmp_path`
paths race — env vars and cwd are per-worker). A suite whose parallel wall time
still disappoints has one recorded, **not-yet-built** fallback lever: a
**session-scoped shared-scaffold fixture** (bootstrap one scaffold per worker
instead of per test). The kit's own meta-suite opts in (24 workers: ~377 s → ~65 s
plain, ~726 s → ~157 s with coverage; subprocess coverage holds per-worker,
combined total unchanged at ~91%).

**Dashboard** — `gen_trajectory.py` renders the root `PROJECT_STATE.html` (the
unified project-state artifact; formerly `docs/trajectory.html`), a generated
*view* (never a source of truth — the `gen_arch_map` / `trace.py` idiom). One
self-contained, **fully-offline** page (the §7 offline-render principle — no CDN,
no cloud tooling, no JS layout library): a project-vision header, definition- and
execution-completeness meters, an **SVG icicle** of the `SN→SR→LLR→TC` spine, and
a **layered SVG DAG** of the work items (ranked by dependency depth,
done/active/queued shaded), both computed in Python. Its `--check` is the
`trajectory-map` freshness gate at G3 — regenerate-in-memory and byte-compare,
exactly like the code map — so the committed dashboard can never silently drift
from the registry; the shipped pre-commit hook runs the same step at every
commit (vacuous for a non-adopter), so a registry edit that stales the
dashboard is caught locally, not first in CI. In `status.md`, the **Next action** then names the next
`WI-###`(s), and the dashboard shows where they sit in the DAG.

**Knowledge tab (consumes the OKF bundle).** When a committed `docs/okf/` bundle
exists, `gen_trajectory.py` gains a **Knowledge** tab: the OKF concepts as a typed
graph (nodes fill-keyed by `type`, directed `SN→SR→LLR→TC` edges parsed from the
bundle's link lists), laid out by the same Python layouter as the WI DAG. This
makes the dashboard the bundle's **first real consumer** — the middle-path
embedding (ruling): the detail panel embeds each concept's one-line
**description** and **links out** to its `docs/okf/<tier>/<id>.md` for the full
body (which sits beside the artifact). It stays a *view* — the registries are the
truth and the bundle is itself generated — so the load stays deterministic (no new
`--check` exclusion). **Omitted without a bundle**, so a bundle-less repo renders
byte-identically to before the tab existed. Because the dashboard now reads the
bundle, the regen order is **arch-map → okf → trajectory** (a stale bundle would
bake stale knowledge into the dashboard); the pre-commit hook reports `okf`
freshness *before* the dashboard's for the same reason.

**Opt-out (why a non-adopter pays nothing).** The layer ships **present but
vacuous**: a fresh scaffold carries only the inert `WI-000` placeholder, so both
`check_trajectory.py` and `gen_trajectory.py --check` pass **vacuously** (no work
items → nothing to validate, nothing to render, no `PROJECT_STATE.html` written). A
repo that wants the layer gone entirely silences it with the one word `off` in
`docs/trajectory-check` — the same first-line-parse toggle as `docs/secrets-scan`.
The cost to a project that ignores the layer is therefore exactly zero, which is
why it ships opt-out rather than opt-in.

## Commit identity & privacy

*Enforced by `.githooks/pre-commit` (author + content lint), `.githooks/commit-msg`
(message lint), and `.githooks/pre-push` (review backstop); advised by
`scripts/setup.{sh,ps1}` (the PROCESS.md §7 process floor).* **Applies when** a
repo wants to keep a real, contactable identity out of its published commits. A
repo without the concern leaves the gate off and pays nothing.

**Identity is not privacy — separate them.** Two concerns hide under "commit
identity", and conflating them is a design trap:

- **Attribution-identity** — *which account* authored a commit. That is the
  user's own `user.name`/`user.email`; it belongs in **per-clone git config**,
  not pinned by the repo. A handle or no-reply address attributes a commit
  without being a route to a person.
- **Privacy (PII)** — whether a *real, contactable person* leaks into the
  history: a personal email as author or in content, an absolute path carrying
  the OS username, the machine's global git identity in a doc, a bio detail.
  This is what the repo defends.

An earlier design put both on one value — an email **glob** that was at once the
author *pin* and the content *allowlist* — so loosening the allowlist to admit a
tool's co-author trailer collaterally loosened the identity pin. The current
design keeps them apart: **identity stays in git config; the repo runs a privacy
gate.** Git still stamps author/committer from `user.name`/`user.email` (the
machine's global config unless the clone overrides it), and fixing attribution
after a push is a history rewrite — so the gate checks the identity *actually
configured* rather than pinning one, and the highest-risk shape (an unattended
run committing many sessions under a private identity) is a preflight failure.

- **The toggle `docs/privacy-check`** (one value, tracked, like `docs/gate`):
  `true` runs the privacy gate at every boundary below; `false` / absent = off,
  zero cost (the successor to the old `inherit`). It declares *intent* only and
  is safe to publish. Set it at repo creation (`bootstrap.py --privacy-check
  true|false`, the cheap moment) or adopt later. Deliberately **repo-wide** — the
  gate constrains every contributor equally.
- **The exempt-email allowlist lives in code**, not the toggle:
  `scripts/check_privacy.py` holds `EXEMPT_EMAILS` — the addresses that may
  appear as author or in content without flagging. The shipped default is
  `*noreply*` (any no-reply-form address: a no-reply mailbox carries no
  contactable person, so it is not PII — even though it may carry an attribution
  handle, which makes this a PII-risk *reduction*, not an anonymity *guarantee*).
  A commented tight enumerated list (`*@users.noreply.github.com`,
  `noreply@anthropic.com`, …) sits beside it for an exact-match posture. RFC 2606
  example domains are always exempt.
- **`scripts/setup.{sh,ps1}` advise, never pin:** setup no longer sets a
  repo-local identity (that is the user's own git config). When the gate is on
  and the clone's author email is not exempt, setup **warns** (via
  `check_privacy.py --author`) that commits will block, pointing at a no-reply
  fix. Enforcement is the hooks, not setup.

**Secrets floor (every repo).** Distinct from the privacy layer below and
**not gated on it:** `scripts/check_privacy.py` always scans for private-key
headers and universal credential shapes (GitHub, Slack, AWS, `sk-…` keys) — the
security net an ordinary identified project gets too, because a committed key is
a leak regardless of who authored it. It runs in the same modes as the privacy
lint (staged diff at pre-commit, the commit message at commit-msg, `--repo` at
every gate, `--range` at pre-push), in **all** repos, privacy-check on or off.
Opt out with the one word `off`
in **`docs/secrets-scan`** (one-word declared policy, absent = on) — the
deliberate exit for a repo whose content *is* secret-shaped; mark individual
false positives with the inline `privacy-ok` marker first and reserve `off` for
a repo that drowns in them. Still a pattern floor, not a DLP product — deep
secrets scanning stays the named external category (gitleaks, trufflehog),
never rebuilt in the kit. *Adoption note:* a repo that had no scanning starts
failing on a committed token when it takes this kit version — that is the point,
and `off` is the escape (ADOPTING.md §6).

**Content & message privacy (privacy-check on).** The author field is the
smaller leak surface; **content and commit messages** are the bigger one — an
absolute path carrying the OS username, the real identity from global git config
pasted into a doc, an email in a test fixture, a bio detail in a README, an
address in a commit-message trailer. These **privacy** classes run only when
`docs/privacy-check` is `true`; a privacy-off repo pays zero for them (the
secrets floor above still runs).

- **Layer 1 — deterministic lint, per commit.** `scripts/check_privacy.py`
  (stdlib) runs the high-confidence *privacy* classes: the commit **author
  email** must be exempt (`--author`, a private author blocks); home-dir path
  shapes carrying an OS username, the current account/hostname, **non-exempt
  emails** (not in `EXEMPT_EMAILS`), and the global-git-config identity in
  content (the always-on secrets floor above scans alongside). Wired into
  `.githooks/pre-commit` for the author + **staged diff**, and into
  `.githooks/commit-msg` (`--message`) for the **commit message** — pre-commit
  runs before the message exists, so the message went unscanned until push,
  which let leaks in trailers pile up across commits; the commit-msg hook blocks
  them at the first commit. `--repo` sweeps every tracked file as a `check.py`
  process step at every gate (catching what slipped in before the gate was
  enabled or past `--no-verify`); `--range` scans a commit range *as history* —
  diffs, messages, author lines — for the pre-push floor and the sync scrub's
  base pass. A documented example line carries the inline `privacy-ok` marker to
  be exempt — mark false positives instead of training yourself to bypass the
  hook.
- **Layer 2 — LLM review at the push boundary.** Publication is where a leak
  becomes harmful and effectively unrecallable, so the **judgment** layer sits
  there — its *primary home* is the sync ritual's scrub step ("Agent iteration
  branch & sync" above), which is structural and fails closed. The optional
  backstop for direct-to-dev-branch edits is `.githooks/pre-push`: it reviews
  the **full outgoing range** — diffs *and* commit messages, so a leak added
  in one commit and removed in a later one is still caught — via the
  **`REVIEW_CMD`** slot (the `AGENT_CMD` family: env var, or per clone
  `git config privacy.reviewcmd`), a fresh-context subagent with a tight brief
  (hunt PII; APPROVE/BLOCK + findings; verdict appended to `docs/log.md` per
  PROCESS.md §5 extended with `Model:` + `Role: PRIVACY-REVIEW`). When the
  policy demands review but the reviewer can't run, the hook **fails closed**
  — a missing tool is never a pass at the one boundary that matters. One
  **declared opt-down** exists for the adopted-but-not-wired-yet window: track
  the word `warn-unwired` in **`docs/privacy-review`** (one-word declared
  policy, absent = require) and an *unwired* reviewer warns instead of
  blocking, leaving the deterministic lint as the floor — a recorded,
  reviewable decision, never a silent default, and it softens *only* the
  unwired case (lint findings and a wired reviewer's BLOCK still block; the
  hook's failure message names this escape at the moment it fires). Honesty:
  hooks are per-clone and tool-circumventable, and `git push --no-verify`
  remains git's own escape hatch for a human; that is why the primary home is
  the branch structure, not this hook. Cost note: review runs **per push**,
  never per commit — an LLM call in every commit would tax the commit-often
  cadence into batching, which is worse for privacy *and* review.
- **Process rule (agent-driven work).** The driver routes privacy findings
  like consistency findings (PROCESS.md §5); an unattended coordinator runs
  the same review before any push step its policy allows and refuses on
  BLOCK. The reviewer runs under the user's own agent account — the same
  trust domain as the driver; no third-party service is introduced.
- **Remediation.** Caught pre-push = the leak exists only in **local**
  history: rewrite it before it publishes (interactive rebase, or a history
  filter tool — the `git-filter-repo` category). Already published = **treat
  as disclosed**: rotate the credential / react to the exposure; a rewrite of
  published history is cosmetic, since mirrors and caches already have it.
  Binary assets carry EXIF/author metadata the lint cannot see — strip on
  ingest ("Binary assets" below).

**The honest boundary.** The guard covers **future commits in clones that ran
setup** (or otherwise enabled the hooks). It cannot (a) fix **existing
history** — that is a rewrite, out of scope (ADOPTING.md §6 notes the
migration); (b) constrain a clone that never enabled the hooks and commits or
pushes with other tooling; (c) deliver full **anonymity** by itself — that is a
stricter goal *beyond this gate's scope* (the gate keeps **PII** out, not
"unlinkable authorship"). Structural anonymity is a posture a repo layers **on
top** — the tight enumerated `EXEMPT_EMAILS` list, the scrub ritual, and an
anonymous **hosting account** — and it also depends on keeping machine-local
paths/usernames out of **committed text**, which the content lint *patterns
for* and the reviewer *judges* but neither can guarantee: the lint is patterns,
the reviewer is probabilistic, and this is not a DLP
product. The trust footprint stays visible instead of pretended away.

## §8 purchased parts

*Referenced from PROCESS.md §8.* **Applies when** the product incorporates
**purchased/external parts** it buys rather than builds (motors, arms, cameras,
compute boards) and wants their status and source tracked in-repo.

**One row per bought part, owned by an interface row.** A purchased part that *no
repo builds* still has a contract of record — its datasheet, vendor, pinned
version — and §8's rule already places that: a **coordinator/repo-held `IF-###`
row is the owner-of-record** for such a part (MULTI_REPO.md §3.3). The
`procurement.csv` registry (`PART-###`) sits **alongside** that, adding only the
**acquisition** facts the interface row doesn't carry: `PART-ID, Name, IF-Ref,
Vendor, Cost, Status, Quantity, Notes`, where `IF-Ref` back-links the owning
`IF-###` and `Status ∈ {needed, ordered, on-hand, backordered, obsolete}`. Off
the `SN→SR→LLR→TC` spine and optional like `interfaces.csv`/`PB-###`: a project
that buys nothing ignores the file; a leftover `PART-000` never blocks a gate.

- **What `trace.py` checks (integrity only).** It flags a malformed/duplicate
  `PART-` id, the always-on floor. It does **not** resolve `IF-Ref` against
  `interfaces.csv`, because trace.py never reads the `IF-###` tier (it is off the
  joined spine, §8); keeping PART integrity-only holds the "no more than PB"
  minimal line and avoids teaching trace.py the interface registry. Cross-checking
  `IF-Ref` against a real interface row is a natural first extension if it earns
  its keep.
- **Deliberately minimal — deferred extensions.** This is a flat parts list, not a
  bill of materials. **Full BOM tracking** — alternates/second-sources,
  per-module allocation and quantity roll-ups, assembly trees, lead-time/reorder
  logic — is **explicitly deferred**; add it only when a project demonstrably
  needs it, extending this registry rather than replacing it.

## Binary assets

*Referenced from PROCESS.md §8 "Binary assets".* **Applies when** a project ships
unavoidably-binary deliverables — game art, music, voice acting, video, rendered
CAD, publication artwork — the kind of asset that can't be line-diffed or
mechanically verified.

This is the Proportionality doctrine's *"track about the asset in text"* stance
(this file, "Proportionality doctrine" (a)) made operational. The asset itself is
binary; the **record of it** is text, tracked, and reviewable.

- **Manage the binary as a pointer + manifest, not as a blob in the tree.** Store
  the asset in **git-LFS** or an **out-of-repo store** (an object store, an asset
  server) and keep, in the repo, a **manifest row** that points at it and pins its
  identity: the optional `requirements/assets.csv` registry (`ASSET-###`). This
  keeps the git history diffable and the checkout small while the manifest stays
  the change-tracked source of truth *about* every asset.
- **Columns (what to track *about* an un-diffable asset).** `ASSET-ID, Name,
  Refs, Kind, Provenance, License, Attribution, ContractRef, Location, Hash,
  Version, Notes`. The load-bearing ones:
  - **`Provenance`** = `human-made | ai-generated | mixed`. Real-world driver:
    distribution platforms (e.g. **Steam**) require **AI-content disclosure**, so
    the provenance of every shipped asset must be recordable and auditable, not
    guessed at release time.
  - **`License`** (SPDX id or `proprietary`) and **`Attribution`** (any required
    credit line) — so a licence obligation can't be lost between acquisition and
    ship.
  - **`ContractRef`** links the **voice-actor release** or **commissioned-work
    agreement** that grants the right to ship the asset — the paperwork a purely
    binary asset would otherwise carry no trace of.
  - **`Location`** is the **pointer** (git-LFS path or store URL); **`Hash`**
    (e.g. `sha256:…`) + **`Version`** make that pointer **verifiable** — you can
    confirm the bytes on the store match the row even though you can't diff them.
  - **`Refs`** back-link the SR/LLR the asset realizes, keeping it on the spine's
    high-altitude thread (usually an `Attest` SR — this file, "Proportionality
    doctrine" (d)); `trace.py` integrity-checks the `ASSET-` id only, off-spine
    like `PART-###`.
- **Privacy advisory:** binary assets carry **EXIF/author metadata** (camera
  serials, GPS, creator names) that no text lint can see — on a privacy-checked
  repo ("Commit identity & privacy" above), strip metadata **on ingest**,
  before the asset reaches the store or the tree.
- **Registry choice — a sibling registry, not a widened `procurement.csv`.**
  Procurement (`PART-###`) tracks parts the project **buys** (owner-of-record is
  an `IF-###` interface row; columns are vendor/cost/status/quantity). A created
  or commissioned **digital asset** is a different concern — license, provenance,
  release paperwork — so it gets its own minimal registry rather than overloading
  procurement's columns with fields that don't apply to a motor, or forcing an
  asset row to fake a vendor/cost. Same off-spine, integrity-only, optional
  pattern; different subject.
- **Deferred product-layer idea — the "asset manifest freshness check."** A
  natural next step is a tool that verifies each `ASSET-###` row against its store
  — the pointer resolves, the `Hash` still matches, no manifest row is orphaned
  from its file and no shipped file is missing a row. This is a **product-layer,
  project-owned** check (it must reach a git-LFS or object store — outside the
  kit's stdlib, offline, no-network line), named here and **deliberately
  deferred**, in the **same family as the Thread-16 CAD/non-code-artifact
  verification stub** (render-on-change, visual diff, design-rule checks): the kit
  **names and routes** these, the project **wires** them, the gate **records** the
  verification (the meters-vs-comparator split, PROCESS.md §9). Until then the
  manifest is the honest, text-tracked record — an ideal reached for, not a check
  faked.

## Intra-repo interfaces & the architecture graph

*Builds on PROCESS.md §8 (the seam registry).* **Applies when** a repo has more
than one module and wants its architecture view to show **how the modules
connect** — the seam the AXES ratification sanctioned ("a cross-component edge
without a declared interface is a finding"). §8 records a shared surface once as
an `IF-###`; the same registry serves an **intra-repo** seam (module→module,
module→file, module→external-actor) exactly as it serves a cross-project one — one
`interfaces.csv`, two uses.

**The model — one row per directed seam.** `ThisProject` = the module path;
`Counterpart` = another module, a **file path** (giving module→file→module
dataflow, so a shared file like `docs/stack.ini` is a hub node many modules
Consume), or an **external actor** (`downstream adopter`, `git`, `agent CLI`);
`Direction` = Provides/Consumes; `Contract` = one testable line (CLI flags + exit
codes, or the file schema); `SR-Refs` links the spine so every seam is
transitively TC-covered. `trace.py` integrity-checks the tier (id shape, the
SR-Refs back-link under `--strict`, a best-effort `ThisProject`↔`LLR.Module`
advisory) — WI-056 closed the SR-002-era gap where trace never read the IF tier.

**Opt-out, default-on (ruled).** By default a contract IF must define how the
architecture connects, so the **coverage warn runs even when `interfaces.csv` is
empty or absent**: a multi-module arch-map with no declared seams reads
**"connectivity undeclared"** instead of passing vacuously, and the How-SW panel
stays a bare module list — the organized graph is *earned* by declaring seams.
`check_trajectory.py` runs this at the hook and the gate, **all warn-first** (it
never changes an exit code). A repo with genuinely nothing to declare silences it
with the one word `off` in `docs/interfaces-check` (the
`trajectory-check`/`okf-export` idiom — no file is scaffolded; absence reads on);
a single-module inventory is vacuous. The warns: every arch-map module is a
declared IF endpoint; each `Active` seam is cited by ≥1 TC; a `Contracts: IF-###`
docstring line (harvested into the arch-map like `Implements:`) matches the
registry.

**The honesty valve.** A pure **source** (produces output, consumes nothing) or
**sink** (consumes, produces nothing) would otherwise breed a boilerplate
opposite-direction row. Mark it instead: make the `Notes` cell of one of that
module's IF rows **begin** with the word `source` or `sink`, and the
missing-direction warn for `ThisProject` is suppressed.

**The graph.** When real seams exist, `gen_trajectory.py`'s How-SW panel renders
them as a directed graph (module / file / external-actor nodes, IF-labeled edges,
reusing the WI-DAG layouter) above the symbol table, and `gen_arch_map.py` merges
module↔module seams into the dependency diagram as distinctly-styled dotted edges.

**Risk — the maintenance surface.** A fully-declared repo is ~30–35 hand-authored
IF rows whose `Contract` text has **no mechanical oracle** (a renamed flag the row
misses). The joins bound the rot to that one column; CLI contracts are already
pinned by the never-break-downstream rule. Declare seams because the connectivity
view earns its keep, not for completeness — and lean on the source/sink valve so a
pure sink doesn't cost a row.

## Research track & knowledge packs

**Applies when** research findings must outlive the session that produced them,
or a specification rests on a load-bearing unknown. This is an optional WI
shape and durable prose home, not a new gate, run phase, or source of
requirements.

**A knowledge pack** is one hand-owned `docs/knowledge/<label>.md` topic. It
holds findings with evidence and retrieval dates, decision rationale,
vendor/tool quirks, and failed approaches. It never restates an SR/LLR/TC/IF
row or generated view: link the id instead. When a finding hardens into a rule,
constraint, or requirement, promote it through §5 change intake; the pack keeps
the why and trail while the spine keeps the what. Packs are advisory and never
gate. A component associates durable module knowledge through its `Knowledge`
refs and optional `DetailDoc`; `trace.py` resolves `docs/knowledge/`-shaped refs
warn-first.

**A research track** is an ordinary `WI-###` row with `Workstream=research`.
Its Done-when names the questions to answer, and its deliverable is a knowledge
pack and/or specification input — never code. It rides the `BuildTier` column
and the review dial with no coordinator changes. Set it
`strong` when synthesis needs a strong coordinator; that coordinator may
delegate directed gathering to quick/medium subagents when the project's
subagent policy permits, but retains source verification and the verdict.

The existing review round becomes a **grounding review**: verify that
load-bearing sources exist and support the claims, retrieval dates are present,
and repo facts match the repo. If source access is unavailable, label the claim
ungrounded rather than silently passing it. Cross-family review is recommended.
Research may be filed at PLAN/spec time as a predecessor to dependent work, or
at intake when the question is clearer than the requirement; both entry points
are optional under proportionality.

**Iterative optimization at WI scale.** Before spending a refinement budget,
write a small search card: candidate representation + constraints, objective +
guardrails, meaningful diversity axes, evaluation/noise protocol, initial
sampling + promotion rule, and stop rule. Construct a conventional optimizer
when variables are explicit and bounded and the objective is stable,
repeatable, and affordable to sample; use LLM iteration when representation or
evaluation is irreducibly semantic; use a hybrid only with an explicit boundary
between machine-owned variables/metrics and model- or human-owned judgments.
Start with random/diverse sampling and preserve a small elite-plus-diversity
archive before adopting a specialized search method. A critique-budget dial is
a resource ceiling, **not convergence**: stop separately on success, a
predeclared practically-insignificant plateau, stability within evaluator noise,
budget exhaustion, or an invalid/drifting search. Record best-so-far, diversity,
evaluation cost, and the stop reason. Algorithm evidence and selection cautions
belong in a knowledge pack; optimizer code remains project product work.

## Component layer

*Referenced from the registry templates (`components.template.csv`).* **Applies
when** a project wants a durable home for **set-grained knowledge and lifecycle**
— a subsystem, an assembly ("the left arm"), a software package group — that no
finer tier can hold: an `IF-###` is one seam, a workstream is mutable by design,
an LLR *is* the WHAT being rewritten. The registry is optional and off-spine
(procurement/assets posture): a scaffold ships only the inert `CMP-000` row, and
a repo that never names a component pays nothing.

**The row is deliberately slim** —
`CMP-ID,Name,Category,Knowledge,State,SupersededBy,PartOf,DetailDoc,Notes` — and
holds **only what a tag can't**: the knowledge refs (`;`-joined skill names,
`docs/knowledge/` labels, URLs), the lifecycle
(`State ∈ planned|built|verified|has-gap|deprecated`, with `SupersededBy` naming
the successor so identity survives a rewrite), nesting (`PartOf`), and an
optional `DetailDoc`. `Category` is an open value set (`software`, `physical`,
…).

When findings need to outlive the session that produced them, use the
"Research track & knowledge packs" layer above; the CMP `Knowledge` cell is the
durable component-to-pack association, not a second copy of the findings.

**Structure is derived, never restated.** Membership lives on the **primitive**
rows: LLR / IF / ASSET / PART each carry a `Component` cell (`;`-joined CMP ids
— tag at the *finest* enclosing CMP; coarser membership derives through
`PartOf`). From those tags everything else is a **view**: an interface with both
endpoints inside a CMP is *internal*; with one endpoint inside it is the CMP's
*boundary* — "the component **is** its interface set" as a derived
characterization, never an authored list. A CMP row therefore has **no**
`Realises`/`Interfaces`/`Assets` columns, and a one-member CMP with no internal
IFs is legal.

**What the kit checks** (`trace.py`, when real CMP rows exist): `CMP-` id
integrity; `PartOf`/`SupersededBy` resolve to real CMP ids; and every primitive
`Component` tag resolves to a real CMP row (the membership join — checked on
all four registries `trace.py` reads: LLR/IF/PART/ASSET).

**A cross-component edge needs a declared seam** (WI-064 — the AXES
enforceability rule, mechanized for software). `check_trajectory.py` joins the
committed arch-map's `Imports (internal):` lines with the `Component`-tag
membership and `interfaces.csv`: an import edge between two *different*
components with no IF row covering the module pair (either endpoint direction)
is a finding — **WARN** at the plain/hook run, **ERROR under `--strict` (G2+)**
— sharing the `docs/components-check` opt-out. Vacuous when any input is absent
(no imports lines, no real CMP rows, an untagged endpoint), so a non-adopting
or small repo pays nothing. A *physical* repo's cross-CMP discipline stays
gate-attested (`Inspection`) — the import graph is the software mechanization.

**The How-SW top view is bounded** (WI-073/FB5). The software-architecture panel
of `PROJECT_STATE.html` shows at most **ten** first-view items — the **top-level**
components (a CMP with no `PartOf` that contains an arch-map module) plus any
**uncontained** module (one with no `Component`-tagged LLR). Exceeding the bound
is a `check_trajectory.py` finding — **WARN** at the plain/hook run, **ERROR
under `--strict` (G2+)** — so an unreadable module map drives *right-sizing of the
component designations* instead of being tolerated. In the render, software items
are **containerized** into the component they belong to; expanding a component
reveals its members (and nested components) and the seams internal to it, while
interface seams that cross a component boundary aggregate to **one** deduplicated
component-to-component edge at the top level. Membership is the same
`Component`-tag join (`LLR.Module → CMP-###`); nesting via `PartOf` counts a
module only at its top-level root. The rule is **opt-out, default-on** like the
connectivity coverage — silence it with the one word `off` in
`docs/components-check` (no scaffolded file; absence reads on) — and **vacuous**
below the bound: a repo with ≤10 modules, or no arch-map inventory, passes
trivially (the bound, not the registry, is the rule), so a small or non-adopting
repo is never broken while a 20-module repo is *supposed* to feel it. (A CMP's
`Category` routes the render: `software` components fill the containerized How-SW
top view, other categories the How-physical table.)

## §9 NFR checklist

<!-- profile: nfr -->
*Referenced from PROCESS.md §9.* **Applies when** deciding which non-functional
concerns a project must consider at G1.

**Consideration checklist (a prompt, not a mandate — don't wear a hat the scope
doesn't need).** At G1, consider which categories apply and route each to a home
(anchor: the **ISO/IEC 25010** product-quality model):

- performance efficiency (time, throughput) and resource use (RAM/VRAM, disk);
- reliability / availability / recoverability;
- **security** (authn/authz, data protection, secrets, audit, dependency /
  supply-chain) — the kit ships a deterministic **secrets floor** for committed
  credentials in every repo (see "Secrets floor (every repo)" above); deeper
  scanning (gitleaks, dependency audit) stays a project-wired external category;
- **observability / operability** (logging, metrics, tracing, health — also the
  prerequisite for *measuring* any of the perf budgets);
- scalability / capacity; compatibility / interoperability;
- portability / installability (incl. artifact size); compliance / legal / licensing;
- safety (cyber-physical); data integrity / durability;
- **cost / economics** (unit/BOM cost, licensing fees, cloud spend; for hardware
  scopes also procurement / supply-chain). Note 25010 is a *software-quality* model
  and omits cost entirely — these systems-engineering categories sit **alongside**
  it, and a quantitative cost budget is just a `PB-###` row (metric-agnostic:
  `Metric=Unit BOM cost, Unit=USD, Direction=lower-better`), compared by
  `check_perf.py` like any RAM budget. No new mechanism.

The kit already covers some — **don't double-prompt**: maintainability (= the core
discipline), usability (= the end-user lens), basic fault tolerance (= the
edge-case table and the SN edge cases), cross-project contracts (= `IF-###`, §8).
<!-- /profile -->

## §9 perf comparator

<!-- profile: nfr -->
*Referenced from PROCESS.md §9.* **Applies when** a project has captured `PB-###`
budgets it wants tracked over time.

A captured budget is inert until something compares the *measured* number against
it. That comparison answers two distinct questions per metric: **absolute** —
"worse than the budget?" (measured vs `Budget`, per `Direction`) — and
**regression** — "suddenly much worse?" (measured vs a committed baseline, outside
the `Tolerance` band). The work splits along the §7 **process/product** line:
*measuring* a metric is **product** work the project wires (`/usr/bin/time`,
`tracemalloc`, `nvidia-smi`, a size command, `pytest-benchmark`/`hyperfine`),
emitting a `docs/test/perf-metrics.json` map of `PB-ID → number`; *comparing* is
**process** work the kit owns — `check_perf.py`, stdlib-only and metric-agnostic
(arithmetic over JSON). The kit owns the comparator; the project owns the meters.

- **Three artifacts, three reviewability classes (§3):** `performance-budgets.csv`
  is the tracked source of truth; `perf-baseline.json` is a **committed golden**
  updated *deliberately*; `perf-report.md` is a **gitignored composite** (current
  vs baseline vs budget + deltas), regenerated each run and published by CI.
- **Baseline-as-golden protocol.** Accepting a regression = committing a new
  `perf-baseline.json` **in the same PR**, so the number move is explicit and
  reviewed — never silent (the same discipline as the coverage threshold and
  phase-deferred SRs). `check_perf.py --update-baseline` rewrites it from the
  current metrics for exactly that purpose.
- **Warn-first; start with the deterministic metrics (honest-gate rule, §4).** The
  per-row `Gate` decides fail-vs-warn and `Tier` decides *when* a row is in scope:
  gate the **low-noise, deterministic** metrics (artifact/binary size, dependency
  count) at `full`; default **noisy runtime** metrics (latency, peak RAM, VRAM,
  throughput) to `Gate=warn` at `release`, with tolerance bands and same-runner /
  best-of-N measurement. A number that can't be a reliable `Test` gate is
  warn-tracked or `Demonstration`, never faked into a binary gate. A budget with no
  measurement this run is skipped, like a missing tool — absent metrics never fail.
<!-- /profile -->

## §10 several modules, one repo

<!-- profile: multi-module -->
*Referenced from PROCESS.md §10.* **Applies when** a repo grows distinct
sub-systems that still build and release as one (rung 2 of the scale ladder).

**No new machinery, just partition the spine.** A multi-module repo is the *same*
spine, grouped by columns that already exist: the LLR **`Module`** column and the
optional **`Area`** tag on SR/TC (§1 "Domain hats"). Each module is a sub-tree of
`SN→SR→LLR→TC`; where a module needs its own discipline it gets its own **domain
hat** owning that slice (§1 already allows this). The repo still builds, gates, and
releases as a whole.

- **Module-scoped review is a convention over the existing columns, not a new
  flag.** A module owner reviews their slice by filtering the registries on
  `Area`/`Module` (a grep or spreadsheet filter); the **repo-level gate stays the
  source of truth** — `trace.py --strict` still requires **0 orphans across the
  whole repo, seams included**. The kit deliberately ships **no**
  `--module`/`--area` filter on `trace.py`/`check.py`: a per-module gate would
  either hide the cross-module seams (a false "green" masking exactly the
  integration gaps this method wants first-class) or need real machinery to tell a
  legitimate seam from an orphan. The whole-repo gate already spans every module;
  per-module *ownership* is a reading convention, not a gate of its own.
- **Integration TCs for the seams.** A module boundary is where two parts must
  agree, so it gets its **own** TCs — not merely each module's internal unit tests.
  These are integration/system-level, usually `Tier=Full` or `Release` (§4 "Test
  tiers"), so the seam is a tested contract rather than an untested gap between two
  individually-green modules.
- **`IF-###` applies *within* a repo, too.** The interface registry (§8) is not
  only for separate repos: two modules in one repo that share a contract record it
  as an `IF-###`, with the counterpart naming the **other module** instead of
  another repo and both rows living in the one `interfaces.csv`. Same
  direction/owner/version/stability discipline, same "one contract, one home,
  backed by a test" rule — applied to the internal seam, with no cross-repo build
  machinery.
<!-- /profile -->

## Parallel tracks (multi-lane operation)

*Builds on PROCESS.md §10 (several modules, one repo) and the "Unattended
operation" / "Agent iteration branch & sync" layers above.* **Applies when** one
repo needs **more than one driver working at once**. The answer is the
**parallel dispatcher + explicit worker assignments** below — the earlier
*track-lane* machinery (`--track`, per-lane `docs/tracks/<name>/` copies of the
coordination files, per-track ID blocks) is **retired outright (WI-210)**: it
split the judgment duties across two control philosophies and forced every
safety guard to be wired per-path. A repo with one active line of work still
pays nothing — a plain launch with the queue holding one ready WI simply runs
one worker.

**What stays repo-singular (integrator-owned, never forked per lane):** the one
`SN→SR→LLR→TC` requirement spine and every registry, `docs/gate` + `gate-policy` +
`push-policy` + `privacy-check` + `guardrails-policy`, the root `status.md`/`log.md`,
`AGENTS.md`, and the generated code map. The spine is **deliberately singular**
(§10): `trace.py --strict` still demands **0 orphans across the whole repo, seams
included** — a per-lane gate would hide exactly the cross-lane seams this method
wants first-class. Workers **propose**; the **integrator lands**. Three of the
old track disciplines survive as dispatcher rules: **registry rows land at
ratification through the integrator** (a worker never edits the registries
mid-flight — its filed drafts land at integration), **generated artifacts are
never text-merged** (a conflict is resolved by regenerating on the composed
tree), and **cross-module contracts are `IF-###` rows** in the one
`interfaces.csv` with an integration TC backing the seam.

**Gating stays single-gate; per-train maturity rides `Phase` tags.** Keep **one**
`docs/gate` for the repo ("Phased delivery" above): Verified is required only
where a phase has actually built, and everything else is listed
**phase-deferred** — the explicit, recorded exemption, never a silent skip.

**One coordinator per checkout.** A **per-worktree lock**
(`out/agent-loop.lock`) refuses a second coordinator in one checkout (the
double-launch / cron-overlap collision): a **kernel advisory lock**
(`flock` / `LockFileEx`) the OS grants atomically and releases when the process
exits *or crashes*, so a dead run never wedges the next one — there is no stale
pid file to reason about. Cross-host on a shared filesystem is best-effort only
(`flock` over NFS is unreliable): the lock guards one checkout on one host, the
case that matters. The dispatcher, each worker (in its own worktree), and an
`--interactive` sitting all take it.

**Worker assignment (parallel dispatch) — the tracks successor.** The
dispatcher-era coordinator replaces long-lived tracks with **explicit worker
assignments** (`--wi "WI-###[;…]" --train <id> [--worktree <path> --base <sha>
--rework <file>]`): one dispatcher-assigned traincar built on branch
`llm/train/<id>` in its leased worktree. A worker has **no lane files** — it
never reads or writes `run-state`/`status.md`/`pause` and never regenerates
generated root artifacts (integrator-owned); its prompt is assembled from
`AGENTS.md` + the WI row + its SpecRef + predecessor context + the current
train diff + any rework finding (never a `status.md` resume), and its **result
is committed evidence**: each WI's final commit carries `WI:`/`Train:`/`Base:`
trailers (a blocker commits `Blocked-WI:` + `BlockRef:` instead; exit 3). Its
session logs (`docs/iteration/<train>-NNN-*.log`) and review verdicts
(`docs/reviews/<train>/NNN-<PHASE>-<sha7>.md`, naming the **exact reviewed
commit**) are train-scoped so parallel workers never collide at integration.
A traincar is **one review scope**: the policy-required review round fires
once, after the *last* constituent commits, over the combined train diff —
intermediate constituents are accepted-on-train, not reviewed, and **no
constituent becomes `done` until the whole train integrates**. Before each
successor the continuation conditions are re-checked; a positive classifier
conflict ends the train early (exit 10) and the dispatcher **transactionally
releases the unstarted constituents' reservations** (built and blocked ones
keep theirs as integrator evidence).
`--track` is **gone** (WI-210): the flag, its lane files, and the per-track
branch guard were retired with the serial driver; the worker assignment above
is the only lane concept.

**The parallel dispatcher (`--jobs`).** `agent_loop.py --jobs N|auto` (or the
`AGENT_JOBS` env) replaces the resume loop with the **dispatcher**: it derives
the ready frontier from the WI registry via `schedule.py` (a **declared
`SafetyClass` is required** — an unclassified WI fails closed without stopping
classified disjoint work), packs it into traincars (ordinary unary hard-chains
cluster up to the cap, default 4; ready spine/gate/attestation WIs cluster into
**one spine-only traincar** — spine packs with spine, never with anything else
(WI-204) — which, like protected work, serializes **whole-project** with every
other lane drained first), **atomically
reserves** each selected traincar's constituent WIs — one off-history
`commit-tree` metadata commit + one `update-ref --stdin` zero-old-value
transaction creating the train branch and every `refs/llm/reservations/WI-###`
ref, all-or-none — leases a linked worktree per train
(`../<repo>-trains/<id>`), and runs workers in parallel up to the ceiling,
rescanning on every worker exit (dynamic refill, never a static wave). A built
train parks **ready-to-integrate with its reservations held** until the
integrator advances the durable disposition, so nothing double-runs across
restarts. `docs/pause` stops new reservations at the next boundary while
in-flight workers finish; a blackout window starts no new worker;
`out/dispatch/` is a rebuildable journal/cache — Git refs are the authority;
root `run-state` becomes a **generated dispatcher outcome**. `--jobs 1` is the
explicit serial mode. **A plain launch is the dispatcher** (WI-210 — one
engine, one selection path): absent `--jobs`/`AGENT_JOBS` resolves to the
two-worker default, held at 1 until the migration audits pass (§14); the
legacy serial resume driver is retired.

**The atomic integrator.** Integration has **one logical writer** against a
dispatcher-owned `refs/heads/llm/integration` ref — advanced **only by
compare-and-swap** and never checked out in the primary worktree. Each ready
train composes on a staging branch `llm/integrate/<train-id>` in its own
worktree from the *current* integration HEAD: reservation scope and the
**exact-head review verdicts** are verified first (a verdict naming an older
commit does not count); a clean 3-way apply takes the fast path with **no
re-review**, while *any* textual conflict parks the train for a **focused
re-review** — never a silent one-side pick. A **source** conflict is human work
(WI-232): the integrator records its merge inputs (train tip + integration head)
and conflicted path(s) under a durable `refs/llm/conflict/<train>` ref, pages
`NEEDS-HUMAN` with a WI-127 `ask:` naming them, and skips the identical merge on
any relaunch whose inputs are unchanged — retrying once only when an input moves.
On the fast path the WI rows go `done` with derived
Deliverables, the log gains the integration evidence, the status snapshot and
iteration index regenerate on the composed tree, and the **combined bar always
runs** (a red bar blocks integration with the ref untouched). One integration
commit carries `Integrated-WI`/`Train-Head` trailers; a stale CAS fails
harmlessly and recomposes. A worker-reported blocker takes the **smaller
disposition transaction** (only its WI → `blocked` + `BlockRef` + trailers +
CAS, reservation released only after). Publication to the development branch
is guarded by the durable `refs/llm/publish-intent` ref (target + expected-old
+ dev ref, written before the second CAS, deleted only after the **verified**
fast-forward/reset sync): a dirty checkout defers publication untouched; a
crash between the CAS and the sync recovers idempotently — the intent, not a
guess, identifies the pre-publication hash. Once the integration ref exists it
is the **authoritative integrated disposition**; the development branch is its
published projection, and `status.md` regeneration only ever touches a file
that is absent or already generator-marked (a hand-authored status waits for
the migration).

**Crash safety (git as the recovery substrate).** `out/dispatch/` is a
rebuildable journal/cache, **never authority**: every startup reconstructs one
ownership/state record per WI and train from Git alone — the reservation refs
and their metadata commits, the train/staging branches and their trailers, the
integration ref's registry, and the publish intent. The reconcile stage
restores an **already-integrated** train (all WIs `done` on the integration
ref) and finishes its pending reservation release rather than re-integrating;
a train branch whose **novel** commits (those in `base..tip` not reachable from
the integration ref) claim a WI **outside its reservation set** is unprovable
ownership and quarantines (nothing deleted), while disjoint proven work
proceeds. The claim is read only from that novel range, so an owner **merging
the development branch into a reserved train** — the sanctioned content-only
sync that preempts stage-3 conflicts — imports integrated history, not claims:
the merged-in WI trailers are already reachable from the integration ref and
are ignored (a genuine foreign claim in a novel commit still quarantines).
A crash at any lifecycle boundary — either side of the reservation
transaction, either side of the integration CAS, after the intent write, or
between the development CAS and the worktree sync — recovers without
double-assignment, false completion, lost commits, or an unclassifiable
publication state (the wired `AGENT_FAULT_POINT` hook is how the kit's own
crash matrix proves it). Kernel locks release on process death; stored PIDs
are hints, never liveness.

**Telemetry & the parallel banner.** The dispatcher records reason-coded events
(frontier, reservation, worker/reviewer start/finish, continuation, fork/join,
overlap, conflict, re-review, integration, recovery, quarantine, cleanup)
stamped with a per-launch **run id**, so telemetry aggregates by `(run, train,
WI, session)` and a parallel session number never collides across runs. A
one-line **banner** reports active lanes, ready-frontier width, integration-queue
depth, and the cost/concurrency ceiling so parallel spend is visible; an
end-of-run rollup (`out/dispatch/telemetry.json`) reports the required
measurements — overlap/conflict/re-review/rework rates, recovery reconciles,
combined-bar failures after individually-green trains — the evidence a
downstream adopter tunes capacity from.

**Downstream migration (the two-worker flip is earned, not assumed).** Enabling
parallel dispatch changes default execution, so it is gated. A repo runs
`--jobs 1` until **both** audits pass: the **SafetyClass audit** (every open WI
carries a resolvable, non-`unclassified` class — one unaudited row holds the
whole repo) and the **soft-edge audit** (every `~` soft predecessor reviewed for
a hidden correctness dependency, signed off by creating `docs/parallel-ready`).
A **fresh scaffold passes by construction** — no soft edges, all drafted WIs
classified — so it ships parallel-by-default (`AGENT_JOBS=2` in the launcher);
a repo migrating from the legacy loop holds at one worker until it signs off,
and the flip is a **recorded** promotion. Legacy `active` WI rows reconcile to
`queued` with a logged finding (runtime activity is dispatcher state, not a
tracked column), and `docs/tracks/*` stays readable for one compatibility window
while the dispatcher never schedules from it. A repo that never opts in
(`--jobs`/`AGENT_JOBS` unset) keeps the legacy single-session resume loop,
byte-for-byte unchanged.

**Throughput caution.** Under `attended` gate authority, every track's human asks
converge on **one** ratifier; parallel tracks multiply the `NEEDS-HUMAN` queue. The
dispatcher's job is to aggregate those asks into one review surface, and 2–3
concurrently *active* lanes is the realistic ceiling while one human ratifies —
dormant lanes (a lane directory + a "blocked on `IF-…`" note, no worktree) cost
nothing until their gating decision lands.
