# Owner notes, 2026-09-23 — spine semantics, sessions, and test strategy

**Status: PROPOSAL. Not a ruling.** A sister plan to
[the assumption-tier proposal](2026-09-20-validation-gap-and-the-assumption-tier.md).
It takes the owner's notes of 2026-09-23, which also affect this repo's scope
and need the same working-through the design assumptions did, and for each one
records what the repo does today (with anchors), what the note would change,
the trade-offs, and a recommendation. Nothing here is built; the questions in §5
are for the owner.

**Revised three times after adversarial review (2026-09-23, §6).** Three codex
Sol reviews (reasoning effort high) found 15, then 6, then 3 problems. The first rejected the
draft as a decision basis: it had the approval-authority question wrong, inferred
a test split the registry does not contain, and understated what several
recommendations need. The second and third confirmed the earlier fixes and
found six, then three, residual problems. Every finding was checked against the
code; all held, and each is applied below.

**Owner responses, 2026-09-23.** The owner answered most questions; each response sits at the end of its section, and §5 is re-posed from them.

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
1. Extend the check beyond SR acceptance, warn-first, tier by tier:

   | tier | cells scanned | waiver lives in |
   |---|---|---|
   | need | `need`, `acceptance` | `why` |
   | system requirement | `requirement`, `acceptance_criteria` | `rationale` |
   | design expectation (LLR) | `detail` | `rationale` |
   | test case | **not scanned** — a TC states a method, not an obligation (`trace_text.py:889-891`), and it has no reason cell; adding one would be a schema migration for no gain | — |

2. Reuse the **existing waiver grammar**, `recorded waiver: <reason>`, in the
   cell above — no second waiver vocabulary.
3. Define the suppression predicate before shipping: an absolute is satisfied
   when it names its domain from a closed list (a registry, an id space, a
   declared set), and the tokenization is documented. What cannot be decided
   mechanically — whether a named domain is really closed — stays a review
   question in the spine-authoring skill.
4. Run the OI-37 sweep the ruling asked for, needs first, as its own work item.

**Owner response (2026-09-23):** *"I'm okay with the recommendation."*

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

**Owner response (2026-09-23):** *"Okay with the recommendation."* It ships in
the assumption-tier plan's terminology package (its §11 T), with Q9's SR
wording.

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
2. The owner's constraints document is provenance only. The need cites the
   specific constraint's anchor in a separate cell, not in its text — **on the
   need, not on the stakeholder row**, because the provenance is per constraint,
   not per stakeholder. The assumption-tier plan's stakeholder list (its §6.2)
   was revised to match, so there is one home.
3. Hats reference the need, not the prose.
4. Priced separately and ruled with the assumption-tier plan's stakeholder list
   (its Q12): the new need cells, their carrier and template entries, dogfood
   sync, and whichever renderer or check consumes them.

**Owner response (2026-09-23): "doesn't this then surface each hat as a
stakeholder?"** No, and the recommendation is sharpened so it can't. There are
three separate things:

| thing | what it is | example |
|---|---|---|
| **stakeholder** | who owns an outcome: one row each | the owner; the adopting team; a reviewer |
| **need** | what a stakeholder owns, and **a design constraint is one of these** | *"a reader two years later can tell why a piece of code exists"*, stakeholder = the owner |
| **hat** | a question put to each decomposition (`hats.toml`: *"a HAT IS NOT A PERSON AND NOT A STAKEHOLDER ROW"*) | MAINTAINER asks *"can a reader two years from now tell why this exists?"* |

So the owner is **one** stakeholder with many constraint-needs; no hat gains a
stakeholder row. A hat that applies a constraint cites that need. A hat gets
`speaks_for` only when it voices a real stakeholder (FIRST-RUN-ADOPTER speaks
for the adopting team, assumption-tier plan §6.5).

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

**Recommendation — an explicit, small amendment to D-4.** Keep deletion; add a
structured retirement record. D-4 says history lives in *"git and the log"*, so a
new structured record is a third home, and the owner should see it as an
amendment rather than a clarification. The lightest form keeps it inside the
existing log: a **structured fragment in `docs/log.d/retired/`**, written in
the same commit as the deletion, with a fixed shape — id, date, successor if
any, reason. The subdirectory matters: `trunk_step.py` folds every top-level
`docs/log.d/*.md` into `log.md` and deletes it, and its glob does not recurse
(S4, 2026-09-24). Two details follow:

- **No self-referential hash.** A commit cannot contain its own hash, so the
  record does not store the deleting commit; the dashboard resolves it at render
  time from git when history is available (`git log` over the fragment), and
  shows *unknown* in a shallow or squashed clone.
- **Append-only by check**, not by trust: a warn-first finding when a retirement
  fragment is edited after it lands, and when a spent id has no fragment from the
  day the rule starts. Retirements before then show as *unknown*.

It costs a fragment shape, a check, a renderer, an `orphans-allow` line for
the subdirectory, and a template/resync entry.

**Owner response (2026-09-23): acceptable, on condition that agents don't go
diving into history just because it exists.** Retirement fragments are for
**lookup, not browsing**: an agent that meets a spent id reads that id's
fragment, and never surveys the set. Only the dashboard renderer reads them all.
This goes in the kit's list of reference-not-working surfaces, beside
`docs/archive/`. It is prose; nothing can mechanically stop a session reading a
file. Its home is PROCESS.md, because `AGENTS.template.md` has 20 B of headroom.

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

**Recommendation — a three-way decision, and the cheap branch is the
recommended one.**

| option | what it takes |
|---|---|
| **(a) drop the ordering idea** — keep every test in the commit bar, as today | nothing |
| (b) add a primary-purpose field to every TC and backfill it | an **approval-bearing** migration: unknown columns default to approved content (`acceptance_record.py:212-219`), and 184 of the 194 TCs are Approved, so up to 184 rows are judged by hand and re-attested — plus carrier, template, renderer and check changes; or splitting mixed TCs into new ids |
| (c) a different carrier for test purpose, outside the approved cells | a design, and an argument for why it is not approval-bearing |

**Recommend (a).** The saving the note hopes for is small — every test already
runs in the bar — and (b)'s cost is close to a whole-registry re-attestation.
Revisit only if a measured benefit appears.

Separately: reconciling the 41 tier disagreements is **not a data cleanup**. Moving slow
   evidence into smoke can break the 60-second budget; changing an approved TC's
   tier amends an approved row and needs re-attestation; and the TC-to-test
   relation is many-to-many, so no trivial derived mapping exists. Decide
   separately what the meta-repo's budget partition means against the shipped
   tier contract, then price the migration.

**Owner response (2026-09-23): a new idea. If a work item only touches one
module, run only the test suites around that module.** This is test-impact
selection, which the kit has **ruled against** as the commit bar
(`PROCESS_OPTIONS.md:2037-2041`): *"a missed transitive dependency passes
silently and the coverage floor breaks"*. The sanctioned cheap layer is the
smoke tier, which runs in about 28 s against its 60 s budget (CLAUDE.md). So
the saving is small and the risk is a silent green. Two ways it could still
enter:

| option | what it is | cost |
|---|---|---|
| (d) **an inner loop only** | the builder runs the module's own tests first for fast feedback; the smoke bar still runs before every commit | nothing is weakened; the gain is a few seconds per iteration |
| (e) **replace the bar** | a module-scoped subset is the commit bar | reverses the ruling; a change that breaks another module through a shared import commits green |

(d) is harmless and optional; (e) is not recommended.

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

**Owner response (2026-09-23): "what does content change mean? Each iteration
of a new feature, even before a review completes? That's unstable, because a
review may surface issues a test doesn't."** As first drafted, yes: a content
hash changes on every commit that touches what the check reads, mid-work-item
included. The recommendation is revised:

- **Triggers are evaluated only at stable checkpoints:** a work item merging to
  trunk after review and adjudication, phase close, and release. Never per
  commit inside a lane.
- **"Content change" means different from the state the check last judged**,
  compared at the checkpoint, so a feature's intermediate iterations never
  fire it.
- **One result record, shared with the assumption tier.** The assumption-tier
  plan has decided (its Q22, Q25) that judgment-based evidence lives in a result
  record keyed by TC, with an author-proposed `max_age` of at least 7 days, and
  that expiry reverts evidence to *specified* and never falsifies. This runner
  reads and writes that record, so there is one home for "when was this last
  judged". The two plans design it once, before the assumption tier's C3.
- **One freshness model.** The shared record stores a digest of the state it
  judged. At a checkpoint the check is due when that digest no longer matches
  what it reads, or when its `max_age` has passed, whichever comes first.
  Automated evidence stays tree-bound in `docs/test/evidence`, as today.

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

**Owner response (2026-09-23): option (a), "refactor as much as possible to
reduce individual or custom code components."** So the service is the one path
for every session, and the refactor's measure is how much per-role and
per-provider code it removes, following PROCESS.md §3's 0→A→B rule:

- **act:** a role differs only in data (brief, route, tier, tool set), never in
  its own launch code;
- **keep:** WI-551 lands through the service; the keep-warm ping is an ordinary
  recorded call, not a direct `run_session` call;
- **record:** one writer replaces the loop's in-line logging and
  `invoke_and_persist`, and S8's adopted schema is written there;
- **provider differences** live in one adapter per provider (argument
  building, output and usage parsing), not scattered through role code;
- S10's retention is a service operation, not a per-role addition.
- **Schema-neutral, so it can proceed now** (review 5): the service ships with
  today's recorded fields. S8's adopted schema later changes only the record
  step's writer, and S10's operation is added when it is cleared. Nothing in S7
  waits on them.

The loop's C901 complexity pin (`tests/test_complexity_ratchet.py`) still
applies: decompose, don't re-stamp.

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

**Owner response (2026-09-23): "this isn't a novel problem. Isn't there
existing research on CLIs, cache hits, and recording fresh versus cached tokens?
Do we need to spawn researchers?"** Agreed that it isn't novel, so the
recommendation changes from designing a log format to **adopting existing
conventions**. Prior art to confirm (from memory, not yet verified here):

- OpenTelemetry's generative-AI semantic conventions define token-usage
  attributes;
- Claude Code can export OpenTelemetry metrics with token counts split by type
  (input, output, cache read, cache creation);
- codex's non-interactive JSON output reports usage, including cached input
  tokens;
- community tools (usage analysers over Claude Code's local logs, and
  multi-provider proxies) already normalise these across providers.

**Proposed: one bounded research pass, not a team.** One question: for each
routed CLI (Claude Code, codex, opencode), what structured usage does it emit
(fresh input, cache read, cache write, output, reasoning), how is it captured
non-interactively, and which published schema should the index adopt? Output: a
field map plus one recorded fixture per CLI. S8 then becomes "adopt that
schema", and the §3.2 items become its implementation.

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

**Recommendation — split roles by what they do, not by what they are called:**

| role | behaviour | tools |
|---|---|---|
| REVIEW-A, REVIEW-B, CRITIQUE, PROBE | judge and report — but a reviewer also **runs the harness and drives real code paths** (`reviewer.template.md:39-41`) | **non-mutating, not read-only**: it must still execute tests and write temporary files; what it must not change is the tree under review (below) |
| BUILD | writes code and rows | full |
| DESIGN-CHECK | a **rework** session: its commit is the rework and arms the next review (`PROCESS_OPTIONS.md:1128-1139`; `agent_loop.py:3047-3061`) | full |
| ADJUDICATE | performs the approval act: the verdict, the scoped Status flips, the snapshot, the dispositions and close — the writes §3.5 keeps it doing | bounded write |

**Why "read-only" is the wrong tool for reviewers.** The third review was
right: a reviewer must run the harness, so a read-only sandbox (or a
`Read,Grep,Glob` allow-list) stops it doing its job; and the loop treats a
missing verdict file as a failed draw that is cooled and rerouted
(`agent_loop.py:2552-2573`). The verdict file is also a ruled carrier: OI-76
makes the gate consume round files from logged reviewer sessions, bound to the
tree they reviewed.

**The simpler mechanism: a disposable copy.** Run each review-type session in a
**throwaway worktree at the same commit** as the tree under review. It can run
anything and write anywhere; when it ends, the coordinator collects its verdict
file, commits it into the lane beside the scoreboard and trailer it already
writes (`agent_loop.py:2726-2744`), and discards the copy. So:

- no provider-specific sandbox is needed to stop reviewers editing the tree —
  their edits never reach it;
- the verdict is still the logged reviewer session's own file, bound to the same
  tree SHA — **OI-76's attestation is preserved**; what changes is only who
  commits the file (the coordinator, not the reviewer), which should be recorded
  as a small amendment to OI-76's workflow;
- a malformed or missing verdict keeps today's failure semantics (a failed draw).

It costs a disposable-worktree step in the coordinator, the collection and
commit, and tests on each supported provider. Dropping the bypass flag for these
roles becomes optional hardening rather than the mechanism.

The adjudicator keeps its own reviewed writes; design-check and build keep full
tools.
3. A declared **phase → skills** map, named in the brief, so discovery can be
   switched off for review roles.

**Owner response (2026-09-23): agreed in practice, with a worry that it could
get out of hand.** Proposed guardrails: pilot on **one** role (REVIEW-A) before
the others; build the disposable-worktree step once, inside the session service
(§3.1), not per role; and measure the added time and disk per review. If the
pilot costs more than it saves, stop.

**Owner ruling (2026-09-23): verify, don't isolate.** The disposable worktree,
its pilot and both prerequisites below are **withdrawn**. The owner's model:
a reviewer works and commits in the lane as today, so OI-76 is unchanged; the
lane is then locked, and the adjudicator's final pass verifies the worktree's
state before setting the flag that triggers the mechanical merge (§3.5). What
makes that verification mechanical:

- a check refuses a reviewer-authored commit that touches anything but its own
  verdict file;
- a tree left dirty after a review session is flagged;
- the adjudicator's pass on the locked lane reads both before setting the
  merge flag.

This removes the per-provider worktree machinery the owner worried could get
out of hand. It depends on the lane commits carrying who authored them, which
the loop's session trailers are the start of; confirming they identify the
reviewer role is part of the work.

*Withdrawn, kept for the record:*

**Two prerequisites before the pilot (review 5):**

- **An OI-76 amendment, ruled by the owner (S16).** OI-76 binds the verdict
  to the logged reviewer session and the tree it reviewed; the pilot changes
  who *commits* that file (the coordinator, not the reviewer).
- **A measurable stop rule (S17).** Proposed: over the first 10 REVIEW-A
  rounds, record per round the added wall time and disk, failed draws, and
  any reviewer write that would have reached the tree. The pilot succeeds
  when no reviewer write reaches the tree and failed draws do not rise; it
  stops when the added wall time exceeds a threshold the owner sets, as a
  share of the median round. The coordinator records the numbers; the owner
  decides.

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

**Owner response (2026-09-23):** *"Agreed with the recommendation."*

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

**Owner response (2026-09-23): "a mechanical layer is still the right
method, so that a work item lands fully in a single commit to the working
branch, not several (changes + status + iteration)."** That separates two
things the note ran together. The first is compatible with everything above;
the second is where OI-45's objection bites:

| option | what is mechanical | the approval act | cost |
|---|---|---|---|
| **(i) squash on merge** | the merge slot squashes the lane (changes, the adjudicator's status-and-snapshot commit, the iteration logs) into **one** trunk commit per work item | unchanged: the adjudicator's reviewed commit, carried inside the squash | anything keyed to a lane commit's hash (trailers, handback reports, a verdict's recorded revision) points at commits that are no longer in trunk's history unless the lane branch is kept; each record needs checking. The **claim commit** also lands on trunk separately, because other lanes must see the claim (`integrate.py:700-704`); in this one-lane repo it could perhaps fold in, which needs checking |
| (ii) a machine approval writer | a script flips Status from a verdict | moves to the script | OI-45: *"what recorded human act authorizes a machine to move the approval record"*; its own ruling (item 3 above) |

**Recommend (i)** if the goal is one commit per work item. It keeps a
mechanical layer and leaves the approval act where it is.

**The owner's model, stated with S9's ruling (2026-09-23):** the adjudicator
reviews the locked lane and, in its reviewed commit, sets the flag that
activates the mechanical merge. That is (i): the flag rides the approval act
the adjudicator already makes, and the merge that follows is mechanical. It is
not (ii), because no script writes an approval.

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
3. **Never from review, critique, design-check or adjudication sessions.** This
   is **prose, not enforcement**, until item 4's design lands: no role is denied
   spawn tools today, and a disposable worktree (§3.3) stops edits, not fan-out.
   Denying spawn tools per provider (Claude's `--tools` allow-list is separate
   from its restricted mode; codex and opencode need their own) is part of that
   design, with fail-closed tests per provider.
4. **Budgets need an observability design first.** Provider-neutral accounting
   assumes a boundary the session engine does not have: `subagent_gate` sees only
   Claude's `Task`/`Agent`, codex routes have no structured stream, and a
   successful codex call returns only its last message. So a fan-out budget is
   contingent on a separate design — the spawn boundary, how a budget is
   inherited, per-provider adapters, what happens when a spawn cannot be observed
   (including whether native in-session delegation is disabled then). Until then,
   the prose rules (1–3) carry it, and the Claude hook stays as Claude-only
   *"supervision, not security"*.

**Owner response (2026-09-23):** *"I'm okay with the recommendation in
principle."*

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

**Owner response (2026-09-23): "builder bias is still the main concern.
Shouldn't the work item ultimately contain the expectation the reviewer can
reference?"** Largely, it already does. The reviewer brief makes each work
item's spec **Done-when** list the checklist (*"map each spec Done-when item to
its covering test or call it UNCOVERED"*), and forbids the builder's
self-assessment (*"Do NOT read or trust the implementer's own session notes"*,
`reviewer.template.md:39`). What is **not** ruled is who writes Done-when, and
whether the builder can change it:

- the planner writes Done-when **before** the build starts;
- a lane whose own diff edits its spec's Done-when is flagged to the reviewer
  and the adjudicator, since that is the builder moving the goalposts.

That is option (c), made concrete. S13 is re-posed on those two points.

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

**Owner response (2026-09-23): "not even sure how it should be assessed. Code
is minimised when the number of clock cycles falls, because that implies a
simpler execution stream over the envelope, and even that is hard to evaluate
across the distribution of pathways. Certainly not public APIs, since those
still allow internal call abuse."** That moves the measure from static to
**dynamic**:

| candidate | what it counts | problem |
|---|---|---|
| public symbols (today, reported) | module-level names | rejected by the owner: internal call abuse is invisible to it |
| static call graph | distinct callable operations | counts what *could* run, not what does |
| **executed operations over a declared workload** | calls or bytecode instructions actually run (stdlib `cProfile` on Python 3.11) | the workload must stand in for the real distribution of paths; the test suite is not that distribution; noisy between runs |
| wall-clock or CPU time | cycles, as the owner framed it | dominated by I/O and machine noise; cheaper is not the same as simpler |

No candidate is ready. The honest recommendation is to **park it as a research
item**. If it is pursued, the measure is executed operations over a declared,
versioned workload, reported as a trend beside the existing caps, and never a
gate.

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

**Owner response (2026-09-23):** *"Agreed."*

---

## 5. Questions for the owner

Re-posed after the owner's responses of 2026-09-23. `DECIDED` means the work
may proceed as written; `CONDITIONAL` means decided with the stated condition;
`RE-POSED` means the response changed the question, which is restated here.

| # | question | standing |
|---|---|---|
| S1 | Extend the absolutes check per the tier matrix (TCs excluded), reusing `recorded waiver:`, with a defined suppression rule; run OI-37's sweep? (§1.1) | **DECIDED**: yes. |
| S2 | LLR → design expectation: prose now, prefix a separate later decision; no edits to old logs? (§1.2) | **DECIDED**: yes. Ships in the assumption-tier plan's terminology package (its §11 T), with Q9. **Flagged 2026-09-24** (not reopened): "expectation" also appears as ordinary wording inside need rows, in the kit's needs template and in adopters; recommended: keep the name with a glossary line ([review pack](2026-09-24-owner-review-pack.md) A3). |
| S3 | Design constraints: each is a need whose stakeholder is the owner, canonical in the need; provenance anchor on the need; **no hat becomes a stakeholder**; schema ruled with the stakeholder list? (§1.3) | **RE-POSED** after the owner asked whether hats become stakeholders (they don't). Rule with the assumption-tier sitting; if ruled, the provenance cell lands in its C1. Facts and options: [review pack](2026-09-24-owner-review-pack.md) B5. |
| S4 | Retired rows: keep deletion, and amend D-4 to add a structured retirement fragment in `docs/log.d/`? (§1.4) | **CONDITIONAL**: yes, provided the fragments are lookup-only for agents (stated in PROCESS.md, not AGENTS). **Home revised 2026-09-24** (reopened because `trunk_step` compiles and deletes every top-level `docs/log.d/*.md`; owner accepted [review pack](2026-09-24-owner-review-pack.md) A2): the fragments live in `docs/log.d/retired/`, which the non-recursive fold skips; the template gains an `orphans-allow` line for it. |
| S5 | Test level: keep every test in the commit bar (a); optionally let builders run a module's own tests first as an inner loop (d), never as the bar; reconcile the 41 tier disagreements as a priced migration? (§2.2) | **RE-POSED** with the owner's module-scoped idea as (d) and (e). Recommend (a) plus optional (d); not (e), which reverses the test-impact ruling. Facts and options: [review pack](2026-09-24-owner-review-pack.md) B7. |
| S6 | Observation tests: evaluate triggers only at checkpoints (work-item merge, phase close, release), "content change" meaning changed since last judged, sharing the assumption tier's result record? (§2.3) | **RE-POSED** after the owner flagged per-iteration firing as unstable. One freshness model: the shared record's judged-state digest, or `max_age`, whichever trips first. Design jointly with the assumption tier, before its C3. Facts and options: [review pack](2026-09-24-owner-review-pack.md) B4. |
| S7 | One session service (act / keep / record), with WI-551 landing through it? (§3.1) | **DECIDED**: (a), with the owner's direction to consolidate as far as possible: shared stages over per-role or per-provider code. It is schema-neutral and proceeds now: S8's schema and S10's retention are added to it when each is cleared. |
| S8 | Telemetry: run one bounded research pass on each routed CLI's structured usage output and a published schema, then adopt that schema, with a provider column and tokens kept distinct from context occupancy? (§3.2) | **RE-POSED**: adopt existing conventions rather than design one. Awaiting a go for the research pass. Facts and options: [review pack](2026-09-24-owner-review-pack.md) B6. |
| S9 | How are reviewers kept from changing the work they review? (§3.3) | **DECIDED 2026-09-23: verify, don't isolate.** Reviewers work and commit in the lane as today (OI-76 unchanged); a check refuses a reviewer commit touching anything but its verdict file and flags a dirty tree; the adjudicator verifies on the locked lane before setting the merge flag. Replaces the disposable-worktree proposal. Mechanism still open: what the check keys on (the coordinator's recorded session range) and who makes the final pass on a build lane, where no adjudicator runs ([review pack](2026-09-24-owner-review-pack.md) B2). |
| S10 | Retention: the adjudicator's lands; builder retention a separate ruled experiment; reviewers never? (§3.4) | **DECIDED**: yes. |
| S11 | One trunk commit per work item: squash the lane in the mechanical merge, keeping the adjudicator's reviewed commit as the approval act inside it (i), or a machine approval writer (ii)? (§3.5) | **RE-POSED**; the earlier leaning to (i) is **superseded pending the owner** by the 2026-09-24 facts (review pack B1, which separates a readable history from an actual single commit): the owner's model has the adjudicator's reviewed commit set the merge flag and the merge follow mechanically, which is (i). Still to check: what is keyed to lane commit hashes, and whether the claim commit can fold in. (ii) stays its own ruling under OI-45. Facts and options: [review pack](2026-09-24-owner-review-pack.md) B1. |
| S12 | Fan-out: rule on peer-tier delegation; tiers, not models; never from review roles; budgets only after an observability design? (§3.6) | **DECIDED in principle.** |
| S13 | Builder bias: the planner writes the work item's Done-when before the build, and a lane that edits its own Done-when is flagged to the reviewer and adjudicator? (§3.7) | **RE-POSED** from option (c): the reviewer already judges against Done-when; what is left is who writes it and whether the builder can move it. Facts and options: [review pack](2026-09-24-owner-review-pack.md) B3. |
| S14 | Operation count: park as research; if pursued, executed operations over a declared workload, reported beside the caps, never a gate? (§4.1) | **RE-POSED**: the owner rejected public-symbol counts and framed it as execution cost. Facts and options: [review pack](2026-09-24-owner-review-pack.md) B7. |
| S15 | The guard rule in PROCESS.md, linked from the prompts, not in the vendored skill? (§4.2) | **DECIDED**: yes. |
| S16 | Amend OI-76 so the coordinator, not the reviewer, commits a reviewer's verdict file? (§3.3) | **WITHDRAWN 2026-09-23**: S9's ruling keeps reviewers committing their own verdicts. |
| S17 | S9's pilot stop rule? (§3.3) | **WITHDRAWN 2026-09-23**: no pilot under S9's ruling. |

**Order, revised.** Now: S15, S2, S1 (prose and a warn-only check). With the
assumption-tier sitting: S3. Designed together before the assumption tier's
C3: S6. Once the research pass lands: S8, which gates any retention beyond the
adjudicator. S7 proceeds now and is schema-neutral; S9's reviewer-commit check
and S11's merge flag and squash fold into the same work, since both sit on the
lane-to-trunk path.

---

## 6. Review log

### 6.1 Round 1 — codex Sol, reasoning effort high (2026-09-23)

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

### 6.2 Round 2 — codex Sol, reasoning effort high (2026-09-23)

A convergence round. Verdict: *"NOT YET SOUND — S9 contradicts two implemented
mutating roles, while S4 and S12 still assume ruling compatibility or
orchestration machinery the repository does not have."* It reproduced the
round-1 counts and confirmed the round-1 fixes landed, and found six residual
problems; each was checked and applied.

| # | finding (short) | where it landed |
|---|---|---|
| 1 | the adjudicator cannot be read-only: it performs the approval act's writes | §3.3 roles by behaviour |
| 2 | design-check is a mutating rework role | §3.3 |
| 3 | a retirement record amends D-4, and a commit cannot contain its own hash | §1.4: an explicit amendment; hash resolved at render time |
| 4 | provider-neutral fan-out budgets assume machinery that does not exist | §3.6: contingent on an observability design |
| 5 | constraint provenance had two candidate homes across the two plans | §1.3, and the assumption-tier plan §6.2 |
| 6 | an all-tier absolutes rule needs a per-tier matrix; TCs have no reason cell | §1.1 tier matrix, TCs excluded |

### 6.3 Round 3 — codex Sol, reasoning effort high (2026-09-23)

Verdict: *"NOT YET SOUND — S9/S12 still assume an unbuilt portable restriction
and verdict-recording mechanism, while S5 omits a near-whole-registry approval
migration."* It reproduced every count and confirmed the round-2 corrections
match the implementation, and found three residual problems; each was checked
and applied.

| # | finding (short) | where it landed |
|---|---|---|
| 1 | reviewers must run the harness and commit a tree-bound verdict (OI-76); read-only breaks that | §3.3: a disposable worktree at the same commit; the coordinator commits the verdict |
| 2 | "those roles cannot spawn anyway" was false | §3.6: prose until the observability design, with per-provider spawn denial in it |
| 3 | a TC purpose field is an approval-bearing migration of up to 184 approved rows | §2.2: a three-way decision; recommend dropping the ordering idea |

The applied fixes were not put through a fourth round.

### 6.4 Round 4 — codex Sol, reasoning effort high (2026-09-23)

A decisions check across both plans and the briefing after the owner's answers
(logged in full in the assumption-tier plan's §12.7). The findings that touch
this plan, each checked and applied:

| # | finding (short) | where it landed |
|---|---|---|
| 1 | S6's "changed since last judged" had no judged state in the shared record | §2.3 one freshness model; assumption-tier §7 |
| 2 | S3's provenance cell was scheduled in neither plan | S3 row; assumption-tier C1 |
| 3 | S2 had no implementation package | S2 row; assumption-tier §11 T |
| 4 | S7 was DECIDED while containing unresolved S8, S9 and S10 | §3.1: schema-neutral, proceeds now |
| 5 | S9's stop rule had no measure, threshold or owner | §3.3; S17 |
| 6 | S9 needed an OI-76 amendment with no question | §3.3; S16 |
| 7 | S1, S2, S10, S12, S15 were DECIDED with no recorded owner response | responses added at the end of §1.1, §1.2, §3.4, §3.6, §4.2 |

### 6.5 Adopter cross-check and research (2026-09-24)

Four read-only passes prepared the owner's next review; results, options and
recommendations are in the [owner review pack](2026-09-24-owner-review-pack.md). For this plan:
S4 is REOPENED and S2 flagged (pack A2, A3); S9's mechanism has two open points
(pack B2); every re-posed item has researched facts (pack B1, B3–B7); and
S11's facts argue against squashing (pack B1). Seven defects the research
surfaced are listed in pack Part C.
