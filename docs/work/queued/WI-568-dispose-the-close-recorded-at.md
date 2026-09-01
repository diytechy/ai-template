+++
id = "WI-568"
title = "dispose: the close recorded at docs/handbacks/WI-508-wi508-architectural-remap.md - cancel / defer / draft a successor / surface an open item (a disposition row never closes early; R3)"
workstream = "process"
specref = "docs/work/partial/WI-508-architectural-remap-program.md"
buildtier = "strong"
safety_class = "adjudication"
brief = "disposition"
+++

## Context

The closed spec is `docs/work/partial/WI-508-architectural-remap-program.md`.

Its per-close report is `docs/handbacks/WI-508-wi508-architectural-remap.md` — READ IT FIRST. The report is the close EVENT's own immutable record: what the lane claims it delivered and did not, the commit range, the keep/discard split, and the review tier it suggests. The lane's claimed outcome is a CLAIM under judgement here, not this row's premise.

Outcomes (R3): cancel / defer / draft a successor / surface an open item. Continuing the work MINTS A SUCCESSOR (drafted in THIS row's `## Dispositions` section, carrying `supersedes`), never a revival of the closed row — a closed row is never re-opened and a scope definition never changes to mean something else. An override moves the byte-identical spec to the corrected terminal folder; the report stays on record as the claim it was. An open item goes to docs/requirements/open-items.toml.

**Named for this adjudication (WI-555 round 005, 2026-09-01):**

- The `580df781` keep/discard explicitly includes the LLR-203 / LLR-204 `Drafted` -> `Approved` flips: stand or revert. They were `Drafted` on trunk at `6d3d9db4` and are `Approved` at `551d1b2c`; the flip is loop-permitted under `human_approval_through = "DevStg-Needs"`, so the question is disposition, not authority.
- It explicitly includes the `docs/archive/last_approved/` baseline move for the off-spine registries: the merge `979c3e5f` carried the branch's snapshot bytes (`580df781` / `4824c0ba`) onto trunk, shifting the baseline off the pre-merge anchor `6d3d9db4:docs/archive/last_approved` (last written at `13593db9`) and collapsing `docs/ratify/CURRENT.md`'s off-spine census from "132 changed, 30 added, 3 removed" across nine rulings to "1 changed, 0 added, 1 removed (WI-553)". Restore trunk's baseline to the `6d3d9db4` bytes for `interfaces.toml` / `external.toml` / `components.toml`, or let the absorption stand — owner-owed; mint an OI through this row's `open_item` cell if the adjudicator judges it needs the owner.
- The handback report's `## Delivered` sentence "the four Drafted slice-1 spine rows" is inaccurate: the true split is 2 `Approved` (LLR-203, LLR-204) / 2 `Drafted` (TC-199, TC-200). Read the archived spec at `docs/work/partial/WI-508-architectural-remap-program.md` and the WI-555 log entries in `docs/log.d/WI-555-wi508-partial-close.md` as the corrected record; the report is immutable and stays as the claim it was.
