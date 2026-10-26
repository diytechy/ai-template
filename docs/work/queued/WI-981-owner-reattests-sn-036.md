+++
id = "WI-981"
title = "Owner re-attests SN-036 on trunk after WI-976's landing"
workstream = "process"
sr_refs = ["SR-161"]
specref = "docs/requirements/open-items.toml"
needs = ["OI-117"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by headless leg 23 (2026-10-26) at WI-976's landing, with
OI-117, as the queued owner row the owner's 2026-10-25 route names
(`docs/decisions/wi-976.toml` D-023): SN-036's re-attestation act moves
to trunk after the landing, since the held-rung lane rule refuses a
MEANING act from a lane. WI-976 landed SN-036's amended acceptance and
every other act of its checkpoint sitting 016
(`docs/reviews/wi-976/016-ADJUDICATE-9d6ad4c.md`, acts 160 and 161), which
ruled SN-036 MEANING on its held rung and recommended it. The owner's
earlier in-lane act is kept under the tag `attended/wi-976-sn036-act`.

## Done-when

- [ ] OI-117 is ruled, and the ruling commit replaces this list with the
      work it routes (OI-102). For (a): the owner, or an attended session
      on the owner's explicit delegation recorded in the commit, takes the
      act on trunk in its own commit, after the text (text then act):
      `intake.py snapshot --approves stakeholder-needs=docs/log.d/2026-10-25-wi976-sn036-ruling.md --reattests SN-036`,
      adding `--verdict docs/reviews/wi-976/016-ADJUDICATE-9d6ad4c.md`
      where the route asks for it. It never lands from a lane. For (b):
      SN-036's text is reworked and re-sat alone, with any row whose
      meaning follows it, and the act follows that sitting.
- [ ] `trace.py --strict-integrity` and `check_trajectory.py --strict`
      pass after the act.
