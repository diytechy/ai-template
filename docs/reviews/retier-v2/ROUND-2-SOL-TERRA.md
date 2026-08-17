# Re-tier v2 — external adversarial round 2 (Sol + Terra)

**Date:** 2026-08-17 · **Round:** external adversarial, over the three
2026-08-17 spine commits — `47234903` (sitting-3 item-3 ruling: 19 `Consumes`
`owner` cells re-pointed SR→LLR, WI-469 filed), `82b91b8b` (SR-171/172
decomposed: LLR-174/175 + TC-168/169/170, three new tests), `d7975c96` (the
three-defect sweep: LLR-153 mint wording, TC-135 tier, the `trace_text.py`
`;`-split asymmetry) — and the claims in log entries `2026-08-17c/d/e`.
**Models:** GPT-5.6 Sol and GPT-5.6 Terra via `codex exec`
(`-c model_reasoning_effort=medium --sandbox read-only`, the house command),
each fed the same hostile brief (refute, don't appreciate) carrying the full
`47234903^..HEAD` diff plus repo pointers; read-only — no writes, no commits.
A first launch of both runs was killed mid-exploration by the session harness
(~15 min in, no output written); the recorded verdicts are from a second,
detached pair that ran to completion (~9 min each). Stated so the round's
provenance is exact.
**Scope reviewed:** the diff `47234903^..HEAD`; live
`docs/requirements/interfaces.toml`, `system-requirements.toml`,
`low-level-requirements.toml`, `docs/test/test-cases.toml`,
`project-trajectory/scripts/{agent_loop,trace,trace_text,trunk_step,intake}.py`,
`tests/`, `docs/log.md` `2026-08-17c/d/e`, `docs/work/queued/WI-469-*.md`.
**Verdict:** both reviewers CHANGES-REQUESTED · 9 distinct findings after
merging the one Sol/Terra overlap — **6 CONFIRMED, 2 CONFIRMED-IN-PART,
1 REFUTED**. Per the standing pattern nothing is applied here: every confirmed
finding is recorded for the owner's ruling (the queue below).

---

## The verdicts, verbatim

Fenced as text so they are byte-exact: the reviewers' citations are absolute
sandbox paths, which `check_docs.py` would otherwise read as broken repo links.

### Sol

~~~text
1. **MAJOR — The 19 item-3 re-points are only module-name matches, not defensible semantic ownership decisions.** Evidence: IF-043's contract covers both secret and identity blocking, but its owner LLR-017 covers secrets only while LLR-018 owns identity ([interfaces.toml](/Users/diytechy/Documents/ai-template/docs/requirements/interfaces.toml:627), [low-level-requirements.toml](/Users/diytechy/Documents/ai-template/docs/requirements/low-level-requirements.toml:178)); IF-117 consumes `module_bindings` but points to LLR-023's unrelated map-splice contract ([interfaces.toml](/Users/diytechy/Documents/ai-template/docs/requirements/interfaces.toml:1434), [low-level-requirements.toml](/Users/diytechy/Documents/ai-template/docs/requirements/low-level-requirements.toml:244)); and IF-127/IF-130 were re-pointed despite their own notes explicitly saying "Owner is SR-140, not a design row" and "No design row fits" ([interfaces.toml](/Users/diytechy/Documents/ai-template/docs/requirements/interfaces.toml:1571), [interfaces.toml](/Users/diytechy/Documents/ai-template/docs/requirements/interfaces.toml:1610)). Correct version: the 81/49/19/27/3 population split is reproducible, but several of the 19 are merely co-located-module candidates and do not supply an answerable LLR for the row's contract.

2. **MAJOR — SR-173's all-or-nothing obligation was weakened into the narrower claim that partial regeneration is acceptable provided it remains uncommitted.** Evidence: the SR requires "leaving no partially regenerated set behind" and its rationale calls this transactional/all-or-nothing ([system-requirements.toml](/Users/diytechy/Documents/ai-template/docs/requirements/system-requirements.toml:822)), while LLR-142 merely says the helper never commits ([low-level-requirements.toml](/Users/diytechy/Documents/ai-template/docs/requirements/low-level-requirements.toml:1395)) and the new test positively requires regenerated partial output to remain dirty in the working tree ([test_trunk_step.py](/Users/diytechy/Documents/ai-template/tests/test_trunk_step.py:299)). Correct version: TC-170 proves absence of a partial set in Git history, not SR-173's stronger no-partial-result/all-or-nothing requirement.

3. **MAJOR — TC-168 claims complete coverage of LLR-174 although mutations can break the parsed-reset retry, fallback ceiling, or default fallback without failing any cited test.** Evidence: LLR-174 requires parsed resets within the ceiling to sleep/retry, `min(fallback, ceiling)`, and defaults `0 / 3600` ([low-level-requirements.toml](/Users/diytechy/Documents/ai-template/docs/requirements/low-level-requirements.toml:1777)); TC-168 claims that complete contract ([test-cases.toml](/Users/diytechy/Documents/ai-template/docs/test/test-cases.toml:1675)), but its fallback test supplies fallback `1` under ceiling `30`, so removing the `min` cap still passes, and no cited integration test combines a parseable reset with `--wait-on-limit` ([test_agent_loop.py](/Users/diytechy/Documents/ai-template/tests/test_agent_loop.py:603)). Correct version: the evidence covers recognition, immediate WAITING, unparseable retry below the ceiling, and parser formats, but not the cap, parsed-reset retry branch, or default fallback value.

4. **MINOR — TC-169 does not pin LLR-175's declared `--stall-limit` default of 3.** Evidence: LLR-175 states default 3 ([low-level-requirements.toml](/Users/diytechy/Documents/ai-template/docs/requirements/low-level-requirements.toml:1789)), while every cited stalling case supplies an explicit limit and the only default-limit evidence commits every iteration, so changing the default would leave the registered evidence green ([test-cases.toml](/Users/diytechy/Documents/ai-template/docs/test/test-cases.toml:1686), [test_agent_loop.py](/Users/diytechy/Documents/ai-template/tests/test_agent_loop.py:300)). Correct version: TC-169 covers counter semantics and exits, but not the declared default.

5. **MAJOR — The rewritten LLR-153 overstates the mint's refusal behavior because a well-formed watermark file missing its `WI` entry silently degrades to zero.** Evidence: `read_watermark` validates file presence and line syntax but not required-space completeness ([trace.py](/Users/diytechy/Documents/ai-template/project-trajectory/scripts/trace.py:880)), and `next_wi_id` uses `.get("WI", 0)` ([intake.py](/Users/diytechy/Documents/ai-template/project-trajectory/scripts/intake.py:194)); TC-158 tests deletion of the whole file, not deletion of the `WI` entry ([test_id_watermark.py](/Users/diytechy/Documents/ai-template/tests/test_id_watermark.py:358)). Correct version: the mint refuses an absent or syntactically malformed watermark file, but does not itself refuse a missing `WI` mark and therefore does not fully enforce the stated "never proceed on a guess" contract.

VERDICT: CHANGES-REQUESTED — semantic mis-ownership, weakened SR-173 coverage, and two materially overstated verification contracts invalidate the sessions' completion claims.
~~~

### Terra

~~~text
1. **MAJOR — IF-127's re-point directly contradicts its unchanged per-row rationale.** Evidence: [interfaces.toml:1579](/Users/diytechy/Documents/ai-template/docs/requirements/interfaces.toml:1579) now assigns `LLR-001`, while [interfaces.toml:1582](/Users/diytechy/Documents/ai-template/docs/requirements/interfaces.toml:1582) explicitly says "Owner is SR-140, not a design row"; the log nevertheless lists this as a valid conversion at [log.md:133](/Users/diytechy/Documents/ai-template/docs/log.md:133). A correct version would say IF-127 remains SR-owned under its recorded exception, unless that rationale is independently superseded.

2. **MAJOR — The claimed "live" population split is not reproducible from the live interface registry.** Evidence: [log.md:122](/Users/diytechy/Documents/ai-template/docs/log.md:122)-[127](/Users/diytechy/Documents/ai-template/docs/log.md:127) says partitioning the 81 live `Consumes` rows yields 49 SR-owned rows, but the live file has 81 `Consumes` rows and only 30 SR-owned rows—the 27 WI-469 rows plus the three `external:` rows; [WI-469:35](/Users/diytechy/Documents/ai-template/docs/work/queued/WI-469-consumes-names-the-medium.md:35)-[69](/Users/diytechy/Documents/ai-template/docs/work/queued/WI-469-consumes-names-the-medium.md:69) does accurately enumerate the 27-file residue. A correct version would identify 49 as the pre-repoint population, not a result derived from the live post-repoint file.

3. **MAJOR — TC-168 claims coverage of the bounded-retry contract that its cited tests do not establish.** Evidence: [TC-168](/Users/diytechy/Documents/ai-template/docs/test/test-cases.toml:1678) requires both parsed-reset retry and `min(fallback, ceiling)` behavior, but [test_agent_loop.py:603](/Users/diytechy/Documents/ai-template/tests/test_agent_loop.py:603)-[612](/Users/diytechy/Documents/ai-template/tests/test_agent_loop.py:603) uses fallback `1` under ceiling `30`, so removing the cap still passes, while [test_agent_loop.py:520](/Users/diytechy/Documents/ai-template/tests/test_agent_loop.py:520)-[534](/Users/diytechy/Documents/ai-template/tests/test_agent_loop.py:534) exercises only the no-wait WAITING exit—not parsed-reset sleep/retry. A correct version would say the evidence covers recognition, the stop path, and an uncapped fallback retry, not every TC-168 clause.

4. **MAJOR — TC-170's "no partial result" proof never creates the later failure its method relies on.** Evidence: [TC-170](/Users/diytechy/Documents/ai-template/docs/test/test-cases.toml:1700) promises that a later failure cannot leave partial history, but [test_trunk_step.py:299](/Users/diytechy/Documents/ai-template/tests/test_trunk_step.py:299)-[327](/Users/diytechy/Documents/ai-template/tests/test_trunk_step.py:327) runs only a successful `arch-map` step and makes every later family skip; the log calls it proof of the "no-partial-set-committed clause" at [log.md:96](/Users/diytechy/Documents/ai-template/docs/log.md:96)-[99](/Users/diytechy/Documents/ai-template/docs/log.md:99). A correct version would say it proves no commit on that green single-step scenario, not the failure-path all-or-nothing claim.

VERDICT: **CHANGES-REQUESTED** — the owner ruling contains an unresolved self-contradiction, and two newly claimed TCs overstate their behavioral coverage.
~~~

---

## Disposition — author re-verified, NOTHING applied

Every finding below was re-verified against the live repo before its verdict
was written (house rule: refute with named evidence, confirm with named
evidence). Per the standing pattern — the Sol row-calls were owner-ruled
before application — no fix rides this round: confirmed findings queue for the
owner. Findings are re-keyed by subject; Sol-3 and Terra-3 are one finding.

| # | Source | Subject | Verdict | Re-verification evidence |
|---|---|---|---|---|
| F1 | Terra-1 + Sol-1c | **IF-127 re-pointed against its own recorded rationale** | **CONFIRMED — OWNER-CALL** | Live row: `owner = "LLR-001"` while its `notes` still argue *"Owner is SR-140, not a design row: the seam carries the re-attestation obligation itself, not one module's surface"* — a deliberate 2026-08-15 judgement (log 2026-08-15h) that `47234903` overrode without updating or acknowledging; log `2026-08-17c` lists the re-point (with the candidate-LLR-gap caveat) but never names the recorded contrary rationale. The author found this row independently before the external round ran. Owner rules: revert to SR-140 under the recorded exception, or supersede the note (and, if the ruling's rule is universal, say why the 2026-08-15 exception fails). |
| F2 | Sol-1c | **IF-130 re-pointed against its own recorded rationale — the notes say the chosen LLR does not fit** | **CONFIRMED — OWNER-CALL** | Live `IF-130.notes` (WI-463 mint, corrected at the 2026-08-16b adversarial round): *"No design row fits: of derive_gate.py's four LLRs (LLR-050 `compute`, …), none names `bar_label`"* — and `47234903` set `owner = "LLR-050"` anyway, the exact row the note rules out, leaving both in the file. Same owner fork as F1; here the note even pre-declares the row "ON the v2 S5 owner re-point worklist rather than pretending a design owner exists today". |
| F3 | Sol-1a | **IF-043's new owner answers for half the row's contract** | **CONFIRMED — OWNER-CALL** | IF-043 contract: blocks a push publishing *"a secret or a gated identity"*. New owner LLR-017 (`Secrets pattern scan`) covers the secrets half only; the identity/PII half is LLR-018 (`Two-axis privacy gating`), same module `check_privacy.py`. The pick was disclosed in 17c only as "(the outgoing-range scan)" — the second candidate was not weighed on the record. Owner rules the answerable row (LLR-017, LLR-018, both, or a re-shape). |
| F4 | Sol-1b | **IF-117's new owner is the row whose artifact the seam explicitly disclaims** | **CONFIRMED — OWNER-CALL** | IF-117 consumes `gen_arch_map.module_bindings` and its contract says *"Deliberately NOT the rendered arch-map"* — while new owner LLR-023's detail covers exactly the rendered-map splice + drift check (`build_map`/`splice_region`; `module_bindings` unnamed). A module-name match, not an answerable owner; same candidate-LLR-gap class 17c disclosed for IF-075/088/089 but did not disclose here. |
| F5 | Sol-3 + Terra-3 | **TC-168 binds LLR-174 clauses its cited tests do not exercise** | **CONFIRMED — RECOMMENDED** | Re-verified: the only `--wait-on-limit` test (`test_unparseable_reset_falls_back_and_retries`) passes fallback `1` under ceiling `30`, so the `min(fallback, ceiling)` cap never binds — deleting the `min` leaves all cited evidence green; no cited test drives the parsed-reset-within-ceiling sleep/retry branch (`grep` confirms exactly one wait-on-limit use in the suite); the 3600 default is unpinned. All five cited tests do exist and pass (run this round). TC-168/LLR-174 are `Drafted`, so this is recorded coverage debt, not a false green — but 17d's "five existing tests as evidence" reads as fuller coverage than the tests hold. Recommendation to the executing session before TC-168 leaves Draft: a capped-fallback case (fallback > ceiling) and a parsed-reset retry case. |
| F6 | Sol-4 | **TC-169 leaves LLR-175's declared default (stall-limit 3) unpinned** | **CONFIRMED (MINOR) — RECOMMENDED** | Every stalling case passes an explicit `--stall-limit`; `test_budget_ceiling` commits every session so the default never fires. A changed default leaves all cited evidence green. Same Draft-tier debt class as F5. |
| F7 | Sol-5 | **LLR-153's refusal sentence overstates: a watermark file missing its `WI` line is not refused by the mint** | **CONFIRMED-IN-PART — OWNER-CALL** | Confirmed in code: `next_wi_id` reads `trace.read_watermark(root).get("WI", 0)` — `read_watermark` raises on an absent file or malformed line but not on a missing space, so the mint proceeds on the filename sweep alone; TC-158's refusal test unlinks the whole file. IN-PART: the always-on integrity floor does catch the state (`_mark_covers_live_findings`: *"id watermark declares no mark for {space} — every id space must be marked, or that space is unguarded"*), so the hole is a mint-time vs check-time gap, not an unguarded space. Owner rules whether `next_wi_id` should refuse a missing `WI` mark outright (and LLR-153's sentence tightened either way). |
| F8 | Sol-2 | **SR-173's requirement reads stronger than the acceptance its decomposition tracks** | **CONFIRMED-IN-PART — OWNER-CALL** | The tension is real and lives inside SR-173 itself: requirement *"leaving no partially regenerated set behind"* vs its own acceptance *"no partially regenerated set is left committed"* — a mid-run failure does leave earlier steps' output in the working tree, uncommitted. IN-PART: SR-173 (text and acceptance both) was minted at `4cf98e4f`, BEFORE this review's range; the in-range LLR-142/TC-170 decomposition tracks the acceptance faithfully rather than weakening anything itself. What is in-range is that 17d claimed SR-173 decomposed without surfacing the requirement-vs-acceptance gap. Owner rules the intended reading (uncommitted-partial-acceptable, or true all-or-nothing) and re-words whichever cell loses. |
| F9 | Terra-4 | **TC-170's Method states a failure-path consequence its cited tests never execute** | **CONFIRMED-IN-PART (MINOR) — RECOMMENDED** | Confirmed: `test_regen_never_commits_the_caller_owns_the_commit` runs one green step (everything else skips) and asserts HEAD unmoved + dirty tree; no cited test asserts git state after a mid-run failure, so the Method's *"so a later step's failure can never leave a partially regenerated set in history"* is an inference, not an executed check. IN-PART because the inference is structurally sound today — `regen` contains no commit machinery at all, and `test_regen_fails_loudly_on_a_broken_generator` (TC-135) covers the stop — but a future edit committing only on the failure path would evade the cited evidence. Recommendation: a failure-path git-state assertion when TC-170 leaves Draft. MINOR against Terra's MAJOR: the TC is `Drafted` and the Method's causal clause is framed as consequence. |
| F10 | Terra-2 | Log 2026-08-17c's "49 SR-owned" not reproducible from the live file | **REFUTED** | The 49 is the ruling session's pre-repoint measurement, and the same entry records the acts that changed it: it lists all 19 re-points old→new, and 49 − 19 = 30 is exactly what the live file holds — re-derived independently this round: 81 `Consumes` rows, 30 SR-owned = the 27 WI-469 rows + `IF-032/036/041` `external:`, matching WI-469's table row-for-row. A log entry records its session's acts at that session's state; no sentence in 17c claims the live post-commit file still partitions to 49. (Sol read the same numbers and called the split "reproducible".) |
| — | Sol-1 (framing) | "The 19 re-points are ONLY module-name matches" | **REFUTED as a generalization** | The other 13 re-points resolve cleanly (counterpart module = the LLR's `Module`, one candidate: `IF-039`→LLR-171, `IF-040`→LLR-006, `IF-055/071/085`→LLR-058, `IF-056/082/083/084`→LLR-049, `IF-093`→LLR-154, `IF-101/116`→LLR-002, `IF-089`→LLR-001 — each re-checked this round), and 17c disclosed the judgment-call class on `IF-075/088/089/101/116/127` on the record. The defensible core of Sol-1 is F1–F4. |

**Queue for the owner (nothing applied):** F1–F4 are one ruling shape — does
the item-3 rule ("`owner` points at the design tier wherever a design row
exists for the owner-side endpoint") admit per-row exceptions where the
resolved LLR is not answerable for the row's contract (F3, F4) or where a
recorded per-row rationale argues the opposite (F1, F2)? F7 and F8 are wording
rulings on LLR-153 and SR-173. F5, F6, F9 are Draft-tier test-coverage debts
for the sessions that mature TC-168/169/170 — recommended, no ruling needed.

## Verification after the round (author, this session)

- The three commits' mechanical claims all reproduced before the external
  verdicts arrived: the 81/49→19/27/3 population split re-derives exactly
  (30 SR-owned `Consumes` live = 27 + 3 `external:`; the WI-469 table matches
  the residue row-for-row); every LLR-174/175 factual claim matches
  `agent_loop.py` (`EXIT_STALL=4`, `EXIT_WAITING=5`, defaults 3/0/3600, the
  `min` cap, `note_session` reset-on-commit, WAITING bypassing the guard);
  `intake.next_wi_id` matches LLR-153's rewritten detail; `test_trunk_step` is
  absent from conftest `SLOW_MODULES` (TC-135/170 `Smoke` is right) while
  `test_agent_loop`/`test_agent_loop_policy`/`test_trace_rules` are in it
  (TC-168/169 `Full` is right).
- All 14 tests cited by TC-168/169/170 ran targeted this round: **14 passed**
  (8.8s). The two TC-170 tests and the new stall-counter and bundle-module
  tests are among them.
- Red-check: `test_a_bundle_moduled_owner_matches_on_any_of_its_modules`
  **fails** against the pre-fix `trace_text.py` (extracted from `d7975c96^`
  into a scratch tree) — the new test genuinely pins the `;`-split defect.
- `trace.py --strict` at HEAD: exit 1, `SN=27 SR=67 LLR=157 TC=153 orphans=0
  integrity=0 drafts=61 interfaces=123 form-findings=1`, **113 advisories**,
  the owner-mismatch advisory exactly one (`IF-128`→`LLR-173`,
  `baseline_snapshot.py` vs `scripts/spine_carrier`), `SR-140` the one gating
  form finding — every 17c/d/e checker claim reproduced.
- Smoke tier re-run this round: **1189 passed, 7 skipped** (31s) — matching
  the 17d/e figures.

## Not done here (stated so its absence is not read as coverage)

- No finding was applied; the registries, scripts, tests and plan docs are
  byte-identical to `d7975c96` — this round's only writes are this document
  and the log entry.
- Neither reviewer (nor the author) executed the TC-147/148/158 intake/
  integrate suites this round (Full tier, exercised at close/CI); the SR-174
  "nothing minted" claim was re-verified against the registry rows and TC-158's
  method/evidence text, not by running those suites.
- The first, harness-killed codex attempt produced no verdict and none of its
  partial exploration was used.
- `scoreboard.txt` is the `score_reviews` surface for lane `REVIEW-A` docs;
  round docs are outside it, as with ROUND-SOL.
