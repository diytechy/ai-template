# WI-454 — REVIEW-A (2026-08-14)

**Reviewer:** OPENAI-TERRA (`gpt-5.6-terra`, medium effort) via the `codex`
CLI — cross-family, fresh context each round, independent of the lane builder.
Charter: [code-review-adversarial](../rubrics/code-review-adversarial.md).
Given the branch diff (`infra/mechanized-loop...wi454-need-form-checker`,
18 files, +629/−29 at round 1's tip 692452fa) and the requirement surface: the
WI-454 row's frontmatter clause list
(`docs/work/complete/WI-454-sn-033-need-form-checker.md`), SN-033's ratified
acceptance text (the commissioning clause), and the specref (sitting-2 plan
decision 7 rider 2 + §6 item 16,
`docs/plans/2026-08-13-sitting-2-boundary-and-context.md`). The spec's
`## Deliverable` prose is the implementer's own account and was supplied only
as claims-to-verify, never as evidence; no other self-assessment was shown.
Run under `--sandbox workspace-write` with an out-of-repo scratchpad; every
round's drives left `git status --porcelain` clean. Machine-local absolute
paths in the reviewer's output are rewritten repo-relative (`<scratch>` = the
session scratchpad); nothing else in the verdicts is edited. Findings were
re-verified by the session author against the real tree before any fix (the
author-re-verifies convention); every consumed finding below reproduced, and
the one refuted finding is recorded with its driven counter-evidence, not
dropped.

**Final verdict: APPROVE at 6d83438f** — round 1 CHANGES-REQUESTED (3 MAJOR
1 MINOR: the one-level-path carve-out, the vacuous-registry clean, the URL
tail; the allow-span challenge refuted), round 2 CHANGES-REQUESTED (2 MAJOR
2 MINOR: sentence-final phrase misnaming, scheme-less `www.` addresses, the
mis-stated allow separator in two registry cells), round 3 CHANGES-REQUESTED
(1 MAJOR: URL-span greed swallowing genuine neighbours), round 4 APPROVE at
6d83438f after the round-3 fix (90f9bbbb). Four rounds follows the WI-442
precedent: the verdict round on the final tip is itself a driven review. The
machine line that governs is the last one in this file.

---

## Round 1 — at 692452fa (CHANGES-REQUESTED, 3 MAJOR 1 MINOR)

WI-454 lands `project-trajectory/scripts/check_need_form.py` — SN-033's
commissioned need-cell form checker (need cells ONLY; acceptance and
engineering cells exempt by SN-033's own text), with the reviewed exception
list `docs/need-form-allow` shipping empty, wired warn-first into `check.py`'s
step table at every bar. Blast radius: every adopter scaffold (bootstrap
MAPPING + manifest), the check.py step floor, trace.py's watermark scan (the
`_offspine_ids` IF/CMP re-arm), and the spine mint
SR-150 → LLR-170 → TC-164 + IF-121/IF-122. The worst failure class is the
checker's own purpose inverted: a silent under-report on the very registry it
was built to guard.

### Failure classes hunted, worst-first

1. Silent under-report on the live registry (regex misses a genuine
   violation class; the SN-id and single-slash carve-outs swallowing real
   violations; span-suppression interactions dropping findings).
2. The exception list as a silencing vector (over-broad entries, malformed
   lines, encoding/separator confusion).
3. Fail-open on the registry read (absent/empty/wrong-schema/malformed).
4. The warn-first wiring accidentally gating, or not running; scaffold
   breakage (bootstrap registration, placeholder rows).
5. The trace.py watermark re-arm regressing trace; spine rows that don't
   join; tests that stay green without the code.

### Exact commands and driven output (reviewer, re-verified by the author)

1. `check_need_form.py --root .` → `clean (27 need cell(s)…)`, exit 0; the
   9-test module suite passed; mutated-registry drives reported row AND
   phrase for planted paths, identifiers and citations.
2. Carve-out probes: need cells carrying `docs/archive` and `docs/work` —
   both REAL one-level internal paths — scanned **clean** (the blanket
   single-slash dot-free exemption). Driven by the author on the live tree:
   both exist in this repo.
3. Allow-list probe: `docs/need-form-allow` entry `docs/SR-101.md — reason`
   silenced the `SR-101` nested inside its own span under `--strict`
   (exit 0). Author counter-drive: the same cell with an independent
   `SR-101` OUTSIDE the span still errors (`ERROR - SN-050 … 'SR-101'`,
   exit 1).
4. Registry-read probes: malformed TOML → loud SystemExit (exit 1); ABSENT
   registry → clean skip; but an EXISTING empty-but-valid TOML and a real
   row with no `need` field both printed `clean (0 need cell(s)…)` — and
   the author's adjacent-machinery drive showed the hole is real at the
   current bar: with the registry emptied, `trace.py` default rc=0 (strict
   is not wired at DevBar-Reqs) and `derive_gate.py --check` rc=0 (the gate
   value is coincidentally unchanged), so nothing hard-fails.
5. URL probe: `https://example.test/docs/status.md` in a need cell reported
   `'test/docs/status.md'` as an internal path — against the docstring's
   own "URLs are deliberately NOT matched".
6. Windows-separator probe (author): `docs\status.md` in a TOML literal
   string reports `'status.md'` (row + phrase) through the identifier
   class, and a raw backslash in a TOML basic string is a loud carrier
   decode refusal — not a silent miss.
7. Wiring/scaffold/trace drives (reviewer): all three bars ran the
   `need-form` step with no `--strict`; a real `bootstrap.py` scaffold
   received and ran the checker; `trace.py` and `check_trajectory.py
   --strict` rc=0; lowered CMP/IF watermarks correctly refused (the
   `_offspine_ids` re-arm is armed); `derive_gate.py --check` current.

### Findings

- [MAJOR] project-trajectory/scripts/check_need_form.py (path class) -> genuine one-level internal paths (`docs/archive`, `docs/work`) are silently missed by the blanket single-slash dot-free exemption -> promote a single-slash dot-free token to a path when it resolves in the scanned tree. **CONSUMED** (the Windows-separator arm of this finding REFUTED in part: driven, the cell still reports row+phrase through the identifier class, and the TOML carrier refuses raw backslashes in basic strings loudly).
- [MAJOR] project-trajectory/scripts/check_need_form.py (allow spans) -> an allow-listed `docs/SR-101.md` suppresses the nested `SR-101`, clean under strict -> **REFUTED with driven evidence**: the suppression is deliberate, documented in the code, and necessary — without it, allow-listing `PROJECT_STATE.html` would re-flag its `PROJECT_STATE` substring, self-defeating the reviewed list; an independent citation outside the allow'd span still reports (driven, exit 1); the trigger requires a human-reviewed list entry that itself embeds the citation, which is exactly what the review of the entry judges.
- [MAJOR] project-trajectory/scripts/check_need_form.py (registry read) -> an existing empty or need-less registry scans as a clean tier, and nothing else in the harness hard-fails on it at DevBar-Reqs -> report a present-but-vacuous registry, keep absent as the pre-scaffold clean skip. **CONSUMED**.
- [MINOR] project-trajectory/scripts/check_need_form.py (URL exclusion) -> `https://example.test/docs/status.md` reports its tail as an internal path, contrary to the documented URL exclusion -> suppress whole URL spans before class matching. **CONSUMED**.

VERDICT: CHANGES-REQUESTED findings=4

**Author re-verification and consume (fix commit 464ec259).** All three
consumed findings reproduced and fixed: `_looks_like_path(token, root)` now
resolves single-slash dot-free tokens against the scanned tree
(`docs/archive` reports; `subjective/perceptual` / `requirement/test` resolve
nowhere and stay exempt); URL spans are pre-suppressed whole via `_URL`; a
present registry yielding zero scannable need cells reports VACUOUS (strict
exit 1) while absent stays a clean skip and a `-000`-only scaffold registry
stays a blank form. +4 tests (13); the three defect-regression tests fail on
the pre-fix checker (`2 failed`/`3 failed` runs driven at 692452fa), the
blank-form test is a no-regression guard and passes pre-fix by design.
LLR-170/TC-164/IF-122 and the spec Deliverable re-stated. Commit bar green:
smoke `1127 passed, 7 skipped`, `check_docs` OK, `trace.py` rc=0,
`check_trajectory.py --strict` rc=0, gate fresh.

---

## Round 2 — at da4d5d2f (CHANGES-REQUESTED, 2 MAJOR 2 MINOR)

REWORK re-verdict per charter R5: re-drive round 1's break scenarios, probe
the new seams the fixes introduced, confirm the regression tests fail
pre-fix.

### Failure classes hunted, worst-first

1. The existence-based path promotion misfiring (resolving English pairs,
   case-insensitive filesystems, odd charset members, wrong cwd/root).
2. The URL span suppression leaking or over-suppressing.
3. The vacuous-registry detection misfiring (markdown carrier, mixed rows,
   warn-first wiring).
4. Regression-test honesty; registry/doc cells overclaiming the fixed
   behavior.

### Exact commands and driven output

1. Round-1 scenarios re-drove clean: resolved one-level paths report,
   scheme URLs suppress, vacuous/absent/scaffold arms behave, allow-span
   counter-case reports, legacy markdown carrier arm behaves, all three
   bars' `need-form` steps strict-less; 13-test module suite passed; the
   historical checker fails the three defect tests; `trace.py`,
   `check_trajectory.py --strict`, `derive_gate.py --check` rc=0.
2. NEW: `A user resumes from docs/status.md.` (sentence-final) reported
   `'docs/status.md.'` — the trailing full stop rides into the phrase, so
   the report misnames the token and its correct allow entry
   `docs/status.md — reason` does NOT silence it (driven: exit 1 under
   strict WITH the entry present). Author corollary, driven: a
   sentence-final either/or pair (`requirement/test.`) would read its stop
   as a file suffix and false-positive.
3. NEW: `www.example.test/docs/status.md` reported as an internal path —
   the scheme-less form of exactly the round-1 URL class.
4. NEW (cells): LLR-170's detail and IF-121's contract both state the
   allow-list separator as ASCII `' - reason'` while the parser requires
   the em-dash ` — ` (`ALLOW_SEP`) — the exact hyphen-authored
   silent-voiding confusion the loud-direction rule exists to prevent.

### Findings

- [MAJOR] project-trajectory/scripts/check_need_form.py (path charset) -> sentence-final paths report with trailing punctuation (`docs/status.md.`), misnaming the phrase and defeating its reviewed exception -> strip the trailing full stop before judging and reporting. **CONSUMED**.
- [MAJOR] project-trajectory/scripts/check_need_form.py (`_URL`) -> scheme-less `www.example.test/docs/status.md` reports although LLR-170 promises an external address's tail never reports -> suppress `www.` forms too. **CONSUMED**.
- [MINOR] docs/requirements/low-level-requirements.toml (LLR-170) -> states the ASCII `' - reason'` separator; the parser requires ` — ` -> state the literal em-dash. **CONSUMED**.
- [MINOR] docs/requirements/interfaces.toml (IF-121) -> repeats the incorrect ASCII separator in the contract cell -> align with `ALLOW_SEP`. **CONSUMED**.

VERDICT: CHANGES-REQUESTED findings=4

**Author re-verification and consume (fix commit ce8e351c).** All four
reproduced and fixed: path-class phrases are `rstrip(".")`-ed before
`_looks_like_path` and before the allow/seen/report path (which also keeps
`requirement/test.` exempt); `_URL` gained the `\bwww\.` alternative (a
genuine `docs/status.md` sharing the cell still reports, driven); both
registry cells state the literal em-dash separator. +2 tests (15). Commit bar
green: smoke `1129 passed, 7 skipped`, `check_docs` OK, module suite 15,
live registry clean at both severities, trace/trajectory/gate rc=0.

---

## Round 3 — at 7f593331 (CHANGES-REQUESTED, 1 MAJOR)

REWORK re-verdict: re-drive round 2's scenarios, probe the rstrip and `www.`
seams.

### Exact commands and driven output

1. Round-2 scenarios held; the two round-2 regression tests fail against the
   pre-round-2 checker; 15 module tests passed; live registry clean at 27
   cells; trace rc=0, trajectory strict rc=0, derive-gate check rc=0; the
   separator cells now match `ALLOW_SEP`; all three bar plans invoke
   `need-form` without `--strict`.
2. NEW (both arms driven, and reproduced by the author): a single-label
   LOCAL path `www.assets/logo.png` — with `www.assets/` existing in the
   scanned tree — is swallowed by the `www.` suppression (`clean`); and the
   span's `\S+` greed swallows a SEPARATE genuine token abutting the URL
   through a comma: `www.example.test/docs/status.md,docs/gate.md` scanned
   `clean`. Both are silent-miss classes on the checker's own worst axis.

### Findings

- [MAJOR] project-trajectory/scripts/check_need_form.py (`_URL`) -> URL-span suppression hides genuine internal paths: single-label `www.assets/logo.png` suppressed even when local, and a comma-delimited neighbour (`…status.md,docs/gate.md`) swallowed by span greed -> require a multi-label `www.` host and stop URL spans at prose delimiters; add both regressions. **CONSUMED**.

VERDICT: CHANGES-REQUESTED findings=1

**Author re-verification and consume (fix commit 90f9bbbb).** Both arms
reproduced and fixed:
`_URL = (?:\b[a-z][a-z0-9+.-]*://|\bwww\.(?=[^\s/,;]+\.))[^\s,;]+` — spans
stop at `,`/`;` and the `www.` form requires a second dot before its first
slash (a real scheme-less address practically always carries one; the
residual — a genuine URL containing a comma has its post-comma tail scanned —
fails only in the noisy WARN direction, never silently). +2 regression tests
(17 total), both fail against the pre-round-3 checker (driven: `2 failed`).
LLR-170/TC-164 and the Deliverable re-stated. Commit bar green: smoke
`1131 passed, 7 skipped`, `check_docs` OK, live registry clean at both
severities, trace/trajectory/gate rc=0.

---

## Round 4 — at 6d83438f (APPROVE)

The final verdict round on the fixed tip, per the WI-442 four-round
precedent.

### Exact commands and driven output

1. Round-3 scenarios re-drove clean: `www.assets/logo.png` (local,
   single-label) REPORTS as an internal path; the comma-abutting
   `docs/gate.md` and semicolon-abutting `docs/log.md` report while their
   URL neighbours stay suppressed; both regression tests fail against the
   pre-fix checker (ce8e351c).
2. New-seam probes survived: a bare multi-label host with no slash stays
   suppressed; a sentence-final URL's trailing stop is harmless inside the
   span; the delimiter-stop residual on comma-bearing URLs fails only in
   the noisy direction (a WARN, never a silent miss).
3. Rounds-1/2 regression sweep held: sentence-final phrase exact + allow
   match, `requirement/test.` exempt, resolving vs non-resolving one-level
   tokens, vacuous/absent/`-000`-only arms, allow-span outside-citation
   reporting, dirty-cell 5 findings with row+phrase, strict exit codes.
4. Whole-tree: module suite `17 passed`; live registry clean at 27 cells at
   both severities; `trace.py` rc=0; `check_trajectory.py --strict` rc=0;
   `derive_gate.py --check` current; all three bar plans invoke `need-form`
   without `--strict`; SR-150 acceptance and TC-164 expected clauses each
   mapped to a covering test or driven observation, none UNCOVERED.
5. The reviewer's sandbox could not complete the FULL unfiltered suite
   (constrained test workers) and did not claim it. **Author supplement,
   driven on the final tip 6d83438f from the main venv:**
   `python -m pytest -q -n auto` → `2492 passed, 11 skipped in 0:06:59`
   (the 8 review-round tests joined the 2484 of the close commit), and
   smoke `1131 passed, 7 skipped`.

### Findings

(none)

**Author re-verification.** Every reviewer claim in this round was
independently spot-driven against the final tip before recording; the full
suite the reviewer could not run is driven above. The review's cumulative
record: 9 findings across three rounds — 8 consumed with regression tests
that fail on their pre-fix code, 1 refuted with driven counter-evidence.

VERDICT: APPROVE findings=0
