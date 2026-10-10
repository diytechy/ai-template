# 2026-10-10 — WI-874: the store lookup, re-measured

WI-874 memoizes the primary checkout's git common directory per root for the
process's life (`session_keep.primary_out_dir`), so a store operation spawns
`git rev-parse` at most once. These are the figures its Done-when asks for, beside
WI-869's quiet figures ([2026-10-09-wi-869-smoke-tier-measurement.md](2026-10-09-wi-869-smoke-tier-measurement.md)).

Command: from the lane (base 39c35146, the change applied),
`python -m pytest -q -n 2 -p no:cacheprovider --durations=0` over the four modules,
summing setup, call and teardown per module. The box was quiet (CPU 12-13% at the
start). Each run: 228 passed, in 18.3 / 17.1 / 17.0 s wall.

| Module | WI-869, quiet (before) | WI-874, three quiet runs (after) |
|---|---|---|
| `tests/test_session_keep.py` | 55.7 s | 5.9 / 5.8 / 5.9 s |
| `tests/test_coordinator_adjudicate.py` | 35.8 s | 15.3 / 15.4 / 15.2 s |
| `tests/test_adjudicator_token.py` | 16.8 s | 4.0 / 4.0 / 4.0 s |
| `tests/test_coordinator_guard.py` | 14.9 s | 4.1 / 4.2 / 4.2 s |

The builder's loaded runs (another workload on the box) read 833.3 / 681.7 /
768.8 s summed before the change and 286.7 / 281.6 / 293.5 s after. They agree in
direction and are not used as figures.
