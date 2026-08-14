# WI-442 — REVIEW-A (2026-08-14)

**Reviewer:** OPENAI-TERRA (`gpt-5.6-terra`, medium effort) via the `codex`
CLI — cross-family, fresh context each round, independent of the lane builder.
Model: gpt-5.6-terra. Charter:
[code-review-adversarial](../rubrics/code-review-adversarial.md). Given the
branch diff (`infra/mechanized-loop...wi442-external-schema`, ~156 files,
+1990/−379 at round 1's tip 75d7d080) and the requirement surface: the WI-442
row's frontmatter clause list
(`docs/work/complete/WI-442-oi-28-seeds-landed-on-the-spine.md`), the sitting-2
rulings it executes (`docs/plans/2026-08-13-sitting-2-boundary-and-context.md`
§1R, decisions 3/4/5/12 and the DESIGN-IT-IN hazard table), and the lane plan
brief (`docs/plans/WI-442-external-frame-and-approval-schema.md`). The spec's
`## Deliverable` prose is the implementer's own account and was supplied only
as claims-to-verify, never as evidence; no other self-assessment was shown.
Run under `--sandbox workspace-write` with an out-of-repo scratchpad; each
round's drives left `git status --porcelain` clean. Machine-local absolute
paths in the reviewer's output are rewritten repo-relative (`<scratch>` = the
session scratchpad); nothing else in the verdicts is edited. Two earlier
ad-hoc reviews of this WI reviewed superseded snapshots and were never verdict
artifacts; this is the fresh verdict round the merge gate requires. Findings
were re-verified by the session author against the real tree before any fix
(the author-re-verifies convention); every finding below reproduced.

**Final verdict: APPROVE at round 2849616e (the round-2 fix commit)** — round 1 CHANGES-REQUESTED
(1 MAJOR, gen_okf exporting the retired column), round 2 CHANGES-REQUESTED
(1 MAJOR, shipped docs still teaching the retired column), round 3 APPROVE on
the fixed tip. The machine line that governs is the last one in this file.

---

## Round 1 — at 75d7d080 (CHANGES-REQUESTED, 1 MAJOR)

WI-442 introduces the depth-0 external frame and approval migration across
persisted registries, scaffold templates, gate derivation, trace enforcement,
and generated documentation. Its blast radius includes every adopter scaffold,
rung-1 stage computation, strict trace output, the 113-row IF registry, and
downstream resync; the requirement is the WI-442 title plus sitting-2
§1R/decisions 3–5 and 12.

### Failure classes hunted, worst-first

1. Silent rung-1 corruption or wrong applies-when behavior.
2. Strict trace false-greens, including dangling frame/tie-back/SR references
   and malformed TOML.
3. Disarmed regression tests and approval-authority tripwire.
4. Scaffold/template/resync and generated-output schema drift.
5. Held `direction`/`counterpart` clause, dashboard/SR-091 dependency, and
   absorbed row dispositions.

### Exact commands and driven output

1. `derive_gate.py --root <scratch>/allapproved`
   `stage=DevStg-Needs stage-ord=0` — all six approved crossings release
   Boundary.
2. `derive_gate.py --root <scratch>/onedraft`
   `stage=DevStg-Boundary stage-ord=1` — one draft crossing holds Boundary.
3. `derive_gate.py --root <scratch>/noframe`
   `stage=DevStg-Needs stage-ord=0` — no `external.toml` skips the optional
   rung.
4. Mutated scratch `external.toml`, IF tie-back, and SR `Boundary-Refs`, then
   ran `trace.py --strict`:
   `FINDING (frame): boundary B-01 Entity references unknown EXT-999`
   `FINDING (frame): IF IF-020 InterfaceToExternal references unknown crossing B-99`
   `FINDING (frame): SR SR-091 Boundary-Refs references unknown crossing B-99`
   `exit=1`
5. Malformed scratch `external.toml`, then ran `trace.py --strict`:
   `spine_carrier: docs/requirements/external.toml does not parse as TOML — refusing to report an unreadable registry as an empty one`
   `trace-exit=1`
6. `bootstrap.py --dest <scratch>/bootstrap442`, then
   `derive_gate.py --root <scratch>/bootstrap442`:
   `created: docs/requirements/external.toml`
   `stage=DevStg-Needs stage-ord=0`
7. Reverted guarded behavior in scratch copies:
   - restoring empty-entity false-green behavior made
     `test_crossings_with_NO_entity_declared_is_a_FINDING_not_a_vacuous_pass`
     fail;
   - making `boundary_incomplete` read `Stability` made
     `test_a_DRAFT_crossing_holds_the_BOUNDARY_rung_open` fail;
   - flipping one frame approval to `approved` made
     `test_nothing_in_the_live_frame_is_approved_yet` fail.
8. `pytest -q -x tests/test_external_frame.py`
   `20 passed in 18.40s`
9. `gen_okf.py --root . --check`
   `gen_okf: OKF bundle up to date (598 file(s)).`
10. `check_docs.py --root . --ignore docs/test/report.md --ignore 'docs/work/*' --stale`
    `check_docs: OK - 403 doc(s), 1189 intra-repo link(s), 0 broken.`

### Done-when coverage map

| Requirement clause | Covering observation | Status |
|---|---|---|
| Five locked entity rows/classes | Parsed `external.toml`; 5 EXT rows | PASS |
| Three external-only relationship rows | Parsed rows; no interface fields | PASS |
| Six locked B-01/02/04/05/06/07 crossings | Parsed rows; B-03 absent | PASS |
| IF rows slim and tie back only when boundary-realizing | Eight tie-backs observed; `direction`/`counterpart` hold explicitly documented against SR-091/WI-455 | PASS |
| Retire Stability for Approval across 113 IF rows | Registry sweep and schema tests; no live IF Stability cells | PASS |
| Approval from external.toml's first commit | `git show 0ff33a95`; all frame rows carry approval | PASS |
| Provisional vocabulary/migration stated | Registry headers state `draft|approved` and D-9 migration | PASS |
| Same-commit gate re-key | `0ff33a95` changes retirement and predicate together; driven gate variants | PASS |
| Approval-versus-realization decision resolved | Gate variant and `test_rung_1_gates_on_APPROVAL_and_NOT_on_realization_coverage` | PASS |
| SR Boundary-Refs and SN-037 checker | Unknown-reference mutation reaches strict failure | PASS |
| IF-020/041, IF-036, IF-038, IF-064 dispositions | Actual rows and recorded dispositions checked; held columns explain retained counterpart cells | PASS |
| Owner-only approval authority | Header prose plus approval-flip tripwire failure | PASS |
| Generated IF one-pagers carry current approval schema | `gen_okf.py` still reads `Stability`; emitted IF-020/041 have `tags: []` despite `approval = "draft"` | FAIL |

### Findings

- [MAJOR] project-trajectory/scripts/gen_okf.py:479 -> the shipped OKF generator still reads retired `Stability`, so every generated IF one-pager silently omits its live `Approval` value (`tags: []`); switch it to `Approval`, update the stale contract comment, regenerate `docs/okf/`, and add a regression assertion that an IF approval is exported.

VERDICT: CHANGES-REQUESTED findings=1

**Author re-verification and consume (lane builder).** Reproduced at
75d7d080: `gen_okf.py:481` read `r.get("Stability")` under a comment calling
it "the one maturity field"; `docs/okf/interfaces/IF-020.md` shipped
`tags: []`; the bundle had been regenerated with the broken read at the prior
fix round, so `--check` called the silent loss fresh. Fixed at **4d624928**:
the tags cell reads `Approval`, the comment states the real column history,
`docs/okf/` regenerated (113 files now `tags: ["draft"]`, `--check` fresh),
and `tests/test_gen_okf.py::test_an_IF_one_pager_exports_the_live_approval_value`
added — confirmed RED against the pre-fix generator in a scratch clone
(`1 failed`) and green on the fixed tree. The same commit re-synced
`.agents/skills/byte-budget-guard/SKILL.md` byte-identical to source: the
prior tip had re-stamped the source and the `.claude` copy only, and the
skills-sync hook refuses every commit on the branch until the third copy
matches. Commit bar at 4d624928: smoke `1118 passed, 3 skipped`; check_docs
`OK - 403 doc(s), 1189 intra-repo link(s), 0 broken`.

---

## Round 2 — at 4d624928 (CHANGES-REQUESTED, 1 MAJOR)

The fix correctly changes the IF OKF tag source from retired `Stability` to
live `Approval`; the regenerated 113 IF one-pagers now carry
`tags: ["draft"]`, and the new regression test genuinely distinguishes pre-fix
from fixed behavior. One active shipped-documentation seam still teaches the
retired field and can recreate the same broken output for adopters.

### Failure classes hunted, worst-first

Silent loss of IF approval in generated OKF; regression test that would remain
green pre-fix; stale or nondeterministic generated bundle; remaining
retired-column consumers; skills-copy drift; regression of boundary-stage
behavior; smoke-bar failure.

### Exact commands and driven output

- `git show 4d624928 --stat` and diff review: only the generator, its
  regression test, regenerated IF pages, and the stated skills-sync unblocker
  changed.
- `gen_okf.py --root . --check` twice: fresh both times; bundle digest
  remained `e67af1cc511b625a945bc570003bbf85dea4c2cb`.
- Parsed all 113 live IF rows against their emitted pages:
  `approval-to-tag mismatches=0`; inspected `docs/okf/interfaces/IF-020.md`
  (`tags: ["draft"]`).
- Scratch-prefix mutation restoring the `Stability` read: new regression test
  failed with `tags: []`; real tip passed.
- `gen_skills_index.py --root . --check-agents`:
  `OK - 12 per-agent skill copy(ies) match source.`
- `pytest -q -n auto -m smoke`: `1118 passed, 3 skipped in 30.48s`.
- Targeted: `tests/test_gen_okf.py` `13 passed`;
  `tests/test_ratification_level.py tests/test_external_frame.py` `82 passed`.
- Fresh bootstrap probe copied stale `stability = "Stable"` examples into the
  scaffolded `docs/interfaces.md`.

### Findings

- [MAJOR] project-trajectory/INTERFACES.template.md:90 -> the shipped scaffold's interface guide still presents `stability = "Stable"` as valid TOML (also `project-trajectory/EXAMPLE.md:292`, `project-trajectory/PROCESS.md:977`, and `project-trajectory/skills/gate-advance/SKILL.md:130` retain the retired IF/gate semantics). An adopter following these active instructions reintroduces a field the current generator ignores, recreating `tags: []`; update the examples and field prose to `approval`, and state the boundary rung in terms of `external.toml` boundary approvals.

VERDICT: CHANGES-REQUESTED findings=1

**Author re-verification and consume (lane builder).** All four sites
reproduced (each twice where the file carries two worked rows:
`INTERFACES.template.md:90/:100` — the file `bootstrap.py` scaffolds straight
into an adopter's `docs/interfaces.md` — and `EXAMPLE.md:292/:302`; plus the
`:22` "stability promise" prose, `PROCESS.md:976-977`'s §8 opening field
enumeration, and the gate-advance skill's DevBar-Reqs bar still keyed on
`Stability = Experimental`). An author sweep for the same class found one more
active-instruction site the reviewer had not named:
`PROCESS_OPTIONS.md:2413-2414`, the rung-2 multi-module profile's
"direction/owner/version/stability discipline" (and its stale
`interfaces.csv` carrier name). Fixed at **2849616e**: all sites teach
`Approval` (worked rows now `approval = "approved"` — fiction in a worked
example, not a manufactured live approval; both live registries still carry
zero `approved` cells, which `test_nothing_in_the_live_frame_is_approved_yet`
pins), and the gate-advance bar re-states rung 1 as `external.toml`
`[boundary.B-##]` approval including the applies-when. Byte budgets per the
guard skill: PROCESS.md 73,604 → 73,617 (+13, flagged, baseline re-stamped in
`byte-budget-guard/SKILL.md` source + both tracked copies);
PROCESS_OPTIONS.md 171,916 → 171,916; AGENTS.template.md untouched (9,994).
Commit bar at 2849616e: smoke `1118 passed, 3 skipped`; check_docs `OK - 403
doc(s), 1189 intra-repo link(s), 0 broken`.

---

## Round 3 — at 2849616e

Round-2’s 10-file documentation/skill re-key correctly replaces active `Stability` authoring guidance with `Approval`, while preserving retirement history and synchronized budget/skill copies. I re-drove the prior failure path and new parser/scaffold seams without modifying the worktree.

### Failure classes hunted, worst-first

- Adopters still authoring the retired field.
- Scaffold output diverging from its template.
- Approval examples arming live-registry tripwires.
- Documentation edits breaking parsed examples or skill synchronization.
- Boundary-rung re-key failing to clear when all crossings are approved.

### Exact commands and driven output

- `git show 2849616e`: exactly 10 warranted files; 27 insertions, 24 deletions.
- `grep -rn -i "stability" project-trajectory/ --include="*.md"`: 13 hits; all are retirement/history or ordinary-English uses, with no active adopter instruction.
- Scratch `bootstrap.py --dest … --agents none --stack any --domain any`: scaffolded `docs/interfaces.md` contains `Approval` worked rows and no active `Stability` field.
- `wc -c project-trajectory/PROCESS.md`: `73617`; all byte-budget copies carry `73,617`.
- `gen_skills_index.py --check-agents`: `OK - 12 per-agent skill copy(ies) match source.`
- `gen_skills_index.py --skills project-trajectory/skills --check`: `OK - 27 skill(s), index fresh.`
- Live approval counts: `0` in each of `docs/requirements/interfaces.toml` and `external.toml`.
- Scratch completed-spine `derive_gate.py --print`: draft crossings yielded `stage=DevStg-Boundary`; changing all six `[boundary.B-##]` approvals to `approved` yielded `stage=DevStg-Needs`, confirming the boundary cap cleared.
- `pytest -q tests/test_bootstrap.py tests/test_dogfood_sync.py tests/test_plan_briefs.py -x`: exit 0.
- `pytest -q tests/test_gen_cases.py -x`: `7 passed in 0.10s`.
- `pytest -q -n auto -m smoke`: `1118 passed, 3 skipped in 29.74s`.
- Final `git status --porcelain` and `git diff --check`: clean.

### Findings

None reproduced.


**Author re-verification.** No findings to consume; the reviewer's
clean-sweep claims were spot-checked against the real tree (residual
`stability` mentions are all retirement/migration narrative; both live
registries carry zero `approved` cells; skills copies byte-match source).
The machine line below is the governing verdict — `parse_verdict` takes
the last matching line in this file.

VERDICT: APPROVE findings=0
