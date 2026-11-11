# The readers' classifications of the duplicated-name groups

Three Claude Opus sub-agents read every definition listed in
[groups_1.txt](groups_1.txt), [groups_2.txt](groups_2.txt) and
[groups_3.txt](groups_3.txt) (2026-11-08, trunk `0fe7277b2`). The third also
traced the twelve behaviours of 2026-08-13 again. Each classified a group as:

- **SAME:** independent copies that agree.
- **DIVERGED:** independent copies that disagree on some input.
- **DELEGATES:** one real home, the other definitions call it.
- **DIFFERENT:** a name collision between unrelated functions.
- **PARTIAL:** a mix of the above.

A finding marked "verified" was checked by running the functions. The others
were read only. These are model readings recorded as they were returned, not
re-checked by hand. [policy.json](policy.json) and
[plumbing.json](plumbing.json) were built from them.

## Batch 1

```text
G1.1 _advance | DIFFERENT | dispatch lane state machine vs plan_round stage field.
G1.2 _changed | DIFFERENT | bookkeeping working-tree vs HEAD (untracked incl.) vs review_set staged-since-merge-base.
G1.3 _clip_title | DIVERGED | check_trajectory (delegates to kitlib.spine.clip_line) vs traj_status (own copy) | PLUMBING | pin covers check_trajectory only | "Fix the thing\nsecond line": check_trajectory joins the lines, traj_status keeps the newline; traj_status also strips trailing spaces before the ellipsis. Verified.
G1.4 _collect | DIFFERENT
G1.5 _count | DIFFERENT
G1.6 _fmt | DIFFERENT | stage vs evidence formatters differ on purpose; the line join is shared in evidence.render_fields.
G1.7 _has | DIFFERENT
G1.8 _identity | DIFFERENT
G1.9 _launch | DIFFERENT
G1.10 _now | SAME | coordinator_guard, session_service | PLUMBING | not pinned | identical strftime; kitlib.observation.format_utc unused by both.
G1.11 _pget | SAME | check, trunk_step | PLUMBING | test_stack_profile covers check only.
G1.12 _real | SAME | assumption_rules, trace_text | PLUMBING | both use kitlib.spine.is_example; only the filter loop is copied.
G1.13 _refusal | DIFFERENT
G1.14 _rev | SAME | integrate, kitlib/verdict | PLUMBING | differ only when git is missing (raise vs None).
G1.15 _shown | DIFFERENT
G1.16 _spec_paths | DIFFERENT | git-tree vs working-tree views over kitlib.registry listings.
G1.17 _status | DIFFERENT
G1.18 _touched | DIFFERENT
G1.19 act | DIFFERENT
G1.20 compare | DIFFERENT
G1.21 derive | DIFFERENT
G1.22 findings_for | DIFFERENT | three doc checks sharing a loop shape.
G1.23 landing_refusal | DIFFERENT | three separate landing gates.
G1.24 load_csv | PARTIAL | gen_release_checklist vs kitlib.spine DIVERGED; wi_convert different (19-column validator) | POLICY | test_csv_header checks header skipping only | byte 0xE9: kitlib replaces, gen_release_checklist raises UnicodeDecodeError. Verified.
G1.25 module_components | SAME | gen_components, trajectory_arch | POLICY | test_components_registry covers trajectory_arch only | raw maps differ (CMP- filter, -000 handling) but every caller intersects with real CMP ids.
G1.26 parse_spec | DIFFERENT
G1.27 read | DIFFERENT
G1.28 record | DIFFERENT
G1.29 render_report | DIFFERENT
G1.30 slugify | DIFFERENT | heading anchors vs filename slug.
G1.31 value_to_cell | DIVERGED | migrate_carrier, spine_carrier | POLICY | pinned by test_the_carrier_value_writer_and_reader_are_the_exact_inverse, no None case | None -> '' vs 'None'. Verified.
```

## Batch 2

```text
G2.1 _blank | DIFFERENT
G2.2 _checked | DIFFERENT
G2.3 _cmd_list | DIFFERENT
G2.4 _context | DIFFERENT
G2.5 _digest | DIFFERENT
G2.6 _git | PARTIAL | bookkeeping, traj_parse DIVERGED; derive_stage delegates to kitlib.git.git_out | PLUMBING | not pinned | non-repo failure: bookkeeping (128, "fatal: ...") vs traj_parse (128, ""); no git: traj_parse (1, "") vs bookkeeping raises.
G2.7 _held | DIFFERENT
G2.8 _install | DIFFERENT
G2.9 _load | DIFFERENT
G2.10 _parsed | DIFFERENT
G2.11 _queued_spec | DIVERGED | handback, integrate (+ inline copy consolidate.py:1532) | POLICY | not pinned | two matches: handback takes the first, integrate raises; none: handback (None, None), integrate raises. Verified.
G2.12 _record_lines | DIFFERENT
G2.13 _report | DIFFERENT
G2.14 _ruling_sync_refusal | DELEGATES | check, integrate -> acceptance_record.ruling_sync_lines | POLICY | tests/test_ruling_sync.py
G2.15 _skip | DIFFERENT
G2.16 _spend | DIFFERENT
G2.17 _text_then_act_refusal | DELEGATES | check, integrate -> text_then_act.text_then_act_lines | POLICY | tests/test_text_then_act.py
G2.18 _tree_text | DIVERGED | adoption_record, plan_coverage | PLUMBING | not pinned | non-UTF-8: raise vs replacement chars; missing path: OSError vs None; rev=None: index vs working tree. Verified.
G2.19 adjudication_keep | DELEGATES | agent_loop -> session_service.adjudication_keep
G2.20 context_block | DIFFERENT
G2.21 evaluate | DIFFERENT
G2.22 git | DIVERGED | agent_common, check_privacy | PLUMBING | not pinned | non-repo: (128, "fatal: ...") vs (128, ""); no git: raise vs (127, ""). Partly verified.
G2.23 lane_branch | DIFFERENT
G2.24 load_registry_rows | SAME | agent_common, schedule (+ inline in pending.open_item_queue) | PLUMBING | tests/test_wi_folder_loaders.py
G2.25 open_item_queue | DELEGATES | pending -> kitlib.spine.open_item_queue | POLICY | tests/test_open_item_queue.py
G2.26 parse_verdict | DIFFERENT
G2.27 read_baseline | DIFFERENT | different TSV schemas; only the shape is alike.
G2.28 record_findings | DIFFERENT
G2.29 scan | DIFFERENT
G2.30 source_paths | DIFFERENT
G2.31 write_baseline | DIFFERENT | the two schemas of G2.27.
```

## Batch 3

```text
G3.1 _cell | DIVERGED (latent) | assumption_rules, consolidate, plan_briefs, trace, rejudge | PLUMBING | not pinned | only rejudge str()s the value; no current input differs.
G3.2 _clip | PARTIAL | adjudicate_brief + agent_common line clips DIVERGED (elision marker); hats + intake delegate to kitlib.spine.clip_line | PLUMBING | hats/intake pinned by test_the_one_line_clip_is_one_home. Verified.
G3.3 _coerce | DIFFERENT
G3.4 _context_block | DIFFERENT
G3.5 _finding | DIFFERENT
G3.6 _git_stdout | DIVERGED | handback, kitlib/git | PLUMBING | not pinned | non-zero exit: (code, stdout) vs None; no git: raise vs None.
G3.7 _id_number | PARTIAL | kitlib/decisions + kitlib/spine SAME (digits after the last dash); wi_convert = byte copy of kitlib/registry spec_id_number (first digit run) | PLUMBING | not pinned | "X2-5" -> 5 vs 2, "WI-12a" -> 0 vs 12. Verified.
G3.8 _judge | DIFFERENT
G3.9 _named | DIFFERENT
G3.10 _parser | DIFFERENT
G3.11 _read | PARTIAL | adjudicate_brief + retire SAME (text or None); plan_coverage differs | PLUMBING
G3.12 _recorded | DIFFERENT
G3.13 _restore | DIFFERENT
G3.14 _say | SAME | dispatch, intake | PLUMBING | prefix differs by design.
G3.15 _span | DIFFERENT
G3.16 _squash_lines | DIFFERENT
G3.17 _tokens | DIFFERENT
G3.18 _walk | DIFFERENT
G3.19 census | DIFFERENT
G3.20 declared_brief | DELEGATES | kitlib/sitting
G3.21 field_block | DELEGATES | kitlib/evidence render_fields
G3.22 interface_findings | DIFFERENT | LLR-041 shape vs LLR-042 connectivity.
G3.23 live_ids | PARTIAL | retire, trace compute the live spine ids twice | PLUMBING
G3.24 load_wis | SAME | check_trajectory, schedule | POLICY | tests/test_wi_loader_sync.py | the pin's reason (schedule stays stdlib-only) is out of date.
G3.25 parse | PARTIAL | kitlib/evidence + kitlib/stage SAME key=value reader; the rest different grammars | PLUMBING
G3.26 preflight | DIFFERENT
G3.27 read_rows | PARTIAL | check_trajectory + gen_okf SAME (= gen_release_checklist.load_csv), DIVERGED from kitlib.spine.load_csv on encoding; consolidate different | PLUMBING. Verified.
G3.28 record_path | DIFFERENT
G3.29 scopes | DIFFERENT
G3.30 strip_dispatcher_block | DELEGATES | prompts
```

## The twelve behaviours of 2026-08-13, traced again

`derive_gate.py` no longer exists. It became the import-only
`spine_rules.py` at WI-498 slice 5, and `derive_stage.py` holds its command
line.

```text
B1  is_example | MULTI, agree on string ids | home kitlib/spine is_example (re-exported by spine_rules, trace_text, gen_release_checklist); copies check_docs _is_sn_example, kitlib/decisions _inert, plan_briefs _skip; 48 inline endswith("-000") in 24 modules. Differ only on None.
B2  declared line | MULTI, agree on line choice | home kitlib/config first_declared_line; copies kitlib/authority _first_declared (agrees), gen_okf read_enabled (raises on undecodable or unreadable file).
B3  value_to_cell | MULTI, DIVERGED | cell_to_value has one home (migrate_carrier); value_to_cell twice (migrate_carrier, spine_carrier); None -> '' vs 'None'.
B4  status predicates | MULTI, agree | home kitlib/spine; restatements spine_carrier is_draft_need, gen_release_checklist _phase_num, inline in traj_parse, pending, trace.
B5  SN id scrapes | MULTI, DIVERGED | homes kitlib/spine sn_all_ids/sn_cited_ids, spine_carrier draft_ids_from_text; copies check_docs _registry_needs, check_flows; on TOML they count comment/description ids (check_flows also SN-000); the need_ids pin is vacuous on TOML.
B6  SN row reader | ONE HOME spine_carrier | trace _sn_prose repeats the -000 skip and emphasis strip; agrees.
B7  [checks] reader | bool toggle one home (kitlib/config process_check); typed siblings (assumption_gate_enabled, process_check_text, subagent_gate read_process_policy, gen_arch_map read_backlink_min) repeat the parse with deliberately different fail directions.
B8  WI registry | MULTI, DIVERGED | spec-folder home kitlib/registry; load_wis twice (check_trajectory, schedule; agree, pinned); agent_common load_wi_registry a third rule (keeps -000); wi_convert parse_spec disagrees with parse_spec_row.
B9  column<->key vocabulary | MULTI, agree | migrate_carrier KEY and spine_carrier SPINE_COLUMN/REGISTRY_COLUMN, exact inverse, pinned.
B10 ref split | MULTI, DIVERGED | home kitlib/spine refs ([;,\s]+); agent_common _refs agrees; ;-only splitters in adjudicate_brief, consolidate (incl. :451 OI edges), intake _owning_srs.
B11 load_csv | MULTI, DIVERGED | home kitlib/spine load_csv (errors=replace); gen_release_checklist load_csv, check_trajectory and gen_okf read_rows raise on a bad byte; agent_common _read_csv_rows agrees on decoding.
B12 module key | MULTI, DIVERGED | home kitlib/spine norm_module; migrate_carrier _short_module differs on __init__.py and non-.py paths; gen_arch_map inline code agrees in practice.
```
