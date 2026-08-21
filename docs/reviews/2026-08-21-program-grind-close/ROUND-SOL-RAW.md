## Findings

1. **CRITICAL — `--correct-mark` authorization is forgeable and replayable by editing one comment**

   Evidence: [trace.py](C:/Projects/ai-template/project-trajectory/scripts/trace.py:723) defines the trusted comment grammar; [trace.py](C:/Projects/ai-template/project-trajectory/scripts/trace.py:910) loads it without authenticating the ruling; [trace.py](C:/Projects/ai-template/project-trajectory/scripts/trace.py:1002) accepts a correction when only the old/new tuple matches; the replay test at [test_id_watermark.py](C:/Projects/ai-template/tests/test_id_watermark.py:526) exercises the CLI, not direct file forgery.

   Failure scenario: replace the current line with `# correction: B 8 -> 999 (anything)` and set `B = 999`. The history check treats the forged comment as authorization. The “one-shot” property only stops a second invocation while the original comment remains; it does not stop replacing or fabricating the record. An ordinary bump does preserve the record, so that narrower claim holds.

   Suggested fix: validate an immutable correction chain against a real ruled OI and its authorized tuple; reject deletion/replacement of committed correction entries.

2. **MAJOR — the new seam-TC gate can be greened by silently growing its allowlist**

   Evidence: [check_trajectory.py](C:/Projects/ai-template/project-trajectory/scripts/check_trajectory.py:1006) accepts live IF IDs with no mandatory reason; [check_trajectory.py](C:/Projects/ai-template/project-trajectory/scripts/check_trajectory.py:1083) removes every listed ID from the hard-error population; hygiene at [check_trajectory.py](C:/Projects/ai-template/project-trajectory/scripts/check_trajectory.py:1101) checks unknown and stale entries, but not growth or missing reasons.

   Failure scenario: introduce an uncovered `IF-138`, then add the bare line `IF-138` to `docs/if-tc-coverage-allow`. At DevStg-Tests it disappears from the ERROR set, and allowlist hygiene reports nothing. This violates the stated “migration list should not grow” contract.

   The initial 120 entries are honest: the live checker independently reproduced exactly 120 uncited seams.

   Suggested fix: ratchet the allowlist population, fail on additions unless accompanied by a non-empty reviewed justification, and report every growth delta.

3. **MAJOR — the backlink campaign conflates “participates in” with “implements the complete LLR”**

   Evidence: LLR-155 names five cooperating symbols and several collective obligations at [low-level-requirements.toml](C:/Projects/ai-template/docs/requirements/low-level-requirements.toml:1551). Each constituent independently carries the full `Implements: LLR-155` assertion: [agent_common.py](C:/Projects/ai-template/project-trajectory/scripts/agent_common.py:267), [agent_common.py](C:/Projects/ai-template/project-trajectory/scripts/agent_common.py:340), [agent_common.py](C:/Projects/ai-template/project-trajectory/scripts/agent_common.py:501), [agent_common.py](C:/Projects/ai-template/project-trajectory/scripts/agent_common.py:647), and [agent_common.py](C:/Projects/ai-template/project-trajectory/scripts/agent_common.py:838). Likewise LLR-067’s inventory and crossing obligations are split between [check_trajectory.py](C:/Projects/ai-template/project-trajectory/scripts/check_trajectory.py:847) and [check_trajectory.py](C:/Projects/ai-template/project-trajectory/scripts/check_trajectory.py:1491).

   Failure scenario: a generated architecture map presents `process_config` as implementing LLR-155 even though it does not perform shape refusal, conflict handling, ordinal comparison, or human-hold interpretation. Coverage stays satisfied as long as any constituent retains the tag, even if another required constituent disappears.

   I sampled tags in `agent_common`, `agent_loop`, `bootstrap`, `check`, `check_privacy`, `check_trajectory`, `derive_gate`, `dispatch`, `integrate`, `schedule`, `trace`, and `traj_render`. The cited code was relevant, but collective rows make the unqualified symbol-level claim stronger than the evidence.

   Suggested fix: distinguish `Implements:` from `Implements-part:`, or place the full backlink on a module/facade symbol and record constituent participation separately.

4. **MAJOR — the import-layer guard detects new SCC membership, not new coupling inside the existing SCC**

   Evidence: [test_import_layers.py](C:/Projects/ai-template/tests/test_import_layers.py:57) stores only SCC node tuples; [test_import_layers.py](C:/Projects/ai-template/tests/test_import_layers.py:206) proves function-body imports are visible, but [test_import_layers.py](C:/Projects/ai-template/tests/test_import_layers.py:231) compares only the resulting component sets.

   Failure scenario: add a new function-body import from `handback` to `intake`, or any new edge among the existing five SCC members. The graph sees the edge, but the five-node SCC remains identical and all tests pass. Cycle density can regress without red.

   Suggested fix: ratchet the exact intra-SCC edge set or edge count, including deferred/function-body edges.

5. **MAJOR — the B-05 conversions erase internal consumers from the structured graph**

   Evidence: IF-021, IF-022, and IF-023 now name only `external:downstream adopter` at [interfaces.toml](C:/Projects/ai-template/docs/requirements/interfaces.toml:349), [interfaces.toml](C:/Projects/ai-template/docs/requirements/interfaces.toml:362), and [interfaces.toml](C:/Projects/ai-template/docs/requirements/interfaces.toml:375). Their notes admit populations of 14+, 9, and 9 internal readers.

   Failure scenario: machine-readable impact analysis reports only an external adopter boundary. An internal reader can be removed or materially changed without the registry exposing which in-repo consumers were affected; the real population survives only as prose and a count.

   Suggested fix: retain a published-contract row plus separate structured internal-consumer rows, or add a machine-readable consumer-set field.

6. **MAJOR — the module-size ratchet is completely blind to the new `kitlib` package**

   Evidence: [test_module_size_ratchet.py](C:/Projects/ai-template/tests/test_module_size_ratchet.py:1848) uses `scripts/*.py`, not a recursive traversal.

   Failure scenario: `scripts/kitlib/registry.py` can grow to 3,000 lines and the module-size test remains green. This batch created precisely the package tree outside the guard’s census.

   Suggested fix: recurse through packages and key baselines by relative path rather than basename.

7. **MAJOR — the batch repeatedly called a mandatory over-budget smoke run green**

   Evidence: [CLAUDE.md](C:/Projects/ai-template/CLAUDE.md:58) and [stack.ini](C:/Projects/ai-template/docs/stack.ini:109) declare 60 seconds. The log records commit-bar runs of 66.21 seconds at [program-grind.md](C:/Projects/ai-template/docs/log.d/2026-08-20-program-grind.md:163), 74.78 at line 329, 116.37 at line 1200, and 116.71 at line 1726; another run reached 142.92 at line 418.

   Failure scenario: pytest exits zero, the commit is described as green, but the repository’s stated commit-bar budget has failed. This trains reviewers to interpret “green smoke” as test-result-only while the governing protocol says the time budget is part of the bar.

   No ceiling was quietly raised; the dishonesty is the pass characterization, not a restamp.

   Suggested fix: make the local smoke command enforce the 60-second wall budget, or explicitly redefine 60 seconds as a CI target rather than a mandatory commit bar.

8. **MAJOR — `spec_move.py` can silently turn a requested directory into a file and make a WI disappear**

   Evidence: [spec_move.py](C:/Projects/ai-template/project-trajectory/scripts/spec_move.py:318) rejects an existing destination of any kind, while [spec_move.py](C:/Projects/ai-template/project-trajectory/scripts/spec_move.py:320) creates only the destination’s parent and then treats the supplied destination as the file path.

   Failure scenario: invoke it with a nonexistent trailing-slash lane such as `docs/work/active/wi448-common-module/`. Windows path normalization loses the directory intent, a file named `wi448-common-module` is created, and registry discovery no longer sees the WI. If no predecessor references the vanished row, no trajectory finding fires.

   Suggested fix: require an explicit destination filename, or recognize directory intent and append the source filename; reject ambiguous destinations loudly.

9. **MAJOR — `trace.exit_code` and its test stub are two unpinned schemas**

   Evidence: [test_trace_rules.py](C:/Projects/ai-template/tests/test_trace_rules.py:779) hand-builds `_findings_stub`; its attributes are manually enumerated starting at line 790. `trace.exit_code` independently reads the real finding attributes at [trace.py](C:/Projects/ai-template/project-trajectory/scripts/trace.py:4832).

   Failure scenario: add a new exit-code arm but forget the stub attribute. Commit-tier tests remain green because this module is outside smoke; the full suite later crashes with `AttributeError` instead of testing the new rule. That happened during the Hat-Refs work.

   Suggested fix: construct the stub from the real Findings type/defaults and assert that the attributes read by `exit_code` equal the schema.

10. **MINOR — IF-070 falsely names `check.py` as a reader of `coverage.json`**

   Evidence: IF-070 lists both consumers at [interfaces.toml](C:/Projects/ai-template/docs/requirements/interfaces.toml:909). [check.py](C:/Projects/ai-template/project-trajectory/scripts/check.py:2056) only clears/unlinks the stale file; [check_coverage.py](C:/Projects/ai-template/project-trajectory/scripts/check_coverage.py:131) actually parses it.

   Failure scenario: dependency analysis sends a coverage-format change to `check.py`, although that module does not consume the format, while conflating lifecycle ownership with content consumption.

   The other low-fan-out samples—IF-025, IF-026, IF-029, IF-035, and IF-052—matched real readers.

   Suggested fix: name only `scripts/check_coverage` as the consumer and model file lifecycle separately if needed.

11. **MINOR — deferral checking produces avoidable noise while genuine stale declarations remain warn-only**

   Evidence: [gen_open_items.py](C:/Projects/ai-template/project-trajectory/scripts/gen_open_items.py:833) extracts every OI ID from the entire payload, then line 838 declares `none` only when no IDs were found. Thus text such as “none — OI-45 is fully executed” is treated as an OI declaration. Meanwhile the old declarations in `2026-08-20-frontier-grind.md:9` and `2026-08-20-owner-rulings-oi45-46.md:3` still name ruled OI-45/46/47.

   Failure scenario: the close command always emits both real stale-declaration warnings and false warnings from explanatory “none” text. Operators become habituated to noise and miss the next real stale fragment.

   Suggested fix: make a leading `none` terminal for that declaration and clean or explicitly supersede the older fragments.

## Adjacent-findings disposition

Every banked item was checked:

- **Confirmed:** OI-46’s prose names the wrong twin pair. `GREPPABLE_KEYS` contains only privacy keys at [agent_common.py](C:/Projects/ai-template/project-trajectory/scripts/agent_common.py:230); the tested behavioral twins are `check_trajectory` and `gen_okf`.
- **Confirmed:** the hook README still says “deny-by-default” at [agent-hooks/README.md](C:/Projects/ai-template/project-trajectory/agent-hooks/README.md:30), contrary to the opt-in/fail-open implementation.
- **Refuted as live debt:** LLR-172 now correctly names `check_trajectory/component_findings` at [low-level-requirements.toml](C:/Projects/ai-template/docs/requirements/low-level-requirements.toml:1753); no live `budget_findings` anchor remains.
- **Confirmed:** “labelled derived requirement” remains in the `spine-authoring` frontmatter and generated index.
- **Confirmed and elevated to Finding 9:** `_findings_stub` is unpinned.
- **Confirmed resolved:** the registry-machinery table now classifies LLR `SR-Refs` correctly.
- **Confirmed:** `hats.py` has no optional-key mechanism, so the proposed `knowledge` field would otherwise become mandatory.
- **Confirmed:** the four-way `kitlib` component tag suppresses cross-component findings by shared membership; OI-48 accurately records this.
- **Confirmed mechanism, historical example resolved:** interface derivability checks module agreement, not semantic relevance. IF-093 was repaired, but the laundering class remains.
- **Confirmed and elevated to Finding 8:** `spec_move` destination asymmetry.
- **Confirmed:** `test_bootstrap.py` hand-maintains a readable subset of `MAPPING` beside the completeness test.
- **Confirmed:** OI-30’s “relaxes nothing” reasoning missed step reachability; WI-473/OI-51 now records and pins the consequence.
- **Confirmed:** nested functions count toward the enclosing C901 result; moving the helper to module scope lowered the measured complexity.
- **Confirmed:** byte-cap measurement reads working-tree bytes and is line-ending-dependent.
- **Confirmed:** `--list` mixes gating and advisory steps in one textual stream; current tests split the sections correctly, but the interface remains error-prone.
- **Confirmed:** no retired-CMP-ID prose detector exists; the 22 current notes were swept manually.
- **Confirmed class:** Windows `write_text` newline translation caused LF-indexed/CRLF-worktree residue. Current count is 51 files, not the earlier ~47.
- **Confirmed:** IF-131 carries exactly one constituent, as OI-49 states.
- **Refuted as current state:** the B/REL spent-watermark problem was corrected to B=8/REL=4. The replacement mechanism is nevertheless forgeable, as Finding 1 shows.
- **Confirmed and elevated to Finding 11:** older fragment declarations are stale.
- **Confirmed:** the line ratchet measures file length rather than functional complexity; the recorded upward/downward restamps are real, but weak evidence.
- **Confirmed and elevated to Finding 6:** package blindness.
- **Confirmed:** substantial LF-indexed/CRLF-worktree residue remains; it is local residue, not committed newline state.
- **Confirmed:** the `test_rule_sync` comment claiming bootstrap can import no sibling is stale; bootstrap now imports `kitlib`.
- **Confirmed and elevated to Finding 8:** nonexistent trailing-slash destinations can become files.
- **Confirmed:** citation-frame checking intentionally catches fresh WI/date notes in live registry prose. This is an ergonomics trap, not a false checker result.
- **Confirmed workflow hazard:** duplicate TOML keys fail loudly but the parser often identifies only the later assignment, making bulk-edit diagnosis poor. It is not a silent product failure.

The Hat-Refs backfill remained snapshot-clean for the intended reason: Hat-Refs is traced, not ratified; changing requirement text would still trip approved-snapshot drift. IF-134/135 also match the declared B-01/B-04 crossings, and IF-135’s B-04-only choice is recorded honestly.

Validation was constrained by the repository’s broken literal `.venv` path, so I could not run the full pytest suite. I ran the compatible generators/checkers under Python 3.8 with `tomli` shims and performed source-path tracing for the remaining cases.

## The three claims I tried hardest to refute and could not

1. **The numeric backlink result is real:** the declared command reproduces **83/165, 50.3%**. The defect is tag semantics, not the arithmetic.
2. **A genuinely uncovered, non-allowlisted seam does hard-fail at DevStg-Tests, and the seeded allowlist honestly measures 120 entries.**
3. **The duplication and ancestry claims hold:** the slice commit reproduces **757→477 redundant lines**, and both `cda29c42` and `dea8364e` are ancestors of `bd8fce68`.