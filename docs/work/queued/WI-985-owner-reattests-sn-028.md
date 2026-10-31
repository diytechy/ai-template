+++
id = "WI-985"
title = "Owner re-attests SN-028 on trunk after WI-966's landing"
workstream = "process"
sr_refs = ["SR-031", "SR-137"]
specref = "docs/requirements/open-items.toml"
needs = ["OI-118"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by headless leg 25 (2026-10-31) at WI-966's landing, with
OI-118, on the route WI-976's SN-036 act took (`docs/decisions/wi-976.toml`
D-023): SN-028's re-attestation act moves to trunk after the landing,
since the held-rung lane rule refuses a MEANING act from a lane. WI-966
landed SN-028's amended acceptance and why, with every other act of its
whole-set sitting 007 (`docs/reviews/wi-966/007-ADJUDICATE-d8f6fd3.md`),
which ruled SN-028 MEANING on its held rung and recommended it.

## Done-when

- [ ] OI-118 is ruled, and the ruling commit replaces this list with the
      work it routes (OI-102). For (a): the owner, or an attended session
      on the owner's explicit delegation recorded in the commit, takes the
      act on trunk in its own commit, after the text (text then act):
      `intake.py snapshot --approves stakeholder-needs=<the owner's ruling record> --reattests SN-028`,
      adding `--verdict docs/reviews/wi-966/007-ADJUDICATE-d8f6fd3.md`
      where the route asks for it. It never lands from a lane. For (b):
      SN-028's text is reworked and re-sat alone, with any row whose
      meaning follows it, and the act follows that sitting.
- [ ] `trace.py --strict-integrity` and `check_trajectory.py --strict`
      pass after the act.
