## 2026-08-20 — OI-45 and OI-46 rule; the rowless watermark ruling finally gets its row (OI-47)

Deferred open items: none — the watermark ruling this session is named for
was minted, twice narrowed, and RULED within this same session; the pending
queue it entered is empty again. (Re-worded 2026-08-21: the ruled id sat on
the declaration line, and the parser harvests every id in that line's payload,
so a citation there read as a deferral of a row the owner had already ruled.
The id is named in the body immediately below.)

OI-47 is the standing `B`/`REL` watermark mechanism: the decision
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

Also answered for the owner: `human_ratification_through`'s
numeric-to-string conversion was NOT in the queue and never had been — OI-21
ruled shape (i) (the int dial MAPPED onto the stage ladder via
`agent_common.DIAL_HOLDS`, executed by WI-445) and named shape (ii), re-keying
the dial to `DevStg-*` strings, as a future option that "can supersede (i)"
after OI-14 — which ruled 2026-08-13, so the door was open but unexercised.
The owner then exercised it (follow-up, 2026-08-20): the conversion is
DECIDED but sits in deferment — **WI-493** minted directly into
`docs/work/deferred/`, carrying the verified touch surface and the
supersedes-shape-(i) note; it enters the frontier only when the owner wakes
it. Watermark `WI` 492 → 493 in the same commit.

Follow-up, same day: the owner read OI-47 and reframed it — a spent-id
record is over-built, because the ruled documents ALREADY carry the spent
ids; seed and correct from a repo-wide citation census instead, and let the
existing refuse-plus-`--bump-ids` machinery keep catching registry hand
edits. Recorded as option (d) on the row with the recommendation moved to
it (scope caveat: tests/golden carry fabricated ids — `OI-77` in test
source — so the census scope must be declared, and its error direction is
the safe one: over-count burns numbers, under-count re-points history).
The row stays PENDING — the reframing is the owner thinking, not yet the
ruling.

Second follow-up, same day: the owner asked whether tests actually carry
placeholder ids and argued the census needs no scope provisions since this
repo's marks are already seeded. A census was run (`git ls-files` + the id
grammar over the tree, 2026-08-20, this box): tests are saturated
(WI-4010, SR-999, B-99, OI-99) AND non-test prose is too — reviews use
SR-999/LLR-999/TC-999/WI-999 illustratively, plans use B-24,
`gen_open_items.py`'s comments use WI-999, the shipped EXAMPLE.md uses
REPO-1..4 — so an unscoped census would seed B=100/SR=1000/WI=4011, and a
scope tight enough to fix that is the provisioning the owner declined. The
owner's structural point survives and goes further: no future first-seed
exists (every space here is seeded; adopters seed from the zero template),
so NO census ships at all and OI-47 collapses to the one-time correction's
mechanism. The marks are NOT yet corrected (still B=7/REL=3 — the owner's
"already corrected" was ahead of the record); the refusal bites only at
the raising commit (`trace._mark_history_findings` justifies by committed
mark or live max, so a landed raise self-justifies). Options rewritten on
the row: (d) recorded as withdrawn-by-measurement, (e) minted (a one-shot
recorded-correction verb carrying the ruling id), (c) re-priced as a
two-commit replay that is green under existing rules. Recommendation:
(e), else (c).

**OI-47 RULED (owner, 2026-08-20): (e).** The correction verb raises a
named mark with the authorizing ruling id recorded in the watermark
header; the integrity rule accepts a recorded raise and nothing else
changes; the one-time B=8/REL=4 correction lands in the same change and
the SPENT IDS block then retires to a pointer at the row. Execution:
**WI-492**. The mint-to-ruled arc ran inside one session — the surface
built for decisions carried the question for exactly as long as it was
open, which is the OI-41 class working as intended. `docs/status.md`'s
hand-authored watermark bullet is deleted rather than re-pointed: the
ruling it announced is made, and execution is the WI registry's business
(naming the id in status prose would refuse its claim). Bookkeeping for
this commit: watermark `WI` 491 → 492 via `trace.py --bump-ids`; surfaces
regenerated.

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
