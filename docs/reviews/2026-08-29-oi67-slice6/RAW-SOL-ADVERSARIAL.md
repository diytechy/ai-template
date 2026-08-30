1. [CRITICAL] `check_trajectory.py:_declaration_sites` — one malformed body disables the entire contract-body gate. `_contract_bodies` correctly raises `ContractsGrammarError`, but `_declaration_sites` catches it and returns `(None, [])`; `contract_body_findings` then returns no findings.

   Reproduction plant: changed `Contract IF-069: ...` to an empty `Contract IF-069:` in `check_coverage.py`.

   Result: `check_trajectory --root . --strict` exited **0**. The same path lets whitespace-only bodies suppress the whole gate.

   Concrete change: never translate a grammar error into “no scan surface.” Return the grammar failure as a strict finding and continue scanning unaffected sources where possible. Add an end-to-end test asserting an empty body exits 1.

2. [MAJOR] `check_trajectory.py:_external_body_findings` — an external-owned seam whose entire far side is external owes no body at all. The function explicitly returns clean when `far` is empty after external endpoints are filtered.

   Reproduction plant: changed `IF-032` to `owner = "external:git"`, `consumers = ["external:y"]`, and removed its declaration/body from `check_privacy.py`.

   Result: `check_trajectory --root . --strict` exited **0**.

   A preliminary plant that changed only the consumer exited 1 because the old `check_privacy` declaration became stray; after removing that declaration, the bodyless row passed.

   Concrete change: reject external→external rows as having no in-tree statement site, or define an explicit document owner. Do not treat “no kit far side” as satisfied.

3. [MAJOR] `check.py:638-656` — the ordinary harness is not currently running the armed mode. `traj_cmd` gains `--strict` only at `DevStg-Impl`; this tree derives `DevStg-LLReqs`.

   Reproduction:

   - `docs/stage` reports `stage = DevStg-LLReqs`.
   - `check_trajectory --root . --strict` exited 0.
   - Inspection of the constructed command showed no `--strict` at the current rung.

   An adopter can also make the arm vacuous through `[checks] interfaces_check = false`, `[arch-map] mode = files`, or an absent scan root. Thus “armed” means only a direct strict invocation or a future Impl-stage harness, not this build’s normal plan.

   Concrete change: decide explicitly whether definition integrity belongs at every adopted rung. If yes, make it an always-strict harness step independent of the trajectory maturity ladder and give it a dedicated opt-out rather than sharing the broad interface switch.

4. [MAJOR] `docs/requirements/interfaces.toml:79-88` and `docs/enforcement-audit.md:45` — live adopter-facing prose contradicts decision 6.2 and the executable gate. Both say an owner declaring nothing is a strict finding; the code leaves it warn-only.

   Reproduction plant: renamed both `Contracts:` and `Contract IF-069:` so the owner declared and stated nothing.

   Result:

   - `check_trajectory --strict` emitted the owner-exact **WARN**.
   - Exit code remained **0**.
   - `gen_arch_map --contracts-doc ... --check` exited 1 because the reference became stale.
   - Neither `PROJECT_STATE.html` nor `docs/ratify/CURRENT.md` exposes the stated-body debt/count.

   Concrete change: either promote the dodge, or correct all live prose to say it is warn-only. Add the stated/unstated count to the approval brief/dashboard if visibility is the justification for not gating it.

5. [MAJOR] the “one CSV reader” claim is false. Live raw CSV readers remain outside `kitlib.spine`:

   - `scripts/agent_route.py:236` — `csv.reader(text.splitlines())`
   - `scripts/intake.py:1600` — `csv.reader(fh)` on a legacy live carrier
   - `scripts/check_flows.py:80` — raw `csv.DictReader(f)` in the residual `col` helper

   Other direct `csv.reader` uses include the intentionally lower-level structural/migration paths, but the three above disprove “every kit reader goes through it.”

   Reproduction: `rg -n 'csv\.(reader|DictReader)' project-trajectory/scripts -g '*.py'`, followed by reading each caller.

   Concrete change: route the live legacy-carrier readers through `kitlib.spine`, and delete the unused `check_flows.col` helper instead of leaving a second idiom available.

6. [MAJOR] `kitlib/spine.py:107-125` — a blank separator after the leading comment block corrupts the header. `csv_body` removes comment lines but preserves the immediately following blank line, so `DictReader` takes that blank line as the header.

   Reproduction input:

   ```text
   # c

   a,b
   1,2
   ```

   Result: `csv_rows` returned `[{None: ['a', 'b']}, {None: ['1', '2']}]`.

   Other reader probes:

   - quoted `"#inside"`: preserved correctly.
   - first-cell `#data`: preserved correctly.
   - BOM: handled correctly.
   - CRLF: handled correctly.
   - middle `#` line: retained as data.
   - empty/header-only: returned no rows.
   - comment ending in `\`: handled correctly.

   Concrete change: define whether blank lines belong to the leading metadata preamble. If so, skip blank lines between that preamble and the CSV header and test it.

7. [MAJOR] `trace.py:interface_findings` detects retired cells by non-empty value, not by schema-key presence. Empty and nested retired keys survive.

   Reproductions:

   - Planted `provider = ""` on `IF-001`: zero retired-cell hits.
   - Planted `[interface.IF-002.legacy] contract = "hidden retired definition"`: zero retired-cell hits.
   - Both `trace --strict` invocations remained at the baseline exit 1 for unrelated findings, with no new retired-cell report.

   A `Contract` token inside `notes` correctly should not count—it is prose, not a key.

   Concrete change: validate each interface table’s allowed top-level key set, reporting retired keys even when empty, and reject nested subtables unless explicitly schema-defined.

8. [MAJOR] `project-trajectory/EXAMPLE.md:396-518` — live shipped example prose still teaches the retired interface shape with `provider`, `contract`, and `req_refs` fields across multiple rows.

   Reproduction: whole-tree retired-cell grep found those live examples, alongside historical records and intentional migration tests.

   Classification:

   - `EXAMPLE.md` hits: live citation rot and adopter-facing defect.
   - `RESYNC_PACK.md` older entries: historical migration records, generally valid.
   - tests containing old shapes: mostly intentional migration/negative fixtures.
   - logs, reviews, plans, archives and open-item histories: records, not findings.
   - current `PROCESS.md`, template header and machinery reference references: deliberate warnings about retirement.

   Concrete change: rewrite the live example to the owner/far-side/channel/data shape with `Contracts:`/`Contract IF-###:` bodies, and add it to the dogfood/live-shape rot test.

9. [MINOR] `gen_okf.py:_doc_title_and_summary` drops content appearing after `-->` on the same line.

   Reproduction input:

   ```markdown
   <!-- hidden --> # Real
   Para
   ```

   Result: `("", "Para")`; `# Real` was discarded.

   Other probes:

   - two leading comments: `("Title", "Summary")`.
   - comment after a leading blank: `("Title", "Summary")`.
   - comment containing a fake heading: correctly ignored.
   - comment-only or unclosed comment: returned empty title/summary.

   Concrete change: after locating `-->`, feed its suffix back through the normal line parser instead of discarding the entire line.

10. [MINOR] WI-533 record — “sixteen reason cells trimmed by this slice” does not reproduce from the named slice boundary.

    Reproduction: `git diff 87c1fc38^ 8599f2b0 -- docs/if-tc-coverage-allow` was empty; the file’s last modifying commit is `816090cd` from slice 4. Non-comment entry counts were 139 both before and after WI-533.

    Concrete change: attribute the trimming to the commit that actually contains it, or provide the correct base revision and driven count.

11. [MINOR] build baseline — the requested strict trace baseline is red, not green.

    Reproduction:

    - `trace.py --root . --strict` → exit **1**, including `LLR-197` provenance and two `SR-181` orphan findings.
    - `check_trajectory.py --root . --strict` → exit **0**.

    The fragment only claims `trace --strict-integrity` was clean, so this is chiefly an incomplete build-health record rather than a regression caused by the new gate.

Other reproductions and checks:

- Deleting the entire `Contract IF-069:` opener correctly made `check_trajectory --strict` exit 1.
- Relevant targeted tests passed: `2 passed, 110 deselected`; migration tests: `3 passed, 33 deselected`.
- `structure_findings` with sixteen comment lines, header on line 17 and malformed row on line 18 correctly reported line 18.
- Migration tests confirm `contract` is retained and re-reported on the second pass.
- Counts reproduced: 154 interface rows; reference says 74/154/154; line ratchets 4480→4638, 5898→5912, `agent_common` +1, `spine.py` 639→676; `PROCESS.md` blobs 87,651→87,782 bytes; smoke stamp 1377→1390.
- The three external bodies otherwise match their adjacent mechanisms. `check_privacy` uses the stated git commands with filesystem fallback for repo sweeps; `check_vendored` normalizes text line endings and treats fetch failures as unverified; `agent_session` handles stdin/argv transport, JSON result extraction and Codex last-message files.
- The attempted `check_privacy` no-git CLI probe initially used invalid arguments (`--repo . --all`) and exited 2; it establishes nothing and was not used as evidence.
- An attempted in-tree malformed performance-budget row plant failed patch-context verification before changing any bytes; the equivalent sixteen-line-header test was then performed in a temporary file.
- Actual plants made: empty IF-069 body; deleted IF-069 body opener; external-only IF-032 far side; external-only IF-032 with old body removed; undeclared IF-069 dodge; empty `provider`; nested `contract`. Every planted file was restored with `git checkout -- <path>`.
- Final `git diff --exit-code` returned 0; the worktree is byte-clean.

VERDICT: CHANGES-REQUESTED findings=11