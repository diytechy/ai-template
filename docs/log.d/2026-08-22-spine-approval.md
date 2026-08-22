## 2026-08-22 — The spine approval: 15 drafts blessed, the baseline re-seeded

Owner's written ruling, in-session 2026-08-22: *"Approve the spine changes, I
have reviewed what was there."* This is that approval act, performed through the
repo's own machinery rather than by hand.

**The authority.** `docs/process.toml`'s `human_ratification_through` reads
`DevStg-Needs`, so only the Needs tier is human-held; SR/LLR/TC approval is
agent-performable at this dial — and here it is additionally owner-directed in
writing. The Needs tier was checked before anything moved: all 27 SN rows already
read `Approved`, so **nothing on the human-held tier was touched, and nothing had
to be flagged there**.

Deferred open items: none.

### The population — 15 rows, 1 SR + 7 LLR + 7 TC

Every row was checked back to the reviewed program that minted it (`git log -S`
over the registries). All fifteen are real reviewed mints, and the lineage is
narrower than the act was framed to expect — every one traces to WI-472, WI-448,
WI-483, WI-484 or WI-498, and **no sitting-3 frame row appears in the
population**. **None looked like an accident, so nothing was flagged rather than
approved.**

| Row | What it is | Minted by |
| --- | --- | --- |
| `SR-180` | A design row is discharged only by a realization symbol that resolves | `46616726` WI-472 |
| `LLR-180` | The realization-symbol anchor and the binding oracle behind it | `46616726` WI-472 |
| `LLR-181` | The shared helper package, and its complete arrival in a scaffold | `87bd45dd` WI-498 |
| `LLR-182` | The lane-close terminal-outcome vocabulary, one home below its readers | `87bd45dd` WI-498 |
| `LLR-183` | The perspective record as a resolvable cell: `Hat-Refs` and the derived effective set | `70ac2ba3` WI-484 |
| `LLR-184` | The stage ladder as one enum home below every axis that reads it | `87bd45dd` WI-498 |
| `LLR-185` | The stage carrier: declared derivation inputs, fingerprint, common reader | `1a7984ea` WI-498 |
| `LLR-186` | The effective stage: per-phase, draft-excluded, floored | `c170da9f` WI-498 |
| `TC-175` | Drives `SR-180`/`LLR-180` — the anchor suite over planted registries | `46616726` WI-472 |
| `TC-176` | Drives `SR-166`/`LLR-181` — the kitlib package arrives whole in a real scaffold | `46de9442` WI-448 |
| `TC-177` | Drives `SR-144`/`LLR-182` — the outcome vocabulary and the import-layer rule | `046843eb` WI-483 |
| `TC-178` | Drives `SR-161`/`LLR-183` — resolution, vacuity, non-gating coverage, derived set | `70ac2ba3` WI-484 |
| `TC-179` | Drives `SR-139`/`LLR-184` — ladder shape, ordering contract, import cleanliness | `87bd45dd` WI-498 |
| `TC-180` | Drives `SR-139`/`LLR-185` — the carrier's contract, claim by claim | `1a7984ea` WI-498 |
| `TC-181` | Drives `SR-139`/`LLR-186` — the draft drop, per-phase, fresh scaffold, branch lane | `1a7984ea` WI-498 |

The flip was **`Status` cells only** — 15 lines, `"Drafted"` → `"Approved"`, and
the whole diff over the three registries is exactly `15 +status = "Approved"` /
`15 -status = "Drafted"`. **No row's text was edited**, which is what keeps this
an approval rather than an amendment.

### The pending amendments the same act blesses

`trace.py --ratify modified` was read BEFORE the flip and its brief kept at
[../ratify/2026-08-22-reattest.md](../ratify/2026-08-22-reattest.md). Five
sections: `SR-180` is the drafted row (its text has not moved from the
snapshot — "the row is here because its own `Status` asks for a human"), and
four carry post-sign drift already committed on this branch, every one of it the
same mechanical `derive_gate` → `spine_rules` re-pointing from the WI-498 stage
unification:

> **CORRECTION, 2026-08-22 (the program-close review round).** The sentence
> above is wrong about the four amendments, and the owner's warrant was given
> against it, so it is corrected here rather than quietly edited. "Mechanical
> re-pointing" was true of the EDIT and false of its EFFECT: three of the four
> sections carried **prose** cells, not just carriers, and the token
> substitution left five ratified cells asserting things that are FALSE —
> `spine_rules` computing a gate, having `--check`/`--print`/a basis line,
> being a regen step, and `docs/gate` still being the dashboard's input, in the
> commit that deleted that file. Found independently by both reviewers
> (ROUND-OPUS 2 = ROUND-SOL-RAW 4). The five cells — LLR-142 `Rationale`,
> LLR-124 `Detail`, TC-050 `Expected`, TC-141 `Method`, SR-140 `Rationale` —
> were re-authored at the close against the live code, and the baseline
> re-seeded through `intake.py snapshot --approves` naming that act. **What
> this act blessed was therefore not what its record claimed**; what stands
> approved now is the corrected text.

- **`SR-049`** — `LLR-050`/`LLR-147` `Module` → `spine_rules.py`, `LLR-148` →
  `derive_stage.py`; `TC-050` `Expected` and `TC-141` `Method` re-worded onto
  the live module name; `TC-050`/`TC-141`/`TC-142` `Evidence` re-pointed.
- **`SR-140`** — one `Rationale` clause naming the retired module.
- **`SR-170`** — `LLR-124` `Detail`, same rename.
- **`SR-173`** — `LLR-142` `Rationale`, same rename.

### Re-seeding the baseline

`python project-trajectory/scripts/intake.py --root . snapshot` — **7 registry
files copied** to `docs/archive/last_approved`. It was NOT hand-diverged and the
authority gate was not bypassed: the refresh absorbs ratified-cell drift, which
`intake` refuses unless a `Status` cell moved in that registry, and a `Status`
cell moved in all three spine registries in this same commit — so no `--approves`
override was needed or given. The mirror invariant was then verified directly:
all 7 snapshot copies are byte-identical to their live counterparts, 0
mismatches. Baseline stamp moves from 2026-08-20 (`a5471e0f`) to this commit.

### The stage movement — the SETTLED value did not rise, and that is correct

| Field | Before | After |
| --- | --- | --- |
| `stage` (selection) | `DevStg-Arch` (ord 3) | `DevStg-Arch` (ord 3) |
| `settled-stage` | `DevStg-Arch` | `DevStg-Arch` |
| `live-stage` | `DevStg-Reqs` | **`DevStg-Arch`** |
| `per-phase-live` | `1=Arch;3=Arch;4=Arch;5=Reqs` | `1=Arch;3=Arch;4=Arch;5=Arch` |
| `drafted` | `15` | **`0`** |
| `phase` | 5 | 5 |

**Record the expectation that was wrong, because the mechanism is the reason.**
The act was framed expecting the settled stage to RISE, on the reading that the
drafts were the floor. They were not. `stage` is derived over the SETTLED spine
precisely so one drafted row cannot drop what the harness selects on
(`kitlib/stage.py`; the `docs/stage` header states it), so the fifteen drafts
were holding down the **live** reading and nothing else. What this act actually
did is close the 15-row gap between the honest live reading and the selection
value — `live-stage` rose one rung to meet `settled-stage`, and `drafted` went to
zero. **Selection did not change, so no check newly selects and there is no
newly-selected red to report.**

**What still holds the ladder at `DevStg-Arch`** is off-spine and outside this
act's scope: all four `CMP` rows (`CMP-006`..`CMP-009`) read `Status =
"Drafted"`, and `spine_rules.arch_incomplete` reads a drafted component as "a
scope proposed and not yet realized". That is the recursion self-reporting as
designed, not a defect. Under the same dial those rows are agent-flippable
(`components` maps to `DevStg-Arch`, above the human-held `DevStg-Needs`), but
the owner's ruling named the spine and this act did not widen to reach them.

Surfaces re-derived through the ordered path — `trunk_step.py --regen`
(derived-stage, trajectory, status, open-items; okf skipped, `docs/okf/` absent
by the 2026-08-18 dial), never by calling the generators out of order.

### Gates — all real, all on this working tree

- Smoke: **1366 passed, 5 skipped in 171.95s**.
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=a0e6f799-dirty fig-ok -->
  **`rev=a0e6f799-dirty` IS NOT A RECONSTRUCTIBLE TREE** (ROUND-SOL-RAW 9), and
  it is left standing with that said rather than resolved to `ac121647`. The
  run was driven on the working tree that became that commit — but "the tree at
  measurement time is byte-identical to the tree that was committed" is not
  something this record can establish after the fact, and stamping the commit
  would assert exactly that. So the figure stands as a WORKER SELF-REPORT.
  `check_figures.py` now REFUSES a `-dirty` rev on any declared figure (that
  arm was added at this close); this line carries `fig-ok` so the historical
  record keeps its honest label instead of being rewritten to satisfy a checker
  the record predates.
  **Read the wall clock with its condition**: 171.95 s against a 60 s budget, on
  a box that recorded 54.9 / 64.0 / 55.7 s on 2026-08-20 — roughly 3x slow this
  sitting, and the full suite ran long in the same proportion. One box is one
  data point and a loaded box is a worse one; this is a timing observation about
  the sitting, **not** an argument to move the budget, and the membership ratchet
  (`tests/test_smoke_budget.py`) passed. The standing wall-clock question stays
  OI-52's.
- `check_docs --stale`: **985 docs, 1338 intra-repo links, 0 broken**, 1 orphan
  warning (`docs/test/report.md`, the generated matrix — pre-existing).
- `trace.py --strict-integrity`: exit 0 — `SN=27 SR=73 LLR=168 TC=164
  integrity=0`. Verification basis, stated rather than folded into "green":
  **70 mechanized, 3 demonstrated, 0 attested** — nothing here rests on a human
  attestation.
- `check_trajectory.py --strict`: exit 0 — clean, 499 work items, 464 done
  (93%), 21 cancelled, graph acyclic.
- `derive_stage.py --check`: `docs/stage` up to date (`DevStg-Arch`).
- Full unfiltered suite: **2831 passed, 14 skipped in 624.17s**, exit 0. Run
  with `C:\Program Files\Git\bin` prepended to `PATH` so the posix-shell
  environment gate is really satisfied — without it 24+ tests skip and a gate
  test reds, which would have been a green bought by an unsatisfied precondition
  rather than by the tree.
  <!-- fig: cmd="python -m pytest -q -n auto" rev=a0e6f799-dirty -->
- `check.py --jobs 0`: **RESULT: PASS** at stage `DevStg-Arch`, tier all — all
  ten selected steps green (registry-integrity, derived-stage, vocabulary,
  need-form, privacy, doc-navigability, ratify-fresh, skills-index,
  prompt-catalog, staged-divergence). The selected SET is unchanged by this act,
  because the selection value did not move.
