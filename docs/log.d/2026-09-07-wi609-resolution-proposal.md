## 2026-09-07 — WI-609 resolution prepared; one ownership decision remains

Investigated the owner's request to resolve the publication blocker while
preserving the stopped coordinator. The
[concrete decision proposal](../reviews/wi-609-resolution/DECISION.md) recommends
one reviewed, supervised transfer of the separate amendment scopes to a new
combined owner after exact PC authoring. Its scope is the actual corrected
candidate's complete Approved-change population, with Drafted riders kept
unapproved. No transfer or primary selection occurred.

The real independent review returned the more complex judgment-only protocol:
it would introduce new intent and evidence-reuse behavior and need a bootstrap
exception. It recommended using the existing publisher with a combined scope
for the current backlog. Preserved the frozen design/prompt, actual provider
metadata and verbatim opinion; neither is an approval of registry cells.
The actual scope parser and absorption verifier accept the combined set in an
isolated diagnostic assuming valid judgments; those assumed judgments are
explicitly synthetic test inputs, not committed Approval evidence or a claim
that semantic review passed.

The earlier statement that no input was needed was too broad. Diagnosis and
preparation required none; transferring the three currently preserved amendment
owners changes the recorded scope constraint. Automatic consolidation refuses
while adjudications are queued. OI-88 now asks for the exact one-time transfer;
WI-609's typed `needs` edge records the hold. Existing WI-601/603/605 scope bytes
remain untouched. No temporary unpause, claim, new runtime mode, verifier
weakening, snapshot copy, code deletion, control window, push or main merge.

Primary approval/publication baseline: **42 passed in 24.93 s**. <!-- fig: `.venv/bin/python -m pytest -q tests/test_primary_approval.py tests/test_primary_publication.py` at 53b36b46; out/run-logs/wi-609/baseline-tests.txt -->
Smoke: **1695 passed, 4 skipped in 49.16 s**, **49.4 s** measured wall within
the enforced **90 s** budget. <!-- fig: `.venv/bin/python -m pytest -q -n auto -m smoke`, time.monotonic wall checked by `scripts/check_smoke_budget.py --mode enforce --elapsed`; unchanged runtime/test tree at 53b36b46 plus this proposal candidate; out/run-logs/wi-609/smoke.txt -->
Normal regeneration and documentation checks passed with existing warnings.
No byte-capped guide changed. This is supervised proposal preparation while
claims are paused; WI-609 remains queued and no completed implementation or
live amendment acceptance is claimed.

Deferred open items: none.

Update 2026-09-07: the owner ruled OI-88; see the OI-88 source-authoring log. The pending question above records the original proposal sitting.
