ocs/requirements/low-level-requirements.toml:1708); TC-162 likewise tests only load/select/compose behavior at `test-cases.toml:1609`. The separate audit path begins with `_audit_needs` at `hats.py:495` and reaches the CLI at `hats.py:787`.  
Failure scenario: audit selection or diagnostics regress while the Approved requirement and its test remain green because neither traces to that behavior.  
Suggested fix: mint a separate audit LLR/TC pair, or explicitly expand LLR-168 and TC-162 to cover the audit functions and CLI.

10. **MAJOR — WI-479’s dashboard-title defense is not behaviorally pinned, and its visual verification is not retained.**  
Evidence: the overlong-title disclosure is implemented at `gen_trajectory.py:788`. WI-479 claims four-width screenshots and keyboard verification at `WI-479-dashboard-title-overflow.md:23`, but the commit contains no retained screenshots. The existing panel test checks only the title/class/id at `test_traj_panels.py:670`, not the disclosure behavior.  
Failure scenario: remove the `<details>/<summary>` routing while retaining the title attribute; all current tests pass although narrow-width defense and keyboard disclosure disappear.  
Suggested fix: add an overlong-active-WI regression asserting native disclosure markup and preserve the declared render matrix as review evidence.

11. **MINOR — The shipped downstream launchers still reproduce the interpreter-selection defect fixed in the repo launcher.**  
Evidence: `run.template.sh:13` chooses ambient `python3`/`python` without version or `.venv` probing; `run.template.cmd:14` does the same on Windows.  
Failure scenario: a downstream repo has a valid Python 3.11 `.venv` but Python 3.8 first on PATH; the launcher selects 3.8 and fails on `tomllib`.  
Suggested fix: reuse WI-475’s candidate enumeration and minimum-version probe in both templates.

12. **MINOR — Retired derived-label language remains in normative and example surfaces.**  
Evidence: PROCESS still says “labelled derived SR” at `PROCESS.md:80`; the authoring skill repeats it at `spine-authoring/SKILL.md:132`; live docstrings retain retired derived-requirement examples at `trace_text.py:465` and `trace.py:1605`.  
Failure scenario: an author follows these instructing surfaces and reintroduces a vocabulary the migration claims to have retired.  
Suggested fix: replace normative wording with the hat-derivation model and mark unavoidable old examples explicitly historical.

13. **MINOR — Several interface records are visibly stale or malformed after the grind.**  
Evidence: IF-103 still calls the resync helper “ONE-SHOT” at `interfaces.toml:1244`, although WI-452 made it live. IF-117’s contract line at `interfaces.toml:1442` contains issue tokens and rationale connective text and exceeds the stated line budget. IF-118 through IF-120 cite obsolete CMP-001–004 identifiers, beginning at `interfaces.toml:1463`, while the live component registry starts at CMP-006.  
Failure scenario: consumers implement a one-shot lifecycle or follow component references that no longer exist; advisory noise also hides later substantive warnings.  
Suggested fix: update IF-103’s lifecycle, rewrite IF-117 as a concise contract, and replace stale CMP references with live IDs.

14. **MINOR — The smoke budget’s claimed headroom has evaporated.**  
Evidence: the budget remains 60 seconds at `stack.ini:109`, while the current stamp records 57.0 seconds and only eight tests of count headroom at `stack.ini:294`. The WI-479 close itself reported a 60.23-second smoke run.  
Failure scenario: normal host jitter turns the smoke gate intermittently red despite no performance regression, encouraging arbitrary restamps or ignored failures.  
Suggested fix: either reduce smoke membership/runtime or establish a justified, measured wall-clock budget with meaningful variance headroom.

15. **MINOR — Fixture Git normalization is relied upon but not defensively tested.**  
Evidence: scaffolding establishes fixture repositories at `conftest.py:878`, and the shipped template relies on `* text=auto eol=lf` at `gitattributes.template:6`. The bootstrap assertion at `test_bootstrap.py:617` checks hook-specific lines but not the global normalization rule.  
Failure scenario: the global line is removed; Windows fixtures begin producing CRLF-sensitive diffs and snapshot failures while the intended bootstrap contract test stays green.  
Suggested fix: assert the global LF-normalization entry in the bootstrap and scaffold tests.

16. **MINOR — Two banked dashboard rendering defects are real and unguarded.**  
Evidence: `_title_clause` splits at the first textual dash at `traj_status.py:540`, so quoted titles containing `" - "` truncate incorrectly. Graph text is fixed at 10px/8.5px at `gen_trajectory.py:318`.  
Failure scenario: a WI title containing an internal dash loses its meaningful suffix, while dense graphs remain technically rendered but illegible at normal responsive widths.  
Suggested fix: parse the actual title delimiter structurally and add render-matrix legibility checks before choosing graph font sizes.

## Adjacent findings disposition

All banked findings were examined:

- **Confirmed:** unresolved LLR-015/LLR-172 local anchors; IF-117’s four advisories; stale CMP references; `_title_clause` truncation; graph font legibility; derived-label residue in PROCESS/skill/docstrings; OI-37’s missing follow-up rows; IF-103’s obsolete one-shot framing; absent LF-normalization assertion; downstream launcher selection; existential `Contracts:` validation; LLR-168/TC-162 audit omission; and stale CMP notes in IF-118–120.
- **Partially confirmed:** the smoke volatility concern is real, but the banked 1,214/1,216 membership numbers are no longer current; HEAD records 1,232/1,240 and 57.0/60 seconds.
- **Confirmed as fact, refuted as a defect:** `_apply_flips` currently performs no status writes. Its refusal is deliberate fail-closed behavior pending an owner policy, not a silently ineffective promised mutation.

I could not rerun the suite: the requested `.venv/Scripts/python.exe` points to a missing Python 3.11 installation, and the only available interpreter is Python 3.8. Findings above come from source tracing, Git diffs/blobs, and existing test semantics.

## The three claims I tried hardest to refute and could not

1. **The signing count and completeness:** commit `2d51f140` contains exactly 243 spine flips—18 SN, 70 SR, 107 LLR, 48 TC—plus 11 frame-row flips. No Drafted or Modified value survived in the five specified registries at that commit. At HEAD, only WI-472’s three deliberately Drafted rows survive; `Modified` does not.

2. **The initial seed’s byte identity:** all seven files under `docs/archive/last_approved/` were byte-for-byte identical to their live counterparts in the signing commit, including the recorded LLR-172 wording correction. The defect is the later unguarded refresh path, not the original seed.

3. **The Implements-harvester coverage number:** WI-486’s reported 1/161 reproduced at its commit. WI-472 subsequently added LLR-180, so the honest HEAD number is now 1/162, with LLR-040 still the sole literal declaration.
tokens used
291,371
## Findings

1. **CRITICAL — The “last approved” snapshot can be refreshed without an approval act, laundering ratified drift.**  
Evidence: `baseline_snapshot.py:362` requires authority only when initially seeding; `baseline_snapshot.py:389` subsequently copies the live registries unconditionally. The public `intake snapshot` path invokes that copy at `intake.py:1787`, despite the approval-only contract at `PROCESS.md:428`. Later WIs—including WI-472—did refresh the snapshot, so its current commit author is no longer the signing reviewer assumed by `low-level-requirements.toml:1765`.  
Failure scenario: alter the rationale or status of an Approved requirement, run `intake snapshot`, and commit both. Live/archive drift disappears and the unanchored-amendment check now treats the altered bytes as approved, even though no approval sitting occurred.  
Suggested fix: permit snapshot writes only through a reviewed approval transaction tied to an explicit sitting/attestation; keep Drafted-row mirroring separate from the ratified-byte baseline.

2. **MAJOR — The newly armed mirror-integrity rule cannot detect an already committed forged or stale snapshot.**  
Evidence: the ERROR rule is declared at `check_trajectory.py:3476`, but its implementation filters only `staged_names` at `check_trajectory.py:3515`. `trace --strict-integrity` calls it with the default HEAD-versus-index view at `trace.py:4604`. The tests exercise staged temporary changes or synthetic exit-code wiring, not a committed mismatch.  
Failure scenario: commit a mismatched archive with hooks bypassed. A clean-index CI invocation sees no staged snapshot files and reports no mirror error.  
Suggested fix: on every strict run, compare the committed live and archive trees—or compare both to an approval anchor—in addition to examining staged changes.

3. **MAJOR — OI-41’s arms can be satisfied without correctly retiring or resolving the deferred exception.**  
Evidence: ARM 1 validates only that the first OI token exists, not that its state or subject matches the exception, at `trace.py:1698`. ARM 3 returns early whenever *any* pending OI exists at `gen_open_items.py:924`. The test at `test_trace.py:1981` explicitly accepts a ruled row for ARM 1, while `test_gen_open_items.py:845` pins the unrelated-pending-row suppression. OI-37’s remaining unanswered questions are acknowledged at `provenance-allow:106` but still have no corresponding rows.  
Failure scenario: reference an unrelated ruled OI from the allow entry and leave any unrelated OI pending. Both arms remain quiet while the original exception and its unresolved questions persist indefinitely.  
Suggested fix: validate each deferral against its own OI’s state and subject; remove the global `if pending: return` shortcut.

4. **MAJOR — WI-466 remains a fluent false signed claim: its cited golden verification did not happen.**  
Evidence: the closed deliverable says the golden fixtures were verified unaffected at `WI-466-verified-triple-in-summary.md:20`. The same day’s record admits the clean and orphan goldens were red after that close at `2026-08-20-frontier-grind.md:95`, and they required the later `74c20704` repair.  
Failure scenario: a reviewer trusts the completed WI record and promotes `8d7ff553`; output-format tests fail immediately.  
Suggested fix: amend the completed WI with the correction and require the relevant golden tests—or the full suite—before closing output-format changes.

5. **MAJOR — Two Approved LLR code anchors do not resolve under the repository’s own strict checker.**  
Evidence: LLR-015 anchors `trace.py::budget_findings` at `low-level-requirements.toml:156`, and LLR-172 anchors `trace.py::component_findings` at `low-level-requirements.toml:1753`. Both names are locals inside `analyze`, at `trace.py:3352` and `trace.py:3390`. The resolver deliberately indexes only module/class bindings, not function locals, at `check_doc_refs.py:449`.  
Failure scenario: `check_doc_refs --strict` rejects two Approved anchors, so the signed spine is not clean under its declared reference instrument.  
Suggested fix: anchor both rows to `analyze`, or extract stable module-level functions and anchor those.

6. **MAJOR — `Modified` is retired from the schema but still interpreted as Release-level maturity by a live reader.**  
Evidence: `derive_gate.py:402` treats unrecognized statuses as Approved contribution rather than failing closed. The behavior is deliberately pinned by `test_derive_gate.py:185`, which expects `Modified` to yield the Release bar.  
Failure scenario: a downstream mid-migration registry containing `Modified`, or a typo such as `Approvd`, is processed directly by `derive_gate.py`; it can produce an advanced gate before the separate integrity checker runs.  
Suggested fix: reject unknown spine statuses in `derive_gate`; retain legacy tolerance only in explicitly transitional input readers.

7. **MAJOR — The status-vocabulary contract test does not fulfill WI-477’s “reds any instructing surface” claim.**  
Evidence: WI-477 makes that claim at `WI-477-status-vocabulary-contract.md:16`. The test scans a hard-coded list of eleven files at `test_status_vocabulary_contract.py:63`, using an assignment-shaped regex at `test_status_vocabulary_contract.py:191`.  
Failure scenario: add “Valid statuses are Drafted, Modified, and Approved” to an instructing page. Because it lacks `Status =`, the contract remains green. A new instructing surface outside the fixed list is also invisible.  
Suggested fix: scan retired terms directly with narrow historical/example exclusions, and derive the instructing-surface set from the shipped kit rather than a fixed enumeration.

8. **MAJOR — `Contracts: IF-*` validation proves existence, not that the interface belongs to the declaring module.**  
Evidence: `check_vocab.py` declares `IF-118` at `check_vocab.py:71`, but IF-118 describes `gen_open_items` and `spine_carrier` at `interfaces.toml:1451`. The checker merely verifies that declared IDs exist at `check_trajectory.py:1175`.  
Failure scenario: a module cites any unrelated live IF ID and passes the seam declaration rule, leaving its real boundary undocumented.  
Suggested fix: normalize the declaring module and require every cited IF row to name it as an endpoint.

9. **MAJOR — Approved LLR-168 and TC-162 omit the substantial hats audit mechanism they ostensibly cover.**  
Evidence: LLR-168 names only load/applicable/brief/condition symbols at `low-level-requirements.toml:1708`; TC-162 likewise tests only load/select/compose behavior at `test-cases.toml:1609`. The separate audit path begins with `_audit_needs` at `hats.py:495` and reaches the CLI at `hats.py:787`.  
Failure scenario: audit selection or diagnostics regress while the Approved requirement and its test remain green because neither traces to that behavior.  
Suggested fix: mint a separate audit LLR/TC pair, or explicitly expand LLR-168 and TC-162 to cover the audit functions and CLI.

10. **MAJOR — WI-479’s dashboard-title defense is not behaviorally pinned, and its visual verification is not retained.**  
Evidence: the overlong-title disclosure is implemented at `gen_trajectory.py:788`. WI-479 claims four-width screenshots and keyboard verification at `WI-479-dashboard-title-overflow.md:23`, but the commit contains no retained screenshots. The existing panel test checks only the title/class/id at `test_traj_panels.py:670`, not the disclosure behavior.  
Failure scenario: remove the `<details>/<summary>` routing while retaining the title attribute; all current tests pass although narrow-width defense and keyboard disclosure disappear.  
Suggested fix: add an overlong-active-WI regression asserting native disclosure markup and preserve the declared render matrix as review evidence.

11. **MINOR — The shipped downstream launchers still reproduce the interpreter-selection defect fixed in the repo launcher.**  
Evidence: `run.template.sh:13` chooses ambient `python3`/`python` without version or `.venv` probing; `run.template.cmd:14` does the same on Windows.  
Failure scenario: a downstream repo has a valid Python 3.11 `.venv` but Python 3.8 first on PATH; the launcher selects 3.8 and fails on `tomllib`.  
Suggested fix: reuse WI-475’s candidate enumeration and minimum-version probe in both templates.

12. **MINOR — Retired derived-label language remains in normative and example surfaces.**  
Evidence: PROCESS still says “labelled derived SR” at `PROCESS.md:80`; the authoring skill repeats it at `spine-authoring/SKILL.md:132`; live docstrings retain retired derived-requirement examples at `trace_text.py:465` and `trace.py:1605`.  
Failure scenario: an author follows these instructing surfaces and reintroduces a vocabulary the migration claims to have retired.  
Suggested fix: replace normative wording with the hat-derivation model and mark unavoidable old examples explicitly historical.

13. **MINOR — Several interface records are visibly stale or malformed after the grind.**  
Evidence: IF-103 still calls the resync helper “ONE-SHOT” at `interfaces.toml:1244`, although WI-452 made it live. IF-117’s contract line at `interfaces.toml:1442` contains issue tokens and rationale connective text and exceeds the stated line budget. IF-118 through IF-120 cite obsolete CMP-001–004 identifiers, beginning at `interfaces.toml:1463`, while the live component registry starts at CMP-006.  
Failure scenario: consumers implement a one-shot lifecycle or follow component references that no longer exist; advisory noise also hides later substantive warnings.  
Suggested fix: update IF-103’s lifecycle, rewrite IF-117 as a concise contract, and replace stale CMP references with live IDs.

14. **MINOR — The smoke budget’s claimed headroom has evaporated.**  
Evidence: the budget remains 60 seconds at `stack.ini:109`, while the current stamp records 57.0 seconds and only eight tests of count headroom at `stack.ini:294`. The WI-479 close itself reported a 60.23-second smoke run.  
Failure scenario: normal host jitter turns the smoke gate intermittently red despite no performance regression, encouraging arbitrary restamps or ignored failures.  
Suggested fix: either reduce smoke membership/runtime or establish a justified, measured wall-clock budget with meaningful variance headroom.

15. **MINOR — Fixture Git normalization is relied upon but not defensively tested.**  
Evidence: scaffolding establishes fixture repositories at `conftest.py:878`, and the shipped template relies on `* text=auto eol=lf` at `gitattributes.template:6`. The bootstrap assertion at `test_bootstrap.py:617` checks hook-specific lines but not the global normalization rule.  
Failure scenario: the global line is removed; Windows fixtures begin producing CRLF-sensitive diffs and snapshot failures while the intended bootstrap contract test stays green.  
Suggested fix: assert the global LF-normalization entry in the bootstrap and scaffold tests.

16. **MINOR — Two banked dashboard rendering defects are real and unguarded.**  
Evidence: `_title_clause` splits at the first textual dash at `traj_status.py:540`, so quoted titles containing `" - "` truncate incorrectly. Graph text is fixed at 10px/8.5px at `gen_trajectory.py:318`.  
Failure scenario: a WI title containing an internal dash loses its meaningful suffix, while dense graphs remain technically rendered but illegible at normal responsive widths.  
Suggested fix: parse the actual title delimiter structurally and add render-matrix legibility checks before choosing graph font sizes.

## Adjacent findings disposition

All banked findings were examined:

- **Confirmed:** unresolved LLR-015/LLR-172 local anchors; IF-117’s four advisories; stale CMP references; `_title_clause` truncation; graph font legibility; derived-label residue in PROCESS/skill/docstrings; OI-37’s missing follow-up rows; IF-103’s obsolete one-shot framing; absent LF-normalization assertion; downstream launcher selection; existential `Contracts:` validation; LLR-168/TC-162 audit omission; and stale CMP notes in IF-118–120.
- **Partially confirmed:** the smoke volatility concern is real, but the banked 1,214/1,216 membership numbers are no longer current; HEAD records 1,232/1,240 and 57.0/60 seconds.
- **Confirmed as fact, refuted as a defect:** `_apply_flips` currently performs no status writes. Its refusal is deliberate fail-closed behavior pending an owner policy, not a silently ineffective promised mutation.

I could not rerun the suite: the requested `.venv/Scripts/python.exe` points to a missing Python 3.11 installation, and the only available interpreter is Python 3.8. Findings above come from source tracing, Git diffs/blobs, and existing test semantics.

## The three claims I tried hardest to refute and could not

1. **The signing count and completeness:** commit `2d51f140` contains exactly 243 spine flips—18 SN, 70 SR, 107 LLR, 48 TC—plus 11 frame-row flips. No Drafted or Modified value survived in the five specified registries at that commit. At HEAD, only WI-472’s three deliberately Drafted rows survive; `Modified` does not.

2. **The initial seed’s byte identity:** all seven files under `docs/archive/last_approved/` were byte-for-byte identical to their live counterparts in the signing commit, including the recorded LLR-172 wording correction. The defect is the later unguarded refresh path, not the original seed.

3. **The Implements-harvester coverage number:** WI-486’s reported 1/161 reproduced at its commit. WI-472 subsequently added LLR-180, so the honest HEAD number is now 1/162, with LLR-040 still the sole literal declaration.
