## 2026-11-16 — WI-999: live component rows carry a derivation record, and the component pass checks it

Deferred open items: none.

Built on the maintenance branch `maint/wi-999`, outside the lane workflow, at
the operator's direction: no claim, no lane review rounds, commits made with
the hook bypassed. Every commit leaves `trace.py --strict` at exit 0.

- **Schema:** the component tier declares eight cells (`candidates`,
  `objective`, `constraints`, `scores`, `selected`, `ruling`, the optional
  `override`, and `derivation`); the template's `-000` row declares each.
- **Backfill and act:** CMP-006 holds the record OI-130's ruling states (P5,
  P3, P4; minimize cut; one-home-per-behaviour violated by all three; P5=140,
  P3=152, P4=235; P5 selected, no override), and CMP-007..009 cite it. The act
  (seq 182) names the ruling's log record in `--approves` and re-attests the
  four rows. Previewed before it ran, it copied only `components.toml` and
  also absorbed CMP-006's `notes` amendment, pending since the 2026-08-30
  copy.
- **Rules:** `trajectory_arch.derivation_record_findings`, called from
  `component_findings`, reports absent, incomplete, malformed and inconsistent
  records; TC-166's evidence names its ten tests.
- **Left open:** the review bar (the branch's cross-family review runs next).
  LLR-172's `Detail` still says "NOT BUILT YET" and TC-166's `Method` still
  says "trace.py's component pass"; both are approved cells, so correcting
  them is an approval act for the operator, not part of this build.
