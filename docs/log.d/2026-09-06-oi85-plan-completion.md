## 2026-09-06 — OI-85 continuation and independent repair close

Scope: resume the accepted redesign from `1e78ada3194c8806578cccf90a23afe2b64b9775`
on `contract_split`, review Fable's repairs, and finish independently justified
work. The owner authorized execution, Sol/Terra/Luna delegation, Claude CLI
adversarial reviews and local commits. No push or unattended launch is included.

Deferred open items: none.

The separate [owner act](2026-09-06-oi85-owner-ruling.md) records the exact three
need changes and needs-only snapshot. No other approval baseline is refreshed.
The general SN-drift detector remains separately deferred.

Fable's linked-lane base fix, interruption accounting, launcher restart bound
and Node-independent kit assertions are retained. The follow-up fixes refuse
coordinator startup when its source identity is unavailable and replace generic
nested-TOML row inference with canonical need-carrier resolution. H1 and R-E
share native path normalization, including whitespace and lexical components;
empty need registries expose an empty ID set and malformed ones refuse. Other
TOML fragments retain path-only judgment, without an invented registry schema.

P9R moves the HTML modules into `rendering/`, retains the supported facade,
shares the existing stage/count reads in memory, and separates core fixtures.
The physical-package-absence test runs the parser/status/pending tests without
`rendering/`; a mutation importing the absent package fails. The review also
restored stage-only compatibility for `_stage_facts` and shared render inputs
in the critique-staleness surface. The local selector is deliberately small:
known independent validators and unchanged registry shapes may omit the HTML
family, but keep core tests, a full-output boundary and actual output freshness.
Unknown/shared/tooling/renamed/deleted changes broaden; CI and phase-close Full
remain unchanged. No runtime framework or new dependency was added.

The module-size restamp is deliberate: `agent_loop.py` 2678→2685 for one existing
preflight boundary; `bootstrap.py` 1663→1665 for the existing delivery manifest;
`check_trajectory.py` 2336→2349 for canonical need row checks and primary/scaffold
render-input surfaces. Extracting more wrappers would not remove those owning
responsibilities. No function-complexity ceiling changed.
<!-- fig: cmd="check_complexity.module_sloc on the three named scripts" rev=1e78ada3+OI85-P9R -->

The common path regression was observed red before correction: `3 failed, 11
passed, 144 deselected in 0.87s`. After repair, runtime/hats/trajectory/selector
modules passed `197 passed in 10.80s`. Structural checks after the reviewed size
restamp passed `54 passed, 1 skipped in 3.06s`. These are focused results, not
Full-suite evidence.
<!-- fig: cmd=".venv/bin/python -m pytest -q tests/test_hats.py tests/test_trajectory.py tests/test_coordinator_code_drift.py tests/test_changed_selection.py" rev=1e78ada3+OI85; out/run-logs/oi85-runtime-selector-final.txt -->
<!-- fig: cmd=".venv/bin/python -m pytest -q tests/test_module_size_ratchet.py tests/test_complexity_ratchet.py tests/test_import_layers.py tests/test_dependency_ledger.py tests/test_dogfood_sync.py" rev=1e78ada3+OI85; out/run-logs/oi85-structure-checks-final.txt -->

Final review, Inspection, broad validation and commit results follow below when
actually observed. The [control preflight](../ai-template-redesign-2026-09-05-codex/CONTROL-PREFLIGHT.md)
records the route-complete reservation gap under the owner's Short envelope;
tracked pause deletion remains its explicit launch act. Conditional replacement
packages are not reported as implemented merely because repairs finish.

### Independent review and actual Inspection

The [dispositions](../reviews/2026-09-06-oi85-dispositions.md) link the Opus 5/high
runtime, record and P9R reviews. Record closure and selector closure both
returned APPROVE; the final selector also closes the review's generated-file
deletion observation. All invocations have separate bounded/redacted telemetry
records, including provider-reported usage and cost where present.

H2/H3/H5 guidance now uses existing process, prompts and scoped records. A
fresh, separate document inspector performed the three procedures and the
negative cases. TC-209 and TC-210 passed. TC-211's independent-purpose judgment
and planted paraphrase case are demonstrated, but its normal sample remains
INCOMPLETE because the existing SR-161 machine perspective record is absent.
[Actual results](../test/inspection-procedures.md) retain that distinction.
The Drafted SR/TC rows remain Drafted; no result is a first-approval act.

### Broad verification corrections

The first complete HTML-family run returned `2 failed, 174 passed in 146.09s`.
The failures were the SVG literal corpus still pointing at the old root
emitters and the package initializer/shared display reader missing from
component ownership. The corpus now follows the real emitters; LLR-035 names
the existing dashboard responsibility's two new source homes. Both cases passed
in `2.36s` after correction. The later full suite includes this complete family.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto over the seven HTML modules in P9R-EXECUTION.md" rev=1e78ada3+OI85-P9R; out/run-logs/oi85-html-family.txt -->
<!-- fig: cmd=".venv/bin/python -m pytest -q tests/test_traj_render.py::test_u3_svg_corner_radii_match_the_declared_scale tests/test_traj_views.py::test_meta_component_top_view_smoke" rev=1e78ada3+OI85-P9R; out/run-logs/oi85-html-repairs.txt -->

The first unfiltered run returned `4 failed, 3643 passed, 22 skipped in 746.06s`.
Two failures correctly detected the unregenerated shipped prompt catalogue;
one caught a synthetic rubric anchor using a retired-stage token; one detected
the new selector's Git-fixture integration tests entering smoke by default.
The catalogue is regenerated, the synthetic anchor uses a distinct name, and
the new selector module is classified as slow under the existing subprocess/
fixture criterion. Its `45` cases take `11.57s` alone and remain in Full/CI;
no existing test changed tier. Both smoke budgets remain unchanged (`60s`,
`1702` membership ceiling). The four failed checks then passed in `1.96s`.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto --junitxml=out/run-logs/oi85-full.xml" rev=1e78ada3+OI85-P9R; out/run-logs/oi85-full.txt -->
<!-- fig: cmd=".venv/bin/python -m pytest -q tests/test_changed_selection.py" rev=1e78ada3+OI85-selector-final; final Sol tool result; also included in the final unfiltered suite -->
<!-- fig: cmd=".venv/bin/python -m pytest -q tests/test_generated_freshness_wiring.py::test_prompt_catalog_step_reds_when_a_template_changes tests/test_routing_and_prompts.py::test_the_catalogue_on_disk_is_FRESH tests/test_stage_ladder.py::test_this_repo_is_clean_at_the_ERROR_severity tests/test_smoke_budget.py::test_smoke_tier_stays_within_its_membership_budget" rev=1e78ada3+OI85-P9R; out/run-logs/oi85-full-failure-repairs-final.txt -->

Watched/capped bytes: PROCESS_OPTIONS `187932→189535` (+1603) for the three
review-record duties and attended identity/return path; byte-budget skill
`4632→4613` (−19) after restamping; spine-authoring `30141→30591` (+450) for the
scoped stopping decision. PROCESS stays `88990`, AGENTS.template `9980`, and
CLAUDE `7975`. Materialized skill copies match; no hard cap changed.
<!-- fig: cmd="wc -c project-trajectory/PROCESS_OPTIONS.md project-trajectory/skills/byte-budget-guard/SKILL.md project-trajectory/skills/spine-authoring/SKILL.md project-trajectory/PROCESS.md project-trajectory/AGENTS.template.md CLAUDE.md" rev=1e78ada3+OI85-final-guidance -->

### Final phase-close result

```text
.venv/bin/python -m pytest -q -n auto --junitxml=out/run-logs/oi85-full-final.xml
3661 passed, 22 skipped in 744.34s (0:12:24)
```

This is the final unfiltered source, including the repaired selector, classified
new test module and regenerated prompt catalogue. The complete P9R HTML family
(176 cases) and core/shared census (130) are green within that run; the
[P9R record](../ai-template-redesign-2026-09-05-codex/P9R-EXECUTION.md#final-measurement-2026-09-06)
distinguishes testcase-duration sums from wall time and from an unobserved
ordinary-change narrow run. The complete current proposal correctly selects
Full. Strict trajectory, trace/schema integrity, vocabulary, Ruff and the
regenerated current surfaces pass. Docs retain the pre-existing report orphan
warning, with no broken links.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto --junitxml=out/run-logs/oi85-full-final.xml" rev=1e78ada3+OI85-final; out/run-logs/oi85-full-final.txt -->

The first commit smoke run passed its tests: `1680 passed, 4 skipped in 80.15s`.
Its time exceeded the unchanged 60-second target; the separate enforcing run
is recorded below. The owner's standing exception covers this machine's flaky
smoke timing, not a correctness or membership failure.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto -m smoke" rev=1e78ada3+OI85-final; out/run-logs/oi85-smoke.txt -->

```text
.venv/bin/python scripts/check_smoke_budget.py --mode enforce
1680 passed, 4 skipped in 61.38s (0:01:01)
smoke wall-clock budget: 61.6s vs 60s budget -> OVER
```

The enforcing command exited 1 on timing alone. The owner's standing permission
to commit despite this computer's flaky smoke timing applies; no timing pass,
budget change, membership-cap waiver or correctness waiver is claimed. Local
commit uses the installed hooks and does not push. The source-anchored resync
entry follows this implementation commit because its exact hash does not
exist until the commit is made.
<!-- fig: cmd=".venv/bin/python scripts/check_smoke_budget.py --mode enforce" rev=1e78ada3+OI85-final; out/run-logs/oi85-smoke-budget.txt -->

The explicit control-launch conditions and existing
SR-161 verification gap remain as recorded above; no new operational hold or
queue mutation was introduced.
