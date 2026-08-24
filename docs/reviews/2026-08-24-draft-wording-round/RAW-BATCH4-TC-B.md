# Raw return - batch 4 (TC-194, TC-198, TC-192, TC-191, TC-189)

Unedited final message from `OPENAI-TERRA` (`gpt-5.6-terra`, `codex exec`),
captured with `--output-last-message`. Adjudicated in `RESUME.md`.

```
=== TC-194 Method
SUGGEST: Drive blocked rows, Drafted or drifted SRs, tracked pauses, and malformed pauses through the former facade. Assert that blocked rows show their pointer, Drafted or drifted SRs show the depth brief, tracked pauses render exactly one bullet, malformed pauses fail closed, and two reads match. Assert every item has `kind`, `owner_cards` equals `pending_items` without the pause, every item line is rendered, the dispatcher's card read and generated owner-surface block equal the read model answer, and the facade resolves all four former names to read-model functions. Build the shipped-script import graph, counting imports inside function bodies, and assert no script imports the dashboard facade. Through the validator's work-registry loaders and real temporary repositories, derive blocked rows end to end and assert a non-answering loader fails rather than producing an empty owner queue for IF-138.
CUT-REDUNDANT: none
CUT-KEPT: Fail-closed malformed pauses, deterministic reads, facade compatibility, function-body imports, and the IF-138 loader path remain because they bound observable failure and ownership behavior.
RISK: none

=== TC-194 Expected
SUGGEST: For SR-168 and LLR-198, the rendered owner block matches the read model, contains every item, exposes the required blocked, brief, and pause states, and has no dependency on the dashboard facade; a failed work-registry loader fails the derivation.
CUT-REDUNDANT: The blanket claim that the case satisfies the parent acceptance; the concrete outcomes replace it.
CUT-KEPT: The loader-failure outcome remains because an empty owner queue would conceal a broken IF-138 seam.
RISK: none

=== TC-198 Method
SUGGEST: Use a real two-commit git repository whose HEAD contains Approved SR-001 and, for tier coverage, Approved LLR-001 and TC-001; stage the change. Amend the requirement while `Hat-Refs` remains unchanged and assert one finding names the row and moved cells while the amendment arm also fires. Edit only `Hat-Refs`, then only `SN-Refs`, and assert neither raises a finding. Move substance and `Hat-Refs` together and assert this finding is absent while the amendment arm still fires. Assert no finding for a row created in the staged change or for a row below approval in both revisions. Amend an LLR and TC in one change and assert exactly one finding, for the LLR, proving the check is scoped to tiers with the column.
CUT-REDUNDANT: none
CUT-KEPT: The staged-change condition, traced-only silence, discharged condition, baseline-vacuity cases, and LLR-versus-TC split remain because each defines when the finding may occur.
RISK: none

=== TC-198 Expected
SUGGEST: For SR-161 and LLR-202, an approved requirement amendment without a matching `Hat-Refs` change produces a row-named finding; traced-only changes, discharged paired changes, new rows, and rows below approval do not. A simultaneous LLR and TC change produces only the LLR finding, while the existing amendment arm continues to fire where required.
CUT-REDUNDANT: The blanket claim that the case satisfies the parent acceptance; the concrete outcomes replace it.
CUT-KEPT: The discharged, vacuous, and tier-scoping outcomes remain because they prevent false findings.
RISK: none

=== TC-192 Method
SUGGEST: Exercise `gen_prompt_catalog.render` directly. `test_the_catalogue_lists_every_shipped_prompt_with_its_digest` asserts that rendered text contains every `prompts.KIT_PROMPTS` key and every `prompts.catalog_rows()` digest. `test_the_catalogue_on_disk_is_FRESH` runs `catalog.main(["--check"])` against the committed file and asserts exit 0 for LLR-164. `test_a_template_edit_moves_its_digest_and_so_the_catalogue` asserts a text edit changes the digest and a line-ending-only edit does not. `tests/test_generated_freshness_wiring.py::test_prompt_catalog_step_reds_when_a_template_changes` runs the wired `[step:]` enforcer on a bootstrapped scaffold: edit a template, assert the commit-floor step fails, run `gen_prompt_catalog.py`, then assert the step passes.
CUT-REDUNDANT: none
CUT-KEPT: The direct render, line-ending exception, committed-file check, and wired scaffold path remain because each verifies a distinct catalogue failure mode.
RISK: none

=== TC-192 Expected
SUGGEST: For SR-146 and LLR-164, the catalogue renders every shipped prompt and digest, `--check` passes for the committed catalogue, text changes alter digests while line-ending-only changes do not, and regenerating after a template edit restores the failing `[step:]` check.
CUT-REDUNDANT: The blanket claim that the case satisfies the parent acceptance; the concrete outcomes replace it.
CUT-KEPT: The line-ending result remains because it distinguishes a stale catalogue from a CRLF-only change.
RISK: none

=== TC-191 Method
SUGGEST: Run the actual folding path. `tests/test_generated_newlines.py::test_the_three_crash_paths_actually_run` calls `agent_common.regenerate_index` on a synthetic `docs/` tree and asserts the generated table exists, exercising the per-session row fold cited by LLR-196. `tests/test_agent_loop.py::test_done_exit_writes_logs_and_index` and `::test_stream_json_echo_and_result_parse` drive a fake CLI session end to end and assert that `wall-secs`, `api-secs`, `turns`, `tokens`, `cache-read`, and `cache-create` are written to the log header read by `regenerate_index`, `per_turn_pace`, and `per_turn_context`. No test groups configured versus occupied lanes or work per wall-hour, because LLR-196 states that grouping is not built; this case verifies grouping inputs, not the SR-177 report.
CUT-REDUNDANT: none
CUT-KEPT: The named telemetry columns and stated missing grouping remain because they define the verified input boundary and residual build gap.
RISK: none

=== TC-191 Expected
SUGGEST: For SR-177 and LLR-196, the generated index exists and a completed fake session writes `wall-secs`, `api-secs`, `turns`, `tokens`, `cache-read`, and `cache-create`. This covers telemetry inputs only: configured-versus-occupied lanes and work-per-wall-hour are not grouped, so the utilisation report, its reported-and-never-gated behavior, and its lack of a declared improvement target are not discharged; the grouping remains the build gap.
CUT-REDUNDANT: The blanket claim that the case satisfies the parent acceptance; concrete input outcomes and the undisclosed report gap replace it.
CUT-KEPT: The non-discharge, non-gating, no-target, and build-gap statements remain because they prevent telemetry collection from being mistaken for the required utilisation report.
RISK: none

=== TC-189 Method
SUGGEST: Exercise the existing `REQUIRED_FIELDS` and `ENUM_FIELDS` table, currently used for IF because no SN entry exists yet, as the mechanism that will carry scope. Assert that a missing column produces a warning naming the row and exact column, gates only with `--strict`, and does not gate on a bare read. Assert that a value outside a closed vocabulary produces a schema finding naming the row, offending value, and full allowed set; `--strict-schema` alone is silent and `--strict` gates. This verifies the missing-or-invalid, row-named mechanism without an SN-specific checker.
CUT-REDUNDANT: none
CUT-KEPT: The bare-read, `--strict-schema`, and `--strict` split remains because it defines both reporting and gating behavior.
RISK: none

=== TC-189 Expected
SUGGEST: For SR-164 and LLR-194, the generic schema mechanism names the row and column for missing fields, and names the row, offending value, and allowed set for invalid enum values. Missing fields gate only under `--strict`; invalid enums are silent under `--strict-schema` alone and gate under `--strict`. This verifies the mechanism shape only: no SN entry exists yet.
CUT-REDUNDANT: The blanket claim that the case satisfies the parent acceptance; the concrete mechanism outcomes replace it.
CUT-KEPT: The absence of an SN entry remains because this case must not be read as validating the required SN scope field.
RISK: none
```
