# Owner questions of 2026-09-05 — answers, what was done, what is left to pick up

**Why this exists.** The owner asked seven questions during the review sitting
(item 1 was already answered) and asked for the answers to be saved as a report
so the work can resume in a later session. State when this was written: trunk
`contract_split`, the loop stopped under the tracked pause `docs/work/pause`.
Predecessor context: [handoff-2026-09-04.md](handoff-2026-09-04.md).

**How to read it.** One section per question. Each states the answer, the
evidence, what was DONE in this sitting (with the commit), and what is still
owed and by whom. Nothing here is a spine ruling; the open-item dispositions
in §6 are recorded in the registry itself when applied.

**Pick-up checklist (the short version):**

1. §5 — mint the writer-fix WI (spec drafted below; needs `trace.py --bump-ids`
   and a regen). The 16 stranded specs are already relocated (this commit).
2. §6 — rule OI-79/80/81 per their own recommendations; hand-fill
   options/recommendation on OI-82/83/84 (drafted below); fix the OI mint's
   title clip in `intake._mint_open_item`; regenerate `docs/open-items.html`.
3. §2 — no estimator WI. One small instrument WI: put the routed tier and the
   `agents.toml` row id in the session-log header. The measured basis is
   Appendix A.
4. §3 — one optional WI: a stdlib `check_escapes.py` ratchet (the one idea
   worth porting from `cleat`).
5. §4 — one optional WI: the `{open_rows}` slot and an `EXTEND` outcome on the
   disposition brief.

---

## 2. Can the required worker tier be estimated from history, and automated?

**Answer: measured, and the answer is no — not from today's data, and not for
the reason you would expect.** The data pull ran over the 48 work items merged
since 2026-08-15 (session telemetry headers, round files, scoreboards, spec
frontmatter, git subjects). The blocker is not sample size. It is that the
features available BEFORE work starts carry no signal, and the outcome being
predicted is currently measuring the reviewer rather than the worker.

**The one honest ex-ante feature has zero correlation.** Spec body size
measured at CLOSE correlates with churn (Spearman +0.50), but the spec body is
written BY the work: WI-580 went from 29 words at mint to 1298 at close,
WI-595 from 29 to 2867. Re-measured at the mint commit, which is the only
value a router could actually read:

| pair (mint-time) | population | Spearman |
|---|---|---|
| mint body words vs CHANGES-REQUESTED | all 48 | +0.10 |
| mint body words vs CHANGES-REQUESTED | 21 build rows | −0.14 |
| mint body words vs review rounds | 21 build rows | −0.16 |

Everything that does correlate — turns, output tokens, cost, wall time
(+0.34 to +0.54) — is measured DURING the work. Those are a stopping signal,
never a starting one.

**Kind separates; the assigned tier is anti-correlated with success.**

| kind | n | review rounds | CHANGES-REQUESTED | reworks |
|---|---|---|---|---|
| adjudication | 10 | 3.90 | 3.00 | 2.90 |
| build | 21 | 3.19 | 2.10 | 1.48 |
| disposition | 12 | 2.33 | 0.83 | 0.50 |
| spot-check | 5 | 0.80 | 0.20 | 0.00 |

| assigned buildtier | n | review rounds | CHANGES-REQUESTED | P(≥2 CR) |
|---|---|---|---|---|
| medium | 23 | 2.09 | 1.00 | 26% |
| strong | 24 | 3.67 | 2.54 | 50% |

Strong-tier rows fail review MORE. That is selection, not causation — strong
is already assigned to the hard rows — but it says the existing assignment
already captures most of the ex-ante difficulty signal, and that raising the
tier is not visibly buying fewer rounds. A naive fit would learn
"strong causes churn" and recommend downgrading.

**The label is corrupted right now.** Handoff 09-04 §4 measured it: single-MINOR
refusals cost four rounds in one day, record-only reworks two more, and every
rework rewrote prose that the next round then faulted. Until CHANGES-REQUESTED
requires a MAJOR or BLOCKER (churn-program item 1, landed but not yet run for
long), round count measures the review threshold, not worker capability.

**Ground truth is n = 3.** Across the repo's entire history of 36 scoreboards,
`agent_route.escalate()` has fired a tier-up exactly three times — all
medium→strong at round 4, and in all three the next round approved. A reactive
mechanism that costs about two extra rounds on roughly 6% of rows is a weak
thing to replace with a predictor that would be wrong more often than that.

**Three instrumentation gaps found, each worth fixing on its own merits.**

1. **The routed tier is absent from telemetry.** The session-log header carries
   `model` and `effort` but no tier and no `agents.toml` row id — and
   `ANTHROPIC-OPUS-STRONG` and `ANTHROPIC-OPUS` are the same model on two
   rows. So no artifact in the repo can tell you whether a given Anthropic
   session ran strong or medium. This is the single biggest blind spot.
2. **`est_tokens` is a declared but dead field.** It is a real optional key
   (the WI-000 exemplar, `schedule.py`, `registry.py`) and ZERO live or
   archived specs set it. The scope estimate an estimator would most want does
   not exist. Populate it or delete it.
3. **No per-close record for a SUCCESSFUL merge.** `dispatch.py`'s
   `suggested_tier` and the typed close report exist only for partial closes
   (`docs/handbacks/` holds five files, all partials). Telemetry also joins on
   the LANE, so a four-row batch replicates one measurement four times.

**What the kit already does, for the record.** Phase defaults with
unknown-routes-up (`agent_loop.DEFAULT_PHASE_TIER`); the per-row `buildtier`
pin; tier-up-never-down in selection (`agent_route.TIER_ORDER`); reactive
win-stay/lose-shift escalation — swap family after two consecutive
CHANGES-REQUESTED, tier up only after the swap also fails, page the human
after two top-tier failures (`agent_route.escalate`); and one mint-time
estimator, `intake.tier_signal`, deriving `buildtier` from rows touched and
stage delta. PROCESS_OPTIONS.md also states the doctrine explicitly: "A fixed
escalation policy, not a learned router (per-project sample sizes are far too
small for a bandit)." Any estimator proposal must argue against that line, not
around it.

**Recommendation: no estimator WI. One small instrument WI, worth doing
regardless.** Add the routed tier and the `agents.toml` row id to the
session-log header (one entry in `agent_common`'s key list plus the value at
the `agent_loop` call site). If that lands and the analysis is still wanted,
a second slice appends a per-close outcome row at the merge slot (id, kind,
start tier, needs count, mint body words, rounds, CHANGES-REQUESTED count,
escalated yes/no) to a generated outcomes CSV under `docs/reviews/`. Revisit the
estimator itself after roughly 60 to 80 merged build rows AND after the review
threshold fix has been in force long enough to clean the label. If it is ever
built, it should feed `intake.tier_signal` as a declared kind-keyed base-rate
table — a measured prior, not a model — and there should be no
`recommended_tier` field beside `buildtier`, which is already the one home for
where a row starts.

The per-WI table this rests on is Appendix A.

## 3. Should `svetdev/cleat` or `a-dithya-b/agent-native-cli` be consumed?

**cleat — PORT ONE IDEA, do not adopt.** MIT, Python 3, five days old at
evaluation (first commit 2026-08-31, v0.0.1, ~22 stars). It is structurally
the layer this kit already ships as `check.py`: a gate orchestrator over
ratcheted checks with a baseline that fails only new debt. Its complexity,
duplication and coverage gates lean on external tools (`lizard`, `jscpd`,
`llvm-cov`), which the dependency ledger's shipped tier rules out, and it
gates duplication, which this repo tore down on measured evidence (D-7).
Windows support is unverified. The one gap it exposes that is worth closing:
**an escapes ratchet** — a count of `# noqa`, `# type: ignore`,
`pytest.mark.skip` and similar suppressions against a stamped baseline, so new
suppressions fail while existing ones are recorded once. The kit ratchets
complexity, module size, smoke budget and coverage floors, but nothing watches
the hatches those ratchets can be evaded through. Hook: a stdlib
`check_escapes.py` beside the other checks, wired as `[step:escapes]` in
`docs/stack.ini` beside `[step:complexity]`, report-only downstream, armed here
once its false-positive rate is known. Two cheaper follow-ons, each its own
WI if wanted: generalise `check_vocab.py` into a config-driven conventions
table; promote the hard-coded byte caps in `tests/test_bootstrap.py` into a
shipped doc-size step (the byte-budget-guard skill already carries the
measurement that justifies it).

**agent-native-cli — IGNORE.** MIT, a single portable `SKILL.md` (not
software), ten days old, ~16 stars, distributed via `npx skills add`. Its
thesis — deterministic tooling behind single semantic commands, compact
parse-stable output, exit codes as status — is already the kit's operating
design (`check.py`, `run_menu.py --list`, `trunk_step.py`, `integrate.py`).
Its headline token-reduction figures are n = 1 repository, 1 model, 3 rounds,
self-disclaimed as non-generalising. Optional: one row in
`project-trajectory/EXTERNAL_SKILLS.md` under "Evaluated and not listed."

## 4. Should consolidation happen at WI close, through the closing adjudicator?

**Assessment.** The kit already does half of this and deliberately not the
other half, and the plan of record says why
([plans/2026-09-02-backlog-restructure-and-consolidation.md](plans/2026-09-02-backlog-restructure-and-consolidation.md)
§1.3). Today: a closing adjudication row drafts its successors in
`## Dispositions`, and `intake._disposition_drafts` mints them at the merge;
consolidation is a SEPARATE census-triggered `consolidate` row minted from
`dispatch._admit` when the station is idle and no adjudication is queued,
guarded by a queue digest so a judged queue state is never judged twice.

**Why the census is not at the close.** (a) The closing lane sees its own
lane's registry, not the trunk queue the census reads at admit, so a
close-time merge would judge against a stale queue. (b) The mechanical close
is peelable from the verdict identity ONLY because it moves exactly the judged
specs and creates or destroys nothing else (`kitlib.verdict._closed_wi_ids`);
a close that also rewrote other queued rows would widen the write set the
peel is allowed to ignore. (c) Overlap arises between independently minted
rows too (gap census, spot checks, amendment adjudications), which a
successor-only check never sees. (d) The drafter judging its own successors is
self-review.

**What the owner's idea DOES buy, and the cheap version of it.** The
disposition brief today does not show the drafter the open rows it might
extend, so it drafts a new row where "add a Done-when line to WI-x" was the
right answer. Two small changes get most of the benefit without moving the
census: give `adjudicate-disposition.template.md` the `{open_rows}` slot the
consolidate brief already has (`adjudicate_brief._other_open_rows`), and add
one disposition outcome, `EXTEND <id>`, that appends the drafted Done-when to
an existing queued row at the mint instead of minting a new one. Contradiction
checks at close already happen: `check_trajectory.queue_conflict_findings`
runs on the composed tree at the refresh. Net: the detriment the owner
anticipated (self-judged, stale-queue merges) is real; the benefit is
recoverable with an `{open_rows}` slot and an `EXTEND` outcome. Recommend a
WI for those two only, not for moving the census.

## 5. Completed work items outside `archive/` — is it captured anywhere?

**No WI captured it; it is a kit defect, and the visible half is fixed in
this commit.** WI-504 (OI-55 ruled (a), 2026-08-22) moved terminal history to
`docs/archive/work/{complete,cancelled,partial,restructured}/`, and
`kitlib.registry.spec_roots` reads both roots so nothing broke — which is why
nothing noticed that TWO of the three mechanical writers never followed:

| Writer | Destination today | Should be |
|---|---|---|
| `handback._close_adjudication_one` (the mechanical adjudication close) | `docs/work/complete/` (`handback.py` ~line 803, `integrate.WORK`) | `docs/archive/work/complete/` |
| `handback.close_partial` (the worker exit-4 partial close) | `docs/work/partial/` (`handback.py` ~line 445) | `docs/archive/work/partial/` |
| `consolidate.archive_absorbed` | `docs/archive/work/restructured/` | correct |
| the worker's own clean close (`prompts/worker.template.md`) | `docs/archive/work/complete/` | correct |

Plus the verdict peel reads the old path: `kitlib.verdict._COMPLETE_SPEC` and
`_WORK_PREFIX` recognise a mechanical close only when the additions land under
`docs/work/complete/`; if the writer is fixed without the reader, every
mechanical close stops peeling and stales its own round (the WI-586 failure,
back). Nineteen test files pin `docs/work/complete/`.

**Done in this commit.** The 12 `complete/` and 4 `partial/` specs stranded
under `docs/work/` were moved with `spec_move.py` (link-aware; two inbound
links re-pointed). `docs/work/complete/` and `docs/work/partial/` now hold
only their README pointers. Prose mentions of the old paths inside closed
specs are historical record and were left alone.

**Owed: one WI (not yet minted — the watermark is at WI-604, so it is WI-605).**
Draft, to file under `docs/work/queued/`:

```
+++
id = "WI-605"
title = "The mechanical closes file terminal rows under docs/archive/work/, and registry-integrity errors on a spec left in docs/work/<terminal>"
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
priority = 6
safety_class = "ordinary"
+++

## Context

WI-504 relocated terminal history under docs/archive/work/, and
kitlib.registry.spec_roots tolerates both roots "until a repo's own move
commit lands". Two mechanical writers never moved: handback.close_partial
writes docs/work/partial/ and handback._close_adjudication_one writes
docs/work/complete/. Sixteen rows accreted there between 2026-08-26 and
2026-09-05 and were relocated by hand on 2026-09-05
(docs/decisions-for-review-2026-09-05.md §5). The owner's intent (2026-09-05):
docs/archive/ holds ALL history, so only the spine defines living
expectations and a closed row cannot be mistaken for how things work today.

## Done-when

1. Both handback writers file into kitlib.registry.spec_archive_dir(...)
   (complete/, partial/), and consolidate.archive_absorbed keeps doing so;
   one shared helper names the destination — no second path constant.
2. kitlib.verdict.mechanical_close_attestation recognises the archive
   destination (the _COMPLETE_SPEC / _WORK_PREFIX pair), still refuses any
   A/D outside "active/<branch>/ -> archive/work/complete/", and a test drives
   a real close on a scaffold repo through the peel.
3. trace.py --strict-integrity ERRORS on any WI-*.md under
   docs/work/{complete,cancelled,partial,restructured}/ (README pointers
   exempt), so the tolerance in spec_roots is a migration device with a
   detector, not a permanent second home.
4. The 19 tests pinning docs/work/complete/ are re-pointed; docs/work/README.md
   and the WI-000 exemplar already state the archive paths and need no change.
5. RESYNC_PACK.md entry: adopters with rows stranded under docs/work/<terminal>
   get the move recipe (spec_move.py per file) and the new integrity error.
```

## 6. The open items: heading cut off, and which to keep

**The heading defect is in the data, not the CSS.** `intake._mint_open_item`
writes `title = _clip(question, 100)` — a mid-sentence clip of the one_line —
and the card renders that. OI-82/83/84 end in `…` at exactly 100 characters;
OI-79/80/81 were hand-authored to 100 characters with no ellipsis. Fix: derive
the title from the question's first sentence (split on `. `, `? `, `: `) and
clip only if that is still over 100; repair the six live titles by hand. This
is a kit change (test in `tests/test_intake.py`, RESYNC entry). Not done yet.

**Census.** 76 rows, 69 ruled, 6 pending. Rulings are recorded as
`status = "ruled"`, `ruled_date`, `ruling_ref` (a `docs/log.d/` fragment since
2026-08-18), and the house prose prefix `RULED (<option>) <date> — …` on
`one_line` and `decision`, original text preserved. After a ruling:
`python project-trajectory/scripts/trunk_step.py --regen` (the open-items
page and the status projection), and `check.py` runs `gen_open_items.py
--check` as a freshness gate. Nothing mechanical requires `ruled_date` or
`ruling_ref`; only the status flip is read (by the scheduler and the renderer).

**Dispositions, applying the owner's rule (rule the peripheral ones per their
own recommendation; retain only what touches core functionality or vision):**

| OI | Class | Disposition | Owner act remaining |
|---|---|---|---|
| OI-79 remote `-HELD-` ref | peripheral | RULE (a) delete. Guard verified this sitting: `git merge-base --is-ancestor fa3c99c4 contract_split` returns 0. | the delete is a push: `git push origin --delete wi508-architectural-remap-HELD-for-owner-verdict` (tag first if a pointer is wanted) |
| OI-80 OI-72's "four Drafted rows" | peripheral | RULE (b) append a dated correction line to OI-72's `decision` cell: "Correction 2026-09-05: LLR-203/LLR-204 were already Approved (580df781); only TC-199/TC-200 were Drafted." | none |
| OI-81 publication cadence | peripheral, one irreversible arm | RULE (c) then (a) after OI-44. Read done this sitting: `wi416-parked-handback-contract` is ONE commit ahead of trunk (`7372e239`, "park: WI-416's proposed disposition, mid-flight and NOT ruled" — 3 files, +344), the only single-copy content. | tag it (`git tag wi416-parked-2026-08 7372e239`) and delete the local branch; merge to main + push stays the owner's, after OI-44 is re-answered |
| OI-82 approval brief narrows to held rungs? | **core** | RETAIN. WI-577 already carries it (`needs = ["OI-82"]`). Fill options + recommendation: (a) narrow the brief to the rungs the dial holds, with a collapsed "delegated to adjudicators" section listing released-rung Drafted chains by id (sight without signature); (b) keep rendering every Drafted chain. Recommend (a): the sitting shows what the owner owes a signature on, and the delegated set stays visible. | rule it; WI-577 then leaves the frontier's waiting state |
| OI-83 coordinator runs stale modules | **core** | RETAIN. Fill options: (a) detect and exit — record a digest of `project-trajectory/scripts/**/*.py` at launch, recompare each tick, on drift finish the tick and exit with a distinct code so the launcher relaunches; (b) in-process re-exec (unsafe across an imported package graph); (c) operating rule only (what already failed on WI-579 round 033). Recommend (a). | rule it; then a WI against `agent_loop.py` |
| OI-84 `default_base` blind on a resumed single-checkout worker | **core** | RETAIN. Fill options: (a) durable base — the claim records its integration base (trunk sha at claim) and `default_base` reads it, falling back to the merge-base only when absent, so all four readers share one answer; (b) each reader carries the "cannot say" the way round 034's fix did. Recommend (a). Pair with OI-83 (an exit-and-relaunch re-derives the base). | rule it; then a WI against `agent_loop.py` |

WI-570 (typed open-item brief, on the ready frontier) is what makes the thin
machine-minted brief unrepresentable going forward; OI-82/83/84 are its
motivating instances.

**Not touched, and why.** The 23 spine rows owing an approval or re-attest
on `docs/open-items.html` are the human-approval gate
(`docs/process.toml [attestation] human_approval_through`), not open-item
briefs; approving them is a reviewed Status-change commit plus `intake.py
snapshot`, and the owner did not delegate that.

## 7. The hand-touched watermarks — do adopters get these checks?

**Yes, at the script level; the pytest pins are this repo's only.** Two
files were touched near the end of the 09-04 run:

- `docs/id-watermark` (IF 176 → 179) was regenerated by `trace.py
  --bump-ids`, not edited by hand; the file's header says so and
  `trace.watermark_findings` refuses a lowered mark, a live id above its mark
  or a missing space. It runs inside `trace.py --strict-integrity`, which
  `check.py` runs as the `registry-integrity` step from DevStg-Reqs upward and
  the pre-commit hook runs on every commit. Adopters get all of that;
  `bootstrap.py` seeds the file and refuses to overwrite it.
- `docs/if-tc-coverage-allow` (+3 rows with reasons) IS a hand edit by design:
  it is the migration allowlist for IF seams cited by no TC.
  `check_trajectory.if_tc_coverage_findings` errors under `--strict`
  (DevStg-Tests and above) on any uncited seam not listed, a listed entry
  without a reason suppresses nothing, and `if_tc_allow_hygiene_findings`
  reports growth and stale entries. All shipped. An adopter with no file gets
  "absent = empty = every uncited seam errors."

What is NOT shipped is the test that pins the 118-id seed set
(`tests/test_trajectory_arch.py`) and the ratchet tests (module size,
complexity baseline, smoke budget). Those test the kit, not the adopter's
repo, and that split is deliberate: the kit's own tests are not the adopter's
bar, the shipped `check.py` steps are. No gap to close for item 7.

---

## What this sitting committed

- The 16 stranded terminal specs relocated into `docs/archive/work/` (§5).
- This report.

## What is left, in order

1. §5 WI-605 mint (spec above): write the file, `python
   project-trajectory/scripts/trace.py --bump-ids`, `python
   project-trajectory/scripts/trunk_step.py --regen`, commit.
2. §6 rulings and brief fills, the OI-72 correction line, the title fix in
   `intake._mint_open_item` with its test and RESYNC entry, regen, commit.
   Record the rulings in one fragment under `docs/log.d/`, named
   `2026-09-05-owner-rulings-oi79-80-81.md` (heading `## 2026-09-05 — …`).
3. §3 optional WI: `check_escapes.py`.
4. §4 optional WI: `{open_rows}` in the disposition brief + `EXTEND` outcome.
5. §2 instrument WI: the routed tier and `agents.toml` row id in the
   session-log header. Revisit the estimator itself only after roughly 60 to 80
   merged build rows and after the review-threshold fix has cleaned the label.

---

## Appendix A — the 48 work items merged since 2026-08-15

Extracted from session telemetry headers (`docs/iteration/*.log`), round
files and scoreboards under `docs/reviews/`, spec frontmatter, and git
subjects. `words@close` is the spec body AT CLOSE, which is why it
correlates and why §2 re-measured at the mint commit instead. Rows with
no wall time were built out of band or by hand, so no session log exists.
A batched lane (WI-569/575, and WI-584/587/588/589) reports the LANE's
wall time and cost against each of its rows — telemetry joins on the
branch, not the row.

| WI | merged | kind | tier | class | needs | words@close | rounds | CR | findings | reworks | err | wall s | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WI-451 | 2026-08-15 | disposition | strong | spine | 0 | 333 | 0 | 0 | 0 | 0 | 0 | — | — |
| WI-484 | 2026-08-30 | build | strong | spine | 0 | 1817 | 0 | 0 | 0 | 0 | 0 | — | — |
| WI-508 | 2026-09-01 | build | strong | spine | 3 | 4399 | 12 | 11 | 25 | 5 | 0 | 5508 | 16.09 |
| WI-521 | 2026-08-30 | build | strong | ordinary | 0 | 3929 | 0 | 0 | 0 | 0 | 3 | 9174 | 10.06 |
| WI-535 | 2026-08-30 | adjudication | quick | ordinary | 0 | 588 | 2 | 1 | 1 | 0 | 0 | 4166 | 12.09 |
| WI-537 | 2026-08-30 | build | strong | spine | 0 | 968 | 3 | 2 | 5 | 1 | 1 | 6648 | 21.26 |
| WI-538 | 2026-08-31 | build | medium | ordinary | 2 | 914 | 7 | 4 | 6 | 1 | 0 | 8269 | 16.69 |
| WI-540 | 2026-08-31 | adjudication | strong | ordinary | 1 | 514 | 0 | 0 | 0 | 1 | 0 | — | — |
| WI-542 | 2026-08-30 | disposition | medium | adjudication | 0 | 602 | 1 | 0 | 0 | 0 | 0 | 986 | 3.85 |
| WI-543 | 2026-09-01 | build | strong | spine | 0 | 1046 | 3 | 2 | 3 | 2 | 2 | 6924 | 7.47 |
| WI-544 | 2026-08-30 | disposition | medium | adjudication | 0 | 487 | 4 | 3 | 5 | 0 | 0 | 187 | 0.99 |
| WI-546 | 2026-08-30 | build | medium | spine | 0 | 323 | 4 | 3 | 4 | 3 | 0 | 3048 | 22.43 |
| WI-547 | 2026-08-30 | disposition | strong | adjudication | 0 | 1338 | 5 | 1 | 1 | 0 | 0 | 273 | 0.94 |
| WI-548 | 2026-08-30 | build | strong | ordinary | 0 | 740 | 5 | 4 | 5 | 4 | 0 | — | — |
| WI-549 | 2026-08-30 | spot-check | medium | adjudication | 0 | 295 | 1 | 0 | 0 | 0 | 0 | 285 | 1.87 |
| WI-550 | 2026-08-31 | disposition | medium | adjudication | 0 | 407 | 2 | 0 | 1 | 0 | 0 | 364 | 2.07 |
| WI-552 | 2026-09-01 | adjudication | strong | ordinary | 0 | 740 | 3 | 1 | 7 | 3 | 4 | 10952 | 29.73 |
| WI-553 | 2026-09-01 | build | medium | ordinary | 0 | 691 | 2 | 1 | 5 | 3 | 0 | 6631 | 72.81 |
| WI-554 | 2026-09-01 | build | medium | ordinary | 0 | 630 | 1 | 0 | 0 | 0 | 0 | 1658 | 9.51 |
| WI-555 | 2026-09-01 | build | strong | spine | 1 | 875 | 4 | 2 | 15 | 2 | 0 | 2167 | 9.98 |
| WI-563 | 2026-09-01 | spot-check | medium | adjudication | 0 | 1438 | 2 | 1 | 6 | 0 | 0 | 284 | 1.72 |
| WI-566 | 2026-09-01 | disposition | strong | adjudication | 0 | 713 | 2 | 1 | 5 | 1 | 0 | 151 | 1.0 |
| WI-567 | 2026-09-01 | build | medium | ordinary | 0 | 393 | 1 | 0 | 0 | 0 | 0 | 585 | — |
| WI-568 | 2026-09-01 | disposition | strong | adjudication | 0 | 1361 | 5 | 3 | 13 | 3 | 1 | 1185 | 2.49 |
| WI-569 | 2026-09-02 | build | strong | spine | 2 | 2120 | 4 | 3 | 8 | 3 | 0 | 2383 | 14.93 |
| WI-571 | 2026-09-01 | build | medium | ordinary | 0 | 808 | 3 | 2 | 5 | 1 | 0 | 5473 | 25.28 |
| WI-572 | 2026-09-02 | adjudication | strong | ordinary | 1 | 1296 | 10 | 8 | 23 | 6 | 3 | 21427 | 45.88 |
| WI-573 | 2026-09-02 | disposition | medium | adjudication | 0 | 770 | 3 | 1 | 3 | 1 | 0 | 332 | 3.31 |
| WI-574 | 2026-09-02 | spot-check | medium | adjudication | 0 | 1921 | 1 | 0 | 3 | 0 | 0 | 1381 | 4.74 |
| WI-575 | 2026-09-02 | build | medium | spine | 0 | 886 | 4 | 3 | 8 | 0 | 0 | 2383 | 14.93 |
| WI-578 | 2026-09-03 | disposition | medium | adjudication | 0 | 1032 | 3 | 1 | 3 | 1 | 0 | 420 | 4.65 |
| WI-579 | 2026-09-03 | adjudication | strong | ordinary | 0 | 5083 | 11 | 10 | 29 | 11 | 5 | 38189 | 125.4 |
| WI-580 | 2026-09-05 | build | medium | ordinary | 1 | 1254 | 5 | 4 | 15 | 4 | 2 | 7494 | 29.55 |
| WI-583 | 2026-09-05 | adjudication | strong | ordinary | 2 | 697 | 0 | 0 | 0 | 1 | 0 | — | — |
| WI-584 | 2026-09-04 | build | medium | spine | 0 | 1209 | 1 | 0 | 0 | 0 | 1 | 15815 | 13.24 |
| WI-585 | 2026-09-03 | disposition | medium | adjudication | 0 | 242 | 1 | 0 | 0 | 0 | 0 | 500 | 4.01 |
| WI-586 | 2026-09-03 | adjudication | strong | adjudication | 0 | 2127 | 6 | 5 | 10 | 0 | 0 | 6092 | 29.32 |
| WI-587 | 2026-09-04 | build | strong | spine | 0 | 1959 | 1 | 0 | 0 | 0 | 1 | 15815 | 13.24 |
| WI-588 | 2026-09-04 | build | strong | spine | 0 | 734 | 1 | 0 | 0 | 0 | 1 | 15815 | 13.24 |
| WI-589 | 2026-09-04 | build | strong | spine | 0 | 414 | 1 | 0 | 0 | 0 | 1 | 15815 | 13.24 |
| WI-590 | 2026-09-04 | adjudication | strong | adjudication | 0 | 1782 | 7 | 5 | 10 | 4 | 4 | 10426 | 13.35 |
| WI-591 | 2026-09-04 | spot-check | medium | adjudication | 0 | 1272 | 0 | 0 | 0 | 0 | 0 | 1187 | 1.87 |
| WI-592 | 2026-09-04 | spot-check | medium | adjudication | 0 | 730 | 0 | 0 | 0 | 0 | 0 | 1094 | 3.42 |
| WI-593 | 2026-09-04 | disposition | medium | adjudication | 0 | 230 | 1 | 0 | 0 | 0 | 0 | 161 | 1.14 |
| WI-594 | 2026-09-04 | adjudication | strong | adjudication | 0 | 336 | 0 | 0 | 0 | 3 | 0 | 389 | 3.48 |
| WI-595 | 2026-09-04 | build | strong | spine | 0 | 2827 | 5 | 3 | 7 | 2 | 0 | 11202 | 15.54 |
| WI-599 | 2026-09-04 | disposition | medium | adjudication | 0 | 216 | 1 | 0 | 0 | 0 | 0 | 486 | 3.72 |
| WI-600 | 2026-09-04 | adjudication | medium | adjudication | 0 | 189 | 0 | 0 | 0 | 0 | 0 | 326 | 3.02 |
