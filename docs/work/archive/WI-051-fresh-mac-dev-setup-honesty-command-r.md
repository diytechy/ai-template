+++
id = "WI-051"
title = "Fresh-Mac dev-setup honesty + .command rung"
workstream = "scripts"
sr_refs = ["SR-032"]
needs = ["WI-027"]
order = 50
+++

## Deliverable

Found live on the owner's Mac (commit d9d434e, 2026-07-10): /usr/bin/{python3,git} are CLT placeholders that satisfy command -v, so dev-setup reported [ok] on a toolchain that did not exist. real() probe (xcode-select -p) in meta + template dev-setup.sh; pytest-cov added to the meta check rows and --install (its absence failed the suite's tests+coverage step); the report prefers ./.venv so tools no longer read [missing] right after --install; new dev-setup.template.command double-click rung (uname-guarded; exec bit via bootstrap MAPPING; kit README row) verified live (dialog popped -> CLT installed -> honest report). Failing-first tests in test_onboard_devsetup.py. SR-032 text unchanged - no re-attestation impact.
