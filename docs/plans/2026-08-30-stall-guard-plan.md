# stall-guard — the loop stops handing finished work back when a REVIEWER is unavailable

**Status:** plan only. Nothing in `C:\Projects\ai-template` was modified writing this.
**Written:** 2026-08-30, by the supervising session of the delegated unattended run, at the
owner's request. **Read at:** `ai-template` branch `contract_split`, trunk `1aa4b98c` and the
lanes of that run. Every claim below was observed live that day; the record is
`docs/decisions-for-review-2026-08-31.md` (decisions 14, 17, 21, 23, 29, 30) and the run logs
kept in the session scratchpad.

**Owner direction (2026-08-30, in session):** *"If both openai and opencode are unavailable, I
would expect the fallback to be an independent opus reviewer, not a partial WI."* And: the
next session runs these changes FIRST, before any further row is claimed (the tracked
`docs/work/pause` armed 2026-08-30 holds the frontier until they land).

---

## 0. The incident, in one paragraph

`WI-521` (the decomposition debt owner) built a clean slice in 33 minutes (`56e7e52b..adfc1204`).
Its REVIEW-A draw then failed three times in a row for reasons that had nothing to do with the
work: OPENAI-TERRA returned a usage-limit ERROR in 3 s; the re-route to OPENCODE-GROK ran the
cited tests and `trace.py`, then went silent until the 7200 s session timeout; OPENAI-TERRA
errored again. Three consecutive non-committing sessions is `--stall-limit`, the worker exited 4
(`EXIT_STALL`), `dispatch._worker_close` read exit 4 as a DECIDED outcome (`_WORKER_OUTCOMES`)
and closed the lane `partial`: the work merged unreviewed, the standing debt-owner row went
terminal, a disposition row (`WI-542`) had to be adjudicated (two Opus sessions) and reviewed
(one round) to draft the successor (`WI-545`), and the module-size ratchet's pointer now names
a closed row. Wall-clock lost to that one outage: ~4 hours. `WI-537` came within one failed
draw of the same close later the same day.

## 1. Where the defects live (read, not guessed)

| # | Defect | Where | Evidence |
|---|---|---|---|
| D1 | One stall counter for every session kind. A reviewer that never answered is booked as the builder not building. | `agent_loop.RoutingState.note_session` (`self.stall = 0 if committed else self.stall + 1`), `stall_verdict(limit)`; `after_session` calls `note_session(committed, outcome == "ERROR")` for BUILD and REVIEW alike | run-3 log: `session 002 ERROR (3 s)`, `session 003 TIMEOUT (7200 s)`, `session 004 ERROR` → `coordinator stopping: STALL` → `partial: WI-521 -> partial/ (worker exit 4)` |
| D2 | `EXIT_STALL` is a *decided* worker outcome, so the dispatcher closes the lane `partial` — finished, approved-or-not work is handed back. | `dispatch._WORKER_OUTCOMES` (contains `ac.EXIT_STALL`), `_worker_close` → `handback.close_partial` | `docs/handbacks/WI-521-wi521-decomposition-debt-owner.md`: `reason = "worker exit 4"`, `keep_commits = []`, `split_decided_by = "adjudicator"` |
| D3 | Liveness is a wall-clock guess. `run_session` has ONE deadline (`timeout`, 7200 s from the launcher) and no idle deadline: a child that stops emitting is discovered two hours later. | `agent_session.run_session(argv, root, timeout, …)` — reader thread pumps lines, the only kill is `timeout` | grok's transcript: last tool output at ~20 min, `coordinator: session timed out after 7200s` |
| D4 | No pre-dispatch probe. A limited/unreachable route is discovered by burning a session (240 s for codex's limit message), then cooled. | `route_session` → `session_bookkeeping` → `reroute_rate_limited` / `build_bookkeeping` `st.cool(...)` — all AFTER the session | run-9 log: `session 010 ERROR wall=240s` |
| D5 | The reviewer fallback ladder ends in nothing. Heterogeneity excludes the builder's family; when every other family is cooled/limited the draw has no candidate, and the stall guard becomes the fallback by accident. | `agent_loop` route selection for `is_review` (`exclude.add(fam)` — line ~1001) over `docs/agents-enabled` order; no same-family rung | the owner's expectation above; three families enabled today, two of them non-Anthropic |
| D6 | (adjacent, same cost class) `EXIT_STALL` also fires when a lane's work is DONE but its spec was never moved: the resumed worker finds nothing to do, three no-op sessions → partial close. | `dispatch._parked_branches` resumes any branch with specs still in `active/`; the shipped `worker.template.md` carries no close step; the adjudication brief forbids the move | `WI-542`/`WI-544` resumed in a cycle; `WI-537` exited DONE with its spec in `active/` (decisions 21, 24, 29) |

Non-defects, stated so nobody "fixes" them: `--wait-on-limit` DOES cover a usage limit when the
loop itself parses a reset time (`WAITING` never counts toward the stall); the re-route on ERROR
is correct; the heterogeneity rule is correct as the FIRST preference.

## 2. The changes — five, each small, each with a test

### C1. Route-aware stall accounting (`agent_loop.RoutingState`)
- Split the streak: `build_stall` (BUILD/DESIGN-CHECK/ADJUDICATE sessions that end without a
  commit) and `review_draw_failures` (REVIEW/CRITIQUE sessions that end ERROR/TIMEOUT/no verdict).
- `stall_verdict(limit)` reads `build_stall` only. A committed verdict resets `review_draw_failures`.
- `after_session` passes the phase kind (`plan["is_review"]`/`is_critique`) into `note_session`.
- Test: a BUILD commit followed by three review ERRORs yields `stall_verdict == None`; three BUILD
  no-commits still yields `"stall"`.
- Ratchet: `agent_loop.py` is baselined by `tests/test_module_size_ratchet.py`; net +10–20 lines is
  a reviewed re-stamp with the reason on the entry (the 2026-08-30 precedent: `intake.py`).

### C2. "Review owed" is a parked state, not a handback (`agent_loop` + `dispatch`)
- New worker end state: build committed, verdict absent after the review ladder is exhausted →
  exit with a distinct code (proposal: `EXIT_REVIEW_OWED`, next free value in `agent_common`),
  banner `REVIEW OWED — <n> draws failed on <families>; lane parked with its work`.
- `dispatch._WORKER_OUTCOMES` does NOT include it (so the lane stays parked and resumable, like a
  crash), and the drain does not merge it (no verdict). The next tick resumes the lane; the
  resumed worker's endstate sees a committed build with an open review and schedules the
  review round directly (today `worker_endstate` cannot express "built, review owed" across a
  restart because `review_queue` is in-process — persist the owed state as a `Review-Owed:`
  trailer on the last telemetry commit, or a lane-local marker under `out/`, read at resume).
- `EXIT_STALL` stays a decided outcome for a REAL build stall (C1 makes that the only way to reach it).
- Test: drive a lane whose build commits and whose three review draws ERROR; assert the lane is
  parked (specs still in `active/`, branch ref present, no `docs/handbacks/` report) and that the
  next cycle schedules REVIEW-A rather than BUILD.

### C3. Idle deadline in `agent_session.run_session`
- Add `idle_timeout` (default 900 s, launcher/env slot `AGENT_SESSION_IDLE_TIMEOUT`): the reader
  thread stamps the last-line time; the waiter kills the process group when `now - last > idle`
  and returns outcome `TIMEOUT` with `idle=True` in the telemetry header (`# timeout: idle`).
- Keep `timeout` (wall) as the outer bound. Both are per session.
- Test: a fake CLI that prints one line then sleeps → killed at the idle deadline, not the wall.
- Ratchet: `agent_session.py` — re-stamp with reason.

### C4. Pre-dispatch liveness probe per route (`agent_route` + `agent_loop.route_session`)
- Before launching a session on a route that has been cooled OR whose family produced an
  ERROR/TIMEOUT earlier in this run, run the row's `cmd_template` with a 30 s wall on the fixed
  prompt `Reply with the single word OK`. A non-`OK` answer cools the route immediately with the
  reason (`limit` if the usage-limit regex matches, `unreachable` otherwise) and the draw moves
  on — no session, no telemetry row, one console line `probe [ROUTE]: <reason>, cooled <s>`.
- Never probe a route with a clean history this run (the probe is a recovery aid, not a tax).
- Test: a fake route whose probe answers with the codex limit text is skipped; a route answering
  `OK` is launched.

### C5. The same-family fallback rung for reviewers (`agent_loop` review draw)
- Ladder: (1) cross-family candidates in enable-list order; (2) when none remains (all cooled /
  limited / errored this round), draw the strong ANTHROPIC row (`ANTHROPIC-OPUS-STRONG` today)
  with `heterogeneity = "relaxed"` recorded in the verdict filename suffix and the scoreboard
  round line (`round N verdict=… tier=… heterogeneity=relaxed`), and a `# heterogeneity: relaxed`
  telemetry header so the record shows which verdicts were same-family.
- An APPROVE from a relaxed round satisfies the merge slot exactly like any other (the rung asks
  for a recorded fresh-context verdict; family is policy, not gate).
- Test: with OPENAI and OPENCODE cooled, the review draw selects the Anthropic strong row and
  the verdict path carries the relaxed marker.

### C6 (adjacent, do in the same slice — it is the other half of D6)
- `worker.template.md`: state the close ritual — `## Deliverable` before `## Context`, `specref`
  cleared, `spec_move.py` to the terminal folder, the fragment opening `## <date> — …`, and
  `trace.py --approve modified --out docs/ratify/CURRENT.md` when the lane minted spine rows.
- `adjudicate-disposition.template.md`: the draft goes in THIS spec's `## Dispositions` as
  top-level keys (no table header), title ≤ 120; and either the adjudicator makes the terminal
  move itself or `dispatch` closes an adjudication lane whose verdict commit carries the `WI:`
  trailer. The dispatcher path is cleaner (one closer for all adjudication lanes).
- `integrate.unload`: shed the loop's OWN `out/run-logs/` streams (it wrote them; their clipped
  copies are tracked under `docs/iteration/`) so a merged lane unloads and the run continues.

## 3. Sequencing for the next session

1. Land C1 + C2 + C3 + C4 + C5 as ONE row (`WI-547`, strong, ordinary — the loop's own engine;
   `safety_class` ordinary, no spine row minted) built BY HAND on a claim branch the session
   opens through `integrate.py claim`, reviewed once cross-family, WI-level verdict compiled as
   this run did (decision 7), merged through the slot. Do not let the loop build the loop.
2. Land C6 as a second row (`WI-548`, medium) the same way — or fold into 1 if the first review
   round is clean.
3. Delete `docs/work/pause` in a reviewed commit; relaunch `agent-resume`; the frontier resumes
   at `WI-546`'s successor state and `WI-545`/`WI-538`/`WI-535`/`WI-536`.

## 4. What to measure afterwards (the acceptance)
- Replay of run 3's shape (BUILD commit, three review ERRORs) ends with the lane PARKED and a
  REVIEW-A drawn on the next cycle — no `docs/handbacks/` report.
- A silent child is killed at the idle deadline (≤ 15 min), not at 2 h.
- With two families down, a same-family relaxed round is drawn and its verdict is marked.
- A merged lane unloads clean with the loop's own streams present.

## 5. Out of scope, named
- Fixing `trace.py --approve modified`'s "Drafted, never approved" wording for a demoted row
  (decision 20) — a generator finding, its own row.
- Re-deriving the WI-level `REVIEW-A` compile inside the loop (decision 7) — bigger; this plan
  keeps the supervisor's compile step.

## C7 (owner question 2026-08-30): why one review round is light and the next eats the OpenAI window — the brief's reading scope

Observed across ~20 codex rounds on 2026-08-30 (transcripts in the session scratchpad):

1. **The review diff is scoped `claim-base..HEAD`**, so after every station refresh it also
   contains everything trunk merged since (the WI-508 lane re-read WI-521's merge, the compiled
   `docs/log.md` entries, regenerated `PROJECT_STATE.html`). Fix: the brief names the exact
   command against the CURRENT trunk with three dots — `git diff <trunk>...HEAD -- .
   ':(exclude)docs/iteration' ':(exclude)docs/log.md' ':(exclude)docs/reviews'
   ':(exclude)PROJECT_STATE.html' ':(exclude)docs/open-items.html' ':(exclude)docs/stage'` —
   or, better, `agent_loop.reviewer_prompt` renders `--stat` + the file list into the brief
   (extend `impl_changed_paths`' exclusion set to iteration logs and declared generated artifacts).
2. **Telemetry rides in the diff**: each session commits a clipped transcript under
   `docs/iteration/`; by round 6 a lane's diff carries ten of them, and reviewers read and lint
   them (the recurring trailing-whitespace MINORs). Excluded by 1.
3. **Harness output is ~200 WARN lines per run** (`check.py` advisories, `trace.py` advisories),
   pulled into context once or twice per round. Brief rule: run `check.py --jobs 0 --trunk-lane`
   ONCE and quote the `Check summary` block; `trace.py --strict-integrity` and quote its last line.
   (Or a `--summary` mode on `check.py`.)
4. **"The requirement surface" sends some reviewers reading whole registries** (`test-cases.toml`
   173 KB) and a path that does not exist here (`docs/process.md` — every reviewer errors on it).
   Brief rule: grep the rows the diff cites; never read a registry or `docs/log.md` whole; name
   the real path (`project-trajectory/PROCESS.md`).
5. **No effort dial on the OPENAI rows** (`docs/agents.toml`): the Anthropic rows carry
   `CLAUDE_CODE_EFFORT_LEVEL`; codex runs at its default reasoning. Try
   `codex exec -c model_reasoning_effort=medium --model {model} …` on the TERRA (review-leg) row
   and measure two rounds each way (wall + the `tokens used` line codex prints).
6. **Round count is the multiplier** — eleven rounds over one lane, each over the whole diff.
   C1–C5 cut the rounds spent on outages; the goalpost-moving class (a new MINOR each round)
   is policy, recorded in decisions 12–20, not fixed here.

Test for the brief change: a fixture lane with a refresh commit and three iteration logs —
the rendered brief's file list contains neither, and the diff command carries the exclusions.

## 6. Adopter compatibility (owner question 2026-08-30) — what ships, what stays, what needs a RESYNC entry

The kit's `project-trajectory/scripts/*.py`, `project-trajectory/prompts/*.md` and the launchers
ARE the shipped copies (this repo dogfoods them in place), so every change above ships
downstream on the next resync. Paths stay stable; three things do not stay free:

1. **A new exit code (C2) is a contract change.** The loop's exit alphabet is documented in
   `PROCESS_OPTIONS.md` ("Unattended operation") and an adopter's own wrapper may switch on it.
   Add the code at the END of the alphabet, document it, and write a `RESYNC_PACK.md` entry.
   Same for the idle-timeout launcher slot (C3): the launchers are shipped templates, and
   `tests/test_dogfood_sync.py` enforces STRUCTURE parity between the kit's launcher template
   and this repo's instance — add the slot to BOTH in the same commit, default-absent = today's
   behaviour, so an adopter who never edits their launcher pays nothing.
2. **Prompt paths must be rendered slots, never literals (C6/C7).** This repo has NO
   `docs/process.md` (the masters live under `project-trajectory/`, CLAUDE.md's stated
   self-application boundary) while every adopter DOES (`bootstrap.MAPPING`: `docs/process.md <-
   PROCESS.md`). The brief's literal `docs/process.md` is therefore right downstream and wrong
   here — the meta-repo hazard in one line. The diff command's trunk name is the same class:
   `contract_split` here, whatever the adopter's trunk is there. Both become slots the loop
   renders (`{trunk}`, `{process_doc}` resolved by `agent_loop` from the tree), and the brief
   test asserts the rendered text, not the template text.
3. **The probe and the relaxed rung are policy-visible (C4/C5).** An adopter with a single-family
   roster is already "relaxed" by construction; the marker on the verdict makes that honest
   rather than new. The probe is extra CLI invocations on the adopter's own accounts — keep it
   recovery-only (never on a route with a clean history this run) and say so in
   `PROCESS_OPTIONS.md`'s routing section. Neither touches `docs/process.toml [policies]`.

Two things already landed today that need their RESYNC entries written in the same slice:
the `check_docs` HTML-comment fix (`59ab2951`'s predecessor `59f52549`), and `docs/agents.toml`'s
`opencode run --dir .` (`59ab2951`) — the shipped registry template carries no opencode row,
so the fix is ONLY in this repo's instance; the resync entry must tell an adopter with their own
opencode rows to add `--dir .`.

**How to build it safely in a meta repo:** the loop is paused; build the row BY HAND on a claim
branch (`integrate.py claim`), never let the loop build the loop; verify the launcher/prompt
changes by BOOTSTRAPPING A SCAFFOLD (`bootstrap.py --dest <tmp>`) and running one `--wi` session
there, not only the unit tests; keep the engine's public names (`agent_loop` re-exports) so no
adopter caller moves.

**Owner note (2026-08-30):** consider moving this repo onto the shipped patterns where cheap —
`AGENTS.md` as the instruction home with `CLAUDE.md` as the pointer stub (the shape the kit
ships), which is a tidy independent of this plan. The process-doc path is the one deviation that
matters for the briefs, and the slot rendering in §6.2 removes it without restructuring
`project-trajectory/` (which must stay the isolated template).

**C3 second sample (2026-08-30 ~18:25–19:11 UTC):** the WI-546 review on OPENCODE-GROK went
silent 5 minutes in (last stream line 18:25:36, killed by hand at 19:12 with no verdict file and
no commit) — the second silent-hang of the day on that route, both after real tool activity.
An idle deadline of 900 s would have cut both at a tenth of the wall timeout. Also: the driver's
doubled `--dir` (template now carries `--dir .`, the supervisor's helper injected another) made
opencode exit `The "paths[1]" property must be of type string` — harmless, but C4's probe should
use the row's template VERBATIM so a template defect is caught by the probe, not by a burned draw.
