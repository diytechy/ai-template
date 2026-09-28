+++
id = "WI-557"
title = "The delegated-decisions record: per-run TOML file, close-time obligation under the decision_recording dial (OI-74/OI-75)"
specref = ""
workstream = "process"
sr_refs = []
needs = ["~WI-552"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Built by one builder in two commits with two Codex Sol rounds (wave-5
arbitration rulings 39 to 43), SOUND at f1020ac1. It realises the owner's
OI-74 and OI-75.

1. **The format** is a template, `project-trajectory/decisions.template.toml`,
   scaffolded to `docs/decisions/run-000-example.toml`. There is one TOML
   file per delegated run at `docs/decisions/<branch>.toml`, whose entries
   are tables with the required keys `decided`, `alternative`,
   `reversal_cost`, `why_not_escalated` and `review = ""`, plus a top-level
   `high_risk` hoist. A `-000` entry is inert. `kitlib/decisions.py` owns the
   path and the reader. This lane's own record is
   `docs/decisions/build-wi-557.toml`.
2. **The dial** is `[attestation] decision_recording = "off" | "record" |
   "escalate-first"`. The template ships "off", and this repository sets
   "record". Under "record" and "escalate-first", the merge ladder refuses a
   lane that closes (complete, cancelled or partial, per OI-74's "every
   delegated run") without its record, naming the path as a hold for a
   person. A malformed entry is reported, never refused. The dial's
   configuration is judged before any record is read, and the reader and
   validator share one normalization.
3. **The doctrine** is a PROCESS_OPTIONS layer, "Delegated decisions
   record", with its applies-when index row. It holds the routing table, the
   one-way confidence ratchet, the rule that the record is not an exit, and
   the overturned-entry path (item 4). The supervisor-resume clause has no
   surface left: the supervisor prompt the spec names lived in
   docs/status.md and is retired, and no prompt template carries one. The
   loop's own build and adjudication sessions are pointed at the record
   through `agent_loop.session_body`, and the process-options "Delegated
   decisions record" layer states the obligation for a supervisor's sitting
   (ruling 40).
5. **Tests** cover the format check and the dial's three values on a
   scaffold (TC-292 to TC-294, red first). PROCESS_OPTIONS.md grew by 3,249
   bytes (watched, re-stamped), and the byte-budget-guard skill stays at
   4,493 of 5,000.

New Drafted rows: SR-225 (a labelled derived requirement on SN-029,
UNATTENDED-OPS lens), LLR-282 to LLR-284, TC-292 to TC-294, IF-255 (the
record file) and IF-256 (the `kitlib.decisions` call). Beyond the dial,
`adjudication_review` is now validated trimmed and case-folded, matching
its reader.

For adopters and the next coordinator: with "record" set, a lane closed
through the kit's merge slot needs its record. The coordinator's hand
squash-merges do not pass that ladder.

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
