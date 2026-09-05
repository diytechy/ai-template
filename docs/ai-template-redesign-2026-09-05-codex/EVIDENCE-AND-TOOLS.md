# Evidence, measurements, and reuse options

**Observation date:** 2026-09-05. **Source checkout:** `/Users/diytechy/Documents/ai-template`. **Revision:** `a9bf6cee29fd0492d136457615598e8e96e5dada`.

This was a read-only design investigation of the repository, with new documents written in the adjacent `ai-template-redesign-2026-09-05-codex` directory. Three Luna agents reviewed runtime architecture, requirements/tests, and external tooling; the runtime agent also critiqued the proposed integration design. Findings were synthesized and selected code was checked by the primary agent. No paid-agent workload benchmark, full suite run, or implementation experiment was performed.

The working tree initially showed an owner-only scratchpad modification. Its contents were not read or used. The existing separate Claude review directory was not read; this package is an independent review.

## Follow-up adversarial review

On 2026-09-05, Claude Fable 5 reviewed the original proposal at high effort through the CLI against repository revision `0d6f3398`. [Its findings and the applied dispositions](FABLE-REVIEW-DISPOSITIONS.md) record the route, limits, and corrections. The census and initial source map below remain the original `a9bf6cee` observations; they were not remeasured or silently updated to the later revision. The follow-up changes implementation sequencing, current-policy authority, human-hold handling, semantic invalidation, and the criteria for judging the integration experiment.

## Owner follow-up: design replacement and rendering isolation

The owner subsequently fixed this plan's permanent location inside `docs/ai-template-redesign-2026-09-05-codex/` and raised LLR design lock-in and HTML test cost. [The follow-up proposal](LLR-AND-RENDERING.md) addresses both. Source inspection at `cb7f5ccebdd77b868158e85199c0cd488e1141ad` found:

- The Spine Authoring skill permits amendments to approved text and treats LLRs as solution-specific; PROCESS's change-intake diagram around lines 860–888 nevertheless routes every violated existing SR/LLR to a coverage gap, without asking whether the design should be replaced.
- `gen_trajectory.py` imports/re-exports rendering, parsing, and text status; `check.py` and `trunk_step.py` invoke the same facade for HTML and `--status`. A physical file split alone does not isolate core dependencies.
- `tests/conftest.py` already keeps several renderer/trajectory modules outside smoke, while `.github/workflows/test.yml` runs the complete suite. The exact renderer cost and safe test membership were not measured here and remain P0/P9R work.

The source links below were repaired for the in-repository location. Fable's raw review and JSON metadata remain historical and unchanged: their hashes identify the revision after that review, not these later owner-requested additions. No new independent review or implementation-test result is claimed.

## Reproducible census

| Surface | Observation | Interpretation |
|---|---:|---|
| Shipped Python under `project-trajectory/scripts` | 82 files; 76,337 physical lines | Includes comments/docstrings and all shipped Python, not only orchestration |
| Python under `tests` | 155 files; 87,679 physical lines | Includes fixtures/helpers; not 155 test cases |
| AST functions named `test_*` under `tests` | 3,254 | Source definitions, not pytest-collected parametrized case count |
| Stakeholder needs | 27 | Parsed `need` tables |
| System requirements | 76 | Parsed `requirement` tables |
| Low-level requirements | 192 | Parsed `design` tables |
| Test-case records | 191 | Parsed `test` tables; distinct from executable tests |
| PROCESS.md | 88,365 bytes; 1,318 lines | Method core |
| PROCESS_OPTIONS.md | 187,932 bytes; 2,767 lines | Optional-method documentation |
| AGENTS.template.md | 9,980 bytes; 190 lines | Agent entry guide close to its declared 10,000-byte cap |

Largest shipped Python files by physical lines: `trace.py` 6,051; `check_trajectory.py` 4,940; `agent_loop.py` 4,573; `bootstrap.py` 3,310; `integrate.py` 3,001; `agent_common.py` 2,982; `intake.py` 2,746. Large files do not alone demonstrate poor design; they identify where to inspect responsibilities.

Reproduce from the source checkout using Python 3.11+ (`python` was not available on this shell's PATH; `python3` worked):

```python
from pathlib import Path
import ast
import tomllib

for folder in ('project-trajectory/scripts', 'tests'):
    files = list(Path(folder).rglob('*.py'))
    lines = sum(len(p.read_text().splitlines()) for p in files)
    tests = sum(
        isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        and n.name.startswith('test_')
        for p in files for n in ast.walk(ast.parse(p.read_text()))
    )
    print(folder, len(files), lines, tests)

for path, table in (
    ('docs/requirements/stakeholder-needs.toml', 'need'),
    ('docs/requirements/system-requirements.toml', 'requirement'),
    ('docs/requirements/low-level-requirements.toml', 'design'),
    ('docs/test/test-cases.toml', 'test'),
):
    print(path, len(tomllib.loads(Path(path).read_text())[table]))

for path in ('project-trajectory/PROCESS.md',
             'project-trajectory/PROCESS_OPTIONS.md',
             'project-trajectory/AGENTS.template.md'):
    content = Path(path).read_bytes()
    print(path, len(content), len(content.splitlines()))
```

These are filesystem measurements at the recorded checkout, not Git-history growth rates or normalized executable LOC. No line-count reduction or runtime saving is claimed for the proposed design.

## Source map and confidence

Paths below are relative to the source repo; line locations refer to the recorded revision. The linked files are next door to this package.

| Finding | Evidence | Confidence / limit |
|---|---|---|
| Maintainability, traceability, test-first and explicit gates are core vision | [README](../../README.md), lines 3–11 | Direct statement |
| Small profile and proportionality already exist as doctrine | [PROCESS](../../project-trajectory/PROCESS.md), lines 25–32 and 254–265 | Doctrine; installed minimal-profile cost still needs measurement |
| Scheduler and admission have different ordering | [schedule.py](../../project-trajectory/scripts/schedule.py), `order_key` line 548; [dispatch.py](../../project-trajectory/scripts/dispatch.py), `_judgement_first` line 368 | Direct code/docstring; intentional override, not an accidental nondeterminism claim |
| Spine work can form a multi-WI lane | [dispatch.py](../../project-trajectory/scripts/dispatch.py), `_admission` lines 389–461 | Direct code |
| Consolidation is called inside admission | [dispatch.py](../../project-trajectory/scripts/dispatch.py), `_admit` lines 1054–1130 | Direct code |
| Consolidation reuse fingerprint omits scope body | [consolidate.py](../../project-trajectory/scripts/consolidate.py), `queue_digest` line 170 | Direct field inspection; end-to-end stale-decision failure not reproduced |
| Reviewer identity is reconstructed through special commits | [kitlib/verdict.py](../../project-trajectory/scripts/kitlib/verdict.py), `mechanical_close_attestation` line 490, `work_tip` 566, `governing_rev` 601 | Direct architecture; existing protections should not simply be removed |
| Mechanical-close path still recognizes old terminal home | [kitlib/verdict.py](../../project-trajectory/scripts/kitlib/verdict.py), lines 437–441 | Direct constants; September 5 report describes writer/readers migration owed |
| Current concurrency need does not promise speedup | [stakeholder needs](../../docs/requirements/stakeholder-needs.toml), SN-027 | Direct need/rationale; default two workers and recovery obligations remain relevant |
| Plan protocol has a substantial optional session cost | [plan_round.py](../../project-trajectory/scripts/plan_round.py), opening protocol and budget comments | Eight-session happy path is documented, not measured token cost |
| Test suite has historical budget/tiers and real integration coverage | [tests/conftest.py](../../tests/conftest.py), lines 42 onward | Direct configuration; no fresh duration measurement |
| Missing routed tier, successful-close telemetry and corrupted outcome label | [September 5 investigation](../../docs/decisions-for-review-2026-09-05.md), §2 | Prior investigation's measurements, not independently re-run here |
| Stale coordinator and resumed-base questions remain owner decisions | [September 5 investigation](../../docs/decisions-for-review-2026-09-05.md), §6, OI-83/84 | Recorded open questions; proposed remedies do not constitute rulings |
| Earlier consolidation plan deliberately retained batching | [September 2 plan](../../docs/plans/2026-09-02-backlog-restructure-and-consolidation.md), §1.7 | Explains why consolidation alone did not simplify assignment |
| Dependency exceptions are permitted with an argument | [Dependency ledger](../../docs/dependencies.md) | Direct governing policy; differs from shorthand “stdlib-only” in some docs |

**Documentation drift example:** root README's configuration table describes `human_approval_through = DevStg-Release` for this repo, while the actual [process policy](../../docs/process.toml) says `DevStg-Needs`. The README also presents an older stage description while the generated status reads DevStg-Tests. These are illustrations of duplicated current-state prose, not reasons to change the authoritative dials. A redesign should remove copied values from prose and render them from the actual policy/state.

## External tools

Official documentation was consulted during this investigation. Recommendations below are architectural judgments; no installation, compatibility trial, pricing study, or benchmark was performed. Do not infer that a tool replaces all semantics merely because its category matches.

| Tool | Decision | Concrete substitution and retained responsibility |
|---|---|---|
| Python `graphlib.TopologicalSorter` | Evaluate for core use | Supplies dependency ordering/cycle detection and ready-node mechanics. WI priority, human holds, cancelled/partial semantics, reconciliation, and lane/exclusivity remain domain policy. It may not save much if the final scheduler is already a short dependency scan. Use APIs available at the 3.11 floor. [Python 3.11 docs](https://docs.python.org/3.11/library/graphlib.html) |
| Git worktrees and commit/tree objects | Keep, narrow wrappers | Worktree add/list/remove/repair are already provided by Git. Preserve only claim ownership, safe cleanup, candidate/ref lifetime, and policy checks in custom code. A commit can carry metadata while naming an existing tree, supporting the proposed same-tree receipt experiment; this does not automatically run hooks or prove authorization. [Worktrees](https://git-scm.com/docs/git-worktree), [commit objects](https://git-scm.com/docs/git-commit-tree) |
| pytest parametrization and Hypothesis | Keep pytest; evaluate Hypothesis as development-only | Parameterization reduces repeated test setup; generated/shrunk inputs and stateful tests can exercise scheduler transitions and recovery sequences. Retain explanatory regression examples and real-Git tests. New test tooling has a maintenance cost and requires the appropriate project dependency review. [pytest](https://docs.pytest.org/en/stable/how-to/parametrize.html), [Hypothesis stateful testing](https://hypothesis.readthedocs.io/en/latest/stateful.html) |
| JSON Schema / `jsonschema`; Pydantic | Defer shipped dependency | A schema validator can replace repeated shape checks if deletion is substantial. JSON Schema is language-neutral; Pydantic is Python-oriented. Neither proves semantic non-overlap or authorized approval. Prefer a few typed records plus boundary parsing initially; do not write a general custom schema engine to avoid a library. [jsonschema](https://python-jsonschema.readthedocs.io/en/stable/), [Pydantic](https://docs.pydantic.dev/latest/) |
| SQLite through stdlib `sqlite3` | Defer; optional derived index only | Useful for a measured indexing bottleneck. A mutable database as the authority would complicate Git review and recovery from tracked text. The current row census alone does not justify one. [Python SQLite interface](https://docs.python.org/3/library/sqlite3.html) |
| GitHub branch protection and merge queue | Optional hosted backend | Can own protected-branch checks and queueing/testing of combined PR changes. Requires GitHub and eligible repo/plan configuration; CI must handle merge-group events. It does not own WI reconciliation or human artifact attestation, and a PR approval is not automatically semantic review of each composed merge-group tree. Preserve the stronger evidence contract where required. [Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches), [merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue) |
| `transitions` | Probably unnecessary | Supplies finite-state-machine conditions/callbacks. A small explicit enum and transition function is easier to inspect for this proposed lifecycle. Reconsider only if it replaces substantial remaining state machinery, not to rename that machinery. [Project documentation](https://github.com/pytransitions/transitions) |
| Temporal, Prefect, LangGraph | Do not adopt for this local core | Provide durable workflows, task orchestration, or persistent agent execution. They introduce additional runtime/persistence concepts; Temporal is a service-based design, while the others have different local/hosted options. They are not interchangeable and are not inherently unsuitable for all agent work, but the local Git-centered loop has not established a need for them. [Temporal](https://docs.temporal.io/), [Prefect](https://docs.prefect.io/v3/concepts/flows), [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview) |

GitHub Issues/Projects or another task service could replace a dashboard or offer convenient manual intake, but making it authoritative would trade offline Git review for synchronization and service dependencies. Do not add a second bidirectional WI registry in the first redesign. If an adopter wants a hosted UI, expose a one-way projection or explicitly choose a hosted authority profile later.

The existing September 5 report already considered `cleat` and `agent-native-cli`. Its recommendation to avoid adopting either is recorded there; this review did not independently re-evaluate their maturity or star counts. An escapes ratchet is a separate possible check, not an orchestration replacement.

## Remaining uncertainty

- Exact numbers of redundant tests and unnecessarily normative LLRs require the row-by-row P0 map. The examples here justify investigation, not wholesale removal.
- No current complete test result is claimed. The repository's full and smoke bars apply when implementation and commits begin; this external document-only investigation did not run them.
- The proposed commit-metadata receipt and serialized final review require P5 validation. Hook/CI behavior, retained rejected candidates, and Git-only recovery are explicit acceptance requirements, not solved by the diagram.
- No measured throughput or token-saving claim is made. Existing telemetry lacks some labels needed for a clean comparison.
- The approved depth-0 architecture frame and outstanding owner rulings remain constraints. A proposed module organization is not an implicit re-attestation of that frame.
- The minimum profile is a proposed packaging outcome. Every currently approved capability must be retained, made explicitly conditional through reviewed scope changes, or deliberately retired.
