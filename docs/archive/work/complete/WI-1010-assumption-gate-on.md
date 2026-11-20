+++
id = "WI-1010"
title = "This repository turns its assumption gate on, once its four steps report nothing"
workstream = "requirements"
sr_refs = ["SR-205", "SR-212", "SR-206"]
needs = ["~WI-1008"]
specref = ""
buildtier = "medium"
safety_class = "spine"
priority = 3
planmode = "single"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1010`, cut from `refactor_again` at
`1cb2e8680`. Both deliverables landed, in the stated order. The operator's
act and the flip follow the lane (below). The spec of record was
`docs/plans/2026-11-11-test-tiers/HANDOFF.md` §12.6; the row's SpecRef cell
was cleared at close.

- **Critique dispositions** (`1ee58e149`): all five findings adopted. The
  Done-when holds only the page and the arguments; the act and the flip are
  "After this row".
- **Plan** (`d69175149`): `docs/plans/WI-1010/plan.md`.
- **Tests first** (`e0a159097`): `tests/test_open_items_assumptions.py`,
  three tests under the declared strict expected-failure marker, each seen
  failing at an assertion (no card; no card for DA-003; no shared model).
  TC-448, `Drafted`.
- **The page** (`5f097b2dd`): `trace.assumption_owing_model` is the one model
  of the assumptions and surrogates owing an acceptance; the brief's section
  is rebuilt on it, its text unchanged, and `gen_open_items` renders it as
  section 2's last block (`_assumption_cards`, with the need card's body
  shared as `_owing_card`, closed by `_relied_on`). The header counts the
  rows and its drifted count takes in a drifted one. **Size:**
  `gen_open_items.py` measured 938 code lines by the ratchet's own
  `module_sloc` (the brief's 996 did not reproduce) and 970 after, under the
  1000 threshold, so it needs no baseline entry; the rendering went there
  because 62 lines of headroom held it, and the model went to `trace.py`
  beside `assumptions_owing`, whose exact pin is re-stamped 3836 -> 3844.
  IF-074 (data, coincident, contract), IF-075 (data, contract), LLR-118 and
  LLR-271 (amended, `Accepted`, drifting for re-accept) say it. The page
  now carries 32 assumption and surrogate cards.
- **The arguments** (`bcbc538e6`, wording fixes `94dabd142`): the table
  below. The new rows, DA-021 to DA-028 and SUR-004, are in
  `docs/requirements/assumptions.toml`, each `Drafted` and `active`; the log
  fragment gives each one's claim in a line.

| Requirement | Argument |
|---|---|
| SR-024 | coincident: the case set expanded from the declared inputs is the coverage the reviewer reads |
| SR-129 | coincident: a cell-exact conversion leaves the registry the derivation reads as it was |
| SR-224 | DA-025 (new): an agent chooses a skill by its description |
| SR-226 | coincident: the record found by the retired id is what the reader finds |
| SR-228 | DA-026 (new): a CLARITY ruling rules as the operator would |
| SR-229 | DA-021, DA-022 (new, B-09) and DA-023 (new fidelity on SUR-004, B-10); IF-080 bridged by DA-021, DA-022; IF-275 tied to B-04 |
| SR-230 | DA-021 and DA-023; reached by IF-275 (B-04, bridged by DA-021) |
| SR-231 | coincident: success is only a verdict this call wrote, at its reserved path, in time; reached by IF-321 (new, from B-10) |
| SR-232 | coincident: a combined sitting is refused whole unless every requested kind is judged; reached by IF-321 |
| SR-233 | DA-027 (new): the normal working environment; DA-028 (new): judging sessions apply the review directions |
| SR-234 | coincident: a verdict is accepted only when it rules every requested finding once; reached by IF-322 (new, from B-10) |
| SR-235 | joint as before, now also DA-007; crossing re-pointed B-05 -> B-09; reached by IF-289 (tied to B-05) |
| SR-236 | coincident: no finding is dropped, renumbered or replaced before rework |
| SR-237 | DA-021 and DA-024 (new): the coordinating session acts on its instructions |
| SR-238 | coincident: the coordinator checks the process tree ended before it continues |
| SR-241 | coincident: no review starts over a tree known to fail its checks |
| SR-242 | coincident: the capped lane's partial close is the outcome the operator reads |
| SR-243 | DA-016 (existing) and DA-024 |
| SR-244 | DA-022 and DA-024 |
| SR-245 | coincident: the parent-first finding is the check's verdict |
| SR-246 | DA-004 (existing, staged arm) and DA-013 (existing, lane arm) |
| SR-247 | DA-014 (existing): the adopter upgrades by the documented route, which runs the migrator |

**The four steps** (gate off, so advisories), base `1cb2e8680` -> tip:

| Step | Before | After |
|---|---|---|
| `assumption-gate` | 79: 49 on a `Drafted` assumption, 9 on a `Drafted` surrogate, 21 citing nothing | 79: 68 on a `Drafted` assumption, 11 on a `Drafted` surrogate, 0 citing nothing |
| `crossing-allocation` | 9 | 0 |
| `interface-allocation` | 6 | 0 |
| `assumption-evidence` | 0 | 0 |

Every line left is a requirement relying on an assumption (DA-001 to
DA-028) or a surrogate (SUR-001 to SUR-004) that is `Drafted`, which the
operator's acceptance clears. No reach finding appears.

Left for the operator, and why:

- **The act.** Accepting DA-001 to DA-028 and SUR-001 to SUR-004, and
  re-accepting the amended rows: the eleven requirements given a waiver
  (`coincident` is accepted text, SR-193) and LLR-118 and LLR-271. All are
  on `docs/open-items.html` §2.
- **The flip**, after the act: `[checks] assumption_gate = true` in
  `docs/process.toml` with its comment dated, and `check.py` passing with it
  on. One line; no row is filed for it.
- **Judgements the operator may overrule.** SR-235's crossing re-point (a
  traced cell that routes to adjudication) in place of a waiver its joint
  argument would contradict; IF-275 and IF-289 tied back against their
  former "No tie-back" notes, on the frame's own B-04 and B-05 text; DA-020's
  falsifier is still met by the October decisions backlog (WI-1008).
- **Not changed:** `form` on any row (each of the six is met at an
  interface); IF-281, IF-284, IF-285 and IF-288 stay untied, as nothing this
  row closes needed them.
- **Review (2026-11-20, `e48a1c01c`).** Sol on the code: no findings.
  Argon on the prose, seven findings, all applied: DA-023 names both fixture
  versions; DA-025 no longer leans on the kit's description floor; DA-027's
  holds_when no longer allows the hand act its assumption rules out;
  SR-226's, SR-234's and SR-238's waivers are bounded to what each row
  checks; IF-074's data names the uncited items and record findings again.

## Context

Filed by hand on 2026-11-18 at the operator's direction: "turn on the
assumption check when ready". `docs/process.toml` holds
`[checks] assumption_gate = false`. Its comment says turning it on is this
repository's own act, taken once its requirements' assumptions are accepted.
With the gate off, `check_assumption_gate.py` prints the same findings as
advisories, so what turning it on would fail is known. On 2026-11-18, after
act seq 183, it was 91 findings:

| Step | Findings | What they are |
|---|---|---|
| `assumption-gate` | 46 | a requirement relies on an assumption that is `Drafted` (all 17, DA-001 to DA-017) |
| | 9 | a fidelity assumption whose surrogate is `Drafted` (SUR-001 to SUR-003) |
| | 21 | a requirement cites no assumption and records no `coincident` waiver: SR-024, SR-129, SR-224, SR-226, SR-228 to SR-234, SR-236 to SR-238, SR-241 to SR-247 |
| `crossing-allocation` | 9 | SR-229, SR-230, SR-231, SR-232, SR-234 and SR-235 name crossings no cited assumption lands on |
| `interface-allocation` | 6 | the same rows: five reached by no boundary interface, SR-229 reached by IF-080, which no cited assumption bridges |
| `assumption-evidence` | 0 | |

SR-033, SR-223 and SR-225 are not in the list, because the gate's joint skip
passes them. WI-1008 writes their premises anyway. Doing it first means one
acceptance act covers every new assumption, hence the soft edge.

At this row's base (`1cb2e8680`, trunk after WI-1008), the steps report 94:
`assumption-gate` 79 (49 lines on a `Drafted` assumption, DA-018 to DA-020
now among them, 9 on a `Drafted` surrogate, and the same 21 citing nothing),
`crossing-allocation` 9, `interface-allocation` 6 and `assumption-evidence` 0.

The operator rules on `docs/open-items.html`, and it does not show
assumptions or surrogates: its §2 renders SR chains and stakeholder needs
only. `docs/status.md` already records the missing view. The Markdown brief
(`trace.py --accept modified`) renders them, as SR-203 asks.

### The delta

**The page (built first).** `docs/open-items.html` §2 gains a block for the
assumptions and surrogates owing an acceptance, after the stakeholder needs.
The rows are the ones the acceptance brief's assumption section renders:
`trace.py` gains `assumption_owing_model`, the brief's section is rebuilt on
it, and `gen_open_items.py` renders the same model as HTML. There is one home
for what is owed, and the page holds no second opinion. Each card shows a
`Drafted` or Status-less row's cells whole, or a drifted row's moved cells
before and after, then the requirements relying on the assumption (for a
surrogate, the assumptions naming it). The seam is the existing one from
`scripts/gen_open_items` (CMP-009) to `scripts/trace` (CMP-006), IF-075, which
gains the new function in its data and contract. No new seam reads
`assumptions.toml` from the page: `trace` reads it, as it does for the brief.
IF-074's data and its `Contract IF-074:` block name the new block, and
LLR-118 and LLR-271 are amended to say it. Both are `Accepted`, so they stay
`Accepted` and drift for the operator's re-accept.

**The arguments (built second).** Registry rows, plus two contract blocks in
code docstrings. Each of the 21 requirements gets either `da_refs` citing an
assumption that carries it to its needs, an existing one where it truly
fits, or a `coincident` waiver that argues its own behaviour is the outcome.
`da_refs` is traced, so citing re-opens no acceptance. `coincident` is
accepted text (SR-193), so a waiver makes its `Accepted` requirement drift
for the operator's re-accept. New assumptions take DA-021 onward and are
`Drafted`. A claim about the model runner lands on B-09, where the operator
reads the work back, as DA-006, DA-016 and DA-017 do. B-10 belongs to the
model provider, no stakeholder's party, so only a fidelity assumption (one
whose surrogate emulates the provider) can land there without a reach
finding. B-05, the delivered package, is never a landing.

The interface-form rows, named exactly (S3):

| Row | Crossing findings | Interface finding | How each is closed |
|---|---|---|---|
| SR-229 | B-09, B-10 | reached by IF-080, bridged by none it cites | cites assumptions landing on B-09 and a fidelity assumption landing on B-10; IF-080's `bridged_by` (traced) gains the agent-CLI assumptions its claim reading rests on |
| SR-230 | B-09, B-10 | reached by none | the same assumptions as SR-229 for its crossings; IF-275, the coordinator guard's hook response, gains its tie-back to B-04 (a guardrail verdict during a session, which B-04 carries) and is bridged by the agent-CLI hook assumption |
| SR-231 | B-10 | reached by none | a `coincident` waiver; a new row IF-321, the verdict file the adjudicator writes at the path the entry point reserved, ties back from B-10 |
| SR-232 | B-10 | reached by none | a `coincident` waiver; IF-321 reaches it through LLR-310's module |
| SR-234 | B-09, B-10 | reached by none | a `coincident` waiver; a new row IF-322, the dispute verdict the adjudicator writes in `kitlib.dispute`'s grammar, ties back from B-10 |
| SR-235 | B-05 | reached by none | joint already; keeps its siblings and cites the independent-review assumption DA-007; its crossing is re-pointed from B-05 to B-09, where the review record is read (both cells traced); IF-289, the review command's result codes, gains its tie-back to B-05, as the result codes of `integrate` (IF-080) carry |

No `form` changes: each of the six is met at an interface. Every IF row is
`Drafted`, so tying one back or minting one re-opens no acceptance. A new row
states its contract beside its owner's code, as every row does. The live frame
test (`tests/test_frame_context.py`) pins the untied rows and B-10's empty
realization, so it moves with them.

## Done-when

This lane delivers two things, in this order, and stops before the
operator's act.

- [x] **The page shows what the operator must accept.** `docs/open-items.html`
      §2 renders every assumption and surrogate owing an acceptance (`Drafted`,
      Status-less, or accepted and drifted from `docs/archive/last_accepted/`),
      each row's cells whole or, for a drifted one, before and after, with the
      requirements relying on it. The rows come from the model the
      `trace.py --accept modified` brief renders, so the two cannot disagree.
      The header counts them. Regression tests pin a first-acceptance card, a
      drifted card and the page's agreement with the brief, and were seen to
      fail first. IF-074 (row and contract), IF-075, LLR-118 and LLR-271 say
      it. `gen_open_items.py` stays under the module size threshold.
- [x] **Every finding left is one the operator's acceptance clears.** Each of
      the 21 requirements cites an assumption that carries it to its needs,
      or records a `coincident` waiver. The nine crossing findings and six
      interface findings in the table above are closed as it says. Each new
      assumption and surrogate states where it lands, when it holds, its
      obstacle and a falsifier someone can observe, and is `Drafted`. After
      the work, `crossing-allocation` and `interface-allocation` report 0,
      `assumption-evidence` reports 0, and every `assumption-gate` line is a
      requirement relying on a `Drafted` assumption or on a fidelity
      assumption whose surrogate is `Drafted`. The before and after counts
      per step and per kind are in the Deliverable.
- [x] `trace.py --strict`, `check_trajectory.py --strict`,
      `gen_open_items.py --check` and the touched test modules pass.

### After this row (not this lane's)

1. **The operator's act.** The operator reads §2 of `docs/open-items.html`,
   accepts the assumptions and surrogates, and re-accepts the requirements
   and design rows this row amended. That act is the operator's alone.
2. **The flip, one line.** Once all four steps report 0, the operator or a
   later session sets `[checks] assumption_gate = true` in
   `docs/process.toml`, with its comment saying when it was turned on, and
   checks that `check.py` passes with it on. No row is filed for it: it is a
   one-line change that follows the act.

## Critique dispositions

Round 1 (Gemini Argon, 2026-11-19,
`docs/reviews/2026-11-19-scope-critiques/WI-1010.md`): CHANGES-REQUESTED, four
MAJORs and one MINOR. All five are adopted. None grows the row: the act and
the flip leave the lane rather than being added to it.

- **B4, the operator's act mixed with build work: adopted.** The Done-when
  now holds only what this lane builds: the page and the arguments. The
  operator's act and the flip to `assumption_gate = true` are stated under
  "After this row" as what follows the lane. The flip is a one-line change
  the operator or a later session makes after the act, and no row is filed
  for it. The lane closes complete when its two deliverables land, not
  partial: nothing in its Done-when waits on the operator.
- **S1, three landable deliverables with no order: adopted, kept whole.** The
  third (the act and the flip) left the lane under B4. The other two stay one
  row, in a stated order: the page first, then the arguments. The page comes
  first because the operator must read the arguments' new rows on it before
  accepting them. The two land on one branch, and one act judges everything
  the arguments add.
- **S4, `planmode`: adopted as `planmode = "single"`.** The page is a code
  change to `gen_open_items.py` and `trace.py` with an IF-074 contract change,
  so a short plan precedes the code (`docs/plans/WI-1010/plan.md`). The
  Done-when's second bullet chooses: the page renders the rows, and the
  regenerated brief is not offered as the alternative.
- **S5, the architectural delta: adopted.** "The delta" above states it. The
  page adds no cross-component seam: it calls `trace` through IF-075, which
  already declares that seam. The arguments add two IF rows (IF-321, IF-322),
  give tie-backs to two existing rows (IF-275 to B-04, IF-289 to B-05) and
  widen one `bridged_by` (IF-080). No requirement changes `form`.
- **S3, which crossings and interfaces: adopted.** The table in "The delta"
  names each row's crossings (B-05, B-09, B-10) and each interface row that
  closes its interface finding (IF-080, IF-275, IF-289, IF-321, IF-322). SR-235
  is in the set although the assumption gate's joint skip passes it, because
  the crossing and interface steps judge it.
