## 2026-09-06 — Continue the redesign through independently justified repairs

Owner-authorized supervised work on `contract_split`, from `83f2c7aa`, using
Sol, Terra and Luna and intermediate Claude CLI reviews requested as Opus 5,
high. The [execution record](../ai-template-redesign-2026-09-05-codex/EXECUTION-RECORD.md)
links the individual evidence and dispositions. No unattended claim, pause
deletion, queue close, policy change, artifact approval or snapshot write is
part of this sitting. No push is authorized.

Delivered scope: declared obligation/scenario and populated Node-adopter
evidence; parent-need hat selection through the existing readers; parsed
multiline dependency mutation in the existing intake writer; text status
without renderer imports; the missing scaffold prompt-catalog generator;
project-specific adopter revalidation; prose objective anchors; and ordinary
LLR replacement through the existing change-intake route. The continuation
also authors the reviewed decomposition amendments without granting approval.

The first unfiltered run found a worker-composer size violation and stale
generated stage fingerprint: `2 failed, 3583 passed, 20 skipped in 734.28s`.
The composer now delegates its commit-range calculation without growing its
module; regenerating stage preserves DevStg-Tests. The stage regression then
passed (`1 passed in 0.02s`). No test exemption or ceiling increase fixed these
failures. <!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=83f2c7aa+continuation-first-freeze; out/run-logs/redesign-continuation-full.txt -->

Focused correction checks passed `113 passed, 56 deselected in 16.23s`, covering
the full intake and worker-policy modules plus capped-document checks.
The live parent-tag hat suite passed `73 passed in 0.22s`.
<!-- fig: cmd=".venv/bin/python -m pytest -q tests/test_intake.py tests/test_agent_loop_policy.py tests/test_bootstrap.py -k 'not test_bootstrap or byte_caps or size_budget or capped_doc_baselines'" rev=83f2c7aa+review-corrections; out/run-logs/redesign-review-corrections.txt; hats from redesign-live-tags-hats.txt -->

The parsed-source repair accepts a deliberately reviewed module-size update,
intake 1397→1453 SLOC; bootstrap 1661→1663 ships and invokes the existing catalog
generator. Agent-loop remains 2678 SLOC and its composer remains below the
unchanged limit. The deletion/operating-burden ledger is in the execution
record. These are bounded repair decisions, not census-driven ratchet resets.
<!-- fig: cmd="check_complexity.module_sloc on intake.py, bootstrap.py and agent_loop.py" rev=83f2c7aa+continuation -->

The final unfiltered run passed: `3586 passed, 20 skipped in 734.63s`. It covers
the final product Python. Subsequent wording/manual-Inspection corrections
passed their focused checks (`155 passed, 1 skipped, 56 deselected in 2.96s`)
and the regenerated stage's currency check (`1 passed in 0.02s`). The initial
red full run is retained. <!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=83f2c7aa+continuation-final-Python; out/run-logs/redesign-continuation-full-final.txt; focused command: .venv/bin/python -m pytest -q tests/test_hats.py tests/test_prompts.py tests/test_dogfood_sync.py tests/test_derive_stage.py::test_this_repo_s_committed_stage_is_current tests/test_module_size_ratchet.py tests/test_complexity_ratchet.py tests/test_bootstrap.py -k 'not test_bootstrap or byte_caps or size_budget or capped_doc_baselines'; redesign-final-wording-checks.txt -->

Smoke initially passed its tests in `84.35s`, over the nominal budget. The
enforcing command reran the same tier and passed: `1670 passed, 4 skipped in
56.14s`; enforced wall `56.4s vs 60s budget -> within`, exit 0. The budget and
tier membership remain unchanged. <!-- fig: cmd=".venv/bin/python scripts/check_smoke_budget.py --mode enforce" rev=83f2c7aa+continuation; out/run-logs/redesign-continuation-smoke-budget.txt; initial run redesign-continuation-smoke.txt -->

Strict trace integrity/schema and trajectory checks pass; no broken document
links; Ruff check and formatting pass. The SR-184 Critique-wording/Inspection
advisory is consciously retained: the method inspects record provenance,
while Critique judges artifact quality. The new manual results remain pending.

Byte deltas: PROCESS `88365→88990` (+625, ordinary design-replacement intake);
canonical byte-budget skill `4781→4632` (−149, row restamp and tighter prose).
AGENTS.template `9980`, CLAUDE `7975`, PROCESS_OPTIONS `187932` have zero delta.
All skill copies match; no cap changed. <!-- fig: cmd="wc -c project-trajectory/PROCESS.md project-trajectory/skills/byte-budget-guard/SKILL.md project-trajectory/AGENTS.template.md CLAUDE.md project-trajectory/PROCESS_OPTIONS.md" rev=83f2c7aa+continuation-final-wording -->

The [code dispositions](../reviews/2026-09-06-redesign-code-dispositions.md),
[dependency dispositions](../reviews/2026-09-06-redesign-p2a-dispositions.md) and
[authoring dispositions](../reviews/2026-09-06-redesign-authoring-dispositions.md)
retain the adversarial findings and corrections, including unusable provider
responses that were not accepted as verdicts. Review invocations use existing
bounded session logs, with requested model/effort and raw reported usage;
unavailable or ambiguous counters are not zero or additive spend.

The final Opus authoring resolution returned APPROVE after a structured retry;
the preceding preamble-only response is retained as unusable, not a verdict.
Regenerated the iteration index, stage, status, dashboard, open items, derived
component view and approval brief. The actual-data generation/freshness command
reported “already up to date” at `real 5.64s`; no stale-output waiver or
approval is implied. <!-- fig: cmd="/usr/bin/time -lp .venv/bin/python project-trajectory/scripts/gen_trajectory.py --root ." rev=83f2c7aa+continuation-final; out/run-logs/redesign-actual-generation.txt -->

Deferred open items: none minted by this sitting. Existing OI-82 remains
pending. The control-window decision and need-tier acceptance/re-attestation
remain owner work; replacement and narrower test cadence are not enabled by
drafting their prerequisites. The scoped partial progress on the queued
residual sweep does not close its remaining obligations.
