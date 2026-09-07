# 2026-09-07 — primary runtime audit

Scope: read-only audit of `primary_adjudication.py`, dispatch primary admission,
`agent_loop.main`/`session_body`/`run_iteration`, `primary_approval.py`,
`primary_publication.py`, and the primary close transformation. Focused runtime
suites passed: 89 tests across adjudicate brief, primary adjudication,
primary publication, and primary approval.

## Findings

1. **Initial first approval cannot publish.**
   `primary_approval.absorption_census` requires an approved snapshot blob for
every accepted registry (`primary_approval.py:357-363`). A first approval is
allowed to judge a Drafted row when no snapshot exists, but any `approve` or
`equivalent` decision then refuses with “needs an explicit initial signing
before automatic publication.” This is a substantive lifecycle mismatch if
first approval is intended to create the initial baseline. Either the initial
signing path must be explicitly held for the manual signer, or the projection
must define and test how the first baseline is created.

2. **Meaning impact evidence is not bound to an actual judgment.**
   `_impact_refusal` validates only that `impact[].evidence` is a nonempty list
(`primary_approval.py:497-516`); it never applies `_evidence_refusal` to those
refs. A model can therefore put arbitrary strings or an unrelated committed
ref into an impact row while the decision evidence is correctly checked. The
schema says these are immutable judgment commits, so each impact evidence ref
needs the same turn/session/candidate provenance check as decision evidence.

3. **The prompt-time impact census and publish-time census use different
   populations.**
   The brief assembler derives impact pairs from the bound base, while
   `primary_approval.impact_census` re-runs `git grep` over the final candidate
   (`primary_approval.py:452-482`). The candidate necessarily adds verdict and
   iteration record files, and those files can contain the judged stable IDs.
   A meaning decision can therefore be shown a base census and be refused at
   publication for extra candidate paths. The census needs a defined base
   corpus with candidate blob rebinding for pre-existing paths, or the prompt
   must be regenerated from the exact post-payload candidate before the model
   commits the Approval section.

## Runtime wiring checks

`dispatch._admit_primary` passes the in-process `agent_loop.main` callback;
`primary_adjudication.run` supplies `primary_turn`, `wi`, `base`, `train`, and
primary checkout paths correctly. `run_iteration` records the model verdict
path, candidate commit and primary turn in the subsequent iteration log, and
`primary_publication` can use that log for provenance after the telemetry
commit. No callback-argument mismatch was found.

`handback._adjudication_close_text` does not parse the verdict and therefore
accepts a primary verdict's text transparently. That is safe only because
primary publication validates the payload and provenance before invoking it.
The exact `WI:` trailer is written in the committed judgment artifact as
required by the primary template; current completion gating uses
`adjudicate_brief.verdict_refusal` against the named verdict path, while the
primary run's final publication independently requires the typed judgment log.

This audit is a runtime finding record, not approval of any live spine cell or
publication.
