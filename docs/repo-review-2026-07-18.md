# Deep Repository Review — 2026-07-18

**Review target:** `cfd24c4` on `dualplan-routing-fix`  
**Scope:** the full repository, including source, tests, requirements registries,
generated views, CI, configuration, dependency metadata, rendered dashboard, and
Git history. Deliberately excluded from content review: `docs/log.md`,
`docs/archive/**`, and `docs/iteration/**`. Generated OKF/dashboard material was
assessed through its generators, freshness gates, and rendered output rather
than line-by-line as hand-authored prose.

## 0. Unfixed items and why

The first report snapshot was committed as `a93a021`; the table below records
what remains after the subsequent confident-fix pass.

| Finding | Still unfixed because | Required next move |
|---|---|---|
| **H-02 — orchestration complexity** | A safe decomposition changes the highest-risk state machines and compatibility surface. Extracting helpers without a state model would merely move complexity around. | File and execute a dedicated high-risk architecture WI: characterize transitions, add a no-new-C901 ratchet, then separate pure decisions from Git/session/integration effects. |
| **H-03 — no license** | OI-4/WI-097 correctly blocks on the owner's public/private and licensing intent; choosing legal terms is not an engineering default. | Owner decision, then add the selected license/notices and README terms. |
| **M-04 — 390 px dashboard clipping** | The defect is certain, but fit-to-width versus an explicit scroll affordance is a UX choice requiring a rendered iteration. The render-critique skill forbids redesigning inline during critique. | **WI-219 filed queued** with SR-052/SR-054 links; fix in the generator and rerun all 36 screenshots. |
| **M-05 — non-atomic requirements** | Splitting ratified SRs changes the traceability spine, evidence links, and attestation history. A mechanical prose split would be dishonest. | Planned spine migration with supersession/evidence preservation. |
| **M-06 — run-menu shell arguments** | The intended compatibility contract is ambiguous, and POSIX-shell versus `cmd.exe` quoting makes an unreviewed patch unsafe. | Decide shell-fragment versus data-argument semantics, then implement explicit argv/placeholder behavior with cross-platform tests. |
| **M-07 — 48 live orphan warnings** | Most warnings are retained reviews/spec evidence. Deleting or globally ignoring them would hide useful history; indexing all of them would bloat navigation. | Define evidence-document taxonomy/indexes and ratchet only newly introduced live orphans. |
| **L-03 — Git identity inconsistency** | Correcting old authors requires disruptive history rewriting; privacy checking is intentionally off. | Standardize future Git identity; rewrite history only as an explicit release decision. |
| **L-04 — large test modules** | Splitting tests before production boundaries stabilize would increase fixture/patch duplication. | Split alongside the H-02 production decomposition by behavior boundary. |

Confident fixes completed in this pass: H-01, M-01, M-02, M-03, L-01, and
L-02. The mobile issue was converted into WI-219 rather than silently left as
prose-only debt.

## 1. Executive summary

This is a serious, unusually well-instrumented process-engineering repository.
Its strongest feature is not any individual script; it is the mutually
reinforcing verification system around the scripts: strict traceability,
generated-view freshness, architectural seam checks, cross-platform tests,
coverage enforcement, duplicate detection, privacy checks, and an explicit
gate model. The baseline G3 run passed all 16 checks with 1,030 tests passing,
34 skipped, and 90.98% statement coverage. *(Validity re-check, §5: the 34
skips are a session-PATH artifact — no POSIX `sh` visible, so the
shell-dependent tests skipped; the canonical environment runs the same
collection as 1,061 passed / 3 skipped. Same tests, same green.)* Strict
traceability found
zero orphans or integrity findings across 25 stakeholder needs, 66 system
requirements, 76 low-level requirements, 76 test cases, 65 interfaces, and five
components. No committed secret, dependency vulnerability, obvious unsafe
deserialization, dynamic execution, or unbounded external input vulnerability
was found.

The blunt assessment is that the repository's verification discipline now
exceeds the maintainability of the implementation it protects. Fifty functions
fail Ruff's default cyclomatic-complexity threshold. The nominal coordinator
split in WI-218 reduced physical concentration but left a 2,125-line dispatch
module with a 698-line, complexity-84 function and a compatibility-heavy entry
module. Several registries and module descriptions still state the retired
serial architecture. The requirements spine is mechanically consistent but
some individual requirements have become multi-thousand-character mini-specs,
which is the opposite of atomic, reviewable requirements. These are not cosmetic
complaints: the code is safe to change largely because the tests are excellent,
not because the core control flow is easy to understand.

The most urgent immediately-fixable issue is CI supply-chain hygiene. Every
GitHub Action is referenced by a mutable major tag and no workflow declares
least-privilege token permissions. The most urgent non-code issue is the absent
license: a reusable kit with no license grants outside users no clear right to
copy, modify, or redistribute it. That decision is already blocked on owner
intent and must not be guessed.

### Overall assessment by area

| Area | Assessment | Bottom line |
|---|---|---|
| Code quality | **Needs focused refactoring** | Idiomatic stdlib Python and good naming, but extreme orchestration functions dominate cognitive load. |
| Architecture | **Sound model, overgrown implementation** | The registry/generator/checker layering is coherent; coordinator boundaries remain leaky after the split. |
| Documentation/prose | **Strong but drifting at edges** | Excellent rationale and operational detail; some authoritative contracts contradict current behavior and many docs are undiscoverable. |
| Security/robustness | **Good runtime posture, weak CI pinning** | Fail-closed checks and explicit trust boundaries are strong; Action references and shell argument composition need attention. |
| Performance | **Generally fast except doc staleness** | Core generators complete in about one second; `check_docs --stale` took 150.1 seconds because of N+1 Git subprocesses. |
| Testing/reliability | **Excellent** | Broad unit/integration coverage, cross-platform CI, 90.98% coverage, and green strict gates. |
| Dependencies/config | **Lean** | Product scripts are stdlib-only; dev dependencies are small and current enough, but reproducibility wording overstates compatible-range pins. |
| Standards/Git | **Strong with minor inconsistency** | WI-oriented history and hooks are useful; author identity and commit-subject conventions are not fully uniform. |
| Legal/accessibility/i18n | **Legal blocker; good a11y foundation** | No license; dashboard has good semantic/theme foundations but a reproducible 390 px clipping defect. i18n is not designed in. |

## 2. Prioritized findings

### Critical

No critical finding was identified. That is not a claim that the system is
perfect; it means no observed issue justifies emergency remediation ahead of
normal review and testing.

### High

#### H-01 — GitHub Actions are mutable and token permissions are implicit

**Location:** `.github/workflows/test.yml:28-30,56-57`,
`.github/workflows/canary.yml:19-20`, and
`project-trajectory/ci/check.yml:34-36,81`

```yaml
- uses: actions/checkout@v4
- uses: actions/setup-python@v5
...
uses: actions/upload-artifact@v4
```

**Problem:** every third-party workflow action is selected by a mutable major
tag. None of the workflows declares a top-level `permissions` block, so the
effective `GITHUB_TOKEN` authority depends on repository/org defaults. The
reference workflow also teaches downstream adopters this weaker pattern.

**Why it matters:** CI executes on pull-request and release paths and is part of
this repository's claimed enforcement floor. A mutable tag is not an immutable
supply-chain boundary; implicit token rights make the blast radius dependent on
external settings. GitHub's own hardening guidance states that a full commit SHA
is the only immutable action reference. The current action majors are also
behind the current official releases: [checkout 6.0.2](https://github.com/actions/checkout/releases/tag/v6.0.2),
[setup-python 6.2.0](https://github.com/actions/setup-python/releases/tag/v6.2.0),
and [upload-artifact 7.0.1](https://github.com/actions/upload-artifact/releases/tag/v7.0.1).

**Suggested improvement:** add `permissions: { contents: read }` at workflow
scope and pin each official Action to its verified full commit SHA, retaining a
version comment for update tooling and human readability. Add a lightweight
test that prevents the scaffolded reference workflow from regressing to tags.
See [GitHub's secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use).

**Disposition:** fixed. Meta and downstream-reference workflows now declare
`contents: read`, use verified full SHAs for checkout 6.0.2, setup-python 6.2.0,
and upload-artifact 7.0.1, and a scaffold test guards both properties.

#### H-02 — Core orchestration complexity is beyond maintainable review scale

**Location:** `project-trajectory/scripts/agent_dispatch.py:1428`, plus
`agent_loop.py`, `trace.py`, `bootstrap.py`, `gen_trajectory.py`, and related
orchestrators.

```python
def dispatch_run(args, root):
    # 698 physical lines; cyclomatic complexity 84
    # (the worker engine path is the module-level _ENGINE sibling, not a
    #  parameter — corrected in the §5 validity re-check)
```

**Problem:** an explicit Ruff C901 census reports **50** functions over the
default complexity limit of 10 at the review target (**51 after this review's
own M-01 fix** — the batched `git_commit_lookup` itself exceeds the limit,
which sharpens the ratchet recommendation below; §5). The worst are
`dispatch_run` (84), `trace.analyze` (50), `bootstrap.main` (41), and several
functions at 28-29. Source files reach 3,016 lines (`gen_trajectory.py`),
2,863 (`agent_loop.py`), 2,125 (`agent_dispatch.py`), 2,002 (`trace.py`), and
1,863 (`bootstrap.py`) by `wc -l` — the counts this repository's registries
and logs use (this report originally quoted unlabeled non-blank counts; §5).
WI-218 created sibling modules, but `agent_loop` still re-exports a large public
surface and `agent_dispatch` now contains the dominant state machine.

**Why it matters:** reviewers cannot reliably hold a 698-line state machine in
working memory. Branch-specific cleanup, rollback, lock ownership, subprocess
control, registry mutation, and user-facing outcomes are interleaved. High test
coverage reduces regression probability but does not make the code locally
comprehensible or the failure modes obvious. No complexity ratchet prevents
further growth.

**Suggested improvement:** treat this as an architectural workstream, not a
drive-by extraction. First add characterization tests around dispatch state
transitions and a report-only complexity baseline that fails only on new debt.
Then split pure planning/state-transition logic from Git/worktree effects,
session execution, integration, and presentation. Replace flat, loosely shaped
dictionaries at module boundaries with small typed records (`dataclass` or
`NamedTuple`, compatible with Python 3.8). Reduce compatibility re-exports only
through a documented deprecation path.

#### H-03 — The repository has no license

**Location:** repository root (no `LICENSE` or equivalent); `docs/open-items.md`
OI-4 / deferred WI-097.

**Problem:** the project presents itself as a reusable kit intended to be copied
into downstream repositories but supplies no license and no public/private
distribution declaration.

**Why it matters:** absent a license, external users generally have no explicit
permission to copy, modify, or redistribute the work. That directly undermines
the stated adoption goal and makes dependency or marketplace distribution
legally ambiguous.

**Suggested improvement:** the owner must first decide whether this is private,
source-available, or open source. Then add the corresponding license, copyright
notice, contribution terms, and a short README licensing section. Do not select
a license automatically; this is an ownership and policy decision, not a coding
default.

### Medium

#### M-01 — Documentation staleness checking has an N+1 Git-process design

**Location:** `project-trajectory/scripts/check_docs.py:488-516`

```python
def lookup(path):
    ...
    out = subprocess.run(
        ["git", "-C", str(root), "log", "-1", "--format=%ct", "--", str(path)],
        ...,
    )
```

**Problem:** `git_commit_lookup` memoizes values but still launches one `git log`
process for every unique document and linked non-document path. On this review's
baseline, `doc-navigability` consumed **150.1 seconds** while every generator
and registry check completed in roughly one second or less.

**Why it matters:** this check is part of the per-commit bar. It consumed about
one-third of the full 455-second parallel G3 wall time and discourages frequent
local verification. Process startup is especially expensive on Windows, one of
the project's explicitly supported platforms.

**Suggested improvement:** obtain last-change epochs for tracked paths in one
Git history traversal, normalize repository-relative path keys, and serve
lookups from an in-memory map. Preserve the clean skip when Git is unavailable
and the `None` result for untracked files. Add unit tests for tracked,
untracked, nested, and platform-normalized paths and record an empirical before/
after measurement.

**Disposition:** fixed. One newest-first `git log --name-only` traversal now
populates the lookup map; tests pin one-process behavior and tracked/untracked/
out-of-root semantics. The repository check fell from 150.1 seconds to **2.6
seconds** on the same Windows checkout.

#### M-02 — Authoritative coordinator documentation still describes deleted behavior

**Location:** `project-trajectory/scripts/agent_loop.py:1-10,32-48` and
`docs/requirements/interfaces.csv:16` (IF-015).

```text
Unattended coordinator: loop fresh agent driver sessions until done.
... each resumes from docs/status.md ... until docs/run-state reaches an end state
```

```csv
IF-015,...,"agent_loop.py CLI: --root . resumes from docs/status.md headless ..."
```

**Problem:** WI-210 explicitly deleted the legacy serial resume driver and made
a plain launch the dispatcher. The same module docstring later says the legacy
driver is retired, so the file contradicts itself. IF-015 is a registry contract
and is therefore worse than a stale comment: it advertises an interface that no
longer exists.

**Why it matters:** operators and downstream adopters use these surfaces to
understand run-state authority, inputs, and concurrency. Contradictory contracts
invite incorrect automation and undermine confidence in the otherwise strict
architecture registry.

**Suggested improvement:** rewrite the module opening around its current three
roles (dispatcher, worker, one-shot interactive session) and update IF-015 to
state the actual CLI/locking/preflight contract. Regenerate architecture views
and keep the behavioral code unchanged.

**Disposition:** fixed. The module opening and operative bullet list now state
dispatcher/assigned-worker/interactive behavior, and IF-015 records the current
WI-registry/Git-backed dispatcher, worker flags, preflight, and lock contract.

#### M-03 — Off-spine integrity requirements omit registries the implementation enforces

**Location:** `docs/requirements/system-requirements.csv:3,6` (SR-002/SR-005),
`docs/requirements/low-level-requirements.csv:6` (LLR-005), and
`docs/test/test-cases.csv:6` (TC-005).

```text
SR-002 AC: duplicate/malformed SR/LLR/TC/PB/MOD/PART/ASSET id
SR-005: optional off-spine registries (PB/MOD/PART/ASSET)
LLR-005: resolves MOD DelegatedSRs
```

**Problem:** the implementation and tests distinguish current `REPO` rows from
legacy `MOD` rows and also enforce `CMP` and `IF` integrity. The acceptance
criteria enumerate the older subset only. The requirements are mechanically
linked and Verified, but their prose understates the verified behavior.

**Why it matters:** a traceability system that tolerates semantic drift in its
own requirements can be green while communicating the wrong assurance claim.
Auditors should not need to infer the current contract from test filenames.

**Suggested improvement:** amend SR-002's complete ID list and describe SR-005/
LLR-005 as PB/REPO (with legacy MOD compatibility)/PART/ASSET. Clarify TC-005's
method without changing IDs or verification state, then regenerate all derived
views and run strict traceability.

**Disposition:** fixed. SR-002 now enumerates all integrity-checked IDs;
SR-005/LLR-005/TC-005 distinguish current REPO from legacy MOD compatibility.
Strict traceability and generated-view freshness remain clean.

#### M-04 — The dashboard clips rightmost content at the supported 390 px view

**Location:** rendered `PROJECT_STATE.html`, reproducible in
`scripts/dashboard-shots/shots/390px-light-sw-full.png` and
`390px-light-arch-full.png`; source generator in
`project-trajectory/scripts/gen_trajectory.py`.

**Problem:** the rightmost component in the software view is clipped at default
zoom, and the architecture icicle exposes only its first columns without a clear
horizontal-scroll affordance. The container technically uses `overflow:auto`,
but the default rendered state fails the repository's own T4 usability rubric
because content appears truncated.

**Why it matters:** mobile users can miss components and relationships while
believing they have seen the whole view. This is an accessibility and truth-of-
presentation defect, not merely an aesthetic preference.

**Suggested improvement:** file a dedicated dashboard WI as required by the
render-critique protocol. Explore an explicit scroll cue/fade, a compact mobile
layout, or a fit-to-width overview with detail-on-interaction. Verify the entire
36-shot width/theme/tab matrix after the change.

**Disposition:** deferred as **WI-219**. The defect and acceptance direction are
recorded; implementation awaits the dedicated rendered UX iteration.

#### M-05 — Several system requirements have become non-atomic mini-specifications

**Location:** `docs/requirements/system-requirements.csv`, notably SR-044,
SR-045, SR-060, SR-061, SR-065, and SR-066.

**Problem:** eleven system-requirement rows exceed 2,000 characters; SR-066 is
about 3,800 characters. Individual rows combine routing, scoring, fallbacks,
escalation, provenance, safety behavior, and detailed acceptance criteria.

**Why it matters:** the IDs are technically traceable but not independently
reviewable, implementable, or changeable. A small policy amendment forces a
large requirement and its linked evidence to be re-ratified. This is excessive
coupling inside the supposedly atomic spine.

**Suggested improvement:** do a planned spine migration: split genuinely
independent obligations into stable new SR/LLR/TC chains, retain parent or
supersession links, and update stakeholder-need coverage deliberately. Do not
mechanically split sentences or renumber existing IDs in a cleanup commit.

#### M-06 — Trailing run-menu arguments are concatenated into a shell command unquoted

**Location:** `project-trajectory/scripts/run_menu.py:107-116`

```python
full = command if not extra else command + " " + " ".join(extra)
return subprocess.run(full, shell=True).returncode
```

**Problem:** the configured command is intentionally trusted and needs shell
syntax, but separately supplied trailing arguments are appended as raw shell
text. Spaces, quotes, redirection, `&`, `;`, pipes, and platform-specific shell
metacharacters can change meaning instead of being passed as one argument.

**Why it matters:** this is at least a correctness defect and can become command
injection when a wrapper forwards data not authored by the same trusted user.
The current documentation collapses two different trust boundaries—declared
command text and invocation arguments—into one.

**Suggested improvement:** define the contract first. Prefer an explicit
placeholder/argv mode for commands that accept forwarded arguments while
retaining shell mode only for fully trusted, self-contained commands. If raw
shell passthrough remains, document that trailing values are shell fragments,
not arguments, and reject its use with untrusted data. Cross-platform quoting
should not be guessed with a single `shlex.quote` call because Windows `cmd.exe`
has different rules.

#### M-07 — Documentation discoverability produces 48 live orphan warnings

**Location:** repository-wide `check_docs.py --root . --stale` output.

**Problem:** after excluding generated report bundles and archive noise, the
checker still reports 48 live documents that no scanned document links to. Many
are historical review/spec artifacts where orphaning may be intentional, but
the current policy does not distinguish retained evidence from forgotten
documentation.

**Why it matters:** a warning count this high becomes background noise. New
accidental orphans are hard to see, and useful specifications may exist without
an entry path for readers.

**Suggested improvement:** define explicit retained-evidence exclusions or
indexes, then ratchet on newly introduced live orphans rather than enforcing an
unrealistic zero immediately. Logs and archives should remain exempt as the
current design intends.

### Low

#### L-01 — README hard-codes a stale interface count

**Location:** `README.md:306`

```text
on — 61 declared seams
```

**Problem / impact:** the authoritative strict trace and generated status both
report 65 seams. This is minor by itself but visible count drift makes generated
truth look optional.

**Suggested improvement:** update the value to 65 or remove the exact count from
hand-authored prose where it adds little value.

**Disposition:** fixed by removing the volatile hand-authored count; the
generated status remains the exact-count surface.

#### L-02 — “Pinned” dev dependencies are compatible ranges, not reproducible locks

**Location:** `requirements-dev.txt`

```text
ruff~=0.15.0
pytest~=8.3
pytest-xdist~=3.6
```

**Problem / impact:** comments repeatedly call this a pinned toolchain, but
compatible-release specifiers allow new releases within the accepted range.
That is a reasonable maintenance policy with the weekly canary, but it is not a
byte-reproducible lock and cannot guarantee identical machinery across dates.

**Suggested improvement:** rename the policy “major/minor constrained” and state
the accepted drift, or generate a hash-locked CI requirements file while keeping
human-maintained input constraints separately.

**Disposition:** fixed in documentation. The file and workflow comments now call
the policy constrained compatible-release ranges and explicitly say it is not a
byte-reproducible lock; dependency behavior is unchanged.

#### L-03 — Git author identity is inconsistent

**Location:** repository history (665 commits).

**Problem / impact:** history contains three author spellings/email combinations,
including a bare `/` author name and two email addresses. Privacy enforcement is
explicitly disabled, so this is not a failed gate, but it weakens attribution
quality and complicates contributor statistics or later public release.

**Suggested improvement:** standardize future `user.name`/`user.email`; decide
separately whether rewriting published history is worth the disruption. Do not
rewrite history casually.

#### L-04 — Large test modules mirror source concentration

**Location:** `tests/test_agent_loop.py` (about 1,540 lines),
`tests/test_gen_trajectory.py` (about 1,430), and
`tests/test_trajectory.py` (about 1,350).

**Problem / impact:** the tests are readable and behavior-oriented, but finding
the correct fixture/patch point is increasingly expensive. Their size also
reinforces internal-module coupling around coordinator compatibility exports.

**Suggested improvement:** split by behavior boundary during the corresponding
production refactors (dispatch lifecycle, reservation/integration, routing,
rendered views), not solely to satisfy a line-count target.

### Positive / good practices

1. **Verification is substantive.** The full G3 gate passed format, lint, tests
   plus coverage, duplicate detection, derived-gate validation, strict
   traceability, privacy, documentation links, performance budgets, design-flow
   checks, strict trajectory, architecture map, trajectory map, status map, OKF,
   and skill synchronization.
2. **Testing is unusually comprehensive.** The Python 3.8 baseline completed
   1,030 tests with 90.98% coverage. Tests exercise real temporary scaffolds,
   Git repositories, subprocesses, locks, failure paths, and cross-platform
   behavior instead of relying only on mocks.
3. **Dependency posture is lean.** Shipped scripts use the Python 3.8 standard
   library only. The small dev-only Python and Playwright sets are separated and
   `npm audit` reported zero known vulnerabilities.
4. **Security boundaries are mostly explicit.** No `eval`, `exec`, `os.system`,
   bare `except`, or obvious unsafe parser was found. Broad exception handlers
   are generally documented as best-effort cleanup/reporting paths. Secret and
   privacy scanning is integrated into the gate.
5. **Architecture is made inspectable.** Components, interfaces, containment,
   requirements, tests, and work items have machine-checked registries and
   generated human views. Strict checks found zero component/interface findings.
6. **Generated artifacts are treated correctly.** Freshness checks prevent
   hand-edited snapshots from silently diverging from their rows of record.
7. **Cross-platform intent is real.** Windows, Linux, and macOS behaviors are
   represented in CI and tests, and platform-specific limitations are documented
   rather than hidden.
8. **Dashboard craft is strong overall.** Both themes are legible, navigation
   wraps cleanly at 390 px, reduced-motion and keyboard semantics have explicit
   rubrics, and the 36-shot matrix makes rendered regressions reviewable.
9. **Git work is mostly logically grouped.** WI/review-oriented commits make the
   history navigable, and destructive publication remains human-controlled.
10. **The stated goal and implementation align.** As a reusable, evidence-first
    project-trajectory kit, the repository is fit for purpose; its principal
    risk is accumulating too much machinery in a few orchestration surfaces.

## 3. Overall recommendations and next steps

1. **Immediately harden CI and repair factual drift.** Pin Actions by SHA, add
   least-privilege permissions, batch the Git staleness lookup, correct the
   coordinator/IF contract, update off-spine requirement terminology, and remove
   the stale README count.
2. **Create a dedicated coordinator-decomposition workstream.** Characterize the
   state machine, introduce a no-new-complexity ratchet, then separate pure
   decisions from Git/worktree/session side effects. Set measurable targets per
   extracted boundary; do not optimize for arbitrary file counts.
3. **Resolve licensing before wider adoption.** OI-4 is a release-readiness
   blocker even though it is not a code blocker.
4. **Migrate oversized requirements deliberately.** New independent obligations
   should get new IDs rather than continuing to append clauses to SR-044/045/066.
   Preserve evidence and supersession history.
5. **Treat the mobile dashboard defect as product work.** File and prioritize a
   separate WI, fix it in the generator, and rerun the entire rendering matrix.
6. **Clarify the run-menu argument contract before changing it.** Separate
   trusted shell recipes from data arguments; cover Windows and POSIX explicitly.
7. **Reduce warning noise with ratchets.** Establish baselines for cyclomatic
   complexity and live doc orphans, then fail on regressions while paying down
   the existing debt in scoped work.

## 4. Verification evidence

- Clean worktree at review start; branch `dualplan-routing-fix`, target
  `cfd24c4`.
- `.venv` Python 3.8 toolchain: Ruff format and configured lint pass.
- Ruff C901 diagnostic (not configured as a gate): 50 findings.
- `trace.py --strict`: SN=25, SR=66, LLR=76, TC=76; zero orphans/integrity,
  zero interface findings, zero component findings.
- `check_trajectory.py --strict`: 216 WIs, 204 done, acyclic.
- Full derived G3 gate: **PASS 16/16**.
- Tests + coverage within the gate: **1,030 passed, 34 skipped, 90.98%**
  (skip split is a session-PATH artifact — §5).
- `check_docs.py --stale`: zero broken links, 48 live orphan warnings;
  doc-navigability step 150.1 seconds.
- Dashboard: all 36 declared width/theme/tab screenshots generated and sampled;
  390 px clipping reproduced.
- `npm audit`: zero known vulnerabilities in the dashboard screenshot helper.

### Remediation closeout

- Full suite after fixes: **1,033 passed, 34 skipped**.
- Final full derived G3 gate: **PASS 16/16**; tests+coverage **1,033 passed,
  34 skipped, 90.98%**.
- Strict trajectory: 217 WIs, 204 done, acyclic; WI-219 is the one newly queued
  rendered-dashboard follow-up.
- Strict traceability: unchanged 25/66/76/76 spine, 65 interfaces, five
  components, zero integrity/orphan/component/interface findings.
- Documentation navigability: zero broken links, the baseline 48 retained-live-
  evidence orphan warnings, **2.5 seconds** in the final G3 run (150.1 seconds
  before batching).
- One earlier G3 attempt had a single scaffold test's `derive_gate.py` subprocess
  return 1 with no output while 1,032 peers passed. The same test passed
  immediately in isolation; the complete G3 rerun then passed all 1,033 tests.
  This is recorded as a Windows temp/resource transient, not concealed as a
  first-try green run.

## 5. Validity re-check (2026-07-18, at `ddaa9cd`, third-party sitting)

This report was independently re-verified after the gilbert-crosscheck filings
(WI-220/WI-221) landed. Every checkable claim was tested against the tree and,
where external, against the source of record. Corrections were applied inline
and are marked "§5"; nothing else was altered.

**Confirmed valid.**

- **H-01 disposition:** all three workflows carry `permissions: contents:
  read` and full-SHA pins with version comments, and the scaffold guard test
  (`test_workflows_pin_actions_and_reduce_token_permissions`) exists. The
  three pinned SHAs were verified against GitHub's tag refs and **all match**:
  `actions/checkout@de0fac2e…` = v6.0.2, `actions/setup-python@a309ff8b…` =
  v6.2.0, `actions/upload-artifact@043fb46d…` = v7.0.1.
- **M-01 disposition:** the single-traversal `git_commit_lookup` is in place
  with its tests; the timing claim reproduces — `check_docs --stale` measured
  **2.3 s** on this checkout (claimed 2.5–2.6 s, vs 150.1 s before batching).
- **M-02/M-03/L-01/L-02 dispositions:** the `agent_loop.py` opening and
  IF-015 now state the dispatcher/worker/interactive contract; SR-002
  enumerates the full integrity-checked id set (with the legacy-MOD note);
  the README count and the "pinned" wording changes are in place.
- **M-04:** WI-219 exists queued as recorded. **M-06** location and behavior
  confirmed at `run_menu.py:116`. Commit count at target (665) and the
  698-line / complexity-84 `dispatch_run` measurements confirmed.

**Corrected inline.**

1. The H-02 code snippet showed `def dispatch_run(args, root, engine_path):`
   — the real signature is `dispatch_run(args, root)`; the worker engine path
   is the module-level `_ENGINE` sibling constant (WI-218 hazard 1), not a
   parameter.
2. The H-02 source-file sizes were unlabeled non-blank counts (~7% under the
   `wc -l` figures every other record in this repository uses); replaced with
   `wc -l` values, and §1's "2,000-line dispatch module" adjusted to 2,125.
3. The C901 census of 50 was correct **at the target**, but this review's own
   M-01 remediation added a 51st over-limit function (`git_commit_lookup`) —
   annotated, since it is live evidence for H-02's no-new-complexity-ratchet
   recommendation: even a remediation pass grows the census when nothing
   fails on it.
4. The "34 skips on Python 3.8" attribution: the skips are not
   Python-version-related. The review session's PATH had no POSIX `sh`, so
   the ~31 shell-dependent tests (the `"needs a POSIX shell"`/`"no POSIX
   shell on PATH"` guards) skipped. On the canonical environment (Git Bash
   present) the identical collection runs **1,064 passed / 3 skipped**
   (re-run at `ddaa9cd`; the 3 are the POSIX-only lock degrade, the
   coverage-run-only probe, and the executable-bit check). Same tests, same
   green — but the split is environmental, and gate evidence should name the
   shell environment when skips exceed the canonical 3.

**Cross-reference (post-report filings).** WI-220 (dispatcher hardening:
diverged-dev NEEDS-HUMAN guard, disposition freshness regen, evidence
salvage — from the gilbert crosscheck) and WI-221 (round-budget default)
were filed after this report and are *adjacent to but distinct from* H-02:
they harden the dispatcher's correctness, not its decomposition. H-02's
required next move — the characterization + ratchet + effect-separation WI —
**remains unfiled** and is still the largest open maintainability item.
