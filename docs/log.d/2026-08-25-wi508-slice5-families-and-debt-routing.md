## 2026-08-25 — WI-508 slice 5: the dispersion survey completes, one more row is earned, and the inherited debt gets an owner that outlives this program

**Summary.** The three items the alignment pass left open are discharged. All
**eighteen** dispersion families now carry a disposition — one consolidate,
twelve keep, one partly upheld by a row already filed. The consolidate is the
one both blind derivations predicted from the requirements alone, and driving it
found the divergence is worse than the requirement records. The module-size
ratchet's debt pointer **moved off this row onto a filed successor**, so this
program's eventual close has nothing to re-point; M-06's four test monoliths
land there too, explicitly unbound from a ride-along rule that has now failed to
deliver across two programs. After this, **everything left on `WI-508` is
owner-owed** and the row says so precisely.

Deferred open items: OI-64 (unchanged — raised at slice 3, still awaiting the
owner's ruling; nothing here re-raises or widens it).

### The fourteen remaining families

Eighteen dispersion families exist, grouped by the (A-module, B-module) pair both
derivations agreed on; four were adjudicated at slice 3. The test is unchanged
and it is the objective used as an instrument: **is there a shared stage, or is
the behaviour re-implemented?**

**One consolidate, twelve keep, one partly upheld.** Every KEEP declares its
grounding — a mechanical shared-stage test (an import edge, or no second
implementation found) or a read rationale — because a survey that reports both
in one voice sounds more certain than it is.

Three keeps rest on a read, and each is a derived-map merge REFUSED with cause:

- **Launchers.** Both maps quoted `SR-046`'s "the platform launchers delegate to
  the one selector rather than carrying commands of their own". But `SR-160`'s
  own text records the split as deliberate — it "spans two audiences … and parts
  along that line" — and the genuinely shared piece, the interpreter probe, would
  have to become a **shell library** to be shared between a git hook and a root
  launcher. The kit ships none, deliberately: a hook must work standing on
  nothing but the repository.
- **Converters.** Both maps merged them to remove "a second cell-exact
  round-trip verifier". Both verifiers exist — and **both migrations have already
  run**: the spine is TOML, the work registry is spec files. These are one-shot
  tools retained as the proof the conversion was lossless, which is their stated
  purpose. A shared verifier would be built for no future caller.
- **Scaffold + manifest.** The shared signal both maps clustered on is the
  inventory, and it has exactly one home. The other two live modules are a
  shipped shell template and a package `__init__` — not second manifest walkers.

### The one that earned a row — and it is worse than the requirement records

**The credential class vocabulary.** Both derivations merged the hook scanner
with the transcript redactor, and both cited `SR-176`'s own rationale as evidence
the duplicated class list had *already* diverged in the field. Driven against
five samples, **four disagree, in both directions**:

| sample | hook scanner | transcript redactor |
| --- | --- | --- |
| PEM private key block | catch | **MISS** |
| `Bearer <30 chars>` | **MISS** | catch |
| `ghp_` + 36 chars | catch | catch |
| `ghp_` + 24 chars | **MISS** | catch |
| `sk-` + 22 chars | **MISS** | catch |

fig: cmd="load check_privacy and agent_common by path, then evaluate KEY_RE + TOKEN_RES against _SECRET_RES over the five samples in the table" rev=754870db

**The first row inverts the protection.** A PEM private-key block is refused at
the commit hook and passes **unredacted into a committed transcript** — the
durable artifact less protected than the ephemeral one, which is the exact hazard
`SR-176` exists to prevent with a different subject. Filed as **`WI-520`**,
`priority = 1`, `safety_class = high-risk`.

**The original rationale was read first and it made the proposal SMALLER.**
`redact_secrets` is documented as "deliberately imperfect — unknown token shapes
pass through, and the raw unredacted stream stays in gitignored `out/run-logs/`
for debugging". That decision STANDS; the row does not make redaction
exhaustive. What the docstring does not license is the measured gap: a PEM key is
not an unknown shape, it is a compiled pattern in a sibling module of the same
package. The row asks for one home for the class vocabulary and a per-class
decision on each side — and it names the asymmetry that should survive, since
over-redacting a transcript costs a reader nothing while a false commit refusal
costs a contributor a lot.

### The debt pointer moved, and the reasoning is now in the ratchet itself

`WI-521` is filed and **every live pointer now names it.** The two test files
carried **eight** mentions of `WI-508` before this slice — the ratchet's module
docstring, its decomposition instruction, its sensor paragraph, its `BASELINE`
header comment and its growth failure message, plus the deferred-import window
and the cycle ratchet in `tests/test_import_layers.py`. Afterwards **three
remain, and all three are the docstring's HISTORY of the hand-off**, kept
deliberately on the same rule that keeps the dated per-entry bump notes pointing
where they pointed: rewriting a record of what was true then would falsify it.

fig: cmd="grep -rn 'WI-508' tests/ --include=*.py | wc -l ; grep -rn 'WI-521' tests/ --include=*.py | wc -l" rev=754870db-dirty

Two grounds, recorded in the ratchet's own docstring because that is where its
rule lives:

1. **A close-time re-point is a promise; a filed row is a fact.** It has been
   honoured exactly once — deliberately, with the defect named — and leaning on
   it a second time makes the sensor's honesty depend on a future session
   remembering.
2. **`WI-508` was never scoped to this axis, and the ratchet already says the
   same about its predecessor in the same words.** `WI-508` is a CONSOLIDATION
   program; this ratchet measures module SIZE, which is decomposition. It held
   the pointer for being the live architectural program, not for matching the
   axis it was named on.

**`WI-508`'s close now has nothing to re-point** — the dead-owner defect made
unreachable rather than deferred a third time. And `WI-521` inherits the rule:
if it closes, the pointer moves in the same commit.

### M-06 lands, and the rule that stranded it does not survive the move

`tests/test_integrate.py` 3,520 · `tests/test_trace.py` 2,099 ·
`tests/test_trajectory_arch.py` 1,927 · `tests/test_agent_loop.py` 1,640.

`WI-483`'s item 4 held that a test split RIDES ALONG with a subsystem
decomposition and that a standalone split was out of scope. It was honoured
across all seven of that program's slices and delivered nothing — no slice needed
one — and `WI-508` then filed no decomposition at all. **A rule that has failed
to deliver across two programs is a rider with no vehicle**, so `WI-521` states
that a standalone split is in scope for it, still taken by stable behaviour
boundary rather than by line count. That rule was `WI-483`'s own SCOPE decision
rather than a standing ruling, which is what makes this a successor row's call
and not an owner question.

**The sensor gap rides with them, carried but NOT executed.** No armed sensor
watches the test tree, which is why three of the four grew 5–36% unnoticed.
Extending the census is deliberately not proposed: that file banks an unruled
owner question about whether the line-count axis survives at all, and extending a
disputed axis to a second tree doubles whatever is wrong with it.

### The 48 fusion pairs are routed, not re-derived

They attach to `WI-521` as the requirements-side evidence the size debt never
had: which modules a reader must hold too much in mind to read (`agent_loop` 14
pairs, `check_trajectory` 13, `agent_common` 10, `bootstrap` 5), reached
independently of line counts. A size ratchet alone can be answered with "it is
big because it does a lot"; this says which obligations two independent
derivations put in different modules.

### `WI-508` after this slice: owner-owed, and nothing else

The program has **no agent-executable work left**. What remains is exactly two
items, both the owner's: `OI-64`'s ruling, and the blessing of the four `Drafted`
rows in `docs/ratify/CURRENT.md`. Everything else is landed or filed as its own
claimable row — `WI-519`, `WI-520`, `WI-521`.

**The row stays ACTIVE, deliberately neither closed nor parked.** Closing it
would strand `OI-64`'s ruling with no row to return to; parking it silently is
what a tracked pause file is for and there is none. Its Context now states
exactly that, so the next reader does not have to infer it.

### Gates

```
python -m pytest -q tests/test_module_size_ratchet.py tests/test_import_layers.py
                                            -> 10 passed in 2.57s   [the two touched modules]
python -m pytest -q -n auto -m smoke        -> 1327 passed, 5 skipped in 27.72s
python scripts/check_smoke_budget.py --mode enforce --elapsed 28.2
                                            -> 28.2s vs 60s budget -> within
python project-trajectory/scripts/check_docs.py --root . --stale
                                            -> OK, 1092 docs, 1435 links, 0 broken
python project-trajectory/scripts/check_trajectory.py --root . --strict
                                            -> clean (518 WIs, 491 done, graph acyclic)
python project-trajectory/scripts/trace.py --root . --strict
                                            -> integrity=0, orphans=2, drafts=4
the six generated-artifact --check gates    -> all fresh
```
fig: cmd="each command as written above, run in this order on this tree" rev=754870db-dirty

**The budget was evaluated on ONE measured run, via `--elapsed`, rather than by
re-running the tier** — deliberate, and the reason is a box condition worth
recording: another repository's `agent_loop.py` is running two worktrees on this
machine throughout this sitting (52% CPU with nothing of this session's own in
flight). Timing the same tier twice under a moving external load measures the
box, not the tier. The single reading came in at **28.2 s against a 60 s
budget**, consistent with this tree's other idle readings (22.8 s, 25.9 s) and
nowhere near the ceiling, so nothing here needed a second opinion — and **no
budget was touched in either direction.**

**Executable surface touched, and what it is.** Two test modules changed —
docstring prose, comment text and the string literals inside two assert
messages. **No assertion, threshold, baseline or census changed**, which the
10-passed run above holds directly. The full unfiltered suite is therefore not
claimed: nothing that any other test reads was altered, and the two files that
were are run in full above.

**Ratchets: none re-stamped, in either direction.** The module-size census
covers `SCRIPTS` only, so editing a test file does not touch its baseline — and
that is the sensor gap this slice records rather than closes.

### The floor caught this sitting's own commit, and that is the finding confirmed live

The first attempt to commit `WI-520`'s spec was **refused by the secrets floor**:
the spec quotes a PEM private-key header as the sample its table is about, and
`check_privacy` did exactly what the row says it does — caught it in the staged
diff and blocked the commit.

That is not an inconvenience, it is the measurement re-run at the hook on real
content. The scanner catches the class; the redactor does not; and the sample
that proves it could not be committed until it was marked. It is exempted with
the sanctioned per-line affordance the checker's own message names — a
`privacy-ok` marker with the reason beside it, self-documenting at the site,
which is what that mechanism exists for: a documented example of a pattern
class, not a key. The opt-out file was NOT touched and no pattern was weakened.

**Three new advisories, expected and correct.** `check_trajectory --strict`
reports that `WI-519`, `WI-520` and `WI-521` pairwise share one spec of record.
They do: all three were filed by the same alignment pass and cite it. That is
the same advisory class `WI-484`/`WI-508` already carry for sharing the
open-items registry, it is a warn and never the exit code, and the alternative —
three near-identical plan documents so each row could cite its own — is the
restatement this program exists to reduce.
