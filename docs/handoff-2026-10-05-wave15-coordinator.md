# Handoff 2026-10-05 (wave 15, coordinator): close out the two active lanes, start nothing new

For the next session's **coordinator**. It replaces
[handoff-2026-10-05-wave14-coordinator.md](handoff-2026-10-05-wave14-coordinator.md)
as the resume map. The wave-13 handoff's "How the program runs" and the wave-11
handoff's roles, tools and "never" list still hold, with the corrections below.
This session's record is
[log.d/2026-10-05-wave15-coordinator.md](log.d/2026-10-05-wave15-coordinator.md).

**The owner's direction for the next session (2026-10-05): close out the two
active lanes, WI-818 and WI-821, and start no new work item.**
- No claim and no scoped unpause.
- No new lane.
- The ready frontier waits for a later session.

The session stopped at about 42% of its context. It was waiting out a Codex plan
limit (Sol and Terra) that resets at 08:48 on 2026-10-05.

## State (trunk `refactor_again` at `2feab680`, nothing pushed)

- **Landed this session:**
  - **WI-822, the coordinator context guard** (act seq 33), squash `8868537c`.
    - The independent adjudicator approved SR-229, SR-230, LLR-300, LLR-301 and
      TC-315 to TC-318, and re-attested LLR-140 and LLR-270.
    - Codex Sol ran four rounds; the last was SOUND.
    - The guard ships dormant at 0; this repo's dial is 50.
  - **WI-806, spine text before the act** (act seq 34), squash `fcf8120b`.
    - The independent adjudicator approved LLR-302 and re-attested LLR-173,
      LLR-245 and TC-173.
    - It accepted the one-commit abandoned-squash residue with no code change,
      and rejected both of Luna's points.
    - Its own text-then-act hook step passed on its own squash landing.
  - **WI-825 and WI-826,** the two re-mints, closed citing acts 33 and 34. In
    both cases the registries equalled their anchors.
- **Filed:**
  - **OI-106 (pending, the owner's),** with its placeholder **WI-827**: SN-029 has
    one untrue clause each in `acceptance` and `why`. The byte-exact text is in
    `docs/reviews/wi-806-text-then-act/dispute-1-ruling.md`.
  - **WI-828:** a hand `git merge` on trunk should judge the commits it brings in,
    as the squash landing does. This is the adjudicator's separate finding.
- **Approval acts run to seq 34.** `docs/work/pause` is tracked and unchanged.
  Watermark: OI 106, WI 828, LLR 304, TC 320, IF 281.
- **The full unfiltered suite at `2feab680`** (detached worktree, fixed basetemp):
  5160 passed, 17 skipped, 0 failed, in 625.3 s.
- **The coordinator lease** is held by this session (`8c1dfc7d-…`). The guard is
  live for claims (`[coordinator] context_guard_pct = 50`).
  - Close-out needs no claim, so the next session needs no lease.
  - Take it with `python project-trajectory/scripts/coordinator_guard.py take
    --transcript <your transcript>` only if a claim is ever needed.
  - If the old holder blocks a take, the owner releases it:
    `coordinator_guard.py release --reason "<why>"`.
  - The tracked `.claude/settings.json` hooks apply to sessions started after
    `8868537c`, so the next session's hooks record its transcript themselves.

## The two lanes to close

Both are claimed and built, and both have open review findings answered in code.
Neither has taken its act. Land them **one at a time**, because acts serialize:
rebase, act, land, then the next lane rebases.

### WI-818, the owner's verdict on a decision (`confirmed` or `overruled`)

The lane is `C:/Projects/ai-template.wt/wi-818`, HEAD `81da4832`. It is **already
rebased onto trunk `2feab680`**.

- **Done so far:**
  - The build, three Sol rounds answered (eight MAJORs and five MINORs, all
    fixed), and Terra's rows through round 3.
  - New rows: LLR-303 and LLR-304, TC-319 and TC-320. Terra minted them as
    LLR-300/301 and TC-315/316; the coordinator renumbered them past other lanes'
    ids.
  - Amended approved rows: SR-225, LLR-283, TC-293 and TC-313. IF-255 and IF-256
    are amended drafts.
  - At the rebase, `acceptance_record.py` reached 1051 SLOC, past the 1000-line
    monolith threshold. It was decomposed, not bumped, to 998 SLOC (D-012):
    - the overrule sync moved to `kitlib/decisions.py`;
    - `git_paths`, `git_show` and `UnreadableBlob` moved to `kitlib/git.py`.
    - Only 2 SLOC of headroom is left.
- **Owed, in order:**
  1. **Terra, row round 4.** The builder's list is
     `C:/Projects/ai-template.wt/review-tmp/wave15/wi818-builder-spine-list-r4.md`:
     LLR-303's `module`, `code_symbol` and `detail` follow the move, IF-256's
     `data` gains the new `overrule_sync_lines(changed, before, after)` call, and
     `git_show`'s tag (`SR-148, SR-225, LLR-303`) needs confirming. Resume Terra
     session `01a10b55-f0df-7ae0-9090-3c54f5cefab5` from the lane.
  2. **Sol round 3, narrow.** Its round-2 review was taken at the pre-rebase
     `5361b3e4`; the rebased review commit is `ee424b3c`. Review
     `git diff ee424b3c..HEAD`: builder round 3 (`23a90c97`), its rows
     (`de638dad`), the decomposition (`81da4832`) and Terra round 4. The
     un-run prompt is
     `review-tmp/wave15/sol-wi818-r3.prompt.md`; regenerate it with
     `BASE=ee424b3c`.
  3. **A fresh independent Opus adjudicator.** Compose two briefs with
     `coordinator-tools/compose_lane.py` from the lane:
     - first approval of LLR-303, LLR-304, TC-319 and TC-320 (SR-225);
     - amendment of SR-225, LLR-283, TC-293 and TC-313.

     The adjudicator also rules the builder's high-risk calls:
     - D-001: the overrule check rides the ruling-sync step;
     - D-004: the citing row must be changed in the same commit, queued or active
       only;
     - D-005: an unreadable record in the commit's tree refuses; an unreadable
       parent counts as having overruled nothing.
  4. **The act** (seq 35), as the lane's last commit, after a rebase if trunk has
     moved.
  5. **Land:**
     - squash; close the row with a Deliverable before Context and
       `specref = ""`, using `spec_move.py`;
     - re-anchor the RESYNC entry (flagged **forced migration**) at the landing's
       parent;
     - archive the tip to `archive/lanes`;
     - run `intake.py sweep --merged WI-818 --branch wi-818 --before <trunk>
       --after <landing>`;
     - close the re-mint citing the act once `cmp` shows the registries equal
       their anchors.
  - The landing commit's hook also needs `gen_components.py` and
    `gen_arch_map.py --cli-doc docs/cli-reference.md` (see the corrections).
  - The lane migrated this repo's `docs/decisions/*.toml` from `reviewed` to
    `owner`. After it lands, every decisions record (the coordinator's
    included) uses `owner = "confirmed"` or `owner = "overruled"`, never
    `reviewed`.

### WI-821, the duplicate-code burn-down

The lane is `C:/Projects/ai-template.wt/wi-821`, HEAD `2e08024e`. It is still on
its cut base `eae1f486`, so it is **not yet rebased** (trunk has taken acts 33 and
34 since).

- **Done so far:**
  - The census falls from 5/5/52 to 2/2/32. What remains is the deliberate
    `human_approves` pair and the CSV pair deferred to WI-817.
  - The commissioning signal reads specrefs as sections.
  - Sol round 1: two MAJORs and one MINOR. MAJOR 1 (duplicate open-item rows)
    and the MINOR (the IF advisory's wording) are fixed in round 2, each
    reproduced red first.
  - Terra's round-1 rows amend LLR-210's detail and the `code_symbol` cells of
    LLR-069, LLR-299, LLR-181, LLR-197, LLR-145, LLR-137 and LLR-124, with TC
    evidence additions. All of these are approved rows.
- **Owed, in order:**
  1. **Rebase onto trunk.** Rebase; never merge-refresh, because its spine rows
     are committed. Take the max per id space in `docs/id-watermark`, keep both
     sides' notes in `stack.ini` and the size ratchet, take trunk's copy of every
     generated view, then regenerate them all.
  2. **Terra, row round 2.** The list is
     `review-tmp/wave15/wi821-builder-spine-list-r2.md`: LLR-133's `code_symbol`
     gains `_cited_cells`, and TC-314 and TC-126 each gain one test. Terra
     session `01a10b69-975e-7173-ad45-1966f2f53526`.
  3. **Sol round 2** over round 2 and the rows.
  4. **A fresh independent Opus adjudicator.** It judges the amendments, MEANING
     or CLARITY: LLR-210's detail, and whether the `code_symbol`-only rows owe an
     act at all (a traced cell owes none, as LLR-298 did at WI-806). It also
     rules **Sol's MAJOR 2, D-001**: the census baseline was re-stamped from a
     stale 0/0/0 up to 2/2/32. The spec says the census reads "0/0/0, or the
     remaining deliberate groups only", re-stamped down, and the CSV pair is
     deferred rather than deliberate. The adjudicator's call is final.
  5. **The act, if any, then land** as above.

## Corrections learned this session

- **Ids collide across unlanded lanes.**
  - A lane mints from trunk's watermark, which knows nothing of another unlanded
    lane's ids.
  - WI-818 minted LLR-300/301 and TC-315/316, which WI-822's lane already held.
  - Brief the spine author with the ids every open lane holds, or renumber in the
    lane before the act. A rebase surfaces it as a registry conflict in the same
    place.
- **A rebase can push a module past the 1000-SLOC monolith threshold.** Two lanes
  each under the threshold can sum past it, as WI-806 and WI-818 did in
  `acceptance_record.py`. Decompose, never bump.
- **Two generated views are checked on trunk but not caught in a lane:**
  `components.derived.toml` and `docs/cli-reference.md`. Regenerate both at every
  landing (`gen_components.py`; `gen_arch_map.py --src project-trajectory/scripts
  --cli-doc docs/cli-reference.md`).
- **The generated-view loop for a rebase:** for each conflict only in generated
  files, run `git checkout --ours` on them and continue, then regenerate once at
  the end. Registries take the union of both sides' rows; the watermark takes the
  max per space.
- **The text-then-act step is live:** a commit that writes the approval record
  while changing spine text is refused. Keep an act commit to Status flips plus
  the snapshot, and commit the verdicts first. The pattern that worked: stash the
  act files, commit the verdicts, pop the stash, then commit the act.
- **The "exits 1 with every hook step passing" quirk** happened twice again on
  trunk landings. Writing the message to a file and committing with `-F` passed
  both times. Read the log before retrying.
- **Codex capacity:** about 22 Codex sessions (Sol and Terra) from about 03:50 to
  05:20 hit the plan limit again; it resets at 08:48. Plan Sol rounds
  narrow, and resume Terra sessions rather than starting new ones.
- **A sandboxed Codex cannot run a shallow-clone test** (git's `sh.exe` fails with
  Win32 error 5). Tell Sol and Terra up front, and run that test outside the
  sandbox.

## Decisions to review (confirm or overrule; high risk first)

- **High risk:**
  - `docs/decisions/wi-806.toml` D-004: the squash exemption needs the tip to
    contain HEAD and the staged registries to equal the tip's. The adjudicator
    accepted the residue (`dispute-1-ruling.md`).
  - `docs/decisions/wi-822.toml` D-001 and D-003 (carried from wave 14), and
    D-014: the store lock is held through launch confirmation.
  - On the lanes, for after they land:
    - `wi-818.toml` D-001, D-004, D-005, D-010, D-011 and D-012;
    - `wi-821.toml` D-001 and D-002.
- **The rest:**
  - `docs/decisions/coordinator-2026-10-05.toml` D-001 to D-005.
  - The remaining lane records of WI-822 and WI-806.
  - The wave-14 list in the previous handoff.

## Unfiled follow-ups (topics, no ids)

- `test_conftest_isolation.py::test_a_module_importing_kitlib_collects_on_its_own`
  takes the child run's last line as its summary (wave 14).
- `acceptance_record._spine_revs` still reads `git diff --name-only` without `-z`;
  safe today, since its paths are fixed and ASCII.
- `kitlib.git.git_out` decodes with `errors="replace"`, so a decisions record with
  a non-UTF-8 name would read as absent (POSIX only, crafted names).
- The ruling sync as one module of its own: the decomposition's larger
  alternative (WI-818 D-012).
- `trunk_step`'s three marker predicates are near-copies (WI-821's builder).
- The guard's relaunch has never run live. Do one supervised relaunch before
  relying on it (WI-822 D-009/D-011).

## Open for the owner (not blocking)

- **Push** `refactor_again` and `archive/lanes`.
- **OI-106** (SN-029), **OI-98** and **OI-105**, and the decisions above.
- **Release the coordinator lease** this session holds, if a later session needs
  to claim.

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator for a CLOSE-OUT session. Read first, in
order: CLAUDE.md; docs/status.md; docs/handoff-2026-10-05-wave15-coordinator.md
(the resume map: the two active lanes, each one's owed steps, and the
corrections); the wave-11 handoff for the roles, the coordinator tools and the
"never" list; your memory index.

The owner's direction: close out the two active lanes, WI-818 and WI-821, and
start NO new work item. No claim, no scoped unpause, no new lane.

Per lane, in the handoff's order: GPT Terra (medium) finishes the rows; Codex
6.1 Sol (high) reviews narrowly; a fresh independent Opus adjudicator
judges the rows and rules the named disputes (its call is final); rebase onto
trunk before the act; the act is the lane's last commit; land by squash,
archive the tip, sweep with --before/--after, read the watermark, and close the
re-mint citing the act. Land WI-818 first, then rebase WI-821 onto the new trunk
and land it. A lane whose review finds new work it cannot close: stop it,
record what is owed in the handoff, and do not start a successor.

Record every call made on the owner's behalf in docs/decisions/<branch>.toml,
high risk first; after WI-818 lands, entries use owner = "confirmed" or
"overruled", never "reviewed". Ask the owner to confirm or overrule, never to
approve. Push and merge to main stay the owner's. Never read OWNER_SCRATCHPAD.md.

At the end (or at 50% context): update docs/status.md (forward-only), write the
next handoff and a log fragment, and run the full unfiltered suite once from a
detached worktree with a fixed --basetemp.
```
