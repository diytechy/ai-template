+++
id = "WI-827"
title = "Owner signs SN-029's amendment after text-before-act"
workstream = "process"
specref = "docs/reviews/wi-806-text-then-act/dispute-1-ruling.md"
needs = ["OI-106"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the wave-15 coordinator on 2026-10-05, as the queued placeholder
that puts OI-106 on the owner's surface: an open item is filed together with the
queued row that cites it. WI-806 landed text-before-act (act seq 34), which makes
two clauses of the owner-held SN-029 untrue; the independent adjudicator's dispute
ruling (`docs/reviews/wi-806-text-then-act/dispute-1-ruling.md`) gives byte-exact
replacement cells.

OI-106 was ruled on 2026-10-07: (a), with the two older staleness fixes in the
same sitting. Its Done-when follows.

## Done-when

- OI-106 ruled 2026-10-07 (a): SN-029's acceptance and why cells are amended
  exactly as the adjudicator's dispute ruling gives them
  (`docs/reviews/wi-806-text-then-act/dispute-1-ruling.md`, section "SN-029").
- The two older staleness fixes land in the same sitting: acceptance's "a digest
  of that row's normative cells" (it predates the whole-file copy) and why's "an
  SN has no Status cell" (needs now carry status). An author drafts their text;
  the adjudicator judges it.
- SN-029 sits on a held rung, so the owner, or an attended session on the
  owner's explicit delegation recorded in the commit, lands it on trunk: the
  text first, then the act in its own commit. It never lands from a lane.
- `trace.py --strict-integrity` and `check_trajectory.py --strict` pass.
