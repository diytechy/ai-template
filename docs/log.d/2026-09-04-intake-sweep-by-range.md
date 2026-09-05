## 2026-09-04 — `intake.py sweep` by range: the recovery door that could not be opened

`sweep` is the documented recovery path for a landed merge whose intake did not
run — `intake_after_merge`'s own refusal banner names it. It could not be used.
The subcommand built its outcomes map by walking the three terminal work folders
(`partial/`, `cancelled/`, `complete/`, unioned with their `docs/archive/work/`
siblings) and passed that map alongside whatever `--before/--after` it was given,
so on this repo a two-commit range arrived carrying every close in the project's
history. Today's supervising session worked around it by calling
`intake.intake_after_merge(root, "104ecb3b", "d6e52407", outcomes=None,
branch="supervisor-oob-…")` from a Python snippet — which minted WI-593/594
correctly, and is exactly the thing a CLI exists to stop people doing.

**The shape now.** A range (`--before` or `--after` given) runs triggers (a)/(a2)
over that range and nothing else — the same call the merge slot makes, minus the
outcomes map no out-of-band range has. `--with-terminal` asks the scan back;
`--branch <label>` names the mint subject, defaulting to `sweep <before>..<after>`.
A bare `sweep` is untouched: `HEAD..HEAD` plus the scan. The ending prints a count
(the mint already announces each row it writes) or `nothing to mint.`, exit 0;
a refusal prints and exits 1.

`None` rather than `{}` is the range shape's outcomes value, and the distinction
is load-bearing: `{}` would read as "this sweep looked at the closes and found
none", which is the claim that would have to be true for triggers (b)/(d) to be
honestly skipped. `None` says the sweep judged no close at all.

**Five tests** in `tests/test_intake.py`, over one fixture (`sweep_repo`) that
carries both populations — an in-range amendment of an approved SR, and a
handed-back spec parked in `partial/` with its close report, committed *after*
the range so the two can be told apart:
`test_a_range_sweep_mints_the_range_and_touches_no_terminal_folder`,
`test_a_range_sweep_run_twice_mints_nothing_the_second_time` (the exact-title
dedup, which is what makes both shapes re-runnable),
`test_with_terminal_asks_the_terminal_scan_back`,
`test_a_custom_branch_label_names_the_mint_subject`, and
`test_a_bare_sweep_still_walks_the_terminal_folders`. Four of the five were
driven RED against the old arm before the fix (the fifth is the unchanged bare
sweep, and it stayed green — which is the point of keeping it).

**Reviewed baseline bump: `intake.py` 1357 → 1363 SLOC.** Six lines: the
`ranged` predicate, the `outcomes = None` / conditional-scan pair, the branch
label default, and the two argparse rows. Two flags on one subcommand cannot be
fewer than two argparse rows, and a sibling module for one CLI arm would put the
mint's own door in another file. The overage was compacted first, not absorbed:
the terminal walk became a dict comprehension (−3 against the naive shape) and
the per-row minted listing was dropped rather than duplicate the line `_mint`
already prints.

**Measured on the commit bar:** smoke tier 1528 passed / 8 skipped in 139 s,
`tests/test_intake.py` 57 passed, `check_complexity --mode enforce` OK (199 rows
over 15, unchanged — no bump), `check_docs --stale` OK (1356 docs, 0 broken).
The smoke **budget** step reads 141 s against its 60 s ceiling — environmental,
this box was running several sessions at once, and nothing is re-stamped for it.
`ruff format --check` reds two files under `docs/reviews/2026-08-29-oi67-slice*/`
which are pre-existing (confirmed by re-running the check on the untouched tree)
and out of this change's scope.

Deferred open items: none — the CLI arm is the whole of the fix, the
`intake_after_merge` seam it calls is unchanged, and the operating note that
called `sweep` structurally unusable (handoff 2026-09-03 §4) is discharged by
this commit rather than carried forward.
