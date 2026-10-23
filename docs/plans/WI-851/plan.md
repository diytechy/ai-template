# WI-851 implementation plan: held-rung spine rows are protected by state (the registry, the snapshot and the dial)

Planner: a fresh Claude Opus session. It read the claim copy
`docs/work/active/wi-851/WI-851-held-rung-state-guard.md` in full, its
`specref` (`docs/plans/2026-10-07-wi841-retro/PROPOSAL.md` §7.1, §7.1b and
§8.4), the owner's ruling 5 in
`docs/log.d/2026-10-07-wi841-retro-owner-rulings.md`, the drafted calls
`docs/decisions/coordinator-2026-10-23.toml` D-002 to D-004, and the code,
registries, prompts, skills and tests the Trust section names. Everything was
read in the lane worktree at `31b8ed941`.

Revision 2 (the plan's one allowed revision), by a second fresh Claude Opus
planner. It re-read the spec in full at the lane's `a4f89d3db`; since
`31b8ed941` the lane gained only the plan, its critique and a telemetry log,
so the spec, code and registries the plan was built on are unchanged. It
answers the one finding of `docs/plans/WI-851/critique-1.md` below, after
confirming it in the code. Every other row stands as first planned.

## Revision 2: the critique's finding, confirmed and answered

- **F1 (MAJOR): confirmed, adopted in P3.** At the lane head,
  `project-trajectory/scripts/kitlib/bootstrap_manifest.py`'s `MAPPING` is an
  explicit list with no wildcard: it maps `scripts/acceptance_record.py` and
  `scripts/text_then_act.py` by name, so a new `scripts/held_status.py` would
  not reach a fresh scaffold. `agent_policy`, `integrate.py` and
  `check_trajectory.py` would then import a module the scaffold lacks, and
  `tests/test_bootstrap.py::test_every_sibling_imported_module_is_shipped_by_mapping`
  fails on exactly that edge. WI-892's own move (`8d498e13f`) is the
  precedent: its squash added the `MAPPING` row with its comment, the
  `scripts/text_then_act.py` line in
  `tests/test_bootstrap.py::test_scaffold_contains_expected_files`'s
  inventory, and the kit-contents row in `project-trajectory/README.md`. P3
  now carries all three in its own behaviour-preserving commit, before any
  successor consumes the move, and runs both bootstrap checks there (tests
  below). P10's overwrite list gains `scripts/kitlib/bootstrap_manifest.py`,
  so an existing adopter's later fresh scaffolds and re-bootstraps carry the
  new mapping too. The component view (`components.derived.toml`) is
  regenerated at the landing (P13), as WI-892's was.

## The architectural-delta answer

DELTA: within

- **Adds a state?** Yes. The verdict binding gains an identity cell, `rows`.
  It records each judged row with the digest of its approved text. Its
  producer is `adjudicate_brief.bind_pending`, and its readers are the act
  turn and the lane rule (P5 to P8).
- **Adds a value to a domain?** Yes, four:
  - the binding grammar gains the `rows` line (IF-287);
  - the amendment brief gains one slot, `{identity}`, which renders the
    `JUDGED-TEXT:` lines (the ADJUDICATE-AMENDMENT template);
  - `text_then_act.LANE_COMMIT_RIDERS` gains a fourth rider;
  - the act turn's refusal set gains one reason (IF-296).

  The `held-status` step's name does not change.
- **Makes an output depend on a new input?** Yes, two:
  - A lane's landing, at the slot and at a squash, now depends on how the
    snapshot copy moves and on the bound identity, not on loop provenance.
  - The marker arm's verdict now also depends on whether the checkout's
    branch is a claimed lane (the claimed-branch reader).
- **Crosses a new boundary?** Yes, and a sub-component split carries it.
  - The held-status section moves out of `acceptance_record` into a new
    module, `held_status.py`, which becomes IF-196's owner (P3). Its new
    requestors are `text_then_act` (the rider), `check` and `agent_policy`.
  - `adjudicate_brief` and `adjudicate_act` read the digest across IF-129.
  - `agent_policy` reads the claimed-branch reader, which moves from
    `check.py` into `kitlib.git` (P2).

Each change is a row of the table:
- P2: the reader's move;
- P3: the module split and IF-196's owner;
- P5: the digest and the identity cell (IF-129, IF-287);
- P6: the brief slot and the producer;
- P7: the act turn's refusal (IF-296);
- P8: the rider, the hook step, the narrowed arm and the retirements.

Revision 2 re-answers the question and the answer stands: F1's scaffold
mapping is the delivery half of P3's module split, the same boundary already
counted above, and adds no state, domain value, input or boundary of its own.

No refactor outside this item is needed. One consequence goes past the spec's
listed row set: the move makes LLR-249's detail name a function that no
longer lives where it says. Settled point 2 records it, and R1 gives the
coordinator a fallback that keeps the set exact.

## Settled points

These points were open in the spec or had to be fixed before the build.

1. **Two prep moves before unit 1, as the spec allows.** On this base,
   `acceptance_record.py` measures 998 SLOC. The module-size ratchet's
   THRESHOLD is 1000, and the module has no baseline entry. Unit 1 adds the
   digest beside `split_changed_cells` (about 10 SLOC). The held clause
   (about 48 SLOC) retires only in unit 2+3's commit. So unit 1 cannot land in
   `acceptance_record` without first moving something out.
   - P3 moves the whole held-status section (108 SLOC) into `held_status.py`,
     which leaves `acceptance_record` at about 890 SLOC.
   - The section is IF-196's: the registry constants, the status readers, the
     `held_status_lines` and `held_status_refusal` judgement, `_empty_tree`
     and `committed_status_moves`.
   - It is the spec's own option ("move that section whole into its own
     module first (WI-892's move of text then act)"). The new lane rule joins
     the section there in P8, so IF-196 keeps one home.
   - The import direction is one way: `held_status` imports
     `acceptance_record`, and never the reverse.
2. **The move touches one row outside D28's list.** LLR-249's detail (SR-210,
   Approved) names `acceptance_record.committed_status_moves`, and that
   function moves.
   - The plan re-points the name in the intent set (P1). Expected ruling:
     CLARITY. The row joins the same combined sitting (P12).
   - The history check's module, `check_trajectory.py`, has an exact baseline
     (1654). Importing the moved names adds the try/except import pair, so P3
     records a reviewed +2 bump with its reason in
     `docs/decisions/wi-851.toml`.
   - R1 gives the coordinator the alternative, a split move that leaves the
     history half in `acceptance_record`.
3. **"Landed with unit 3" is read as "in unit 2+3's commit"** for the prose
   that states the rule:
   - the `spine-authoring` line;
   - PROCESS.md §4's held sentence;
   - the two `coordinator-cycle` lines;
   - the brief and hook wording.

   So no commit carries a rule that its own docs contradict. Two items are not
   in that commit:
   - the spine rows, authored once in P1 and reconciled at the checkpoint;
   - the RESYNC entry, a separate later commit (P10), because its anchor is
     set at the landing.

   All four units land on trunk together, in one landing.
4. **The digest** is `acceptance_record.approved_text_digest(registry, id_col,
   row)`, placed beside `split_changed_cells` (IF-129).
   - It takes every cell except the id column and `Status`, and keeps those
     that `spine_cell_class` classes `approved`.
   - It drops empty values, so an absent cell and an empty one hash alike, as
     `split_changed_cells` compares them.
   - It serializes the result with `json.dumps(sort_keys=True,
     ensure_ascii=True, separators=(",", ":"))` and returns `"sha256:"`
     followed by the first `kitlib.done_when._DIGEST_CHARS` (16) hex
     characters.
   - Rows are read through `spine_carrier`'s readers. TOML and CSV carriers
     then yield the same column names, so a carrier change does not move the
     digest.
   - The module comment that records the 2026-08-15 directive (which retired
     the on-row `TextHash`) gains one paragraph: this digest lives in no row,
     needs no separator, and reuses IF-129's classes (D-002).
5. **The identity cell.** The binding gains one optional line:
   `rows = <ID>=sha256:<16 hex>;<ID>=sha256:<16 hex>`.
   - `kitlib.sitting.render_requested(brief, kinds, outcome,
     identities=None)` writes it only when identities are given.
   - `read_requested` keeps its `(brief, kinds, outcome)` return unchanged, so
     `kitlib.done_when`, `plan_gate.py`, `plan_coverage.py` and
     `adjudicate_act._unaccepted_reason` read nothing new.
   - `read_identities(text)` is a new reader. It returns `({id: digest},
     None)`, or `(None, reason)` for "no identity cell" or "a malformed cell".
     Every token must match `<ID>=sha256:<16 lowercase hex>`, and an id may
     not repeat.
   - `accepted_identities(root, rev, verdict_path)` is the one reader of an
     accepted verdict's bound identities. It returns `(identities, None)` only
     when `accepted_at` reads the verdict as accepted, and `(None, reason)`
     otherwise.
   - `write_binding` gains `identities=None`.
   - `adjudicate_brief.record_outcome` must keep the cell when it rewrites the
     binding to `accepted` or `failed`. It reads the bound identities back
     beside `bound_kinds`. If it dropped them, every held CLARITY act would be
     refused, so the plan names this explicitly and P4 tests it.
6. **The producer.** `amendment_values` returns a new `identity` value: one
   `JUDGED-TEXT: <ROW-ID> <digest>` line per row the brief shows.
   - It covers the requirement-chain rows (`_amended_rows`) and the need,
     assumption and surrogate rows (`_unchained_amended_rows`).
   - Each digest is computed from the row text that the brief's own reader
     loads, so for one text the brief's digest and the rule's digest are
     equal. P4 pins this on a clean lane.
   - The template gains `{identity}` under the AMENDED CELLS block, and the
     catalog regenerates.
   - `bind_pending(verdict_path, brief, prompt, exclusive)` reads those lines
     off the composed prompt, `adjudicate_brief.requested_identities(prompt)`
     being the one reader of the line, and writes them. A combined prompt
     carries them inside its amendment section. A prompt with none writes no
     cell.
   - Both routes reach this through `bind_pending`: the coordinator's entry
     point at reservation, and the loop at composition.
   - `_HELD_ARMS["reattest"]` gains one sentence. The re-attestation is bound
     to the text shown, and an edit after the verdict refuses the act.
7. **The act turn.** In `adjudicate_act._derive`, `_state` gains one check for
   a held re-attestation of a row that claims approval and does not equal its
   copy (an owed held CLARITY act).
   - The committed row's digest must equal the identity that the verdict's
     binding records for that row.
   - A missing cell, a malformed cell, an unbound row or a different digest
     each refuse the whole derivation. The reason names the row, the bound
     digest and the committed digest. So `compose_act` refuses, and
     `coordinator_adjudicate.py act` refuses before launch.
   - Released rungs and "taken" states are not touched.
   - The `--verdict` naming in the act brief stays, for audit.
8. **The claim predicate is a pure function**,
   `held_status.held_claims(after, before, held)`. P5 tests it in process.
   - `after` and `before` each map `(registry, id col)` to `(live rows, copy
     rows)` on one side. `held(registry)` is the dial test.
   - It returns `{(row id, registry, id col): "a" | "b"}` for every row whose
     registry the dial holds and that makes a D2 or D3 claim on that side.
   - `-000` rows are skipped.
   - A (b) "move" means `split_changed_cells` reports an approved cell, or the
     copy's `Status` differs, between the copy's two sides. A traced-only move
     is not a claim.
   - The exception's five conditions (D5 to D9) are a separate function. Only
     its last two read git.
9. **The verdict search.** For each held row that needs the exception, the
   candidate bindings are the `*.requested` files under `docs/reviews/` in the
   judged tree that name the row in a `rows =` line. They are found with one
   `git grep -l -F "<ID>="` at the tree, or `--cached` for the index.
   - Each candidate is read through `accepted_at` and
     `accepted_identities`.
   - The row passes when one candidate's amendment part rules it `CLARITY`,
     read through `row_rulings`, so a row tagged both ways reads MEANING and a
     `[MEANING+BLESS]` row fails.
   - That candidate's bound digest must also equal the digest of the row at
     the commit.
   - A grep git cannot run is a refusal line, never "no candidate".
10. **The narrowed marker arm (D-004, option ii)** is one function,
    `held_status.marked_refusal(root, base, head, dial, paths=None)`. Both
    the hook step and `agent_policy.loop_held_status_refusal` call it.
    - **Status moves:** today's off-spine walk, unchanged, plus the spine
      status walk over the requirement, design, test and need tiers. That
      walk is extracted from `committed_status_moves` as
      `_spine_status_moves`, so the two share one walk, and each row is
      reported once.
    - **Approval claims:** `held_claims` with no exception.
    - It runs only for a marked process outside a claimed lane.
      `kitlib.git.claimed_work_branch(repo)` answers None off git, on a
      detached HEAD, and on an unclaimed branch, so such a commit is judged.
    - The writers follow with no code change: `bookkeeping._commit_object`
      (on trunk) is judged; `handback._loop_commit` (in a lane) passes at the
      commit; `agent_common.commit_telemetry` is judged when its root is not
      a lane.
11. **The hook step's three modes.** `check._held_status_refusal` handles
    them in this order:
    1. Off git: None.
    2. A squash in progress (`kitlib.git.squash_commits`, no MERGE_HEAD): the
       squash is judged whether it is marked or not. This calls
       `text_then_act.squash_walk(root, head, tip, paths, riders)` with
       `held_status`'s watched paths and its rider alone.
       - `squash_walk` is extracted from `_squash_lines`, which keeps its own
         paths and rider, behaviour-identical.
       - It is admitted when the tip contains HEAD and the staged carriers of
         the eight registries and the record equal the tip's.
       - When it is not admitted, the index is judged as one lane commit
         against HEAD, with the CLARITY exception, plus the squash rebase
         hint.
    3. Marked, outside a lane: `marked_refusal` over the index against HEAD,
       with MERGE_HEAD during a merge through `pending_status_moves`, and the
       dial committed at HEAD.

    Every other case is None. The composition sits in `check.py`, because
    `text_then_act` imports `held_status` for the rider, so `held_status`
    cannot import `text_then_act`.
12. **The rider.** `held_status.commit_held_approval_lines(root, rev)` judges
    one commit.
    - Its parents come from `acceptance_record._commit_parents`, so an
      unreadable parent is a line, never a root.
    - The dial is `dial_at(root, "HEAD")`, which is trunk at the slot.
    - The commit's claims are those made against every parent, so a refresh
      merge claims nothing that trunk brought in.
    - The CLARITY exception reads the commit's own tree.
    - Each line names the commit, the row, its rung and the dial, and carries
      its own remedy. `integrate._with_text_then_act_remedy` leaves it alone,
      so `integrate.py` gains no new code for the rider.
13. **D27 needs no lane edit.** Both deferred specs already satisfy it:
    - `docs/work/deferred/WI-800-session-store-and-usage-ledger.md` needs
      WI-851 and says "Its LLR-246 amendment follows WI-851's state rule";
    - `WI-809-in-lane-sitting.md` needs WI-851 and says its held rows "are
      judged by WI-851's state-based check".

    P9 re-reads both at the checkpoint. If either has drifted, the
    coordinator amends it on trunk; a lane does not edit another row's spec.
14. **The four IF rows stay Drafted.** Interface rows are off-spine, outside
    the approval act (`OUTSIDE_THE_APPROVAL_ACT`, OI-30 D3). Their contract
    text rides the one change set and is shown to the combined sitting as
    context for the rows that cite it. No act moves them (P12).

## The plan

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | The intent change set, one commit, authored by the declared spine author (Terra), drafted once. It amends the normative cells of SR-208 (the rule, stated without code: a held-rung row's approval lands from a lane only as a CLARITY re-attestation bound to its judged text, and a marked autonomous commit outside a lane may not move a held status or claim a held approval), LLR-246 (the lane rule, the walk, the narrowed marker arm, the slot rung's retirement), LLR-278 (the held ledger clause retires; the text identity: digest, brief lines, binding cell, act-turn refusal), LLR-249 (its module re-point, settled point 2), TC-241 and TC-278 (their method and expected), the data, rationale and notes of IF-196, IF-287, IF-296 and IF-129, and IF-220's notes (`verdict` recorded, no rule requires it). Traced cells (module, code symbol, evidence, test refs) and IF-196's owner are re-pointed in the commits that make them true. | D28; SR-208; SR-178; TC-241; TC-278 | IF-196; IF-287; IF-296; IF-129; IF-220 | |
| P2 | Behaviour-preserving move A, its own commit. `check._claimed_work_branch` moves into `kitlib.git` as `claimed_work_branch(root, notice=None)`. `check.py` passes a `notice` callable that prints today's implausible-name stderr line, and `_work_branch` and its cache are unchanged. `kitlib.git.__all__` gains the name. `check.py` is re-stamped downward in the module-size baseline. | D22; SR-208 | no interface row: kitlib.git declares none (git_out, git_show and squash_commits carry no IF row); a behaviour-preserving move of check.py's own reader into it | P1 |
| P3 | Behaviour-preserving move B, its own commit. The whole held-status section (`NEEDS_REGISTRY`, `HELD_STATUS_REGISTRIES`, `STATUS_TABLES`, `_status_cells`, `_status_delta`, `_offspine_status_moves`, `staged_status_moves`, `merge_status_moves`, `pending_status_moves`, `held_status_lines`, `held_status_refusal`, `_empty_tree`, `committed_status_moves`) moves to the new `project-trajectory/scripts/held_status.py`, which imports `acceptance_record` one way. `Contracts: IF-196` and its body move with it, and IF-196's owner is re-pointed to `scripts/held_status`. Every caller imports the new module: `agent_policy` (module level), `check.py` (deferred), `integrate.py` (module level, so it adds no deferred edge), `check_trajectory.py` (module level), and the tests. Ratchets in the same commit: `acceptance_record` drops about 108 SLOC and stays unbaselined; `check_trajectory` takes the reviewed +2 (settled point 2); `test_import_layers`' deferred window is re-stamped if `check -> held_status` takes it past 39, with the reason. **Delivery, in the same commit (F1):** `kitlib/bootstrap_manifest.py`'s `MAPPING` gains `("scripts/held_status.py", "scripts/held_status.py")` beside `text_then_act.py`, with a comment naming its unguarded importers; `tests/test_bootstrap.py::test_scaffold_contains_expected_files` gains `scripts/held_status.py` in its inventory; `project-trajectory/README.md`'s kit-contents table gains the `scripts/held_status.py` row (stdlib only, IF-196's home, its callers), and `acceptance_record.py`'s row drops the held-status section it no longer holds. The commit runs `tests/test_bootstrap.py::test_every_sibling_imported_module_is_shipped_by_mapping` and `::test_scaffold_contains_expected_files` green before P4 starts. | D1; F1; SR-208; TC-241 | IF-196; IF-195; IF-102 | P2 |
| P4 | Tests first, committed alone before any behaviour change. New modules: `tests/test_held_status.py` (in process, smoke tier, the family's pin) and `tests/test_held_status_git.py` (real git, added to `tests/conftest.py` SLOW_MODULES). Cases are added to `tests/test_adjudicate_brief.py`, `tests/test_adjudicate_act.py` and `tests/test_coordinator_act.py`. Each new behaviour is marked `xfail(strict=True)`, with stubs where a name is new, so each red reaches its own assertion. The cases are listed per step below. | D29; D30; D31; D32; D33; D34; D35; D36; D37; D38; D39; D40; D41; D42; SR-208; SR-178; TC-241; TC-278 | no interface — test files only | P3 |
| P5 | Unit 1a: the digest and the identity cell. `acceptance_record.approved_text_digest` (settled point 4), with IF-129's contract body extended in the module header and the 2026-08-15 comment answered. `kitlib.sitting`: `render_requested(..., identities=None)`, `read_identities`, `write_binding(..., identities=None)` and `accepted_identities` (settled point 5), with IF-287's contract body extended. Stdlib only: `hashlib`, `json`. | D20; D9; D47; SR-178; TC-278; TC-331 | IF-129; IF-287 | P4 |
| P6 | Unit 1b: the producer. `amendment_values` renders the `identity` value; ADJUDICATE-AMENDMENT gains the `{identity}` slot and its dispatcher note, and the held CLARITY sentence now says the verdict binds the shown text. `adjudicate_brief.requested_identities(prompt)`; `bind_pending` writes the cell; `record_outcome` carries it through its rewrite; `_HELD_ARMS["reattest"]` gets its sentence (settled point 6). `prompts/CATALOG.md` is regenerated in the commit (the `prompt-catalog` step). | D20; SR-178; TC-278; TC-331 | IF-115; IF-287; IF-129 | P5 |
| P7 | Unit 1c: the act turn and runtime flow 6. In `adjudicate_act._state`, the held CLARITY identity check (settled point 7), plus its refusal reason in IF-296's contract body. `docs/runtime-flows.md` flow 6: the bind step records the judged rows' identities; the act turn's refusal branch gains "a held CLARITY row whose approved text differs from its bound identity"; the prose's hand confirmation that the judged rows are unchanged becomes that check for held CLARITY rows. | D20; D33; SR-178; TC-278 | IF-296; IF-287 | P6 |
| P8 | Units 2 and 3 in ONE commit, with their prose (settled point 3). **The rule** in `held_status.py`: `HELD_TIERS` (every tier of the eight snapshotted registries, pinned equal to `baseline_snapshot.SNAPSHOT_TIERS`); `held_claims`; the exception; `held_approval_lines(root, bases, head, dial, exception=True)`, which reads trees through `acceptance_record._tier_reads`, live and under `SNAPSHOT_DIR`, and follows the Trust ruling's failure shapes; `commit_held_approval_lines` (the rider); and `marked_refusal` with `_spine_status_moves` extracted from `committed_status_moves`. **The walk:** the rider joins `text_then_act.LANE_COMMIT_RIDERS` after parent-first; `squash_walk` is extracted from `_squash_lines`; `check._held_status_refusal` takes its three modes; the hook's comment entry is rewritten. **The retirements:** `integrate._held_status_refusal` and its `_merge_refusal` call (`_loop_window` stays for the trailer rung); `acceptance_record.held_reattest_refusal`, `_held_act_lines`, `_held_row_line`, `_below_approval` and `_held_row`, with their call in `merge_approval_refusal`. `lane_acted_set`, `backed_act_refusal`, `reattest_scope_refusal`, the unaccepted and uncovered refusals and the copy check stay untouched. **The narrowed arm:** `agent_policy.loop_held_status_refusal` composes the lane test and `marked_refusal`. **Docstrings** that name the retired arm are fixed: IF-091's body, `adjudicate_act`, `baseline_snapshot`, `intake`. **Prose:** `spine-authoring` `references/in-lane.md` line 60–62 (the CLARITY verdict, bound to the text, permits the act; `--verdict` is for audit), PROCESS.md §4's held paragraph (the byte-budget guard runs before and after), the `coordinator-cycle` SKILL.md line 541 and recipes.md line 662, the dogfooded skill copies (`skills-sync`). **Ratchets:** `integrate.py` and `check.py` are re-stamped to their measured SLOC (down expected; any up is a reviewed bump with its reason), and the complexity baseline is updated only for a function over its threshold, with the reason. | D1; D2; D3; D4; D5; D6; D7; D8; D9; D10; D11; D12; D13; D14; D15; D16; D17; D18; D19; D21; D22; D23; D24; D25; D26; D30; D31; D32; D33; D34; D35; D36; D37; D38; D39; D40; D41; D42; D48; D49; D50; SR-208; SR-178; TC-241; TC-278 | IF-196; IF-091; IF-287; IF-195; IF-102; IF-308; IF-261 | P7 |
| P9 | The D27 read: WI-800's and WI-809's deferred specs still need WI-851 and cite its state rule (settled point 13). The coordinator gets the result; nothing is written in the lane. | D27; SR-208 | no interface — a read of two specs | P8 |
| P10 | The RESYNC_PACK entry, its own commit, anchored `[since <trunk sha>]` at the lane's trunk base and re-anchored after any rebase. **What changed:** the state rule and its two walks; the retired act-ledger CLARITY arm and the retired slot rung; the narrowed marker arm (marked, outside a lane, all eight registries); the binding's `rows` cell and the amendment brief's `{identity}` slot; `intake.py snapshot --verdict` stays optional and recorded. **What to do:** an adopter's unmarked trunk approvals are untouched; a held CLARITY verdict sat before the upgrade carries no identity and must be re-sat before its act. **Kit-owned files — overwrite:** `scripts/held_status.py` (new), `scripts/acceptance_record.py`, `scripts/kitlib/git.py`, `scripts/kitlib/sitting.py`, `scripts/kitlib/bootstrap_manifest.py` (the new module's mapping, F1), `scripts/adjudicate_brief.py`, `scripts/adjudicate_act.py`, `scripts/text_then_act.py`, `scripts/check.py`, `scripts/integrate.py`, `scripts/agent_policy.py`, `scripts/check_trajectory.py`, `scripts/baseline_snapshot.py`, `scripts/intake.py`, `hooks/pre-commit`, `prompts/adjudicate-amendment.template.md`, `prompts/CATALOG.md`, `PROCESS.md`, `skills/spine-authoring/references/in-lane.md`. | D43; D44; D45; D46; SR-208 | no interface — kit prose | P8 |
| P11 | Regression and fixture audit: one full unfiltered suite run (`python -m pytest -q -n auto`), with the real output pasted. A fixture that today flips a held-rung row in a lane only to reach a later rung is fixed in the fixture: release its dial, or route the flip through a bound CLARITY act. It is test data, never a rule exception. Then SR-178's and SR-208's TCs are re-run over the result. | D21; SR-178; SR-208; TC-153; TC-269; TC-271; TC-278; TC-331; TC-241 | IF-091; IF-196; IF-287 | P9; P10 |
| P12 | D28's one combined sitting at the checkpoint. P1's set is reconciled against the settled code: the traced cells follow the code, and the normative text matches what was built. Then one combined sitting judges the set as amendments: SR-208 and LLR-246 (expected MEANING, marked `[MEANING+BLESS]` if blessed), LLR-278, TC-241, TC-278, and LLR-249 (expected CLARITY). All of these rungs (Reqs, LLReqs, Tests) are released under `DevStg-Boundary`, so the act turn re-attests them and no owner act is needed. The IF rows ride as context (settled point 14). | D28; SR-208; SR-178; TC-241; TC-278 | no interface — a registry act, no code changes | P11 |
| P13 | The gate over the checkpoint tip, one cross-family REVIEW-A (Codex Sol), then the landing. At the landing the coordinator re-anchors P10's entry and regenerates the trunk-only artifacts: cli-reference (the `--held-status` help), interface-reference (IF-196's new owner and bodies), the component view and PROJECT_STATE.html. | D43; SR-208 | no interface — review and landing, no code | P12 |

## Tests per step, and what each fails on before its change

Unless a case is marked *characterization*, it goes in at P4 as a strict
expected failure and turns green in the step named. Real-git cases go in
`tests/test_held_status_git.py`, and in-process cases go in
`tests/test_held_status.py`, unless another module is named.

**P2 and P3** (characterization; no new red):
- The existing `held-status`, writer and history suites run unchanged over
  the moved code: TC-241's `tests/test_integrate_admission.py` cases, the
  `tests/test_loop_provenance.py` history cases, and `tests/test_plan_gate.py`
  and `tests/test_ruling_sync.py`, which import the moved names. Only import
  paths change.
- `test_the_claimed_branch_reader_has_one_home` asserts
  `check._claimed_work_branch` delegates to `kitlib.git.claimed_work_branch`,
  and that the implausible-name notice still reaches stderr. It fails before
  P2: the attribute is absent.
- `test_held_status_owns_IF_196` asserts the module declares `Contracts:
  IF-196` and `acceptance_record` no longer does. It fails before P3: no such
  module.
- `tests/test_bootstrap.py::test_scaffold_contains_expected_files` gains
  `scripts/held_status.py` (F1). Its new line fails before P3's mapping row:
  a fresh scaffold has no such file.
- `tests/test_bootstrap.py::test_every_sibling_imported_module_is_shipped_by_mapping`
  runs unchanged in P3's commit (F1). It is the class guard: had P3 moved the
  section and re-pointed the callers without the `MAPPING` row, it would fail
  on the `agent_policy -> held_status` and `integrate -> held_status` edges.

**P5** (in process):
- `test_the_digest_ignores_the_id_status_and_traced_cells`: changing `Status`,
  the id, or a traced cell (`Module`, `SN-Refs`) leaves the digest unchanged,
  and changing `Requirement` moves it. Fails before: the name is absent.
- `test_the_digest_is_carrier_blind_and_empty_equals_absent`: a TOML row and
  its CSV twin hash alike, and an empty cell hashes like a missing one. Fails
  before (absent).
- `test_the_digest_has_the_done_when_shape`: it matches `^sha256:[0-9a-f]{16}$`.
  Fails before (absent).
- `test_a_binding_round_trips_its_identities` and
  `test_read_requested_ignores_the_identity_cell`: the new reader returns the
  map, and the old 3-tuple is unchanged. Fail before: `render_requested`
  takes no `identities`.
- `test_a_malformed_or_absent_identity_cell_reads_as_no_identity[no cell,
  bad token, short hex, repeated id]`. Fails before (absent).

**P6** (`tests/test_adjudicate_brief.py`):
- `test_the_amendment_brief_states_each_shown_rows_digest`: one
  `JUDGED-TEXT:` line per shown row, the need tier included, each equal to
  `approved_text_digest` of the committed row on a clean lane. Fails before:
  no such line.
- `test_bind_pending_records_the_briefs_identities`: also for a combined
  prompt, with no cell for a first-approval-only prompt. Fails before: the
  binding has no `rows` line.
- `test_record_outcome_keeps_the_identity_cell`: accepted and failed alike.
  Fails before: the rewrite drops it.

**P7** (`tests/test_adjudicate_act.py` in process;
`tests/test_coordinator_act.py` real git):
- `test_a_held_CLARITY_act_bound_to_the_exact_text_is_owed` (D32). Fails
  before: the fixture's binding carries an identity the old code ignores, so
  this case is *characterization* for the owed result, plus an assertion that
  `owed_acts` consulted the identity (a stub spy), which fails before.
- `test_a_held_CLARITY_act_whose_text_changed_after_the_verdict_is_refused`
  (D33): it names the row and both digests. Fails before: the act is owed.
- `test_a_held_CLARITY_act_whose_binding_has_no_identity_is_refused` (D34,
  D46). Fails before: owed.
- `test_the_act_turn_refuses_before_launch_when_held_text_moved`
  (`test_coordinator_act.py`): `coordinator_adjudicate.py act` exits nonzero,
  naming the row, and the stub adjudicator is never launched. Fails before:
  the stub runs.

**P8, the claim predicate** (in process, pure):
- `test_a_live_flip_into_approval_is_a_claim[Approved, Founded, born
  Approved]` (D2). Fails before: the stub returns `{}`.
- `test_a_copy_entry_move_or_retirement_is_a_claim[entered, approved cell
  moved, Status moved, retired]` (D3). Fails before (stub).
- `test_not_judged[Drafted sibling, demotion, below-approval move,
  traced-only copy move, released rung, -000 row]` (D11 to D15). The fixture
  also holds one real claim, and the result must equal exactly that one
  claim. Fails before (stub), and catches over-reporting after.
- `test_an_unmapped_registry_is_held`. Fails before (stub).
- `test_HELD_TIERS_equals_the_snapshotted_tiers`. It is a pin, so it fails
  before: the name is absent.
- `test_the_rule_rides_the_lane_commit_walk`: the rider is in
  `LANE_COMMIT_RIDERS` after `commit_parent_first_lines`. Fails before.
- `test_the_slot_no_longer_runs_a_loop_lane_held_status_rung`: there is no
  `integrate._held_status_refusal`, and `_merge_refusal`'s ladder does not
  call it. `tests/test_text_then_act.py`'s rung list drops the name in the
  same commit. Fails before.
- `test_the_ledger_clarity_arm_is_retired`: `acceptance_record` has no
  `held_reattest_refusal`. Fails before.

**P8, the slot** (real git; each case drives `integrate.integrate_one`, so
before P8 each fails because the lane merges or reaches a later rung):
- `test_a_lane_approving_a_held_SN_with_its_copy_is_refused` and
  `test_a_lane_flipping_a_held_rows_status_without_its_copy_is_refused`
  (D30). The refusal names the row, its rung and the dial.
- `test_loop_coordinator_and_reclaimed_lanes_are_judged_alike` (D31): the
  same flip in a marked lane, an unmarked lane and a re-claimed lane, each
  refused.
- `test_a_held_CLARITY_reattestation_bound_to_the_exact_text_lands` (D32),
  once with `--verdict` named and once without (D21: optional, recorded). It
  passes the approval-act rung and the rider, and stops at the fixture's
  declared-bar question.
- `test_held_text_changed_after_its_CLARITY_verdict_is_refused_at_the_slot`
  (D33).
- `test_a_binding_with_no_identity_cell_is_refused` and
  `test_a_held_MEANING_BLESS_reattestation_is_refused` (D34).
- `test_a_held_retirement_is_refused` (D35).
- `test_a_held_CLARITY_act_carrying_an_edited_Drafted_sibling_lands` and
  `test_a_traced_only_copy_move_lands` (D36).
- `test_a_refresh_merge_carrying_trunks_approvals_lands` (D37). The
  approvals were taken on trunk by an unmarked commit.
- `test_an_unreadable_or_unparseable_registry_or_copy_is_refused_by_name[live
  undecodable, live unparseable, copy unparseable]` (D38).
- `test_an_off_spine_demotion_and_a_born_Drafted_row_land_from_a_loop_lane`
  (D12 and D-003: what loop lanes lose).

**P8, the hook and the writers** (real git; each drives `check.py
--run-steps held-status` or a writer, so before P8 each fails on its exit or
refusal assertion):
- `test_an_unmarked_plain_trunk_commit_approving_a_held_row_passes` (D19,
  D39): exit 0.
- `test_the_same_commit_marked_is_refused_by_the_hook_step` (D40, D23):
  exit 1, naming the row. It fails before because the marked arm watches no
  spine tier.
- `test_a_marked_held_SN_demotion_outside_a_lane_is_refused` (D22, D-004).
- `test_each_loop_writer_outside_a_lane_refuses_a_held_approval[claim, mint,
  telemetry]` (D40, D24). Fails before: the writers see no off-spine move.
- `test_a_marked_commit_inside_a_lane_passes_at_commit_and_is_judged_at_landing`
  (D41). The hook step passes, as does `handback._loop_commit`, which before
  P8 refused (TC-241's residue-writer case is rewritten to this); the slot
  then refuses the lane.
- `test_a_squash_landing_is_judged_by_its_lane_commits[marked, unmarked]`
  (D42, D18): a squash whose lane carries a refused commit fails, naming the
  commit, and a clean lane's squash passes.
- `test_a_squash_not_admitted_is_judged_as_one_commit` (D42): the staged
  registry differs from the tip, and the index's own claim is refused with
  the rebase hint.
- *Characterization:* `tests/test_text_then_act.py`'s squash cases pass
  unchanged over the extracted `squash_walk`.

**Rewritten or retired in P8** (TC-241 and TC-278 evidence):
- `tests/test_integrate_admission.py` §6 and §6b: the slot rung cases become
  lane-rule cases above. The person's-lane case inverts, because every lane
  is judged. The writer cases keep claim, mint and telemetry, and the
  residue case moves to D41.
- `tests/test_loop_provenance.py`: the two cases calling
  `integ._held_status_refusal` retire. Their re-claim and unreadable-claim
  arms survive on the trailer rung, and the history cases are untouched.
- `tests/test_snapshot_readers.py`: the eight `held_rung_*` cases and
  `test_a_rejected_bound_sitting_cannot_carry_a_held_rung_reattestation`
  retire into the slot cases above. `test_a_held_rung_is_read_from_trunk_not_from_the_merge_base`
  is re-expressed for the rider: dial at trunk's HEAD, not the lane's tree.
  `test_a_lone_retirement_on_a_held_rung_is_refused_by_row` is kept as D35's
  second witness.
- TC-241's and TC-278's evidence cells are re-pointed in the same commit.

**P9, P10, P12, P13:** prose, acts and review. `tests/test_check_resync.py`
checks the entry's anchor and shape, and the `skills-sync` step checks the
dogfooded copies.

## Risks and open points for the coordinator

- **R1, the move's reach past D28 (settled point 2).** Recommended: the whole
  move, with LLR-249 re-pointed in the one sitting and a reviewed +2 on
  `check_trajectory.py`. The fallback keeps D28's set exact: move only
  `staged_status_moves`, `merge_status_moves`, `pending_status_moves` and
  `held_status_refusal` (31 SLOC, which still fits unit 1).
  - The cost is that IF-196 then spans two modules: its history half stays
    in `acceptance_record` for `check_trajectory`.
  - That needs either a second IF row or IF-196 re-scoped.
  - The plan does not take the fallback on its own; the coordinator rules.
- **R2, the claimed-branch reader's breadth.** Its recorded residual says any
  branch whose name ever appeared under `docs/work/active/` reads as claimed.
  So a marked commit on a re-cut branch of that name passes the narrowed arm
  at the commit. It is still judged if it lands through the slot or a squash.
  It would escape only by landing some other way, which OI-113 (d) leaves to
  review.
- **R3, in-flight lanes.** Once the rider lands, each lane's commits are judged
  at its landing. A coordinator lane that flips a held row, or re-attests one
  under a CLARITY verdict sat before this row (no identity), is refused and
  re-sits. That is the intended effect (D46), and it is worth stating in the
  landing note.
- **R4, the deferred-import window and the smoke budget.** `check ->
  held_status` is a new deferred edge. The window's top (39) may need a
  reasoned re-stamp in P3. The new smoke module adds about 20 fast cases;
  `run.cmd audit` judges the tier against `[smoke-budget]` at phase close.
- **R5, the IF rows at the sitting (settled point 14).** If the coordinator
  wants the IF contract text judged formally, the combined grammar has no
  interface kind. That is a separate ruling, and not this row's.

## Surfaced, not in scope

- `committed_status_moves` reads assumptions both through
  `HELD_STATUS_REGISTRIES` (the whole file) and through `APPROVAL_ACT_CSVS`'
  `DA-ID` and `SUR-ID` tiers. Its contract says "each row once". P8's
  `_spine_status_moves` extraction keeps the history walk's current output
  byte-identical, and does not fix the possible double report. It is a
  candidate successor row.
- `held_status_refusal`'s wording ("the loop may not change a status ...")
  stays as it is for the narrowed arm. A rewording would only be cosmetic.
