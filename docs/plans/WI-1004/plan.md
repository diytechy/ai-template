# WI-1004 plan: ten behaviours walked in series, each to one home

Planned on the maintenance branch `maint/wi-1004`, base `426f88f60`, against
the spec as its critique dispositions left it (`b09b33fed`). The kept answer
on each disputed input is the spec's; this plan says how each lands.

## The walk

One commit per behaviour, in the spec's order. Each commit carries: the
pinning tests (seen red first, for the reason named), the home, the callers
re-pointed, the copies deleted, the tests that exercised only a deleted copy
removed or re-aimed at the home (operator B5, 2026-11-19), the design and
test-case rows, a RESYNC entry where a shipped file changes, and the views
`trunk_step.py --regen` rewrites. A module the size ratchet pins is
re-stamped in the same commit with its reason.

New pins live in one new file, `tests/test_policy_one_home.py`, a section
per behaviour, except where a pin already exists: B3's and B5's repaired pins
stay in `tests/test_rule_sync.py`, where the vacuous ones stand today.

## The construction, per behaviour

1. **B3.** `kitlib.spine.value_to_cell(value)`: `None` is `""`, a list joins
   on `;` with each element `str()`ed, anything else is `str()`. Deleted:
   `migrate_carrier.value_to_cell` and `spine_carrier.value_to_cell`;
   `compare` and `rows_from_toml` call the home. The equality pin becomes an
   identity check plus a value battery with the `None` case.
   Rows: LLR-382, TC-438.
2. **B12.** `migrate_carrier._llr_single_modules` folds through
   `_kitspine.norm_module`; `_short_module` is deleted. Pin: an LLR whose one
   module is `.../pkg/__init__.py` and one whose module is `hooks/x.sh` fold
   to `scripts/pkg` and `hooks/x`. Rows: TC-439 (verifies LLR-197).
3. **Id number.** `kitlib.spine.id_number(rid)` (the renamed `_id_number`).
   Deleted: `kitlib.decisions._id_number` (that module imports
   `kitlib.spine`; a minimal edit, WI-1009 also edits the file),
   `kitlib.registry.spec_id_number` and `wi_convert._id_number`. Pin: `X2-5`
   is 5, `WI-12a` is 0, `WI-0012` is 12, and `read_spec_rows` orders by it.
   Rows: LLR-383, TC-440.
4. **B5.** `check_docs._registry_needs` takes its existence set from
   `_kitspine.sn_all_ids(text, path.suffix)`; `check_flows.load_ids` takes
   `known["SN"]` from the same call. Pins: a TOML needs file whose comment and
   stakeholder description name ids that are no need, run through both
   checkers (the README citing one fails; a flow citing one is unknown); and
   the `need_ids` agreement test on the live TOML needs file. IF-112's note is
   corrected. Rows: TC-441 (verifies LLR-215).
5. **B10.** `consolidate._commissioning_docs` reads its open items from
   `split_pred_edges`; every other ref-cell read in `consolidate`,
   `adjudicate_brief._cited_spine` and `intake._owning_srs` calls
   `kitlib.spine.refs`; `agent_common._refs` binds the home. Pins: for every
   `Predecessors` cell in a battery (`;`, `,`, whitespace, `~`, `OI-5x`),
   `_commissioning_docs` returns exactly `split_pred_edges`' open items; the
   comma-separated `SR-Refs` and `Supersedes` cases read two ids in each
   site. Rows: TC-442 (verifies LLR-210).
6. **B8b.** `kitlib.registry.parse_spec_row` refuses a non-string scalar
   (`priority` may be an integer) and a non-string list element.
   `wi_convert.parse_spec` refuses `active/`, then calls the home and wraps a
   `ValueError` as a `ConvertError`; `split_spec`, `parse_deliverable`,
   `status_from_location`, `_scalar` and `_text` go. Pins: the three disputed
   inputs through both entry points, and `read_spec_rows` reporting the
   `title = 5` spec through `on_error`. Rows: LLR-388, TC-443.
7. **Queued-spec lookup.** `kitlib.registry.queued_spec(work_dir, wi_id)`.
   `integrate` (three callers), `handback._enact_plan` and
   `consolidate._archive_plan` call it; the two `_queued_spec` copies and the
   inline glob go. Pins: two queued specs of one id refuse in all three,
   writing nothing; none refuses in all three. Rows: LLR-384, TC-444.
8. **§13.13.** `kitlib.registry.governing_spec(paths)` over one key
   (terminal folder, then active, then any other; archive, then work; then
   the path). `agent_policy.authoritative_spec` binds it (its `SPEC_HOMES`
   stays: callers still list both homes); `kitlib.done_when._copy_at`
   chooses with it instead of the folder index. Pins: the three disputed
   cases through both entry points, `spec_at` over a git fixture. Rows:
   LLR-385, TC-445.
9. **§13.22.** `split_cmd` moves to `kitlib.config`; `agent_session` imports
   it under its name, and `check._expand` calls it. `check._split_template`
   goes. Pins: a template with an unquoted `#` expands whole through
   `check._expand`, and a JSON array reads as its tokens. LLR-163 drops
   `split_cmd` from its traced `code_symbol`. Rows: LLR-386, TC-446.
10. **§13.16.** `kitlib.config.declared_entries(path)` returns
    `(entries, unparsed)`: `[(lineno, key, reason)]` for each line carrying
    ` — `, `[(lineno, line)]` for each other declaring line. The
    required-separator readers keep their own key rules over it. The
    declared-absences grammar over it (a key with any trailing `/`
    stripped) is `kitlib.config.declared_absences(path)`, which
    `check_doc_refs.read_declared_absences` and `trace._declared_absences`
    both call, so no new edge between two scripts is drawn. The
    `trajectory_arch` edit is the one loop in `_parse_kernel_allow`.
    Pins: a BOM'd file, an undecodable byte, a hyphen line and an unspaced
    em dash, read by every reader. IF-072's note is corrected. Rows: LLR-387,
    TC-447.

## Checks at each commit

The touched test modules plus the standing six; the ratchet; the hook.
`[dupes-census]` is read at the close and re-stamped only if it drops.
