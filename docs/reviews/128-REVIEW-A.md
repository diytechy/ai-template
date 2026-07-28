# 128-REVIEW-A

**VERDICT: CHANGES-REQUESTED — 6 findings: 2 BLOCKER, 2 MAJOR, 2 MINOR.**

Review scope: exactly `fd844f2..HEAD` (`a862c56`, `8df42c0`). Repository files were not changed; final status remains exactly `?? docs/pause`, with no staged or unstaged tracked diff.

The required venv launcher could not start in this sandbox because its base interpreter was inaccessible. Consequently, full-suite and timing claims are not certified. Version-independent census probes and targeted diagnostics used the available Python 3.8 interpreter and are identified below.

## Claim verification

| Claim | Result | Verification |
|---|---|---|
| Current census contains 208 blocks | **CONFIRMED** | `check_dupes.py --src project-trajectory/scripts --emit-census` produced 208 lines; `docs/dupes-allow` contains 208 non-comment entries; sorted diff was empty; ordinary checker exited 0. |
| Uniform LF and uniform CRLF each produce 208 pre-fix | **CONFIRMED** | Archived `fd844f2`, converted all 37 Python files mechanically to LF and CRLF, then ran its pre-fix checker: 208 in each case. Their fingerprints differed, as expected (`Compare-Object` reported 398 one-sided differences). |
| Post-fix LF and CRLF censuses are identical | **CONFIRMED** | Current source over all 37 files emitted 208 entries from both an LF and CRLF copy, with exact diff 0. |
| 191 of 208 already sanctioned at `1b65c4d`; 17 drift | **CONFIRMED** | Multiset intersection—not naïve set membership—between current emitted census and `git show 1b65c4d:docs/dupes-allow` was exactly 191, leaving 17 current entries. A set comparison misleadingly gives 192 because repeated identical census lines are count-sensitive. |
| 80 of 208 matched the invalid committed census | **CONFIRMED** | Multiset intersection against `fd844f2:docs/dupes-allow` was exactly 80, leaving 128 unmatched. |
| Mixed tree produced 164 blocks from 28 LF / 9 CRLF files | **UNVERIFIABLE** | `fd844f2:docs/dupes-allow` has 164 entries, but no record names the nine CRLF files. The historical mixed corpus cannot be reconstructed independently. |
| Classification distribution sums to 208 | **CONFIRMED** | Parsed every grouped census entry: 77+64+21+11+11+9+5+4+2+2+1+1 = 208; section counts match exactly. |
| Classification is a truthful per-block audit | **REFUTED** | The 64-entry `intra-module` group is a same-path catch-all and assigns one blanket rationale—“WI-280 owns it”—to semantically different blocks, including modules outside WI-280’s declared scope. See BLOCKER 2. |
| Smoke membership `449 → 453` | **CONFIRMED** | Collection on archived `a862c56` reported `449/1612`; current collection reported `453/1616`. The four-test increase is exact. |
| Smoke wall time `24.3 s vs 60 s` | **UNVERIFIABLE** | No raw timing artifact is committed. The fallback diagnostic run did not finish within 180 seconds and stopped at 95%; the unsupported interpreter prevents treating that as a refutation, but the signed 24.3-second number is not reproducible. |
| WI-337’s three guards can fail | **CONFIRMED** | Baseline: `18 passed`. In a temporary copy, replacing newline normalization with `return text` made all three named tests fail, including `test_normalization_is_what_makes_the_census_portable`. The monkeypatch test is not the only evidence; the token and CLI census tests independently red. |
| One live process is under the requested hard cap | **CONFIRMED** | `test_this_live_process_runs_under_the_hard_cap_it_asked_for` passed and queried ENABLE, HARD_CAP, and CpuRate from Windows. |
| Second independent run always gets a private ceiling | **REFUTED** | Unmodified `tests/test_cpu_cap.py` produced `5 passed, 1 failed`; the alleged second independent process reported `SHARED warned=0`. See BLOCKER 1. |
| WI-336’s three corrected guards can fail | **CONFIRMED** | Baseline: all 8 advisory tests passed. Three isolated mutations—name-level gating suppression, `drafts>0`, and removing `module-coverage` from the exclusion—each failed exactly its named test. |
| G3 `--require-verified` runs end-to-end during a real window | **CONFIRMED** | In a current temporary copy with a real derived-format G2 window, `check.py --gate G2 --tier smoke --jobs 0` ran ordinary traceability and then an advisory command containing both `--require-verified` and `--strict-schema`. |
| Draft-window discriminator is sound | **REFUTED** | Direct probes returned `True` for an early `1=G1;2=G0` project and `False` for a mature single-phase project reopened by a Draft. See MAJOR 3. |
| Excluding advisory `module-coverage` is correct | **CONFIRMED** | `module-coverage` consumes `coverage.json`; `_clear_stale_coverage_report()` only clears it when the gating plan runs `tests+coverage` (`check.py:1075-1087`). Excluding the consumer with the producer avoids grading stale evidence. |
| “67 tracked files” were safely normalized | **UNVERIFIABLE** | No filename manifest or before-state exists. The operation is invisible to Git by design. |
| The 67-file operation changed no committed blobs | **CONFIRMED** | `a862c56` changes 13 paths substantively; normalized parent/current blob comparison found zero line-ending-only blob changes. Thus no 67-file rewrite landed, but the historical count and refusal checks cannot be reconstructed. |
| Full suite `1609 passed / 7 skipped` | **UNVERIFIABLE** | Collection supports a 1,616-test total, but the mandated venv could not run and no full suite was completed independently. |

## Findings

### BLOCKER 1 — The corrected CPU-cap rule is still false, and its new guard fails on the unmodified branch

The new claim says a second run from a different process tree necessarily gets a private ceiling (`conftest.py:12-18`, `docs/status.md:63-71`, `docs/log.md:16316-16325`). Windows’ rule does not say that.

The restriction applies when the process is already in a job: the target must be empty or compatible with its existing nested hierarchy. An unjobbed process may join a populated named job, while processes sharing a compatible parent job can also join the same child job. Microsoft explicitly documents both the conditional assignment rule and peer processes in nested job hierarchies: [AssignProcessToJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject), [Nested Jobs](https://learn.microsoft.com/en-us/windows/win32/procthread/nested-jobs).

The test does not launch independent trees. Both the holder and “second” probe are direct children of the same pytest process (`tests/test_cpu_cap.py:287-302`). On this machine:

```text
first:  SHARED
child:  CHILD SHARED
second: SHARED warned=0
```

Thus the unmodified test fails at `tests/test_cpu_cap.py:303`. This is ambient-job-dependent and can behave differently under a shell, CI runner, xdist, or another host. It also checks membership but never queries the purported second ceiling’s rate.

False records remain at:

- `conftest.py:12-18`
- `conftest.py:175-203`
- `docs/status.md:63-71`
- `docs/log.md:15993-16008`
- `docs/log.md:16316-16342`
- `docs/archive/specs/WI-335.2026-07-27.md:43-55`
- `docs/archive/specs/WI-335.2026-07-27.md:90-92`
- WI-335 and WI-338 Deliverables in `docs/requirements/work-items.csv:334-337`

Required correction: describe the private fallback as conditional on an incompatible existing job hierarchy, not process-tree identity. Build a topology-controlled test that creates genuinely distinct compatible and incompatible job hierarchies, queries rate control in each, and does not derive its expected result from the ambient launcher.

### BLOCKER 2 — The “0 unclassified” census audit uses `intra-module` as a blanket catch-all

The arithmetic is exact, but the classification is not the per-block acceptance audit claimed at `docs/dupes-allow:104-135` and `docs/log.md:16344-16370`.

Every same-file pair is placed under `intra-module`, then all 64 are declared “not F5 at all” and debt owned by WI-280 (`docs/dupes-allow:331-336`). That classification can be derived from the two path strings without reading the block. It conflates:

- small declared-file parsing repetition in `check_docs.py:405-410` and `check_docs.py:685-690`;
- two similar source walkers in `gen_arch_map.py:300-307` and `gen_arch_map.py:321-327`;
- parallel OKF tier-row construction in `gen_okf.py:335-370`;
- large dispatcher/renderer duplication that plausibly is decomposition debt.

WI-280’s row (`docs/requirements/work-items.csv:279`) names session/train/route decomposition, `gen_trajectory`, and `bootstrap`; it does not establish ownership of every same-module duplicate. The repo’s own WI-304 correction (`work-items.csv:303`) explicitly says that treating ordinary intra-module boilerplate as WI-280 debt was wrong and extracted it instead.

This recreates the failure 127-REVIEW-A identified: a broad class makes the count reach zero without establishing why each sanction is acceptable.

Required correction: triage the 64 entries by semantic block and disposition—extract, deliberate local parallel structure, or a specifically scoped debt WI. A same-path predicate is useful metadata, not an acceptance rationale.

### MAJOR 3 — `window_open()` misclassifies realistic phased repositories in both directions

The discriminator is:

```python
levels = re.findall(r"=(G\d)", per_phase.group(1))
return bool(levels) and max(levels) > computed.group(1)
```

at `project-trajectory/scripts/check.py:804-809`.

It gets at least two realistic cases wrong:

- `computed=G0 per-phase=1=G1;2=G0` returns `True`. Phase 1 has only reached G1 and phase 2 is being drafted; this is still an early project that has never earned the G2/G3 advisory bar.
- `computed=G0 per-phase=1=G0` returns `False` even when a previously mature single-phase repository adds a new Draft within that phase. The Draft erases the phase’s previous G3 level from the current breakdown, so no phase remains “above” computed.

The tests cover only `1=G0` and `1=G3;…;4=G0` (`tests/test_advisory_during_window.py:29-45`), omitting both boundary cases. Consequently, `docs/status.md:95-97` overstates what the heuristic separates.

Required correction: derive the window from persistent transition/attestation evidence, not only the current minimum. At minimum, require a G2/G3 phase to avoid the false positive and explicitly narrow the claim for single-phase/same-phase Drafts; a complete fix needs prior maturity or an explicit window marker.

### MAJOR 4 — Several signed measurements depend on discarded working-tree state

The following exact claims cannot be independently reconstructed:

- the 28-LF/9-CRLF mixture and resulting 164 blocks (`docs/dupes-allow:65-72`);
- the 67 normalized files and per-file byte-identity refusal (`docs/archive/specs/WI-337.2026-07-27.md:95-100`);
- the classifier’s four passes (`docs/log.md:16344-16347`);
- the 24.3-second smoke measurement (`docs/stack.ini:52-57`, `docs/log.md:16439-16448`).

The committed invalid census corroborates 164 entries, and Git proves no 67-file rewrite landed, but neither fact reproduces the stated input state or procedure.

Required correction: narrow these to historical, non-reproducible observations or attach the evidence needed to rerun them—exact filename manifests, commands, before/after hashes, and raw timing output. Future transient-tree measurements should not be signed without that record.

### MINOR 5 — `check.py --list` hides the advisory plan it will execute

`main()` computes `advisory` at `check.py:1232-1237`, but `--list` prints only `plan` and returns at `check.py:1239-1247`.

With a real open G2 window, `--list` showed only the weaker G2 traceability command and no `--require-verified`; running the same invocation executed the hidden G3 advisory command. The option’s help says “print the plan,” so this is materially incomplete plan output.

Required correction: list the advisory tier separately, with its non-gating label and exact commands.

### MINOR 6 — The archived WI-333 record became stale when WI-336 closed

`docs/archive/specs/WI-333.2026-07-27.md:5-7` still says the advisory-step process question “is still open,” and its Done-when boxes remain unchecked at lines 65-80. WI-336 is now done and `docs/status.md:87-99` says the ruling is implemented.

Required correction: add a dated closure note pointing to WI-336 and reconcile the affected boxes without rewriting the historical observation.