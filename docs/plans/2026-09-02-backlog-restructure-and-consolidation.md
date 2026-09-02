# Backlog restructure, the consolidation adjudicator, and adjudication review policy

Date: 2026-09-02. Owner direction (this date): do this OUTSIDE a standard WI,
because it touches the very mechanisms the loop has not yet shown trustworthy
(the verdict carrier, the close, the mint). Three parts, one plan, executed as
a hand trunk commit series recorded in `docs/log.d/`, not as lanes.

Every claim below was read from the scripts on this date; line references are
to trunk `9de63e78`.

---

## 0. The facts the plan rests on

- **Five adjudicator briefs, four routed.** `adjudicate_brief._ASSEMBLERS`
  (`adjudicate_brief.py:823`) fills `amendment`, `first-approval`,
  `disposition`, `red-tc`. The `conflict` brief has a template and a verdict
  grammar (`QUEUE | QUEUE-WITH-EDGE | RETURN-TO-DRAFT needs=<id>`) but **no
  mint trigger, no evidence assembler, and no reader of its `needs=` field**.
  Its `{digests}` slot names a scope+spine digest nothing computes. The only
  live piece is `check_trajectory.queue_conflict_findings` (near-duplicate
  title, shared SR-Refs, shared SpecRef), warn-only.
- **All judgement rows are one kind.** Every intake trigger hardcodes
  `kind = "adjudication"`; the scheduler ranks the kind (rank 1, exclusive,
  no bar) and `dispatch._judgement_first` partitions it to the head of the
  frontier before admission. Among several adjudication rows the tie-break is
  `Priority` desc, then downstream count, hard-path length, id.
- **R1/R3.** A WI id is created only by a human trunk commit or the intake
  helper. A `## Dispositions` draft may never declare
  `safety_class = "adjudication"` (`intake._draft_refusal`), so a judgement
  cannot spawn a judgement.
- **`supersedes` is single-valued.** `_apply_supersede` /
  `_replace_inbound_edges` take one id string. The disposition brief tells
  the session to write `supersedes = "<one id>"`.
- **Terminal vocabulary is three words** — `complete` / `partial` /
  `cancelled` — and it is read in at least nine places: `wi_convert.STATUS_DIRS`,
  `kitlib.registry.SPEC_STATUS_DIRS`, `agent_common.TERMINAL_STATUSES`,
  `check_trajectory.TERMINAL_STATUSES`, `schedule._TERMINAL_DISPOSITION`,
  `intake.SWEEP_OUTCOMES` / `_closed_spec`, `kitlib.station.CLAIMED_OUTCOMES`,
  `integrate.Outcome`, `docs/work/README.md`, plus the folder-enumerating
  tests (`test_wi_folder_loaders`, `test_intake`, `test_integrate_admission`).
- **A cancelled row poisons its successors' context.** `intake.context_block`
  injects "Cancelled precedent on the same SRs (do not re-propose the
  refuted)" into every later worker brief that shares those SRs
  (`intake.py:474`). Closing a row as `cancelled` because it was *absorbed*
  would brief every successor that the absorbed scope was refuted. That is
  why `cancelled` cannot carry the restructure and a fourth terminal word is
  needed.
- **Adjudication lanes owe a REVIEW-A they cannot produce.** `ADJUDICATE` is
  in `agent_loop.NON_BUILD_PHASES` (no round is scheduled after its commit),
  yet `integrate._verdict_gate` demands `docs/reviews/WI-<n>-REVIEW-A.md`
  with an APPROVE for every merged WI, with no adjudication exemption.
  `integrate._adjudication_lane` already answers "is every claimed spec an
  adjudication row" for the bar skip; the gate does not consult it. Result:
  every adjudication merge is a supervisor stop (WI-550, WI-573, WI-578 will
  be next).
- **The worker brief renders one row.** `agent_loop.worker_prompt(root,
  wi_rows, wi, …)` fills `worker.template.md` from ONE id and the template
  opens "You are assigned ONE work item … this assignment is your whole
  scope." `current_assignment_wi` correctly walks a multi-row assignment one
  session at a time, so a spine batch is a series of sessions each told it
  holds one row. The reviewer brief names no WI at all.

---

## 1. The consolidation adjudicator

### 1.1 What it is

One more adjudication brief, `consolidate`, whose verdict may **absorb
several queued rows into one successor**. It is the conflict brief's job
(contradiction with the spine, overlap with an open row, already answered)
plus a fourth outcome the conflict brief lacks. It is built as its own
function set, not by widening `disposition`, because it is the only judgement
that closes rows it was not minted from.

### 1.2 The verdict grammar

    OUTCOME: QUEUE|QUEUE-WITH-EDGE|RETURN-TO-DRAFT|CONSOLIDATE needs=<id or -> absorbs=<id;id;… or ->

- `QUEUE` — no conflict; every candidate stays as it is.
- `QUEUE-WITH-EDGE needs=<id>` — a named pair must not run concurrently; the
  close writes the hard `needs` edge on the later row. (The reader the conflict
  template promised and never got.)
- `RETURN-TO-DRAFT` — a contradiction or an already-answered scope; the named
  row moves `queued/ -> draft/` with the finding quoted into its Context.
- `CONSOLIDATE absorbs=<ids>` — the session drafts ONE successor in
  `## Dispositions` with `supersedes = ["WI-a", "WI-b", …]` (a list — see 1.5),
  and the close moves every absorbed row to `archive/work/restructured/`.

`adjudicate_brief.VERDICT_GRAMMAR["consolidate"]` carries the enum; the
existing `verdict_refusal` arm validates it, so a session that commits without
the line is not DONE.

### 1.3 When it mints — and why it cannot recurse

The trigger is a **census, not a merge hook**, so a mint at merge cannot fire it
on its own output:

1. It runs from `dispatch._admit` at the top of a tick, **only when the
   station is idle and no adjudication row is queued or active** (a
   consolidation never stacks on another judgement, and it never judges a row a
   lane holds).
2. Candidates are the `queued` rows only. The mechanical pre-filter is
   `queue_conflict_findings` **plus two new signals**: shared `SpecRef` plan
   document (rows commissioned by one plan/OI), and shared touched-module set,
   read from each row's Context/Done-when by the same `_code_map_lines` join
   the worker brief already uses. Any cluster of two or more rows is a
   candidate cluster; the row minted lists them in a typed `adjudicates` cell
   (the WI-572 scoping mechanism, reused).
3. **The recursion guard is the digest.** The row carries `digests =
   "<sha of sorted (id, title, needs, safety_class) over queued/>|<sha of the
   three spine registries>"` — the pair the conflict template's `{digests}`
   slot always asked for. The census refuses to mint while a `consolidate` row
   whose queue digest matches is queued, active, or **archived**: a queue state
   that has been judged is never judged again. A consolidation's own successors
   change the queue digest, so the next census sees a new state — but its
   candidates are rows the last verdict *chose* to mint, and the brief tells
   the session so (the prior verdict's `absorbs` set is in the evidence, and
   re-absorbing a row minted by a consolidation is a `RETURN-TO-DRAFT` of the
   *consolidation's* judgement, which pages the owner instead). R3 still
   forbids the draft from declaring `adjudication`, so it cannot mint a judge.
4. **Priority.** Minted with `priority = 9` (the frontier sorts `Priority`
   desc inside rank), so among judgements it goes first; `_judgement_first`
   already puts judgements ahead of everything else. No rank-table change.

### 1.4 The evidence assembler (`adjudicate_brief.consolidate_values`)

All-or-nothing like its four siblings:

- `{candidate}` → the cluster's rows, full frontmatter + Context + Done-when.
- `{open_rows}` → every other open row as (id, title, sr_refs, needs).
- `{spine}` → the SR/LLR rows the cluster cites, id + normative text.
- `{mechanical}` → the pre-filter findings for the cluster, one per line.
- `{digests}` → the pair from 1.3.
- A new `{prior}` slot: the absorb sets of every archived `consolidate` row,
  so the session can see what an earlier judgement already merged.

A cluster with no cited spine still composes: `{spine}` is then the literal
"(the cluster cites no SR/LLR)" — stated, not blank — because contradiction
with the spine is one of three questions and the other two remain.

### 1.5 The close (`handback.close_adjudication`, new arm) and the mint

- **Absorbed rows must still be `queued` at close.** One that was claimed in
  the meantime cannot be — the census guard in 1.3 makes this a race only a
  hand claim can produce; the close then refuses by name (fatal, owner reads).
- Each absorbed row moves `queued/ -> archive/work/restructured/` with a
  `## Deliverable` of exactly one line: `Restructured into WI-<successor>.`
  Its scope text is untouched, `specref` INCLUDED — the same rule as
  `partial`, and for the same reason R-F's partial carve-out states: the
  successor's `supersedes` lineage is worth nothing if the thread it continues
  has already been cut. (First execution, 2026-09-02: the strict check
  errored R-F on all eight rows because the carve-out named only `partial`;
  the carve-out now names both. Review round 1 caught the wrong remedy.)
- `supersedes` becomes a **list** everywhere: `wi_convert` parses a string or
  a list into the `Supersedes` cell (`;`-joined); `_apply_supersede` loops;
  `_replace_inbound_edges` re-points every dependent of every absorbed row to
  the successor, dropping duplicates. Test: three absorbed rows, two dependents
  each, one successor, edges re-pointed exactly once.
- The successor's Context opens with the lineage line every minted row gets,
  then the verdict's stated scope prose verbatim, then the absorbed rows'
  Done-when blocks **quoted under their old ids** — decompose, don't
  paraphrase; the old text is the spec the successor must still satisfy.

### 1.6 The fourth terminal word: `restructured`

`restructured` joins the vocabulary as a terminal status with folder
`archive/work/restructured/`. Readers to extend, each with a test:
`wi_convert.STATUS_DIRS`, `kitlib.registry.SPEC_STATUS_DIRS`,
`agent_common.TERMINAL_STATUSES`, `check_trajectory.TERMINAL_STATUSES`,
`schedule._TERMINAL_DISPOSITION` (`("restructured", "restructured:absorbed")`),
`intake._closed_spec` dirs (**excluded** — a restructure never mints a
disposition), `intake.context_block` (**excluded** from the cancelled-precedent
join — it is not refuted work), `kitlib.station.CLAIMED_OUTCOMES` (**not** a
claimed outcome — a lane never closes into it; only the consolidation close and
a hand trunk commit may), `integrate.Outcome` (unchanged for the same reason),
`docs/work/README.md`, `hard_preds_satisfied` (a `restructured` predecessor is
satisfied by its successor — the edge was re-pointed at close, so this is a
validator-net assertion, not a scheduler rule).

This vocabulary change is **step 1 of part 2's execution** (below), because the
restructure itself needs the folder before the mechanism that would later use
it exists.

### 1.7 What stays out

- No structural classifier producer (the `structural=` seam in
  `schedule.kind_of`). Consolidation reads declared classes; a row misdeclared
  `ordinary` while authoring spine text is caught after merge by trigger (a),
  as today. Separate row if wanted.
- No change to the batch admission. Consolidation makes rows homogeneous by
  judgement; the batch remains the safety mechanism for spine class.

---

## 2. The restructured backlog

### 2.1 Findings over the queue as of this date

Eighteen queued rows excluding `WI-000`. Pending judgement `WI-578` (amendment
over LLR-158/203/204) runs first by construction.

**Contradiction.** `WI-545` (decompose `agent_loop` / `integrate` / `dispatch`)
needs only merged rows, so it is on the frontier at strong tier NOW, while
`WI-551`, `558`, `559`, `560`, `561`, `562` all edit those modules behind it and
`WI-551` re-applies a preserved 3876-line patch. First-landed wins, every later
lane pays a ratchet re-stamp and a conflict; landed first, `WI-551` becomes a
rebuild. Its own Context cites exactly this hazard for `WI-552`/`553`.

**Overlaps.**
- `WI-558` DW2 retires the gate's freshness comparison (tree identity);
  `WI-560` DW1 builds one shared freshness definition for the gate and the C2
  derivation. Unsequenced; the second undoes part of the first.
- `WI-559` DW2 (ADJUDICATE schedules a round like BUILD) depends on
  `WI-558`'s definition of a round. No edge.
- `worker.template.md` is edited by `WI-560` DW2, `WI-562` DW2, and the
  batch-assignment fix from §0 — three lanes for one file.
- `WI-564`, `565`, `576`: three one-file fixes from clean-close spot checks;
  `WI-565` itself argues for one commit range. `OI-77` is RULED, so `WI-565`
  is not gated any more.
- `WI-561`, `562` DW1: same class (lane-close hygiene in dispatch/integrate),
  both quick, both P3, both edgeless.

**Misdeclaration.** `WI-564` is `ordinary` but its likely exit authors a TC
row (spine). It would dispatch parallel while writing `test-cases.toml`.

### 2.2 The new rows (ids from the watermark: WI = 578, so 579…)

| New | Absorbs | Kind / tier / priority | Carries |
|---|---|---|---|
| **WI-579** The verdict carrier and adjudication review policy | `WI-558` whole; `WI-559` DW2; `WI-560` DW1 | ordinary / strong / **P9** | 558 DW1–5 verbatim; the review-owed derivation reads the same tree-identity trailer the gate reads (560 DW1's honest half); ADJUDICATE rounds scheduled only under the policy in part 3; the gate consults `_adjudication_lane` and demands a verdict from an adjudication lane only when part 3 says one is owed |
| **WI-580** The worker and reviewer briefs | `WI-559` DW1; `WI-560` DW2; `WI-562` DW2; §0 batch finding | ordinary / medium / **P8** | one-turn close bar (559 DW1 verbatim); `{assignment_block}` listing every assigned row with evidence state and the current focus, opening sentence corrected; reviewer brief gains `{wis}` naming the rows under review; scratch home named; amendment-regeneration named |
| **WI-581** Lane-close hygiene | `WI-561`; `WI-562` DW1; `WI-560` DW3 | ordinary / quick / **P6** | quarantine spares monotone/record paths (561 verbatim); `out/integrate.lock` declared; trunk step regenerates `CURRENT.md` after a merge that touched it |
| **WI-582** The WI-552 residual sweep | `WI-564`; `WI-565`; `WI-576` | **spine** / medium / **P4** | 564's IF row + covering TC (Drafted, never flipped); 565's DOTALL fix under OI-77's ruling + two cosmetics; 576's test exemption. Spine because it authors a TC; runs exclusive, batched with whatever `WI-578` drafts |
| **WI-583** The consolidation adjudicator | — (new; part 1) | ordinary / strong / **P5** | §1.2–1.5 and 1.7; `needs = ["WI-579", "WI-570"]` (570 edits `parse_dispositions` / `_mint_shape_refusal`, the same functions) |

Rows kept under their ids, edited in place on trunk:

| Row | Edit |
|---|---|
| `WI-551` re-land retention layer | `needs = ["WI-579", "WI-580"]`, `priority = 7` |
| `WI-541` verify retention layer | `priority = 7` (already needs 551) |
| `WI-545` decomposition debt | `needs = ["WI-579", "WI-580", "WI-581", "WI-551", "WI-583"]`, `priority = 1` — last among module-touching rows |
| `WI-570` typed OI brief | unchanged (P5; lands before 583 by edge) |
| `WI-536`, `539`, `556`, `557` | unchanged, independent plan/doctrine rows |
| `WI-577` | unchanged, waits on `OI-82` (pending) |
| `WI-578` | unchanged, runs first as the pending judgement |

Absorbed rows `WI-558`, `559`, `560`, `561`, `562`, `564`, `565`, `576` move to
`archive/work/restructured/` with `Restructured into WI-<n>.` as their whole
Deliverable and their scope text untouched.

### 2.3 Resulting order (frontier after `WI-578` merges)

1. `WI-579` (P9) — the unblocker; after it, no supervisor hand-compile.
2. `WI-580` (P8).
3. `WI-551` (P7, needs 579+580) → `WI-541` (P7).
4. `WI-581` (P6), `WI-570` (P5), `WI-583` (P5, needs 579+570).
5. `WI-582` (spine, P4, **needs 579+580**) — batched with any `WI-578`
   follow-ups still queued. The edge is what makes this position real: a
   READY spine row ranks 0 in the scheduler's ruled table and stops all
   admission until it runs, so without it `WI-582` would have run before
   `WI-579` (measured at first execution; review round 1).
6. `WI-536`, `539`, `556`, `557` (P2).
7. `WI-577` when `OI-82` rules.
8. `WI-545` (P1) last.

`WI-558`, `559`, `551`, `541` — the owner's named priorities — are positions
1, 2, 3, 3 in that order (558+559 as 579/580).

### 2.4 Execution, out of band

All hand trunk commits on the integration branch, each ending with the smoke
bar, the log fragment `docs/log.d/2026-09-02-backlog-restructure.md` carrying
the reasoning:

1. **Vocabulary first** (§1.6): the `restructured` status, folder, nine
   readers, tests. Full suite green before step 2.
2. **`supersedes` as a list** (§1.5), tests.
3. **Mint the five rows** with `python -c "import intake; print(intake.next_wi_id(root))"`
   sequence or a small one-shot script that calls `wi_convert.write_spec_file`
   for each draft — then `python project-trajectory/scripts/trace.py --bump-ids`
   so the watermark reads `WI = 583`. Never hand-write the mark.
4. **Move the absorbed rows** with `spec_move.py` into
   `archive/work/restructured/`, write each one-line Deliverable, re-point
   inbound edges (`_replace_inbound_edges`, now list-aware).
5. **Edit the kept rows** (`WI-551`, `541`, `545`) — `needs` and `priority`
   only.
6. **Verify**: `schedule.py ready --explain` shows `WI-578` as the first
   READY row and the §2.3 rows in that relative order (the scheduler's total
   order also lists WAITING rows by rank, which is not admission order);
   `check_trajectory.py --strict` shows no new ERROR and the shared-spec
   warning pairs fall from 11 to the 4 that are one ruling each by design
   (`WI-556/557/579` on OI-76's registry, `WI-580/581` on the 2026-08-31
   plan);
   `trace.py` integrity green; `python -m pytest -q -n auto` full suite green.
   Paste the outputs into the fragment.
7. **Regenerate** `PROJECT_STATE.html` and `docs/status.md` per the trunk step;
   scrub every absorbed id from `docs/status.md` (forward-only rule).

---

## 3. Review policy for adjudication rows

### 3.1 The position

A round over every adjudication is a fresh session with less context judging
the one session that held the whole chain, at strong-tier cost, and today it
is also the mechanism that stops every unattended run. The adjudicator IS the
cross-family judge by routing (§0). A second opinion earns its cost only where
the verdict **creates work or moves scope**.

### 3.2 The dial

`docs/process.toml [attestation] adjudication_review = "never" | "when-minting" | "always"`,
template ships `"when-minting"`, this repo sets `"when-minting"`.

- `never` — no round after ADJUDICATE; the gate never asks an adjudication lane
  for a verdict.
- `when-minting` — a round is scheduled, and the gate demands its verdict,
  when the merged adjudication's `## Dispositions` drafts **any** successor
  whose kind is `spine` or `high-risk`, **or** the brief is `consolidate`
  (every consolidation drafts a successor and closes rows). An amendment
  verdict that only recommends a flip, a red-tc that drafts ordinary fix rows,
  a clean-close spot check: no round.
- `always` — today's intended-but-broken behaviour, made real.

Read in exactly two places: `agent_loop` where `NON_BUILD_PHASES` gates the
round (ADJUDICATE leaves the set; the dial decides), and `_verdict_gate`
(`_adjudication_lane` + the dial + the drafts decide whether a verdict is
owed). One reader function in `agent_common`, `adjudication_review_owed(docs,
brief, drafts)`, so the two cannot disagree.

### 3.3 Where it lands

`WI-579` carries the dial and both readers (it is the verdict-carrier row and
the only one touching the gate). `WI-583` declares `consolidate` as always
review-owed under `when-minting`.

---

## 4. Acceptance for the whole plan

- Three consecutive rows merged by one launch with zero supervisor commits
  (the OI-76 measurement) reads non-zero after `WI-579`.
- A spine batch session's prompt names every assigned row (test on
  `worker_prompt` with a two-id assignment).
- The consolidation census, run against a scaffold queue of five rows with two
  overlapping pairs, mints exactly one `consolidate` row; run again on the same
  queue, mints nothing; run after that row's close absorbed two rows, mints
  nothing (the digest changed but the only overlap is the consolidation's own
  successor).
- No `restructured` row appears in any worker brief's cancelled-precedent
  join.

---

## 5. Review round 1 (2026-09-02) — what the plan got wrong

Two adversarial rounds over the first execution (`891a5b24..c16182cb`):
OpenAI Sol at medium effort through codex (8 findings) and an independent Opus
session (15 findings), both against one hostile brief. No blocker. The
corrections that changed THIS document are marked inline above (§1.5 specref,
§2.3 the WI-582 edge, §2.4 step 6's criteria). The rest — quote fidelity in the
new rows, the Deliverable grammar and its validator, many-to-many `supersedes`
re-pointing, a dashboard reader and legend, PROCESS_OPTIONS's vocabulary
sentences, the RESYNC entry for list-valued `supersedes`, and the log's pair
count — are recorded with their commits in
`docs/log.d/2026-09-02-backlog-restructure.md`.

