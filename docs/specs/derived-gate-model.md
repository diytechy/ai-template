# Design spec — Derived gate model (replace the monolithic declared gate)

**Status: RATIFIED (owner G1, 2026-07-12).** Branch: `derived-gate-model`.
Registered as **WI-088** (campaign `derived-gate`, design done). This doc is the
spec-of-record; the implementation is filed as **WI-089…096** (§10).

Owner direction (2026-07-12): **replace** the monolithic gate (not opt-in);
**hybrid** derivation via a fast check script that caches the last-computed state
(with a compute date) so the gate is known on checkout; **no new column** on
SR/LLR/TC (reuse the open-vocabulary `Status`); **audit the artifact attributes
correctly** to derive the gate and drive the right checks.

## Ratification (owner G1 — 2026-07-12)

1. **Derivation rules — ratified.** `Status` is the *"needs
   decomposition-checking"* flag; the **level of decomposition** (ratified → has
   its LLR/TC → `Verified`) derives the per-artifact gate. (§3.)
2. **Ratification = a reviewed commit — ratified.** The commit that moves a
   `Status` is the sign-off for the artifacts it touches; **an agent may make
   that commit** on a human's behalf, with the `docs/gate-policy` level governing
   *who may* (attended / single-ratify / autonomous). (§6.)
3. **Phase — ratified:** the derived-gate **drop** is the *detector*; the
   committed `[phase]-[g*]` work item is the *anchor* of phase identity +
   membership (§9.3).
4. **SN maturity — decided: section-as-state** (§4 option (a)).

---

## 1. The problem

The gate is a single hand-set fact (`docs/gate`, one line, monotonic) that a
human bumps. Two failures keep recurring:

- **You can't cleanly reopen cleared work.** New content often *affects* an
  already-verified requirement, but you don't know *which* until you do the
  requirement work. Per-item reopening assumes foreknowledge you don't have.
- **The monolithic marker forces all-or-nothing.** Taking on new scope either
  drags the whole repo's bar down (regressing the marker un-enforces confirmed
  work) or is wedged into the phase tag as an exception. Iteration fights the model.

## 2. The model

- **Gate is DERIVED from artifact states, not declared.** The repo (and each
  phase) is at gate `G` iff every in-scope artifact meets `G`'s bar. SSOT applied
  to the gate itself.
- **Parallel for pre-dev, series for dev.** A phase's requirement work
  (G0→G1→G2) is structured as a **batch, in parallel** — which is exactly where
  conflicts and "this also modifies SR-12" become visible — then each work item
  runs **G2→G3 in series** (the vertical-slice channeling WIs already do).
- **Phase is derived from gate trajectory, anchored in a committed WI.** The
  derived gate **dropping** — a reopen, or new draft content entering below the
  last closed level — is the *detector* that a new phase is due; the
  `[phase]-[g*]` work item is the committed *anchor* of its identity + membership
  (§9.3). Phase = the time-bucket that captures *leak-in*; campaign stays a
  *named* new-work set (they diverge exactly when other work is pulled in).
- **The pre-dev batch is a first-class work item:** `[phase]-[g1]` / `[phase]-[g2]`.

## 3. Artifact-state model (no new column)

Maturity is **mostly derived from existing structure**, gated by one `draft` bit:

| Artifact | State home | Ladder |
|---|---|---|
| SR / LLR / TC | existing **`Status`** (open-vocab today: `Planned`→`Verified`) | prepend **`Draft`**: `Draft` → `Planned` → `Verified` |
| SN | markdown table (no `Status`) — **§4 open decision** | `Draft` → `Ratified` |

Per-artifact gate is **computed**, not hand-assigned:

- **SR** — `Draft` ⇒ **G0** (unratified requirement); `Status≥Planned` ⇒ **G1**
  (requirement ratified); has its required LLR **and** TC (decomposed) ⇒ **G2**;
  its test-verifiable TCs `Verified` ⇒ **G3**. (LLR-exempt verifications —
  `Analysis`/`Inspection`/`Attest`/`Critique` — need the TC, not the LLR, per
  today's rule.)
- **LLR / TC** — `Draft` ⇒ G0; present + `Planned` ⇒ G2; `Verified` ⇒ G3.
- **SN** — `Draft` ⇒ G0; `Ratified` ⇒ G1.

**Ratification date is git-derived**, not a new field — the commit that moved the
`Status` (the `--stale`/as-of idiom the kit already uses). "Ratified with a date"
= the date of that reviewed commit. (Owner's "or some other form.")

**Draft artifacts are exempt from the child-completeness rule.** A `Draft` SR
with no LLR/TC is **not** an orphan — this is what makes requirement-first
drafting legal in the live spine, retiring the `-000`/off-spine workaround. This
is the single biggest change to `trace.py`'s orphan logic.

## 4. Open decision — where SN maturity lives

SN is a markdown table with no `Status` column. Options (pick at G1):

- **(a) Section-as-state** — a `## Draft needs (unratified)` heading; ratified SNs
  sit under `## Core needs`. No new column; state = which section. Date git-derived.
- **(b) A `Status` cell** appended to the SN table (a table column, not a spine
  CSV — the owner's "no new column" was scoped to SR/LLR/TC).
- **(c) A ratification ledger** `docs/requirements/ratifications.csv`
  (`id,gate,state,who,date`) covering SN *and* recording human ratification for
  the whole spine in one auditable place.

**Decided (owner G1, 2026-07-12): (a) section-as-state** for SN (least schema
churn, git-derived date); (c) revisitable only if per-artifact *human* attribution
beyond git-author is later wanted.

## 5. The derived gate — the hybrid check script

New `derive_gate.py` (or a `check_trajectory.py` mode):

- **Compute.** For each in-scope artifact (not `deferred`, phase-scoped), compute
  its per-artifact gate (§3); the phase gate = **min** over its artifacts; the
  repo gate = min over active phases (also reported per-phase).
- **Cache with a compute date.** Write the result to `docs/gate` — now a
  **generated** file: the derived value + a `# computed <as-of commit> <date>`
  comment. So the gate is known from the last computed state **on checkout**,
  no recompute needed to read it.
- **`--check` (rot guard).** Recompute and compare to the cache; a mismatch is a
  finding (the artifact states moved but the cache didn't). Fast (registry-only
  read, ~like `check_trajectory`). The compute date makes any staleness visible;
  a pre-commit step keeps it fresh the way generated artifacts are today.
- **`check.py` consumes it.** `resolve_gate()` still reads `docs/gate`, but the
  value is now derived; `--gate` override still wins for a scoped local run. The
  checks a gate runs are unchanged **once the derived gate is known** — the
  derivation just replaces the hand-set input.

**Auditing correctness (the owner's core concern).** The derivation is the trust
root, so it is spec'd precisely and **tested against fixtures**: every per-artifact
gate rule, the in-scope filter, the min-aggregation, and the draft-exemption get
a red→green test; a malformed/ambiguous state fails loud (never silently reads as
a lower or higher gate). `trace.py` gains a draft-aware orphan pass, and its
existing `--require-verified`/`--strict-schema` become the G3/G2 *derived* bars.

## 6. Ratification workflow (what the human does now)

The human no longer bumps a gate line; they **mark a batch of artifacts ratified**
(`Draft`→`Planned`, or SN section move) **in a reviewed commit** — that commit *is*
the ratification, and the gate derives from it. `Attest` (who+when in the TC)
still records subjective sign-offs. This **preserves the reviewed-commit
discipline** while making the marker computed. It composes with the gate-authority
levels: `attended` = human ratifies each batch; `single-ratify` = the batch is
ratified once at its `[phase]-[g2]` close (a natural fit — one review per phase
gate); `autonomous` = a fresh-context reviewer's recorded verdict ratifies.

## 7. The `[phase]-[g*]` work-item archetype

A phase's pre-dev batch is a first-class WI: `[phase]-[g1]` (requirement
structuring) and `[phase]-[g2]` (decomposition + TCs). All the phase's open
non-deferred WIs' pre-dev artifacts batch under it (parallel); its predecessors
are the prior phase's close. When `[phase]-[g2]` ratifies, the constituent WIs
run G2→G3 (series). `check_trajectory` learns this archetype (id shape, the
contains-relation, closure = all constituent artifacts at ≥G2).

## 8. Parallel/series in one picture

```
Phase N:  [phase-N-g1]  draft+ratify ALL new/reopened SN/SR   (parallel, batch review)
              │
          [phase-N-g2]  decompose to LLR/TC, all Planned      (parallel, batch review)
              │
          WI-a ─ G2→G3 ─┐
          WI-b ─ G2→G3 ─┤  (series, per-WI vertical slices)
          WI-c ─ G2→G3 ─┘
```
Backward movement (a reopen during Phase N+1's g1) revs the phase; the affected
verified artifact returns to `Draft`/`Planned`, the derived gate for that phase
drops, and the batch review sees it alongside the new work.

## 9. Risks & open questions

1. **Inverts the `check.py`/CI contract** — the most-copied tool now consumes a
   derived value. Mitigated by the hybrid cache (CI reads the file as today).
2. **Simplicity for small projects.** Replacing (not opt-in) means a one-shot
   repo also runs the derive script. Mitigation: the derive step is fast and the
   cache means the gate is still a readable one-liner; a fresh scaffold derives
   trivially (all draft ⇒ G0/G1).
3. **Phase = derived detector + committed anchor (resolved).** The *signal* to
   open a phase is derived — the repo's derived gate **dropping below the last
   closed phase's level** means new content entered (added or reopened), so a
   check warns "open a `[phase]-[g*]`". But phase **identity and membership** live
   in the committed `[phase]-[g*]` work item, not a pure git-history walk, for two
   reasons: (i) **membership** — knowing a phase *started* isn't knowing which
   artifacts are *in* it; the anchor names its members, versus attributing
   "below-bar-since-the-boundary" by replaying history; (ii) **stability** — a
   rebase/squash rewrites history, so a purely history-derived boundary moves,
   while a committed anchor doesn't. Within a phase the derived gate only rises
   (draft → ratify → decompose → verify), so a drop from a closed level is an
   *unambiguous* boundary — the detection is robust; the anchor just makes
   membership legible and durable. *(Fully-derived with no anchor stays possible
   as a purist variant — pure SSOT, at the cost of rebase-sensitivity and a full
   history walk; not recommended.)*
4. **Cache rot.** The compute date + `--check` + a pre-commit freshness step
   bound it (the generated-artifact discipline the kit already runs).
5. **Migration.** Existing repos seed initial states (current `Verified` rows ⇒
   G3; a monolithic-`G3` repo ⇒ all-ratified) once, then derive. Downstream
   re-sync ships `derive_gate.py` + the seed recipe.

## 10. WI breakdown (filed on ratification)

1. **Artifact-state + draft-exemption** — `Draft` in the `Status` vocabulary;
   `trace.py` orphan pass exempts draft; fixtures.
2. **SN maturity** — the §4 decision, in `stakeholder-needs(.template).md` + reader.
3. **`derive_gate.py`** — compute + cached `docs/gate` (compute date) + `--check`.
4. **`check.py` integration** — consume the derived gate; keep `--gate` override.
5. **Phase derivation + `[phase]-[g*]`** — `check_trajectory` archetype + phase rev.
6. **Ratification workflow** — Status-change-as-ratification; `gate-advance` skill
   + `gate-policy` levels updated.
7. **Process docs** — PROCESS.md §4/§7 rewrite (derived gate), PROCESS_OPTIONS
   phased-delivery folded in, the parallel/series workflow.
8. **Migration + dogfood** — ADOPTING recipe; migrate the meta's own spine and
   prove the derived gate reads `G3` byte-for-byte against today's declared one.

## 11. Done-when (the campaign) — LANDED 2026-07-12 (WI-089…096)

- [x] This design ratified by the owner (G1). *(WI-088, 2026-07-12.)*
- [x] `docs/gate` is generated from artifact states (`derive_gate.py`, WI-091);
      `--check` guards rot; the meta's derived gate reads **`G3`**, matching its
      declared gate (WI-096 migration — the meta `docs/gate` is now the generated
      form, full `--check` basis-compared).
- [x] Draft artifacts live in the live spine without orphaning (WI-089 trace
      exemption + WI-090 SN section-as-state); requirement-first drafting +
      ratify-to-climb is fixture-tested (`test_derive_gate.py`,
      `test_trace.py`).
- [x] `[phase]-[g*]` archetype + the phase-drop detector land in
      `check_trajectory` (WI-093); the parallel-pre-dev / series-dev workflow is
      documented (process-options.md "Derived gate model").
- [x] The monolithic hand-set gate is retired (`derive_gate.py` is the authority,
      `check.py` consumes it, WI-092); PROCESS/PROCESS_OPTIONS/`gate-advance`
      skill/gate-policy updated (WI-094/095); the downstream migration recipe
      ships in ADOPTING §5/§6 (WI-096).
