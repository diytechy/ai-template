# Handoff 2026-10-04 (wave 12, coordinator): the frontier waits on the owner

For the next session's **coordinator**, and for the owner's review of the unattended
wave-11 session. It replaces
[handoff-2026-10-04-wave11-coordinator.md](handoff-2026-10-04-wave11-coordinator.md)
as the resume map.

- **The roles, tools and recipe** of the wave-11 handoff hold, with the
  corrections below.
- **This session's record** is
  [log.d/2026-10-04-wave11-coordinator.md](log.d/2026-10-04-wave11-coordinator.md).
- **Decisions made on the owner's behalf** are listed below, high risk first, and
  render at the bottom of [open-items.html](open-items.html) under "Decisions to
  review".

## State at handoff (trunk `refactor_again`, nothing pushed)

- **Landed this session** (squash, lane tips in `archive/lanes`):
  - **WI-791** (`9c9e83b7`, OI-100): amended needs, assumptions and surrogates
    reach the meaning-or-clarity adjudication; on a held rung an independent
    adjudicator may re-attest a row it ruled CLARITY, naming its verdict. Act
    seq 29 was taken in the lane after three in-lane fix rounds.
  - **WI-790** (`5be0bc4d`, OI-102): work items cite the open items they wait on
    in `needs`; the owner surface follows the queue and ends with "Decisions to
    review"; the commit-time sync rule refuses a ruling that leaves a citing
    row's Done-when untouched. Act seq 30 was taken in the lane after two in-lane
    rounds.
  - The two re-mint rows the sweeps minted (WI-792, WI-793) were closed by citing
    their acts, as the owner agreed.
- **WI-788 is held at its checkpoint.** Its half-1 design note (four chapters,
  the amend/preserve/retire matrix, a graph of twenty `S788-*` successor rows,
  questions Q-3 to Q-12) is committed on lane `wi-788` at `f5ac7e6b`, NOT on
  trunk; the row stays claimed. It was reviewed by Codex 6.1 Sol (5 BLOCKER,
  7 MAJOR, 3 MINOR, fixed), and an independent Opus adjudicator ruled the three
  disputed points. **OI-104** asks the owner to approve it, and the queued
  placeholder **WI-794** cites it. No successor row is filed.
- **Blocked:** WI-684 on OI-98 (the owner's FileBackup re-sync), WI-794 on
  OI-104. WI-625 is deferred.
- **Approval acts run to seq 30.** `docs/work/pause` is tracked and byte-identical
  to its 2026-09-04 declaration; each of the three claims was a scoped unpause.
- **The full unfiltered suite** ran twice: on WI-790's lane tip `9c39bab2`
  (5030 passed, 17 skipped, 0 failed, 2140.8 s on a loaded box), and on trunk at
  this session's end (@FULLSUITE@).
- **The `Bash(codex exec *)` allow rule** in `.claude/settings.local.json` stays:
  the queue has not drained.

## For the owner, in order

1. **OI-104: WI-788's design note.** Read
   `C:/Projects/ai-template.wt/wi-788/docs/plans/2026-10-04-wi788-design/README.md`
   (the lane's worktree), then the chapter sections each question names. Rule
   Q-3 to Q-12; two are collisions between your own rulings (Q-8: OI-101 Q2
   against OI-103 Q4 for a lane that took an act; Q-11: batched lanes under one
   squash). Ruling OI-104 must update WI-794's Done-when in the same commit (the
   new sync rule refuses it otherwise).
2. **The decisions below**, high risk first. Mark each reviewed with
   `reviewed = true` in its record; WI-788's record is on its lane until the lane
   lands.
3. **The four MEANING-ruled needs** (SN-003, SN-008, SN-025, SN-043): still yours
   to sign; SN-009 (CLARITY) is held with them by gap 3's coupling, which OI-100
   kept.
4. **OI-98**: the FileBackup re-sync, then rule it, updating WI-684's Done-when in
   the same commit.
5. **Standing:** merge-to-main and push stay yours (`push = "human"`).

## Decisions to review (high risk first)

### High risk

- **docs/decisions/wi-790.toml D-001.** The shipped open-items template's live example rows OI-1 and OI-2 are deleted rather than paired with shipped placeholder work items; the status template's example bullets now name the inert OI-000, check_docs S-3 ignores a -000 id, and id-watermark.template keeps OI = 2 (a mark never falls). *Reversal:* Low: restore the two rows from git and add two template work items plus their MAPPING rows.
- **docs/decisions/wi-790.toml D-002.** Bootstrap files OI-3's placeholder WI-001 by running the format's single writer, wi_convert.write_spec_file, as a subprocess in the new repo (the way it already runs trace.py and gen_open_items.py there), and raises the WI watermark to 1. *Reversal:* Low: one function in bootstrap.py.
- **docs/decisions/wi-790.toml D-005.** The merge-slot ruling-sync rung judges every lane (a person's lane too), each commit against its first parent, oldest first, and is chained with the loop-trailer rung in one expression so _merge_refusal stays inside its complexity ceiling. *Reversal:* Low: one call site in integrate._merge_refusal.
- **docs/decisions/wi-790.toml D-017.** The merge-slot form reads a commit's first parent off the commit object (git cat-file commit), not rev^1: no parent line is a true root commit and answers nothing; a parent the repository cannot read is refused by name, telling the operator to fetch it (Sol review 1, MAJOR 1). *Reversal:* One function, acceptance_record.commit_ruling_sync_lines.
- **docs/decisions/wi-791.toml D-003.** Gap 2's 'must name the verdict' is enforced at the merge slot: acceptance_record.held_reattest_refusal (called from merge_approval_refusal on an adjudication lane) refuses each row re-attested on a rung trunk's dial holds unless the act's ledger entry names a verdict file whose '- [CLARITY] <id>' line rules it. The snapshot CLI only records --verdict and refuses a verdict with no --reattests or ... *Reversal:* Remove one call in merge_approval_refusal; the tests releasing the dial in test_snapshot_readers.py's TC-271 fixtures would then be unnecessary but harmless.
- **`docs/decisions/wi-788.toml` (on lane `wi-788`) D-001.** Commits made outside the one entry point (no session log) are attributed to a family by their Co-Authored-By trailer, read from the judged commit itself, for family exclusion (ch.2 section 3 step 2; README Q-10). *Reversal:* Small: one reader in the proposed ask exclusion step; nothing is built yet.
- **`docs/decisions/wi-788.toml` (on lane `wi-788`) D-002.** B2 is changed: MERGE is derived from trunk's tree (each spec the lane tip holds in a terminal folder sits at the same path on trunk), not from git ancestry, because the ruled squash landing (OI-103 Q4) takes the lane tip out of trunk's ancestry; the Lane-Tip trailer is the landing audit's link only, never a state input (ch.1 section 1, change 19). *Reversal:* Low: a derivation rule in a proposed module; the squash ruling stands either way.
- **`docs/decisions/wi-788.toml` (on lane `wi-788`) D-010.** The shipped template retains the adjudicator and the adjudication reviewer at context_reset_pct = 55; this repo stays at 0 (ch.2 section 2). *Reversal:* One template value, but every adopter that re-syncs inherits it.
- **`docs/decisions/wi-788.toml` (on lane `wi-788`) D-016.** The station authority is a fenced lease (out/station/authority.json found through the git common directory; a generation counter; a 120-minute expiry dial renewed per step; a filesystem that cannot lock refuses), and out/integrate.lock folds into it; lane-side claims still take it; every tool ref advance re-checks the generation and swaps the ref inside one critical section; a coordinator's trunk ... *Reversal:* Medium: the authority is the backbone of the adjudication slices.
- **`docs/decisions/wi-788.toml` (on lane `wi-788`) D-022.** Each ask kind has an exact judged scope and exclusion list (ch.2 section 3 step 2's table): authoring sessions are excluded hard, families are ranked preferences recorded when unmet (for author-review the adjudicator's family first, then the builders', per the 2026-10-04 adjudication of dispute 2); B10's exception (the adjudicator's own author ranges, each followed by another session's ... *Reversal:* Medium: the exclusion step of the unbuilt ask, and the act rung.
- **`docs/decisions/wi-788.toml` (on lane `wi-788`) D-027.** Landing is one landing per lane, one ref advance by compare-and-swap; a single-item lane is one squash commit per item; how an act-taking lane and a spine batch land are put to the owner (README Q-8, a conflict between OI-101 Q2 and OI-103 Q4; README Q-11, batches), each with a recommendation, not settled (fix round, Sol BLOCKER 1 and MAJOR 4). *Reversal:* Medium once built: the landing's commit shape.
- **`docs/decisions/wi-788.toml` (on lane `wi-788`) D-031.** A lane built by both families (today's implementer swap, agent_loop.py:618-621) is settled by the one rule the adjudication ruled for dispute 2: for review, judge and adjudicate, authoring sessions are excluded hard and families are ranked preferences (first not the latest authoring range's family, then not an earlier one's), dropped only when the pool cannot meet them; the unmet preference is ... *Reversal:* Medium: the exclusion step and the act rung of unbuilt code.

### The rest, by record

- **docs/decisions/wi-790.toml**
  - D-003: The ruling-sync trigger counts a pending row DELETED from the registry as leaving pending, the same as a status change.
  - D-004: 'Updates the Done-when' is read mechanically as: the row's Done-when section in the new tree is non-empty AND its raw text (outer blank lines trimmed) differs from the parent's. (Rework round 1 reversed the first reading, ...
  - D-006: The one queue projection lives in kitlib/spine.py (open_item_queue) over plain registry rows, with pending.open_item_queue as the views' committed-tree reader; check_trajectory calls the kitlib function directly.
  - D-007: A `needs` token naming no open item reads blocked with reason blocked:open-item-unknown:<id> (still under the dangling-edge ERROR), not waiting.
  - D-008: The Next-work card lists ready rows, then rows an open item holds (each naming the item, linked to its card), then waiting rows, under the existing cap.
  - D-009: The reviewed key is compared trimmed and case-folded; a non-zero float is truthy; the string '0' is falsy beside the number 0; any other type (a list, a table, a date) is unrecognized and reported.
  - D-010: 'Decisions to review' always renders as the last section of open-items.html, saying there is no record when docs/decisions/ is absent; the status snapshot's count line appears only when docs/decisions/ exists.
  - D-011: The status snapshot's open-items bullets name the rows each item holds ('_(holds WI-684)_') and add one 'Uncited' bullet naming any pending item no queued row cites; the Blocked list reads the projection's held map.
  - D-012: The specref state check fails an open row whose specref names the open-items registry when every item it cites is ruled, including a row that cites no item at all.
  - D-013: The ruling-sync pre-commit step answers ok outside a git checkout; inside one, an unreadable diff or tree is a refusal line, never a skip.
  - D-014: A staged merge in progress is judged index-against-HEAD like any commit, with no MERGE_HEAD special case.
  - D-015: gen_open_items.load_open_items is deleted: the queue projection replaced its only caller, and the two tests that used it now read pending.open_item_queue.
  - D-016: An open row whose specref names an open-items anchor must name an item its needs cites; a mismatch (citing OI-5, anchored at OI-6) is an ERROR from open_item_specref_findings (rework round 1, Sol review 1 MAJOR 5; the ...
  - D-018: The sync rule reads the open-items registry in each tree through spine_carrier's carrier resolution (TOML, else CSV), and the specref checks match the registry by its carrier-free stem, so a CSV-carrier adopter is judged like a ...
  - D-019: review_queue ignores non-string members of a malformed high_risk list rather than raising, so the owner page renders every entry and shows record_findings' report of the malformation (Sol review 1, MAJOR 3).
- **docs/decisions/wi-791.toml**
  - D-001: The amendment walk reads a SIBLING constant, acceptance_record.AMENDMENT_CSVS, defined as an alias of APPROVAL_ACT_CSVS (SR, LLR, TC, SN, DA, SUR); SPINE_CSVS keeps its three tiers.
  - D-002: The pre-commit amend-without-flip warn takes the SAME scope as the mint: staged_spine_findings reads staged_spine_amendments, which now walks AMENDMENT_CSVS, so an approved need, assumption or surrogate amended without a ...
  - D-004: The audit listing lives at the end of open-items.html section 2 (Approval & re-attestation), rendered by gen_open_items.verdict_reattest_block from the act ledger: every entry naming a verdict, newest first, with 'None recorded.' ...
  - D-005: The amendment brief renders the new tiers: adjudicate_brief._unchained_amended_rows reads baseline_snapshot.tier_owing (needs_owing generalised) for SN/DA/SUR rows in scope, and _aftermath derives each held-rung verdict's arm ...
  - D-006: adjudication_action gains a verdict parameter with three arms: loop-held -> 'flip'; human-held with CLARITY -> 'reattest'; human-held otherwise -> 'recommend'. flip_verified and the 'adjudicate' CLI pass no verdict and are ...
  - D-007: Two ratchets re-stamped with reasons rather than decomposed: intake.py's size baseline 1658 -> 1672 (the --verdict flag, the held arm's CLARITY case, the Context wording) and test_import_layers' deferred-import window 30 -> 31 ...
  - D-008: Sol review 1 MAJOR 1 confirmed and fixed at the root: merge_approval_refusal takes a REQUIRED keyword `trunk`, the commit the merge lands on, and held_reattest_refusal reads the dial there. integrate._approval_act_refusal passes ...
  - D-009: Sol review 1 MINOR 1 confirmed and fixed where the path is recorded: baseline_snapshot.verdict_rel spells --verdict repo-relative with forward slashes and no './' (an absolute path under the root is made relative); copy_live and ...
  - D-010: Sol review 1 MINOR 2: ENFORCE SR-228's first-draft condition rather than change the SR. Under the held-rung allowance, a re-attested row that is below approval or absent at the act's head is refused at merge ('below approval (or ...
- **`docs/decisions/wi-788.toml` (on lane `wi-788`)**
  - D-003: No DONE state: ARCHIVE plus a closed flag (ch.1).
  - D-004: Session decisions keep their own commits and are admitted after the fact by the existing range rules (S9, S11 section 4.7), rather than routed through the provider's decide (ch.1).
  - D-005: The provider is two modules: pure enums and state_of in kitlib/station.py, effects in scripts/lane_state.py, which also hosts the station authority (ch.1; integrator).
  - D-006: Liveness comes from the dispatcher's process handles, otherwise from a lock probe, never from the pid written in a lock file (ch.1).
  - D-007: out/review-owed retires in the provider slice; the unguarded-lock fallback (D12 of the dual-path census) retires for the per-worktree lock too; the manual-worker base fallback (D16) stays justified until hand sittings run on ask ...
  - D-008: Dual-plan round directories are named by work item (docs/plans/<WI>/round-<n>/), retiring the DP id allocator (ch.3).
  - D-009: On-demand replanning fires at the second consecutive CHANGES-REQUESTED, folded into the family swap; the OI-103 Q5 dial skips on-demand replans and decomposition children; a child's tier is the plan's Tier column, else the ...
  - D-011: The rejudge brief moves to the [judge] family; all five adjudication briefs are retained, so retain_for retires (ch.2 section 2).
  - D-012: The usage ledger U1 is docs/usage-ledger.csv, appended at the final regeneration inside the station authority, and replaces docs/iteration_index.md (no caller since 2026-09-06) (ch.2 section 6).
  - D-013: Retained slots are keyed by family and scope, not by route (a slot records its route@account; only cooldowns are keyed by it); the lease wait is 1,200 s for every retained slot, and it is never waited while holding the station ...
  - D-014: No route row for OpenCode's own free models. The decisions note goes to every kind except those whose range S9 mechanically confines to the verdict file: S9 reads REVIEW-A/B today (kitlib/verdict.py:189, :944), and S788-ask ...
  - D-015: REFRESH inside the lock runs the commit-tier bar; the full declared bar runs once, on the final tree (ch.4).
  - D-017: Spine-text rounds stay inside the sitting (the adjudicator drafts, the adjudication reviewer edits); a code finding goes back to the builder as a return (ch.4 section 7).
  - D-018: The decisions-record gap is accepted as history: since 2026-09-28, 75 closes owed a record and 2 carry one; none is backfilled (ch.4 section 6).
  - D-019: A return moves the specs back to active/<branch>/ in the sitting's commit, and the landing refuses a lane whose folders disagree with its recorded merge action; S788-dual-pickup is ordered after S788-mint; S788-glossary is a ...
  - D-020: The glossary's text is carried in the note's README, and the kit-shipped project-trajectory/GLOSSARY.md file is built by the first successor row (S788-glossary), not in half 1 (coordinator).
  - D-021: The claude and codex resume-by-id probes (a few cents, local) were run alongside the authorized OpenCode live probes, under the owner's 2026-10-04 session authorization (coordinator).
  - D-023: A dual-plan PAGE closes the parent partial and, at MINT, mints the open item and a successor decomposition row that carries the parent's round evidence and needs the open item; the owner's ruling becomes the successor's Done-when ...
  - D-024: At the fourth sitting, a lane that owes a return ends merge-partial: with a green bar its work lands partial and the minted successor carries each upheld finding; with a red bar caused by its own work the keep set is empty (the ...
  - D-025: Cancellation stops the sitting's process, harvests its usage, bumps the generation and leaves the lane PARKED for today's reconcile note (no discard); F1 (a killed refresh aborts its own merge) and F2 (ARCHIVE ordered and re-run ...
  - D-026: The successor graph is made dependency-complete without a cycle: S788-station-authority no longer requires every tool writer to pass the landing; the writer census moves to the last writer move, S788-dual-pickup; ...
  - D-028: U1 attributes usage per invocation: each adapter declares call or thread scope; thread-scope rows are end minus a stored baseline; kill recovery counts only entries after a cursor stored at launch (ch.2 section 6, fix round, Sol ...
  - D-029: Provider contracts are fixed from documentation (ch.2 section 5's table), with each remaining live check named with its row: a FreeLLMAPI row ships only for a pinned id with a declared one-model chain, else none; Gemini's adapter ...
  - D-030: Owner questions trimmed with stable ids: Q-1 becomes a forced-migration notice (the retirement is already directed), Q-2 is decided (homes in the user config directory), Q-3 keeps only the spend authorizations (its Gemini option ...
- **docs/decisions/coordinator-2026-10-04.toml**
  - D-001: Each scoped unpause's deletion commit counts as 'reviewed' when it passes the commit bar and cites the owner's written session authorization of 2026-10-04; no separate review session is drawn for the one-file deletion.
  - D-002: When the first pause-deletion commit was refused by the hook but integrate.py claim still claimed WI-791 (it reads the working tree's pause file, which the staged deletion had removed), the coordinator reset its own unpushed ...
  - D-003: The WI-788 lane is kept open (claimed, its design note committed on the lane, not landed) at the owner checkpoint; the checkpoint item holds the row and the owner reads the note on lane wi-788.
  - D-004: WI-788's checkpoint is filed as pending OI-104 plus a queued placeholder row WI-794 citing it in needs (WI-790's rule, live since its landing), rather than an OI with wi_refs; WI-788 itself stays claimed on its lane and does not ...
  - D-005: The full unfiltered suite was run twice: once on WI-790's lane tip before its adjudication (to catch slow-tier reds while rounds remained), and once on trunk at the session's end.

## Corrections learned this session

- **`integrate.py claim` reads the pause file in the working tree, not in HEAD.** A
  staged deletion whose commit the hook refused still let a claim through. Commit
  the deletion first and check that HEAD moved before claiming (the scratch
  `scoped_claim.sh` recipe does).
- **GPT Terra's `apply_patch` fails on the registries' long single-line cells**
  ("Failed to find expected lines") and it then gives up silently. Tell it up front
  to edit with a guarded Python replace (read with `newline=""`, assert each old
  value occurs once, write with `newline=""`), and to check with tomllib that list
  cells stay lists: one of its scripted edits turned IF-073's `consumers` list into
  a string, which the smoke tier caught.
- **Resume a Terra session** with `codex exec resume <session id> -m gpt-5.6-terra
  -c model_reasoning_effort="medium" -c 'windows.sandbox="unelevated"'
  -c 'sandbox_mode="workspace-write"'
  -c 'sandbox_workspace_write.writable_roots=["C:/Projects/ai-template.wt/review-tmp"]'
  --skip-git-repo-check -o <out> - < <prompt>`, run from the lane directory
  (`resume` takes no `-s` or `-C`). The id is in the first run's log
  (`session id:`).
- **Sandboxed pytest in a codex session** hits Windows locks on a shared basetemp
  with `-n 2`; ask for `-n 0`, and run the decisive tests yourself.
- **A builder that restamps a skill** may miss the `.agents` mirror; the hook's
  `skills-sync` step catches it; `bootstrap.py --dest . --sync` fixes it.
- **A complexity row that went down** is deleted from `docs/complexity-baseline`,
  which is TAB-separated; match on the tab, not on `::`.
- **`git commit -F /dev/stdin`** fails in this Git for Windows; write the message to
  a file.
- **Removals are still unrouted**: a lane that retires a row must carry it into its
  in-lane amendment scope by hand, and the act names it in `--reattests`.
- **The adjudicator's in-lane rounds work as designed**, and they are where the
  real defects surfaced: in both lanes the authored rows dropped clauses the code
  still keeps, replaced lists of cases with "the existing cases hold", or claimed
  tests that did not exist. Mutation probes on a scratch export found them.

## New coordinator tools (outside the repo, `C:/Projects/ai-template.wt/coordinator-tools/`)

- `sol_review.sh <lane> <prompt> <out> [effort]`: a Codex 6.1 Sol review through the
  `codex` on PATH; `sol-review-prompt.template.md` is its brief (fill with
  `mkprompt.py`).
- `terra_author.sh <lane> <prompt> <out> [effort]`: a GPT Terra spine-authoring
  session that edits the lane; `terra-spine-prompt.template.md` is its brief.
- `preview_mint.py <before> [<after>]` (run from the lane root): what the merge would
  mint, through the kit's own draft builders.
- `compose_lane.py WI-NNN <brief> "<ids>" "<srs>" <verdict> <out>` (from the lane
  root): an in-lane adjudication brief, the lane's row with `Brief`, `Adjudicates`
  and `SR-Refs` overridden.

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator. Read first, in order: CLAUDE.md;
docs/status.md; docs/handoff-2026-10-04-wave12-coordinator.md (the resume map,
the corrections and the decisions the owner reviewed); the wave-11 handoff for
the roles, tools and in-lane cycle; your memory index.

If the owner has ruled OI-104:
- apply its ruling in the same commit that records it (the sync rule refuses a
  ruling that leaves WI-794's Done-when untouched);
- amend the WI-788 note on its lane as the ruling directs, refresh the lane, land
  it by squash, archive its tip, sweep, and close WI-788 on the approved note;
- file the approved S788-* successor rows on trunk in the note's graph order,
  each with its Done-when, review bar and RESYNC flag;
- then build them in that order with the wave-11 cycle (Opus builder, Terra spine
  rows, Codex 6.1 Sol review, in-lane Opus adjudication, squash landing).

If it has not, stop: no row on the frontier moves without the owner.

The roles, the commit bar and the "never" list of the wave-11 handoff hold.
```
