# {{PROJECT_NAME}}

<!-- Build this README out from the PROJECT BRIEF at kickoff (the kit's
     KICKOFF_PROMPT.md): the Vision below, who it serves, what it does, and how
     to evaluate it. The README is the human front door — it exists from day
     one and grows with the project. Replace every "fill in", then delete this
     comment. -->

## Vision

**PROJECT-VISION:** *(fill in: 1–3 sentences max — for whom · what · the one
thing that makes it worth building. Seeded from the kickoff brief's "Goal"
line.)*

This is the **canonical home** of the project's purpose. Every other document
(the needs registry, AGENTS.md's one-liner) *points at this tag* — grep
`PROJECT-VISION` or link `README.md#vision`; never re-author a variant.

## Run it

Double-click the launcher for your platform — no commands to remember:

| Platform | Launcher |
|---|---|
| Windows | [run.cmd](run.cmd) |
| Linux | [run.sh](run.sh) |
| macOS | [run.command](run.command) |

Each is a short, readable script that starts the product from the repo root.
The underlying command lives in the launcher's `RUN_CMD` slot — document it
here too once wired: *(fill in: the launch command and what to expect)*. For a
pure library, delete the launchers and this section and describe usage instead.

## Getting started (contributors)

The onboarding ladder (docs/process.md §7) — each rung a readable,
consent-first script that explains itself before acting:

1. **Fresh machine → checkout:** double-click `scripts/onboard.*` (`.cmd`
   Windows · `.sh` Linux · `.command` macOS).
2. **Workstation:** `scripts/dev-setup.*` — detects and reports by default;
   installs only with consent.
3. **Product toolchain:** `scripts/setup.*` — dependencies + the pre-commit
   hook.
4. **Verify:** `scripts/check.*` — the gate harness; green means you're set.

## Development

This repo follows a gated, requirement-traced process. The working brief is
[AGENTS.md](AGENTS.md); the method is [docs/process.md](docs/process.md). Start
with the code map in [docs/architecture.md](docs/architecture.md) and the
current state in [docs/status.md](docs/status.md).

**Resuming agent work:** double-click `agent-resume.*` (root) to boot the
right agent session — or the unattended coordinator loop — under the declared
gate policy. Inert until its `AGENT_CMD` slot is wired; wiring it (typically
with the agent's permission-bypass flag) is your explicit consent to
unattended sessions — see docs/process-options.md "Unattended operation". Not
using agents? Delete the `agent-resume.*` launchers and this note.
