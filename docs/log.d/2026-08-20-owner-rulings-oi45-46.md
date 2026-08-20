## 2026-08-20 — OI-45 and OI-46 rule; the rowless watermark ruling finally gets its row (OI-47)

Deferred open items: OI-47 — minted THIS session and deliberately left
pending. It is the standing `B`/`REL` watermark mechanism: the decision
announced on two surfaces (`external.toml`'s SPENT IDS header,
`docs/status.md`'s "ONE ruling still owed" bullet) that OI-41's founding
evidence named as the sharpest announced-but-rowless instance — and that
the 2026-08-20 batch-close RESUME queued for ruling still without an id.
The owner noticed the absence and asked why it never surfaced on the
open-items view; the answer is that the 2026-08-18 mint session deliberately
skipped it ("it needs no brief because the question is stated there"), a
call the review era has since retired. Pending, on the surface built for it,
with options and a recommendation, is its honest state until the owner rules.

The owner ruled the two pending briefs in one message (2026-08-20); each row
flipped `pending -> ruled` with the ruling recorded at the top of its
recommendation cell and its executing WI queued in the same commit.

| OI | Ruling | Execution |
|---|---|---|
| OI-45 | **(b) RETIRE THE ARM, with an owner scope note on who may still move a Status cell.** What retires is MECHANICAL ratification — a scripted path moving a Status cell with no judgment behind it. The note: an LLM session or adjudicator is fully expected to flip a row's Status to `Approved` and further to `Founded` for spine content past the human approval gate/level (`human_ratification_through`) — at the human's request, or when working through content the declared level does not hold to human ratification. Bites on comments and docstrings, not code paths: the record says "not MECHANIZED", never "no agent may ever move a Status cell." Also answers the authority half of D-9 consequence 2: an agent-authored `Founded` under those conditions is sanctioned. | **WI-490** |
| OI-46 | **(1a) + (2a) as recommended** — `subagent_gate.py`'s present-but-unparseable arm aligns to its twins' fail-closed reading (absence stays allow, the ruled opt-in posture untouched), and the session banner surfaces `out/subagent-gate.log`'s tail count so the fail-open record becomes auditable. M-13 tests extended; RESYNC entry owed. | **WI-491** |

Also answered for the owner, nothing minted: `human_ratification_through`'s
numeric-to-string conversion is NOT in the queue and never was — OI-21 ruled
shape (i) (the int dial MAPPED onto the stage ladder via
`agent_common.DIAL_HOLDS`, executed by WI-445) and named shape (ii), re-keying
the dial to `DevStg-*` strings, as a future option that "can supersede (i)"
after OI-14 — which ruled 2026-08-13, so the door is open but the re-key is
its own owner decision, not a filed item. `agent_common.py`'s "THE DIAL DOES
NOT MOVE" block is the standing record.

Bookkeeping in the same commit: watermark `OI` 46 → 47 and `WI` 489 → 491 via
`trace.py --bump-ids`; `docs/status.md`'s hand-authored watermark bullet
re-pointed at OI-47 (the ruling is unchanged and still owed — what changed is
that the surface built for decisions now carries it); open-items.html, the
dashboard and the status block regenerated. `gen_open_items --check` warns
(exit 0, ARM-2 weak-by-design) that the frontier-grind fragment declares
OI-45/46 deferred while the rows now read `ruled` — accurate history from the
session that deferred them, left standing. Commit bar: smoke
(`python -m pytest -q -n auto -m smoke`) 1245 passed / 5 skipped, 77.9 s wall
on this box this run — past the 60 s ceiling, one box one data point;
`check_docs.py --stale` 0 broken.
