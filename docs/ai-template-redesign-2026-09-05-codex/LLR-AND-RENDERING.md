# Replaceable LLR designs and an isolated HTML renderer

**Owner follow-up:** 2026-09-05. **Status:** additions to the redesign proposal, after the Fable review; not independently reviewed by Fable and not implemented. The authoritative home of this plan is `docs/ai-template-redesign-2026-09-05-codex/` inside this repository. Keep its documents and review history here.

## 1. LLRs should constrain the selected implementation without freezing the design

Your concern is credible. LLRs are normally the solution-specific decomposition of a parent requirement. That makes them useful implementation contracts, but it must remain possible to replace a contract when a better design satisfies the parent obligation. Approval means the current design was accepted; it does not mean future work must preserve its mechanism indefinitely.

The repo already permits this. The [Spine Authoring skill](../../.agents/skills/spine-authoring/SKILL.md) explicitly allows a worker to amend approved row text while reserving the approval act for the appropriate adjudication session. [PROCESS](../../project-trajectory/PROCESS.md), around lines 447–465, also separates approval of text from passing implementation and says a child amendment does not itself amend its parent.

But the same process's change-intake diagram, around lines 860–888, has only two routes: an existing SR/LLR is violated → coverage gap; no row speaks to it → requirement gap. It does not ask whether the existing design is still justified. This is a concrete source of pressure to patch code around an obsolete LLR. It supports the concern about the workflow; it does not prove how often agents chose a workaround for this reason.

### Add one normal intake outcome: replace an unsuitable design

Before classifying a mismatch as missing test coverage, ask whether the governing obligation and its current decomposition remain appropriate.

| Situation | Normal action |
|---|---|
| Parent obligation and selected design remain sound; code violates them | Write the missing regression and fix the implementation |
| Parent obligation remains sound; the LLR's chosen mechanism is the problem | Amend or replace the LLR and its implementation-specific verification together |
| Proposed change alters externally promised behavior, a justified constraint, or acceptance | Amend the affected SR/SN through its applicable authority before enabling the change |
| Requirement is sound and only a module/path/symbol moved | Update its trace references; do not invent a new behavior requirement |

A concrete example is LLR-149's multi-WI spine batch. If the owner accepts one WI per lane, preserving batching through an adapter would preserve the very complexity the redesign removes. Replace the batch design and its tests while maintaining bounded execution, serial integration, and approval integrity. Here SR-148 also embeds an admission mechanism, so it must be included in the amendment; simply calling the change an LLR replacement does not make that parent constraint disappear.

A less coupled example is LLR-182: its terminal-outcome invariants may remain correct while the helper/module organization changes. Keep the externally meaningful distinction between missing, ambiguous, and valid outcomes; do not require a wrapper just to keep an obsolete import path, unless supported adopter compatibility actually requires it.

### Make replacement cheaper than a workaround

Use the existing WI and amendment review, not another mandatory registry or approval layer. The brief needs a compact comparison: affected LLRs, parent acceptance clauses and justified constraints, why the current mechanism is unsuitable, replacement design, preserved behavior, tests retained/replaced, and the code/compatibility paths that become removable.

- A worker may author that replacement within an already authorized WI's outcome. Do not automatically ask the human again because an LLR is Approved. Apply the current approval dial to the affected artifact tier; writing a proposal and approving it remain separate acts.
- If it changes the WI's promised result, declared execution risk, dependency/exclusive scope, or held authority, return that change to intake before continuing dependent execution. Do not silently expand an active assignment or force the old design merely to avoid reclassification.
- Keep an LLR ID when it still names the same design responsibility and its content is amended. When obligations split, combine, or disappear, use the existing retirement/history convention and explicit successor references. Do not reuse an ID for unrelated meaning or create a new live lineage database.
- Provide a small replacement preview showing old/new design, affected parent clauses, and typed inbound references. Apply the reviewed reference updates atomically with the replacement and validate missing/dangling references; do not use blind text substitution. Start with existing amendment tooling before adding a helper. Keep the existing deletion/history convention for supersession, rather than adding a live `supersedes` field or requiring a new ID for every semantic amendment.
- Preserve previous approved text and its acceptance record as history. Update the live design, trace links, and tests together and re-attest the changed content through the existing mechanism. The parent is re-approved only if its own normative content changes or the governing policy otherwise requires it. Its text approval can remain while derived stage/Founded state falls until the replacement child chain is ready; do not present preserved parent approval as proof that the new implementation is complete.
- Preserve tests of enduring outcomes and known failures. Translate a regression to the new boundary where necessary. Retire a test whose only purpose is the removed mechanism after the replacement obligation/evidence is reviewed; do not keep a fake old API just to satisfy it.
- An LLR is not automatically disposable: derived safety/security behavior, externally consumed interfaces, performance bounds, and compatibility commitments need their rationale examined. An allegedly internal choice may carry an obligation the parent states incompletely; surface that issue rather than deleting it.

**Implementation placement:** P0 inventories mechanism-preserving tests and migration obligations. P1/P1A amend the intake decision and any conflicting contracts. P7's worker/reviewer briefs explicitly permit justified design replacement and ask whether a proposed workaround exists only to satisfy an obsolete LLR. P9 removes displaced live doctrine and tests. This is one change to the normal authoring route, not a separate process for every refactor.

**Acceptance:** a representative refactor can replace a selected LLR without changing unchanged parent approval, bypassing required child approval, or retaining an obsolete shim. The preserved behavioral regression still catches the original failure. A changed stakeholder obligation cannot be hidden as a design-only replacement.

## 2. Isolate rendering as a package in this repository

I recommend a package and test boundary first, not another repository. A separate repository would introduce versioning, releases, adopter synchronization, and cross-repository contract testing before those costs have been justified.

The HTML implementation is already split into `traj_render`, `traj_views`, `traj_panels`, and `traj_graph`. Merely moving those files would not establish independence: [gen_trajectory.py](../../project-trajectory/scripts/gen_trajectory.py) is a facade that imports/re-exports renderer, parser, and text-status functionality; [check.py](../../project-trajectory/scripts/check.py), around lines 950–980, and [trunk_step.py](../../project-trajectory/scripts/trunk_step.py), around lines 546–557, invoke that same command for both HTML and `--status`.

The boundary should be:

```text
Authoritative work/spine/policy readers
                 ↓
        shared project snapshot
           ↙             ↘
 CLI / text status     HTML rendering package
                           ↓
                    PROJECT_STATE.html
```

The snapshot is a typed in-memory read model, not a second authored registry or a required intermediate file. Reuse the proposed domain/read-model layer; do not build a framework around it. Core scheduling, validation, and text status must not import HTML templates, graph layout, CSS, or browser code. The renderer consumes the snapshot and cannot mutate work, approve artifacts, or decide scheduling.

Separate generation/freshness of text status from HTML at the command boundary. Keep a temporary compatibility launcher for existing `gen_trajectory.py` callers if the migration contract needs it, with an explicit deletion release. Its `--status` path must not import the renderer. Classify other generated HTML, including open-items views, deliberately rather than leaving an unnoticed second rendering path in the core.

Separate tests by behavior, not filename prefix. `test_trajectory_*` includes registry, approval, and architecture integrity checks that must not be demoted to optional UI tests. Some `test_traj_*` tests exercise parsing and text status and belong in the shared/core set. Refactor shared fixtures so collecting core tests does not import the renderer facade.

### Run expensive rendering tests when the rendering capability can be affected

“Only when HTML source files change” is too narrow. A shared parser can change status values; a snapshot producer can change graph edges; a font, template, or long content value can break layout without an edit to the Python emitter.

Use a small explicit selection table in the existing test/CI configuration, with one owner for membership and no general test-impact engine:

| Change | Ordinary change validation |
|---|---|
| Core code proven independent of the renderer and its snapshot inputs | Core tests and shared contract checks; omit the expensive HTML suite |
| Routine registry/WI values with unchanged input shape | Core/trace checks plus actual-input generation/freshness and a cheap renderer boundary smoke when HTML is enabled; no automatic full width/theme/tab matrix |
| HTML emitter, layout, styles, JavaScript, templates, assets, or renderer fixtures/tests | Full rendering test family and applicable visual/accessibility scenarios |
| Snapshot schema, shared parser/producer, stage/status vocabulary, graph semantics, shared fixtures, or relevant dependency/toolchain changes | Shared contract tests and affected rendering suite; do not classify as core-only |
| Test selection, bootstrap/profile wiring, broad refactor, unknown impact, or unavailable comparison base | Run the broader suite; report why selection could not narrow it |
| Phase close, release, and a declared periodic assurance run | Full enabled-capability suite, including rendering, to detect omissions in change selection |

The inexpensive boundary checks should validate snapshot shape/meaning and one representative output, including honest status labels and escaping. They do not prove visual quality. Changed content that is known to stress layout or interaction should trigger the relevant visual case; routine data changes are not a reason to rerun every rendering scenario.

Keep required generated-output freshness when source data changes. That is one generation/validation of the current input, not thousands of renderer regressions. If committed HTML becomes too expensive to regenerate, changing its publication/freshness policy is a separate explicit decision; test isolation must not silently turn a stale dashboard into a passing one.

Selection must compare the complete proposed change to its recorded base, account for renamed/deleted files and shared inputs, and broaden on uncertainty. Do not base it only on the last commit. Initially retain the full CI matrix while evaluating narrower local selection. Once a separate, evidenced cadence decision authorizes selective CI, local and CI invocation must use the same selection result; an always-running required job reports what ran and why a rendering suite was not applicable. Do not leave a required check pending through a workflow-level path skip, and do not report unrun cases as passing.

Current CI runs the complete suite on its test matrix, and several trajectory modules are already excluded from the local smoke tier in [tests/conftest.py](../../tests/conftest.py). Changing these declarations requires the relevant assurance-contract amendments, especially SN-007's full-suite acceptance, and measured before/after duration. No selectors, coverage floors, gates, or test membership have been changed by this proposal. Full runs must retain honest renderer coverage; core-only runs must not claim full-project coverage from partial evidence.

### Rendering work package and exit criteria

P9R can proceed independently of the runner rewrite after P0's boundary inventory and the rendering-specific contract amendments are ready:

1. Measure rendering-family costs separately from core, shared parsing, and generation/freshness. Produce an explicit test membership list from behavior; do not infer it from `traj` in the name.
2. Extract the snapshot and rendering package; split text-status CLI and fixtures; preserve current observable HTML behavior and accessibility.
3. Establish core/shared/rendering test families, the small impact table, and a broad-run fallback. Verify selection for core-only, data-only, schema, CSS/JS/assets, renderer removal/rename, and unknown-base changes.
4. Demonstrate that core imports and test collection work with the HTML package absent, and that an enabled renderer still receives correct current data and meets its full suite.
5. Compare core-change latency, actual-data generation, and full-suite duration against the recorded baseline. Retain periodic/full gate verification under the approved cadence; delete displaced facade imports and duplicated fixtures after the compatibility window.

The result should be a normal core WI that does not load or regression-test HTML, and an HTML-affecting change that reliably gets the appropriate assurance. Splitting directories without that dependency and test boundary is not completion.

## 3. Cross-reference qualification

The [Claude comparison](CROSS-REFERENCE-CLAUDE.md) adds an early adopter fixture, replacement-preview tooling, and a staged rollout of test selection. Its claimed smoke cost from `test_traj_graph` does not match `tests/conftest.py`: that module is already in `SLOW_MODULES` at both the original source baseline and comparison revision. Measure actual savings; do not count an already-excluded family as a new per-commit reduction. These additions are proposal changes, not a new Fable review or an implemented cadence change.
