# WI-914 adjudication 004: amendment of LLR-292's Detail

I judged the one amended cell at `3c4f79638`. Since the anchor (`247dc36c4`), only LLR-292's `detail` line moved in the LLR registry, and no other registry changed. The LLR rung is released (`human_approval_through = "DevStg-Boundary"`).

## amendment

- [CLARITY] LLR-292 Detail -> distinct edges in freshly emitted How, When, Process and System-context SVGs, every drill layer included, never overlap along a segment or join end to end outside a shared actual terminal; departures and arrivals get separate channels and terminal runs are reserved first; shared node identity permits no join outside the port; perpendicular crossings stay under the T8 critique, and "no claim is made that crossing count is minimal" -> the same obligation, ending "this row sets no bound on their count" -> identical. Both endings say the row imposes nothing on how many perpendicular crossings occur and leaves them to the T8 critique. The old wording disclaimed a minimality promise the row never made. The new wording states the same absence as a closed, observable scope, with no unmeasurable term ("minimal"). No count was required before, and none is now. An emitter correct under the old text (no overlaps, no off-terminal joins, any crossing count) is correct under the new one, and the new text forbids nothing the old allowed. Nothing else in the cell moved, and no carrier is named.

VERDICT: CLARITY rows=1

**Aftermath:** the row keeps its attestation. This session re-anchors it on the released rung, in its own act commit:

`python project-trajectory/scripts/intake.py snapshot --reattests LLR-292`

SITTING: JUDGED kinds=amendment
