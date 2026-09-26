# Handoff 2026-09-26 (coordinator) — the assumption tier's second build wave, mid-review

For the next session's **coordinator**: an Opus session that coordinates the
build, arbitrates, and spins up builder subagents that build in their own
worktrees and are cross-reviewed by codex Sol. It replaces the
[morning handoff](handoff-2026-09-26.md) as the resume map. That one keeps
its read order, its owner items and its build procedure, and this one
overrides it where they differ.

## Read first, in this order

1. [`CLAUDE.md`](../CLAUDE.md), the `session-protocol` and `spine-authoring`
   skills.
2. The [spine map](plans/2026-09-25-assumption-tier-spine-map.md) §4 and §6
   (D1–D32), and the [builder brief](plans/2026-09-26-assumption-tier-builder-brief.md)
   every builder is handed.
3. This wave's record: [the Sol chain reviews and the arbitration](reviews/2026-09-26-assumption-tier-wave2/ARBITRATION.md)
   (the `sol-*.md` files beside it), and the build log fragment
   `docs/log.d/2026-09-25-assumption-tier-build.md` from "Session resumed
   (2026-09-26)" on.

## Your role and the loop

- **You coordinate and arbitrate** (owner's direction, 2026-09-26). When a
  builder and a Sol review disagree, or you disagree with Sol, rule yourself:
  state the governing row text, then the ruling, and record it in the wave's
  `ARBITRATION.md`. An approved row outranks a Drafted one, and the carrier's
  conventions (an absent key IS an empty cell) bind the rows written under
  them.
- **Builders** are general-purpose subagents, each in its own worktree cut
  from a named commit. Never use the Agent tool's `isolation: "worktree"`: it
  cuts from `main`'s July commit. Hand each builder the brief, its work item,
  its worktree path, its pre-assigned interface ids, and `-n 2`. Run **at most
  four at once**. Eight ran concurrently this session, and the smoke tier
  took 957 s.
- **Sol reviews** run read-only from the tip's worktree, and on Windows need
  the elevated sandbox or every command is "blocked by policy":
  `codex exec -m gpt-5.6-sol -c model_reasoning_effort="medium" -c 'windows.sandbox="elevated"' -s read-only --skip-git-repo-check -o <out> - < <prompt>`.
  Sol cannot run pytest there (no writable temp directory), so the builders'
  red and green runs and your bar are the executed evidence.
  - Review a stack as **one chain**, oldest first, with per-commit verdicts
    and a cross-chain section. The prompts used are reproducible from the
    `sol-*.md` headers.
- **Fixes** go back to the builder as ONE follow-up commit. A session limit
  stops every builder at once, and their worktrees keep the work. A new
  session cannot message this session's builders, so resume one by
  spawning a fresh builder into the SAME worktree. Tell it to read `git log -3`,
  `git status` and `git diff` first, then finish the listed fixes on top of
  the uncommitted partial work.

## State of the wave

Trunk is `refactor_again` at `5c546358`. This session landed the suite fix
`938348c1` and WI-645 `5c546358`. Worktrees are under
`C:/Users/Peter/AppData/Local/Temp/claude/c--Projects-ai-template/baa5ab98-b0ad-4052-bc47-f7e0f47c15bc/scratchpad/wt-NNN`.
Their branches `build/wi-NNN` hold every commit, even if a worktree folder
is lost.

| item | branch commits (oldest first) | review | follow-up state at pause |
|---|---|---|---|
| WI-645 | 4aec3a2a, a03b4187 | NOT YET SOUND → fixed | **landed** as 5c546358 |
| WI-646 | on 4aec3a2a: 0312d591, 91781421 | NOT YET SOUND → fixed (tests only) | **ready to integrate** |
| WI-629 | 5453f920 | NOT YET SOUND: TC-222 to Full + slow module (amendment); `sr_form_findings(srs)`; restrict the missing-copy exception to the assumptions registry | **partial, uncommitted** (a new `tests/test_cell_classes.py` exists) |
| WI-630 | on 5453f920: b501e5f4, d1665f5c | fixed per ruling 3 | **done**; rebase onto WI-629's follow-up (it edited the TC-222 test WI-629 moves) |
| WI-631 | on 5453f920: 378a49e9, c6a43dd9 | c6a43dd9 took Sol's key-presence reading; ruling 6 reverses it | **partial rework, uncommitted**: value-based `_present` restored in the tree; reference-doc wording and tests still to finish |
| WI-632 | on 378a49e9: df8053a9 | blocker: a typed approval-act ledger instead of parsing the README stamp; derive `ROW_REGISTRIES`; validate record filenames; TC-229 stays Smoke (ruling 1). IF-220/221 pre-assigned | **partial, uncommitted** (tests only so far) |
| WI-636 | 26c0419b | 2 blockers, 3 major: ruling 4's ownership rule (+ drafted SR-209, LLR-246, LLR-248 amendments); SN/STK at DevStg-Needs; one tree-bound dial reader; judge merges; the stale `_bookkeeping_commit` text | **partial, uncommitted** (tests written, red run not recorded) |
| WI-637 | on 5453f920: 6defae22 | checker-level regressions for SR-213/SR-214 wiring; the hat metric block | **partial, uncommitted** |
| WI-640 | 890db8d6 | blocker: read TC approvals over the whole history, start gates only the requirement (+ drafted LLR-257 amendment); `PROCESS_ONLY_KEYS` row; PROCESS.md line (byte-budget-guard). Association timing: owner's (below) | **partial, uncommitted** |
| WI-647 | on 26c0419b: 329155cd | plan the relink against HEAD/scratch; drift check after `before_advance` or narrow IF-186; trace the isolation tests from a TC (amendment); narrow the running-scripts exception | **not started**: waits for WI-636's follow-up (it consumes the new dial reader), then rebase |

Each item's full findings are in `sol-chainA.md` (629, 631, 632),
`sol-chainA-630.md`, `sol-chainA-637.md`, `sol-chainB.md` (645, 646),
`sol-chainC.md` (636, 647) and `sol-wi640.md`, as modified by the rulings.

## Integrating

- **Order:**
  1. WI-646.
  2. WI-629, then WI-630, WI-631 and WI-637, then WI-632.
  3. WI-640.
  4. WI-636, then WI-647.
- **Base items squash, stacked items cherry-pick.** A base item that sits
  directly on an old trunk commit squash-merges (`git merge --squash
  build/wi-NNN`). A stacked item is cherry-picked onto trunk (`git
  cherry-pick -n <its own commits>`), so its base's pre-fix commit never rides
  in twice. Or rebase the stacked branch onto its fixed base first and let
  its builder re-run its modules.
- **Expected conflicts:** `RESYNC_PACK.md` (keep all entries, oldest first,
  and re-anchor `[since <sha>]` to the trunk commit before the landing),
  `tests/conftest.py` `SLOW_MODULES`, `tests/test_module_size_ratchet.py`
  (several builders re-stamped `trace.py` from 3425; recompute),
  `docs/requirements/interfaces.toml`, and `docs/id-watermark` (take the
  highest mark).
- **Close each spec:** `## Deliverable` before `## Context`, `specref = ""`,
  then `spec_move.py <spec> docs/archive/work/complete/`. **Write files with
  LF.** Python's text-mode write on Windows emits CRLF, which the spec parser
  refuses (WI-645's first bar). Use `open(p, 'wb')` or `newline='\n'`.
- **Then:** add a log section, run `trunk_step.py --regen`, run the bar
  (the morning handoff's list, plus the slow modules the change touches), and
  commit `WI-NNN: …` with the `WI:` trailer.

## The joint amendment adjudication (owed before any snapshot refresh)

This wave drafts amendments to approved rows, with status left Approved:

| row | cells amended | amended by |
|---|---|---|
| TC-061 | `method` | WI-645 (landed) |
| TC-161 | `method`, `tier` | WI-645 (landed), WI-646 |
| LLR-167 | `detail` | WI-646; draft K adds more |
| TC-222 | `tier` | WI-629 follow-up |
| LLR-257 | `detail` | WI-640 follow-up |
| SR-209 | acceptance | WI-636 follow-up |
| LLR-246, LLR-248 | `detail` | WI-636 follow-up |
| a TC covering the bookkeeping isolation tests | per WI-647's follow-up | WI-647 follow-up |

Draft K also carries LLR-167's two false clauses, and draft H (LLR-140,
LLR-154, TC-144) belongs in the same sitting. Under row-level refusal, any
snapshot act refuses while these stand unnamed. So once the wave lands, one
**independent** adjudicator session (a subagent that did not direct the
amendments) rules them from the amendment brief. It files the verdict, and
one `intake.py snapshot --reattests <ids>` re-anchors them. Do this before
the C1 sitting commit (WI-643).

## After the wave

- **File the drafts** in [plans/2026-09-26-wave2-drafts/](plans/2026-09-26-wave2-drafts/K-llr167-amend.md)
  (A, B, C, E, F, G, H, I, J, K, L, N; ids from `trace.py --bump-ids`).
  Also file the census-routing follow-up (ruling 2).
- **Backlog audit, awaiting the owner's go-ahead:**
  - Cancel WI-596 and WI-597, which WI-635 made obsolete.
  - Rewrite WI-551 as WI-620's keep operation.
  - Merge WI-607 into WI-621, WI-611 into WI-606, and draft H into K.
  - Re-scope WI-539, WI-581 and WI-582 to what remains.
  - Lower WI-541 and WI-551 from P7.
  - Mark WI-644 `spine`.
  - Backfill Done-when on the twelve items that lack one.
  - Widen draft B: `trace.load_registries` 39 → 42, and
    `test_bookkeeping._whole_tree_git_calls`.
- **Then build** WI-633, WI-634 and WI-638, the C1 sitting commit (WI-643),
  and the reversal sweep (WI-644), in the generated frontier's order.
- **Interface ids:**
  - Used so far: 190, 194–201, 208 and 214–217.
  - Held for follow-ups: 220 and 221 (WI-632).
  - Leave the other gaps. Next free: **IF-222**.

## For the owner

- **Still owed:** re-attest SN-041 to SN-044 (D6/D20 first, then D2 and D5),
  and the reserved D8, D14, D22, D29, D30 and D10. D10 is the smoke tier:
  it ran 285–957 s against a 60 s budget this session.
- **SR-217 association timing (ruling 5):** a test case should count as a
  requirement's from the first commit where it reads approved AND names the
  requirement or one of its design rows. Today a test case attached after
  the code landed inherits its earlier approval date. This changes SR-217,
  LLR-257 and TC-250, and sits under SN-042's reserved rule. Decide it with
  D6.
- **SR-211 (WI-637):** every boundary interface with neither `bridged_by`
  nor `coincident` is advised, 43 on this repository, with no "until adopted"
  clause. Sol judged this intended; say if you want the requirement-side
  vacuity instead.
- **The backlog cleanup above**, and the stakeholder-status double report
  (morning handoff).

## Traps (new this session)

- Codex's login was revoked at session start. The owner re-logged in, and
  the old config is kept at `~/.codex.bak-2026-09-26`.
- The full suite needs about 69 minutes at `-n 4` on this 4-core box. Its
  early modules make it look like a 3-hour run.
- `tests/test_derive_stage.py`, `test_phase_rule.py` and
  `test_pre_commit_hook.py` fail to import `kitlib` when an xdist worker
  collects only that module (draft L).
