<!-- Copied verbatim on 2026-08-30 from C:/Projects/ai-template-plans/complexity-pushback/PLAN.md — the plan of record for the rows that cite it; its companions there (the source reports, the prototype, the drafts, the review transcripts) stay outside the repo. -->

# complexity-pushback — repo-integration plan

**Status:** plan only. Nothing in `C:\Projects\ai-template` was modified writing this.
**Written:** 2026-08-29. **Read at:** `ai-template` HEAD `85fb3742` (branch `contract_split`).
**Working tree at survey time was dirty in four paths** — `PROJECT_STATE.html`,
`docs/decisions-for-review-2026-08-29-slices-4-6.md`, `docs/stage`, `docs/status.md`,
plus an untracked `docs/log.d/2026-08-29-owner-rulings-oi67-decisions.md`. Everything quoted
below was read from the working tree EXCEPT `docs/status.md`, which was read at HEAD via
`git show HEAD:docs/status.md`. A session executing this plan must re-read those five paths
before touching them: another session was mid-OI-67-slice-6 the whole time.

**Re-verified after the concurrent session committed.** While this plan was being written the
tree advanced to `b19d4bf7` ("sitting: the owner accepts decisions 4.1, 6.2, 6.7 and 6.8 of the
OI-67 slices — recorded, nothing changes in code") and went clean. That commit touched only
`PROJECT_STATE.html`, `docs/stage`, `docs/status.md`, `docs/decisions-for-review-2026-08-29-slices-4-6.md`
and a new log fragment — none of which this plan quotes normatively. **Every load-bearing
number below was re-measured at `b19d4bf7` and is unchanged:** the watermark still reads
`IF=173 LLR=205 OI=67 SR=182 TC=201 WI=534`, and `wc -c` still gives `PROCESS.md` 87,836 ·
`PROCESS_OPTIONS.md` 179,209 · `AGENTS.template.md` 9,980 · `byte-budget-guard/SKILL.md` 4,795.

**Sources this plan executes:** `..\knowledge-pack-review\00-SYNTHESIS.md` §2, §3 ranks 1–3,
§5 plan 1; `..\knowledge-pack-review\05-compact-code-and-complexity-pushback.md` §2, §4
(P1/P2/P3/P4/P6), §5. **The owner has approved the proposal in principle**; phase 0 is the
ruling that decides its shape, not its existence.

**The script itself is not in this plan.** A sibling agent is prototyping it under
`prototype/` — it now exists (`prototype/check_complexity.py`, 49 tests green, census in
`prototype/analysis.txt` and `prototype/PROTOTYPE-NOTES.md`; see `README.md` beside this file).
The prototype's numbers are the WORKING figures in this plan and the OI brief. Do not copy a
number out of report 05 into a registry cell or a baseline file: report 05's figures were taken
with an unvalidated walker and read materially high (`plan_round.record` 135 there, 61 by the
validated prototype). The shipped script's own first run is the only number that may be stamped
into the repo; the prototype's are what the ruling is read against.

---

## 0. What the program is, in one paragraph

Build `check_complexity.py` — a stdlib-`ast` Sonar-style **cognitive complexity** + SLOC
census per function (plus a reported, ungated public-symbol count per module), with a central
TSV baseline, exact equality in both directions, `--report` / `--restamp`, and **no inline
suppression pragma ever**. Ship it `--report`-only; arming it is an opt-in
`PROCESS_OPTIONS.md` layer. Land it **as a trade, not an addition**: the same ruling that
admits it decides whether `tests/test_module_size_ratchet.py` retires, which is the owner
question already banked in the 2026-08-20 log. Alongside it: a `deep-module-design`
`scope: kit` skill (the one real content gap), and one PROCESS.md §3 bullet formalising the
structure-vs-behaviour commit split that WI-521 slices 1–2 already practised.

**Two rulings constrain everything here and neither is reopened.** **D-7** (2026-08-10) tore
down the *gating* duplication census; any proposal that re-arms a duplication gate is dead on
arrival, and this program adds no duplication check of any kind. **OI-16** (owner correction,
2026-08-12) is the program's warrant: *"the monolith risk was really around function size /
complexity, not strictly file size."*

---

## 1. The seams, exactly as they are today

Each subsection records what the repo does **now**, with the file path and a verbatim
pattern. This is the reference the execution WIs work from; nothing here is a proposal.

### 1.1 OI filing — `docs/requirements/open-items.toml`

**Carrier.** One TOML table per decision, id-keyed and bare: `[open_item.OI-###]`. The file's
own header states the contract (it declares `IF-073`):

```
# Contract IF-073: one `[open_item.OI-###]` table per owner decision, carrying
#     `title`, `status`, `raised`, `one_line`, `decision`, `blast_radius`,
#     `options`, `recommendation` and `wi_refs`. `status` is `pending` or
#     `ruled`, and only a pending row renders as a brief card — a ruled row is
#     history, and the Decisions log is its record. `-000` example rows are
#     dropped, and an absent registry renders an empty queue rather than
#     failing, so a repo carrying no decisions still has the surface.
```

**The `-000` row IS the schema** (`docs/requirements/open-items.toml` lines 16–27), and its
cell values are the authoring guidance. Copied verbatim as the pattern to fill:

```toml
[open_item.OI-000]
title = "Example row - the shape of an owner decision brief"
status = "pending"
raised = "2026-01-01"
one_line = """the one-line form status.md projects - what is being decided, and the recommendation in a clause"""
decision = """What is being decided, who raised it and when, and any context a ruler needs that is not obvious from the one-line."""
blast_radius = """What breaks or changes if this is ruled either way - the honest cost, not the optimistic one."""
options = """Option (a) ... · Option (b) ... · Option (c) ... - each with its FOR and AGAINST, separated by the middot the other registries use for lists-in-cells."""
recommendation = "The driver's recommendation and WHY, in the same voice a reviewer would argue it."
wi_refs = ["WI-000"]
```

**Field census over the 59 real rows** (`grep -oE '^[a-z_]+ = ' | sort | uniq -c`):
`title`/`status`/`recommendation`/`raised`/`options`/`one_line` on all 59; `ruling_ref` and
`ruled_date` on 58; `blast_radius` on 57; `decision` on 49; `wi_refs` on 26. So
`blast_radius` and `decision` are conventionally-required-but-not-schema-required, and
`wi_refs` is genuinely optional — **a brief may be filed with no WI row yet**, which is what
phase 0 does.

**How the fields actually work, read from live rows.**

- `status` — `pending` while it owes a ruling, flipped to `ruled` when the owner answers.
  Only a `pending` row renders as a card. **There is exactly one `status = "pending"` row in
  the file today and it is `OI-000`, the example** — every real OI is ruled. So the phase-0
  brief will be the only live card, which is the surface the owner reads.
- `raised` — the date the question was put, `YYYY-MM-DD`.
- `wi_refs` — `["WI-###"]`, the rows that carry the work. Filled after the ruling for a
  brief filed before any WI exists.
- `one_line` — what `docs/status.md` projects. **The house convention on a ruled row is to
  PREPEND the ruling and keep the original one-line behind it**, e.g. OI-67:
  `"""RULED (a) 2026-08-29 — the owner: "..." Original brief: rule the shape of an interface row; recommend (a): ..."""`
- `decision` — what is being decided plus the context a ruler needs. On a ruled row the
  ruling is written INTO this cell at the top (OI-16 opens `RULED ADDENDUM (owner,
  2026-08-13): ...`).
- `ruled_date` + `ruling_ref` — added at the ruling. `ruling_ref` points at
  `docs/log.md#decisions-log`, `docs/repo-lock.md#d-5`, or a
  `docs/log.d/<date>-<slug>.md` fragment (OI-67 uses
  `docs/log.d/2026-08-29-oi67-ruled-a.md`).
- `options` — lettered, each with FOR and AGAINST. Long rows use `###`-headed markdown
  inside the `"""` string (OI-67 does); short rows use one `·`-separated line (OI-11 does).
- `recommendation` — the driver's call and why, argued in a reviewer's voice.

**How the brief is composed and rendered.** There is no composer script — the brief is
**hand-authored into the TOML row**, and `project-trajectory/scripts/gen_open_items.py`
RENDERS it. That module's docstring is explicit about owning no second opinion:

> ANTI-DUPLICATION, deliberately: the git archaeology and the cell comparison live in
> `trace.reattest_model`, and the pending projection lives in `pending.pending_block`. This
> module imports both and RENDERS.

It emits three ordered sections into `docs/open-items.html`: (1) one card per
`status=pending` row (the one-line, what is being decided, blast radius, options,
recommendation, and the WI rows that carry the work); (2) approval & re-attestation, every
`Drafted`-or-drifted SR with its whole chain; (3) pending owner actions, reused verbatim from
`pending.pending_block`.

**Regen command** (`--root` defaults to cwd, `--check` byte-compares for the freshness gate;
the step name is `open-items` in `check.py` and the `[generated]` row is
`docs/open-items.html = openitems`):

```
python project-trajectory/scripts/gen_open_items.py --root .
python project-trajectory/scripts/gen_open_items.py --root . --check   # the freshness gate
```

**`adjudicate_brief.py` is a different machine — do not reach for it here.** It fills an
*adjudication session's* prompt for a WI row carrying `safety_class = "adjudication"` and a
declared `brief` key (`amendment|disposition|conflict|red-tc`). It has nothing to do with an
open-item brief. Its two governing rules are worth knowing anyway because they bear on how
this program's evidence is presented: *"a judge's brief never contains the claim under
judgement as its premise"*, and *"a half-filled brief is WORSE than the generic prompt — a
brief whose evidence section is thin does not fail loudly, it reads as a completed
investigation that found nothing"* — which is why the OI draft below marks every unfilled
number `<<prototype>>` instead of guessing one.

**What OI-16 already rules, and what it leaves open.** OI-16 (`status = "ruled"`,
`ruled_date = "2026-08-13"`, `wi_refs = ["WI-448"]`) is the common-module doctrine. Two of its
cells carry the part that matters here. The `decision` cell:

> The owner also corrected the reasoning this brief had used against a single large module:
> big files are not inherently a problem, and the monolith risk was always about FUNCTION
> size and complexity, not file length. That correction is accepted and has a consequence of
> its own, in the last bullet below.

and the last bullet of `blast_radius`:

> - The ratchet: the module-size ratchet measures LINES, so a consolidated common file will
>   fire it. By the owner's own correction that is the wrong axis — it should measure
>   function size and complexity. Bumping a line baseline for a file that got SIMPLER is the
>   check asking for the opposite of what is wanted, and it is now the second reason to
>   revisit that ratchet.

**So OI-16 rules the AXIS and explicitly does NOT rule the retirement.** The retirement is
the *banked question*, and it is banked in two homes, both verbatim below.

**Home 1 — `docs/log.d/2026-08-20-program-grind.md` lines 2174–2196** (the 2026-08-20 log the
ratchet's docstring points at):

> - **The module-size ratchet measures the wrong axis, and WI-448 is the second witness the
>   owner's own correction predicted** (OI-16: "the monolith risk was always about FUNCTION
>   size and complexity, not file length"). Concretely: `bootstrap.py` shed two duplicated
>   helper BODIES and gained a MAPPING declaration block, and the line ratchet demanded a
>   reviewed bump on a file that got structurally simpler; meanwhile
>   `agent_common`/`check_trajectory` each lost 230-ish lines of pure duplication and the
>   ratchet's only response was "re-stamp downward". Neither direction told anyone anything
>   about complexity. Note the axis it wants ALREADY EXISTS unused-for-this-purpose:
>   `tests/test_complexity_ratchet.py` runs ruff `C901` per function and, unlike the line
>   ratchet, RECURSES into packages. NOT redesigned here, deliberately — filing it is the
>   WI's instruction. **The question for the owner is whether the line ratchet retires in
>   favour of the complexity one, or the two keep different jobs with the line one demoted to
>   advisory.**
> - **The line ratchet is blind to packages.** `test_module_size_ratchet._census` globs
>   `scripts/*.py` (top-level only), so every module under `scripts/kitlib/` is uncensused —
>   a 3,000-line module could land there and the ratchet would never see it. Not fixed in
>   WI-448 because the fix forces a keying decision (`path.name` collides once two packages
>   hold a `registry.py`; `test_complexity_ratchet` already keys on the relpath) and that is
>   the same axis question above. Cheap to fix, but it should be fixed WITH the ruling, not
>   before it.

(The package-blindness half was since fixed — the ratchet's own docstring now says it
"recurses into packages too since 2026-08-21 (see `_all_modules`)" — which **strengthens** the
trade: *"the two now cover the same files and differ only in what they measure about them."*)

**Home 2 — `tests/test_module_size_ratchet.py`, the closing lines of its module docstring:**

> AND THE SENSOR MEASURES AN AXIS ITS OWN OWNER DISPUTES. The owner's `OI-16` correction is
> that "the monolith risk was always about FUNCTION size and complexity, not file length",
> and WI-448 produced the worked counterexample: `bootstrap.py` shed two duplicated helper
> bodies, gained a MAPPING declaration block, and this file demanded a reviewed bump on a
> module that got structurally simpler. `tests/test_complexity_ratchet.py` measures the
> disputed axis; this census recurses into packages too since 2026-08-21 (see
> `_all_modules`), so the two now cover the same files and differ only in what they measure
> about them. Whether the line ratchet retires in favour of the complexity one or the two
> keep different jobs is an open question for the owner, banked in the 2026-08-20 log; until
> it is ruled, this file stays armed, because an unruled axis is not a reason to stop sensing
> growth.

### 1.2 WI filing — `docs/work/`

**Status is the DIRECTORY**, never a frontmatter field. `docs/work/README.md` declares five
seams (`IF-023`, `IF-024`, `IF-054`, `IF-079`, `IF-159`) in an HTML-comment header; the three
this program touches, verbatim:

- **`IF-023`** — the registry as a validated registry: "One row is one Markdown spec file
  whose `+++` frontmatter carries `id`, `title`, `workstream`, `sr_refs`, `needs` and the
  optional scheduling keys, and whose `## Deliverable` body is the backward-only record; the
  filename repeats the id. STATUS IS THE DIRECTORY, so a spec under a directory outside the
  declared set RAISES rather than being skipped — inventing a folder takes rows out of the
  registry instead of adding a state to it."
- **`IF-054`** — the same registry read for READINESS: "A row offers its status, its `needs`
  edges (an entry prefixed `~` is a SOFT edge and never blocks) and the optional `priority`,
  `exclusive`, `blockref`, `est_tokens` and `safety_class` keys. An absent optional key reads
  as its documented default, and the defaults are chosen to fail closed: an absent safety
  class is `unclassified` and is never scheduled... **A hard edge is satisfied only by an
  integrated `done` predecessor** — a cancelled one never satisfies it."
- **`IF-159`** — the WRITE side and the format's single writer: "one registry row rendered as
  one spec file under the row's status directory, the filename repeating the id, UTF-8 with
  LF endings on every platform. The file is RE-READ and re-parsed before its path is
  returned: a spec whose frontmatter does not reconstruct its source row cell-exact, the
  order key included, raises."

**The writer named by IF-159 is `project-trajectory/scripts/wi_convert.py`.** Row of record in
`docs/requirements/interfaces.toml`:

```toml
[interface.IF-159]
owner = "docs/work/"
requestors = ["scripts/wi_convert"]
channel = "file"
data = "one spec file per row, written and read back cell-exact before its path is returned"
version = "v1"
status = "Drafted"
component = "CMP-006"
```

The function is `wi_convert.write_spec_file(work_dir, row, order=None)` (line 552).
`intake.py` is what MINTS (`_mint`, `_mint_shape_refusal`, `mint_gap_rows`) and drives the
writer.

**The exemplar, `docs/work/queued/WI-000-example.md`** — frontmatter verbatim:

```
+++
id = "WI-000"
title = "EXAMPLE work item (permanent exemplar — keep)"
workstream = "example"
sr_refs = []
needs = []
buildtier = "medium"
priority = 0
+++
```

Its own key documentation, condensed: all keys optional except `id` and `title`; **an absent
key and an empty one mean the same thing, so empty keys are omitted rather than written as a
wall of `= ""`**. `workstream` = the mutable grouping. `sr_refs` = the requirement ids it
delivers. `needs` = predecessor ids; a bare id is a HARD edge, a `~`-prefixed id is a SOFT
edge, "the `~` is meaning, not decoration, and is carried verbatim". `specref` = the forward
bridge (rule R-E), a `docs/specs/WI-###.md` file or a `doc#anchor` that resolves while open
and clears at close. **`buildtier` is the frontmatter spelling** (`strong|medium|quick`;
legacy `weak` reads as `quick`; "the STARTING tier for this item's build sessions and never
caps escalation") — `BuildTier` is the registry-column spelling, not the key. `priority` int
default 0; `exclusive` semantic mutex keys; `blockref` (its PRESENCE is what makes a `queued`
row `blocked`); `est_tokens`; `safety_class` ∈
`ordinary|spine|gate|attestation|protected|high-risk|adjudication`, **fails closed** (absent
reads `unclassified` and is never scheduled); `planmode = "dual"`; `brief` only on an
adjudication row; `order` is a migration artifact a hand-filed spec omits.

**The body while a row is OPEN.** `## Deliverable` is **backward-only (rule R-A)**: it stays
EMPTY while the work is open and is filled with what shipped at close; `check_trajectory`'s
R-A is a hard finding both ways (a non-terminal WI with a filled Deliverable, or a terminal
WI with an empty one). The forward-looking narrative goes in a `## Context` section, which
`kitlib/registry.py::parse_spec_deliverable` clips off before reading the cell
(`SPEC_CONTEXT = "\n## Context\n"`, lines 156–162: "so a minted row whose body is
context-only parses with an empty Deliverable rather than as a malformation").
**`docs/work/active/wi521-decomposition-debt-owner/WI-521-decomposition-debt-owner.md` is the
worked example of that shape** — `## Context` with `###` sub-sections and per-slice landing
records, and no `## Deliverable` at all. Every WI draft in §2 follows it.

**How ids are minted, and the rule a lane must obey.** Owner ruling **R1** (2026-08-01,
executed as WI-397, `docs/log.md` §"2026-08-01 — WI-397: a work branch never mints a
work-item id"):

> Minting a work-item id is a **serial trunk-side act only**. A new work item takes
> `max(existing id) + 1`, a lane can only see its own tree, and the arithmetic does the rest
> — on 2026-08-01 two lanes independently minted `WI-392`, and three rows lived only on the
> unmerged `wi-391` branch while trunk's max sat *below* them... An id a branch cannot create
> cannot collide.

Enforced by `integrate._minted_id_refusal`: at the merge slot, a finished branch whose
`docs/work/` delta from `merge-base(trunk, branch)` to tip **ADDS** a spec file carrying an id
outside its claimed set is refused, naming the foreign ids, the paths, the claimed set and the
rule. Adds-only, spec-filenames-only, `--no-renames` load-bearing. The authoritative counter
is `docs/id-watermark` (generated by `trace.py --bump-ids`, never hand-edited; a mark only
ever RISES, and lowering one is refused by the integrity pass).

**Watermark at HEAD `85fb3742`** — so the next mints are the numbers below **if nothing else
mints first**; the executing session must re-read the file, never trust this:

```
basis: B=5 CMP=9 EXT=5 IF=173 LLR=205 OI=67 PB=4 REL=3 SN=40 SR=182 TC=201 WI=534
```

→ next: **OI-68, WI-535, SR-183, LLR-206, TC-202, IF-174**.

### 1.3 WI-521 — extend it, or sit beside it?

**Read in full.** `WI-521` is `active` under
`docs/work/active/wi521-decomposition-debt-owner/`, `buildtier = "strong"`,
`safety_class = "ordinary"`, `priority = 2`, `sr_refs = []`, `needs = []`,
`specref = "docs/plans/2026-08-25-remap-alignment.md"`. It is
**`tests/test_module_size_ratchet.py`'s named debt owner**, and it says of itself:

> **THIS ROW IS A STANDING DEBT OWNER, NOT A ONE-SITTING TASK.** Do not claim it expecting to
> finish it. It is claimable for one scoped slice at a time, and it is closed only when the
> debt below is paid or re-homed — and if it is ever closed, **the ratchet pointer must move
> in the same commit**, which is the rule it inherited.

It owns three things: (1) the four wide modules (`agent_loop`, `check_trajectory`,
`agent_common`, `bootstrap`), corroborated from the requirements side by two independent
derivations; (2) M-06's four test monoliths (slice 2 split `test_integrate.py` by node-id set
equality; `test_trace.py` 2,099, `test_trajectory_arch.py` 1,993, `test_agent_loop.py` 1,640
remain); (3) **the sensor gap** — and its §3 is the load-bearing paragraph for this decision:

> `tests/test_module_size_ratchet.py` censuses `SCRIPTS` only, so **no armed sensor watches
> the test tree** — which is why three of the four monoliths grew 5–36% between the
> 2026-08-19 review and the `WI-483` close with nothing saying so.
>
> **Do not just extend the census.** That file's own docstring banks an unruled owner
> question — whether the line-count axis survives at all, given the owner's `OI-16`
> correction... Extending a disputed axis to a second tree doubles whatever is wrong with it.
> **The honest sequence is to raise the axis question with the measurement this row can now
> supply, and extend only what survives the answer.**

Slice 2's close restates it: *"the sensor gap stays CARRIED — extending a disputed line-count
axis to a second tree still doubles whatever is wrong with it."*

**RECOMMENDATION: sit BESIDE WI-521, with edges, and do not extend it.** Four reasons, in
order of weight.

1. **WI-521 has already declared this work out of its own scope, twice, in writing.** Its §3
   instruction is *raise the axis question*, not *build the sensor*. A row that says "the
   honest sequence is to raise the question and extend only what survives" is telling the
   next session to file the question elsewhere. Folding the build into it would consume its
   own stated instruction.
2. **The row is a STANDING debt owner and must not close.** If `check_complexity.py` were
   filed as a WI-521 slice, its completion would still leave WI-521 open (correctly), so the
   program would have no closable row of its own — and the sensor's arrival is exactly the
   event that should be closable and reviewable on its own evidence.
3. **The retirement is a different act from the build, with a different blast radius.**
   Retiring `test_module_size_ratchet.py` touches `docs/stack.ini` `[generated]`,
   `tests/test_generated_freshness_wiring.py::OTHERWISE_ENFORCED`, a shipped module's
   docstring, and WI-521's own pointer. That is the phase-2 row's job and it is a *this-repo*
   act; the build is a *kit* act.
4. **The dependency runs the other way and is real.** WI-521 needs the new sensor's census as
   a prioritiser ("which of the baselined monoliths is actually moving"); the sensor does not
   need WI-521. An edge expresses that; a merge hides it.

**The `needs` edges, stated exactly.**

- `WI-<sensor>` (phase 1): `needs = ["WI-<ruling>"]` — HARD, **only if phase 0 is filed as a
  row**. Phase 0 is an OI brief, not a WI, so in the normal case `needs = []` and the row is
  simply not filed until OI-68 is ruled.
- `WI-<arm>` (phase 2): `needs = ["WI-<sensor>"]` — HARD; plus `"~WI-521"` — SOFT. The soft
  edge is honest and load-bearing in exactly one direction: **if the ruling retires the line
  ratchet, WI-521's pointer moves in the same commit as the retirement**, so the two rows must
  be ordered but WI-521 must never block. A hard edge on a standing debt owner would deadlock
  the phase forever — `IF-054`: "A hard edge is satisfied only by an integrated `done`
  predecessor."
- `WI-<ship>` (phase 3): `needs = ["WI-<arm>"]` — HARD.
- **WI-521 itself gains NO new `needs` edge.** Instead the phase-2 row edits WI-521's
  `## Context` §3 to record what the ruling answered — the same in-place amendment WI-521
  already uses for its slice records.

### 1.4 Spine — does a shipped check need SR/LLR/TC rows? Yes. Here is the exact pattern.

PROCESS.md §2 fixes the id scheme (`SN-###` → `SR-###` via `SN-Refs` → `LLR-###` via
`SR-Refs` (+ Module/CodeSymbol, Detail/Rationale) → `TC-###` via `Verifies`; "Stable,
zero-padded, never reused"). §3's first three bullets are the authoring law: *one fact, one
home*; *decompose, don't paraphrase*; *registries are the machine source of truth*. The
enforcement audit's first row makes the consequence mechanical: "Everything traces
`SN→SR→LLR→TC`; 0 orphans before a gate | Harness | `trace.py --strict`".

**`check_smoke_budget.py` is NOT the model to copy.** It lives in this repo's own
`scripts/` (`scripts/check_smoke_budget.py`), not in `project-trajectory/scripts/`. It is
meta-repo harness, off the traced product (CLAUDE.md: "The traced 'product' is
`project-trajectory/scripts` + `tests/`"), and it carries **no SR/LLR/TC row** — grep over
`docs/requirements/*.toml` and `docs/test/*.toml` for `smoke_budget` returns only OI-52 prose.
`check_complexity.py` is a kit script and takes the full chain.

**`check_dupes_census.py` IS the model to copy** — same shape, same posture, same tier. Its
three rows, verbatim (elided where the cell is long):

```toml
# docs/requirements/system-requirements.toml
[requirement.SR-182]
title = "Duplicated function bodies in the kit's own scripts are measured against a stamped baseline, never gated"
sn_refs = ["SN-007"]
boundary_refs = ["B-05"]
hat_refs = ["CONSISTENCY"]
requirement = """The delivered harness shall report the kit's own duplicated-function-body count against a stamped baseline at a warn-only severity, never gating a bar on it."""
rationale = """Realizes SN-007 (the kit holds itself to its own standard): the consolidation doctrine states the goal in prose, and a number that moves is what proves it is not just prose. ... One row because the standing measurement and its never-gating posture are one contract: a version of this check that gated would be a different requirement, not a stricter reading of this one."""
acceptance_criteria = """A fresh run reports the current duplicated-function-body group/copy/line counts over the kit's own script tree; when compared against a stamped baseline (the current carrier: `docs/stack.ini` `[dupes-census]`) any count above baseline is reported as a finding naming the delta, any count below baseline is reported as an invitation to re-stamp downward, and an unstamped repo (no baseline yet) reports the bare reading; the check exits 0 in every one of those cases, including under `--strict` — a gating change here is a new requirement, not a tightened acceptance of this one."""
priority = "S"
verification = "Test"
status = "Approved"
phase = 5
aspect = "process"
```

```toml
# docs/requirements/low-level-requirements.toml
[design.LLR-195]
sr_refs = ["SR-182"]
title = "Standing duplicated-function-body census, warn-first forever"
module = "project-trajectory/scripts/check_dupes_census.py"
code_symbol = "measure/main"
detail = """measure() walks project-trajectory/scripts/**/*.py (excluding __pycache__), hashes each function's AST-dumped body (docstring stripped, bodies under 4 lines excluded) and groups identical hashes ... main() reads the stamped baseline from docs/stack.ini [dupes-census] (groups/copies/lines) via configparser and prints OK/WARN accordingly; a missing baseline is reported as a bare reading, never a finding. --strict is accepted (for the [step:] convention's uniform command shape) but never changes the exit code ... Wired as [step:dupes-census] (layer=product, from-stage=DevStg-Impl) in docs/stack.ini."""
rationale = """The always-0 exit is the part that could silently regress toward gating the count it measures, so it is the one behavior this row states explicitly rather than leaving to the implementation's discretion: the parent realizes a measurement, never a floor..."""
test_refs = "(see TC-190)"
status = "Approved"
component = "CMP-007"
phase = 5
```

```toml
# docs/test/test-cases.toml
[test.TC-190]
verifies = ["SR-182", "LLR-195"]
level = "Integration"
method = """Synthetic project-trajectory/scripts/ fixtures under tmp_path, run through check_dupes_census.py as a subprocess: no baseline stamped reports the bare reading and exits 0; a reading unchanged from a stamped baseline reports OK; a reading worse than baseline (new duplicate function added) prints a WARN naming the regression and exits 0 under both no-flag and --strict — the never-gates-even-under---strict pin; a reading better than baseline (duplicate removed) asks for a downward re-stamp and still exits 0; an absent project-trajectory/scripts/ directory is vacuously OK."""
tier = "Smoke"
expected = "Satisfies the acceptance folded into LLR-195 (parent SR-182)"
automated = "Yes"
evidence = "tests/test_check_dupes_census.py"
status = "Approved"
phase = 5
```

**`check_dupes_census.py` has NO `IF-` row.** Grepping `check_dupes_census` over
`docs/requirements/interfaces.toml` returns nothing. Under the post-OI-67 model an IF row is
one owner + one direction + one kind, and its definition must live in a `Contract IF-###:`
body in the owner's header — with the gate armed (WI-533), *"a row whose owner declares it but
states no `Contract IF-###:` body is a `check_trajectory --strict` finding"*. So an IF row is
**optional** for a check script and its absence is the status quo for the closest sibling.
This plan drafts one anyway (`drafts/registry-rows.md`) and marks it explicitly optional, with
the argument each way.

**The registry schemas.** The live registries carry **no header comment** — the schema lives
in the templates' `-000` rows. `project-trajectory/registries/system-requirements.template.toml`
says it outright:

> THE `-000` ROW BELOW IS THE SCHEMA. There is no header line to declare a column, so this
> example row is the only place the vocabulary is written down: it sets EVERY key the tier
> has, with the guidance for each as its value.

Binding rules pulled from those `-000` rows and used by the drafts:

- SR `requirement` is **one testable shall-statement on an EARS pattern**, condition IN FRONT:
  *Ubiquitous* `The <system> shall <response>`; *Event-driven* `When <trigger>, the <system>
  shall <response>`; *State-driven* `While <state>, ...`; *Unwanted* `If <trigger>, then ...`;
  *Optional feature* `Where <feature is included>, ...`. Any other opener ("Before…",
  "During…") warns (`trace_text.ears_advisories`). Exactly one `shall`
  (`trace_text.form_findings`, gating under `--strict`).
- **`rationale` is never provenance** — "no work-item id, ruling, sitting, review-round or
  open-item reference, decision id, edit verb or date stamp; the history belongs in the log
  (process.md §3)". Warn-first via `trace_text.provenance_advisories`; **gating** under
  `--strict` for a WI id or process-doc citation in an SR/LLR/TC normative cell.
- **A requirement cell never names a concrete artifact** (re-tier v2 R2, extended to SN
  2026-08-18): a `*.py` token in an SR `requirement` cell warns unless the `rationale`
  carries a `recorded waiver:` reason. **The concrete filename belongs at LLR
  (`module`/`code_symbol`) or inside `acceptance_criteria` as the current carrier** — exactly
  what SR-182 does (``the current carrier: `docs/stack.ini` `[dupes-census]` ``).
- LLR `detail` is decomposition detail, "NOT a paraphrase of the SR (reference it by id).
  Name the real (or planned) module + symbol." **No `shall` in an LLR** (gating).
- TC has **no reason cell**; `expected` cites the verified requirement's acceptance by id and
  does not paraphrase it. `level ∈ Unit|Integration|…`, `tier ∈ Smoke|Full|…`,
  `automated = "Yes"`, `evidence` names the test module or `module::test` ids.
- `aspect` is a CLOSED vocabulary on SR: `process | trajectory | unattended-loop |
  connectivity | perf | portability`. `process` is the value SR-182 uses.
- `phase` is a bare integer. The live product rows sit at `phase = 5`.
- `component` on LLR: `CMP-006` W1 Registry & conformance · **`CMP-007` W2 Gatekeeper** ·
  `CMP-008` W3 Autonomy · `CMP-009` W4 Human & adopter surfaces. A check script is `CMP-007`.
- `hat_refs` roster names available: `SECURITY, FIRST-RUN-ADOPTER, UNATTENDED-OPS,
  CROSS-PLATFORM, MAINTAINER, TEST-ENGINEER, UX-DESIGNER, UX-ENGINEER, SAFETY, LEGAL,
  DATA-PROTECTION, ACCESSIBILITY, PERFORMANCE, CONSISTENCY, INTEGRITY-RECOVERABILITY,
  PRODUCT-FITNESS`.

**Candidate parents.** `SN-007` — "The people maintaining this kit hold it to its own
standard: it stays traceable and tested through every change" — is SR-182's parent and the
natural one. `SN-012` — "the process is **right-sized**… small changes stay cheap, and heavy
layers are opt-in", acceptance "Opt-in layers … cost a repo that doesn't use them nothing" —
is the parent for the *report-only-and-opt-in* half. The draft uses
`sn_refs = ["SN-007", "SN-012"]`; SR-006 shows the two-parent shape is house-legal.
**Uncertain, flagged rather than guessed** — see §5.2.

### 1.5 Gate wiring — `docs/stack.ini`, `stack.ini.template`, `check.py`

**How a step becomes real.** `check.py::extra_steps` (line 362) reads every
`[step:<name>]` section of `docs/stack.ini`. Its docstring is the contract:

```
    [step:capability-integrity]
    command    = {py} scripts/check_capabilities.py {src}  # required
    from-stage = DevStg-Impl                      # optional, default DevStg-Impl
    layer      = product                          # optional, default product
    lane       = tests+coverage                   # optional (see below)
```

`{py}/{src}/{tests}/{coverage}/{tier}` expand; the required-import set is auto-derived from the
argv; a name that shadows a `BUILTIN_STEP_NAMES` member exits loudly; a section with no
`command =` exits loudly. **`complexity` is free** — the builtin set is `format, lint,
tests+coverage, derived-stage, registry-integrity, traceability, vocabulary, need-form,
privacy, doc-navigability, perf-budgets, design-flows, trajectory, backlink-coverage,
trajectory-map, status-map, open-items, component-view, cli-reference, …`.

**`docs/process.toml` `[checks]` is NOT the opt-in for this.** That section carries the kit's
own layer dials (`trajectory_check`, `interfaces_check`, `components_check`, `okf_export`,
`live_status`, `subagent_gate`, `backlink_coverage_min`) — kit layers, not project steps. A
project-declared step's opt-in is its **presence** in `stack.ini`. **Nothing needs to change
in `process.toml`.**

**The live `[step:dupes-census]` + its baseline section, verbatim** — this is the pattern the
new step copies, including the comment style (a `#` prose block above the keys carrying the
WI/ruling, the re-measure command, and every re-stamp with its reason):

```ini
[dupes-census]
# WI-507 (OI-58 (a)+(b), ruled 2026-08-22): re-arms the WI-448 function-body
# duplication census as a standing MEASUREMENT, not a gate — narrower than the
# [step:dupes] machinery D-7 tore down above, and it does not revisit that
# ruling: F5 duplication stays unbounded, check_dupes_census.py never fails
# a gate even under --strict, and this baseline is DOWNWARD-ONLY, hand
# re-stamped with a reason (the module-size ratchet's own convention) — never
# a mechanized rewrite. Re-measure with:
#   python project-trajectory/scripts/check_dupes_census.py --root .
# ... [each re-stamp recorded with its reason and its log fragment] ...
# ZERO IS A READING, NOT A FLOOR. The census stays armed and stays warn-first
# (D-7): a future duplicate re-appears as a WARN against 0/0/0 ...
groups = 0
copies = 0
lines = 0
# fig: cmd="python project-trajectory/scripts/check_dupes_census.py --root ." rev="77d67c38 and this commit's tree (WI-448 slice 4): 6/6/76 -> 0/0/0"...

[step:dupes-census]
# The standing WI-448 census (see [dupes-census] above): reports the current
# reading against the stamped baseline, WARN-ONLY forever — never exits
# nonzero, not even under --strict (D-7 stays in force; only the measurement
# is re-armed). Product layer, DevStg-Impl, beside the other quality sensors.
command = {py} project-trajectory/scripts/check_dupes_census.py --root .
from-stage = DevStg-Impl
layer = product
```

and `[step:module-coverage]`, the tier-sensitive one with a serialising `lane`:

```ini
[step:module-coverage]
# Per-module coverage floors (WI-279; repo-review 2026-07-22 M-4). The global
# [coverage] threshold above is one aggregate number, so a heavily-tested
# generator can subsidize thin coverage in a security/process boundary
# (agent_session.py, subagent_gate.py, plan_runner.py) while the headline still
# passes. check_coverage.py compares the per-file percents in coverage.json ...
# Raise a floor (in docs/coverage-floors) only alongside the focused tests that earn it.
command = {py} project-trajectory/scripts/check_coverage.py --tier {tier} --skip-tiers smoke
from-stage = DevStg-Impl
layer = product
# Serialize AFTER tests+coverage (it reads that step's coverage.json): this
# repo's CI runs `check.py --jobs 0` (parallel), where an un-laned step would
# race the producer, find no JSON yet, and SKIP — silently NOT enforcing the
# floors. `lane` puts it in the tests+coverage lane so it runs once the JSON
# exists (a no-op at --jobs 1, which is already ordered).
lane = tests+coverage
```

**Note the path shape.** In `docs/stack.ini` the command is
`{py} project-trajectory/scripts/<x>.py` (the kit-path invariant, OI-59). In
`project-trajectory/stack.ini.template` it is `{py} scripts/<x>.py` — the adopter's own copy.
Values legitimately diverge; structure must not.

**`stack.ini.template` has NO `[step:dupes-census]`** — grep for `dupes` returns nothing. Its
project-step block is a **commented catalogue** under `# --- Project-specific gate steps ---`:

```ini
# Prose reference rot — ... Warn-first by design, so TRIAGE BEFORE YOU WIRE IT: run it
# once, fix or classify what it finds, and only then add --strict here. ...
# [step:doc-refs]
# command = {py} scripts/check_doc_refs.py --root . --strict
#
# Per-module coverage floors (the kit-owned comparator, stdlib-only): ...
# [step:module-coverage]
# command = {py} scripts/check_coverage.py --tier {tier} --skip-tiers smoke
# lane = tests+coverage
```

**Why the comment marks matter, mechanically.** `tests/test_dogfood_sync.py::
test_stack_ini_declares_every_template_section` runs `stack_section_drift`, whose
`_sections()` is `re.finditer(r"(?m)^\[([^\]]+)\]", text)` — anchored at column 0. **A
commented `# [step:x]` is not a section**, so a commented template step imposes no obligation
on `docs/stack.ini`; an UNcommented one would force `docs/stack.ini` to declare
`[step:complexity]` too. That is the lever: **ship the template step commented** (the house
convention for an opt-in gate an adopter must triage before wiring), and this repo's live
step is then a free choice rather than a forced one.

### 1.6 `PROCESS_OPTIONS.md` — the layer format, and what the byte guard says

**The Applies-when index** is the table at lines 14–52: "Scan this table once, then read only
the sections whose trigger matches your scope… Rows are in document order; each maps to the
`##` section of the same name below." Three columns:
`Layer | Applies when — skip the section if not | What it adds`. The two nearest rows in tone:

```
| Enforcement audit | your process outgrew one reader's head and you want to know which rules actually bind | `docs/enforcement-audit.md` |
| Signed measurements | you are about to write a measured number into a doc, log or registry row | a commit-the-evidence-first rule + a historical-observation marker |
```

**"Signed measurements" (line 1402) is the short-layer pattern**: an `## <Name>` heading, an
opening `**Applies when** …` sentence naming the trigger and the cost in one clause, two or
three paragraphs of *why*, a numbered rule list, and a closing paragraph naming what is
**deliberately not built** and its enforcer tier. Its closing move is the one to imitate:

> The *truth* of a figure is not mechanizable — no check distinguishes a live measurement
> from a recollection — so that enforcer stays **Reviewer**, in the enforcement audit above
> with the honestly-unbacked rules. The *presence* of provenance on a declared figure now is:
> `check_figures.py` (opt-in `[step:figures]`, warn-first, `--strict` gates) … its honest
> claim is "declared figures carry provenance", never "all figures do". Re-derivation … is
> **deliberately not built** … Never imply it is covered.

**Byte budget.** `.claude/skills/byte-budget-guard/SKILL.md` puts `PROCESS_OPTIONS.md` in the
**Watched** table, not the Capped one:

> **Watched** — growth is allowed but must be flagged with a byte delta + reason in the
> session/WI note. NOTHING PINS THESE: both had drifted un-flagged before WI-498 slice 5
> measured them, so re-stamp on the way past.
>
> | `project-trajectory/PROCESS.md` | 87,836 | 2026-08-29 | **+54** FLAGGED: … |
> | `project-trajectory/PROCESS_OPTIONS.md` | 179,209 | 2026-08-29 | **+449** FLAGGED: … |

and the delta-reporting rule, verbatim from its Procedure §3 and Report shape:

> **Re-measure and compute the delta.** Every capped file must be at or under its cap. Flag
> any watched file's growth with the delta and a reason, then **re-stamp** the changed row —
> source plus every tracked skill copy, in the same commit. A re-stamp **replaces** the
> row's baseline, date and reason; never nest the superseded one in a parenthetical —
> history lives in `docs/log.md`.
>
> ```
> Byte deltas, one line per touched file:
> <file> <before> -> <after> (headroom left under its cap, or delta + reason).
> ```
>
> Never report "within budget" without the actual `wc -c` number.

**"every tracked skill copy"** = three files: `project-trajectory/skills/byte-budget-guard/
SKILL.md`, `.claude/skills/byte-budget-guard/SKILL.md`, `.agents/skills/byte-budget-guard/
SKILL.md`. (There is no `.gemini/skills/` dir in this repo.) That skill is itself **capped at
5,000** and stood at 4,795 on 2026-08-29 — **205 bytes of headroom** — and a re-stamp
*replaces* a row rather than appending, so two re-stamped rows cost roughly their own delta.
Measure it; do not assume.

**Measured now, at HEAD:** `wc -c project-trajectory/PROCESS.md project-trajectory/PROCESS_OPTIONS.md
project-trajectory/AGENTS.template.md CLAUDE.md` → `87836 / 179209 / 9980 / 7827`. The two
watched baselines in the guard are current.

### 1.7 `PROCESS.md` §3 — where the structure-commit bullet goes

`PROCESS.md` §3 runs lines 105–~200. The **0→A→B bullet is at line 180**, and the bullet
immediately after it is **Thin orchestrators** (line ~192). The new bullet goes **between
them**: after 0→A→B, before Thin orchestrators — inside the "Consolidate, don't duplicate"
cluster CLAUDE.md already points at, so it is not a new home for an old fact. Verbatim
neighbours:

```
- **Modularity/dedup**: shared logic in exactly one place; pure cores separated
  from I/O/GUI shells; small functions; one-page-readable architecture.
- **Consolidate, don't duplicate — the 0→A→B rule.** Edit-conservatively (agent
  guide, "Working agreement") is scoped to the task in front of you: smallest
  diff, within that one change. Across the codebase the goal is the opposite —
  prefer the change that minimizes **total** behavior. ... (vendored at
  `skills/antidote/`, a per-fix companion to this repo-scale doctrine).
- **Thin orchestrators**: an entry point / top-level routine should *compose, not
  compute* — a short, ordered sequence of well-named calls ...
```

**PROCESS.md is 87,836 bytes and is WATCHED, not capped.** The draft bullet is ~470 bytes; the
phase-3 WI must flag the delta with a reason and re-stamp the guard's PROCESS.md row (source
+ 2 copies).

### 1.8 Skills — the schema, the house shape, and the real fan-out

**Schema** — `project-trajectory/skills/README.md` declares `IF-035`:

> Contract IF-035: one skill is one directory holding a `SKILL.md` whose leading `---`
> frontmatter block carries the agent-facing `name` (lowercase-hyphen, equal to the directory
> name) and `description`, plus this kit's applicability axes `scope`, `stacks`, `domains`,
> `phases` and `tags`. A list value is written `[a, b, c]` and a scalar is bare; only that
> shape is parsed, so a skill needing richer YAML is out of scope for both readers. The set
> is walked at scaffold time to select which skills a repo receives, and scanned again to
> regenerate the flat `INDEX.csv`, one row per skill.

Closed vocabularies: `stacks ∈ {python, node, go, rust, powershell, any}`,
`domains ∈ {web, game, hardware, data, any}`, `phases ∈ {setup, dev, gate, release}`; `tags`
freeform lowercase-hyphen. `scope ∈ {kit, this-repo}` — `kit` ships and materializes
downstream, `this-repo` "kept in the kit as a reference/dogfood source, **not** materialized
downstream".

**House shape** — `structured-output-contract/SKILL.md` (19 lines) and
`design-token-steward/SKILL.md` (18 lines) are the template: frontmatter, then
`**When to use.**` with an italic `*Why:*` clause, then `**Procedure.**` as 3–4 numbered
imperatives whose LAST item is `**Done when:**`, then an optional `**Knowledge:**` pointer.
Shipped skills run 19–27 lines, not 100–200.

**The fan-out, measured — and the RESYNC pack overstates it.**
`project-trajectory/skills/` holds **30** skills; `.claude/skills/` and `.agents/skills/`
hold **8** each (`antidote, byte-budget-guard, downstream-resync, gate-advance,
registry-hygiene, render-dashboard-critique, session-protocol, spine-authoring`); there is
**no `.gemini/skills/`**. Why only 8: this repo hand-curates the set it dogfoods.
`bootstrap.py::sync_agent_skills` iterates the **destination** dirs
(`for name_dir in sorted(p for p in agent_skills.iterdir() if p.is_dir())`) and its own
docstring says it "touches ONLY the `<agent>/skills/<name>/` subtree of a per-agent dir that
ALREADY exists (a subset dir stays a subset; creating a per-agent dir is `--agents`' job), and
only the skills that dir already carries". `gen_skills_index.check_agent_sync` matches: "Only
skills that EXIST in a per-agent dir are compared — a subset dir is legitimate … so a source
skill MISSING from a per-agent dir is NOT reported."

**Consequence:** `--sync` will NOT create `.claude/skills/deep-module-design/`. It must be
created deliberately, exactly as WI-507 did for `antidote` —
`docs/log.d/2026-08-22-wi507-consolidation-doctrine.md`: *"Dogfooded byte-identical into
`.claude/skills/antidote/` and `.agents/skills/antidote/` (`gen_skills_index.py
--check-agents`: OK, 16 copies match source)."* `RESYNC_PACK.md`'s antidote entry gets this
right for the downstream reader in its last sentence (*"If your repo hand-curates … decide
whether to add it explicitly — it is not force-selected by scope alone once a repo has
departed from full auto-selection"*) but its first sentence overstates it (*"`bootstrap.py
--sync` … picks up the new `scope: kit`, `domains: [any]` skill automatically"*).
**Recorded as a finding, not fixed here** (§5.7).

**Fan-out steps for a new kit skill, in order:**

1. Author `project-trajectory/skills/deep-module-design/SKILL.md`.
2. `python project-trajectory/scripts/gen_skills_index.py` — regenerates
   `project-trajectory/skills/INDEX.csv` (30 → 31 rows). Freshness-gated: the `[generated]`
   row is `project-trajectory/skills/INDEX.csv = skillsindex`, step name `skills-index`.
3. **Decide whether this repo dogfoods it.** `deep-module-design` is `domains: [any]`,
   `stacks: [any]`, `scope: kit` — the same profile as `antidote`, which this repo DOES
   dogfood, and its subject (interface depth) is directly this repo's own problem. **Recommend
   yes.** Then create `.claude/skills/deep-module-design/SKILL.md` and
   `.agents/skills/deep-module-design/SKILL.md` as byte-identical copies — the WI-507 act.
4. `python project-trajectory/scripts/bootstrap.py --dest . --sync` — keeps them identical
   thereafter.
5. `python project-trajectory/scripts/gen_skills_index.py --check-agents` — the S7 drift gate;
   must print `OK - N per-agent skill copy(ies) match source.` (N goes 16 → 18 if this repo
   dogfoods it).
6. Scaffold-verify, per WI-507's own record:
   `python project-trajectory/scripts/bootstrap.py --dest <scratchpad>/dmd-scaffold --agents claude --domain any --stack python`
   then `diff` the scaffold's `.claude/skills/deep-module-design/SKILL.md` against source.

**Byte note:** a `kit`-scope skill materializes into up to three per-agent dirs for every
adopter that selects it, so the body stays **< 4 KB** (Anthropic's own guidance is "under 500
lines" and *"the context window is a public good"*). The draft is ~2.6 KB.

### 1.9 `RESYNC_PACK.md` — the entry format

Entries are `### <Title> [since <sha>]` under §3, each opening with the anchoring note, then
`**What changed.**` and `**What you must do.**`. `[since <sha>]` is *"the kit commit at which
the change landed"*, and range selection is mechanical against `docs/kit-version`: *"your
stamp's SHA to your target SHA is a range, and an entry applies when its `since` SHA is **in**
that range."* The convention for an entry that cannot know its own commit is stated inside the
entry:

> *(Anchored at the preceding commit: an entry cannot know its own SHA.)*

The nearest exemplar is `### The consolidation doctrine lands, plus a standing duplication
census [since 1806f5c8]`, quoted in full in `drafts/RESYNC_PACK-entry.md`. Note its
`**What you must do.**` shape: merge, then *either adopt verbatim or skip with a stated
reason*, then **stamp your own baseline** — "run `check_dupes_census.py --root .` once with no
baseline present, and write the printed reading into `[dupes-census]`". The complexity entry
copies that shape exactly, because an adopter's baseline is their tree's, never the kit's.

**One finding this program must not repeat.** `check_dupes_census.py` is **not in
`bootstrap.MAPPING`**. An AST read of the MAPPING literal gives the kit scripts it omits:
`bootstrap.py, check_dupes_census.py, gen_prompt_catalog.py, gen_skills_index.py`. So the
RESYNC entry telling adopters to "adopt `[step:dupes-census]` + `check_dupes_census.py`
verbatim" describes a file **a fresh scaffold never receives** and a re-syncing adopter must
copy by hand. **`check_complexity.py` MUST get a MAPPING row in phase 3** or its
`stack.ini.template` step and its RESYNC entry name a file that is not there.

### 1.10 Tests, tiers, ledger, MAPPING

**Smoke tier.** `tests/conftest.py` `SLOW_MODULES` (line 60) is a frozenset of module stems;
`smoke_tier_for` returns `"slow"` for a member and `"smoke"` otherwise, and
`pytest_collection_modifyitems` marks every item ("Total by construction — one test maps to
exactly one tier, so nothing lands outside both"). **Tiering is opt-out: a new in-process test
module is in the commit bar by default.** The set's stated class is
subprocess/scaffold-heavy: hooks, `test_bootstrap`, the integrator family (`test_integrate`
+ the three WI-521 slice-2 splits), `test_dispatch`, `test_old_kit_resync`,
`test_dual_plan_round`.

Membership is ratcheted: `docs/stack.ini` `[smoke-budget]` `max-tests` (deterministic,
always-on, `tests/test_smoke_budget.py`) plus `seconds` (wall, enforced by
`scripts/check_smoke_budget.py --mode enforce`). Both are "growth SENSORS with headroom, not
exact freezes (new in-process unit tests SHOULD accrue — the WI-122 intent). Re-stamp
together, reason in the log."

**Retiring `test_module_size_ratchet.py` — everything that references it.** Live
(non-archive, non-log-record) references:

| Path | What it is | Action on retirement |
|---|---|---|
| `docs/stack.ini` line 878 | `[generated]` row: `tests/test_module_size_ratchet.py = linecounts` | **DELETE the row** |
| `tests/test_generated_freshness_wiring.py` lines 57–66 | `OTHERWISE_ENFORCED = {"linecounts": "tests/test_module_size_ratchet.py"}` — "The kinds whose enforcer is NOT a check.py step, each named with its reason" | **DELETE the entry**, same commit, or this test reds |
| `tests/test_import_layers.py` line 14 | docstring: "It is the topology sibling of `test_module_size_ratchet.py`" | re-point at the new sensor |
| `tests/test_agent_loop.py` line 419 | comment citing a recorded `ruff format` fact | re-word |
| `project-trajectory/scripts/traj_context.py` line 16 | **a SHIPPED module's docstring** naming a this-repo test as the reason the view is its own module | re-point or generalise |
| `docs/work/active/wi521-…md` §3 + slice records | the debt owner's own text | amend in place, in the retirement commit |
| `docs/work/active/wi508-…md` line 358 | program text | amend or leave (a landed record) |
| `docs/registry-machinery-reference.md` line 626 | "Both are **growth sensors with headroom**" — about the **smoke-budget pair**, not this ratchet | **verify before touching; probably leave** |
| `docs/concurrency-restructure.md` 540, `docs/spine-restructure-2026-08-08.md` 663 | dated historical records | leave |

**`docs/registry-machinery-reference.md` lists NO checks** (grep for `check_dupes_census` /
`check_figures` / `[step:` returns nothing). Its scope note says why: the four spine tiers,
the stage derivation, and the harness's stage→tier→coverage path. **No update needed.**

**`docs/cli-reference.md` is GENERATED** — "**Generated. Do not edit the block below by
hand.** It is derived from each module's own `argparse` tree by `gen_arch_map.py --cli-doc`
and freshness-gated by `check.py`'s `cli-reference` step, so it cannot drift from the code the
way a hand-written paraphrase can." A new shipped script with an `argparse` tree lands there
**automatically**; the WI regenerates and commits it and edits nothing by hand.

**Dependency ledger — NO ROW NEEDED, and here is the proof.** `docs/dependencies.md` is
scanned by `tests/test_dependency_ledger.py`, which *"scans every import in
`project-trajectory/scripts/` against this table and **fails on any Python import not declared
here**"*. Tiers: `coordinator | shipped | system | kit`. `check_complexity.py` imports `ast`,
`argparse`, `pathlib`, `sys` (+ `configparser` if it reads `stack.ini`) — all stdlib — so it
declares nothing. **This is load-bearing, not incidental:** the ledger's `shipped` tier says a
shipped-check dependency "forces every adopter to install it, so the bar is highest (owner
ruling required, expected rare, ideally never — stdlib remains *preferred* for shipped
checks)". `tests/test_complexity_ratchet.py`'s
`pytestmark = pytest.mark.skipif(… find_spec("ruff") is None …)` is the living demonstration
of the cost of the alternative.

**`bootstrap.MAPPING` and the sibling test — the brief's premise is half-right, so read this
carefully.** The test is
`tests/test_bootstrap.py::test_every_sibling_imported_module_is_shipped_by_mapping` (line
1328). It parses the `MAPPING` **literal** by AST ("not the file text: a whole-file regex also
matches script names in docstrings and comments, which would silently mark an unmapped module
as mapped") and asserts that **a SHIPPED script's sibling imports are themselves mapped**. Its
skip line is decisive:

```python
if owner == "bootstrap" or owner not in mapped:
    continue  # the scaffolder itself is not shipped; nor are kit-only tools
```

So **an unmapped kit script does not fail that test** — `check_dupes_census.py` is the live
proof, and this plan corrects the brief's premise on that point. What *does* force a MAPPING
row is the **ship decision**: phase 3 puts `{py} scripts/check_complexity.py` in
`stack.ini.template` and an entry in `RESYNC_PACK.md`, and both are false unless the file
reaches a scaffold. Two further tests bear on it once the row exists:
`tests/test_dogfood_sync.py::test_scaffold_mapping_covered_or_declared` (every MAPPING
destination is present, kit-served in place, or declared in `SCAFFOLD_OMISSIONS`) and
`::test_scaffold_omissions_list_is_current`. The row shape is a `(src, dst)` tuple with a `#`
comment above it stating **why it ships** — the shipped exemplars:

```python
    ("scripts/check_figures.py", "scripts/check_figures.py"),
    ("scripts/check_coverage.py", "scripts/check_coverage.py"),
    # The need-form check (SN-033, WI-454): warn-first lint keeping SN `need`
    # cells in stakeholder language. Shipped because the registry it scans is
    # the adopter's own, and check.py's step table names it at every bar.
    ("scripts/check_need_form.py", "scripts/check_need_form.py"),
```

`bootstrap.py`'s own module docstring carries a prose list of shipped scripts (line 69:
`scripts/check_stubs.py, check_coverage.py, check_doc_refs.py, check_figures.py, …`) —
**update it in the same edit**, and `project-trajectory/README.md`'s kit-contents table, per
the session-protocol's standing instruction: *"update `test_bootstrap.py` file lists and
`README.md` kit-contents / `bootstrap.py` `MAPPING` when the scaffold surface changes."*

### 1.11 Docs, status, and the commit bar

**`docs/enforcement-audit.md`** is "evidence, not a rule source — the rules live in
`AGENTS.template.md` and `PROCESS.md`; this table only records where each one bites". Classes
are **Harness › Test › Reviewer › Prose**, strongest wins. The row this program changes,
verbatim (line 64):

```
| Right-size; every line is a liability | Reviewer | Prose — over-engineering flagged either way (no hard check) |
```

Draft replacement in `drafts/enforcement-audit-rows.md`. The audit's own second-half rule
governs the honesty text:

> a new or widened one has its false-positive rate **measured** against the live corpus, with
> negative cases pinning the known hazards, before any claim is made about what it found — a
> rate that is reported rather than measured is a guess wearing a number. And a detector is a
> **worklist, not a definition of done**: its vocabulary is always narrower than the rule it
> stands for, so a cleanup that stops when the checker goes quiet has proved only that the
> checker is quiet.

**`docs/status.md` is forward-only** and declares `IF-163`: "Only what must happen NEXT
belongs here — what already happened lives in log.md — so a work-item id recorded closed must
not appear in the hand-authored prose, and a claim naming one there is refused; inside the
generated block that rule stands down, because the generated frontier legitimately names
queued ids." The generated block is fenced by `<!-- BEGIN GENERATED STATUS -->` /
`<!-- END GENERATED STATUS -->` and refreshed by `gen_trajectory.py --status`.
**Hand-authored status prose about this program names only the open frontier**; closed rows
leave at close. The enforcer is `check_trajectory`'s done-id rule (warn / ERROR `--strict`).

**The commit bar** (session-protocol §3), all three before EACH commit:

```
python -m pytest -q -n auto -m smoke
python scripts/check_smoke_budget.py --mode enforce
python project-trajectory/scripts/check_docs.py --root . --stale
```

"it means results AND seconds, not results alone (OI-52 ruling (a), 2026-08-23)". ≤ 60 s wall
(`docs/stack.ini` `[smoke-budget]`; 27.27 / 28.16 / 27.86 s over three warm runs at the WI-496
re-tier). The **full** unfiltered suite (`python -m pytest -q -n auto`, ~6 min here; a WI-484
run recorded 17m23s on a busy box) before claiming a slice/phase done, at close, and after a
broad script change. The **gate bar** is `check.py --gate <gate>` (`--jobs 0` to parallelise)
and belongs to phase close and CI, not to each mid-phase slice.

**Log fragments.** A session writes `docs/log.d/<date>-<slug>.md` opening
`## YYYY-MM-DD — <title>`, then `**Summary.**`, then a `Deferred open items:` declaration
(`gen_open_items.fragment_declarations` warns if a declared id does not name a pending row;
`none` is a legal declaration — "Deferred open items: none — the split needed no ruling and
files no new question").

### 1.12 `AGENTS.template.md` — P4 confirmed

**Measured now: 9,980 / 10,000 bytes — 20 bytes of headroom.** Its own footer states the rule:

> **Customizing:** add a rule only after you've had to repeat it, and **pay for it by
> tightening another** — this file has a hard byte budget (keep ≥2k headroom under Gemini's
> ~12k AGENTS.md cap for project facts). Delete rules you don't enforce — unbacked rules are
> noise.

The bullet in question, verbatim (lines 159–162):

```
- **Right-size the solution.** The simplest thing that satisfies the
  requirement; no speculative flexibility — **every line is a liability**, so
  before adding, ask what you can delete. Judge "simple" against the whole
  design; flag over-engineering either way. (`SHORTCUT:` convention: §3.)
```

**P4's recommendation is CONFIRMED: do not add a rule.** The existing line is already
specific and already carries the deletion prompt, and the ETH *Evaluating AGENTS.md* result
is that specific instructions are followed while repository overviews are not. The optional
byte-paid sharpening (making the *reuse* failure explicit — the one agent-specific failure
mode MSR 2026 measured, and the one the current line does not name) is drafted with real
before/after counts in `drafts/AGENTS-swap.md`. It is **optional and owner-gated**; the
program does not need it.

---

## 2. The four phases

Every phase lands independently. Ids below are placeholders — `WI-<n>` — because **a work
branch never mints a WI id (R1)**: the mint is a serial trunk-side act via `intake.py`, and
the watermark at HEAD says the next is `WI-535`. Re-read `docs/id-watermark` at filing time.

### Phase 0 — the ruling

**Deliverable:** one open-item brief, `[open_item.OI-68]`, `status = "pending"`, put to the
owner with three questions and their evidence. Full text: `OI-BRIEF-draft.md`.

**This phase files no WI.** An OI row's `wi_refs` is optional (26 of 59 rows carry it) and this
brief is filed before any row exists — `wi_refs` is filled at the ruling with the phase-1/2/3
rows. If the executing session prefers a row to carry the authoring, file it as a
`workstream = "process"`, `buildtier = "quick"` row; nothing in the machinery requires it.

**Files touched**

- `docs/requirements/open-items.toml` — one new `[open_item.OI-68]` table appended after
  `[open_item.OI-67]`.
- `docs/open-items.html` — **regenerated, never hand-edited**:
  `python project-trajectory/scripts/gen_open_items.py --root .`
- `docs/status.md` — one forward-only bullet naming the pending brief (hand-authored region),
  plus the generated block refreshed by `gen_trajectory.py --status`.
- `docs/log.d/<date>-complexity-sensor-brief.md` — the fragment, declaring
  `Deferred open items: OI-68`.
- `PROJECT_STATE.html`, `docs/stage` — regenerated if the frontier changed.

**Verification**

```
python project-trajectory/scripts/gen_open_items.py --root .
python project-trajectory/scripts/gen_open_items.py --root . --check     # must exit 0
python project-trajectory/scripts/trace.py --root . --strict-integrity
python -m pytest -q -n auto -m smoke
python scripts/check_smoke_budget.py --mode enforce
python project-trajectory/scripts/check_docs.py --root . --stale
```

**Rollback:** delete the `[open_item.OI-68]` table, re-run `gen_open_items.py`, revert the
status bullet. Nothing else has moved. **Reversible in one commit** (the OI number is spent,
which is intended — the watermark only rises).

**Owner eyes:** the whole phase IS an owner action.

---

### Phase 1 — the sensor, report-only

**WI draft** — frontmatter:

```
+++
id = "WI-<n1>"
title = "check_complexity.py: a stdlib cognitive-complexity + SLOC census with a central TSV baseline, report mode only"
specref = "docs/plans/<date>-complexity-sensor-plan.md"
workstream = "process"
sr_refs = ["SR-<new>"]
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++
```

`needs` is empty because phase 0 is an OI brief, not a WI — the row is simply not filed until
OI-68 is ruled. (If phase 0 is filed as a row, `needs = ["WI-<n0>"]`, hard.)
`buildtier = "strong"`: the two correctness traps below are the discriminator — this is a
"figure it out" spec, not a "cite the pattern" one.

**Body** (`## Context`, the WI-521 shape — `## Deliverable` stays absent until close):

> ## Context
>
> **What this row builds.** `project-trajectory/scripts/check_complexity.py`: a stdlib-`ast`
> census of every function in the declared source surface, reporting **cognitive complexity**
> (SonarSource rules) and **SLOC** per function, plus a per-module **public-symbol count**
> that is REPORTED and never gated. The baseline is a central TSV at
> `docs/complexity-baseline`. Modes: `--report` (print the census, always exit 0),
> `--restamp` (write the current census), and the default compare mode.
>
> **Why cognitive and not cyclomatic, in one measurement.** `tests/test_complexity_ratchet.py`
> already runs ruff `C901` per function. On this tree cyclomatic is largely explained by size
> while cognitive is much less so, and a population of functions is deeply NESTED rather than
> widely BRANCHED — invisible to a C901 census by construction. The count and the worked
> examples go in the log at the close, measured by THIS script, not borrowed from a research
> pass. (The prototype's reading at HEAD `7fc42a5a`, to be re-derived: of 179 script functions
> over cognitive 15, only 43 appear in the 47-entry C901 baseline — 136 are invisible to ruff;
> 41 of the 199 over-15 functions have textbook McCabe ≤ 10, e.g. `traj_graph.py::_seg_hits_rect`
> at cognitive 19 / cyclomatic 7. The largest function in the tree, `check.py::steps`, is 314
> SLOC at cognitive 14 and correctly silent.)
>
> **Why stdlib and not a linter.** A shipped check that needs a linter forces every adopter to
> install it (`docs/dependencies.md`, the `shipped` tier's own bar). The C901 ratchet is the
> demonstration of the cost: it `skipif`s away without ruff, and its baseline is coupled to
> ruff's counting rules, so a ruff upgrade that started counting comprehensions would red the
> whole baseline. This script pins its own counting rules in its docstring, which is the
> property that makes its baseline a property of the code rather than of a tool version.
>
> **The two correctness traps, each owed a test.** (a) `elif` is parsed as a nested `If` in
> `orelse`: a naive recursion both double-counts and over-nests, inflating every `elif` ladder
> in the tree — flatten it, and treat the else-branch as +1 flat with no nesting increment.
> (b) A `BoolOp` scores **runs of like operators**, not operators: `a and b and c` is +1,
> `a and b or c` is +2. A third, kit-specific: a nested `def` takes a nesting increment and no
> base increment, so **decomposing outward is rewarded and nesting inward is not** — say so in
> the docstring, because the C901 ratchet has a recorded trap in the other direction.
>
> **The baseline file.** `docs/complexity-baseline`, TSV, one row per over-threshold function,
> sorted, LF-only. TSV rather than TOML/JSON for one reason: minimum merge-conflict surface
> when two concurrent sessions each re-stamp.
> Header: `# path<TAB>function<TAB>cognitive<TAB>sloc<TAB>reason`.
>
> **The seeded baseline is a DEBT STATEMENT, NOT AN APPROVAL** — the same stance
> `test_module_size_ratchet.py` took and defended, and the file's own header says so.
>
> **Posture in THIS phase: report-only.** No `[step:]` row, no gate, no arming. The census
> lands in the log as the measurement the phase-0 ruling was answered with, re-derived by the
> shipped script.
>
> **NOT in scope.** Arming (phase 2). Retiring any existing sensor (phase 2). Shipping
> (phase 3). The relative-churn sensor — separate, and unfiled.

**Files touched**

- **new** `project-trajectory/scripts/check_complexity.py` (~200 lines, stdlib only)
- **new** `tests/test_check_complexity.py` (~150 lines; the `tests/test_check_dupes_census.py`
  model — synthetic fixtures under `tmp_path`, driven as a subprocess via `conftest.run_py`)
- **new** `docs/complexity-baseline` (seeded from the script's own first run; the prototype
  reads 179 rows for scripts, 199 with `tests/` — `prototype/baseline-seed.tsv` is the dry run)
- `docs/requirements/system-requirements.toml` — `[requirement.SR-<new>]`
- `docs/requirements/low-level-requirements.toml` — `[design.LLR-<new>]`
- `docs/test/test-cases.toml` — `[test.TC-<new>]`
- `docs/requirements/interfaces.toml` — `[interface.IF-<new>]` **if** the optional IF row is
  taken (`drafts/registry-rows.md`); if taken, the script's `Contracts:` header must carry a
  `Contract IF-###:` body **in the same commit** — the gate is armed (WI-533)
- `docs/id-watermark` — via `python project-trajectory/scripts/trace.py --bump-ids`, never by
  hand
- `docs/cli-reference.md` — **regenerated**, not edited
- `docs/stack.ini` `[smoke-budget]` — re-stamp `max-tests` if the new module joins the tier
- `tests/conftest.py` `SLOW_MODULES` — **decide deliberately** (risk below)
- `PROJECT_STATE.html`, `docs/stage`, `docs/status.md`, `docs/log.d/<date>-<slug>.md`

**The tiering risk, stated so it is not discovered at the bar.** The `check_dupes_census` test
model drives the script as a **subprocess**, and subprocess-heavy modules are what
`SLOW_MODULES` exists to drop from the commit bar. But `tests/test_check_dupes_census.py` is
**not** in `SLOW_MODULES` and its TC tier is `Smoke` — so the house precedent is that a small
subprocess-fixture module stays in the bar. **Measure before deciding**: run
`python -m pytest -q -n auto -m smoke` before and after and compare wall seconds against the
60 s budget. If the module costs more than about a second, split it — in-process unit tests of
the cognitive-complexity function (the two traps) in the smoke tier, the subprocess CLI drives
in a `SLOW_MODULES` sibling. Do not silently push the bar past its budget; the OI-52 ruling
exists because a day of commits were once described as green against a bar that had failed.

**Verification**

```
python project-trajectory/scripts/check_complexity.py --root . --report     # the census
python project-trajectory/scripts/check_complexity.py --root .             # exit 0 vs the seeded baseline
python -m pytest -q tests/test_check_complexity.py
python -m pytest -q -n auto -m smoke
python scripts/check_smoke_budget.py --mode enforce
python project-trajectory/scripts/check_docs.py --root . --stale
python project-trajectory/scripts/trace.py --root . --strict
python project-trajectory/scripts/check_trajectory.py --root . --strict
python -m pytest -q tests/test_dependency_ledger.py                        # proves the stdlib claim
python -m pytest -q -n auto                                                # THE FULL SUITE — a new script is a broad change
```

Paste the real output. Never report a green you did not produce.

**Rollback:** the script, its test and the baseline are new files — `git rm` them. The
registry rows are additive; deleting them and lowering the watermark is **refused by
`trace.py`'s integrity pass** (a mark only rises), so the ids are spent even on a rollback.
That is the intended cost of a mint, not a defect. **Reversible except for the id numbers.**

---

### Phase 2 — arm it here, and retire whichever sensor the ruling retired

**WI draft** — frontmatter:

```
+++
id = "WI-<n2>"
title = "Arm the complexity sensor in this repo, and execute the OI-68 ruling on the line ratchet"
specref = "docs/plans/<date>-complexity-sensor-plan.md#phase-2"
workstream = "process"
sr_refs = ["SR-<new>"]
needs = ["WI-<n1>", "~WI-521"]
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++
```

The `~WI-521` **soft** edge is deliberate and load-bearing: WI-521 is a STANDING debt owner
that will not close, and `IF-054` says a hard edge is satisfied only by an integrated `done`
predecessor — a hard edge here would deadlock the phase permanently. The soft edge records the
ordering (this row amends WI-521's §3 and, if the ruling retires the ratchet, moves its
pointer) without blocking, and it renders dashed on the roadmap, which is the honest picture.

**Body** (`## Context`):

> ## Context
>
> **What this row does, in three acts, in one direction.**
>
> 1. **Arm.** `[step:complexity]` in `docs/stack.ini` (`layer = product`,
>    `from-stage = DevStg-Impl`), running the compare mode: exact equality both directions,
>    nonzero on either. Growth FAILS ("simplify — a bump is a reviewed baseline edit whose
>    reason lands in the log"); improvement FAILS ("re-stamp downward or delete, in the same
>    commit"). `--restamp` makes the re-stamp one command so the **diff** is what gets
>    reviewed. **No inline suppression pragma, ever** — the escape hatch is the central file,
>    because the documented failure mode elsewhere is suppression migration, which
>    self-replicates as new code copies the suppression. The failure message names the three
>    legitimate escapes: *decompose outward* (a new module or a sibling function, not a nested
>    `def`), *replace branches with a data table*, *define the error out of existence so the
>    branch disappears*.
> 2. **Scope.** Extend the census to `tests/` **iff** OI-68 Q2 ruled it in. That is the whole
>    of WI-521's §3 sensor gap, answered on the right axis instead of by extending a disputed
>    one.
> 3. **Retire, iff OI-68 Q1 ruled it.** `tests/test_module_size_ratchet.py` is DELETED, and
>    with it — in the same commit — `docs/stack.ini`'s `[generated]` row
>    `tests/test_module_size_ratchet.py = linecounts` and
>    `tests/test_generated_freshness_wiring.py`'s `OTHERWISE_ENFORCED["linecounts"]` entry. The
>    docstring references in `tests/test_import_layers.py`, `tests/test_agent_loop.py` and
>    **`project-trajectory/scripts/traj_context.py`** (a SHIPPED module citing a this-repo
>    test) are re-pointed at the new sensor. WI-521's `## Context` §3 records what the ruling
>    answered and, if the ratchet is gone, its debt-owner pointer moves in the same commit —
>    the rule WI-521 itself states.
>
> **If Q1 ruled KEEP, this row still lands** — the arming and the scope decision stand alone,
> and item 3 becomes a one-paragraph amendment to WI-521's §3 recording that the line ratchet
> keeps a distinct job (or is demoted to advisory, if that is what was ruled).
>
> **The re-stamp is a review artifact, not a formality.** Every baseline row carries a
> `reason`. Re-stamping to clear a finding is the one thing the ratchet convention forbids
> ("never to clear a finding").

**Files touched**

- `docs/stack.ini` — new `[step:complexity]` section (`drafts/stack-ini-step.md`);
  `[generated]` `linecounts` row deleted iff retiring
- `project-trajectory/scripts/check_complexity.py` — the compare/exit-code arm, if phase 1
  shipped report-only
- `docs/complexity-baseline` — re-seeded if the scope widened to `tests/`
- `tests/test_module_size_ratchet.py` — **DELETED** iff retiring
- `tests/test_generated_freshness_wiring.py` — `OTHERWISE_ENFORCED` entry deleted iff retiring
- `tests/test_import_layers.py`, `tests/test_agent_loop.py`,
  `project-trajectory/scripts/traj_context.py` — docstring re-points
- `docs/work/active/wi521-decomposition-debt-owner/WI-521-decomposition-debt-owner.md` — §3
  amended; pointer moved iff retiring
- `docs/requirements/open-items.toml` — OI-68 flipped to `ruled` with `ruled_date` +
  `ruling_ref` (if not already done at the ruling sitting)
- `docs/enforcement-audit.md` — the two rows (`drafts/enforcement-audit-rows.md`)
- `docs/open-items.html`, `PROJECT_STATE.html`, `docs/stage`, `docs/status.md`,
  `docs/log.d/<date>-<slug>.md`

**Verification**

```
python project-trajectory/scripts/check.py --run-step complexity --root .
python project-trajectory/scripts/check_complexity.py --root .          # exact-equality green
python -m pytest -q tests/test_generated_freshness_wiring.py            # the linecounts deletion's tripwire
python -m pytest -q -n auto -m smoke
python scripts/check_smoke_budget.py --mode enforce
python project-trajectory/scripts/check_docs.py --root . --stale
python project-trajectory/scripts/check_doc_refs.py --root . --strict   # catches a dangling test_module_size_ratchet.py
python -m pytest -q -n auto                                             # THE FULL SUITE
python project-trajectory/scripts/check.py --gate DevStg-Impl --jobs 0  # the gate bar, at phase close
```

`check_doc_refs --strict` is the one that catches a retired path still named in a doc; run it
before claiming the retirement clean.

**Rollback:** arming is one `stack.ini` section — delete it. **The retirement is NOT cheaply
reversible in effect**: `git revert` restores the file, but every baseline entry it carried has
meanwhile diverged from the tree, so a revert lands a red ratchet needing a hand re-stamp with
reasons nobody has. Treat the retirement as a one-way door and take it only on an explicit
ruling.

---

### Phase 3 — ship it downstream

**WI draft** — frontmatter:

```
+++
id = "WI-<n3>"
title = "Ship the complexity sensor: MAPPING row, a commented template step, the opt-in layer, the deep-module-design skill and the structural-move commit rule"
specref = "docs/plans/<date>-complexity-sensor-plan.md#phase-3"
workstream = "process"
sr_refs = ["SR-<new>"]
needs = ["WI-<n2>"]
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++
```

**Body** (`## Context`):

> ## Context
>
> **The scaffold surface changes, so the standing lesson applies: verify by BOOTSTRAPPING A
> SCAFFOLD, not by this repo's suite.** That lesson is written in blood — `MAPPING` once
> omitted `schedule.py` and every fresh scaffold died on its first claim while this repo
> stayed green.
>
> **Five deliverables, each independently reviewable.**
>
> 1. **`bootstrap.MAPPING` gains `("scripts/check_complexity.py",
>    "scripts/check_complexity.py")`**, with a `#` comment above it stating why it ships — the
>    house convention. `bootstrap.py`'s own docstring script list and
>    `project-trajectory/README.md`'s kit-contents table are updated in the same edit.
>    **This is not optional**: `check_dupes_census.py` is the counterexample — it has a
>    `RESYNC_PACK.md` entry telling adopters to adopt it and is in NO `MAPPING` row, so a
>    fresh scaffold never receives it.
> 2. **`project-trajectory/stack.ini.template` gains a COMMENTED `[step:complexity]`**, in the
>    project-specific-steps block beside the commented `[step:doc-refs]` and
>    `[step:module-coverage]`, running `--report`. Commented is a structural choice, not a
>    stylistic one: `tests/test_dogfood_sync.py::test_stack_ini_declares_every_template_section`
>    scans `^\[…\]` at column 0, so an UNcommented template section would force
>    `docs/stack.ini` to declare `[step:complexity]` too. Values may diverge (report there,
>    enforce here); structure must not.
> 3. **`PROCESS_OPTIONS.md` gains the "Complexity ratchet" layer** plus its Applies-when index
>    row, in document order.
> 4. **`PROCESS.md` §3 gains "A structural move is its own commit"**, placed after the 0→A→B
>    bullet and before Thin orchestrators.
> 5. **`project-trajectory/skills/deep-module-design/SKILL.md`** (`scope: kit`,
>    `domains: [any]`, < 4 KB), `INDEX.csv` regenerated, dogfooded byte-identical into
>    `.claude/skills/` and `.agents/skills/`, `--check-agents` green.
>
> Plus the `RESYNC_PACK.md` §3 entry covering the whole range.
>
> **Both watched docs move. Run `byte-budget-guard` before and after and re-stamp both rows —
> source plus the two tracked copies of that skill — in the same commit.**

**Files touched**

- `project-trajectory/scripts/bootstrap.py` — MAPPING row + docstring list
- `project-trajectory/README.md` — kit-contents row
- `project-trajectory/stack.ini.template` — commented `[step:complexity]`
- `project-trajectory/PROCESS.md` — §3 bullet (**watched**, ~+470 B)
- `project-trajectory/PROCESS_OPTIONS.md` — new layer + index row (**watched**, ~+3.0 KB)
- **new** `project-trajectory/skills/deep-module-design/SKILL.md`
- `project-trajectory/skills/INDEX.csv` — **regenerated**
- **new** `.claude/skills/deep-module-design/SKILL.md`,
  `.agents/skills/deep-module-design/SKILL.md` — byte-identical copies
- `project-trajectory/RESYNC_PACK.md` — one `### … [since <sha>]` entry
- `project-trajectory/skills/byte-budget-guard/SKILL.md` + its 2 tracked copies — two
  re-stamped rows (**capped at 5,000; 4,795 on 2026-08-29 — 205 B headroom; measure**)
- `docs/enforcement-audit.md` — if not already done in phase 2
- `PROJECT_STATE.html`, `docs/stage`, `docs/status.md`, `docs/log.d/<date>-<slug>.md`

**Verification**

```
wc -c project-trajectory/PROCESS.md project-trajectory/PROCESS_OPTIONS.md \
      project-trajectory/AGENTS.template.md CLAUDE.md \
      project-trajectory/skills/byte-budget-guard/SKILL.md          # BEFORE and AFTER

python project-trajectory/scripts/gen_skills_index.py
python project-trajectory/scripts/bootstrap.py --dest . --sync
python project-trajectory/scripts/gen_skills_index.py --check-agents  # OK - N copies match

# THE SCAFFOLD BOOTSTRAP — the only thing that verifies a scaffold-surface change
python project-trajectory/scripts/bootstrap.py --dest <scratchpad>/cx-scaffold \
       --agents claude --domain any --stack python
diff project-trajectory/skills/deep-module-design/SKILL.md \
     <scratchpad>/cx-scaffold/.claude/skills/deep-module-design/SKILL.md    # empty
test -f <scratchpad>/cx-scaffold/scripts/check_complexity.py                 # MUST exist
cd <scratchpad>/cx-scaffold && python scripts/check_complexity.py --root . --report
cd <scratchpad>/cx-scaffold && python scripts/check.py --gate DevStg-Impl     # scaffold still green

python -m pytest -q tests/test_dogfood_sync.py
python -m pytest -q tests/test_bootstrap.py -k "byte_caps or size_budget or mapping"
python -m pytest -q -n auto -m smoke
python scripts/check_smoke_budget.py --mode enforce
python project-trajectory/scripts/check_docs.py --root . --stale
python -m pytest -q -n auto                                                  # THE FULL SUITE
python project-trajectory/scripts/check.py --gate DevStg-Impl --jobs 0
```

**Rollback:** every item is additive and independently revertible. The MAPPING row is the one
with downstream reach — an adopter who re-syncs after it lands gets the file, and reverting it
later would take a file back out of their tree. **Treat the MAPPING row as the point of no
return for the ship decision.**

---

## 3. Dependency graph

```
                 ┌─────────────────────────────────────────┐
                 │ PHASE 0 — OI-68 ruling (owner)          │
                 │ Q1 replace the line ratchet?            │
                 │ Q2 cover tests/?                        │
                 │ Q3 armed or report-only here?           │
                 └──────────────────┬──────────────────────┘
                                    │ HARD — decides scope and posture
                                    ▼
                 ┌─────────────────────────────────────────┐
                 │ PHASE 1 — WI-<n1>  the sensor           │
                 │ check_complexity.py + tests + baseline  │
                 │ SR/LLR/TC (+ optional IF)               │
                 │ report-only; no [step:]; no retirement  │
                 └──────────────────┬──────────────────────┘
                                    │ HARD
                                    ▼
   WI-521 ······SOFT (~)······▶ ┌─────────────────────────────────────────┐
   (standing debt owner;        │ PHASE 2 — WI-<n2>  arm + retire         │
    never closes, so a          │ [step:complexity] in docs/stack.ini     │
    HARD edge would             │ tests/ scope iff Q2                     │
    deadlock — IF-054)          │ DELETE test_module_size_ratchet.py      │
                                │   + [generated] linecounts row          │
                                │   + OTHERWISE_ENFORCED entry   iff Q1   │
                                │ amend WI-521 §3; move its pointer       │
                                └──────────────────┬──────────────────────┘
                                                   │ HARD
                                                   ▼
                                ┌─────────────────────────────────────────┐
                                │ PHASE 3 — WI-<n3>  ship                 │
                                │ bootstrap.MAPPING row                   │
                                │ commented [step:complexity] in template │
                                │ PROCESS_OPTIONS layer (+ index row)     │
                                │ PROCESS.md §3 bullet                    │
                                │ deep-module-design skill + fan-out      │
                                │ RESYNC_PACK entry                       │
                                │ VERIFY BY BOOTSTRAPPING A SCAFFOLD      │
                                └─────────────────────────────────────────┘

Independent of all four (do not sequence into them):
  · AGENTS.template.md byte-paid swap — owner-gated, optional, P4 says DON'T
  · relative-churn sensor — unfiled; report-only forever if ever built (D-7 posture)
```

**Two items in phase 3 have no dependency on phases 0–2** and could be split out if the ruling
stalls: the `deep-module-design` skill and the PROCESS.md §3 bullet. Both are zero-machinery
and neither mentions `check_complexity.py`. **Recommendation: keep them in phase 3 anyway** —
they are the prose half of the same argument, and the byte-budget re-stamp is then one act
rather than three. Split them only if the ruling is genuinely blocked.

---

## 4. What the owner must put eyes on

Ordered by irreversibility. Nothing below may be done on an agent's own judgement.

### 4.1 Rulings — no code moves until these are answered

1. **OI-68 Q1 — does `check_complexity.py` REPLACE `tests/test_module_size_ratchet.py`?** The
   banked question, banked twice (log 2026-08-20; the ratchet's own docstring). It authorises
   a **deletion**, and the ratchet's own file says: "until it is ruled, this file stays armed,
   because an unruled axis is not a reason to stop sensing growth."
2. **OI-68 Q2 — does the sensor cover `tests/` as well as `project-trajectory/scripts/`?**
   WI-521's §3 explicitly refuses to extend the disputed axis to a second tree and asks for
   this to be ruled first.
3. **OI-68 Q3 — armed here, or report-only here too?** This changes THIS repo's own gate
   posture and every future session's bar.
3b. **OI-68 Q4 — the two Sonar-spec conventions and the threshold.** `match` = one increment
   (spec-explicit); comprehension `if` conditions take the nesting increment (199 vs 166 seeded
   rows — a one-function change either way); threshold 15 carries 43/47 C901 entries, 14 would
   carry 45/47. The prototype's choices are recommended; whichever is ruled gets pinned in the
   docstring and a test so the number is defensible against any third-party tool.

### 4.2 Deletions and retirements

4. **Deleting `tests/test_module_size_ratchet.py`** — 2,055 lines, ~91% of it reviewed
   commentary recording every baseline decision this repo has made on that axis. That record
   leaves with the file unless the retirement commit says where it went.
5. **Deleting `docs/stack.ini`'s `[generated]` `linecounts` row** and
   `tests/test_generated_freshness_wiring.py`'s `OTHERWISE_ENFORCED["linecounts"]` entry —
   both must go in the SAME commit as the file, or the suite reds.
6. **Moving WI-521's debt-owner pointer** — WI-521's own standing rule, and it is the third
   hand-off of that pointer; the row's own history is a record of that pointer going stale.

### 4.3 Byte-capped and byte-watched edits

7. **`PROCESS.md`** — watched, 87,836 B, ~+470 B. Flag the delta with a reason; re-stamp the
   guard's row (source + 2 tracked copies).
8. **`PROCESS_OPTIONS.md`** — watched, 179,209 B, ~+3.0 KB. Same.
9. **`skills/byte-budget-guard/SKILL.md`** — **capped at 5,000**, 4,795 B on 2026-08-29,
   **205 B of headroom**, and this program re-stamps TWO of its rows. `wc -c` before and
   after; if it would breach, the row prose gives, not the cap.
10. **`AGENTS.template.md`** — **capped at 10,000**, at **9,980**, 20 B headroom. **The
    recommendation is to change nothing.** If the owner wants the reuse sharpening, exact text
    and counts are in `drafts/AGENTS-swap.md` (variant B: 9,980 → **9,984**, +4; variant C:
    → **9,973**, −7 at a content cost). Never land it on this plan's arithmetic — run
    `byte-budget-guard` and `pytest tests/test_bootstrap.py -k "byte_caps or size_budget"`.

### 4.4 Downstream-migrating

11. **The `bootstrap.MAPPING` row** — the moment it lands, every re-syncing adopter receives
    `check_complexity.py`. Reversing it later takes a file back out of adopters' trees.
12. **The `RESYNC_PACK.md` entry** — instructions a downstream agent will execute
    unsupervised. Its "stamp your own baseline" step is what stops an adopter inheriting the
    kit's numbers.
13. **The commented `[step:complexity]` in `stack.ini.template`** — the wording an adopter
    triages before wiring. Getting "warn-first, triage before you wire it" wrong here is how a
    check earns the ignore that D-7 documents.
14. **The opt-in layer's applies-when** (draft: *"a repo past roughly 5,000 lines of code whose
    agents author most of the diff"*) — the one sentence an adopter reads to decide whether the
    layer is theirs.
15. **The `deep-module-design` skill** — `scope: kit`, `domains: [any]`, so it materializes
    into up to three per-agent dirs for every adopter that selects it, and loads into their
    context. Its content is judgement, not mechanism.

### 4.5 Standing risks worth an explicit owner acknowledgement

16. **The seeded baseline is a DEBT STATEMENT, NOT AN APPROVAL.** With a Sonar-default
    threshold the seed is large (179 rows; 199 with `tests/`). Every row is active debt, and the file
    must say so in its own header, as `test_module_size_ratchet.py` does.
17. **No controlled study shows that enforcing a complexity threshold reduces defects.** The
    strongest enforcement evidence available is this repo's own 48-day natural experiment:
    the capped doc grew +2.6%, the two watched docs +91% and +1,101%. This program rests on
    mechanism reasoning plus that one in-repo result — stated plainly rather than dressed up.
18. **A new check owes a measured false-positive rate before any claim is made about what it
    found** (`docs/enforcement-audit.md`'s own rule; Google's <10% bar). A metric the kit has
    never run on anyone else's codebase has no false-positive evidence — which is the whole
    justification for shipping `--report` only, and it is the D-7 lesson applied forward
    rather than re-litigated.

---

## 5. Where the repo's convention is unclear — check these, do not guess

1. **Whether `check_complexity.py` should carry an `IF-` row at all.** The closest sibling
   (`check_dupes_census.py`) has none. Under the armed WI-533 gate, declaring one obliges a
   `Contract IF-###:` body in the module header in the same commit. **Check:**
   `docs/requirements/interfaces.toml` header block (lines 1–146) and
   `docs/enforcement-audit.md`'s `contract_body_findings` row.
2. **Which SN parents the new SR.** SR-182 takes `SN-007` alone; the report-only/opt-in half
   argues for `SN-012` as well. **Check:** `.claude/skills/spine-authoring/SKILL.md` and
   `PROCESS.md` §3's eight-characteristics table.
3. **Whether the new test module belongs in `SLOW_MODULES`.** `tests/test_check_dupes_census.py`
   is a subprocess-driving module that is NOT in the set and whose TC tier is `Smoke`; the
   conftest comment says the set is for "subprocess/scaffold-heavy" modules. The precedent
   cuts both ways. **Check:** `tests/conftest.py` lines 60–110, and measure the delta.
4. **Whether `docs/complexity-baseline` needs a `[generated]` row.** The line ratchet's
   baseline lives INSIDE its test file and is declared `linecounts` with `OTHERWISE_ENFORCED`
   naming the test as its enforcer; the dupes-census baseline lives in `docs/stack.ini` and
   has no `[generated]` row at all. A standalone TSV matches neither precedent exactly.
   **Check:** `docs/stack.ini` `[generated]` and `tests/test_generated_freshness_wiring.py`'s
   `WIRED` / `OTHERWISE_ENFORCED` split (its comment: "A row lands here only when the artifact
   genuinely has no mechanical regenerator to `--check` against — never because wiring one was
   inconvenient", which is exactly the ratchet argument: re-deriving a baseline "would blindly
   approve whatever the tree currently measures").
5. **Whether `docs/complexity-baseline` needs a `docs/declared-absences` entry** so
   `check_doc_refs --strict` does not flag it in a fresh scaffold that has not stamped one.
   **Check:** `docs/declared-absences` and `check_doc_refs.py --declared-absences`.
6. **Whether the RESYNC entry's `[since <sha>]` anchors at phase 3's commit or the program's
   first.** Existing entries anchor at *the preceding commit* because "an entry cannot know
   its own SHA", and a three-commit program has three candidate anchors. **Check:** how the
   multi-commit OI-67 program did it — `RESYNC_PACK.md` entries `[since 088a6cca]` and
   `[since 816090cd]` are one program in two entries, which is probably the answer: one entry
   per landing that changes an adopter's surface.
7. **`RESYNC_PACK.md`'s antidote entry overstates `--sync`.** It says `--sync` "picks up the
   new skill automatically"; `bootstrap.sync_agent_skills` iterates DESTINATION dirs and
   creates nothing. **Check:** `project-trajectory/scripts/bootstrap.py::sync_agent_skills`
   (line 626) against `RESYNC_PACK.md` ~line 3346. **Recorded as a finding; not fixed by this
   program** (CLAUDE.md: surface a design smell as a separate finding, not an inline fix).
8. **`project-trajectory/scripts/traj_context.py` — a SHIPPED module whose docstring cites
   `tests/test_module_size_ratchet.py`, a this-repo test an adopter will never have.** Adjacent
   to CLAUDE.md's rule that a token the kit mandates into an adopter's cell must mean something
   in their repo. It is a docstring, not a mandated cell, so it is at worst a smell — but it
   becomes a dangling reference the moment the ratchet retires. **Check:**
   `project-trajectory/scripts/traj_context.py` lines 14–19.
9. **Whether phase 2's arming needs an SR of its own.** SR-182's own rationale says a gating
   version of a warn-only check "would be a different requirement, not a stricter reading of
   this one". If the new SR is written warn-only, arming it here **needs a second SR** — or the
   SR must be written from the start as *report by default, gate where the repo opts in*, which
   is what `drafts/registry-rows.md` does and flags. **Check:** SR-182's rationale cell, and
   whether the adjudicator accepts a single row spanning both postures.
