+++
id = "WI-977"
title = "One work item per lane: the managed loop's spine batch retires, so every admission, claim, resume, worker assignment and lane close names exactly one work item, and contract_split's single-item rows are ported"
workstream = "process"
sr_refs = ["SR-144", "SR-148", "SR-156", "SR-026"]
specref = ""
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
+++

## Deliverable

One work item per lane (the review-churn plan's item 15, owner revision
25): the managed loop's spine batch retires. Admission has no batch arm,
so a spine row takes the exclusive arm and admits alone and every
admitted assignment carries one id; the claim, the worker's `--wi`, the
resume and the partial and adjudication closes each take exactly one work
item, and an empty, separator-only, list or multi-id input refuses before
any lock, move, commit or launch; a parked lane claimed with several rows
stops the run by name. The multi-row prompt block goes, the claim subject
is written with one id while the history readers still parse the two
historical joined subjects, and the mechanical close peels only a close
moving exactly one row. The 23 spine rows (SR-144, SR-148, SR-156, LLR-058,
LLR-061, LLR-123, LLR-144, LLR-149 to LLR-152, LLR-161, LLR-207, TC-058,
TC-061, TC-138, TC-143 to TC-146, TC-154, TC-156, TC-205) were judged at
checkpoint sittings 005 to 007 and re-attested in one act from whole-set
sitting 014. Two counted rounds, a gate whose MAJOR dispute 011 ruled FIX,
and an all-MINOR second gate. One RESYNC entry (both `--wi` flags take one
id; a parked multi-row lane must land or close before an upgrade).
Decisions: `docs/decisions/wi-977.toml` D-001 to D-027.

## Context

Filed from the review-churn plan's item 15, the queue's row P4
(`docs/handoff-2026-10-11-attended-coordinator.md`): "one WI per lane
(retire the batch; port `contract_split`'s rows). After B4's rebuild lands
...; before the managed loop is unpaused". B4's successor (WI-969) has
landed. The owner's ruling (revision 25): "if the rest of the mechanisms in
the current branch are only built for a single WI, agreed scope should be
configured to match ... in general I would expect a single WI per pass."
Rulings 1 (closed coverage), 3 (S1 is the only split rule), 5 (no code in a
requirement cell) and 9 (`planmode` from S4; advice binding) shape this
spec. `contract_split` means its tip `961f9e47`; the common ancestor is
`607cf609`.

**Anchor.** SR-156 (Approved, "Bounded lanes narrowing to one gated
landing") under SN-027 (Approved). SR-144 (the close) and SR-148 (admission
and selection), both Approved and under SN-027, change with it. SR-026
(Approved) is LLR-061's parent and does not change. No SN changes.

**Every site of the batch (read on trunk at `e4a3a4ccd`).**

- **Admission.** `dispatch.py`: the header ("admits ALL spine rows
  TOGETHER as one batch (one branch, one `agent_loop --wi 'A;B'` worker,
  one re-attest window, one owner sitting)"); `_kind_action` (spine ->
  `"batch"`); `_admission` (`admit-exclusive` with every frontier row of
  the first row's kind); `_claim_lanes` (one claim per batch, ids joined
  with `;`); `_residue_wi_count` and `_poll`'s merged count, which count
  ids per branch because "a spine batch is ONE branch carrying several
  WIs".
- **Claim (WI-381).** `integrate.py`: the `claim --wi` CLI splits on `;`;
  `claim`, `_claim_locked`, `_claim_refusal`, `_abandoned_claim`,
  `_claim_delta` and `_relinked_exactly` all take a list; the subject
  grammar `agent_common.claim_subject` joins the ids.
- **Resume.** `dispatch._admit_parked` relaunches whatever the trunk holds
  in `active/<branch>/` (`integrate._claimed_wi_ids`), any count.
- **The worker.** `lane.worker_argv` joins the ids into `--wi`;
  `agent_loop`'s `--wi` help ("the assigned traincar's ordered constituent
  WI list, e.g. 'WI-201' or 'WI-201;WI-204'"); `agent_common.parse_wi_list`
  (`;`, `,` or whitespace lists), read by the shared worker preflight and
  by `agent_loop.build_worker_assignment`; `agent_loop.current_assignment_wi`
  walks the list a row per session; `agent_common.stale_terminal_assignment`
  exists for a batch lane's own closed rows.
- **The prompt.** `agent_brief.assignment_block` (WI-580) and the
  `{assignment_block}` slot of `prompts/worker.template.md`, rendered only
  for a lane of two or more rows. `WORKER` is not overridable
  (`prompts.py` IF-099), so an adopter holds no copy of the slot.
- **The close.** `handback.close_partial` writes one report per claimed
  spec and restores "every report this call wrote"; `open_claimed_specs` is
  "ONE HOME FOR THE BATCH FILTER"; `close_adjudication` moves every open
  claimed row through `station.mechanical_close_order` and
  `mechanical_close_subject`.
- **The peel.** `kitlib/verdict.py` `mechanical_close_attestation`
  re-derives a multi-row close's ids through the shared order
  (`kitlib/station.py`, "every batch lane re-opens the staled-APPROVE
  failure").
- **The refresh bar.** `integrate._lane_bar_directives` skips the bar only
  when every claimed row is an adjudication row ("a mixed batch runs it")
  and takes the strictest `bar` among the rows.
- **Text.** `PROCESS_OPTIONS.md`'s "Multi-WI assignments (WI-133 -> the
  scheduler)" paragraph, which still offers `--wi "WI-a;WI-b"` to
  adopters; `project-trajectory/README.md`'s `dispatch.py` row; the worker
  template's operator notes; `docs/concurrency-v2.md` §A4, §A4.4 and the
  §A6.1 passage keeping `--wi 'WI-201;WI-204'`; `docs/runtime-flows.md`
  ("the batch admits alone"); the `dispatch.py` and `agent_loop.py`
  headers; the generated `docs/cli-reference.md` `--wi` row and
  `prompts/CATALOG.md`.
- **Tests.** `test_dispatch.py::test_the_spine_batch_admits_first_and_together`,
  `test_dispatch_admission.py` (the two batch cases),
  `test_integrate.py::test_a_spine_batch_claims_as_one_commit`,
  `test_handback.py` (the two batch-row closes),
  `test_agent_loop_worker.py` (the batch prompt, the multi-WI build, the
  list parse), `test_agent_loop_policy.py` (a two-row banner),
  `test_verdict_record.py::test_a_two_row_batch_close_peels_under_one_canonical_order`,
  `test_loop_order.py::test_an_adjudication_row_outranks_a_spine_batch`.

**Not the batch, and unchanged:** several claims under one scoped unpause,
each its own lane (the `coordinator-cycle` recipe's "A batch claimed under
one scoped unpause"); a consolidation verdict acting on queued rows it
names (an effect on the queue, not a claim); `intake.py sweep --merged`
(a reader of landed merges); the act ledger's batch approvals and
`--approves` (item 5's sense of "batch").

**Historical multi-WI records, and how they stay evidence.** Two batch claim
commits on trunk (`2f660cb7a` "claim: WI-569;WI-575 -> ...", `794de60d5`
"claim: WI-589;WI-584;WI-587;WI-588 -> ..."), their archived specs under
`docs/archive/work/complete/`, their iteration logs, reviews and log
entries, and the RESYNC entries that describe the batch. Both branches are
deleted and every claim directory on trunk holds at most one spec today, so
nothing in flight is a batch. The readers of claim history
(`agent_common.claim_base`, `agent_common.loop_claimed`,
`kitlib/provenance.py`'s claim pattern) keep parsing the joined subject, so
those commits still read as claims; no writer composes it again, and no
admission, resume, close or merge acts on such a record.

**Found at filing (each joins this row).**

- **Two more rows carry the batch.** LLR-152 ("a mixed batch ... fails
  TOWARD the bar", "the batch's strictest value") and LLR-207 ("a
  multi-row batch close cannot fail on a sorting") are the single-WI
  halves of TC-146 and TC-205. `contract_split` amended both under the
  primary-turn group, which does not come back, so their batch clauses are
  this lane's own text.
- **LLR-149 already disagrees with the code.** Its detail says attestation
  and gate rows "admit as the queued batch at single-approve's close";
  `_admission`'s keep-nondependent close surfaces them. `contract_split`'s
  LLR-149 states what the code does, so the port also repairs it; the
  `dispatch.py` header carries the same stale sentence.
- **An empty claim fails open (by reading; not driven).**
  `integrate.py claim --wi ";" --branch x` reduces to an empty list; no
  rung refuses it, and `_claim_locked` would commit a claim that moves no
  spec and cut the branch.

**Deliverables and landing order (S1).** Two deliverables, kept as one row:

1. The spine change set, authored at the intent turn, test cases first
   (item 13's order): the amendments listed under "The spine" below.
2. The retirement: code, tests, text, generated pages, one RESYNC entry.

Neither can land alone. The code without the rows leaves Approved LLR-149,
LLR-151 and LLR-061 stating a batch the code refuses; the rows without the
code approve a single-item contract the code breaks. The checkpoint sitting
judges deliverable 1 against deliverable 2 built.

**Authority (S2).** No deliverable gives a file authority over a hold, an
act or a gate, so no `## Trust` section is owed. The claim commit and the
claim directory keep the authority they have (the claim base the merge gate
binds a review to, WI-884); this row narrows what they may name and adds no
reader.

**Coverage (S3).** Each entry point takes exactly one work item. Its
allow-set is below, and **the rule for everything else is refusal before
any state change**: no lock is taken, no spec moves, nothing is committed,
no branch or worktree is cut and no provider is launched, and the refusal
names the input. A value given on a command line is free text, so it is
deny-by-default: the allowed form is one work-item id in that entry point's
existing grammar (the claim CLI keeps its case normalization), and any
empty or separator-only value, or any value holding a `;`, `,` or
whitespace separator, refuses. The bound is PROCESS.md §6 "Review threat
model": a claim directory or claim commit made by hand to hold two specs is
outside the promise, so the readers named last are not given refusals of
their own.

| Entry point | Admits | Refuses |
|---|---|---|
| Admission (dispatcher) | one row per assignment: a parallel row per free lane, or the first exclusive row alone into an idle station, spine rows included; later spine rows wait for later exclusive turns | no admitted assignment carries more than one id, so there is no input to refuse |
| Claim (CLI and in-process) | one queued work item | empty, two or more ids, a list form |
| Resume (parked lane) | a branch whose trunk claim holds one spec | a claim holding two or more: the run stops loudly (a composed part's refusal), nothing relaunched |
| Worker assignment and preflight | `--wi` naming one id | empty, a list, a malformed or repeated id: preflight exit before a provider launches |
| Prompt | names the one assigned row (id, title, SpecRef, as today) | the multi-row block and its slot are removed |
| Close (partial and adjudication) | a branch whose trunk claim names one spec; that spec already terminal on the lane keeps today's answer (the immutability refusal, or the no-op) | zero (as today), or two or more: before any report, residue commit or move |
| Mechanical-close peel | a close moving exactly one row | any other shape declines to peel (fails toward more review) |

The other readers of a lane's claimed set (the refresh's bar directives,
the merge slot, the round-owed read, the residue count, the session
service's attribution, the coordinator entry point's open-row check) read
what the claim wrote, which is now one spec. They keep their code; only
their batch-only wording and arms go.

**Planning (S4).** `single`: the row touches several script families (the
dispatcher, the integrator, the closes, the worker loop and its brief, the
verdict peel) and promises behaviour over an input space (the table above).
It adds code paths (the refusals), so the deletion exemption does not
apply. `dual` is not needed.

**Architectural delta (S5).** A value leaves a domain: the admission table
loses `batch` (spine rows take the `exclusive` arm), and a lane's
assignment goes from an ordered list to one id, through the claim, the
worker's `--wi`, the walk and the close. The worker prompt loses one slot.
No new state, input or boundary crossing; no interface row changes (IF-080's
`claim --wi --branch` already names one value).

**Dependencies (S6).** No `needs`. B4's rebuild (WI-969), which shared
`handback.py`, has landed. Two orderings are stated rather than edged: this
row lands before the managed loop is unpaused (the owner's act), and P5,
item 16's watermark carrier, files after it. It changes the claim and close
the coordinator cycle runs on, so it lands alone (revision 37). No new
dependency.

**The spine** (one checkpoint sitting, top-down; target meaning only).
Every cell this row restates whole names no code file, function, symbol or
test module (ruling 5). Where only a batch clause changes (LLR-152, LLR-207,
TC-146, TC-205), only that clause is replaced, in the same voice, and the
rest of the cell waits for item 5's migration. The traced `module`,
`code_symbol` and `evidence` cells follow the code as traced edits. For
each row: ancestor `607cf609` (A), `contract_split` `961f9e47` (CS), this
branch (H).

- **SR-144** (`requirement`, `acceptance_criteria`: A = H). CS's meaning
  moves in: a close of a lane whose claim is other than one work item is
  refused before any report or state change, and a refused close restores
  the one report it created, leaving the claim and terminal state unchanged.
  H's `coincident` stays.
- **SR-148** (`requirement`, `rationale`: A = H; `acceptance_criteria`:
  H rewritten). CS's meaning moves in: every assignment admits exactly one
  work item, spine admission included, and an ordinary frontier fills
  several lanes through separate single-item assignments; the rationale
  says admission cardinality here and claim cardinality in SR-156 bound
  one contract at two boundaries. H's acceptance text stays around CS's
  added sentence (the adopted-successor clause included).
- **SR-156** (`requirement`: A = H; `acceptance_criteria`: H rewritten).
  CS's meaning moves in: exactly one work item per lane; an empty or
  multi-item claim, assignment or resume refuses before any state change;
  historical multi-item records stay readable as evidence and are never
  run as claims. H's Done-when blessing and review-gate sentences stay.
- **LLR-144** (`detail`: A = H). CS's meaning: the partial close refuses
  a claim of other than one spec before any report or state change and
  moves the one spec; the quarantine arm stays.
- **LLR-151** (`detail`: H rewritten; `title`, `rationale`: A = H). Title
  "Dispatch-lock ownership and single-WI claim". H's lock and
  bookkeeping-commit meaning stays; "batch-aware" becomes: one claim commit
  moves one queued spec and cuts its branch; empty or multi-item input
  refuses before any move, commit, branch or worktree; historical
  multi-item claim commits stay readable and are neither split nor
  re-claimed. Rationale: CS's trade (N exclusive re-attestation windows for
  N spine rows instead of one shared window).
- **LLR-161** (`detail`: H adds the adoption sentence). CS's meaning: a
  refusal restores the one report this close created and leaves the claim
  and terminal state unchanged; H's adoption sentence stays.
- **LLR-058** (`title`: A = H; `detail`: H rewritten). Title only, CS's
  "WI-DAG dependency-ready frontier": ordering is LLR-123's. H's detail
  stays.
- **LLR-061** (`detail`: A = H; H's `module` adds the brief). The prompt
  names the one assigned row; an empty or multi-item assignment refuses
  before a session starts; `--wi` names one work item and has no list
  form; the multi-row block retires. CS's completion-state line for the one
  row is not ported (drafter notes).
- **LLR-123** (all three cells A = H). CS's meaning: "traincar" becomes
  "work item" and the last tiebreak is the WI id.
- **LLR-149** (`detail`: A = H). CS's meaning, which matches the code's
  surface arm: the first spine row in order admits alone ahead of ordinary
  work, the remaining spine rows stay queued for later exclusive turns;
  held attestation and gate rows drain and surface, and the
  keep-nondependent dial never releases their hold; at a delegated tier
  they dispatch one at a time, exclusive.
- **LLR-150** (`detail`: A = H). CS's meaning: the parked-lane resume
  hands the lane mechanics only a single-item assignment and refuses
  another before any mutation or launch; the tree signal is the one
  assigned spec leaving the claim directory.
- **LLR-152** (found at filing; batch clauses only). The no-bar arm applies
  when the lane's one claimed row is an adjudication row; any other kind,
  or unreadable frontmatter, runs the bar; the bar key is that row's.
- **LLR-207** (found at filing; batch clause only). The peel admits a
  mechanical close moving exactly one row; the shared multi-row ordering
  leaves the row.
- **TC-058** (`method`: A = H). "Traincar order" becomes "work-item order".
- **TC-061** (`method`: H rewritten). H's text stays; its two-row arm (the
  every-row block, the sibling read as `built`) becomes: an empty or
  multi-item assignment refuses before a provider launches, and the prompt
  names the one row; "a `--wi` list with a malformed or repeated id"
  becomes any value that is not exactly one well-formed id.
- **TC-138** (`method`: A = H). CS's meaning: an empty or multi-spec claim
  refuses the partial close before any report or state change, every
  claimed spec intact; the one spec moves.
- **TC-143** (`method`: A = H). CS's meaning, matching LLR-149 above.
- **TC-144** (`method`: A = H). CS's meaning: each spine claim moves one
  item and its worker receives only that id; the next spine item waits for
  the exclusive lane's return; a parked resume with an empty or multi-item
  assignment refuses before any mutation or launch, while a single-item
  lane resumes under the barrier.
- **TC-145** (`method`: H rewritten with the bookkeeping helper). H's text
  stays; its batch-claim arm becomes CS's: one item claims in one commit,
  empty and multi-item claims refuse with no partial claim, and a
  historical multi-spec claim commit is neither re-claimed nor split.
- **TC-146** (single-WI part only). "A mixed batch bars as usual" becomes:
  a lane whose one row is any other kind bars as usual. CS's primary-turn
  text does not come back.
- **TC-154** (`method`: A = H). "A ready spine batch" becomes "a ready
  spine work item".
- **TC-156** (`method`: H adds adoption). CS's arm joins: an injected
  refusal after the single report is created restores it and leaves the
  claim and terminal state unchanged.
- **TC-205** (single-WI part only). The batch-shape arm (a two-row close
  peeling under one canonical order) becomes: a mechanical close moving two
  rows does not peel. CS's primary-turn text does not come back.

**Unchanged, on purpose:** spine exclusivity (item 16's); LLR-208's
"traincar is one review scope" (with one item per lane it still holds);
SR-026; every IF and CMP row; the two-part completion predicate the walk
reads.

## Done-when

**The spine** (the intent turn, test cases first; one checkpoint sitting)
- [ ] The 23 rows above carry their target meaning: SR-144, SR-148, SR-156;
  LLR-058, LLR-061, LLR-123, LLR-144, LLR-149, LLR-150, LLR-151, LLR-152,
  LLR-161, LLR-207; TC-058, TC-061, TC-138, TC-143, TC-144, TC-145,
  TC-146, TC-154, TC-156, TC-205 (TC-146 and TC-205 in their single-WI
  parts only).
- [ ] No cell this row restates whole names a code file, function, symbol
  or test module, and no replaced clause does; traced cells follow the
  code.
- [ ] The amendments are judged at one checkpoint sitting and acted on
  from its verdict; none of the rows' acts is the owner's (SR, LLR and TC
  rungs sit above `human_approval_through`), so no step of this row is held
  for the owner.

**The retirement** (the coverage table in Context is the contract)
- [ ] Admission: the admission table has no `batch` arm; a spine row takes
  the exclusive arm and admits alone; every admitted assignment carries
  exactly one id.
- [ ] Claim: the CLI and the in-process claim take one work item; an empty,
  separator-only, multi-id or list-form input refuses before the lock and
  before any move, commit, branch or worktree, naming the input (the empty
  case is driven, since it fails open today).
- [ ] Resume: a parked branch whose trunk claim holds two or more specs
  stops the run loudly, naming the branch, with nothing relaunched or
  mutated.
- [ ] Worker: `--wi` takes one id; the help text says so; an empty, list,
  malformed or repeated value fails preflight before a provider launches;
  the walk, the shared preflight and the assignment read one id.
- [ ] Prompt: the multi-row assignment block, its `{assignment_block}`
  slot and its operator notes are removed; the one-row prompt renders as
  today.
- [ ] Close: the partial and adjudication closes refuse a claim of zero or
  of two or more specs before any report, residue commit or move; the
  multi-report restore and the batch filter reduce to one spec.
- [ ] Peel: the mechanical close writes one row, and the attestor peels
  only a close moving exactly one row; the shared multi-row ordering goes
  if nothing else reads it.
- [ ] The claim subject is written with one id only, and the history
  readers still parse the two historical joined subjects as claims (driven
  on a fixture holding one).
- [ ] Batch-only wording and arms go from the other readers of the claimed
  set (refresh bar, residue and merged counts), which keep working on one
  spec.
- [ ] The batch tests listed in Context are removed or turned into the
  refusal tests above; each refusal has a test that fails on today's code.
- [ ] Text: `PROCESS_OPTIONS.md`'s multi-WI paragraph goes (the
  `byte-budget-guard` skill reports the delta and restamps); the
  `project-trajectory/README.md` dispatcher row, the `dispatch.py` and
  `agent_loop.py` headers, `docs/runtime-flows.md` and the
  `docs/concurrency-v2.md` batch passages state one item per lane (the
  design doc gains a note at §A4 naming item 15, its history kept).

**Shipping and the bar**
- [ ] One RESYNC entry: spine rows admit one per exclusive turn (N
  re-attestation windows for N rows); `integrate.py claim --wi` and
  `agent_loop --wi` take exactly one id, so a script or launcher passing a
  list fails; a parked lane claimed with several rows refuses to resume, so
  an adopter closes or lands such a lane before upgrading; the worker
  template lost a slot (kit-owned, overwritten); no data migrates. It
  supersedes the batch sentences of the 81cac0e1 dispatcher entry and the
  f4ca1bd5 batch-lane entry.
- [ ] `docs/cli-reference.md`, `prompts/CATALOG.md` and the other
  generated pages are regenerated.
- [ ] The commit bar is green, and both strict lints (`trace.py --strict`,
  `check_trajectory.py --strict`) are clean on the landing tip.
