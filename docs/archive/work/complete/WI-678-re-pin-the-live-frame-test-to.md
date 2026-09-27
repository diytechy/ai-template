+++
id = "WI-678"
title = "Re-pin the live-frame test to the C1 frame, and settle IF-215 and IF-220's untied external endpoints"
workstream = "tests"
specref = ""
buildtier = "quick"
safety_class = "ordinary"
priority = 5
+++

## Deliverable

`tests/test_traj_parse.py::test_frame_context_reads_this_repo_s_own_locked_frame`,
the slow-tier pin of this repository's depth-0 frame, now pins the C1 frame.
It had been red since the sitting.

- **The frame:** 5 entities, the 7 crossings B-01, B-02, B-04, B-05, B-09,
  B-10 and B-11, and 1 relationship.
- **Crossings:** B-02 and the three new crossings are pinned unrealized
  today; B-05's IF-080/IF-081 bundle still holds.
- **Untied rows:** the list is IF-032, 036, 041, 151, 154, 155, 157, 168,
  171 and 215, each stating its "No tie-back" reason.
- **IF-220:** its `external:downstream adopter` consumer was wrong, since
  only `baseline_snapshot` reads the act ledger. It is removed and the notes
  say why.
- **Review:** Sol asked for the new crossings to be pinned empty rather than
  left unpinned (arbitration ruling 21), and the integrator applied it.
- **Noted:** IF-041's notes still describe REL-003, which the sitting
  promoted to B-10. Its re-tie is deferred by package §7.

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
