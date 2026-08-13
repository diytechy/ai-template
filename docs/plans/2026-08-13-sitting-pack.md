# The sitting pack — run the whole re-attest sitting from this one document

Assembled by the coordinator during the 2026-08-13 pre-absence charge-through;
the authority for everything applied is the log's **Decisions entry of
2026-08-13** (the batch ruling). This is **v2: self-contained.** v1 was an index
that sent you to five other files to decide anything. Every fact you need to
decide is now quoted or summarised *here*.

## 0. How to run this sitting

1. **Read this document top to bottom first.** It carries the context for every
   decision; you should never have to open another markdown file to rule.
2. **Then open [`../open-items.html`](../open-items.html)** — the ONE outbound
   pointer, and deliberately so. It is *generated* and it is the actual
   **signing surface**: per-cell before/after word-level diffs for every `Draft`
   and `Modified` row, with the baseline revision printed on every section, and
   a toolbar box that reveals the untouched cells too (a diff says what moved;
   an attestation asks whether the evidence still verifies what the row now
   *says*). It cannot be honestly reproduced in markdown, which is why it stays
   a pointer.
3. **§1 tells you what each `Modified` row in that html WILL SAY before you open
   it.** Read §1, then sign; don't discover the batch in the diff viewer.
4. **§2 is the six decisions.** Each is self-contained: question, context,
   recommendation, cost of yes and of no. None blocks the others.
5. **§3 and §4** are the provisional partition and the hats roster — accept,
   edit or overturn. **§5** is the mechanical state and what closing looks like.
6. **The one rule: fatigue is the enemy.** The 12 previously-laundered rows come
   FIRST, while you are fresh. They are the rows where a rewrite was already
   caught changing meaning once.

---

## 1. The re-attest batch — what you are signing

### 1a. The 12 previously-laundered rows — read these first

Round 1 of the 2026-08-10 prose rewrite claimed 26 preserving / 3 changing
rewrites. The adversarial reviewer (codex `gpt-5.6-sol`, 2026-08-11) showed **12
of the "preserving" rows had dropped or invented a qualifier** — the document
was mis-stating its own risk by a factor of four. Revision 2 restored every one
verbatim rather than reclassifying. At application (WI-444) each row's registry
text was re-compared to the plan's final text by token multiset:
**12 / 12 pass — no obligation-bearing word removed on any of them.**
*(sources: prose-rewrite §A rule 4 + §B; wi444 ledger part 1)*

| row | what round 1 was caught doing | verify in the html that… |
|---|---|---|
| **SN-001** | **invented** *"the same day"* — a time bound with no clause behind it | no time bound appears; the change is subject/verb only ("A team can drop the kit into" → "An adopting team can add this process to") |
| **SN-004** | **invented** an authority claim: wrote *"The repo owner decides when work advances"* | the predicate is verbatim — *"explicit approval gates"* and *"a gate passes only when its mechanical bar is met"*; no owner-authority clause |
| **SN-006** | softened *"typed code"* → "a **named** outcome", and *"repo text alone"* → "repository-written state" | both are back verbatim — *"typed code"* in the acceptance cell, *"repo text alone"* in the need cell (1a-ii quotes both); a name is not a typed exit code. (The plan proposed **no change** to either cell — both are byte-identical to the baseline) |
| **SN-024** | **three drops in one row**: broadened the scoped cases to every *"judgement call"*; weakened *"independent critical eye"* / *"never by the session that authored the artifact"* to "someone other than the author"; **added** a new requirement that the rubric be written *"in advance"* | the scope clause, *"independent critical eye"* and *"never by the session that authored the artifact"* are all verbatim, and *"in advance"* is **absent** |
| **SN-026** | dropped *"per capability level"* and *"wherever that is configured"* — the second is load-bearing, it makes the cross-family routing **conditional on configuration** rather than unconditional | both phrases present |
| **SN-027** | dropped **bounded**, **parallel lanes**, and **serialized and gated** — the three constraints that are the entire content of the need | all three present |
| **SN-028** | reduced *"a single hand-edited, machine-read file"* to *"one place"* — all three qualifiers at once; then claimed form (ii) would remove names form (i) had already removed | *"single hand-edited, machine-read file"* is verbatim; the acceptance cell still names `docs/process.toml`, bare `[section]`, `tomllib`, the hooks' sh, the adversarial-file pinning and `bootstrap.py --migrate-config` (measured: **zero** tokens removed) |
| **SN-013** † | dropped *"skip-or-report"* — making reporting unconditional **changed the allowed outcome** | see the note below — this row no longer exists; verify **SR-021** |
| **SN-014** † | dropped the measurable **`SKIP(missing)`** token | see below — verify **SR-006** |
| **SN-016** † | dropped **stdin closed**, the headless *mechanism* | see below — verify **SR-026** |
| **SN-020** † | dropped both the *logged `ERROR`* and the **all-`ERROR`** qualifier | see below — verify **SR-028** |
| **SN-022** † | dropped the **`-000`** class token and the bar-scope qualifier (round 1's text read *"from [DevBar-Tests] on"*, in the retired tag of that day) | see below — verify **SR-003** |

**† Five of the twelve are no longer rows.** SN-013…SN-022 were the edge-case
tier, and the **OI-18 dissolution deleted them** later the same day (§1b). So
their restored qualifiers were applied and then the carrier was retired. Where
each qualifier lives now:

- **SN-013** → **SR-021** carries it, and its acceptance cell says so verbatim:
  *"(The launcher half folded in from retired SN-013's expectation at the
  2026-08-13 dissolution — the review round caught that SR-021 alone carried
  only the hooks.)"* The *"skip-or-report"* words are in SR-021's requirement.
- **SN-016** → **SR-026**'s acceptance, likewise flagged in-cell: *"(The
  backoff/budget clauses folded in from retired SN-016's expectation at the
  2026-08-13 dissolution — the review round caught that no SR carried them.)"*
  *"stdin closed"* is in SR-026's requirement.
- **SN-014** → **SR-006** requirement: *"…reporting SKIP(missing) rather than
  silently passing."* ✅ token present.
- **SN-020** → **SR-028**, split across two cells (1a-ii quotes both): the
  **all-ERROR** stall clause in its requirement — *"…report an all-ERROR stall
  as an unavailable agent rather than a work stall"* — and the *logged
  `ERROR`* half in its acceptance_criteria. ✅ both qualifiers present.
- **SN-022** → **SR-003** requirement: *"…under --no-placeholders, flag any
  leftover -000 example row…"* ✅ the `-000` token is present in both its
  requirement and acceptance — but ⚠ NEITHER cell restates the bar-scope
  qualifier (the old *"from [DevBar-Tests] on"* clause). This is the weakest
  of the three already-carried judgements (1a-ii quotes the cells).

**Honest gap:** SN-013 and SN-016 were caught by an adversarial round; SN-014 /
SN-020 / SN-022 were judged already-carried by the SRs above rather than folded.
That judgement is the four sentences quoted immediately above — it is checkable
by eye, and it is yours to reject. *(ledger part 2, OI-18)*

### 1a-ii. Before → after, row by row

The table above says *what was caught*. This says *what the cell reads now*, so
you never have to diff by hand. **Before** is the pre-batch baseline
`81a142c2` — the last commit before the prose batch applied. **After** is the
live registry. Cells are quoted whole; nothing inside a quote is trimmed.

Only the cell (or cells) carrying the laundered qualifier is quoted. Where a
cell is byte-identical between the two revisions it is stated as such rather
than printed twice.

---

**SN-001** — `need` cell.

Before (`81a142c2`):
> "A team can drop the kit into a new or existing repo and get a working gated, requirement-traced process without hand-building the tooling."

After (live):
> "An adopting team can add this process to a new or existing repository and get a working gated, requirement-traced process, without hand-building the tooling."

**What moved:** round 1 **invented** *"the same day"* — a time bound with no
clause behind it. Restored, the delta is subject/verb only ("A team can drop the
kit into" → "An adopting team can add this process to"); no time bound appears.
The `acceptance` cell is byte-identical to baseline.

---

**SN-004** — `need` cell.

Before (`81a142c2`):
> "Progress advances only through **explicit approval gates** (G1→G2→G3→…), and a gate passes only when its mechanical bar is met."

After (live):
> "A team advances only through **explicit approval gates** (DevBar-Reqs→DevBar-Tests→DevBar-Release→…), and a gate passes only when its mechanical bar is met."

**What moved:** round 1 **invented** an authority claim — *"The repo owner
decides when work advances"*. Restored, the predicate is verbatim (*"explicit
approval gates"*, *"a gate passes only when its mechanical bar is met"*) and no
owner-authority clause appears; the subject shifts "Progress" → "A team". The
gate-tag change inside the parenthesis is **not** the prose batch: it is the
WI-445 stage-ladder sweep (§1b), a vocabulary substitution. The `acceptance`
cell is byte-identical to baseline.

---

**SN-006** — the two caught phrases live in different cells, so both are quoted.

Before (`81a142c2`, `need`):
> "An agent can run **unattended** and resume from repo text alone; such a run never blocks on a prompt and fails clearly."

Before (`81a142c2`, `acceptance`):
> "`agent_loop.py` resumes from `docs/status.md`, exits a **typed code** at each end state, and a preflight refuses a broken footing (no agent CLI, not a git repo, private author under privacy-check) rather than hanging."

After (live): **both cells are byte-identical to the baseline above** — the plan
proposed no change to either, and none was written.

**What moved:** nothing. Round 1 had softened *"typed code"* → "a **named**
outcome" (that phrase is in `acceptance`) and *"repo text alone"* →
"repository-written state" (that phrase is in `need`); revision 2 restored both,
and the batch then wrote neither cell. A name is not a typed exit code.

---

**SN-024** — `need` cell.

Before (`81a142c2`):
> "Subjective/perceptual acceptance — a realistic-looking render, an artifact comparison with no crisp measurable interface — is adjudicated by an **independent critical eye against a written rubric**, never by the session that authored the artifact."

After (live):
> "A reviewer can trust subjective/perceptual acceptance — a realistic-looking render, an artifact comparison with no crisp measurable interface — because it is adjudicated by an **independent critical eye against a written rubric**, never by the session that authored the artifact."

**What moved:** three drops in one row, all restored — the scope clause (round 1
broadened it to every *"judgement call"*), *"independent critical eye"* and
*"never by the session that authored the artifact"* (weakened to "someone other
than the author"), and the **added** requirement that the rubric be written *"in
advance"*, which is absent from the live cell. The live delta is the stakeholder
subject only ("A reviewer can trust … because it is"). The `acceptance` cell is
byte-identical to baseline.

---

**SN-026** — `need` cell.

Before (`81a142c2`):
> "**Several LLM families are configurable** — selected per job and per capability level — and work that benefits from an independent second opinion is automatically routed to a *different* family wherever that is configured."

After (live):
> "The repo owner can configure **several LLM families** — selected per job and per capability level — so that work benefiting from an independent second opinion is automatically routed to a *different* family wherever that is configured."

**What moved:** round 1 dropped *"per capability level"* and *"wherever that is
configured"* — the second is load-bearing, it makes the cross-family routing
**conditional on configuration** rather than unconditional. Both phrases are
present. The `acceptance` cell also changed, by exactly one token —
`docs/agents.csv` → `docs/agents.toml` — which is the OI-23 carrier rename
(§1b), not the prose batch.

---

**SN-027** — `need` cell.

Before (`81a142c2`):
> "Ready work **fans out across bounded parallel lanes**, while mutation of the integration branch stays **serialized and gated**."

After (live):
> "A team gets more than one piece of ready work moving at once: ready work **fans out across bounded parallel lanes**, while mutation of the integration branch stays **serialized and gated**."

**What moved:** round 1 dropped **bounded**, **parallel lanes** and **serialized
and gated** — the three constraints that are the entire content of the need. All
three are present; the live delta is a prepended stakeholder clause. The
`acceptance` cell is byte-identical to baseline.

---

**SN-028** — both cells carried a catch, so both are quoted.

Before (`81a142c2`, `need`):
> "**Every policy dial has one home** — a single hand-edited, machine-read file — and a repo that declares the same dial twice is REFUSED rather than resolved by precedence."

After (live, `need`):
> "The repo owner can find and change every policy dial in **one home** — a **single hand-edited, machine-read file** — and a repo that declares the same dial twice is REFUSED rather than resolved by precedence."

Before (`81a142c2`, `acceptance`):
> "`docs/process.toml` holds every process dial under bare `[section]` headers, one `key = value` per line; the SHAPE is checked rather than conventional, because two grammars read the file (`tomllib` and the hooks' sh) and every shape only one of them understands is a silent flip of a security gate; the two readings are pinned equal over a table of adversarial files; a legacy one-word file still present alongside its key is a REFUSAL naming both, and `bootstrap.py --migrate-config` (run by bootstrap and by the documented re-sync) converts and deletes the legacy files so an adopter never meets that refusal un-aided; a wrong-typed or out-of-range dial is refused, never defaulted."

After (live, `acceptance`):
> "`docs/process.toml` holds every process dial under **bare `[section]` headers**, one `key = value` per line. The SHAPE is checked rather than conventional, because two grammars read the file (`tomllib` and the hooks' sh) and every shape only one of them understands is a silent flip of a security gate; the two readings are pinned equal over a table of adversarial files. A legacy one-word file still present alongside its key is a REFUSAL naming both, and `bootstrap.py --migrate-config` — run by bootstrap and by the documented re-sync — converts and deletes the legacy files so an adopter never meets that refusal un-aided. A wrong-typed or out-of-range dial is refused, never defaulted."

**What moved:** round 1 reduced *"a single hand-edited, machine-read file"* to
*"one place"* — all three qualifiers at once — and then claimed form (ii) would
remove names form (i) had already removed. The phrase is verbatim in the live
`need`. In `acceptance` the only edits are punctuation and emphasis: seven
semicolon-to-full-stop / parenthesis-to-em-dash splits and one bolding
(**zero** tokens removed). `docs/process.toml`, bare `[section]`, `tomllib`, the
hooks' sh, the adversarial-file pinning and `bootstrap.py --migrate-config` are
all still named.

---

**TRANSFORMED: SN-013 (edge need, deleted at the OI-18 dissolution) → SR-021 (its carrier)**

Before (`81a142c2`, SN-013 `scenario`):
> "No Python 3 interpreter on PATH (or the Windows Store alias that resolves but exits nonzero)"

Before (`81a142c2`, SN-013 `expected`):
> "The git hooks / coordinator **probe by running** a candidate and skip-or-report clearly; they never crash cryptically."

After (live, SR-021 `requirement`):
> "The git hooks and the root launchers (dev-setup / agent-resume, the coordinator's entry) shall locate a working python3 by running a candidate and skip-or-report clearly when none resolves or a Store-alias exits nonzero."

After (live, SR-021 `acceptance_criteria`):
> "With no working python3 the hook and each root launcher report clearly and do not crash cryptically; with one, they run their action. (The launcher half folded in from retired SN-013's expectation at the 2026-08-13 dissolution — the review round caught that SR-021 alone carried only the hooks.)"

**What moved:** round 1 dropped *"skip-or-report"*, making reporting
unconditional and so **changing the allowed outcome**. The words are in SR-021's
requirement; the launcher/coordinator half of the probe was folded into SR-021
at the dissolution and the fold is annotated in-cell with its date and reason.

---

**TRANSFORMED: SN-014 (edge need, deleted at the OI-18 dissolution) → SR-006 (its carrier)**

Before (`81a142c2`, SN-014 `scenario`):
> "A required harness tool is absent"

Before (`81a142c2`, SN-014 `expected`):
> "`check.py` reports `SKIP(missing)` and **fails the gate** — a missing tool is never a silent pass (SN-008)."

After (live, SR-006 `requirement`):
> "check.py shall run the required steps of the gate that must next be passed (the strictness selector cached in docs/gate) and fail that gate when a required tool is missing, reporting SKIP(missing) rather than silently passing."

**What moved:** round 1 dropped the measurable **`SKIP(missing)`** token. The
token is in SR-006's requirement, together with the fail-the-gate half. This is
one of the three rows judged *already carried* rather than folded — the honest
gap noted above.

---

**TRANSFORMED: SN-016 (edge need, deleted at the OI-18 dissolution) → SR-026 (its carrier)**

Before (`81a142c2`, SN-016 `scenario`):
> "An unattended run must never block on a prompt at launch **or mid-run**"

Before (`81a142c2`, SN-016 `expected`):
> "`agent_loop.py` runs headless (stdin closed); a rate limit backs off, a stall aborts to protect the budget — the loop is never wedged by a prompt."

After (live, SR-026 `requirement`):
> "agent_loop.py shall resume headless with stdin closed, never blocking on a
> prompt.
> Resume authority (one path - the serial resume loop is retired): a worker
> resumes from its explicit claimed assignment plus the committed trailer evidence
> on its branch, and the integrator (SR-132) derives claim/queue state from trunk
> history alone.
> docs/status.md is a generated reference surface (SR-059), never a session input."

After (live, SR-026 `acceptance_criteria`):
> "A worker reconciles from its assignment + committed evidence and the integrator from trunk history; every mode runs with stdin closed and a prompt cannot wedge it; a model rate limit backs off rather than failing the run, and a stall aborts to protect the budget. (The backoff/budget clauses folded in from retired SN-016's expectation at the 2026-08-13 dissolution — the review round caught that no SR carried them.)"

**What moved:** round 1 dropped **stdin closed**, the headless *mechanism* —
leaving the property with no stated means. It is in SR-026's requirement, and
the rate-limit/stall clauses were folded into SR-026's acceptance at the
dissolution, annotated in-cell.

---

**TRANSFORMED: SN-020 (edge need, deleted at the OI-18 dissolution) → SR-028 (its carrier)**

Before (`81a142c2`, SN-020 `scenario`):
> "The agent CLI / model errors before doing work (retired model, expired auth)"

Before (`81a142c2`, SN-020 `expected`):
> "The session is logged `ERROR` and an all-`ERROR` stall is reported as an **unavailable agent**, not a work stall. *(tests/test_agent_loop.py — error region)*"

After (live, SR-028 `requirement`):
> "agent_loop.py shall end each session in a typed outcome code, guard a zero-commit HEAD, and report an all-ERROR stall as an unavailable agent rather than a work stall."

After (live, SR-028 `acceptance_criteria`):
> "A repo with no commits does not crash the loop; an agent-CLI error is logged ERROR; an all-ERROR region is reported as an unavailable agent."

**What moved:** round 1 dropped both the *logged `ERROR`* and the **all-`ERROR`**
qualifier. Both survive, but in different cells: the **all-`ERROR`** stall
clause is in SR-028's requirement, and the *logged `ERROR`* half is in its
acceptance. Judged *already carried*, not folded.

---

**TRANSFORMED: SN-022 (edge need, deleted at the OI-18 dissolution) → SR-003 (its carrier)**

Before (`81a142c2`, SN-022 `scenario`):
> "A committed example row / placeholder is left in a registry at a gate"

Before (`81a142c2`, SN-022 `expected`):
> "`--no-placeholders` flags a leftover `-000` row from G2 on; a fresh scaffold stays green until it claims a gate."

After (live, SR-003 `requirement`):
> "trace.py shall, under --no-placeholders, flag any leftover -000 example row, and under --strict-schema, require non-empty required fields and in-vocabulary Verification/Tier values."

After (live, SR-003 `acceptance_criteria`):
> "--no-placeholders reports every -000 row across SR/LLR/TC and the SN doc; --strict-schema reports an empty required field or an out-of-vocabulary Verification/Tier value."

**What moved:** round 1 dropped the **`-000`** class token and the bar-scope
qualifier (round 1's text read *"from [DevBar-Tests] on"*, in the retired tag of
that day). The **`-000`** token is present in both SR-003 cells. **The bar-scope
half is not restated in either cell** — `--no-placeholders` is a flag the
harness wires per bar rather than a clause SR-003 carries. This is the weakest
of the three *already carried* judgements, and the most worth your eye.

### 1b. Everything else in the batch, by group

**The prose batch itself (WI-444 part 1).** 29 SN rows + 17 SR rows from the
2026-08-10 plan, applied as **exact replacement cells** — no wording was
authored at application; every cell written is the plan's own text. 24 SN cells
written, 6 no-ops (the plan proposed no change), 0 skipped; 16 SR cells written,
**1 skipped (SR-082 — §2.2)**. Method is legibility only: the stakeholder
becomes the grammatical subject, participial chains become separate sentences.
Seven `Verified` SRs flipped to `Modified` by it (SR-026, SR-042, SR-046,
SR-049, SR-050, SR-055, SR-110); nine were already `Modified` or `Draft`. Four
rows' plan-stated word deltas did not reproduce under token counting (SR-049,
SR-042, SR-110, SR-059) — accounting slips in the plan, **no words removed in
any of them**. One reconstruction is stated plainly: four
`tests/test_agent_loop.py::…` citations were **retained**, because form (i) is
*defined* as the form where the mechanical citation stays, and deleting them was
the unruled form (ii).

**The OI-18 dissolution + two review-caught obligation folds.** SN-013…SN-022
(the ten edge-case rows) **deleted** — under D-4, supersession is deletion; the
SN count went 37 → 27, and `uncovered=0` held before *and* after, so ten needs
leaving the denominator did not masquerade as coverage improving. 38 SR
`sn_refs` arrays shed the retired ids; two re-anchors as ruled (SR-021 → SN-001,
SR-029 → SN-025). The adversarial round then caught **two obligations the
dissolution would have orphaned**, and both were folded into carriers rather
than lost: SN-013's launcher/coordinator interpreter-probe half → **SR-021**
(which had carried only the hooks), and SN-016's *"a rate limit backs off; a
stall aborts to protect the budget"* → **SR-026**'s acceptance (no SR carried
either clause). Both folds are annotated in-cell with their date and reason.

**The OI-17 launcher reframe.** SN-025 rewritten to pure self-direction — the
launcher clause removed, the pointer to SN-034 left in place; SN-034's
acceptance now declares itself **the ONE home for launcher-class obligations**
and sheds its sitting note; SN-035 sheds its sitting note. Exactly one rewrite
of SN-025 occurred (the prose batch deliberately left it unchanged), so no
double-edit.

**The OI-23 stale-row amendments — 15 rows / 16 defects.** From the reading-
verdicts table: **8 rows confirmed TRUE and left alone**; 15 amended, in four
groups — (a) *carrier renames* (SR-002 narrowed rather than rewritten, SR-129,
SR-147's parenthetical past-tensed, LLR-002, LLR-034, LLR-118, SN-026, LLR-136
aligned); (b) *dial re-homes* on the SR-017 precedent pattern (SR-042, SR-043
×2, SR-067, SR-074, LLR-040 — which also lost a second falsity: the log path is
now `out/subagent-gate.log`); (c) *singletons* (SR-049's rationale repointed;
LLR-150's refuted parenthetical corrected, `run_worker` kept as the declared
seam); (d) the *retired "active gate" vocabulary* in SR-006/SR-049.
**Scope extension, recorded:** four adjacent `[policies]`-fold rows (SR-018,
LLR-018, SR-040, LLR-140) rode the batch — same class, same window; SR-040's
requirement half was already fixed by the prose batch. LLR-018/LLR-140 initially
omitted the migration-window parenthetical; the adversarial round caught it;
fixed. **Measured corrections to the OI-23 brief:** the "six dial rows" are six
cells across **five** rows, and `components_check` / `live_status` are named by
no spine cell at all.

**SN-005 narrowed (OI-24).** Its acceptance now states per-moment equivalence
against the declared `[ci-tiers]` table, **shipped-workflow-only**, with the
not-claimed half explicit: *"An adopter-edited workflow copy is outside this
repo's reach, and this need claims nothing about it. … (Narrowed 2026-08-13 per
OI-24: full local-CI equivalence on all inputs is not mechanizable and is not
claimed.)"* SR-019's acceptance carries the CI-mirror relation (amend, not mint,
per the ruling), pinned by `tests/test_ci_tier_declaration.py`.

**Status honesty.** Prose-amended `Verified` rows flipped `Modified`: SR-002,
SR-006, SR-018, SR-019, SR-021, SR-043, SR-067, SR-074, SR-129 + LLR-002,
LLR-018, LLR-034, LLR-040, LLR-118, LLR-136, LLR-140, LLR-150.
**Ref-array-only edits did NOT flip** (traced-cell reading).

**The WI-445 stage-ladder sweep.** The retired `G*` gate tags were swept
repo-wide to the eight-rung `DevStg-`/`DevBar-` ladder. Two spine rows carried
the old vocabulary in *authored* cells and so flipped `Modified` by the sweep:
**SR-004** (rationale now reads *"…while leaving the call to the DevBar-Reqs
review — a heuristic lint must not gate."*) and **SR-053**. They are text-only
vocabulary corrections, not obligation changes. *(handoff, WI-445)*

---

## 2. The decisions

Six. Each needs a yes/no; none blocks the rest.

### 2.1 — Six one-obligation-per-row form findings

**The question.** The prose batch's legibility method converts participial
chains into separate `It shall …` sentences. That is exactly what makes these
rows readable — and exactly what the kit's own one-obligation-per-row rule
flags. `trace.py` reported `form-findings=6` after the batch; the same command
at the pre-batch baseline reported none. **All six are rows the batch rewrote.**
*(ledger part 1)*

**The blast radius, precisely.** Form findings join the exit code only under
`trace.py --strict`, which `check.py` runs at the traceability step from the
**DevBar-Tests** bar on. At today's `DevBar-Reqs` nothing blocks — but this
sitting exists to move the bar back up, and these six will fail there.

The six rows, trimmed to their shall-clauses (verbatim from the live registry):

- **SR-040** *Per-phase routing and review dial* — **3 shalls**
  > "The unattended coordinator **shall select** the agent command template per in-process session phase (…) via AGENT_CMD_MAP/--cmd-map, falling back to the single AGENT_CMD.
  > It **shall surface** the declared reviewer dial (docs/process.toml [policies] review_rounds, default 1; …) at run start without enforcing it.
  > It **shall warn** (never block) when a lane resume surface exceeds the declared size threshold."
- **SR-042** *OKF knowledge-bundle export* — **2 shalls**
  > "gen_okf.py **shall export** the spine registries AND the key process docs as a generated Open Knowledge Format bundle under docs/okf: …
  > The bundle **shall be deterministic** (no clocks), with --check failing on any stale, missing or extra bundle file; …"
- **SR-050** *Process reference view* — **2 shalls**
  > "gen_trajectory.py **shall render** a Process reference tab in PROJECT_STATE.html beside the existing views, presenting how the project is built as three linked panels: …
  > The tab **shall be data-derived** where a canonical source exists (…); self-contained and byte-deterministic; a data-less repo renders byte-identically; --check freshness unchanged."
- **SR-057** *WI-DAG frontier scheduling* — **3 shalls**
  > "A stdlib schedule.py library/CLI **shall derive** the dependency-ready frontier from the tracked WI registry plus the active claims - never from prose.
  > It **shall exclude** blocked (queued + blockref), deferred, claimed, protected-conflicting and exclusive-conflicting WIs.
  > It **shall expose** ready --explain, ready --format json and simulate --jobs N."
- **SR-130** *Serial trunk step compiles log fragments…* — **2 shalls**
  > "A serial trunk step **shall compile** docs/log.d/ work-branch log fragments into docs/log.md in merge order derived from git history.
  > It **shall validate** every fragment before any write, rebase relative links to the log's home, delete compiled fragments, fail loudly at the first error, and never commit."
- **SR-131** *Tracked pause drains claiming to a merged stop* — **2 shalls**
  > "A tracked docs/work/pause file (TOML: reason, since) **shall pause claiming** — everything in flight finishes and integrates.
  > It **shall be read** via pause_reason as the ONE pause home (…), failing closed on malformation."

**The choice: SPLIT or WAIVE.** Splitting mints new SR ids and changes the
decomposition — **that is your act, not an agent's** (an agent minting ids to
silence its own lint is the failure mode the rule exists to catch). Waiving
means recording a reason on each row and accepting the finding standing at the
tests bar.

- **Yes (split)** costs: 8 new SR ids, their LLR/TC re-pointing, and 6 rows'
  chains re-attested. Buys: the rule holds, and the tests bar passes clean.
- **No (waive)** costs: six standing findings the harness will report at every
  tests-bar run forever, plus a documented exception the next reader must
  re-litigate. Buys: zero rework now.

**No recommendation is on the record for this one** — the ruling that authorised
the batch explicitly left it to the sitting. Note only that SR-130 and SR-131
already carry the rule in their own rationale cells (*"…is SR-134's obligation
(one row, one obligation)"*), so those two rows are self-aware exceptions.

### 2.2 — SR-082: the one skipped rewrite

**Current cell, verbatim:**
> "The coordinator shall apply fixed win-stay/lose-shift escalation and page for
> shared failure, contradictions and tripwires per the declared ratification
> level, keyed on whether the tier in process is still the human's to ratify and
> on **the separate drain dial the retired three-value enum bundled into the
> same word**."

**Prepared replacement, held (§E.1, exact):**
> "The coordinator shall apply fixed win-stay/lose-shift escalation and page for
> shared failure, contradictions and tripwires per the declared ratification
> level, keyed on **two separate dials: whether the tier in process is still the
> human's to ratify (`human_ratification_through`), and whether non-dependent
> work keeps running while a ratification is queued (`keep_nondependent`)**."

**Why it was skipped.** Δ **+6 / −13** — it is the only row in the batch that is
not word-preserving. The removed words are the periphrasis *"the separate drain
dial the retired three-value enum bundled into the same word"*; the added words
**name what that periphrasis denotes**. So applying it is *deciding* the
referent, not transcribing it.

**The condition, in one sentence:** *"the sitting confirms the drain-dial
reading"* means **you confirm that "the separate drain dial" is
`keep_nondependent`** — nothing else. The evidence the plan offers is
`docs/process.toml`'s own comment on that key: *"This is an ORTHOGONAL policy an
ordinal cannot express (it was the old `single-ratify` level's distinguishing
behaviour)"*. The plan calls that strong but an **inference about intent**, and
so marked it conditional rather than asserted.

- **Yes** costs: one `Edit`, one re-attest of an already-`Modified` row. Buys: a
  cell that names its two dials instead of describing a retired enum.
- **No** costs: nothing mechanical; the row keeps a periphrasis that will
  puzzle every future reader, and the naming question stays open.

### 2.3 — Three Draft-status lifts on shipped work

The work shipped; the text was corrected in the batch; **only the status lift is
owed**, and lifting it without you would launder the ratification. *(ledger part 2)*

| row | title | one-line gist | status |
|---|---|---|---|
| **SR-147** | "One machine-parseable carrier for the requirement spine" | the kit shall carry SN→SR→LLR→TC in ONE machine-parseable carrier rather than two, and ship a converter that proves the conversion cell-for-cell **before** the authority flip, refusing any round-trip that loses a cell | `Draft` |
| **LLR-165** | "The spine carrier converter (markdown + CSV -> TOML)" | `migrate_carrier.py` — `convert()` returns `(findings, written_paths)` so the caller decides whether a lossy conversion writes; ids stay bare and prefixed; `compare()` re-reads what it emitted and diffs it against one projection that serves both carriers | `Draft` |
| **TC-160** | *(verifies SR-147, LLR-166)* | drives the carrier reader over a real repo cut over CSV→TOML in one commit and asserts the four properties that fail open if wrong — pre- and post-migration revisions both read, a lossless cutover is silent to the amendment guard while smuggled text is NAMED, and an unparseable carrier is reported absent rather than empty | `Draft` |

**The work is done and merged** — the carrier cutover completed across every
registry (WI-443 finished it: interfaces + components moved to TOML, the CSVs
deleted). These three rows describe shipped, tested machinery.

- **Yes (lift to `Planned`/`Verified` per tier)** costs: reading three rows.
  Buys: three rows stop dragging the derived bar down for no reason.
- **No** costs: the derived bar stays floored by rows whose work is finished —
  i.e. the bar reports a maturity lower than the repo's actual state.

### 2.4 — The rationale-citation sweep

**~29 SR `rationale` cells still cite the retired SN-013…SN-022 ids as
history.** One example cell, verbatim (SR-006):

> "Realizes SN-004 (gates enforce their bar), SN-008 (no false green) and
> **SN-014 (a missing tool fails, never skips)**. The work-branch lane skip is
> SR-133's obligation (one row, one obligation)."

**The choice: keep as history, or sweep.** The dissolution ruled **keep**, under
D-4 (*"any document citing a retired id keeps its citation"*) — and note the
parentheticals carry real content: *"a missing tool fails, never skips"* is
worth more than the id it hangs off. The counter-argument is that a reader who
follows `SN-014` finds nothing, and a dead id in a live rationale looks like rot.

- **Keep (the standing ruling)** costs: 29 cells citing ids that no longer
  resolve. Buys: zero churn, no re-attest, the history stays readable.
- **Sweep** costs: purely mechanical (drop the id token, keep the parenthetical)
  — but it is 29 edits to `rationale` cells, and rationale is a traced cell, so
  it flips those rows `Modified` and **opens a second re-attest window**.

**Recommendation on the record:** keep. Sweeping trades a cosmetic dead link for
a fresh round of 29 re-attestations.

### 2.5 — WI-419 chain-flip scoping

**The context, two sentences.** The WI-419 precedent flipped **every**
non-superseded `Verified` SR in an amended need's chain — including rows whose
own text did not change (SR-035, SR-114 that day). This batch flipped **only the
SRs whose own ratified text it rewrote**, because applying the WI-419 rule to 15
rewritten core needs would flip most of the 147-row SR registry, and the batch
is certified text-only so the children's grounding is unchanged.

**The call: confirm the narrow scoping, or order the wider flip.**

- **Confirm (recommended, and what is currently applied)** costs: nothing.
  Buys: the ~62 real re-blessings stay visible instead of drowning in ~100
  untouched rows.
- **Widen** costs: roughly 100 additional `Modified` rows to sign, none of whose
  text changed. Buys: strict consistency with the WI-419 precedent.

### 2.6 — The four unblocked stale-text verdicts

These four were marked **CANNOT VERIFY** in 2026-08-10 because the token
`gate_policy` named **two different things**: a retired configuration enum
(`attended`/`single-ratify`/`autonomous`) and a **live runtime label**
(`human-held`/`loop-held`). One token, two meanings, one of them retired — so
"page through gate policy" could not be classified stale-vs-current.

**WI-437 (OI-25) removed the ambiguity**: the live runtime label was renamed to
`session_hold` (`agent_loop.py:2876` — *"the derived label is `session_hold` —
WHO HOLDS this run"*). The token `gate policy` in a spine cell can now **only**
mean the retired enum. These are therefore OI-23-class amendments, still owed.
*(handoff WI-437; prose-rewrite §E.3)*

| row | status | the stale phrase, verbatim | proposed correction direction |
|---|---|---|---|
| **SR-082** | `Modified` | acceptance: *"…shared top-tier failure, contradictions, or tripwires page **according to gate policy**."* | re-word to the declared ratification level + `session_hold`, matching the row's own requirement cell |
| **SR-085** | `Verified` | requirement: *"…and **page through gate policy** when the cap is exhausted."* (acceptance: *"the configured cap pages through the declared policy"*) | same — name the declared ratification level |
| **SR-108** | `Verified` | requirement: *"…and **surface PAGE per gate policy**, never silently."* | same |
| **SR-125** | `Modified` | **title only**: *"PAGE maps through gate policy"* — its requirement and acceptance already say *"the declared ratification level"* and *"human-held"/"loop-held"* correctly | re-title; the cells need no change |

- **Yes** costs: four cell edits; SR-085 and SR-108 flip `Verified`→`Modified`
  and owe a re-attest (SR-082/SR-125 are already `Modified`). Buys: no spine
  cell names a retired enum.
- **No** costs: four rows keep text that is now unambiguously stale, and the
  next stale-text audit re-raises them.

---

### 2.7 — System requirements that name implementation (raised by the owner, 2026-08-13)

**The question.** Under the ruled decomposition (the OI-21 ladder: an SR states
what a scope must PROVIDE at its boundary; an LLR is how the inside is
realized), a system requirement that names a script is naming a solution.
Measured on the live registry: **75 of 148 SRs name a `.py` script in their
requirement text** — roughly 25 name only entry-point-class scripts
(`check.py`, `bootstrap.py`, the launchers — the things the outside world
invokes, where the script name arguably IS the boundary port), and **~50 name
at least one internal module**, which no boundary reading defends.

**Why it stands today.** `SR-126` (Verified) deliberately PERMITS this — its
acceptance carves out that *"a script name, artifact path, rubric or sibling
spine id does not"* open a re-attest window. That carve-out predates the
ladder ruling and is now in tension with it. This session's amendments
deliberately did NOT touch the class: the OI-23 repairs changed facts, never
requirement shape, and the stage sweep changed vocabulary only.

**Where it IS already scheduled, honestly:**
- **SN-037 (Draft, in THIS sitting's ratification queue)** is the mechanization
  vehicle: *"Every system-requirement input and output references a declared
  interface; … unresolved references, uncovered crossings and incompatible
  signal types are mechanical findings."* Ratifying it commissions exactly the
  SR-tier boundary conformance the question asks for.
- The OI-14 ruled sequence carries a **RE-SCORE** loop — SRs re-stated against
  the derived boundaries after the partition ratifies — and Part B built the
  typed interface schema those restatements will cite.
- What did NOT exist until now: an execution row owning the pass. **WI-451**
  (queued) now owns it: the port-vs-internal census over the 75 rows, then the
  re-statement program, gated on this decision.

**The decision:** rule the discriminator. (a) RECOMMENDED — an SR may name an
artifact only where that artifact is a DECLARED BOUNDARY CROSSING (an IF row
with an external counterpart: the harness entry, the launchers, the scaffold
command); every internal-module mention re-states against the interface or
demotes to the LLR tier, executed as WI-451 after this sitting, with SR-126's
carve-out NARROWED to match in the same act. (b) Keep SR-126's blanket
carve-out and accept the mixed tier as this repo's dev-tooling idiom — zero
work, but the ladder's rung-2 definition stays aspirational for half the
registry. Cost of (a): a large re-statement program over ~50 rows — but it
rides the re-attest machinery this session already proved, and the census
comes first so you size it before committing.

## 3. The provisional partition (P5) — accept or overturn

Ruled at OI-14 (options A3 + A6), executed as WI-441 and **provisionally adopted
warn-first**: safe, because `LLR.Component` is a *traced* cell, so adopting it
opened **no re-attest window**. *(shortlist ruling + data pack §5)*

### The ranking

| Rank | Candidate | Cut / Straddle | Why it places here |
|---|---|---|---|
| **1 — ADOPTED** | **P5 narrow-waist** (4 components) | **31 / 7 of 12 (best)** | Best on the PRIMARY constraint: lowest behaviour straddle, and the only candidate that single-homes B3 (`value_to_cell`), B4 (gate policy), B9 (carrier vocabulary), B12 (`_norm_module`). Best boundary count (**4**) at a cut statistically tied with the best. **Zero new interface rows owed.** Same 8-module rework as the runner-up. Closest to the Core adopter's ratified answer — the strongest external evidence OI-14 names. |
| 2 — runner-up | P3 actor-boundary (5) | **30 (best)** / 10 | Lowest raw cut, 1 new IF row — but its components are AUDIENCE distinctions, and Parnas asks what CHANGES together; a dashboard and a decision brief may not. **If you overturn P5, reach for this.** |
| 3 | P4 functional (9) | 48 / 9 | Most faithful to the pure method, second-best straddle — but **15 interface rows that do not exist today** must be written before its checks are honest, and its F7 work-flow cluster at 22 crossings says that grouping is not one component. Right shape for a later depth-1 recursion, not depth 0. |
| 4 | P1 minimal-change (today's 5) | 33 / 10 | The honest floor: zero modules move, and it deletes the fail-open. But it ratifies the accident A1 was refuted for. Its value was making every other candidate justify its rework. |
| 5 | P2 shared-kernel (6) | 48 / **11 (worst)** | The measured **TRAP**, ranked last on purpose: extracting shared services without deleting the duplicated copies makes everything worse (cut 33→48, straddle 10→11, a 31-crossing hub K). Kept in the record because it is the move a reader reaches for first. |

### What P5 is — the four components, as minted

| id | name | mission (live `components.toml`) |
|---|---|---|
| **CMP-006** | W1 Registry & conformance | the spine and everything that decides whether it holds — `spine_carrier`, `trace`, `trace_text`, `derive_gate`, `check_trajectory`, `plan_coverage`, `migrate_carrier`, `wi_convert`, `gen_arch_map` (9) |
| **CMP-007** | W2 Gatekeeper | every verdict a hook, CI job or gate run consumes — `check`, `check_privacy`, `subagent_gate` + the 8 `check_*` lints, and the shipped hooks (11) |
| **CMP-008** | W3 Autonomy | the unattended coordinator end to end — the 5 `agent_*`, the 5 `plan_*`, `adjudicate_brief`, `dispatch`, `handback`, `intake`, `integrate`, `lane`, `prompts`, `schedule`, `score_reviews`, `spec_move`, `trunk_step` (20) |
| **CMP-009** | W4 Human & adopter surfaces | everything a person or an adopting repo reads or runs — `bootstrap`, `run_menu`, the 7 `gen_*`, the 6 `traj_*` (15) |

Per-component interface load: **W1 26 · W3 17 · W4 14 · W2 5** (only W2 meets
the ≤6 narrow-waist target). **W1 is deliberately coarse** — under the OI-21
ladder architecture RECURSES, and W1 is the first candidate for a depth-1
partition at the scheduled re-score; P4's F1/F2 split is the natural seed.

### The 8-module rework, executed

`check`, `check_privacy`, `gen_arch_map`, `migrate_carrier`, `prompts`,
`run_menu`, `subagent_gate`, `wi_convert` re-homed; the 5 multi-tagged modules
(`bootstrap`, `agent_common`, `agent_session`, `derive_gate`, `handback`) each
narrowed to ONE component. **CMP-006…009 minted, CMP-001…005 retired** under D-4
(ids never re-meaning). **149 `LLR.Component` + 54 IF `Component` cells
re-pointed; advisories 15 → 0, exactly as predicted.** All 31 cross-component
seams already have an IF row — **zero new rows** for the internal cut.

### The constraint finding underneath it

**One-home-per-behaviour is unsatisfiable by ANY partition of today's tree:**
the 12 duplicated behaviours live as **39 (behaviour, home) pairs across 16
modules**, so the *copies* — not the boundaries — are the violation. The
partition adopts the owning home; the D-8 common-module program (WI-448) is what
DELETES the copies. P2's measurement is the proof the two must land together.

### `SR.Area` → aspect — the verdict to ratify

Neither pure option survived measurement: **25 of 31** `Area` values are a
component by another name (derivable → redundant), and the **6 spanning values
carry 65 of 147 SRs** and are **ASPECTS** — cross-cutting concerns a partition
structurally cannot express. So "derive from Component" deletes information and
"retire outright" deletes the only grouping of SR-137…146. The provisional
verdict:

- `Area` as a 31-value free-text authored column **retires**;
- the six spanning values become a **closed aspect vocabulary**: `process`,
  `trajectory`, `unattended-loop`, `connectivity`, `perf`, `portability` — an
  aspect is a REVIEW grouping, not an ownership claim (cleanly compatible with
  the OI-19 hats axis);
- the 25 derivable values are dropped at conversion;
- **Portability's homelessness is not a defect** — its 3 SRs are depth-0
  system-level obligations discharged by every module, and under the OI-21
  ladder the system IS the depth-0 component.

**Not yet executed** — it is queued for the next SR-registry touch.

### What accepting vs overturning costs

Four things to accept or overturn: (1) P5 as the depth-0 partition; (2) the
CMP-006…009 mint and CMP-001…005 retirement; (3) the Area→aspect conversion;
(4) the boundary inventory (34 crossings, its completeness declaration, and the
two OI-28 seeds inside it).

- **Accept** costs: nothing further; the warn-first state becomes the ruled one.
- **Overturn** costs: **a mechanical re-tag and a re-derive of generated
  surfaces — and nothing else.** `LLR.Component` is a traced cell, so no
  re-attest window opens either way. This is the cheapest decision in the pack.

---

## 4. The hats roster — owner text, shipped as drafted

Lives at [`../requirements/hats.toml`](../requirements/hats.toml); read by
`project-trajectory/scripts/hats.py`. Ruled at OI-19 option (a): ship the
six-hat starting roster, **injection first, record second**. A hat is **not a
person and not a stakeholder row** — it is a QUESTION put to every decomposition
it applies to. Three keys are required per hat (`hats.py` refuses a row missing
any); a hat that names no failure class is refused as ceremony. **Absence is
opt-out, malformed is a refusal.**

**Your job here: review the six, cut what does not earn its place, add what is
missing, and rewrite any `applies_when` that does not match how this repo
actually files work.** A roster chosen by an agent and left unread is exactly
the ceremony SN-036 was admitted to prevent.

All six, verbatim:

**`SECURITY`** — `applies_when = "always"`
- *asks:* "What secret, credential, or irreversible action does this touch — and which requirement says who may reach it?"
- *listens_for:* "A decomposition that spends a secret, or takes an action nothing can undo, with no requirement naming the authority for it."

**`FIRST-RUN-ADOPTER`** — `applies_when = 'scope == "template" or scope == "both" or tags contains "templates"'`
- *asks:* "Does this hold for a stranger with only the shipped README and examples — no context from this project, no one to ask?"
- *listens_for:* "A requirement only satisfiable by someone who already knows this project: an undocumented convention, an example that does not run as shipped, a step whose prerequisite is never stated."

**`UNATTENDED-OPS`** — `applies_when = 'tags contains "unattended" or tags contains "loop"'`
- *asks:* "What does this look like at 3am with no human — what happens when its input is missing, stale, or half-written?"
- *listens_for:* "A failure that pages nobody: a silent degrade, a partial write left behind, an unbounded retry, a green that is green because nothing looked."

**`CROSS-PLATFORM`** — `applies_when = 'tags contains "scripts" or tags contains "launcher" or tags contains "shell"'`
- *asks:* "Which of Windows, macOS and Linux breaks this — path separators, line endings, console encoding, shell quoting, case sensitivity?"
- *listens_for:* "A rule that is true only on the author's platform and shipped as if it were universal."

**`MAINTAINER`** — `applies_when = "always"`
- *asks:* "Can a reader two years from now tell why this exists, and what would break if they deleted it?"
- *listens_for:* "A requirement whose reason lives only in the session that wrote it, leaving the next reviser unable to tell load-bearing from accident."

**`TEST-ENGINEER`** — `applies_when = "always"`
- *asks:* "What mechanical check fails if this is quietly violated — and can that check be shown to fail when it should?"
- *listens_for:* "An obligation with no enforcer, or an enforcer that passes because it never actually looks at the thing it claims to check."

**Two honest limits.** (1) The composer today declares `tags` (a work item's
Workstream + SafetyClass) and does **not** declare `scope`, because SN rows do
not yet carry a scope field — that is SN-039's job, so the three `scope ==`
clauses in `FIRST-RUN-ADOPTER` are honestly **silent**, not quietly true.
(2) SN-036 also requires a per-decomposition **record** of which hats were
applied and what each produced. Only injection shipped; **nothing gates on a hat
today.**

---

## 5. Mechanical state, and what closing looks like

**The basis line as it stands** (`docs/gate`, computed 2026-08-13):

```
# basis: SN=27 SR=148 LLR=151 TC=148 drafts=51 modified=64 uncovered=0
#        computed=DevBar-Below ex-draft=DevBar-Below phase=4
#        per-phase=1=DevBar-Tests;2=DevBar-Tests;3=DevBar-Tests;4=DevBar-Below;5=DevBar-Below
#        stage=DevStg-Needs stage-ord=0 stage-of=8
DevBar-Reqs
```

Read it honestly: the value is **the bar that must next be CLEARED**, computed
as the MIN over every in-scope row's own bar and floored to `DevBar-Reqs`. So
the least-mature row picks it, and **`drafts=51` + `modified=64` are the window
this sitting closes**. `uncovered=0` held through the dissolution.

**Mechanically, closing the sitting is:**

1. You sign in `docs/open-items.html` — that is where the per-cell evidence is.
2. The signed rows' `Status` moves in a **reviewed commit**: `Modified` →
   `Verified`, `Draft` → `Planned`. `docs/gate` is **derived, never hand-set**.
3. `python project-trajectory/scripts/derive_gate.py` regenerates the bar; the
   `drafts`/`modified` counts fall and the bar rises on its own arithmetic. The
   freshness `--check` is a commit-bar step, so a stale `docs/gate` is a red.
4. Regenerate the dependent surfaces (`trunk_step.py --regen` covers arch-map,
   okf, derived-gate, trajectory, status, open-items).
5. Record the attestation as a row in `docs/log.md` **`## Sittings`** — a named
   human, the date, and the **rung range** the sitting certifies. (The table's
   existing rows preserve the retired tag vocabulary verbatim under the OI-21
   attestation carve-out; the header note carries the translation.)

**Push and merge-to-main stay yours.** Everything is committed locally on
`infra/mechanized-loop`; this repo runs `push = "human"`. The last composed-tree
full bar: **2452 passed / 6 skipped, zero failures.**

**Where the depth lives if you want it** (citations, not required reading): the
applied-batch ledger `2026-08-13-wi444-batch-application.md`; the round-1 review
record and per-row rewrite tables `2026-08-10-sn-sr-prose-rewrite.md`; the
partition ruling and its measured inputs `2026-08-13-part-a-shortlist-ruling.md`
+ `2026-08-13-part-a-data-pack.md`; the session account in `docs/log.md`.
