# ADJUDICATE (first approval): WI-790, LLR-298, LLR-299, TC-313 and TC-314 at 92ece287

An independent spine adjudicator (Claude Opus) judged these four first drafts, in the lane as
the owner directed on 2026-10-03 (S11). It authored none of them. The SR, LLR and TC tiers are
released in this repository, so the approval is this session's. The judgement read SR-148's
whole chain as the kit brief composed it, the work item, OI-102, Sol's review 1, and the code at
92ece287 (see `001-ADJUDICATE-AMENDMENT-92ece28.md` for what was read and how the probes ran).

## Mutation probes on these rows

| # | Mutation | Row | Result |
|---|---|---|---|
| M1 | removing a pending item's row is no trigger (only `ruled` counts) | LLR-298 / TC-313 | **survived** (killed by Fix F3) |
| M2 | an unreadable parent read as nothing to close | LLR-298 / TC-313 | caught |
| M3 | the parent read via `rev^1`, so a shallow boundary reads as a root | LLR-298 / TC-313 | caught |
| M4 | an emptied Done-when accepted | LLR-298 / TC-313 | caught |
| M5 | the citing set read from the new tree | LLR-298 / TC-313 | caught |
| M6 | the TOML carrier only | LLR-298 / TC-313 | caught |
| M7 | the slot judges only the lane's tip | LLR-298 / TC-313 | caught |
| M8 | merge admission no longer calls the ruling-sync rung | LLR-298 / TC-313 | **survived** (killed by Fix F3) |
| M9 | the pre-commit hook drops the ruling-sync step | LLR-298 / TC-313 | **survived** (killed by Fix F3) |
| M10 | Done-when compared with path-bearing lines stripped | LLR-298 / TC-313 | caught |
| M11 | a root commit refused | LLR-298 / TC-313 | caught |
| M12 | `--ruling-sync` always exits 0 | LLR-298 / TC-313 | caught |
| P1 | the uncited finding silenced | LLR-299 / TC-314 | caught |
| P2 | the uncited finding after the no-work-items return | LLR-299 / TC-314 | caught |
| P3 | a deferred citer surfaces the item | LLR-299 / TC-314 | caught |
| P4 | the anchor-must-be-cited check dropped | LLR-299 / TC-314 | caught |
| P5 | the registry matched in its TOML spelling only | LLR-299 / TC-314 | caught |
| P6 | a cited item absent from the registry read as ruled | LLR-299 / TC-314 | **survived** (killed by Fix F4) |
| P7 | a registry SpecRef clocked by the file | LLR-299 / TC-314 | caught |
| P8 | SpecRef integrity judged on queued rows only | LLR-299 / TC-314 | **survived** (killed by Fix F4) |
| P9 | a registry SpecRef citing no item passes | LLR-299 / TC-314 | **survived** (killed by Fix F4) |

M8 ran against `tests/test_ruling_sync.py` and `tests/test_integrate_admission.py` (73 passed).
Nothing in the suite reaches the rung through `_merge_refusal`. TC-313's merge case calls
`integrate._ruling_sync_refusal` directly.

## Rulings

- [RETURN] LLR-298 -> the obligation: a commit that takes an open item out of pending must, in the same diff, give every row open in its parent tree that cites the item a changed, non-empty raw Done-when section, or close or remove that row; the staged check and merge admission run one comparison; a root commit closes nothing; an unreadable parent is refused -> the chain: UPWARD, SR-148 holds work behind a human-held stop and derives it from tracked registries, and this row keeps a released row's recorded criteria in step with the ruling that releases it, the owner's mechanism in OI-102 Q3 (parentage: observation 2 of the amendment verdict). SIDEWAYS, it overlaps none of LLR-288 (readiness), LLR-299 (the state check) or the backlog-staleness warning. DOWNWARD, TC-313 pins most of it: M2 to M7 and M10 to M12 are caught. But M1, M8 and M9 survive every cited test -> not ready. The text says "from pending to ruled", while the code, A8 and the code's own comment trigger on any departure from pending, a deleted pending row included. The text therefore understates the rule a correct implementation must keep, and nothing pins that arm. It also does not say that a side that does not parse is refused, or that the staged check is the pre-commit hook's step. RETURN, Fix F1, with the tests in Fix F3.
- [RETURN] LLR-299 -> the obligation as written: a pending open item without a queued citer is an error; a queued placeholder's SpecRef must name its cited pending item; a placeholder whose items are all ruled may not keep the open-item registry as SpecRef -> the chain: UPWARD, as LLR-298. SIDEWAYS, LLR-118 renders the notice from the same projection, and LLR-288 owns the block. DOWNWARD, TC-314: P1 to P5 and P7 are caught, while P6, P8 and P9 survive -> not ready. The text and the code disagree in three places. (1) "Name its cited pending item": the code accepts an anchor naming any item the row cites, ruled or pending, and accepts a registry SpecRef with no anchor at all. (2) "A queued placeholder": the code judges every open row (draft, queued, active, deferred or blocked), as IF-054 states, and P8, which narrows it to queued rows, survives. (3) The per-item staleness clock that TC-314 verifies is stated by no LLR (`_specref_staleness` names SR-148 alone). Two clauses the code keeps are also unpinned: an absent item is not ruled (P6), and a registry SpecRef on a row citing no item is reported (P9). RETURN, Fix F2, with the tests in Fix F4.
- [RETURN] TC-313 -> the obligation: drive staged and committed ruling transitions over git repositories, covering each arm LLR-298 states -> the chain: it verifies SR-148 and LLR-298, and its evidence pins most of the clauses (above) -> not ready. "A no-verify lane commit is refused at merge admission" is verified only through `integrate._ruling_sync_refusal` called directly. So deleting the rung from the merge ladder (M8) passes, and so does deleting the step from the pre-commit hook (M9). The removal trigger (M1) is unverified. RETURN, Fix F3: three tests, `method` and `evidence`.
- [RETURN] TC-314 -> the obligation: drive the open-item and work-item registries through each clause LLR-299 states -> the chain: it verifies SR-148, LLR-299, IF-073 and IF-054 -> not ready. The method omits the anchor rule and the CSV spelling, which its evidence pins. It verifies a staleness clock its LLR does not state. And it leaves P6, P8 and P9 alive. RETURN, Fix F4: three tests, `method` and `evidence`.

OUTCOME: RETURN rows=4

## Aftermath: no flip this round

Every row is returned, so no Status moves and no snapshot is taken. After the fix round, all
sixteen rows are re-judged together with the two retirements. If every row is then settled, the
lane's single act is:

- flip LLR-298, LLR-299, TC-313 and TC-314 to `Approved`;
- `python project-trajectory/scripts/intake.py snapshot --approves "docs/requirements/low-level-requirements.toml=WI-790;docs/test/test-cases.toml=WI-790" --reattests <the twelve amended rows, as blessed>,LLR-289,TC-302`.

No system-requirements token is needed. `baseline_snapshot.copy_live` copies every registry
holding a row that `--reattests` names (`_authorised_registries`), so naming SR-225 brings that
registry into the act's scope.

## Required fixes (to be applied in this lane, then re-judged)

Each replacement is the WHOLE cell value, byte-exact, between the fences (one line, no trailing
newline). Every other cell stays byte-exact. Validated with the amendment verdict's fixes, as
described there.

### Fix F1: LLR-298 `detail`

`LLR-298` `detail` (`docs/requirements/low-level-requirements.toml`):

```
When a commit takes an open item out of pending, by ruling it or by removing its row, compare that commit's parent tree with its resulting tree. Every work row open in the parent tree whose needs cite the item must, in the same commit, close by moving under the archive, be removed, or keep a non-empty Done-when section whose raw text differs from its parent text; otherwise the commit is refused, naming the row and the item. The citing set is the parent tree's, so removing the needs token discharges nothing. The open-items registry is read through either carrier, and a side that does not parse is refused rather than read as unchanged. The pre-commit hook's ruling-sync step applies the comparison to HEAD and the staged tree, the empty tree standing as the parent of a first commit; merge admission applies it to the lane's commits one at a time, against the first parent named in the commit object, so a no-verify commit is refused, a root commit closes nothing, and a parent the repository cannot read is refused by name.
```

### Fix F2: LLR-299 `detail`, `code_symbol` and `rationale`, and one back-link

`LLR-299` `detail` (`docs/requirements/low-level-requirements.toml`):

```
Report as an error, whatever the gate and before the checker's no-work-items return, a pending open item that no queued work item cites in its needs, read from the one queue projection, open_item_queue, that also feeds the owner surface and the status snapshot; a citer that is not queued does not count. For each open work row whose SpecRef names the open-items registry under either carrier's spelling, report the row when the SpecRef carries an #OI anchor naming an item its needs do not cite, and when none of the items it cites is pending or absent from the registry, a row citing none included. Backlog staleness clocks such a SpecRef per item, each item the row cites and the item its anchor names, never by the registry file, so filing another item stales no row.
```

`LLR-299` `code_symbol` (`docs/requirements/low-level-requirements.toml`):

```
uncited_open_item_findings/open_item_specref_findings/_registry_ref/_registry_ref_findings/_specref_staleness/open_item_queue/_pending_items/_held_rows
```

`LLR-299` `rationale` (`docs/requirements/low-level-requirements.toml`):

```
A pending owner decision must remain visible beside the work it holds, while a ruled item is no longer the specification the released work implements. Clocking a registry SpecRef by the registry file would stale every placeholder whenever any decision is filed, so the clock reads the items the row cites.
```

In `project-trajectory/scripts/check_trajectory.py`, `_specref_staleness`'s docstring line
`Implements: SR-148` becomes `Implements: SR-148, LLR-299`.

### Fix F3: TC-313 `method` and `evidence`, and three tests

`TC-313` `method` (`docs/test/test-cases.toml`):

```
Drive staged and committed ruling transitions over git repositories: with a row citing two pending items, ruling one while the row's Done-when is untouched is refused, naming the row and the item, by the staged check and by the hook's ruling-sync step, while the same ruling with the raw section updated passes, including an added criterion carrying a path; deleting a pending item's row is refused the same way; removing the needs token in the ruling commit does not discharge the parent-tree citation; closing or removing the row passes, and emptying its Done-when does not; a root commit is vacuous; a shallow boundary is judged from the commit object's parent, and an unreadable named parent is refused by name; the CSV carrier is judged like the TOML one; and at merge admission the refusal ladder refuses a lane whose no-verify ruling commit leaves its citer stale, even when a later lane commit updates the row, while a lane whose ruling commit carries the update lands.
```

`TC-313` `evidence` (`docs/test/test-cases.toml`):

```
tests/test_ruling_sync.py::test_a_ruling_with_the_citing_rows_done_when_untouched_is_refused; tests/test_ruling_sync.py::test_the_same_ruling_with_the_done_when_updated_is_accepted; tests/test_ruling_sync.py::test_removing_a_pending_items_row_takes_it_out_of_pending_too; tests/test_ruling_sync.py::test_removing_the_token_in_the_ruling_commit_does_not_discharge_it; tests/test_ruling_sync.py::test_a_row_closed_in_the_ruling_commit_is_accepted; tests/test_ruling_sync.py::test_a_first_commit_has_nothing_to_close; tests/test_ruling_sync.py::test_a_no_verify_lane_commit_is_refused_at_the_merge_slot; tests/test_ruling_sync.py::test_the_merge_ladder_consults_the_ruling_sync_rung; tests/test_ruling_sync.py::test_the_pre_commit_hook_runs_the_ruling_sync_step; tests/test_ruling_sync.py::test_a_shallow_boundary_is_judged_never_read_as_a_root_commit; tests/test_ruling_sync.py::test_a_parent_the_repository_cannot_read_is_refused_by_name; tests/test_ruling_sync.py::test_the_csv_carrier_is_judged_like_the_toml_one; tests/test_ruling_sync.py::test_an_added_criterion_carrying_a_path_counts_as_an_update
```

Append these three tests to `tests/test_ruling_sync.py`. They use only that module's imports,
pass at 92ece287, and kill M1, M8 and M9 respectively. They are `ruff format` and `ruff check`
clean:

```python
def test_removing_a_pending_items_row_takes_it_out_of_pending_too(tmp_path):
    # LLR-298: the trigger is an item leaving `pending`, and deleting its
    # pending row leaves it; each citing row's Done-when is owed the update.
    root = _base(tmp_path)
    _items(root, OI_6="pending")  # OI-5's pending row removed outright
    _git(root, "add", "-A")
    (line,) = ar.staged_ruling_sync_lines(root)
    assert line.startswith("WI-001 cites OI-5, which this commit takes out of pending")


def test_the_merge_ladder_consults_the_ruling_sync_rung(tmp_path, monkeypatch):
    # TC-313: merge admission itself refuses a lane's --no-verify ruling
    # commit. The cheaper rungs ahead of this one are passed so the ladder
    # reaches it on a minimal repository; the rung is the real one.
    root = _base(tmp_path)
    _git(root, "checkout", "-q", "-b", "wi-001")
    _items(root, OI_5="ruled", OI_6="pending")
    bad = _commit(root, "rule OI-5 without the row")
    _git(root, "checkout", "-q", "main")
    monkeypatch.setattr(
        integrate, "branch_outcomes", lambda r, b: ({"WI-009": "merged"}, [])
    )
    for rung in (
        "_close_record_refusal",
        "_minted_id_refusal",
        "_approval_act_refusal",
        "_held_status_refusal",
        "_loop_trailer_refusal",
    ):
        monkeypatch.setattr(integrate, rung, lambda *a, **k: None)
    _outcomes, refusal = integrate._merge_refusal(root, "wi-001", ["WI-009"])
    assert refusal is not None and bad[:10] in refusal
    assert "WI-001 cites OI-5" in refusal


def test_the_pre_commit_hook_runs_the_ruling_sync_step(tmp_path):
    # TC-313: the staged check is in the pre-commit hook's failing set, and the
    # step the hook names refuses a staged ruling that leaves its citer stale.
    hook = (SCRIPTS.parent / "hooks" / "pre-commit").read_text(encoding="utf-8")
    line = next(
        ln for ln in hook.splitlines() if ln.startswith('"$PY"') and "--run-steps" in ln
    )
    assert "ruling-sync" in line.split("--run-steps", 1)[1].split()[0].split(",")
    root = _base(tmp_path)
    _items(root, OI_5="ruled", OI_6="pending")
    _git(root, "add", "-A")
    proc = run_py([SCRIPTS / "check.py", "--run-steps", "ruling-sync"], root)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "WI-001" in proc.stdout + proc.stderr
```

### Fix F4: TC-314 `method` and `evidence`, and three tests

`TC-314` `method` (`docs/test/test-cases.toml`):

```
Drive open-item and work-item registries in temporary repositories. An uncited pending item is an error with no work rows at all and without --strict, and a citer that is only deferred does not cite it, while a queued placeholder carrying only a title, a safety class, its needs token and a SpecRef to its item's registry record passes every check under --strict and is blocked. A registry SpecRef whose anchor names an item the row's needs do not cite is reported. A row keeping a registry SpecRef, under the TOML or the CSV spelling, is reported once none of its cited items is pending, whether the row is queued or deferred, and so is a row citing no item, while a cited item missing from the registry leaves it unreported. Cited cards, the uncited notice and the status snapshot read one projection. Backlog staleness clocks a registry SpecRef per cited item: filing an unrelated item stales no placeholder, and editing its own item does.
```

`TC-314` `evidence` (`docs/test/test-cases.toml`):

```
tests/test_open_item_readiness.py::test_an_uncited_pending_item_is_an_error_even_with_no_work_items; tests/test_open_item_readiness.py::test_a_ruled_items_row_may_not_keep_the_registry_as_its_specref; tests/test_open_item_readiness.py::test_a_placeholder_row_passes_every_check_and_is_blocked; tests/test_open_item_readiness.py::test_a_registry_specref_must_name_an_item_the_row_cites; tests/test_open_item_readiness.py::test_the_csv_carriers_registry_specref_is_judged_too; tests/test_open_item_readiness.py::test_specref_integrity_judges_every_open_row; tests/test_open_item_readiness.py::test_a_cited_item_missing_from_the_registry_is_not_ruled; tests/test_open_item_readiness.py::test_a_registry_specref_on_a_row_citing_no_item_is_reported; tests/test_open_item_queue.py::test_an_uncited_pending_item_is_a_notice_not_a_card; tests/test_open_item_queue.py::test_the_status_snapshot_lists_the_same_projection; tests/test_ruling_sync.py::test_a_registry_specref_is_clocked_per_cited_item
```

Append these three tests, with their helper, to `tests/test_open_item_readiness.py`. They pass at
92ece287 and kill P8, P6 and P9 respectively:

```python
def _specref_findings(root):
    return ct.open_item_specref_findings(
        root, ct.load_wis(ct.read_registry_rows(root / ct.WI_CSV))[0]
    )


def test_specref_integrity_judges_every_open_row(tmp_path):
    # LLR-299: a deferred (or draft, active) row keeping the registry SpecRef
    # after its items are ruled is reported as a queued one is.
    _items(tmp_path, ("OI-5", "ruled"))
    _spec(tmp_path, "WI-001", where="deferred", needs=["OI-5"], specref=OI + "#OI-5")
    (finding,) = _specref_findings(tmp_path)
    assert finding.startswith("WI-001: every open item it cites (OI-5) is ruled")


def test_a_cited_item_missing_from_the_registry_is_not_ruled(tmp_path):
    # LLR-299: an item absent from the registry is not ruled (the dangling-edge
    # error reports it), so the row may keep its registry SpecRef.
    _items(tmp_path, ("OI-5", "ruled"))
    _spec(tmp_path, "WI-001", needs=["OI-5", "OI-404"], specref=OI + "#OI-5")
    assert _specref_findings(tmp_path) == []


def test_a_registry_specref_on_a_row_citing_no_item_is_reported(tmp_path):
    # LLR-299: with no item cited, none is pending, so the registry SpecRef is
    # reported, and its anchor names an item the row does not cite.
    _items(tmp_path, ("OI-5", "pending"))
    _spec(tmp_path, "WI-001", specref=OI + "#OI-5")
    findings = _specref_findings(tmp_path)
    assert any("names OI-5, which its needs do not cite" in f for f in findings)
    assert any("every open item it cites (none) is ruled" in f for f in findings)
```

