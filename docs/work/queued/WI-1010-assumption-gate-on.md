+++
id = "WI-1010"
title = "This repository turns its assumption gate on, once its four steps report nothing"
workstream = "requirements"
sr_refs = ["SR-205", "SR-212", "SR-206"]
needs = ["~WI-1008"]
specref = "docs/plans/2026-11-11-test-tiers/HANDOFF.md#126-progress-log"
buildtier = "medium"
safety_class = "spine"
priority = 3
+++

## Context

Filed by hand on 2026-11-18 at the operator's direction: "turn on the
assumption check when ready". `docs/process.toml` holds
`[checks] assumption_gate = false`. Its comment says turning it on is this
repository's own act, taken once its requirements' assumptions are accepted.
With the gate off, `check_assumption_gate.py` prints the same findings as
advisories, so what turning it on would fail is known. On 2026-11-18, after
act seq 183, it was 91 findings:

| Step | Findings | What they are |
|---|---|---|
| `assumption-gate` | 46 | a requirement relies on an assumption that is `Drafted` (all 17, DA-001 to DA-017) |
| | 9 | a fidelity assumption whose surrogate is `Drafted` (SUR-001 to SUR-003) |
| | 21 | a requirement cites no assumption and records no `coincident` waiver: SR-024, SR-129, SR-224, SR-226, SR-228 to SR-234, SR-236 to SR-238, SR-241 to SR-247 |
| `crossing-allocation` | 9 | SR-229, SR-230, SR-231, SR-232, SR-234 and SR-235 name crossings no cited assumption lands on |
| `interface-allocation` | 6 | the same rows: five reached by no boundary interface, SR-229 reached by IF-080, which no cited assumption bridges |
| `assumption-evidence` | 0 | |

SR-033, SR-223 and SR-225 are not in the list, because the gate's joint skip
passes them. WI-1008 writes their premises anyway. Doing it first means one
acceptance act covers every new assumption, hence the soft edge.

The operator rules on `docs/open-items.html`, and it does not show
assumptions or surrogates: its §2 renders SR chains and stakeholder needs
only. `docs/status.md` already records the missing view. The Markdown brief
(`trace.py --accept modified`) renders them, as SR-203 asks.

## Done-when

- [ ] Each of the 21 requirements cites an assumption that carries it to its
      needs, or records a `coincident` waiver. SR-229, SR-230, SR-231,
      SR-232, SR-234 and SR-235 each have their crossings and boundary
      interfaces bridged or waived. A new
      assumption row is `Drafted`.
- [ ] The assumptions and surrogates owing an acceptance are shown where the
      operator rules. Recommended: `docs/open-items.html` §2 renders them, as
      the brief does, so the operator reads one page. The alternative is to
      point the operator at the regenerated brief.
- [ ] The operator's act accepts the assumptions and surrogates and
      re-accepts the amended requirements. That act is the operator's.
- [ ] All four `check_assumption_gate.py` steps report 0 findings. Then
      `[checks] assumption_gate = true` in `docs/process.toml`, with its
      comment saying when it was turned on, and `check.py` passes with it on.
