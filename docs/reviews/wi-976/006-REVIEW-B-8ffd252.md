Reviewed: 8ffd25250c067ee70e7c235895555e5eaa679740

### REVIEW-B (independent, Claude Opus) — WI-976 full lane aa36a5b6e..8ffd25250 — 2026-10-25

**Verified.** `git rev-parse HEAD` printed the reviewed commit. Failure classes hunted first, worst first: (1) silent wrong content, meaning a decomposition round whose brief omits an applicable hat, or a non-round that carries hats; (2) fail-open, meaning a malformed roster composing a round, or hat outcome lines changing a parsed ruling; (3) breakage, meaning an assembler's new `_hat_parents` key reaching the strict `prompts.fill`, or an override without `{hats}` no longer composing.

I drove the real shipped path, `adjudicate_brief.compose`, on this lane's own spine, with the WI-976 row and its tags (Workstream=process, SafetyClass=ordinary):
- An amendment sitting over SN-036;SR-161;LLR-183;TC-178;TC-211 carries the 11 applicable hats' questions and the `- HAT` outcome instruction.
- A first-approval sitting over LLR-360;TC-399 carries `NOT_A_ROUND` and no question.
- A combined sitting over both carries the questions once, in one `=== THIS SITTING'S PERSPECTIVES ===` part after the last section, with the instruction to write the outcome lines under that section's heading.

`HAT_PARENTS` is popped in `fill_hat_slot` before the strict fill on every path. `_assemble` is the only consumer of the assembler values, so no other route leaks the key. Strict fill refuses unknown keys, so an override without `{hats}` gets no `hats` value and composes unchanged, and a test pins that equality. A combined section never reads the roster; only the tail does, once, over the union of its sections' parents.

Regression tests: I copied the reviewed tree (`git archive`) to scratch and restored the pre-fix `plan_briefs.py`, `adjudicate_brief.py` and `mkprompt.py` from `de132d748`. On that copy, the four fix-round regression tests (7 cases) all fail: the amended-SR need case, the combined cross-section need case, the author-prompt parent scope case and the empty `HATS` value case.

Retirement and spine:
- The retirement is complete. No live surface names the sidecar, the `record` command, LLR-297 or TC-312. What remains is the superseded RESYNC entry, and "perspective record" meaning Hat-Refs, which is kept on purpose per the spec. ruff F/E9 is clean on the touched modules, with no orphaned import or symbol in `hats.py`. LLR-297 and TC-312 have retirement records.
- The ruling fragment (36fc6d6f7) is committed alone before the first registry commit (4fc5d55f4).
- SN-036, and SR-161's requirement, acceptance and verification, match `contract_split` 961f9e47. So does SR-161's rationale, apart from its citation, which now names the ruling by its dates as the spec asks.
- LLR-360 reads true against the code (rubric K1). Its contract: the round is decided by first-approval SRs or amended needs; an amended SR's need joins a round but makes none alone; each need is widened alone; the slot is optional; a combined sitting carries it once; absent is opt-out and malformed refuses by name.
- K2: no SN or SR cell names a script. K3: the new functions are tagged `Implements: SR-161, LLR-360` and appear in LLR-360's `code_symbol` and `module`. No Status flips: SN-036, SR-161 and LLR-183 stay Approved pending the sitting, and LLR-360 and TC-399 are Drafted.
- SAFETY is gone from the live roster and kept in the template, with the name pins split. The header counts and the three recipe copies are consistent. The PROCESS.md byte delta is real (98,185 -> 97,962, -223) and restamped.

Done-when coverage:
- Covered by tests in TC-399's evidence: the round definition, applicability per need with widening and no merging, the optional slot and an override composing unchanged, the combined sitting carrying the block once, absent versus malformed roster, outcome lines changing no ruling, the author-prompt `HATS` slot and its refusals, and the cycle naming the slot.
- Covered by the corrected text at each site: the rubric R1/B1, the inspection procedure and its abnormal input, PROCESS.md section 1, spine-questions (c3), both roster headers, the RESYNC entry, the IF-133 cell and the generated pages.
- Not yet due at this tip, so not counted as gaps: P9's checkpoint sitting as TC-211's sample (TC-211's `inputs` naming its brief and verdict are set at that reconcile, per the plan), P10's owner-held SN-036 act, P11's TC-211 re-judge, and the "does not land before the act" landing condition.

Coverage-extension note, no severity: a judged SR whose `sn_refs` names an undeclared need fails closed. The sitting refuses, though its reason is prefixed "cannot be composed from docs/requirements/hats.toml", which names the roster for a fault in the needs registry.

**Commands.**
- `git rev-parse HEAD` -> 8ffd25250c067ee70e7c235895555e5eaa679740
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r2b/wi-976 tests/test_plan_briefs.py tests/test_adjudicate_brief.py tests/test_prompts.py tests/test_hats.py tests/test_dogfood_sync.py` -> `346 passed, 1 skipped in 54.95s`
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (973 work item(s), 863 done (89%), 34 cancelled, graph acyclic).`
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=138 LLR=326 TC=353 orphans=0 integrity=0 verified-mechanized=131 verified-demonstrated=7 verified-attested=0 drafts=2 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=255 interface-findings=0 ac-advisories=1 paraphrase-advisories=2.` (the regenerated report is byte-identical; the lane stayed clean)
- `python -m ruff check --no-cache --select F,E9 <touched modules and tests>` -> `All checks passed!`
- Pre-fix probe: the reviewed tree with the de132d748 versions of the three fixed modules, running the 4 fix-round regression tests -> `7 failed in 3.06s`
- Real-path probe (`adjudicate_brief.compose` on this lane's spine, as amendment, first-approval and combined sittings, written under r2b/probe) -> the round blocks and non-round lines as described above

Findings:
- [MINOR] project-trajectory/skills/coordinator-cycle/references/recipes.md:128 -> the spine author's `HATS` value is defined as "the SN ids the set amends or adds an SR under" (in all three recipe copies; also scripts/coordinator/mkprompt.py:9 and scripts/coordinator/terra-spine-prompt.template.md:30), but the sitting's round, after the round-1 fix, also takes the needs of every amended SR it judges. A lane that amends SN-X and an SR under SN-Z gets an author prompt without SN-Z's hats, while its sitting asks for them, so the Done-when's "carries the same block" fails for that set. This was confirmed by reading `sitting_hat_block` (its `amended` parents) against `hats_block`, which receives only the named needs. -> in a turn that makes a round, have the recipe and the mkprompt docstring also name the needs of each SR the set amends. Text only; `round_questions` already widens correctly for any SN ids given. -> @coordinator
- [MINOR] project-trajectory/RESYNC_PACK.md:9870 -> the new entry says "One `scope: this-repo` skill changed too ... `skills/coordinator-cycle/`", but this range also changes `skills/byte-budget-guard/SKILL.md` (the PROCESS.md row restamp), which earlier entries list when it moves (RESYNC_PACK.md:9009, 9342, 9445). -> name `skills/byte-budget-guard/SKILL.md` beside coordinator-cycle as a this-repo skill, synced only if vendored. -> @builder

VERDICT: APPROVE findings=2
