## 2026-08-18k — The artifact-voice rule reaches the NEED tier (owner directive, in-session)

**The directive, as given.** Recorded verbatim because it is the ruling that
authorizes the tier extension — there is no earlier written form of it:

> the no-concrete-artifact rule that re-tier v2 R2 established for SR cells
> extends to the SN tier as well — SN cells (the acceptance intent especially)
> state the observable condition, never the instrument/artifact, unless
> unavoidable with a recorded, arguable reason.

Filed as a **log fragment with no WI row**, following this month's precedent for
in-session owner-directive sweeps (`2026-08-18-doc-diet`, `-okf-off`,
`-scripts-sweep`, `-spine-hardening`, `-budget-guard`): the directive is the
authority and the fragment is its record; a WI row would be a second home for
the same fact. Every edit below is **provisional** — every spine tier is
human-held here (`human_ratification_through = 4`), no `status` cell moved, and
nothing was attested. The re-attest sitting countersigns the fifteen amended
need rows.

---

### 1. The rule, extended in its three documented homes

**`project-trajectory/PROCESS.md` §3** (the canonical statement, lines 129–142).
The bullet was already there and now names both tiers rather than one:
"A **need or requirement** cell names no concrete artifact unless its **reason
cell** records why constraining that artifact is necessary" — with the SN half
stated where it bites ("an SN `acceptance` states the observable *condition*,
never the instrument that observes it") and the waiver home named per tier
(`Rationale` at SR, `why` at SN). Minimal by construction: no new bullet, no new
section. **Byte delta `81,385 → 81,602` (+217)**, watched file, re-stamped in all
three `byte-budget-guard/SKILL.md` copies (source + `.claude` + `.agents`, held
byte-identical at 4,124 against a 5,000 cap).

**`skills/spine-authoring/SKILL.md`** — five edits, all three copies identical:
the authority line now cites the two-tier rule; §1 gains **(e)**, the SN-intake
question ("does the acceptance intent name an INSTRUMENT?") carrying the `why`
waiver home and the two classes that need no waiver; §2(b) *Voice* says "SN and
SR alike"; §2(d) lists the SN detector as advisory (iii) and re-words the
re-stamp clause onto "the tier's reason cell"; §3's two acceptance bullets say
they hold at SN acceptance-intent too.

**The detector** — `trace_text.sn_artifact_advisories`, wired into `trace.py`'s
`analyze()` → `Findings` → report section → console loop. Warn-only, never the
exit code, verified: 13 rows fired on the live registry and `trace.py` still
exited 0. Four design calls, each measured or argued rather than assumed:

- **A wider artifact vocabulary than the SR arm** (`.py .toml .ini .csv .html
  .yml .yaml .sh .cmd .ps1 .bat .json`). Measured over the 27 live needs:
  anchoring on `.py` alone catches 9 of the 14 rows that name a carrier and
  misses `docs/stack.ini`, `docs/process.toml`, `docs/agents.toml` and
  `PROJECT_STATE.html` — which are exactly what a need reaches for.
- **`.md` measured and REJECTED.** It adds four tokens across three rows, two of
  them SN-027's "Spec of record: …" — *provenance* citations §3 explicitly
  sanctions. The extension would have charged a waiver for doing the right thing.
- **`acceptance` only.** `check_need_form.py` already owns the `need` cell on
  SN-033's commission; scanning it here too would report one token from two
  checks. Its docstring's claim that acceptance evidence "legitimately names the
  machinery that produces it" — the ruling-day 16-of-27 measurement read as a
  licence — is corrected in place rather than left to contradict this ruling.
- **No per-artifact census at SN.** "Two rows sharing one artifact identity" is
  R1's *one home per method*, a requirement-tier defect. Two needs may honestly
  describe outcomes one file happens to serve. Importing that census would have
  invented a rule the directive does not contain.

Wiring detail worth keeping: `load_registries` now holds the needs **whole**
(`reg.sn_needs`) beside the two-key `raw_sns` projection. A text rule fed the
projection — or `spine_carrier.folded_needs`, which drops `status` — scans a
blank cell on every row and reports a clean tier it never looked at. That is the
same trap the 2026-08-18h enum-floor fix records one rule over, arriving one rule
later. `trace.py` ratchet re-stamped **4272 → 4298 (+26)**; `trace_text.py` (983)
and `check_need_form.py` (326, held line-neutral) stay under THRESHOLD.

Tests: three new cases in `tests/test_trace_rules.py` — the positive arm over all
three artifact shapes plus condition-voice/suffix-word/`-000`/empty negatives; the
scope arm (`need` and `why` unscanned, `.md` excluded); and the waiver arm (`why`
carries `13v`, an unrelated `why` does not silence, no shared-artifact census).
The three `tests/golden/*.txt` regenerated: **additive only**, one new report
section per file.

---

### 2. The sweep — this repo's own 27 need rows

**Fifteen rows rewritten, twelve untouched.** The line held, and it is the line
the skill now states: **artifact carriers (scripts, paths, config files,
generated pages) become the condition they produce; declared vocabulary tokens
(a dial name, a status word, a `--flag`) and provenance citations stay**, because
neither is a carrier. No row's meaning changed, no `status` cell moved.

| Row | Cell | Before → after |
|---|---|---|
| SN-001 | acceptance | `` `bootstrap.py --dest <repo>` produces a scaffold `` → **A single scaffolding action against a destination repository** produces a scaffold |
| SN-002 | acceptance | `` `trace.py --strict` reports zero orphans `` → **The strict traceability check** reports zero orphans |
| SN-003 | acceptance | declared once in `` `docs/stack.ini` ``; a stack swap edits **that file** → declared once, **in a single declared configuration file**; a stack swap edits **that declaration** |
| SN-004 | acceptance | `` `check.py --gate GN` `` enforces that gate's required steps → **A harness run for a named gate** enforces that gate's required steps |
| SN-005 | acceptance | the declared moment-to-tier table **(`docs/stack.ini [ci-tiers]`)** → the declared moment-to-tier table *(parenthetical dropped; SN-003 already declares the single-file home)* |
| SN-006 | acceptance | `` `agent_loop.py` `` resumes from `` `docs/status.md` `` → **The unattended loop** resumes from **the repository's tracked status surface** |
| SN-007 | acceptance | `` `pytest -q` `` green is required → **a green run of that whole suite** is required |
| SN-008 | acceptance | `` `check.py` `` **fails** (not skips) → **The harness** **fails** (not skips) · `--lenient` KEPT (a declared mode of the now-named subject, not a carrier) |
| SN-009 | acceptance | `` `check_privacy.py` ``'s always-on secrets floor → **The always-on secrets floor** · `privacy_check` KEPT (a policy token) |
| SN-010 | acceptance | `` `check_docs.py` `` fails on a broken link → **The documentation check** fails on a broken link · `--check`, `PROJECT-VISION` KEPT (declared vocabulary) |
| SN-011 | acceptance | a row in `` `docs/dependencies.md` `` … `` `tests/test_dependency_ledger.py` `` fails the suite → a row in **the dependency ledger** … **the suite fails** on an undeclared import |
| SN-023 | acceptance | The root `` `PROJECT_STATE.html` `` renders → **The single root dashboard** renders |
| SN-024 | acceptance | against a `` `docs/rubrics/` `` rubric → against **a written rubric** *(the need cell already said "a written rubric")* · `Verification=Critique` KEPT (a cell value) |
| SN-026 | acceptance | `` `docs/agents.toml` `` declares … `` `docs/agents-enabled` `` is the consent surface → **A declared agent roster** carries … **a separate consent surface** |
| SN-028 | acceptance | `` `docs/process.toml` `` holds every dial … (`` `tomllib` `` and the hooks' sh) … `` `bootstrap.py --migrate-config` `` → **A single declared process-dial file** holds every dial … (**a TOML parser** and the hooks' **plain-sh parse**) … **a declared migration action** |

**Kept, with the reason — no waiver token owed.** Both are provenance, which §3's
provenance clause sanctions and the detector's `.md`-free vocabulary therefore
does not flag. Recording them here rather than minting a `13v` keeps the token
meaning what it says:

- **SN-025** acceptance names `docs/next-wi` as "the file this need made
  unnecessary, retired by WI-180". The artifact is named as the thing the need
  **abolished**; deleting the name deletes the evidence that it stayed gone.
- **SN-027** acceptance ends "Spec of record: `docs/archive/specs/
  parallel-wi-dispatch.2026-07-20.md` + `docs/concurrency-restructure.md`" — a
  citation, not an instrument. `--jobs 1` kept on the vocabulary rule.

**Untouched, already conformant (12):** SN-012, SN-025, SN-027, SN-029, SN-033,
SN-034, SN-035, SN-036, SN-037, SN-038, SN-039, SN-040. Worth naming the shape:
**every row minted after the re-tier discipline (SN-033…SN-040) was already
clean**, and SN-029 — the longest acceptance cell in the registry — names no
carrier at all. The defect is generational, not structural, which is the honest
argument that the rule is writable rather than aspirational.

Verification: `sn_artifact_advisories` fires **13 rows before, 0 after**;
`check_need_form` clean (27 cells); `check_vocab` clean; `derive_gate --check`
up to date (the basis line is unmoved — no `status` cell was touched).

---

### 3. The resync carries the obligation

`RESYNC_PACK.md` gains a **Reserved** entry (awaiting its `[since <sha>]`)
appended after the architecture-retirement entry, in the pack's own newest-last
placement. It states the rule change, that the detector warns on **both** tiers
and gates on neither, and — as the action its reader performs — the four-step
conformance sweep over their own older SN **and** SR rows, naming the `13v`
waiver token and its per-tier home (`Rationale` at SR, `why` at SN) and the two
classes that must **not** be waived. `skills/downstream-resync/SKILL.md` is
**untouched by design**: it is a pure router ("Nothing else belongs in this
file") and processes pack entries generically, so a sweep-class entry needs no
new instruction.

---

### Verification run

`python -m pytest -q -n auto` (full, unfiltered): **2576 passed, 10 skipped in
437.99s**. `ruff format --check` on the five touched Python files: *5 files
already formatted*. `ruff check` on the same five: 5 findings, **all five present
at HEAD** (confirmed by re-running against a stashed tree) — the change adds
none. `check.py` at the derived bar: **RESULT: PASS**; the advisory reds
(`lint`, `doc-refs`, `figures`, `traceability`, `trajectory`) are the branch's
known pre-existing set — WI-455 provenance cites and the re-tier program's
`Modified` SR rows — none of them touching a file this change edits.

**Byte deltas, one line per touched budgeted file:**
`project-trajectory/PROCESS.md` 81,385 → 81,602 (+217: §3's artifact-voice rule
extends from SR up to SN — the need tier's `acceptance` cell and its `why`
waiver home, stated inside the one bullet that already carried the rule).
`byte-budget-guard/SKILL.md` 4,036 → 4,124 (886 of headroom left under its 5,000
cap; the re-stamp itself).
