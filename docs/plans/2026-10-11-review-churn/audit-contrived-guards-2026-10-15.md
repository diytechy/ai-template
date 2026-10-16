# Audit: guards built for contrived review findings (lanes reviewed 2026-10-08 onward)

Read-only audit, 2026-10-15. Rule applied: PROCESS.md §6 "Review threat model" (2026-10-08), plus the owner's 2026-10-13 extension: contrived, improbable scenarios are dismissed too, including any scenario that needs a hand act the process forbids or tools used in an order no supported route produces. Malformed agent-written repo content, supported configurations and regressions stay in scope.

**What was read.** Trunk lanes with review files dated 2026-10-08 or later: wi-834, 848, 852, 853, 858, 870, 880, 881, 887, 913 and 921. Lanes whose rounds raised no MAJOR were checked and had nothing to classify: wi-823, 847, 854, 859, 865, 869, 874, 875, 882, 884, 888, 892, 895 and 901. The open worktrees read were wi-911, 914, 923, 798 and 902. WI-852's rounds live only in `C:/Projects/ai-template.wt/wi-852-notes/sol-852-full*-out.md`; its decisions record names them.

**Totals.** 69 MAJOR findings and 0 BLOCKERs. Of these, 17 were skipped:
- 6 were dismissed.
- 9 were answered with text, a spine act or an operational step.
- 1 became an owner-ruled successor row (wi-921 004 F1, now WI-925).
- 1 was accepted but is not built yet (wi-902 015 F1).

The other **52 were accepted and built**. Commit hashes below are lane commits; the archive/lanes ref and the lane branches keep them.

## Summary

| Class | Findings | Table rows |
|---|---|---|
| CONTRIVED | **20** | 18 |
| PLAUSIBLE | **32** | 32 |

The eight findings first graded UNCLEAR were reclassified after the owner's review of this report (2026-10-15h): five to CONTRIVED, three to PLAUSIBLE, each row's reason saying why. The owner's rulings on the table: WI-834's grammar rows are contrived (the by-construction alternative is refusing model work at the launch point during a blackout); WI-834's hook re-enabling folds into WI-926; WI-852's duplicated-count fix is discarded; WI-858's fix is kept because it simplified the code; WI-881's interrupt and late-spawn guards are removed; WI-902's two history rows dissolve with its record-at-close reshape; WI-921's non-ASCII fix is kept. Each removal is its own row, filed after reading the original rationale.

### The most costly CONTRIVED builds

1. **wi-834, the blackout hook's shell grammar** (002 F1, 018 F1, 024 F1, 028 F1, 030 F1). Each round, one more improbable launch form was built:
   - a model call inside a here-document's `$(...)`;
   - `$result.Answer = claude`;
   - `. claude`;
   - `time -p claude`;
   - `coproc WORK while claude`.

   The cost was about six narrow rounds, dispute sittings 025 and 031 (both FIX), and part of checkpoint sittings 023 and 038. `kitlib/shell_line.py` is now 359 lines. `coordinator_guard.py` grew to 1705 lines, and the module ratchet forced the `kitlib/guard_hooks.py` split. Sitting 031 itself called the coproc form "close to contrived".
2. **wi-887, store record-shape validation** (001 F2, 002 F1, 007 F1/DA, 010 F1/DC). Four rounds and two sittings (008, 011) typed every optional and nested field of the kit-written runtime JSON store. Every reproduction needs a hand-edited store file; the coordinator wrote as much in D-005 and still routed it to a sitting.
3. **wi-881, interrupt windows in the kill tree** (006 F1, 007 F1). Two build rounds, two narrow rounds, a second checkpoint and a fresh gate. They added about +192/−97 lines to `agent_session.py`, about 200 test lines and a `TreeNotEnded` BaseException. The scenario is a Ctrl-C landing in a window of a few lines between resuming the child and publishing its job, and then a denied SYNCHRONIZE right.
4. **wi-852, the "rollup" branch-name refusal** (dispute B, then the `Rollup` letter case). The code is small, but it took a shared dispute sitting (006), a re-blessing sitting (007) and two extra full-lane gates: full4 found only the case variant, and full5 confirmed it. The coordinator had argued it contrived; the sitting ruled FIX.
5. **wi-798, Windows id aliasing** (`WORK` vs `WORK.`, and token-variable names that differ only in case). The code was cheap and rode a round that ran anyway. It is listed for the class, not the cost.

**Context.** Every CONTRIVED build above was ruled or built before the 2026-10-13 extension, under the host-only test of 2026-10-08. The sittings (025, 031, 852-006, 887-008, 887-011) weighed "is it a compromised host?" and "is the fix cheap?", not "would an agent or a supported route ever produce this?".

## Findings

| Lane | Round file and finding (quoted) | What was built | Class | Reason |
|---|---|---|---|---|
| wi-834 | 002-REVIEW-A-9bc1eb2-narrow F1: "the actual blackout hook now allows Bash `cat <<EOF\n$(\nclaude -p x\n)\nEOF`" | af4083d03: expandable here-doc and here-string bodies are read (`kitlib/shell_line.py` +55/−15) | CONTRIVED | No agent launches a model from a substitution inside a here-doc body during a pause. Evasion-shaped; its sibling R4F1 was dismissed at sitting 005. |
| wi-834 | 018-REVIEW-A-fd605d5-narrow F1: "no denial for `$result.Answer = claude -p x`, `$answers[0] = claude -p x`" | D-022/D-023, 70d69014f + f5757cc67: an assignment is found by its unquoted operator, and a Word carries its quoted spans (`coordinator_guard.py` +84/−52, `shell_line.py`) | CONTRIVED | Property, index and typed-array targets for a model call are forms no agent writes. The ordinary `$r = claude` was already fixed (R16F1). |
| wi-834 | 024-REVIEW-A-5d0a27e F1: "the actual hook allows PowerShell `. claude -p x` and `$r = . claude -p x`" | Sitting 025 FIX, D-024; 2ca10961f (`coordinator_guard.py` +15) | CONTRIVED | Nobody dot-sources a native CLI. The sitting ruled on grammar coverage, not on whether anyone writes it. |
| wi-834 | 028-REVIEW-A-72615c7 F1: "Bash's ordinary `time -p claude -p x` ... starts model work through an armed blackout" | D-025; a3658d32a, a grammar-word table meant to "derive the full set of grammar" (+32/−6) | CONTRIVED | Timing a model call with `-p` inside a blackout is improbable; plain `time claude` was already denied. D-025 widened the fix to enumerate all grammar. |
| wi-834 | 030-REVIEW-A-a3658d3-narrow F1: "still allows `coproc WORK while claude -p x; do :; done`" | Sitting 031 FIX, D-026; 3de760859 (+8/−4) | CONTRIVED | The sitting conceded "close to contrived"; a named coprocess whose loop condition launches a model is fantastical. |
| wi-887 | 001-REVIEW-A-01ac7b2 F2: "a malformed scoped object such as {"scope": <iteration scope>, "state": "active"} reaches _record_path". 002-…-narrow F1: "Removing judged from an otherwise valid active scoped record" | 031da1719 + e47a64b2b: one record reader with declared variants (`session_keep.py` +48/−24, +150 test lines) | CONTRIVED | Needs a hand-edited, kit-written runtime file. `judged` and `governing_hash` existed before the lane, so no upgrade path produces these shapes. |
| wi-887 | 007-REVIEW-A-27831e0 F1 (DA): "changing rollout_requests to the JSON string "oops" still yields a record" | Sitting 008 FIX, D-004; ebc38a33f, which types every optional field (+21/−3, +98 test lines) | CONTRIVED | A hand edit of the runtime store. It was in scope only because the lane's own Trust text promised "malformed = no record". |
| wi-887 | 010-REVIEW-A-1e11dd4 F1 (DC): "replacing its lease with {"holder": [], "until": a future epoch} still makes store_load return" | Sitting 011 FIX, D-005; 6b6affc0d (+36/−6, +67 test lines) | CONTRIVED | The fourth round of the same hand-edit class. D-005 itself says it "needs a hand-edited runtime store file". |
| wi-852 | sol-852-full3-out.md F2 (dispute B): "Filing on the valid branch `rollup` loses the accepted review." | Sitting 006 FIX, D-005/D-006; 74cbf7804: filing refuses the rollup directory, whose name `ROLLUP_DIR` moved into `kitlib/verdict` | CONTRIVED | Claims mint `wi-NNN` lanes, so this needs a hand-chosen branch that collides with a generated directory. The coordinator argued exactly that. |
| wi-852 | sol-852-full4-out.md F1: "On a real branch named `Rollup`, the actual `file` command exits 0" | D-007; 90c2f740c, a case-insensitive refusal | CONTRIVED | A letter-case variant of the same hand-named branch. It cost a fourth and a fifth full-lane gate. |
| wi-881 | 006-REVIEW-A-0960348 F1: "A coordinator interruption during the new Windows containment/resume stage bypasses cleanup" | D-006; d30097e3d: the spawn owns the child until hand-over, under one try/finally (`agent_session.py` +124/−84, +98 test lines) | CONTRIVED | Needs a Ctrl-C to land between resuming the child and publishing its job, a window of a few lines. |
| wi-881 | 007-REVIEW-A-b31c3d2-narrow F1: "Confirmed with a real resume followed by KeyboardInterrupt and denied member wait access" | D-007; 4d412d9e2, a `TreeNotEnded` BaseException (+68/−13, +99 test lines) | CONTRIVED | Stacks the same millisecond interrupt window on a denied SYNCHRONIZE right: a guard on a guard. |
| wi-798 | 001-REVIEW-A-290c777 F2 and F3: "Accepted Windows IDs WORK and WORK. name the same physical home"; token-file variable names that differ only in case | D-008; 9752b92ea: an account-id grammar and `env_name_key` comparison (`agent_route.py`) | CONTRIVED | Needs the owner to declare two accounts differing only by a trailing dot or letter case. The code was cheap. |
| wi-834 | 018 F2: "Re-enabling hooks silently deletes unrelated existing hooks when they share a group with coordinator_guard.py" | D-022/D-023; command-level ownership in the new `kitlib/guard_hooks.py` (+117) | CONTRIVED | Needs the user's own command inside the kit's hook group. That is legitimate user config, but uncommon. Reclassified after the owner's review (2026-10-15h): "re-enabling hooks" is not a normal act. The owner's rule replaces it: check the required hooks by name, install them on first run when none are there, complain and exit when other hooks occupy the slot (into WI-926). |
| wi-852 | sol-852-full2-out.md F2: "A bound review containing `VERDICT: APPROVE findings=7 findings=0` and no findings is accepted" | 3d17ac209: refuses a duplicated field (`review_brief.py`) | CONTRIVED | Agent-written verdicts are in scope, but no model writes a duplicated count. A round later the whole-grammar check superseded it. Reclassified after the owner's review (2026-10-15h): discard; agents are trusted to judge and to write a well-formed verdict line, and the whole-grammar check already superseded this fix. |
| wi-881 | 002-REVIEW-A-8a82eeb-narrow F1: "a normal descendant can be created after _open_job_members returns and before TerminateJobObject" | D-004; 86e533acd: the job is closed to new members before the snapshot (+125/−30, +100 test lines) | CONTRIVED | Late spawns happen, but the harm is milliseconds before an already-terminated process is signalled. The broken guarantee was the lane's own (D-003). Reclassified after the owner's review (2026-10-15h): remove; a few milliseconds of signalling an already-terminated process is not impactful enough to build anything around. |
| wi-902 | 003-REVIEW-A-69c1237-narrow F1: "_standing_successors treats an exact title match as proof of prior mint identity" | Sitting 004 FIX, D-004; 5785b35b1 (`intake.py` +46/−11) | CONTRIVED | Titles are agent-written (in scope), but this needs an exact title collision with an unrelated row that carries lineage. Reclassified after the owner's review (2026-10-15h): an exact title collision with an unrelated row is improbable (a title is plain text, the WI id a separate field); using a title as identity is the smell, and WI-902's record-at-close reshape removes it. |
| wi-902 | 010-REVIEW-A-7768b93-narrow F1: "_landing_commit treats the oldest visible path-touch as a proven landing even when it is a shallow boundary" | Sitting 011 FIX, D-007; cc27d43ae (+18/−10, +109 test lines) | CONTRIVED | Shallow clones are ordinary git, but no kit route runs the recovery sweep in one (the kit's CI uses `fetch-depth: 0`). The reviewer wrote the shallow file by hand. Reclassified after the owner's review (2026-10-15h): no kit route runs the sweep in a shallow clone, and the reviewer built one by hand; WI-902's record-at-close reshape stops reading history at all. |
| wi-834 | 001-REVIEW-A-785a004 F1: "allows ... `env -S 'claude -p x'` ..., but denies harmless `echo 'pause; claude notes'`" | D-010/D-011; 9bc1eb2: new `kitlib/shell_line.py` (+272), and an unreadable line is denied fail-closed | PLAUSIBLE | Over-denying a quoted `;` during close-down is plausible. The evasion half (`env -S`, a quoted prefix) is contrived. This seeded six later grammar rounds. Reclassified after the owner's review (2026-10-15h): the over-denial half (a harmless quoted `;` denied) is what a normal agent hits, and the quote-aware reading answers it; the evasion half (`env -S`, a quoted prefix) stays contrived and is dropped with the grammar rows. |
| wi-858 | 001-REVIEW-A-4d1db06 F1: "call 4 replayed call 2's marker and also resumed session-1 while call 3 remained running" | D-002: consumption is bound to the per-call lease (`session_keep.py`) | PLAUSIBLE | Needs a failed marker unlink (real on Windows) plus overlapping calls on one retained session. The fix simplified the code rather than adding a guard. Reclassified after the owner's review (2026-10-15h): keep; the failed unlink is real on Windows and the fix simplified the code rather than adding a guard. |
| wi-921 | 001-REVIEW-A-bd4d7da F1: "a valid claimed spec with a non-ASCII slug, such as WI-007-café.md, passes unblessed" | D-012; f69a9c95f, the lossless path reader (`kitlib/done_when.py` +24/−17) | PLAUSIBLE | A default git setting, and it fails open. But minted slugs are ASCII, so only a hand-named spec reaches it. The fix reused an existing reader. Reclassified after the owner's review (2026-10-15h): keep; filing a row by hand is a documented route, so an adopter's hand-chosen non-ASCII slug is reachable under git's default path quoting, and the fix reused git's exact path reader. |
| wi-834 | 001 F3: "The promised review-next/handoff and rework-producing wrap-up scenario is absent" | D-012; 9bc1eb2, a test only | PLAUSIBLE | Coverage of a supported route that the spec promised. |
| wi-834 | 009-REVIEW-A-ecca75b F1: "a wrap-up starts at 18:59, the tick runs at 19:01 while that call is still in flight" | 8cb21762d (`session_keep.py` +10/−4) | PLAUSIBLE | Long adjudications straddle the window's edge on the supported service flow. |
| wi-834 | 012-REVIEW-A-3b1d473 F1: "with the real C:\Python38 first on PATH and the real 3.11 runtime still installed" | D-017; a65b0b5a3, one resolved interpreter for every `run.*` and `dev-setup.*` | PLAUSIBLE | This is the owner's own workstation, as D-016 recorded. |
| wi-834 | 016-REVIEW-A-e6717f0 F1: "denies `claude -p x` but allows `$response = claude -p x`" | Sitting 017 FIX, D-020/D-021; fd605d5b1 | PLAUSIBLE | Ordinary PowerShell output capture. |
| wi-834 | 016 F2: "All eight newly shipped hook commands use bare `python`" | Owner ruling D-019, D-021; fd605d5b1 | PLAUSIBLE | An older Python first on PATH crashed the hook, so the call went through. |
| wi-834 | 024 F2: "a bare Windows run with a working Python but no Git on PATH exit before the menu" | 2ca10961f (`dev-setup.ps1` and its template) | PLAUSIBLE | A regression the lane introduced, on a reachable workstation. |
| wi-834 | 032-REVIEW-A-3de7608 F1: "the root Windows -ForRun interactive branch calls only Offer-Cli and Offer-Signin" | 55b661e98 (`scripts/dev-setup.ps1`) | PLAUSIBLE | The spec's promise was missing on a supported path. |
| wi-852 | sol-852-full-out.md F1: "The rendered review can judge the wrong commit." | e5afee1cf: the brief's range ends at the reviewed sha | PLAUSIBLE | Rendering a sha below HEAD is a normal coordinator step. |
| wi-852 | full F2: "Both `VERDICT: APPROVE findings=0.5` and ... `VERDICT: NEEDS-HUMAN findings=0` exited 0" | e5afee1cf, whole-line validation | PLAUSIBLE | Verdicts are agent-written, and 87 historic files carry several verdict lines (wi-870 D-002). |
| wi-852 | full2 F1: "Filing silently loses reviews from ordinary branch names containing `/`." | 3d17ac209, a branch-scope refusal | PLAUSIBLE | Branches like `feature/x` are ordinary in adopters' repos. |
| wi-852 | full3 F1 (dispute A): "The boundary checks selected tokens rather than the complete grammar" | Sitting 006 FIX; 74cbf7804 | PLAUSIBLE | The root fix for the verdict class; it ended the token patching. |
| wi-853 | sol-review-full-r1.md F1: "A cited fragment replaces the finding ID without checking that the ruling concerns the excluded finding." | D-003 (`plan_coverage.py`) | PLAUSIBLE | A plan exclusion citing the wrong ruling is agent-written; the gate failed open. |
| wi-887 | 001 F1: "persisted mode promotes every retained full-labelled round without authoritative evidence" | D-001; 031da1719 (`kitlib/verdict.py`) | PLAUSIBLE | A supported dial setting under which the merge gate cleared the wrong rounds. |
| wi-887 | 001 F3: "replacing the REVIEWER override leaves the governing hash identical" | 031da1719 (`session_service.py`) | PLAUSIBLE | Editing the override is a supported change. |
| wi-887 | 001 F4: "persisted final drawing always returns an empty route pin" | 031da1719 (`session_keep.py`) | PLAUSIBLE | Two weighted routes is a supported configuration. |
| wi-887 | 002 F2: "After an ordinary markdown template edit between rounds ... sends identical old text" | e47a64b2b (`agent_brief.py`) | PLAUSIBLE | Landings change templates while the loop runs. |
| wi-887 | 007 F2: "context_reset_pct=50 with final_reviewer="persited" resolves to (50, fresh)" | D-004; ebc38a33f (`kitlib/config.py`) | PLAUSIBLE | An owner's config typo, and the documented fallback did not hold. |
| wi-913 | 001-REVIEW-A-96b00df F1: "The closed planmode domain fails OPEN for false, 0, [], and {} in a claim copy" | D-003; 0f23c755b (`kitlib/plan_pass.py`) | PLAUSIBLE | An agent writing `planmode = false` is plausible, and it fails open. The fix is one type check. |
| wi-913 | 004-REVIEW-A-0f23c75 F1: "merely registering this built-in never puts it in the shipped pre-commit hook" | D-004; 21790a1ec, the hook's step floor | PLAUSIBLE | The gate never ran on the normal path. |
| wi-911 | 003-REVIEW-B-bd52ffa F1: "A convergence reviewer that runs the brief's own command therefore prints every earlier accepted finding" | D-010 (`reviewer.template.md` pathspec) | PLAUSIBLE | Reachable in every convergence round. |
| wi-911 | 006-REVIEW-B-6e2ad9f F1: "Every review now loses the delegated-decisions record, including ordinary rounds" | D-012: the exclusion applies to convergence rounds only (`review_brief.py`) | PLAUSIBLE | A regression of every ordinary review. |
| wi-902 | 001-REVIEW-A-52dbc7e F1: "a successfully adopted successor's ordinary completion permanently turns the old disposition into a sweep refusal" | D-001; 977628cff | PLAUSIBLE | The adopted row completing is the ordinary case. |
| wi-902 | 001 F2: "adoption validates and returns no draft but never participates in _apply_supersedes" | 977628cff | PLAUSIBLE | Reached by every adoption on the normal route. |
| wi-902 | 002-REVIEW-A-5a629f0-narrow F1: "title dedup removes the already-minted drafted successor before _write_mint builds lineage" | D-003; 3ad2b4ba9 | PLAUSIBLE | A replayed sweep; this class already stranded WI-541. |
| wi-902 | 008-REVIEW-A-4a8e7f6 F1: "a later bare sweep ... redirects the dependent to that rejected successor" | Sitting 009 FIX, D-006; 7768b93f2 | PLAUSIBLE | The bare sweep is the recovery command the refusal message documents. |
| wi-902 | 010 F2: "_tree_text reads authoritative specification content through kgit.git_out, whose errors="replace"" | D-007; cc27d43ae | PLAUSIBLE | Agents have committed cp1252 bytes into specs. |
| wi-798 | 001 F1: "the actual CLAUDE-A@WORK launch received both CLAUDE_CODE_OAUTH_TOKEN and ANTHROPIC_API_KEY" | D-008; 9752b92ea (`session_service.py`) | PLAUSIBLE | Ambient API keys are common, so the wrong account authenticates. |
| wi-798 | 001 F4: "resolve_routing_setup raises TypeError for cli=[]/cli={}, token_file_variable=7 and verified=true" | D-008; 9752b92ea | PLAUSIBLE | A malformed registry is in scope. Over-graded, though: a loud TypeError fails closed. |
| wi-798 | 002-REVIEW-A-9752b92-narrow F1: "GEMINI-A@GE1 launched ... with ambient GOOGLE_API_KEY, GOOGLE_GENAI_USE_VERTEXAI" | D-009; 9be10a034 | PLAUSIBLE | The same ambient-credential class, for Gemini. |

## Patterns

1. **Every CONTRIVED MAJOR came from Codex Sol (REVIEW-A).** Its findings carry a boilerplate justification: "validation at a genuine trust boundary (PROCESS §3) ... antidote's smallest change". That framing treats shell text a hook reads, hand-edited runtime JSON and hand-chosen names as trust boundaries, which pre-empts the threat-model dismissal. The Claude stand-ins (the trial on wi-911, 913 and 921 since 2026-10-14) raised no contrived MAJOR, but that sample is three lanes.
2. **Over-broad Trust and acceptance text turns improbable input into a "regression".** Three lane promises did this:
   - wi-887's "malformed record = no record";
   - wi-834's "any command word";
   - wi-881's "returns only once the job is empty" (D-003).

   Each promise made later hand-edit, grammar or timing findings "stated behaviour", which §6 keeps in scope (sitting 008 says so explicitly). Bounding these promises to supported routes would have let those findings be dismissed.
3. **The "third round of a class goes to a dispute" rule became a FIX pipeline.** Nine sittings ruled on findings that were later built. Seven of them covered findings now classed CONTRIVED, and all seven ruled FIX:
   - 834-025 and 834-031 (contrived);
   - 852-006 B (contrived);
   - 887-008 and 887-011 (contrived);
   - 902-004 and 902-011 (first graded unclear, now contrived).

   They asked whether the host was compromised and whether the fix was cheap ("small fix, ends the class"), not how likely the scenario was. Sitting 834-005 is the one contrived finding that was dismissed.
4. **Recurring CONTRIVED families:**
   - (a) one more shell-grammar form per round against a supervision hook;
   - (b) a hand-edited kit-written runtime store;
   - (c) name or identity aliasing: a trailing dot, letter case, `Rollup`, a quoted non-ASCII path;
   - (d) millisecond interrupt and kill windows.
5. **Still pending (not built, so not in the table), with the same shape:**
   - **WI-922** is claimed. It comes from three MINORs on wi-913, which D-006 describes as "each escaping only a hand landing ... or needing a hook bypass" (detached HEAD, a hand `merge --no-ff`, an alias branch after `--no-verify`). Its planner listed 24 shapes.
   - **WI-925** is queued: a reference-transaction hook of about 250–350 lines for amend, cherry-pick, revert, hand fast-forward and linked-worktree shapes on trunk. It is owner-ruled (wi-921 D-014), but most of its shapes are hand acts on trunk.

   Both are worth checking against the 2026-10-13 extension before they are built.
6. **Built proactively, not from a finding:** wi-881 D-005 checks a held handle against PID reuse inside the kill window. It is a contrived scenario built "because it sits at the same boundary".
