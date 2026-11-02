# WI-967 implementation plan: each act-ledger entry records the registries its act copied

**Item:** `docs/work/active/wi-967/WI-967-oi-115-ruling-route-wi-963-fix.md`. Spec of record: `docs/specs/WI-967.md`. Planmode: single. SR: SR-178.
**Read in the lane at:** 3f4b989df (wi-967). The trunk ledger holds 163 legacy entries, seq 1..163, none with `copied`.

## What the code does today (the parts this plan changes)

- **Writer.** `baseline_snapshot.copy_live` already builds `copied_rels`: the canonical `SNAPSHOTTED` paths that `_copy_registry` actually wrote. It uses that list to choose the README stamp and to decide whether to append an entry. It then drops the list. `_record_act(base, standing, approved, reattested, verdict)` writes only `seq`, `date`, `approved`, `reattested` and an optional `verdict`.
- **Validators.**
  - `acts_problems(text)` (whole file) checks the fields above and that `seq` increases.
  - `parse_acts` rebuilds every entry from a fixed key list, so any extra key is lost.
  - `acts_findings` puts the problems on trace's integrity floor through `record_findings`.
  - `_standing_acts` refuses an act on a malformed ledger.
  - No rule reads a commit against its parent. Only the readers do that: `_acts_at` here, and `acceptance_record._added_acts`.
- **Consumers.**
  - `acceptance_record._ledger_acts` reads raw TOML dictionaries, so it keeps unknown keys.
  - `kitlib/sitting` reads only `approved`, `reattested` and `verdict`.
  - `gen_open_items` reads through `read_acts`.
  - None of them needs a change to carry `copied`.
- **IF-220** (`docs/requirements/interfaces.toml`): status Drafted. Its `data` cell is about 240 characters, over the 160-character warn limit `trace.IF_DATA_MAX`. Consumers today: `["scripts/acceptance_record"]`.

## Architectural delta (architecture-decomposition skill, steps 1-4)

1. **Mode classes (A2).** No new mode class or transition.
   - The ledger's legacy prefix followed by a recorded suffix is an ordering property of the file's data. The whole-file rule holds it. It is not a runtime mode.
   - No flow in `docs/runtime-flows.md` draws the ledger. Flow 6's `Agent->>Records: take amendment act, then first-approval act` and Flow 4's slot steps keep their transitions.
   - `docs/runtime-flows.md` is therefore not edited.
2. **Value domains (A3, A6).** A value is added to a domain.
   - IF-220's entry gains `copied`. It is either absent (a legacy entry: copy set unknown) or a non-empty, sorted, unique list of repo-relative registry paths.
   - When a commit adds the entry, every path must be a `SNAPSHOTTED` file. The needs file is named by its canonical `.toml` path whichever carrier is live.
   - A reader's copy set gains the value "unknown", which is distinct from the empty set. The empty set never occurs: an act that copies nothing appends no entry.
   - P3 records this on IF-220's row.
3. **Dependencies (A4).** Outputs depend on new inputs. Recorded here; the table has no `Plan-WI` column:

| Output | Depends on | New cell? |
|---|---|---|
| a new entry's `copied` | `copy_live`'s `copied_rels`: the files `_copy_registry` wrote in this act, sorted | yes |
| a new entry's `approved`, `reattested`, `verdict` | the act's named rows and verdict | no |
| `parse_acts` entry dictionary | ledger text; `copied` is present exactly when the entry carries it | yes |
| `acts_problems` verdict | ledger text, plus the shape of `copied` and its order after the first entry that carries it | yes |
| `added_acts_findings` verdict | the index ledger, HEAD's ledger (and MERGE_HEAD's ledger during a merge), `SNAPSHOTTED` | yes |
| acceptance_record, kitlib/sitting, gen_open_items outputs | unchanged; they never read `copied` | no |

4. **A8 descent.**
   - **Requirement descent.** The obligation is a boundary value domain under SR-178. It is recorded on IF-220 (P3) and verified by one new test case (P4). No new LLR is written:
     - the existing LLRs defer the ledger's shape to IF-220 (LLR-278's `_ledger_acts`: "IF-220 is the ledger's shape");
     - the spec names no other row.
   - **Component descent.** Three cuts were compared for the commit-bound rule:
     - (a) In `baseline_snapshot` (CMP-006), the owner of IF-220, `SNAPSHOTTED` and `acts_problems`. **Chosen.**
     - (b) In `acceptance_record`, next to `staged_snapshot_findings`. Rejected: its import edge points away from `baseline_snapshot` (see its `SNAPSHOT_DIR` comment), so it would have to restate the registry universe.
     - (c) As a new `text_then_act.LANE_COMMIT_RIDERS` rider. Rejected: it only adds coverage for hook-bypassed lane commits, which are outside the coverage bound. The landing commit, whether a hand `git merge --squash` or the slot's commit (which "has to pass its own floor"), runs the pre-commit `registry-integrity` step. That step judges every entry the landing adds against trunk.
   - No new component, no partition change, and CMP-006 (`docs/requirements/components.toml`) is unchanged.
   - No new boundary. The git reads go through `check_trajectory._git` and `kitlib.git.staged_heads`. Both sit inside CMP-006: its notes include kitlib's `git.py`.

DELTA: within

The architecture change is carried by rows P1 (the new output field and where its value comes from), P2 (the validators' new input, the parent ledger) and P3 (IF-220's domain, notes and consumers).

## Steps

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P0 | Record D2 as delivered: the scope critique's four dispositions (spec "Critique dispositions"; coordinator-2026-11-01 D-006) and the confirming round's APPROVE (D-007); tick D2 in the claimed row | D2 | no interface (bookkeeping in the claimed row) | |
| P1 | The writer records `copied`; `parse_acts` exposes it only when present; the header and README template name it | D3; SR-178; TC-269 | IF-220; IF-123 | P0 |
| P2 | Validators: whole-file shape rule and order rule in `acts_problems`; the commit-bound rule `added_acts_findings`, added to `record_findings`; `_acts_at` shares the seq comparison | D4; SR-178; TC-278; TC-331 | IF-220 | P1 |
| P3 | IF-220's row and the module's Contract IF-220 docstring: entry shape, legacy reading, commit boundary, coverage bound; consumers set from the grep | D5; SR-178 | IF-220 | P2 |
| P4 | Draft one new test case verifying SR-178 and IF-220, with P1/P2's tests as evidence; mint its id with `trace.py --bump-ids` | D3; D4; SR-178 | IF-220; IF-161 | P2 |
| P5 | One RESYNC entry: what an adopter's ledger gains, and that no existing entry is edited | D6; SR-178 | IF-220 | P3 |
| P6 | First approval of the new test case in the lane (whole-set sitting and act turn, run by the coordinator). Its entry is the first that carries `copied`; check it | D3; D7; SR-178 | IF-220; IF-091 | P4; P5 |
| P7 | Landing: commit bar green; `trace.py --strict` and `check_trajectory.py --strict` clean on the landing tip; regression test cases run; lands alone, before WI-963, which then rebases onto it | D1; D7; SR-178; TC-153; TC-269; TC-271; TC-278; TC-331; TC-398 | IF-220; IF-091 | P6 |

### P0: D2 (bookkeeping)

- The four MAJOR findings of scope critique round 1 (Sol, 2026-11-01) were all adopted. They are written into `docs/specs/WI-967.md`, sections "Trust", "The record", "Architectural delta" and "Critique dispositions", and `planmode = "single"` is set (D-006).
- The confirming round APPROVEd with no findings (D-007, recorded in commit 273510e8e).
- Action: tick D2's box in the claimed row, citing D-006 and D-007.
- D-006 sent the Trust section's shared Ruling to the owner to confirm or overrule, and its `review` cell is still empty. The build follows the Ruling as written. An overrule reopens this plan.
- No test. This is bookkeeping.

### P1: the writer (`project-trajectory/scripts/baseline_snapshot.py`)

**Code changes:**
- **`_record_act`** takes `copied` and writes `("copied", sorted(copied))` after `reattested` and before the optional `verdict`.
- **`copy_live`** passes its existing `copied_rels`. It adds no branch, keeping `copy_live` under the C901 complexity bar.
- **The four act shapes then each name their files:**
  - an approval or re-attestation act names its registry;
  - a traced re-anchor (`--approves REG=ref` with no ids) names REG;
  - a mixed act (`--approves A=ref --reattests <id in B>`) names A and B;
  - a re-seed or first signing names every `SNAPSHOTTED` file that has a live carrier.
- **Unchanged behaviour:**
  - An act that copies nothing still appends no entry.
  - A registry with no live carrier is not written, so it is not named; its stale copies are still removed as today.
- **`parse_acts`** adds `copied` to an entry's dictionary only when the entry carries it, the same pattern as `verdict`. A legacy entry's dictionary stays byte-for-byte what it is today: no `copied` key, never `[]`. No helper infers a copy set. WI-963 adds the first consumer.

**Wording changes:**
- `_ACTS_HEADER` (new ledgers only; existing files keep their header) adds "the registries it copied".
- `project-trajectory/registries/last-approved-README.template.md`, paragraph "Beside them, `acts.toml`...", gains the same words and the legacy reading.
- Keep the strings pinned by `test_the_shipped_README_describes_the_writer_that_exists`.

**Size budget:** `baseline_snapshot.py` measures 890 SLOC against the size ratchet's `THRESHOLD = 1000`. P1 and P2 together must stay under 1000. If they do not, add a reviewed `BASELINE` entry, following the ratchet's convention.

**Tests** (`tests/test_baseline_snapshot.py`, a `SLOW_MODULES` module so it runs in the Full tier). Each drives the real producer through `_snapshot_cli` (`intake.py snapshot`) on `_git_tree` or `_tree`. Each fails before the change because the entry has no `copied`:
- `test_an_approval_act_records_the_registry_it_copied`: a Status flip of a Drafted SR gives `copied == [SR_REL]`.
- `test_a_reattesting_act_records_the_registry_it_copied`: `--reattests <SR>` after an approved-cell amendment gives `copied == [SR_REL]` and `reattested == [sid]`.
- `test_a_traced_reanchor_naming_no_row_records_its_registry`: `--approves interfaces=<ref>` with no ids gives `approved == reattested == []` and `copied == [IF_REL]`.
- `test_a_mixed_approves_and_reattests_act_records_both_registries`: `--approves interfaces=<ref> --reattests <SR>` gives `copied == sorted([IF_REL, SR_REL])`, and the entry still lists only the SR as `reattested`.
- `test_a_reseed_records_every_registry_it_copied`: `--seed` over a standing record gives `copied ==` the sorted `SNAPSHOTTED` files with a live carrier. A registry with no live carrier in the fixture is absent from the list.
- `test_the_needs_file_is_recorded_by_its_canonical_path`: with the needs file on its other carrier, `copied` names `docs/requirements/stakeholder-needs.toml`.
- Extend `test_an_act_that_copies_nothing_adds_no_ledger_entry` to assert that the entry count is unchanged and that no entry has an empty `copied`. This passes before and after; it is a guard.

### P2: the validators (`baseline_snapshot.py`)

**1. Whole-file rule, in `acts_problems` and therefore `parse_acts`, `_standing_acts`, `acts_findings` and `risk_acceptance_act`:**
- A new helper `_copied_problems(where, entry)` refuses a `copied` that is present but is not a non-empty list of strings in sorted order with no repeats.
- The loop refuses any entry that omits `copied` after an earlier entry that carries it.
- Membership in `SNAPSHOTTED` is deliberately not checked here. A later change to the kit's registry universe must not turn committed history malformed. The commit-bound rule checks membership instead (D4's wording).
- Because `_standing_acts` now applies the order rule, the writer refuses to act on a ledger that breaks it.

**2. Commit-bound rule.**
- **Pure core.** `added_acts_problems(text, parent_texts)` reads entries by `seq`. An entry is "added" when its `seq` is in no parent's ledger. That is the same reading as `_acts_at` and `acceptance_record._added_acts`; `_acts_at` is refactored to use the shared comparison `_entries_added`.
- **What it refuses:** an added entry that lacks `copied`, or that names a path outside `SNAPSHOTTED`. A canonical `.toml` name is required, so a `.md` carrier spelling is refused.
- **Remedy in the finding text:** take the act again with the current `intake.py snapshot`; never add `copied` to an entry by hand; never edit an entry that is already committed.
- **When it reports nothing:**
  - If `acts_problems(text)` is non-empty, the core returns `[]` and the whole-file finding speaks instead.
  - If a parent ledger is malformed, the core returns `[]`. No supported route commits a malformed ledger, because the integrity floor refuses it at the commit. A malformed parent is a hand edit, outside the coverage bound. Stated in IF-220's notes.
- **Git side.** `added_acts_findings(root)` reads the index (`:path`) against HEAD, and also against MERGE_HEAD while a merge is in progress (`kitlib.git.staged_heads`, the reading `staged_text_then_act_lines` uses).
  - Before the first commit, nothing is judged, as in every per-commit hook step.
  - Off git, it returns `[]`.
  - It is added to `record_findings(root)`. trace.py's integrity floor therefore reports it, and the pre-commit hook's `registry-integrity` step (`trace.py --strict-integrity`) refuses the commit being made.
  - On a clean tip the index equals HEAD, so the rule is vacuous there. The landing tip is judged by the whole-file rules.
- **Unchanged:** `acceptance_record._ledger_acts` keeps its raw TOML reading, the same as for every other malformation today.

**Tests** (`tests/test_baseline_snapshot.py`):
- **`_BAD_LEDGERS` gains six cases:** "copied not a list", "copied empty", "copied holds a number", "copied unsorted", "copied repeats a path", "an entry omits copied after one that carries it". They run through `test_a_malformed_act_ledger_is_refused_whole`. Each fails before the change, because `acts_problems` returns `[]` for it.
- **`test_a_legacy_entry_parses_unchanged_and_names_no_copy_set`:** `parse_acts(_GOOD_ACT)` equals today's exact dictionary and has no `copied` key. A ledger with a legacy entry followed by a recorded one parses, with `copied` on the second entry only. Fails before: the second entry's `copied` is dropped.
- **`test_a_commit_adding_an_entry_without_copied_is_refused`:** commit a legacy two-entry ledger at HEAD, then stage a third legacy-shaped entry. `added_acts_findings` names its `seq`, and so does `record_findings`. Fails before: the function does not exist.
- **`test_a_commit_adding_an_entry_naming_a_foreign_registry_is_refused`:** a staged added entry with `copied = ["docs/notes.toml"]`, then one with the needs file's `.md` spelling. Both are refused. Fails before: no such rule.
- **`test_legacy_entries_a_commit_does_not_add_are_never_refused`:** the HEAD ledger is legacy and the index changes another file. Result is `[]`. Guard: passes before and after.
- **`test_the_writers_own_entry_passes_both_rules`:** over a committed legacy ledger, an act through `_snapshot_cli`, staged, gives `added_acts_findings == []` and `acts_problems == []`. Fails before: the entry has no `copied`, and the function does not exist.
- **`test_a_merge_counts_no_entry_its_other_parent_holds_as_added`:** MERGE_HEAD's ledger carries a legacy entry that HEAD lacks; the merged index is not refused. Fails before: the function does not exist.
- **`test_readers_carry_copied_without_loss`:**
  - over a two-commit repository, `acceptance_record._added_acts` returns the writer's entry with `copied` intact;
  - `gen_open_items._ledger_entries` lists a legacy entry and a recorded entry, and the legacy entry has no `copied`.
  - Fails before: the writer wrote no `copied`.
- The existing pin `baseline_snapshot.record_findings(` in trace.py (test at line 1451) keeps the trace join covered.

### P3: IF-220 and the module contract (D5)

- **`data`.** Rewrite to 160 characters or fewer, as a schema pointer with no connective. Suggested text: `acts.toml [[act]]: seq, date, approved, reattested, optional verdict; copied = sorted SNAPSHOTTED paths the act wrote, absent on a legacy entry`.
- **`notes`.** Keep the existing text, and add:
  - the full field meanings moved out of `data`;
  - a legacy entry reads as copy set unknown, never empty, and is never inferred or backfilled;
  - an entry added by a commit (by `seq`, against HEAD, and MERGE_HEAD during a merge) must carry `copied` naming only `SNAPSHOTTED` files;
  - in the whole file, no entry may omit `copied` after one that carries it;
  - a malformed parent and a hand-edited ledger are outside the coverage bound (PROCESS.md §6);
  - a copied file is no evidence that its rows were judged.
- **`consumers`.** Set to the result of these two greps, run at build time on the lane tip:
  - `git grep -lE 'acts\.toml|SNAPSHOT_ACTS|baseline_snapshot\.(ACTS|read_acts|parse_acts|acts_problems|acts_findings|record_findings|ActLedgerError)\b' -- project-trajectory/scripts ':!project-trajectory/scripts/baseline_snapshot.py'` (direct readers and the findings consumer);
  - `git grep -lE '_ACT_KINDS|act-ledger entr' -- project-trajectory/scripts ':!project-trajectory/scripts/baseline_snapshot.py'` (entry-field consumers).
  - Today the union is `["scripts/acceptance_record", "scripts/gen_open_items", "scripts/kitlib/sitting", "scripts/trace"]`. That equals the spec's Trust Consumers list without `intake`, which is the producer's route (IF-123), not a consumer. If the grep differs at build time, the row follows the grep, and the difference is recorded in the WI log.
- **Keep:** `owner`, `channel = "file"` and `status = "Drafted"`. No act is owed on a Drafted interface.
- **Version:** `version` "v1" becomes "v2", because the data domain changed.
- **Docstring:** rewrite `baseline_snapshot.py`'s `Contract IF-220:` paragraph and the `ACTS` comment block to match.
- No test of its own. P7's strict lints and the IF data/note advisories read the row.

### P4: the new test case (`docs/test/test-cases.toml`)

- **Id.** Mint with `trace.py --bump-ids` in the same commit. At today's mark of 399 that is TC-400. If WI-987 lands one first, take the next id above trunk's mark when rebasing, following the recipes' watermark rule.
- **Cells:**
  - `verifies = ["SR-178", "IF-220"]`, level Integration, tier "Full" (the evidence is in a `SLOW_MODULES` module);
  - Method: the four act shapes driven through `intake.py snapshot`, the whole-file rules and the commit-bound rules, with both sides of each;
  - Expected: each entry names the files its act copied; a legacy entry parses unchanged with its copy set unknown; an added entry without `copied`, or with a foreign path, is refused; a ledger that omits `copied` after an entry that carries it is refused;
  - evidence: P1's and P2's test node ids;
  - status "Drafted".
- No new LLR (see the delta's step 4).

### P5: RESYNC entry (`project-trajectory/RESYNC_PACK.md` §3)

- Heading: `### Each act-ledger entry names the registries its act copied [since <lane's trunk base sha>]`. Use the "Anchored at the preceding commit" line. Re-anchor at the rebase, as the bar's `check_resync` step requires.
- **What changed:**
  - every new `[[act]]` entry carries `copied`;
  - a traced re-anchor, a mixed act and a re-seed now name every file they copied;
  - the two new `trace.py --strict-integrity` refusals.
- **What to do:**
  - re-sync `scripts/baseline_snapshot.py` and `registries/last-approved-README.template.md`;
  - `copied` appears in your ledger at your next act;
  - no existing entry is edited or backfilled, and you must not add `copied` to existing entries by hand;
  - an act taken by a writer that has not been re-synced, in another clone or lane, must be taken again after the re-sync before it is committed.

### P6: first approval of the new test case (coordinator-run, in the lane)

- Trunk carries no Drafted spine row today: every TC, LLR and SR is Approved. Following the recipes, the coordinator therefore runs a whole-set sitting over the new test case and then the act turn in the lane, before the squash. The build session does not take the act itself.
- **Check:** the act's new entry (seq 164 on today's trunk) must carry `copied = ["docs/test/test-cases.toml"]` and `approved` containing the new test case. The act commit's own hook must pass the new rule. This is the real transition D3 describes, on the kit's own ledger.
- Then run the commit bar in the lane after the act turn, as the recipes require.

### P7: landing

**Pre-landing checks** (on the rebased lane tip, then on the squash):
- Run the commit bar: `[tiers] smoke` from `docs/stack.ini`, which includes both strict lints, `check_docs --stale` and `check_resync`.
- Run the Full tier once over:
  - `tests/test_baseline_snapshot.py`;
  - the evidence modules of TC-153, TC-269, TC-271, TC-278, TC-331 and TC-398, among them `tests/test_snapshot_readers.py`, `tests/test_acceptance_record.py`, `tests/test_accepted_risk.py`, `tests/test_integrate_admission.py`, `tests/test_adjudicate_brief.py`, `tests/test_adjudicate_act.py` and `tests/test_held_status*.py`.
  - These guard every reader of the ledger and the merge floor's use of `_added_acts`.

**Squash rules:**
- The lane lands alone, because it changes the act ledger the cycle runs on. WI-963 rebases onto it afterwards (D1, coordinator-2026-11-01 D-002 and D-004).
- Before the squash, list the worktrees (`git worktree list`) and name in the handoff any lane whose ledger holds entries beyond trunk's. Each such entry must be taken again after that lane rebases, or its landing's hook refuses it.
- At this read, `wi-963` (144 entries) and `wi-987` (163 entries) hold none of their own.

## Risks and the calls the critic should check

- **The commit rule lives on the hook-run integrity floor, not on a slot rider.** This is cut (a) in the delta, and it relies on every landing commit passing its pre-commit floor. A lane commit made with `--no-verify` that adds an entry without `copied` is still judged at the landing commit, against trunk.
- **A malformed parent ledger yields no commit finding.** This is stated as outside the bound. The alternative would make a repair commit impossible to land.
- **Membership is checked only at the commit.** The whole-file rule checks shape and order only, so a future change to the kit's registry universe cannot retroactively break history.
- **The new test case lands Approved through P6.** If the coordinator instead lands it Drafted for an intake mint, P6 shrinks to that call, and D3's live check moves to the next trunk act.

### Critical Files for Implementation
- C:/Projects/ai-template.wt/wi-967/project-trajectory/scripts/baseline_snapshot.py
- C:/Projects/ai-template.wt/wi-967/tests/test_baseline_snapshot.py
- C:/Projects/ai-template.wt/wi-967/docs/requirements/interfaces.toml
- C:/Projects/ai-template.wt/wi-967/docs/test/test-cases.toml
- C:/Projects/ai-template.wt/wi-967/project-trajectory/RESYNC_PACK.md
