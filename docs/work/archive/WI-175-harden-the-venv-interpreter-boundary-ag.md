+++
id = "WI-175"
title = "Harden the .venv/interpreter boundary against coverage debris (VS Code pin + dev-setup ambient warning)"
workstream = "scripts"
needs = ["WI-104", "WI-105"]
buildtier = "medium"
order = 174
+++

## Deliverable

Owner-directed (2026-07-15): 3259 gitignored .coverage.* fragments were found stranded at root. Traced to a full --cov run on the AMBIENT global C:\Python38 (pytest-cov 4.1.0, the pre-5.0 racing version .coveragerc/WI-105 document), NOT the pinned ./.venv (pytest-cov 5.0.0) which would have combined cleanly. So: not a missing cleanup step and not a low pin - WI-104's pins already sit above the break and 5.x is the 3.8-floor ceiling (pytest-cov 6.0 dropped 3.8). Three recs. Rec 1 (prefer ./.venv in the harness/hook) was ALREADY shipped - project-trajectory/hooks/pre-commit probes+prefers ./.venv and check.py runs the coverage command under sys.executable (which the hook makes the venv); the only residual is a direct non-hook global --cov run, the owner-disclaimed local call, and re-exec of the kit-shipped check.py was considered+declined (downstream blast radius). Rec 2: .vscode/settings.json pins the workspace ./.venv as the default interpreter + wires pytest as the test runner so VS Code Run/Test use the pinned toolchain not a global python. Rec 3: scripts/dev-setup.{sh,ps1} gained a warn-only ambient-interpreter probe (never changes the exit code) that names a pre-5.0 pytest-cov on the PATH python and points at ./.venv - verified live on Windows (flagged C:\Python38 pytest-cov 4.1.0). Meta-only; the downstream dev-setup.template.* and check.py interpreter contract are untouched. Test: test_onboard_devsetup.py::test_meta_devsetup_warns_on_racing_ambient_pytest_cov (textual, both twins). Off-spine dev tooling - no SN/SR/LLR/TC change, no re-attestation.
