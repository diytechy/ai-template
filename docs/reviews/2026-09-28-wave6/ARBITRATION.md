# Wave 6 arbitration

Under the owner's 2026-09-28 roles, a dispute between a builder (Codex Sol)
and the reviewer (Claude Sonnet), or a finding the coordinator doubts, goes to
a fresh independent Opus agent that directed none of the work. It rules; the
coordinator records the ruling here with its reasoning. A finding the builder
accepts needs no arbitration, and most of this wave's did not.

1. **WI-732 (0e8616b9): where DA-016 and DA-017 land. For the builder.**
   The Sonnet review held that both new assumptions belong at B-10 (the
   model-runner crossing, where the citing SRs' `boundary_refs` sit and
   where DA-008 lands), not B-09 (the owner's read of the spine and views).
   The builder had chosen B-09 deliberately.

   **Ruling:** DA-016 → B-09 and DA-017 → B-09. The reviewer's major does
   not stand.
   - "Where the outcome lands" means the stakeholder's crossing, not the
     seam where the system meets the world. This is stated in the registry
     header (`assumptions.toml:19-24`), the tier plan
     (`2026-09-20-validation-gap-and-the-assumption-tier.md:518-524`) and
     approved SR-195.
   - Both rows serve needs whose stakeholder, STK-01, is EXT-006. Its
     crossings are B-02 and B-09, and EXT-001 mediates for it. B-10 belongs
     to EXT-005.
   - The kit's own `reach_gaps`, run in memory, is clean at B-09. At B-10,
     alone or added, it flags "reaches none of the needs it serves". Once the
     assumption gate is armed, that becomes an SR-205 boundary-gate failure.
   - DA-008 lands at B-10 only because it is a fidelity row (realized by
     SUR-001, which emulates EXT-005). Fidelity rows must land on the
     emulated party's crossing. DA-006, a runner premise with no surrogate,
     correctly sits at B-09. No existing row is misplaced.
   - A requirement's `boundary_refs` (where the system acts) and an
     assumption's `effect_at` (where the stakeholder meets the outcome) are
     different edges by design. The one check tying them, SR-212's Boundary
     arm, judges only `form = "interface"` rows, and no SR declares one.

   **Finding for later (kit design, not this lane):** SR-195 and SR-212's
   Boundary arm can collide.
   - The case: an SR later given `form = "interface"` at a crossing whose
     party is neither a stakeholder nor a mediator (B-10, B-11).
   - That SR would need an assumption landing there, and SR-195 and SR-205
     penalise any non-fidelity landing there. Only a waiver, or a fidelity
     row with a surrogate, satisfies both.
   - It cannot fire today, because no SR carries a Form cell. It is recorded
     as a kit gap in the log, for the assumption tier's C3/C4 work, before
     any SR is classified interface-form at B-10 or B-11.
