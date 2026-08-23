+++
id = "WI-489"
title = "Execute OI-34's ruling: the derived-requirement label dies, the rows carry their deriving HAT(s), and the 16 allow entries retire with the migration (ruled 2026-08-18, unminted until the ARM-3 vacuity check surfaced it)"
workstream = "requirements"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "spine"
priority = 2
+++

## Deliverable

OI-34's ruling is executed — the derived-requirement label is gone from
the spine. 17 SR rationale cells migrated (16 dated PROVISIONAL markers +
SR-053's signed variant; the ruling's 18th, SR-040, left when OI-38 struck
its paragraph), each keeping its `Hat-derived (hat.NAME)` prose as the
hat-carrying form until WI-484's field lands. Four cells needed prose
beyond the marker (SR-033/SR-052/SR-175 carried label references that
would have dangled or gone false; SR-043's OPEN QUESTION paragraph retired
under OI-37's marker-and-entry-go-together instruction, replaced by the
standing reason the fail-open arm is deliberate under the relaxed need).
All 17 allow entries retired with retirement records — the file's zero-
active state is documented as the intended resting state, not a clean
bill; the snapshot refreshed byte-identical. Vacuity findings 2 → 0;
citation-frame findings 0 → 0 (the entries covered exactly the markers);
integrity 0; full suite 2647 passed / 13 skipped. One test assertion
changed deliberately and stated: the non-empty allow-list guard became
one-key-per-declaring-line — stronger, valid at zero. PROCESS.md's
labelled-derived-SR vocabulary deliberately left for WI-484 (not violated
by this migration; its retirement needs the replacement WI-484 mints).

## Context

OI-34 was ruled (c) on 2026-08-18 — KILL the label; SRs/LLRs instead carry
the HAT(s) they were derived from, and that hat data feeds the generated
component view (OI-32's program, WI-484) — with "18 rows to migrate as its
own WI". The WI was never minted: exactly the deferral-without-a-queue-row
class OI-41 exists for, surfaced on WI-485's first day live when ARM 3
reported "0 pending rows, yet docs/provenance-allow carries 16 entries
naming OI-34". This row is that mint.

Scope: migrate the labelled rows (the census said 18; re-measure — the
2026-08-20 readability sweep counted 15 dated "(Derived-requirement label,
added <date> — PROVISIONAL, unsigned.)" markers plus SR-053's signed
variant; two rows may have lost labels to later rulings) from the
parenthetical label marker onto the hat-carrying form OI-34's ruling
specifies — coordinate the FIELD SHAPE with WI-484's Phase 0/1 (the
concern/hat reference field: one name, one shape; if WI-484 has not landed,
mint the field per its Phase-0 reconciliation or record the label content
in the existing Hat-derived prose form the rows already use). Each
migrated row's allow entry retires IN THE SAME COMMIT (marker and entry go
together — the standing rule); the snapshot refreshes (post-sign registry
edits); the "unsigned" wording dies with the marker (the rows are signed
since 2026-08-20). Also adjudicate the ONE OI-37 entry (SR-043 Rationale)
the same vacuity report names: its ruling executed 2026-08-18, so either
the residual token retires with this sweep or the reason it stays is
recorded on the entry.

Spine class: these are SR/LLR rationale-cell edits on signed rows —
wording-marker removal, not obligation change, but the drift detector will
report each until the adjudication blesses the batch; land as ONE reviewed
commit with the before/after in the log fragment, the post-sign amendment
discipline.
