Verdict: not ready to close. I found 1 CRITICAL, 9 MAJOR, and 1 MINOR defect.

1. **CRITICAL — the freshness gate can pass while committing a stale `docs/stage`.**

   Evidence: the plan claims the commit bar refuses a stale committed copy at [stage-unification-plan.md:80](C:/Projects/ai-template/docs/plans/2026-08-21-stage-unification-plan.md:80), but every freshness check reads the working tree, not the index [check.py:1391](C:/Projects/ai-template/project-trajectory/scripts/check.py:1391). The only index comparison is warn-only [check.py:1443](C:/Projects/ai-template/project-trajectory/scripts/check.py:1443), and the hook itself admits regeneration without staging turns the checks green over stale committed bytes [pre-commit:246](C:/Projects/ai-template/project-trajectory/hooks/pre-commit:246).

   Failure scenario: stage a registry edit, run `derive_stage.py` but do not stage the regenerated `docs/stage`, then commit. `derive-stage --check` sees fresh working-tree bytes and passes; `staged-divergence` warns but exits 0; the commit contains the edited registry and old stage.

   Suggested fix: run generated-artifact freshness against an index materialization during pre-commit, or make staged divergence strict and compare staged artifact bytes with a staged-input derivation.

2. **MAJOR — a fully settled spine does not reach `DevStg-Impl` on the scaffold the kit actually ships.**

   Evidence: bootstrap always installs blank `external.toml` and `components.toml` [bootstrap.py:1758](C:/Projects/ai-template/project-trajectory/scripts/bootstrap.py:1758). An existing but row-empty external registry holds `DevStg-Boundary` [spine_rules.py:498](C:/Projects/ai-template/project-trajectory/scripts/spine_rules.py:498). The acceptance tests obtain their expected spine rungs by explicitly deleting both real-scaffold files [test_derive_stage.py:65](C:/Projects/ai-template/tests/test_derive_stage.py:65), while teaching prose falsely says a fresh scaffold derives `DevStg-Reqs` [KICKOFF_PROMPT.md:89](C:/Projects/ai-template/project-trajectory/KICKOFF_PROMPT.md:89).

   Failure scenario: an adopter completes every SN→SR→LLR→TC row but leaves the scaffolded placeholder frame files untouched. The derived stage stays at Boundary, so `format`, `lint`, and `tests+coverage` never select from the derived value.

   Suggested fix: either do not scaffold optional frame registries until adopted, or treat placeholder-only registries as absent; then add a real, unmodified-bootstrap acceptance test.

3. **MAJOR — a component-only multi-rung drop ending at Arch bypasses the phase rule.**

   Evidence: the rule recognizes only added rows or `Status` changes in SR/LLR/TC [derive_stage.py:303](C:/Projects/ai-template/project-trajectory/scripts/derive_stage.py:303). Its purported Impl→Arch test changes the component and also adds an SR; the SR is the only reason a finding exists [test_phase_rule.py:213](C:/Projects/ai-template/tests/test_phase_rule.py:213).

   Driven counterexample: a settled `DevStg-Impl` spine with `CMP-001 Standing=""` changed only to `Standing="has-gap"` produced:

   `was=DevStg-Impl`, `now=DevStg-Arch`, `changed_rows=[]`, `findings=[]`.

   This is not the exempt LLReqs→Arch pair.

   Suggested fix: model all stage-affecting edits, including component and boundary fields, and fail/warn whenever a non-exempt decrease has no qualifying phase signal.

4. **MAJOR — the approval act signed false amendments as “mechanical re-points.”**

   Evidence: the approval record says all four drift groups are mechanical renames [2026-08-22-spine-approval.md:48](C:/Projects/ai-template/docs/log.d/2026-08-22-spine-approval.md:48). The blessed live cells instead claim:

   - `spine_rules` “computes the gate” [system-requirements.toml:477](C:/Projects/ai-template/docs/requirements/system-requirements.toml:477);
   - `spine_rules` has `--check`, a basis line, and `--print` [test-cases.toml:534](C:/Projects/ai-template/docs/test/test-cases.toml:534);
   - `docs/gate` remains the dashboard/status input [low-level-requirements.toml:1401](C:/Projects/ai-template/docs/requirements/low-level-requirements.toml:1401).

   The program itself says `spine_rules.py` derives no gate and writes no file [WI-498 program:41](C:/Projects/ai-template/docs/work/active/wi498-stage-unification/WI-498-stage-unification-program.md:41).

   Failure scenario: a later reviewer trusts the re-seeded approved baseline and designs or verifies against nonexistent CLI modes and a deleted carrier. Every snapshot-drift check remains green because the false text is now the blessed baseline.

   Suggested fix: reopen the affected SR/LLR/TC cells, re-author their semantics—not just filenames—and re-seed only after a new explicit approval.

5. **MAJOR — “every current-stage consumer uses the common reader” is false.**

   Evidence: the ruled contract says everything needing current stage calls one function [stage-unification-plan.md:72](C:/Projects/ai-template/docs/plans/2026-08-21-stage-unification-plan.md:72). The dashboard deliberately parses committed `docs/stage` directly [traj_parse.py:451](C:/Projects/ai-template/project-trajectory/scripts/traj_parse.py:451), as does the generated status block [traj_status.py:100](C:/Projects/ai-template/project-trajectory/scripts/traj_status.py:100).

   Failure scenario: edit a stage input on a claimed branch and render the dashboard/status before trunk regeneration. `check.py`, authority decisions, and the event detector see the freshly derived value; the generated displays show the stale committed value. Generated-view freshness is among the branch-skipped steps.

   Suggested fix: narrow the contract honestly to decision consumers, or make renderers consume a supplied fresh record while separately displaying the committed-record discrepancy.

6. **MAJOR — the fingerprint ignores a forbidden second carrier.**

   Evidence: `input_paths` accepts the first existing suffix and stops [stage.py:143](C:/Projects/ai-template/project-trajectory/scripts/kitlib/stage.py:143). The real registry resolver instead refuses when TOML and CSV both exist [spine_carrier.py:617](C:/Projects/ai-template/project-trajectory/scripts/spine_carrier.py:617). `read_stage` trusts the cached record when the first carrier’s fingerprint matches [stage.py:547](C:/Projects/ai-template/project-trajectory/scripts/kitlib/stage.py:547).

   Failure scenario: start with a fingerprinted TOML registry, then add a conflicting CSV beside it. The fingerprint remains unchanged because only TOML is hashed, so common-reader consumers return the recorded stage without invoking the derivation that would refuse the two-home state.

   Suggested fix: fingerprint the complete carrier-presence vector and refuse multiple live carriers inside `input_paths`.

7. **MAJOR — both “Release unreachable” guards survive a producer mutation.**

   Evidence: the exhaustive test varies only Verification and the four Status spellings [test_ratification_level.py:733](C:/Projects/ai-template/tests/test_ratification_level.py:733). The structural arm searches source text only for the literal `STAGE_RELEASE` [test_ratification_level.py:760](C:/Projects/ai-template/tests/test_ratification_level.py:760).

   Mutation result: adding a conditional `return _ladder.STAGE_ORDER[-1]` behind a new `EvidencePassed` field caused both existing guards to pass—the 128 enumerated shapes still excluded Release and both source-string assertions passed—while the hidden shape returned `DevStg-Release`.

   Suggested fix: use an AST guard that rejects any return expression capable of resolving to the final rung, plus property-based row-key/status generation.

8. **MAJOR — the “seven stale Approved rows” census materially undercounts live false specifications.**

   Evidence: the banked list claims six plus SR-148 [WI-498 log:1605](C:/Projects/ai-template/docs/log.d/2026-08-21-wi498-stage-unification.md:1605). Additional Approved TCs still require deleted machinery:

   - dashboard from `docs/gate` [test-cases.toml:543](C:/Projects/ai-template/docs/test/test-cases.toml:543);
   - `--next-phase` leaving `docs/gate` unchanged [test-cases.toml:1392](C:/Projects/ai-template/docs/test/test-cases.toml:1392);
   - `derived-gate` preceding two consumers [test-cases.toml:1700](C:/Projects/ai-template/docs/test/test-cases.toml:1700).

   SR-140 and LLR-124 are additional false cells [system-requirements.toml:477](C:/Projects/ai-template/docs/requirements/system-requirements.toml:477), [low-level-requirements.toml:1244](C:/Projects/ai-template/docs/requirements/low-level-requirements.toml:1244).

   Failure scenario: WI-501 repairs only its stated seven-row population; the Approved TC methods remain impossible to execute and regenerate unchanged into `report.md/html`.

   Suggested fix: rebuild the population by value over every SN/SR/LLR/TC ratified cell, not from the banked row names.

9. **MAJOR — the signed full-suite totals are not reproducible from their records.**

   Evidence: the session protocol requires command plus revision under `fig:` [session-protocol:117](C:/Projects/ai-template/.agents/skills/session-protocol/SKILL.md:117). Slice totals at [WI-498 log:96](C:/Projects/ai-template/docs/log.d/2026-08-21-wi498-stage-unification.md:96), [WI-498 log:235](C:/Projects/ai-template/docs/log.d/2026-08-21-wi498-stage-unification.md:235), and [WI-498 log:465](C:/Projects/ai-template/docs/log.d/2026-08-21-wi498-stage-unification.md:465) carry no producing revision. The approval close uses `rev=a0e6f799-dirty` [spine-approval.md:130](C:/Projects/ai-template/docs/log.d/2026-08-22-spine-approval.md:130), which is not a reconstructible tree.

   Failure scenario: checking out `a0e6f799` cannot reproduce the 2,831 result because the uncommitted approval changes are absent, and the other slice results do not identify which tree to check out at all.

   Suggested fix: record a tree OID or post-change commit for every driven figure; make the figure checker reject `-dirty` and unmarked pytest totals.

10. **MAJOR — PB-004 remains a fluent stale signed measurement.**

   Evidence: PB-002 was correctly remeasured, but PB-004 still says the current pre-commit floor includes `derived-gate` and attributes its 7.7 s measurement to the old hook [performance-budgets.csv:5](C:/Projects/ai-template/docs/requirements/performance-budgets.csv:5). The current hook runs `derived-stage`, not `derived-gate` [pre-commit:270](C:/Projects/ai-template/project-trajectory/hooks/pre-commit:270).

   Failure scenario: a performance review compares today’s hook against a baseline measuring a different step set; because no metric producer is wired and the row is warn-only, nothing reports the invalid comparison.

   Suggested fix: remeasure PB-004 on the current hook and restamp its exact step membership and revision.

11. **MINOR — the sweep altered immutable historical evidence after correctly reverting three other record edits.**

   Evidence: archived review/spec citations were changed from links to plain code text, e.g. [repo-review-2026-07-12b.md:228](C:/Projects/ai-template/docs/archive/history/repo-review-2026-07-12b.md:228) and [WI-243.2026-07-20.md:50](C:/Projects/ai-template/docs/archive/specs/WI-243.2026-07-20.md:50). The range diff attributes these edits to the stage-unification sweep.

   Failure scenario: an auditor reading the historical review loses the navigable evidence while `git blame` misleadingly attributes a 2026-07 finding to the later migration.

   Suggested fix: restore historical bytes; if navigation is needed, add a separate present-day index pointing to the historical blob.

Banked-item reconciliation: the frame dominance, live-only recursion signal, phase rule being warn-first/unwired, phase detector vacuity, latent collection-order imports, unused imports, module-size growth, watched-baseline non-enforcement, asymmetric alias semantics, and smoke overruns are confirmed. WI-473, removal of `process.toml` from `DECLARED_INPUTS`, PB-002, anchor teaching, and the obsolete `derive_gate` size/caller findings are resolved. The byte stamps are exact—CLAUDE 7,238; all guard-skill copies 4,925—and the seven approval-baseline files are byte-identical to live. `derive_stage.py --check` also reports current `docs/stage` fresh.

I could not rerun the recorded full suites: the configured 3.11 environment points to a missing interpreter, and the read-only environment provides no writable pytest temporary directory. The two mutation counterexamples above were driven in memory with the installed interpreter.

The three claims I tried hardest to refute and could not:

1. The 15 approval flips in `ac121647` were Status-cell-only: exactly 15 Drafted→Approved replacements.
2. The six sampled selection thresholds—registry integrity, traceability, design flows, trajectory, backlink coverage, and ratify freshness—match their stated artifact-existence rule.
3. Apart from the dual-carrier representation hole, the declared fingerprint input list matches every file `spine_stage` actually reads; `process.toml` is correctly excluded.