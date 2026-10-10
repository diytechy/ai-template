+++
id = "WI-885"
title = "adjudicate: LLR-045, TC-082 - approved/routed cell(s) amended on merged trunk 39c3514..d0a4b62 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-045", "TC-082"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second sitting is held (the re-mint trap, S11 plan §4.2; owner-agreed close, 2026-10-03). WI-847's in-lane amendment sitting 001 (`docs/reviews/wi-847/001-ADJUDICATE-7825c62.md`) ruled LLR-045 and TC-082 MEANING and re-attested each (act seq 92, docs/archive/last_approved/acts.toml), and at the landing d0a4b623 the system, low-level and test registries are byte-equal to their approved snapshots under docs/archive/last_approved/.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-045 `Detail`: 'Schedules review-policy sessions in managed mode, constructs redacted prompt-map briefs, parses verdicts, logs selectio…' -> 'Schedules review-policy sessions in managed mode, constructs redacted prompt-map briefs, parses verdicts, logs selectio…'
- TC-082 `Expected`: 'Managed scheduling matches policy with redacted logged routing; bad prompts fail preflight; unmanaged mode stays legacy.' -> 'Managed scheduling matches policy with redacted logged routing; bad prompts fail preflight; unmanaged mode stays legacy…'
- TC-082 `Method`: "Run review-policy 0/1/2, prompt-map, redaction, selection logging, verdict, and unmanaged cases. The queue's phases are…" -> "Run review-policy 0/1/2, prompt-map, redaction, selection logging, verdict, and unmanaged cases. The queue's phases are…"

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
