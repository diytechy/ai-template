## 2026-11-08 — WI-996: a removed red mark is proven red by the lane's last review record, and no red mark lands

Deferred open items: none.

`[bars] red_mark` declares the strict expected-failure mark, read in one parse
with `[bars] review` (`kitlib/red_mark.py`). `attest` judges each test file's
mark count against the lane's last review record or its base, the refresh
refuses a tree holding a mark, and the coordinator's hand landing runs the same
check on the staged squash (recipes §3). The RESYNC entry is a forced migration:
every adopter declares the key, and a lane cut before this landing refuses at
`attest` until it rebases (today `wi-902` and `codex/simplify-spine-resync`).

Stamps moved with it:

- `integrate.py` 1801 -> 1793: the review bar's own parse moves into
  `kitlib.red_mark.read_bars`, net of the red-mark calls added to `attest`'s
  preflight and the refresh.
- `gen_arch_map.py` 1575 -> 1558: the review set's test-file rule (the hidden
  path check and the suffix list) moves byte for byte to `kitlib/spine.py`, so
  the counter and the tag reader call one predicate (wi-996 D-005, for the
  owner to confirm or overrule).
- `PROCESS.md` 100,273 -> 100,417 bytes (§4: a lane proves its failing test by
  the declared red mark); the byte-budget-guard row re-stamped.

- Headless legs 36 to 38: leg 37's machine crash cut the C3+C4 build off; leg
  38 kept it whole and finished it. Two counted rounds (round 1's MAJOR, a
  tests root of `.` counting the declaration, fixed with a regression test),
  the checkpoint (sitting 005: SR-156 and LLR-207 MEANING+BLESS, LLR-368 and
  TC-421 to TC-426 approved), the gate's convergence-class MAJOR to dispute
  sitting 008 (FIX: the hand landing's check), one fix round, and a final
  review with both reviewers approving. Acts 180 and 181.
- Follow-ups, not built here (wi-996 D-004, D-007, D-010): the spec's coverage
  bound still says a near-miss spelling (an added `reason=`) is unmarked to the
  check, and whether to widen the count to the declared text's call head; the
  counter reads every blob under the tests root before filtering; SR-156's
  "refuses both" and TC-423/TC-426's deferring expected cells, for clarity.
