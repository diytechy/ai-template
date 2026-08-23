## 2026-08-23 — WI-484 phase 3: the generated component view, and `DetailDoc` retires

Executed OI-32's ruling (d) for phase 3 only. Phases 2-writer / 2-duplication
(spec items 2–3) and 4–5 are untouched and stay owed.

**The four things landed together, because the wiring test fails BOTH ways.**
Proven before wiring, not assumed:

- `[generated]` row without a `WIRED` entry →
  `test_every_declared_generated_artifact_has_an_enforcer` FAILS: *"declared
  generated with NO freshness enforcer (SN-010 is a universal, so one of these
  makes it false): {'docs/requirements/components.derived.toml': 'components'}"*.
- `WIRED` entry without the `[generated]` row → the same test's reverse arm
  FAILS (*"this table names kinds docs/stack.ini no longer declares"*) and so
  does `test_every_wired_enforcer_is_a_real_step_and_runs_in_the_commit_floor`
  (*"components: no step named 'component-view' in the plan"*).

So the change carries all four at once: `scripts/gen_components.py`,
`docs/requirements/components.derived.toml`, the `docs/stack.ini` `[generated]`
row (`= components`), the `component-view` step in `check.py` (built-in, at
`DevStg-Impl` like its generated-artifact siblings, registered in
`BUILTIN_STEP_NAMES`, in `_TRUNK_FRESHNESS_STEPS`, and in the shipped
`hooks/pre-commit` `--run-steps` floor), and the `WIRED` entry. Two things the
brief did not name were added for the same reason: a `component-view` entry in
`trunk_step.REGEN_STEPS` (without it the trunk's `--regen` leaves the artifact
stale and reds the next `check.py` for no real defect — it is a LEAF like
`open-items`, nothing reads it back), and the `bootstrap.py` `MAPPING` row, since
the generator is kit machinery and must reach an adopter.

**The view's shape.** One `[derived]` census table, one
`[component_view.CMP-###]` per declared component, one repo-wide `[unplaced]`.
Per component: `name`, `sr_refs`, `sr_shared_refs`, `llr_refs`, `hat_refs`,
`modules`, `seam_internal_refs`, `seam_boundary_refs`. The table name is
`component_view`, deliberately NOT `component`: `spine_carrier` keys a CMP row
off the `component` table, so a second file using that name would present itself
to every CMP reader as a second components registry. **No approval, maturity or
standing cell appears** — the hand file declares the component and holds its
approval, this file describes it; a test pins that neither `Approved` nor
`Drafted` appears in any emitted cell.

**The three coverage edges — RE-MEASURED at HEAD first, because the brief's
counts have all moved, and answered in the OUTPUT rather than in the
generator's head.**

Measured BEFORE the design, on the tree at `d6818b0b` (i.e. before this slice's
own six spine rows): childless SRs **5** (brief: 12), multi-component SRs **7**
(brief: 6), component-tagged IF rows **62 of 130** (brief: 57 of 125), and 0 of
the 68 untagged rows unplaceable by endpoint. The same census AFTER the slice,
read off the artifact it produced:

fig: cmd="python project-trajectory/scripts/gen_components.py && python -c \"import tomllib;print(tomllib.load(open('docs/requirements/components.derived.toml','rb'))['derived'])\"" rev=d6818b0b-dirty — `{'components': 4, 'design_rows': 181, 'seam_rows': 135, 'requirements_placed': 70, 'requirements_unplaced': 5, 'seams_unplaced': 0}` (the +1 design row and +5 seams are this slice's own `LLR-199` and `IF-139`–`IF-143`; 65 of the 135 now carry a `Component` cell).

1. **The childless SRs — 5, not 12** (`SR-034`, `SR-036`, `SR-114`, `SR-163`,
   `SR-181`), and all five are now `Approved`, where the brief expected nine
   `Drafted` rows that would acquire children. Three are the brief's named
   never-members (constraints over every component: stdlib-plus-ledger,
   cross-OS, human-actor re-sync). **The answer: one repo-wide `[unplaced]
   sr_refs` list, counted in `[derived]`, and the view does NOT distinguish
   "not yet decomposed" from "constraint over everything".** It cannot: no
   registry cell carries that distinction, and hard-coding a per-repo list of
   never-members inside shipped kit machinery would mandate a token about rows
   an adopter can never read (the CLAUDE.md copy-ready rule). The reading is
   stated in the emitted header, so a reader can tell "deliberately outside
   every component" from "the generator lost it". **Noted, not acted on:**
   `SR-163` and `SR-181` are Approved with no LLR and no TC and are already
   `trace.py`'s standing orphan findings — WI-508's subject, not this slice's.
2. **The multi-component SRs — 7, not 6** (`SR-049`, `SR-070`, `SR-139`,
   `SR-146`, `SR-152`, `SR-155`, `SR-170`). **The answer: the SR appears in
   EVERY component it reaches, AND in each of their `sr_shared_refs`.** Both
   halves matter — listing it once would pick an owner the registries do not
   name, and listing it in both without marking it shared reads as a duplicate.
3. **The seams — they DO enter the view, and every one is placed.** 62 of the
   130 measured at design time carry a
   `Component` tag; the other 68 resolve through their endpoints
   (`ThisProject`/`Counterpart` → `LLR.Module` → `Component`) using
   `trace_text.norm_module`, the SAME normalizer `trace.interface_findings`
   already joins on — a second reconciliation would be a second answer waiting
   to disagree. Placement is the tag UNIONED with the endpoint resolution,
   because the two disagree on 38 of the 62 tagged rows and the disagreement is
   not an error: the tag names the row's OWNING component while the endpoints
   span the pair, and a seam between two components is a boundary of BOTH.
   Classification is the components layer's own rule (both endpoints inside →
   internal, otherwise → boundary). **Measured at HEAD: 0 unplaceable.** A row
   that resolves nowhere is named in `[unplaced] seam_refs`, never dropped —
   pinned by a test, since today's zero is a property of this repo and not of
   the generator.

**`detail_doc`'s disposition: RETIRED, and nothing had to be migrated.** No live
CMP row carries it (measured — the key is absent, not empty, on all four); the
only value anywhere was the shipped template's `docs/cmp/example.md`, pointing at
a directory the kit never creates. Removed from
`registries/components.template.toml` (row + its `notes` gloss),
`spine_carrier.OFFSPINE_COLUMN` + `OFFSPINE_KEYS["CMP-ID"]`, `migrate_carrier.KEY`,
`PROCESS_OPTIONS.md`'s Component layer (three places) and
`knowledge/README.template.md`, plus the six test fixtures that carried the
column. Dropping the `migrate_carrier.KEY` entry is the sanctioned retirement
shape, stated in that file for the IF tier's `Status`: a stray legacy cell now
keys as `DetailDoc` and is caught by the schema tier rather than silently
absorbed. The three "living pointers" the brief worried about are **not** this
column's — they are SN-027/SR-049/SR-043 rationale cells citing archived specs,
and the ruling left their disposition as a separate question; nothing here
touched them.

**Spine acts, all minted `Drafted`** — the standing precedent, since a snapshot
refresh is REFUSED at HEAD on LLR-147's pre-existing drift, so no approval is
claimable (verified: the refusal is still there and was not fought):
`LLR-199` (the view, `code_symbol = build/render/seam_placement/module_components`,
CMP-009), `TC-195` (fourteen cases), and five IF rows for the module's declared
seams — `IF-139` (provides the `--check` CLI to `check.py`), `IF-140` (provides
the artifact), `IF-141` (consumes `trace.effective_hats`), `IF-142` (consumes
`spine_carrier`), `IF-143` (consumes `trace_text.norm_module`). The three
`Consumes` rows are the cross-component crossings the architecture rule requires
(this module is CMP-009, all three counterparts are CMP-006); `TC-195` cites all
five so the seam-TC coverage rule is satisfied at mint rather than allow-listed.
Watermark: `IF 138 → 143`, `LLR 198 → 199`, `TC 194 → 195` (`trace.py --bump-ids`).

**Deviations from spec.** Three, each recorded rather than folded in:

1. The brief's counts were all stale and the re-measurement changed one answer's
   shape — with five childless SRs all `Approved`, the "nine will acquire
   children" reading no longer holds, which is why `[unplaced]` is a plain list
   with a stated reading rather than a two-way split.
2. `trunk_step.REGEN_STEPS` and the `bootstrap.py` MAPPING row are additions the
   spec's four-things rule did not name; both are load-bearing (see above).
3. The generator imports `trace` for `effective_hats` rather than re-deriving the
   union. That is a deliberate CMP-009 → CMP-006 edge on the `IF-075` precedent
   (`gen_open_items` → `trace`): a second copy of the derivation would be a
   second answer, and the whole value of the cell is that a parent re-ruling
   propagates with no child edit.

**Ratchets re-stamped, with reasons at the stamp** (never to green a step):
`check.py` 2332 → 2351 (+19: the step tuple, its `BUILTIN_STEP_NAMES` row, its
`_TRUNK_FRESHNESS_STEPS` membership, and the ten comment lines recording why the
step ships with the artifact); `bootstrap.py` 3124 → 3125 (+1: the MAPPING row);
`[smoke-budget] max-tests` 1280 → 1294 (+14 collected, one new in-process module,
13 of 14 with no subprocess; +8 headroom over the measured 1286).
NOT re-stamped, deliberately: `tests/test_complexity_ratchet.py` fired on the
generator's own `build` at 11 against the limit of 10, and the answer was the
one that file's own rule prescribes — DECOMPOSE, do not bump. `build` is now
three named folds (`_blank`, `_add_members`, `_add_seams`) and no baseline row
was added. `tests/test_check_lane.py`'s whole-set contract on
`_TRUNK_FRESHNESS_STEPS` was edited, because that set genuinely gained a member;
the edit carries its reason inline, as that test's own comment demands.

**Adopter surface.** `bootstrap.py` MAPPING + docstring module list,
`tests/test_bootstrap.py` file list, `README.md` kit-contents table, and a
`RESYNC_PACK.md` entry `[since f1cc0b44]` naming the four steps an adopter takes
(copy the generator, declare the `[generated]` row in THEIR stack.ini, generate
once, and dispose of any `detail_doc` cell they carry).

**Scaffold-verified by bootstrapping, not by reading.** `bootstrap.py --dest
<scratchpad>/scaffold-wi484` → 153 files; `scripts/gen_components.py` is
byte-identical to the source (`diff`, zero output); the scaffold's
`components.toml` no longer carries `detail_doc`; and in the scaffold
`python scripts/gen_components.py` and `--check` both exit 0 with *"no real CMP
row … nothing to derive (vacuous)"*, as does
`python scripts/check.py --run-steps component-view`. A blank-registry scaffold
never crashes and never reds.

**Byte deltas, one line per touched budgeted file:**
`project-trajectory/PROCESS_OPTIONS.md` 177,715 → 178,307 (**+592** FLAGGED: the
Component layer now records the generated view and states that the row carries no
approval; the `DetailDoc` sentences it replaces were shorter) — watched row
re-stamped. `project-trajectory/skills/byte-budget-guard/SKILL.md` 4,835 → 4,827
(-8, its own re-stamp; 173 under its 5,000 cap), all three tracked copies in this
commit. `AGENTS.template.md` (9,980), `CLAUDE.md` (7,827) and `PROCESS.md`
(85,862) untouched.

**Gates.**

fig: cmd="python -m pytest -q -n auto -m smoke" rev=f1cc0b44-dirty — 1281 passed, 5 skipped in 22.22s (1286 collected against the re-stamped 1294 ceiling).

`python scripts/check_smoke_budget.py --mode enforce` — 20.1s vs the 60s budget,
within.

`python project-trajectory/scripts/check_docs.py --root . --stale` — OK, 1034
doc(s), 1356 intra-repo link(s), 0 broken (1 orphan warning, pre-existing).

`python project-trajectory/scripts/check_trajectory.py --strict` — exit 0. Every
WARN it prints is pre-existing and unrelated (IF/LLR CodeSymbol tag drift,
over-long open-WI titles, the `if-tc-coverage-allow` entry naming the retired
IF-130). `trace.py --strict` still exits 1 on the four pre-existing SR-163 /
SR-181 orphan findings — WI-508's subject, untouched here, and confirmed present
before this slice.

fig: cmd="python -m pytest -q -n auto --basetemp=D:\pytest-tmp-w484b" rev=f1cc0b44-dirty — 2925 passed, 14 skipped in 1044.21s (0:17:24), run because this is a broad script change. Two edits landed AFTER that run started and are named rather than hidden: `ruff format` on `tests/test_components_registry.py` + `tests/test_gen_components.py` (whitespace only — both modules re-run green afterwards, 29 passed), and this fragment plus the status/spec prose. The smoke tier and all four checks above were re-run on the FINAL tree.

Pre-existing and NOT fixed here (confirmed present at `HEAD` before this slice,
so not this change's to carry): `ruff check` reports two unused imports,
`tests/test_agent_loop.py:16` (`inspect`) and `tests/test_trace_hats.py:38`
(`pytest`).

Deferred open items: none — this slice raised no question the owner must rule.
The two it could have (whether `SR-163`/`SR-181` should be decomposed, and the
disposition of the five archived mechanism documents) are already carried: the
first by WI-508, the second by OI-32's own recommendation, which states it as a
separate question the row still owes.
