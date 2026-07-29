+++
id = "WI-118"
title = "Test-suite hermeticity - scrub inherited coordinator routing env"
workstream = "scripts"
needs = ["~WI-107"]
order = 117
+++

## Deliverable

Found live 2026-07-12, first coordinator-launched driver session: the agent-resume launcher exports the AGENT_* routing contract (AGENT_CMD / AGENT_MODEL_MAP / AGENT_TIER_MAP=BUILD=strong / ...), the pytest suite inherits it, and 8 agent_loop tests fail - the ambient AGENT_TIER_MAP re-routes their scaffold loops to 'no routable model at tier strong' - so the unattended layer could never produce a green commit bar from inside its own sessions. Fix: tests/conftest.py scrubs the whole AGENT_* namespace from os.environ at conftest import, before any test copies the env; no test reads these vars from ambient (each sets its own in the child env it builds). Verified live: the 8 failures reproduce with the vars present and the full suite reads 640 passed / 34 skipped with the contamination still in the launching shell.
