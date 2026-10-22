+++
id = "WI-969"
title = "A disposition adopts an existing successor: the record-at-close rebuild, its plan revised for sitting 016's FIX"
workstream = "process"
sr_refs = ["SR-148", "SR-220"]
specref = ""
buildtier = "medium"
priority = 3
safety_class = "ordinary"
planmode = "single"
supersedes = "WI-902"
+++

## Deliverable

Closed at its landing on 2026-10-22, after its gate, in headless leg 11
(WI-902's successor on the owner's route, coordinator-2026-10-20 D-008):

- A disposition verdict can discharge its successor obligation by adopting
  an already-open row whose `supersedes` names the closed row. The close
  (`handback.close_adjudication`) validates the adoption once, in the lane
  HEAD's tree, and writes the `adopted` record in its own closing commit;
  a consolidation verdict that adopts is refused before its first write.
- One commit check (`adoption_record.py`) judges every adoption record
  against its parents: the close's own commit, recognised by a close test
  that admits the close's exact inbound relinks through
  `spec_move.exact_relink` (sitting 016's FIX), or a later commit carrying
  the record and its request unchanged; every other record change, and a
  requesting spec moved into a complete folder without a record, is
  refused at the merge slot (`LANE_COMMIT_RIDERS`) and at the pre-commit
  hook's new `adoption-record` step, with its own squash walk. The peel is
  unchanged.
- The merge sweep trusts the record: it compares the request with the
  record, re-points from the record beside the drafts, mints nothing for
  an adoption, and refuses an unreadable merged spec. One complete-section
  parser pairs fences and refuses a fence line off column zero; the mint's
  lineage corrections refuse a title match on another lineage before any
  write.
- Spine: SR-148, LLR-153, LLR-161, LLR-312, TC-147, TC-156 and TC-254
  re-attested; LLR-335, LLR-345, TC-360 and TC-383 approved (sitting
  007-ADJUDICATE-9d73112, acts 149 and 150); IF-294, IF-303 and IF-304
  stated, IF-175 amended. WI-902's lane acts 113 to 117 never reach trunk.

## Context

Drafted by WI-953 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

Advisory registry joins (WI-388; never gating):

### Cancelled precedent on the same SRs (do not re-propose the refuted)
- WI-810 (cancelled) MINT in the lane: one allocator, the consumption list and station lan… — reason: CANCELLED (owner, 2026-10-20; coordinator-2026-10-20 D-009): split, then cancelled. Its one bullet still owed, a settled amendment is never minted, is WI-963. …

### Decomposition code map (LLR/TC on the same SRs)
- LLR-058 [project-trajectory/scripts/schedule.py :: ready/frontier/evaluate] tests: (see TC-058) — WI-DAG frontier + deterministic traincar ordering
- LLR-059 [project-trajectory/scripts/schedule.py :: classify/safety_class] tests: (see TC-059) — Pure safety classifier
- LLR-060 [project-trajectory/scripts/trunk_step.py :: REGEN_STEPS/regen] tests: (see TC-060) — next-wi/run-phase retirement + generated status/run-state
- LLR-089 [project-trajectory/scripts/schedule.py :: kind_of/classify] tests: (see TC-091) — Structural safety cross-check
- LLR-123 [project-trajectory/scripts/schedule.py :: frontier/evaluate] tests: (see TC) — Deterministic traincar ordering
- LLR-131 [project-trajectory/scripts/schedule.py :: classify] tests: (see TC) — Contradiction-safe dual-plan class

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-010 scripts/gen_arch_map <- scripts/check;scripts/trunk_step: cli --doc | --cli-doc | --contracts-doc | --src | --mode | --check | --strict-parse | --backlink-coverage | --str…
- IF-150 scripts/gen_arch_map -> scripts/check;scripts/trunk_step: exit-code 0 current · 1 a stale target under --check, an unparseable module under --strict-parse, or coverage below the…
- IF-012 scripts/gen_okf -> scripts/check;scripts/trunk_step: exit-code 0 clean, vacuous or opted out · 1 stale, missing or extra bundle file under --check
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-163 docs/status.md -> scripts/agent_common;scripts/check_docs;scripts/check_trajectory;scripts/gen_okf;scripts/integrate;scripts/trunk_step: file the hand-authored blackboard outside the GENERATED STATUS marker pair; the block between the markers is its w…

### Spec of record, carried

The sections below are WI-902's spec of record (`docs/work/partial/WI-902-disposition-adopts-existing-successor.md`, this row's `specref`), from its Deliverables to its end, byte for byte: the single-plan brief, the plan gate and the Done-when hold read this row's own spec, which the mint left without a Done-when (wi-969 D-001). Where they say WI-902, the work is this row's. Sitting 016's FIX (`docs/reviews/wi-902/016-ADJUDICATE-7ffa12c.md`) binds the plan, on the owner's route (`docs/decisions/coordinator-2026-10-20.toml#D-008`).

## Deliverables

One lane, one landing (S1 below). Each item names its surface. The builder
writes each rule in that surface's own voice.

1. **The close writes the record** (`project-trajectory/scripts/handback.py`,
   `_archive_one_adjudication_row` and `_adjudication_close_text`). The close
   validates every adoption the section requests, in the tree its closing
   commit is made on. It then writes the validated `adopted` record into the
   closed spec, in the same rewrite that clears `specref`.
2. **The record's cell** (`scripts/kitlib/registry.py`, `scripts/wi_convert.py`
   and `scripts/plan_artifacts.py`; the key is documented in
   `project-trajectory/work/WI-000.template.md`). It is a declared `Adopted`
   column, with front-matter key `adopted`, beside `Adjudicates` and
   `Digests`, so no reader or converter drops it. One strict reader parses it.
3. **The commit check** (see Trust, "Consumers"). One rule judges a commit
   against its parent. It runs as a rider on `scripts/text_then_act.py`'s
   `LANE_COMMIT_RIDERS`, which covers the merge slot's walk of each lane
   commit and the hook's squash path. It also runs as a staged form in the
   pre-commit hook's step list (`scripts/check.py`,
   `project-trajectory/hooks/pre-commit`).
4. **The sweep trusts the record** (`scripts/intake.py`, `_merged_dispositions`).
   Recorded adoptions join the one lineage operation. The lane's history
   readers (`_landing_commit`, its shallow-boundary test, `_UNLANDED`) and the
   sweep's own adoption validation are deleted.
5. **One complete-section parser** (`scripts/intake.py`,
   `parse_disposition_section`). A `## Dispositions` section whose fences do
   not pair is refused, for drafts and adoptions alike (review 015's MAJOR).
6. **The shared adoption module** (`scripts/kitlib/adoption.py`, new, with its
   `kitlib/bootstrap_manifest.py` row and its seam IF-294). It holds the block
   parser, the disposed-id reader and the validation rule over a listing the
   caller supplies. It is pure: no git calls and no writes.
7. **The disposition prompt**
   (`project-trajectory/prompts/adjudicate-disposition.template.md`; the
   prompt catalog is regenerated). It teaches the adoption form. It says the
   close accepts an adoption only if that row is open and supersedes the
   closed row in the lane's tree when the row closes.
8. **The coordinator recipes**
   (`project-trajectory/skills/coordinator-cycle/references/recipes.md` §8
   and §3, synced to `.claude/skills/`; this repo's tooling, so no RESYNC
   entry). An adopting disposition closes through
   `handback.close_adjudication` and lands inside the squash, never by a hand
   close. §3's citation "(WI-902, act 117)" is updated to follow the lane
   record.
9. **`RESYNC_PACK.md`**: one entry, anchored at the landing's parent, that
   replaces the lane's entry.
10. **The mint's lineage corrections** (`scripts/intake.py`,
    `_standing_successors` and `_mint`; the lane's D-003 and D-004). A
    replay re-points a late dependent to the full successor set, drafts-only
    replays included. A standing row found by exact title must carry the
    draft's `supersedes`, or the mint refuses before any write. Both hold for
    drafts whether or not adoptions sit beside them.

## Trust

This section was written before the claim, answering the scope critique's S2
(coordinator-2026-10-11 D-005). It was re-sat on 2026-10-14 under the owner's
verdict on D-005 (the handoff's B4 row). Four parts of that ruling stand: the
carrier, the title-derived disposed row, minting nothing and the
consolidation-close refusal. "Accepted only while the named row is open,
re-read at each consumer" is replaced by a record that the close validates
once and writes. Two authorities follow. Naming an existing row as the
successor gives the adjudicator's text authority over the close, and the
close's record gets authority over the sweep. This section therefore states
both carriers, their producers, their consumers and a ruling per consumer,
under `project-trajectory/PROCESS.md` §3, "When a guard is owed".

**Two carriers: the request and the record.**
- The *request* is an adoption block in the disposition row's own
  `## Dispositions` section. It sits beside drafts or replaces them, in the
  section the drafts already live in, never in the verdict file. It is a
  fenced TOML block holding exactly one key, `adopts = "WI-NNN"`. Any of the
  following is a parse refusal, as a malformed draft is today: a block with
  `adopts` and any other key, a value that is not one well-formed WI id, or
  an id that another block already adopts. The verdict's machine line
  (`OUTCOME: ... successors=N`) is unchanged. The verdict reader checks only
  that `successors=` is present, and this row adds no count comparison.
- The *record* is the closed spec's `adopted` front-matter cell: a TOML list
  of the adopted WI ids, in the request's block order. One strict reader
  accepts only a non-empty list of distinct, well-formed WI ids. Any other
  shape is malformed: a bare string, an empty list, a table, or a repeated or
  malformed id. A row that adopts nothing carries no cell.

**Producers and write routes.**
- The adjudicator writes the request in the sitting's own spec in the lane,
  as it writes drafts, and commits it with the verdict. A failed call, a
  timeout or a structured error from the CLI ends the sitting with exit 1
  (no valid verdict), and the loop's `adjudication_owed` holds the close as
  today. Nothing a failed sitting already wrote is ever closed on, whether a
  partial block or section, committed or not. The close runs only after a
  sitting that exited 0, and the coordinator reverts a failed sitting's
  writes before the re-sit.
- Only the close writes the record (`handback.close_adjudication`, per row in
  `_archive_one_adjudication_row`). It writes the record only after the
  request has parsed, the disposed row has resolved and every adopted row has
  passed the validation below. The record goes into the same rewrite that
  moves the spec into `complete/` and clears `specref`, and it is committed
  in the closing commit. On any refusal, nothing moves and no record is
  written. A failed move or a failed commit leaves no committed record, just
  as either leaves no committed close today. A committed file cannot be read
  half-written, only malformed. Every consumer below refuses a malformed
  request or record, and none repairs or guesses one.

**What the authority binds to.**
- An adoption names only the successor. The disposed row is never read from
  the adjudicator's text. It is read from the disposition row's title, the
  immutable event token `_mint` dedups on (the row's `specref` is cleared at
  the close). Both minted title forms carry a terminal path whose file name
  leads with the disposed row's id. A report-backed close's title names the
  close report (`<wi>-<branch>`). A report-less cancellation's title
  (`intake._close_drafts`, "the cancellation recorded at") names the
  cancelled spec (`WI-NNN-<slug>.md`). One function, shared by the close, the
  commit check and the sweep, resolves that id. A title whose token is absent
  or does not resolve to exactly one WI id is refused at each, never guessed.
- The validation is one rule, LLR-335's. Each adopted id must name exactly
  one spec standing open (`draft/`, `queued/` or `active/`) in the tree the
  closing commit is made on. That tree is the lane's HEAD, which becomes the
  closing commit's parent. The spec must read as strict UTF-8 and parse, and
  its `supersedes` must name the disposed row. The close applies this rule
  once. The commit check re-applies the same function to the closing
  commit's parent.
- The record binds to the closing commit. The adoption is decided in the tree
  the row was closed on, and nothing re-opens it. A later claim, completion
  or cancellation of the adopted row never turns a recorded adoption into a
  refusal. No consumer reads git history or the adopted row's later state to
  decide it again. A lane rebased before it lands is checked again on its new
  parent, which then becomes the tree the record binds to.
- **What the binding leaves open** (the owner's validate-once trade, stated
  rather than left implicit). A successor cancelled on trunk between the
  close and a landing that is not rebased first, which is the loop's
  merge-slot path, is not re-checked: the record stands, and a dependent
  re-pointed onto the cancelled row surfaces as a dead dependency, which
  `check_trajectory` reports. A coordinator landing rebases first, so its
  closing commit is judged again on current trunk.
- The closing commit is still the machinery's own close, which the review
  gate peels (`kitlib.verdict.mechanical_close_attestation`). The record it
  adds is the request's validated result, and the commit check verifies it.

**Absent, unreadable and failed inputs.**
- At the close, each of these refuses: a malformed request or section; an
  adopted id naming no open row ("names no open row"); a spec that cannot be
  read or parsed (with the distinct reason "cannot read"); a tree that cannot
  be listed; and an untokened title. Nothing is moved and no record is
  written. No case falls back to minting or to accepting.
- At the commit check, a parent the repository cannot read, including a
  shallow boundary, is reported by name and never read as a root (the walk's
  parent reader). A record or request that does not parse is refused.
- At the sweep, each of these refuses the sweep (the merge stands, nothing is
  minted, exit 1): a request with no record, a record with no request, a
  record whose ids differ from the request's, a malformed record, and a
  merged spec it cannot read or whose front matter does not parse. The sweep
  never falls back to re-validating. Today it skips an unreadable merged
  adjudication spec; this row makes that a refusal, because a skipped early
  close is a close that vanishes without a successor.
- An absent `## Dispositions` section keeps today's rule at every consumer.
  The close and the sweep refuse it for a row that owes a successor, and the
  scheduler and the gate read it as nothing drafted.

**Consumers and rulings** (found by grep over `project-trajectory/scripts` for
`Dispositions`, `owes_successor`, `_DRAFT_KEYS`, `parse_dispositions`,
`adjudication_review_owed` and `LANE_COMMIT_RIDERS`; the builder re-greps for
`adopted` once the cell exists):

- **The close** (`handback._archive_one_adjudication_row`, through
  `close_adjudication`). `owes_successor` is discharged by a draft or by a
  validated adoption. The close validates and writes the record as above.
  Otherwise it refuses with the reason, as the guard refuses an empty section
  today. A consolidation row's close (`_consolidation_close`) refuses an
  adoption before its first write, because its absorbs reconcile against
  drafts' `supersedes` only.
- **The commit check** (new). It judges each commit that adds, changes or
  removes a record, and each commit that moves a spec whose section requests
  an adoption into `complete/`. Such a commit passes in two cases only:
  - It is the close's own commit, its record equals the request, and every
    adopted id passes the validation in its parent's tree. The close's own
    commit moves that spec from `active/<branch>/` into `complete/` under
    the machinery's composed close subject (the shape
    `mechanical_close_attestation` reads).
  - It carries an existing record and request unchanged (a later move).

  Every other such commit is refused. A merge is judged by what neither
  parent carried. The check runs where the kit's other per-commit rules run:
  - as a rider on `text_then_act.LANE_COMMIT_RIDERS`, which the merge slot
    walks over each lane commit (`integrate._each_lane_commit`) and the
    pre-commit hook walks over a squash landing's commits;
  - in the pre-commit hook over the staged tree. Outside a squash landing,
    any staged record change, or any requesting spec moved into `complete/`,
    is refused there: the close commits with the hook skipped, so it never
    meets the hook in that position.
- **The sweep** (`intake._disposition_drafts` through `_merged_dispositions`,
  from `intake_after_merge` for the merge slot and from `intake.py sweep`).
  It trusts the record. Each recorded id joins the one lineage operation
  (`_apply_supersedes`) as an (adopted, disposed) pair, beside the drafted
  successors. The disposed row's inbound `needs` are re-pointed to the full
  successor set without allocating an id, on the landing sweep and on every
  replay alike. The sweep reads no git history and no state of the adopted
  row, and refuses as stated above. OI-73's "no third exit" holds: an
  adoption is the successor exit, a queued successor, not a third exit.
- **The mint** (`intake._mint` and `_draft_refusal`). An adoption block is
  never a draft and is never minted, and `_DRAFT_KEYS` does not gain
  `adopts`. Exact-title dedup resolves a standing successor's identity and
  lineage together, and refuses a mismatch before any write. This holds for
  drafts whether or not adoptions sit beside them.
- **The review scheduler and the merge gate** (`agent_loop.dispositions_drafted`
  and `integrate._verdict_owed`, both through
  `agent_policy.adjudication_review_owed`). They read the block's shape
  only, never the adopted row or the record. A well-formed adoption owes no
  spine review, because it mints and amends nothing. A malformed section
  (an unpaired fence included) or an unreadable spec keeps today's
  fail-toward-review rule.
- **The machinery-close peel** (`kitlib.verdict.mechanical_close_attestation`).
  What it verifies is unchanged. Its stated premise is that nothing a
  reviewer could judge differently enters the tree; that premise now names
  the record and the check that verifies it.
- **The historical absorption reader** (`consolidate._enacted_supersedes`,
  read through `enacted_absorbs`, `judged_absorbed` and
  `consolidation_successors` by the census's `_seed_pairs` and `clusters`,
  and by `adjudicate_brief._prior_lines`). It is unchanged. It reads only a
  `consolidate` outcome's drafts' `supersedes`, and an adoption carries no
  `supersedes`, so an adoption never counts as an absorption. It keeps its
  draft-only rule for bad input. An absent section enacted nothing. A block
  that does not parse is skipped, since the close and the mint refuse a
  malformed verdict and so no absorption rode on one. A consolidation close
  refuses an adoption (above), so no consolidation verdict on trunk carries
  one.
- **The successor sweep for Done-when verdicts** (`intake._successor_drafts`).
  A SUCCESSOR Done-when verdict still needs a draft. It reads the section
  through the same parser, so an unpaired fence there is refused too.
- **The registry readers and the converter** (`kitlib.registry.parse_spec_row`,
  `wi_convert`, `plan_artifacts`). They carry the `Adopted` column through as
  data and grant it nothing.

## Done-when

- A disposition verdict can discharge the successor obligation by adopting
  an existing open row whose `supersedes` names the closed row. The close
  validates the adoption once and writes the `adopted` record in its closing
  commit. The sweep re-points from the record and mints nothing. An early
  close that names neither a draft nor such a row is still refused by both.
- The scope of OI-73's "no third exit" is kept: naming an existing successor
  is the same exit (a successor is queued), not a third one.
- Tests, each red before its change:
  - The close: a valid adoption closes and writes the record. Each of these
    is refused and writes nothing: a missing, closed, unreadable or
    non-superseding row; an untokened title; a repeated adoption; and an
    adoption in a consolidation verdict. A drafted successor beside an
    adoption still mints.
  - The commit check passes the close's own commit, and a later commit that
    carries the record unchanged. It refuses each of these:
    - a record written in any other commit (a hand or agent edit, in a lane
      or staged on trunk);
    - a record that differs from the request, or that fails the validation
      in the parent's tree;
    - a record changed or removed later;
    - a requesting spec moved into `complete/` without a record.
  - The sweep: a recorded adoption re-points a dependent, including a late
    one, to the full successor set together with the drafts. It still does
    so after its successor completes, and in a shallow clone, which shows the
    sweep reads no history. Each of these is refused with nothing minted: a
    request with no record, a record with no request, the two differing, a
    malformed record, and an unreadable merged spec.
  - The parser: review 015's reproduction (a valid block, then an unclosed
    one) is refused at the close and at the sweep, for an adoption and for a
    draft.
- No `## Dispositions` section on trunk fails the tightened grammar. This is
  checked over every spec and verdict file that has one.
- The spine states the change and passes adjudication:
  - SR-148, LLR-153, LLR-161, LLR-312, TC-147, TC-156 and TC-254 are re-sat.
  - The reshaped LLR-335 and TC-360, and the commit check's new rows, are
    first-approved.
  - IF-294 states the seam as rebuilt.
  - The lane's acts 113–117 never reach trunk.
- Reviews run in the shape the `coordinator-cycle` skill carries once WI-911
  lands. The lane's round count starts at zero at its next review (plan,
  revision 6–7 clarifications), recorded as a lane decision.
- `RESYNC_PACK.md` has one entry anchored at a trunk commit, replacing the
  lane's, with no forced migration. It names three tightenings:
  - an unpaired fence is refused, for drafts too;
  - an unreadable merged spec refuses the sweep;
  - a drafted title on another lineage refuses the mint.
- The bar is green on the landing tip: the smoke tier within its budget,
  `check_trajectory.py --strict` clean, and `trace.py --strict` with no
  finding beyond LLR-292's.

## Scope answers

- **S1:** three deliverables could each land alone.
  - **(A) The section parser's unpaired-fence refusal.** It fixes a defect
    trunk already has for drafts: when a valid draft is followed by an
    unclosed one, the second draft is silently lost.
  - **(B) The record at the close.** This covers the record, its cell, the
    commit check, the sweep that trusts the record, and the deleted history
    readers. B's parts cannot land apart: the record is trustworthy only
    through the check, and the check has nothing to judge without the record.
  - **(C) The mint's lineage corrections** (deliverable 10). A drafts-only
    replay re-points to the full successor set, and an exact-title match on
    another lineage refuses the mint. Both fix trunk's mint for drafts,
    without the record.

  They are kept together at the coordinator's direction
  (`docs/decisions/coordinator-2026-10-14.toml` D-013 for A, D-014 for C),
  for four reasons:
  - the reshape rewrites A's parser and its return shape;
  - A's regression is review 015's adoption reproduction;
  - C's functions are the ones B's lineage join extends with adopted pairs,
    and C is already built and reviewed in the lane (D-004 builds dispute
    004's FIX);
  - a split would serialize more mechanism landings on the same functions.

  If the owner splits them, A and C land first, in either order, then B.
- **S2:** yes. Two authorities are created: the request gives the
  adjudicator's text authority over the close, and the record gives the
  close's result authority over the sweep's re-point. The commit check gates
  the record. See `## Trust`.
- **S3:** every input space is enumerated, and anything outside it is
  refused:
  - **Section fences:** an opening `` ```toml `` line and a bare `` ``` ``
    closing line, paired in order. Any other fence line, or an unpaired one,
    is refused.
  - **Block keys:** an adoption block holds exactly `adopts`; drafts keep
    `_DRAFT_KEYS`.
  - **Title event token:** exactly one, leading with exactly one WI id.
  - **Open states:** `draft`, `queued` and `active`.
  - **Record shape:** a non-empty list of distinct, well-formed ids, equal to
    the request's.
  - **Commit-check cases:** the close's own commit, a record carried
    unchanged, and a merge judged by what neither parent carried. Every
    other record change is refused.
  - **The sweep's request-and-record pairs:** neither present, or both
    present and equal. Any other pair is refused.
- **S4:** `single`. The row has a Trust section and promises behaviour over
  input spaces. It also touches several script families: `handback`,
  `intake`, `kitlib`, the registry tables, the per-commit rules and the hook.
  It builds after WI-913 (G).
- **Architectural delta:** yes, within this row's scope.
  - It adds a value to the work-item row's domain (the `Adopted` cell) and a
    block shape to the Dispositions grammar.
  - The close's output gains the record, which depends on the request.
  - The sweep's re-point depends on the record.
  - A rule joins the per-commit walk and the hook.

  It crosses no new boundary: the check reads git trees as text-then-act
  already does, and the lane's git-history input is removed.
- **Dependencies:**
  - **Waits on:** WI-911 (the record-at-event rule and the critique anchors
    this amendment is judged against) and WI-913 (G, because S4 is
    `single`). Both must land before the rebuild's first build. They are soft
    edges, as the batch's other rows carry theirs; the coordinator's queue
    sets the order.
  - **Not WI-914 (B2):** no act of the lane lands at its old seq (see the
    lane record), so WI-914's LLR-292 act takes seq 113 without a collision.
  - **Downstream:** WI-810 already needs this row, and P4 and P5 follow it,
    since they share `handback.py` and `intake.py`.
  - **Landing:** it changes machinery the cycle runs on (the close, the
    sweep and a hook step), so it lands alone.
  - **Third-party:** none.

## Critique dispositions

Round 1 (Codex Sol, medium, 2026-10-14; APPROVE, one finding):

- **S1, MINOR: adopted.** The S1 answer now names a third independently
  landable deliverable, "(C) The mint's lineage corrections (deliverable
  10)", carried by deliverable 10, and records keeping it in this landing
  with its reasons and the order if split: "If the owner splits them, A and
  C land first, in either order, then B." The keep-together is
  `docs/decisions/coordinator-2026-10-14.toml` D-014.
