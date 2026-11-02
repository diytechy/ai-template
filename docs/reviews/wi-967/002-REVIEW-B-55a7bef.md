Reviewed: 55a7befe0a3fd0a9ae266498140d26228b3f6ecd

Verified. Full-lane review of 3f4b989df..55a7befe0, read against WI-967's row, its spec of record docs/specs/WI-967.md (Problem, The record, Architectural delta, Trust, Critique dispositions), SR-178, LLR-239, LLR-271, LLR-278, IF-220, TC-234 and the new TC-400. The worst failure classes this change admits are: (1) silent wrong content, where an entry names a copy set that differs from what the act wrote (reconstructed from ids, or listing a registry with no live carrier); (2) fail-open, where an entry a commit adds without `copied` passes the hook, especially on the kit's own `git merge --squash` landing; (3) a false refusal of legacy history or of a merge's other parent. I hunted those first, through the real producer and validators on real git repositories built from this repo's registries (scratch probes under r1-967-B/probe/):
- The seed recorded all eight canonical paths. The writer after a legacy history recorded `copied = [system-requirements.toml]`.
- A staged legacy add is refused by the shipped `trace.py --root <tmp> --strict-integrity` (exit 1, "act entry seq 2: the commit adds it without `copied`"). An unstaged legacy entry after a recorded one is refused by the order rule through trace.py.
- A lane's legacy act squashed onto trunk with `git merge --squash` (no MERGE_HEAD) is refused, so the landing route is covered.
- A non-canonical path (`./docs/...`, `acts.toml` itself) is refused as foreign. An unescaped-backslash path is refused whole as unparseable.
- Off git, the commit-bound rule returns [].
- In a `--no-ff --no-commit` merge the other parent's legacy entry is not counted as added. A mutant that drops MERGE_HEAD reports it, so test_a_merge_counts_no_entry_its_other_parent_holds_as_added discriminates.
- The pre-change `_entry_problems` has no unknown-key refusal, so an un-resynced checkout still parses a ledger carrying `copied`.
- No active lane (docs/work/active/*) carries an act entry absent from trunk's ledger (seq/date/rows compared per branch), so landing this row refuses no in-flight lane.
- Readers: acceptance_record._added_acts, gen_open_items._ledger_entries and risk_acceptance_act pass `copied` through or ignore it. test_accepted_risk.py (TC-234's evidence) passes.

Done-when coverage:
- (a) The writer, for each act shape through `intake.py snapshot`: COVERED by test_an_approval_act_records_the_registry_it_copied, test_a_reattesting_act_records_the_registry_it_copied, test_a_traced_reanchor_naming_no_row_records_its_registry, test_a_mixed_approves_and_reattests_act_records_both_registries and test_a_reseed_records_every_registry_it_copied, plus the needs-carrier test.
- (b) The validators, both sides: COVERED by the `_COPIED_DEFECTS` parametrization (order rule, shape), test_a_commit_adding_an_entry_without_copied_is_refused, test_a_commit_adding_an_entry_naming_a_foreign_registry_is_refused, test_legacy_entries_a_commit_does_not_add_are_never_refused, test_a_legacy_entry_parses_unchanged_and_names_no_copy_set and the merge test. Each would fail on a plausible wrong implementation: ids-reconstruction fails the re-anchor test, judging every entry fails the legacy test, ignoring MERGE_HEAD fails the merge test.
- (c) IF-220 states the v2 shape. Its consumers list matches my grep: acceptance_record, gen_open_items, kitlib/sitting, trace. record_observation and assumption_rules read only the derived risk_acceptance_view.
- (d) The RESYNC entry is present and says no existing entry is edited.
- (e) The strict lints on the landing tip are owed at landing. At this tip check_trajectory --strict is clean and trace.py --strict-integrity exits 0.

Relationship decisions:
- IF-220 changed (v1 to v2). Counterparts:
  - TC-234 is RETAINED: its claim rests on seq/approved/reattested, which are unchanged, and its suite passes.
  - TC-400 CARRIES the change.
  - LLR-239 is RETAINED: risk_acceptance_act never reads `copied`.
  - LLR-278 is RETAINED: `_added_acts`/reattested_between read `reattested` only, and test_readers_carry_copied_without_loss shows the field preserved.
  - SR-178 is unchanged and its acceptance is preserved.
- LLR-271's code_symbol changed. Its counterpart, LLR-271's own detail, is NOT justified as retained: see the MAJOR finding below.
- No Status flipped. TC-400 is Drafted. The TC-400 sweep against TC-234 and the existing IF-220 rows found no contradiction or overlap.

Commands:
- `git rev-parse HEAD` -> 55a7befe0a3fd0a9ae266498140d26228b3f6ecd
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r1-967-B/wi-967 tests/test_baseline_snapshot.py tests/test_acceptance_record.py tests/test_snapshot_readers.py` -> `215 passed in 363.99s (0:06:03)` (posix-shell gate unsatisfied, 0 skips)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (984 work item(s), 869 done (88%), 34 cancelled, graph acyclic).` exit 0
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=138 LLR=326 TC=354 orphans=0 integrity=0 ... drafts=1 ...` exit 0
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r1-967-B/wi-967b tests/test_accepted_risk.py` -> `14 passed in 18.24s`
- `probe/probe.py`, `probe/p2.py`, `probe/p3.py` (scratch) -> the scenario results quoted above

- [MAJOR] docs/requirements/low-level-requirements.toml:2852 -> K1/K3: the five new act-ledger symbols (`_copied_problems`, `_copied_order_problems`, `_entries_added`, `added_acts_problems`, `added_acts_findings`) are appended to the code_symbol of Approved LLR-271, "The needs file's two tiers compared with their recorded copy". Its detail says nothing of a `copied` record, the commit-bound refusal or the whole-file order rule. So `Implements: SR-178, LLR-271` (project-trajectory/scripts/baseline_snapshot.py:1590, 1614, 1727, 1741, 1771) back-links each new rule to an LLR that does not state it. The plan's own reasoning is "no new LLR, IF-220 carries the domain", so the back-link targets neither its stated home nor a suitable LLR. Because code_symbol is a traced cell, the move needs no re-attestation. That is exactly the workaround PROCESS.md §5 change intake routes away from ("parent sound; LLR unsuitable -> amend LLR + verification"). In normal use, an adjudicator re-attesting LLR-271's needs-tier text is recorded as owning the commit-bound refusal's design, and WI-963's settlement, which builds on `copied`, finds no LLR detail to be judged against. -> The concrete change: state the record and its two refusals in an LLR whose detail says them, with TC-400 verifying that LLR, and back-link the new symbols there instead of LLR-271. Either draft a new SR-178 LLR, or amend the ledger LLR (LLR-239/LLR-278) through its approval authority. SR-178's acceptance, IF-220 and the enduring tests are preserved either way. -> @owner
- [MINOR] project-trajectory/scripts/baseline_snapshot.py:1722 -> §3 "Consolidate, don't duplicate": the new `_entries_added` restates the seq set difference `acceptance_record._added_acts` (project-trajectory/scripts/acceptance_record.py:1149) already computes ("an entry is added when its `seq` is not in base's ledger"). The kit now has two homes for "which act entries a commit adds", and they can drift, for example on non-dict entries, which one filters and the other cannot see. -> Give the comparison one home that both call. acceptance_record sits below baseline_snapshot in the import graph (baseline_snapshot -> check_trajectory -> acceptance_record), so a list-level helper there can serve `_entries_added`'s two callers and `_added_acts`. -> @owner
- [MINOR] project-trajectory/scripts/baseline_snapshot.py:199 -> for clarity: the contract docstring cites "(process.md §6)", a file that does not exist. The coverage bound is PROCESS.md §6 "Review threat model". -> Write `PROCESS.md §6`. -> @owner

VERDICT: CHANGES-REQUESTED findings=3
