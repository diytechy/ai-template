# WI-402 — REVIEW-A (independent)

### REVIEWER — G3 — Round 1 — 2026-08-02

Reviewed at `7995cd5f` (branch `wi-402-phase-numeric-only-and-next-phase`;
work commit `e0623526`; trunk = `ConcurrencyTrainRewrite`). I did not write
this work; I drove it to break it. Requirement surface read: the spec of
record `docs/work/complete/WI-402-phase-numeric-only-and-next-phase.md`
(frontmatter title — both halves and the ruled phase-boundary),
`docs/registry-machinery-reference.md` §3.3 as amended, and the §A5.1/§A5.2
ratified/traced doctrine (`docs/concurrency-v2.md` +
`check_trajectory.SPINE_RATIFIED_CELLS`). `docs/log.d/` fragments were not
read.

Verdict: APPROVE

## Findings

**1. MINOR — TC-003's amended `Method` re-asserts a suite that does not
drive the phase clauses it describes.** The amended cell reads *"Run the
registry-checks suite; … (once the spine is phased) a ratified row whose
Phase is not a full-cell bare integer (blank, prefixed like P1/v2, or
unparseable) are flagged"*, and TC-003's `Evidence` cites only
`tests/test_registry_checks.py` — but that file contains **zero**
phase-related tests (`grep -c` phase = 0; its 26 tests drive the `-000`,
required-field and enum halves). Every driver of the phase rule lives in
`tests/test_trace.py`: `test_phase_ratified_rule_arms_and_fires` (:953),
`test_phase_ratified_rule_is_numeric_only` (:972),
`test_ratified_blank_phase_fails_strict_schema` (:1019),
`test_ratified_prefixed_phase_fails_strict_schema` (:1030). The mis-pointer
is **pre-existing** (the before-text made the same "registry-checks suite"
claim for the blank/unparseable case, with the same Evidence cell), so this
is perpetuated, not introduced — but the WI-402 amendment sharpened the
claim (P1/v2 named) while leaving the pointer stale, and an adjudicated
cell should not re-assert a location that is false. The behavior itself is
fully verified (I ran all four drivers green, and drove the rule by hand —
"Verified" below). **Remedy (follow-up, no round owed):** extend TC-003
`Evidence` to `tests/test_registry_checks.py;tests/test_trace.py` (or move
the four tests). `Evidence` is a *traced* cell (§A5.1), so the fix is a
mechanical edit — no re-attest window. -> follow-up -> @builder

**2. NOTE — a Draft row's phase "is not yet scope" for Half 2 but ARMS the
rule in Half 1; the asymmetry is documented on each side and reconciled on
neither.** Driven: `{SR-001 Draft Phase=v9, SR-002 Verified Phase=blank}`
produces the SR-002 blank-Phase finding — the Draft row alone armed the
rule — while the same Draft row is excluded from `--next-phase`'s max
("a Draft row's phase is not yet scope"). Pre-existing arming semantics
(the arming line is unchanged context in the diff; the docstring's "phases
ANY spine row" is accurate) and defensible — a phased Draft signals the
discipline is adopted even before ratification — but §3.3 now states both
stances without noting they diverge on Draft rows. Recorded; no remedy
owed this round. A one-line note in §3.3 would close it.

**3. NOTE — `--next-phase` silently short-circuits `--check` and
`--print`.** `derive_gate.py --check --next-phase` prints the number and
exits 0 without running the freshness guard (the `if args.next_phase:
… return 0` block sits above both). This mirrors the pre-existing modal
precedence (`--print` already short-circuits `--check` the same way), so it
is consistent house CLI style; recorded so nobody wires
`--check --next-phase` into a hook expecting both. No remedy owed.

## Verified (hunted, held — no remedy owed)

- **The staged-amendment surface is exactly the two argued cells.**
  `check_trajectory.staged_spine_amendments(".", base="ConcurrencyTrainRewrite",
  head="HEAD")` returns precisely two records: `LLR-003` with one RATIFIED
  cell (`Detail`) and `TC-003` with one RATIFIED cell (`Method`); no traced
  changes, no other amended rows (LLR-148/TC-142 are NEW rows, excluded by
  design). Nothing else on the branch touches attested prose.
- **Half 1, driven by hand on scratch registries** (all six shapes,
  outputs observed): bare integers green (incl. ` 2 ` — stripped, matching
  the literal joins which also strip); `P1` red once armed, naming the row;
  a `vN` registry **arms the rule AND fails it, per cell** (two findings on
  `v1`+`v2`, each quoting its literal cell — reads sanely); Draft rows
  exempt with `v9` or blank; an unphased spine leaves the rule dormant
  (`[]`); an armed ratified blank still reds. The finding text names both
  silently-vacuous joins verbatim: *"a prefixed label silently misses the
  literal --phase/--ratify and phase-drop joins"*.
- **Grandfathering intact:** `phase_num` (trace.py:175) and its F5 copy
  (derive_gate.py:139) are untouched by the diff; `check_trajectory.py` is
  not in the diff at all. The literal joins confirmed literal:
  `in_phase` (trace.py:2070) matches `tag in phases` on the stripped cell;
  `_scope_srs` (trace.py:1030) matches `_cell(s,"Phase").lower()`.
- **Legacy anchors untouched:** `[vN]`-style titles exist in
  `docs/work/complete/` (e.g. `WI-141-v3-…`) and the only complete/ file in
  the diff is WI-402's own spec.
- **Half 2:** `derive_gate.py --next-phase --root .` prints `5` on this
  repo (basis `phase=4` + 1), including from a foreign cwd via `--root`;
  `git status docs/gate` clean after both runs. The byte-pin test exists
  and passes (`test_next_phase_prints_max_plus_one` asserts docs/gate
  byte-identical; Draft row at 4 never bumps a max of 3); the unphased
  spine prints 2 (`test_next_phase_on_an_unphased_spine`) — a sane recorded
  judgment: blank rows ARE the implicit foundation (1) under `in_phase`, so
  the first opened phase must be 2 or it would collapse into the
  foundation. The `return 0` sits before every write path; `sys.exit(main())`.
- **Doc coherence:** WI-401 compose claim holds — WI-401's reference-doc
  hunks (`38091685`: @@ −67, −278, −310, −318, −339, −375) are disjoint
  from WI-402's (@@ −131, −183, −685, −721), and `sn_cited_ids`/`uncovered=`
  still present (3 hits). PROCESS.md §-headings byte-identical to trunk
  (§-numbering stable). Byte budgets re-stamped **with reason** in all
  three byte-budget-guard homes, and the three copies are byte-identical;
  the guard's check passes: `wc -c` = **64,460** (PROCESS.md) and
  **169,010** (PROCESS_OPTIONS.md), exactly the stamps. ADOPTING.md §6
  carries the migration note (strip `v2`→`2`; correctly states `Phase` is
  traced, so no re-attest window — true per SPINE_TRACED_CELLS). EXAMPLE.md
  updated and `tests/test_gen_cases.py` (the EXAMPLE.md snippet-parse
  guard) green.
- **Registration truth:** LLR-148 and TC-142 read exactly what I measured
  (`max+1`, bare, docs/gate never written, Draft excluded, unphased → 2);
  the amended LLR-003 `Detail` matches the shipped rule clause-for-clause
  (numeric-only once armed, digit-parse arming, literal-join rationale,
  `phase_num` grandfathering) — the sole inaccuracy is the suite location
  carried in TC-003's Method, finding 1.
- **Mechanical, all re-run by me at `7995cd5f`:** touched + adjacent suites
  `test_trace.py test_derive_gate.py test_module_size_ratchet.py
  test_gen_cases.py test_dogfood_sync.py` → **106 passed**; the five
  WI-402-named tests pass in isolation. Smoke `-m smoke -n auto`: **620
  passed, 2 skipped in 9.97s** (the spec's fig is 616/6 at `e0623526` —
  same 622 total; skip-count drift is environmental, the figure is
  rev-pinned and plausible). Full unfiltered suite `-q -n auto`: **1874
  passed, 6 skipped in 0:04:51**, exit 0 (the spec's fig is 1870/10 at
  `e0623526` — same 1880 total, the identical 4-skip drift as smoke).
  Spot-check two of the 28 figures: the `--next-phase prints 5` fig
  reproduced exactly; the full-suite fig reproduced to the same total with
  the environmental skip split noted. `trace.py
  --strict --no-placeholders --html --require-verified --strict-schema`
  rc=0; `derive_gate --check` rc=0 ("docs/gate up to date (G3)");
  `check_trajectory --strict` rc=0 and **the WI-402 SpecRef WARN is gone**
  (remaining SpecRef warns name WI-389/WI-390 only — pre-existing,
  concurrency-v2.md); `check_figures --strict` rc=0 with **28 declared
  figures**; `check_doc_refs --strict` rc=0; `ruff check .` clean; trace.py
  ratchet **2919 exact** (`len(splitlines())` = 2919 = baseline, reason
  comment in place). docs/work delta is WI-402-only (active→complete move;
  one log.d fragment added, unread per protocol).

**ADJUDICATION ACT (LLR-003 `Detail`, TC-003 `Method`).** Under
`docs/gate-policy` `autonomous`, a recorded independent reviewer verdict
carries the adjudication-class judgment below G-Final (the same
autonomous-act shape as WI-392's SR-136 ratification). **This APPROVE is
that act: the no-flip amendment of LLR-003 `Detail` and TC-003 `Method` at
`e0623526` is hereby adjudicated as scope-not-moved** — the §A5.2 cheap
outcome, taken directly instead of round-tripping through a minted
adjudication WI whose only sane verdict this is. Grounds, from the diff and
the doctrine, not the lane's say-so: (a) the attestation unit is the SR,
and SR-003's ratified cells never spoke of the Phase rule at all — its
Requirement/AcceptanceCriteria cover `-000` rows, required fields and
Verification/Tier vocabulary, all untouched — so no ratified requirement
scope moved; (b) the old cells were **factually falsified by an owner
ruling** ("a downstream vN parses and passes" stopped being true the moment
the 2026-08-01 numeric-only ruling shipped), and the amendment restores
registry truth to the ruled behavior — the grammar/truth-restoration shape
§A5.2 names; (c) the scope question the Modified window exists to put in
front of a sitting was already answered *by the owner, in the ruling this
WI implements* — flipping SR-003 would open exactly the spurious re-attest
window the same ruling's boundary text condemns (the WI-280 shape); (d) the
amended cells are re-verified: I re-ran their evidence green and drove the
described behavior by hand. Finding 1 is recorded beside the act as a
bounded registration residue (a stale *traced* Evidence pointer perpetuated
from before this WI) — it does not narrow the adjudicated cells' truth and
owes a follow-up, not a round. Had scope moved, this would have been MAJOR;
it did not.

Findings this round: 1 MINOR (follow-up owed), 2 NOTE (recorded, no remedy
owed). Both halves of the WI are built as specified, the registration is
true where it is load-bearing, and every mechanical claim in the
deliverable reproduced under my own runs.

VERDICT: APPROVE findings=3
