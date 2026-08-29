+++
id = "WI-525"
title = "Price the component-side contract header: the generated reference, its gate, the harvester fix, the missing anchors and the adopter migration (OI-65 ruled (b'))"
specref = ""
workstream = "architecture"
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

The price, taken **by measured analogue rather than by estimate**, and filed on
`OI-66` so the go/no-go is ruled against numbers. Record:
[../../../plans/2026-08-28-header-build-price.md](../../../plans/2026-08-28-header-build-price.md).
No interface cell moved and no header convention shipped under this row.

**The finding that changes the question.** Both `OI-63` and `OI-65` recorded that
option (b)'s precondition was unbuilt, and cited `WI-512` as the precedent that
worked *because* a committed, freshness-gated `docs/cli-reference.md` already
existed. That is not what happened —
`git log --diff-filter=A -- docs/cli-reference.md` returns `c54ddd10`, WI-512's
own commit. **The precedent built its reference from nothing, inside one work
item.** So the missing artifact is a cost, not an unbounded prerequisite, and
the argument that carried two rulings does not survive the record.

**The analogue.** `WI-512` cost **+2,024 / −156 across 36 files**: the reference
566, its generator 189, its freshness gate 79 across `check.py`/`trunk_step.py`/
`docs/stack.ini`, registry-side reader and checks 239, tests 334, adopter-facing
kit surfaces about 110, and the 27 cells themselves 114.

**Four deltas against it**, three upward and one down: the cell pass is 71 rows
against 27 (the only item that scales, ~2.6x on the registry line); 21 of 78
modules carry no `Contracts:` anchor and each needs one authored; the harvester
is broken and fixing it is a precondition; and it is *less* work in one place,
because the anchor, its grammar and its citation check already exist — WI-512
built those.

**The price: order 2,000 changed lines across about 35 files. One work item of a
size this repo has absorbed before, not a program.**

**What is not priced, and is said so on the row:** the authoring judgement inside
the cell pass. WI-512 harvested the CLI surface mechanically from `argparse`; a
contract body is written by a person reading the code, and 71 rows of that is not
a line count. A five-row sample is the only honest way to get it, and `OI-66`
carries that as option (d).

**A defect found while pricing, recorded not fixed:**
`gen_arch_map.module_contracts` returns `['IF-080']` for `handback.py`, whose
docstring reads *"No `Contracts:` line, deliberately"*. The guard admits any line
carrying the word `Contracts`, and a negated declaration carries it. Fixing it
raises the question the bug exposes — whether a module may declare "no contracts,
deliberately" as a first-class state — so it is `OI-66`'s required guard rather
than a silent repair here.

## Context

`OI-65` part 1, ruled (b') on 2026-08-28: the header is committed to in
principle, and nothing moves until the build is priced and the owner accepts the
price. The precondition had stayed unbuilt through two rulings, which is why the
price was taken before any cell moved rather than after.

## Done when

- [x] All five items priced with their file lists, not estimated as a class.
- [x] The numbers land on `OI-66`.
- [x] No interface cell moved; no header convention shipped.
- [x] Commit bar green.
