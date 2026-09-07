## 2026-09-06 — Control window: spend watch raised to US$1000, launch authorized

**Decision (owner).** The US$100 spend figure in the Short control ruling is
raised to **US$1000**. The enabled routes bill against a subscription, so the
figure is a watch over reported spend, not a reservation; unreported spend
still never stops admission (re-ruled earlier today). The WI, day and
coordinator-hour bounds are unchanged.

**Decision (owner).** The owner instructed that the next session perform the
reviewed deletion of `docs/work/pause` and start the window. The owner's
instruction is the review; the deletion commit is the frozen launch commit.
Procedure and kickoff prompt: `docs/handoff-2026-09-06.md`, "Launch
procedure". Recorded in the control decision's owner section, the preflight,
the handoff and the status board.

**Review of the intervening implementation commit (`7a7a07a0`).** The SN-036
ruling was applied as scoped: SN-036 acceptance through the needs-only
snapshot, SR-161 re-pointed to the brief/review mechanism with Inspection,
LLR-183's clause re-worded, SR-186/TC-211 re-pointed, plus one TC-178 Expected
cell; no new cell, carrier, check or backfill. TC-211's Inspection now passes.
Observations carried forward rather than fixed:

- WI-605's spec enumerates 18 SR and 34 LLR Approved cells drifted from their
  snapshot that any whole-registry copy would absorb. That pre-existing drift
  is now visible in one place; it makes WI-605 a heavy early sample for the
  window. Left in the queue by owner choice.
- The complexity baseline is still not re-keyed for the `rendering/` move
  (29 FAILs, armed only from DevStg-Impl), and `check_changed.py` remains an
  uncalled duplicate of `check.py`'s step list. Both wait for an ordinary WI.
- SR-161's rationale now cites the ruling log by path, which the citation-frame
  advisory reports; it was asked for by the ruling and is accepted.
- OI-86 and OI-87 were recorded as ruled (a) on the owner's behalf in the same
  commit; the owner had said they would review them. The owner confirms or
  reopens at the next sitting.

Deferred open items: none.
