# WI-444 — application record for the prepared SN/SR prose batch

**Source of the applied text:** [`2026-08-10-sn-sr-prose-rewrite.md`](2026-08-10-sn-sr-prose-rewrite.md)
— section **B** (per-SN, **form (i)** only) and section **E.1** (per-SR exact
replacement `requirement` cells).

**Authority:** OI-22, RULED (owner, 2026-08-13) — *(a) ADOPT THE BATCH*, apply-now
mode, applied ahead of the consolidated re-attest sitting.

**Nature of this record.** A plain before/after ledger of what a mechanical pass
applied. **No wording was authored here.** Every cell written is the plan's text.
Where the plan's text could not be applied without a judgement, the row was
skipped and is listed under *Skipped* rather than resolved.

**Not in scope, deliberately untouched:** form (ii) re-homings (unruled — §F item
3), the OI-17 SN-025/SN-034 reframe, the OI-18 edge-tier dissolution, the OI-23
stale-row corrections, the SN-005 CI narrowing, SN-033..SN-040 (minted after the
batch was prepared), and the LLR/TC registries.

---

## Counts applied

| tier | rows the batch covers | cells written | no-op (plan proposes no change / already identical) | skipped |
|---|---|---|---|---|
| SN core (18) | 18 | 15 need + 1 acceptance | 3 (SN-006, SN-023, SN-025 — plan proposes no change) | 0 |
| SN edge (10) | 10 | 8 expected | 2 (SN-017, SN-019 — identical under form (i)) | 0 |
| SN draft (1) | 1 | 0 | 1 (SN-029 — plan recommends "leave the Need cell alone") | 0 |
| **SN total** | **29** | **24** | **6** | **0** |
| SR (E.1) | 17 | 16 | 0 | **1 (SR-082)** |

**Status flips, `Verified` → `Modified`: 7** — SR-026, SR-042, SR-046, SR-049,
SR-050, SR-055, SR-110. The other nine SR rows written were already `Modified`
(SR-040, SR-057, SR-059, SR-060, SR-130, SR-131, SR-132) or `Draft` (SR-137,
SR-140) and keep their state.

**SN state: unchanged, and no field was invented.** The SN carrier has no
`Status` cell — its only state mechanism is `kind = core|draft|edge`, and the
batch moves no row between kinds. Per the WI-419 precedent recorded in that
commit's own message, *"an SN has no Status cell, so a changed ratified need
rides its SR chain's `Modified`."*

> **Divergence from WI-419 flagged for the coordinator.** WI-419 flipped **every**
> non-superseded `Verified` SR in an amended need's chain, including rows whose own
> text did not change (SR-035, SR-114). This pass flipped **only the SRs whose own
> ratified text it rewrote**. Applying the WI-419 rule to 15 rewritten core needs
> would flip most of the 147-row SR registry, which is a scoping judgement, not a
> mechanical one. **Owed decision:** whether the 15 rewritten SNs' full SR chains
> also owe the marker.

## Derived-state movement (honest, not fought)

`docs/gate` basis: `modified=38 → 45`; `per-phase` 2 and 3 dropped `G3 → G2`; the
gate value itself stays `G1` (already at the floor). Regenerated with
`trunk_step.py --regen` (arch-map, okf, derived-gate, trajectory, status,
open-items) plus a new re-attestation brief
`docs/ratify/2026-08-13-wi444.md` (32 `Modified` SR sections), following the
WI-419 date-stamped-brief precedent rather than rewriting the 2026-08-08 brief
the `ratify-fresh` message named.

---

## ⚠ Consequence the batch introduces: 6 new requirement-form findings

`trace.py` reported **`form-findings=6`** after the batch; the same command at
`HEAD` reported **none** (the field is absent from the baseline summary line).
All six are rows this batch rewrote:

`SR-040` (3 shall) · `SR-042` (2) · `SR-050` (2) · `SR-057` (3) · `SR-130` (2) · `SR-131` (2)

**Cause:** §E.1's legibility method converts participial chains into separate
`It shall …` sentences. That is exactly what makes the rows readable, and it is
exactly what the kit's own one-obligation-per-row rule flags.

**Blast radius:** form findings join the exit code only under `trace.py --strict`,
which `check.py` runs at the **traceability** step at **G2/G3 only**. At today's
`G1` nothing blocks — but the re-attest sitting exists to move the gate back up,
and these six will fail there. **Not resolved here:** splitting a requirement
mints ids and changes the decomposition. Owed to the sitting.

---

## Skipped — needs the coordinator

**`SR-082` — the only skipped row.** §E.1 marks its rewrite
**PRESERVING-CONDITIONAL**, and §E.3 records the condition as unmet: the
replacement text names `keep_nondependent` as the referent of *"the separate
drain dial"*, and the plan states this **"is marked conditional rather than
asserted"**, standing *"conditional on the sitting confirming the drain-dial
reading."* The sitting has not happened. It is also the only row in E.1 that is
not word-preserving (Δ **+6 / −13**) — it substitutes a naming claim for a
periphrasis, so applying it would be *deciding* the referent, not transcribing it.
One `Edit` away if the owner has already confirmed the reading.

*Current cell left as-is; `status` left at `Modified`.*

---

## The 12 previously-laundered rows — verification outcome

Round 1 caught 12 rows where revision 1 had dropped a qualifier. Before applying,
each row's **current registry text** was compared against the plan's **final**
text by token multiset (markdown emphasis and backticks stripped, punctuation
stripped, lowercased) to confirm no qualifier is dropped.

**Result: 12 / 12 pass — no obligation-bearing word is removed on any of them.**
Seven remove *zero* tokens; five remove only function words or verb inflections
forced by the subject rewrite.

| row | tokens removed | reading | verdict |
|---|---|---|---|
| SN-001 | `a, drop, the, kit, into, repo` | subject/verb swap: "drop the kit into … repo" → "add this process to … repository" | ✅ revision-1's invented *"the same day"* is absent, as the disposition requires |
| SN-004 | `progress` | subject swap only | ✅ *"explicit approval gates"*, `(G1→G2→G3→…)`, *"its mechanical bar is met"* all verbatim; no owner-authority claim reintroduced |
| SN-006 | — | plan proposes no change | ✅ *"typed code"* and *"repo text alone"* untouched in the registry |
| SN-024 | — | zero removed | ✅ scope clause, *"independent critical eye"*, *"never by the session that authored the artifact"* all verbatim; no *"in advance"* added |
| SN-026 | `are, configurable, and, benefits` | inflection: "are configurable" → "can configure"; "benefits" → "benefiting" | ✅ **both** round-1 drops present: *"per capability level"* and *"wherever that is configured"* |
| SN-027 | — | zero removed | ✅ *"bounded"*, *"parallel lanes"*, *"serialized and gated"* all verbatim |
| SN-028 | `has` | "Every policy dial has one home" → "find and change every policy dial in one home" | ✅ *"single hand-edited, machine-read file"* restored verbatim; acceptance cell removes **zero** tokens (`docs/process.toml`, bare `[section]`, `tomllib`, hooks' sh, adversarial-file pinning, `bootstrap.py --migrate-config` all kept) |
| SN-013 | — | bolding only | ✅ *"skip-or-report"* present |
| SN-014 | `sn-008` | see flag below | ✅ the measurable **`SKIP(missing)`** token present and now emphasised |
| SN-016 | — | bolding only | ✅ **stdin closed** present |
| SN-020 | — | bolding only | ✅ logged **`ERROR`** and **all-`ERROR`** both present |
| SN-022 | — | bolding only | ✅ **`-000`** and *"from G2 on"* present |

### Two transcription flags raised by that comparison

1. **Sibling-need cross-refs dropped by the plan's own text.** SN-014's proposed
   cell drops the trailing `(SN-008)` and SN-021's drops `(SN-010)`. Both tokens
   were present on 2026-08-10 (verified at `14925426`), so this is the plan's
   choice, not drift — applied as written. Note it is the same class of edit the
   plan holds back as a *recommendation* on SN-008 (*"a need citing its own
   child … recommend deleting the token"*). Neither deletion orphans anything;
   both parents are real rows.
2. **SN-015 quote glyph.** The plan renders `"not a git repo"` with single
   quotes. Applied verbatim; the delta is the quote glyph only.

---

## One reconstruction, stated plainly

**SN-017 / SN-018 / SN-019 / SN-020 — the `tests/test_agent_loop.py::…`
citations were RETAINED.** §B's edge table elides them from the proposed cells,
but form (i) is *defined* as the form in which *"the mechanical citation
**stays**"*, and the plan assigns deleting exactly these four citations to
**form (ii)** (*"Form (ii) for this tier deletes the four
`tests/test_agent_loop.py::test_…` citations (SN-017, SN-018, SN-019,
SN-020)"*) — which is unruled. Taking the table cells literally would have
executed form (ii) on four rows. The citations were therefore kept and only the
table's wording changes applied; that makes SN-017 and SN-019 no-ops.

---

## Per-row before/after ledger

`hash` = first 12 hex of `sha256` over the pre-edit cell. Text columns are the
first 60 characters; `⏎` marks an inserted line break.

### SN

| row | cell | old hash | old (60c) | new (60c) | action |
|---|---|---|---|---|---|
| SN-001 | need | `7c2d5f9ab4d4` | A team can drop the kit into a new or existing repo and get  | An adopting team can add this process to a new or existing r | APPLIED |
| SN-002 | need | `bd4b358f496b` | The trace from need → requirement → design → test is **mecha | A reviewer can trust the chain from need to requirement to d | APPLIED |
| SN-003 | need | `28a47ea05237` | The kit is **stack-agnostic** — a non-Python project uses it | A team in any language can use this process: it is **stack-a | APPLIED |
| SN-004 | need | `f650486ef3fe` | Progress advances only through **explicit approval gates** ( | A team advances only through **explicit approval gates** (G1 | APPLIED |
| SN-005 | need | `9298c5ea5444` | AI agents and humans work from the **same playbook**, with t | AI agents and humans work from the **same playbook**, and th | APPLIED |
| SN-006 | need | — | — | — | no change proposed by the plan |
| SN-007 | need | `9cc236ee2803` | The kit's **own** changes stay traceable and tested — a chan | The people maintaining this kit hold it to its own standard: | APPLIED |
| SN-008 | need | `a13860079b1c` | Gates are **honest** — a green never hides a skipped check,  | A reader can believe a green: gates are **honest**, and a gr | APPLIED |
| SN-009 | need | `a51bc5a2c23b` | A committed **secret or private identity** is caught before  | A team is protected from publishing a **secret or private id | APPLIED |
| SN-010 | need | `1badc84158ea` | Documentation stays **navigable and honest** — links resolve | A reader can navigate the documentation and trust it: **navi | APPLIED |
| SN-011 | need | `b6d19332f2e4` | The kit's scripts run on a **clean Python 3.11+ with minimal | An adopting team can run every check on a **clean Python 3.1 | APPLIED |
| SN-012 | need | `177663ef93a3` | The process is **right-sized**, not ceremony for its own sak | A team can keep small changes small: the process is **right- | APPLIED |
| SN-023 | need | — | — | — | no change proposed by the plan |
| SN-024 | need | `63c49a77f291` | Subjective/perceptual acceptance — a realistic-looking rende | A reviewer can trust subjective/perceptual acceptance — a re | APPLIED |
| SN-025 | need | — | — | — | no change proposed by the plan |
| SN-026 | need | `f0d9ce761ede` | **Several LLM families are configurable** — selected per job | The repo owner can configure **several LLM families** — sele | APPLIED |
| SN-027 | need | `d0b525f4075b` | Ready work **fans out across bounded parallel lanes**, while | A team gets more than one piece of ready work moving at once | APPLIED |
| SN-028 | need | `edd791e4da77` | **Every policy dial has one home** — a single hand-edited, m | The repo owner can find and change every policy dial in **on | APPLIED |
| SN-028 | acceptance | `5a19ae4ec232` | `docs/process.toml` holds every process dial under bare `[se | `docs/process.toml` holds every process dial under **bare `[ | APPLIED |
| SN-029 | need | — | — | — | no change (plan: "leave the Need cell alone"; row also amended 2026-08-12, after the plan) |
| SN-013 | expected | `9db5d97be7c4` | The git hooks / coordinator **probe by running** a candidate | The git hooks / coordinator **probe by running** a candidate | APPLIED |
| SN-014 | expected | `5c103d836474` | `check.py` reports `SKIP(missing)` and **fails the gate** —  | `check.py` reports **`SKIP(missing)`** and **fails the gate* | APPLIED |
| SN-015 | expected | `c17e90fc84aa` | The coordinator preflight reports "not a git repo" and exits | The coordinator preflight reports 'not a git repo' and exits | APPLIED |
| SN-016 | expected | `b51eb57f5ec9` | `agent_loop.py` runs headless (stdin closed); a rate limit b | `agent_loop.py` runs headless (**stdin closed**); a rate lim | APPLIED |
| SN-017 | expected | `9fe137a601df` | The per-worktree lock is a kernel advisory lock the OS relea | *(unchanged)* | no-op under form (i) |
| SN-018 | expected | `2b84626eb055` | It is **refused** rather than risking a two-writer race. *(t | A second coordinator is **refused** rather than risking a tw | APPLIED |
| SN-019 | expected | `2853ff9fecc7` | The coordinator's rev-parse guard does not crash the loop. * | *(unchanged)* | no-op under form (i) |
| SN-020 | expected | `f1e9118f610b` | The session is logged `ERROR` and an all-`ERROR` stall is re | The session is logged **`ERROR`** and an **all-`ERROR`** sta | APPLIED |
| SN-021 | expected | `3cde27cf1bdb` | Its `--check` fails at the gate — a stale generated doc is a | Its `--check` fails at the gate — a stale generated doc is a | APPLIED |
| SN-022 | expected | `69fb66b5d424` | `--no-placeholders` flags a leftover `-000` row from G2 on;  | `--no-placeholders` flags a leftover **`-000`** row from G2  | APPLIED |

### SR

| row | cell | old hash | old (60c) | new (60c) | action |
|---|---|---|---|---|---|
| SR-026 | requirement | `85c18fc5cfff` | agent_loop.py shall resume headless with stdin closed, never | agent_loop.py shall resume headless with stdin closed, never | APPLIED + `Verified`→`Modified` |
| SR-040 | requirement | `6976792c2206` | The unattended coordinator shall select the agent command te | The unattended coordinator shall select the agent command te | APPLIED (already `Modified`) |
| SR-042 | requirement | `3464391bd5eb` | gen_okf.py shall export the spine registries AND the key pro | gen_okf.py shall export the spine registries AND the key pro | APPLIED + `Verified`→`Modified` |
| SR-046 | requirement | `988f385db4fe` | The root run.cmd/run.sh/run.command launchers shall present  | The root run.cmd/run.sh/run.command launchers shall present  | APPLIED + `Verified`→`Modified` |
| SR-049 | requirement | `846c1953997a` | derive_gate.py shall compute the active gate from the spine  | derive_gate.py shall compute the active gate from the spine  | APPLIED + `Verified`→`Modified` |
| SR-050 | requirement | `82d0db472ea4` | gen_trajectory.py shall render a Process reference tab in PR | gen_trajectory.py shall render a Process reference tab in PR | APPLIED + `Verified`→`Modified` |
| SR-055 | requirement | `26f6d88f0251` | The Process tab shall additionally render the project's two  | The Process tab shall additionally render the project's two  | APPLIED + `Verified`→`Modified` |
| SR-057 | requirement | `20b5ccd62cb8` | A stdlib schedule.py library/CLI shall derive the dependency | A stdlib schedule.py library/CLI shall derive the dependency | APPLIED (already `Modified`) |
| SR-059 | requirement | `aa793e4f96bb` | The migration shall delete docs/next-wi and docs/run-phase o | The migration shall delete docs/next-wi and docs/run-phase o | APPLIED (already `Modified`) |
| SR-060 | requirement | `b17f6b924f2b` | The session engine shall run explicit per-worker claimed ass | The session engine shall run explicit per-worker claimed ass | APPLIED (already `Modified`) |
| **SR-082** | requirement | `—` | *(left as written)* | *(left as written)* | **SKIPPED — needs the coordinator** |
| SR-110 | requirement | `f53eb364a6e3` | check_coverage.py shall fail when a module listed in the cov | check_coverage.py shall fail when a module listed in the cov | APPLIED + `Verified`→`Modified` |
| SR-130 | requirement | `fc6ce6e58956` | A serial trunk step shall compile docs/log.d/ work-branch lo | A serial trunk step shall compile docs/log.d/ work-branch lo | APPLIED (already `Modified`) |
| SR-131 | requirement | `ef6649f62cca` | A tracked docs/work/pause file (TOML: reason, since) shall p | A tracked docs/work/pause file (TOML: reason, since) shall p | APPLIED (already `Modified`) |
| SR-132 | requirement | `613438a751da` | The local integrator shall claim work via a serial trunk com | The local integrator shall: ⏎ (1) claim work via a serial tru | APPLIED (already `Modified`) |
| SR-137 | requirement | `a0916582d380` | The kit shall read every process policy dial from a single ` | *(line breaks only)* | APPLIED (`Draft`, stays `Draft`) |
| SR-140 | requirement | `eece24288bae` | The kit shall record each acceptance ON THE ACCEPTED ARTIFAC | The kit shall record each acceptance on the accepted artifac | APPLIED (`Draft`, stays `Draft`) |

Most SR rows share their first 60 characters with the original because §E.1's
method is largely re-punctuation and inserted line breaks; the ledger above is a
locator, and the full before/after is in `docs/ratify/2026-08-13-wi444.md`.

Two plan-stated deltas did not reproduce exactly under token counting and are
recorded as accounting slips in the plan, not text problems — **no words are
removed in either**: SR-049 (plan `+2`, measured `+0` words plus three list
numerals — "and"/"The" were already present) and SR-042 (plan `+2`, measured
`+4`). SR-110 and SR-059 likewise measured `+0` against claimed `+3`/`+1`.

---

## Verification run at application

- `trace.py --root . --strict-integrity` → **exit 0**; `orphans=0 integrity=0`,
  `form-findings=6` (new, analysed above), 36 pre-existing paraphrase advisories.
- `check.py --run-steps <the pre-commit set>` → **12/12 PASS** after regeneration.
- `check_docs.py --root .` → **exit 0**; 838 docs, 1131 links, 0 broken.
- `pytest -q -n auto -m smoke` → **987 passed, 2 skipped** in 114 s.
