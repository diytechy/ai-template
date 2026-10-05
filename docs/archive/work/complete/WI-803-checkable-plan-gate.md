+++
id = "WI-803"
title = "A checkable plan gate over Done-when, findings, SR and TC coverage"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

`plan_coverage.py` is a gate. A SINGLE run (`--item SPEC.md [--findings FILE]`) takes its clauses from the item's Done-when (`D#`, through `kitlib.done_when`) and open review findings (`F#`); every clause is covered by a row or named under `Excludes: <clause> — <reason>`, and an unexplained gap exits 1 naming it. The SINGLE run also diffs the item's SRs (each must be cited; an SR cannot be excluded) and the TCs that verify them (named or excluded with a reason). By the independent adjudicator's ruling on the builder-reviewer dispute (`docs/reviews/wi-803-plan-gate/dispute-1-ruling.md`), an unexplained DUAL goal-clause gap fails too; existing DUAL fixtures and their `--out` report bytes are unchanged, and the planner prompt teaches the `Excludes:` line. An optional `Tier` column is carried. LLR-069 and TC-069 were re-attested in the lane (act seq 32, MEANING, verdict `002-ADJUDICATE-2a64d0b.md`); IF-060, IF-152, IF-153, IF-161 and IF-242 were amended. Codex 6.1 Sol: round 1 two MAJOR and one MINOR, round 2 one MINOR, all fixed. Decisions: `docs/decisions/wi-803.toml`.

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-plan-gate (ch.3 §4.5, §6). `plan_coverage`
today reports coverage gaps as payload, never findings. This row makes it a gate:
a `SINGLE` plan's clauses are the item's Done-when items (`D#`, from
`kitlib.done_when`) plus open review findings (`F#`) on a replan; a `DUAL` plan's
are its goal's `C#` clauses. A clause is covered by a row or named under
`Excludes: <clause> — <reason>`; an unexplained gap fails. For `SINGLE` the gate
also diffs the item's SRs and their TCs. An optional `Tier` column is allowed. The
drafters, the plan-critic and `BUILD` all read this gate. It has no `needs`.

## Done-when

- A SINGLE plan missing a Done-when item exits 1 naming it.
- An excluded clause with a reason passes.
- The SR/TC diff names an uncovered SR and an unnamed TC.
- Existing DUAL fixtures stay byte-identical.
- Each spine row the README matrix gives this row (LLR-069, TC-069, IF-057,
  IF-060; IF-242, where `plan_coverage` joins `kitlib.done_when`'s requestors) is
  amended and passes adjudication of that row, on whichever adjudication path is the
  one path when this row lands.
- The row's test bar: its affected modules' tests plus the smoke tier at `-n 2`; no
  extra bar is named.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit, for the planner grammar
  (`Excludes:`, `D#`/`F#` clauses, the `Tier` column).
