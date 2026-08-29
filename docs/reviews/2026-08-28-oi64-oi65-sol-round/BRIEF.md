# OI-64 / OI-65 legibility round — what was checked, accepted and declined

**Date:** 2026-08-28. **Reviewer:** OPENAI-SOL (`codex exec --model gpt-5.6-sol`),
cross-family. **Trigger:** the owner could not tell what either row was asking.
**Scope:** no file was edited by the reviewer; every finding below was
re-verified in this repo before it was applied.

The registry's own schema already forbids what these two rows had become —
*"WRITE FOR A RULER, NOT FOR THE RECORD… one_line: ONE sentence, <= ~35 words…
WHAT DOES NOT BELONG IN A BRIEF: how the item came to be filed; which review
found what; rebuttals of objections nobody has raised."* The rewrite is schema
enforcement, not a style preference.

## Findings accepted, each independently re-verified

| # | Finding | How it was verified | Effect |
|---|---|---|---|
| 1 | The "eleven-to-thirteen restating rows" is **ten**. `SR-015` states no severity, location or vacuity rule; `SR-164` states only "naming the row". | Read all 13 rows' `requirement` + `acceptance_criteria`. | Count corrected on `OI-64`; both rows named as excluded. |
| 2 | Four of the ten (`SR-167`, `SR-180`, `SR-181`, `SR-182`) make severity or exit behaviour **part of the obligation**, not a side clause. At most six clauses are removable. | Same read. | Option (a)'s sweep re-stated as "up to 6 clauses", not 13 rows. |
| 3 | `SR-158` does **not** declare itself unsatisfied. It states a condition; the measurement found the per-class declarations; the row is `Approved`. | Read the acceptance cell and `status`. | The "corpus concedes the hole in its own words" passage deleted as an over-read. |
| 4 | An SR row has **no field for citing an interface**. | Enumerated SR keys across all 75 rows: title, sn_refs, boundary_refs, hat_refs, requirement, rationale, acceptance_criteria, priority, verification, status, phase, aspect. | Recorded on `OI-64` as a blocker: option (a) has no legal mechanism today. |
| 5 | The anchor count is **57 of 78 modules, leaving 21** — not 57 of 76 / 19. | `find project-trajectory/scripts -name '*.py'` → 78; `grep '^\s*Contracts: IF-'` → 57. | Corrected on `OI-65` and in `docs/status.md`. |
| 6 | `gen_arch_map.module_contracts` **already miscounts**: it reads `handback.py` as declaring `IF-080` although its docstring says *"No `Contracts:` line, deliberately"*. | Called the function directly on the parsed module; it returned `['IF-080']`. | Recorded on `OI-65`; option (b) cannot be priced as though the harvester works. |
| 7 | The character figures are per-clause judgements, not measured spans, and two rows were later reclassified without updating the total. | Re-summed the verdict table (43,995 / 28,305 / 8,975 / 6,715 all sum exactly) and read the addendum. | Row counts kept as exact; character figures marked approximate. |
| 8 | Arithmetic error in the cleanup record: 6,715 − 6,136 = **579**, stated as 679. | Arithmetic against `2026-08-25-if-contract-verdicts.md:496-497`. | Character figures no longer leaned on; the record's line is left for its own correction. |
| 9 | "Nothing reads an IF `rationale` at all" is too strong — the loader parses and retains it. The accurate claim is that no **content lint** inspects it. | `IF_REASON_CELLS = ("Notes", "SignalNote")` at `trace.py:2194`; the field is loaded and 37 rows carry it. | Wording narrowed to "no content lint reads `rationale`". |
| 10 | Both rows bury the decision under filing history, method narration and rebuttals of objections nobody raised. | — | `one_line`, `options` and `recommendation` rewritten in "Do X / Effect / FOR / AGAINST" form; `decision` cut to the facts needed to rule. `OI-64` 16,215 → 5,185 chars; `OI-65` 15,512 → 7,463. |

## Found in this round, not by the reviewer

**`SR-181` is a counter-example inside `OI-64`'s own list.** Its acceptance says
the rule *"degrades silently (reports nothing) when no prior committed state is
available to compare against"*, while `SN-008` requires that a pass verdict never
hide a skipped check. So the fourth clause `OI-64` admits it never measured —
*every degrade is named, never silent* — already has a live violation in an
`Approved` row. A contract carrying that clause lands red on day one. Recorded on
the row as a required guard.

## Confirmed unchanged

- `_WI_TOKEN_RE` at `trace_text.py:272` is case-sensitive; `wI-280` sits in
  `IF-082`, `IF-083`, `IF-084` and is invisible to it. Exactly 3 tokens repo-wide.
- Widening `IF_REASON_CELLS` to include `rationale` produces **0 findings** on the
  current 37 cells. Option (iv) is free on today's tree — driven, not estimated.
- All ten deletion-queue rows exist and are `Drafted`; editing them needs no
  re-approval. All 135 interface rows are `Drafted`.
- The `OI-65` totals re-sum exactly, and `trace.exit_code` composes from named
  failure collections only — no advisory reaches it.

## Declined

- **The reviewer's recommendation of (a) for `OI-64`.** Its own finding #4 shows
  (a) is not executable: there is no way for an SR to cite an interface. The row
  now recommends **(b) now, (a) later if that field is built** — same contract
  stated, no re-approval, and the six-clause cleanup stays available.
- **Re-measuring the character counts before ruling.** Nothing in either
  recommendation turns on them; they are marked approximate instead. Re-measuring
  is a third pass on a number no option depends on.

## Not done here, and why

The two false claims in `IF-117` and `IF-061` are named but **not corrected** —
writing their true replacement text is option (i)'s work and needs the owner's
ruling first. The harvester false positive (#6) is **recorded, not fixed**: it is
a shipped-script change and this was a registry-legibility pass.

## Verification

`trace.py` exits 0. `pytest -q -n auto -m smoke` → **1363 passed, 6 skipped**.
The smoke wall-clock budget check FAILS here (112.5 s vs the 60 s budget) — this
is **pre-existing on this machine**: stashing the change and re-running at HEAD
also breaches it (86.6 s). Not introduced by this pass.
