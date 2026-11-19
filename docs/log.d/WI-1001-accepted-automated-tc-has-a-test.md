## 2026-11-19 — WI-1001: an accepted automated test case that no test declares is a strict finding

Deferred open items: none.

Built on the maintenance branch `maint/wi-1001`, cut from `refactor_again` at
`b696b6c36`, outside the lane workflow at the operator's direction: no claim,
no lane review rounds, commit hooks on. The parent session reviews and merges.

- **The rule.** `trajectory_arch._undeclared_case_findings`, called once from
  `tc_tag_findings`, reads `<TC>: no test declares it` for an `Accepted` or
  `Founded` case whose `automated` cell reads `Yes` and that no tag names,
  whatever its `evidence` cell holds. It takes the WI-997 finding's gating
  unchanged: WARN plain, ERROR under `--strict`. A `Drafted` case, a case not
  automated, a `-000` row and a case with a part in an unreadable file read
  nothing.
- **Measured at the base.** 380 live test cases, 374 accepted and automated;
  the rule named one, TC-035, the Analysis case reading the CI matrix result.
  TC-165 and TC-166 were already declared (WI-1000, WI-999). TC-035's
  `automated` cell moved to `No` (traced), so the repository lands at 0 tag
  findings with no exception. Its two new warn-only advisories (no `inputs`,
  no `max_age`) are accepted cells and are left to the operator.
- **Rows.** TC-428 (the ruling's table) and TC-429 (the sequence), both
  `Drafted`, verify SR-157 and IF-263. No LLR states the rule; amending
  LLR-366 or minting one is the operator's call. IF-263's `data` names the
  finding.
- **Text.** `PROCESS.md` §3, the registry reference's tag paragraph,
  `check_trajectory.py`'s docstring, `trace.py`'s `Automated=Yes` message, and
  a forced-migration RESYNC entry anchored at `b696b6c36`.
- **Sizes.** `trajectory_arch.py` 1132 -> 1145 SLOC, pin re-stamped.
  `PROCESS.md` 100,773 -> 100,990 bytes (+217, after the review fixes),
  re-stamped in `byte-budget-guard`; its row had read 100,417 since
  2026-11-07, so +356 bytes had landed unflagged before this change.
- **Review fixes.** The prose review found two: `PROCESS.md` §3 said
  "accepted" where the rule holds `Accepted` and `Founded`, and the RESYNC
  entry's adopter-merged files named only the `automated = "No"` remedy. Both
  now name each.
