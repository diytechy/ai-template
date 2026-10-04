+++
id = "WI-814"
title = "Weekly-pace account selection within a family"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-usage-pacing"
needs = ["WI-798", "WI-801"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-usage-pacing, added by the checkpoint
ruling (README A2; D-034). It builds A1's step 5: within the family step 4 chose,
draw the account with the largest weekly headroom, so no subscription is left with a
large unused budget while another is exhausted at reset. Readings per account, each
under its own home: Claude's OAuth usage read (5-hour and 7-day used percent, with
reset times), read-only and never refreshing a copy of the credential; Codex's
`codex app-server` `account/rateLimits/read` under the account's `CODEX_HOME`. Both
endpoints are undocumented, so each is a route contract with `verified`. The
reference implementation is the owner's gauges (`ai_usage_feeder.py`, NagLight's
`gauge.go`). Budget pacing is a stakeholder outcome no current need covers, so the
row first drafts a new need for the owner's signature, then its SR rows. It replaces
today's enable-list order rule; it never adds beside it.

## Done-when

- A new stakeholder need for budget pacing is drafted and signed by the owner
  before any SR row of this row is drafted.
- The applicable windows are every limit the provider reports that governs the
  route's model: the account's weekly window, a model-scoped weekly window where
  one is reported, and the 5-hour window. A window's length is the reported
  duration, else its declared kind; its start is its reset time minus its length.
- Per applicable weekly window, `elapsed = clamp((now - start) / length, 0, 1)`,
  `pace = 100 x (1 - elapsed)` and `headroom = remaining percent - pace`; an
  account's headroom is the smallest over its weekly windows, and the account
  with the largest headroom is drawn.
- An account with ANY applicable window at no remaining budget is on cooldown
  until that window resets, whatever its headroom.
- A reading is fresh within `[routing] usage_max_age_minutes` (shipped 30); an
  account with no fresh reading counts as exactly on pace (headroom 0), logged.
- Pacing never chooses between families, and today's enable-list order for
  accounts within a family is replaced, not kept beside it.
- Each spine row this row adds (the new need and its SRs) passes adjudication of
  that row, on whichever adjudication path is the one path when this row lands.
- The row's test bar: its affected modules' tests plus the smoke tier at `-n 2`,
  plus fixture readings for both providers, an unreadable source, a stale reading,
  two Claude accounts, a model-scoped weekly window, an exhausted weekly window
  beside a low-headroom live one (the live one is drawn), and an exhausted
  account-wide window under a model-scoped window with budget left (never drawn).
- Review bar: A+B (REVIEW-A plus an independent REVIEW-B).
- RESYNC_PACK: an entry anchored at a trunk commit; it adds the
  `usage_max_age_minutes` dial.
