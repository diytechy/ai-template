+++
id = "WI-459"
title = "Crossing ownership, pulled forward out of sitting 3 (decision 8): answer for each of B-01/02/04/05/06/07 which SRs and IFs realize it and who owns each gap - now that the deferral's first condition is MET (Boundary-Refs populated on all 64 rows). The measured answer is a FINDING, not a formality: B-05 carries 55 of 70 references (79%) while B-06 and B-07 carry one each, and FOUR of six crossings (B-01, B-02, B-06, B-07) are realized by no interface row at all. Decide whether B-05 is under-decomposed or the imbalance is real - the registry does not distinguish those readings today, and the difference decides whether the re-tier is finished."
specref = "docs/plans/2026-08-15-retier-completion.md#5-relationship-to-sitting-3--no-conflict-one-pull-forward"
workstream = "process"
sr_refs = ["SR-137", "SR-139"]
needs = ["WI-458"]
buildtier = "strong"
safety_class = "adjudication"
priority = 2
+++

## Context

Sitting-3 ledger decision 8 was ruled **DEFERRED** (`2026-08-14d`), re-landing
by name *"after slice 2 populates `Boundary-Refs` + the D-3 re-key."* It asks
verbatim: *"for each of B-01/02/04/05/06/07, which SRs and IFs realize it, and
who owns closing each gap."*

- **Condition 1 is MET** — `Boundary-Refs` is populated on all 64 SR rows
  (0 uncovered), which is exactly the state the deferral named.
- **Condition 2 is NOT** — the IF tie-back re-key is D-3's, still unexecuted on
  the `wi455-architecture-retirement` lane. That is why this row is scoped to
  the **SR side plus the measurement**, and hands the IF side to D-3 rather
  than racing it.

**The owner expected decision 8 might "effectively dissolve in the full
re-tier," and recorded it so it would re-land either way. It has not
dissolved.** Measured on merged trunk:

| Crossing | SRs referencing it | Interfaces realizing it |
|---|---|---|
| B-01 | 5 | **0** |
| B-02 | 2 | **0** |
| **B-05** | **55** | 7 |
| B-04 | 6 | 1 |
| B-06 | **1** | **0** |
| B-07 | **1** | **0** |

## Why this is pulled OUT of sitting 3 rather than left in it

This is a **tiering and grouping** question — the re-tier's own stated purpose —
not a vocabulary or ratification question, which is what the rest of sitting 3
is (decisions 5/6/7 are the D-9 + D12 status program, ruled to run as one
sequence with the ratification wave). Leaving it there files the sharpest
re-tier finding under a sitting about status words.

**Pulling it forward REMOVES work from sitting 3; it adds none.** Nothing here
flips a Status, closes an enum, or touches the ratification wave.

## The question to rule, and it is genuinely open both ways

A partition in which one cell holds four fifths of the population is not
classifying — it is a default with five exceptions. Two readings, and the
registry does not distinguish them:

- **B-05 is under-decomposed.** Supporting evidence: it already required a
  *sixth* bucket, minted at ruling `2026-08-14c` (the "package-wide property"
  class), to absorb four rows that fit none of its five. A bucket set that
  needed widening once may need it again.
- **The frame is right and the imbalance is real.** This repo's product
  genuinely is one package crossing one boundary; the other five crossings are
  thin because the repo is thin there, and forcing balance would manufacture
  structure.

Raised for the owner as `OI-29`.

## Done-when

- The six-row table above is regenerated at execution time (do not trust these
  figures — re-derive) and recorded with each crossing's SR list and IF list.
- The B-05 question is ruled: under-decomposed (with the decomposition) or real
  (with the reason stated, so a later reader does not re-open it).
- Each of B-01, B-02, B-06 and B-07 has a named owner for its missing
  realization, or a recorded statement that no interface should realize it.
- The IF-side re-key stays D-3's; this row states what D-3 must produce, and
  does not execute it.
- Sitting 3's §0.3 ledger row 8 is marked closed-by-this-row, so the sitting
  does not carry a decision that has already been made.
