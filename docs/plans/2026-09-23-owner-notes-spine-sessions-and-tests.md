# Owner notes, 2026-09-23 — spine semantics, sessions, and test strategy

**Status: PROPOSAL. Not a ruling.** A sister plan to
[the assumption-tier proposal](2026-09-20-validation-gap-and-the-assumption-tier.md).
It takes the owner's notes of 2026-09-23, which also affect this repo's scope
and need the same working-through the design assumptions did, and for each one
records what the repo does today (with anchors), what the note would change,
the trade-offs, and a recommendation. Nothing here is built; the questions in §5
are for the owner.

**Revised after an adversarial review (2026-09-23, §6).** A codex Sol review
(reasoning effort high) rejected the first draft as a decision basis: it had the
approval-authority question wrong, inferred a test split the registry does not
contain, and understated what several recommendations need. Every finding was
checked against the code; all held, and each is applied below.

**Who this is for.** The owner, as a decision document. Each section keeps the
owner's note number, so a note maps to exactly one place.

**Headline.** Several notes describe things the repo already does, or half does.
Saying so is the most useful result here, because it changes each ask from
"build X" to "finish or adjust X":

| note | the ask | what exists today |
|---|---|---|
| 1 | a common way to act, keep and record LLM sessions | spawning is already common; **recording** has two wrappers; retention is designed for the adjudicator but not landed |
| 1 | a token-usage log | `docs/iteration_index.md` records date, phase, model, tokens and cost per session — **for Claude only**; codex's usage never reaches it |
| 2 | the adjudicator works in its own lane, and the merge is mechanical | **already the ruled design**: an exclusive adjudication lane whose reviewed commit is merged `--no-ff` with a trunk-ancestor precondition that makes conflicts unrepresentable |
| 3 | every SR needs at least one test | **already** a rule (`coherence.py:134-135`) and fully met: 0 of 79 SRs lack a TC naming them |
| 3 | LLRs are design, not requirements | the registry's table is **already** named `design`, and a `shall` in an LLR already fails the strict check |

---

## 1. Spine authoring

### 1.1 Absolutes (note 0)

> *"Absolutes in general should be rare as they can over-constrain a design. I
> see many absolutes ('Never', 'Always') both in stakeholder needs and system
> requirements, but such assertive language can be hurtful long term."*

**Today.** Whole-word counts over the normative and acceptance cells:

| registry | cells | rows with an absolute | commonest |
|---|---|---|---|
| stakeholder needs (27) | `need`, `acceptance` | **23 of 27** | every (16 rows), never (10), no (7), any (5) |
| system requirements (79) | `requirement`, `acceptance_criteria` | **66 of 79** | no (41), every (38), never (28), any (17) |

The kit already has the rule and a sliver of an implementation. PROCESS.md:650-651:
*"every comparative or absolute term in an acceptance criterion must name its
predicate"*. But the checker (`trace_text.ac_advisories`, `:269-289`) scans only
SR acceptance cells, its term list (`:146-156`) holds only comparatives, and it
only warns. The owner has ruled on this once already (OI-37): *"An absolute in a
need is a promise every child must keep under every condition … Read the needs
for unwarranted absolutes as a class."* SN-006 was rewritten as a result; the
class-wide sweep did not follow.

**Analysis.** Not every absolute is a defect:

| kind | example | verdict |
|---|---|---|
| a quantifier over a **closed domain the system controls** | *"every row in the registry resolves"*; *"an id is never re-issued"* | fine: finite, checkable, and it is the invariant |
| a quantifier over the **open world or open time** | *"never silently"*, *"in every repo"* | a hidden assumption: it can be sampled, not tested. Bound it, or carry it in an assumption row (assumption-tier plan §6) |
| a **prohibition of a mechanism** in a need | *"never from prose … never from predefined tracks"* | a design decision leaking into the need tier (SN-033's concern) |

Broad words — *any*, *all*, *no* — will fire constantly without a suppression
rule, so a naive term list would be noise.

**Recommendation.**
1. Extend the check to the **normative and acceptance cells of every spine
   tier**, not just SR acceptance, warn-first.
2. Reuse the **existing waiver grammar**, `recorded waiver: <reason>`, in each
   tier's existing reason cell (`why` on a need, `Rationale` on an SR) — no second
   waiver vocabulary.
3. Define the suppression predicate before shipping: an absolute is satisfied
   when it names its domain from a closed list (a registry, an id space, a
   declared set), and the tokenization is documented. What cannot be decided
   mechanically — whether a named domain is really closed — stays a review
   question in the spine-authoring skill.
4. Run the OI-37 sweep the ruling asked for, needs first, as its own work item.

### 1.2 LLRs become design expectations (note 3)

> *"LLRs become design expectations (DE) because they truly are not
> requirements. Old logs referencing LLRs can have header updated to clarify LLRs
> are now DEs."*

**Today.** The semantics already agree with the note: the registry table is
named `design` (`spine_carrier.py:217-222`), and a `shall` in an LLR fails the
strict check. Only the *name* says "requirement" — and it is everywhere: 832
occurrences in 66 kit scripts (303 `LLR-###` ids), 256 in 12 kit docs, 936 in
74 test modules, 16,829 across 1,070 files under `docs/`. The stage rung is
`DevStg-LLReqs`.

**Precedents.** MOD → REPO kept legacy read compatibility (`trace.py:409-411`).
UN → SN deliberately kept none (*"a real orphan you want surfaced, not silently
bridged"*, `RESYNC_PACK.md:272-275`), kept the id numbers, and did not rewrite
historical quotes.

**Recommendation — the same shape the owner chose for SR/SS (Q9 in the
assumption-tier plan):** rename in prose now; the prefix is a separate later
decision.

- Docs, prompts and the dashboard call the tier **design expectations**; one
  glossary line in PROCESS.md records that *`LLR-###` rows are design
  expectations (the prefix is historical)*.
- **Do not edit old logs.** They are records; one glossary line does what 1,070
  header edits would.
- If the prefix changes later, follow UN → SN: keep the numbers, no legacy
  bridge, historical quotes untouched, and rename the rung with it.

### 1.3 Design constraints as stakeholder needs (note 3)

> *"Need stakeholder need pointing at .md files related to my human design
> constraints … All design constraints must be explicitly defined stakeholder
> need references."*

**Today.** The owner's working constraints live in prose, and no need cites
them: the Working agreement (`AGENTS.template.md:146-183`), CLAUDE.md's
principles. Some needs read as constraints — SN-012 (proportionality), SN-033
(needs in stakeholder language), SN-011's `why`, SN-007 — but none points at the
text it came from. Only one need cites a markdown file (SN-027's acceptance).
The need row's core is `need`, `why`, `priority`, `acceptance`
(`spine_carrier.py:779-780`); there is no `source` cell and no stakeholder list
yet.

**Analysis.** A design constraint is a stakeholder need whose stakeholder is the
owner. The review sharpened what that means for one-fact-one-home: **the need is
the canonical obligation**. The spine-authoring skill already requires every
load-bearing clause in the normative need text, so the constraint must be *in*
the need, not only in a document it points at. The document is provenance —
where the constraint came from and its reasoning — not a second normative copy.
And hats should *apply* a constraint during decomposition, not restate it.

SN-033's check also flags internal paths in need text, deliberately, so the
pointer cannot live in the need cell.

**Recommendation.**
1. Each design constraint becomes a need, stated in stakeholder language, whose
   stakeholder is the owner.
2. The owner's constraints document is provenance only; the need cites it in a
   separate cell, not in its text.
3. Hats reference the need, not the prose.
4. Priced separately and ruled with the assumption-tier plan's stakeholder list
   (its Q12): the new need cells, their carrier and template entries, dogfood
   sync, and whichever renderer or check consumes them.

### 1.4 Retired rows: a registry space, or git? (note 3)

**Today.** Supersession is deletion (`docs/repo-lock.md:348-352`, D-4: *"A
superseded row is deleted; history lives in git and the log"*). Ids are never
reused: `docs/id-watermark` counts mints from the high-water mark (13 SN, 107
SR, 18 LLR and 17 TC ids spent). The one mass deletion left a prose forwarding
map in the log (`docs/log.md:32374-32405`).

**Analysis.** Deletion keeps the registries stating only what *is*. What it costs
is discoverability: why a spent id disappeared, and what replaced it. The first
draft proposed deriving that from existing sources, and the review was right
that they cannot supply it: the watermark holds only high-water marks,
`docs/declared-absences` is a path-and-reason list, git history can be shallow or
squashed downstream, and the log's forwarding maps are prose.

**Recommendation.** Keep deletion. Record a **structured, append-only retirement
event at deletion time** — id, date, the commit that removed it, the successor
if any, the reason — in a file outside the live registries, so D-4 holds. The
dashboard renders it. Retirements before the file existed show as *unknown*
rather than guessed.

---

## 2. Test strategy

### 2.1 Every SR needs at least one test (note 3)

**Already the rule, and fully met.** `coherence.py:134-135` reports *"SR {sid}
has no test (TC)"* for every non-Drafted SR; PROCESS.md:742-743: *"Every SR needs
≥1 TC row regardless of method"*. 0 of 79 SRs lack a TC naming them directly.
Coverage *through* LLRs was considered and rejected by the owner on 2026-07-07.
An SR that rests only on an assumption still needs its own TC; the assumption's
evidence is separate.

### 2.2 Should lower-level tests run only when SR-level tests fail? (note 3)

> *"Smoke tests must not run any DE tests unless all SR tests are run? If SR
> passes is there any need to burn on lower level testing? Only if it fails do we
> need to uncover why."*

**Today.**
- **There is no "SR test" population and no "DE test" population.** 182 of the
  194 TCs cite both an SR and an LLR; 9 cite only an SR, and 3 only an LLR. Of
  those nine SR-only rows, five are manual or non-pytest evidence.
- Smoke is opt-out tiering by **module** (`tests/conftest.py` `SLOW_MODULES`),
  with no link to the spine; test-impact selection is explicitly rejected
  (`PROCESS_OPTIONS.md:2037-2041`).
- The TC `tier` cell and the pytest marker disagree for **41** TCs: 24 declared
  Full cite only smoke-module evidence, 11 declared Smoke cite only slow-module
  evidence, and 6 declared Smoke cite a mix. `pytest.ini:4-23` records that this
  repo's smoke/slow partition deliberately differs from the shipped marker
  scheme, and the smoke tier has an enforced 60-second budget.

**Analysis.** The note's idea — run the top level first and descend only on
failure — cannot be applied, because the registry does not say which tests are
"top level". A TC that cites both an SR and an LLR is not one or the other, and
inferring level from its references would be wrong. Separately, design
expectations exist because design detail is not fully observable at the SR
level, so skipping design-level tests after a green SR-level run would hide the
defects they exist to catch. Where "descend only when something changed or
failed" *is* the right economics is expensive, judgment-based verification
(§2.3).

**Recommendation.**
1. Keep every test in the commit bar that is there today.
2. If test level matters, **first give each TC a primary verification purpose**
   (or split mixed TCs where that is honest), then measure the populations —
   before any ordering or conditional policy.
3. Reconciling the 41 tier disagreements is **not a data cleanup**. Moving slow
   evidence into smoke can break the 60-second budget; changing an approved TC's
   tier amends an approved row and needs re-attestation; and the TC-to-test
   relation is many-to-many, so no trivial derived mapping exists. Decide
   separately what the meta-repo's budget partition means against the shipped
   tier contract, then price the migration.

### 2.3 How often observation tests run (note 3)

> *"Sometimes the test is just checking the design (observation), how often does
> this sort of thing get done since it's LLM dependent? Ideally based on token /
> complexity shift."*

**Today.** Four Inspection TCs (TC-036, TC-209–211) and one Critique (TC-055).
**No runner executes them.** Phase close runs the mechanical gate and a
contradiction audit (`PROCESS_OPTIONS.md:2025-2046`), not Inspections or
Critiques; the release checklist only *collects* manual items at release time.
TC-209–211 are still Drafted, and TC-211's procedure is marked incomplete
(`docs/test/inspection-procedures.md:62-73`). A Critique fires only on a
committing build that touches an SR with `Verification = Critique`, and no SR has
it; TC-055 records *"a one-time judgement that nothing re-fires"*.

**Recommendation — event-triggered, each trigger declared on the TC**, as a new
design rather than an extension of something that runs:

| trigger | fires when |
|---|---|
| content change | the rows or artifact the check reads change (a content hash) |
| complexity shift | a covered module's complexity or size moves past a declared delta |
| judge change | the model that judges changes |
| age | a declared maximum age passes |

It needs, before approval: somewhere to record each check's last run and the
state it judged; who owns firing it; what a red result blocks; and how it
interacts with release. The Drafted and incomplete Inspection rows are resolved
separately. The assumption-tier plan's event-triggered rubric checks are the
same rule.

---

## 3. Sessions and orchestration

### 3.1 A common session service (note 1)

> *"Note the method of acting, maintaining, and recording a session is common
> between adjudication and other LLM actions, so it should have a common
> method / function."*

**Today.**
- **Spawning is already common.** Only two functions start a CLI:
  `agent_session.run_session` (headless) and `agent_loop._run_attached_session`
  (interactive). Every role — build, both review legs, critique, design-check,
  adjudicate, dual-plan roles, route probes — shares `build_argv`,
  `invoke_session`, `run_session`, `write_session_log` and `commit_telemetry`.
  The adjudicator has no launcher of its own.
- **Recording has two wrappers**: the worker loop's in-line logging, and
  `agent_common.invoke_and_persist`.
- **Keeping a session is designed for the adjudicator only**, ruled (OI-69), and
  not landed: the code is an unapplied patch
  (`docs/work/handback/wi-540-adjudicator-retention-layer.patch`), with WI-551
  (re-land) and WI-541 (verify) queued. Its keep-warm ping calls `run_session`
  directly and **bypasses** `invoke_session`, so as written it would add a third
  recording path.

**Recommendation.** One session service with three operations:

| operation | today | change |
|---|---|---|
| **act** — launch a role with a brief on a route | common | none |
| **keep** — resume by id, keep warm, reset | adjudicator patch only | land WI-551 *through* the service, so keep-warm is recorded like any session |
| **record** — telemetry for every call | two wrappers | fold into one (the 0→A→B rule) |

### 3.2 Token usage (note 1)

> *"At each session call, the token usage gets appended to a session log
> including time, date, provider, model, and tokens used."*

**Today.** It exists for Claude: `write_session_log` writes date, model, tokens,
cost, cache and reasoning tokens and context use into each tracked
`docs/iteration/*.log`, and `docs/iteration_index.md` rolls them into one table.

**The gap is parity, and it is not a parser.** On a successful codex call,
`run_session` *replaces* the captured output with codex's
`--output-last-message` file (`agent_session.py:536-538`, `:617-621`) — so the
stream holding *"tokens used 165,534"* never reaches the log. The codex routes
do not request structured output, and opencode's telemetry is unverified.

**Recommendation.**
1. Keep a separate raw telemetry stream alongside the deterministic final text,
   or switch the routes to verified structured provider output with test
   fixtures.
2. Add an explicit provider column to the index.
3. **Distinguish per-call tokens from live context occupancy.** A cumulative
   token count is not how full a context is; nothing that resets sessions (§3.4)
   may use the first as the second.

### 3.3 Fewer tools per role, and skills handled mechanically (note 1)

> *"Ignores skills because that can be handled mechanically? Tool minimization?
> (Because a session doing a review doesn't really need tools? Or minimal tools
> to read diffs)"*

**Today — tools.** No role is restricted. Every route in `docs/agents.toml`
carries its provider's bypass flag (`--dangerously-skip-permissions`,
`--dangerously-bypass-approvals-and-sandbox`), for every phase. Restrictions are
prose only (*"Do not edit the code you are reviewing"*). A manual precedent
exists outside the loop: a review run with `--tools Read,Grep,Glob
--allowedTools Read,Grep,Glob --permission-mode dontAsk`.

**Today — skills.** Nothing injects skills into a session: they are chosen
mechanically at **scaffold** time (tag intersection) and discovered by the CLI at
**run** time, so every session pays for discovery.

**Analysis.** A reviewer that cannot write cannot edit what it reviews. But the
review was right that **a registry map alone changes no permissions**: the
command templates carry the bypass flags, so restriction means building each
provider's command differently per role. And "read-only except for one verdict
file" is not expressible in codex's sandbox modes.

**Recommendation.**
1. **Provider-specific command construction per role** — part of this item, not
   a follow-on: restricted roles (REVIEW-A/B, CRITIQUE, DESIGN-CHECK, PROBE,
   ADJUDICATE) drop the bypass flag and get their provider's read-only mode;
   BUILD keeps full tools.
2. **Restricted sessions never write files.** They return their verdict as
   output (stdout or the last message), and the **orchestrator** validates it and
   writes the verdict file. That is least privilege without per-path sandbox
   rules.
3. A declared **phase → skills** map, named in the brief, so discovery can be
   switched off for review roles.

### 3.4 Sessions that outlive one work item (notes 1 and 2)

> *"Session would be based on component, and might be refreshed to keep the cache
> fresh similar to adjudicator."* … *"If a session is building for a component,
> should we maintain that session for future component work until context
> exceeds x amount?"*

**Today.** Every session is fresh: *"session grouping was REMOVED"* (WI-383), and
the archived ruling reads *"every LLM actor is a **bounded fresh session**"*.
Rework is carried as text: a separate review session's verdict is embedded in the
next build's prompt. Retention is ruled only for the adjudicator (OI-69), under
its own `[adjudicator]` table, with per-family resume adapters, CLI-home
isolation, drain and compaction rules, and reset inputs
(`docs/plans/2026-08-29-adjudicator-session-retention-plan.md`). No live context
threshold exists: WI-506 found OI-57's ~66% restart *"not implementable on real
context accounting today, on any routed provider"*.

**Analysis.**

| gain | cost |
|---|---|
| no relearning (the retention plan records the adjudicator *"spun up for every small work item, relearned and reloaded the spine… usage was extreme"*) | context degradation as the transcript grows |
| prompt-cache reuse | stale beliefs carried from one work item into the next |
| continuity across related work | correlated blind spots — the assumption-tier plan's §8.4 limit, applied to sessions |
| | review independence: a reviewer that remembers the build is not independent |

Two corrections from the review. A retained **builder** does not remove the
verdict-as-text round trip: the verdict comes from a *separate* review session,
so it has to cross a session boundary as text or another explicit artifact
either way. And reusing the adjudicator's dial for builders would silently widen
OI-69 and leave behind most of its safety machinery.

**Recommendation — retention by role:**

| role | retain? |
|---|---|
| adjudicator | yes — ruled (OI-69); land it (§3.1) |
| a builder, within its own work item or across a component | **a separately ruled experiment**: its own config scope, reset inputs, CLI-home isolation and resume adapters, measured against a fresh session plus a good brief — and only after §3.2 gives real context accounting |
| reviewers, critics, design-check | never — independence is the point |

The verdict keeps crossing sessions as explicit text in every case.

### 3.5 Where the adjudicator's approval happens, and what triggers it (note 2)

> *"If approval done in lane by adjudicator, approval must have mechanical
> trigger to minimize churn on main development branch. This reverses a
> direction made earlier to have the adjudicator perform all changes on the main
> branch. Instead, the adjudicator's session should get 'locked', and its work
> should be performed on the worktree. Then once it's ready to merge, that merge
> itself is mechanical."*

**Today — the worktree-and-mechanical-merge shape is already the ruled design.**
The 2026-09-01 plan of record defines the adjudicator as *"a trunk-side,
exclusive adjudication session"* whose *"ADJUDICATE session runs on the serial
trunk side as an exclusive lane; its APPROVE performs the flip and takes the
snapshot … in its own reviewed commit"*
(`docs/plans/2026-09-01-approval-act-adjudicator-only.md:67-75`, `:94-103`).
"Trunk-side" there *means* the exclusive admitted lane. So:

- the adjudicator works in its own lane worktree, and nothing else claims while
  it runs;
- its approval commit lands on the lane branch;
- the merge is mechanical: `git merge --no-ff` in the merge slot, admitted only
  when trunk is already an ancestor of the branch, so *"a merge CONFLICT becomes
  unrepresentable"* (`integrate.py:6-13`);
- trunk churn per adjudication is **two commits** (claim and merge); iteration
  and logging stay in the lane.

Two facts worth knowing: git `main` is not the trunk (the trunk is the primary
checkout's branch — `refactor_again` now — and *"the loop never merges to main
and never pushes"*, OI-81); and this repo runs one lane.

**What a mechanical approval trigger would really change.** Today the
adjudicator session edits the Status cell and takes the snapshot in its own
reviewed commit — *"That commit IS the approval."* A mechanical trigger would
have a script perform the flip from a verdict the session emits. That runs
straight into OI-45, which retired every machine path that moves an approval
record (*"writes nothing, permanently"*, `intake.py:2327-2335`) and asked *"what
recorded human act authorizes a machine to move the approval record, and through
which single door."* The review was right that a verdict file does not answer
that: a content hash proves **which bytes were judged**, not **who held the
authority** to approve them, and a field claiming a human's attestation is not an
authenticated human act. It would recreate the laundering surface OI-45 removed.

**Recommendation.**
1. **Record that the note's shape is already in place** — own lane, isolated
   iteration, mechanical merge, two trunk commits — and that the 2026-09-01
   ruling needs no amendment.
2. **Keep the adjudicator's reviewed status-and-snapshot commit as the approval
   act.** Do not add a machine writer.
3. If a mechanical trigger is still wanted, it is **its own ruling**, and must
   specify: how the issuer is authenticated, the rung and id scope, replay
   prevention, an atomic flip-plus-snapshot, and who invokes the writer.
4. Take session "locking" as retention (§3.4) plus the existing exclusive
   admission — no new lock.

### 3.6 Fanning out to other models (note 3)

> *"Need to update prose for fanning out carefully — only delegate to lower tier
> models, do they need to be named? Or is fanning out from a model just never
> permitted because of abuse / unexpected results?"*

**Today.** PROCESS.md permits **two** kinds of fan-out, not one: stepping a
mechanical subtask **down** a tier, and **peer-tier** delegation to give bulk
content a dedicated context or to run an independent review (`:52-55`,
`:933-939`); gate-closure review *"is never delegated down"*
(`PROCESS_OPTIONS.md:536-537`). This repo *"runs subagents freely under a
human-launched loop"* (`docs/process.toml:225`). `subagent_gate` is a **Claude
Code hook** that recognizes only Claude's `Task` and `Agent` tools, fails open,
and is off here; it neither sees nor budgets fan-out from codex or opencode. And
every route runs with its provider's bypass flag, so a subagent inherits full
permissions.

**Analysis.** The risks the note names are real: cost nothing budgets, subagents
with full permissions, work that never reaches the session log. Naming models in
prose would rot; the kit's stable vocabulary is tiers (*quick*, *medium*,
*strong*) mapped to models in the routing registry.

**Recommendation.**
1. **Rule explicitly** whether peer-tier dedicated-context delegation stays. The
   note's "only down-tier" would retire it; that is a policy change, not a
   clarification.
2. Prose names **tiers, not models**.
3. **Never from review, critique, design-check or adjudication sessions** — and
   with §3.3's restricted command construction those roles cannot spawn anyway.
4. Budget and record fan-out **in the outer orchestrator**, provider-neutral. The
   Claude hook remains useful supervision for Claude routes, and the prose should
   call it Claude-only and *"supervision, not security"*.

### 3.7 Who plans, who builds, who reviews (note 3)

> *"Need to review plan/build/review sequence, and likely most plans should be
> routed through same builder. If not it can be a secondary reviewer."*

**Today.** PLAN runs at the strong tier; BUILD and both review legs at medium
(`agent_loop.py:337-354`). Review prefers a family different from the
implementer's. Each phase is a fresh session, and the plan reaches the builder as
text.

**Options.**

| option | gain | cost |
|---|---|---|
| (a) the planner builds | the builder knows why | builds at the strong tier cost more; no independent check of the plan; needs planner retention, which nothing proposes yet |
| (b) the builder plans, at its own tier | cheapest; continuity | plan quality at the medium tier |
| (c) **keep review independent, and hand the planner's intent to it as a conformance checklist** | the build is checked against what the plan meant; review stays independent; no extra strong-tier session | the plan must state its intent checkably |
| (d) the planner as an **additional, advisory** reviewer | the plan's author checks conformance | a strong-tier session per build; anchors that leg to the plan's own assumptions |

The first draft recommended the planner *replacing* a review leg. The review was
right that this is neither cost-neutral (a strong-tier route) nor independent.

**Recommendation: (c).** (d) only where a work item is marked plan-heavy and the
strong-tier cost is measured first.

---

## 4. Code-quality doctrine

### 4.1 Minimizing the number of expressed operations (note 3)

> *"There should be a way to minimize code complexity by looking at defined /
> expressed operations and trying to minimize those (this forces
> consolidation), but how would it end up getting abused?"*

**Today.** The module-size ratchet (SLOC per module, *"decompose, do not bump"*);
`check_complexity.py` (cognitive complexity and SLOC per function, and a
per-module **public-symbol count, reported, never gated**); ruff's C901 cap; the
duplicate-body census; and PROCESS.md's 0→A→B rule, *"prefer the change that
minimizes **total** behavior."*

**The existing count is not an operation count.** It counts every non-underscore
module-level class, function and assignment (`check_complexity.py:328-350`), so a
public constant or a configuration table moves it without any operation
changing. It is also per module, not per component.

**How a count of operations gets gamed** (Goodhart's law):

| move | lowers the count by | what it costs |
|---|---|---|
| merge unrelated functions behind a mode flag | fusing operations | complexity per function rises |
| stringly-typed dispatch (`do(op, …)`) | collapsing a family into one symbol | type safety, greppability |
| move logic into data, config or eval | hiding operations | reviewability |
| delete validation and tests | dropping operations | correctness |
| inline everything | removing named helpers | readability; duplication returns |

**Recommendation.** First decide what is being measured — public API surface,
callable operations, or behavioural paths — and validate that the chosen measure
tracks real consolidation findings. Only then add a component join and a trend
store. Whatever it becomes, it is a **paired, reported** signal beside the
complexity and size caps, never a lone gate.

### 4.2 When a guard is owed (note 3)

> *"Need to emphasize to reviewers and builders - don't build a guard if the
> ingested data is already produced with sanity unless there is real risk of
> corruption (file on disk), or operation is critical on public infra where
> attack could be feasible."*

**Today.** The doctrine is scattered: the `antidote` skill (*"validate once at
the boundary, then trust the type"*); PROCESS.md:244-247 (right-sizing never
trims validation at trust boundaries); `AGENTS.template.md` (*"validate
schema/shape at the boundary"*); the reviewer prompt, which makes an added guard
name *"why the defect cannot be made UNREPRESENTABLE instead"*. What is missing is
the owner's concrete definition of **where the boundary is**.

**Where it must not go:** the `antidote` skill is vendored *"verbatim from
upstream"* (`.agents/skills/antidote/SKILL.md:11-17`), with three byte-identical
copies; editing it would falsify its provenance. And putting the rule in both a
skill and a prompt would state one rule twice.

**Recommendation.** One repository-owned home — PROCESS.md, beside the 0→A→B
rule it refines — linked from the reviewer and builder prompts rather than copied
into them:

> A guard is owed only where the input crosses a trust boundary — a file on disk,
> the network, a person, another process, or a model's output — or where the
> operation is irreversible or exposed to attack. Data this code produced
> in-process is trusted: fix the producer instead.

Two consequences to state with it: the kit's registries are hand-edited files on
disk, so validating them is owed; and a model's output is a boundary, so
validating structured output is owed too.

---

## 5. Questions for the owner

| # | question | recommendation |
|---|---|---|
| S1 | Extend the absolutes check to every tier's normative and acceptance cells, reusing `recorded waiver:`, with a defined suppression rule; run OI-37's sweep? | yes (§1.1) |
| S2 | LLR → design expectation: prose now, prefix a separate later decision; no edits to old logs? | yes (§1.2) |
| S3 | Design constraints: each a need, canonical in the need; the owner document as provenance only; schema ruled with the stakeholder list? | yes (§1.3) |
| S4 | Retired rows: keep deletion, and record structured retirement events from now on, outside the registries? | yes (§1.4) |
| S5 | Test level: give TCs a primary verification purpose before any ordering policy; treat the 41 tier disagreements as a priced migration, not a cleanup? | yes (§2.2) |
| S6 | Observation tests: design an event-triggered runner (state, owner, failure semantics) before approving triggers? | yes (§2.3) |
| S7 | One session service (act / keep / record), with WI-551 landing through it? | yes (§3.1) |
| S8 | Telemetry parity: a raw telemetry stream or structured output for codex and opencode, a provider column, and tokens kept distinct from context occupancy? | yes (§3.2) |
| S9 | Per-role command construction: restricted roles drop the bypass flag, and the orchestrator writes their verdicts? | yes (§3.3) |
| S10 | Retention: the adjudicator's lands; builder retention a separate ruled experiment; reviewers never? | yes (§3.4) |
| S11 | Keep the adjudicator's reviewed commit as the approval act; a mechanical trigger only as its own ruling with authenticated issuance? | yes (§3.5) |
| S12 | Fan-out: rule on peer-tier delegation; tiers not models; never from review roles; budgeted in the orchestrator? | yes (§3.6) |
| S13 | Plan and build: independent review with the planner's intent as a conformance checklist? | (c) (§3.7) |
| S14 | Operation count: define the measure first; paired and reported, never a lone gate? | yes (§4.1) |
| S15 | The guard rule in PROCESS.md, linked from the prompts, not in the vendored skill? | yes (§4.2) |

**Suggested order**, cheapest and most independent first: S15, S2 and S1 are
prose and a warn-first check; S7 and S9 reshape the session path together; S8
precedes any retention beyond the adjudicator (S10); S5 and S6 are designs to
settle before migrations.

---

## 6. Review round 1 — codex Sol, reasoning effort high (2026-09-23)

Verdict: *"REJECT as a decision basis in its current form. The approval-authority
reversal, nonexistent SR/DE test split, and retention/tool-control assumptions
must be corrected before the S1–S15 rulings are put to the owner."* 15 findings;
each checked against the code; all held.

| # | finding (short) | where it landed |
|---|---|---|
| 1 | a verdict file proves the bytes judged, not who held authority — it recreates OI-45's laundering surface | §3.5: keep the reviewed commit; a trigger needs its own ruling |
| 2 | "trunk-side" in the 2026-09-01 plan already means the exclusive lane; no amendment is owed | §3.5 |
| 3 | there is no SR-test vs DE-test population (182 of 194 TCs cite both) | §2.2 |
| 4 | 41 tier disagreements, not 35, and fixing them is a priced migration | §2.2 |
| 5 | a retained builder does not remove verdict-as-text; the adjudicator's dial should not widen silently | §3.4 |
| 6 | PROCESS.md also permits peer-tier fan-out; `subagent_gate` is Claude-only | §3.6 |
| 7 | a registry map changes no permissions; "read-only plus one file" is not expressible | §3.3 |
| 8 | no phase-close runner executes Inspections or Critiques | §2.3 |
| 9 | the absolutes checker scans only SR acceptance; the waiver grammar already exists; counts corrected | §1.1 |
| 10 | a retired-id index cannot be derived reliably from current sources | §1.4 |
| 11 | `antidote` is vendored verbatim; one rule in two places is two homes | §4.2 |
| 12 | the need is the canonical obligation; the document is provenance | §1.3 |
| 13 | codex's usage line is discarded before it could be parsed | §3.2 |
| 14 | the planner as a review leg is neither cost-neutral nor independent | §3.7 |
| 15 | the existing public-symbol count is not an operation count | §4.1 |
