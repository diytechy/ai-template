<!-- The brief both item 11 fitness analysts received, identical except that {WT} was each one's own detached worktree at eae8e1cbe and {NAME} was astra or fable. The two context files it names are the handoff and the plan README as of 2026-10-12, before revision 14. -->

# Brief: will item 11 (LLRs carried by interfaces) hold, or cause rework again?

You are an independent analyst for the ai-template repo. Another model is running
this same brief separately; you will not see its answer and it will not see yours.

## Where things are

- **Repository (read-only):** `{WT}`, a detached worktree at commit `eae8e1cbe`.
  Read anything there except `OWNER_SCRATCHPAD.md`, which you must never open.
  Modify nothing in it: no edits, no commits, no generated files.
- **Two files newer than that commit** are in `C:/Projects/ai-template.wt/review-tmp/2026-10-12-item11-fit/context/`:
  - `item-11-llr-interface-check-handoff.md`: **the query you are answering.** Read it
    first and in full. Its "Method" and "Deliverable" sections are your task.
  - `README.md`: the review-churn plan at its newest revision. Item 11 ("What points
    where", section 11) is the proposal under test; read all of it, including the
    "Owner rulings" section near the top (items 1–10 are ruled) and the bullet
    "Will the interface carry the requirement, or only reach it?". Where this
    README differs from the worktree's copy, this one governs.
- **Write only** inside `C:/Projects/ai-template.wt/review-tmp/2026-10-12-item11-fit/`
  (scratch scripts are fine there). Python 3.11 with `tomllib`: `{WT}/.venv/Scripts/python.exe`,
  or `python` on PATH.

## The owner's lens (judge everything against this)

The owner wants **long-term design sustainability**. Concretely:

1. **Keep the reference structure that lets behavioural expectations stay (at least
   partly) divorced from implementation.** A requirement should survive a refactor of
   the code that realizes it; code and tests should point up, so moving code never
   reopens a requirement row.
2. **Do not over-complicate the spine or its connection points.** Every authored link
   (a cell, a tag, a citation) is something a human or an agent must keep true
   forever. A link earns its place only if the orientation it gives a reader (human
   or LLM: "what problem does this solve, within the larger vision?") or the check it
   enables is worth more than the maintenance it costs. Count that cost explicitly.
   Prefer derived over authored, and one home per relation.

## Your task

Carry out the handoff's Method and produce its Deliverable, with these additions.

1. **Treat the handoff itself as a set of claims.** It may be wrong in its numbers,
   in its three fitness tests, or in its framing. If a test is mis-stated (for
   example, if "the user-observable outcome" is the wrong standard for an LLR whose
   interface is a component-level seam rather than the system boundary), say so,
   propose the corrected test, and classify with the corrected one, reporting both
   where they differ.
2. **Counts with a reproducible method.** For the "55 of 302 LLRs in modules that own
   no IF" claim, state your exact matching rule (path normalization, how multi-module
   cells count) and the result. Do the same for every count you report.
3. **Per-LLR classification file.** Write
   `C:/Projects/ai-template.wt/review-tmp/2026-10-12-item11-fit/{NAME}-classes.csv`
   with one row per LLR (all 302) and columns:
   `llr, component, fitness (fit | reword | reframe-or-retire), failed_tests
   (e.g. "1;3" or empty), interface_class (existing-if | boundary-artifact |
   kernel-or-internal-edge | no-observable-seam), candidate_if (an IF id, or a short
   proposed name, or empty), basis (hand | script), note (short)`.
   Mark at least 30 rows `hand`, spread across components, and read the evidence
   tests for those (do not classify a TC's level from its `level` cell alone).
4. **Alternatives, not just a verdict.** Compare at least these designs on (a)
   one-time migration cost, (b) ongoing maintenance: the number of authored links
   that must be kept true, and what breaks them, (c) orientation value to a reader,
   (d) how well each keeps behaviour divorced from implementation:
   - **A. Item 11 as proposed:** code → IF only (`Implements:` retires), IF → LLR/SR
     authored, every LLR carried by an interface, files declare their component.
   - **B. Reword first, then attach:** A, gated on each LLR passing the (corrected)
     fitness tests before it moves.
   - **C. Boundary-artifact variant:** LLRs whose behaviour is only observable in a
     delivered artifact (the dashboard HTML, a generated registry, a CLI's output)
     attach to one IF for that artifact; no call seams minted for internals
     (OI-48).
   - **D. Minimal change:** keep code → LLR (`Implements:`) as the trace, add IF → LLR
     only where an IF genuinely carries the behaviour, and do not require every LLR
     to have an interface.
   - Any variant of your own that you judge better.
5. **Recommendation and owner calls.** Lead the report with your answer: the counts,
   whether item 11 reduces rework as designed, the variant you recommend and why, and
   the owner calls that remain open. Ground every claim in a file path, a row id or a
   command you ran. Flag design smells you notice as separate findings; do not fix
   them.

## Constraints

- Requirements never reference code (owner ruling 2026-10-11; README ruling 5): any
  LLR rewording you propose is in capability voice, with no symbols, markup or file
  names (shipped boundary artifacts may be named at LLR and TC only).
- Read OI-48 in `docs/requirements/open-items.toml` before recommending any
  `call`-channel seam.
- Read-only everywhere except the review root. Do not start a migration.

## Output

Write the report to
`C:/Projects/ai-template.wt/review-tmp/2026-10-12-item11-fit/{NAME}-report.md`
(aim for 150–350 lines; lead with the answer), plus the CSV above.
