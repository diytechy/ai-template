# Grind Review B — Process / Traceability / Prose (WI-1.47…1.52 batch)

> **RESOLVED 2026-07-10 (review triage, WI-1.53).** All 4 findings fixed:
> B1 (spine SN-Refs) + B2 (OKF count) in triage commit 1/5 — B1 rode the
> pending re-attestation as recommended; B3 (template trim) + B4 (ADOPTING
> caveat) in commit 5/5. See IMPROVEMENT_PLAN.md WI-1.53.

**Reviewer:** Claude (Opus 4.8) — REVIEWER B (process/trace/prose charter), fresh
context, no shared transcript with the implementer · **Date:** 2026-07-10 ·
**Branch:** `MultiRepoSupport` (not pushed).

Adversarial review of the 2026-07-10 grind batch — the commit range
`513939e..HEAD` (11 commits, `a8cea97`…`33b40e3`). Charter: SSOT violations,
traceability honesty, requirement/TC text quality, doc honesty,
template/scaffold coherence, downstream-migration safety. Method/risk/corner-case
bugs are the sibling reviewer's charter and are skipped here. Every finding is
verified against the tree with the read-only checks noted; nothing was modified
except this report.

> How to read: the batch is genuinely well-executed — mechanically clean spine,
> green suite, fresh artifacts, honest statuses, byte budgets respected. **There
> is no HIGH and no false-green.** B1 (MEDIUM) is a need-citation-honesty defect
> on the meta-repo's own spine; B2–B4 are a wrong number, a mild SSOT drift, and
> a migration-doc omission. The verified-clean list is long on purpose — most of
> the charter's hunt list came back sound.

---

## Scope reviewed

- **Range:** `git log --oneline 513939e..HEAD` — WI-1.45 (F2 hook), WI-1.46
  (F4–F8 closure), WI-1.47 (TC `Evidence`), WI-1.48 (`check_dupes`), WI-1.49
  (dynamic layer), WI-1.50 (`check_doc_refs`), WI-1.51 (OKF export), WI-1.52
  (root `PROJECT_STATE.html`), plus the ingest-audit + grind-records commits.
- **Spine:** `docs/requirements/*.csv` + `docs/test/test-cases.csv` (the kit's
  own registries) — SR-039…042 + LLR-036…039 + TC-039…042 added, SR-038 /
  LLR-035 / TC-038 extended, the whole TC table migrated to the `Evidence`
  column.
- **Templates the kit ships:** `project-trajectory/registries/test-cases.template.csv`,
  `review-policy.template`, `EXAMPLE.md`, `ADOPTING.md`, `PROCESS_OPTIONS.md`,
  both READMEs, `STATUS.template.md`, `bootstrap.py` — kept distinct from the
  kit's own filled registries.
- **Read-only checks run:** `trace.py --strict --no-placeholders
  --require-verified --strict-schema` (0/0/0/0/0); `pytest -q` (445 passed, 2
  skipped, reproduced); `gen_trajectory.py --check`, `gen_okf.py --check`,
  `check.py --run-step arch-map` (all fresh); `check_docs.py --root . --stale`
  (0 broken); `check.steps(80,'full','G3')` enumeration.

## Severity index

| ID | Sev | One-liner |
|---|---|---|
| **B1** | **MEDIUM** | The batch's new opt-in-layer SRs mis-route their need citations — SR-041 (a doc-currency linter) never cites SN-010; SR-039/041/042 assert SN-012's opt-in/zero-cost property but none cite SN-012 (which even names "OKF export"); SR-041 cites SN-004 approval-gates for a warn-first linter. |
| **B2** | LOW | The OKF bundle is recorded as "148 files" in `IMPROVEMENT_PLAN.md` (WI-1.51) and in the dogfood `work-items.csv` (WI-034) — the committed and `--check`-verified count is **151** (the commit message is correct). |
| **B3** | LOW | `review-policy.template`'s comment block restates the floors + split-charter semantics that `PROCESS_OPTIONS.md` also carries — heavier duplication than its sibling policy templates keep; a mild SSOT drift within the sanctioned self-documenting-config pattern. |
| **B4** | nit | `ADOPTING.md` §6's OKF entry omits the partial-re-sync caveat (hook step 1c `okf` against a pre-Thread-48 `check.py` fails "no step named 'okf'") that the sibling WI-1.45 trajectory-map change documented. |

---

## B1 — MEDIUM · New opt-in-layer SRs mis-route their `SN-Refs`

**What.** Three of the four new capability SRs cite stakeholder needs that do
not match the need-level truth their own text states, and skip the needs that
do. The kit's whole premise is *need-traced* requirements dogfooded on itself;
here the need-mapping is imprecise on the spine that is supposed to be the proof.

**Evidence (verified against the tree).**

- `docs/requirements/system-requirements.csv` (`git diff 513939e..HEAD`):
  - `SR-041` (Doc reference validation → `check_doc_refs.py`) cites
    **`SN-004;SN-008`**. Its own AcceptanceCriteria/Rationale are entirely about
    doc currency: *"prose naming a renamed/deleted file … the two rot classes
    link resolution cannot see."* That is verbatim **SN-010** — *"Documentation
    stays navigable and honest — links resolve … generated views cannot silently
    rot"* (`stakeholder-needs.md:30`). **SR-041 never cites SN-010.** Instead it
    cites **SN-004** (*"Progress advances only through explicit approval
    gates"*) for a checker that is **warn-first, exit 0** unless `--strict` — it
    has nothing to do with gate progression.
  - `SR-039` (Duplicate-code lint) cites **`SN-008`** only; `SR-042` (OKF
    export) cites **`SN-004;SN-010`**. Both rationales lean on the opt-in /
    zero-cost property — SR-039: *"an opt-in product-layer step … so a
    non-adopter pays nothing"*; SR-042: *"owner-ruled on-by-default/opt-out"* —
    which is precisely **SN-012**'s acceptance intent: *"heavy layers are opt-in
    … Opt-in layers (perf, guardrails, unattended, parallel tracks, **OKF
    export**) cost a repo that doesn't use them nothing"* (`stakeholder-needs.md:32`).
    SN-012 **names OKF export by name**, yet `SR-042` does not cite it.
- Cross-check of who cites what (`csv` scan):
  - `SN-010` cited by SR-012, SR-013, SR-022, SR-023, SR-038, SR-042 — **not
    SR-041**, the most doc-honesty-shaped script in the repo.
  - `SN-012` cited by SR-005, SR-009, SR-014, SR-025, SR-037 — **none of the
    three opt-in scripts this batch added** (SR-039/041/042).

**Why it matters.** This is a traceability-honesty defect, not a mechanical one:
`trace.py` stays green because those SNs already have other SRs, so no orphan
appears. But the meta-repo is the kit's evidence that it *"traces itself with its
own process,"* and the charter test is *"does the SR state a need-level truth."*
Here the answer is no for SR-041 (a doc-currency need mapped to gate-progression
needs) and incompletely for SR-039/042 (the opt-in-layer need SN-012 — the one
that even names OKF export — is uncited). An auditor reading the spine to learn
*why* each script exists is pointed at the wrong needs.

**Suggested fix (local, spine-touching so it rides the pending re-attestation).**
Re-point the `SN-Refs` cells: `SR-041` → add `SN-010` (its true home; keep or
drop SN-008, drop SN-004); `SR-039` → add `SN-012` alongside SN-008; `SR-042` →
add `SN-012` (keep SN-010). Re-run `trace.py --strict --require-verified
--strict-schema` (SN coverage only widens) and note the correction in the same
`docs/log.md` re-attestation entry.

---

## B2 — LOW · The OKF bundle file-count is wrong in two live records

**What.** The generated OKF bundle is stated as **148 files** in two places that
purport to record reality; the committed and freshness-verified count is **151**.

**Evidence.**
- `IMPROVEMENT_PLAN.md` WI-1.51 entry (line ≈6855): *"The meta-repo commits its
  own **148-file bundle**."*
- `docs/requirements/work-items.csv`, row `WI-034` Deliverable note: *"meta
  bundle = **148 files**."*
- Tree reality: `git ls-files 'docs/okf/*'` → **151**; `gen_okf.py --check` →
  *"OKF bundle up to date (**151** file(s))."* The count is exact: 22 SN + 42 SR
  + 39 LLR + 42 TC = 145 concepts, + 4 tier `index.md` + 1 root `index.md` + 1
  `UPSTREAM.md` = 151.
- The **commit message** of `27ebc29` says *"151-file bundle"* — so the code and
  the commit got it right; only the plan doc and the dogfood registry carry the
  stale 148 (the count *before* SR-042/LLR-039/TC-042 — the OKF layer's own three
  spine rows — were added).

**Why it matters.** `work-items.csv` is the kit's *own filled registry* and part
of the dogfooded trajectory layer; a wrong number in a Deliverable note is the
low-grade honesty rot the process exists to prevent (the same class as
THREAD_52_REVIEW F3's "narrative not data"). Harmless to the gate, but it is a
factual claim contradicted by the tree it describes.

**Suggested fix.** Replace "148" with "151" in both the WI-034 note and the
WI-1.51 plan entry. (Cosmetic; not spine-touching.)

---

## B3 — LOW · `review-policy.template` duplicates PROCESS_OPTIONS semantics more heavily than its siblings

**What.** The new `docs/review-policy` value (0|1|2) is documented in **two**
full places: its own 20-line comment block *and* the new PROCESS_OPTIONS
"reviewer dial + cross-provider routing" paragraph — both spelling out the
floors (autonomous ⇒ ≥1, spine-WI ⇒ 2) and the A=method / B=process split
charter.

**Evidence.**
- `project-trajectory/review-policy.template:14-19` — floors + split charter +
  cross-provider recommendation, in-file.
- `project-trajectory/PROCESS_OPTIONS.md` (the "reviewer dial" block,
  `git diff`) — the same floors and the same A/B charter, in prose.
- Sibling precedent: `gate-policy.template` and `push-policy.template` keep
  their comment blocks to **value meanings only** and defer the narrative to
  `process-options.md` ("Gate authority levels" / "Agent iteration branch &
  sync"). `review-policy.template` goes further, carrying floors and charter
  detail that its siblings leave to the prose doc.

**Why it matters.** The kit's own rule (CLAUDE.md) is *"state a rule once, link
to it."* Self-documenting config files are a sanctioned pattern (the gate/push
templates prove it), so this is **not** a clean violation — but the review-policy
file restates more of the operative rule than the pattern needs, so a later edit
to the floors/charter must touch two files to stay consistent (split-brain risk).

**Suggested fix (optional).** Trim the template comment to the value meanings
(0|1|2 + "floors and charter: see process-options.md 'Unattended operation'"),
matching the gate/push templates; let PROCESS_OPTIONS own the floors + charter.
Judgment call — leaving it is defensible if the owner wants the dial fully
self-explaining offline.

---

## B4 — nit · ADOPTING §6's OKF entry omits the partial-re-sync failure caveat

**What.** The shipped pre-commit hook gains **step 1c** `check.py --run-step
okf`. An adopter who re-syncs the kit-owned hook against an *older* `check.py`
(no `okf` step) gets a hard `check: no step named 'okf'` on every commit — the
exact mixed-state failure the WI-1.45 trajectory-map change called out
explicitly. The ADOPTING OKF entry (`ADOPTING.md` §6, the new bullet) does not
mention it.

**Evidence.** `project-trajectory/hooks/pre-commit:113-117` (step 1c added);
`ADOPTING.md` §6 OKF bullet says only *"run `gen_okf.py` once … or opt out"* —
no re-sync-together note. Contrast WI-1.45's entry, which documented the
identical caveat for `trajectory-map`.

**Why it matters.** Low — the §6 preamble already states the general rule
(*"re-sync the kit-owned set together"*), which covers it. But the sibling
generated-artifact step got an explicit caveat and this one didn't, so the
migration guidance is asymmetric for two changes of the same class.

**Suggested fix.** One clause on the OKF bullet: *"(re-sync `check.py` with the
hook — an old `check.py` has no `okf` step)."*

---

## Cross-cutting observation (not a new finding)

The dogfood DAG still carries the **THREAD_52_REVIEW F3** looseness the batch did
not (and was not asked to) resolve: e.g. `WI-038` is `done` while its declared
predecessor `WI-033` is `active` — a completed item behind an unfinished
prerequisite. This is honestly **disclosed** as an open owner item ("F3
data-pass on the 42-WI DAG edges") in `docs/status.md`, so it is not a fresh
finding; noted only so the re-attestation sitting sees it is still open.

---

## Verified clean (checked and found sound)

- **Spine mechanically clean.** `trace.py --strict --no-placeholders
  --require-verified --strict-schema` → `SN=22 SR=42 LLR=39 TC=42 orphans=0
  integrity=0 status-findings=0 placeholders=0 schema-findings=0`. Matches the
  log/status counts exactly.
- **Suite reproduced.** `pytest -q` → **445 passed, 2 skipped** — the exact
  figure the log/plan claim. No green was reported that I could not produce.
- **Generated artifacts are fresh** (no silent rot): `gen_trajectory.py --check`
  (root `PROJECT_STATE.html`) → up to date; `gen_okf.py --check` → 151 files up
  to date; `check.py --run-step arch-map` (honoring `stack.ini`
  `src=project-trajectory/scripts`) → up to date.
- **G3 step count honest.** `check.steps(80,'full','G3')` yields 13 candidates,
  but `registry-integrity` is `gates={'G1'}` and does not apply at G3 — leaving
  **12** G3 steps, exactly the log's "PASS (12/12)" and status.md's "12 steps."
- **`Evidence` column migration coherent.** All 38 TC rows moved the `node=`
  overload out of `Parameters` into the new `Evidence` column; `Parameters`
  restored to dimensional inputs; template header + `TC-000` example +
  `EXAMPLE.md`'s five snippet blocks (incl. the ATTEST + seam-test cases) +
  ADOPTING §6 recipe all agree; the conditional `--strict-schema` rule
  (required-non-empty for `Automated=Yes`) is honestly framed as a G3 migration
  nudge, documented in ADOPTING §6.
- **Scaffold surface agrees across all four sources.** `bootstrap.py` MAPPING +
  its docstring + `tests/test_bootstrap.py` + both READMEs list the same new
  surface (`review-policy.template`, `check_dupes.py`, `check_doc_refs.py`,
  `gen_okf.py`). Templates stay copy-ready (`test-cases.template.csv` TC-000
  fills a plausible `Evidence`).
- **Opt-in / opt-out claims are true.** `check_dupes.py` and `check_doc_refs.py`
  are **not** in the built-in gate — only reachable via `[step:dupes]` /
  `[step:doc-refs]` profile lines (verified against `check.py steps()`); `okf`
  is on-by-default at G3 + hook 1c with the `docs/okf-export: off` opt-out;
  none of `docs/okf-export`, `docs/dupes-allow`, `docs/run-phase` exist in the
  meta-repo (defaults apply, as claimed).
- **`docs/trajectory.html` → root `PROJECT_STATE.html` swept cleanly.** The old
  file is `git rm`'d and gone; CLAUDE.md, both READMEs, STATUS.template,
  PROCESS_OPTIONS, bootstrap docstring, check.py step comment, and the hook all
  re-point to the root artifact; the only residual `docs/trajectory.html`
  mentions are legitimate (the ADOPTING migration recipe "delete your committed
  …" and a `gen_trajectory.py` "formerly …" comment) plus frozen history
  (IMPROVEMENT_PLAN landed-thread records, THREAD_52_REVIEW).
- **Byte-budgeted files respected.** `AGENTS.template.md` = 9976 B (< 10000) and
  `PROCESS.md` = 56375 B — **both untouched** in the range (`git diff --stat`
  empty).
- **SR/LLR/TC texts state testable truths and the tests mechanize them.** Spot-
  verified: SR-038's new claims (root artifact, git-derived as-of stamp
  *excluded* from `--check`, How-SW view omitted without an inventory) are each
  pinned by real tests (`test_asof_stamp_from_git_and_excluded_from_check`,
  `test_no_git_means_no_stamp…`, `test_how_sw_view_renders_from_the_module_map`);
  TC-039 (dupes: both locations named, one merged finding, tunable, allowlist,
  in-block non-self-report), TC-040 (cmd-map routes REVIEW-B, broken entry fails
  preflight, banner carries the dial, size guard warns-not-blocks), TC-042 (OKF
  determinism, `--check` on edits/extras, prune, vacuous, off) all resolve to
  present, matching test methods.
- **Dogfood registry statuses honest.** `work-items.csv` = 42 WIs, **41 done +
  WI-033 active** — matches `status.md`. New rows WI-034/035/037/039/040/041/042
  carry accurate `SR-Refs` (SR-042/041/039/038/[019;038]/[037;038]/040) and
  done-statuses backed by landed work; WI-036 (Evidence column, no new SR)
  correctly has an empty `SR-Refs`.
- **Resume surface accurate.** `docs/run-state` = `NEEDS-HUMAN` (matches "the run
  is paused"); `docs/status.md` is a single-screen blackboard naming the three
  human asks (re-attestation / push / F3 data-pass); `docs/log.md`'s 2026-07-10
  spine-change entry is complete — SR-039…042 added, SR-038/LLR-035/TC-038
  extended, re-attestation PENDING (correctly **mandatory** because a Verified
  SR's text changed), with an honest verification split (**42 mechanized / 0
  attested = 39 Test · 1 Analysis · 2 Inspection**, which I recomputed from the
  SR `Method` column and confirmed).
- **Doc graph intact.** `check_docs.py --root . --stale` → **0 broken** across
  663 intra-repo links; the one orphan warning (`docs/test/report.md`) is the
  pre-existing generated trace report, not introduced here; the stale *hints*
  are below-WARN and expected on a commit that edits those scripts.
- **`.gitattributes` riders present** (both template and meta): `docs/okf/**
  linguist-generated=true -diff`, matching the "commit-for-availability, diffs
  suppressed" claim.
