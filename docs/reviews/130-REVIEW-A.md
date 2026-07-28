# 130-REVIEW-A — adversarial review of the 2026-07-28 batch

**Reviewer:** `codex` / OpenAI (non-Anthropic, per SR-084 — the builder was
Opus, so provider heterogeneity is what makes this an independent check).
**Subject:** `07c0db6..0bf010f` — 11 commits, 43 files, +3538/-337, covering
WI-326, WI-344, WI-348, WI-349, WI-352, WI-353, WI-325, WI-339 and the filing
of WI-354.

The reviewer was given the branch's calibration explicitly — that its recurring
defect is signed CLAIMS the code does not support, not broken code — and told to
mutate guards to check they can fail. It restored the worktree byte-exact.

**All seven findings held.** The disposition is recorded in `docs/log.md`.

---

VERDICT: CHANGES-REQUESTED — 7 findings (4 BLOCKER, 3 MAJOR)

Reviewed 11 commits across 43 files (`+3538/-337`).

1. **BLOCKER — WI-348 broke three generator/coordinator write paths**

   Files: `agent_common.py:1088`, `agent_common.py:1410`, `agent_dispatch.py:3041`

   Refuted claim: WI-348’s Deliverable says all 17 `Path.write_text()` sites were converted to working `open(..., newline=...)` forms.

   The new expressions omit parentheses, so Python evaluates `"run-state".open(...)`, `"iteration_index.md".open(...)`, and `"telemetry.json".open(...)` before joining the path.

   Evidence from direct calls to the real functions:

   ```text
   _write_runstate AttributeError 'str' object has no attribute 'open'
   regenerate_index AttributeError 'str' object has no attribute 'open'
   telemetry_summary AttributeError 'str' object has no attribute 'open'
   ```

   These are live paths: `_write_runstate` is called throughout both coordinators, `regenerate_index` during integration, and `telemetry_summary` at dispatcher shutdown. `ruff` still reported `All checks passed!`.

   Fix: parenthesize each path before `.open()` and add direct behavioral tests for all three functions.

2. **BLOCKER — the environment anti-drift guard still accepts an uncounted gated skip**

   File: `test_env_gates.py:289`

   Refuted claim: “a `shutil.which` result for a gated tool must never decide a skip.”

   I added a new `test_*.py` where a module helper calls `shutil.which(tool)`, another helper calls `pytest.skip()`, and the gated tool comes through a variable. The shipped guard found nothing:

   ```text
   C:\Python38\python.exe -m pytest -q \
     tests/test_env_gates.py::test_no_test_decides_a_skip_from_its_own_tool_probe

   . [100%]
   1 passed in 0.69s
   ```

   This skip would not carry `ENV_GATE_SKIP_PREFIX`, so the banner cannot predict it and the summary cannot count it—the exact BLOCKER the replacement claims to prevent.

   Fix: enforce ownership at every `pytest.skip`/`skipif` site, with narrowly allowlisted platform skips, rather than relying on same-function AST co-occurrence. Add mutation cases for helper indirection, variables, module-level probe assignments, fixtures, and subprocess failures.

3. **BLOCKER — the LF guard permits an explicit CRLF policy**

   File: `test_generated_newlines.py:104`

   Refuted claim: the AST pair “is what makes the fix stick” and guarantees generated text is LF.

   I changed the real `trace.py` report writer from `newline="\n"` to `newline="\r\n"` and ran the complete guard module:

   ```text
   C:\Python38\python.exe -m pytest -q tests/test_generated_newlines.py

   ..... [100%]
   5 passed in 0.83s
   ```

   The guard checks only that a `newline` keyword exists, not that it denotes LF. Its behavioral tests exercise only `derive_gate.py` and `gen_okf.py`, so the real `trace.py` mutation remained invisible. `io.open`, built-in `open`, `os.fdopen`, and handles opened elsewhere are also outside its modeled surface.

   Fix: validate the actual newline value as LF, cover all text-writing APIs, and behavior-test every generator family or centralize artifact writes behind one tested primitive.

4. **BLOCKER — the shipped pre-commit hook forces a downstream migration**

   Files: `pre-commit:177`, `stack.ini.template:224`, `work-items.csv:324`

   Refuted claim: the live step “costs … exactly nothing and forces no migration.”

   A fresh scaffold with the new stack entry did pass:

   ```text
   PASS ratify-fresh
   trace: ratify-check — no brief ... nothing to gate
   ```

   I then removed only `[step:ratify-fresh]` to model an adopter whose project-owned `stack.ini` predates WI-325, while retaining the newly shipped hook. The hook’s exact batched command failed:

   ```text
   check: no step named 'ratify-fresh'
   exit code 1
   ```

   Thus updating the kit-owned hook without migrating `stack.ini` blocks every commit.

   Fix: make `ratify-fresh` an unconditional built-in step, conditionally include it in the hook, or document and automate the required migration. The current “no migration” claim must be removed.

5. **MAJOR — both signed WI-352 census measurements are false**

   Files: `check_trajectory.py:1335`, `work-items.csv:351`, `log.md:17044`

   Refuted claims:

   - “Run over the archive it produced 38 findings.”
   - “258 of 282” checkboxes are under a Done-when heading.

   I measured the exact landing commit `6af702c` using the shipped heading and checkbox predicates:

   ```text
   commit 6af702c archive_findings 40 zero_ticked 36 nonzero 4
   checkbox_inside_total 281 296 outside 15 specs 109
   ```

   The out-of-section cases were also identified:

   ```text
   docs/archive/specs/WI-322.2026-07-26.md   total=8 inside=0
   docs/archive/specs/working-surface-and-architecture-restructure... total=5 inside=0
   docs/specs/WI-321.md                       total=4 inside=2
   ```

   Fix: commit a reproducible census helper/test and replace the signed figures with its post-edit output. Re-evaluate the live-only design against the actual 40 archive findings.

6. **MAJOR — WI-339 does not hash every binary file exactly**

   Files: `check_vendored.py:96`, `work-items.csv:338`

   Refuted claim: “binary is hashed exactly as it is” and “a genuine binary must not be normalized into a false match.”

   The implementation classifies data as binary only when it contains NUL. I drove it with a valid binary PPM image whose single pixel is `(13,10,255)`—therefore its pixel bytes contain CRLF but no NUL:

   ```text
   nul_present False
   looks_binary False
   normalized True
   hashes_exactly False
   collides_with_changed_pixel True
   ```

   Two byte-distinct binary images therefore compare equal. The committed PNG fixture contains NUL and cannot expose this false-negative class.

   Fix: explicitly declare text/binary treatment in the manifest, or normalize only positively identified text. Add a valid no-NUL binary fixture containing CR/CRLF.

7. **MAJOR — WI-348’s implementation constraint names the wrong Python version**

   Files: `test_generated_newlines.py:25`, `log.md:17279`, `work-items.csv:347`

   Refuted claim: `Path.write_text(newline=...)` is “3.13+” and raises `TypeError` on the supported Python 3.11 floor.

   Python added the `newline` parameter to `Path.write_text` in 3.10, so it is available throughout this kit’s 3.11+ support range. The [official Python documentation](https://docs.python.org/3.11/library/pathlib.html) confirms this. The repository already says the correct version:

   ```text
   gen_okf.py:580: is Python 3.10+
   gen_arch_map.py:774: write_text(newline=) is 3.10+
   gen_trajectory.py:5097: write_text(newline=) is 3.10+
   ```

   The branch appears to have confused `Path.write_text` with `Path.read_text`, whose `newline` parameter is 3.13+.

   Fix: correct every signed claim and reconsider the mechanical two-line conversions; on the declared floor, `Path.write_text(..., newline="\n")` is valid and avoids the precedence regressions in finding 1.

Claims checked and HELD:

- The historical WI-326 measurement held at commit `893579b`: forced-closed gates reported exactly `ENVIRONMENT-GATED SKIPS: 250`. HEAD reports 256 because WI-325 later added six gated tests.
- The 8 pre-commit and 18 pre-push skip counts reproduced exactly.
- At `07c0db6`, AST found exactly 17 `Path.write_text()` calls; HEAD has zero. A broader scan found 35 current text-write `open()` calls and none lacking `newline=`.
- WI-325’s baseline-preservation tests held: 16 ratify/baseline tests passed, including the differing-baseline case.
- A fresh scaffold with no `docs/ratify/` passed `ratify-fresh` vacuously.
- WI-353’s mutation twin genuinely reproduced the broken-link defect; all six archival/rebase tests passed.
- The Done-when sibling/subheading boundary behavior held in targeted tests, despite the false census figures.
- Collection increased from 1,636 tests at `07c0db6` to 1,713 at HEAD; no collection loss was observed.
- `git diff --check 07c0db6..HEAD` is clean.
- Final worktree status is restored exactly: only the pre-existing `?? docs/pause` remains.
