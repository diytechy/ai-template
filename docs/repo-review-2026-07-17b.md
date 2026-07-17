# Deep repository review (second pass) — 2026-07-17b

Scope: the full active repository — kit scripts, templates, skills, hooks, CI,
the meta-repo's self-adopted spine, tests, and documentation. Excluded as
historical working memory (per the review brief): `docs/log.md`,
`docs/archive/**`, `docs/iteration/**`, and the owner-only `OWNER_SCRATCHPAD.md`.

This pass follows the same-day review `docs/repo-review-2026-07-17.md` (report
`6ceb172`, remediation `3ee0a3b`). Rather than restating that report, this one
**verifies the remediated state and hunts for what it missed**. Findings that
review already recorded and deliberately deferred (coordinator complexity,
archive-backed WIs, license, orphan-doc noise, per-module coverage, dependency
bands, benchmark contract) are carried in §0, not re-argued in §3.

## 0. Unfixed items and why

Filled after the fix pass. Items from **this** review left unfixed:

| Item | Final state | Why it remains unfixed |
|---|---|---|
| M2 (part) — README "Configuration at a glance" is hand-maintained | Values corrected; mechanization deferred | The stale cells (`gate-policy`, seam count) are fixed, but making the table *generated or test-pinned* is a design decision: it either becomes another generated block (like the status snapshot) or gets a test that parses README prose. Both encode policy the owner should pick; a drive-by regex test over prose would be brittle. |
| L3 — `main()` signature and annotation drift across kit scripts | Left intact | 20 scripts use `main()`, 8 use `main(argv=None)`, one adds `-> int`. Harmonizing means touching 20 stable, working entry points for zero behavior change — churn the conservative-edit rule exists to prevent. Adopt `main(argv=None)` prospectively for new scripts. |
| L4 — `_disposition` reason-code prefix (`excluded:blocked:`) on `blocked`/`deferred` dispositions | Left intact | The codes are pinned by `tests/test_schedule.py` as a consumed contract (dashboard + dispatcher read them). Renaming for cosmetic prefix-consistency would break a stable machine-read vocabulary for no functional gain. |
| Carried from 2026-07-17 §0 — H3 (dispatcher complexity: `dispatch_run` still Ruff C901 = 84, re-confirmed this pass), H4 (archive-backed deferred WIs), H5 (no LICENSE — WI-097/OI-4), M5 (orphan-doc warnings), M6 (per-module coverage floors), M7 (Python floor / action majors), M8 (benchmark contract for the stale `~47 s / ~66 s` claims; measured full suite this pass: 103 s) | Still open | Each needs an owner policy ruling or a separately scoped campaign, as that report's §0 records. Nothing in this pass changed that calculus; re-fixing them opportunistically here would repeat the mistake that report explicitly declined. |

Fixes completed in this pass (details in §3):

| Finding | Disposition |
|---|---|
| H1 — exclusive-key starvation by an unclassified WI | Fixed: `_exclusive_conflicts` now only lets *schedulable* candidates claim a key; reserved holders unchanged. Regression test added. |
| M1 — no schema pin between `plan_artifacts.WI_HEADER` and the shipped template | Fixed: a test now reads `work-items.template.csv` and asserts equality with both `WI_HEADER` and the test fixture's header. |
| M2 (part) — README config table stale (`gate-policy`, seam count) | Fixed: table now reads `autonomous` and 61 seams, matching `docs/gate-policy` and `docs/requirements/interfaces.csv`. |
| M3 — status.md "Next action" cites a fixed defect as an open residual | Fixed: the hand-authored bullet now reflects the 2026-07-17 remediation (`ready --explain` fixed; blank-`SafetyClass` quarantine is the designed posture). |
| L1 — README misattributes the verification vocabulary to TC `Method` | Fixed: reworded to cite the SR `Verification` column; TC `Method` is the free-form "how to run". |
| L2 — WI-211/212 filed at the top of the id-ordered registry | Fixed: rows moved to the tail; dashboard/status regenerated. |

## 1. Executive summary

The repository is in the strongest state I can verify it has been in: the full
suite passes (**1,040 passed, 3 skipped, 103 s**), the default Ruff gate is
clean, the same-day remediation (`3ee0a3b`) is genuinely well-executed — the
header-aware CSV filer, the `blocked` lifecycle state (including the
staleness-policy rationale in `BACKLOG_STALE_STATUSES`), and the
`ready --explain` fix are all correct and tested — and the previously-flagged
evidence gap (Verified manual TCs with empty `Evidence`) is now empty when
re-queried. The verification culture is real: checks were re-run for this
report, not inferred.

What this pass found is a thinner but genuine layer of defects **underneath**
that green:

1. **A liveness bug in the new scheduler** (the one High): an unclassified WI —
   which by design can never be scheduled — can still *claim* an `Exclusive`
   mutex key, permanently starving a classified, ready WI that shares the key.
   Confirmed empirically; the live dispatcher consumes exactly this code path,
   and round-filed dual-plan children are *deliberately* unclassified until
   audited, making the collision realistic, not theoretical.
2. **Documentation drift in the exact places the kit promises none.** The README
   table that says of itself "checked against this repo's tree" asserts a
   `gate-policy` of `single-ratify` while the tree says `autonomous`, and counts
   51 seams where the registry holds 61. Nothing checks that table.
3. **The H1 failure mode can recur.** The remediation made the filer
   header-aware and taught the tests the modern 17-column header — but the test
   hardcodes its *own copy* of that header. No test reads the actual shipped
   template, so the next added column drifts all three surfaces apart silently
   again.

None of this dents the overall judgment: the architecture (pure cores, declared
policies, derived-not-declared state, fail-closed scheduling) is coherent and
unusually disciplined, and the deferred items from the first review remain the
real release-level work — above all the 84-complexity `dispatch_run()` and the
missing LICENSE for a kit whose stated purpose is being copied.

## 2. Evidence and method

Local evidence, 2026-07-17 (Windows 11, the pinned dev toolchain):

- `python -m pytest -q -n auto` — **1,040 passed, 3 skipped in 103.25 s**.
- `python project-trajectory/scripts/check.py --jobs 0` — full G3 gate, run for
  this review (result recorded in §5).
- `ruff check` (project rules) — clean. Extended census
  (`C901,PLR0912,PLR0915`): **94 findings**, largest `dispatch_run()` at
  complexity **84** — unchanged from the first review; carried as H3 there.
- The scheduler starvation was reproduced with a two-row in-memory registry
  (an unclassified and an ordinary WI sharing key `K`): both evaluate to
  `excluded`, the key held by the WI that can never run.
- Policy files were diffed against every "This repo" cell in README's
  configuration table; the spine CSVs were re-queried for the evidence-
  completeness gap the first review reported (now clean).
- The remediation diff (`3ee0a3b`) was read line-by-line against its six
  claimed fixes; all six are present and tested.

## 3. Prioritized findings

### Critical

None. No security exposure, data-loss path, or failing gate was found. The
secrets/privacy posture and the one documented `shell=True` boundary
(`run_menu.py`, executing the user's own declared `[run]` command) are unchanged
and honest.

### High

#### H1. An unclassified WI can hold an `Exclusive` key and starve classified ready work

**Location** — `project-trajectory/scripts/schedule.py:342-367`
(`_exclusive_conflicts`); consumed live at
`project-trajectory/scripts/agent_loop.py:4220` (`schedule.evaluate(wis, reserved)`)
and packed by `pack_traincars`.

```python
candidates = sorted(
    (
        w
        for w in wis
        if w["status"] == "queued"
        and w["id"] not in reserved
        and hard_preds_satisfied(w, status)
    ),
    ...
)
```

**Problem** — The candidate filter checks status, reservation, and
predecessors, but not the safety classification. The docstring says the key is
contested "among the WIs that would otherwise be ready" — but an unclassified
WI is *never* ready (it fails closed by design). Reproduced: with
`WI-001` (blank `SafetyClass`, key `K`) and `WI-002` (`ordinary`, key `K`),
`evaluate()` returns `WI-001 excluded [unclassified:missing, …]` and
`WI-002 excluded [excluded:exclusive-conflict:K@WI-001]`. The key is owned by a
WI the scheduler will never run; nothing ever releases it.

**Why it matters** — This is a deadlock-shaped liveness hole in the newest
orchestration layer, and the triggering condition is *the documented normal
state*: dual-plan rounds file children with a blank `SafetyClass` precisely so
they quarantine until audited. Any such child sharing a mutex key with
classified work silently freezes that work; the dispatcher's frontier just
shrinks with no human-facing explanation beyond a reason code on a WI nobody is
looking at. The exclusion is not even conservative — the mutex exists to
prevent *concurrent* execution, and a quarantined WI is not executing.

**Suggested improvement** — Require candidates to be schedulable
(`is_schedulable_class(classify(w)[0])`) before they may claim a key. Reserved
holders must keep their keys regardless (a live train is running, whatever its
row now says). Add a regression test for the unclassified-holder case.

### Medium

#### M1. Nothing pins `plan_artifacts.WI_HEADER` — or the test fixture — to the shipped template

**Location** — `project-trajectory/scripts/plan_artifacts.py:40-60` (`WI_HEADER`,
17 names), `tests/test_plan_artifacts.py:33-37` (`WI_HEADER_LINE`, a second
hand-typed copy of the same 17 names),
`project-trajectory/registries/work-items.template.csv:1` (the actual product
contract).

**Problem** — The first review's H1 existed because the filer and the template
disagreed and the tests used a private fixture that couldn't see the disagreement.
The remediation fixed today's *values* but reproduced the *structure*: there are
now three independently hand-maintained copies of the registry header and still
no assertion connecting any of them to the file adopters copy. `test_rule_sync.py`
exists precisely to pin duplicated logic pairs (the F5 rule's safety net); the
duplicated schema has no equivalent.

**Why it matters** — The next schema column repeats H1 silently: `WI_HEADER`
and the test fixture stay green together while the shipped template drifts. In a
repo whose core promise is that duplicated facts are mechanically pinned, this
is the one duplication the recent incident proved dangerous.

**Suggested improvement** — One test that reads
`registries/work-items.template.csv`'s header row and asserts it equals both
`pa.WI_HEADER` and the fixture's header. Three copies, one truth.

#### M2. README's "Configuration at a glance" contradicts the tree it claims to be checked against

**Location** — `README.md:294-313`. The table's preamble: "this table is the
map, checked against this repo's tree."

**Problem** — Two cells are false: `gate-policy` reads "**`single-ratify`** +
register" while `docs/gate-policy` declares `autonomous` (owner directive
2026-07-15, correctly reflected in `docs/status.md`); `interfaces-check` reads
"on — 51 declared seams" while `docs/requirements/interfaces.csv` holds 61 and
the generated status snapshot says 61. And the "checked against this repo's
tree" claim is itself prose — no test or generator touches this table.

**Why it matters** — `gate-policy` is a *consent* surface: it states who may
advance gates and whether an unattended loop pauses on open items. The repo's
front page telling a reader the loop pauses for single-ratify when it actually
runs autonomous misdescribes the safety posture, in the one document adopters
read first. It is also exactly the hand-maintained-copy drift the kit's own
philosophy (and this table's own preamble) promises against.

**Suggested improvement** — Correct both cells now. Separately decide how the
table stays true: fold it into the generated-status pattern, or add a check
that parses the `docs/…` column and compares declared values. (Deferred — see
§0.)

#### M3. `docs/status.md` "Next action" reports a fixed defect as an open residual

**Location** — `docs/status.md:59-67` (hand-authored, below the generated
marker).

**Problem** — The bullet lists "two recorded residuals worth triage as WIs",
one of which — "the `schedule.py ready --explain` text renderer's
duplicate-`reasons` formatting defect" — was fixed and regression-tested in
`3ee0a3b` hours before this review. The other (blank `SafetyClass` on round-filed
children) is no longer a defect to triage but the ratified fail-closed design
per that remediation.

**Why it matters** — `status.md` is the blackboard an unattended resume reads
*first*; the file's own header says only what must happen next lives here. A
fresh session (or the coordinator) acting on this bullet would re-open work that
is done — the precise failure the forward-only rule exists to prevent.

**Suggested improvement** — Rewrite the bullet to the current truth: migration
complete, remediation landed, frontier = the deferred backlog + owner items.

### Low

#### L1. README misattributes the verification vocabulary to the TC `Method` column

**Location** — `README.md:139` ("classified by `Method` (Test / Demonstration /
Inspection / Attest)"); contrast `PROCESS.md:411` and
`system-requirements.template.csv` (the `Verification` column holds that
vocabulary) and `test-cases.template.csv` / the meta-repo's own TC rows, where
`Method` is a free-form "how to run" sentence.

**Problem** — The classification lives on the SR tier; the README teaches
adopters to put it on the TC tier, where neither the schema check nor any script
reads it. Both the shipped template's example row and this repo's 76 real TCs
use `Method` as descriptive prose.

**Suggested improvement** — Reword to "each TC states its `Method` (how it
runs); the verification class (Test / Demonstration / Inspection / Attest)
rides the SR's `Verification` column."

#### L2. WI-211/212 filed at the head of the otherwise id-ordered registry

**Location** — `docs/requirements/work-items.csv:2-3`, ahead of WI-001.

**Problem** — All 210 other rows are in id order; the remediation inserted its
two new WIs at the top. No validator cares, but every human and diff-reader
does — the registry's convention is the implicit index.

**Suggested improvement** — Move the two rows to the tail and regenerate the
dashboard/status snapshot.

#### L3. Entry-point signature drift across kit scripts

**Location** — 20 scripts use `main()`, 8 (the newer ones) use
`main(argv=None)`; `check_dupes.py` alone adds a return annotation.

**Problem** — Purely stylistic, but the `argv=None` form is what lets tests
drive a CLI in-process, and the split reflects accretion rather than a rule.
Left unfixed (see §0); adopt the `argv=None` form prospectively.

#### L4. Scheduler reason-code prefixes are internally inconsistent

**Location** — `schedule.py:380-382`: a `blocked` disposition carries the code
`excluded:blocked:<ref>`; `deferred` likewise `excluded:deferred`, while
`reserved`/`waiting`/`done` use their own prefixes.

**Problem** — Cosmetic asymmetry in a machine-read vocabulary. Pinned by tests
as a consumed contract, so left unfixed (see §0).

### Positive / good practices (verified this pass)

1. **The remediation was engineering, not appeasement.** `blocked` was added
   with a thought-through staleness policy (`BACKLOG_STALE_STATUSES` includes
   `blocked` — parked work's cited requirements can still drift — with the
   rationale written at the constant). The filer rewrite handles legacy,
   modern, and absent headers with `DictWriter(extrasaction="ignore")` and
   preserves line-ending conventions, and the new tests cover both schema
   generations plus an end-to-end `check_trajectory --strict` pass.
2. **Fail-closed defaults are consistent** across the scheduler (`SafetyClass`
   absent ⇒ unclassified ⇒ never scheduled), the subagent gate (deny-by-default
   policies with an honest "supervision, not security" disclosure and
   fail-*open*-with-paper-trail where wedging tools would be worse), and the
   dangling-predecessor rule (an unknown edge counts as unsatisfied).
3. **Derived-not-declared state is real.** `derive_gate.py` computes the gate
   from artifact states with a compared `# basis:` line, a legacy-migration
   path, and G0-drop visibility; the status snapshot, dashboard, arch map, and
   OKF bundle are all freshness-gated generated views.
4. **The duplication that exists is a documented policy** (the F5
   independently-copyable-script rule) and — for *logic* — mechanically pinned
   by `test_rule_sync.py`. (M1 is the one place the pin is missing for
   *schema*.)
5. **CI matrix design is reasoned, not cargo-culted** — the macOS/3.8 exclusion
   comment explains exactly why the cell is redundant; the gate job explains
   why one platform suffices; the canary job floats unpinned deps on a schedule
   so the pins can't hide upcoming breakage.
6. **Tests read as specifications.** Docstrings name the SR/TC they verify,
   fixtures state their invariants ("smoke and slow PARTITION the suite"), and
   the suite's hermeticity scrub (`AGENT_*` env) documents the live incident
   that motivated it.

## 4. Overall recommendations and next steps

1. **Land the scheduler liveness fix first** (H1) — it is small, pure, and
   guards the exact configuration the dual-plan path produces every round.
2. **Pin the schema triangle** (M1) — one test, three copies, done. Consider a
   follow-up that runs the same pin over the other template headers the scripts
   re-declare (`check_trajectory.load_wis`'s expected columns, the TC/SR
   headers in `plan_coverage`), so schema drift anywhere fails a test somewhere.
3. **Stop hand-maintaining repo-state claims in README** (M2). Either generate
   the configuration table like the status block or test it; until then it will
   rot again, because it already has — twice, counting the seam count.
4. **Keep `status.md` forward-only in practice** (M3): make clearing the
   residual bullet part of closing the work it describes — the remediation
   updated the registry and the report but not the blackboard.
5. **Then return to the first review's §0 queue** — the dispatcher
   decomposition campaign (H3 there; complexity 84 re-confirmed here), the
   LICENSE ruling (H5/OI-4), and the archive-backed WI triage (H4) remain the
   substantive release blockers. Nothing found today changes their priority;
   today's findings are the last of the cheap correctness work in front of them.

Fitness against the stated vision: unchanged from the first review's verdict,
with the caveat now smaller — the structural/traceability machinery is
excellent and the newest orchestration layer is one small liveness fix away
from matching the rest of the kit's fail-closed-but-live discipline.

## 5. Final verification after the fix pass

Recorded after fixes: see the closing section appended below.
