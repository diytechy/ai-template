Reviewed: 5ba44ea0ac1dd8b89ede713fad627074a2806f06

**Verified.** `git rev-parse HEAD` in the lane printed the reviewed commit. Reading scope: the brief's three-dot diff (hook, check.py, integrate.py, kitlib/done_when.py, conftest helper, three test modules, LLR-019/307/309 and TC-019/325 with their last_approved copies and act 116, RESYNC entry, recipes §3), the WI-921 spec in full, and the rubric. Failure classes I hunted first: fail-open (an unblessed Done-when change reaching trunk), wrong-reading fail-open (a quoted path or failed git read taken as "no change"), and fail-closed breakage of normal kit routes.
- **Real paths.** I bootstrapped a scaffold from the lane's kit, set `core.hooksPath .githooks` and made real `git commit`s on `main` after a claim commit. A Context-only trunk amendment of the claim copy printed `PASS  done-when-blessed`. A trunk commit narrowing its Done-when printed `integrate: REFUSED - WI-007: its Done-when differs ... (digest sha256:c3f79f15c10cc276) ...` and `FAIL  done-when-blessed`. The same probe on the pre-fix kit (9ddc5ee2a's hook, check.py, integrate.py, done_when.py) never ran the step. The scaffold's other FAILs (trajectory-map, registry-integrity) come from its unfilled registries and are not related to this change.
- **Pre-fix runs.** I ran the post-fix tests against the pre-fix code files in an export. Every new regression test fails there: the census names `done-when-blessed: a built-in step in no class (floor, by name, or not at commit)`; both two-commit-landing params, the trunk amendment, the claim-copy deletion, the index-delta, branch-identity and quoted-path tests each fail with `AssertionError: None`; the shipped-floor test fails on `'PASS  done-when-blessed' in ...`; and the scaffold test fails on `'done-when-blessed' in [...]`.
- **Lossless read in isolation.** I mutated only `staged_changes` and `_copy_at` back to the plain `git_out` listing, keeping the rest post-fix. `test_a_claim_copy_whose_path_git_quotes_is_judged_like_any_other` then fails (`AssertionError: None`) while the plain-path trunk amendment test passes. So that test pins the lossless read itself.
- **Census and floor.** `check.steps(80,"full","all")` returns 38 names, equal to `BUILTIN_STEP_NAMES`. Census tier: smoke, since `test_commit_floor_census` is not in `SLOW_MODULES`.
- **Bypass probe.** I tried to slip past the lone-`A` exemption with a two-commit slug re-cut on trunk: add an edited second copy, then delete the old one, then close. `staged_done_when_refusal` passes all three. But the first commit puts two specs for one WI id, which `check_trajectory.py:589` reports as a duplicate-id integrity error (`trajectory` is in the floor). This rests on reading that line, not on a run, and the chain is contrived (PROCESS.md §6), so it is not raised.
- **Done-when coverage.**
  - (1) floor + comment: the diff, the shipped-floor test, the census.
  - (2) hook-driven test incl. scaffold: fail before, pass after (above).
  - (3) census in smoke, fails before naming the step, plus its three fault tests.
  - (4) WI-835 replay, trunk amendment, no-Done-when change: covered; each held case fails pre-fix.
  - (5) unlistable index delta: covered, fails pre-fix.
  - (6) RESYNC entry `[since 9ddc5ee2a]`, which equals trunk `refactor_again`'s tip.
  - (7) LLR-019/307/309 and TC-019/325 amended. Their registry hunks are byte-identical to the last_approved hunks; act 116 re-attests those five.
  - (8) `check_trajectory --strict` is clean, and `trace.py --strict`'s only finding is LLR-292's. I did not run the smoke budget (the brief forbids it).
- **Rubric and spine.** WI-921's own Done-when is unchanged from its trunk claim copy. K3: every new `Implements:` tag names LLR-307 (module `kitlib/done_when.py`, symbols listed) or LLR-309 (`staged_done_when_refusal`). The LLR-307/309 text matches `_staged_base` (K1).
- **Not run here.** The 12 posix-shell-gated tests were skipped on this host. The real-`git commit` probe above stands in for them.
- **Side effects.** `trace.py` rewrote the git-ignored `docs/test/report.md` in the lane, and the Python runs refreshed ignored `__pycache__`. No tracked file changed (`git status --porcelain` is empty).

**Commands**
- `git rev-parse HEAD` -> `5ba44ea0ac1dd8b89ede713fad627074a2806f06`
- the brief's pytest command (18 modules, `-n 2`, the literal basetemp) -> `407 passed, 14 skipped in 630.23s (0:10:30)` (12 skips: posix-shell gate unsatisfied)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (920 work item(s), 801 done (87%), 30 cancelled, graph acyclic).` exit 0
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=303 TC=317 orphans=0 integrity=0 ... form-findings=1 ...` exit 0
- `python project-trajectory/scripts/trace.py --strict` -> one `FINDING (requirement form): LLR LLR-292 ...`, same summary, exit 1 (the Done-when's permitted LLR-292 finding)
- pre-fix export: the census module + the WI-921 tests -> `11 failed, 3 passed` (the 3 passes are the census-function fault tests, which do not read the hook)
- mutation export (lossless reads reverted) -> `1 failed, 1 passed` (the quoted-path test fails)
- `probe/e2e_hook.sh` (scaffold + real `git commit`, post and pre kit) -> post: `PASS  done-when-blessed`, then `FAIL  done-when-blessed` with the digest; pre: the step never runs
- `probe/slug.py` (two-commit slug re-cut) -> `None` / `None` / `None` (closed by the duplicate-id integrity error, not raised)

**Findings**
- [MINOR] project-trajectory/hooks/pre-commit:291 -> for clarity (K4). The hook's fail-open residue list leaves out the linked-worktree residue that LLR-307's detail and the spec's Trust section state (D-014): a commit in a linked worktree on the trunk branch, while the primary checkout is on another branch, reads as elsewhere, so a non-close Done-when change is not judged. The RESYNC entry (project-trajectory/RESYNC_PACK.md:8368) leaves it out too. Also, "One residue fails open" introduces five shapes. -> add the linked-worktree shape to both lists and say "These residues fail open". -> @builder
- [MINOR] project-trajectory/scripts/check_trajectory.py:2587 -> coverage-extension note, fails closed by name (K1). The hold-by-rename remedy still says "or delete the stranded claim". On trunk, the hook now refuses that deletion (a lone `D` of a claim copy) with "no copy of its spec ...", and no blessing releases it (pinned by test_a_trunk_commit_deleting_a_claim_copy_is_held_and_no_blessing_releases_it). So the kit's own remedy text names an act the floor refuses. -> drop that alternative, leaving the PARTIAL close (a close, judged and released when the Done-when is unchanged), or name the refusal next to it. -> @builder
- [MINOR] docs/test/test-cases.toml:3315 -> for clarity (K1). TC-325's evidence lists test_a_trunk_commit_deleting_a_claim_copy_is_held_and_no_blessing_releases_it, but its method's run list does not name it, and neither method nor expected states what it asserts (a deleted claim copy on trunk is held, and no blessing releases it). -> add it to the method's run list with a one-clause assertion. -> @builder
- [MINOR] project-trajectory/scripts/kitlib/done_when.py:574 -> design note (K3). After this change `staged_closes` has no non-test caller (`staged_done_when_refusal` goes through `staged_hold`), yet its return shape changes to `(closes, why)`, an adopter-visible IF-286 API break the RESYNC entry has to announce, for a function the kit no longer uses. -> either delete it (and its `code_symbol` entry) and let the tests read `staged_changes`, or keep it and say in the IF-286 contract that it is kept for external callers. -> @builder

VERDICT: APPROVE findings=4
