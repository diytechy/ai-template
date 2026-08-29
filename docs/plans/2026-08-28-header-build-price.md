# WI-525 — the price of the component-side contract header

**Filed:** 2026-08-28, under `OI-65` ruled (b'). This document prices the build;
it rules nothing. The go/no-go is `OI-66`.

The price is taken **by analogue, not by estimate**. `WI-512` built the same
shape of mechanism — thin the cells to their crossing, harvest the removed
content into a committed generated reference, freshness-gate it, ship the
convention to adopters — and its cost is a measured diff, not a judgement.

---

## The finding that changes the picture

Both `OI-63` and `OI-65` recorded that option (b)'s precondition was unbuilt,
and cited `WI-512` as the precedent that *worked because* a committed,
freshness-gated `docs/cli-reference.md` already existed.

**That is not what happened.** `docs/cli-reference.md` was created **by WI-512
itself**, in the same commit:

```
$ git log --oneline --diff-filter=A -- docs/cli-reference.md
c54ddd10 WI-512: thin the 27 CLI contracts to their crossing, and give the
         cell two checks it never had
```

fig: `git log --oneline --diff-filter=A -- docs/cli-reference.md` @ c54ddd10

So the precedent did not depend on a pre-existing artifact — it built its
reference from nothing, as part of one work item. The "unbuilt precondition"
that argued for pricing before committing is real in the sense that the
artifact does not exist, but it is **not** an unbounded prerequisite: the
analogue tells us what building one costs.

---

## The measured analogue

`WI-512` in full: **+2,024 / −156 across 36 files.**

fig: `git show --numstat --format="" c54ddd10 | awk '{ins+=$1; del+=$2} END {...}'` @ c54ddd10

The mechanism-only subset — what OI-66's five priced items correspond to:

| Item | WI-512's cost |
|---|---|
| The generated reference itself | `docs/cli-reference.md` **+566** |
| Its generator | `gen_arch_map.py` **+189** |
| Its freshness gate | `check.py` +33, `trunk_step.py` +42, `docs/stack.ini` +4 |
| Registry-side reader/checks | `trace.py` **+239** |
| Kit surfaces shipped to adopters | `PROCESS.md` 13, `interfaces.template.toml` +26, `INTERFACES.template.md` 3, `RESYNC_PACK.md` +54, `ADOPTING.md` +9, `EXAMPLE.md` 6 |
| Tests | `test_trace_rules.py` +181, `test_gen_arch_map.py` +122, `test_generated_freshness_wiring.py` +19, `test_check_lane.py` +7, two ratchets +5 |
| The cells themselves (27 rows) | `interfaces.toml` +114 |

---

## Where the header build differs from the analogue, and by how much

Three deltas, each in the direction of **more** work, and one in the direction
of less.

1. **Scale of the cell pass: 71 rows against 27.** `WI-512` thinned 27 CLI rows;
   the remainder sits on 71 of 108. That is the one item that scales roughly
   linearly — call it **2.6x** on the `interfaces.toml` line only (+114 → ~+300).
   It does not scale the generator or the gate, which are per-mechanism.

2. **The 21 modules with no anchor.** 57 of 78 modules carry a `Contracts:`
   header line; 21 do not, and each needs one authored before it can hold a
   contract body. This has no analogue in `WI-512` (the CLI surface was
   harvested from `argparse`, which every script already had).

   fig: `find project-trajectory/scripts -name '*.py' | wc -l` = 78;
   `grep -rn '^\s*Contracts: IF-' --include='*.py' | wc -l` = 57 @ 2026-08-28

3. **The harvester is broken and the fix is a precondition, not a nicety.**
   `gen_arch_map.module_contracts` returns `['IF-080']` for `handback.py`,
   whose docstring says *"No `Contracts:` line, deliberately"*. The guard is
   documented as "restricted to lines carrying the word `Contracts`, so an IF id
   merely mentioned in prose is not mistaken for a declaration" — and a
   **negated** declaration carries that word, so the guard passes it through.
   Small in lines; load-bearing, because the header mechanism reads this
   function. Fixing it also needs a decision the bug exposes: whether a module
   may declare *"no contracts, deliberately"* as a first-class state.

4. **Less work than the analogue in one place:** the `Contracts:` anchor,
   its grammar and its both-directions citation check already exist —
   `WI-512` built those. This build extends a body onto an anchor that is
   already there on 57 modules, rather than inventing the anchor.

---

## The price

**Roughly the size of `WI-512`: order 2,000 changed lines across ~35 files,
plus the two items the analogue does not cover.** Stated as a range rather than
a point, because (2) and (3) are authored work rather than mechanism:

- **Mechanism** (generator, gate, reference, registry reader, tests): ~1,200
  lines, closely tracking `WI-512`'s equivalents. Confident.
- **The cell pass** (71 rows): ~300 lines of registry edit. Confident.
- **The 21 anchors**: authored per module, no analogue. Least certain item.
- **The harvester fix**: small in lines, but carries the "deliberately none"
  design question above.
- **Adopter migration**: ~100 lines across five kit files plus a `RESYNC_PACK`
  entry, tracking `WI-512` closely. Confident.

**It is one work item of the size this repo has absorbed before, not a
program.** That is the honest headline, and it is a different answer from the
one both prior rulings assumed.

---

## What this does not price

The **authoring judgement** inside the cell pass. `WI-512` harvested the CLI
surface mechanically from `argparse`; a contract body is written by a person
reading the code. 71 rows of that is the real cost and it is not a line count.
The analogue is silent here, and no honest number is available without doing a
sample — a tranche of five rows would produce one.
