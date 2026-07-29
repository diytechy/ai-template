+++
id = "WI-302"
title = "dev-setup quoted a remedy that CANNOT satisfy the floor it enforces - the runtime hint sent macOS users to `xcode-select --install` / dev-setup.command, but the Command Line Tools ship Python 3.9, below the 3.11 floor the same line reports as unmet, so following the hint returned the reader to an unchanged report with no exit from the loop (hit live 2026-07-25: owner ran dev-setup expecting it to seed the interpreter). Root cause of the confusion: dev-setup DETECTS a runtime and never provisions one - it pip-installs the dev tools INTO ./.venv, which needs a Python to already exist."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
order = 299
+++

## Deliverable

Fixed 2026-07-25. (1) The runtime hint is now platform-aware and names provisioners that actually ship 3.11+ (uv / brew / python.org on Darwin; uv / distro package / python.org elsewhere; winget / uv / python.org on the PowerShell rung), and explicitly warns that xcode-select and the Command Line Tools are NOT a 3.11+ source. Fixed in the meta-repo script AND in dev-setup.template.{sh,ps1}, since the same dead-end shipped downstream. (2) New offer_python(): ONE consented offer of a runtime, gated on a provisioner ALREADY installed (uv, pyenv, brew) - the offer_cli pattern held to a stricter line - falling through to the printed hint when none is present, and re-running discovery via the new discover_py() after an accepted install rather than dead-ending. (3) The fail-closed exit now repeats the actionable hint and notes a managed interpreter may need a new shell. DESIGN RULING (owner, 2026-07-25): the kit never bootstraps a provisioner and never pipes a downloaded script into a shell - a language runtime is not a leaf tool (a wrong one shadows the system interpreter beyond this repo) and these scripts SHIP, so curl|sh would push a supply-chain surface onto adopters who never chose it. Borrow trust a developer already extended; never manufacture it. That invariant is now pinned executably by test_no_setup_script_pipes_a_remote_script_into_a_shell across all 8 setup scripts, scanning executable lines only. Verified live on the owner's Mac: no-provisioner path offers nothing and exits with a real hint; with a fake uv on PATH the offer fires, declines gracefully on a closed stdin, and re-discovers after accept.
