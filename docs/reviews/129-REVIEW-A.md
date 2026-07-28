# 129-REVIEW-A

**VERDICT: CHANGES-REQUESTED — 5 findings: 1 BLOCKER, 3 MAJOR, 1 MINOR.**

Review scope: exactly `63fb07e..86d0276` on `dualplan-routing-fix`. I ran `git show 86d0276`, the requested range diff, real `check_dupes.py`, `check_trajectory.py --strict`, `derive_gate.py --check`, targeted pytest, mutation probes in disposable copies, and the required G3 harness. The harness passed all 19 steps; its full test stage reported `1630 passed, 6 skipped in 1227.69s`. The pre-existing untracked `docs/pause` remains the only worktree change.

## Claim verification

| Claim | Result | Verification |
|---|---|---|
| Census fell from 208 to 207. | **CONFIRMED** | Parsed sanctions from both revisions: `63fb07e=208`, `86d0276=207`; current `check_dupes.py --emit-census` emitted 207. |
| The one-block reduction was caused by the `_raw_level` extraction merging the named spine-loader runs. | **CONFIRMED** | Range diff shows the refactor; current census contains `108925d1de82` where the old header names the two predecessor fingerprints. |
| Distribution is 34 extract / 20 debt / 7 direct deliberate / 3 merged classes, totaling 64 same-file blocks. | **CONFIRMED** | Parsed 31 sections: 207 total. Same-file entries total 64; extract=34, debt=20, direct deliberate=7, and the remaining 3 are the same-file members of `import-fallback`, `declared-file`, and `okf-row`. |
| Per-class counts and all 207 census entries match the emitted checker census. | **CONFIRMED** | `tests/test_dupes_census_audit.py` passed; direct parser found 31 sections, 207 entries, zero stray entries; ordinary checker reported `OK`. |
| The 64-block triage is a truthful per-block audit. | **REFUTED** | The `declared-file` sanction at `docs/dupes-allow:362-379` groups `check_docs.py:405` and `:685` as deliberate under an F5 rationale, although both occurrences are in the same script. The audit itself says F5 does not justify same-file duplication. See MAJOR 3. |
| `signature-echo` is not copy-paste debt. | **CONFIRMED** | Real checker findings are `agent_loop.py:1661 == :2896` (function parameter list and its call) and `agent_route.py:983 == :1051` (intentionally uniform routing APIs). |
| Sampled extraction/debt dispositions correspond to source. | **CONFIRMED, except declared-file above** | Located actual checker extents: `ref-namespace` (`agent_dispatch.py:210/:324`) matches WI-343 extraction; `train-disposition` (`:2131/:2301`) fits WI-280; `staged-close-scan` (`check_trajectory.py:1478/:1543`) fits WI-344; `spine-load-repeat` (`gen_trajectory.py:349/:557`) fits WI-346; `graph-layout` (`:887/:1070`) fits WI-280; `ctx-unpack` and CLI samples were also consistent. |
| The new census guard has 13 tests and each named assertion can fail. | **CONFIRMED** | Collection: `13 tests`. In seven isolated copies, each primary assertion failed when its corresponding invariant was broken: coverage, disposition, header count, distribution, WI-module ownership, path-name ban, and majority rule. |
| The guard prevents a future broad catch-all. | **REFUTED** | A real probe against the shipped guard rebuilt the 64 entries into arbitrary `misc-a`/`misc-b` 32-entry classes and added an open WI whose Title merely listed the module basenames. Every guard function passed. See BLOCKER 1. |
| `_raw_level` preserves existing `raw` and `per_phase` behavior. | **CONFIRMED for tested cases** | Direct old/new `compute()` comparison agreed for mature, Draft-SR, Draft-SN, Draft-TC, and LLR-exempt fixture spines. |
| `ex-draft` closes the single-phase Draft false negative without a new false negative. | **REFUTED** | A mature SR whose sole LLR is changed to `Draft` computed `computed=G0 ex-draft=G1` and `window=False`; this is a mature reopened spine held down by a Draft. See MAJOR 2. |
| String comparisons against `G2` are valid for generated values. | **CONFIRMED** | `derive_gate` emits only `G0`–`G3`; lexical ordering used by `window_open()` is correct for that closed one-digit domain. |
| Legacy gate-file fallback remains operational. | **CONFIRMED** | Existing no-`ex-draft` fixtures exercised the fallback; a mature legacy multi-phase basis returned true, an early one false, and the single-phase legacy case retained its old false negative as documented. |
| WI-342 marked the 28/9 and 67-file observations historical. | **CONFIRMED** | `docs/dupes-allow:65` and archived WI-337 lines 95–101 explicitly mark the observations historical/non-reproducible and name the remaining checkable evidence. |
| The classifier’s “four passes” claim is gone. | **REFUTED** | `docs/log.md:16354` still says “it took four passes,” while the new entry at `:16645-16647` says the claim is gone. |
| `470 passed / 25.0 s`, `470 / 29.1 s`, and `1629 passed, 7 skipped` are substantiated. | **UNVERIFIABLE** | Smoke collection confirmed `470/1636`; the bounded smoke run could not finish before timeout. The required full rerun instead produced `1630 passed, 6 skipped in 1227.69s`; no raw artifact supports either signed historical timing/count. |
| `check.py --gate G3 --jobs 0` passes all 19 steps. | **CONFIRMED** | Actual rerun ended `RESULT: PASS`, with all 19 named steps passed. |
| PROCESS_OPTIONS byte delta is `163,113 → 165,000 (+1,887)`; other two watched files unchanged. | **CONFIRMED** | `git cat-file -s` and current sizes: AGENTS `9975→9975`, PROCESS `63249→63249`, OPTIONS `163113→165000`. |
| Dashboard was `1,640,447 → 1,655,456 (+15,009)` for six new WIs. | **REFUTED** | Blob sizes are `1,640,447 → 1,658,490`, a delta of **18,043**. The range adds **seven** rows, WI-343 through WI-349, not six. |
| WI-348 found 17 `write_text()` sites without `newline`, while four already specify it. | **REFUTED** | AST scan found exactly 17 `Path.write_text()` calls: **17 omit** `newline`, **0 specify** it. |
| WI-349’s one-physical-line dependency is unenforced. | **CONFIRMED** | `check_trajectory.py:1478` documents the assumption; repository search found no validator or test rejecting CR/LF in WI cells. |

## Findings

### BLOCKER 1 — The replacement census guard still permits a catch-all audit

`tests/test_dupes_census_audit.py:314-329` bans only a single majority class and `:220-246` accepts ownership when arbitrary module basenames appear in a WI Title or Deliverable. This does not establish that the WI will dissolve the class.

I drove the shipped checks with a rebuilt census: all 64 same-file blocks were put into two arbitrary classes, `misc-a` and `misc-b`, with 32 entries each; an open synthetic WI-900 merely listed every basename in its Title. Coverage, dispositions, counts, distribution, ownership, path-name, and majority checks all returned clean:

```text
BYPASS PASSED: arbitrary 32/32 catch-all split plus cosmetic WI module names passes every guard
```

This recreates the exact failure mode under two labels. A future session can satisfy every rule while using arbitrary partitions and a cosmetic WI row; the claimed anti-catch-all property is therefore false.

Required correction: require an auditable per-class rationale tied to concrete code symbols or declared deliverables, prohibit arbitrary split classes, and test a realistic two-class/keyword-stuffed-WI bypass—not only a renamed single majority bucket.

### MAJOR 2 — `ex-draft` still misses a mature spine reopened through its sole LLR

`derive_gate.py:279-285` removes Draft LLRs before recomputing `ex_draft`. That also removes the only structural evidence that an SR is decomposed.

I constructed and drove a real spine with a Verified SR, one TC, and its sole LLR changed to `Draft`. `compute()` and `window_open()` returned:

```text
# basis: ... drafts=1 modified=0 computed=G0 ex-draft=G1 phase=1 per-phase=1=G0
window=False
```

The row can represent a mature G3 chain reopened by changing its existing LLR to Draft; the Draft is precisely what suppresses the gate, but the new counterfactual erases its pre-existing structural role and calls the remaining SR undecomposed. The advisory window therefore remains closed.

Required correction: distinguish a newly added Draft child from a pre-existing child reopened to Draft, or retain appropriate structural decomposition while excluding its Draft maturity contribution. Add this exact SR/sole-LLR/TC case to both producer and consumer tests.

### MAJOR 3 — The `declared-file` same-file sanction contradicts the audit’s F5 rule

`docs/dupes-allow:364-379` calls `check_docs.py:405-410` and `:685-690` deliberate because “each script reads its own declaration rather than importing a sibling.” These are not different scripts: they are two loops in `check_docs.py`, one collecting non-comment lines and one selecting/parsing the last non-comment line.

The commit repeatedly states that F5 buys cross-script copyability and “never justified a same-file copy” (`docs/dupes-allow:185-187`, `docs/log.md:16585-16587`). No separate local rationale explains why the shared read/strip/comment-skip loop must remain duplicated.

Required correction: either extract the common declared-file reader and file it under the appropriate WI, or state and defend a specific same-file design reason. Do not use the cross-script F5 rationale for this block.

### MAJOR 4 — Newly signed measurements are still false or unsupported

The new “Signed measurements” rule is not applied to several numbers the commit signs:

- `docs/log.md:16687-16696` and `tests/test_dashboard_size_budget.py:37-43` claim `1,655,456`, `+15,009`, and six new WIs. Git blob sizes prove `1,658,490`, `+18,043`, and seven new WIs.
- WI-348 says 17 `write_text()` sites omit `newline` and four already specify it. AST inspection proves 17 omit it and zero specify it.
- `docs/log.md:16645-16649` says the old four-pass claim is gone, but `docs/log.md:16354` still makes that claim.
- The fresh `29.1 s` and commit’s `25.0 s`/`1629 passed, 7 skipped` figures have no committed raw output. The independent full run produced a different count: `1630 passed, 6 skipped`.

Required correction: correct the false figures; either attach raw command output for new measurements or mark them historical/non-reproducible; and reconcile or explicitly annotate the surviving four-pass statement.

### MINOR 5 — The commit fails `git diff --check`

`git diff --check 63fb07e..86d0276` reports:

```text
docs/dupes-allow:595: new blank line at EOF.
```

Required correction: remove the trailing blank line.