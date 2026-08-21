# The stage unification plan — v1 FINAL (owner-ruled 2026-08-21)

**Status: FINAL — the owner answered all four §6 questions on 2026-08-21
(answers recorded in §6) and OI-51 is RULED on this plan's shape.** The
executing program row is WI-498. Direction and evidence:
[2026-08-21-stage-unification-design-record.md](2026-08-21-stage-unification-design-record.md)
(and the three measurement docs it cites). This document turns the owner's
2026-08-21 chain-of-thought into an executable shape, keeping each of their
mechanisms and stating where engineering adjusted one and why.

## 1. `docs/stage` — the file

Replaces `docs/gate`. One committed file, still the single home for all
derived stage state (as the basis line is today), carrying:

- **the effective stage** (the headline value — the designed derivation:
  per-phase, draft-excluded, floored; design record §4.2)
- **the current phase** and the per-phase breakdown (see §4)
- **the input fingerprint** (see §2) and the as-of revision
- the raw/ex-draft diagnostic fields the basis line carries today

The committed copy stays load-bearing (not just cache): the event detectors —
phase-drop, tier signal — need the committed HISTORY of this file, which is
also why readers never write it (§3).

## 2. Freshness: fingerprint the INPUTS, not the repository

The owner's intent: the file records what was measured and a hash that lets
any consumer know whether the measurement still holds; their concern:
hashing the repo scope is expensive and duplicates other scans.

**The adjustment that dissolves the concern: the derivation's input set is
not "the repository" — it is enumerable and small.** `derive_stage` is a
pure function of the spine registries (`docs/requirements/*.toml`,
`docs/test/test-cases.toml`), the declared dials it reads
(`docs/process.toml`), and — once the Release rung is evidence-gated — the
test-evidence carrier. That is under a dozen files. The schedule map
verified this: the current `--check` already recomputes from exactly the
live registries. OWNER_SCRATCHPAD.md, ignored files, and the rest of the
tree were never inputs, so they never need scanning or excluding — the
exclusion problem disappears with the inventory.

Mechanics:

- The input set is DECLARED in one place (the kitlib stage module, §5
  slice 0/1) — adding an input (the evidence carrier) is an edit to one
  list, and the fingerprint automatically covers it.
- Fingerprint = SHA-256 over the LF-normalized content of each input file
  (paths + digests folded into one digest). LF-normalized because the
  byte-cap and commit-probe episodes both showed Windows working trees
  carry CRLF where the index holds LF; a fingerprint that flips on line
  endings is stale-noise.
- Cost: the input files total a few hundred KB; hashing them is
  single-digit milliseconds — and every current consumer already PARSES
  these same files wholesale (trace.py, derive_gate), which costs far more
  than hashing. The fingerprint is a fast path that lets a reader SKIP the
  parse when fresh, so the net scan count goes DOWN, not up.
- Per-process memoization in the common reader (digest keyed by
  path+size+mtime) so N readers in one process hash once. mtime is only a
  memo key, never the freshness truth — git checkout rewrites mtimes, and
  the worst case is a harmless re-hash.
- Rejected alternatives, recorded: whole-repo scope hash (expensive,
  inputs conflated with state, exclusion list to maintain); git index OIDs
  (misses unstaged working-tree edits — the exact mid-session window the
  mechanism exists to close); mtime-only (checkout noise, clock skew).

## 3. The common reader — one method, self-healing

The owner's rule, adopted whole: **everything that needs the current stage
calls one kitlib function.** Contract:

- Reads `docs/stage`; recomputes the fingerprint over the declared inputs;
  on match returns the recorded value (no parse), on mismatch derives fresh
  IN MEMORY and returns that.
- **Readers never write the file.** Writing stays where it is today: the
  trunk regen points (`trunk_step.regen`) and the human's post-ratification
  regenerate; the commit-bar `--check` still refuses a commit whose
  committed copy is stale. This keeps read paths side-effect-free on
  claimed branches and in CI, keeps the committed history clean for the
  event detectors, and keeps regeneration an auditable act.
- This contract closes BOTH stale windows the schedule map found, by
  construction: the branch-lane window (readers no longer trust a cache
  the freshness step cannot police there — they verify per call), and the
  once-per-run hoisting in `agent_loop`/`dispatch` (the hoist becomes a
  call to the common reader wherever the value is consumed, or at minimum
  re-verifies per tick like `tracked_pause` already does). The
  `spine_stage_of` trust-invariant mismatch dissolves rather than needing
  re-documentation.

## 4. Phase: keep it DERIVED; the decrease rule becomes an authoring check

The owner proposed: if the stage DECREASED — except the
`DevStg-LLReqs → DevStg-Arch` transition — increment the phase; and asked
whether phase should be stored in a file.

**Finding that shapes the answer:** phase is already derived, not stored —
rows carry a `Phase` column, `phase=` is the max over ratified rows, and a
Drafted row's `DevStg-Below` is already documented as "the new-phase
signal" (`derive_gate.py:56`, `:1198-1204`). Storing an auto-incremented
counter would create a SECOND phase concept beside the row-derived one —
new state, new drift surface, against the repo's single-owner doctrine.

**Proposed landing (i), keeping the owner's rule and the derivation:** the
decrease rule becomes an AUTHORING-TIME check, not a stored counter. When a
newly drafted/redrafted row would DECREASE the effective stage, the check
requires that row to carry a NEW (or already-open lower) phase tag —
"a scope change surfaces as a phase bump" made mandatory instead of
conventional. The derived `phase=` then increments BECAUSE the rows say so,
exactly as today, and stays recomputable from the registries alone.
`docs/stage` carries the derived phase (as `docs/gate` does now) — so yes,
it is in a file for easy fetching, without becoming independent state.

The exemption, expressed in that form: a decrease landing exactly on the
`LLReqs → Arch` transition demands no new phase — architecture rework
surfaced by decomposition is within-phase churn. (§6 asks the owner to
confirm the intended breadth: only the one-rung LLReqs→Arch drop, or any
Arch-tier rework while the phase sits at LLReqs.)

Alternative (ii), recorded in case the owner wants it anyway: a stored
monotonic counter in `docs/stage`, incremented by the WRITER when the
recorded stage decreases across a regen. Cost: phase is no longer a pure
function of the registries (two regens vs one between edits give different
counts), and the row `Phase` tags must then FOLLOW the counter or the two
diverge. (i) is recommended.

## 5. Slices (each ends green at the commit bar; program row per slice set)

0. **One enum home.** The eight-rung ladder + order + descriptions move to
   kitlib; `check.py`/`agent_common`/`check_vocab` import it; the equality
   pins retire; the bar constants and `STAGE_BAR` are deleted with the axis
   (in slice 2 — slice 0 only extracts what survives).
1. **`derive_stage` + `docs/stage` + the common reader** (§§1-3), with the
   effective-stage derivation designed per the record; the deep-check's
   nine corner cases become this slice's driven acceptance tests (draft
   drop, per-phase, fresh scaffold, DevStg-Below ordering, truncation,
   cross-ladder token, non-monotonic selection, hoisting, branch lane).
2. **Selection re-keys at-or-above** the effective stage; each step's
   `gates=` set re-derived deliberately into a from-stage threshold;
   `check.py`'s bar constants deleted; `docs/gate` readers → common reader.
3. **Ladder re-discrimination + the phase rule** (§4): all-Founded →
   `DevStg-Impl`; `DevStg-Release` reachable only from the test-evidence
   carrier (unreachable until built — honest); the authoring-time decrease
   check with its exemption.
4. **Event detectors over stage history:** phase-drop against per-phase
   anchors; tier signal as a two-point delta of the committed file — fixed
   (WI-497 folds in) and re-keyed; dead `read_declared` removed.
5. **Vocabulary + migration:** PROCESS.md §4 and skills re-teach one
   vocabulary; `check_vocab` gains the bar→stage alias generation (reviewed,
   not scripted — spellings are shared across the old axes); RESYNC_PACK
   migration entries; WI-493 (dial re-key) folds in; the 648-site sweep.

Evidence carrier (Release's input) is its OWN row, sequenced independently —
slice 3 does not wait for it; Release simply stays unreachable until it
lands.

## 6. The owner's answers (2026-08-21) — the plan finalized on these

1. **Phase mechanism: (i), with the alignment check the owner asked for
   verified.** Phase is traced on SPINE items only — all 73 SRs carry
   `phase =`, LLR/TC likewise, the derivation reads exactly
   `srs + llrs + tcs` (`derive_gate.py:1202`), and no off-spine registry
   carries the column. The owner's consistency principle ("either stage
   and phase are both stored to a file for traceability, or neither")
   holds in this plan's shape: BOTH are derived values and BOTH are
   recorded in `docs/stage` — same treatment, one file, still
   recomputable from the registries alone.
2. **Exemption breadth: exactly the one permutation `LLReqs → Arch`** —
   the permitted decomposition cycle. Any deeply decomposed problem
   would otherwise run the phase counter up; no wider Arch-tier
   exemption.
3. **No interim.** This is a meta repo; the owner is not worried about
   how phases/stages run while the change goes through. OI-51's narrow
   (a) is NOT taken; slice 2 delivers selection.
4. **Branch trust model confirmed.** Spine work happens in series, so a
   claimed branch derives from its OWN registries; the computation
   running there does not hurt; and on merge the trunk adopts the
   branch's computed stage/phase directly — that spine work was the only
   spine work in flight, so its derived result IS the trunk's next
   value.
