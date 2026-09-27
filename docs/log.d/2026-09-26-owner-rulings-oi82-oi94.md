## 2026-09-26 — The owner rules OI-82 and OI-86 to OI-94; OI-88 stays open for discussion

The owner answered the ten pending open items in one message at the start of
the coordinator's third session. Their words are quoted in each row's
`decision` cell in
[../requirements/open-items.toml](../requirements/open-items.toml); this
entry records what each ruling sets in motion. Nine are ruled. OI-88 stays
pending because the owner asked for more discussion.

**OI-82 — (a), refined.** Every unapproved chain stays in the approval brief.
A chain on a released rung renders in full, labelled "Waiting for automated
adjudication" and collapsed by default. WI-577 was parked on this row; it now
carries the ruling in its Context and is released.

**OI-86 — (a).** SN-041 to SN-044 stand as approved, including SN-042's
prospective narrowing (D6/D20) and the D5 deferral. The owner's clarification
decides it: the held rung stops a *mechanically triggered* session from
approving without the owner's intent. It does not stop the owner delegating an
approval to the attended session they direct. The Fable stand-in acted under
that delegation. The owner asked whether this needs clearer documentation. It
does: the dial is documented as "the human approves" everywhere, with no word
on delegation. **WI-649** states it once, where PROCESS.md defines the dial.
The owner's second note (an amended row whose meaning is unchanged is
re-anchored by the amendment adjudication, not re-signed) holds for SR, LLR and
TC today. For needs it waits on the drift detector (OI-91).

**OI-87 — (a) plus an addition.** A requirement's test case counts from the
first commit at which it reads approved AND names the requirement or one of its
design rows. Owner's addition: a defined test still runs once its
implementation is done. If its test case is not approved, the result carries a
warning that it may not reflect the intended behaviour. **WI-650** drafts the
SR-217/LLR-257/TC-250 amendments, places the warning on the spine, builds both,
and files the adjudication.

**OI-88 — pending, direction recorded.** The owner leans toward approving a
level-0 interface that meets a boundary together with the assumption that
needs it, or toward baking the interface into the assumption. The driver's
analysis is added to the row. The frame's crossings already are those level-0
interfaces, approved with the frame at DevStg-Boundary, and assumptions already
land on them (`effect_at`). So a Boundary arm of SR-212 over crossings, option
(c), matches the owner's intent without moving when interface rows are
approved. The recommendation is revised to (c). WI-634 still builds SR-212's
Arch arm as approved; (c) adds an arm rather than undoing that build.

**OI-89 — (a).** SR-187 stays a derived requirement. The owner asked how the
kit accommodates one. It traces to the need it serves (SN-043), names the lens
that derived it in `hat_refs` (FIRST-RUN-ADOPTER), and argues the derivation in
its `rationale` (spine-authoring skill, rule (c)). The operation/delivery
`system` cell is what lets delivery-frame requirements (the kit, its process)
sit beside a product's populated needs without claiming to derive from them.
The upward feedback leg, rendering the derived set to the need owner, is not
built yet; WI-633's per-need view is its queued home.

**OI-90 — (a).** The Automated-cell marker stands.

**OI-91 — (a), fund.** **WI-651** adds the need tier to the snapshot
comparison and the re-attestation brief. It is sequenced after the assumption
tier's build.

**OI-92 — (b), re-tier.** The 60 s budget stands and the tier's membership
changes. The condition is representativeness. The owner frames it as a trial
("Is saving 4 minutes each commit worth it? It may not be, but I'm willing to
try it"). **WI-652**, prioritised so later commits get a real seconds bar.

**OI-93 — (a).** The integrity report stays. **WI-653** drafts LLR-216's
amendment and drops the frame-class report.

**OI-94 — (b), on a condition.** The owner accepted making SR-211's report
vacuous "as long as" queued work returns to close the gap. Checking that
condition showed it did not hold: C2 (writing the assumption rows and each
boundary interface's `bridged_by` or `coincident`) was a plan step with no
queued item. **WI-655** files C2 in this commit, so the condition now holds.
**WI-654** amends and builds SR-211's vacuity.

Deferred open items: OI-88 — the owner asked for more discussion; the revised
brief carries the driver's analysis and option (c).
