# D-9 + D12 status-vocabulary migration — the re-derived execution plan

**Provenance:** produced 2026-08-15 by a read-only Opus analysis pass over the
archived checklist
([archive/plans/2026-08-11-status-ladder-migration.md](../archive/plans/2026-08-11-status-ladder-migration.md),
figures stale by its own header) and the current tree. **Nothing here is
executed.** Counts marked *(transient)* were measured while WI-458 was landing
and must be re-derived at execution.

**⚠ §D IS SUPERSEDED (owner directive, 2026-08-15):** the anchor half
(TextHash/HashedOn columns, the on-row writer, the co-mutation guard) is ruled
**unnecessary complexity**. Approved spine changes instead copy their documents
to `archive/last_approved/`, and every comparison — the adjudicator or human
re-attest read, and the HTML generators — diffs the live registries against
that snapshot. A dedicated analysis of that design is in
[2026-08-15-baseline-snapshot-design.md](2026-08-15-baseline-snapshot-design.md)
(in flight at the time of this writing). §D is retained below as the record of
what was considered and superseded; its *problem statement* (§3.2's hard
coupling, Option B′'s proof that the git walk dies under D-9) still governs —
only the mechanism changed.

---

## Four corrections that change the archived plan

**C1 — `--strict-schema` runs only at DevBar-Release, so "close the enum" as
written is INERT.** `check.py:470-476` appends `--strict-schema` only when
`gate in (BAR_RELEASE, "all")`. The always-on floor is `--strict-integrity`
(`check.py:592-606`, tagged `{BAR_REQS}`, plus the pre-commit hook). Adding
`Status` to `trace.ENUM_FIELDS` (`trace.py:312`) routes it through
`schema_findings` (`trace.py:1191-1206`) — which the repo, at
`computed=DevBar-Below`, **never runs**. The Status closure must join the
**integrity** finding class (`trace.py:3008-3020`) or the self-announcing
property remains a claim with no mechanism at today's gate.

**C2 — `Drafted`/`Approved`/`Founded` are NOT unused constants.**
`derive_gate.py:500` defines them and they are live: `BIF_MATURITY` (513-518)
and `CMP_MATURITY` (522-539) map the off-spine vocabularies onto them;
`_maturity` (542-561) and `_caps` (564-566) consume them; `boundary_incomplete`
(582-626) and `arch_incomplete` (628-645) gate rungs 1 and 3 on them. **D12 is
already half-built.** `derive_gate.py:480-499` states the intended landing
verbatim: *"D-9's migration is then a TABLE EDIT rather than a predicate
rewrite … when it lands only the spine rows of this table move."*

**C3 — the SN tier has already shed both `draft` and `edge`.**
`stakeholder-needs.toml`: 27 rows, all `kind = "core"`, zero `status` keys
*(transient)*. The nine-reader list is obsolete; three chokepoints remain:
`spine_carrier.folded_needs`/`needs_from_text`/`draft_ids_from_text`
(`spine_carrier.py:825-844, 882, 914`), with `traj_parse._sn_rows` and
`gen_okf.sn_rows` delegating.

**C4 — all four `Founded` discharge tests now exist** (WI-429:
`check_doc_refs.symbol_findings`; SN = the coverage rung; SR =
`derive_gate._decomposed_sr_ids:569`; TC = the `Evidence` existence half).
`Founded` is computable for all four tiers today.

---

## A. The re-derived step sequence

**The enum-close-first rule, restated executably:**

> At every commit, the declared Status enum equals exactly the set of values at
> least one live predicate recognizes, and that set narrows monotonically.

| # | step | edits | preconditions | act type |
|---|---|---|---|---|
| 0 | Re-measure | nothing | spine lanes settled | mechanical |
| 1 | **Close the vocabulary at its live truth + route to the integrity floor** | `trace.ENUM_FIELDS` (`trace.py:312`): `Status: {Draft, Planned, Modified, Verified}` under SR, TC, and a **new LLR key** (LLR has no ENUM_FIELDS entry at all today); split the Status arm of `schema_findings` into an integrity-class producer joined at `trace.py:3012` | none | mechanical |
| 2 | **Repair `Planned`-blindness** | `is_planned` in `trace.py` + `derive_gate.py` + the `test_rule_sync` pin; wire into `traj_status.py:202`, `gen_open_items.py:665`, `check_trajectory.py:3477`/`3520`, `dispatch._TC_NOT_RED` (`dispatch.py:835`), and a `planned=N` basis counter (`derive_gate.py:971-975`, `basis_line:1036`) | step 1 | mechanical |
| 3 | ~~D-1 anchor half~~ → **the `archive/last_approved/` snapshot mechanism** (superseded §D; see the snapshot design doc) | — | step 1 | mechanical |
| 4 | **`is_drifted` as a derived overlay, running ALONGSIDE `is_modified`** — drift = the live row differs from its `last_approved` copy; `reattest_model` (`trace.py:1976`) selects `modified OR drifted`; `gen_open_items.py:665` same | step 3 | mechanical |
| 5 | **THE RENAME — three of four values, no judgement moves**: `Draft`→`Drafted`, `Planned`→`Approved` (per §C fold-out, if ruled), `Verified`→`Approved`; predicates (`trace_text.py:45`, `trace.py:133`, `derive_gate.py:233/238`); the `derive_gate` table edit (C2); basis counters; PROCESS.md §4/§7, PROCESS_OPTIONS.md; the 4 spine templates; ~185 test literals *(transient)*. Enum narrows to `{Drafted, Approved, Modified}` — **`Modified` survives as transitional** | steps 1–4 | mechanical |
| 5b | **D12 off-spine rename, same commit**: `BIF_MATURITY` `"draft"`→`"drafted"`; `approval` cells in interfaces.toml + external.toml; both headers | step 5 | mechanical |
| 6 | **⟵ THE SIGNING ACT.** Owner rules each `Modified` row; `intake._apply_flips` (`intake.py:1570-1600`) writes `Approved`; the snapshot copy to `archive/last_approved/` rides the same reviewed commit | brief regenerated post-step-5 | **SIGNING** |
| 7 | **Retire the transitional word**: delete `is_modified` (`trace.py:142`, `derive_gate.py:335`); enum → `{Drafted, Approved, Founded}`; `test_rule_sync` gains the **negative** assertion (no predicate honours a retired word); retire `trace._changed_cells`' suppression (`trace.py:1948` — retire, do NOT re-key); resolve `intake.py:1591` into a refusal | step 6 clears the last `Modified` | mechanical, gated on 6 |
| 8 | `Founded` computed + **`sr_bar` ceiling**: `sr_bar` (`derive_gate.py:309-311`) stops at `BAR_TESTS`; DevBar-Release becomes unreachable-by-cell, an owner-visible declared gap, until the harness driver lands (repo-lock D-9's own CORRECTION, `docs/repo-lock.md:400-423`) | step 7 | mechanical + one owner ruling |
| 9 | Regenerate; confirm the gate | step 8 | mechanical |

**Steps 0–5b and 8's code precede the signing. Step 6 alone IS the signing**
(ruling 14e: the transition rides the wave). Step 7 is follow-on bookkeeping in
the same reviewed act.

---

## B. Code touchpoint table (complete; risk graded per sitting-3 §3.1)

### Predicates
| file:line | current | must become | risk |
|---|---|---|---|
| `trace_text.py:45-51` | `is_draft` | `is_drafted` | LOUD |
| `trace.py:133-139` | `is_verified` | `is_approved` | LOUD |
| `trace.py:142-154` | `is_modified` | retires at step 7; `is_drifted` succeeds | **SILENT** |
| `derive_gate.py:233-235, 238-242, 335-342` | same trio | same | mixed |
| `tests/test_rule_sync.py:53-120` | pins the copies equal + mutual exclusion | moves in the SAME commit; adds the negative assertion | **SILENT if omitted** |

### Vocabulary declaration
| file:line | current | must become | risk |
|---|---|---|---|
| `trace.py:312` ENUM_FIELDS | no Status anywhere; no LLR key at all | Status under SR/LLR/TC, narrowing per §A | **SILENT** |
| `trace.py:1191-1206` | schema class, Release-only | Status arm → integrity class at `trace.py:3012` | **SILENT** (C1) |

### Drift / re-attest
| file:line | current | must become | risk |
|---|---|---|---|
| `trace.py:1976, 2280` | `statuses=("modified",)` | snapshot-drift selector | **SILENT — the hard coupling** |
| `trace.py:2277` | "No Modified SR — nothing owes a re-attest" | drift predicate | **SILENT — clean bill on an unmigrated tree** |
| `trace.py:2054, 2065, 2072` | `state == "draft"` arms | `"drafted"` | **SILENT** (renders ratify as reattest) |
| `trace.py:1948` | `_changed_cells` suppression of Verified→Modified | **retire, never re-key** | **SILENT, HIGH** |
| `trace.py:1886-1930` `_attested_baseline` | git walk for newest `Verified` rev | keys off the snapshot — the walk dies under D-9 (no flip → newest-Approved rev is HEAD → empty diff **by construction**) | **SILENT** |
| `gen_open_items.py:665` | `("modified","draft")` | `("drifted","drafted")` (+planned pre-fold) | **SILENT — the owner's decision surface** |

### CLI / harness contract
| file:line | current | must become | risk |
|---|---|---|---|
| `trace.py:3762, 3785` | `--ratify` reserved scope `"modified"` | renamed; **closed set** `_RESERVED_RATIFY_SCOPES`; `_scope_srs` raises on a scope matching nothing (empty brief = refusal, not output) | **SILENT, HIGH** — today falls through to an empty brief at exit 0 |
| `check.py:840-850` | `ratify-fresh` hardcodes `--ratify modified --check` | same commit as trace.py:3762 | **SILENT, HIGH** |
| `check.py:989` `_BASIS_RE` | `drafts=(\d+)…modified=(\d+)` | moves with `basis_line`; add a producer-consumer round-trip pin (`check._BASIS_RE.search(derive_gate.basis_line(result))`) | **SILENT, HIGHEST** (twelve-commit precedent at `check.py:1046-1050`) |

### Gate arithmetic
| file:line | current | must become | risk |
|---|---|---|---|
| `derive_gate.py:309-311` `sr_bar` | `decomposed and verified → BAR_RELEASE` | ceiling at `BAR_TESTS` (step 8) + regression pin | **gate RISES** |
| `derive_gate.py:718-745` `spine_stage` | the OI-21 5c rung predicates | the C2 table edit — same file, same predicates, ONE sequence | coupling |
| `derive_gate.py:971-975, 1036-1085` | `drafts=`/`modified=` counters | rename with the value | **SILENT** via check.py:989 |
| `derive_gate.py:513-518, 522-539` | BIF/CMP maturity maps | `"drafted"` (5b); CMP `"planned"` collision → §C | LOUD |

### Writers
| file:line | current | must become | risk |
|---|---|---|---|
| `intake.py:1564, 1597` | writes `"Verified"` | `"Approved"` | LOUD |
| `intake.py:1591` | `if status != "Modified": continue` | unchanged through step 6; **becomes a refusal at step 7** | **SILENT if left** |
| `gen_cases.py:206` | `status = "Draft"` | `"Drafted"` | LOUD |

### Read-only consumers
`traj_status.py:202-215` (**SILENT** — pending-owner-actions projection) ·
`traj_parse.py:131-133` (LOUD) · `dispatch.py:835` `_TC_NOT_RED` (loud) ·
`check_trajectory.py:3477` (loud) · `check_trajectory.py:3520` (**SILENT** —
amend-without-flip guard) · `trace.py:1609/1681/2483`, `spine_carrier.py:687-914`,
`check_docs.py:558` (inert today) · `hats.py:34`, `migrate_carrier.py:561-564`
(prose/frozen).

### Shipped prose + templates
`PROCESS.md:321-342, 487, 545, 580, 923` · `PROCESS_OPTIONS.md:165-201, 228` ·
`EXAMPLE.md` · `ADOPTING.md` · `KICKOFF_PROMPT.md` · `README.md` ·
`RESYNC_PACK.md` (migration entry) · `registry-machinery-reference.md` ·
templates: `system-requirements.template.toml:25`,
`low-level-requirements.template.toml:21` (**ships `status = "Planned"`** — §C),
`test-cases.template.toml:23`, `stakeholder-needs.template.toml`,
`interfaces.template.toml:23`, `external.template.toml:28`. Prose moves **in
step 5's commit** — earlier makes live documentation false.

---

## C. `Planned`'s fate — RECOMMENDATION: fold out into `Approved`

Measured *(transient)*: SR 10 · LLR 2 · TC 2 carry `Planned`, plus the shipped
`low-level-requirements.template.toml:21`. Driven finding: **`Planned` reads
identically to `Bananas`** — no predicate anywhere recognizes it:

- `traj_status.py:202` — a Planned SR projects **no pending owner action**.
- `trace.py:1976`/`gen_open_items.py:665` — in **neither** the re-attest brief
  **nor open-items.html**.
- `check_trajectory.py:3520` — never scanned by the amend-without-flip guard.
- `derive_gate.py:971-975` — in neither `drafts=` nor `modified=`.

So sitting-3 §3.5 understates it: `Planned` is not merely outside D-9's ladder,
it is outside **every predicate in the repo** — the §3.1 SILENT direction,
already firing (WI-458 measured it: seven LLR amendments riding no surface).

**Option 1, fourth rung:** enum grows; predicate quadruplication; a
`spine_stage` rung decision; and a **fatal collision** — `CMP_MATURITY`
(`derive_gate.py:526`) maps `"planned"` → DRAFTED, so under D12's one shared
vocabulary the same word would mean DRAFTED for components and above-Drafted
for the spine — the exact `Stable`-in-two-columns defect interfaces.toml's
header records. Requires re-opening the uniformity ruling.

**Option 2, fold out:** `Planned` means "text ratified, evidence not
established" (its two authoring sites: `traj_status.py:213`, `trace.py:2273`).
D-9's `Approved` means the same rung; the Planned-vs-Verified distinction is
the **pass claim**, and D-9 deletes the pass rung (repo-lock: *"`Verified` is
not re-pointed, it ceases to exist"*). Cost: 14 rows + one template line + a
RESYNC entry. Hazard: post-fold a decomposed ex-Planned SR would read
BAR_RELEASE under today's `sr_bar` — **mitigated by step 8's ceiling**, owed
independently.

**Recommend Option 2** — (i) same rung semantically; (ii) Option 1 is a direct
D-3/D12 one-name-one-meaning violation; (iii) 14 rows and no code vs a
re-opened ruling. Step 2 (`is_planned`) is still cheap insurance meanwhile,
deleted again at step 5.

---

## D. ~~The anchor coupling — build TextHash/HashedOn now~~ **SUPERSEDED**

Owner directive 2026-08-15: no hashes, no commit-id walks — **approved spine
changes copy their documents to `archive/last_approved/`; the adjudicator, the
human re-attest read, and the HTML generators diff live vs snapshot.** The
snapshot design doc owns the mechanism. What this section proved still stands
and transfers:

- **Option A (keep selecting the retired literal) is rejected** — the brief
  returns clean-bill forever at exit 0 once the last `Modified` clears.
- **Option B′ (reuse the git walk) is dead under D-9 by construction** — with
  no Status flip on amendment, `_attested_baseline`'s newest-`Approved`
  revision is HEAD and the diff is empty. A baseline **outside the live file**
  is forced; the snapshot is exactly that, minus the hash bookkeeping.
- The engine that computes comparable row text **exists and is tested**:
  `check_trajectory.normative_text` (:3285-3301), `sn_normative_text` (:3312),
  `digest` (:3332), `current_digests` (:3338-3371),
  `tests/test_attestation_digest.py`. The snapshot design should reuse
  `normative_text` as the row-comparison basis and skip `digest` entirely.
- D-1's on-row items (two columns, the writer, `_DIGEST_EXCLUDED` additions,
  the co-mutation guard, template columns) die with the anchor. Its **third
  cell class** question and Q3 (how far back the guard compares) transfer to
  the snapshot design.

---

## E. The authority extension (§3.6) — RECOMMENDATION: keep the ordinal, add a declared list

Existing: `agent_common.ratification_level` (:456-483, int 0-4, out-of-range
malformed never clamped), `DIAL_HOLDS` (:536-553, the declared level→rungs
lookup), `human_holds` (:556-589, unreadable/unrecognized ⇒ held),
`dispatch._kind_action` (:256-286). Off-spine approval cells are protected by
**prose only** (`external.toml:50-56`, `interfaces.toml:35-40`).

The gap: `human_holds` answers *"does this stage surface to a human?"*, never
*"who may write this cell?"* At any dial below 4, an attestation-kind WI
dispatches and nothing stops a loop session writing `approval = "approved"`.

**Recommended shape — additive, ordinal untouched:**

```toml
[attestation]
human_ratification_through = 4          # unchanged, spine tiers only
# NEW (D12/§3.6): registries whose APPROVAL cells only a human may move,
# in a reviewed Status-change commit. Spine governed by the ordinal above.
# An UNLISTED approval-carrying registry is HELD, not free.
human_approval_registries = ["interfaces", "external", "components"]
```

Why not a tier-set replacement: `DIAL_HOLDS` is already the set-valued lookup
(the ordinal is its key); OI-21 ruled the dial does not move
(`agent_common.py:487-494` — re-keying is silently-less-human by the back
door); and "through" semantics are meaningless over unordered off-spine
registries. Enforcement: `agent_common.human_approves(docs, registry)` (one
home, mirroring `human_holds`), read by `dispatch._kind_action` and any writer
that would set `approved`; ship the key in the process.toml template
(test_dogfood_sync structure rule).

---

## F. Top 5 silent-laundering risks, each with its mechanical guard

1. **Basis-line rename blinds `check.py:989`'s window detector** — twelve gate
   steps stop running (measured precedent at `check.py:1046-1050`). Guard: move
   `_BASIS_RE` with `basis_line` in one commit + a producer-consumer round-trip
   pin.
2. **`--ratify modified` becomes an empty brief at exit 0** (`trace.py:3762`
   falls through to a no-match scope). Guard: closed reserved-scope set;
   `_scope_srs` raises on empty resolution.
3. **An unmigrated `Modified` row vanishes from the brief** (§3.1's row).
   Guard: the enum-close-first rule on the integrity floor + the negative
   rule-sync assertion.
4. **The migration removes the only drift detector** (§3.3). Guard: the step
   ordering — `is_drifted` (snapshot) runs alongside `is_modified` through
   step 6; `is_modified` retires only after the successor has run live.
5. **`Planned`→`Approved` raises the gate for rows that never passed**
   (`sr_bar` → BAR_RELEASE). Guard: step 8's ceiling + a regression pin
   (`sr_bar(Approved-and-decomposed) == BAR_TESTS`).

Runner-up: `trace.py:1948`'s suppression — retire it, never re-key; a mis-keyed
successor suppresses the one cell the brief exists to show.
