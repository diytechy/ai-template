# Blind derivation A — outside-in capability breakdown

**Derivation date:** 2026-08-16 · **Team:** A (clean-room, blind) · **Axis:**
outside-in, actor/crossing-driven.

## Blind input set

Exactly three inputs were read:

1. `README.md` — the `PROJECT-VISION` tag and intro.
2. `docs/requirements/stakeholder-needs.toml` — 27 core needs (SN-001…SN-012,
   SN-023…SN-029, SN-033…SN-040) plus the NG-1 non-goal.
3. `docs/requirements/external.toml` — the locked depth-0 frame: 5 entities,
   6 crossings (B-01, B-02, B-04, B-05, B-06, B-07), 3 relationships.

**Disclosure.** The README read ran past the intended stop point (the intro) into
its "headline pieces" bullets, which name concrete scripts and files. Those names
and the design detail around them were deliberately **excluded** from this
derivation; nothing below is phrased from them, and no row names a file. No other
repo file was opened — no requirement, interface, test, component or process
registry, no log, no status, no plan, no history.

## Method

For each external entity and each crossing it owns, I asked: *what must the
system deliver at this crossing so the needs that cite this actor are satisfied?*
Capabilities are grouped by the crossing/actor they serve, in capability /
artifact-class voice — each row must hold for **all** acceptable implementations,
so no row names a script, file or command. Scope is capped to the needs as
written; where a need demands something the frame gives no crossing for, it is
recorded as a **tension** (§Tensions) rather than answered with invented scope.

Two structural facts of the frame shape the result and should be read before the
table:

- **B-05 carries almost everything.** The system's deliverable *is* the package,
  so most needs land as *properties of delivered content* rather than as separate
  crossings. The frame itself decomposes B-05 into six bundles (harness verdict,
  scaffold, unattended loop, generators, hook floor, package-wide property); the
  B-05 group below follows that grain.
- **The self-adoption path is not a crossing.** REL-002 puts this repository's own
  status/dashboard/console surfaces *outside* the system, and REL-003 puts the
  model-provider surface outside it too. Needs that read like "a reviewer sees X"
  or "the loop talks to a provider" therefore become obligations on delivered
  content, verifiable in that content's own records — see T-1 and T-4.

---

## Group 1 — EXT-001 Development session · crossings B-01 (in), B-02 (in), B-04 (out)

| ID | Obligation (one shall) | SNs | Crossings | Observable |
|---|---|---|---|---|
| **A-1** | The system shall admit an edit into governed state only after that edit has passed every declared admission check, and shall refuse the write otherwise. | SN-005, SN-008, SN-009, SN-002 | B-01, B-04 | On an un-bypassed write path, 100% of candidate writes carrying a declared violation class are refused; 0 admitted. |
| A-1.1 | It shall screen every candidate write's content, message and outgoing range against the always-on secret classes, adding the identity/personal-data classes when the declared dial enables them, in every repository with no adopter setup step. | SN-009 | B-01, B-04 | A seeded secret in any of the three surfaces is caught on a default scaffold with zero configuration actions performed. |
| A-1.2 | It shall apply the fast process floor — format, spine integrity and the checks the in-process gate requires — to each candidate write. | SN-004, SN-005, SN-008, SN-002 | B-01 | A write that breaks the spine join or the in-process gate's required step is refused at admission, not at a later stage. |
| A-1.3 | Every refusal shall name the failing check and locate the offending row or phrase. | SN-008, SN-005 | B-04 | Each refusal message identifies check + location; a refusal with neither is a defect. |
| A-1.4 | The admission checks shall apply identically regardless of which session originated the write, human or any agent family, and per-agent configuration shall mirror the floor without being able to replace or weaken it. | SN-005 | B-01, B-04 | Identical candidate writes from differently-configured sessions produce identical verdicts; removing a per-agent config changes no verdict. |
| **A-2** | The system shall return an explicit allow/deny verdict to the acting session at the moment of each guarded act, such that no guarded act completes verdict-less. | SN-005, SN-008, SN-006 | B-04 | Every guarded act in a session yields exactly one determinate verdict; count of verdict-less guarded acts = 0. |
| A-2.1 | It shall state, as part of the same obligation, that the session-local verdict is bypassable and is therefore paired with the hosted re-run of the same bar (A-19.4) rather than claimed sufficient alone. | SN-005, SN-008 | B-04, B-07 | A write admitted via a local bypass is still caught by the hosted re-run before it can be treated as validated. |
| **A-3** | The system shall accept ratification, ruling and status-advancing input only through the declared human-authority channel, and shall treat every other actor as unable to advance a reserved tier. | SN-004, SN-029, SN-028 | B-02 | An automated actor attempting a reserved-tier advance is refused in 100% of attempts. |
| A-3.1 | It shall determine from a single declared cumulative level which tiers a human still ratifies, compare that against a separately derived in-process stage, and hold exactly those tiers. | SN-029, SN-004 | B-02 | For each declared level 0–4, the set of held tiers matches the level's definition exactly; no fourth interpretation of the same word exists. |
| A-3.2 | On a tier released to automation, it shall append a durable approval record naming the row, the transition, the acting reviewer and the commit, distinguishable from a human approval by query. | SN-029 | B-02 | Every released-tier approval has a matching record; a query separates automated from human approvals with no manual reading. |
| A-3.3 | It shall anchor each acceptance on the accepted artifact's own row — the commit carrying the accepted text plus a digest of that row's normative cells — and surface any later divergence of that text regardless of status movement. | SN-029, SN-002 | B-02, B-01 | Editing an accepted row's normative text without re-acceptance drops the derived stage, even when status is flipped in the same change. |
| A-3.4 | Every unreadable, out-of-range or wrong-typed authority input shall resolve toward more human involvement, never less. | SN-029, SN-008 | B-02 | Over an adversarial input table, 100% of malformed inputs fail toward the more-human outcome; 0 fail open. |

## Group 2 — EXT-002 Template · crossing B-05 (out)

### 2a. Scaffold bundle

| ID | Obligation (one shall) | SNs | Crossings | Observable |
|---|---|---|---|---|
| **A-4** | The package shall deliver a single-action capability that installs the gated, requirement-traced process into a new or existing repository such that the resulting repository's harness passes immediately, with no tooling hand-built by the adopter. | SN-001, SN-034 | B-05 | A freshly installed target repository's harness returns pass on first run, with zero manual construction steps. |
| A-4.1 | Re-application onto an existing repository shall replace only package-owned artifacts and shall preserve every adopter-authored file. | SN-001 | B-05 | After re-application, adopter-authored files are byte-identical; only package-owned files differ. |
| A-4.2 | Installation shall omit artifacts specific to a stack the declared target does not use. | SN-003 | B-05 | A non-reference-stack installation contains zero reference-stack-only artifacts. |
| A-4.3 | Installation and the documented re-sync shall convert any legacy scattered policy declarations into the single declared dial home, so an adopter never encounters the duplicate-declaration refusal unaided. | SN-028 | B-05 | Installing over a repository holding legacy scattered declarations yields a repository that passes the duplicate-declaration check with no adopter intervention. |

### 2b. Harness-verdict bundle

| ID | Obligation (one shall) | SNs | Crossings | Observable |
|---|---|---|---|---|
| **A-5** | The package shall deliver a harness that, given a named gate, executes exactly that gate's required steps and returns a single pass/fail verdict. | SN-004, SN-008, SN-012 | B-05 | For each named gate, the executed step set equals the declared required set; verdict is binary and total. |
| A-5.1 | A required step whose tool is absent shall **fail**, never be silently skipped; the one sanctioned degrade to skip shall be an explicitly-requested local mode that is never a gate or hosted default. | SN-004, SN-008 | B-05 | With a required tool removed, the default invocation fails; only the explicit opt-in degrades, and it is absent from every gate/hosted default path. |
| A-5.2 | The toolchain the harness invokes shall be declared once in a repository-local declaration, so that swapping stacks edits that declaration and no package script. | SN-003 | B-05 | A stack swap performed by editing only the declaration yields a passing harness; package scripts unmodified. |
| A-5.3 | It shall offer declared cost tiers such that each moment (per-change, slice close, release) has exactly one definition of passing. | SN-005, SN-012, SN-007 | B-05, B-06 | For each declared moment, exactly one tier is assigned; two readers of the moment table select the same tier. |
| A-5.4 | It shall detect, at the declared gate, work that presents as complete while carrying a stub or an unmet acceptance criterion, and shall fail on detection. | SN-008 | B-05 | A seeded stub or unmet criterion turns the gate verdict red; a green with a seeded stub present is a defect. |

### 2c. Verification-of-the-chain bundle

| ID | Obligation (one shall) | SNs | Crossings | Observable |
|---|---|---|---|---|
| **A-6** | The package shall deliver a capability that mechanically joins the need→requirement→design→test chain and reports every orphan, so trust in the chain rests on the join rather than on assertion. | SN-002, SN-007 | B-05 | Strict join over a complete chain reports zero orphans; a deliberately unlinked row is reported. |
| A-6.1 | A gate shall pass only when the join reports zero orphans. | SN-002, SN-004 | B-05 | Introducing one orphan turns the gate red 100% of the time. |
| A-6.2 | A malformed or duplicated identifier shall fail at any stage that reads it. | SN-002 | B-05 | Each of malformed-id and duplicate-id fails at every reading stage, not only the first. |
| **A-7** | The package shall deliver checks that judge how requirements are *authored*, not only whether they link. | SN-033, SN-036, SN-039 | B-05 | Each declared authoring rule has a check that reports a violating row by id and phrase. |
| A-7.1 | It shall report any stakeholder-need statement that carries an internal path, an implementation-only identifier or a process citation, honoring a reviewed exception list for names that are themselves user-facing interfaces. | SN-033 | B-05 | A need cell containing an internal path is reported with row and phrase; an exception-listed name is not. |
| A-7.2 | It shall require every non-example need row to carry a scope value drawn from a closed vocabulary, and shall report a missing or invalid value. | SN-039 | B-05 | A need row lacking scope, or carrying a value outside the vocabulary, is reported; valid rows are silent. |
| A-7.3 | It shall require each decomposition to carry a machine-readable record of the declared expert and downstream-user perspectives, the applicability decision for each, and the requirements or explicit no-finding each produced — and shall report any applicable declared perspective absent from that record. | SN-036 | B-05 | An applicable perspective missing from the record is reported; a perspective recorded as no-finding is accepted. |
| **A-8** | The package shall deliver a capability that keeps the promised behaviors, their boundary locations and the architecture mutually resolvable at all times. | SN-037, SN-040 | B-05 | Unresolved references, uncovered crossings and incompatible signal types are each reported as findings. |
| A-8.1 | Every requirement input and output shall reference a declared interface, and every referenced interface shall identify its endpoints and whether its signal is discrete or variable. | SN-037 | B-05 | Count of requirement inputs/outputs without a resolving interface reference = 0 at the gate. |
| A-8.2 | Every declared component-boundary crossing shall have an interface row, and a change altering one side of the requirement/interface relationship shall carry — or explicitly justify omitting — the corresponding change on the other. | SN-037 | B-05 | An uncovered crossing is reported; a one-sided change without recorded justification is a finding. |
| A-8.3 | A component partition shall be accompanied by a reproducible record of the candidates considered, the declared objective and constraints they were scored against, the selected partition, and the human ruling that named it. | SN-040 | B-05 | A reviewer re-running the comparison from the record reaches the same ranking; a partition with no such record is a finding. |
| **A-9** | The package shall deliver a coverage capability establishing, for every file it supplies, at least one requirement chain resolving to a stakeholder need, so no supplied file exists without a recorded reason. | SN-038 | B-05 | Every inventoried supplied file has a resolving chain; unmapped files are reported under the declared warn-to-gate policy. |
| A-9.1 | A declared inventory shall define the coverage universe and its exclusions, and missing files, stale entries and unresolved references shall each be reported. | SN-038 | B-05 | Adding an un-inventoried file, or removing an inventoried one, is reported by the next check run. |
| A-9.2 | A generated output may satisfy the mapping through its generator. | SN-038 | B-05 | A generated artifact with a mapped generator is not reported as unmapped. |

### 2d. Generator / readable-surface bundle

| ID | Obligation (one shall) | SNs | Crossings | Observable |
|---|---|---|---|---|
| **A-10** | The package shall deliver capabilities that keep its documentation navigable and its generated views incapable of silently rotting. | SN-010, SN-023, SN-025 | B-05 | A broken intra-repository link, an undeclared or duplicated vision statement, and a stale generated view are each detected. |
| A-10.1 | It shall fail on a broken intra-repository link and on a missing single declaration of the project's purpose. | SN-010 | B-05 | Breaking one link or removing the purpose declaration turns the check red. |
| A-10.2 | Every generated artifact shall carry a freshness contract that reports staleness without regenerating, and every human-read status surface shall be generated rather than hand-copied. | SN-010, SN-025 | B-05 | Editing a generated artifact's source without regenerating is reported as stale; no human-read status surface is hand-maintained. |
| A-10.3 | It shall render, in one view, both the project's progress decomposition and the declared interface graph, and shall check mechanically — warning first — that every module in the inventory is either a declared interface endpoint or an explicit source/sink. | SN-023 | B-05 | The single view shows both; a module that is neither endpoint nor declared source/sink raises a warning. |

### 2e. Unattended-loop bundle

| ID | Obligation (one shall) | SNs | Crossings | Observable |
|---|---|---|---|---|
| **A-11** | The package shall deliver an unattended run capability that resumes from tracked repository state alone, never blocks on a prompt, and ends in a clearly-typed outcome. | SN-006, SN-025 | B-05 | With no interactive input available, a run either completes or exits with a typed end-state code; count of indefinite hangs = 0. |
| A-11.1 | A preflight shall refuse a broken footing — no agent runner, not a version-controlled tree, an authorship state the privacy dial forbids — rather than starting and hanging. | SN-006 | B-05 | Each seeded broken-footing condition produces a refusal before any work begins. |
| A-11.2 | Each end state shall exit a distinct, declared code so an outer caller can act on the outcome without parsing prose. | SN-006 | B-05 | The set of end states maps one-to-one onto declared codes. |
| A-11.3 | With no human curating what comes next, it shall derive the next work from the tracked work-item dependency graph plus version-control history — never from prose, a hand-maintained pointer, or predefined tracks. | SN-025 | B-05 | No hand-maintained next-step artifact exists or is read; deleting all prose planning text does not change what the loop dispatches. |
| A-11.4 | The ready frontier shall be ordered deterministically, so two readers of the same tracked state dispatch the same work. | SN-025, SN-027 | B-05 | Repeated derivations over identical state yield identical ordering, 100% of runs. |
| **A-12** | The package shall deliver parallel execution of independent ready work across bounded lanes while keeping mutation of the integration line serialized and gated. | SN-027 | B-05 | With N independent ready items, up to the configured ceiling run concurrently; concurrent mutations of the integration line = 0. |
| A-12.1 | Fan-out shall run each lane in an isolated working copy up to a configured ceiling, and the single-lane setting shall preserve the fully serial semantic. | SN-027 | B-05 | Lanes never share a working copy; the single-lane setting reproduces serial behavior exactly. |
| A-12.2 | Every finished lane shall land through one serial, fail-closed integrator that runs the declared bar on the composed result. | SN-027, SN-008 | B-05 | Every landing carries a bar result on the composed tree; a failing bar blocks the landing. |
| A-12.3 | A declared pause shall stop new claiming while draining what is already in flight. | SN-027 | B-05 | After a pause is declared, new claims = 0 and in-flight items still reach an end state. |
| A-12.4 | A crash at any lifecycle boundary shall be recoverable from version-control history alone, without double-assignment or half-integrated authoritative state. | SN-027 | B-05 | Killing the run at each declared boundary and restarting yields no duplicate assignment and no partially-integrated authoritative state. |
| **A-13** | The package shall let the owner declare several model families, selected per job and per capability level, and shall route work benefiting from an independent second opinion to a different family wherever one is configured. | SN-026 | B-05 | With ≥2 families routable, second-opinion sessions draw cross-family in 100% of eligible dispatches. |
| A-13.1 | The families, models and capability levels shall be declared as registry rows, with a separate explicit consent surface whose presence turns managed selection on and whose absence leaves behavior unchanged. | SN-026, SN-012 | B-05 | Without the consent surface, selection behavior is byte-identical to the unmanaged baseline. |
| A-13.2 | When only one family is routable it shall degrade to the documented same-family mode rather than silently omitting the second opinion. | SN-026, SN-008 | B-05 | Single-family conditions produce a recorded degraded second opinion, never a skipped one. |
| A-13.3 | Every selection shall be logged before launch, so no model substitution is silent. | SN-026 | B-05 | Each dispatched session has a pre-launch selection record; unlogged dispatches = 0. |
| **A-14** | The package shall adjudicate subjective or perceptual acceptance by an independent critical eye against a written rubric, never by the session that authored the artifact. | SN-024 | B-05 | Every critique verdict is issued by a session distinct from the authoring session and, where families permit, from a different family. |
| A-14.1 | The rubric shall be derived from the stakeholder/system intent rather than from the possibly-lax test case, and shall carry numbered good/bad anchors the verdict cites. | SN-024 | B-05 | Each verdict cites at least one numbered anchor; a verdict with no anchor citation is invalid. |
| A-14.2 | Bounded iteration shall drive rework toward the bar, and exhaustion of the declared budget shall escalate to the human rather than accepting the artifact. | SN-024, SN-029 | B-05 | On budget exhaustion, the outcome is escalation, never a pass. |

### 2f. Package-wide properties

| ID | Obligation (one shall) | SNs | Crossings | Observable |
|---|---|---|---|---|
| **A-15** | The package shall place every policy dial in one hand-edited, machine-read home, and shall refuse a repository that declares the same dial twice rather than resolving it by precedence. | SN-028 | B-05, B-01 | A duplicate declaration produces a refusal naming both sources; precedence resolutions = 0. |
| A-15.1 | The dial file's shape shall be constrained so that every consumer reading it — full parser and minimal parser alike — reads the same value, pinned equal over a table of adversarial files. | SN-028, SN-009 | B-05 | Over the adversarial table, the two readings agree on every row; a divergence is a defect. |
| A-15.2 | A wrong-typed or out-of-range dial value shall be refused, never silently defaulted. | SN-028, SN-029 | B-05 | Each malformed dial value produces a refusal; count of silent defaults = 0. |
| **A-16** | The package shall place, at the repository's front door on every supported platform, a single-action entry point for each of the two universal contributor actions — preparing the development environment and resuming the automated loop. | SN-034 | B-05 | Both entry points exist at the root of a fresh installation for each supported platform, and each starts its action in one step. |
| A-16.1 | Where a platform cannot honor a single click, the one platform-required preparatory step shall be documented rather than assumed. | SN-034 | B-05 | For each platform where one click is impossible, the required step is documented at the entry point. |
| A-16.2 | The adopter-facing guide shall name the front-door capability and invite its reuse. | SN-034 | B-05 | The guide names the capability; absence is a finding. |
| A-16.3 | For a repository that adopts the package into itself, a front-door menu shall list the repository's available actions from one declared action inventory and run the chosen one, so completeness is checkable against a single source. | SN-035 | B-05 | The menu's entries equal the declared inventory; a divergence is a finding. |
| **A-17** | The package shall run every check it asks an adopter to run on a clean declared-minimum runtime, on Windows, Linux and macOS alike. | SN-011, SN-003 | B-05, B-06 | The adopter-run check set completes on a clean minimum runtime on all three platform families. |
| A-17.1 | Any dependency beyond the runtime's standard library shall be admitted only through a reviewed ledger row naming what it replaces, why hand-rolling is worse, and the ruling that admitted it. | SN-011 | B-05 | Every non-standard-library import has a ledger row; an undeclared import fails the package's own suite. |
| A-17.2 | The checks an adopter runs shall remain standard-library-preferred, since a dependency there is imposed on every adopter. | SN-011 | B-05 | Count of non-standard-library imports reachable from the adopter-run check set is zero, or each is individually argued in the ledger. |
| **A-18** | The package shall be right-sized: a repository that does not enable an optional layer shall pay nothing for it. | SN-012 | B-05 | With every optional layer disabled, the enabled-path cost and required artifacts equal the baseline; no disabled layer contributes a required step. |
| A-18.1 | The heavier layers shall be opt-in by declaration rather than on by default. | SN-012, SN-026, SN-024 | B-05 | Each optional layer is inert until its declaration exists. |
| A-18.2 | The granularity of design and test decomposition shall be governed by a stated proportionality rule, so small changes stay small. | SN-012 | B-05 | A small change's required artifact count is bounded by the stated rule, not by a fixed ceremony. |
| **A-19** | The package shall deliver one guide that governs humans and agents from the same playbook, with any per-agent configuration mirroring it rather than replacing it. | SN-005 | B-05 | Exactly one governing guide exists; per-agent configurations contain no rule absent from it. |

## Group 3 — EXT-004 Hosted CI · crossings B-06 (in), B-07 (out)

| ID | Obligation (one shall) | SNs | Crossings | Observable |
|---|---|---|---|---|
| **A-20** | The package shall deliver a hosted validation definition that, on each declared trigger, runs the same documented harness entry point a local session runs, at the tier the declared moment-to-tier table assigns to that trigger. | SN-005, SN-008 | B-06, B-07 | For each declared trigger, the hosted entry point and tier equal the local ones for that moment; a divergence is a defect. |
| A-20.1 | The trigger-to-tier assignment shall be pinned by test for the shipped reference definition, with no claim made about an adopter-edited copy. | SN-005 | B-06 | A change to the reference definition's trigger/tier mapping fails the pinning test. |
| A-20.2 | The hosted run shall exercise the declared platform × runtime matrix and shall be green across it. | SN-011, SN-007 | B-06 | All declared matrix cells run; failures in any cell fail the run. |
| A-20.3 | Each hosted run shall emit a pass/fail verdict and a step log sufficient to locate the failing step without re-running locally. | SN-008, SN-005 | B-07 | Every failing hosted run names the failing step in its log. |
| A-20.4 | The hosted run shall re-apply the session-local admission bar, so a write that bypassed the local verdict is still caught before it is treated as validated. | SN-005, SN-008 | B-07, B-04 | A deliberately bypassed local check is caught by the hosted run 100% of the time. |

## Group 4 — the maintaining session on this repository · crossings B-01, B-05

| ID | Obligation (one shall) | SNs | Crossings | Observable |
|---|---|---|---|---|
| **A-21** | The system shall hold its own delivered capabilities to the bar it delivers: its own artifacts traced by its own join, and its own checks exercised end-to-end against a freshly installed instance before a change is admitted. | SN-007, SN-001, SN-002 | B-01, B-05 | Each admitted change is preceded by a green full-suite run that installs a temporary instance and exercises every delivered script; a claimed green with no run is a defect. |
| A-21.1 | Its own registries shall satisfy the same join, orphan and identifier rules it imposes on an adopter. | SN-007, SN-002 | B-01 | The self-applied join reports zero orphans under the same strictness an adopter's gate uses. |

---

## Coverage check

### Every SN mapped to ≥1 capability (27/27)

| SN | Capabilities |
|---|---|
| SN-001 | A-4, A-4.1, A-21 |
| SN-002 | A-1, A-1.2, A-6, A-6.1, A-6.2, A-3.3, A-21, A-21.1 |
| SN-003 | A-4.2, A-5.2, A-17 |
| SN-004 | A-1.2, A-3, A-3.1, A-5, A-5.1, A-6.1 |
| SN-005 | A-1, A-1.2, A-1.3, A-1.4, A-2, A-2.1, A-5.3, A-19, A-20, A-20.1, A-20.3, A-20.4 |
| SN-006 | A-2, A-11, A-11.1, A-11.2 |
| SN-007 | A-5.3, A-6, A-20.2, A-21, A-21.1 |
| SN-008 | A-1, A-1.3, A-2, A-2.1, A-5, A-5.1, A-5.4, A-12.2, A-13.2, A-20, A-20.3, A-20.4, A-3.4 |
| SN-009 | A-1.1, A-15.1 |
| SN-010 | A-10, A-10.1, A-10.2 |
| SN-011 | A-17, A-17.1, A-17.2, A-20.2 |
| SN-012 | A-5, A-5.3, A-13.1, A-18, A-18.1, A-18.2 |
| SN-023 | A-10, A-10.3 |
| SN-024 | A-14, A-14.1, A-14.2, A-18.1 |
| SN-025 | A-10, A-10.2, A-11, A-11.3, A-11.4 |
| SN-026 | A-13, A-13.1, A-13.2, A-13.3, A-18.1 |
| SN-027 | A-11.4, A-12, A-12.1, A-12.2, A-12.3, A-12.4 |
| SN-028 | A-3, A-4.3, A-15, A-15.1, A-15.2 |
| SN-029 | A-3, A-3.1, A-3.2, A-3.3, A-3.4, A-14.2, A-15.2 |
| SN-033 | A-7, A-7.1 |
| SN-034 | A-4, A-16, A-16.1, A-16.2 |
| SN-035 | A-16.3 |
| SN-036 | A-7, A-7.3 |
| SN-037 | A-8, A-8.1, A-8.2 |
| SN-038 | A-9, A-9.1, A-9.2 |
| SN-039 | A-7, A-7.2 |
| SN-040 | A-8.3 |

No SN is unmapped. Thinnest coverage: **SN-035** (one sub-row, A-16.3) and
**SN-040** (one sub-row, A-8.3) — both are single-obligation needs, so thinness
here is proportionate rather than a gap.

### Every crossing served

| Crossing | Direction | Served by | Note |
|---|---|---|---|
| B-01 | in | A-1 (+ .1–.4), A-3.3, A-15, A-21, A-21.1 | Fully served. |
| B-02 | in | A-3, A-3.1–A-3.4 | Fully served; the only crossing whose whole group is one capability tree. |
| B-04 | out | A-1, A-1.1, A-1.3, A-1.4, A-2, A-2.1, A-20.4 | Served, but only jointly with B-07 — see T-3. |
| B-05 | out | A-4 … A-19, A-21 | The dominant crossing: 16 of 21 top-level rows. |
| B-06 | in | A-5.3, A-17, A-20, A-20.1, A-20.2 | Fully served. |
| B-07 | out | A-20, A-20.3, A-20.4, A-2.1 | Fully served. |

No crossing is unserved-by-need. **No capability was derived that no SN demands**
— the second-system guard held; candidates considered and dropped are listed as
T-6.

---

## Tensions

**T-1 — the reader-facing surfaces have no out-crossing.** SN-023 ("a reviewer
can see progress and how the parts connect from one dashboard-like file"),
SN-010's generated-view half and SN-025's "the status surface a human reads is
generated" all describe something a *human reads*. The frame routes exactly those
surfaces to REL-002 — an external-to-external self-adoption flow the system is
not a party to — and deliberately removed the crossing that used to carry them.
So the strongest form I can state is an obligation on delivered *generator*
content at B-05 (A-10, A-10.3): the system must deliver the capability, but the
rendered artifact a reviewer actually looks at is an adopted-toolkit output, and
a verifier watching "a reviewer sees it" is standing outside the boundary. The
needs and the frame are consistent only under that reading, and it is worth
confirming that the reading is intended rather than a residue of the B-03 removal.

**T-2 — SN-007 and SN-035 are about *this* repository, and the frame has no
crossing for that.** "The people maintaining this kit hold it to its own
standard" (SN-007) and "a person working on this repository can open one action
menu" (SN-035) describe obligations whose subject is this repository's own
practice. In the frame that activity is EXT-001 acting through B-01, with the
delivered content arriving via REL-002 — again not a system crossing. I placed
SN-007 in its own group (A-21) at B-01/B-05 and SN-035 as delivered-pattern
content (A-16.3), but neither placement is clean: a verifier auditing them is
auditing a relationship, not a crossing.

**T-3 — SN-005's obligation cannot be carried by any single capability.** A
session-local admission verdict is bypassable by construction, so "no unchecked
write enters governed state" is only decidable as a *pair*: the act-time verdict
at B-04 plus the hosted re-run at B-07. I encoded that honestly (A-2.1 + A-20.4
reference each other), but it means the crossing-by-crossing decomposition my
axis produces cannot keep this obligation in one row. A reviewer must read the
pair together or they will read a weaker promise than the need makes.

**T-4 — the model-provider needs have no provider-facing crossing.** SN-026
(multi-family scheduling), SN-024 (heterogeneous critic) and SN-013-class backoff
behavior all describe interaction with model services, which the frame places on
REL-003 — session-to-provider, system not a party. Every obligation I could
derive is therefore a property of *delivered loop content* (A-13, A-14),
observable only in the loop's own selection and verdict records, never at a
provider interface. That is derivable, but it makes "prefers a cross-family draw"
verifiable only against the loop's self-report — a weaker evidence class than the
need's confident wording implies.

**T-5 — SN-034 spans a crossing and a non-crossing.** The need demands the two
entry points exist "in a fresh scaffold **and** in this repository". Only the
scaffold half crosses B-05; the this-repository half is the REL-002 reading again.
A-16 states the crossing half; the second half rides on T-2.

**T-6 — vision-level promises with no SN behind them, deliberately excluded.**
The README intro promises license text dropped into every scaffold so a
downstream repository can be redistributed without chasing it. No SN demands it,
so under the second-system guard I derived **no capability** for it. Either an SN
is missing, or the promise is decoration in the README. The same call was made
for the "cross-platform launcher scripts ship for each OS" phrasing beyond what
SN-034 states.

**T-7 — SN-025 and SN-029 pull opposite ways, and the resolution is a dial.**
SN-025 wants no human curating what comes next; SN-029 reserves specific tiers
for a human. Both are satisfiable simultaneously, but only relative to a declared
level — so no capability row can state a fixed threshold for "the loop should
have stopped here". A-3.1 and A-11.3 are jointly correct only when read against
the declared level, which means the *observable* for both is conditional on
configuration rather than absolute. Verifiers must be given the level as an input.

**T-8 — SN-009's "in every repository, without extra setup" outruns B-01's
declared carrier.** B-01 admits writes "ONLY through the git hook floor", and a
hook floor is per-clone installed state. "Every repo, no extra setup" therefore
depends on the scaffold bundle installing that floor (A-4) as much as on the
screening capability itself (A-1.1). The need reads as one promise; the frame
splits it across two crossings' worth of delivered content.
