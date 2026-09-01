# WI-543 — REVIEW-A rollup

Compiled by the supervising session (2026-09-01) from the round files under
`docs/reviews/wi-543-sr163-verification-tc/`, time-ordered, governing line
last — the loop does not write this file yet (OI-76, WI-558). Sessions 010
and 011 ended REVIEW-A ERROR (provider failures; no round file); round 3 ran
with heterogeneity **relaxed and recorded** (independent Opus fallback,
`012-REVIEW-A-7b49d30-relaxed.md`, scoreboard alongside).

### REVIEW-A — Round 1 — session 005 — tip 47579c8

- [MAJOR] project-trajectory/scripts/gen_arch_map.py:2049 -> `mapping_purpose_findings` and `mapping_purpose_report` are only defined here and exercised by `tests/test_mapping_purpose.py`; no delivered CLI, bootstrap flow, or `check.py` step calls them, so adding an unmapped/unresolved/missing/stale inventory entry in a real repository produces no SR-163 report or gate result -> wire the checker to a delivered command/harness path that loads the declared inventory, spine, and exclusions, and add an end-to-end regression test that drives that path -> @owner

VERDICT: CHANGES-REQUESTED findings=1

### REVIEW-A — Round 2 — session 007 — tip 35c7146

- [MAJOR] project-trajectory/scripts/gen_arch_map.py:2176 -> SR-163 AcceptanceCriteria requires a shipped file absent from the declared inventory to be reported, but `mapping_purpose_over_repo` supplies `mapping_purpose_findings` only `bootstrap.mapping_entries()` and the checker only iterates those entries; it never enumerates the delivered package and compares it to the inventory/exclusions. Driven against the actual shared path by removing the real `docs/process.toml` row from `bootstrap.MAPPING` in memory: `mapping_purpose_over_repo('.')` returned no finding for that still-shipped destination and `mapping_purpose_report(...)[1]` remained `True`, so an omitted shipped file silently passes; the new CLI and tests exercise only declared rows and cannot catch it -> make the delivered path enumerate every shipped source/destination (including generator-derived outputs), diff that universe against MAPPING plus declared exclusions, report the omitted file under the declared policy, and add an end-to-end regression that fails when a real shipped row is removed from MAPPING -> @owner

VERDICT: CHANGES-REQUESTED findings=1

### REVIEW-A — Round 3 — session 012 — tip 7b49d30 — heterogeneity RELAXED (recorded)

Scope: `git diff contract_split...HEAD` for WI-543 (SR-163's owner) — the tolerant
MAPPING reference cell, the four-class purpose checker, the independent
delivery-universe census (REVIEW-A round-2 rework), the `--mapping-purpose` CLI,
and TC-204. Build commit (TC-204 registered Drafted, not a gate approval), so no
`--approve` hierarchy was in scope.

Driven (not just read): the round-2 fail-open closed — a planted stray physical
source gated (exit 1, gate-class `missing_file`) via the
`bootstrap.delivery_inventory()` physical walk, and the regression
`test_cli_mapping_purpose_gates_when_real_shipped_row_is_removed` bites the
pre-fix behavior; real inventory green (`--mapping-purpose --root .` exit 0,
gate classes 0); full scaffold copy pass exit 0; census matches what ships
(212 sources, 0 unclassified); Check `RESULT: PASS`, trace `integrity=0`,
smoke 21.2 s vs 60 s within, 1452 collected ≤ 1458 budget; every filled SR
Approved and resolving to a live SN; TC-204 covers every SR-163 AC class.
(Full account: `012-REVIEW-A-7b49d30-relaxed.md`.)

- [MINOR] docs/stack.ini:663 -> the re-stamp rationale states "Measured 1450 collected" and "17 tests" for tests/test_mapping_purpose.py, but the module has 19 smoke tests and smoke now collects 1452 — stale prose from an earlier round (both off by exactly the 2 tests round-2 added); the enforced `max-tests = 1458` is correct and passes with headroom, so this is comment accuracy only -> update the two counts to 1452 / 19 -> @owner

VERDICT: APPROVE findings=1
