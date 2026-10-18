Reviewed: b629f232891d3e6b027a517e13d313d87cf96f26

Full-lane review in the convergence stance, range c58293d5443a881585864be3491f6e0cd0c749c0..b629f232891d3e6b027a517e13d313d87cf96f26 (WI-916, spec docs/work/active/wi-916/WI-916-resync-entry-presence-check.md).

**Verified.** Before hunting I named the failure classes this change admits. Fail-open comes first: a shipped kit change passes the bar with no entry, through a wrong base, a missed changed path or a mis-classified path. Next is a wrong-anchor pass, then fail-closed noise that blocks legitimate work. I drove the real CLI (`scripts/check_resync.py`) in a scratch clone of b629f23 on a `trunk` branch, where `default_base` resolved to HEAD. These cases behaved correctly:
- An edit to `project-trajectory/scripts/trace.py` with no entry is REFUSED and named.
- The same edit plus `### Probe entry [since <HEAD short sha>]` before §4 passes ("1 shipped path(s) changed; entry anchored at b629f23...").
- The same entry anchored at c58293d54 is REFUSED as "anchored at c58293d54, not at the change's base".
- Re-anchoring an existing entry to HEAD, with no new entry, is REFUSED ("no RESYNC_PACK.md entry added").
- On the lane itself the check prints "OK, no shipped path changed (base c58293d5...)". RESYNC_PACK.md is a kit-side exclusion, so the lane's own §5 edit owes no entry, and the Done-when "landing's own entry passes the check" holds.

Fail-open hunts that found nothing:
- `changed_paths` covers the working tree against the base with untracked files and both sides of a rename, and returns None, never an empty list, on a failed read.
- A deleted shipped file is judged through the base inventory.
- A file whose classification flips is judged through `both`.
- An unclassified kit path is denied by default.
- An ambiguous or unresolvable short anchor resolves to None and is refused.
- `pre-` and `Reserved:` headings never count.
- On the trunk checkout `claim_base` finds no `-> active/<trunk>` claim, so the base is HEAD. The coordinator-cycle recipe runs the bar on the staged squash before the landing commit, so the landing is judged against its parent and not vacuously.
- The repo's `.gitattributes` carries no `export-ignore`, so `git archive` of the base kit is complete.

Convergence fix confirmation: I swapped each fix's pre-fix script into the clone.
- The re-anchor cancellation fix (69131a5bf): with 91e201242's `scripts/check_resync.py`, `test_a_re_anchored_existing_entry_does_not_count`, `test_a_retitled_and_re_anchored_entry_does_not_count` and `test_a_new_entry_beside_a_removed_one_does_not_count` FAIL (3 failed).
- The legacy-console fix (b629f2328): with ce1a33825's script, `test_a_refused_heading_a_legacy_console_cannot_encode_is_still_named` FAILS.
- The whole new module fails at the base, since `scripts/check_resync.py` does not exist at c58293d5.

Done-when coverage:
- Deliverable 1:
  - shipped/no entry: `test_a_shipped_change_with_no_entry_is_refused`
  - other-commit anchor: `test_an_entry_anchored_at_another_commit_is_refused`
  - edited-only: `test_an_edited_only_entry_does_not_count`, plus the re-anchor cases
  - this-repo skill: `test_a_change_only_to_a_this_repo_skill_owes_no_entry`, plus `test_the_real_inventory_classifies_the_kit`
  - deleted shipped file: `test_a_deleted_shipped_file_owes_an_entry`, `test_an_untracked_shipped_file_counts`
  - outside the kit: `test_a_change_outside_the_kit_owes_no_entry`
  - unreadable base: `test_an_unreadable_base_is_refused`
  - absent pack: `test_an_absent_pack_is_refused`
  - inventory failure: `test_an_uncomputable_inventory_is_refused`
  - generator sources, deny by default and stop shipping: their named tests
  - HEAD on trunk: `test_the_cli_on_trunk_judges_against_head`
- Smoke tier: `test_check_resync` is not in `SLOW_MODULES`, so it is smoke tier. I did not re-measure the 60 s budget, because the brief forbids running the smoke tier.
- Grammar one home: `test_the_entry_grammar_has_one_home`.
- Wiring order: `test_the_declared_commit_bar_runs_the_strict_lints_before_its_budget`. No `.githooks`, `check.py` built-in step or `[step:]` change is in the diff.
- K4 is gone from the rubric. RESYNC_PACK.md §5 and the enforcement-audit row are present.
- WI-913 (b803dd019) and WI-914 (4fe9114a1) landed on trunk before the base, and the plan-gate pass record is in `docs/plans/WI-916/pass.toml`.

Rubric anchors:
- K1/K2: no SN/SR/LLR/TC row is added or changed.
- K3: the check is untraced tooling per the spec, with no `Implements:` tag and no Status flip.
- Interface sweep: the diff changes the IF-049 `[run]` smoke line's value, not its format, so the counterpart contract (`docs/requirements/interfaces.toml` IF-049) is retained.
- B1: each finding below is confirmed by running the CLI.

**Commands**
- `git rev-parse HEAD` -> b629f232891d3e6b027a517e13d313d87cf96f26
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp <scratch>/wi-916 tests/test_check_resync.py tests/test_resync_pack.py tests/test_smoke_budget.py` -> `42 passed in 29.92s`
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (941 work item(s), 822 done (87%), 30 cancelled, graph acyclic).` (exit 0; four pre-existing WARN lines about other WIs)
- `python scripts/check_resync.py` (lane worktree) -> `check_resync: OK, no shipped path changed (base c58293d5443a881585864be3491f6e0cd0c749c0)`
- Scratch clone of b629f23 on `trunk`, `python scripts/check_resync.py`:
  - shipped edit, no entry -> exit 1, `REFUSED project-trajectory/scripts/trace.py: no RESYNC_PACK.md entry added for this change`
  - plus an entry at HEAD -> exit 0
  - entry at c58293d54 -> exit 1
  - re-anchor only -> exit 1
  - retitle only -> exit 1
  - retitle plus a valid new entry -> exit 1
- Pre-fix swaps in the clone, against tests/test_check_resync.py:
  - `-k legacy_console` with the ce1a33825 script -> `1 failed`
  - `-k "re_anchored or retitled or removed_one"` with the 91e201242 script -> `3 failed, 1 passed`

**Findings**

- [MINOR] docs/enforcement-audit.md:35 -> The row says "a re-anchored or retitled entry counts zero", and so do the docstrings at scripts/check_resync.py:8-10 and :197-200. In fact a retitled entry that keeps its true anchor is REFUSED outright, not counted zero. In a clone of b629f23, retitling `### The TC \`Tier\` column [since af852db7]`, with no shipped change, exits 1 with "anchored at af852db7, not at the change's base". So an honest heading fix to any landed entry can never pass the bar. Whoever reads the enforcement reference is told the opposite. -> Reword the three sites: a retitled heading is refused unless anchored at the base, and only a heading re-anchored at the base counts zero. Or, if retitles are meant to pass, pair a removed base heading with its same-anchor replacement as an edit. Either way, the code and the record must say the same thing. -> @owner
- [MINOR] scripts/check_resync.py:216 -> A base entry heading that the working tree no longer holds cancels a valid added entry. When that happens, every shipped path is refused with NO_ENTRY ("no RESYNC_PACK.md entry added for this change") although an entry was added, and the refusal names neither the cancelling heading nor the cancellation. Observed: a retitle plus a valid `### Probe entry [since b629f2328]` plus an edit to trace.py prints exactly that message for trace.py. The builder gets a reason that contradicts what they see in the pack. -> When `entries < 1` but some added heading passed `_heading_refusal`, give the cancelling base heading(s) as the reason instead of NO_ENTRY. This is a message change, not a new guard, so no unrepresentable clause is owed. -> @owner

VERDICT: APPROVE findings=2
