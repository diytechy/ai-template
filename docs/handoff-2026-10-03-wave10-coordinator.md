# Handoff 2026-10-03 (wave 10, coordinator): in-lane adjudication works; the queue waits on the owner and WI-788's design

For the next session's **coordinator**. It replaces
[handoff-2026-10-03-wave9-coordinator.md](handoff-2026-10-03-wave9-coordinator.md) as
the resume map.

- **The roles, tools and recipe** of [the wave-8 handoff](handoff-2026-10-03-wave8-coordinator.md)
  still hold, with the corrections below.
- **The tools** are in `C:/Projects/ai-template.wt/coordinator-tools/`.
- **This session's record** is
  [log.d/2026-10-03-wave9-coordinator.md](log.d/2026-10-03-wave9-coordinator.md).

## State at handoff (trunk `refactor_again`, clean, nothing pushed)

- **Landed:**
  - batch R (act 25);
  - WI-784, the two reds the full suite found;
  - WI-688 (acts 26 and 27; TC-211 RECORDED pass);
  - WI-541, closed as done: occupancy 44% on a real adjudication;
  - WI-787 (act 28; codex occupancy from codex's default home);
  - the redundant re-mint rows WI-785, WI-786 and WI-789, closed by citing their
    acts.
- **Approval acts run to seq 28.** The full unfiltered suite last ran at `d040ad75`
  (9.5 min, 2 reds, both fixed by WI-784). It has not been re-run since.
- **The pause is tracked.** It was lifted once for WI-688's claim and restored
  byte-identical.
- **Open:**
  - **WI-788** (strong): session families with reset terms, a glossary, one labelled
    entry point for every model call, per-route provider homes, and new routes
    (SuperGrok, Google's CLI, FreeAI through opencode). Its spec carries the owner's
    direction and rulings on nine design risks. **Half 1 (research and a design
    note) stops for the owner before any build.**
  - **WI-684:** waits on OI-98 (the owner's FileBackup re-sync).
  - **WI-625:** deferred.

## Owed by the owner

- **OI-100:** route amended needs to the existing meaning-or-clarity adjudication,
  and let a CLARITY verdict re-attest on a held rung. Four gaps (0 to 3).
- **The S11 plan's seven questions**:
  [plans/2026-10-03-s11-in-lane-adjudication.md](plans/2026-10-03-s11-in-lane-adjudication.md) §6.
- **The four MEANING-ruled needs:** SN-003, SN-008, SN-025 and SN-043. The adjudicator
  recommends restoring SN-025's exclusions before signing. SN-009 (CLARITY) is held by
  the whole-registry copy until they are signed.
- **The `docs/requirements/hats.toml` header:** it still says the perspective record
  "is not built yet". It is owner text, left untouched.

## The in-lane cycle (owner's S11 direction), as run this session

1. Build on the lane, then have Codex Luna review it.
2. Compose the briefs the merge would mint, in advance:
   `adjudicate_brief.compose(root, row, verdict_path)`, where `row` is the work
   item's registry row with `Brief`, `Adjudicates` and `SR-Refs` overridden (see the
   log for WI-688 and WI-787).
3. Run an independent adjudicator in the lane. A RETURN carries a byte-exact fix,
   with no Dispositions. The builder (resumed) applies it, and the adjudicator
   (resumed) re-judges.
4. The adjudicator takes the act as the lane's last spine commit, naming CLARITY
   rows in `--reattests` too.
5. Land the lane. The sweep then mints a redundant amendment row (the re-mint trap,
   S11 plan §4.2). Confirm no drift and close it citing the act; the owner agreed to
   this.

## Corrections learned this session

- **The `kit-builder` agent type** is available in a new session.
- **Claiming** (`integrate.py claim`):
  - It refuses while `docs/work/pause` exists. A scoped unpause is: a reviewed
    deletion commit, then the claim, then a byte-identical restore.
  - It refuses while hand-written status.md prose names the item.
  - It needs a single-segment branch name (`wi-NNN`, not `build/wi-NNN`).
- **Running a judge through the kit's own path** (`agent_loop --wi`):
  - Pass `--agent-cmd` (the launcher's `AGENT_CMD`).
  - Set `--base` past the lane's build commits. Otherwise their `WI:` trailers make
    the row read as done before the judge runs.
  - ADJUDICATE's tier is pinned by the row's BuildTier, and `--tier-map` is
    ignored. When the build ran outside the loop, nothing excludes the builder's
    family, so pass `--prefer-map ADJUDICATE=<cross-family row at that tier>`.
  - After a successful re-judge the loop re-routes and exits 7 (NEEDS-HUMAN). That
    is expected.
- **Codex Luna as an image judge:** `codex exec -i <png>` per tile, at about 5k
  tokens per tile. Split a 120-tile width by theme.
- **A Deliverable section must precede `## Context`:** the parser clips everything
  after Context.
- **A hand landing sweep:** `intake.py sweep --before <trunk before> --after
  <landing> --branch <lane> --merged "WI-a;WI-b"`.
- **The `.agents` skill mirror:** if the hook reports drift, run
  `bootstrap.py --dest . --sync`.
- **The full suite:** about 9.5 minutes on this box. Run it from a detached
  worktree, with a fixed `--basetemp`, in the background.
- **The `Bash(codex exec *)` allow rule** stays until the queue drains.
