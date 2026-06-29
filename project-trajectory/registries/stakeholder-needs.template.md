# Stakeholder Needs (SN-###)

Owned by the **Stakeholder** hat — whoever the system serves: an end user, an
operator, or **another system** (represented by its owner/integrator).
Plain-language needs + edge-case expectations. Engineering translations live in
`system-requirements.csv` (referenced by `SN-Refs`); do not restate them here.
Priority: **M**=Must · **S**=Should · **C**=Could.

## Core needs

| SN-ID | Need (plain language) | Why it matters | Priority | Acceptance intent (how we'd know it's met) |
|---|---|---|---|---|
| SN-000 | _EXAMPLE — replace this row; number real needs sequentially (the `-000` id is a placeholder the tooling ignores)._ | | | |

## Edge-case expectations

How the system should behave when things go wrong (the highest-value part — be
specific; the System Engineer turns each into measurable SRs).

| SN-ID | Scenario | Expected behavior |
|---|---|---|
| SN-0xx | Interruption / power loss / killed mid-operation | |
| SN-0xx | Invalid / corrupt / unsupported input | |
| SN-0xx | Resource exhaustion (disk / memory full) | |
| SN-0xx | Missing dependency / wrong version | |
| SN-0xx | Output target removed / locked / unwritable | |
| SN-0xx | Unattended/automated run (must never block; clear failure) | |
| SN-0xx | First-run setup & discoverable docs / quick-reference | |
