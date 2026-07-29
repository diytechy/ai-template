+++
id = "WI-198"
title = "Round artifact filer - DP-NNN directory allocation; tracked stage artifacts; log verdict summary; selected rows filed as queued WIs passing check_trajectory (DP-001 selected plan P5)"
workstream = "unattended"
needs = ["WI-190"]
buildtier = "medium"
order = 194
+++

## Deliverable

WI-198 (2026-07-16, opus build / fable integrate): scripts/plan_artifacts.py - the round's write-side effects: allocate_round_dir (max existing DP-### +1, zero-padded, deterministic, never gap-fill), write_stage (stable-named UTF-8, newline='' byte-stable), append_log_summary (blank-line separated, line-ending preserving), file_selected_wis (Plan-WI table -> queued registry rows: all fresh ids allocated BEFORE predecessor mapping so fan-in rows resolve; the round's parent WI appended to every row; empty Deliverable per R-A; BuildTier from tier_map default medium; csv-module quoting-safe append preserving the file's line-ending convention + terminating the prior last row). Verified through the REAL check_trajectory on a fixture repo (exit 0 plain AND --strict). 14 tests. Spine LLR-074/TC-074 under SR-061 (provisional); Proposed IF-061 (source; write seam - nearest IF-054/IF-023 are read-side), CMP-004; scaffolded.
