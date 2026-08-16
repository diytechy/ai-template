# Blind re-derivation — alignment map (WI-467, ALIGNMENT pass)

**Date:** 2026-08-16 · **Pass:** ALIGNMENT (the only role permitted to read both
the fresh breakdowns and the legacy registries) · **Protocol:**
`docs/plans/2026-08-16-tiering-research-memo.md` §2 · **Spec:**
`docs/work/queued/WI-467-blind-rederivation-validation.md`.

**This is a validation instrument. It recommends no edit.** Every orphan below is
a *finding for the owner*, not a deletion candidate and not a mint order. Where a
legacy row looks unwanted, its own rationale is quoted first (the
read-rationale-before-judging rule) and the row is classified, never dispositioned.

**Inputs.** `2026-08-16-blind-derivation-a.md` (77 rows: 21 top-level + 56
sub-rows, actor/crossing axis) · `2026-08-16-blind-derivation-b.md` (73 rows: 24
top-level + 49 sub-rows, lifecycle axis) · `system-requirements.toml` (63 SRs,
one-decision reword landed) · `low-level-requirements.toml` (155) ·
`test-cases.toml` (150) · `interfaces.toml`.

**Join method.** Fresh rows were clustered into distinct *obligations* (C-##)
before legacy was opened. Fresh↔legacy joins key on the **SN reference set**
first, with **obligation text** as the tiebreaker where one SN carries several
rows. TC coverage is computed mechanically: `SR → LLR.sr_refs → TC.verifies`,
unioned with TCs verifying the SR directly.

---

## Part 1 — A ↔ B cross-team comparison (legacy unopened)

### 1.1 Convergent obligations — both teams derived it independently

59 clusters. These are the strongest signal in the exercise: two teams working
from different axes, with no shared vocabulary, landed on the same shall.

| C | Obligation | A | B | SNs |
|---|---|---|---|---|
| C1 | Single invoked action installs into new *or existing* repo; bar passes immediately | A-4, A-4.1 | B-1, B-1.1 | SN-001 |
| C2 | Re-application/re-sync preserves every adopter-authored file | A-4.1 | B-1.3, B-24 | SN-001 |
| C3 | Toolchain declared once; non-reference profile omits reference-only artifacts | A-4.2, A-5.2 | B-1.2 | SN-003 |
| C4 | Legacy config converted at install *and* documented re-sync | A-4.3 | B-1.4, B-24 | SN-028 |
| C5 | Every adopter-run check runs on a clean minimum runtime, all supported OSes | A-17 | B-2, B-2.2 | SN-011 |
| C6 | Non-stdlib dependency only via reviewed ledger row; undeclared import fails the kit's own suite | A-17.1, A-17.2 | B-2.1 | SN-011 |
| C7 | OS × runtime matrix exercised and green as a landing condition | A-20.2 | B-2.3 | SN-011, SN-007 |
| C8 | Every shipped file maps to a stakeholder outcome; generated maps via generator | A-9, A-9.2 | B-3, B-3.2 | SN-038 |
| C9 | A declared inventory + exclusions defines the coverage universe | A-9.1 | B-3.1 | SN-038 |
| C10 | Front-door single-action entry point per platform for both universal actions | A-16, A-16.1 | B-4, B-4.1, B-4.2 | SN-034 |
| C11 | Action menu enumerated from one declared action inventory | A-16.3 | B-4.3 | SN-035 |
| C12 | One policy home; a doubly-declared dial is **refused**, never precedence-resolved | A-15 | B-5 | SN-028 |
| C13 | Both readers (full parser + minimal parser) resolve every dial identically | A-15.1 | B-5.1 | SN-028, SN-009 |
| C14 | Wrong-typed / out-of-range dial refused, never silently defaulted | A-15.2 | B-5.2 | SN-028, SN-029 |
| C15 | Optional layers cost a repository that has not opted in **nothing** | A-18, A-18.1 | B-6 | SN-012 |
| C16 | Chain mechanically joined; orphans reported; a gate needs zero | A-6, A-6.1 | B-7 | SN-002 |
| C17 | Malformed/duplicate identifier fails at every stage that reads it | A-6.2 | B-7.1 | SN-002 |
| C18 | Need cells free of internal path / impl id / process citation, reviewed exception list | A-7, A-7.1 | B-8, B-8.1 | SN-033 |
| C19 | Every non-example need row carries a closed-vocabulary scope value | A-7.2 | B-8.2 | SN-039 |
| C20 | Machine-readable perspective record per decomposition; applicable-but-absent is a finding | A-7.3 | B-9, B-9.1 | SN-036 |
| C21 | Partition derivation record: candidates, objective, constraints, selection, human ruling | A-8.3 | B-9.2 | SN-040 |
| C22 | Every requirement I/O resolves to a declared interface with endpoints + discrete/variable signal | A-8, A-8.1 | B-10, B-10.1 | SN-037 |
| C23 | Every declared component-boundary crossing has an interface row | A-8.2 | B-10.1 | SN-037 |
| C24 | A one-sided requirement/interface change carries or justifies its counterpart | A-8.2 | B-10 | SN-037 |
| C25 | Every module is a declared endpoint or an explicit source/sink (warn-first) | A-10.3 | B-10.2 | SN-023, SN-037 |
| C26 | Enforcement agent-neutral; per-agent config mirrors the floor, never replaces it | A-1.4, A-19 | B-11 | SN-005 |
| C27 | Accept/reject verdict returned at the moment of the guarded act | A-2 | B-11.1 | SN-005 |
| C28 | The local floor is bypassable → the claim is the **pair**, local verdict + hosted re-run | A-2.1, A-20.4 | B-11, T-4 | SN-005, SN-008 |
| C29 | Hosted run invokes the documented entry point at the declared per-trigger tier, pinned by test | A-20, A-20.1 | B-11.2 | SN-005 |
| C30 | Secrets floor always on, over staged content + message + outgoing range, zero adopter setup | A-1.1 | B-12, B-12.1 | SN-009 |
| C31 | Identity/PII classes added on the declared dial; an unreadable dial refuses, never silently off | A-1.1 | B-12.2 | SN-009, SN-028 |
| C32 | The gate in force selects the required step set, not the operator | A-5, A-5.1 | B-13, B-13.1 | SN-004 |
| C33 | Missing tool **fails**; exactly one explicitly-requested local degrade, never a gate/hosted default | A-5.1 | B-13.2 | SN-004, SN-008 |
| C34 | Stub / unmet-criterion detectors run at the declared gate and red the bar | A-5.4 | B-13.3 | SN-008 |
| C35 | Subjective acceptance judged by a fresh, cross-family session, never the author | A-14 | B-14 | SN-024 |
| C36 | Rubric derived from need/requirement intent (not the test), numbered anchors cited | A-14.1 | B-14.1 | SN-024 |
| C37 | Bounded iteration; budget exhaustion escalates to a human, never passes | A-14.2 | B-14.2 | SN-024, SN-029 |
| C38 | The kit holds itself to the bar it delivers: install-and-exercise suite green before a change lands | A-21, A-21.1 | B-15 | SN-007 |
| C39 | Unattended run resumes from tracked state, never prompts, ends in a typed outcome | A-11, A-11.2 | B-16, B-16.2 | SN-006 |
| C40 | Preflight refuses a broken footing rather than starting and hanging | A-11.1 | B-16.1 | SN-006 |
| C41 | Next work derived from the tracked work graph + VCS, never prose or a hand-kept pointer | A-11.3 | B-17 | SN-025 |
| C42 | The ready frontier is deterministically ordered | A-11.4 | B-17.1 | SN-025, SN-027 |
| C43 | The human-read status surface is generated, never hand-copied | A-10.2 | B-17.2 | SN-025, SN-010 |
| C44 | Bounded lanes in isolated working copies; ceiling-1 preserves the serial semantic | A-12, A-12.1 | B-18, B-18.1 | SN-027 |
| C45 | One serial fail-closed integrator runs the declared bar on the composed tree | A-12.2 | B-18.2 | SN-027, SN-008 |
| C46 | A declared pause stops new claiming while draining in-flight work | A-12.3 | B-18.3 | SN-027 |
| C47 | A crash at any lifecycle boundary recovers from VCS alone, no double-assignment | A-12.4 | B-18.3 | SN-027 |
| C48 | Model capacity declared as (family × level) registry rows, selected per job | A-13, A-13.1 | B-19, B-19.1 | SN-026 |
| C49 | An explicit consent surface turns managed selection on; absent = unchanged behavior | A-13.1 | B-19 | SN-026, SN-012 |
| C50 | Cross-family draw preferred for second-opinion roles | A-13 | B-19 | SN-026 |
| C51 | Documented single-family degrade, never a silent skip | A-13.2 | B-19.2 | SN-026, SN-024 |
| C52 | Every selection logged **before** launch — no silent model swap | A-13.3 | B-19 | SN-026 |
| C53 | Authority reserved by a declared cumulative level compared against a separately derived stage | A-3, A-3.1 | B-20, B-20.1 | SN-029, SN-004 |
| C54 | Every malformed authority input resolves toward **more** human involvement | A-3.4 | B-20.2 | SN-029, SN-008 |
| C55 | Acceptance anchored to the accepted text; later drift surfaces regardless of status movement | A-3.3 | B-21, B-21.1, B-21.2 | SN-029, SN-002 |
| C56 | A delegated approval leaves a record distinguishable from a human's **by query** | A-3.2 | B-21.3 | SN-029 |
| C57 | One reader-facing surface showing progress **and** the connection graph | A-10.3 | B-22 | SN-023 |
| C58 | Docs navigable: intra-repo links resolve; purpose declared exactly once | A-10, A-10.1 | B-23, B-23.1 | SN-010 |
| C59 | Every generated artifact carries a freshness contract that fails when stale | A-10.2 | B-23.2 | SN-010 |

### 1.2 Single-team obligations — one team stated it, the other did not

12 clusters. Weaker signal: possibly a real obligation one axis surfaces better,
possibly an axis artifact.

| id | Obligation | Team | SNs | Why the other axis may have missed it |
|---|---|---|---|---|
| S-A1 | A-1.2 — the fast process floor (format + spine integrity + the in-process gate's required checks) applies at admission | A | SN-004, SN-005, SN-008, SN-002 | B's L3 stage states the *verdict* (B-11.1) but never enumerates the floor's content beyond secrets |
| S-A2 | A-1.3 — every refusal names the failing check **and** locates the offending row or phrase | A | SN-008, SN-005 | B states it per-check (B-8.1 row+phrase, B-5.2 offending key), never as one property |
| S-A3 | A-5.3 — declared cost tiers: exactly one definition of passing per moment (per-change / slice close / release) | A | SN-005, SN-012, SN-007 | B carries only the hosted half (B-11.2); the local half has no lifecycle home |
| S-A4 | A-16.2 — the adopter-facing guide names the front-door capability and invites its reuse | A | SN-034 | Documentation-of-a-capability is not a lifecycle stage |
| S-A5 | A-18.2 — a stated proportionality rule governs design/test decomposition granularity | A | SN-012 | B's B-6 reads SN-012 as cost-of-optional-layers only, missing the granularity half |
| S-A6 | A-20.3 — the hosted step log locates the failing step without a local re-run | A | SN-008, SN-005 | B-16.2 states the same idea for the *loop*, never for hosted CI |
| S-B1 | B-7.2 — the join is produced from the registries at check time, never hand-maintained | B | SN-002, SN-010 | A folds this into the generic freshness contract (A-10.2) |
| S-B2 | B-16.2 — each end state reported as a machine outcome **and** a terminating human-readable summary | B | SN-006 | A-11.2 states the machine code only |
| S-B3 | B-19.1 — provider turnover is a data change; zero provider names in executable content | B | SN-026 | A-13.1 says "declared as registry rows" without the negative clause |
| S-B4 | B-20 — the three stop causes are a closed classification (`unclassified stops = 0`) | B | SN-029 | A-3.1 states the level, never that the stop set is exhaustive |
| S-B5 | B-21.4 — authority inputs enter through the **same governed write path** as any other change | B | SN-005, SN-029 | A treats B-02 as its own channel (A-3) and never joins it to B-01 |
| S-B6 | B-24.1 — the release-tier bar is a distinct explicit gate reachable only from passed prior bars | B | SN-004, SN-008 | A's actor axis has no release moment; no crossing carries it |

### 1.3 Divergences — the two teams state the same thing differently

No flat contradiction was found. Five divergences of placement or claim strength:

| D | Subject | A's position | B's position | Note |
|---|---|---|---|---|
| D1 | SN-023's rendered surface | Outside the boundary; only the *generator capability* is claimable at B-05 (A-T1) | Stated flatly as a delivered surface obligation (B-22), no caveat | The sharpest divergence: A thinks the frame forbids what B asserts |
| D2 | Hosted re-run strength | "caught by the hosted run **100% of the time**" (A-20.4) | Pinnable only for the shipped configuration; unverifiable by construction for an adopter (B-T4) | Same obligation, materially different observable |
| D3 | Partition record crossing | B-05 alone (A-8.3) | B-05 **and B-02** — the human ruling is an authority act (B-9.2) | Legacy sides with A (see §2.1, SR-165) |
| D4 | Module-endpoint check placement | Generator bundle (A-10.3) | Authoring stage (B-10.2) | Axis artifact; obligation identical |
| D5 | SN-037's reach | A-8 family only | Also B-9.2 (partition) and B-10 pulls in SN-023 | B spreads one need across two stages |

### 1.4 Merged tension list

**Hit by BOTH teams independently — the strongest defect signal in this exercise:**

| TT | Tension | A | B |
|---|---|---|---|
| **TT1** | SN-005 is only decidable as a **pair** (act-time verdict + hosted re-run); no single capability can carry it | T-3 | T-4 |
| **TT2** | SN-007 ("hold the kit to its own standard") has no crossing and is not a stage — it re-enters everything at once and cannot be placed | T-2 | T-2 |
| **TT3** | SN-035 (this-repo action menu) has no natural home on either axis; its real content is a governance act, not a delivered obligation | T-2 | T-1 |
| **TT4** | Model-provider obligations sit on REL-003; every derivable observable is the loop's **self-report**, a weaker evidence class than the needs' wording implies | T-4 | T-6(a) |
| **TT5** | Second-system guard fired on both sides: frame/README promises with no SN behind them (A: license text, launcher phrasing; B: versioned release artifacts, changelogs) | T-6 | T-3 |
| **TT6** | SN-023 is structurally awkward — A: no out-crossing for the reader-facing surface; B: it straddles two lifecycle moments. Same need, two independent complaints | T-1 | T-8 |
| **TT7** | SN-029 entangles with its neighbours — A: SN-025 vs SN-029 pull opposite ways and only a dial resolves them; B: SN-004/008/029 all answer "what does the gate say" | T-7 | T-5 |

**A-only:** TA1 (SN-034 spans a crossing and a non-crossing — the "fresh scaffold
**and** this repository" clause, T-5) · TA2 (SN-009's "every repo, no extra
setup" outruns B-01's hook-floor carrier; the promise splits across two crossings'
worth of delivered content, T-8).

**B-only:** TB1 (**nothing in the SN set says how authority arriving at B-02 is
authenticated** — B-21 can require it be recorded, never that its source be
proven, T-6(b)) · TB2 (SN-012's obligation is an *absence*, verifiable only
differentially against configurations the kit itself defines — near
self-referential, T-7) · TB3 (scope-qualified needs hold in two products at
once, T-9).

---

## Part 2 — Fresh ↔ legacy alignment

### 2.1 MATCHED — 47 legacy SRs

Fit: **exact** = same obligation, same reach · **narrower** = SR is one instance
of a broader fresh capability · **broader** = SR spans several fresh rows.

| SR | Title | Fresh | Fit | LLR | TC coverage |
|---|---|---|---|---|---|
| SR-006 | Gate/tier harness enforces required steps | A-5, A-5.1 / B-13, B-13.1, B-13.2 | broader (also carries the work-branch skip, which no fresh row demands) | 6 | TC-006, 008, 014, 016, 101, 134 |
| SR-007 | Declared stack profile, refused when broken | A-5.2 / B-1.2 | exact | 2 | TC-007, 008 |
| SR-009 | Conditional scaffold profiles | A-4.2 / B-1.2 | exact | 1 | TC-009 |
| SR-010 | Scaffold runs green out of the box | A-4 / B-1, B-1.1 | exact | 1 | TC-010 |
| SR-011 | Idempotent re-runnable scaffold | A-4.1 / B-1.3 | exact | 1 | TC-011 |
| SR-017 | Always-on secrets floor | A-1.1 / B-12.1 | exact | 1 | TC-017 |
| SR-018 | Privacy gate two-axis | A-1.1 / B-12.2 | exact | 1 | TC-018 |
| SR-019 | Pre-commit hook floor | A-1, A-1.4, A-2, A-2.1 / B-11, B-11.1 | exact (both sides state the pair) | 2 | TC-019, 021 |
| SR-020 | Pre-push hook outgoing scan | A-1.1 / B-12.1 | narrower (one of three surfaces) | 2 | TC-020, 021 |
| SR-022 | Vendored-doc drift | A-10 / B-23 | narrower (one drift class) | 1 | TC-022 |
| SR-026 | Coordinator resumes headless | A-11 / B-16 | exact | 3 | TC-026, 061, 137 |
| SR-027 | Coordinator preflight | A-11.1 / B-16.1 | exact | 3 | TC-027, 029, 030 |
| SR-028 | Coordinator typed outcomes | A-11.2 / B-16.2 | narrower (B also wants the human summary — S-B2) | 1 | TC-028 |
| SR-031 | Declared-policy readers agree | A-15.1 / B-5.1 | exact | 1 | TC-031 |
| SR-032 | Onboarding and dev-setup scaffold | A-16 / B-4.1 | narrower (SR = it *works*; fresh = it *exists at the front door*) | 1 | TC-032 |
| SR-034 | Kit scripts on stdlib + ledger deps | A-17.1, A-17.2 / B-2.1, B-2.2 | exact | 0 | TC-034, 149 |
| SR-035 | No language-specific token in the shipped scheme | A-4.2 / B-1.2 | narrower | 1 | TC-035, 165 |
| SR-036 | Deliberate re-sync integration | A-4.1 / B-24 | exact | 0 | TC-036 (evidence = ADOPTING.md, Inspection) |
| SR-040 | Per-phase routing and review dial | A-13 / B-19 | narrower; its resume-surface size tripwire matches nothing fresh | 1 | TC-040 |
| SR-046 | Run capability menu | A-16.3 / B-4.3 | exact | 1 | TC-047 |
| SR-049 | Derived gate from artifact states | A-3.1, A-3.3 / B-20.1, B-21.2 | exact | 4 | TC-050, 123, 141, 142 |
| SR-070 | Generated views offline/deterministic/drift-checkable | A-10.2 / B-23.2 | broader (offline + byte-stable exceed both fresh rows) | 6 | TC-023, 038, 042, 078, 079 |
| SR-113 | Dev-setup wires the process floor | A-1.1 + A-T8 / B-12 | narrower — A's T-8 derived exactly this dependency | 1 | TC-032 |
| SR-114 | Kit scripts run across supported OSes | A-17 / B-2, B-2.3 | exact | 0 | TC-035 |
| SR-137 | One policy home, with a checked shape | A-15, A-15.2 / B-5, B-5.2 | exact | 1 | TC-150, 151 |
| SR-138 | Legacy config converts automatically and totally | A-4.3 / B-1.4 | exact | 1 | TC-152 |
| SR-139 | Ratification as an ordinal over a derived spine stage | A-3.1, A-3.4 / B-20.1, B-20.2 | exact | 2 | TC-150, 151 |
| SR-140 | Acceptance recorded by a copy riding its approval commit | A-3.2, A-3.3 / B-21, B-21.2, B-21.3 | exact (mechanism differs; obligation identical) | 2 | TC-153, 167 |
| SR-148 | Autonomous loop work selection | A-11.3, A-11.4 / B-17, B-17.1, B-17.2 | broader (6 sn_refs; fresh splits it across four rows) | 10 | TC-058, 059, 060, 091, 097, 143, 146, 154, 161 |
| SR-150 | SN cells stay in stakeholder language | A-7.1 / B-8.1 | exact | 1 | TC-164 |
| SR-151 | Hosted CI runs the declared bar per trigger | A-20, A-20.1 / B-11.2 | exact | 0 | **none** |
| SR-152 | Hosted CI verdict is the harness's own | A-20.3, A-20.4 / B-11 | exact | 0 | **none** |
| SR-154 | Independent review routed across families | A-13, A-13.1–.3, A-14 / B-19, B-19.1–.2, B-14 | broader (merges A's and B's model-routing *and* critique clusters) | 6 | TC-046, 048, 082, 083, 084, 085 |
| SR-156 | Bounded lanes narrowing to one gated landing | A-12, A-12.1–.4 / B-18, B-18.1–.3 | exact | 5 | TC-131, 132, 139, 144, 145 |
| SR-157 | Spine + work-registry rules red the harness verdict | A-6, A-6.1, A-6.2 / B-7, B-7.1 | broader (also work-item coherence, which no fresh row demands) | 15 | TC-001–005, 037, 075, 077, 086, 100, 126, 127, 128, 155 |
| SR-158 | Documentation drift reds or warns per its tier | A-10, A-10.1 / B-23, B-23.1 | exact | 4 | TC-012, 013, 041, 140 |
| SR-159 | Declared-architecture connectivity gaps | A-8.2, A-10.3 / B-10.2 | exact | 5 | TC-044, 049, 067, 068, 080 |
| SR-160 | Front-door launchers, two universal actions | A-16, A-16.1, A-16.2 / B-4, B-4.1, B-4.2 | exact | 0 | **none** |
| SR-161 | Decompositions carry a perspective record | A-7.3 / B-9.1 | exact | 0 | **none** |
| SR-162 | Requirement boundary refs resolve against the frame | A-8, A-8.1 / B-10, B-10.1 | narrower — the two-sided-change clause (C24) is a **named residual** in its own rationale | 0 | **none** |
| SR-163 | Every shipped file maps to a stakeholder outcome | A-9, A-9.1, A-9.2 / B-3, B-3.1, B-3.2 | exact | 0 | **none** |
| SR-164 | SN scope is a declared, checked value | A-7.2 / B-8.2 | exact | 0 | **none** |
| SR-165 | Partition carries a reproducible derivation record | A-8.3 / B-9.2 | exact (crossing attribution differs — D3; legacy sides with A) | 1 | TC-166 |
| SR-166 | Package materializes where its manifest declares | A-4 / B-1.1 | narrower | 0 | **none** |
| SR-168 | State view shows current progress and next work | A-10.3 / B-22 | exact (the progress conjunct) | 6 | TC-038, 051, 052, 056, 057, 136 |
| SR-169 | State view shows how the parts connect | A-10.3 / B-22 | exact (the connection conjunct) | 5 | TC-081, 087, 088, 089, 090 |
| SR-170 | Shared authority surfaces are the serial actor's alone | A-12.2, A-12.4 / B-18.2 | narrower (the id-mint half matches nothing fresh) | 7 | TC-060, 130, 134, 135, 147, 148, 158 |

*47 rows. SR-040 also appears in §2.2: the row matches on its routing half, and
only its resume-surface tripwire clause is orphaned, so it is counted here.
47 matched + 16 orphaned = 63.*

**Observation from the join, not from either side:** the 2026-08 re-tier's
newest rows (SR-160 through SR-166) match fresh capabilities **exactly** and
carry **zero TCs** — they are `Drafted`, phase 5, un-decomposed. The blind teams
independently demanded precisely the obligations legacy has stated but not yet
tested. That is a *good* signal about the re-tier's targeting and a plain reading
of where the untested frontier is.

### 2.2 ORPHANED-IN-LEGACY — 16 SRs no fresh capability demands

Classification: **(i)** implementation-born (a derived-requirement candidate, the
DO-178C class — traceable to *how* the system was built, not to a need)
· **(ii)** genuine need the blind teams missed because the SN/frame understates
it (a **NEEDS** defect, not an SR defect) · **(iii)** true accretion.

| SR | Rationale, in its own words (one line) | Class | Note |
|---|---|---|---|
| **SR-015** Perf-budget back-links | "Realizes SN-002 — the off-spine budget rows stay traceable to the spine." | **(ii)** | No SN demands a performance layer at all; SN-012 names "perf" only parenthetically as an opt-in. Neither team derived any perf obligation. |
| **SR-024** Permutation case generation | "dimensional coverage is generated from the SR's declared inputs, not hand-listed." | **(i)** | A test-authoring mechanism. No SN asks for dimensional coverage. |
| **SR-033** Release checklist generation | "SN-004 — the release gate has a generated checklist surfacing the budgets a human must tick off." | **(i)** | Adjacent to B-24.1 (release gate exists), but the *generated checklist* is machinery. |
| **SR-040**† Resume-surface size tripwire clause | "a growing resume surface is a smell and not a defect, and failing on a smell trains an operator to bypass the check." | **(i)** | Row matched on its routing half (§2.1); this clause alone is orphaned. |
| **SR-043** Subagent spawn gate | "SN-006 (a walk-away run stays safe — bounded, supervised fan-out with the override held by the human, not the model)" | **(ii)** | SN-006's *safety* half lives only in its `why` cell; its `need` and `acceptance` say only *resumable*. Both teams therefore derived resumability and nothing about bounding what an agent may spawn. |
| **SR-052** Dashboard accessibility | "perceptual accessibility has no crisp measurable interface, so a row claiming a mechanized verification would assert a green that nothing actually checks." | **(ii)** | See cluster note below. |
| **SR-053** Dashboard UI uniformity | "how alike is alike enough is subjective at the margins, so cross-view coherence cannot be pinned to a threshold without pinning the wrong thing." | **(ii)** | 8 LLRs, 8 TCs. |
| **SR-054** Dashboard usability | "task-level usability is perceptual (is this findable, is this legible), so a test can confirm an element exists and not that a reader can use it." | **(ii)** | 9 LLRs, 9 TCs. |
| **SR-111** Kit-version stamp | "without a recorded origin an adopter cannot tell which kit version they are on, so a re-sync degrades from a diff into a guess." | **(i)** | Textbook derived requirement: it exists because C2/SR-036's re-sync needs a baseline. |
| **SR-112** Checked per-agent skill fan-out | "each agent harness looks in its own path; the fan-out is forced, so the copies are generated and drift is a finding." | **(i)** | The rationale says outright that the obligation exists because of an implementation constraint. |
| **SR-129** Registry representation migration | "an unproven representation change is where a registry silently loses cells." | **(i)** | A migration mechanism for an internal carrier change. |
| **SR-144** Lane close = terminal state + immutable record | "Five successive dedup mechanisms leaked because each reconstructed the return event from a MUTABLE proxy." | **(i)** | Adjacent to C47 (crash recovery); the per-close immutable report with keep/discard split is defect-response machinery. |
| **SR-146** Prompts are reviewable files + audit trail | "Prose steers the sessions this loop launches and had been reviewable only by reading Python source, which makes the process trusted rather than inspectable." | **(ii)** | Both teams read SN-005's "same playbook" as *enforcement neutrality* only (C26). Instruction **inspectability** is a second reading of the same need that neither team reached — the need does not say it. |
| **SR-147** One machine-parseable carrier | "The two-carrier split has no recorded rationale and costs on both sides… CSV cannot represent the cells that actually exist." | **(i)** | Explicitly a tooling-cost argument. Pure derived requirement. |
| **SR-149** Retired-vocabulary refusal | "an earlier sweep removed a retired-tag construct… and it REGENERATED within days. A ~2,500-edit conversion held in place by attention is a conversion that comes undone." | **(i)** | A migration-support check. Neither team stretched SN-010's honesty to vocabulary hygiene. |
| **SR-155** Contested planning rounds | "Realizes SN-024 (a decomposition judged by a competing plan and an independent arbiter rather than its author)" | **(ii)/(iii)** | SN-024's subject is *subjective/perceptual acceptance*; SR-155 extends it to **planning**. 11 LLRs, 10 TCs — the largest need-less structure in the corpus. |
| **SR-167** Perf-budget breach verdict | "Vacuous in THIS repository… but the template ships the layer, and the owner's ruling is that a shipped layer owes a stated, tested obligation even where locally unused." | **(ii)** | The rationale itself records that this row exists because a layer ships, not because a need asks. |

† SR-040 is counted in MATCHED; only its tripwire clause is orphaned. Distinct
orphaned rows: **16**.

**The dashboard-quality cluster (SR-052/053/054).** Three rows, 22 LLRs, 22 TCs,
all phase 3, all priority C. Both teams derived the *critique mechanism* (C35,
C36, C37 — SN-024) with high confidence and neither derived a single obligation
about the dashboard being accessible, uniform or usable. SN-023 demands that a
reviewer *can see* progress and connections; SN-024 demands that *subjective
acceptance be adjudicated*. Neither states a perceptual **quality bar** for the
delivered view. Class (ii): if these obligations are wanted, the need that wants
them is not written down.

### 2.3 ORPHANED-IN-FRESH — 11 fresh capabilities with no carrying SR

| Fresh | Obligation | SN | Verdict | Evidence |
|---|---|---|---|---|
| **C34** (A-5.4 / B-13.3) | Stub / unmet-criterion detectors run at the declared gate and red the bar | SN-008 | **REAL HOLE** | `stub` appears **0 times** in all 63 SRs; SN-008's own acceptance names "the no-stub detector"; `check.py` has a `no-stub` step; LLR-016 (`check_stubs.py`) and TC-016 exist and hang off **SR-006**, whose shall says nothing about stubs. Built, designed, tested — stated by no requirement. |
| **C24** (A-8.2 / B-10) | A one-sided requirement/interface change carries or explicitly justifies its counterpart | SN-037 | **REAL HOLE, already known** | SR-162's own rationale: *"NAMED RESIDUAL… the need's last clause… is a REVIEW obligation this row does not claim to mechanize, and no SR states it yet."* Both blind teams demanded it anyway. |
| **C15** (A-18, A-18.1 / B-6) | Optional layers cost a non-adopting repository nothing — as a package-wide property | SN-012 | **REAL HOLE** | SN-012 has 9 citing SRs, but in every one the vacuity is a *secondary clause* ("a repo declaring no PB rows pays nothing"). No SR's subject is right-sizing. B-T7 independently flags this observable as the weakest in its breakdown. |
| **S-A5** (A-18.2) | A stated proportionality rule governs design/test decomposition granularity | SN-012 | **REAL HOLE** | `proportional` and `granularity` each appear **0 times** in the SR corpus; SN-012's acceptance names "the proportionality doctrine governs LLR/TC granularity". |
| **S-A2/C26** (A-19) | One guide governs humans and agents; per-agent config mirrors it, never replaces it | SN-005 | **REAL HOLE** | `playbook`, `one guide` and `PROCESS.md` each appear 0 times in the SR corpus. SR-112 covers *generated skill copies*; nothing covers the governing guide itself. |
| **C38** (A-21, A-21.1 / B-15) | The kit's own registries pass its own join; the full suite is green before a change lands | SN-007 | **PARTIAL HOLE** | The only carrier is a clause in **SR-010's acceptance** ("the meta-suite runs every script against that scaffold"). No SR states the pre-landing green bar or the self-applied join. Both teams flagged SN-007 as unplaceable (TT2) *and* still derived the obligation. |
| **S-A3** (A-5.3) | Exactly one definition of passing per moment, local and hosted alike | SN-005 | **PARTIAL HOLE** | SR-151 pins the hosted half against `[ci-tiers]`; SR-006 offers `--tier`. Nothing states the local↔hosted equality of the moment-to-tier table. |
| **S-A2** (A-1.3) | Every refusal names the failing check and locates the offending row or phrase | SN-008, SN-005 | **DISTRIBUTED, no single home** | Stated per-check in SR-157, SR-137, SR-150, SR-162. Effectively covered; the cross-cutting property has no home. Not a coverage hole in practice. |
| **S-B2** (B-16.2) | A terminating human-readable summary beside the machine outcome code | SN-006 | **OVER-READ** | SN-006's acceptance demands only "exits a **typed code** at each end state". SR-028 delivers exactly that. B added the human half. |
| **S-B6** (B-24.1) | A distinct release gate reachable only from passed prior bars | SN-004 | **OVER-READ / covered** | SR-049 derives the gate ladder from artifact states; SR-006 runs the gate in force. B's release stage is an axis artifact, and B's own T-3 admits "the release stage is thinly demanded". |
| **S-B5** (B-21.4) | Authority inputs enter through the same governed write path | SN-005, SN-029 | **COVERED** | SR-019's hook floor runs on *every* commit agent-neutrally; an attestation commit is a commit. Nothing exempts authority. |

Real or partial holes: **7**. Over-read or covered: **4**.

---

## Part 3 — Headline numbers and the top-10 for the sitting desk

### 3.1 Counts

| Measure | Value |
|---|---|
| Fresh rows read | A: 77 (21 top + 56 sub) · B: 73 (24 top + 49 sub) |
| Distinct obligation clusters across A ∪ B | **71** |
| — convergent (both teams) | **59 (83%)** |
| — single-team A | 6 |
| — single-team B | 6 |
| Flat contradictions between A and B | **0** (5 divergences of placement or claim strength) |
| Tensions raised | A: 8 · B: 9 · merged distinct: **12** · **hit by both teams: 7** |
| Legacy SRs | **63** |
| — MATCHED | **47 (75%)** |
| — ORPHANED-IN-LEGACY | **16 (25%)** — class (i) 8, class (ii) 7, class (ii)/(iii) 1 |
| ORPHANED-IN-FRESH | **11** — 7 real/partial holes, 4 over-read or covered |
| Matched SRs with **zero** TC coverage | **8** (SR-151, 152, 160, 161, 162, 163, 164, 166 — all `Drafted`, phase 5) |

### 3.2 Top-10 findings, ranked

1. **The no-stub detector is built, designed, tested — and stated by no requirement.** `stub` occurs 0× across all 63 SRs; LLR-016/TC-016 hang off SR-006 whose shall never mentions it. Both teams demanded it independently. *(A-5.4 + B-13.3 → no SR → SN-008.)* Same defect class SR-167's own rationale describes for the perf verdict — a repeat, not a one-off.
2. **Three dashboard-quality SRs, 22 LLRs and 22 TCs rest on a need neither team could reach.** Both derived the critique *mechanism*; neither derived a perceptual quality bar for the delivered view. *(no fresh row → SR-052/SR-053/SR-054 → SN-024, SN-023.)*
3. **SN-037's two-sided-change clause is demanded by both teams and admitted missing by legacy itself.** SR-162's rationale calls it a "NAMED RESIDUAL… no SR states it yet". *(A-8.2 + B-10 → gap under SR-162 → SN-037.)*
4. **SN-012's right-sizing has 9 citing SRs and no home.** Every citation is a secondary vacuity clause; no SR's subject is the property. B independently rated its own observable for this the weakest in its breakdown. *(A-18 + B-6 → no SR → SN-012.)*
5. **SN-007 cannot be placed by either axis, yet both derived its obligation anyway** — and legacy carries it only as a clause inside SR-010's acceptance. *(A-21/A-21.1 + B-15 → SR-010 acceptance only → SN-007.)*
6. **SR-155 (contested planning, 11 LLRs / 10 TCs) is the corpus's largest structure with no need behind its subject.** SN-024 governs *perceptual acceptance*; SR-155 extends it to planning. *(no fresh row → SR-155 → SN-024.)*
7. **SN-006's safety half lives only in its `why` cell, so SR-043 (subagent gate) reads as need-less.** Both teams derived resumability and neither derived bounded fan-out — a needs defect, not an SR defect. *(no fresh row → SR-043 → SN-006.)*
8. **The perf layer ships with three SRs and no need.** SR-167's own rationale concedes the row exists because a layer ships, not because a need asks; SR-015 and SR-033 sit on the same footing. *(no fresh row → SR-015/SR-033/SR-167 → SN-012, SN-002, SN-004, SN-008.)*
9. **SN-005's "same playbook" has two readings and the SR layer carries only one.** Both teams read enforcement-neutrality (SR-019, covered); nobody derived instruction-inspectability (SR-146) or the one-guide obligation (A-19, uncovered). *(A-19 → no SR; SR-146 → no fresh row → SN-005.)*
10. **Eight matched SRs carry zero TCs — and they are exactly the rows the blind teams matched most cleanly.** SR-160/161/162/163/164/166 (plus SR-151/152) are `Drafted`, phase 5, un-decomposed. Convergent demand, zero verification. *(A-16/A-7.3/A-8.1/A-9/A-7.2 + B-4/B-9.1/B-10.1/B-3/B-8.2 → SR-160–166 → SN-034, SN-036, SN-037, SN-038, SN-039.)*

### 3.3 Three structural readings the desk may want

- **The one-decision reword did its job.** 47 of 63 SRs joined to a fresh
  capability on obligation text alone, and the newest re-tier rows joined
  *exactly*. Where the join was hard it was hard for content reasons (§2.2), not
  because the text was unreadable.
- **The orphan classes split cleanly and unevenly.** 8 of 16 legacy orphans are
  class (i) — derived requirements the DO-178C model expects to exist and expects
  to be *labelled* as derived. 7 are class (ii): the needs understate something
  the kit really does. Only SR-155 leans toward (iii).
- **Every real fresh-side hole is a *package-wide property*** — right-sizing,
  proportionality, one-guide, self-application, one-definition-of-passing,
  refusal-legibility. The SR layer is strong at per-capability obligations and
  thin at properties that hold across the package. That is a shape, not a list of
  mistakes.

---

## 4. Hat-aware delta (team C)

Team C re-ran the derivation with `docs/requirements/hats.toml` in the blind input set (13 hats, 8 reachable, 5 aspect hats shipped OFF): 80 rows, 64 reachable + 16 conditional. A hat is a *lens*, so its yield is the DO-178C **derived requirement** class — legitimate only when the deriving lens is named. That is precisely the label §2.2 could not apply.

### 4.1 Re-test of finding #2 — the SR-052/053/054 quality family

A and B derived the critique *mechanism* and no quality bar. C splits the family three ways, and the split is the finding:

| SR | Obligation | Deriving lens | Status |
|---|---|---|---|
| SR-054 usability | findability — declared reader, decision answered in the first viewport | **UX-DESIGNER** (C-UXD-1/6), `always` | **now derivable** |
| SR-054 / SR-052 | legibility **as robustness** — verified as rendered, no clipping, malformed ≠ empty | **UX-ENGINEER** (C-UXE-1/2/3), `always` | **now derivable** |
| SR-052 accessibility | keyboard + assistive-tech operability; **measurable** contrast/size/zoom thresholds | **ACCESSIBILITY** (C-ACC-1/3), tag-gated, **shipped OFF** | derivable only from a lens nobody can switch on |
| **SR-053 uniformity** | cross-view **consistency** — one vocabulary, one treatment per meaning | **no charter in the roster** | **underivable from any current input** |

**Plainly, for SR-053:** three independent derivations — needs-only (A), frame-only (B), hat-aware (C) — have now failed to produce it. The blind teams did not miss it; **no declared input of this repository demands cross-view coherence.** SR-053 carries 8 LLRs and 8 TCs. Either a need or a hat charter is missing (C's R-4), or the row is genuine accretion. It is the one §2.2 row the exercise can now call *underivable* rather than merely underived.

Net on legibility: the roster's answer to "is it readable" today is **"it doesn't overflow."** Everything past that sits behind a tag nobody sets.

### 4.2 §2.2 orphans that gain a deriving hat

14 of 16 gain a named lens, so the derived-requirement label becomes available for them. **4 gain it only through a switched-OFF hat** — a roster finding, not a licence.

| SR | Deriving hat | Row |
|---|---|---|
| SR-015 perf back-links · SR-033 release checklist | PERFORMANCE **(OFF)** | C-PRF-2 |
| SR-024 permutation cases · SR-129 carrier migration · SR-147 one carrier | TEST-ENGINEER | C-TST-1 (a check must be shown to bite; round-trip proof) |
| SR-040† resume-surface tripwire | UX-ENGINEER / UNATTENDED-OPS | C-UXE-2, C-UNA-8 |
| **SR-043 subagent gate** | **SECURITY** | C-SEC-2 — *enumerate the irreversible actions an unattended run can take, each naming its authorising dial.* A direct, exact hit. |
| SR-052 dashboard a11y | ACCESSIBILITY **(OFF)** | C-ACC-1/3 |
| SR-054 usability | UX-DESIGNER + UX-ENGINEER | C-UXD-1, C-UXE-2 |
| SR-111 kit-version stamp · SR-112 skill fan-out | MAINTAINER | C-MNT-7 (a generated surface names its inputs) |
| SR-144 lane terminal close | UNATTENDED-OPS | C-UNA-3/5 (bounded claim, durable record) |
| SR-146 reviewable prompts | SECURITY | C-SEC-5 (brief egress inclusion rule declared, not implicit) |
| SR-149 retired vocabulary | MAINTAINER | C-MNT-3 (one normative definition per enum value) |
| **SR-053 uniformity · SR-155 contested planning** | **none** | the two that stay lens-less as well as need-less |

**Reading:** every class-(i) orphan acquired a lens. That does not make the rows wanted — it makes them *labellable*, and a derived requirement with a named lens is reviewable, which "implementation-born" alone is not.

### 4.3 NEW items C exposed — carried by neither A/B nor the legacy layer

| Item | One line | Class |
|---|---|---|
| **R-2** gating level | Hats evaluate *work-item* tags; SN rows carry none — DATA-PROTECTION cannot read SN-009, ACCESSIBILITY cannot read SN-023, PERFORMANCE cannot read SN-027. The hat that most obviously governs a need is the one guaranteed not to see it. | **roster defect** (the largest) |
| **R-4** no coherence charter | Nothing asks "is this rendered the same way as the same thing elsewhere", across ≥3 status-bearing surfaces plus the dogfood obligation. | **roster defect** → makes SR-053 underivable |
| **R-5** integrity lens is tag-gated | Atomic writes, bounded claims and crash recovery arrive only via UNATTENDED-OPS; an *attended* session that half-writes a registry gets no lens, though the corruption is identical. | **roster defect** |
| **R-6** no product-fitness hat | All 13 charters are engineering-side; none asks "is this still the need" or "who asked for this". The roster hardens a decomposition and is blind to hardening the wrong one. | **roster defect** (explains SN-033 landing text-only) |
| **C-DPR-3** provider egress | Commit authorship — names, emails — is personal data, and repo content is briefed to external providers with no declared basis, boundary or exclusion in any need. | **needs defect** |
| **C-DPR-2** finding-record retention | The privacy *finding record* is the one artifact guaranteed to contain the personal data it reports, and nothing bounds its retention or access. | **new derived-obligation candidate** |
| **C-PRF-1** throughput budget | SN-027's whole justification is speed, it commissions the system's most complex machinery, and declares no measurement of the improvement — unfalsifiable as written. | **needs defect** |
| **C-ACC-2** colour-only signal | SN-008's "a reader can believe a green" names the system's most important signal by its **colour**; if colour is the only channel the signal does not exist for a substantial class of readers. | **new derived-obligation candidate** |

### 4.4 Revised top-10 for the sitting desk

Six entries move. `NEW` = C-only; the last column is the §3.2 rank.

| # | Finding | Was |
|---|---|---|
| 1 | The no-stub detector is built, designed, tested and stated by no requirement (`stub` 0x in 63 SRs) | 1 |
| 2 | **`NEW` R-2: the roster's gating level makes the governing lens unreachable for SN-009, SN-023 and SN-027** — it explains several §2.2 orphans at once, and is fixable | — |
| 3 | (down) **SR-053 alone** is underivable from any current input after three independent derivations (8 LLRs / 8 TCs); SR-052 and SR-054 now have named lenses | 2 |
| 4 | SN-037's two-sided-change clause: demanded by A **and** B, admitted missing by SR-162's own rationale | 3 |
| 5 | SN-012's right-sizing has 9 citing SRs and no home | 4 |
| 6 | **`NEW` C-DPR-3: repository authorship metadata crosses to external model providers with no declared basis** — a needs defect at a crossing the frame already draws | — |
| 7 | (down) SN-007's self-application bar survives only as a clause in SR-010's acceptance | 5 |
| 8 | (up) **SR-043 is not accretion** — SECURITY's C-SEC-2 derives it exactly; SN-006's safety half being `why`-only is the real defect | 7 |
| 9 | (down) SR-155 (11 LLRs / 10 TCs) is the largest structure with neither a need nor a lens behind its subject | 6 |
| 10 | (up) **`NEW` C-PRF-1: SN-027 justifies itself entirely in speed and declares no measurement** — this and the perf orphans (SR-015/033/167) share one cause: a shipped layer with no need | 8 |

Dropped from the top ten, unchanged in substance: the SN-005 two-readings finding (§3.2 #9) and the eight zero-TC matched SRs (§3.2 #10) — the latter still holds and is the cleanest good news in the exercise.
