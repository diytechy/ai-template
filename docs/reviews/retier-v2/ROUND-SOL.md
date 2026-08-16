# Re-tier v2 — external adversarial round (Sol)

**Date:** 2026-08-16 · **Round:** external adversarial, re-tier v2 (the WI-467
option-(b) application pass, provisional for the 2026-08-16 sitting)
**Model:** GPT-5.6 Sol via `codex` (cross-family per the routing policy), medium
effort, read-only sandbox — no writes, no commits
**Scope reviewed:** `docs/requirements/stakeholder-needs.toml`,
`docs/requirements/system-requirements.toml`, `docs/requirements/hats.toml`,
`project-trajectory/PROCESS.md` §3,
`project-trajectory/skills/spine-authoring/SKILL.md`
**Verdict:** CHANGES-REQUESTED · 19 MAJOR + 3 MINOR — 12 applied, 7 queued for
the sitting, 1 overruled by a standing ruling, 1 refuted in its factual core and
applied in part

---

## The verdict, verbatim

Fenced as text so it is byte-exact: the reviewer's citations are absolute
sandbox paths, which `check_docs.py` would otherwise read as broken repo links.

~~~text
## Findings

1. **MAJOR — SN-006’s new safety obligation is not covered by its acceptance criteria and conflicts with SR-043’s fail-open behavior.**  
   [stakeholder-needs.toml, SN-006](/C:/Projects/ai-template/docs/requirements/stakeholder-needs.toml:144) says: “what it may set running, and anything it does that cannot be undone, is bounded, with the override held by a human rather than by the model.” Its acceptance criteria mention only resume, typed outcomes, and preflight. Meanwhile [system-requirements.toml, SR-043](/C:/Projects/ai-template/docs/requirements/system-requirements.toml:269) requires the spawn gate to “fail open on any error,” allowing the action whose bound the need now promises. The “Hat-derived (hat.SECURITY)” label is also unsupported: SECURITY asks about secrets, credentials, and irreversible actions; starting another agent is not shown to be irreversible.  
   Rewrite SN-006 acceptance to include: “During unattended operation, configured limits bound every spawned worker and irreversible action; only an explicit human-provided override may exceed those limits; a gate error preserves the configured bound.” Then either fail closed or document a narrower, independently enforced ceiling that remains active when the hook fails.

2. **MAJOR — The pending SN re-attestation state exists only in comments, so the registry still presents amended rows as ratified core needs.**  
   [stakeholder-needs.toml, header](/C:/Projects/ai-template/docs/requirements/stakeholder-needs.toml:93) says: “PENDING RE-ATTEST … NOTHING here is signed,” followed by “an amended need cannot be flipped.” A consumer or gate reading tables sees only `kind = "core"` and cannot distinguish unchanged ratified text from amended unsigned text. This contradicts the stated goal that amendment state be mechanized rather than inferred from prose.  
   Replace the history-heavy block with a machine-readable amendment marker, for example `attestation = "pending"` and `amended = "2026-08-16"` on affected rows. Keep one short header sentence: “Rows marked `attestation = "pending"` require owner re-attestation.”

3. **MAJOR — SN-006’s amended need text is too syntactically tangled to recover its obligations reliably.**  
   [stakeholder-needs.toml, SN-006](/C:/Projects/ai-template/docs/requirements/stakeholder-needs.toml:147): “An agent can run unattended and resume from repo text alone; such a run stays safe — what it may set running, and anything it does that cannot be undone, is bounded, with the override held by a human rather than by the model — never blocks on a prompt, and fails clearly.” The subject of “never blocks” is obscured by two nested dashes, and “anything it does that cannot be undone, is bounded” does not say what kind of bound is required.  
   Rewrite: “An agent can run unattended and resume from repository state alone. The run never waits for interactive input and reports failures clearly. Declared limits bound the workers it may start and the irreversible actions it may take; only a human-provided override may relax those limits.”

4. **MAJOR — The hats silence taxonomy contradicts itself about SAFETY.**  
   [hats.toml, silence taxonomy](/C:/Projects/ai-template/docs/requirements/hats.toml:59) first says: “THREE of the five ASPECT hats (SAFETY, LEGAL, DATA-PROTECTION) are silent BY DESIGN,” then says: “SAFETY is silent BY DOMAIN, a third kind neither of those names.” SAFETY cannot simultaneously exemplify the first category and a third category “neither” of the earlier categories.  
   Rewrite the taxonomy as three explicit cases:

   - “LEGAL and DATA-PROTECTION are silent by configured opt-in.”
   - “FIRST-RUN-ADOPTER was silent because of a defective predicate; that defect is fixed.”
   - “SAFETY is reachable by predicate but currently unused because this repo has no distinct safety-domain need.”

5. **MAJOR — The always-on PERFORMANCE charter presupposes a budget for every decomposition, conflicting with right-sizing and opt-in performance.**  
   [hats.toml, hat.PERFORMANCE](/C:/Projects/ai-template/docs/requirements/hats.toml:177) asks: “What is the declared budget here, measured on what, and what happens when it is exceeded?” Applied `always`, this assumes every subject needs a budget. That conflicts with SN-012’s opt-in performance layer and PROCESS §3’s warning against over-aggressive traceability.  
   Rewrite: “Does this need a measurable performance or size bound? If yes, what is the budget, how is it measured, and what happens when it is exceeded?” The failure class should begin: “A material speed or size risk left unassessed, or a declared budget…”

6. **MAJOR — CONSISTENCY is explicitly a charter minted after the fact to justify SR-053.**  
   [hats.toml, hat.CONSISTENCY](/C:/Projects/ai-template/docs/requirements/hats.toml:186) says the charter was added because three derivations “failed to produce SR-053’s cross-view uniformity obligation.” [system-requirements.toml, SR-053](/C:/Projects/ai-template/docs/requirements/system-requirements.toml:326) then labels itself “Hat-derived (hat.CONSISTENCY)” while conceding “the charter did not exist when this row was written.” That is the circular derivation the review charter explicitly forbids: an existing row supplied the charter that is then cited as its authority.  
   Do not label SR-053 derived from this charter until the charter is independently ratified against stakeholder needs and then used in a fresh derivation. Until then, classify SR-053 as an underivable legacy row awaiting disposition.

7. **MAJOR — SR-015’s PERFORMANCE label claims support the charter does not provide.**  
   [system-requirements.toml, SR-015](/C:/Projects/ai-template/docs/requirements/system-requirements.toml:61) says: “Hat-derived (hat.PERFORMANCE): a declared budget whose back-link does not resolve … is the charter’s own failure class.” The actual charter concerns an undeclared budget or one without measurement; it says nothing about trace-reference resolution. SN-002 already supplies the real basis.  
   Remove the hat-derived label. Plain rationale: “Derived from SN-002: a budget row that cannot be traced to a requirement, design item, or module cannot demonstrate what it constrains.”

8. **MAJOR — SR-033’s PERFORMANCE label likewise exceeds the charter.**  
   [system-requirements.toml, SR-033](/C:/Projects/ai-template/docs/requirements/system-requirements.toml:206) claims the charter requires warn-tier budgets to appear in a release checklist. The charter asks what happens when a budget is exceeded; it does not prescribe a checklist or human tick-off.  
   Either derive the requirement from an explicit stakeholder need for review visibility or move checklist placement to an LLR. Plain SR wording could be: “The release review shall surface every warn-only performance-budget breach to the reviewer.”

9. **MAJOR — SR-024 confuses input coverage with demonstrating that an enforcer fails when it should.**  
   [system-requirements.toml, SR-024](/C:/Projects/ai-template/docs/requirements/system-requirements.toml:134) says generated cases are “how a check is shown to bite” and that the TEST-ENGINEER question is “unanswerable for a hand-listed case set.” Generation increases systematic coverage, but it does not prove that the tested enforcer fails; mutation or planted-failure tests do that. A hand-listed negative case can demonstrate failure.  
   Rewrite the rationale: “Hat-derived (hat.TEST-ENGINEER): systematic expansion reduces the risk that dimensional combinations are omitted. Separate negative tests must demonstrate that the resulting checks fail on violations.”

10. **MAJOR — SR-111 and SR-112 cite MAINTAINER obligations absent from the roster charter.**  
    [SR-111](/C:/Projects/ai-template/docs/requirements/system-requirements.toml:365) claims “C-MNT-7 requires a generated artifact to name what it was generated FROM”; [SR-112](/C:/Projects/ai-template/docs/requirements/system-requirements.toml:377) claims the same lens requires generated copies to declare themselves generated. But [hat.MAINTAINER](/C:/Projects/ai-template/docs/requirements/hats.toml:113) asks only why something exists and what deletion would break. The named C-MNT rules are not in the reviewed roster surface.  
    Either add those questions to the charter before citing them or remove the labels. For SR-111: “The stamp lets a maintainer identify the upstream version used for a scaffold and compute a re-sync diff.” For SR-112: “Generated marking prevents maintainers from editing disposable copies.”

11. **MAJOR — SR-040 contains three independently failing obligations in one row.**  
    [system-requirements.toml, SR-040](/C:/Projects/ai-template/docs/requirements/system-requirements.toml:256) requires per-phase command routing, displaying a reviewer dial, and warning on resume-surface size. Its rationale admits “only the resume-surface tripwire clause is orphaned.” Routing can work while the banner is absent; both can work while size warnings fail. This violates PROCESS §3’s “one decision per row.”  
    Split into:

    - “The coordinator shall select each session command from the declared per-phase mapping, using the declared default when no phase-specific mapping exists.”
    - “The coordinator shall report the configured review policy at run start.”
    - “The coordinator shall warn when a resume input exceeds its declared size threshold.”

12. **MAJOR — SR-026’s acceptance criteria introduce obligations absent from the requirement.**  
    [system-requirements.toml, SR-026](/C:/Projects/ai-template/docs/requirements/system-requirements.toml:150) requires prompt-free resumption and distinct worker/integrator state sources. Its acceptance adds: “a model rate limit backs off rather than failing the run, and a stall aborts to protect the budget.” Neither behavior appears in the requirement. Acceptance criteria cannot silently mint requirements.  
    Remove those clauses or mint separate requirements: “The coordinator shall retry declared transient model limits under a bounded backoff policy” and “The coordinator shall stop a session after the declared stall limit.”

13. **MAJOR — SR-028 does not test its leading obligation.**  
    [system-requirements.toml, SR-028](/C:/Projects/ai-template/docs/requirements/system-requirements.toml:174) requires the coordinator to “end each session in a typed outcome code,” but acceptance checks only an empty repository, ERROR logging, and all-ERROR classification. A coordinator could return arbitrary untyped codes and still meet the listed acceptance.  
    Add: “Every declared end state returns its assigned outcome code; an unrecognized end state fails rather than returning a success code.”

14. **MAJOR — SR-046 is a menu specification containing multiple actions and concrete design syntax, not one capability-level decision.**  
    [system-requirements.toml, SR-046](/C:/Projects/ai-template/docs/requirements/system-requirements.toml:281) separately specifies an interactive menu, direct named launch, machine listing, empty-declaration behavior, exit-code passthrough, `name = command`, `name.desc`, and Windows/POSIX support. These fail independently and exceed PROCESS §3’s “at most one method/action.”  
    Capability-level rewrite: “The repository-root launchers shall expose every declared runnable capability consistently to interactive users, direct command callers, and automated discovery.” Put menu numbering, listing format, declaration grammar, fallback text, and exit handling into separate LLRs.

15. **MAJOR — SR-129 remains implementation- and history-shaped at the requirement tier.**  
    [system-requirements.toml, SR-129](/C:/Projects/ai-template/docs/requirements/system-requirements.toml:414) names “the spec folder (status = directory, TOML frontmatter, Deliverable in the body)” and “the retired flat CSV form,” then prescribes non-empty-target and drained-stop mechanics. This violates capability voice and requires repository history to understand. No artifact-altitude waiver is recorded.  
    Rewrite: “The kit shall convert the work-item registry between its current and legacy representations without losing or changing any cell, and shall refuse conversion while either representation is in use.” Put directory layout, frontmatter fields, target emptiness, and claim detection in LLRs.

16. **MAJOR — SR-147 puts migration history and concrete carrier designs in normative text without a relevant waiver.**  
    [system-requirements.toml, SR-147](/C:/Projects/ai-template/docs/requirements/system-requirements.toml:518) says: “rather than two (stakeholder needs as markdown prose tables, the other three tiers as CSV, as they were until the 2026-08-10 cutover)” and requires a converter “BEFORE the authority flip.” The recorded 13v waiver covers the one-`shall` issue, not PROCESS §3’s ban on normative history or concrete artifact identity.  
    Rewrite: “The kit shall store every spine tier in one machine-parseable representation, with a verified migration that preserves every cell before the new representation becomes authoritative.”

17. **MAJOR — SR-148’s fan-out re-stamp does not cure a many-obligation requirement.**  
    [system-requirements.toml, SR-148](/C:/Projects/ai-template/docs/requirements/system-requirements.toml:531) combines work-source authority, pointer-file abolition, a four-class priority order, deterministic selection, per-item fail-closed policy checks, human ratification holds, and generated-status freshness. The rationale calls all this “one decision,” but each clause can fail while the others pass. The acceptance paragraph confirms distinct observables and migration behavior.  
    Split at least into selection source, selection ordering, invalid-input exclusion, human-held stops, retired-pointer migration, and generated-status authority. A re-stamp is appropriate for many children of one observable, not for several separately observable policies.

18. **MAJOR — SR-170’s new split still merges exclusive writing, regeneration transactionality, and identity allocation.**  
    [system-requirements.toml, SR-170](/C:/Projects/ai-template/docs/requirements/system-requirements.toml:790) requires a sole writer for three artifact classes, dependency-ordered regeneration, first-failure stopping, lane prohibition, collision avoidance, and—only in acceptance—non-reuse of deleted identities. These are not one decision merely because the “serial trunk actor” participates in each.  
    Split into:

    - “Only the serial integrator shall write shared generated records.”
    - “Shared regeneration shall run in dependency order and leave no partial result after failure.”
    - “Work-item identity allocation shall prevent duplicate or reused identities.”

    Plainer terminology should replace “shared authority surface,” “mint,” “serial integration seam,” and “composed tree.”

19. **MAJOR — SR-169 is not cold-readable and embeds an unexplained external rule in its normative cell.**  
    [system-requirements.toml, SR-169](/C:/Projects/ai-template/docs/requirements/system-requirements.toml:777) says: “seams terminating at the containing boundary … the absent-registry case being the artifact contract’s omission rule and not this row’s.” A first-time reader must already know what “seams,” “containing boundary,” and “artifact contract’s omission rule” mean. The final clause is effectively an internal cross-reference without an ID.  
    Rewrite: “The generated architecture view shall show declared components, their containment hierarchy, and the interfaces between them. When the registries exist but declare no interfaces, the view shall display an explicit ‘no interfaces declared’ state.” Put absent-registry omission under the separately identified artifact-contract requirement.

20. **MINOR — PROCESS §3 states an absolute rule and then describes a waiver to that same rule.**  
    [PROCESS.md §3](/C:/Projects/ai-template/project-trajectory/PROCESS.md:125) says: “A requirement cell never names a concrete artifact,” but lines 132–134 say the checker warns when one appears “without a recorded per-row waiver.” A first-time adopter cannot tell whether the rule is absolute or waivable.  
    Rewrite the heading rule: “An SR requirement cell must not name a concrete artifact unless its rationale records why constraining that artifact is necessary.”

21. **MINOR — The spine-authoring skill opens with unnecessarily categorical jargon.**  
    [spine-authoring/SKILL.md, “solution-freedom”](/C:/Projects/ai-template/project-trajectory/skills/spine-authoring/SKILL.md:26) says: “which artifact carries a capability is trace data, categorically,” followed by “artifact identity = trace tier.” “Trace tier” is not one of SN/SR/LLR/TC and must be inferred from a later list.  
    Rewrite: “Keep the SR independent of filenames. Record the current implementation location in existing trace fields such as LLR `Module`, TC `Evidence`, code back-links, or a registry ID.”

22. **MINOR — The hats roster’s count and status narration is stale and history-dependent.**  
    [hats.toml, header](/C:/Projects/ai-template/docs/requirements/hats.toml:4) says the roster “grown to thirteen,” while the file contains sixteen hats; [the PRODUCT-FITNESS preface](/C:/Projects/ai-template/docs/requirements/hats.toml:212) similarly says “all thirteen prior charters.” A cold reader has to reconstruct that three provisional rows were appended later.  
    Rewrite the live header: “This roster currently contains sixteen hats: thirteen ratified hats and three pending owner review.” Keep the historical growth record in the log.

**VERDICT: CHANGES-REQUESTED — the registries contain unsupported and circular hat derivations, several multi-obligation rows that violate their own adjudication rule, and an amended safety need whose acceptance and fail-open implementation do not preserve the promised bound.**
~~~

---

## Disposition

Owner-dispositioned; applied 2026-08-16 by the application pass. Findings are
claims — each APPLIED row below was checked against the file before the edit.

| # | Subject | Disposition | What happened |
|---|---|---|---|
| F1 | SN-006 bound vs SR-043 fail-open | **APPLIED (in part)** | SN-006 `acceptance` gains Sol's clause verbatim, with a qualifier naming the last sentence as the sitting's OPEN QUESTION rather than a met bar (the delivered gate fails open, so claiming the bound holds through a gate error would be the false green SN-008 forbids). SR-043's rationale now records the fail-open-vs-bounded tension and its two candidate resolutions. **Behavior unchanged** — fail-closed vs a narrower always-enforced ceiling is an owner ruling, not an application-pass edit. Sol's secondary claim that the `hat.SECURITY` label is unsupported was **not applied**: C-SEC-2 asks that the irreversible actions of an unattended run be enumerated with their authorising dial, and spawning further actors is the row's subject — the label is left for the sitting to test alongside F10's class. |
| F2 | Amendment state lived only in prose | **APPLIED** | `attestation = "pending"` + `amended = "2026-08-16"` now sit on each amended row — **17 rows**, not 18: SN-001/003/005/006/009/011/012/023/025/026/027/028/029/034/035/038/039 (sixteen `tags`-only amendments plus SN-006, whose `need`/`why` also moved). The header's PENDING RE-ATTEST block drops from twelve lines of history to two sentences pointing at the marker. Verified schema-tolerant: the SN tier has no entry in `spine_carrier.SPINE_TIER_KEYS`, `needs_from_toml` passes every key through, and `trace.py --strict-integrity` is unchanged at `orphans=0 integrity=0`. |
| F3 | SN-006 need text unrecoverable | **APPLIED** | Rewritten to Sol's three-sentence structure. Obligation audit before/after: (a) unattended + resume from repository text — kept, with "repo text" spelled out rather than widened to "state"; (b) never blocks on a prompt — kept as "never waits for interactive input"; (c) fails clearly — kept; (d) bounded workers + irreversible actions with a human-held override — kept, with "never one the model can set" preserved from the original, which Sol's wording had dropped. Nothing lost. `check_need_form.py` clean. |
| F4 | Silence taxonomy self-contradiction | **APPLIED, with two of Sol's three cases corrected** | The contradiction is real and is gone; both rosters now carry three explicit, non-overlapping cases. Sol's bullet 1 is **stale**: `hats.py audit` reports LEGAL reach **1** (SN-011) and DATA-PROTECTION reach **2** (SN-006, SN-009) — the 2026-08-16 need tags woke both, so they are opt-in-by-tagging but no longer *silent*, and the live file now says so. Sol's FIRST-RUN-ADOPTER claim **verified TRUE**: its original predicate keyed on the undeclared `scope` field, WI-453 re-pointed it at deliverable tags, and it now reaches **10** needs — so nothing in the roster is silent by defect today. Sol's bullet 3 **verified TRUE**: SAFETY reach **0**, no row carries the `safety` tag; kept as silent-by-domain with the owner's disposition question intact. |
| F5 | PERFORMANCE presupposes a budget | **APPLIED** | `asks` reworded to Sol's conditional form and `listens_for` to "A material speed or size risk left unassessed, or a declared budget with no measurement behind it" — identical in the live roster and the shipped template. Each row's preface now states why an unconditional hat may carry a conditional question, which is the SN-012 right-sizing collision Sol named. |
| F6 | SR-053 / CONSISTENCY circularity | **QUEUED** | Already an open sitting call — the row itself records that the charter postdates it and that cutting the charter returns the row to *underivable*. Sol reaches the same verdict independently from a cold read, which is corroboration worth carrying into the sitting; the disposition (ratify the charter and re-derive, or classify the row as underivable legacy) is the owner's. |
| F7 | SR-015 PERFORMANCE label overclaims | **APPLIED** | Confirmed against the charter: neither the old nor the new `listens_for` mentions trace-reference resolution. The label is withdrawn, the withdrawal recorded in the row, and SN-002 stated as the basis in Sol's words. |
| F8 | SR-033 PERFORMANCE label exceeds charter | **APPLIED** | Confirmed: no charter text and no `C-PRF-*` clause prescribes a checklist or a human tick-off. The label is narrowed rather than dropped — the charter asks *what happens when a budget is exceeded*, and this row is this project's **answer** for a warn-tier budget, which the rationale now says explicitly. The requirement cell is untouched: moving checklist placement to an LLR is a structural change outside this pass. |
| F9 | SR-024 conflates coverage with biting | **APPLIED** | Confirmed. Rationale rewritten to Sol's wording: systematic expansion answers the coverage half; demonstrating an enforcer fails is a separate obligation (negative or planted-failure tests — the roster's own C-TST-6 asks for exactly that), not this row's. |
| F10 | SR-111/SR-112 cite absent MAINTAINER obligations | **REFUTED in its factual core; APPLIED in part** | **Evidence:** C-MNT-7 exists and reads *"Every generated view **shall** identify itself as generated and name the inputs it was generated from"* — `docs/plans/2026-08-16-blind-derivation-c-hats.md` §hat.MAINTAINER, line 209. Both cited halves are that clause verbatim: SR-111 cites "name what it was generated FROM", SR-112 "declare itself generated". The clauses are **derivation output from the MAINTAINER charter**, not invented after the fact, and every other `C-*` citation in the registry resolves to the same document. Sol's narrower point stands: the clauses are not in `hats.toml`, so a cold reader of the roster cannot check the citation. Applied accordingly — both labels now name where C-MNT-7 is defined, and each row carries Sol's plain sentence as a reason that stands **without** the citation (PROCESS §3: a citation is context on top of a standalone reason, never a substitute). Whether the roster file should carry the clause set is a live sitting question. |
| F11 | SR-040 three-way split | **QUEUED** | Sol is describing a structural split of a ratified row (routing / dial banner / resume-size tripwire), which mints ids and re-tiers children. That is a sitting decision, not an application-pass edit — and the row's own rationale already concedes the orphaned third clause. |
| F12 | SR-026 acceptance-minted obligations | **QUEUED** | Backoff and stall-abort genuinely appear only in acceptance. But the fix is either deleting live obligations or minting two SRs; both are sitting calls. Carried as a split/mint candidate with Sol's proposed wordings attached. |
| F13 | SR-028 leading obligation untested | **APPLIED** | Acceptance now opens with "Every declared end state returns its assigned outcome code, and an unrecognized end state fails rather than returning a success code". Verified realistic against the carrier: `agent_loop.py` already exposes a closed `EXIT_*` set (DONE / PREFLIGHT / BLOCKED / STALL / WAITING / BUDGET / NEEDS_HUMAN / PAUSED), so this states a bar the row can be held to rather than an aspiration. |
| F14 | SR-046 menu specification | **QUEUED** | The capability-level rewrite plus an LLR fan-out is a re-tier of a shipped launcher contract; the sitting rules it. |
| F15 | SR-129 implementation/history voice | **QUEUED** | Voice-depth call at the requirement tier, with a rewrite proposed. No artifact-altitude waiver is recorded on the row today, which is itself the thing to rule. |
| F16 | SR-147 history in normative text | **QUEUED** | Confirmed that the recorded 13v waiver covers the one-`shall` finding only (`trace.py` still reports SR-147 for it), not normative history or carrier identity. Whether to re-word or to widen the waiver is the sitting's. |
| F17 | SR-148 fan-out re-stamp | **OVERRULED — standing ruling** | The owner's S4 re-stamp ruling stands: splitting SR-148 would restore the 13-part merge that ruling deliberately settled. Sol's read is noted and not acted on. |
| F18 | SR-170 three-way split | **QUEUED** | A structural split of a freshly minted S4 row, one day old; the sitting that ruled the split rules its follow-on. Sol's terminology complaint ("shared authority surface", "mint", "composed tree", "serial integration seam") is carried with it. |
| F19 | SR-169 not cold-readable | **APPLIED** | Requirement and acceptance rewritten in plain words — "components" and "interfaces" for "structural units" and "seams", the containment/boundary rule spelled out — keeping **one** `shall` (verified: `trace.py` reports no form finding for this row) and keeping the empty-vs-absent scoping Sol wanted moved. The cross-reference now names **SR-070**, which is the row that actually carries the omission rule, closing Sol's "cross-reference without an ID". |
| F20 | PROCESS §3 absolute-then-waivable | **APPLIED** | The bullet's opening is now "A requirement cell names no concrete artifact unless its `Rationale` records why constraining that artifact is necessary." — the rationale-gated form, which also aligns the rule with the published-standards position the tiering memo records (INCOSE R31, ISO 29148, NASA). Bullet kept compact; the `trace.py` warn-on-missing-waiver sentence now reads as the enforcement of that same rule. `PROCESS.md` 76,133 → 76,226 bytes (+93). |
| F21 | spine-authoring jargon | **APPLIED** | "trace data, categorically" and "artifact identity = trace tier" replaced with Sol's plain form, naming the four trace homes inline. The §3 rule summary in the skill's Authority block was updated to match F20's new wording. Both per-agent copies re-synced (`bootstrap.py --dest . --sync`); `gen_skills_index.py --check-agents` reports OK, 14 copies matching source. |
| F22 | Stale roster counts | **APPLIED** | The live header now opens with the true count — sixteen hats, thirteen ratified plus three provisional pending owner review — with the growth history compressed to one parenthetical clause. The PRODUCT-FITNESS preface's "all thirteen prior charters" becomes "every other charter in this roster". The template header gets the same treatment. |

## Verification after application

- `trace.py --strict-integrity` → exit 0; `SN=27 SR=63 LLR=155 TC=150 orphans=0
  integrity=0 form-findings=2` (the two are the pre-existing SR-140 and SR-147
  one-`shall` findings — no new class, and none from the rewritten rows).
- `check_need_form.py` → clean, 27 need cells, no internal path, implementation
  identifier or process citation.
- `pytest tests/test_hats.py tests/test_trace_rules.py tests/test_dogfood_sync.py
  tests/test_bootstrap.py -q` → **157 passed, 1 skipped** (identical to the
  pre-change baseline).
- `hats.py audit` → parses; reach counts as quoted in F4.

## Not done here (stated so its absence is not read as coverage)

- The generated mirrors of the edited SR rows (`docs/okf/system-requirements/`)
  and `PROJECT_STATE.html` are now stale for SR-015/024/028/033/043/111/112/169.
  They regenerate on the trunk lane (`gen_okf.py`, `gen_trajectory.py`), which
  was outside this pass's edit scope.
- `tests/test_hats.py` `LIVE_NAMES` / `LIVE_ALWAYS` still pin the sixteen-hat
  roster including the three provisional charters; those pins remain stale-by-
  design until the sitting rules, exactly as the roster's own preface records.
