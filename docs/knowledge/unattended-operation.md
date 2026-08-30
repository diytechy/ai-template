# Unattended operation: the 3am failure that pages nobody — DRAFT

> **DRAFT (agent-authored, WI-546, 2026-08-30).** Drafted by the unattended lane so the `hat.UNATTENDED-OPS` roster entry has a `knowledge` value to point at; the owner reviews and cuts at RETURN, per the `hats.toml` header's own rule. This distills THIS repo's accumulated perspective from its own decisions and surfaces — it is not retrieved external research, and its claims are the drafter's reading, not a settled finding.

This repo runs itself unattended: `agent-resume.*` drives
`project-trajectory/scripts/agent_loop.py`, which claims work through
`dispatch.py` and merges through a serial integrator. The charter in
`docs/requirements/hats.toml` (`[hat.UNATTENDED-OPS]`) asks what this looks like
at 3am with no human, and listens for four failure shapes: a silent degrade, a
partial write left behind, an unbounded retry, and a green that is green because
nothing looked. The most valuable evidence here is that this repo has already
been bitten by the fourth, measured it, and hardened against the first three by
construction — so the hat's job is to hold new work to the standard already met,
not to invent one.

## What this hat looks for here

- **A green because nothing looked — the measured instance.** `LLR-037` carried
  `status_size_warning` as a live design claim for **five weeks** after the
  symbol was deleted (at `c4aeab9f`, WI-210), and it was caught **by a census,
  not by a check** (`docs/requirements/open-items.toml`, the OI-38 body near
  :1129, :1507). The existing `code_symbol` anchor rule would have caught a
  dangling symbol; it missed this one because the cell described the symbol in
  PROSE while its token pointed elsewhere. Worse, the retired tripwire itself
  only *warned and never blocked* (:1527) — a smell, printed, that could not
  fail a run or a gate. Two silent-failure shapes stacked: an unenforced warning,
  then a stale Approved row publishing a deleted symbol into the generated
  bundle. The lesson the hat carries: an anchor that verifies a token is not the
  same as one that verifies the sentence around it.

- **A partial write left behind.** The `hat.INTEGRITY-RECOVERABILITY` charter is
  the sibling here, but UNATTENDED-OPS owns the durable-artifact case. The design
  answer is that lane state is **derived from git history, not asserted**
  (`docs/concurrency-restructure.md` §on retiring `events.jsonl`/`run-state`,
  ~:168, :250): a crash mid-run leaves recoverable git state, not a corrupt
  side-file. `claim()`'s two-write window was deliberately re-ordered so a crash
  between the writes leaves at worst an orphan branch the dispatcher deletes and
  re-claims — the failure was moved to the *benign* side and `_stranded_claims`
  deletes with it (`docs/concurrency-v2.md` §A3, ~:449-456).

- **An unbounded retry.** The retry is **bounded by design**: after one lost
  optimistic race a branch takes the slot pessimistically for its retry, so a
  slow lane cannot be starved and a fast one cannot spin forever
  (`docs/concurrency-v2.md` ~:251, :284). A refresh is a disposable
  `git reset --hard` commit, not an accreting loop. New loop code that can retry
  should say what bounds it.

- **A failure that pages nobody.** When a lane cannot proceed, the exit is
  `EXIT_NEEDS_HUMAN` (`agent_common.py:134`, value 7). `agent_loop.py`
  (~:640-641) turns it into `handback.close_partial` — an immutable per-close
  report plus a `blockref` that `schedule._disposition` reads as `blocked` — so
  the hold is a visible, queued, durable page rather than a stalled process.
  `adjudicate_brief.py` states the sharp rule the hat should enforce on any
  paging surface: **"a half-filled brief is WORSE than the generic prompt"**
  (~:26) — a thin evidence section reads as a completed investigation that found
  nothing, so an assembler returns nothing rather than a plausible-looking
  partial. A degrade must fail loud, not degrade quiet.

- **A claim a dead lane never releases.** `SR-144`
  (`docs/requirements/system-requirements.toml:552`) requires every lane close
  to be a TERMINAL state with one immutable per-close record — refusing a second
  close of the same event rather than overwriting the first, and refusing a
  report that names neither a keep/discard split nor an explicit deferral. A lane
  that dies holding a claim is reclaimable (the `_stranded_claims` path above);
  a terminal spec with no report is LOUD, not silently un-disposed.

## Application

- Ask of any new loop-facing or `unattended`-tagged work: what does the next
  reader find if this is killed mid-write, and can the system name the state it
  is in afterward? Prefer derive-from-git over a side-file that can rot.
- Distrust a check that verifies a *token* and treat it as blind to the *prose*
  around it — the LLR-037 miss is the repo's own proof that a passing anchor is
  not a read cell. A periodic census, not only a gate, is what caught it.
- A warn-only tripwire is a silent degrade unless something reads the warning;
  say who reads it, or make it block.
- Any human-facing hold must page durably (`blockref`/terminal close) and must
  refuse to emit a half-filled artifact rather than one that looks complete.

## Open questions / bounded here

- **Census cadence is not mechanized.** LLR-037 was caught by a hand census five
  weeks late; nothing schedules the next one. The prose-vs-token gap that hid it
  is the same class the traceability-enforcement pack documents (MEANING-checking
  is refused by ruling D-4, not merely unbuilt), so this is a known, bounded gap,
  not a proposal.
- **`NOTHING GATES ON A HAT TODAY`** (the `hats.toml` header states this). This
  pack informs a review lens; it enforces nothing on its own, and its locators
  are line-approximate — re-derive against the live files before quoting a number.
