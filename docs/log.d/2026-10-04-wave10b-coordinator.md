Deferred open items: OI-98

# 2026-10-03/04 — wave 10b coordinator: design and owner rulings, no builds

Resumed from [handoff-2026-10-03-wave10-coordinator.md](../handoff-2026-10-03-wave10-coordinator.md).
This session was a design and rulings sitting with the owner present. No work item
was claimed or built. Every commit is a docs, rulings or routing change on trunk.

### Rulings and filings

- **OI-101** (WI-788's six questions), raised from a coordinator review and an
  independent Codex Sol 6.1 review. Ruled 2026-10-03.
- **OI-102** (WI-790's three questions). Ruled 2026-10-03; Q3 is the owner's own
  design, a commit-time block.
- **OI-100**, ruled (a), and **WI-791** filed to build it.
- **OI-103** (six lane-state questions, from a second Sol review). Ruled 2026-10-04.
- Records: [2026-10-03-owner-rulings-oi100-oi102.md](2026-10-03-owner-rulings-oi100-oi102.md),
  [2026-10-04-owner-rulings-oi103.md](2026-10-04-owner-rulings-oi103.md).
- **The S11 plan's §6** is recorded as ruled, as recommended. The owner said these
  questions were already ruled, but the record had carried them as owed.

### Work items shaped

- **WI-790** (filed). Work items cite the open items they wait on; open items stop
  carrying `wi_refs`.
  - `open-items.html` shows only items a queued row cites, and ends with "Decisions
    to review", marked off by a boolean `reviewed` key.
  - A commit that closes an open item must update or remove the Done-when of each
    row citing it.
  - Sol amendments A1 to A9.
- **WI-788** (widened by the owner, in passes):
  - session families and reset terms;
  - a kit-shipped glossary;
  - one labelled entry point (risks 1 to 9);
  - provider routes, with Grok and FreeLLMAPI through OpenCode;
  - plan kinds and the lost dual-plan pickup (lost when `31ad569d` deleted the old
    dispatcher on 2026-07-29);
  - the arbiter evidence (DP-001: the arbiter added nothing);
  - the delegated-decisions record on every path;
  - a rolling usage ledger on trunk (U1);
  - one lane-state provider (LS1 to LS10);
  - Sol amendments B1 to B12;
  - OI-103's rulings.

  Half 1 is a design note in four chapters that stops at the owner's checkpoint.
  Half 2 becomes successor rows.

### Artifacts

- [wi-lifecycle.html](../iteration/wi-lifecycle.html): a sequence diagram of today's
  work-item lifecycle, drawn from the code.
- [plans/2026-10-04-planning-before-build-research.md](../plans/2026-10-04-planning-before-build-research.md):
  the research on planning before the build, with sources.
- Sol reviews:
  - [2026-10-03-wi788-readiness](../reviews/2026-10-03-wi788-readiness/sol-review.md);
  - [2026-10-03-wi790-proposal](../reviews/2026-10-03-wi790-proposal/sol-review.md);
  - [2026-10-04-wi788-widened](../reviews/2026-10-04-wi788-widened/sol-review.md).

### Routing and environment

- The owner bumped the agent definitions (`2c629ea0`). The review fix (`da857485`):
  - Opus pinned to `claude-opus-5-5` (`claude-opus-5` answered as Opus 5);
  - `xhigh` in place of the invalid `extrahigh`;
  - the commented-out OpenCode rows removed from `docs/agents-enabled`.
- Machine changes, outside the repo:
  - the npm codex 0.157.1 → 0.160.0, so `gpt-6.1-sol` runs from PATH;
  - the native Claude Code 2.1.201 → 2.1.289, so `claude-opus-5-5` runs;
  - Claude Code subagents set to a 1-hour prompt cache (user settings).

Bar at every commit: the smoke tier within its 60 s budget, `check_trajectory --strict`
clean, and `check_docs` OK. The full unfiltered suite was not run this session; it
last ran at `d040ad75`.
