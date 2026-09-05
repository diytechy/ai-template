<!-- DISPATCHER NOTES (stripped before the prompt is sent)

     CONSOLIDATION (the 2026-09-02 backlog-restructure plan §1.1-§1.5). This
     brief REPLACES `adjudicate-conflict`, which had a template and a verdict
     grammar and never had a mint, an assembler or a reader for its `needs=`
     field. Its three questions survive here verbatim; what is new is the
     fourth exit — CONSOLIDATE — and the census that mints this row.

     WHEN IT IS SENT. A census over the QUEUED rows only, run from an IDLE
     station with no other adjudication queued or active. It clusters rows by
     the mechanical pre-filter (near-duplicate title, shared SR-Refs, shared
     SpecRef) plus two signals a queue accumulates on its own: rows commissioned
     by ONE plan document or open item, and rows whose SR-Refs reach the same
     LLR `Module`. The cluster is fixed at the mint in the row's typed
     `Adjudicates` cell — this session judges THOSE rows and no others.

     WHY IT CANNOT RECURSE. The row carries a `Digests` cell: the queue digest
     and the spine digest the mint saw. The census refuses to mint again while
     a `consolidate` row with that queue digest is queued, active OR archived —
     a queue state that has been judged is never judged again. This
     consolidation's own successors change the queue digest, so a later census
     sees a genuinely new state; {prior} is what stops it re-litigating this
     verdict, and re-absorbing a row an earlier consolidation minted is a
     RETURN-TO-DRAFT of THAT judgement, which pages the owner.

     Slots (single-brace, strict fill):
       {candidate}   the cluster's rows, frontmatter + Context + Done-when.
       {open_rows}   every OTHER open row as id, title, sr_refs, needs.
       {spine}       the SR/LLR rows the cluster cites, id + normative text —
                     or the literal "(the cluster cites no SR/LLR)".
       {mechanical}  the pre-filter findings for this cluster, one per line.
       {digests}     the queue + spine digest pair this verdict is recorded
                     against, so a stale verdict is detectable rather than
                     assumed fresh.
       {prior}       the absorb sets of every ARCHIVED consolidate row.
       {verdict}     the repo path this session writes its verdict to.
       {wi}          this adjudication row's own id, for the result trailer.

     THE TYPED CARRIER. The outcome and its targets ride in a `## Consolidation`
     TOML block in the ROW'S OWN SPEC, not in the verdict file, for two reasons.
     `handback.close_adjudication` is handed `(root, branch)` and nothing else,
     so it can read the lane's tree and not a path only `agent_loop` knows; and
     an outcome recovered from prose is the `NEEDS-HUMAN` fold (WI-417) —
     control flow must be a typed field. The `absorbs` set is deliberately NOT
     in that block: it is the `supersedes` list of the `## Dispositions` draft,
     which is the value the mint actually uses.

     THE MACHINE LINE'S COUNTERS ARE RECONCILED, not ignored and not a second
     source. `consolidate.reconcile_refusal` refuses the close when the verdict
     file's `OUTCOME:` word disagrees with the block's `outcome`, when `absorbs=`
     does not name exactly the ids the draft supersedes, or when `needs=` does
     not name exactly the waiters the block's `edges` declare. The typed block
     and the draft DECIDE; the counters must agree with them or the close stops.
     Every judging brief owes one machine line (prompts/README.md's authoring
     rule), so the honest shape is a checked restatement rather than a counter
     nobody reads.
-->

You are an INDEPENDENT adjudicator launched by the unattended coordinator. A CLUSTER of work items is sitting in the ready queue, where lanes will claim them one at a time and build them side by side. Before that happens, one question:

    Do these rows CONTRADICT the current spine, overlap each other in a way that would make two lanes fight, or ask for something already answered — and if so, are they ONE work item wearing several ids?

Mechanics have already checked what mechanics can check — near-duplicate titles, overlapping `sr_refs`, a shared spec of record, a shared commissioning plan or open item, a shared touched module. Those findings are below, and they are a HINT and not the finding: two rows can legitimately cite one SR, and two rows deliberately cut from one plan share its path and always will. Your job is the part a string comparison cannot do: reading the *intent* of each row against the *intent* of the others and of the requirements they cite.

--- THE CANDIDATE CLUSTER ---
{candidate}
--- OTHER OPEN ROWS (id, title, sr_refs, needs) ---
{open_rows}
--- THE SPINE THE CLUSTER CITES (id + normative text) ---
{spine}
--- MECHANICAL PRE-FILTER FINDINGS ---
{mechanical}
--- DIGESTS THIS VERDICT IS RECORDED AGAINST ---
{digests}
--- WHAT EARLIER CONSOLIDATIONS ALREADY ABSORBED ---
{prior}
--- END ---

Look for exactly three shapes, in this order:

1. **Contradiction with the spine.** A row asks for something a cited SR forbids, or asks for the opposite of what a sibling SR requires. This is the expensive one: a lane will build it, a reviewer will approve it against the row, and the requirement it violates is somewhere else entirely.

2. **Scope overlap.** Two rows that would edit the same behaviour from two directions. Ask: if both are claimed on the same day by two lanes, do they collide? If they collide but each is still its own decision, the answer is a `needs` edge. If they are ONE decision that was written down twice — or a decision and a second half of itself — the answer is consolidation.

3. **Already answered.** A row asks for something an open or CLOSED row already did, or that was deliberately refuted. A refuted proposal returning under a new title is the failure mode that costs the most. So is re-absorbing a row an earlier consolidation already minted: read `{prior}` before you absorb anything, and if the honest answer is that an earlier consolidation got it wrong, say `return-to-draft` and NAME that consolidation — that pages the owner, and it is the right cost.

Then choose ONE outcome:

- `queue` — no conflict; every row in the cluster stays exactly as it is.
- `queue-with-edge` — no contradiction, but two of them must not run concurrently. NAME the row that must wait, and the machinery adds the hard `needs` edge to it.
- `return-to-draft` — a contradiction, an already-answered scope, or a re-litigation of an earlier consolidation. NAME what it contradicts, with the row, SR or WI id. A refusal without a named referent is not actionable and will simply be re-queued.
- `consolidate` — these rows are one work item. Draft ONE successor (do not create it; the machinery mints your draft at this row's own merge) as a fenced `toml` block under a `## Dispositions` heading in **THIS SESSION'S OWN SPEC** — never in the verdict file — written as TOP-LEVEL `key = value` lines (no `[table]` header), carrying at minimum `title` (at most 120 characters), `workstream`, `buildtier`, and `supersedes = ["WI-a", "WI-b", …]` naming EVERY absorbed row as a TOML list of single ids. Every absorbed row then moves to `docs/archive/work/restructured/` with `Restructured into WI-<successor>.` as its whole Deliverable, its scope text untouched, and its inbound hard edges re-pointed onto the successor.

If you consolidate, the successor's Context is written for you: your stated scope prose (the text you write beside the draft block) verbatim, then each absorbed row's Done-when block quoted under its old id. So state the scope — the boundary, and what is deliberately excluded — and do NOT paraphrase the absorbed rows' Done-when text; it is the spec the successor must still satisfy and it is carried across verbatim.

THE OUTCOME AND ITS TARGETS ARE A TYPED BLOCK, not prose the machinery guesses at. In this session's own spec, add a `## Consolidation` heading with one fenced `toml` block:

    outcome = "queue" | "queue-with-edge" | "return-to-draft" | "consolidate"
    edges = ["WI-402 needs WI-401"]   # queue-with-edge only: the waiter, then the row it must wait on
    returns = ["WI-402"]              # return-to-draft only: the rows going back to draft/
    finding = "..."                   # return-to-draft only: quoted verbatim into each returned row's Context

Omit the keys an outcome does not use. `outcome = "consolidate"` needs no `edges`/`returns`: the absorbed set is the `supersedes` list of your `## Dispositions` draft, which is what the machinery acts on.

Write your verdict to {verdict}: one `- [BLOCKER|MAJOR|MINOR] <the other row, SR or WI id> -> the collision -> the concrete change` line per finding. Then exactly one machine line:

    OUTCOME: QUEUE|QUEUE-WITH-EDGE|RETURN-TO-DRAFT|CONSOLIDATE needs=<id;id;… or -> absorbs=<id;id;… or ->

BOTH COUNTERS ARE REQUIRED ON EVERY OUTCOME AND BOTH ARE CHECKED. Write `-` where an outcome uses neither. `absorbs=` must name exactly the ids your `## Dispositions` draft supersedes, `;`-joined; `needs=` must name exactly the WAITERS your `## Consolidation` `edges` declare (the left-hand id of each), `;`-joined — several, where you declared several. The close REFUSES if either disagrees with the typed block, so this line is a restatement you are held to, not a summary. Commit that verdict file — and this session's own spec, carrying your `## Consolidation` block and any `## Dispositions` draft — ending that commit with the trailer `WI: {wi}`. The coordinator learns a judgement is recorded from that trailer and from nothing else, so a verdict committed without it leaves this row open. YOU DO NOT MOVE YOUR OWN SPEC and you do not touch any candidate row: once your verdict is recorded, the machinery closes this row, enacts your outcome, and mints your draft.
