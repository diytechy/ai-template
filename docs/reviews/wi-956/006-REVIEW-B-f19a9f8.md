Reviewed: f19a9f827b42952cca9b60ce58a833cec616c3bd

Verified. The checkout is the reviewed commit (`git rev-parse HEAD` printed f19a9f827b42952cca9b60ce58a833cec616c3bd) and the lane was clean before and after every run. I looked for three failure classes first, worst first: a wrong peel that destroys work, a fail-open record, and silent wrong content.

Peel and merge slot:
- `kitlib/verdict.py` `refresh_attestation` now needs the refresh subject, then `bar_attestation`, then a bar in `LANDING_BARS`.
- `work_tip`, `_peel_target` and `governing_rev` still reach it only through `refresh_attestation`. So a `review` attestation is never peeled, even on a refresh subject (`test_work_tip_never_peels_a_review_attestation` and `test_governing_rev_never_peels_a_review_attestation`).
- `_merge_ready` refuses a tip that carries only a review attestation, and its refusal names both bars.

Verifier: `bar_attestation` accepts exactly one column-0 label line and binds `tree=` and `work=` to the commit's own tree and first parent. A quoted or indented copy and a duplicate line are refused, which keeps squash bodies (indented) inert.

Producer:
- `_attest_commit` stages, runs the bar, sheds residue and runs `write-tree`, then commits and re-verifies.
- A hook-refused commit restores the index. A hook-rewritten tree is undone with `reset --soft` plus `read-tree`.
- The refresh's harder undo (`reset --hard work_tip`) is unchanged.

Attest route:
- `attest` refuses missing hooks, the primary's branch, a dirty worktree (`--untracked-files=all`, rename source skipped), an undeclared or empty `[bars] review` (read from the lane's staged checkout), and a message carrying the label. All of these come before any bar runs.

Red-before evidence:
- I extracted be80354d9 with f19a9f8's `tests/` overlaid. 44 of the new cases fail there.
- The 2 that pass are `test_a_verified_refresh_still_peels_under_the_new_grammar[landing|no-bar]`. They are self-declared characterization tests. They cannot fail before the change, because the old regex matched the new line as summary text.

Done-when map:
- Grammar: test_bar_attestation.py verifier cases.
- Peel: the two never-peels tests, the still-peels test, and `test_merge_ready_refuses_a_tip_carrying_only_a_review_attestation`.
- Producer: test_integrate_attest.py staged, empty, red-bar/red-named-test, dirty, missing-key and hook cases.
- Refresh: `test_the_refresh_trailer_names_the_landing_bar`, `test_the_adjudication_refresh_names_no_bar`, `test_the_refresh_commits_through_the_shared_producer`, and the station suite green with fixtures moved.
- Digest: the any-order and differs cases.
- Landing-tip lints: `check_trajectory --strict` clean and `trace.py --strict-integrity` exit 0, below.
- LLR-207: judged at the sitting, not here. Its Approved status is kept with amended text pending that authority.
- RESYNC: anchored `[since be80354d9]`, the current trunk.

Two Deliverable-5 gaps (IF-173) are named below. The RESYNC entry and the worker brief sentence are present.

Commands:
- `git rev-parse HEAD` -> f19a9f827b42952cca9b60ce58a833cec616c3bd
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-20c-leg05/r956-2/B/wi-956 tests/test_bar_attestation.py tests/test_integrate_attest.py tests/test_integrate_station.py tests/test_integrate.py tests/test_verdict_record.py tests/test_hooks_on_routes.py tests/test_hooks_on_census.py tests/test_kitlib_station.py` -> `294 passed in 649.02s (0:10:49)`
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (955 work item(s), 842 done (88%), 30 cancelled, graph acyclic).` exit 0
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=132 LLR=307 TC=326 orphans=0 integrity=0 ... interfaces=246 interface-findings=0 ...` exit 0
- Red-before run on base be80354d9 with f19a9f8's tests: `pytest tests/test_bar_attestation.py tests/test_integrate_attest.py -k "not cli"` -> `44 failed, 2 passed` (the 2 are the still-peels characterization cases, confirmed with `-k still_peels` -> `2 passed`)
- Probe, driving the real `integ.attest` on the `attest_repo` fixture from a copy of f19a9f8. The message file was `WI-401: the build round\n\nBody.\n\nWI: WI-401\n`. Result: the commit verifies, but `git log -1 --format=%(trailers:key=WI,valueonly)` prints an empty string -> `AssertionError: WI trailer lost from the trailer block`.

Counterpart decisions:
- integrate.py's CLI and call surface (the changed side) gained `attest`. Its counterparts IF-154, IF-080 and IF-173 must carry the change, and the spec names IF-173 explicitly.
- docs/stack.ini (the changed side) gained `[bars]`. Its counterpart IF-022's section list must carry it.
- kitlib/verdict.py gained the grammar, verifier and digest. IF-175's summary-level data cell ("scope, phase, filing and trailer readers") may be retained: it already covers a trailer reader, and the plan's wording is an option, not a need.
- LLR-207's amendment is left to the sitting, as the spec orders. The finding below is advice to that sitting.

- [MAJOR] project-trajectory/scripts/integrate.py:2874 -> `_attest_commit` appends the `Bar-Green:` line to the message as a new paragraph (`message + "\n\n" + line`). When `attest --message-file` carries the repo's own trailer block (`WI: WI-NNN`, `Blocked-WI:`, `Co-Authored-By:`), that block is no longer git's last paragraph. `%(trailers:key=WI)` then reads nothing (probe above). `agent_common.train_evidence`, "the worker's one result channel", and check_trajectory's completion read would see a built WI as unbuilt, which is the stall/partial-close path the worker brief warns can revert work. Anchor K1, B1 (confirmed by running). -> Append the line the way `kitlib/provenance.with_loop_trailer` already does: extend an existing trailer block with "\n", else open one with "\n\n". Do it through one shared helper in provenance rather than a second joiner, and add an attest test whose message file ends in a `WI:` trailer and asserts `%(trailers:key=WI)` still reads it. -> @owner
- [MAJOR] docs/requirements/interfaces.toml:1138 -> Spec Deliverable 5 ("IF-173's data cell gains `attest`") was not delivered: the lane changes no interface row. The CLI rows enumerating integrate.py's verbs, IF-154 (line 1118) and IF-080 (line 1107), still list only claim/refresh/integrate/done-when-hold/audit, though the module header's Contract IF-154 paragraph now documents `attest`. IF-022's section list (line 497, "sections: paths, product, tiers, ...") omits the new `[bars]` section, which docs/stack.ini:1314 cites as IF-022. The registry text is now false about the shipped surface. Anchor K1. -> Add `attest` to the IF-173 and IF-154 data cells (IF-154 with `--branch --bar review --tests --message-file`) and to IF-080's verb list, and add `bars` to IF-022's sections. -> @owner
- [MINOR] project-trajectory/scripts/integrate.py:2965 -> `_run_review_bar` takes `harness_python(root)` but never asks `agent_common.harness_floor_failures`, which `_declared_bar_or_refusal` runs before every refresh bar (WI-286/WI-361). In a repo that declares the pinned toolchain but lacks its .venv, `attest` runs the bar on ambient Python and can record a `review` green that the refresh would refuse to run. This is rare, since dev-setup creates the venv. Anchor B1 (read). -> Run the same floor refusal in `_attest_preflight`, through one shared floor rung with `_declared_bar_or_refusal` rather than a copy. The check cannot be made unrepresentable here: the floor is an environment fact read at run time, at the producer's boundary. -> @owner
- [MINOR] project-trajectory/scripts/integrate.py:2967 -> The PATH prefix re-implements in intent run_menu.py's `_interpreter_dir`, the rule its own docstring cites ("the rule `run_menu` states for `[run]` lines"). It drops run_menu's POSIX half: there the interpreter's directory may hold a different `python` or none, so run_menu writes shims. With no venv on POSIX, the bare `python` in this repo's `[bars] review` line resolves to some other interpreter (it fails closed in practice). PROCESS.md §3, consolidate, don't duplicate. -> Call run_menu's interpreter-directory helper (or move it to a kitlib home both import) instead of `os.path.dirname(py)`. -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:2185 -> LLR-207's amended `code_symbol` now claims `attest`, `_attest_preflight`, `_review_bar_command`, `_run_review_bar` and `_unstaged_dirt`, and each carries `Implements: LLR-207`. But its detail states none of their contract: the `[bars] review` declaration with no default or fallback (D-002), the dirty-worktree refusal, the named tests under the lane's own basetemp, and the refusal of a message carrying the label. Its title is still "The verdict record". The spec tells the sitting to draft a derived SR if the amendment does not carry the review-bar record. Anchors K1, K3. -> At the sitting, either extend LLR-207's detail with attest's refusal contract or draft the derived SR/LLR the spec anticipates and move those symbols under it. -> @owner
- [MINOR] tests/test_hooks_on_census.py:146 -> `NOT_BUILT = set()` and `_route_params`, the strict-xfail scaffolding for "routes listed before their code lands" (reason hard-coded to "WI-956: integrate.py attest is not built"), stay in the shipped test after the code commit emptied the set. It is dead machinery that the next reader must reason about. Anchor B1 (read). -> Delete `NOT_BUILT` and `_route_params`, and restore `@pytest.mark.parametrize("route", ROUTES, ids=_route_id)` on both tests. -> @owner
- [MINOR] docs/stack.ini:1315 -> `[bars] review` repeats the `[run] smoke` shell line verbatim (line 1301). This is two homes for one command in one file, and nothing pins them equal, so an edit to the smoke bar silently leaves the review bar on the old one. -> Declare it as `review = python project-trajectory/scripts/run_menu.py smoke` (one home, the run menu's own interpreter rule), or pin the two equal in a test. -> @owner
- [MINOR] docs/test/test-cases.toml:1304 -> For clarity: TC-132's amended method says attest "refuses before that bar for a dirty worktree, an unavailable declaration, a message carrying the label, or a hook refusal". A commit refused by a hook happens after the bar, and `test_a_hook_refused_attest_commit_leaves_branch_and_index` asserts the bar ran. Only the hooks-off refusal comes before it. Anchor K1. -> Split the clause: "refuses before that bar when the hooks are off, the worktree is dirty, the declaration is unavailable or the message carries the label; a commit a hook refuses or rewrites is undone after it". -> @owner

VERDICT: CHANGES-REQUESTED findings=8
