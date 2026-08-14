# WI-451 slice 1 — the SR census against the §1R.2 boundary frame

**Date:** 2026-08-14 · **WI:** WI-451 (slice 1 of 2) · **Status: measurement
only — this document edits no registry row.** Row changes are slice 2's, and
the spine is human-held (`docs/process.toml` `human_ratification_through = 4`);
this census is written so the owner can ratify the campaign's shape from it at
sitting 3.

**Spec of record:**
[sitting-2 §3R](2026-08-13-sitting-2-boundary-and-context.md#3r-the-requirement-form-rule--ruled-2026-08-13s)
(the form rule, a guideline per 13v), §1R (the LOCKED depth-0 frame — 5
entities · 6 crossings · 3 relationships), and §2 (the port set, kept as
sizing). Registry censused:
[`../requirements/system-requirements.toml`](../requirements/system-requirements.toml)
at revision 255bb980.

## 1. Method and vocabulary

Every one of the 148 SR rows was read in full and classified by judgment
against §1R.2's six crossings (B-01/02/04/05/06/07); scripts derived the
mechanical counts only (row totals, `.py` naming, shall-shape stats). Per 13v
the form rule is a **guideline bendable with a stated per-row reason** — each
row below carries its reason class, and nothing here is an unconditional
verdict. Four classes:

- **HOLDS** — the shall is already stated at the SR's own level: against one
  of the six crossings, against a **declared B-05 contract surface** (the
  §1R.2 B-05 row names `check.py`, `bootstrap.py` + MAPPING, `agent_loop.py`,
  `check_vendored.py`, `gen_cases.py`, `gen_release_checklist.py`, the hooks
  and the launchers as IF definitions of the crossing — sitting-1 ruling
  2.7(a)'s license to name a declared boundary artifact), or as a
  package-wide delivered property. Slice 2's touch is mechanical: populate
  the interface-reference field, apply any flagged cleanup.
- **RE-STATES** — the obligation is genuinely SR-level but the text does not
  state it against a crossing: it addresses a removed-B-03 surface, narrates a
  retired mechanism, pins an implementation, or (SR-035) lacks any observable.
  The row survives at SR tier re-worded; detail clauses may shed to LLR.
- **DEMOTES** — the shall's substance is component-level: an internal
  module's behavior (§2's internal-seam classes — `trace.py`,
  `gen_trajectory.py`, `check_trajectory.py`, `schedule.py`, the plan_* and
  review machinery, and `integrate.py`/`trunk_step.py`, the last two ruled
  internal at 13u). The row is mis-tiered: slice 2 moves it to LLR under a
  parent SR — minting LLR ids, re-pointing TCs, re-homing sn_refs.
- **TOMBSTONE (n/a)** — a supersession bookkeeping row ("SR-NNN is superseded
  by …; active requirements shall cite the replacement rows"). Its "shall" is
  registry housekeeping, not a system obligation; the boundary frame does not
  apply. Recommendation at §5-F2: exempt the class once, by ruling, rather
  than record 26 identical per-row waivers.

Where a row belongs to the **B-05 bundle**, the table records **which
delivered capability** it attaches to, because slice 2 splits along that axis
(13s): `harness` (harness verdict) · `scaffold` (scaffold/MAPPING, launchers,
re-sync, registry carriers) · `loop` (unattended loop) · `generators` ·
`hook-floor`. Two extra labels the census had to add: `pkg-wide` (a property
of the whole package that does not split by capability — a finding, §5-F3)
and `—` for non-B-05 rows.

## 2. Headline numbers

The universe is all 148 SRs (`SR-001`…`SR-149`, `SR-039` retired).
<!-- fig: cmd="/Users/diytechy/Documents/ai-template/.venv/bin/python - # tomllib over docs/requirements/system-requirements.toml, len(data['requirement'])" rev=255bb980 -->

| Classification | Rows | Share |
|---|---|---|
| **HOLDS** | **34** | 23.0 % |
| **RE-STATES** | **15** | 10.1 % |
| **DEMOTES** | **73** | 49.3 % |
| **TOMBSTONE (n/a)** | **26** | 17.6 % |
| Total | 148 | 100 % |

<!-- fig: derived="hand classification of every row, recorded per-row in the §3 table; totals are the table's column sums (34+15+73+26=148)" -->

**The demotion, sized: 73 rows — roughly half the registry — are mis-tiered
as written**, plus 15 more that stay SRs only after re-statement. 13q's ~100
sizing figure was in the right region: the census's own number for
rows-that-change-text is 73 + 15 = 88 (and 34 more take only the mechanical
interface-reference/aspect touches).
<!-- fig: derived="88 = 73 DEMOTES + 15 RE-STATES from the classification table above" -->

**B-05 capability breakdown** (all 118 rows that attach to the B-05 bundle,
by class):

| Capability | HOLDS | RE-STATES | DEMOTES | Total |
|---|---|---|---|---|
| harness verdict | 5 | 1 | 27 | 33 |
| scaffold/MAPPING | 11 | 2 | 0 | 13 |
| unattended loop | 5 | 4 | 30 | 39 |
| generators | 3 | 4 | 16 | 23 |
| hook floor | 4 | 2 | 0 | 6 |
| pkg-wide property | 2 | 2 | 0 | 4 |
| **B-05 total** | **30** | **15** | **73** | **118** |

<!-- fig: derived="per-row capability column of the §3 table, summed; the 4 non-B-05 rows are SR-043 (B-04), SR-137 (B-01/B-02), SR-139, SR-140 (B-02); 118+4+26 tombstones=148" -->

**Sizing figures re-derived** (the prior session's numbers were unverified;
re-derivation was mandatory): 75/148 rows name a `.py` in requirement text —
18 name only the ten port scripts, 57 name at least one internal module —
reproducing §2's figures exactly. 147/148 rows carry `area` (`SR-049` the
exception). 128/148 rows have a leading subject before their first `shall`
(≤120 chars), 81 distinct subjects; 17 rows carry more than one `shall`, none
carry zero. The prior unverified "120 leading subjects / 73 distinct" did
**not** reproduce under this stated method — carried here with its method so
the next reader can.
<!-- fig: cmd="/Users/diytechy/Documents/ai-template/.venv/bin/python - # tomllib over system-requirements.toml; re r'\\b([A-Za-z_][A-Za-z0-9_]*\\.py)\\b' over requirement text with the §2 ten-port set; area presence; re r'^(.{1,120}?)\\s+shall\\b' and count of r'\\bshall\\b' per row" rev=255bb980 -->

## 3. The per-row table

Columns: what the row's shall actually names (crossing, declared contract
surface, or internal seam) · classification · reason · B-05 capability ·
flags. Flags: **MH** = migration/design history in the Requirement cell ·
**MH-acc** = same in the acceptance cell · **MW** = live legacy
migration-window clause · **MS** = multiple shalls (count) · **B03** =
addresses a removed-B-03 surface · **D8** = sits on `docs/architecture.md`,
ruled to die · **rider** = a WI-451-window rider named in the spec.

| SR | Names | Class | Reason | Cap. | Flags |
|---|---|---|---|---|---|
| SR-001 | `trace.py` (internal seam) | DEMOTES | shall is against an internal module's CLI; the boundary observable is the harness verdict | harness | |
| SR-002 | `trace.py` | DEMOTES | internal module flag behavior | harness | |
| SR-003 | `trace.py` | DEMOTES | internal module flag behavior | harness | |
| SR-004 | `trace.py` | DEMOTES | internal advisory mechanics | harness | |
| SR-005 | `trace.py` | DEMOTES | internal check mechanics | harness | |
| SR-006 | B-05: `check.py` contract | HOLDS | declared harness entry; the adopter-typed verdict observable | harness | |
| SR-007 | B-05: `check.py` + `docs/stack.ini` | HOLDS | declared contract: stack profile read at the harness entry | harness | |
| SR-008 | B-05: `check.py` | HOLDS | fail-loud contract at the declared entry | harness | |
| SR-009 | B-05: `bootstrap.py` | HOLDS | declared scaffold contract (profiles) | scaffold | |
| SR-010 | B-05: `bootstrap.py` | HOLDS | declared scaffold contract (green out of the box) | scaffold | |
| SR-011 | B-05: `bootstrap.py` | HOLDS | declared scaffold contract (idempotence) | scaffold | |
| SR-012 | `check_docs.py` (internal) | DEMOTES | internal harness step | harness | |
| SR-013 | `check_flows.py` (internal) | DEMOTES | internal harness step; its Runtime-flows input dies with architecture.md | harness | D8 |
| SR-014 | `check_perf.py` (internal) | DEMOTES | internal harness step | harness | |
| SR-015 | PB registry (governed data) | RE-STATES | a delivered registry-format invariant, no crossing stated; near-pair with SR-005's checker (§5-F6) | scaffold | |
| SR-016 | `check_stubs.py` (internal) | DEMOTES | internal harness step | harness | |
| SR-017 | `check_privacy.py` (internal) | RE-STATES | the secrets-floor verdict is a B-01/B-04 event observable (§1R.6 shape); the module and toggle mechanics shed to LLR | hook-floor | MW |
| SR-018 | `check_privacy.py` | RE-STATES | same: privacy verdict re-stated at the B-01/B-04 crossing | hook-floor | MW |
| SR-019 | B-01/B-04: pre-commit hook | HOLDS | the hook floor is the declared admission mechanism; ACC already states the B-06/B-07 pairing (§1R.6 honest limit) | hook-floor | |
| SR-020 | B-01/B-04: pre-push hook | HOLDS | declared hook-floor verdict at the publish edge | hook-floor | |
| SR-021 | B-05: hooks + root launchers | HOLDS | declared-content robustness (python probe) at the contract surfaces | hook-floor | MH-acc |
| SR-022 | B-05: `check_vendored.py` | HOLDS | declared adopter-invoked generator contract | generators | |
| SR-023 | `gen_arch_map.py` (internal) | DEMOTES | internal generator; target surface dies with D8 | generators | D8 |
| SR-024 | B-05: `gen_cases.py` | HOLDS | declared adopter-invoked generator contract | generators | |
| SR-025 | `gen_skills_index.py` (internal) | DEMOTES | internal generator of B-05 skills content | generators | |
| SR-026 | B-05: `agent_loop.py` contract | HOLDS | declared loop entry (headless resume); Requirement cell carries retired-mechanism narration + cross-row refs to scrub | loop | MH |
| SR-027 | B-05: `agent_loop.py` | HOLDS | declared entry contract (preflight refusal, typed exits) | loop | |
| SR-028 | B-05: `agent_loop.py` | HOLDS | declared entry contract (typed outcomes) | loop | |
| SR-029 | coordinator lock (internal) | DEMOTES | pins the mechanism (kernel advisory lock); the no-stale-wedge observable belongs to an LLR | loop | |
| SR-030 | B-05: `agent_loop.py` | HOLDS | declared entry contract (single-writer refusal) | loop | |
| SR-031 | policy readers (internal set) | RE-STATES | the SR-level obligation is dial-coherence across the delivered package at the `process.toml` surface; "share one parse" is mechanism | pkg-wide | MW |
| SR-032 | B-05: onboarding/dev-setup | HOLDS | declared launcher content runs green | scaffold | |
| SR-033 | B-05: `gen_release_checklist.py` | HOLDS | declared adopter-invoked generator contract | generators | |
| SR-034 | B-05: shipped script set | HOLDS | package-wide delivered property (stdlib + ledger); §2's "PORT-ish" worked example | pkg-wide | |
| SR-035 | (no crossing, no observable) | RE-STATES | real B-05 delivered property (stack-agnosticism) with no observable; 13u rider rides this window — candidate observable already ruled | pkg-wide | rider |
| SR-036 | B-05: re-sync (ADOPTING §6) | HOLDS | declared re-sync contract of the delivered package | scaffold | |
| SR-037 | supersession row | TOMBSTONE | registry bookkeeping | — | |
| SR-038 | supersession row | TOMBSTONE | registry bookkeeping | — | |
| SR-040 | coordinator routing + dial | RE-STATES | loop-contract-level obligation (per-phase routing, dial surfacing) wrapped in retired-file narration and three shalls | loop | MH MW MS(3) |
| SR-041 | `check_doc_refs.py` (internal) | DEMOTES | internal harness step | harness | |
| SR-042 | `gen_okf.py` (internal) | DEMOTES | internal generator mechanics | generators | MW MS(2) |
| SR-043 | B-04: subagent-spawn gate | HOLDS | §1R.6 event-shaped verdict stated at the crossing | — | MW |
| SR-044 | supersession row | TOMBSTONE | registry bookkeeping | — | |
| SR-045 | supersession row | TOMBSTONE | registry bookkeeping | — | |
| SR-046 | B-05: `run.*`/`run_menu.py` | HOLDS | declared launcher contract | scaffold | MH |
| SR-047 | supersession row | TOMBSTONE | registry bookkeeping | — | |
| SR-048 | supersession row | TOMBSTONE | registry bookkeeping | — | |
| SR-049 | `derive_gate.py` (internal) | RE-STATES | "the gate advances only when mechanical states do" is an SR-level process property; the module CLI and basis-line format shed to LLR | harness | area-missing |
| SR-050 | `gen_trajectory.py` Process tab | DEMOTES | per-tab render content is component detail | generators | B03 |
| SR-051 | supersession row | TOMBSTONE | registry bookkeeping | — | |
| SR-052 | `PROJECT_STATE.html` | RE-STATES | accessibility is a delivered-generator property; the surface is REL-002's, not a system output (13u) | generators | B03 |
| SR-053 | `PROJECT_STATE.html` | RE-STATES | same: uniformity as a generator property | generators | B03 |
| SR-054 | `PROJECT_STATE.html` | RE-STATES | same: usability as a generator property; Requirement cell carries rubric meta-narration | generators | B03 MH |
| SR-055 | Process tab loops | DEMOTES | render-content detail | generators | B03 |
| SR-056 | decomposition views | DEMOTES | render-polish detail | generators | B03 |
| SR-057 | `schedule.py` (internal) | DEMOTES | CMP-008 frontier machinery (§2 worked example) | loop | MS(3) |
| SR-058 | supersession row | TOMBSTONE | registry bookkeeping | — | |
| SR-059 | "The migration" (past event) | RE-STATES | the surviving obligations are B-05 properties (scaffold ships no retired surfaces; status generated + freshness-gated); the migration narrative is history — known flag row | scaffold+generators | MH rider |
| SR-060 | session engine (internal) | DEMOTES | worker-protocol mechanics (prompt assembly, branch discipline, trailers); carries the dead `docs/next-wi` clause | loop | MH dead-clause |
| SR-061 | supersession row | TOMBSTONE | registry bookkeeping (carries deletion narrative) | — | MH |
| SR-062 | supersession row | TOMBSTONE | registry bookkeeping (same narrative) | — | MH |
| SR-063 | supersession row | TOMBSTONE | registry bookkeeping | — | |
| SR-064 | supersession row | TOMBSTONE | registry bookkeeping | — | |
| SR-065 | supersession row | TOMBSTONE | registry bookkeeping (same narrative) | — | MH |
| SR-066 | supersession row | TOMBSTONE | registry bookkeeping | — | |
| SR-067 | `check_trajectory.py` (internal) | DEMOTES | internal harness step | harness | MW |
| SR-068 | `check_trajectory.py` | DEMOTES | internal harness step | harness | |
| SR-069 | `check_trajectory.py` | DEMOTES | internal harness step | harness | |
| SR-070 | `gen_trajectory.py` (internal) | RE-STATES | the offline self-contained state view is the generators capability's top-level deliverable — natural parent SR for the cluster | generators | B03 |
| SR-071 | `gen_trajectory.py` | DEMOTES | conditional-view detail | generators | |
| SR-072 | `gen_trajectory.py` | DEMOTES | determinism/responsiveness of one generator — component property under the generators parent | generators | |
| SR-073 | `trace.py` | DEMOTES | internal integrity check | harness | |
| SR-074 | `check_trajectory.py` | DEMOTES | internal advisory | harness | |
| SR-075 | `gen_trajectory.py` + `gen_arch_map.py` | DEMOTES | internal render detail; arch-map half dies with D8 | generators | D8 |
| SR-076 | `check_trajectory.py` | DEMOTES | internal coverage check | harness | |
| SR-077 | `check_trajectory.py` | DEMOTES | internal spec-section validation | harness | |
| SR-078 | `plan_coverage.py` (internal) | DEMOTES | dual-plan review machinery | loop | |
| SR-079 | `agent_route.py` (internal) | DEMOTES | routing machinery | loop | |
| SR-080 | coordinator (internal policy) | DEMOTES | review-session scheduling mechanics | loop | |
| SR-081 | `score_reviews.py` (internal) | DEMOTES | scoring machinery | loop | |
| SR-082 | coordinator (internal policy) | DEMOTES | escalation mechanics keyed on dials; the dial semantics live at SR-139-level, the win-stay/lose-shift detail is component-level | loop | |
| SR-083 | `agent_route.py` | DEMOTES | planner-pair selection machinery | loop | |
| SR-084 | coordinator (internal policy) | DEMOTES | critique-dispatch mechanics | loop | |
| SR-085 | coordinator (internal policy) | DEMOTES | rework-loop mechanics | loop | |
| SR-086 | `trace.py` | DEMOTES | one vocabulary value in an internal checker (§3's "thin but grounded" example) | harness | |
| SR-087 | `check_trajectory.py` | DEMOTES | internal top-view check | harness | |
| SR-088 | `gen_trajectory.py` | DEMOTES | render detail | generators | |
| SR-089 | `gen_trajectory.py` | DEMOTES | render detail | generators | |
| SR-090 | `gen_trajectory.py` | DEMOTES | render detail | generators | |
| SR-091 | `gen_trajectory.py` | DEMOTES | render detail | generators | |
| SR-092 | `gen_trajectory.py` | DEMOTES | interaction detail | generators | |
| SR-093 | `schedule.py` | DEMOTES | classification machinery | loop | |
| SR-094 | `schedule.py` | DEMOTES | cross-check machinery | loop | |
| SR-095 | supersession row | TOMBSTONE | registry bookkeeping (deletion narrative) | — | MH |
| SR-096 | supersession row | TOMBSTONE | same | — | MH |
| SR-097 | supersession row | TOMBSTONE | same | — | MH |
| SR-098 | supersession row | TOMBSTONE | same | — | MH |
| SR-099 | supersession row | TOMBSTONE | same | — | MH |
| SR-100 | supersession row | TOMBSTONE | same | — | MH |
| SR-101 | supersession row | TOMBSTONE | same | — | MH |
| SR-102 | `plan_round.py` (internal) | DEMOTES | dual-plan state machine internals | loop | |
| SR-103 | `plan_briefs.py` (internal) | DEMOTES | brief-assembly internals | loop | |
| SR-104 | `plan_coverage_step.py` (internal) | DEMOTES | adapter internals | loop | |
| SR-105 | `plan_artifacts.py` (internal) | DEMOTES | artifact/WI-filing internals | loop | |
| SR-106 | `plan_runner.py` (internal) | DEMOTES | round-execution internals | loop | |
| SR-107 | worker (internal) | DEMOTES | path-isolation mechanics | loop | |
| SR-108 | dual-plan round (internal) | DEMOTES | disposition mechanics | loop | |
| SR-109 | `check_trajectory.py` | DEMOTES | internal lifecycle check | harness | |
| SR-110 | `check_coverage.py` (internal) | DEMOTES | internal harness step | harness | |
| SR-111 | B-05: `bootstrap.py` | HOLDS | declared scaffold contract (kit-version stamp) | scaffold | |
| SR-112 | B-05: skills fan-out | HOLDS | delivered-content coherence property (skills are B-05 content per §1R.7(5)) | scaffold | |
| SR-113 | B-05: dev-setup launcher | HOLDS | declared launcher wires the hook floor | hook-floor | |
| SR-114 | B-05: kit scripts on 3 OSes | HOLDS | package-wide portability property, evidenced at B-06; ACC carries argument prose | pkg-wide | MH-acc |
| SR-115 | `schedule.py` | DEMOTES | ordering machinery | loop | |
| SR-116 | trunk lane (internal) | DEMOTES | trunk-step/status regen discipline; status.md is a REL-002 surface | loop | MH B03 |
| SR-117 | supersession row | TOMBSTONE | registry bookkeeping (deletion narrative) | — | MH |
| SR-118 | supersession row | TOMBSTONE | same | — | MH |
| SR-119 | supersession row | TOMBSTONE | same | — | MH |
| SR-120 | supersession row | TOMBSTONE | same | — | MH |
| SR-121 | supersession row | TOMBSTONE | same | — | MH |
| SR-122 | `gen_trajectory.py --check` | DEMOTES | freshness-check detail | generators | |
| SR-123 | `check_trajectory.py` | DEMOTES | internal ratchet check | harness | |
| SR-124 | `schedule.py` | DEMOTES | PlanMode-class machinery | loop | |
| SR-125 | dual-plan round (internal) | DEMOTES | PAGE-mapping mechanics; the ratification-level semantics live at SR-139 | loop | |
| SR-126 | `trace.py` | DEMOTES | internal strict rule; its script-name carve-out narrows in this window (13u rider) | harness | rider |
| SR-127 | `trace.py` | DEMOTES | internal form lint | harness | |
| SR-128 | `trace.py` | DEMOTES | internal paraphrase advisory | harness | |
| SR-129 | B-05: "The kit" (wi_convert) | HOLDS | package-level delivered converter capability; cites the retired CSV form | scaffold | MH |
| SR-130 | trunk step (internal, 13u) | DEMOTES | `trunk_step.py` = IF-081, ruled internal — demotion explicitly licensed | loop | MS(2) |
| SR-131 | pause file (internal) | DEMOTES | pause-drain mechanics; known migration-history flag row | loop | MH MS(2) |
| SR-132 | local integrator (internal, 13u) | DEMOTES | `integrate.py` = IF-080, ruled internal; six-clause mega-row | loop | MS(6) |
| SR-133 | B-05: `check.py` lane skip | HOLDS | declared harness-entry behavior on claimed branches | harness | |
| SR-134 | trunk step (internal) | DEMOTES | regen-order mechanics | loop | |
| SR-135 | pending surface (internal) | DEMOTES | REL-002 surface render detail | generators | B03 |
| SR-136 | `check_figures.py` (internal) | DEMOTES | internal harness step | harness | |
| SR-137 | B-01/B-02: `docs/process.toml` | HOLDS | the dial surface the session edits — §2's own worked PORT example; three shalls to reconcile with the form rule | — | MS(3) |
| SR-138 | B-05: `bootstrap.py --migrate-config` | HOLDS | declared scaffold contract (config conversion is its live purpose, not history) | scaffold | MS(3) |
| SR-139 | B-02: ratification ordinal | HOLDS | the authority-input semantics, stated at package level | — | MS(2) |
| SR-140 | B-02: attestation anchor | HOLDS | acceptance-recording semantics at the authority crossing | — | MS(3) |
| SR-141 | admission (internal) | RE-STATES | the adjudication-first + never-past-a-hold property is loop-contract level; the rank-table mechanism sheds; overlaps SR-148 (§5-F5) | loop | MS(2) |
| SR-142 | idle census (internal) | DEMOTES | census/routing machinery | loop | MS(2) |
| SR-143 | validator (internal) | DEMOTES | overlap-warning machinery | harness | |
| SR-144 | lane close (loop contract) | RE-STATES | no-silent-abandonment (terminal close + immutable record surfaced to adjudication) is SR-level, B-02-adjacent; directory/report mechanics shed | loop | MS(4) |
| SR-145 | disposition rows (internal) | DEMOTES | adjudication-record bookkeeping under the SR-144-level parent | loop | MS(3) |
| SR-146 | loop prompts (content) | RE-STATES | shipped-prompt auditability is a B-05 loop-content property; the prompt's flight to the model is REL-003, session-side, not a system crossing | loop | |
| SR-147 | B-05: spine carrier | HOLDS | package-level registry-carrier property; cites the 2026-08-10 cutover as history | scaffold | MH MS(2) |
| SR-148 | B-05: coordinator order | HOLDS | loop-contract-level selection order + holds from the declared level | loop | MS(2) |
| SR-149 | B-05: "The harness" | HOLDS | model of the target form — capability-level subject, module named only in ACC | harness | MS(2) |

## 4. What slice 2 must do (sized from this table)

1. **73 demotions.** Each mints an LLR id, re-points its TCs, re-homes its
   `sn_refs` through a parent SR. By capability: **loop 30 · harness 27 ·
   generators 16.**
2. **Parent-SR minting, along the capability axis.** The harness cluster has
   live parents (SR-006/007/008 + re-stated SR-049; SR-149 is the form
   model). The generators cluster's natural parent is **re-stated SR-070**.
   The loop cluster's entry contract holds (SR-026/027/028/030/148) but its
   sub-bundles — review/critique (8 rows), dual-plan (8), integration/trunk
   (5), scheduling (5), worker protocol (4) — need parents minted or folded
   under the invariant **one SR per (need, crossing-or-delivered-property)**
   (13p); the exact parent count falls out of the sn_refs join at execution,
   not this census.
3. **15 re-statements** against the crossing vocabulary — including SR-035's
   observable mint (the 13u rider's candidate is already ruled) and the four
   B-03-surface dashboard rows (SR-052/053/054/070) re-keyed to the
   generators capability.
4. **The riders:** SR-126's script-name carve-out narrowed in the same act;
   Area→`aspect` on 147 rows plus minting one for SR-049; SN-033…SN-040's
   first coverage (uncovered=8, bites at `trace.py --strict` from
   DevBar-Tests); the §6 items — migration-history scrubs (SR-040/059/131
   plus the census's additions, §5-F4) and SR-060's dead `next-wi` clause.
5. **Populate the SR-side interface-reference field** the schema row mints —
   machine-resolvable boundary ids land with WI-442 (`external.toml`); this
   census ran against §1R.2 as text, as scoped.
6. **17 multi-shall rows** to reconcile with the one-shall guideline — split,
   or keep with a recorded reason (13v).

## 5. Findings the census exposes (deliverables per 13s)

- **F1 — B-06/B-07 have no SR of their own.** No row states the hosted-CI
  crossings as its own obligation; the moment→tier CI mirror rides SR-019's
  acceptance cell and SR-114's evidence clause. Slice 2 should mint (or
  promote) a dedicated pair — §1R.6 already gives the artifact-shaped form.
- **F2 — the tombstone class needs one ruling, not 26 waivers.** 26 rows
  (17.6 %) are supersession bookkeeping; recommend a class exemption from the
  form rule, recorded once. 14 of them also carry the dispatcher-deletion
  narrative in their Requirement cells — acceptable *for tombstones* if the
  class ruling says so.
- **F3 — B-05 has package-wide properties that do not split by capability.**
  SR-034/114 (portability), SR-031 (dial coherence), SR-035
  (stack-agnosticism) are bundle-wide. The five-capability axis needs a
  declared sixth bucket (package-wide) or these four attach to B-05 direct.
- **F4 — the migration-history class is bigger than the three known rows.**
  Beyond SR-040/059/131: retired-mechanism narration in SR-026/046/060/116/129/147
  Requirement cells, live legacy migration-window clauses in
  SR-017/018/031/040/042/043/067 (a scrub-or-keep call per clause — the
  windows may still be live obligations), and history in acceptance cells on
  SR-021/114.
- **F5 — SR-141 and SR-148 state overlapping admission-order obligations**;
  slice 2 should merge or explicitly partition them.
- **F6 — data-invariant/checker near-pairs** (SR-015 vs SR-005): one states
  the registry-format invariant, one the checker that polices it — keep
  deliberately or fold, but say which.
- **F7 — SR-049 lacks `area`** — the one row the aspect conversion must mint
  rather than convert.
- **F8 — prior unverified sizing did not fully reproduce.** 75/18/57 and
  147/148 reproduce exactly; "120 leading subjects / 73 distinct" does not
  (this census: 128/81 under a stated method) — a small live example of why
  the declared-figure convention exists.

The census's judgment is one reader's; every classification above is
advisory-with-a-recorded-reason (13v), and the owner's sitting-3 ratification
is the act that makes any of it binding.
