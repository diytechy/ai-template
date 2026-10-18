Reviewed: f881d233d807e458ac4bc867663af2912e3db6d6

Verified. Full-lane review of 6533a2331..f881d233d (plan commits 008035121, 5aee0fd1b, 01ede9e6e; build f881d233d) against `docs/work/active/wi-916/WI-916-resync-entry-presence-check.md`. Worst failure classes hunted first: fail-open (a shipped change passing with no entry, or an input the check cannot read passing), then false refusal on a normal workflow (pycache/ignored files, CRLF checkouts, trunk landing base). I drove the real `check_resync.run` and the CLI on a shared clone of the lane tip (scratch only), against the real kit inventory with base 6533a2331:
- an edit to `project-trajectory/scripts/trace.py` with no entry was refused; the same edit plus `### Trace tweak [since 6533a2331]` passed; the same edit plus an entry anchored at trunk's 396ff9f44 refused both the heading and the path;
- an untracked new `project-trajectory/scripts/newthing.py` was refused;
- an edit to the `scope: this-repo` skill `render-dashboard-critique/SKILL.md` passed with no entry;
- adding `scripts/check.py` to `mapping-source-exclusions` (same bytes in check.py) refused `scripts/check.py` as a file that stops shipping. Adding `scripts/trace.py` there correctly still ships it as a generator source;
- the CLI on a temp trunk (no linked worktrees) judged against HEAD and resolved a 9-char anchor (1.2 s).
`__pycache__/` and `*.py[cod]` are gitignored here, so running kit scripts does not create untracked kit paths. The pack sections split correctly on a CRLF checkout (`read_text` and `splitlines`). `####` sub-headings in existing entries are not picked up as `### ` headings. `default_base` gives HEAD on the primary trunk checkout, because no claim subject names the trunk branch. The changed-path check is cut to an empty kit only when no `project-trajectory/` path changed, and every route that flips a path's shipping status (the exclusions file, `bootstrap.py`, skill frontmatter) is itself a kit path. So that shortcut cannot hide a flip. No requirement rows changed, so there was no registry sweep. WI-913 and WI-914 are both under `docs/archive/work/complete/` at the base. The pre-commit hook, `check.py` and every `[step:]` are untouched. K4 is gone, and no other live file cites it. The new and changed tests cannot pass on the pre-change code: the module does not exist there, and the old `[run] smoke` chain lacks the new step. `test_check_resync` is not in `SLOW_MODULES`, so it is smoke tier. Its serial cost under pytest's job-object cap read 40.9 s (`--durations`; the same CLI path costs 1.2 s outside pytest). I did not measure the tier's 60 s budget (the brief bars running the tier). Done-when map, deliverable 1 (D1):
- shipped, no entry: `test_a_shipped_change_with_no_entry_is_refused`
- anchor at another commit: `test_an_entry_anchored_at_another_commit_is_refused`, `test_an_unresolvable_anchor_is_refused`
- edited-only entry: `test_an_edited_only_entry_does_not_count`, which covers body edits only (see finding 1)
- this-repo skill: `test_a_change_only_to_a_this_repo_skill_owes_no_entry` + `test_the_real_inventory_classifies_the_kit`
- deleted shipped file: `test_a_deleted_shipped_file_owes_an_entry`, `test_an_untracked_shipped_file_counts`
- change outside the kit: `test_a_change_outside_the_kit_owes_no_entry`
- unreadable base: `test_an_unreadable_base_is_refused`; also absent pack and uncomputable inventory
- one grammar home: `test_the_entry_grammar_has_one_home`

The remaining Done-when items map as follows:
- D2 bar order: `test_the_declared_commit_bar_runs_the_strict_lints_before_its_budget`.
- D3 records: K4 removal, the §5 rewording and the audit row, all checked by reading.
- Landing's own entry: no shipped path changed in this lane (RESYNC_PACK.md is excluded as kit-side), so none is owed and the check reads OK on the tip.

Coverage-extension notes (fail-closed, no severity):
- Retitling an existing entry's heading counts as an "added" heading anchored elsewhere, so it is refused even in a pack-only change.
- Deleting an existing entry is not judged; that stays with review.
- `kit_classes` with a relative `kit_dir` misresolves the `scripts` path because it also sets `cwd`. The CLI always resolves `--root`, so only a direct API caller reaches it, and it fails closed.

Side effect: `trace.py --strict-integrity` rewrote the gitignored `docs/test/report.md` in the worktree. `git status` stays clean and HEAD is unchanged.

Commands:
- `git rev-parse HEAD` -> f881d233d807e458ac4bc867663af2912e3db6d6
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-18a/wi916-r1-opus/wi-916 tests/test_check_resync.py tests/test_resync_pack.py tests/test_smoke_budget.py` -> 36 passed in 19.88s
- `python -m pytest -q -p no:cacheprovider -n 0 --durations=6 --basetemp (same) tests/test_check_resync.py` -> 20 passed in 40.90s
- `python project-trajectory/scripts/check_trajectory.py --strict` -> check_trajectory: clean (941 work item(s), 821 done (87%), 30 cancelled, graph acyclic). exit 0
- `python project-trajectory/scripts/trace.py --strict-integrity` -> Traceability: SN=31 SR=131 LLR=304 TC=318 orphans=0 integrity=0 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=3. exit 0
- `python scripts/check_resync.py` (lane tip) -> check_resync: OK, no shipped path changed (base 6533a2331b2eba3ebe4c0b9e94d4baa5bfc0ddb3) exit 0
- scratch probes of `check_resync.run` on a `git clone --shared` of the lane tip (scenarios above), and a timing probe of the CLI on a stub temp repo -> as reported in Verified

- [MINOR] scripts/check_resync.py:198 -> An edit to an existing entry's heading counts as this change's entry, which D1 says it must not ("These do not count: an edit to an existing entry"). Probe: re-anchoring the base's `### The TC \`Tier\` column [since af852db7]` to `[since 6533a2331]`, with an edit to the shipped `scripts/trace.py` and no new entry, made `run` return no refusals. `test_an_edited_only_entry_does_not_count` covers only a body edit with the heading set unchanged. No rubric anchor; this is the brief's D1 coverage map. -> Count an added heading as an entry only when its title matches no heading title at the base, and (or) refuse a change that removes a base heading. Add a test for the re-anchored and retitled cases. -> This is validation at the pack's own trust boundary (the spec's Trust section: the hand-edited pack is the producer), so no unrepresentable clause is owed. -> @owner
- [MINOR] docs/enforcement-audit.md:35 -> The row's honest residue says "a commit made without the bar is caught at the next build round's bar or at landing". That holds for a lane commit only. On trunk the base is HEAD (`default_base`), so a trunk-direct commit made without the bar leaves its shipped change outside every later range and is never caught. -> Say "a lane commit made without the bar ...", and add that a trunk-direct commit made without the bar escapes the check. -> @owner

VERDICT: CHANGES-REQUESTED findings=2
