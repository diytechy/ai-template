+++
id = "WI-908"
title = "Owner-assisted Claude login-isolation check: two account homes on Windows show two logins"
workstream = "process"
sr_refs = ["SR-222"]
specref = "docs/plans/2026-10-04-wi788-design/2-sessions-routing-accounts.md#5-providers-and-routes"
needs = ["WI-798", "OI-114"]
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by the coordinator on 2026-10-11 (leg 03) as the owner-dependent half of
WI-798's login-isolation check, split out before WI-798's claim to answer its
scope critique's B3 (coordinator-2026-10-11 D-014), and as the queued
placeholder that puts OI-114 on the owner's surface. WI-798 builds account
homes and records the no-spend empty-home half; a Claude account other than
the ambient login that authenticates by login stays unverified, printed as
such at preflight, until this row passes (D-029). The adjudicator is
unaffected: it authenticates by its long-lived token.

## Done-when

- After WI-798 has landed, the owner provisions a second Claude login under
  a declared account home (WI-798's account tables), attending the session
  while the coordinator runs this check (OI-114 ruled (a), 2026-10-14).
- Run under each home, with no model spend, Claude's status command reports
  each home's own login, and signing in under one leaves the other and the
  ambient login unchanged; the result is recorded in a log fragment.
- On a pass, that account's `verified` cell is set to the date and Claude
  version in a reviewed commit citing the fragment.
- On a fail, the cell stays empty, and the fragment and the RESYNC entry
  record that login-authenticated non-ambient Claude accounts are unsupported
  on Windows (token accounts are unaffected).
- Review bar: A (one cross-family REVIEW-A).
