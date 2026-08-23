+++
id = "WI-278"
title = "Branch integration & CI-on-branch — implement the owner ruling from OI-8: open/maintain a PR so branch pushes run CI (or add the dev branch to on.push.branches in test.yml) and merge in reviewed slices rather than letting the delta grow"
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
order = 275
+++

## Deliverable

OI-8 ruled 2026-07-25 in favour of the trigger edit over the PR: .github/workflows/test.yml now runs on push to EVERY branch (branches: ["**"]), so a development branch cannot go ~845 commits without a hosted run just because nobody kept a PR open, and naming the current branch cannot re-lapse at the next one. The pull_request trigger stays for the one case push cannot see (a fork's PR) behind a per-job fork-only guard, so no job double-runs. Guard: test_meta_ci_runs_on_every_branch_push_exactly_once, verified to fail against both the branches-[main] and the guard-removed defects. Merge-to-main remains a separate owner call under docs/push-policy: human.
