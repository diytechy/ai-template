## 2026-09-07 — Refresh committed provenance before primary selection

The [failed selection record](../reviews/wi619-selection-recovery/README.md)
preserves the actual uncommitted machine turn and hook refusal. The new Drafted
interface changed committed provenance only after the source commit existed, so
its re-attestation/open-items renderings needed the canonical post-commit refresh.
The selection never committed and no provider session started. Its bytes are
preserved outside the pending-turn directory; the queued WI and scope remain.

The declared regeneration updates views only. No registry cell or accepted
snapshot changes; no semantic approval or fabricated selection/session evidence.
The coordinator stays paused; no control window, push or main merge.

Deferred open items: none.

Smoke: **1696 passed, 4 skipped in 52.39s**, wall **52.58s**, budget enforced. fig: exact argv and revision `35020525450fb12b9b404823cc5dffa74256af9b` in `docs/reviews/wi619-selection-recovery/checks.json`; candidate adds only recovery records and derived provenance.
