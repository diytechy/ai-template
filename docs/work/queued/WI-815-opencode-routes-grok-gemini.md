+++
id = "WI-815"
title = "Grok and FreeLLMAPI groundwork through OpenCode, and an untested Gemini route"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-routes"
needs = ["WI-798", "WI-801"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-routes (ch.2 §5, §9; OI-101 Q3, Q4). Grok
and FreeLLMAPI run through OpenCode, with no separate xAI CLI route; Gemini is
documentation-only and untested. Every row gains `verified = "<date> <cli
version>"`, empty meaning untested; preflight prints each enabled untested route and
the shipped defaults enable none. Family fixes: an OpenCode row's `family` is the
model's trainer (Grok `XAI`, Kimi `MOONSHOT`; README change 21). The Gemini row moves
to stdin, with its adapter built from the documented schema on a synthetic fixture.
FreeLLMAPI's OpenCode config comes from a kit-shipped
`opencode-freellmapi.template.json` in the account home, its key in an untracked
`key` file; a FreeLLMAPI row ships only for a pinned id with a declared one-model
chain (D-029); no `auto` row and no `opencode/*-free` row (D-014). **The FreeLLMAPI
route row and its one live call are not in this row:** they wait on OI-105 and its
placeholder WI-795 (README Q-4), which the owner rules once the router runs.

## Done-when

- The `verified` field and its preflight line exist; untested rows are visibly
  unverified and enabled nowhere by default.
- The Grok row exists with its declared window, and the OpenCode family fixes are
  applied.
- The Gemini row runs on stdin, and its adapter passes a synthetic fixture (usage
  from `stats`, no occupancy, so every-call reset).
- The FreeLLMAPI account template and its OpenCode config are shipped;
  `opencode models freellmapi` resolves under the account home.
- A FreeLLMAPI row with no declared one-model chain is refused.
- No FreeLLMAPI route row ships and no live FreeLLMAPI call is made here: both wait
  on OI-105 and WI-795.
- No adopter is forced to install a CLI.
- Each spine row the README matrix gives this row (LLR-266/267/268, TC-262..265,
  IF-045, IF-245, shared with WI-798) is amended and passes adjudication of that
  row, on whichever adjudication path is the one path when this row lands.
- The row's test bar: its affected modules' tests plus the smoke tier at `-n 2`. The
  README's extra bar, one live call (Q-3), is the FreeLLMAPI call, held by OI-105.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit; it adds `verified` to route
  rows and ships `opencode-freellmapi.template.json`.
