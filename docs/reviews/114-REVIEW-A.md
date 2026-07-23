# 114-REVIEW-A — WI-270 (reconcile the Python-floor requirement spine 3.8 → 3.11)

Independent adversarial review (REVIEW-A) of commit `a9e2b45` on
`dualplan-routing-fix` (WI-270). Reviewer did not write the change and read no
builder self-assessment (the `docs/log.md` WI-270 entry was treated as narrative,
not evidence). Judged the diff + its requirement surface and drove the shipped
checks. Rubric: `docs/rubrics/code-review-adversarial.md`.

## Subject frame (R1)

**What changed.** A text-only **requirements-change / re-attestation** WI. WI-262
already bumped the kit's *actual* floor 3.8 → 3.11 (scripts, `test.yml`,
`requirements-dev.txt`, ADOPTING.md) but froze the requirement CSVs. This commit
reconciles the lagging spine + docs: `SN-011`, `SR-034` (Requirement) and
`SR-035` (Requirement **and** its AcceptanceCriteria narrative), `TC-035`
Parameters, `architecture.md`, `status.md` (Scope), and the `WI-064.md`
build-note — all `3.8` → `3.11`. Generated artifacts (`PROJECT_STATE.html`,
`docs/okf/*`) regenerate from the edited spine. `work-items.csv` flips WI-270
`queued` → `active`. The substantive edit is **rewriting SR-035's AC**: the old
"macOS+3.8 excluded because macos-latest is arm64 with no CPython 3.8 build"
story → a new narrative that must match what `test.yml` actually does.

**Blast radius.** Downstream adopters read these SR rows as the contract;
`TC-035` points reviewers at `.github/workflows/test.yml`; the OKF bundle and the
dashboard are generated from the spine, so a stale edit shows up as a `--check`
failure. No executable path changes.

**Requirement it must satisfy.** The WI-270 Done-when (docs/specs/WI-270.md) plus
the honesty obligation that `SR-034`/`SR-035` stay `Verified` truthfully. Ground
truth for SR-035's AC is `.github/workflows/test.yml` (its `matrix:` + `exclude:`).

Worst failure classes hunted first (R3): an **inaccurate AC** (does SR-035 now
faithfully describe `test.yml`? is the macOS-exclusion rationale right — a
coverage call, not arm64-availability? any self-contradiction?); a **missed live
3.8 surface** or a doc now contradicting a 3.11 sibling; **broken evidence /
dishonest Verified**; and **scope creep** into code/CI/templates/byte-budgeted
files.

## What I drove (reproduced, not assessed — R2)

**1. Spine integrity + gate, both strict, clean.**
```
$ ./.venv/bin/python .../trace.py --root . --strict
    SN=25 SR=109 LLR=97 TC=100 orphans=0 integrity=0 verified-mechanized=92
    verified-demonstrated=17 component-findings=0 interface-findings=0     EXIT 0
$ ./.venv/bin/python .../check_trajectory.py --root . --strict
    check_trajectory: clean (268 work item(s), 256 done (96%), acyclic).   EXIT 0
$ cat docs/gate   ->   G3   (basis drafts=0 computed=G3, all 4 phases G3)
```

**2. Generated artifacts match the edited spine; full G3 gate green (driven, not
trusted).** The commit claims `check.py --gate G3 PASS`; I reproduced it whole.
```
$ ./.venv/bin/python .../check.py --run-steps "okf,status-map,trajectory-map,arch-map,doc-navigability,traceability"
    okf "bundle up to date (407 file(s))" · traceability PASS (--require-verified,
    status-findings=0 schema-findings=0) · status-map "up to date" ·
    doc-navigability "0 broken" (only "possibly stale" hints, non-failing) ·
    arch-map "code map up to date" · trajectory-map "dashboard up to date"  all PASS
$ ./.venv/bin/python .../check.py --gate G3
    format · lint · tests+coverage 425.0s · dupes · derived-gate · traceability ·
    privacy · doc-navigability · perf-budgets · design-flows · trajectory ·
    arch-map · trajectory-map · status-map · okf · skills-sync    16/16 PASS
    RESULT: PASS
```
The `okf`/`trajectory-map`/`status-map` "up to date" results prove the committed
`PROJECT_STATE.html` + `docs/okf/SR-035.md` etc. ARE fresh at commit — the edited
AC propagated to every generated view, no hand-maintained drift.

**3. `test.yml` vs SR-035's new AC — they AGREE (the crux).** Read the workflow
matrix:
```yaml
os: [ubuntu-latest, windows-latest, macos-latest]
python: ["3.11", "3.x"]
exclude:
  - os: macos-latest      # comment: 3.11 has arm64 macOS builds, so this
    python: "3.11"        # exclusion is now a coverage call, not a runner-
                          # availability workaround; macOS's job is fcntl.flock/
                          # paths/git worktrees, invariant across Python version.
```
Effective cells: ubuntu×{3.11,3.x}, windows×{3.11,3.x}, macos×{3.x} only.
SR-035's rewritten AC states: matrix "spans Linux, Windows and macOS on Python
3.11 and latest (3.x) … macOS runs on current Python (3.x) only … the 3.11 floor
is a platform-agnostic language/stdlib guarantee already exercised on Linux and
Windows, while macOS's job is OS-specific behavior (fcntl.flock, paths, git
worktrees) that does not vary by Python version, so the macOS+3.11 cell is
excluded as a redundant-coverage call (M-27), not a runner-availability
workaround (3.11 has arm64 macOS builds)." Clause-by-clause this matches the
workflow's axes, the `(macos,3.11)` exclusion, the OS-specific-behavior list
(verbatim), and — critically — the exclusion **rationale**: a coverage/cost call,
NOT arm64-availability, with the correct note that 3.11 *does* have arm64 macOS
builds. The shipped AC does **not** claim macOS runs on 3.11; it states 3.x-only
and then names the excluded cell. **No mismatch, no self-contradiction.** `M-27`
resolves (docs/repo-review-2026-07-21.md:674) to the CI cost/redundant-matrix-cell
measure — an on-theme citation for a coverage-driven exclusion.

**4. SR-034 evidence is version-agnostic and green.** SR-034's AC is an AST
stdlib-only scan (no version literal), so amending "3.8+"→"3.11+" cannot touch it.
Drove it: `pytest tests/test_stdlib_only.py` → 2 passed. Keeping `Verified` is
honest. SR-035's evidence (TC-035 → `test.yml`, Verification=Analysis) now matches
the shipped matrix, and the full suite the CI runs is green (§2); keeping it
`Verified` is honest.

**5. No missed live 3.8 surface.** Broad `grep -rI "3\.8"` across ALL file types
(incl. `.sh`/`.ps1`/no-extension), minus the legit-history set
(archive/log/reviews/repo-review/iteration, the WI-270 spec, done-WI deliverables
WI-020/104/105/175), returns only: `requirements-dev.txt` (a comment explaining
the *dissolved* 3.8-gated pytest-cov split — it already asserts "the kit's 3.11
floor"), `tests/test_stdlib_only.py` (fallback behavior "below the 3.11 floor" —
explicitly not a floor claim), and `ADOPTING.md` (the WI-262 migration note,
past-tense "was 3.8"). All three are reconciled to 3.11 and describe history, not
a live floor. The shipped CI template `project-trajectory/ci/check.yml` and every
`dev-setup.*` say `3.x`/"Python 3.11+" — no 3.11-vs-3.8 sibling contradiction.

**6. Scope — text-only, no forbidden surface.** `git show --stat a9e2b45`: 14
files, all docs/spine/generated. **No** kit script, **no** `.github/workflows/*`,
**no** shipped `*.template.*`, and **none** of the byte-budgeted files
(`AGENTS.template.md`, `PROCESS.md`, `PROCESS_OPTIONS.md`). No scope creep.

## Done-when coverage map (R4)

| WI-270 Done-when item | Status |
| --- | --- |
| SN-011 / SR-034 / SR-035 / TC-035 / architecture.md / status.md all read 3.11, zero live 3.8 floor claims outside history | **COVERED** — diff moves all six (+ WI-064 note); broad grep confirms no live 3.8 claim remains (§5) |
| SR-035's AC describes the actual `test.yml` matrix (no arm64-3.8-exclusion story) | **COVERED** — clause-by-clause match incl. rationale; drove the workflow read (§3) |
| SR-034/SR-035 re-attested; `trace.py --strict` + `check_trajectory` clean; gate stays G3 | **COVERED** — both strict exit 0, `docs/gate`=G3 (§1); SR-034 evidence re-driven green (§4) |
| Full suite + `check.py --gate G3` green; independent reviewer's verdict; dashboard/OKF/status regenerated | **COVERED** — `check.py --gate G3` RESULT: PASS 16/16 (§2); OKF/dashboard/status "up to date"; this review is the recorded verdict |

Every Done-when item maps to a driven observation; none UNCOVERED.

## Findings

- [MINOR] docs/specs/WI-270.md:32 -> the Scope prose "`ubuntu/windows/macos × {3.11, 3.x}`, **macOS pinned to the floor cell**" is inverted (the floor cell is 3.11, which `test.yml` *excludes* for macOS) and contradicts line 30's "runs macOS on current Python only"; it is only imprecise spec prose — the **shipped** SR-035 AC correctly says "macOS runs on current Python (3.x) only", so the deliverable is right and no live claim is wrong -> reword the frozen spec note to "macOS pinned to the current-Python (3.x) cell; the 3.11 floor cell excluded" so the historical build-note doesn't misdirect a future reader -> @owner

## Verdict

Tried to break it across every worst class the frame named. The AC rewrite is
faithful to `test.yml` line-for-line, including the load-bearing rationale flip
(coverage call, not arm64-availability) with the correct "3.11 has arm64 macOS
builds" note, and carries no self-contradiction. The missed-surface sweep found
no live 3.8 floor claim and no 3.11/3.8 sibling contradiction; both SRs stay
`Verified` honestly (SR-034's AST scan is version-agnostic and green, SR-035's AC
matches the green matrix); the change is strictly text with no code/CI/template/
byte-budget touch; the generated OKF/dashboard/status are fresh; and the full G3
gate is green. Every Done-when item is covered. The sole finding is a non-blocking
imprecision in the frozen descriptive spec, not in the shipped requirement.

- VERDICT: APPROVE findings=1
