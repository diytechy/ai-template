+++
id = "WI-422"
title = "Measured dead-symbol sweep across project-trajectory/scripts: nothing in the kit catches an ORPHANED symbol. The module-size ratchet catches GROWTH (a module that gets bigger must argue for it), test_complexity_ratchet catches a function getting harder, and check_dupes catches a block getting copied - but a helper whose last caller left is invisible to all three, because deleting the caller made the module SMALLER, which every ratchet reads as an improvement. The 2026-08-08 mechanized-loop program retired several call paths (the gate-policy enum's four re-interpretation tables, the handback-into-queued shape, the three prompt string constants), so this sweep runs at a moment there is likely real residue. METHOD, and it must be MEASURED rather than eyeballed: take gen_arch_map.py's symbol inventory as the candidate set, grep every candidate across scripts/ + tests/ + the templates, and classify each zero-hit symbol as (a) genuinely dead - delete it, (b) a PUBLIC seam a downstream repo may call, in which case it is not dead and its docstring should say who calls it, or (c) reached dynamically (a getattr, a CLI subcommand table, a re-export). Class (b) is the reason this is a judgement and not a script: the kit's scripts are copied INTO other repos, so an unused-here symbol may be someone else's entry point. Deliver the classified inventory in the spec's Deliverable, not just the deletions. EXPLICITLY NOT a broad refactor: WI-390 forbids being built as a dead-code sweep and this row does not license one either - delete what is provably unreachable, record what is not, and stop."
workstream = "scripts"
specref = "docs/plan-2026-08-08-mechanized-loop.md"
buildtier = "medium"
safety_class = "ordinary"
+++

## Context

Plan §9's first cleanup finding, verified when the plan was written: there is no
existing WI for unused functions. The queued set at that time was WI-000
(exemplar), 390, 413, 415, 416, 417, 418, and WI-390 *explicitly forbids* being
built as a dead-code sweep.

Why it is worth doing NOW rather than whenever: the SN-028..032 program
deliberately retired several call paths in one pass. A sweep is cheapest right
after a retirement and least useful long after one, because that is when the
residue is both largest and still explicable — the person reading a zero-hit
symbol can still tell whether it died last week or was always a public seam.

The classification is the deliverable. A list of deletions with no record of
what was KEPT and why leaves the next sweep to re-derive the same judgements
from scratch.

**2026-08-11 (WI-426, repo-lock D-7).** This row's title lists three ratchets
that catch adjacent failures and argues a dead symbol slips past all of them.
One of the three is gone: the duplication census (`check_dupes.py`) was torn
down by owner ruling, along with its census file and the spine chain
`SR-039 → LLR-036 → TC-039`. **The row's argument is unaffected and arguably
stronger** — the premise was that no existing check sees an orphaned symbol, and
the census was named only as one of the three that does not. Read the title's
third clause as history. The two live ratchets (the module-size ratchet,
`test_complexity_ratchet`) still bound growth and complexity, and
`gen_arch_map.py`'s symbol inventory — the candidate set this row's METHOD
starts from — is untouched by the teardown.
