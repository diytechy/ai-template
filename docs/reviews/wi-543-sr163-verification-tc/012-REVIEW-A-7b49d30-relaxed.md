# WI-543 / SR-163 — Independent review (REVIEW-A, round-3, 7b49d30)

Scope: `git diff contract_split...HEAD` for WI-543 (SR-163's owner) — the tolerant
MAPPING reference cell, the four-class purpose checker, the independent
delivery-universe census (REVIEW-A round-2 rework), the `--mapping-purpose` CLI,
and TC-204. Build commit (TC-204 registered Drafted, not a gate approval), so no
`--approve` hierarchy was in scope.

## What I drove (not just read)

- **Fail-open closed (the round-2 defect):** planted a stray physical source
  `scripts/kitlib/stray_probe.py`; the shipped `gen_arch_map.py --mapping-purpose`
  gated it (exit 1, gate-class `missing_file`). The `bootstrap.delivery_inventory()`
  physical walk — not MAPPING — is what makes an omitted source observable, so the
  regression test `test_cli_mapping_purpose_gates_when_real_shipped_row_is_removed`
  genuinely bites the pre-fix (MAPPING-defined-universe) behavior.
- **Real inventory green:** `--mapping-purpose --root .` → missing_file 0 [GATE],
  stale_entry 0 [GATE], unmapped_file 152 [WARN], unresolved_reference 0 [WARN],
  exit 0. Baseline 147 rows / 20 filled / 127 bare confirmed independently (127 +
  25 generated-bare = 152).
- **Tolerant cell safe in the real copy pass:** full `bootstrap.py --dest` scaffold
  exit 0; every triple-referenced destination (docs/process.toml, prompts/worker,
  hats.toml, check.yml, performance-budgets.csv, docs/stage, interfaces.md) copied.
- **Census matches what ships:** `materialize_agent_layer` copies only per-skill
  `SKILL.md`; `delivery_inventory()` classifies every physical source
  (`sources == classified`, 212 sources, 0 unclassified, 0 declared-but-absent).
- **Harness:** Check `RESULT: PASS`; trace `integrity=0` (LLR-197/SR-168/SR-181
  findings are pre-existing, untouched by this diff); smoke 21.2s vs 60s within,
  1452 collected ≤ 1458 budget; TC-204 modules 22 passed.
- **Requirement surface:** every filled SR (SR-049/137/146/159/147/015/161/151) is
  Approved and resolves SR→live SN, each semantically apt; TC-204 covers every
  SR-163 AC class and every WI done-when. No new/changed SN/SR rows to sweep.

## Findings

- [MINOR] docs/stack.ini:663 -> the re-stamp rationale states "Measured 1450 collected" and "17 tests" for tests/test_mapping_purpose.py, but the module has 19 smoke tests and smoke now collects 1452 — stale prose from an earlier round (both off by exactly the 2 tests round-2 added); the enforced `max-tests = 1458` is correct and passes with headroom, so this is comment accuracy only -> update the two counts to 1452 / 19 -> @owner

VERDICT: APPROVE findings=1
