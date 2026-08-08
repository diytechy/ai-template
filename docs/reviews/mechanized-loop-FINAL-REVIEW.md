# FINAL ADVERSARIAL REVIEW — mechanized-loop program (2026-08-08)

**Reviewer:** OpenAI `gpt-5.6-sol` via `codex exec`, reasoning effort **medium**,
read-only, run against the branch at commit `5a9bba21` (P0-P14 all committed).
Owner-directed: *"The final adversarial review should be run using openai over
cli, using sol on medium effort."*

**Command:**

```
codex exec --model gpt-5.6-sol -c model_reasoning_effort=medium   --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check
```

The brief gave it the three program documents, told it to prefer findings it
DROVE over findings it reasoned to, told it not to report declared-later work as
a defect, and named the three inherited host failures so it would not re-report
them. It drove every finding below.

**This review is filed UNRESOLVED.** Its verdict is not a formality and is not
softened here: the program's isolated machinery is well tested and its
operational cutover is not finished. The findings are the honest state of the
branch, and the work they name has not been done.

---

## VERDICT

Not sound enough to hand over. The isolated APIs are generally well tested, but the operational cutover is incomplete: several runtime paths bypass the new machinery or report success while required adjudication has not occurred. The largest risk is therefore a convincing green suite around components that the shipped unattended loop and fresh scaffold do not actually use.

## FINDINGS

### BLOCKER Python-less policy absence disables the default-on secrets floor

- WHERE: `project-trajectory/hooks/pre-commit:84`, `project-trajectory/hooks/commit-msg:54`, `project-trajectory/hooks/pre-push:94`, `project-trajectory/scripts/config.py:219`, `tests/test_pre_commit_hook.py:337`
- FAILURE: On a machine without Python, a repository with no `docs/config.toml` or retired privacy file exits 0 and skips all scans. But absent configuration means schema defaults, and `policy.secrets_scan` defaults to `true`. Thus an unreadable default-on security gate is treated as permission to commit/push.
- EVIDENCE: Driven with `pytest ... test_hook_still_skips_for_a_repo_that_declares_nothing -vv`; it passed. The test explicitly deletes all declarations and asserts `returncode == 0`. The hook prints “skipping process checks,” while `config.py:219-223` declares the secrets floor always on.
- FIX: With no working interpreter, block unconditionally while `secrets_scan` defaults on, or implement an equivalent pure-shell secrets floor. Do not infer “all security checks off” from absence of a config file.

### BLOCKER Queue admission is neither universal nor crash-safe

- WHERE: `project-trajectory/scripts/admit.py:1379`, `project-trajectory/scripts/admit.py:1409`, `project-trajectory/scripts/check_trajectory.py:2362`, `project-trajectory/scripts/intake.py:885`, `project-trajectory/scripts/plan_artifacts.py:175`
- FAILURE: `admit()` moves Draft→Queued before appending its first ledger event. If that append fails during the first admission, the candidate remains queued, the ledger remains absent, and the strict gate deliberately returns no finding. Separately, `intake` and `plan_artifacts` still write directly to `queued/`, contradicting “one transaction owns every move.”
- EVIDENCE: Driven by injecting `OSError("simulated crash after move")` into the real append step. Result: `draft_exists=False`, `queued_exists=True`, `ledger_exists=False`, `strict_findings=[]`. Also drove `test_the_rung_is_silent_until_the_repo_has_adopted_the_transaction`; it passes by asserting this silence.
- FIX: Establish a recoverable transaction marker/admissions ledger before moving, so any interrupted first admission is detectable. Route every producer through Draft→`admit()` and remove ledger-presence opt-in from new scaffolds.

### BLOCKER The unattended planner reports success instead of adjudicating

- WHERE: `project-trajectory/scripts/dispatch.py:775`, `project-trajectory/scripts/dispatch.py:780`, `project-trajectory/scripts/dispatch.py:798`, `project-trajectory/scripts/dispatch.py:815`
- FAILURE: A valid unadjudicated Partial outcome selects the `outcomes/adjudicate` rung, but `_planner_gate()` merely drains, changes no ledger state, and returns exit 0. Relaunching repeats the same successful no-op indefinitely. The “autonomous adjudication loop” does not execute adjudication, prose rulings, or admission.
- EVIDENCE: Driven with a valid `outcome.write_outcome(..., outcome="partial")`, then the real planner gate with drain stubbed read-only. Output: `planner rung outcomes [adjudicate]`; `rc=0`, `ledger_changed=False`, `has_disposition=False`.
- FIX: Wire each automatic upper rung to its configured routed adjudicator and enact the resulting typed decision. If required automatic adjudication cannot run, return a non-zero typed refusal rather than success.

### MAJOR Attestation’s claimed single-head append rule races

- WHERE: `project-trajectory/scripts/attest.py:676`, `project-trajectory/scripts/attest.py:696`, `project-trajectory/scripts/attest.py:701`, `project-trajectory/scripts/attest.py:721`
- FAILURE: The documented claim that two writers naming the same head “cannot both land” is false. Head validation and append are separate, unlocked operations. Concurrent writers can append two children of one parent, and `read_events()` accepts the fork.
- EVIDENCE: Driven with two threads synchronized immediately after both read the same head. Both returned success; the ledger contained two different event IDs whose `parent` was the same base ID, and reading all three records raised no error.
- FIX: Hold a cross-process lock across read/head-check/append and flush the append durably. Also make readers reject a forked or discontinuous artifact chain.

### MAJOR Id-less ledger records are accepted as actionable events

- WHERE: `project-trajectory/scripts/outcome.py:453`, `project-trajectory/scripts/outcome.py:495`, `project-trajectory/scripts/adjudicate.py:249`, `project-trajectory/scripts/resume_plan.py:596`, `tests/test_outcome.py:607`
- FAILURE: Although the normative envelope requires every event to carry a reproducible ID, the outcome/disposition readers verify IDs only when present. An id-less Partial record becomes a pending outcome with `event=None`; the planner reports no corruption and asks to adjudicate an empty ID.
- EVIDENCE: Driven with `{"kind":"outcome","wi":"WI-999","outcome":"partial"}`. `read_events` accepted it, `snapshot.findings == ()`, and the planner returned `Decision(rung='outcomes', action='adjudicate', items=('',), ...)`. The repository test explicitly asserts acceptance of an id-less record.
- FIX: Require and validate the complete envelope—`schema`, `kind`, `id`, and `ts`—in every ledger reader, followed by kind-specific schema validation. Remove the id-less fixture exception.

### MAJOR Prompt, routing, and provenance cutover did not happen

- WHERE: `project-trajectory/scripts/agent_loop.py:278`, `project-trajectory/scripts/agent_loop.py:516`, `project-trajectory/scripts/agent_loop.py:603`, `project-trajectory/scripts/agent_loop.py:795`, `project-trajectory/scripts/agent_loop.py:2491`, `project-trajectory/scripts/agent_loop.py:2705`, `tests/test_prompt_render.py:535`
- FAILURE: Live worker/reviewer/critic sessions still use embedded constants and legacy `agents.csv`/`agents-enabled` routing. `draw_for_job()` has no production caller outside its CLI, and `prompt_render.provenance()` likewise has no session/outcome/verdict caller. Session metadata records only `prompt-chars`, not the required hashes, route identity, arguments, or source-artifact hashes.
- EVIDENCE: Fresh bootstrap driven in a temporary directory: `prompt_render.py check` returned `OK, 0 declared prompt(s)`, `agent_loop.py` still contained `WORKER_PROMPT`, and the G1 harness nevertheless returned `RESULT: PASS`. `tests/test_prompt_render.py:536-538` still calls runtime cutover “a later slice,” despite P13/P14 being closed.
- FIX: Make shipped external templates and config job pools the live defaults; route every launch through `draw_for_job()` and `prompt_render.render()`, persist provenance in every required record, delete embedded/legacy fallback paths, and add as-launched integration tests against a fresh scaffold.

## WHAT IS SOUND

The isolated implementations are substantial and mostly disciplined:

- The focused new-machinery suite passed: `824 passed`.
- The full suite, with exactly the three declared inherited failures deselected, passed: `2914 passed, 8 skipped`.
- The 0–3 inclusive ratification matrix, stage-to-gate mapping, meaning/clarity behavior, scope digest coverage, Partial classification, failure fingerprinting, and deterministic planner precedence are well exercised in isolation.
- Declared malformed configuration and below-floor interpreter cases fail closed when a configuration exists.
- Traceability reported zero orphans, integrity errors, placeholders, and schema findings.
- OKF, trajectory dashboard, derived gate, and the correctly parameterized architecture map were fresh.
- Fresh bootstrap produced the expected layout and passed its basic G1 harness; the defect is that the new adjudication/admission/prompt surfaces are dormant, not that bootstrap fails mechanically.
