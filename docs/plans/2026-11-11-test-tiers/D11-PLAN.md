# D11: the legacy readers leave the core for the migrator

Planned 2026-11-16 at `maint/vocabulary` `887d36c66` (a read-only planning
pass); the operator ruled decisions A to D the same day, and E and F were taken
as recommended (HANDOFF §12.2). This is §10.7 item 8. Line numbers are at
`887d36c66`; paths are under `project-trajectory/scripts/` unless given.

## The ruling, and where its wording and the code differ

D11 (HANDOFF §2, 2026-11-11): "Migration tooling is its own kind of thing and
is not part of the core; the legacy readers leave the core scripts for it, in a
separate change after the vocabulary." D3: the core reads current spellings
only.

1. Three of the twelve tables are not readers of a stored value, and stay:
   `RETIRED_TAG_RE` (the detector), `FAILURE_CAP_RETIRED_KEY` (a refusal naming
   the new key), and bootstrap's copy of `LEGACY_ACCEPTANCE`, which backs the
   live `--gate-policy` preset (PROCESS.md: the words "are `--gate-policy`
   presets that translate into the `[authority]` dials and are never stored").
2. `bootstrap.py` is not a core script: it is never copied into an adopter, and
   HANDOFF §5 counts `--migrate-config` among the migration tools. Its
   `LEGACY_CONFIG` fold stays (decision C).
3. Adopters hold what two readers read: `gates =` in `docs/stack.ini` at
   gilbert, Finance-Auditor and NotHomeWrecker (verified), and `--gate G3` in
   PictureSorter's own CI (`.github/workflows/check.yml:43`, verified). The
   migrator takes the first; the second is cut and changed by hand (decision A).
4. Four tables read nothing anything stores: `_RETIRED_WI_BARS`,
   `_RETIRED_BARS`, `LEGACY_GATE_DIALS` (in effect), `_RETIRED_FLAG`. For these
   "leave the core for the migrator" means delete.
5. Not on D11's list and left out (decision D): SN-028's one-word-file window
   (the `PROCESS_KEYS` fallback in `declared_policy`, `check_privacy`,
   `check_trajectory`, `trajectory_arch`, `subagent_gate`, `gen_okf`, the three
   hooks); `kitlib/decisions.py` `RETIRED_KEY` with `migrate_text`;
   `check_trajectory.PHASE_ANCHOR_RE` (translates `[g1]`/`[reqs]` anchors in
   work-item titles, which are records under D-4); `expected_failure.RETIRED =
   "bars"` (a refusal).
6. Removing the core dial readers while bootstrap keeps its dial steps would
   leave a gap: `_migrate_dial_key_name` and `_migrate_dial_ordinal` look only in
   `[authority]`, and only the migrator renames `[attestation]`. So the dial's two
   respellings move into the migrator's policy step.
7. Once the dial tables go, `authority.read_dial(policy)` computes what
   `dial_from_config(policy)` computes; merge them.
8. `check_vocab.SUGGEST["G2"]` suggests `DevStg-Tests`, but `check.py` reads
   `--stage G2` as `DevStg-Impl` (WI-498 ROUND-OPUS 8). The RESYNC entry states
   the CLI mapping itself; correct the suggestion too.

## The tables, and the move for each

No traced test-case row cites `test_selection_at_or_above.py`; TC-007/008 cite
`test_stack_profile.py` whole; TC-163 cites `test_stage_ladder.py`; TC-151
cites `test_acceptance_level.py`.

| Table | Where; readers | Spelling, posture; stored where | Accepted rows | Move |
|---|---|---|---|---|
| `RETIRED_STAGE_ALIASES` | `kitlib/config.py:536`; `check.py:1432` `_resolve_stage_alias`, the argparse `choices` at `check.py:2614`, `config.py:603` | `G1`..`G3`, `DevBar-*` by meaning (`G1` Reqs, `G2`/`G3` Impl), warn once; a CLI argument in an adopter's CI, and via `gates =` | none | **Delete.** `gates` goes to the migrator step below; the CLI aliases are cut (A) |
| `_LEGACY_BAR_THRESHOLD`, `_LEGACY_GATES_WARNED` | `config.py:552`, `:562`; `step_threshold` `:584-625` | `[step:*] gates = <list>` to the lowest threshold it names; `docs/stack.ini` at three adopters | none describe it; LLR-038's detail quotes `gates = DevStg-Impl` (stale) | **Migrator step "stack profile"** (B): each `[step:*]` `gates = <list>` becomes `from-stage = DevStg-Needs` when the list names `G1`, `DevBar-Reqs` or `DevStg-Reqs`, else `from-stage = DevStg-Impl`; an unknown token, a continuation line, `gates` under `[DEFAULT]` or both keys present is left, named, exit 1; re-parsed with kitlib's one parser (`test_the_stack_ini_parse_is_one_home` forbids a second). The core keeps a short refusal in `step_threshold` naming `from-stage` and the migrator: a silently ignored `gates = G1 ...` would move a step from Needs to Impl |
| `_RETIRED_WI_BARS`, `_RETIRED_BARS` | `intake.py:214`, `integrate.py:1927` (F5 copy); `normalize_checks_stage`, `_normalize_checks_stage` | a `checks_stage` of `g1`..`g3`/`devbar-*`, silently; nothing holds one | none (LLR-152, TC-146/147 describe refusing a bad value, which stays) | **Delete**, no step: the mint and the landing already refuse an unknown value by name |
| `LEGACY_DIAL_ORDINALS` | `kitlib/authority.py:121`; re-exports `agent_policy.py:508`, `agent_common.py:139`; copy `bootstrap.py:1248`; `read_dial`, `PROCESS_KEY_LEGACY_VALUES`, `_migrate_dial_ordinal` | `operator_accepts_through = 0..4`; `docs/process.toml`, no known holder | SR-139; LLR-156; TC-152; LLR-246, TC-241 | **Migrator policy step**: a bare integer 0..4 becomes the quoted rung (`type(v) is int`, so a bool never matches). Delete the core table, the re-exports, bootstrap's copy and `_migrate_dial_ordinal` |
| `LEGACY_DIAL_KEY` | `authority.py:129`; re-exports; copy `bootstrap.py:1322`; `read_dial:203`, `_retired_dial_note`, `_migrate_dial_key_name` | `human_ratification_through`; `docs/process.toml`, no known holder | LLR-155; TC-150; TC-152; LLR-246, TC-241 | **Migrator**: a `POLICY_KEYS["authority"]` row, run after the table rename. Delete the core copies, bootstrap's copy and `_migrate_dial_key_name` |
| `LEGACY_GATE_DIALS` (+ `LEGACY_GATE_KEY`, `LEGACY_GATE_DEFAULT`, `GATE_POLICY_PATH`, `_first_declared`) | `authority.py:112-139`, `:222`; `read_dial`'s fallback, `dial_at`'s git read of `docs/gate-policy` | the gate-policy word when no dial is declared; the file is folded by bootstrap, the TOML key outranked by the template's dial | SR-139; TC-151; LLR-246, TC-241 | **Delete**, no step |
| `LEGACY_ACCEPTANCE` (was `LEGACY_APPROVAL`) | `agent_policy.py:435`, `legacy_acceptance` `:528`; re-exports; copy `bootstrap.py:1223` | the same word to three dials; core fallbacks for `final_review` and `keep_nondependent` (`:860`, `:1049`) via `PROCESS_KEYS["gate-policy"]`; bootstrap's `apply_gate_policy` (the live preset) and `_migrate_gate_policy` (the fold) | LLR-156; TC-152; SR-138, SR-139 | **Delete the core copy**, `legacy_acceptance`, the two fallbacks and the `PROCESS_KEYS["gate-policy"]` row. **Keep bootstrap's copy, renamed `GATE_POLICY_DIALS`** (F) |
| `LEGACY_CONFIG` | `bootstrap.py:1279`; `_migrate_legacy_file` via `migrate_legacy_config`, every scaffold pass | 14 one-word files folded and deleted | SN-028, SR-138, LLR-156, TC-152 | **Keep** (C) |
| `PROCESS_KEY_LEGACY_VALUES`, `_in_legacy_window` | `agent_policy.py:193`, `:510`; re-export `agent_common.py:128`; `_key_value_findings:1131-1152`, `_vocab_findings:1190` | lets a 0..4 integer past the wrong-type refusal | none change (an integer becomes a wrong-typed dial) | **Delete**, with the two legacy branches and the integer branch |
| `_RETIRED_FLAG` | `check.py:1462`; `_warn_retired_flag_spelling`, the argparse alias `:2611` | `--stage-cleared`; no adopter passes it | none | **Delete** (A) |
| `FAILURE_CAP_RETIRED_KEY` | `kitlib/config.py:329` | `[build] red_rounds_max`, refused naming the new key; shipped on trunk from `b70ecbe9e` | TC-382 evidence | **Keep the refusal, and add a `POLICY_KEYS["build"]` migrator row** (E) |
| `RETIRED_TAG_RE` | `check_vocab.py:116` | the detector | SR-149, LLR-169, TC-163 | **Keep.** Rewrite the docstring's "DECLARATION SITES" paragraph, which names translation tables that will be gone; correct `SUGGEST["G2"]` |

Every migrator line naming `G1` or `DevBar-*` carries `# check_vocab: allow`.

## Decisions, as ruled

| | Ruling |
|---|---|
| A. Retired CLI spellings (`--gate G1..G3`, `DevBar-*` values; `--stage-cleared`) | **Cut both.** argparse refuses loudly; the RESYNC entry gives the mapping; PictureSorter's one CI line changes by hand. The flag name `--gate` stays |
| B. `gates =` in `docs/stack.ini` | **The migrator rewrites them** by meaning; the core keeps a short refusal naming the fix |
| C. Bootstrap's one-word fold | **Stays in bootstrap**, running on every scaffold pass; only the dial's key and integer respellings move to the migrator |
| D. SN-028's one-word-file window | **Left out**, to close under SN-028's own ruling |
| E. `red_rounds_max` | Taken as recommended: keep the refusal and add the migrator row |
| F. Bootstrap's `LEGACY_ACCEPTANCE` | Taken as recommended: renamed `GATE_POLICY_DIALS` (it backs the live preset) |

## Accepted rows to amend (drafts; accepting them is the operator's act)

These join `ROW-AMENDMENTS.md` as a D11 section, applied after the last
migrator run and accepted in one act with SR-247, LLR-369 and TC-427 (D18).
Evidence and `code_symbol` changes are traced cells and move with the code (D4).

- **SR-139 `acceptance_criteria`**, whole: "Level N holds exactly the tiers the
  shipped template documents (cumulative, strictly-less-than the stage); the
  terminal stage rung is held by no level, the end-of-run hold being its own
  dial; an unreadable stage, an absent dial, and a wrong-typed dial all read as
  operator-held; an out-of-range level falls back to the conservative end AND is
  refused loudly." (The gate-policy-word clause goes; SR-138 already requires
  the fold to expand the word.)
- **LLR-155**: `module` `project-trajectory/scripts/agent_policy.py`;
  `code_symbol` `process_config/config_conflicts/acceptance_through/operator_holds`;
  `detail` loses its last sentence ("A legacy dial key the migration cannot
  rename in place is refused rather than altered."), now carried by the
  migrator's Drafted rows.
- **TC-150 `method`**, whole: "Run the process-config suite over a duplicated
  declaration, wrong-typed dials and out-of-range dials, and valid policy files
  containing a dotted key, an inline table or a multi-line string. Assert each
  guarded entry point refuses a duplicated declaration by naming its key and both
  homes, that invalid values are refused rather than defaulted, and that valid
  TOML forms cause no configuration refusal." `evidence` drops
  `test_bootstrap.py::test_the_dial_key_rename_refuses_an_old_key_held_in_an_inline_table`
  (the case moves to TC-427).
- **TC-151 `method`**: delete "the legacy-word translation, "; add "a bare
  integer" to the malformed inputs.
- **LLR-156**: `code_symbol` drops `_migrate_dial_ordinal` (and follows F);
  `detail`'s sentence "`LEGACY_ACCEPTANCE` is F5-duplicated ... pinned equal by
  `test_rule_sync`." becomes "`GATE_POLICY_DIALS` is the one statement of the
  three dials each word means: the `--gate-policy` preset writes them and the
  fold of a `docs/gate-policy` file writes them, and no other script holds a
  copy."; `rationale`, whole: "One table for the preset and the fold means a
  repository scaffolded with a word and one folded from the same word get the
  same three dials. A copy that could disagree about what `single-approve` meant
  would let a repository scaffold with one posture and run with another, the
  shadowing defect the dial was introduced to remove."
- **TC-152**: `method` deletes "the ordinal migration ignores a string decoy;"
  and replaces "that the F5 translation tables are pinned equal" with "that each
  gate-policy word lands the three dials it always meant"; `evidence` drops
  `test_the_dial_key_under_a_bare_authority_header_is_renamed_in_place` and
  `test_the_ordinal_migration_reads_the_dial_never_a_line_inside_a_string`.
- **LLR-246**: `detail`'s "translating each legacy spelling exactly as
  agent_common.acceptance_through does and printing nothing" becomes "reading it
  as agent_common.acceptance_through does, an absent or unrecognised dial as the
  most-held rung, and printing nothing"; `code_symbol` `read_dial` becomes
  `dial_from_config` if the readers are merged.
- **TC-241**: `method`'s "never from the working file and translating each
  legacy spelling silently." becomes "never from the working file, and printing
  nothing."; `evidence` follows the renamed `test_loop_provenance` test.
- **LLR-038** (optional, already stale): "(gates = DevStg-Impl," becomes
  "(from-stage = DevStg-Impl,".

Drafted rows that change (not amendments): SR-247 (after "...each row its
Dispositions section drafts", add "; and in the stack profile, a step's retired
list of stages as the one stage it meant"), LLR-369 and TC-427 (the new steps),
and IF-195 (rationale, data — `read_dial -> (rung, legacy)` goes — and notes).

## RESYNC_PACK

- §1.3 step 1 is unchanged (C).
- Extend the vocabulary entry (`[since 3e7a3a6ee]`, last before §5); no new
  entry. "What changed" gains: "The scripts also stop reading the spellings
  older than this vocabulary: the `G1`-`G3` and `DevBar-*` tags as a `check.py`
  stage value, in a `[step:*] gates =` list and in a work item's `checks_stage`;
  the flag `--stage-cleared`; the dial's 0-4 value and its key
  `human_ratification_through`; and the `gate-policy` word where no dial is
  declared. The migrator rewrites the ones a repository stores."
- Table rows: `gates = <list>` to `from-stage = <rung>` with the rule;
  `human_ratification_through` and `0`-`4` to `operator_accepts_through` and
  the five rungs; `[build] red_rounds_max` to the new key; `--stage`/`--gate
  G1`, `DevBar-Reqs` to `DevStg-Reqs`, `G2`, `G3`, `DevBar-Tests`,
  `DevBar-Release` to `DevStg-Impl`, `--stage-cleared` to `--stage` (`--gate`
  stays).
- Step 7 gains: "`check.py` refuses a retired tag as a stage value and the flag
  `--stage-cleared`; the migrator cannot reach your CI, so change it by the
  table." "Adopter-merged files": `docs/stack.ini` "rewritten by the migrator
  where a `[step:*]` holds `gates =`".
- One supersession line each in the older entries `08c985cb` ("Nothing breaks
  on day one", steps 3 and 4), `7ccbd3a6` ("Nothing breaks at the re-sync"),
  `1a7984ea`, `2a0a85a4` (gates still read; the dial "keeps working"),
  `7e898d15` ("Skipping this is not fatal") and `c907d31b` ("translated
  silently"), per the pack's rule that a superseding pair says so.
- Other prose: `ADOPTING.md:124`, `stack.ini.template:298`,
  `process.toml.template:68-70`, `skills/gate-advance/SKILL.md:61` and its two
  mirrors; regenerate `docs/cli-reference.md`.

## Size and commit order

Roughly 650 lines out and 110 in; 8 accepted amendments (9 with LLR-038) and 4
Drafted rows extended.

1. The migrator learns the older spellings (the new steps, the stack-profile
   text parser use, tests, the Drafted rows). Additive; `--check` here should
   owe nothing.
2. Bootstrap drops its dial steps and copies; `LEGACY_ACCEPTANCE` becomes
   `GATE_POLICY_DIALS`.
3. The core dial readers go, `read_dial` merged into `dial_from_config`, with
   their tests and IF-195.
4. The stage tags go: the `gates` refusal, `check.py`'s aliases and flag, the
   work-item tables, the prose, `docs/cli-reference.md` regenerated.
5. The RESYNC entry extended, with the six supersession lines.
6. One re-stamp commit (size ratchet for `check`, `bootstrap`, `agent_common`,
   `integrate`, `intake`; the `read_dial` complexity row deleted), as D17 did.
7. The four lints and the named modules; the amendment drafts into
   `ROW-AMENDMENTS.md`; then the migrator's last run, and the unfiltered suite
   once.
