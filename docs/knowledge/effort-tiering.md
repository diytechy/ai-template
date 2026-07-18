# Per-task reasoning-effort evidence

This pack preserves why the loop distinguishes mechanical gathering from
design-shaping synthesis. Tier assignments themselves remain WI data and
process policy, not facts copied here.

## Findings retained

The [effortmining project](https://github.com/nagisanzenin/effortmining)
(retrieved 2026-07-15) reports roughly 450 preregistered runs on one model. Its
calibrated dispatch used 64.7% fewer output tokens than uniform `xhigh` at the
same aggregate pass rate. The useful direction is supported, but the calibration
is not portable: it used one model, small per-cell samples, and self-contained
tasks that sometimes saturated at low effort.

The most important negative result is qualitative: a low-effort worker invented
a plausible ticket identifier in a composite research task. That makes low-tier
research output suitable for directed gathering, not for an unverified verdict.
Context can also change the required tier: a question that passed alone failed
inside a larger job.

## Application here

- Send bounded search, extraction, and formatting to lower tiers when the
  coordinator can verify their output.
- Keep synthesis, design choices, and spine-touching work at the WI's declared
  tier; never silently downgrade the route.
- Verify load-bearing gathered claims against primary evidence and use a fresh,
  grounded second opinion for research deliverables.
- Treat calibration as model- and workload-specific. Measure before changing a
  tier map; do not infer quality from token savings alone.

## Failed or bounded approaches

- Uniform maximum effort wastes tokens after quality saturates.
- Uniform low effort can fabricate plausible details.
- Importing another project's calibration table without local evidence turns a
  measured result into an unsupported policy.
