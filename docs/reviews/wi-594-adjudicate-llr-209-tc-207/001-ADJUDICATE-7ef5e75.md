# WI-594 ADJUDICATE round 001 — 7ef5e75

All-approve. Both rows are the SR-181 chain's only decomposition and its only
verifier, and both were read against the code and the tests they name rather
than against each other's prose. This is a FIRST approval on both: no prior act
returned `LLR-209` or `TC-207` (the three returns in this neighbourhood belong to
`WI-586`/`WI-590` and land on `LLR-207`/`TC-205`, which the trunk narrowing took
out of this row's scope — verified in `docs/reviews/wi-590-*` and in this spec's
Context). Nothing here is a reread of unchanged text.

Instruments run before ruling: `tests/test_phase_rule.py` → `13 passed in
3.91s`, every node `TC-207` cites and no test in the module left uncited;
`trace.py --strict-integrity` → `orphans=0 integrity=0 interface-findings=0`,
with no advisory naming either row; `derive_stage.py --phase-rule` on this tree
→ `phase rule clean`, the same reading the last cited test asserts.

Claim-by-claim re-derivation of `LLR-209.Detail` against
`project-trajectory/scripts/derive_stage.py` (every sentence, not a sample): the
strict-decrease early return (`:473`), the exemption as an ordered pair
(`_EXEMPT_DECREASE`, `:309`, compared as `(was, now)` at `:475` — so a two-rung
drop ENDING at Arch is not matched), the attributed set of five registries with
the derivation's own cells (`_ATTRIBUTED_ROWS`, `:288-294`), attribution on
new-or-moved with a stripped case-insensitive compare (`:401-412`), the frame
arm (`_PHASELESS_KEYS`, `:300`, `:501-514`), the silent degrade off git
(`_spine_at`, `:331-332`, `:468-469`), and the carrier tiers in `main`
(`:594-600`: WARN + exit 0, `--strict` → FAIL + exit 1, and no caller anywhere
else — `grep -rn phase_rule` finds no gate wiring, so the row's negative claim is
true at this tip). The one clause that is a claim about ANOTHER function I
re-derived independently rather than reading back: "the same basis the recorded
`phase =` field is derived from" — `phase_rule_findings` folds
`max(phase_num)` over non-Drafted `srs/llrs/tcs` of the before side
(`:481-488`), and `derive` folds exactly that over the same three keys
(`:237-240`). Same basis; the rule and the field cannot come to mean different
things, as stated.

- [APPROVE] LLR-209 -> a builder must ship one authoring-time predicate over two trees: load the live spine and the spine at HEAD, return nothing unless the live effective stage is strictly lower, exempt exactly the ordered pair `DevStg-LLReqs -> DevStg-Arch`, attribute the decrease to every row of the five stage-affecting registries that is new or whose derivation-read cells moved, fault only those carrying the standing phase (max Phase over the before side's non-Drafted rows), report a frame row with its cause instead of demanding a phase cell it has no place for, return `[]` where there is no HEAD, and carry it on `main --phase-rule` at WARN with `--strict` as the sole promotion -> UPWARD it decomposes `SR-181` clause for clause and adds nothing the parent did not ask for (`SR-181` itself names the firing case, the one exemption, the frame row, the silent degrade and the warn tier); SIDEWAYS it is the parent's only child and it does not reach into its module-mates' decisions — `LLR-186` owns the record producer (`derive/_stage_map/_phase_groups`) and `LLR-148` owns `--next-phase`, so the shared `main` carries three distinct modes with one decision each; DOWNWARD `TC-207` is its sole verifier and drives every arm it states -> READY. Every clause above verified TRUE against the module at this tip (line-by-line above), the row restates as one closed obligation with no unnamed actor and no observable left to the reader's judgement, and its two negative claims — "matched as a pair and not as a destination" and "not wired into any gate's strict trio" — are the two a stale row would most likely be lying about, so both were driven rather than read: the first has a dedicated failing-if-broken test, the second I re-grepped across the tree. The standing-phase clause even closes the case the code guards separately (`standing is None`): a spine with no settled phased row has no standing phase for a row to carry, so "a row carrying that standing phase is the finding" already entails the silence, and the row needs no extra sentence for it.
- [APPROVE] TC-207 -> the test must drive the rule on real git repositories (its before-state IS `HEAD`), pin the finding SET on each arm rather than merely observing a non-empty report, and cover both sides of every decision `LLR-209` states: fires in the standing phase, silent under a new higher tag AND under an already-open lower one, exempt on the pair, fires on the two-rung drop that only ends at Arch, fires on component-only and boundary-only edits, fires on a re-drafted child, cannot fire on a new draft at all, silent with no git, WARN-then-FAIL at the CLI, and clean on this repo -> its `Verifies` names both `SR-181` and `LLR-209`, its `Expected` restates the parent's acceptance criteria without inventing a condition the parent does not impose, and each of the 13 `Evidence` node ids resolves to a test that exists and passes -> READY. The Method is accurate about the fixtures, not just about the intent: the arms assert counts (`len(findings) == 1`/`== 2`) alongside content, so nothing extra can hide behind a substring match; the exemption arm really does re-introduce a component registry, which is what makes the Arch rung reachable at all; and the frame arms assert the finding names the row and the moved cell (`"Standing" in joined`) rather than asserting a bare truthy report. Coverage is closed in both directions: no clause of `LLR-209` goes undriven, and no test in `tests/test_phase_rule.py` is left uncited by this row (13 functions, 13 citations). `Tier = "Full"` is the honest tier and not an overstatement — the module is in `conftest.SLOW_MODULES` (`tests/conftest.py:173`) and so is excluded from the smoke bar, exactly as `Full` claims.

OBSERVATION FOR A LATER LANE, not a finding and not a condition of this
approval: `_effective` deliberately leaves the test-evidence verdict at its
default on BOTH sides of the comparison (the `WI-500` decision recorded in its
docstring, `derive_stage.py:362-368`), which is the one decision inside this
row's own `CodeSymbol` set that its `Detail` does not state — `LLR-209` says the
stage is derived "through the module's own producer", which is true of
`_stage_map`/`effective_stage` but leaves a rebuilder free to thread the live
evidence verdict through. It is symmetric either way, so nothing observable
turns on it today and it is not a gap in the obligation; it is one sentence a
future amendment could add if that symmetry ever stops holding.

OUTCOME: APPROVE rows=2
