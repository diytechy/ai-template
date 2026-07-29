+++
id = "WI-111"
title = "dev-setup --install delta-awareness - nothing-to-do fast path"
workstream = "scripts"
needs = ["WI-109"]
order = 110
+++

## Deliverable

Owner-asked 2026-07-12 (wants to test dev-setup from their machine with no unnecessary installs): audit + fix. Audit: --check was already report-only (exit 0, zero mutations) and the agent CLIs are hint-only rows (never auto-installed under any mode); but a consented --install unconditionally ran `pip install --upgrade pip` + the 4-tool pip line and prompted even with a complete ./.venv - exactly the unnecessary-install class the owner ruled out. Fix: both twins (scripts/dev-setup.{sh,ps1}) gain a delta-aware fast path - when ./.venv already imports ruff+pytest+pytest_cov+xdist, report 'nothing to install' and stop BEFORE the prompt and the pip self-upgrade (the hooksPath floor wiring still runs: local idempotent git config, not an install; ps1 reuses HasModule, which already probes the venv interpreter). Verified LIVE on this machine (complete venv): report + floor no-op + fast-path line, no prompt, no pip, exit 0. Missing-tool path unchanged (prompt; pip no-ops already-satisfied packages). Textual fast-path assertion on both twins added to test_onboard_devsetup (executing --install in a test would prompt/mutate). (WI-112 later reshaped the fast path from exit-0 to skip-section so the agent-CLI offers still run.)
