# Owner notes, 2026-09-23 — spine semantics, sessions, and test strategy

**Status: PROPOSAL. Not a ruling.** A sister plan to
[the assumption-tier proposal](2026-09-20-validation-gap-and-the-assumption-tier.md).
It takes the owner's notes of 2026-09-23, which also affect this repo's scope
and need the same working-through the design assumptions did, and for each one
records what the repo does today (with anchors), what the note would change,
the trade-offs, and a recommendation. Nothing here is built; the questions in §5
are for the owner.

**Who this is for.** The owner, as a decision document. Each section keeps the
owner's note number, so a note maps to exactly one place.

**Headline.** Several notes describe things the repo already does, or half does.
Saying so is the most useful result here, because it changes each ask from
"build X" to "finish or adjust X":

| note | the ask | what exists today |
|---|---|---|
| 1 | a common way to act, keep and record LLM sessions | spawning is already common; **recording** has two wrappers; retention is designed but not landed |
| 1 | a token-usage log | `docs/iteration_index.md` records date, phase, model, tokens and cost per session — **for Claude only**; codex's `tokens used` line is never parsed |
| 2 | the adjudicator works in a worktree, and its merge is mechanical | it **already** runs as an exclusive claimed lane in a worktree, and the merge is already `--no-ff` with a trunk-ancestor precondition that makes conflicts unrepresentable |
| 3 | every SR needs at least one test | **already** a rule (`coherence.py:134-135`) and fully met: 0 of 79 SRs lack a TC naming them |
| 3 | LLRs are design, not requirements | the registry's table is **already** named `design`, and a `shall` in an LLR already fails the strict check |

---

## 1. Spine authoring

### 1.1 Absolutes (note 0)

> *"Absolutes in general should be rare as they can over-constrain a design. I
> see many absolutes ('Never', 'Always') both in stakeholder needs and system
> requirements, but such assertive language can be hurtful long term."*

**Today.** Counted over whole words (research, 2026-09-23):

| registry | cells | rows with an absolute | commonest |
|---|---|---|---|
| stakeholder needs (27) | `need`, `acceptance` | **23 of 27** | every (16 rows), never (10), any (5), no (5) |
| system requirements (79) | `requirement`, `acceptance_criteria` | **66 of 79** | every (38), no (38), never (28), any (17) |

The kit already has the rule and half an implementation. PROCESS.md:650-651:
*"every comparative or absolute term in an acceptance criterion must name its
predicate"* — but the checker (`trace_text.py:146-156`) lists only comparatives
(*identical*, *equivalent*, *matches* …) and only warns. The owner has ruled on
this once already (OI-37): *"this is not the first time I've seen absolutes in a
place it wasn't warranted … An absolute in a need is a promise every child must
keep under every condition … Read the needs for unwarranted absolutes as a
class."* SN-006 was rewritten to *"supervision rather than an absolute"* as a
result, but the class-wide sweep did not follow. The spine-authoring skill and
`check_need_form.py` say nothing about absolutes.

**Analysis.** Not every absolute is a defect. Three kinds behave differently:

| kind | example | verdict |
|---|---|---|
| a quantifier over a **closed domain the system controls** | *"every row in the registry resolves"*; *"an id is never re-issued"* | fine: finite, checkable, and it is the invariant |
| a quantifier over the **open world or open time** | *"never silently"*, *"always recoverable"*, *"in every repo"* | a hidden assumption: it cannot be tested, only sampled. It should be bounded (a declared domain) or carried by a DA (assumption-tier plan §6) |
| a **prohibition of a mechanism** in a need | *"never from prose … never from predefined tracks"* | a design decision leaking into the need tier (SN-033's concern) |

So the useful rule is the one PROCESS.md already states — *name the predicate* —
extended from comparatives to absolutes: an absolute must name the closed domain
it ranges over, or carry a recorded reason.

**Recommendation.**
1. Extend `trace_text.py`'s term list with the absolute quantifiers
   (*never, always, every, all, any, none*, and *no* as a quantifier),
   warn-first, satisfied when the row names its domain or carries
   `recorded absolute: <why this must hold universally>` in `Rationale` (the
   same valve as the one-`shall` waiver).
2. Add one question to the spine-authoring skill's adjudicator list: *is this
   absolute over a closed domain the system controls? If not, bound it, or move
   the open-world part into an assumption row.*
3. Run the OI-37 sweep the ruling asked for, needs first (23 rows), as its own
   work item.

### 1.2 LLRs become design expectations (note 3)

> *"LLRs become design expectations (DE) because they truly are not
> requirements. Old logs referencing LLRs can have header updated to clarify LLRs
> are now DEs."*

**Today.** The semantics already agree with the note:

- the registry table is named `design` (`spine_carrier.py:217-222`, announced in
  `RESYNC_PACK.md:892-894`);
- a `shall` in an LLR fails the strict check (PROCESS.md; `trace_text.py`);
- only the *name* says "requirement".

The name is everywhere: 832 occurrences in 66 kit scripts (303 `LLR-###` ids),
256 in 12 kit docs, 936 in 74 test modules, and 16,829 across 1,070 files under
`docs/` (the iteration logs alone hold 5,344). The stage ladder's rung is
`DevStg-LLReqs`.

**Precedents for a rename.** MOD → REPO kept legacy read compatibility
(`trace.py:409-411`, `coherence.py:112`). UN → SN deliberately kept none
(*"a real orphan you want surfaced, not silently bridged"*,
`RESYNC_PACK.md:272-275`), kept the id numbers, and did not rewrite historical
quotes.

**Recommendation — the same shape the owner chose for SR/SS (Q9 in the
assumption-tier plan):** rename in prose now, and treat the prefix as a separate
decision.

- Docs, prompts and the dashboard call the tier **design expectations**; the
  glossary in PROCESS.md says *"`LLR-###` rows are design expectations (the
  prefix is historical)"* once.
- **Do not edit old logs.** 1,070 files and git history are records; one
  glossary line does what 1,070 header edits would, and cannot drift.
- If the prefix does change later, follow UN → SN: keep the numbers, no
  legacy bridge, historical quotes untouched. The rung name (`DevStg-LLReqs`)
  goes with it.

### 1.3 Design constraints as stakeholder needs (note 3)

> *"Need stakeholder need pointing at .md files related to my human design
> constraints … All design constraints must be explicitly defined stakeholder
> need references."*

**Today.** The owner's working constraints live in prose, and no need cites
them: the Working agreement (`AGENTS.template.md:146-183`), CLAUDE.md's
principles (stdlib-preferred, no unargued dependencies, edit conservatively,
consolidate). Some needs read as constraints — SN-012 (proportionality), SN-033
(needs in stakeholder language), SN-011's `why` (*"a blanket 'no dependencies'
rule is itself a design constraint"*), SN-007 — but none points at the document
that states the constraint. Only one need cites a markdown file (SN-027's
acceptance). The `docs/knowledge/` packs are explicitly advisory (*"when a
finding becomes a rule, promote it through change intake"*). There is no
guardrails document (`guardrails = "off"`).

**Analysis.** A design constraint is a stakeholder need whose stakeholder is the
owner: an outcome the owner wants from how the system is built. Two things pull
against simply pasting a path into a need:

- SN-033's check (`check_need_form.py`) flags internal paths in need text,
  deliberately — a need is stated in stakeholder language;
- a need cell that points at a file has no way to say *which* constraint in it.

**Recommendation.**
1. One owner-authored document of record for design constraints, each
   constraint under its own anchor.
2. Each constraint a need, stated in stakeholder language, whose **stakeholder
   row** (the list proposed in the assumption-tier plan, Q12) is "repo owner — design
   constraints" and names the document; a need cites its anchor in a `source`
   cell, not in the need text. That keeps SN-033's rule intact and makes each
   constraint traceable to requirements, hats and tests like any other need.
3. The hats are where most constraints bite (assumption-tier plan §6.5): a constraint
   such as *"no unargued dependencies"* is a hat-shaped check on every
   decomposition, not only a requirement.

### 1.4 Retired rows: a registry space, or git? (note 3)

**Today.** Supersession is deletion (`docs/repo-lock.md:348-352`, D-4: *"A
superseded row is deleted; history lives in git and the log"*). Ids are never
reused: `docs/id-watermark` counts mints from the high-water mark, so 13 SN, 107
SR, 18 LLR and 17 TC ids are spent. The one mass deletion (26 SRs) left a
forwarding map in the log (`docs/log.md:32374-32405`). Open items are the
exception: ruled rows stay, as history.

**Analysis.** Deletion keeps the registries stating only what *is*, and the
watermark keeps ids safe. What it costs is discoverability: finding why a spent
id disappeared, and what replaced it, means git archaeology or a log search. A
retired-row space in the registry would fix that but reintroduce tombstones that
can be cited as live and must be maintained.

**Recommendation.** Keep deletion. Add a **generated** retired-id index — spent
id → the commit that deleted it → the forwarding target where one was recorded —
derived from the watermark, git history, `docs/declared-absences` and the log's
forwarding maps, and rendered in the dashboard. Derived, so it cannot drift;
nothing to hand-maintain.

---

## 2. Test strategy

### 2.1 Every SR needs at least one test (note 3)

**Already the rule, and fully met.** `coherence.py:134-135` reports *"SR {sid}
has no test (TC)"* for every non-Drafted SR; PROCESS.md:742-743 says *"Every SR
needs ≥1 TC row regardless of method"*. 0 of 79 SRs lack a TC naming them
directly (0 of 192 LLRs lack one either). Coverage *through* LLRs was
considered and rejected by the owner on 2026-07-07
(`docs/archive/IMPROVEMENT_PLAN.md:4729-4737`).

One interaction with the assumption-tier plan: an SR that rests only on an assumption
(the "clearly assumed" form) still needs its own TC — S-evidence — and the
assumption's evidence is separate (TC `assumption_refs`).

### 2.2 Should lower-level tests run only when SR-level tests fail? (note 3)

> *"Smoke tests must not run any DE tests unless all SR tests are run? If SR
> passes is there any need to burn on lower level testing? Only if it fails do we
> need to uncover why."*

**Today.**
- Smoke is opt-out tiering by **module**: every test is smoke unless its module
  is in `tests/conftest.py`'s `SLOW_MODULES` (74 modules slow; 80 of 154 stay
  smoke).
- Selection has no link to SR-level vs design-level TCs.
- The TC `tier` cell (Smoke / Full / Release) is not joined to the pytest marker
  (`registry-machinery-reference.md:872-875`), and they disagree: 11 TCs declared
  Smoke cite only slow-module evidence, and 24 declared Full cite only
  smoke-module evidence.
- Test-impact selection is explicitly rejected (`PROCESS_OPTIONS.md:2037-2041`).
- 182 of 194 TCs cite both an SR and an LLR, so "SR tests" and "DE tests" are not
  separate populations today.

**Analysis.** Running the top level first and descending only on failure saves
compute when top-level tests are cheap, reliable and complete. None of those
holds here:

- **Not cheap.** SR-level evidence is mostly subprocess- and scaffold-heavy —
  that is *why* those modules are slow. The fast tests are the design-level ones.
- **Not complete.** Design expectations exist because design detail is not fully
  observable at the SR level. A green SR test does not show that an unexercised
  design path works; skipping design-level tests would hide exactly the defects
  they exist to catch.
- **Diagnosis latency.** Descending only on failure turns one red run into two.

Where the idea *is* right is **expensive, judgment-based verification**:
Inspections, Critiques and LLM reviews. There, "only descend when something
changed or failed" is the correct economics (§2.3).

**Recommendation.**
1. Keep design-level tests in the commit bar.
2. First make the declared tier real: join TC `tier` to the pytest marker, or
   derive one from the other, and fix the 35 disagreements. Any tier policy
   depends on the declared tier meaning what it says.
3. If Full-run wall time matters, order SR-level tests first and fail fast —
   ordering, not skipping.

### 2.3 How often observation tests run (note 3)

> *"Sometimes the test is just checking the design (observation), how often does
> this sort of thing get done since it's LLM dependent? Ideally based on token /
> complexity shift."*

**Today.** Four Inspection TCs (TC-036, TC-209–211) and one Critique (TC-055).
Inspections run as a written procedure (`docs/test/inspection-procedures.md`)
and are picked up by the release checklist. A Critique is triggered only by *"a
committing build whose WI touches a Critique SR"* — and no SR has
`Verification = Critique`, so it never fires; TC-055 records *"a one-time
judgement that nothing re-fires"*. Nothing ties cadence to token cost or
complexity change.

**Recommendation — event-triggered, each trigger declared on the TC:**

| trigger | fires when | source |
|---|---|---|
| content change | the rows or artifact the check reads change (a content hash) | the spine, the rendered artifact |
| complexity shift | a covered module's complexity or size moves past a declared delta | `check_complexity.py` and the size ratchet already measure both |
| judge change | the model that judges changes | the routing registry; the render critic's `holds_when` (assumption-tier plan §8.4) already names the model |
| age | a declared maximum age passes | the evidence record |

Plus the phase-close run that already exists. This is the same rule as the
assumption-tier plan's event-triggered rubric checks, stated once for every
observation-style test.

---

## 3. Sessions and orchestration

### 3.1 A common session service (note 1)

> *"Note the method of acting, maintaining, and recording a session is common
> between adjudication and other LLM actions, so it should have a common
> method / function."*

**Today.**
- **Spawning is already common.** Only two functions start a CLI:
  `agent_session.run_session` (headless, `Popen`) and
  `agent_loop._run_attached_session` (interactive). Every path — build, the two
  review legs, critique, design-check, adjudicate, dual-plan roles, route probes
  — shares `build_argv`, `invoke_session`, `run_session`, `write_session_log` and
  `commit_telemetry`. The adjudicator has no launcher of its own; it differs
  only in its brief, phase, tier and verdict check.
- **Recording has two wrappers**: the worker loop's in-line logging, and
  `agent_common.invoke_and_persist` (*"Invoke a non-worker session, durably
  account it"*).
- **Keeping a session is designed, not landed.** Resume-by-id and keep-warm are
  specified in `docs/plans/2026-08-29-adjudicator-session-retention-plan.md` and
  ruled (OI-69), but the code is an unapplied patch
  (`docs/work/handback/wi-540-adjudicator-retention-layer.patch`); WI-551 (re-land)
  and WI-541 (verify) are queued. The patch's keep-warm ping calls `run_session`
  directly and **bypasses** `invoke_session`, so as written it would add a third
  recording path.

**Recommendation.** One session service with three operations, used by every
role:

| operation | today | change |
|---|---|---|
| **act** — launch a role with a brief on a route | common | none |
| **keep** — resume by id, keep warm, reset past a context threshold | patch only | land WI-551 *through* the service, so keep-warm is recorded like any session |
| **record** — telemetry for every call | two wrappers | fold into one (the 0→A→B rule) |

### 3.2 Token usage (note 1)

> *"At each session call, the token usage gets appended to a session log
> including time, date, provider, model, and tokens used."*

**Today.** It exists: `write_session_log` writes date, model, tokens
(input + output), cost, cache reads and writes, reasoning tokens and context use
into each tracked `docs/iteration/*.log`, and `docs/iteration_index.md` rolls them
into one table (*Date · Phase · WI · Model · Outcome · Commits · Tokens · Cost
USD · … · Ctx %*).

**The gap is parity.** Only Claude sessions get numbers. codex prints *"tokens
used 165,534"* in the body and the header stays blank
(`docs/iteration/071-20260714-232536.log`); opencode is unverified; context
fields are blank for every non-Claude family (`agent_loop.py:3268-3269`).

**Recommendation.** No new log — one exists. Parse codex's and opencode's usage
lines into the same header fields, and add an explicit provider column to the
index (today it is implied by the model). Everything in §3.4 depends on this:
a context threshold cannot be enforced on a provider whose usage is not read.

### 3.3 Fewer tools per role, and skills handled mechanically (note 1)

> *"Ignores skills because that can be handled mechanically? Tool minimization?
> (Because a session doing a review doesn't really need tools? Or minimal tools
> to read diffs)"*

**Today — tools.** No role is restricted. Each provider family uses one command
template for every phase, with its bypass flag
(`--dangerously-skip-permissions`, `--dangerously-bypass-approvals-and-sandbox`).
Restrictions are prose only (*"Do not edit the code you are reviewing"*;
*"you NEVER edit the spine or the artifact yourself"*). `subagent_gate` gates
only spawning, fails open, describes itself as *"Supervision, not security"*, and
is off in this repo. A manual precedent exists outside the loop: a review run
with `--tools Read,Grep,Glob --allowedTools Read,Grep,Glob --permission-mode
dontAsk`.

**Today — skills.** Nothing injects skills into a session. They are chosen
mechanically at **scaffold** time (tag intersection) and discovered by the CLI at
**run** time from each skill's description — so run-time use is model-driven,
and every session pays for skill discovery.

**Analysis.** A reviewer that cannot write cannot edit what it reviews; the
prose rule becomes a mechanism. The cost is small and per-provider: Claude has
tool allow-lists and a permission mode; codex has `--sandbox read-only`;
opencode's equivalent is unverified. One complication: the adjudicator writes
today (it hand-edits the Status cell and runs the snapshot, §3.5), so it cannot
be read-only unless §3.5's mechanical trigger lands.

**Recommendation.**
1. A **role → tool profile** map in the routing registry: REVIEW-A/B, CRITIQUE,
   DESIGN-CHECK and PROBE get read-only; BUILD gets the full set; ADJUDICATE gets
   read-only plus writing its verdict file — which is exactly what §3.5 needs.
2. A **phase → skills** map, declared, whose skills are named in the brief;
   discovery can then be switched off for review roles to save context. Skills
   stay instructions, not tools.

### 3.4 Sessions that outlive one work item (notes 1 and 2)

> *"Session would be based on component, and might be refreshed to keep the cache
> fresh similar to adjudicator."* … *"If a session is building for a component,
> should we maintain that session for future component work until context
> exceeds x amount?"*

**Today.** Every session is fresh. *"session grouping was REMOVED"* (WI-383), and
the archived ruling reads *"every LLM actor is a **bounded fresh session**"*
(`docs/archive/AGENT_ROLES.md:124-128`). Rework is carried as text: the verdict is
embedded in the next build's prompt. Only the adjudicator's retention is ruled
(OI-69), and its dial `context_reset_pct` defaults to 0 (off). A live context
threshold does not exist: WI-506 found OI-57's ~66% restart *"not implementable
on real context accounting today, on any routed provider"*.

**Analysis.**

| gain | cost |
|---|---|
| no relearning (the retention plan records the adjudicator *"spun up for every small work item, relearned and reloaded the spine… usage was extreme"*) | context degradation as the transcript grows |
| prompt-cache reuse (OI-69 priced a keep-warm ping at ~0.1× input, break-even near 17 hours) | stale beliefs carried from one work item into the next |
| continuity across a component's related work | correlated blind spots — the assumption-tier plan's §8.5 limit, applied to sessions |
| | review independence: a reviewer that remembers the build is not independent |

**Recommendation — retention by role, one mechanism (§3.1):**

| role | retain? |
|---|---|
| adjudicator | yes — already ruled (OI-69) |
| a builder across its own work item's rework rounds | yes — same work item, low risk, and it removes the verdict-as-text round trip |
| a builder across different work items of one component | opt-in behind the same `context_reset_pct` dial plus a maximum number of work items — once §3.2's telemetry parity exists |
| reviewers, critics, design-check | never — independence is the point |

### 3.5 Where the adjudicator's approval happens, and what triggers it (note 2)

> *"If approval done in lane by adjudicator, approval must have mechanical
> trigger to minimize churn on main development branch. This reverses a
> direction made earlier to have the adjudicator perform all changes on the main
> branch. Instead, the adjudicator's session should get 'locked', and its work
> should be performed on the worktree. Then once it's ready to merge, that merge
> itself is mechanical."*

**Today — most of this is already how it works.** The owner's 2026-09-01 ruling
read *"Approval acts on spine rows… are the adjudicator's alone, performed on the
serial trunk side"* (`docs/log.md:56356`, `:56379-56384`). The implementation did
not take it literally: *"The adjudication runs as an exclusive claimed lane, not
as a bare trunk-side session… Read literally as 'commits directly on trunk', that
would be a new execution mode"* (`docs/log.md:56856-56864`). So today:

- the adjudicator works in a **lane worktree** (`<root>-drive/<branch>`);
- its approval commit lands on the **lane branch** (for example `2e1197fd
  approve: LLR-207, TC-205 -> Approved`);
- the **merge is mechanical**: `git merge --no-ff` in the merge slot, admitted
  only when trunk is already an ancestor of the branch, so *"a merge CONFLICT
  becomes unrepresentable"* (`integrate.py:6-13`);
- trunk churn per adjudication is **two commits** (claim and merge); iteration
  and logging stay lane-side (4–5 commits typically, up to 34–35 for rework-heavy
  items).

Two facts the note should know: git `main` is not the trunk (the trunk is the
primary checkout's branch — `refactor_again` now — and *"the loop never merges to
main and never pushes"*, OI-81); and this repo runs one lane (`docs/stack.ini`
declares no `lanes`).

**What would actually change.**

| part of the note | today | the change |
|---|---|---|
| work in a worktree, iteration isolated there | done | none |
| mechanical merge, no conflicts | done | none |
| **mechanical approval trigger** | the session hand-edits the Status cell and runs `intake.py snapshot --approves …` — *"That commit IS the approval"* | the adjudicator writes a **verdict record** (APPROVE, the row ids, the content hash it judged); a script applies the flip and the snapshot from that record, in the lane |
| **"locked" session** | exclusivity comes from admission (an exclusive work-item kind), not a session lock | the retained adjudicator session (§3.4) plus the existing slot lock; no new lock needed |

**The mechanical trigger reverses OI-45(b).** OI-45 retired every machine path
that moves an approval record — the machine writer *"writes nothing,
permanently"* (`intake.py:2329-2331`) — because a machine path is *"the widest
laundering surface in the kit"*, and it asked *"what recorded human act
authorizes a machine to move the approval record, and through which single
door."* A verdict record answers that directly, **for loop-approvable rungs**:
the single door is *verdict record → apply script*, the authority is the
recorded verdict, and the script refuses when the judged content hash no longer
matches. On a **human-held** rung the recorded act must be the human's, so the
same script would refuse unless the verdict carries the human's attestation.

**Recommendation.**
1. Record that the worktree-and-mechanical-merge half is already in place, and
   amend the 2026-09-01 ruling's wording (*"serial trunk side"*) to match what
   was built.
2. Adopt the verdict-record → apply-script trigger as a deliberate, recorded
   reversal of OI-45(b), scoped by the approval dial as above. It also lets the
   adjudicator run read-only (§3.3).
3. Take session "locking" as retention (§3.4), not a new lock.

### 3.6 Fanning out to other models (note 3)

> *"Need to update prose for fanning out carefully — only delegate to lower tier
> models, do they need to be named? Or is fanning out from a model just never
> permitted because of abuse / unexpected results?"*

**Today.** The prose permits it, down-tier: *"Spawn a separate agent for an
independent pre-gate review, to step a mechanical subtask down a tier, or to
give bulk content a dedicated context … never to split the hats' shared
context"* (PROCESS.md:52-55); the driver *"steps down … when the hand-off pays
for itself"* (:933-938); gate-closure review *"is never delegated down"*
(PROCESS_OPTIONS.md:536-537). This repo *"runs subagents freely under a
human-launched loop"* (`docs/process.toml:225`), with `subagent_gate` off. And
every session runs with its provider's bypass flag, so a subagent inherits full
permissions.

**Analysis.** The risks the note names are real here: cost that nothing budgets,
subagents acting with full permissions, and work that never reaches the session
log. Naming models in prose would rot, since models change monthly; the kit
already has the stable vocabulary — tiers (*quick*, *medium*, *strong*) mapped to
models in the routing registry.

**Recommendation.**
1. **Prose:** fan-out is permitted only down-tier, only for a bounded mechanical
   subtask or an independent pre-gate review, and names **tiers, not models**.
2. **Never from review, critique, design-check or adjudication sessions** — and
   with §3.3's read-only profiles those roles have no spawn tool at all.
3. **Unattended runs:** turn `subagent_gate` on with a declared spawn budget per
   session, and record spawns in the session log. It is supervision, not
   security, and the prose should keep saying so.

### 3.7 Who plans, who builds, who reviews (note 3)

> *"Need to review plan/build/review sequence, and likely most plans should be
> routed through same builder. If not it can be a secondary reviewer."*

**Today.** PLAN runs at the strong tier; BUILD, REVIEW-A and REVIEW-B at medium;
DESIGN-CHECK, CRITIQUE and ADJUDICATE at strong (`agent_loop.py:337-354`). Review
prefers a different family from the last implementer, and REVIEW-B from
REVIEW-A, relaxing when no other family is available. Each phase is a fresh
session; the plan reaches the builder as text (*"fresh sessions have no chat
memory"*). Nothing routes a builder to the plan it wrote.

**Options.**

| option | gain | cost |
|---|---|---|
| (a) the planner builds (one route, and with retention one session) | no plan re-reading; the builder knows why | builds at the strong tier cost more; no independent check of the plan before building |
| (b) the builder plans, at its own tier | cheapest; continuity | plan quality at the medium tier |
| (c) **keep them separate, and make the planner a reviewer of the build** — it checks conformance to the plan it wrote | the plan gets checked, by the one reader who knows its intent; cost unchanged | one more review leg, or REVIEW-A's route changes |

**Recommendation: (c) by default, (a) where retention is available** and the
work item is marked plan-heavy. (c) matches the note's own fallback.

---

## 4. Code-quality doctrine

### 4.1 Minimizing the number of expressed operations (note 3)

> *"There should be a way to minimize code complexity by looking at defined /
> expressed operations and trying to minimize those (this forces
> consolidation), but how would it end up getting abused?"*

**Today.** Several measures exist:
- the module-size ratchet (SLOC per module; above 1,000 needs an exact baseline;
  *"decompose, do not bump"*, and shrinking must be re-stamped too);
- `check_complexity.py` (cognitive complexity and SLOC per function, and a
  per-module **public-symbol count — reported, never gated**), with a baseline
  that calls itself a *"DEBT STATEMENT, NOT AN APPROVAL"*;
- ruff's C901 cap;
- the duplicate-body census (warn-first);
- PROCESS.md's 0→A→B rule: *"prefer the change that minimizes **total**
  behavior."*

**How a count of operations gets gamed** (Goodhart's law, concretely):

| move | lowers the count by | what it costs |
|---|---|---|
| merge unrelated functions behind a mode flag | fusing operations | complexity per function rises |
| stringly-typed dispatch (`do(op, …)`) | collapsing a family into one symbol | type safety, greppability |
| move logic into data, config or eval | hiding operations | reviewability |
| delete validation and tests | dropping operations | correctness |
| inline everything | removing named helpers | readability; duplication returns |

**Recommendation.** Keep the count as a **paired, reported** signal, never a lone
gate: public operations per component, trended in the dashboard, next to the
per-function complexity and size caps that already bite. A drop in operations
that raises per-function complexity is not consolidation, and the pairing makes
that visible. A growing count is a review trigger — the 0→A→B question asked —
not a failure.

### 4.2 When a guard is owed (note 3)

> *"Need to emphasize to reviewers and builders - don't build a guard if the
> ingested data is already produced with sanity unless there is real risk of
> corruption (file on disk), or operation is critical on public infra where
> attack could be feasible."*

**Today.** The doctrine exists but is scattered: the `antidote` skill (*"Add a
defensive guard … Ask why that state is reachable. Fix the cause, not the
symptom"*; *"validate once at the boundary, then trust the type"*; a red flag
for guards against a state that *"should not happen"*); PROCESS.md:244-247
(right-sizing never trims validation at trust boundaries, data-loss handling,
security, accessibility); AGENTS.template.md (*"validate schema/shape at the
boundary"*); and the reviewer prompt, which makes an added guard name *"why the
defect cannot be made UNREPRESENTABLE instead"*. What is missing is the owner's
concrete definition of **where the boundary is**.

**Recommendation.** One test, stated once, in the `antidote` skill and the
reviewer prompt (not `AGENTS.template.md`, which has 20 bytes free):

> A guard is owed only where the input crosses a trust boundary — a file on disk,
> the network, a person, another process, or a model's output — or where the
> operation is irreversible or exposed to attack. Data this code produced
> in-process is trusted: fix the producer instead.

Two consequences worth stating with it: the kit's registries are hand-edited
files on disk, so validating them is owed (that is what `trace.py` does); and a
model's output is a boundary (an interpreting far side, in the assumption-tier plan's
terms), so validating structured output is owed too.

---

## 5. Questions for the owner

| # | question | recommendation |
|---|---|---|
| S1 | Extend the absolutes rule (warn-first, with a recorded-absolute waiver) and run OI-37's sweep? | yes (§1.1) |
| S2 | LLR → design expectation: prose now, prefix as a separate later decision; no edits to old logs? | yes (§1.2) |
| S3 | Design constraints: one owner document, each constraint a need with a `source` anchor, the owner as a listed stakeholder? | yes (§1.3) |
| S4 | Retired rows: keep deletion, add a generated retired-id index? | yes (§1.4) |
| S5 | Keep design-level tests in the commit bar, and join the TC `tier` to the pytest marker first? | yes (§2.2) |
| S6 | Event-triggered observation tests (content, complexity, judge, age)? | yes (§2.3) |
| S7 | One session service (act / keep / record), with WI-551 landing through it? | yes (§3.1) |
| S8 | Token telemetry parity for codex and opencode, plus a provider column? | yes (§3.2) |
| S9 | Role → tool profiles (reviewers read-only) and a phase → skills map? | yes (§3.3) |
| S10 | Retention by role: adjudicator yes, builder within its own work item yes, across a component opt-in, reviewers never? | yes (§3.4) |
| S11 | The adjudicator's verdict record → apply script, as a recorded reversal of OI-45(b) scoped by the dial; and amend the 2026-09-01 wording to what was built? | yes (§3.5) |
| S12 | Fan-out: down-tier only, tiers not models, never from review roles, gated with a budget when unattended? | yes (§3.6) |
| S13 | Plan / build: (c) the planner reviews the build, or (a) the planner builds? | (c) by default (§3.7) |
| S14 | Operation count: paired and reported, never a lone gate? | yes (§4.1) |
| S15 | The guard test in `antidote` and the reviewer prompt? | yes (§4.2) |

**Suggested order**, cheapest and most independent first: S8 (telemetry parity)
unblocks S10; S15, S1 and S2 are prose and a warn-first check; S5 is a data fix;
S7 and S9 reshape the session path and should land together; S11 depends on S9
and S10.
