# Handoff 2026-10-05 (wave 16, coordinator): both lanes landed; no lane is open

For the next session's **coordinator**. It replaces
[handoff-2026-10-05-wave15-coordinator.md](handoff-2026-10-05-wave15-coordinator.md)
as the resume map. The wave-13 handoff's "How the program runs" and the wave-11
handoff's roles, tools and "never" list still hold, with the corrections below
and the wave-15 handoff's. This session's record is
[log.d/2026-10-05-wave16-coordinator.md](log.d/2026-10-05-wave16-coordinator.md).

This was a **close-out session** (owner, 2026-10-05): it closed the two active
lanes and started no work item. Nothing was claimed and nothing was unpaused.

## State (trunk `refactor_again`, nothing pushed)

- **Landed this session:**
  - **WI-821, the duplicate-code burn-down** (act seq 35), squash `e81c43d1`.
    - The census fell from 5/5/52 to 2/2/32 and is stamped there.
    - The independent adjudicator **accepted D-001** (the baseline, Sol's
      round-1 MAJOR 2). It returned LLR-210's detail and TC-314's method with
      byte-exact text and one owed test, then re-attested both.
    - Codex Sol ran two rounds; the second was SOUND.
    - The re-mint WI-829 was closed citing act 35.
  - **WI-818, the owner's verdict on a decision** (act seq 36), squash
    `a8458c22`.
    - A decisions entry now carries `owner = "confirmed" | "overruled"`;
      `reviewed` is retired and this repo's records are migrated.
    - An overrule must change open work citing it in the same commit (hook
      and merge slot).
    - A run name carrying `#` or a character git refuses has no record, so a
      citation parses one way. `/` still becomes `-`.
    - Sol ran five rounds; the last was SOUND. Rounds 3 and 4 found
      crafted-name holes.
    - The adjudicator **upheld** Sol's round-4 MAJOR in
      `docs/reviews/wi-818-owner-verdict/dispute-1-ruling.md` and set the fix
      above, and **accepted** D-001, D-004, D-005 and D-014.
    - Over two more sittings it approved LLR-303, LLR-304, TC-319 and TC-320,
      and re-attested SR-225, LLR-283, LLR-284, TC-293, TC-294 and TC-313.
    - The re-mint WI-830 was closed citing act 36.
- **WI-821 landed first**, reversing the wave-15 handoff's order (coordinator
  `docs/decisions/coordinator-2026-10-05.toml` D-006).
- **Filed** (from the WI-818 adjudicator's separate findings):
  - **OI-107 (pending, the owner's)**, with its placeholder **WI-832**: a
    decisions record is named by a lossy, reusable branch name. `a/b` and
    `a-b`, or a reused branch, share one record, and any fix moves record
    paths.
  - **WI-833** (queued, against SR-225): a commit can rewrite an entry's
    disclosure fields under a kept owner verdict. It should be refused against
    the parent.
- **Minted by the WI-818 sweep and left queued:** **WI-831**, a re-judge of
  TC-055. Its declared trigger (CMP-009) fired. It is an observation re-judge,
  not a re-mint. Under the owner's "start nothing new" it was not run;
  WI-823 (TC-055's rubric) is related.
- **Approval acts run to seq 36.** `docs/work/pause` is tracked and unchanged.
  - Watermark: OI 107, WI 833, LLR 304, TC 320, IF 281.
- **The full unfiltered suite** at `07a276e5` (detached worktree, fixed
  basetemp): 1 failed, 5224 passed, 13 skipped, in 614.3 s. The one failure, test_bootstrap.py::test_capped_doc_baselines_match_the_real_sizes, was WI-818's landing stamping the byte-budget-guard skill's own size as 4,491 for a 4,490-byte file; it was re-stamped in the close-out commit and the test passes. A first attempt ran the disk out of space; see the
  corrections.
- **No lane is open.** The worktrees `wi-806`, `wi-818`, `wi-821` and `wi-822`
  remain under `C:/Projects/ai-template.wt/`. Their tips are in
  `archive/lanes`, so they and their branches can be removed; with no other lane
  open, removing them strands nothing.
- **The coordinator lease** is still the wave-15 session's (`8c1dfc7d-…`).
  This session claimed nothing, so it never took the lease. A session that
  claims takes it: `coordinator_guard.py take --transcript <path>`. If the old
  holder blocks the take, the owner releases it.
- **Codex use:** 8 sessions (Sol 4, Terra 4) from about 16:00. No limit was hit.

## The ready frontier (generated; recheck before choosing)

The frontier is WI-798, WI-799, WI-823, WI-828, WI-833 and the re-judge
WI-831. These are held by the owner's open items:

| Item | Holds |
|---|---|
| OI-98 | WI-684 |
| OI-105 | WI-795 |
| OI-106 | WI-827 |
| OI-107 | WI-832 |

The S788-* campaign (status item 1) continues from the frontier by coordinator
session, claiming each batch under one scoped unpause. Starting it is the owner's
call.

## Corrections learned this session

- **Resume a Codex session from the lane directory:**
  `codex exec resume <id> -m <model> -c model_reasoning_effort="medium"
  -c 'windows.sandbox="unelevated"' -c sandbox_mode="workspace-write"
  -c 'sandbox_workspace_write.writable_roots=["C:/Projects/ai-template.wt/review-tmp"]'
  --skip-git-repo-check -o <out> - < <prompt>`. It takes no `-C` or `-s`.
  Terra kept its lane context across rounds 4, 5 and 6 this way.
- **A landing also needs `docs/ratify/CURRENT.md` regenerated.** WI-818's
  landing failed `approval-fresh` until
  `trace.py --approve modified --out docs/ratify/CURRENT.md` ran.
  - The landing's regeneration list is now:
    1. `derive_stage`;
    2. `gen_open_items`;
    3. `gen_trajectory` (twice: plain and `--status`);
    4. `gen_components`;
    5. `gen_arch_map --cli-doc docs/cli-reference.md`;
    6. `gen_arch_map --contracts-doc docs/interface-reference.md --interfaces
       docs/requirements/interfaces.toml`;
    7. that `trace.py` line.
- **Closing a row:** use `spec_move.py <src>
  docs/archive/work/complete/<name>.md`. `--archive` moves the file to
  `docs/archive/specs/`, which is the wrong home for a closed row.
- **Applying a byte-exact cell:**
  - A single-quoted TOML literal cannot carry an apostrophe. Rewrite the whole
    `key = ...` line as a JSON-escaped basic string.
  - Then assert with tomllib that the parsed cell equals the verdict's fenced
    block and that no other cell moved.
- **`git add -A <paths>`** aborts the whole add when one path does not exist,
  and `2>/dev/null` hides it. The hook then fails `staged-divergence`.
  `components.derived.toml` lives at `docs/requirements/`.
- **A third round of crafted-input findings goes to the adjudicator as a named
  dispute,** not into another blind build round. The adjudicator set a fix that
  fails closed and adds no collision. It refuted part of Sol's stated harm, and
  filed the real cause as WI-833.
- **A full-suite basetemp is about 4 GB and is never cleaned up by itself.**
  - Three finished runs (`fullsuite-bt`, `fullsuite-w14`, `w15-full`) left 12 GB
    under `review-tmp`. The disk ran down to 42 MB, and this session's first
    full run broke at 54% with a burst of errors that look like failures.
  - Once a run's result is recorded, delete its basetemp, and the lane
    basetemps too.
  - Check free space before a full run: `(Get-PSDrive C).Free`.
- **A sweep can mint an observation re-judge** (a TC's declared trigger fired)
  beside the expected re-mint. Close only the re-mint; the re-judge is real
  work.

## Decisions to review (confirm or overrule; high risk first)

Every entry now takes `owner = "confirmed"` or `owner = "overruled"`, never
`reviewed` (an overrule needs its `review` note and a citing open work item in
the same commit). 133 entries are not yet seen; open-items.html lists them.

- **High risk:**
  - `docs/decisions/wi-818.toml`:
    - D-001, D-004, D-005 and D-014, all four accepted by the adjudicator;
    - D-013, a run name carrying `#` refuses;
    - D-015, the refusal text lives in kitlib.decisions;
    - D-010, D-011 and D-012.
  - `docs/decisions/wi-821.toml`: D-001 (accepted by the adjudicator) and
    D-002.
  - The wave-15 list: `wi-806.toml` D-004; `wi-822.toml` D-001, D-003 and
    D-014.
- **The rest:**
  - `docs/decisions/coordinator-2026-10-05.toml` D-001 to D-006;
  - the remaining lane records of WI-818, WI-821, WI-822 and WI-806;
  - the earlier waves' lists.

## Unfiled follow-ups (topics, no ids)

- **WI-817 does not own the deferred CSV-reader pair**
  (`check_trajectory.read_rows` / `gen_release_checklist.load_csv`), which now
  sits in the census baseline. It needs one Done-when line on WI-817, or a small
  row after it (WI-821 adjudicator).
- **The consolidation census's spec-of-record half now repeats the pair
  producer's shared-SpecRef signal.** Every shared-spec pair gets two finding
  lines, and dropping the half changes no cluster (a WI-810 candidate; WI-821
  adjudicator).
- **`record_path` can write a filename Windows cannot hold.** Git accepts `"`,
  `<`, `>` and `|` in a branch name (WI-818 builder). It belongs with OI-107.
- Carried from wave 15:
  - the conftest-isolation test reads the child run's last line;
  - `kitlib.git.git_out` still decodes with replacement for its other callers;
  - the ruling sync as one module of its own (WI-818 D-012's larger
    alternative);
  - `trunk_step`'s three near-copy marker predicates;
  - the guard's relaunch has never run live.

## Open for the owner (not blocking)

- **Push** `refactor_again` and `archive/lanes`.
- **Rule** OI-107 (new), OI-106, OI-98 and OI-105, and the decisions above.
- **Choose** the next session's scope: the S788 campaign's next batch, or the
  smaller ready rows.
- **Release** the wave-15 coordinator lease if a later session needs to claim.

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator. Read first, in order: CLAUDE.md;
docs/status.md; docs/handoff-2026-10-05-wave16-coordinator.md (the resume map:
state, the frontier, the corrections, the decisions for the owner); the
wave-15 and wave-11 handoffs for the in-lane cycle, the roles, the coordinator
tools and the "never" list; your memory index.

No lane is open. Work only the scope the owner names for this session. If it
includes claims: take the coordinator lease, claim the batch under ONE scoped
unpause (a reviewed deletion commit, the claims, a byte-identical restore),
then run the in-lane cycle per row: Claude Opus builds (kit-builder, medium);
GPT Terra (medium) authors the rows; Codex 6.1 Sol (high) reviews; a fresh
independent Opus adjudicator judges the rows and rules disputes (its call is
final); rebase onto trunk before the act; the act is the lane's last commit;
land by squash, archive the tip, sweep with --before/--after, and close the
re-mint citing the act. Lanes with acts land one at a time.

Record every call made on the owner's behalf in docs/decisions/<branch>.toml,
high risk first; ask the owner to confirm or overrule, never to approve. Push
and merge to main stay the owner's. Never read OWNER_SCRATCHPAD.md.

At the end (or at 50% context): update docs/status.md (forward-only), write the
next handoff and a log fragment, and run the full unfiltered suite once from a
detached worktree with a fixed --basetemp.
```
