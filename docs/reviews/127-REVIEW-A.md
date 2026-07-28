# 127-REVIEW-A

**VERDICT: CHANGES-REQUESTED — 8 findings: 3 BLOCKER, 4 MAJOR, 1 MINOR.**

Review scope included commits `45022e8..ffa7377` and the final working tree. The latter contains uncommitted WI-336 changes in seven tracked files plus `tests/test_advisory_during_window.py`. I did not modify, stage, or commit repository files; mutation testing used a temporary copy.

## Claim verification

| # | Result | Verification |
|---|---|---|
| 1. Windows CPU cap and shared named job | **REFUTED** | The Windows mechanism is real: `JOB_OBJECT_CPU_RATE_CONTROL_HARD_CAP = 0x4` and `CpuRate = percent * 100` are correct per [Microsoft’s API definition](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_cpu_rate_control_information). The conflict fallback also genuinely caps its private job: the live-process test passed after emitting “shared job owned by another process tree… capped at 50% ON ITS OWN.” But that fallback explicitly destroys the promised shared ceiling. Windows only permits assignment when the existing-job hierarchy is compatible; an independently hosted process tree cannot make the same named job its child ([AssignProcessToJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject), [nested jobs](https://learn.microsoft.com/en-us/windows/win32/procthread/nested-jobs)). The unconditional assertions at `conftest.py:7-8`, `conftest.py:21-25`, `docs/status.md:60-64`, `docs/log.md:15983-15989`, and the WI-335 Deliverable are false. The generic exception path is explicitly uncapped, and POSIX merely calls `os.nice(5)` at `conftest.py:193-194`, which is not a CPU cap. |
| 2. “Mutation-proven” CPU guards | **CONFIRMED**, with a material coverage gap | In a temporary repository copy I performed all four named mutations. `HARD_CAP 0x4→0x2` failed the live OS-query test; replacing `_bound_windows(percent)` with `pass` failed the live OS-query test; default `50→90` failed the default-pin test; removing `@pytest.hookimpl(optionalhook=True)` failed the no-xdist subprocess test with `PluginValidationError`. The previously vacuous subprocess guard now loads the root conftest and is not vacuous. Baseline: `5 passed`. However, no guard proves the advertised cross-run shared ceiling, and `tests/test_cpu_cap.py:183-203` accepts either the shared or private job while claiming to check both. |
| 3. WI-333 latent versus live `F402` hazard | **CONFIRMED** | I parsed `git show 45022e8:tests/test_gen_trajectory.py`. It contains exactly 13 `for label, html in ...` loops. Their body ranges begin at lines 2045, 2103, 2153, 2275, 2310, 2647, 3543, 3602, 3750, 3797, 3852, 3914, and 4005. An AST traversal found zero `html.*` attribute calls inside those bodies. The shadowing was latent, not a live bug. |
| 4. WI-334 duplicate characterization | **REFUTED** | At pre-WI-334 commit `1b65c4d`, the default checker reported 18 maximal unallowed findings, not 86. Reconstructing the claimed 86 from the census transition produced only **34 CLI-preamble cases**, versus **50 other non-CLI fingerprint drifts**, one new cross-module `_git` duplicate, and the one extracted intra-module block. Thus CLI preambles were not “MOST.” Current census has 164 entries, all allowed, and the current checker reports zero, but the premise used to justify those sanctions is false. `docs/dupes-allow:63` says 69 fingerprints while `docs/dupes-allow:70` says 86 reported blocks. |
| 5. Re-attestation | **CONFIRMED with scope qualification** | Cell-level CSV comparison found exactly 59 SR + 57 LLR + 24 TC = **140** `Modified→Verified` changes, with no other registry-cell changes. The new brief contains 59 `## SR-` sections; the older brief contains 15. A literal assertion that the entire commit changed only Status cells would be false: `git show --stat 98141a5` reports 152 files, 2,300 insertions, and 213 deletions because the brief and derived artifacts were also regenerated. The status-only claim is true only for the three source registry CSVs. |
| 6a. Worker counts | **CONFIRMED** | With the root hook disabled, the repository run created `12/12` workers. The same xdist probe outside the repository/root conftest created `24/24`. |
| 6b. Ruff `20 → 0` | **CONFIRMED** | At `1b65c4d`, Ruff reported exactly 20 errors: 13 `F402`, 2 `F821`, and 5 `F401`. Current scoped source reports `All checks passed`. |
| 6c. Duplicate checker `86 blocks → 0` | **REFUTED** | Current zero is confirmed. The historical default checker reported 18 maximal unallowed findings. “86” is a reconstructed census-change accounting, not the checker’s reported before-count, and its published category breakdown is false as described above. |
| 6d. `test_gen_trajectory.py` total | **UNVERIFIABLE** | Collection confirms exactly 151 tests. A serial run did not complete within a five-minute targeted-review window, so I do not certify the claim that all 151 passed. |
| 6e. Full-suite totals | **UNVERIFIABLE** | I did not rerun the approximately eleven-minute full suite. The quoted 1,592/1,595/1,596-style totals remain historical assertions, not independently verified results in this review. |
| 6f. CPU/process and timing measurements | **UNVERIFIABLE** | The quoted process peaks, burner percentages, and 20.4/20.7-second wall times were not independently reproduced. Current targeted CPU tests pass, but that does not validate those historical measurements. |

## Findings

### BLOCKER 1 — The central “one shared 50% ceiling” claim is false

The implementation has three materially different outcomes:

1. Compatible Windows process trees join the named job and share its ceiling.
2. A foreign/incompatible process tree falls back to a private job and receives its **own** 50% ceiling.
3. API failure falls through to an explicitly uncapped warning.

The code acknowledges outcome 2 at `conftest.py:162-180`, but the docstring still says every concurrent run shares one ceiling at `conftest.py:7-8` and `conftest.py:21-25`. The same false unconditional promise appears in `docs/status.md:60-64`, `docs/log.md:15983-15989`, the archived WI-335 spec, and the WI-335 Deliverable at `docs/requirements/work-items.csv:334`.

This is not theoretical. The live review process hit the foreign-tree path and was assigned a private job. Two such runs can consume approximately 100% together. On POSIX there is no hard cap at all.

Required correction: either implement a mechanism that actually enforces a machine-wide shared ceiling across foreign process trees, or narrow every assertion to the conditions the code delivers.

### MAJOR 2 — The mutation suite cannot substantiate the advertised concurrency property

The four named mutations are genuinely caught. That part is sound.

The broader evidence claim is not. `tests/test_cpu_cap.py:183-203` succeeds when the process is in either the named job **or** an immediate private fallback, despite the comment at `tests/test_cpu_cap.py:189` saying it is “Checking both.” It checks an OR condition, not both branches. There is also no test that launches concurrent independent process trees and proves they share one CPU-rate object.

This missing guard is exactly why the false shared-ceiling documentation survived while all five tests passed.

### BLOCKER 3 — WI-334’s sanction premise and completed audit record are false

The claim that most of the 86 items were deliberate CLI preambles is numerically wrong. My reconstructed classification was:

- 34 CLI-preamble cases
- 50 other non-CLI fingerprint drifts
- 1 new cross-module `_git` duplicate
- 1 extracted intra-module duplicate

The omitted new `_git` block is between `project-trajectory/scripts/gen_trajectory.py:4524-4540` and `project-trajectory/scripts/trace.py:1021-1034`; its sanction appears at `docs/dupes-allow:244`.

The F5 ruling permits small stable duplicated helpers more broadly than CLI preambles, so this does not automatically prove all 164 sanctions are technically invalid. It does prove that the signed characterization used to justify them is false and that the required block-by-block classification was not recorded. The archived WI-334 spec’s required audit boxes remain unchecked at `docs/archive/specs/WI-334.2026-07-27.md:53-63`.

Affected false assertions include:

- `docs/dupes-allow:63`
- `docs/dupes-allow:70-89`
- `docs/log.md:16095-16115`
- `docs/requirements/work-items.csv:333`

The sanctions require a truthful census and review, not a retroactive blanket category.

### BLOCKER 4 — WI-336 does not run the promised stronger traceability check

The uncommitted WI-336 rewrite constructs its advisory list from a step table already specialized to the **current** gate:

- `steps()` adds `--require-verified` only for `G3` or `all`: `project-trajectory/scripts/check.py:434-449`.
- `main()` calls `steps(..., gate, ...)` before deriving advisory steps: `project-trajectory/scripts/check.py:1116-1132`.

At G2, traceability is already a gating step, so it is excluded from advisory execution—and its current-gate command lacks `--require-verified`. At G1 it may be advisory, but it is still the G1 form without `--require-verified`. The promised stronger traceability variant therefore runs in neither case.

The new test entrenches the defect: `tests/test_advisory_during_window.py:79-86` explicitly asserts traceability is not advisory instead of asserting that the higher-gate variant runs.

This refutes the WI-336 Deliverable at `docs/requirements/work-items.csv:335`, `docs/status.md:81`, and `docs/log.md:16132-16141`. The same construction also loses other gate-dependent stronger command variants.

### MAJOR 5 — Ordinary G1 drafting is misclassified as an attestation window

`window_open()` returns true whenever the status basis contains any Draft or Modified rows: `project-trajectory/scripts/check.py:742-763`.

But Draft SR/SN rows are normal in a genuine G0/G1 project; `derive_gate.py:19-42` explicitly treats that as ordinary early-gate state. A synthetic basis with `drafts=1 modified=0 computed=G0` and runnable G1 produces `window_open=True` and enables the higher-gate advisory list.

That directly contradicts the code comment at `check.py:753-756`, the claimed “genuine G1 projects are not nagged” behavior in `docs/status.md:85` and `docs/log.md:16147`, and the new test’s stated premise. A real attestation-window discriminator needs more evidence than the presence of drafts.

### MAJOR 6 — Advisory module coverage can grade stale data

WI-336 excludes the `tests+coverage` producer from advisory execution through `ADVISORY_EXCLUDE` at `project-trajectory/scripts/check.py:728-739`, but still adds `module-coverage`, whose input is the coverage report.

`_clear_stale_coverage_report()` only removes the old report when the current gating plan contains `tests+coverage`: `project-trajectory/scripts/check.py:959-969`. In a G1/G2 advisory run, the producer is absent while `module-coverage` remains present. A pre-existing `coverage.json` is therefore treated as current evidence; if it is absent, the advisory check merely lacks data.

My G1 probe produced exactly that plan: module coverage present, coverage producer absent, with an existing 574,232-byte `coverage.json`. This is not a current low-cost signal. It is stale or missing evidence.

### MAJOR 7 — WI-336’s byte-budget measurement is false

The working-tree record says `PROCESS_OPTIONS.md` changed by `+782`, from 164,738 to 165,520 bytes, and describes the prior state as 2,967 bytes over baseline at `docs/log.md:16173-16175` and `docs/requirements/work-items.csv:335`.

Direct measurements are:

- `HEAD:project-trajectory/PROCESS_OPTIONS.md`: 162,342 bytes
- Working tree: 165,520 bytes
- Actual scoped delta: **+3,178 bytes**
- Watched baseline: 161,771 bytes
- HEAD overage before WI-336: **+571 bytes**, not +2,967

The recorded “before” measurement came from an intermediate working state, not the commit base. As written, the signed delta is false.

### MINOR 8 — Archived work-item state was left inconsistent

The supposedly closed archived specs retain live-state assertions:

- `docs/archive/specs/WI-333.2026-07-27.md:3` says closed, while line 9 says `Status: queued`.
- `docs/archive/specs/WI-334.2026-07-27.md:3` says closed, while line 8 says `Status: queued`.
- WI-334’s Done When audit boxes at lines 53-63 remain unchecked.
- `docs/log.md:15866` displays the obsolete `specs/WI-333.md` path even though the link target is archived.

These are precisely the kind of remnants that make the documentary record disagree with the claimed lifecycle state.