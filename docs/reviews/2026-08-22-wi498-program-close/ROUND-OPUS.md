# ROUND-OPUS — adversarial review, WI-498 stage-unification program close

_Reviewer: internal adversarial (Opus). Range `f23e6002..d3f119ea`, branch
`requirements/ears-and-quality-characteristics`, HEAD `d3f119ea`. Brief:
`docs/reviews/2026-08-22-wi498-program-close/BRIEF.md`._

**Method.** Every numbered finding below was reproduced or traced to file:line
before it was written. Where a guard was suspected of being unfalsifiable it was
MUTATION-TESTED in a scratchpad copy of the tree (`git archive HEAD` into the
session scratchpad), never in the working tree. Nothing tracked was modified,
staged, or committed by this review; the only write is this file. Suspicions I
could not reproduce are listed at the end as SUSPICIONS and are deliberately
kept out of the numbered findings.

**Count: 14 findings — 0 CRITICAL, 7 MAJOR, 7 MINOR.**

---

## 1. MAJOR — The DevStg-Release "two pins" are both evadable; mutation-verified

**Evidence.** `tests/test_ratification_level.py:760-777`
(`test_the_RELEASE_rung_has_no_PRODUCER_in_the_source`) and
`tests/test_ratification_level.py:733-757`
(`test_NO_status_combination_reaches_the_RELEASE_rung`).

The structural pin greps the CONSTANT NAME:

```python
assert "return STAGE_RELEASE" not in body
assert "STAGE_RELEASE" not in body.split('"""')[-1]
```

The exhaustive pin enumerates 2 × 4³ = 128 spines over the closed `Status` enum.

**Reproduced.** I injected a live Release producer into a scratchpad copy of
`project-trajectory/scripts/spine_rules.py`, immediately after
`bifs = bifs or []` / `cmps = cmps or []` in `spine_stage`:

```python
if tcs and all((r.get("Status") or "").strip() == "Released" for r in tcs):
    return "DevStg-Release"
```

Result: `2 passed` for the two Release pins, and `50 passed` across
`test_stage_ladder.py`, `test_kitlib_ladder.py`, `test_spine_rules.py`,
`test_derive_stage.py`. **A live, reachable `DevStg-Release` producer passes the
entire guard set.**

Two independent evasions, and the mutant used both: the literal string dodges a
name-based grep (as would `_ladder.STAGE_RELEASE`, `STAGE_ORDER[-1]`, or a
helper `return _top()`), and any arm keyed on a value outside the four-member
`Status` enum — a new column, a `bifs`/`cmps` predicate, an evidence-carrier
parameter — dodges the enumeration. Note that the evidence carrier is exactly
what WI-500 is minted to add, so the arm most likely to be written is the one
neither pin can see.

**Failure scenario.** WI-500 lands the test-evidence carrier and wires the
Release rung on a fixture-invisible condition, or a later refactor spells the
constant differently. `spine_stage` starts returning `DevStg-Release` on real
spines; `check.py` selects a Release-threshold plan and `human_holds` compares
against a rung the ladder promised nothing derives. Both pins stay green, and
the docstring at `spine_rules.py:606-622` ("No combination of Status cells
returns it") continues to read as verified. This is the OI-30 D2 guard —
"a Status cell can never claim the evidence passed" — going quietly vacuous.

**This is the program's own recorded lesson turned on itself.** The fragment
banks the census blind spot three separate times (slice 0's enum inventory keyed
on constant NAMES, slice 3's pin census, slice 4's reader census) and concludes
at `docs/log.d/2026-08-21-wi498-stage-unification.md:1711-1714`: "grep the
VALUE, not the constant name". The structural pin greps the name.

**Fix (one line):** assert on the VALUE — `assert ladder.STAGE_RELEASE not in
body_after_docstring` where `body` is the source with string literals intact,
i.e. test the rendered value `"DevStg-Release"`, and add an AST-level assertion
that no `Return` node in `spine_stage` can yield it.

---

## 2. MAJOR — The vocabulary sweep rewrote PROSE cells of Approved rows, against its own recorded restraint, and the rewrites are false

**Evidence.** `c170da9f` ("WI-498: retire docs/gate and finish the one-vocabulary
sweep"), confirmed by `git log -S` on each string.

Slice 5's own banked restraint rule, at
`docs/log.d/2026-08-21-wi498-stage-unification.md:1623-1627`:

> Slice 5 re-pointed only what a rename or a move makes MECHANICALLY wrong — the
> `module =` carriers (a carrier must point at the carrier), and LLR-148's …
> **and left the prose, because re-authoring an Approved cell is a
> ratification-bearing act**.

That is not what it did. `docs/ratify/2026-08-22-reattest.md` records these
changed cells, all authored by `c170da9f`:

| row | cell | class |
|---|---|---|
| LLR-050, LLR-147, LLR-148 | `Module` | carrier — consistent with the rule |
| TC-050, TC-141, TC-142 | `Evidence` | carrier — consistent |
| **LLR-142** | **`Rationale`** | **prose** |
| **LLR-124** | **`Detail`** | **prose** |
| **TC-050** | **`Expected`** | **prose** |
| **TC-141** | **`Method`** | **prose** |
| **SR-140** | **`Rationale`** | **prose** |

Five prose cells across five Approved rows — the exact act the rule forbids.

**And the rewrites assert things that are false.** The sweep replaced the token
`derive_gate` with `spine_rules` without checking the referent survived:

- `docs/requirements/low-level-requirements.toml` — LLR-142 `rationale`, after:
  **"spine_rules runs before the dashboard/status regens because `docs/gate` is
  their input, not their output."** Both halves are wrong. `spine_rules.py` has
  no CLI at all — running it produces nothing, and the module's own comment at
  `project-trajectory/scripts/spine_rules.py:718` records that "this module's
  whole CLI" was deleted. And `docs/gate` is the file this very commit deleted:
  the sweep swept the SCRIPT name and left the FILE name in the same sentence.
- LLR-124 `detail`, after: "trunk_step --regen runs gen_trajectory --status
  **after spine_rules** (the gate is its input)". `spine_rules` is not a regen
  step; `REGEN_STEPS` at `project-trajectory/scripts/trunk_step.py:435-465` is
  `okf, derived-stage, trajectory, status, open-items`.
- TC-050 `expected`, after: "**spine_rules** computes the correct gate … and
  `--check` catches drift; the compared **basis line** carries modified=N …
  `--print` shows the derived current phase". `spine_rules` has no `--check`, no
  `--print`, and no `basis_line` — all three retired with the bar axis.

I verified the absence directly: `grep -n "def main\|argparse\|__main__\|--check\|--print\|basis_line" spine_rules.py` returns only the line-718 obituary, and `python project-trajectory/scripts/spine_rules.py --check` produces no output and does nothing.

**Then these were blessed as inert.** Commit `ac121647`'s message:

> The same copy blesses the four pending post-sign amendments the re-attest brief
> reports (SR-049/140/170/173), **all of them the mechanical derive_gate ->
> spine_rules re-pointing** from the WI-498 stage unification.

"Mechanical re-pointing" is true of the EDIT and false of its EFFECT: it
characterizes as a rename a set of amendments that inserted false statements
into ratified requirement, design and test-case cells. The owner's warrant
("Approve the spine changes, I have reviewed what was there") was given against
that characterization. This is the repo's dominant defect class — a fluent
signed claim — sitting on its highest-authority act in the range.

**Fix (one line):** file a corrective WI that re-authors LLR-142/LLR-124/TC-050
against what `derive_stage`/`trunk_step` actually do, and amend the slice-5
record to state that prose cells WERE rewritten, so the restraint rule and the
diff stop disagreeing.

---

## 3. MAJOR — The owner's DECLARED_INPUTS ruling was not swept into the adopter-facing migration recipe

**Evidence.** `project-trajectory/RESYNC_PACK.md:2948-2955`, live at HEAD:

> **This step is AFTER the dial re-key on purpose.** `docs/process.toml` is one
> of the declared derivation inputs (`kitlib/stage.py DECLARED_INPUTS` — it is
> listed deliberately over-inclusively, because an over-inclusive fingerprint
> costs a spurious re-derivation while an under-inclusive one costs a stale
> read). So rewriting the dial **CHANGES THE FINGERPRINT**: regenerate first and
> step 3 immediately re-stales the file you just committed, and step 6 fails
> `derived-stage` with a correct complaint.

Every load-bearing sentence there is now false. `project-trajectory/scripts/kitlib/stage.py:132-139`:

> `process.toml` is DELIBERATELY NOT an input (owner ruling 2026-08-21, amending
> the plan's §2 list) … Dials govern who may ratify, not what stage is derived.

Confirmed by `b816177f`, whose own message says "docs/process.toml dropped from
DECLARED_INPUTS (owner ruling amending plan section 2)". `git show --stat
b816177f` shows it touched `kitlib/stage.py` and `tests/test_kitlib_stage.py`
and **did not touch RESYNC_PACK.md**.

The same commit claims to have performed "the declared-policy staleness sweep".
That sweep covered the DIAL change and missed the DECLARED_INPUTS change.

**Driven, in a scratchpad copy of HEAD** (both directions, to be sure the code —
not just the comment — has the ruling): appending a line to
`docs/requirements/components.toml` (a declared input) moves the fingerprint
`3d013e24…` → `b0c7827f…` and `derive_stage.py --check` exits **1**; appending a
line to `docs/process.toml` leaves the fingerprint untouched and `--check` exits
**0**, reporting "docs/stage up to date". The code has the ruling. The
RESYNC_PACK contradicts the code.

**Second stale site, same cause.** `tests/test_pre_commit_hook.py:34-42`, the
`set_dial` helper docstring:

> `docs/process.toml` is a DECLARED derivation input (`kitlib/stage.py`
> DECLARED_INPUTS), so writing ANY dial changes the stage fingerprint and the
> commit floor's `derived-stage` step then correctly reports the committed
> record as stale.

False as of `b816177f`. The helper's `run_py(["scripts/derive_stage.py", ...])`
call at line 44 is now a no-op for its stated purpose, and the docstring's
recorded lesson ("which is exactly how these tests failed at the slice-5 close")
is attached to a mechanism that no longer exists.

**Failure scenario.** An adopter re-syncing follows §4, reads that rewriting the
dial re-stales `docs/stage`, and orders their migration around a constraint that
is not real. The worse case is the belief, not the ordering: they carry away
"policy dials are fingerprint inputs" and reason from it the next time they
touch `process.toml` or extend `DECLARED_INPUTS` themselves. The RESYNC_PACK is
the kit's migration contract; a false mechanism statement there propagates to
every downstream repo.

**Fix (one line):** rewrite `RESYNC_PACK.md:2948-2955` to say the dial is NOT a
derivation input (so the step order no longer needs that justification) and
correct the `set_dial` docstring in `tests/test_pre_commit_hook.py`.

---

## 4. MAJOR — The "six Approved rows" census undercounts by class, for the fourth time

**Evidence.** The banked finding at
`docs/log.d/2026-08-21-wi498-stage-unification.md:1618-1632` names **six**
Approved spine rows describing deleted machinery (LLR-050, LLR-051, LLR-142,
LLR-148, LLR-157, SR-006), plus SR-148 at :1605 as "a SEVENTH". I verified the
list is short at both the TC tier and the off-spine registries. All Status cells
below confirmed by reading the row:

| row | Status | cell | what it names that no longer exists |
|---|---|---|---|
| `docs/test/test-cases.toml:543` **TC-051** | **Approved** | `method` | "renders its three panels from the live registries + **docs/gate** (the current-gate highlight matches **docs/gate** …)" |
| `docs/test/test-cases.toml:1392` **TC-142** | **Approved** | `method` | "leaves **docs/gate** byte-identical (output mode only)" |
| `docs/test/test-cases.toml:1700` **TC-170** | **Approved** | `method` | "**arch-map** before okf, **derived-gate** before its two consumers" |
| `docs/requirements/performance-budgets.csv:5` **PB-004** | — | `Notes` | lists **`derived-gate`** among the pre-commit run-steps |
| `docs/requirements/interfaces.toml:1051` **IF-081** | Drafted | `contract` | "`--regen` re-derives … **derived-gate** BEFORE the dashboards whose input it is" |

**TC-170 is the sharp one.** It is `tier = "Smoke"`, `automated = "Yes"` — part
of the mechanized verification basis that `ac121647` reports as "70 mechanized /
3 demonstrated / 0 attested". Its `method` cell describes the regen order as
"arch-map before okf, derived-gate before its two consumers". The real test,
`tests/test_trunk_step.py:249-250,277-293`, asserts the sequence
`okf, derived-stage, trajectory, status, open-items` — and its own comment at
line 284 says "`arch-map` LED this list until WI-455 retired it". So an Approved
TC row counted as mechanized evidence names two retired steps, neither of which
the test it points at asserts.

**PB-004 is a partial sweep inside one file.** PB-002 in the same CSV WAS
correctly re-keyed and re-measured at `d35ced83`; PB-004 four lines below it was
not touched.

**Failure scenario.** A verifier executing TC-051 or TC-142 as written cannot:
the artifact they instruct comparing against does not exist. A reader auditing
the "70 mechanized" figure finds at least one row whose method does not describe
its test. The blind spot is the same one the program recorded three times, in a
fourth shape: this census keyed on the SR/LLR TIERS and missed the TC tier and
the off-spine registries.

**Fix (one line):** re-run the retirement census by grepping `docs/gate`,
`derive_gate` and `derived-gate` across **all** registry carriers (SR, LLR, TC,
IF, PB, CMP), and correct the banked count — the Approved total goes from six to
at least nine (adding TC-051/142/170), with PB-004 and IF-081 as two further
live rows outside the Approved set.

---

## 5. MAJOR — SR-139's normative requirement cell still mandates the retired 0–4 ordinal

**Evidence.** `docs/requirements/system-requirements.toml`, SR-139
("Ratification as an ordinal over a derived spine stage"), `status = "Approved"`:

> `requirement` = "The kit shall express human ratification authority as **a
> cumulative integer 0-4** naming the highest spine tier a human still ratifies,
> compared against a separately derived SPINE STAGE (**0=SN..4=nothing in
> process**) with a declared, auditable mapping to **the harness gate** …"

`acceptance_criteria` compounds it: "**Level N** holds exactly the tiers …;
**stage 4** is held by no level …; an **out-of-range level** falls back …".

WI-493 (folded into this program) re-keyed the dial to rung strings. The shipped
homes now carry `human_ratification_through = "DevStg-Release"`
(`project-trajectory/process.toml.template`) and `"DevStg-Needs"`
(`docs/process.toml`), pinned by
`tests/test_ratification_level.py:251-282`; the 0–4 ordinal survives only as
`agent_common.LEGACY_DIAL_ORDINALS`, a migration table that emits "Set it to a
`DevStg-*` rung". And "the harness gate" the mapping is declared against was
deleted with the bar axis.

This is strictly worse than the banked SR-148 finding at fragment line 1605,
which the record calls "worse than the six below in kind" because it states
retired values as an ACCEPTANCE CRITERION. SR-139 states them in the
**normative requirement cell** — the obligation itself, not its test. SR-139 is
not mentioned anywhere in the fragment's banked findings (`grep SR-139` returns
one unrelated hit at line 225).

**Failure scenario.** The spine's own normative statement of ratification
authority requires a mechanism the kit no longer ships. Any future adjudication
that reads SR-139 to decide what the dial must be will re-derive the retired
ordinal from an Approved row.

**Fix (one line):** add SR-139 to the WI-499 re-authoring campaign and correct
the banked count, which currently stops at "a seventh row".

---

## 6. MAJOR — "no consumer can read a stale stage, on any lane" is false as stated, and it is published in the generated file

**Evidence.** `project-trajectory/scripts/kitlib/stage.py:331-334`, rendered
verbatim into the committed `docs/stage` header:

> `fingerprint` is a SHA-256 over … the declared derivation inputs … A reader
> recomputes it and trusts the values above ONLY on a match, deriving fresh in
> memory otherwise — **so no consumer can read a stale stage, on any lane.**

Three live consumers read `docs/stage` without the fingerprint check:

| consumer | line | what it does |
|---|---|---|
| `traj_parse._stage_value` | `traj_parse.py:471` | `_kitstage.parse(path.read_text(...))` — feeds `traj_panels.process_panel` and `gen_trajectory` |
| `traj_status._stage_facts` | `traj_status.py:115` | same, feeds the `docs/status.md` generated block |
| `intake._stage_moved` | `intake.py:513-525` | `git show <rev>:docs/stage`, two-tree history delta |

Only three call sites reach `read_stage`: `check.py:1258`,
`agent_common.py:895`, `check_trajectory.py:1888`.

Each bypass is individually defensible and individually documented —
`traj_parse.py:456-462` and `traj_status.py:105-110` both say plainly that they
read the recorded file so a generated artifact describes the commit it ships
with, and `kitlib/stage.py:45-52` ("READERS NEVER WRITE") is coherent with that.
**The design is fine; the sentence is not.** "No consumer, on any lane" is an
unqualified universal, and the dashboard and status block are consumers that by
design can and do render a stale value.

**Failure scenario.** `docs/stage` goes stale (any declared-input edit). The
harness derives fresh and is correct; `PROJECT_STATE.html` and `docs/status.md`
render the stale rung. A reader who trusts the header sentence — printed in the
very file they are reading — concludes the dashboard's rung is verified. The
header is the most-read prose in the mechanism and it overclaims the one
property the program is named for.

**Fix (one line):** qualify the header and the docstring to "no SELECTION or
RATIFICATION consumer can read a stale stage", and name the display bypass in
the same sentence.

---

## 7. MAJOR — Nothing guards the inverse defect: an input read but undeclared

**Evidence.** `project-trajectory/scripts/kitlib/stage.py:125-140`
(`DECLARED_INPUTS`) versus `project-trajectory/scripts/spine_rules.py:723-800`
(`load_spine`). `grep -rn "DECLARED_INPUTS" tests/ project-trajectory/` returns
seven hits, none of which pins the list against what the derivation reads:

- `tests/test_kitlib_stage.py:33,232` — iterate the list, assert resolution count
- `tests/test_kitlib_stage.py:286` — `test_process_toml_is_NOT_an_input`, one
  named exclusion
- the rest are the definition and its two consumers

I verified by hand that the list is complete TODAY: `load_spine` reads exactly
system-requirements, low-level-requirements, test-cases, stakeholder-needs,
external and components; and the carrier suffix orders match
(`spine_carrier.py:445-446` `CARRIERS = (".toml", ".csv")`,
`NEED_CARRIERS = (".toml", ".md")` against the declared tuples). **The contract
holds by inspection and is held by nothing else.**

The existing pin is one-directional by construction: it proves a named file is
NOT an input. Nothing proves an unnamed file is not an input.

**Failure scenario.** A future rung reads a registry the list does not name —
`docs/requirements/interfaces.toml` is the obvious candidate, since it is a
spine registry that `load_spine` does not currently read, and the ladder already
has two rungs keyed to off-spine registries. From that moment the fingerprint no
longer covers an input: `read_stage` matches on a fingerprint that ignores the
edit, returns the recorded record, and **every consumer silently reads a stale
stage — permanently, not transiently.** `derive_stage --check` also passes,
because it compares the same uncovered fingerprint. The entire self-healing
property fails closed-mouthed. This is the precise inverse of the defect the
owner's process.toml ruling corrected, and it is the expensive direction: the
over-inclusive error cost a red commit bar, the under-inclusive error costs a
false green.

**Fix (one line):** add a test that runs `load_spine` under a `Path.read_text`/
`open` audit (or a temp tree where every non-declared `docs/**` file is
poisoned) and asserts the set of files actually read is a subset of
`input_paths(root)`.

---

## 8. MINOR — Two translations of the same retired vocabulary, in one file, disagreeing by three rungs

**Evidence.** `project-trajectory/scripts/check.py:397-399` versus `:1141-1151`.

```python
_LEGACY_BAR_THRESHOLD = {STAGE_REQS: STAGE_NEEDS,
                        STAGE_TESTS: STAGE_IMPL,      # Tests bar -> Impl rung
                        STAGE_IMPL:  STAGE_IMPL}
RETIRED_STAGE_ALIASES = {"G1": STAGE_REQS,
                         "G2": STAGE_TESTS,           # Tests bar -> Tests rung
                         "G3": STAGE_IMPL,
                         "DevBar-Tests": STAGE_TESTS, ...}
```

The slice-2 record derives the correct translation explicitly
(`docs/log.d/2026-08-21-wi498-stage-unification.md:270-280`): the bar was a MIN
over every in-scope row, so the `DevStg-Tests` bar "was reached **only by a
spine already fully decomposed and TC'd**, which on the ladder is the
`DevStg-Impl` RUNG, three above the span's floor". `_LEGACY_BAR_THRESHOLD`
applies that rule. `RETIRED_STAGE_ALIASES` does not — it maps the tag to the
same-spelled rung.

**Driven.** `python project-trajectory/scripts/check.py --gate G2 --list` warns
and resolves to `DevStg-Tests`, yielding a 12-step plan. `--stage DevStg-Impl`
yields 26. The 14 steps that drop out include **`traceability`** and
**`backlink-coverage`**. I confirmed their pre-change membership against the
source rather than the slice-2 table: at `f23e6002` (the commit before the
re-key), `check.py:652` reads
`("traceability", (), trace_cmd, {BAR_TESTS, BAR_RELEASE}, "process")` and
`check.py:782-785` gives `backlink-coverage` the same `{BAR_TESTS, BAR_RELEASE}`
set. Under the old membership rule `--gate G2` (= `BAR_TESTS`) selected both.
It no longer does.

**Failure scenario.** An adopter's CI or hook passes `--gate G2` or
`--gate DevBar-Tests` literally (the exact scenario the silent-`--gate`
concession exists to protect). After the re-sync their pipeline stays green,
prints one warning about vocabulary, and quietly stops running traceability and
backlink coverage. The warning text at `check.py:1176-1181` reports the value
re-reading and says nothing about the plan shrinking, so the operator has no
signal that 14 checks left.

**Fix (one line):** either route `RETIRED_STAGE_ALIASES` through
`_LEGACY_BAR_THRESHOLD` (so `G2` → `DevStg-Impl`, preserving effective arrival),
or extend the warning to name the steps that a bar-era value no longer selects.

---

## 9. MINOR — The kit's flagship generated artifact still teaches the deleted bar axis

**Evidence.** `project-trajectory/scripts/traj_panels.py:966`:

```python
("gate bar", "the full check.py --gate run at phase close / advance"),
```

and `traj_panels.py:1092`: `"a phase closes at the <strong>gate bar</strong> —
the commit-bar-vs-gate-bar cadence …"`. `grep -o "gate bar" PROJECT_STATE.html`
returns **4** occurrences in the committed dashboard.

Against `project-trajectory/PROCESS.md:501-506`, which states the ruling: "no
second 'bar' axis and no second spelling".

`check_vocab --strict` reports clean (424 live authored files, no retired gate
tags) because its refused set is TAGS (`G1`/`G2`/`G3`, `DevBar-*`, `[g1]`,
`[g2]`) — the retired CONCEPT and the deprecated flag spelling are invisible to
it. `PROJECT_STATE.html` is additionally exempt as generated
(`check_vocab.py:212`), so neither the source nor the artifact is policed.

**Failure scenario.** The dashboard is the most-read surface in the kit and the
first thing an adopter sees. It teaches "gate bar" and `check.py --gate` as the
phase-close procedure — the axis slice 5 deleted and the flag spelling the kit
now only tolerates. The one-vocabulary claim fails at the highest-traffic
surface, and no check can see it.

**Fix (one line):** re-word the two `traj_panels` strings to the rung-boundary
vocabulary and regenerate, or add the retired CONCEPT phrases to
`check_vocab`'s refused set for kit-authored source.

---

## 10. MINOR — Shipped templates teach the deprecated flag and a retired tag metavariable

**Evidence.**

- `project-trajectory/PLAN.template.md:39` — "**Done-when:** `TC-000` passes in
  the smoke tier; `scripts/check.py --gate DevStg-Tests` green."
- `project-trajectory/specs/WI-000.template.md:51` — "The change is implemented
  and the harness is green (`check.py --gate <G>`)."

The second is the worse one: `<G>` is a metavariable from the retired G-tag
generation, so the template teaches an adopter to fill a cell with a vocabulary
this program spent a slice retiring. `check_vocab` cannot catch it — it matches
the literal tokens `G1`/`G2`/`G3`, not a `<G>` placeholder — and I confirmed
templates ARE in scope (`.md` is in `TEXT_SUFFIXES` at `check_vocab.py:228` and
no `EXEMPT_GLOBS` entry covers `project-trajectory/**`), so the clean result is
a blind spot rather than an exemption.

Also: `PLAN.template.md:39`'s recipe is now weaker than it reads —
`--gate DevStg-Tests` does not run `traceability` (see finding 8).

**Failure scenario.** Every repo adopting the kit inherits a plan template and a
spec template whose done-when clause names the deprecated spelling, and one that
names a retired tag class. CLAUDE.md's rule — "a token the kit MANDATES into an
adopter's cell must mean something in **their** repo" — is violated by `<G>`.

**Fix (one line):** change both to `check.py --stage DevStg-Tests` and
`check.py --stage <rung>`.

---

## 11. MINOR — A live error message routes the operator to the flag that warns

**Evidence.** `project-trajectory/scripts/check.py:1545-1548`:

```python
sys.exit(
    "check: --strict applies only to --staged-divergence today (the "
    "plan's severity comes from --stage-cleared)"
)
```

`--stage-cleared` is the one flag spelling the program deliberately kept
*warning* (`check.py:1186-1207`, `_RETIRED_FLAG`) precisely because "it makes a
CLAIM about the axis … and that claim is the exact trap OI-51 retires".

**Failure scenario.** An operator hits this error, follows its advice, and is
immediately warned by the same program for using the spelling it just
recommended. The kit teaches the retired reading in its own remediation text.

**Fix (one line):** change `--stage-cleared` to `--stage` in that message.

---

## 12. MINOR — `Implements: SR-139` on the phase rule is a mis-trace

**Evidence.** `project-trajectory/scripts/derive_stage.py:361` — the
`phase_rule_findings` docstring closes with `Implements: SR-139`.

SR-139 is "Ratification as an ordinal over a derived spine stage" — it governs
the `human_ratification_through` dial and its fail-safe directions (see finding
5 for its text). The phase rule's obligation is "a spine edit that LOWERS the
effective stage must surface as a phase change" (plan §4, owner answer §6.1).
These are unrelated obligations at different tiers.

**Failure scenario.** `backlink-coverage` counts this declaration toward SR-139's
realization evidence, so a requirement about ratification authority accrues a
back-link from a function that does not implement it — inflating the coverage
percentage with a false edge and leaving the phase rule itself rowless.

**Fix (one line):** point the backlink at the row that actually carries the
phase-rule obligation, or mint one (the plan announced the rule; no SR names it).

---

## 13. MINOR — A dated attestation record now contains a different work item's drift

**Evidence.** `docs/ratify/2026-08-13-wi444.md` — filename dates it 2026-08-13
and names WI-444. Its current content:

> _Baseline: `docs/archive/last_approved` — copied **2026-08-20 (a5471e0f)** …_
> _Approval provenance: … is **1a7984ea (2026-08-21)** …_

followed by SR-049 / SR-140 / SR-170 / SR-173 sections — the WI-498 drift, with
nothing about WI-444. `c170da9f` added 77 lines to it.

`git log -- docs/ratify/2026-08-13-wi444.md` shows **ten** rewrites. This is
pre-existing machinery behavior (`ratify-fresh` regenerates the newest brief in
place), not something WI-498 introduced — I flag it because this program wrote
into it and because the brief asked for records the sweep touched.

**Failure scenario.** The attestation record for a given date is mutable until a
newer brief is minted, so "what was owed at WI-444" is unrecoverable from the
file that claims to record it. An auditor reading `2026-08-13-wi444.md` gets a
2026-08-21 answer.

**Fix (one line):** have `--ratify modified --check` regenerate an undated
`docs/ratify/CURRENT.md` and require a dated brief to be immutable once minted.

---

## 14. MINOR — The staleness message states a cause that is false in the common case

**Evidence.** `project-trajectory/scripts/derive_stage.py` `--check` failure
path. Observed output when I edited one declared input in a scratchpad copy of
HEAD:

```
derive_stage: docs/stage STALE — the derived stage moved but the cache did not.
```

followed by a `cached:` / `now:` pair in which **every derived value is
byte-identical** — `stage`, `stage-ord`, `floored`, `settled-stage`,
`live-stage`, `phase`, `per-phase`, `per-phase-live`, `drafted` all match. The
only field that differs is `fingerprint`.

The derived stage did NOT move. The fingerprint did.

This is not an edge case; it is the case the program says is normal. The banked
finding at `docs/log.d/2026-08-21-wi498-stage-unification.md:1538-1543` states
it outright: "an input edit that moves no stage value still reds `--check` —
correctly … the file goes stale strictly more often than its headline changes,
and that is the intended direction". So the message asserts "the derived stage
moved" precisely when the design expects it not to have.

**Failure scenario.** An author edits a requirement's prose, hits a red commit
bar, and is told the derived stage moved. They diff the printed `cached:`/`now:`
blocks, see identical values, and conclude the check is broken or the message is
lying — the two blocks are printed side by side specifically to be compared, and
they refute the sentence above them. The honest and more useful message is that
an input changed, so the recorded fingerprint has become a false claim.

**Fix (one line):** branch the message — "the derivation inputs changed" when
only `fingerprint` differs, "the derived stage moved" when a value differs.

---

## SUSPICIONS — raised, investigated, NOT established (deliberately unnumbered)

- **Inverse fingerprint defect, present tense.** I suspected something read but
  undeclared TODAY. Traced `load_spine` and the carrier suffix orders line by
  line: the six declared inputs are exactly what is read, in matching carrier
  order. No present-tense defect. (The absent GUARD is finding 7.)
- **`agent_common.py:901` `startswith("DevStg-")`.** A prefix test where
  membership was available — the class `kitlib/stage.py:222-228` says it
  retired. But the value reaching it has already passed `parse` →
  `_refuse_non_rungs` → `require_rung`, and `human_holds` re-tests membership
  with the human-held (safe) default. Not reachable as a defect; noted only.
- **`integrate.py:1611` `max(bars, key=_BAR_GATES.index)`.** Orders rungs by a
  private tuple index rather than `ladder.stage_ord`. Pre-existing, attached to
  the WI `bar:` frontmatter key the fragment explicitly DEFERRED (:1633-1644)
  with reasons I checked and accept. Out of range.
- **`traj_panels.py:939` `stage in span.split("→")`.** No tier highlights at
  `DevStg-Release`. Unreachable while nothing derives that rung — becomes real
  when WI-500 lands. Not a defect today.
- **Sweep damage to archived records.** I diffed every archive/log.d file
  `c170da9f` touched. The edits convert dangling markdown links into inline code
  spans (`[derive_gate.py:78](…)` → `` `derive_gate.py:78` ``), preserving the
  historical words exactly. This is correct restraint; I found no fourth bad
  hunk.
- **Smoke-budget over-run absorbed rather than reported.** I expected the 60 s
  ceiling to have been quietly widened or the breaches soft-pedalled. The
  opposite: `docs/stack.ini:443` states the "SECONDS budget stays 60 and is NOT
  touched here", `scripts/check_smoke_budget.py:19-32` volunteers the worst case
  against itself ("of 17 smoke wall times … 12 exceed 60 s (up to 142.9)" …
  "moving a budget to fit the machine it embarrasses is how a budget stops
  meaning anything"), CLAUDE.md reports the 54.9 / 64.0 / 55.7 spread including
  the breach, and `ac121647` labels its own 171.95 s reading "a loaded-box
  observation and NOT an argument to move the 60 s budget". Reported, not
  absorbed, at every surface I checked.
- **`check_vocab` alias tables by MEANING.** `check_vocab.py:143-149`
  (`[g1]`→`[DevStg-LLReqs]`, `[g2]`→`[DevStg-Impl]`) and
  `check_trajectory._ANCHOR_REACH:1834-1839` (`reqs`/`g1`→LLReqs,
  `tests`/`g2`→Impl) agree, and both are right by meaning: a phase that closed
  its reqs anchor has requirements settled, so LLReqs is what is in work. No
  inversion. (They are two separate declarations pinned to each other by
  nothing, which is a latent drift risk, not a current defect.)

---

## The three claims I tried hardest to refute and could not

**1. "The 15 flips were status-cells-only, and the re-seeded baseline is
byte-consistent with live."** (`ac121647`.) I attacked both halves. The registry
diff, filtered to changed lines across all three spine registries, is exactly
`15 -status = "Drafted"` / `15 +status = "Approved"` and nothing else — no row's
text moved in that commit. I then re-implemented the mirror invariant
independently rather than trusting the script: all 7 files under
`docs/archive/last_approved/` are byte-identical to their live counterparts.
`trace.py --ratify modified` at HEAD reports "No spine row differs from its
`docs/archive/last_approved` copy, and no row awaits a first approval", with the
baseline correctly re-stamped to `ac121647`. The act's mechanics are sound. (Its
*characterization* of the four blessed amendments is finding 2 — a different
claim.)

**2. "A stale committed `docs/stage` cannot survive a commit."** I looked for a
lane where the freshness step stands down. `derived-stage` is threshold
`DevStg-Needs` (`check.py:735`), i.e. selected at every rung including the
floor; it is in the pre-commit hook's batched floor by name
(`project-trajectory/hooks/pre-commit:270`); and CI runs the same `check.py`
invocations (`ci/check.yml:81,85,90`). I also confirmed the live file is
genuinely fresh at HEAD despite its `# computed 2026-08-22 (as-of a0e6f799)`
stamp being two commits behind — `derive_stage.py --check` exits 0, and the
stamp is deliberately excluded from the compared block (`kitlib/stage.py:371-382`),
so the apparent staleness is a documented non-defect. I could not construct a
committing path that skips the check.

**3. "The phase rule ships warn-first and deliberately unwired, and that is
honestly recorded."** This was my strongest expectation of an overclaim and it
did not survive contact. The exemption is the exact PAIR the owner ruled, not a
predicate over the Arch rung — `_EXEMPT_DECREASE = (STAGE_LLREQS, STAGE_ARCH)`
compared as a tuple at `derive_stage.py:372`, so a multi-rung drop ending at
Arch is not exempt and neither is `Arch → anything`. `grep -rn "phase-rule"`
across `project-trajectory/`, `docs/stack.ini` and `.github/` confirms it is
wired nowhere: it exists only in `derive_stage.py` and one RESYNC entry. And
that entry (`RESYNC_PACK.md:2842-2853`) states the posture without varnish: "It
**warns and exits 0**; `--strict` exits 1. It is **not wired into `check.py` and
cannot block a commit**, so **no action is required at re-sync**". The 26 tests
in `test_selection_at_or_above.py` + `test_phase_rule.py` pass. Honestly built
and honestly recorded.
