# Blind derivation B — lifecycle / value-flow axis

**Derivation date:** 2026-08-16
**Team:** B (clean-room, blind)
**Axis:** *lifecycle / value-flow.* Capabilities are grouped by the stage of the
delivered kit's value flow at which the obligation must hold — adoption &
installation → requirement/architecture authoring → day-to-day gated development
→ verification & gating → unattended operation → review & ratification →
visibility → release & re-sync. Grouping is by **stage**, never by actor: the
same actor (a session, the owner) appears in several stages, and the same stage
serves several actors.

**Blind input set (the only files read):**

1. `README.md` — the `PROJECT-VISION` tag and its immediately surrounding intro.
2. `docs/requirements/stakeholder-needs.toml` — the 27 SN rows (SN-001…SN-012,
   SN-023…SN-029, SN-033…SN-040) plus the non-goal NG-1.
3. `docs/requirements/external.toml` — 5 entities, 6 boundary crossings
   (`B-01`, `B-02`, `B-04`, `B-05`, `B-06`, `B-07`), 3 external-to-external
   relationships.

No requirement, design, test, interface, script, plan, log or history file was
opened. Where an input referenced a file outside that set, the reference was not
followed.

**Voice rule applied:** every row states one delivered, observable obligation in
capability / artifact-class terms. No row names a concrete file, script or
command — the obligations below are intended to hold for *every* acceptable
implementation. Where an SN's own acceptance text names an artifact, the
obligation here is restated as the class of thing that artifact is an instance
of.

**Naming collision warning:** the boundary crossings in the frame are also
`B-##`. In this document, capability ids are written `B-1`, `B-1.1` (single
digit, no leading zero) and boundary crossings are always written with two
digits and the word "crossing" or in the *Crossings* column: `B-01`, `B-05`.

---

## Stage L1 — Adoption & installation

*What must happen first: the package must arrive in a repository, working, on the
adopter's own terms, with everything it brought accounted for.*

| id | Obligation (one shall) | SNs | Crossings | Observable |
|---|---|---|---|---|
| **B-1** | The kit **shall** be installable into a new or pre-existing repository as a single invoked action that yields a process instance whose declared bar passes without hand-built tooling. | SN-001, SN-003 | B-05 | On a repository with no prior kit content, one action then the declared bar → bar exits pass, zero manual edits interposed. |
| B-1.1 | The scaffold produced **shall** be self-sufficient: its declared bar runs green on a clean supported machine immediately after installation. | SN-001 | B-05 | Fresh install + immediate bar run → pass rate 100%, zero "missing artifact" findings. |
| B-1.2 | The toolchain the harness invokes **shall** be declared in one adopter-owned declaration, such that adopting a non-reference language changes only that declaration, and an installation profile for that language omits reference-language-only artifacts. | SN-003 | B-05 | Re-point the toolchain declaration to a different stack → zero kit-supplied executable files edited; a non-reference profile install → zero reference-language-only artifacts present. |
| B-1.3 | Re-application of the kit onto a repository that already has content **shall** preserve every adopter-owned artifact it did not supply. | SN-001 | B-05 | Re-apply over a populated repo → count of adopter-owned files modified or deleted = 0. |
| B-1.4 | Installation and documented re-application **shall** convert any superseded configuration form it finds, so an adopter never has to resolve a legacy/current conflict by hand. | SN-028 | B-05 | Install over a repo carrying legacy config forms → zero legacy forms remain, zero refusals raised at first bar run. |
| **B-2** | Every check an adopter is expected to run **shall** execute on a clean installation of the declared minimum reference runtime, on each supported operating system, with non-runtime-supplied dependencies admitted only through a reviewed ledger entry stating what each replaces and why. | SN-011 | B-05, B-06, B-07 | Clean runtime, no extra installs → adopter-facing checks complete; every non-stdlib import present in the ledger, else the kit's own suite fails. |
| B-2.1 | An import not carried by a reviewed ledger entry **shall** fail the kit's own verification rather than being tolerated. | SN-011 | B-05 | Introduce an undeclared non-runtime import → kit suite exit ≠ 0. |
| B-2.2 | The adopter-facing tier of checks **shall** remain runnable with zero installed dependencies beyond the reference runtime. | SN-011 | B-05 | Adopter tier on a bare runtime → 0 install steps required, 0 import errors. |
| B-2.3 | The supported operating-system × runtime-version matrix **shall** be exercised and green as a condition of the kit's own change acceptance. | SN-011, SN-007 | B-06, B-07 | Every declared matrix cell reports pass before a change lands; any red cell blocks. |
| **B-3** | Every file the kit delivers **shall** be traceable to at least one stakeholder outcome through a declared inventory, and any file that is not **shall** surface as a named coverage finding. | SN-038 | B-05 | Inventory ∪ exclusions covers 100% of delivered files; unmapped file count reported, and the declared warn-to-gate policy applied at the stated threshold. |
| B-3.1 | A declared inventory with explicit exclusions **shall** define the coverage universe, so completeness is checkable against one source. | SN-038 | B-05 | Delivered-file set minus inventory minus exclusions = ∅; stale inventory entries (listed, not present) reported. |
| B-3.2 | Each inventoried file's mapping **shall** resolve transitively to a stakeholder need, with generated outputs permitted to map through their generator. | SN-038 | B-05 | Unresolved-reference count = 0; unmapped-file count reported with its policy disposition. |
| **B-4** | Each of the two universal contributor actions — preparing the development environment, and resuming the automated development loop — **shall** be startable from the repository's front door as a single action on every supported platform, or the one platform-imposed extra step **shall** be documented. | SN-034 | B-05 | On each supported platform, both entry points present at repository root; each reaches its action in one user action, or names the one required step. |
| B-4.1 | The environment-preparation entry point **shall** exist at the root of both a fresh installation and the kit's own repository, per supported platform. | SN-034 | B-05 | Fresh install → entry point present for each platform; count of platforms lacking one = 0. |
| B-4.2 | The loop-resume entry point **shall** likewise exist per platform and require no remembered command. | SN-034 | B-05 | Resume reachable with zero typed arguments on each platform. |
| B-4.3 | A menu-class entry point **shall** enumerate the repository's available actions from one declared action inventory and run the chosen one. | SN-035 | B-05 | Menu's listed actions ≡ declared inventory (set difference = ∅ both ways); chosen action executes. |
| **B-5** | Every process policy dial **shall** live in exactly one hand-edited, machine-read declaration, and a repository declaring one dial in two places **shall** be refused rather than resolved by precedence. | SN-028 | B-05, B-01 | Duplicate declaration → refusal naming both sources; number of dials readable only outside the single home = 0. |
| B-5.1 | The declaration's shape **shall** be constrained so that every reader of it — including a minimal, non-runtime reader — resolves each dial to the same value. | SN-028, SN-009 | B-05 | Over an adversarial file table, reading A and reading B agree on 100% of dials. |
| B-5.2 | A wrong-typed or out-of-range dial value **shall** be refused, never silently defaulted. | SN-028, SN-029 | B-05 | Inject a bad value → refusal with the offending key named; count of silent fallbacks = 0. |
| **B-6** | Optional process layers **shall** impose no cost on a repository that has not opted into them. | SN-012 | B-05 | Bar run in a repo with all optional layers off vs. a minimal baseline → identical required-step set, no added required artifacts, no added failures. |

## Stage L2 — Requirement & architecture authoring

*Before any code moves: the chain from stakeholder outcome to test, and the
architecture it is anchored in, must be authored so that it can be mechanically
checked and independently validated.*

| id | Obligation (one shall) | SNs | Crossings | Observable |
|---|---|---|---|---|
| **B-7** | The chain from stakeholder need through requirement and design to test **shall** be mechanically joinable and reported, with zero unlinked rows required before a gate advances. | SN-002 | B-01, B-05 | Strict join report: orphan count = 0 at every gate advance; a gate attempted with orphans > 0 fails. |
| B-7.1 | Identifier integrity **shall** be enforced at every tier: a malformed or duplicated identifier fails rather than being skipped. | SN-002 | B-05 | Inject a duplicate or malformed id at any tier → non-zero exit naming the row. |
| B-7.2 | The join **shall** be produced from the registries at check time rather than maintained by hand, so it cannot drift from the rows it summarizes. | SN-002, SN-010 | B-05 | Edit a registry row without regenerating → freshness check fails; hand-maintained join copies = 0. |
| **B-8** | Each stakeholder-need statement **shall** be recognizable to the stakeholder who asked for it: expressed as an outcome, free of internal implementation vocabulary, and carrying a declared applicability scope. | SN-033, SN-039 | B-05, B-01 | Every non-example need row: legibility findings enumerated with row and phrase; scope value present and in vocabulary for 100% of rows. |
| B-8.1 | A declared check **shall** report the row and the offending phrase when a need statement carries an internal path, implementation-only identifier or process citation, with a reviewed exception list for names that are themselves user-facing, and the resulting findings **shall** appear in the requirements-bar review evidence. | SN-033 | B-05 | Findings list produced per review; exceptions reviewed, not ad hoc; unexplained violations at bar = 0. |
| B-8.2 | Every non-example need row **shall** carry a scope value drawn from a closed vocabulary, with missing or invalid values reported. | SN-039 | B-05 | Rows missing/invalid scope → reported count; the field is part of the registry schema, not a one-off column. |
| **B-9** | Each decomposition of a need into requirements **shall** leave a machine-readable provenance record sufficient for a reviewer to re-run the reasoning rather than take it on trust. | SN-036, SN-040 | B-05, B-02 | For each decomposition: a record exists; missing applicable perspectives and missing partition rationale are reported as findings. |
| B-9.1 | The record **shall** name the declared review perspectives, the applicability decision for each, and either the requirements produced from it or an explicit no-finding result; an applicable perspective absent from the record **shall** be reported. | SN-036 | B-05 | Applicable-perspective coverage = 100% or a finding per gap; no-finding results recorded explicitly, not by omission. |
| B-9.2 | The record **shall** carry the candidate component partitions considered, the objective and constraints they were scored against, the selected partition and a comparison a reviewer can reproduce, kept with the architecture rather than in session prose; the final choice **shall** be a human ruling. | SN-040 | B-05, B-02 | Reviewer re-scores the recorded candidates and reaches the recorded ranking; partition selections lacking a human ruling = 0. |
| **B-10** | Every promised system behavior **shall** name the declared boundary at which its inputs enter and its outputs leave, and a change to either side of the requirement/architecture pair **shall** carry — or explicitly justify the absence of — the corresponding change on the other. | SN-037, SN-023 | B-05, B-01 | Unresolved interface references = 0; uncovered component-boundary crossings = 0; signal-type incompatibilities = 0; one-sided reviewed changes carry a recorded justification. |
| B-10.1 | Each declared interface **shall** identify its endpoints and the nature of its signal, and every component-boundary crossing **shall** have one. | SN-037 | B-05 | Crossings without an interface row → finding; endpoints or signal nature missing → finding. |
| B-10.2 | Every module in the architecture inventory **shall** be either a declared interface endpoint or an explicitly recorded source/sink, checked mechanically. | SN-023, SN-037 | B-05 | Modules that are neither → reported count (warning-first policy honored, threshold declared). |

## Stage L3 — Day-to-day gated development

*While work is being done: every write into governed state meets the same floor,
regardless of who or what made it.*

| id | Obligation (one shall) | SNs | Crossings | Observable |
|---|---|---|---|---|
| **B-11** | Process enforcement **shall** be agent-neutral: the floor that admits a governed write is the same floor a hosted re-run applies, and per-agent configuration may only mirror it, never replace it. | SN-005 | B-01, B-04, B-06, B-07 | The same documented entry point runs locally and in hosted validation; per-agent config files introduce zero enforcement rules of their own. |
| B-11.1 | A governed write **shall** receive an accept/reject verdict at the moment of the act, independent of which session (human or agent) produced it. | SN-005, SN-009 | B-01, B-04 | Identical offending write from two different session kinds → identical verdict; verdicts returned before the write is admitted. |
| B-11.2 | Hosted validation **shall** run the documented entry point at the tier a declared moment-to-tier mapping assigns to that trigger, pinned so the shipped reference configuration cannot drift from the mapping. | SN-005 | B-06, B-07 | For each declared moment (per-change bar, slice close, release): tier run ≡ tier declared; drift → test failure. |
| **B-12** | Content leaving a repository **shall** be screened for secrets and, when the identity dial is on, for private-identity classes — in every repository, with no additional setup by the adopter. | SN-009 | B-01, B-04 | Planted secret in staged content, in the change message, and in the outgoing range → each blocked; setup steps required by the adopter = 0. |
| B-12.1 | The secrets floor **shall** be always-on and cover staged content, the change description, and the outgoing range. | SN-009 | B-01, B-04 | All three surfaces scanned per event; disabling the floor is not an offered configuration. |
| B-12.2 | Identity/PII classes **shall** be added on top of the floor when the declared dial is on, and refused rather than assumed when the dial is unreadable. | SN-009, SN-028 | B-01, B-04 | Dial on → additional classes active; dial malformed → refusal, not silent off. |

## Stage L4 — Verification & gating

*The moment of truth: the bar that decides whether work may advance, and the
guarantee that a pass means what it says.*

| id | Obligation (one shall) | SNs | Crossings | Observable |
|---|---|---|---|---|
| **B-13** | Advancement **shall** occur only through explicit gates whose mechanical bar is enforced, and a pass **shall** never be reported when a required check did not actually run. | SN-004, SN-008 | B-05, B-04 | For each gate: required-step set determined by the gate in force; a required capability absent → fail (not skip); count of passes containing an unexecuted required step = 0. |
| B-13.1 | The required steps of a bar **shall** be selected by the gate in force rather than by the operator's choice. | SN-004 | B-05 | Same tree, two gates → different required-step sets, both derived; operator override of the set = not offered. |
| B-13.2 | Exactly one explicitly-requested, locally-scoped degrade to "skipped" **shall** exist, and it **shall** never be the default in a hosted or gate-bearing run. | SN-008 | B-05, B-06 | Degrade active only when explicitly requested; hosted/gate runs with degrade active = 0. |
| B-13.3 | Honesty detectors — unimplemented-stub and unmet-criterion classes — **shall** run at their declared gate and fail the bar when they fire. | SN-008 | B-05 | Planted stub / unmet criterion at the declared gate → bar exit ≠ 0. |
| **B-14** | Acceptance that is subjective or perceptual **shall** be adjudicated by a fresh, provider-heterogeneous critical reviewer against a written rubric derived from the need/requirement intent — never by the session that produced the artifact, and never solely by a possibly-lax test case. | SN-024 | B-05 | Critique verdicts whose judging session == authoring session = 0; verdicts whose judging family == authoring family = 0 while heterogeneity is available. |
| B-14.1 | The rubric **shall** carry numbered good/bad anchors and be derived from stakeholder/requirement intent rather than the authoring session's own output. | SN-024 | B-05 | Every critique verdict cites at least one numbered anchor id; rubrics authored by the session under judgement = 0. |
| B-14.2 | Iteration **shall** be bounded and drive rework, escalating to a human on budget exhaustion rather than passing or looping. | SN-024, SN-029 | B-05, B-02 | Iterations ≤ declared budget; on exhaustion, an escalation record exists and the item is not marked accepted. |
| **B-15** | The kit **shall** hold itself to the standard it delivers: its own traceability and its full verification suite pass before any change to it is accepted, exercising the delivered scripts end to end against a temporary installation. | SN-007, SN-011 | B-05, B-06, B-07 | Every accepted change is preceded by a green full-suite run that includes an install-and-exercise pass; scripts never exercised by the suite = 0. |

## Stage L5 — Unattended operation

*Walk-away value: the loop must start itself, choose its own next work, use more
than one lane and more than one provider, and stop only where the owner said.*

| id | Obligation (one shall) | SNs | Crossings | Observable |
|---|---|---|---|---|
| **B-16** | An unattended run **shall** resume from the repository's tracked state alone, never block on an interactive prompt, and end in a distinguishable, typed outcome. | SN-006 | B-05 | Run with no interactive input available → completes or exits; prompts awaiting input = 0; each end state carries a distinct outcome code. |
| B-16.1 | A preflight **shall** refuse a broken footing — absent model runner, non-repository working copy, an identity that the active privacy policy forbids — rather than starting and hanging. | SN-006 | B-05 | Each broken-footing condition → refusal before any work begins, with the condition named; hangs observed = 0. |
| B-16.2 | Each end state **shall** be reported both as a machine-readable outcome and in a terminating human-readable summary. | SN-006 | B-05 | Outcome code ∈ declared set for 100% of runs; summary present at every termination. |
| **B-17** | What the loop does next **shall** be derived from the repository's tracked work graph and version-control state, never from prose or a hand-maintained pointer, and the derivation **shall** be deterministic. | SN-025 | B-05 | Two independent derivations over the same tracked state produce the same ordered ready set; hand-maintained next-step pointers in the tracked tree = 0. |
| B-17.1 | The ready frontier **shall** be computed from dependency readiness and totally ordered by a declared rule, so two readers dispatch the same work. | SN-025 | B-05 | Repeat derivation → identical first item, N times out of N. |
| B-17.2 | The status surface a human reads **shall** be generated from the tracked state, never hand-copied from it. | SN-025, SN-010 | B-05 | Change tracked state without regenerating → freshness check fails; hand-authored duplicates of generated status = 0. |
| **B-18** | Ready work **shall** fan out across bounded parallel lanes while mutation of the integration line stays serialized behind one fail-closed integrating step. | SN-027 | B-05 | With N independent ready items and ceiling C: concurrent lanes ≤ C; concurrent mutations of the integration line = 1 at all times. |
| B-18.1 | Each lane **shall** work in an isolated working copy, and a ceiling of one **shall** preserve exactly the serial semantic. | SN-027 | B-05 | Lanes sharing a working copy = 0; ceiling-1 run ≡ serial run in observable sequence. |
| B-18.2 | Every completed lane **shall** land only through the single integrating step, which runs the declared bar on the composed result and refuses on failure. | SN-027, SN-008 | B-05 | Landings bypassing the integrator = 0; composed-tree bar failure → landing refused. |
| B-18.3 | A declared pause **shall** stop new claiming while draining work already in flight, and an interruption at any lifecycle boundary **shall** be recoverable from version-control history alone, without double-assignment or a half-integrated authoritative state. | SN-027, SN-006 | B-05 | Pause → new claims = 0, in-flight completes; kill at each boundary → recovery yields exactly-once assignment and a consistent integration line. |
| **B-19** | Model capacity **shall** be declared as (family × capability-level) rows selected per job and per level, with an explicit consent surface enabling managed selection, a cross-family preference for second-opinion roles, a documented single-family degrade, and every selection logged before the session starts. | SN-026 | B-05 | Consent surface absent → behavior identical to unmanaged; present → each launch preceded by a logged selection naming family, model and level; second-opinion roles drawn cross-family whenever ≥2 families are routable. |
| B-19.1 | Available capacity **shall** be declared in a registry rather than hard-coded, so provider turnover is a data change. | SN-026 | B-05 | Adding/retiring a provider edits declared rows only; provider names embedded in executable content = 0. |
| B-19.2 | When only one family is routable, the loop **shall** degrade to the documented same-family mode rather than silently skipping the independent opinion. | SN-026, SN-024 | B-05 | Single-family condition → second opinion still produced and its degraded mode recorded; silently skipped reviews = 0. |
| **B-20** | An autonomous run **shall** get as far as it honestly can: it stops for a human only where the declared ratification level reserves that tier, where a round cannot converge, or where requirement/test text changes such that the derived stage falls below what automation may attest. | SN-029 | B-05, B-02 | Stops classified against the three reserved causes: unclassified stops = 0; continuations past a reserved tier = 0. |
| B-20.1 | The reserved set **shall** be expressed as a cumulative level naming the highest human-held tier, compared against a separately derived stage indicating which tier is in process, with a declared mapping to the enforcement bar. | SN-029, SN-004 | B-05 | Level ∈ declared range; stage derived, not declared; mapping single-valued for every (level, stage) pair. |
| B-20.2 | Every failure direction — an unreadable stage, an out-of-range level, a wrong-typed dial — **shall** resolve toward *more* human involvement. | SN-029, SN-008 | B-05, B-02 | Over the enumerated failure inputs, resolved behavior is more-human in 100% of cases. |

## Stage L6 — Review & ratification

*The distinguished input: a human's authority enters here, and what it accepted
must stay pinned to the exact text that was accepted.*

| id | Obligation (one shall) | SNs | Crossings | Observable |
|---|---|---|---|---|
| **B-21** | Acceptance of an artifact **shall** be recorded against that artifact's own row — the state of the accepted text plus the point in history carrying it — so that later drift is detectable, and every approval, human or delegated, **shall** leave a durable record naming who or what approved it. | SN-029, SN-004, SN-002 | B-02, B-01 | Every accepted row carries an anchor resolving to the accepted text; approval records queryable and separable into human vs. delegated; approvals without a record = 0. |
| B-21.1 | The anchor **shall** live on the accepted row itself, not in a second registry keyed on the same artifact. | SN-029 | B-02 | Registries holding a parallel acceptance key = 0. |
| B-21.2 | Text that has moved away from what was accepted **shall** surface regardless of any status-value movement, dropping the derived stage exactly as newly introduced text does. | SN-029 | B-02 | Amend-and-flip an accepted row in one change → stage drops; amendments invisible to the detector = 0. |
| B-21.3 | An approval delegated to automation **shall** still be a review from a declared perspective against the row's actual evidence, recorded distinguishably from a human approval. | SN-029 | B-02 | Delegated approvals with no perspective or no evidence citation = 0; a query separates the two classes with no ambiguity. |
| B-21.4 | Authority inputs — rulings, attestations and status changes — **shall** enter through the same governed write path as any other change, so no acceptance bypasses the floor. | SN-005, SN-029 | B-01, B-02 | Acceptance changes admitted outside the governed path = 0. |

## Stage L7 — Visibility

*So the value is legible: one place to see where the project stands and how its
parts connect, and documentation that cannot quietly rot.*

| id | Obligation (one shall) | SNs | Crossings | Observable |
|---|---|---|---|---|
| **B-22** | One generated, repository-root reader-facing surface **shall** present both the project's progress/decomposition and the declared connection graph between its parts. | SN-023, SN-025 | B-05 | Single surface renders both views; hand-maintained progress surfaces = 0; surface regenerates from the registries with no manual edit step. |
| **B-23** | Documentation **shall** be navigable and honest: internal references resolve, the project's purpose is declared exactly once, and every generated view carries a check that fails when it is stale. | SN-010 | B-05 | Broken internal reference → check fails; purpose declarations ≠ 1 → check fails; stale generated artifact → freshness check fails. |
| B-23.1 | The purpose statement **shall** have exactly one home and every other mention **shall** be a reference to it. | SN-010 | B-05 | Independent restatements of the purpose = 0. |
| B-23.2 | Every generated artifact **shall** expose a verification mode that fails when its content no longer matches its sources. | SN-010, SN-002 | B-05 | Generated artifacts without a freshness mode = 0; stale artifact detected before the gate it feeds. |

## Stage L8 — Release & re-sync

*Closing the loop: the versioned release bar, and moving an already-adopted
repository onto a newer revision of the kit without losing its own work.*

| id | Obligation (one shall) | SNs | Crossings | Observable |
|---|---|---|---|---|
| **B-24** | An already-adopted repository **shall** be movable onto a newer revision of the kit by replacing only kit-owned content, preserving every artifact the adopter authored, with superseded configuration forms converted in the same operation. | SN-001, SN-028 | B-05 | Re-sync run → adopter-authored files changed = 0; kit-owned files at new revision = 100%; legacy forms remaining = 0. |
| B-24.1 | The release-tier bar **shall** be a distinct explicit gate, reachable only from the passed prior bars, and applicable only when a versioned release is being made. | SN-004, SN-008 | B-05 | Release gate attempted with a prior bar unpassed → fail; non-releasing repositories incur no release-gate steps. |

---

## Coverage check

### Every SN maps to ≥1 capability

| SN | Capabilities |
|---|---|
| SN-001 | B-1, B-1.1, B-1.3, B-24 |
| SN-002 | B-7, B-7.1, B-7.2, B-21, B-23.2 |
| SN-003 | B-1, B-1.2 |
| SN-004 | B-13, B-13.1, B-20.1, B-21, B-24.1 |
| SN-005 | B-11, B-11.1, B-11.2, B-21.4 |
| SN-006 | B-16, B-16.1, B-16.2, B-18.3 |
| SN-007 | B-15, B-2.3 |
| SN-008 | B-13, B-13.2, B-13.3, B-18.2, B-20.2, B-24.1 |
| SN-009 | B-12, B-12.1, B-12.2, B-5.1, B-11.1 |
| SN-010 | B-23, B-23.1, B-23.2, B-7.2, B-17.2 |
| SN-011 | B-2, B-2.1, B-2.2, B-2.3, B-15 |
| SN-012 | B-6 |
| SN-023 | B-22, B-10.2 |
| SN-024 | B-14, B-14.1, B-14.2, B-19.2 |
| SN-025 | B-17, B-17.1, B-17.2, B-22 |
| SN-026 | B-19, B-19.1, B-19.2 |
| SN-027 | B-18, B-18.1, B-18.2, B-18.3 |
| SN-028 | B-5, B-5.1, B-5.2, B-1.4, B-12.2, B-24 |
| SN-029 | B-20, B-20.1, B-20.2, B-21, B-21.1, B-21.2, B-21.3, B-14.2 |
| SN-033 | B-8, B-8.1 |
| SN-034 | B-4, B-4.1, B-4.2 |
| SN-035 | B-4.3 |
| SN-036 | B-9, B-9.1 |
| SN-037 | B-10, B-10.1, B-10.2, B-9.2 |
| SN-038 | B-3, B-3.1, B-3.2 |
| SN-039 | B-8, B-8.2 |
| SN-040 | B-9, B-9.2 |

**Result: 27 / 27 needs covered.** No capability exists without at least one SN
behind it (second-system guard applied — see tension T-6).

### Every lifecycle stage grounded in ≥1 SN

| Stage | Grounding needs |
|---|---|
| L1 Adoption & installation | SN-001, SN-003, SN-011, SN-012, SN-028, SN-034, SN-035, SN-038 |
| L2 Requirement & architecture authoring | SN-002, SN-023, SN-033, SN-036, SN-037, SN-039, SN-040 |
| L3 Day-to-day gated development | SN-005, SN-009 |
| L4 Verification & gating | SN-004, SN-007, SN-008, SN-011, SN-024 |
| L5 Unattended operation | SN-006, SN-025, SN-026, SN-027, SN-029 |
| L6 Review & ratification | SN-002, SN-004, SN-005, SN-029 |
| L7 Visibility | SN-010, SN-023, SN-025 |
| L8 Release & re-sync | SN-001, SN-004, SN-008, SN-028 |

**Result: 8 / 8 stages grounded.**

### Boundary-crossing coverage

| Crossing | Served by |
|---|---|
| B-01 (governed writes in) | B-11.1, B-12, B-21.4, B-7, B-5, B-8, B-10 |
| B-02 (authority in) | B-21, B-9.2, B-14.2, B-20 |
| B-04 (guardrail verdicts out) | B-11.1, B-12, B-13 |
| B-05 (the delivered package out) | most rows — every stage's obligation is package content |
| B-06 (hosted trigger + matrix in) | B-2.3, B-11.2, B-15, B-13.2 |
| B-07 (hosted verdict + log out) | B-2.3, B-11.2, B-15 |

All 6 crossings served. The three `REL-###` external-to-external flows are
correctly **not** served by any capability — the system is not a party to them.

---

## Tensions and notes

**T-1 · SN-035 has no natural lifecycle host.** An action-menu launcher scoped to
*this repository only* is not part of the value flow that reaches an adopter; it
sits in L1 by adjacency (front-door discoverability) but its real content is a
governance act — amending the recorded self-application boundary. B-4.3 carries
the mechanical half; the boundary amendment itself is a ratification-stage event
that no capability can hold, because it is a one-time decision, not a delivered
obligation.

**T-2 · SN-007 is not a stage, it is the whole pipeline reflected.** "The kit
holds itself to its own standard" re-enters every stage at once. Modelling it as
one capability (B-15) understates it; modelling it as a clause on every row would
duplicate it 24 times. B-15 is written as the *observable* obligation (the full
suite, including an install-and-exercise pass, is green before a change is
accepted) and the rest is left to the fact that this repository is also an
adopter.

**T-3 · The release stage is thinly demanded.** Only SN-001's re-sync clause and
SN-004's gate ladder ground L8. No need asks for versioned distribution,
changelogs, upgrade notes or release artifacts, so none was invented — B-24 is
deliberately about *not losing adopter work*, and B-24.1 about the release gate
being a gate. If a release-artifact obligation is wanted, it needs a need.

**T-4 · SN-005 disclaims exactly the part hosted validation would prove.** The
need narrows itself to the shipped reference workflow and explicitly claims
nothing about an adopter-edited copy. So B-11.2's observable is pinnable only for
the shipped configuration; for an adopter's repository, the crossings B-06/B-07
obligation is *unverifiable by construction*, and the honest floor is the
local-verdict half (B-11.1). The frame's own note on `B-04` says the same thing
from the other side: a local floor is bypassable, so the pair is the claim.

**T-5 · SN-004 / SN-008 / SN-029 overlap on "what does the gate say".** Three
needs touch gate state from different angles: which steps run (SN-004), whether a
pass is honest (SN-008), and whether the stage may be advanced without a human
(SN-029). I placed step selection and honesty in L4 and stage derivation in L6,
with cross-references. An alternative placement putting stage derivation in L4
would be equally defensible; the split matters because the two have different
verifiers (harness vs. reviewer).

**T-6 · Two frame facts have no SN behind them, and no capability was written.**
(a) The rate-limit / auth-expiry / model-retirement surface named in REL-003 is
grounded only insofar as SN-026 demands a *degrade* — generic reactive backoff
has no need behind it, so none is claimed here. (b) Nothing in the SN set says
how authority arriving at crossing `B-02` is *authenticated*; B-21 can only
require that authority be recorded and anchored, not that its source be proven.

**T-7 · SN-012's obligation is an absence.** "Opt-in layers cost a repo that
doesn't use them nothing" is verifiable only differentially (baseline vs.
all-layers-off required-step set). B-6's observable is written that way, but it
is the weakest observable in this breakdown, and a differential that only ever
compares two configurations the kit itself defines is close to self-referential.

**T-8 · SN-023 straddles L2 and L7.** The interface graph is authored in L2
(B-10) and rendered in L7 (B-22). The need's acceptance mixes both ("renders
both … checked mechanically"), so it is the one SN whose single row demands
obligations at two distinct lifecycle moments. Splitting it was necessary to keep
one decision per row.

**T-9 · Scope-qualified needs (SN-033/034/036/037/038/039/040) hold in two
products at once** — the delivered blank forms and this repository's own filled
instance. On a lifecycle axis that shows up as the same obligation appearing in
L1 (as delivered package content) and again implicitly through B-15
(self-adoption). No row was duplicated for this; the reading is that a capability
delivered at `B-05` is exercised on the kit itself by B-15.
