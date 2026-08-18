# 2026-08-17 desk — internal adversarial round (Opus)

**Date:** 2026-08-17 · **Round:** owner-directed adversarial, over **all** of the
day's changes — the span `47234903^..HEAD` (28 commits, `47234903` … `6fe5e5bb`)
and log entries `2026-08-17c` through `2026-08-17u`.
**Reviewer:** Claude Opus 5, in-session, with three hostile sub-reviewers
(same model) fanned out over targets 2–6; every sub-reviewer finding was
**re-verified by the author against the live repo** before it was allowed into
this document, and the re-verification evidence is recorded per row.
**Scope reviewed:** the eight unification commits (`53679b11` … `6fe5e5bb`) and
their live surfaces; `f1d9c57c` (the 50-cell acceptance-form pass) and
`docs/plans/2026-08-17-acceptance-form-ledger.md`; `d28e1ccb` (attestation as a
cell claim); `0c890716` (watermark seeding); `8f97e866` (the five owner cells);
`43bf51a7` (the TC pins); the docs/desk sweeps `166b406d`/`cbeb695a`/`db9ca307`/
`dda5cc0c`/`ba23fe3d`; plus live `docs/requirements/*.toml`, `docs/test/*.toml`,
`project-trajectory/scripts/`, `tests/`, the shipped templates and `RESYNC_PACK.md`.
**Verdict:** CHANGES-REQUESTED · **18 findings — 13 CONFIRMED, 2
CONFIRMED-IN-PART, 3 RELAYED (sub-reviewer evidence, author did not
independently re-derive)** — plus **2 staleness hypotheses REFUTED** and
recorded under CLEAN. Per the standing pattern **nothing is applied**: every
finding is recorded for the owner's ruling. This round's only writes are this
document and the log entry.

The day's headline claims mostly hold, and several hold impressively — the
18/9 SN split, the 138-cell off-spine census, the SN schema census
non-vacuity, and the trap-(i) no-writer guard all reproduced exactly under
adversarial re-derivation, and the two staleness charges the round went hunting
for turned out to be false.

What this round found instead is a single **recurring class**, and it is worth
naming before the findings: *evidence offered as a measurement, produced by an
instrument that cannot see the thing it is offered as measuring*. **F3, F8, F9,
F13 and F14 are five independent instances of it in one day's work** — a
byte-identical basis line that is blind to the tier that changed most; a
byte-identical advisory set from a checker that never reads acceptance prose; a
pickaxe over a file that did not exist when the ids were cut; a cap pin that
asserts on the printed message rather than the served sleep; and a
failure-path test whose failure is planted in the last step, so the stop it
exists to prove is unreachable. **F1 is what that class costs when it lands on
a live guard.** The individual fixes are mostly cheap; the pattern is the
finding.

---

## The findings

### F1 — MAJOR · CONFIRMED · the components split moved a rung-gating fact onto an axis nothing reads

**Claim refuted** (`2026-08-17u`, `2026-08-17t` design call 3): that
`components.state` was conflating maturity with lifecycle, and that
`has-gap`/`deprecated` were *"LIFECYCLE facts folded onto maturity"* — so
splitting them out to `standing` costs nothing.

The code's own recorded rationale said the opposite, and `6f39b2ed` deleted it
without citing it. The deleted `CMP_MATURITY` entry read, verbatim:

~~~text
    # `has-gap` is an explicit statement that the partition does NOT yet hold —
    # the strongest possible DRAFTED signal, and the one place a lenient mapping
    # would let a known-broken partition report a finished architecture rung.
    "has-gap": DRAFTED,
~~~

`has-gap` was load-bearing **on the maturity axis by design**. It now lives on
`standing`, and the replacement comment concedes `standing` is *"not a
maturity"* and that **"nothing maps here"** (`derive_gate.py:644`).

**Author re-verification — measured, both worlds:**

~~~text
PRE  (810f1c01)  state=has-gap                     -> arch_incomplete: True
PRE  (810f1c01)  state=verified                    -> arch_incomplete: False
POST (HEAD)      status=Founded + standing=has-gap -> arch_incomplete: False
POST (HEAD)      status=Founded, standing=deprecated -> arch_incomplete: False
POST (HEAD)      status=Drafted                    -> arch_incomplete: True
~~~

A component carrying an explicitly recorded gap now **closes** architecture
rung 3 — precisely the outcome the deleted comment named as the failure to
avoid. (First attempt at this measurement was itself wrong — the pre-migration
predicate reads `r.get("State")`, not `"Status"`, so passing `Status` produced
a false "True" for every value through the unrecognized-reads-DRAFTED default.
The numbers above are the corrected run.)

**Latent today, not live:** all four CMP rows are `Drafted` and **zero rows
write `standing`** — so nothing is mis-reporting right now. But the axis was
created exactly so a gap could be recorded *alongside* a mature status, and
that is the combination with no reader. Owner rules: map `standing` into the
rung predicate, or record why a known-broken partition may report a finished
rung.

### F2 — MINOR · CONFIRMED · `arch_incomplete`'s docstring still teaches the retired vocabulary

`project-trajectory/scripts/derive_gate.py:754-772` still reads *"any component
at DRAFTED maturity (`planned` or `has-gap`)"* and *"this predicate reading a
newly minted `planned` CMP row"*. Both words were deleted from CMP's
vocabulary by `6f39b2ed`/`9b8370d9`. **Re-verified:** `git show 9b8370d9 --
project-trajectory/scripts/derive_gate.py` shows those docstring lines as
unchanged context — the commit re-keyed the predicate's *field* (`State` →
`Status`) two lines below and left the prose. Refutes `2026-08-17u` step 9's
*"swept the prose surfaces"* for the very function the split re-keyed.

### F3 — MAJOR · CONFIRMED-IN-PART · "no row's maturity moved, measured not asserted" is unmeasured for the CMP tier

**Claim** (`2026-08-17u`): *"The `derive_gate` basis line is BYTE-IDENTICAL to
its pre-migration value at every checkpoint"* — offered as the measurement
behind **NO ROW'S MATURITY MOVED**.

**The identity itself is true.** Re-derived independently in a worktree at
`810f1c01` versus HEAD — byte-identical, both lines:

~~~text
# basis: SN=27 SR=70 LLR=159 TC=155 drafted=68 modified=147 uncovered=0 computed=DevBar-Below ex-draft=DevBar-Below phase=5 per-phase=1=DevBar-Below;3=DevBar-Tests;4=DevBar-Below;5=DevBar-Below stage=DevStg-Boundary stage-ord=1 stage-of=8
derived gate: DevBar-Reqs
~~~

**But the instrument is blind to a quarter of the change.** Flipping **all four**
CMP rows from `planned` (DRAFTED) to `verified` (FOUNDED) — the maximum
maturity move available on that tier — leaves the basis line **byte-identical**
and the derived gate unchanged. `spine_stage` reports the *lowest* unfinished
rung, which is Boundary (`stage-ord=1`); rung 3's `arch_incomplete` never
reaches the output.

**In part, because the other leg is sound:** flipping all 123 IF + 11 EXT rows
`drafted` → `approved` **does** move the line (`stage=DevStg-Boundary
stage-ord=1` → `stage=DevStg-Reqs stage-ord=2`). So the byte-identity is real
evidence for **134 of the 138** off-spine cells and **no evidence at all** for
the 4 CMP cells — which are the only cells whose field was *structurally split*
rather than renamed, i.e. the highest-risk quarter. The second evidence leg
(*"the off-spine trace golden regenerated to zero diff"*) does not close the
gap either: `tests/golden/offspine.txt` is a 1-row synthetic scaffold fixture
and renders no CMP maturity.

### F4 — MINOR · CONFIRMED · the shipped hats template still teaches a field the same day deleted

`2026-08-17u` disclosed **one** `kind` survivor — `hats.py`'s `SCALAR_FIELDS` —
and left it deliberately. It did not disclose that two *prose* surfaces still
teach the dead field as the worked example of the `applies_when` grammar:

- `project-trajectory/registries/hats.template.toml:34` — `kind == "core"  (also !=)`
- `docs/requirements/hats.toml:38` — same line

**Re-verified:** `git log 47234903^..HEAD -- project-trajectory/registries/hats.template.toml docs/requirements/hats.toml project-trajectory/scripts/hats.py`
returns **empty** — untouched by the whole 28-commit span. The sharp edge is
downstream: `RESYNC_PACK.md`'s new entry instructs adopters to map
`kind = "core"` → `status = "Approved"` **and drop the key**, while the hats
template they scaffold alongside it documents `kind == "core"` as how you write
a condition. Refutes step 9's *"swept the prose surfaces"*.

### F5 — MAJOR · CONFIRMED · SR-159's re-home is claimed against rows that do not carry the obligation

**Claim** (`2026-08-17s` / the acceptance-form ledger): *"every stripped
binding verified or re-homed"*. The ledger's SR-159 disposition
(`docs/plans/2026-08-17-acceptance-form-ledger.md:80`) states
`TOP_VIEW_MAX -> its declared bound (bound value at LLR-049/TC-049)`.

Old cell: *"...and the `TOP_VIEW_MAX` bound of **10 items** (warn plain, error
under `--strict`)"*. New cell: *"...hold the top view to its **declared
bound**"*.

**Author re-verification** —
`grep -rn 'TOP_VIEW_MAX|bound of 10|10 items' docs/requirements/*.toml docs/test/*.toml`
returns three hits, **none containing the number 10**:

- `docs/requirements/low-level-requirements.toml:526` (LLR-049) — *"enforces TOP_VIEW_MAX with nesting, opt-out, and vacuity rules"* — symbol, no value
- `docs/requirements/low-level-requirements.toml:857` — same shape
- `docs/test/test-cases.toml:521` (TC-049) — *"Run TOP_VIEW_MAX, containment, nesting, opt-out, and vacuity cases"* — symbol, no value

The only statement of the value in the repo is
`project-trajectory/scripts/check_trajectory.py:179: TOP_VIEW_MAX = 10`. The
numeric threshold was stated in the spine before this commit and is stated
nowhere in the spine after it, while the ledger asserts by name that it was
re-homed. (Sub-reviewer additionally found the second half — the `[checks]
components_check` opt-out — has no design-tier home either, LLR-042 carrying
only `interfaces_check`; recorded but the `10` is the decisive half.)

### F6 — MAJOR · CONFIRMED · the SR-040 phantom symbol is live on a shipped adopter-facing surface

**Claim** (`2026-08-17s`): the removed `AGENT_STATUS_WARN_BYTES` occurs nowhere
in code or tests, so nothing live was dropped; the residual divergence is
scoped to `LLR-037`.

**Author re-verification** —
`grep -rn 'AGENT_STATUS_WARN_BYTES' project-trajectory/ docs/requirements/`
returns exactly one live hit, and it is not `LLR-037`:

~~~text
project-trajectory/PROCESS_OPTIONS.md:802:(`AGENT_STATUS_WARN_BYTES`, default 8192, `0` silences) — every session
~~~

That is a **shipped, scaffolded, adopter-facing process doc** documenting the
variable as real. The sitting is being handed a divergence scoped to one
registry row while the same phantom is copied into every downstream repo the
kit scaffolds. Sub-reviewer's companion point, recorded: the strip removed the
*falsifier* (a named env var you can grep for and fail to find) while keeping
the obligation in artifact-free prose, and the re-voicing's stated trace home
`LLR-037` names a retired function (`agent_loop.py:499` — *"status_size_warning
retired with the serial driver, WI-210"*).

### F7 — MINOR · CONFIRMED · SR-167's DevBar-Release wiring observable is now stated at no spine row

Old SR-167 acceptance named *"the harness wiring at DevBar-Release via
`test_harness_runs_perf_at_g3`"*. New cell: *"proven end to end against a
bootstrapped scaffold."* **Re-verified:**
`grep -rn 'test_harness_runs_perf_at_g3' docs/requirements/ docs/test/` returns
**nothing**, while `tests/test_check_perf.py:162` defines it. The LLR-014
re-home genuinely landed for the other bindings but says nothing about which
bar the step runs at, and the ledger's SR-167 disposition does not acknowledge
the drop. Capped at MINOR: SR-006 generically covers *"the harness runs that
bar's declared steps"* and `docs/stack.ini` declares the step's `gates`, so the
obligation is reachable by composition — but it is no longer asserted.

### F8 — MAJOR · CONFIRMED · the acceptance-form pass's "byte-identical advisories" evidence is vacuous

**Claim** (`f1d9c57c`): *"advisories 112 → 112, byte-identical"*, offered as
evidence that rewriting 50 acceptance cells changed no obligation.

**The identity is true — and worthless.** Author re-verification, in throwaway
worktrees at `f1d9c57c^` and `f1d9c57c`: the generated `docs/test/report.md` is
byte-identical across the commit (`diff` → **0 changed lines**), summary line
identical both sides (`form-findings=1 paraphrase-advisories=5`).

Then the vacuity test. Replacing SR-001's **entire** `acceptance_criteria` cell
with the string `it works.` and re-running `trace.py --root . --strict`:

~~~text
mutations applied: 1
Traceability: SN=27 SR=70 LLR=159 TC=155 orphans=0 integrity=0 drafts=68 components=4 component-findings=0 interfaces=123 interface-findings=0 form-findings=1 paraphrase-advisories=5. Report -> docs/test/report.md
REPORT IDENTICAL -> blind to acceptance prose
~~~

No finding, no advisory, no report delta. **The kit's own checkers cannot see
acceptance-criteria prose at all**, so a byte-identical advisory set across a
50-cell acceptance rewrite is not evidence the rewrite preserved obligations —
it is evidence the instrument never looks. (My first attempt at this mutation
silently matched nothing — the field is `acceptance_criteria`, not
`acceptance`; that run reported "identical" for the wrong reason and was
discarded. The run above applied a verified mutation.)

This is F3's class, on a different surface, and it is the structural reason F5,
F6 and F7 were able to happen at all: 50 cells were rewritten with no
mechanical check watching. Sub-reviewer's related structural note, recorded for
the owner: the pass replaced backticked paths/symbols with *"the declared X"*
throughout, and `check_doc_refs.py` can only fire on a path-shaped backticked
token — so for the ~31 rows disposed as "already homed elsewhere, verified",
the SR acceptance cell is now inert to the kit's own reference checker too.

### F9 — MAJOR · CONFIRMED · the watermark's "ever allocated" verification used a structurally blind probe; `B` is under-seeded

**Claim** (`2026-08-17n`): *"The marks written: `B = 7`, `EXT = 5`, `REL = 3` —
the highs EVER allocated, verified against the registry's full git history, not
the column restated"*, dismissing the counter-examples as *"The sitting-2
draft's `B-08`/`REL-004` … were never registry rows — checked per-id with
`git log -S` over `external.toml`."*

**B-08 was allocated and cut by owner ruling.**
`docs/plans/2026-08-13-sitting-2-boundary-and-context.md:174` —
*"### 1R.2 The system's boundary crossings (v2 — **six**; B-08 removed 13o,
B-03 removed 13u)"*; the ruling itself at `:313`.

**The stated verification route could not have seen it.** Author
re-verification, three commands:

~~~text
$ git log --diff-filter=A --format='%h %ad %s' --date=short -- docs/requirements/external.toml
0ff33a95 2026-08-14 WI-442: mint external.toml, retire Stability for Approval, re-key rung 1

$ git log --format='%h %ad %s' --date=short -S'REL-004 folds into REL-003' -- docs/log.md
e32fd9a0 2026-08-13 sitting 2: the depth-0 frame CONFIRMED and LOCKED (owner in session, 2026-08-13o)

$ git log --oneline -S'B-08' -- docs/requirements/external.toml
(empty)
~~~

`external.toml` was **created 2026-08-14**; B-08 and REL-004 were cut
**2026-08-13**. A pickaxe over that file can never see an id retired before the
file existed. The empty result was read as *"never a registry row"* when it is
what a blind probe returns for everything. This is the standing
*re-derive-by-an-independent-route* rule failing in the specific way it exists
to catch.

**Consequence is live:** `docs/id-watermark` reads `B = 7`, so the next boundary
crossing minted is `B-08` — silently re-pointing an id cited in a live ruled
plan document *and* in `docs/log.md:411`, which is exactly the harm the
watermark header's own text claims to prevent. The entry's own tie-break argues
the fix direction: *"over-seeding is fail-safe — it wastes numbers, never
re-points history."*

### F10 — MAJOR · CONFIRMED · `REL` is under-seeded, same class, same root cause

`docs/log.md:3472` (ruling 13o, commit `e32fd9a0`): *"**REL-004 folds into
REL-003.**"* REL-004 was allocated in the v2 relationship space and folded by
ruling; `docs/id-watermark` reads `REL = 3`, so the next mint is `REL-004`.
Same blind probe, same consequence. Verified by the commands under F9.

### F11 — MINOR · CONFIRMED · the `EXT` mark is v2-scoped while the file header promises an unscoped guarantee

`EXT = 5` is correct for the v2 space, but three v1 ids are cited **in the live
registry itself** — `docs/requirements/external.toml:82`:

~~~text
absorbs = "v1 EXT-001; dissolved into it: v1 EXT-005 (git), EXT-007 (OS/filesystem/Python), EXT-008 (test+coverage toolchain)"
~~~

so the next three EXT mints re-point ids cited in that same file. `docs/id-watermark`'s
header states the unscoped promise (*"The highest id ever allocated in each
space … re-using it silently re-points every commit message, log entry and
archived document that cites that id"*) and the v1→v2 recycling has already
happened once (v1 EXT-005 = git; v2 EXT-005 = model services). The scoping
sentence belongs in the header. Note `_mark_history_findings`' new first-seed
exemption means nothing mechanical will ever raise this.

### F12 — MAJOR · CONFIRMED · "stricter-never-quieter" is false as a blanket claim: the Modified-chain advisory class went silent

**Claim:** the `2026-08-17m` code changes were stricter-never-quieter.

`d28e1ccb` deletes `modified_chain_advisories` (−89 lines) and its `analyze()`
call site. **Author's independent evidence** — the change is visible in the
committed goldens, which is how it surfaced here before the sub-reviewer's
report arrived. `git diff 47234903^..HEAD -- tests/golden/clean.txt tests/golden/orphan.txt`:

~~~text
-None. No unlifted LLRs, no Modified chain rows riding an unflagged or unresolvable owning SR.
+None. No unlifted LLRs.
~~~

A whole reported advisory class left the report. Four input classes that
produced a WARN before are silent after: LLR or TC `Modified` under all-`Approved`
owning SRs, and LLR or TC `Modified` with **no resolvable owning SR**.

**The sharp half is the second pair.** The ruling's rationale (a `Modified`
child under an `Approved` SR is a legitimate cell-level state, caught by the
snapshot-drift arm) does not cover a `Modified` child whose `SR-Refs` resolve
to nothing — and the surviving `sr_chain_drifts` docstring in the same commit
concedes the drift arm cannot fire on it: *"`is_drifted` fires only for a row
whose live Status claims approval, so a `Modified` child never counts as
drifted."* That arm was retired with no successor detector and no recorded
justification.

**Fairness, on the record:** `docs/log.md` itself is honest here — it scopes
*"stricter in exactly the ruling's direction"* (line 491) **only** to the
`check_trajectory` exemption removal, and records the residual. The refutation
lands on the blanket summary characterisation, not on the log entry's own
wording. Related MINOR, recorded: `tests/test_module_size_ratchet.py:657-661`
still describes the deleted suppression in the present tense as current
behaviour (*"suppressed when the owning SR flips in the same commit (the
attestation unit)"*), and the same commit re-stamped `check_trajectory.py`
4208 → 4169 in that file without correcting the adjacent clause.

### F13 — MAJOR · CONFIRMED · the `min()` cap pin observes the PRINTED message, not the served sleep

**Claim refuted** (`43bf51a7` commit body and TC-168's method): *"the `min()`
cap pinned load-bearing by a fallback-above-ceiling case (5 > 1 naps 1s)"*;
LLR-174 (`low-level-requirements.toml:1782`) *"an unparseable wording sleeps
`min(--limit-retry-fallback, ceiling)`"*, rationale *"the fallback nap is capped
at the same ceiling."*

`agent_loop.py` computes `wait = min(args.limit_retry_fallback,
args.wait_on_limit)`, prints it, then `time.sleep(wait)`. **Mutation** — leave
the `min` (and therefore the printed string) untouched, and nap the raw dial:

~~~diff
-            time.sleep(wait)
+            time.sleep(args.limit_retry_fallback)
~~~

**Author re-verification — the pin does not bite:**

~~~text
UNMUTATED: tests/test_agent_loop.py::test_fallback_nap_is_capped_at_the_wait_ceiling
           1 passed in 1.53s
MUTATED:   tests/test_agent_loop.py::test_fallback_nap_is_capped_at_the_wait_ceiling
           1 passed in 5.57s
~~~

The runtime is the proof: **1.53s → 5.57s**. The mutated loop demonstrably slept
the raw 5s past a ceiling of 1s, and the test that exists solely to prove the
cap load-bearing **passed anyway** — its only cap assertion is
`assert "sleeping 1s (--limit-retry-fallback)" in proc.stdout`
(`tests/test_agent_loop.py:673`), a string check on the print. The test's own
comment is accurate about the mutation it anticipated (*"Deleting the cap naps
**and prints** the raw 5s fallback and this fails"*) — deleting `min` moves both,
so it bites. Any mutation that separates the two slips through. The pin proves
the message, not the behaviour, and the behaviour is the guard against an
unbounded silent sleep in a walk-away run. Note also that the `_nosleep_loop`
recorder — the instrument the log cites as *"observed, never served"* — is not
used by this test; the one pin whose whole subject is a wait duration never
measures a wait.

### F14 — MAJOR · CONFIRMED · TC-170's failure is planted in the LAST regen step, so `regen`'s stop-at-first-failure is unpinned

**Claim refuted** (`43bf51a7`): *"TC-170: the failure-path sentence executed,
not inferred"*; TC-170's method promises *"a run whose **later step** fails
after green steps have dirtied the tree"*. LLR-142
(`low-level-requirements.toml:1400`) requires *"stopping loudly at the first
failure"*, and `trunk_step.py:480-482` states *"Stops at the FIRST failure — a
later generator may read an earlier one's output."*

The new test plants its failure in `open-items.toml`. **Author re-verification
of the ordering:**

~~~text
$ python -c "import trunk_step as T; print([s[0] for s in T.REGEN_STEPS])"
['arch-map', 'okf', 'derived-gate', 'trajectory', 'status', 'open-items']
last step: open-items
~~~

`open-items` is the **last** step — nothing runs after it, so "a later step
fails" is vacuous and the early return skips nothing observable.

**Mutation** — make `regen` carry on past a failure instead of stopping
(`_rc = 1; continue`, `_rc` seeded 0, `return _rc`), i.e. every downstream
generator now runs on a RED input:

~~~text
tests/test_trunk_step.py      15 passed in 1.20s
tests/test_trajectory_arch.py 76 passed in 4.33s   (the only other regen() caller)
~~~

Nothing bites. The documented invariant that protects downstream generators
from a RED upstream is enforced nowhere, and the test written specifically to
execute the failure path was constructed so it cannot reach it. *(My first
attempt at this mutation targeted a loop header that does not exist — the real
one is `for name, applies, argv, why in REGEN_STEPS:` — leaving `_rc` unseeded;
that run "failed" 4 tests on a `NameError`, which is a crash, not a result, and
was discarded. The run above is the corrected mutation, syntax-checked before
execution.)* Tree restored and re-verified green afterwards.

### F15 — MINOR · RELAYED · the ceiling boundary (`<=`) is unpinned in either direction

Sub-reviewer mutation (author did not independently re-run): `agent_loop.py`
`wait <= args.wait_on_limit` → `wait <`, so a reset landing exactly at the
consented ceiling abandons the run at `EXIT_WAITING` instead of sleeping.
Reported result: `tests/test_agent_loop.py` + `test_agent_loop_policy.py` →
88 passed, 1 skipped. The new parsed-reset pin uses ceiling `90000` against a
wait `< 86400`, so it is structurally incapable of touching the boundary, while
LLR-174 states the fork explicitly (*"a parsed reset **within that ceiling** is
slept … **Past the ceiling** … stops at `EXIT_WAITING`"*).

### F16 — MINOR · RELAYED · TC-170's "HEAD unmoved" proof is unfalsifiable by construction

Sub-reviewer's reading (author confirmed only that `regen()` contains no git
invocation): the log's proof — *"a mutation planting a commit-on-failure
bites"* — inserts a git call that does not exist in `regen()` and that no
plausible edit would add, and `test_regen_never_commits_the_caller_owns_the_
commit` already asserts the property. "Mutation-proved" here means an arbitrary
insertion was detected, which is not evidence of a pin.

### F17 — MINOR · CONFIRMED · the desk's "the shape you are signing" table is false at HEAD

`docs/plans/2026-08-13-sitting-3-spine-verification.md:215-216`:

~~~text
| spine | `SN=27 SR=63 LLR=155 TC=150` · `orphans=0 integrity=0` | the shape you are signing |
| pending signature | **147 `Modified` + 52 `Drafted`** (SR 40/19 · LLR 83/17 · TC 24/16) | ... |
~~~

**Author re-verification** — measured repeatedly this round via
`trace.py --root .`: `SN=27 SR=70 LLR=159 TC=155 … drafts=68`. Off by **+7 SR,
+4 LLR, +5 TC**, and 68 drafts against a stated 52. Four subsequent
desk-reconcile commits (`db9ca307`, `dda5cc0c`, `43bf51a7`, the 17u sweep)
re-stamped the scoreboard ~60 lines below without touching this row.
**Mitigation, stated honestly:** the block self-labels *"measured `2026-08-16r`,
RE-DERIVE AT CONVENING … Re-run the command; if it disagrees, it wins"* — a
stamped snapshot, not a currency claim. Hence MINOR. But the note column reads
*"the shape you are signing,"* which is the one place a stale number is
load-bearing.

### F18 — MINOR · CONFIRMED-IN-PART · `ba23fe3d`'s frame-count correction has no Decisions entry

`grep -c 'ba23fe3d' docs/log.md` → **0**. The commit moved `docs/status.md`
from "5 entities · 6 crossings · 3 relationships" to "4 entities · 4 crossings ·
3 relationships since the `2026-08-16q` cut" — a substantive frame-count
correction. **In part**, and the caveat matters: the Decisions section is
explicitly scoped *"Ratified or executed decisions only"*, and a catch-up of
numbers to an already-ruled cut is arguably bookkeeping rather than a decision,
so its absence may be correct by the section's own rule. Recorded for the owner
to place, not asserted as a defect.

### F19 — MINOR · RELAYED · an unpinned `HEAD` in a frozen review package

`docs/plans/2026-08-15-review-package.md:15` — *"## 1. What landed (the range
`bb4ac776..HEAD` on `infra/mechanized-loop`)"*. The file's last touch was
`d28e1ccb`; commits have landed since, so the section's inventory is false at
HEAD by construction and grows more so. A range doc should pin both ends.

---

## Checked and CLEAN

Recorded so the owner knows what the round covered, not only what it caught.

**The unification (target 1) — the arithmetic all reproduces.**

- **The 18-row amendment set and the SN split**: live
  `docs/requirements/stakeholder-needs.toml` carries exactly **18 `Modified` +
  9 `Approved`** = 27 rows, the claimed figures.
- **The 138 off-spine cells**: **123 IF · 11 EXT/B/REL · 4 CMP** — re-derived by
  anchored grep excluding comment lines (an unanchored count gives 12 for EXT
  by matching the header comment; the claim is right and the naive count is
  wrong). Matches `6f39b2ed`'s stated 4 entity + 4 boundary + 3 relationship.
- **No lowercase survivors**: `grep` for `= "drafted"|"approved"|"founded"|
  "planned"|"verified"|"draft"` across all live registries and shipped
  templates returns **nothing**.
- **§5B was truly not executed**: `is_modified` alive at `derive_gate.py:417`
  and `trace.py:178` with live call sites; `Modified` present in
  `trace.py:378 STATUS_VALUES`. Confirmed as claimed.
- **Trap (i) — the no-writer guard bites, proved live.** Planting a writer into
  a shipped script in each of the three spellings reds
  `test_no_shipped_loop_module_WRITES_an_approval_cell`:
  `status = "Approved"` → FAILED, `approval = "approved"` → FAILED,
  `state = "verified"` → FAILED. Tree restored to 0 dirty files after each.
- **The SN schema census is non-vacuous, proved live.** Deleting the `tags`
  line from `project-trajectory/registries/stakeholder-needs.template.toml`
  reds the new leg exactly as claimed:
  `FAILED tests/test_dogfood_sync.py::test_template_declares_every_key_the_live_registry_uses[SN-ID]`
  — *"template no longer declares key(s) tags the tier schema states"*
  (1 failed, 36 passed). Restored.
- **Design call (2) — "`Founded` where a discharge predicate exists" — is
  actually enforced, not just doctrine.** `trace.py:455-476` carries genuine
  per-registry subsets: `IF`/`EXT`/`B`/`REL` → `{Drafted, Approved}`; `CMP` →
  `{Drafted, Approved, Founded}` plus `Standing → {active, has-gap,
  deprecated}`. An IF row cannot be written `Founded`.
- **The shipped components template carries the split in full** —
  `components.template.toml:5-6` declares both `status = "Drafted"` and
  `standing = "active"`, and its notes document the two axes, the `Founded`
  rule and `omit = active`. **`RESYNC_PACK.md`** carries both downstream-visible
  entries with the value maps. (F4 is the gap in this otherwise-complete sweep.)
- **The basis line is genuinely byte-identical** at `810f1c01` vs HEAD
  (worktree-verified). F3 is about what that proves, not whether it is true.

**Targets 3/4 — sub-reviewer findings that came back CLEAN under re-verification.**

- **The `check_trajectory` exemption removal is genuinely never-quieter.** The
  deletion removes a `continue` guarded by `any(_flagged_sr(...))`; removing a
  suppression can only add findings, and the surviving gate
  `if head_status != cur_status or head_status not in _RATIFIED_TEXT: continue`
  is byte-unchanged.
- **"The retired class emitted 0 findings on today's tree" — independently
  re-derived, TRUE.** The retired predicate re-implemented straight off the
  TOML registries (not from trace's output): 83 `Modified` LLRs, every one
  owned by a `Modified` or `Drafted` SR; 24 `Modified` TCs, zero with an
  all-unflagged or unresolvable owner set. Both arms return `[]`.
- **The shipped kit carries no surviving chain reading.** `PROCESS.md:374-381`
  is rewritten to the cell reading; the three skills and their `.claude/` +
  `.agents/` copies follow. The surviving teach-surfaces are the generated
  `docs/ratify/*` banners and closed WI/review docs — genuine append-only
  history, deliberately not filed.
- **IF-043's "one engine" claim is TRUE in the code.**
  `check_privacy.py:318-380`: `Scanner.__init__(root, secrets_on, privacy_on)`
  compiles the identity/PII terms onto the same object, and `scan_line` (:357)
  yields **both** classes from one function body — privacy at :361-371, secrets
  at :372-380; `scan_diff_text` (:382) walks one `git log -p` stream with that
  one scanner. Not separate code paths for the `--range` verdict IF-043 names.
  (Boundary the notes don't state, not filed: `check_author()` at :489 is a
  separate identity path in a different CLI mode, outside `--range`.)
- **IF-128 → LLR-166's refusal claim is TRUE.** `spine_carrier.resolve` (:576)
  raises at :598-599 — *"REFUSED — {} exists under BOTH carriers"* — and `load`
  (:641) raises at :660 and :669. LLR-166's `code_symbol` names both symbols;
  LLR-173's names neither, so the-definer-answers re-point is supported.

**Target 2 — acceptance cells sampled adversarially and found to be genuine
restatements** (highest-specificity-loss diffs chosen first): SR-006
(*strengthened* — the replacement is a strict superset of the three named
steps), SR-034, SR-113, SR-147, SR-149, SR-151 (the strongest re-home — both
stripped tokens are stated verbatim in the row's own `rationale`), SR-154,
SR-157, SR-158 (the model re-home — every stripped token appears in the LLR-012
/ LLR-038 detail cells added in the same commit), SR-166, SR-129/138/168/169,
and SR-052/053/054 (chain-closure openers, *strengthened*: each new cell adds
explicit fail conditions absent before). The ledger's integrity mechanism was
also spot-checked: recomputing `sha256(old_cell)[:12]` at `f1d9c57c^` for
SR-006/040/159/167 reproduces the ledger's hashes exactly — the ledger is not
fabricated, and the 50-cell decomposition (39 + 3 + 8) is arithmetically
consistent. All **8** re-homed LLR ids named in the entry are genuinely present
in the diff (LLR-012/014/035/038/044/067/136/156) — no phantom entries.

**Target 6 — the two staleness charges this round went hunting for are REFUTED.**

- **The §0.4 SCOREBOARD is NOT stale at HEAD.** It lives at
  `docs/plans/2026-08-13-sitting-3-spine-verification.md:275` (not in
  `2026-08-15-review-package.md`, which has no §0.4), and reads *"SCOREBOARD —
  re-stamped `2026-08-17u`, the current truth of this list. **OPEN CALLS:
  NONE.** Item 6 was the last one, and it is now RULED AND EXECUTED."* That
  matches the actual commits `f1d9c57c` (item 19), `810f1c01` (item 6 ruled)
  and the nine unify steps. The `17q`-era open list ("6 / 18-pins / 19") was
  superseded three re-stamps ago.
- **`docs/status.md` is NOT stale at HEAD.** Line 30 reads *"…re-pruned
  `2026-08-17n`, `r`, `s`, `t` and `u`; the live list is EMPTY and item 6 has
  now LANDED."* The `items 6 · 19` string survives only at `docs/log.md:328`,
  inside entry `2026-08-17r`, correctly scoped to that entry's moment.

**Target 6 — desk claims that reproduced exactly.**

- `2026-08-17q`'s anchor: `git show 1635ace4` subject is *"39 of 70 SRs name an
  artifact in acceptance, 34 cells use the current-carrier idiom"* — hash,
  numbers and content all match the entry.
- The 39 → 40 drift is **self-corrected, not hidden**: `docs/log.md:264-268`
  (17s) records *"40 of 70 … (the item-19 table said 39; the +1 is `SR-112`)"*.
- `2026-08-17j`'s *"Test pin TAKEN (`tests/test_gen_cases.py`, +2 tests)"* —
  `git show cbeb695a -- tests/test_gen_cases.py | grep -c '^+def test_'` → **2**.
- `db9ca307`'s subject matches log `2026-08-17l:623-624` exactly.
- The `rev=166b406d` fig anchors inside entry `2026-08-17j` (shipped in
  `cbeb695a`) follow the parent-rev measurement convention used identically
  elsewhere (`rev=f1d9c57c` inside `810f1c01`). Not a defect.

**Target 5 — the pins that are sound.** The `--limit-retry-fallback` default
`3600` and `--stall-limit` default `3` mutations would fail their tests by
direct string/count assertion; those two pins are genuine. F13 and F14 are the
two that were probed at the caps and boundaries and did not hold.

---

## Coverage — what this round could not reach

Stated so its absence is not read as coverage.

- The **five pins were probed at three points, not five.** F13 and F14 were
  author-re-run and confirmed; F15 and F16 carry the sub-reviewer's evidence
  only. The `3600` and `3` default pins were reasoned about, not mutated.
- **The "31 class-A findings" count of `2026-08-17i`/`j` was not independently
  recounted** — only checked for internal consistency against
  `docs/plans/2026-08-17-shipped-docs-staleness-audit.md`. Neither confirmed
  nor refuted.
- No finding was applied. The registries, scripts, tests, plans and templates
  are byte-identical to `6fe5e5bb`; `git status --porcelain` shows only this
  new review directory. Every temporary mutation in this round (three planted
  writers, the template `tags` deletion, two worktree registry edits, one
  acceptance-cell blanking, the `agent_loop` nap mutation, the `trunk_step`
  regen mutation) was restored or discarded with its worktree, each verified;
  `test_trunk_step.py` re-run green (15 passed) after restore.
- The **full unfiltered suite was not re-run** this round. `2026-08-17u`'s
  closing figure (2579 passed, 10 skipped) was not independently reproduced;
  the tests this round ran were targeted (`test_dogfood_sync.py` — 1 failed
  under mutation / 36 passed clean; `test_ratification_level.py` single test ×
  3 mutations). No finding here turns on a suite-wide count.
- F1's live impact is **latent**, not active — no CMP row writes `standing`
  today. It is filed as a design/enforcement gap, not a false green.
- Sub-reviewer findings are marked where the author re-verified the decisive
  half but relayed a companion half (F5's `components_check` leg, F6's
  LLR-037-is-stale leg, F12's `test_module_size_ratchet` leg). Those legs carry
  the sub-reviewer's evidence, not a second author derivation.
