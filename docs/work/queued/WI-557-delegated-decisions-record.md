+++
id = "WI-557"
title = "The delegated-decisions record: per-run TOML file, close-time obligation under the decision_recording dial (OI-74/OI-75)"
specref = "docs/requirements/open-items.toml#OI-74"
workstream = "process"
sr_refs = []
needs = ["~WI-552"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

`OI-74` and `OI-75` RULED 2026-08-31 (record
`docs/log.d/2026-08-31-owner-rulings-oi74-75.md`; evidence base
`docs/knowledge/decision-routing.md`): delegated runs record their decisions
in one pure-TOML file per run, the owner reviews IN PLACE by filling each
entry's `review` cell with any free string, and a new `[attestation]` dial
governs the obligation. The record is never an exit — OI-70/OI-73's queued
successor and minted OI remain the only ways work routes; this file is what
the owner is TOLD about calls already made. The soft edge on `WI-552`
orders this behind the close-machinery rework where the scheduler can
manage it; nothing here blocks on it.

## Done-when

1. The format exists as a template: one TOML file per delegated run at a
   declared per-run path (the naming keeps the medium conflict-free across
   branches, like `docs/log.d/`), entries as tables carrying REQUIRED keys
   `decided`, `alternative`, `reversal_cost`, `why_not_escalated`, and
   `review = ""` — empty means unreviewed, any owner string means reviewed,
   no machinery reads the review state. A `-000` example entry keeps the
   template copy-ready and trace-inert. A top-level high-risk hoist names
   the entry numbers the writer judges deserve the owner's eyes first.
2. The dial exists: `decision_recording = "off" | "record" | "escalate-first"`
   in `[attestation]`, one `key = value` line under the IF-037 format
   constraints, template ships `"off"`, this repo's `docs/process.toml` sets
   `"record"`, structural parity held by the dogfood-sync test. Semantics as
   ruled: `off` — no obligation; `record` — a delegated run's close owes the
   record file, the handback-report precedent for an owed close artifact
   (missing file at the close is a refusal, malformed entries warn);
   `escalate-first` — doctrine directs sessions to prefer the OI-70/OI-73
   exits over deciding.
3. The doctrine lands where delegated sessions read it: a PROCESS_OPTIONS
   opt-in layer (applies-when: delegated or unattended runs) stating the
   routing table (action fields and counts — registry, spine and kit-file
   touches record at minimum; irreversible or external acts take the ruled
   exits; scratch and generated-file work decides silently — initial
   contents adjustable by the owner), the one-way confidence ratchet (low
   confidence or reviewer dissent may promote a decision to more scrutiny,
   never the reverse), and the record-is-not-an-exit rule. The supervisor
   resume prompt's recording instruction points at the format instead of an
   ad-hoc file.
4. An overturned entry's path is stated in the doctrine: the owner's review
   note names it and a WI is minted to undo or redo — the record itself
   never carries the work.
5. Tests drive the format check and the dial's three values on a scaffold;
   the full suite stays green; byte budgets respected on any capped doc
   touched.
