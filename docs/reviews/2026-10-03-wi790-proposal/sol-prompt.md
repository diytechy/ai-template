# Review brief: WI-790 proposal (read-only; do not modify any file)

You are an independent reviewer for the ai-template repo (cwd). Do NOT read, cite or act on `OWNER_SCRATCHPAD.md`. Do not edit, create or delete any file.

## Artifact under review

`docs/work/queued/WI-790-wi-cites-the-oi-it-waits-on.md` (queued work item, filed 2026-10-03 at HEAD 83abd4d2). It records the owner's words across three passes, the coordinator's readings, a confirmed Design (points 1-8) and a Done-when. It reverses part of WI-746 (`docs/archive/work/complete/WI-746-let-a-work-item-wait-on-an-o.md`, landed 9dbb5103): open items stop carrying `wi_refs`; work items cite open items as `OI-###` tokens in `needs`; `open-items.html` shows a pending open item only when a queued work item cites it; every minted open item has a placeholder row; a ruled open item forces its citing rows' Done-when to change (an ERROR, owner's third pass).

Owner standing rules you must apply: fix a single point of failure rather than add fallback / degenerate / legacy code paths; a RESYNC entry is the migration (no transition reader); judgements and reviews are independent; the kit's scripts are stdlib-only and cross-platform (Windows + POSIX, Python 3.11+); templates stay copy-ready for adopters; keep this repo and the shipped template structurally in sync.

## What to do

1. **Soundness of the design against the code.** For each design point, check it against the code it changes and say whether it is buildable as written, with file:line evidence. Key code: `project-trajectory/scripts/schedule.py` (hard_preds_satisfied, dispositions waiting/blocked), `kitlib/spine.py` split_pred_edges, `intake.py` (_inject_open_item, _mint_open_item, _DRAFT_KEYS, dispositions), `gen_open_items.py`, `traj_status.py`, `rendering/traj_panels.py`, `check_trajectory.py` (backlog_staleness_findings, wi_refs checks, R-rules, exit-code handling, `--strict`), `kitlib/registry.py` (done_when_section, spec body parsing), `integrate.py` claim, `prompts/adjudicate-disposition.template.md`, `project-trajectory/registries/open-items.template.toml`, `docs/requirements/open-items.toml`.
2. **The sync ERROR (design 6, third pass).** Is "Done-when differs between the transition commit's parent and the tree under check" well-defined and robust? Consider: CI checkout depth (`.github/workflows/test.yml`) and shallow clones; the ruling uncommitted in the working tree (pre-commit hook runs); rows created AFTER the transition (a placeholder minted citing an already-ruled item); an item ruled then re-opened; renamed spec files (title edits; `--follow` blind spot noted in backlog_staleness_findings); lanes/worktrees and the merge slot composing trees; a row whose Done-when lives after `## Context` (the body parser clips Context; does `done_when_section` read the raw file?); bootstrap/scaffold repos with no history; adopters' repos. Does it introduce a degraded second path anywhere? Propose the tightest definition that stays mechanical, or a better mechanization meeting the owner's intent ("If an open item transitions ... to closed ... the work item must also be modified and its Done When and other applicable fields must be updated").
3. **The surface rule (design 4) and the uncited-pending finding.** Gaps: draft/deferred citing rows, pending items with no work (e.g. OI-98 is a gate on a person's act; OI-100), ruled-row history, the status snapshot. Does hiding an uncited pending item plus making it an error leave any state where the owner cannot see a decision they owe?
4. **Placeholder rows (design 5).** Verify a row holding only title, safety_class, `needs = ["OI-###"]`, specref = open-items registry is valid under every check and the claim path, and that it is blocked. Is pointing specref at the registry sound (R-E, staleness per-file clock)?
5. **Spine and migration completeness.** Are the named rows (IF-073, IF-074, IF-054, IF-176, LLR-058, LLR-288, LLR-289, TC-253, TC-301, TC-302, WI-205's rows) the full set to amend? Find others that pin `wi_refs`, `waiting:open-item-pending`, or the disposition brief's open-item clause (grep docs/requirements, docs/test, tests/). Is the migration (OI-98, OI-101 -> needs; OI-100 placeholder; ruled rows keep wi_refs as history) complete, and does keeping historical `wi_refs` keep any reader alive?
6. **Contradictions** inside the spec (between passes, design and Done-when) and with standing rulings (WI-746, IF-073 wording, S13 claim Done-when warning, R-A Deliverable rule, OI-45 "no script approves").
7. **Unasked owner questions** that the build would otherwise have to guess.

## Output (final message)

- `VERDICT:` SOUND / SOUND-WITH-FIXES / NOT-SOUND.
- `FINDINGS:` numbered, most severe first; each: claim, evidence (file:line), consequence, proposed fix (byte-level spec wording where useful).
- `OWNER QUESTIONS:` only decisions the owner must make, each with options and a recommendation.
- `MISSING ROWS / FILES:` for the amendment list.
Be concrete and terse. Findings are claims: back each with evidence.
