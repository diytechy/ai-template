# WI-1059 plan, revision 1: a derived act's flip waits while its parent stays unaccepted

Written in the worktree `D:/ai-template-wt-wi1059`, branch `maint/wi-1059`, head `8db60ba58` (cut from trunk `refactor_again`). `planmode = "single"`: this plan settles the choices before any edit; the build waits for the coordinator's go-ahead.

Read in full: the spec `docs/work/queued/WI-1059-act-holds-returned-parent.md`; its scope critique `docs/reviews/2026-11-23-scope-critiques/WI-1059.md`; WI-1057's verdict `docs/reviews/wi-1057-adjudicate-fourth-sitting/001-ADJUDICATE-ca5a7d9.md` (LLR-406 ACCEPT, SR-251 RETURN); the rows LLR-338, SR-231, SR-232, LLR-306, LLR-310, LLR-305, LLR-357, LLR-358, SR-245, SR-246, TC-368, TC-321, TC-365, TC-396, TC-397, IF-284, IF-285, IF-296 and IF-308; runtime Flow 6. Code read: `adjudicate_act.py` whole; `coordinator_adjudicate._act_inputs`, `_act_report` and `act`; `kitlib.spine.claims_acceptance`, `PARENT_EDGES`, `_declared_rows`, `_unaccepted_parents`, `parent_first_findings` and `parent_first_line`; `acceptance_record._tree_tiers`, `PARENT_FIRST_CSVS`, `parent_first_lines`, `staged_parent_first_lines`, `commit_parent_first_lines` and `rows_at`; `adjudicate_brief.governing_templates` and `_add_act_template`; the act template and its catalogue row. Tests read: `tests/test_adjudicate_act.py`, `tests/test_coordinator_act.py`, the `owed_acts` case in `tests/test_held_status_git.py`, `tests/test_smoke_budget.py`. The coordinator-cycle skill's act-turn recipe (`references/recipes.md`) and `RESYNC_PACK.md`'s entry convention.

**The live case, reproduced on this head.** `owed_acts` over WI-1057's verdict returns `{'first-acceptance': {'accepts': {'docs/requirements/low-level-requirements.toml': ['LLR-406']}}}` and `left_owed` returns `flip LLR-406 (docs/requirements/low-level-requirements.toml)`. After this item, the same call refuses (section 2), and `left_owed` reports the flip marked as waiting on SR-251.

## Rules this plan holds every row to

- **No code name in row text.** LLR-338's amendment, TC-368's amendment and Flow 6's lines name no file, module, function, symbol, flag or test. LLR-338's accepted text carries none today (I read every cell: its terms are "act assembler", "later-act derivation", "bless mark", "held-rung act policy" and the ruling words), so nothing inherited is left in it. TC-368's accepted text carries none either.
- **One obligation per row, every clause tested.** No SR is written. Every clause LLR-338 gains is driven by a test TC-368 names (section 5 maps them).
- **A child stays inside its parent.** Section 4 checks LLR-338's amendment against SR-231 (and SR-232, its other parent), and TC-368's against the rows it verifies.
- `Accepted` rows change text only; no status moves; no snapshot.

## A vocabulary call: "waits", not "held"

The spec says a flip is "held". The kit already uses "held" for the held rung, in the very texts this item edits: LLR-338 says "held MEANING", "held APPROVE" and "on a held rung"; the act template's notes say "a held APPROVE row"; `adjudicate_act` carries a `held` flag on every authorized row meaning the rung. A flip "held" under a returned parent would read as a flip on a held rung. So everything this item writes into a row, a brief, a refusal or a report calls the flip **waiting**, and says what it **waits on**. The spec's "held" maps one-to-one onto it; the Deliverable states the mapping. If the coordinator prefers the spec's word, the change is mechanical.

## Ids

None minted. The hold is an amendment of LLR-338 (the spec settles that), and its tests extend TC-368, the case that already verifies LLR-338 (the brief's preference). LLR-409 to LLR-411 and TC-513 to TC-518 stay unminted, so no `--bump-ids` run is owed.

## 1. Where the wait is computed, which edges, which predicate, and why it terminates

**One place: `adjudicate_act._derive`**, the step both `owed_acts` and `left_owed` already call, and through `owed_acts` also `act_values` and `compose_act`. It returns the owed list it returns today (a waiting flip stays in it: it is owed) plus a map `{waiting row: [(parent, parent status)]}`. The brief, the all-waiting refusal and the later-act report read that one map, so they cannot disagree. The coordinator's entry point needs no code change: `_act_inputs` refuses with whatever `compose_act` refuses, and `_act_report` prints `left_owed`'s answer verbatim.

**The edges are the parent-first rule's own, all of them:** an SR's stakeholder needs (`SN-Refs`), an LLR's SRs (`SR-Refs`), and a TC's verified SRs and LLRs (`Verifies`), with the rule's exclusions (an IF, B or DA id, an undeclared id, a `-000` row). They are not restated anywhere new.

**The predicate is the rule's one whole-spine function, `kitlib.spine.parent_first_findings`**, the function the commit hook's parent-first step and the standing integrity finding both call (LLR-357, LLR-358). It in turn reads acceptance through `claims_acceptance`, the shared pair the derivation already uses. No second edge walk is written.

**The tiers come from the hook's own reader.** `acceptance_record._tree_tiers(root, prefix)` reads the four spine tiers at one tree from the first listed carrier of each and reports a carrier that cannot be read or does not parse. I make it public under the name `parent_first_tiers` (a rename: its definition, its two call sites and one comment, all in its own module; no SLOC growth in a 972-SLOC module) and add it to IF-308's contract. The derivation then judges exactly the rows the hook will judge, through the same carriers. A registry among them that fails to read refuses the whole derivation, naming it: this is what makes the spec's Trust sentence ("an unreadable or unparseable registry already refuses the whole derivation") true for the parent tiers, which the derivation's row reader (`rows_at`) would otherwise skip silently. The read happens only when a first-acceptance flip is owed; an amendment-only act reads nothing new.

*Rejected: calling the private `_tree_tiers` from `adjudicate_act`.* The repository has precedent for it (`held_status` calls `acceptance_record._tier_carriers`), and it would spare the 27 test modules importing `acceptance_record` a run. A second reader of a function is the moment to make it public, so I take the run.

**The computation is a fixpoint.** Let `flips` be the owed first-acceptance rows, and `after(T)` the tiers at the revision with each row of `T` set to `Accepted`.

```
taken = set(flips)
loop:
    late = {child of each finding of parent_first_findings(after(taken))} ∩ taken
    if late is empty: stop
    taken = taken − late
waiting = flips − taken, in verdict order
for each waiting row r:
    parents(r) = [(parent, status) for each finding of parent_first_findings(after(taken ∪ {r})) whose child is r]
```

- **The chain falls out.** A test case whose design row is late in one pass sees that row back at `Drafted` in the next, and is late then. A finding about a row already accepted at the revision (a standing case) is ignored: only flips are in `taken`.
- **It terminates.** Each pass either finds no late flip and stops, or removes at least one row from the finite `taken`: at most `len(flips) + 1` passes. Since every parent edge points to an earlier tier (SN, SR, LLR, TC), each removing pass settles one more tier of the chain, so in practice at most four passes and a final empty one.
- **It is the right answer, not merely an answer.** `taken` is the largest set of flips whose every parent is accepted at the revision or in the set: starting from all flips and removing only what the predicate condemns gives the greatest fixpoint. So the act lists every flip it can, and its flips, taken together, leave the hook's predicate with no finding on a moved row.
- **Each waiting row names every parent it waits on.** The naming pass asks the predicate once per waiting row, with only that row and the takeable flips applied, so a waiting parent is named alongside a parent that was never in the act (a test case verifying a returned SR and a waiting LLR names both). Naming from the pass that removed the row would miss a parent removed in the same pass.

*Why not an ordered pass, SN to TC?* With tier-ordered edges it computes the same set in one sweep, but it must look up each row's parents itself: `PARENT_EDGES` and `_unaccepted_parents` restated outside `kitlib/spine.py`, or a new per-row entry point there. The fixpoint asks only the function the hook asks, and costs a few whole-spine calls over a few hundred rows each.

The hold lives in two small helpers beside `_derive` (the fixpoint, and the tiers read with its refusal), so no function nears the complexity ratchet's limit of 10.

## 2. What the brief shows, and the exact refusal

**Where it sits.** Inside part 2, the `{acceptance_act}` slot, after the listed flips' command. No new slot, so an operator override of `ADJUDICATE-ACT` keeps filling and gets the block too. The flip line keeps its form (`Flip ... for exactly these rows: ...`), and `{registries}` and `{accepts_rows}` cover the listed flips only.

**Some flips wait.** Part 2 reads (for this item's fixture):

```
Flip `Status` from `Drafted` to `Accepted` for exactly these rows: LLR-002 (docs/requirements/low-level-requirements.toml).
Then run, and commit the flips and the copy together, ending the commit with `WI: WI-301`:

    python project-trajectory/scripts/intake.py snapshot --accepts "docs/requirements/low-level-requirements.toml=WI-301"

Not in this act: each row below is owed a flip under this verdict, but a parent it cites is not accepted and this act does not accept it, so the parent-first rule would refuse the flip. Leave its `Status` at `Drafted` and leave it out of the command; a later act lists it once each parent it waits on is accepted.

    - LLR-003 (docs/requirements/low-level-requirements.toml) waiting on SR-002 (Drafted)
```

One renderer writes each waiting line, `<row> (<registry>) waiting on <parent> (<status>)[, <parent> (<status>)]`, a missing status reading `no status` as `parent_first_line` reads it. The brief, the refusal and the report all use it.

**Every owed flip waits, but an amendment act is owed.** Part 1 is the amendment act as today; part 2 is `No flip can be taken in this act.` followed by the same `Not in this act` block. `{registries}` and `{accepts_rows}` read `none owed`, as for an amendment-only act today.

**Every owed act is a waiting flip.** `owed_acts`, and so `compose_act`, refuse with exactly:

```
the verdict <rel> owes no act that can be taken at <rev>: every flip it still owes waits on a parent that is not accepted, and a later act lists each once its parent is accepted: <line>[; <line>]
```

For WI-1057's verdict at this head, that is `the verdict docs/reviews/wi-1057-adjudicate-fourth-sitting/001-ADJUDICATE-ca5a7d9.md owes no act that can be taken at HEAD: every flip it still owes waits on a parent that is not accepted, and a later act lists each once its parent is accepted: LLR-406 (docs/requirements/low-level-requirements.toml) waiting on SR-251 (Drafted)`. The act turn prints it as `act: refused: ...` and exits 2, before launch. The existing refusals keep their order ahead of it: an acceptance with no acceptance record, then a verdict owing no act at all.

**The template.** The shipped text needs no new instruction: the rendered block carries its own. Its dispatcher notes gain the waiting case beside the list of rows "never listed", and the `{acceptance_act}` slot's description gains the block. That edit moves the template's catalogue digest (regenerated), and, through `_add_act_template` (LLR-305), the governing identity of a retained adjudicator holding an actable class: such a session drains at its next clear point, once. The `RESYNC_PACK.md` entry says so.

## 3. The later-act derivation and the act report

**`owed_acts`' shape (IF-296).** The first-acceptance part becomes `{"accepts": {registry: [ids]}, "waiting": {id: [(parent, status)]}}`: `accepts` holds the listed flips only and is empty only beside an amendment part; `waiting` is present only when a flip waits, as `retires` is present only when a retirement is owed. Every existing equality assertion over `owed_acts` stays true: I found no existing fixture with a waiting flip (each one that accepts TC-002 accepts LLR-002 beside it, or points TC-002 at the accepted LLR-001).

**`left_owed`.** A waiting flip stays in its answer, so it never returns None while one is left: `re-accept ...; flip LLR-002 (registry); flip LLR-003 (registry) waiting on SR-002 (Drafted)`. Listed flips keep today's grouped form; each waiting flip gets its own `flip <line>` entry. `left_owed` reads `_derive` directly, not `owed_acts`, so the all-waiting case is reported as owed and marked there, never as the refusal.

**What the coordinator's act report prints.** Unchanged code; the line it already prints carries the marking:

```
act: exit 0 (...)
act: owed after the call: flip LLR-003 (docs/requirements/low-level-requirements.toml) waiting on SR-002 (Drafted)
```

and the act turn exits 1, not complete. Once the parent's own act lands, a re-run of `act` on the same verdict lists LLR-003 and can complete.

**LLR-306 needs no amendment.** Its act-turn clauses are "It refuses before launch for a lane, route, uncommitted lane change, or act-derivation refusal, naming the relevant input" and "it succeeds only after a successful call leaves no authorized act owed and no changed verdict record, otherwise fails". The all-waiting refusal is an act-derivation refusal, and a waiting flip is an authorized act still owed, so the act turn fails while one is left. LLR-306 states no wording for the owed-after line; that wording is the later-act derivation's, which LLR-338 states. IF-285 (Drafted, "act also reports owed-after, verdict-record writes or complete") is unchanged for the same reason.

## 4. The rows

### LLR-338 (Accepted), `detail` only

Two changes; every other sentence stays byte-exact.

**Added**, after "...any unrecognized state or unmatched tier refuses the whole derivation naming the row.":

> An owed first-acceptance flip waits when a parent the parent-first rule reads for it would not claim acceptance after the act, being neither accepted at the revision nor flipped by the act; a flip under a waiting parent therefore waits too. The parent-first rule's own findings decide this, over the registries that rule reads at the revision, and a registry among them that cannot be read or does not parse refuses the whole derivation naming it. A waiting flip stays owed: the brief does not list it for flipping and names it with each parent it waits on and that parent's status, and once each such parent claims acceptance the same verdict's act lists it. A verdict whose every remaining act is a waiting flip refuses the whole derivation, naming each waiting row and its parents.

**Changed**, from "At a revision, the later-act derivation reports the acts a verdict still owes or its refusal, and reports no outstanding act only when every authorized act is taken." to:

> At a revision, the later-act derivation reports the acts a verdict still owes, marking each waiting flip with each parent it waits on, or its refusal, and reports no outstanding act only when every authorized act is taken.

"Flipped by the act" excludes a waiting flip by definition, which is what makes the chain a consequence rather than a second rule. The edges are not restated: the parent-first rule (LLR-357) is their one home.

**Inside SR-231.** SR-231's completion contract is "succeeds only when its call succeeds, every authorized act is taken, and verdict records remain unchanged": a waiting flip stays owed, the later-act derivation keeps reporting it, so a turn that leaves one fails, as the spec's ruling requires; SR-231 is not amended. Its pre-launch list ("an unrecorded verdict, one owing no act, a verdict that judged a row in an unexplained state, or uncommitted lane changes") is what the act turn must refuse, not all it may: LLR-338 already refuses an acceptance with no acceptance record, which SR-231 does not list. The all-waiting refusal is the "owing no act" case for an act nothing can take yet, and the hold only narrows what is taken, inside "takes only an act an accepted current verdict authorizes". SR-232 (combined sittings) is untouched: the hold changes no part's scope or grammar. **For the coordinator to confirm.**

**No other accepted row states the listing.** I searched the SR, LLR, TC, IF, DA and need registries for text on the act, the act brief, owed or authorized acts. LLR-338 is the only row stating what the derived act lists. SR-231 is unchanged (above). LLR-306 is unchanged (section 3). LLR-310 states which verdict backs a merge act; LLR-305 the act brief's retained identity; LLR-359 the held CLARITY identity; none states the listing. TC-321's text ("succeeds only when the delivered call has taken every authorized act") still holds. TC-368 is amended (below), because its method and expected must state the new scenarios.

### TC-368 (Accepted), `method` and `expected`, each gaining one passage

> **method**, appended: Derive acts from verdicts that accept a design row whose system requirement they return, that accept both, that accept a test case verifying both a waiting design row and an unaccepted system requirement, and whose only remaining act is a waiting flip; take each listed act and run the parent-first commit judgement over it; derive the later act after an act turn that leaves a waiting flip and again once the parent is accepted; derive one over a parent registry that does not parse; and assert that the waiting decision is read from the parent-first rule's findings.

> **expected**, appended: A first-acceptance flip whose parent the act leaves unaccepted waits: the brief names it with each parent it waits on and that parent's status and does not list it, and the listed flips, once taken, pass the parent-first commit judgement; a parent the act accepts lets its child be listed, and a flip under a waiting parent waits too. A verdict whose every remaining act waits is refused, naming each waiting row and its parents; the later-act derivation reports a waiting flip as owed and marked with its parents, and an act turn that leaves one does not read complete; once the parent is accepted the same verdict's act lists the flip. A parent registry that does not parse refuses the derivation naming it.

TC-368 verifies SR-231, SR-232, LLR-338, LLR-310 and IF-296; the act-turn clause is SR-231's completion contract, so it claims nothing its rows do not state. `verifies` is unchanged, so no routed traced change. Its `evidence` grows by the new tests (a traced cell, regenerated from the tests' declarations).

### Drafted interface rows, rewritten (owed first acceptance, as they already are)

- **IF-296** `data`: gains `waiting first-acceptance flips; all-waiting refusal`. The module docstring's Contract IF-296 states the new `waiting` key, the all-waiting refusal, `left_owed`'s marking and the parent-registry refusal.
- **IF-308** `data`: gains `parent_first_tiers(root, prefix) returns the tiers that judgement reads and the registries that failed`. CMP-008 is already among its requestors, and `adjudicate_act` already imports `acceptance_record` and `kitlib.spine`, so no import edge is added.

### Runtime Flow 6

- **Prose**, one sentence added after "...derives only the remaining authorized work from that committed verdict.": "A first-acceptance flip whose parent would still not be accepted after the act waits: the act brief names it with that parent instead of listing it, and it stays owed, so an act turn that leaves it does not read complete; a later act takes it once the parent is accepted."
- **The refusal branch** becomes `alt verdict is unrecorded, owes no act, owes only flips waiting on an unaccepted parent (LLR-338), has an unexplained row state, or binds a held CLARITY row to other text than its committed accepted text (LLR-359)`.
- **The act line** becomes `Agent->>Records: take amendment act, then first-acceptance act; a waiting flip is named, never flipped`, and the last `else` reads `work remains (a waiting flip included) or verdict records changed`.

### Kit text outside the rows

- **The coordinator-cycle recipe** (`project-trajectory/skills/coordinator-cycle/references/recipes.md`, and its dogfooded copy under `.claude/skills/`): exit 1's "an act is still owed (printed)" gains "a waiting flip marked with its parent"; exit 2's list gains "one whose every remaining act waits on an unaccepted parent (named)"; and the "Accept a parent with its children" bullet says the act now names a child whose parent stays Drafted as waiting instead of listing it, and that the verdict's act is re-run once the parent's own act lands. The spec does not name the recipe; I include it because it states today's behaviour (the hook refusing the act) and the skill is the coordinator's one procedure home. **For the coordinator to confirm.**
- **`RESYNC_PACK.md`**: one entry, "A derived act names a first-acceptance flip whose parent stays unaccepted as waiting, instead of listing it", anchored at the commit before the build; kit-owned files to overwrite (`scripts/adjudicate_act.py`, `scripts/acceptance_record.py`, `prompts/adjudicate-act.template.md`, `prompts/CATALOG.md`); an override of `ADJUDICATE-ACT` needs no change; a retained adjudicator drains once.

## 5. The tests

All in-process except T9. Each is red on this head unless marked; a test green on this head is shown to bite by the named mutation once the code exists. The fixture adds a Drafted SR-002, a Drafted LLR-003 citing it, and (T3) a Drafted TC-003 verifying SR-002 and LLR-003, to the existing CSV spine (SR-001, LLR-001, TC-001 accepted; LLR-002 drafted under SR-001).

`tests/test_adjudicate_act.py`, each `Implements: TC-368` (smoke tier):

| # | Test | Shows | Red first? |
|---|---|---|---|
| T1 | a flip under a returned parent waits, and the listed flips pass the parent-first check | ACCEPT LLR-002 and LLR-003, RETURN SR-002: `accepts` lists LLR-002 only, `waiting` names LLR-003 on SR-002 (Drafted); the brief's flip line omits LLR-003 and its block names it; taking the listed act leaves `commit_parent_first_lines(HEAD)` empty | red: LLR-003 is listed today |
| T2 | a parent accepted in the same act lets its child be listed | ACCEPT SR-002 and LLR-003: both listed, nothing waits; the taken act passes the parent-first check | green on head; bites when the fixpoint reads parents at their committed status only |
| T3 | a test case waits on a waiting design row and names every parent | ACCEPT LLR-002, LLR-003 and TC-003, RETURN SR-002: LLR-002 listed; LLR-003 waits on SR-002; TC-003 waits on SR-002 and LLR-003, both named | red |
| T4 | a verdict whose only remaining act waits is refused, naming each row and parent | ACCEPT LLR-003, RETURN SR-002 (WI-1057's shape): `owed_acts` and `compose_act` refuse with section 2's reason, naming LLR-003 and SR-002 (Drafted) | red |
| T5 | the later-act derivation reports a waiting flip as owed and marked, never as taken | T1's verdict after the listed act is taken: `left_owed` is `flip LLR-003 (...) waiting on SR-002 (Drafted)`, not None | red: today it reads `flip LLR-003 (...)` unmarked |
| T6 | once its parent is accepted, the same verdict's act lists the waiting flip | T4's verdict: refused while SR-002 is Drafted; SR-002 flipped and recorded; the same verdict's act lists LLR-003 | red on its first half; its second half bites a hold that reads the verdict's RETURN instead of the parent's status |
| T7 | a parent registry that does not parse refuses the derivation, naming it | T1's verdict with an unparseable SR registry carrier listed first at HEAD: refused, naming that carrier | red |
| T8 | the wait is read from the parent-first rule's one predicate | the act module calls `parent_first_findings` and the public tier reader, and states no edge table of its own | red: no call today |

`tests/test_coordinator_act.py`, `Implements: TC-368` (full tier, a `SLOW_MODULES` module; TC-368 keeps its smoke evidence):

| # | Test | Shows | Red first? |
|---|---|---|---|
| T9 | an act turn that leaves a waiting flip owes it and does not read complete | T1's verdict in a lane; the stub takes the listed act; exit 1 and `act: owed after the call: flip LLR-003 (...) waiting on SR-002 (Drafted)` | red: today the stub flips both and the turn exits 0 |

T9 tags TC-368, not TC-321: the clause it drives is LLR-338's marking and SR-231's completion, both TC-368's, and TC-321's accepted method names test functions, which an edit would owe a scrub of.

Clause to test, LLR-338's added text: waits when a parent stays unaccepted (T1, T4); not when the act flips the parent (T2) or the parent is already accepted (the existing LLR-002 cases); the chain (T3); the rule's own findings decide (T8); the failing registry (T7); not listed, named with each parent and status (T1, T3); listed once the parent is accepted (T6); the all-waiting refusal (T4); the later-act marking (T5, T9).

Unchanged and run: every other case in both modules, `tests/test_held_status_git.py`, and `tests/test_parent_first.py` and `tests/test_parent_first_git.py` (the renamed reader's own tests). The smoke tier collects 3752 tests against `max-tests = 3890`; T1 to T8 add 8.

## Architectural delta

DELTA: within

- **States.** An owed first-acceptance flip gains a state: waiting (owed, not takeable), beside owed, taken and retirement. Flow 6's refusal branch gains the all-waiting case.
- **Value domains.** IF-296's acts mapping gains the `waiting` key; `left_owed`'s answer gains the marking; the derivation's refusals gain the all-waiting reason and the failing parent registry.
- **Output on input.** The derived act now depends on the committed statuses of the rows its flips cite as parents, read through the parent-first tiers at the revision.

| Output | Inputs today | Added |
|---|---|---|
| listed flips (`accepts`) | verdict, binding, dial, judged rows and their copies at the revision | parent rows' statuses at the revision, the act's own flips |
| `waiting` | none | the same |
| refusal | verdict, binding, dial, judged rows, acceptance record | every flip waiting; a parent-first registry failing to read |
| `left_owed` | as `accepts` | the marking |

- **Boundaries.** None crossed anew: CMP-008 already calls CMP-006 through IF-308 and already imports both modules. IF-308's surface gains the public tier reader; IF-296's data gains the waiting part.

## Build

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Tests first: T1 to T9 written and run on this head; T1, T3, T4, T5, T6 (first half), T7, T8 and T9 shown failing, T2 recorded green for its mutation proof | D2; D3; D4; SR-231; TC-368 | IF-296; IF-308 | |
| P2 | The tier reader made public; the wait computed in `_derive`; `owed_acts`, `left_owed` and the part-2 rendering; the all-waiting and failing-registry refusals; docstrings (IF-296, IF-308); the act template's notes and the catalogue regenerated; T2 and T6 mutation proofs | D1; D3; D4; SR-231; TC-368 | IF-296; IF-308 | P1 |
| P3 | Rows and text: LLR-338 and TC-368 amended; IF-296 and IF-308 data; Flow 6; the recipe in both copies; the `RESYNC_PACK.md` entry; `trunk_step.py --regen`; every touched registry parsed with `tomllib`; evidence regenerated | D5; SR-231; TC-368 | IF-296; IF-308 | P2 |
| P4 | Checks: the modules importing `adjudicate_act` or `acceptance_record` (27 for the latter), TC-321's modules (`tests/test_coordinator_act.py`, `tests/test_coordinator_adjudicate.py`), `tests/test_import_layers.py`, `tests/test_module_size_ratchet.py`, `tests/test_dogfood_sync.py`, `tests/test_complexity_ratchet.py`, `trace.py --strict`, `check_trajectory.py --strict`, the docs check, then `run_menu.py smoke` once | D1; D2; D3; D4; SR-231; TC-368; TC-321 | no interface: checks only | P3 |
| P5 | Close: the `## Deliverable` (each Done-when item, the real summary lines, the acts owed, the held-to-waiting mapping, the live verdict's new refusal), the spec moved to `docs/archive/work/complete/` with `specref` cleared and its links checked, the log fragment | D5 | no interface: records only | P4 |

Excludes: TC-365 — it verifies the coordinator's account and sign-in resolution under SR-231, which this item does not change; its three modules import no module this item edits directly (they reach `adjudicate_act` only through the unchanged entry point).

## Acts owed (preview; the Deliverable gives the final list)

- **Amendments to `Accepted` rows (text only):** LLR-338 `detail`; TC-368 `method` and `expected`.
- **Routed traced changes to `Accepted` rows:** none.
- **First acceptance, `Drafted`, rewritten:** IF-296 and IF-308 (`data`).

## For the coordinator's go-ahead

1. **"Waits" for the spec's "held"**, in every row, brief, refusal and report this item writes, because "held" names the held rung in the same texts.
2. **The hook's tier reader made public** (`_tree_tiers` renamed `parent_first_tiers`), so the wait and the hook judge the same rows and a failing parent registry refuses the derivation. Cost: the 27 test modules importing `acceptance_record` are run.
3. **A fixpoint over `parent_first_findings`**, not an ordered pass, so no edge table is restated.
4. **The waiting block rendered into the existing `{acceptance_act}` slot**, with no new slot and no new static instruction in the template; only its notes change, which drains a retained adjudicator once.
5. **SR-231 and LLR-306 unamended** (sections 3 and 4), the all-waiting refusal read as SR-231's "owing no act" for an act nothing can take yet.
6. **The coordinator-cycle recipe and a `RESYNC_PACK.md` entry are in scope**, though the spec does not name them.
7. **T9 tags TC-368**, not TC-321.

## Noticed, not in scope

- A waiting flip leaves its verdict owing an act that only a later sitting (the parent's) can unblock. Nothing reports a lane, or trunk, carrying such a verdict; the coordinator learns it from the act turn's exit 1. WI-1057's LLR-406 is in that state now. A standing report of verdicts with waiting flips would be a separate row.
