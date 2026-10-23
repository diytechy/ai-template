+++
id = "WI-851"
title = "Held-rung spine rows are protected by state: the registry, the snapshot and the dial"
workstream = "process"
sr_refs = ["SR-208", "SR-178"]
specref = "docs/plans/2026-10-07-wi841-retro/PROPOSAL.md"
needs = ["WI-892", "WI-849"]
buildtier = "strong"
safety_class = "ordinary"
priority = 5
planmode = "single"
+++

## Context

Amended 2026-10-20 (coordinator-2026-10-20 D-013): WI-807 and WI-810 are cancelled (D-009, D-010); where this spec names them as later amenders of LLR-246, read WI-800 and WI-809 only.

Re-homed 2026-10-10 (D-015): the shared lane-commit walk this row rides
moved from WI-828 (closed partial) to WI-892, which landed the same day.
OI-113 was ruled (d), won't fix, on 2026-10-14, and WI-893 was cancelled: no
hook walks a hand merge, and the merge slot is the sanctioned landing path.

Amended 2026-10-14 (the review-churn plan's revision 36, owner): a headless
coordinator leg is marked as an autonomous run (`KIT_LOOP_SESSION`), and its
held acts stay refused. Ruling 5 exempts a direct trunk approval "by the owner
or an authorized approver", which an autonomous run is not, so the
marker-armed arm of `held-status` narrows to a marked commit outside a lane
instead of retiring.

Filed by hand on 2026-10-07 from the WI-841 retrospective (proposal §7.1,
row P4), carrying the owner's ruling 5 of 2026-10-07
(`docs/log.d/2026-10-07-wi841-retro-owner-rulings.md`): held-rung rows are
protected by state alone. The rule judges what lands from a lane. A direct
trunk approval by the owner or an authorized approver is not judged.

Today two checks protect a held rung, and neither judges state:
- `held-status` (pre-commit and a merge-slot rung) is armed only for commits
  carrying the `Loop-Session` trailer. "A person's own lane is not governed",
  and no coordinator-path commit carries the trailer, so a coordinator lane
  counts as a person's.
- `held_reattest_refusal` requires an adjudication act to name a CLARITY
  verdict in the act ledger.

The coordinator lands by hand, so the rule rides the lane-commit walk that
WI-892 made shared between the merge slot and the hook's squash path.

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

Amended 2026-10-23 (scope critique, leg 16). Since filing, WI-912 split the
judging turn from the act turn (`adjudicate_act.py`, runtime flow 6) and
WI-943 made a MEANING row's blessing a typed mark (`[MEANING+BLESS]`, read by
`kitlib.sitting.judged_rows`). Neither binds a judged row's text: the binding
beside a verdict records the brief class, the requested kinds and the outcome
(`kitlib.sitting.render_requested`), and the amendment grammar's machine line
carries `rows=` only. Two gaps follow today, both closed by this row:
- A held-rung first approval lands from any lane when an accepted APPROVE
  verdict backs it. `merge_approval_refusal` reads the dial for
  re-attestations only, and the `held-status` rung and step watch the
  off-spine registries and the stakeholder table, never a spine tier.
- A held row's text edited after its CLARITY sitting is still re-attested.
  `held_reattest_refusal` and the act turn check the ruling, not the text;
  flow 6's "the coordinator has confirmed the judged rows are unchanged" is a
  hand step.

## Deliverables

Four units could land alone. They land in this order:
1. **The row-text identity.** One digest of a row's approved text; the
   amendment brief states it per row; the verdict's binding records it at
   reservation; the act turn reads it. Its readers need it, so it lands first.
2. **The lane rule** (the held-approval judgement, its slot rider and its
   squash path in the hook).
3. **The retirements:** the act-ledger CLARITY arm and the slot's loop-lane
   `held-status` rung retire, and the marker arm narrows. Units 2 and 3 land
   in one commit, so no landing leaves a held rung with no rule, or with two
   rules that disagree.
4. **Text:** the spine rows, the `spine-authoring` line and the RESYNC entry,
   landed with unit 3.

Behaviour-preserving moves the plan needs (the claimed-branch reader into
`kitlib`, and any move of `acceptance_record`'s held-status section under the
size ratchet) are their own commits, before unit 1. The units stay in one row
because together they replace one authority rule end to end. Unit 1 alone
would change the binding grammar while the slot still enforced the ledger arm,
and it would put LLR-278 and IF-287 through two sittings.

## Trust

Done-when gives five carriers authority over a lane's landing and over a
marked commit: the committed dial, the live registries, the snapshot copies,
an accepted verdict with its binding (which now records the row-text
identity), and the git state that says whether a commit is a lane's. All are
files on disk, and the verdict is model output, so the guard is owed under
[PROCESS.md §3, "When a guard is owed"](../../../../project-trajectory/PROCESS.md#3-traceability--anti-duplication).

- **Producers and failed-write shapes:**
  - *The dial:* `[attestation] human_approval_through` in `docs/process.toml`,
    edited by the owner or an authorized policy editor in a reviewed commit.
    Failed shapes: an uncommitted edit, unparseable TOML, an unknown rung, a
    legacy key.
  - *The live registries:* the eight `baseline_snapshot.SNAPSHOTTED`
    registries, under the carriers `spine_carrier` resolves. They are written
    by authoring edits, by the act turn's `Status` edits and by the owner.
    Failed shapes: as WI-850's (a decode error, a missing or out-of-vocabulary
    status, a truncated file, a carrier under both forms).
  - *The snapshot copies* under `docs/archive/last_approved/`:
    `baseline_snapshot.copy_live`, reached only through `intake.py snapshot`.
    It writes whole-registry byte copies, so a Drafted sibling rides an act's
    copy, and it removes stale other-carrier copies. Failed shapes: a partial
    act (some copies written), a hand edit (the mirror invariant's finding),
    no record yet (never signed), and a lawfully absent first copy
    (`FIRST_COPY_AT_APPROVAL`).
  - *The verdict and its binding* (`<verdict>` and `<verdict>.requested`
    under `docs/reviews/`):
    - The adjudicator session writes the verdict, which is model output.
    - The route writes the binding through `kitlib.sitting.write_binding`:
      `adjudicate_brief.bind_pending` writes it at reservation
      (`coordinator_adjudicate.py`, exclusively) or at composition (the loop),
      and `adjudicate_brief.record_outcome` records `accepted` or `failed` in
      its own commit (`agent_common.commit_telemetry`).
    - New here: the binding gains an identity cell (`rows`), naming each row
      the brief showed with the digest of its approved text. `bind_pending`
      writes it at reservation from the brief's identity lines (one
      `JUDGED-TEXT: <row> <digest>` line per row, which the amendment
      composer renders). The adjudicator's rewrite cannot touch it.
    - Failed shapes: a pending binding (the call crashed), a failed outcome,
      an empty or partial verdict, a verdict invalid against its binding, a
      binding written before this row (no identity cell), and a malformed
      identity cell.
  - *The act ledger* (`acts.toml`): `baseline_snapshot._record_act`, appended
    in the snapshot act. The held rule stops reading it (see Consumers).
  - *Whether a commit is a lane's:*
    - the loop marker (`kitlib.provenance.loop_session`);
    - the claimed-branch reader (`check._claimed_work_branch`, moved into
      `kitlib`): the checkout's branch holds, or once held, a claim under
      `docs/work/active/<branch>/`;
    - git's `SQUASH_MSG` (`kitlib.git.squash_commits`).

- **Consumers** (grep over `project-trajectory/scripts`,
  `project-trajectory/hooks` and `scripts/coordinator`:
  `held_reattest_refusal|held_status|loop_held_status_refusal|dial_at|accepted_at|requested_path|write_binding|_record_act|_ledger_acts|copy_live|LANE_COMMIT_RIDERS|squash_commits`):
  - *The rule's one home:* `acceptance_record`'s held-status section
    (IF-196). It holds:
    - the approved-text digest, beside `split_changed_cells` (IF-129), so the
      digest and the drift report class cells one way;
    - the held-approval judgement over a tree and its parents, with a
      per-commit rider form and a squash form;
    - the existing status-move readers (`staged_status_moves`,
      `held_status_lines`), unchanged.

    The plan may move that section whole into its own module first (WI-892's
    move of text then act), so `acceptance_record` does not grow.
  - *The identity record's one home:* `kitlib.sitting` (IF-287).
    `render_requested` and `read_requested` gain the identity cell, and one
    reader returns an accepted verdict's bound identities. Every other reader
    of a binding ignores the cell: `kitlib.done_when`, `plan_gate.py` and
    `plan_coverage.py` read `brief`, `kinds` and `outcome` only.
  - *Callers that only call:*
    - `adjudicate_brief.py`: the amendment composer (`amendment_values`,
      reached also by `combined_values`) renders the identity lines;
      `bind_pending` reads them.
    - `adjudicate_act.py` (IF-296), `_state`: for a held CLARITY
      re-attestation, the act is owed only while the committed row's digest
      equals the bound one. Otherwise the derivation refuses, naming the row,
      so `coordinator_adjudicate.py act` refuses before launch.
    - `text_then_act.py`: the rider joins `LANE_COMMIT_RIDERS` after
      parent-first. `_squash_lines` keeps walking text then act's own rider
      only.
    - `integrate.py`: `_text_then_act_refusal` already walks every rider.
      `_held_status_refusal` and its call in `_merge_refusal` retire.
      `_loop_window` stays for the trailer rung; a re-claim's closed window
      exempts nothing from the lane rule, which reads no window.
    - `check.py`, the `held-status` step (no new step name, so adopters' step
      lists do not change):
      - on a squash landing, it walks the squashed lane commits with the
        rider;
      - on a marked commit outside a lane, it runs the narrowed arm;
      - otherwise it passes.
    - `agent_policy.loop_held_status_refusal`, which `agent_common`
      re-exports, narrows to a marked process outside a lane. Its writers
      follow without code changes:
      - `bookkeeping._commit_object` (the claim and the mint, always on
        trunk) is still judged;
      - `handback._loop_commit` (always in a lane worktree) no longer refuses
        at commit, and its lane is judged at landing;
      - `agent_common.commit_telemetry` is judged where its root is outside
        a lane.
    - `acceptance_record.merge_approval_refusal`: the
      `held_reattest_refusal` call and the function retire. `lane_acted_set`,
      `backed_act_refusal`, `reattest_scope_refusal`, `unaccepted_refusal`,
      `uncovered_refusal` and the copy check (WI-849's) are unchanged.
  - *Readers checked and unchanged:*
    - `kitlib.authority` (IF-195);
    - `baseline_snapshot.copy_live`, `_record_act` and the
      `intake.py snapshot` CLI: `--verdict` stays optional and is recorded
      for audit, but no rule requires it;
    - the ledger's other readers: `lane_acted_set`, `pending.py`, and the
      risk-acceptance views `record_observation.py` and
      `assumption_rules.py`, which report evidence and grant no release;
    - `kitlib.provenance` and `scripts/coordinator/overnight_legs.py`, which
      read re-claim records for the trailer rung only;
    - the parent-first rider and step (IF-308);
    - `check_trajectory.loop_held_status_findings` (SR-210), the history
      advisory. It stays warn-only, reads each trailer commit against its own
      tree's dial, and is never consulted by the hook or the slot. Under
      Done-when's rule it also lists in-lane loop commits whose non-approval
      held status moves now land (its audit surface).
    - `trace.py`'s integrity floor: the ledger shape and the mirror invariant.

- **Ruling** (drafted for the owner to confirm or overrule):
  - *What the authority binds to:*
    - The hold: the dial committed at HEAD of the checkout that runs the
      judgement. That is trunk at the slot and at a squash landing, and the
      commit's parent for the narrowed arm. Never a lane's own tree, never a
      working file.
    - A claim: one lane commit's tree against each of its parents. A claim
      counts as the commit's own only when it is a claim against every
      parent, so a refresh merge that brings in trunk's own approvals claims
      nothing.
    - The exception: a (row id, approved-text digest) pair recorded in an
      accepted binding committed in that commit's tree. Never a verdict's
      text alone, and never a ledger entry.
  - *The dial:* read through `kitlib.authority.dial_at`. Absent, unreadable,
    malformed or unknown reads as the most-held rung, and legacy spellings
    translate. A registry or tier the rung map does not name is held.
  - *The registries and the copies at a tree* are read through
    `kitlib.git.git_show` and `spine_carrier`'s text readers, as WI-850's
    judgement reads them. Never through `_spine_rows_at`, which takes both
    failures for absence.
    - Absent on the commit side: no rows.
    - Listed but unreadable, or not parsing, on the commit side: a refusal
      line naming the file and the tree.
    - The same on a parent side: every approval-claiming held row of the
      commit side counts as a claim.
    - A diff git cannot produce: a refusal, never a skip.
    - No HEAD yet: nothing is judged.
  - *The verdict and the binding:*
    - Any of these gives no exception: no binding; a pending or failed
      outcome; a verdict invalid against its binding; an accepted verdict
      that does not rule the row CLARITY (a row tagged both ways, or marked
      `[MEANING+BLESS]`, included); no identity cell; a malformed cell; a
      digest that differs.
    - Candidate bindings are found by the row's identity among the bindings
      committed under `docs/reviews/` in the judged tree, and each candidate
      is read through `kitlib.sitting.accepted_at`.
    - A missing exception refuses the row. It is never an error that stops
      the walk.
  - *Whether a commit is a lane's:*
    - Off git, or with a detached HEAD, a commit reads as outside a lane, so
      a marked commit is judged.
    - An unreadable `SQUASH_MSG` reads as no squash. An unmarked commit is
      then a plain trunk commit, not judged (the ruled residual). A marked
      one gets the narrowed arm.
    - A squash is admitted as a landing when its tip contains HEAD and the
      staged snapshotted registries and record equal the tip's. Otherwise
      its index is judged as one lane commit against HEAD.
  - *A crashed step* exits nonzero, which the runner reads as FAIL.

- **The bound**
  ([PROCESS.md §6, "Review threat model"](../../../../project-trajectory/PROCESS.md#6-review-depth-triage-efficiency)):
  - Inside: what supported workflows and the kit's own routes write, a hand
    edit of an authored row included.
  - Outside:
    - hand-edited kit-written state: a binding, a snapshot copy, a composed
      brief file, or `SQUASH_MSG` (for example deleted by a stash);
    - a hand-chosen id alias;
    - a sub-second window;
    - a digest collision (64 bits, an identity, not an authentication).
  - Residual (proposal §7.1): an agent's unmarked plain commit on trunk is
    not judged, and stays review-enforced.

## Architectural delta

- **New state:** the binding's identity cell (IF-287). Its producer is
  `bind_pending`, from the composer's `JUDGED-TEXT:` lines. Its readers are
  the act turn (IF-296) and the lane rule (IF-196). One function computes it,
  next to IF-129: SHA-256 over the row's approved cells (id and `Status`
  excluded, classed by `spine_cell_class`), serialized as sorted JSON, then
  truncated as `kitlib.done_when.digest` truncates. This answers the
  2026-08-15 directive that retired a row text hash, point by point:
  - no on-row cell;
  - no separator problem, because JSON escapes;
  - no second exclusion list, because the digest uses IF-129's classes.

  A copy cannot do this job. It is written at the act, so it cannot witness
  the sitting. A recorded commit id cannot do it either, since the rebase
  acts require rewrites it.
- **An output depends on a new input:** a lane's landing now depends on the
  snapshot copy's movement and on the bound identity, rather than on loop
  provenance. The marker arm's output now also depends on whether the commit
  is a lane's (the claimed-branch reader).
- **Shared owners it stays inside:**
  - `acceptance_record` (or its held-status section, moved): the rule and the
    digest;
  - `kitlib.sitting`: the binding;
  - `adjudicate_brief`: the producer;
  - `adjudicate_act`: the act turn;
  - `text_then_act.LANE_COMMIT_RIDERS`: the walk;
  - `agent_policy.loop_held_status_refusal`: the one writer composition;
  - `check.py`'s `held-status` step;
  - `kitlib.authority`: the dial.

  The claimed-branch reader moves from `check.py` into `kitlib` as a
  behaviour-preserving commit, so `check.py` and `agent_policy` share one
  reader. No consolidation beyond these owners is needed, so no preparatory
  row is filed.
- **Interface rows:**
  - amended: IF-196 (it gains the held-approval judgement; its callers
    narrow), IF-287 (the identity cell and its reader), IF-296 (the held
    CLARITY refusal reason) and IF-129 (the digest);
  - notes only: IF-220 (the ledger's `verdict` is recorded, and no rule
    requires it);
  - unchanged: IF-195, IF-124, IF-175 and IF-308.
- **Runtime flow 6:**
  - The judging turn's bind step also records the judged rows' identities.
  - The act turn's refusal branch gains "a held CLARITY row whose approved
    text differs from its bound identity".
  - The prose's hand confirmation that judged rows are unchanged becomes
    that check for held CLARITY rows.

## Done-when

- On every lane commit, judged against each of its parents, a row is judged
  when its registry is one of the eight snapshotted registries and the dial
  committed on trunk holds its tier's rung. The commit makes an approval
  claim on the row when either holds, as a claim against every parent:
  - (a) the row's live `Status` moved into `Approved` or `Founded`
    (`kitlib.spine.claims_approval`), a row added already claiming one
    included; or
  - (b) the row's snapshot copy claims approval at the commit and entered
    the copy, or moved in its approved cells or `Status`; or the copy held
    the row claiming approval at the parent and holds no row at the commit
    (a retirement).

  A claim is refused, naming the row, its rung and the dial, unless all of
  these hold:
  - it is a (b) claim;
  - the row's live `Status` is unchanged and claims approval on both sides;
  - the live row equals its copy at the commit;
  - an accepted amendment verdict in the commit's tree rules the row CLARITY;
  - that verdict's binding records the row's approved-text digest, equal to
    the row's at the commit.

  Not judged:
  - a row that claims approval in neither the copy nor the live registry,
    such as a Drafted sibling that a whole-registry copy carries;
  - a demotion, or a status move between values below approval;
  - a copy move in traced cells only;
  - a row on a released rung;
  - an example `-000` row.
- The walk is WI-892's shared lane-commit walk:
  - at the merge slot, the rider in `LANE_COMMIT_RIDERS`;
  - in the hook, the `held-status` step on a squash landing, walking the
    squashed commits, or judging the index as one lane commit when the
    squash is not admitted as one.

  An unmarked plain trunk commit is not judged.
- The row-text identity: the amendment brief states each row's approved-text
  digest, and the binding records it at reservation. The act turn refuses
  before launch, naming the row, a held CLARITY re-attestation whose
  committed text no longer matches. Runtime flow 6 says so.
- The act-ledger CLARITY arm (LLR-278's held clause, `held_reattest_refusal`)
  retires into this one rule, in this row. `intake.py snapshot --verdict`
  stays optional and recorded. WI-849's backing, scope and copy checks are
  unchanged.
- The marker-armed arm of `held-status` (LLR-246's loop-marker condition)
  narrows instead of retiring. A commit made under the loop marker outside a
  lane, other than a squash landing, that moves a held status or makes a held
  approval claim is still refused:
  - at pre-commit;
  - by each loop writer, through `agent_policy.loop_held_status_refusal`.

  The slot's loop-lane `held-status` rung retires into the lane rule.
- `spine-authoring`'s `references/in-lane.md` held CLARITY line follows the
  rule (proposal §8.4). The CLARITY verdict, bound to the text, is what
  permits the act; naming it with `--verdict` is for audit.
- WI-800 and WI-809 amend LLR-246 after this row and cite this rule.
- Its rows (SR-208, LLR-246, LLR-278, TC-241 and TC-278, and the contract
  text of IF-196, IF-287, IF-296 and IF-129) are authored as one change set
  and judged in one combined sitting. All of them sit on released rungs here,
  so the sitting needs no owner act.
- Tests:
  - a lane commit that approves a held SN, with its copy, is refused, and so
    is one that flips a held row's `Status` without its copy;
  - loop and coordinator lanes are judged alike, and a re-claimed lane is
    judged too;
  - a CLARITY re-attestation bound to the exact text passes;
  - text changed after that verdict is refused, at the slot and by the act
    turn before launch;
  - a binding with no identity cell, and a held `[MEANING+BLESS]`
    re-attestation, are refused;
  - a held retirement is refused;
  - Drafted sibling: a held CLARITY act whose whole-registry copy carries a
    Drafted row edited in the lane passes, and so does a traced-only copy
    move;
  - a refresh merge carrying trunk's approvals passes;
  - an unreadable or unparseable registry or copy at the commit is refused,
    naming it;
  - an unmarked plain trunk commit approving a held row passes;
  - the same commit made under the loop marker is refused, by the hook step
    and by each loop writer;
  - a marked commit inside a lane passes at commit and is judged at landing;
  - a squash landing, marked or not, is judged by its lane commits, and a
    squash not admitted as one is judged as one commit.
- RESYNC_PACK: an entry anchored at a trunk commit. It names:
  - the retired CLARITY arm and the narrowed marker arm;
  - that an adopter's unmarked trunk approvals are untouched;
  - that a held CLARITY verdict sat before the upgrade carries no identity
    and is re-sat.

No third-party dependency is proposed.

Dependencies:
- **WI-892 (landed):** it made the lane-commit walk shared between the slot
  and the hook's squash path, which the rider joins.
- **WI-849 (landed):** it built the kit-wide acted set (`lane_acted_set`)
  and the accepted-verdict backing (`backed_act_refusal`,
  `kitlib.sitting.judged_rows`). This row keeps those whole and replaces only
  the held-rung clause, and its exception reads the same accepted-record
  reader.

## Critique dispositions

Scope critique (Codex, 2026-10-23, leg 16; CHANGES-REQUESTED, findings=6):

- **F1, MINOR, S1 (no deliverable order): adopted.** `## Deliverables`
  lists four units: "Unit 1 ... lands first", and "Units 2 and 3 land in one
  commit, so no landing leaves a held rung with no rule, or with two rules
  that disagree". It records the reason for one row: "together they replace
  one authority rule end to end".
- **F2, MAJOR, S2 (no Trust section; a bare verdict): adopted.** `## Trust`
  names the five carriers with their producers and failed-write shapes, the
  consumers by path with the grep that found them, and a ruling per input.
  The verdict ruling reads: "Any of these gives no exception: no binding; a
  pending or failed outcome; a verdict invalid against its binding; an
  accepted verdict that does not rule the row CLARITY ...; no identity cell;
  a malformed cell; a digest that differs."
- **F3, MAJOR, S3 (an open predicate; the Drafted sibling): adopted.** Checked
  against `adjudicate_act`'s docstring ("a whole-registry copy carries Drafted
  rows") and `copy_live`. Done-when's first bullet is now a closed predicate:
  claims (a) and (b), the exception, and "Not judged: a row that claims
  approval in neither the copy nor the live registry, such as a Drafted
  sibling that a whole-registry copy carries". Tests carry "Drafted sibling:
  a held CLARITY act whose whole-registry copy carries a Drafted row edited in
  the lane passes".
- **F4, MAJOR, S4 (no `planmode`): adopted.** The frontmatter carries
  `planmode = "single"`.
- **F5, MAJOR, S5 (no digest carrier; the marked writers): adopted.**
  Confirmed in the code: `GRAMMAR["amendment"]` carries `rows` only, the
  binding records `brief`, `kinds` and `outcome`, and neither bless mark nor
  binding carries a digest. `loop_held_status_refusal` reads the marker
  alone, so `handback._loop_commit` refuses inside a lane. `## Architectural
  delta` declares the identity: "Its producer is `bind_pending`, from the
  composer's `JUDGED-TEXT:` lines. Its readers are the act turn (IF-296) and
  the lane rule (IF-196)". `## Trust` gives each writer's disposition, for
  example "`handback._loop_commit` (always in a lane worktree) no longer
  refuses at commit, and its lane is judged at landing".
- **F6, MINOR, S6 (WI-849's reason): adopted.** The Dependencies list:
  "WI-849 (landed): ... This row keeps those whole and replaces only the
  held-rung clause", and "No third-party dependency is proposed."

The three calls the revision drafted for the owner (the row-text digest in the binding, approval claims only in the lane rule, and the narrowed marker arm across all eight snapshotted registries) are recorded as coordinator-2026-10-23 D-002 to D-004, to confirm or overrule.
