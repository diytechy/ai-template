+++
id = "WI-429"
title = "D-9 gives three of the four Status=Founded discharge tests an existing home (SN = derive_gate's uncovered rung, SR = derive_gate's G2 decomposition test, TC = the Evidence file-existence check, sufficient under R2) and leaves the LLR's OPEN, because an LLR has no children in this schema. D-9 records the natural discharge as CodeSymbol/Module RESOLVING - which would give CodeSymbol its first real job (F-3: required today, never resolved) - and the owner said proceed on 2026-08-11. Build that computation against TODAY'S data, in this order and no other: (1) CENSUS all 149 live LLR rows through spine_carrier, classifying every failure (renamed - moved module - deleted - a method/attribute/local rather than a module-level name - a joined multi-value cell - empty-but-required - legitimately not a Python name, e.g. a CSS custom property or a shell script). (2) REPAIR deterministically the way the Evidence-selector repair was done: build a name->module map, repoint where there is EXACTLY ONE home, prove a rename with git log -S where ambiguous, and LEAVE + REPORT anything with no defensible answer rather than guessing. Module/CodeSymbol are TRACED cells (check_trajectory.SPINE_TRACED_CELLS), so a repoint opens no re-attest window - re-verify that before editing and STOP if it has become RATIFIED. (3) WIRE the rule into the checker that already joins these exact cells, reusing gen_arch_map's symbol inventory rather than growing a second symbol parser (the D-6/F5 hazard), and prove it non-vacuous by planting an LLR naming a nonexistent symbol in a tmp_path scaffold. Decide severity on the argument, not by copying a neighbour: under D-9 this becomes the LLR tier's Founded gate input, so an advisory nothing acts on makes Founded vacuous for one tier. DO NOT implement the ladder, change any Status value, or touch the Draft/Verified/Modified vocabulary - Q11 holds that migration behind the sitting."
workstream = "scripts"
specref = ""
buildtier = "strong"
safety_class = "ordinary"
+++

## Deliverable

**DONE 2026-08-11. The LLR discharge test, taken under the owner's 2026-08-11
"proceed" on D-9's open sub-question; ratification owed with the ladder
migration.** Links below are written for `docs/work/complete/`, where this spec
lands. No `Status` value, and nothing in the `Draft`/`Verified`/`Modified`
vocabulary, is touched here — Q11 still holds that migration.

### Phase 1 — the census (149 live LLR rows)

Read through `spine_carrier.load`, never by hand-parsing TOML. The symbol oracle
is `gen_arch_map.module_bindings` — one new function in the module that already
owns AST symbol extraction, not a second parser.

**The cell has no enforced grammar, and that is the census's first finding.**
`CodeSymbol` cells are `/`-, `+`-, `;`- and `,`-joined lists whose members are
not all module-level names. Measured across the 149 live rows they include
module-level functions and classes (the majority), private helpers
(`_ring_ink`), module constants (`STATUS_FILL`), class methods, and also
*function locals* (`budget_findings`, `tier_legend`), *instance attributes*
(`critique_rounds`), CSS custom properties (`--nhead`, `--tiny`), hook and shell
script names (`pre-commit`, `dev-setup`) and free prose (`every emitter\'s
paint`). F-3\'s "required today, never resolved" is exactly why: nothing ever
held the cell to a shape, so it drifted into a label.

| class | before repair | after repair |
|---|---:|---:|
| every identifier-shaped token binds in a named `.py` module | 109 | **118** |
| anchored (≥1 binds) but ≥1 token does not | 21 | 18 |
| **NO identifier-shaped token binds** — the rows the check reds | **9** | **4** |
| no identifier-shaped token at all (CSS / prose cells) | 4 | 4 |
| no checkable `.py` module (a hook, a shell template, or a `Module` absent from disk) | 6 | 5 |
| empty-but-required | 0 | 0 |

<!-- fig: cmd="python project-trajectory/scripts/check_doc_refs.py --root . --show-untraced" rev=13addbcf -->

`Module` paths absent from disk: **1** (LLR-143, `scripts/drive.py`) → **0**.

**Failure classification of the 31 rows that carried ≥1 non-binding token.** The
underlying rot is two module splits and a long tail of labels that were never
symbols:

| class | rows | the evidence |
|---|---|---|
| **moved module** — the symbol exists, in exactly one *other* module | 13 (LLR-035, 051, 055, 078, 079, 080, 099, 103, 107, 115, 119, 130, 143) | the WI-280 split of `gen_trajectory.py` into `traj_parse`/`traj_views`/`traj_panels`/`traj_render` (`25b9ce6c`, `d6009692`), and the WI-381 `drive.py` → `dispatch.py` rename (`81cac0e1`) |
| **renamed symbol** | 1 (LLR-084) | `critique_staged_findings` appears in **zero** commits under `project-trajectory/scripts/`; `staged_completion_findings`\'s docstring names `critique_ratchet_findings` as its family member, and the row\'s title is "Critique closure ratchet" |
| **deleted symbol** | 4 (LLR-037, 118, 143, 099) | `status_size_warning` is retired in a comment at `agent_loop.py:497` (WI-210); `_resume_or_claim`/`_stranded_claims`/`_default_worker` died with `drive.py`; `mask_local` in `41b228a5`/`5508b478`; `sw_view` survives only as a comment in `traj_views.py` |
| **a local, an attribute or a template placeholder — never a module-level name** | 8 (LLR-005, 011, 015, 058, 059, 077, 082, 112) | `budget_findings`/`module_findings` are locals in `trace.analyze`; `critique_rounds` is `self.critique_rounds` on `RoutingState`; `tier_legend` is a local in `gen_trajectory.build_html` feeding a `$tier_legend` template slot; `safety_class` is a dict key in `intake.py`/`agent_common.py`; `write`, `ready`, `tabindex`, `sw`, `phase` are fragments of a `/`-joined phrase |
| **never existed anywhere** — aspirational labels | 13 tokens (`_nav`, `_descend`, `_breadcrumb`, `_tier_column`, `_svg_node`, `_drill_svg`, `_drill_edges`, `spec_ref_findings`, `build_module_map`, `critique_failure_action`, `VERIFICATION_VALUES`, `critique_staged_findings`, `structural_safety`) | `git log -S<name> -- project-trajectory/scripts/` returns **zero** commits for every one; the only history hits are the registry file itself |
| **legitimately not a Python name** | 15 rows (LLR-011, 019, 020, 021, 032, 103, 104, 107, 108, 110, 111, 112, 113, 117, 122) | CSS custom properties (`--nhead`, `--w-*`), hook/shell script names (`pre-commit`, `pre-push`, `dev-setup`, `onboard`), prose (`every focusable/role=img emit site`) |
| **`;`-joined multi-value cell** | 5 (LLR-080, 110, 112, 113, 117) | LLR-080 alone uses `;` *positionally* — `Module = gen_trajectory.py;gen_arch_map.py`, `CodeSymbol = sw_graph/build_html;build_module_map` — a pairing convention no rule states; the other four use it as a plain sub-list separator |
| **empty-but-required** | 0 | every live row carries a non-empty `CodeSymbol` |

### Phase 2 — the repair

`check_trajectory.spine_cell_class("…/low-level-requirements.toml", "Module")`
and `…("CodeSymbol")` both return `"traced"` (§A5.1, WI-380/WI-388), re-verified
before the first edit — a repoint amends no attested prose and opens no
re-attest window. **14 rows repaired: 13 `Module` repoints and 1 `CodeSymbol`
rename.**

| row | change | why it is determined, not guessed |
|---|---|---|
| LLR-035 | `Module` += `traj_parse.py`, `traj_views.py` | `spine_stats` has exactly one home (`traj_parse`); `arch_icicle`/`dag_svg` exactly one (`traj_views`) |
| LLR-051 | += `gen_trajectory.py` | `build_html` has exactly one home |
| LLR-055 | += `traj_views.py` | `when_view` has exactly one home |
| LLR-078 | += `traj_panels.py` | `know_graph` has exactly one home |
| LLR-079, LLR-130 | += `traj_parse.py` | `_asof` has exactly one home |
| LLR-080 | += `traj_views.py` | `sw_graph` has exactly one home |
| LLR-099 | += `traj_panels.py`, `traj_render.py` | `know_view` → `traj_panels`; `_render_drill` → `traj_render` |
| LLR-103 | += `traj_render.py` | `_ring_ink` and `_ring_style` each have exactly one home |
| LLR-107 | += `traj_render.py`, `traj_views.py` | `_drill_layer_svg` → `traj_render`; `arch_icicle`/`dag_svg` → `traj_views` |
| LLR-115 | += `traj_panels.py` | `_next_work_html` has exactly one home |
| LLR-119 | += `traj_render.py`, `traj_panels.py` | `_drill_block_label`/`_fit_lines` → `traj_render`; `_next_work_title` → `traj_panels` |
| LLR-143 | `drive.py` → `dispatch.py` | `81cac0e1` "split the driver — drive.py becomes dispatch.py"; `docs/declared-absences:92` had already **scheduled this exact repoint** |
| LLR-084 | `CodeSymbol` `critique_staged_findings` → `critique_ratchet_findings` | the only `CodeSymbol` edit; the old name never existed in any commit, and the surviving function matches the row\'s title |

Repointing is **additive** where the row\'s other symbols still live in the
original module: a row keeps naming every module it genuinely spans, and the
check reads the `;` list as a UNION rather than as a positional pairing — the
only reading that is safe when one live row (LLR-080) uses the positional
convention and nothing states it.

**LEFT, with the reason — 22 rows keep ≥1 non-binding token, 4 of them with no
anchor at all.** The four the check reds:

| row | cell | why no repair is defensible |
|---|---|---|
| LLR-015 | `budget_findings` | a correct description of a **local variable** in `trace.analyze`; naming the enclosing function would change what the row claims, and the cell is not wrong so much as out of scope |
| LLR-087 | `_drill_svg/_drill_edges` | neither name has ever existed in any commit; the seam-port code now lives across `traj_render`/`traj_views` under different names, and choosing which would be inventing intent |
| LLR-088 | `_descend/_breadcrumb` | same — never existed anywhere |
| LLR-112 | `emitted querySelectorAll wiring; tabindex + native-link emission` | pure prose; `tabindex` is an HTML attribute that merely *looks* like an identifier — an honest false positive of the shape test, recorded rather than special-cased |

**These four are the true answer, not a defect in the run:** under D-9 they are
LLRs that are **not `Founded`**, and that is what the computation is for. They
are the handback this row owes the owner, and the residue Q11\'s ladder
migration inherits.

### Phase 3 — the check, and why it is the ANCHOR rule

Wired into **`check_doc_refs.py`** as `symbol_findings` — the checker that
already reads `low-level-requirements.toml`\'s `Module`/`CodeSymbol`/`TestRefs`
cells for file existence (`SPINE_CELLS`, WI-394 / ruling R2), already owns a
symbol oracle, and already ships the warn-first/`--strict` idiom. No new script;
the findings file through the same `(dangling, untraced)` split the path and
registry tiers use.

**The rule: a row\'s `CodeSymbol` must carry AT LEAST ONE identifier-shaped token
that binds at module scope in one of the `.py` modules its `Module` cell names.**

Not "every token resolves", and the census is the argument. A per-token rule
reds **31 of 149** live rows, 18 of them for tokens that were never symbol
claims at all — a local, an attribute, a CSS variable, a prose fragment. That is
a check that reds the tree on arrival, enforcing a grammar no ruling ever gave
the cell. The anchor is the same trade **R2** made on the sibling cell: validate
the coarse claim (this row\'s code is real, at a module that is real, under a
name that is really there), rule the fine claim prose — the identical shape as
checking the FILE half of `tests/x.py::node` <!-- path-ok: the R2 example form -->
and ruling the selector prose. And it answers precisely the question D-9 asks of
`Founded`: *do the artifacts this row calls for exist?*

Per-token misses are not discarded. They file as **untraced** — 28 of them
today — counted on every run and listed under `--show-untraced`, which is the
WI-062 discipline: a reason classifies, a suppression list hides, and a count
you can watch is how a later tightening stays possible.

**Severity: DANGLING — a hard error under `--strict`, beside the orphan-class
rules, not beside the paraphrase advisories.** The argument, in order:

1. **D-9 makes it a gate input.** `Founded` is COMPUTED, and the LLR tier\'s
   discharge is this rule. An advisory nothing acts on would make `Founded`
   vacuous for exactly one of four tiers — the asymmetry D-9 spent its whole
   ruling deleting from the ladder.
2. **The sibling rule on the same two cells already gates.** The file-existence
   half of `Module`/`CodeSymbol` is dangling-class under `--strict` today. A
   split severity across one cell-pair would be arbitrary, and would read as a
   judgement about *importance* when the only real difference is *grammar*.
3. **A paraphrase warn is a taste finding; this is an existence finding.** The
   advisory family says a `Detail` reads too much like its parent — a matter of
   judgement, which is why it never gates. "The code this row points at is not
   there" is not a matter of judgement, and existence findings in this repo gate.
4. **It costs an adopter nothing on upgrade.** `check_doc_refs` is warn-first by
   default (`rc 0` without `--strict`), `gates = G3` in `docs/stack.ini`, and
   opt-in downstream — so a repo with unrepaired LLR data is warned, never
   broken. This repo sits at G1, so the four residue rows warn today and become
   a real bar at G3, which is exactly where ratification happens.

**Proved non-vacuous.**
`tests/test_check_doc_refs.py::test_llr_symbol_anchor_reds_on_a_planted_defect`
builds a `tmp_path` scaffold with a real module and a real LLR naming a real
symbol, asserts `--strict` is silent, then plants `LLR-901` naming
`no_such_symbol_anywhere` in that same module and asserts the finding appears,
that `--strict` exits 1, and that the founded row is *not* swept in. Five more
tests pin the boundaries the census made load-bearing: the one-anchor semantics
with its untraced misses; a non-`.py` `Module` skipped; private names, module
constants, classes and class methods RESOLVING (the arch-map\'s public-item table
cannot see 41 of the 149 live rows\' names — the reason the oracle is
`module_bindings` and not the rendered map); a missing `Module` not
double-reported against the path tier; and `*-000` placeholder rows skipped.

### The one new function, and its drift guard

`gen_arch_map.module_bindings(tree)` returns every name a module binds at module
scope, plus class-level `def` names. It lives in `gen_arch_map.py` because that
module already owns AST symbol extraction — a second parser in a second script
is the D-6/F5 hazard, whose failure mode is not a loud crash but a silent "that
symbol does not exist".
`tests/test_gen_arch_map.py::test_module_bindings_covers_every_rendered_public_item`
pins it against `scan_module`\'s rendered rows for every module in this repo, so
the two walks inside the one file cannot drift.

### A second bug the repair exposed — `module_components` never split its cell

Repointing 13 rows dropped the `traj_parse` module out of every CMP component and
red `check_trajectory --strict`. The cause was **not** the repair:
`check_trajectory.module_components` normalized the whole `Module` cell as a
single key, so a `;`-joined `a.py;b.py` produced one nonsense key and tagged
**neither** module. Two live rows were already losing their tags this way
(LLR-080, LLR-142) — silently, because a membership map missing an entry reads
exactly like a module nobody tagged. This is the D-6 failure mode verbatim, in
the reader that had not learned the shape. Fixed to split on `;` like every
other reader of that cell, with
`tests/test_components_registry.py::test_module_components_splits_a_joined_module_cell`.

## Context

Filed and executed 2026-08-11 under the owner's "proceed" on the sub-question
D-9 left open (`docs/repo-lock.md` §2 D-9, "What `Founded` costs to compute —
three of the four tests already exist"). This row builds the **computation**;
the ladder migration that consumes it is held behind the sitting (Q11), and no
`Status` value, and nothing in the `Draft`/`Verified`/`Modified` vocabulary, is
touched here.
