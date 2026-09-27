+++
id = "WI-678"
title = "Re-pin the live-frame test to the C1 frame, and settle IF-215 and IF-220's untied external endpoints"
workstream = "tests"
specref = "tests/test_traj_parse.py"
buildtier = "quick"
safety_class = "ordinary"
priority = 5
+++

## Context

`tests/test_traj_parse.py::test_frame_context_reads_this_repo_s_own_locked_frame`
pins this repository's depth-0 frame as data. It is in the slow tier, so no
per-commit bar saw it go red, and it is red on trunk twice over:

- The C1 sitting (WI-643) redrew the frame to 5 entities, 7 crossings
  (B-01, B-02, B-04, B-05, B-09, B-10, B-11) and 1 relationship. The
  package's §6 checklist named `tests/test_external_frame.py` but not this
  second pin.
- Two interface rows the second build wave added now sit in the frame's
  `untied` list: IF-215 and IF-220. IF-215's notes carry a "No tie-back"
  reason, as the test's convention requires. IF-220's (the approval-act
  ledger, `docs/archive/last_approved/acts.toml`) does not.

IN SCOPE: re-pin the counts and crossing ids to the C1 frame, and re-check
each crossing's `realized_by` assertion. For IF-215 and IF-220, decide per
row whether its `external:` endpoint is right. For IF-220, a kit-written
file under `docs/` is probably not an external party at all, so its endpoint
may be wrong. If the endpoint is right, give the row its "No tie-back"
reason; if not, correct the endpoint. Both are Drafted rows, so they can be
edited directly. Then pin the resulting untied list. Update the test's
comment history in the established style.

## Done-when

- The test passes on trunk, pinning the C1 frame and an untied list whose
  every row states its reason.
- `trace.py --strict-integrity` and `check_trajectory.py --strict` pass, and
  the commit bar passes.
