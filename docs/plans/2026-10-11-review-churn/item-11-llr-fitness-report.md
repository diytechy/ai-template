# Item 11: are the LLRs fit to be carried by interfaces?

*For the owner. Answers [`item-11-llr-interface-check-handoff.md`](item-11-llr-interface-check-handoff.md), 2026-10-12, at commit `eae8e1cbe`. Two independent analyses ran on the same brief: GPT-6 Astra (medium effort) and Claude Fable 5.1 (medium effort). Their full reports and per-LLR tables are in [`reviews/`](reviews/): [`astra-medium-item11.md`](reviews/astra-medium-item11.md), [`fable-medium-item11.md`](reviews/fable-medium-item11.md), the two `item11-classes-*.csv` tables, and the shared [`brief-item11.md`](reviews/brief-item11.md). The integrator (Claude Opus 5.5) checked each claim used below against the repository. Where a figure differs from a reviewer's, the checked figure is the one given here.*

## The answer

**Item 11 as proposed would not reduce rework. It moves the spine's links rather than removing them, and the defects that cause churn would move with them.** Both analysts reached this on their own, and the checks confirm it.

| Question | Result |
|---|---|
| LLRs in modules that own no IF | **55 of 302**, under the rule "no module in the LLR's `module` cell equals an IF `owner`" after normalizing paths. The handoff's "not reproduced" is wrong. Its 90 / 64 matches no rule. The looser rule ("at least one module owns none") gives 101. |
| Fit as written / reword first / reframe or retire | Astra **68 / 226 / 8**, Fable **83 / 215 / 4**. They agree on fitness for 254 of 302 rows. |
| Why they need rewording | Mostly test 2: the row names code symbols or narrates mechanism (Astra 223, Fable 213 of 302). **Ruling 5 already requires that rewording**, whatever item 11 decides. |
| Interface availability | About 228–255 LLRs have an existing IF by owner, but **an owned IF is not a carrying IF**: IF-011 is `gen_trajectory`'s exit code and cannot carry LLR-100's breadcrumb. 33–65 are observable only in a delivered artifact with no IF row, chiefly the dashboard (21 rows). 5–8 are kernel or internal decisions, where OI-48 applies. 2–4 have no observable seam at all. |
| Does A simplify the spine? | **No.** Holding all 302 LLRs, A needs at least 302 IF → LLR allocations plus about 206 code → IF pairs, so at least 508 authored links. Today's code-side anchors are 321 file–LLR pairs plus 206 file–IF pairs, 527 in total. The saving is about 19 links, at a coarser grain. It comes before 117–150 file component headers, the grammar rewrite, and two reversed decisions (Astra, checked arithmetic). |

**Recommendation: variant E**, "D, plus the missing boundary seams, plus fitness at touch":

- Keep code → LLR (`Implements:`) as the trace.
- Add IF → LLR only on interfaces that genuinely carry a behaviour, with the SR side derived.
- Mint the few seams the kit is missing for artifacts it actually delivers. The dashboard comes first.
- Measure LLR reachability through interfaces; don't gate on it.
- Apply the corrected fitness tests when a row is touched, not as a 302-row migration gate.

The brief named A–D and asked each analyst for "any variant of your own". Each proposed one beyond D, and called it E, the next free letter. The two differ in detail:
- **Fable's E** mints the missing seams outright and adds the reach dial.
- **Astra's E** keeps the dashboard interface only "if that allocation earns its cost" and leaves file component headers optional.

The E here combines the two. "Variant E, link by link" below lays it out against today, A and D.

**Since revision 15:** the owner refined E into **variant F**, recorded in the plan's [item 11](README.md) with a table comparing it to E. In short: components are declared on the realization (LLR → CMP retires), there is no IF → LLR list, and interfaces are thin. F also corrects E's IF → SR derivation, which must follow the assumption bridge as well as the crossing cells.

## Why E, on your two criteria

**1. Behaviour stays divorced from implementation.** The things that couple a requirement to its implementation are the symbols and mechanism inside LLR text, and the `module` and `code_symbol` cells. Item 5 removes both, whatever is decided here. After that, every remaining link points up, from code and tests to LLRs. A refactor moves `Implements:` tags, which live in code, and never reopens a requirement row. Item 11 adds nothing to this, and A weakens one part of it. With every LLR routed through an IF, the IF → LLR allocation becomes a new authored relation that changes whenever a seam is split or merged. A seam split is a refactor-shaped event, so under A a refactor *can* reopen the spine, through the IF rows.

**2. No maintenance burden without orientation benefit.** E authors a link only where it tells a reader something no other link does, and derives the rest. Each link and its reason are in the table below.

## Variant E, link by link

What each design does to each link or rule. B is A with a fitness verdict required before each LLR attaches. C is A with delivered-artifact seams in place of internal call seams. So neither gets a column. Unchanged everywhere: LLR → SR, TC → LLR, and test files naming their TC (revision 8).

| Link or rule | Today | A: item 11 as proposed | D: minimal | **E: recommended** | Why E chooses this |
|---|---|---|---|---|---|
| Code → LLR (`Implements:`) | about 900 lines, 228–230 LLR ids | **retired** | kept | **kept** | The most precise code-to-purpose path. It is checked at the commit and breaks only when an LLR retires, the signal wanted. Ruling 5 stands as written |
| Code → IF (`Contracts:` / `Contract IF-NNN`) | module header (docstring or top comment) | on the realizing *symbols*: grammar and three readers rewritten | kept | **kept, grammar unchanged** | A contract is a seam's bounds (your definition); a per-symbol grammar buys coarse reachability only |
| IF → LLR | none; reached through LLR `module`, which item 5 removes | authored on **every** IF; every LLR must appear on one | optional, unspecified | **authored only on IFs that genuinely carry the behaviour (about 100–150 cells), each reviewed for meaning** | Tells a seam's consumers what it promises and why. On every IF it is bookkeeping. Review answers OI-67's "verified by nothing" |
| IF → SR | none; `boundary_refs` and the crossing cells exist | authored, or derived (open) | none | **derived** through `boundary_refs` and the crossing cells | Already has a home; authoring would give it a second. Ruled once with OI-112 |
| "Every LLR is carried by an interface" | no such rule | **a rule**: mint `call` seams for the 55, or reframe them | no | **a measured dial**, with a closed internal allowance in the `kernel-modules-allow` idiom | A rule would mint seams OI-48 declined, or retire real decision rows (LLR-149, LLR-159, LLR-188) |
| New IF rows | none | `call` seams for internals, or none if reframed | none | **delivered dashboard first; then other delivered-artifact and CLI seams, judged one by one** (Fable lists 6–10 + 3); never a `call` seam to satisfy a rule | 21 LLRs are observable only in the dashboard, which has no interface row |
| IF owner | authored cell | generated from citations (roles open) | authored | **authored owner id, role-bearing** | The one independent check on an over-claimed citation; generating it makes that check circular (both analysts) |
| File → CMP | none (derived from LLR `module` + `component`) | **header on every file** (117–150 sites) | optional | **not adopted now**; the map stays derived | Add later if the derived map proves wrong; nothing E builds blocks it |
| LLR → CMP | authored | checked against headers, or derived (open) | authored | **authored design intent** | Deriving it from code removes the independent allocation check |
| What discharges an LLR (SR-180's replacement) | its `code_symbol` resolves (item 5 retires this) | a code-cited IF carries it and a TC verifies it | a live `Implements:` and a verifying TC | **as D: structure checked at the commit, meaning judged by the reviewer, results at the gate** | Reachability is not discharge (Astra F1) |
| Fitness of LLR text | none | none | none | **the corrected tests, applied when a row is touched**: tokens by item 5's text check, meaning by the spine-authoring rubric | A 302-row gate (B) depends on the reviewer: 7 of 15 jointly hand-read rows differ |
| Minimum profile (no IF registry) | works | needs a new rule (mandatory boundary IF, or `Implements:` survives) | works | **works unchanged** | Code reaches LLRs without an interface |
| Blast radius of a changed file | file → `Implements:` → LLR → CMP / TC | file header → CMP → IFs → carried LLRs → TCs | as today | **derived:** file → `Implements:` → LLR → CMP and TCs, plus each carrying IF's consumers | Every link it uses already exists or is reviewed |

## What E costs

- **Already owed by item 5, not item 11:** about 215–226 LLR rewordings. About a third are symbol-only, a mechanical lint fix (Fable's hand sample: about 10 of 27). The rest narrate mechanism and need a sitting's judgement.
- **New seams:** one IF for the delivered dashboard. Possibly 5–9 more for other delivered artifacts: the launchers, the prompt catalogue, the composed briefs, and the evidence and record files (Fable's list). Plus 3 unregistered CLI seams (`check_vocab`, `check_dupes_census`, `dispatch`), already owed under `trajectory_arch`'s connectivity warn. "65 boundary-artifact rows" (Astra) does not mean 65 interfaces: most share one artifact.
- **IF → LLR cells:** on the carrying interfaces only. Fable estimates 100–150. Each one is reviewed for meaning, which answers OI-67's "hand-written and verified by nothing".
- **TC repairs:** the handler-text pins that will reopen rows on a refactor, namely TC-057, TC-090 and TC-103, and the two constant-reading TCs, TC-105 and TC-108. Repair them when their LLRs are touched.
- **Reframe or retire:** LLR-050 (both: retire), and LLR-184 and LLR-197 (both: reframe). LLR-031, 032, 159, 180, 181 and 188 split the analysts. Settle each in one batch act when item 5's migration reaches it. LLR-180 retires with SR-180's replacement in any case.
- **Not spent:** retiring about 900 `Implements:` lines, the symbol-level citation grammar (`gen_arch_map`, `trajectory_arch`, the strict body gate), about 117–150 file headers, re-founding the LLR floor on reachability, and overruling OI-67 and the 2026-09-23 `realizes` rejection a second time.

## The alternatives, compared

| | One-time cost | Authored links to keep true | Orientation | Behaviour independence |
|---|---|---|---|---|
| **A: as proposed** | largest: retire `Implements:`, allocate all 302, headers, grammar rewrite, two reversals | about 508 or more, plus 117–150 headers; IF splits reopen allocations | strong at architecture entry; one citing function inherits every obligation of its IF | wording is item 5's doing; allocation churn is new |
| **B: reword, then A** | A plus a fitness verdict per row | as A | as A | better prose than A; the same allocation churn |
| **C: boundary artifacts in A** | less than A: no internal seams minted | as A, with fewer rows | best for delivered outputs | as A |
| **D: minimal** | smallest: item 5 cleanup only | about 527 today, plus optional IF → LLR | precise code → purpose; IF context only where present | meets the aim |
| **E: D + C's seams + fitness at touch (recommended)** | small: a few seams, IF → LLR on carrying IFs, a reach dial | D plus about 100–150 reviewed IF → LLR cells | D plus "what this seam promises" where one exists | meets the aim, and keeps OI-48's line |

Keep A in view if you value **one up-direction from code** (code → IF only) and **a component declared on each file** more than function-level trace and the minimum profile. E can grow into A later without discarding anything: the IF → LLR cells it authors are a subset of A's, and A's headers can be added on top of it. A, once adopted, cannot shrink back to E without restoring the retired `Implements:` tags.

## Where the analysts disagreed, and how it is judged

1. **Fitness counts (68/226/8 against 83/215/4).** They agree on 254 of 302 rows, but differ on 7 of the 15 rows both read by hand (LLR-004, 006, 021, 088, 120, 181, 190). *Judgement:* a per-row fitness verdict depends on the reviewer. A 302-row fitness gate before migration (variant B) would itself generate review rounds, which is the churn this plan exists to stop. So the mechanical part (symbol and markup tokens) goes to item 5's commit-time text check. The semantic part goes into the spine-authoring rubric, judged when a row is touched.
2. **Evidence for interactive dashboard behaviour.** Astra: a browser is appropriate for LLR-088 and LLR-100's navigation effects. Fable: parsing the delivered document *is* exercising the artifact seam, so no browser is needed. *Judgement:* they agree on the defect. A test that asserts the emitter's handler source (`trail=trail.slice(0,i+1)`) can pass while navigation is broken. The kit's suite has no browser, and adding one is a dependency-ledger decision. So: LLRs claim what the delivered document exposes, and interactive behaviour is checked by inspection (the `render-dashboard-critique` skill already screenshots it). Whether you want executable interaction evidence is an owner call (below).
3. **How many LLRs are boundary-artifact (33 against 65).** Astra ranked across all 302 rows, Fable mainly within the 55. This doesn't change the recommendation: a handful of artifact seams either way.
4. **Corrected fitness tests.** Each analyst corrected the handoff's tests 2 and 3 in the same direction. The merged wording is below.

## The fitness tests, corrected

The handoff's test 2 ("the user-observable outcome") and test 3 ("at the level the user sees it") are wrong for LLRs. The 2026-08-13 form rule ties an LLR to a *component-level* interface, whose observer is that seam's consumer, not the end user. Held to the user's view, every LLR becomes a system-boundary statement, which is an SR. That would collapse the tiers. The integrator raised this in the brief, and both analysts adopted it and refined it.

1. **Decidable from the row.** A reader holding only the row and the seam's contract can say what would fail: input domain, outcome, threshold, refusal. A vague-word lint catches few failures (10–13 of 302). Most undecidable rows are undecidable by omission (LLR-032: "runs to a green developer setup").
2. **Stated at its seam.** States what crosses the interface it attaches to, as observed by that interface's consumer. It survives a behaviour-preserving refactor and names no symbol, topology or emitter syntax. Markup and ARIA tokens are the artifact's surface, so they belong in the IF contract and the TC, not the LLR.
3. **Evidence drives that seam.** Its evidence stimulates the seam and observes what crosses it, or uses an inspection for an expressly bounded structural property. A test that pins handler source, or reads module constants instead of the produced artifact, fails.

## Found on the way (separate findings, not fixed; each checked)

- **The authoring guidance still produces the defect.** `project-trajectory/prompts/spine-questions.md:218` says "LLRs name modules and symbols by design", and `skills/spine-authoring/SKILL.md:42` points LLR identity at the `Module` cell. Until item 5 lands, every new LLR adds to the 215–226 rows that need rewording. *Recommend* moving this text change into phase 1's rubric edits: it is text only, and ruling 5 already decided it.
- **IF `data` cells name code: 114 of 243**, 103 of them on the 115 `call`-channel rows (for example IF-056, IF-083: "check_trajectory loaders: …"). Ruling 5 says IF rows name no code. The plan counted only the `owner` cells. So item 5's IF rewrite is about twice what it states. Many of these call rows are intra-kit library usage, the shape OI-48 declined. **Classify them before rewording any**, as a cross-component seam (keep and reword) or helper usage (retire). That is a large possible simplification of the spine.
- **The dashboard, the kit's main human-facing artifact, has no IF row.** `docs/open-items.html` (IF-074) and `docs/test/report.html` do.
- **147 of 243 IFs are exempt from TC coverage** (`docs/if-tc-coverage-allow`; Fable's "217" was the file's line count). Any IF → LLR list inherits that gap, another reason not to make interfaces the only route.
- **LLR-292's strict-lint failure is a false positive.** "minimal" sits in "no claim is made that crossing count is minimal". Item 6's "fix LLR-292" should teach the lint about negation, or reword the sentence without losing it, rather than treat a correct sentence as the bug.
- **TC-029 and TC-030 name `tests/test_agent_loop.py`, but the lock tests live in `tests/test_agent_loop_support.py`.** Their evidence is stale.
- **Requirement cells carrying history:** LLR-050 is wholly a retirement record, LLR-147 and LLR-157 partly, and LLR-159 states that its own census is structurally dead.
- **The plan's "module docstring only" is too narrow.** `gen_arch_map.module_contracts` also reads a `Contracts:` line in the first eight lines of top-of-file comments. Function-body citations remain outside the grammar.

## Owner calls

1. **Item 11's direction:** E (recommended), or A, B, C or D? E leaves ruling 5's "code references up to its requirements" intact, declines "every LLR carried by an interface" as a rule, and defers file component headers.
2. **Mint the delivered-dashboard interface** (artifact-class wording; the file name stays at LLR and TC per ruling 5)? And the other delivered-artifact and CLI seams, judged one by one?
3. **IF → LLR on carrying interfaces only, with the SR side derived,** ruled once with OI-112 (one direction, one home)?
4. **"LLRs reachable from a code-cited seam": a measured dial** with a closed internal allowance in the `kernel-modules-allow` idiom (recommended), or a gate?
5. **SR-180's replacement: discharge is not reachability** (Astra). Structural completeness (a live `Implements:` and a verifying TC, checked at the commit) stays separate from semantic correspondence (the reviewer) and from passing tests (the gate).
6. **Fitness at touch:** the three corrected tests go into the spine-authoring rubric and item 5's text check, and apply when a row is amended, not as a migration gate. The authoring-guidance fix moves to phase 1.
7. **Interactive dashboard evidence:** LLRs limited to what the delivered document exposes, with interaction checked by inspection, or a browser-level harness (a dependency-ledger row)?
8. **The 114 IF `data` cells naming code:** classify the `call` rows first, keeping cross-component seams and retiring helper usage, inside item 5?
9. **Recursion, (a) or (b), stays a separate decision.** This census neither needs it nor rules it out. E delivers refactor independence without it.
