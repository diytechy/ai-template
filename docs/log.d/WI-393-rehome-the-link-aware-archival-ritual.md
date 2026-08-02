## 2026-08-01 — WI-393: the link-aware spec-move ritual is rehomed, and every move site runs it

**Summary.** The move+relink machinery Phase 5 deleted with the dispatcher
(`31ad569d`: `_relink_archived_specs`, `_rebase_moved_spec_links`, their two
shared primitives) is restored as the new kit sibling
[`spec_move.py`](../../project-trajectory/scripts/spec_move.py): `move_spec`
performs move + outbound rebase + inbound redirect + staging as ONE indivisible
operation — no caller can perform two thirds of it — with the original
discipline verbatim (link text untouched, `#fragment`s carried,
external/protocol-relative/bare-anchor targets left alone, root-relative
excused only in the rebase half, CRLF preserved via `newline=''`, per-link
decisions split out of the traversals). Wired at every move site:
`integrate.claim`'s bare `git mv` is replaced (the claim commit now carries
the relinks — the 2026-08-01 claim-move that broke the backlog plan's row
links is the driven instance), `handback.hand_back` returns specs through
`move_spec(new_text=...)`, and the CLI (`SRC DEST` | `--archive [--date]`)
serves the worker's by-hand terminal close and spec-of-record archival — the
deviation WI-394's close recorded ("the ritual was applied by hand") retires.
This close's own spec move to `complete/` was performed with the new CLI.

- **Deliverables:** `project-trajectory/scripts/spec_move.py` (the ritual, its
  pure `rewrite_text`/`expected_relink` oracles, the CLI);
  `project-trajectory/scripts/integrate.py` (claim wiring; `_abandoned_claim`
  widened by ORACLE — `_relinked_exactly` excuses an `.md` modification only
  when byte-identical to `spec_move.expected_relink` over the commit's own
  move pair, `_claim_delta` is that clause's C901 extraction);
  `project-trajectory/scripts/handback.py` (return wiring);
  `tests/test_spec_move.py` (16 tests, the restored WI-288/WI-353 guard shape
  including the MUTATION TWIN: the archived fixture passes the REAL
  `check_docs` while the same move without the rebase fails it); claim/return
  wiring driven in `tests/test_integrate.py` (ritual in the one claim commit;
  crashed relinked claim re-cuts; a non-relink `.md` edit still convicts) and
  `tests/test_handback.py`; registration per the handback precedent — kit
  README + bootstrap rows, LLR-145 + TC-139 tagging the module into CMP-004
  under SR-132, dupes census (cli 85→86; the `link-rebase` class returns for
  the trunk_step pairing), size stamps (integrate.py 1890→1946 reviewed bump;
  bootstrap.py 2250→2257 registration), arch map + gate + dashboard
  regenerated; the WI spec closed to
  [`docs/work/complete/`](../work/complete/WI-393-rehome-the-link-aware-archival-ritual.md)
  with `specref` cleared (R-F; its `docs/specs/README.md#lifecycle` ref was
  the shared lifecycle doc, not a per-WI spec-of-record, so nothing archives).
- **Red-then-green (watched):** `tests/test_spec_move.py` failed at collection
  before the module existed; `test_claim_runs_the_link_aware_move_ritual`
  red on the unwired claim (`'](../../../../seed.txt)' not in text`), then
  green; `test_a_crashed_claim_that_relinked_docs_is_still_re_cut` red at
  `_abandoned_claim` after the claim wiring and before the oracle clause,
  then green; the handback ritual test red at its claim-premise assertion,
  then green.
- **Deviations from spec:** (1) the spec scoped the ritual to archival with
  the close path as candidate host; the drain plan (row 5) widened it —
  "owed at claim as well as at archival" — so claim and handback are wired
  too, and the host is a new sibling rather than `integrate.py`, which sits
  at its exact size baseline as a named decomposition target (the
  WI-374/WI-387 extraction escape the ratchet documents). (2) LLR-145 +
  TC-139 were filed at build time by this ordinary lane — the WI-387
  fragment's own argument, after the station refresh twice redded on a
  module no builder bar could see missing from the component web. (3) The
  RULING-6 `audit` allowed-set was NOT widened: a claim that relinks a doc
  outside bookkeeping+generated surfaces would flag in a window audit.
  In practice inbound linkers of queued specs are bookkeeping surfaces;
  widening the audit is an owner ruling, not this lane's call — surfaced
  here rather than silently absorbed.
- **Byte deltas on budgeted files:** none (no budgeted doc touched).
- **Verification (watched):** `pytest -q tests/test_spec_move.py` — **16
  passed**; smoke tier (`pytest -q -n auto -m smoke`) — **594 passed, 6
  skipped in 9.22s** (membership 600/640); full unfiltered suite
  (`pytest -q -n auto`) — **1822 passed, 10 skipped in 282.35s (0:04:42)**;
  `trace.py --strict --require-verified` rc=0 (SN=25 SR=135 LLR=128 TC=125,
  orphans=0, integrity=0); `check_trajectory --root . --strict` rc=0 (the
  WI-389/WI-390 SpecRef WARNs are pre-existing and not this lane's);
  `check_doc_refs --root . --strict` rc=0.
