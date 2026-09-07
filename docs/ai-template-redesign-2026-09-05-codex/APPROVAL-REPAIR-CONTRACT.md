# Approval repair — governing amendment proposal

Status: authoring only. This document grants no approval and changes no live
spine or snapshot. Each exact amendment below needs independent whole-chain
judgment before runtime implementation.

## Minimal carrier design

An adjudication WI stays queued. Under the existing coordinator/integration
lock, the coordinator runs the existing review engine in process in the primary
checkout, with explicit arguments saying that the lock is already held. It
creates no worktree, branch, or active claim. One immutable pending record at
`docs/reviews/primary/<WI>-<base>/turn.toml` binds a unique turn, WI, primary
base, primary branch/root identity, exact initial spec/frontmatter scope, and
live and approved registry blob identities. Existing verdict files carry judgment and
review progress. A pending record resumes before queue selection and blocks all
other primary writers. Completion derives from the terminal spec and final
publication commit; there is no additional phase enum or journal.

The queued WI gains an `## Approval` fenced TOML section whose exact per-row
decisions are already part of the non-record tree identity used by review; no
decision registry or ignored-record hash is added. The existing intake writer
gains a stage-only operation. From those reviewed `## Approval` bytes, exact
candidate binding, `Adjudicates` scope and WI-596 absorb
ledger, it deterministically stages the allowed Status/snapshot/close/successor
projection. The coordinator commits that projection atomically while retaining
the lock. `UNCERTAIN` is a semantic outcome, never a Status or lifecycle phase:
the existing CLARITY/MEANING verdict grammar may record zero accepted cells and
hold the baseline. Every WI branch,
including an adjudication-class branch, is refused for snapshot and approval
ledger writes.

The adjudicator remains the Git **author** of the approval commit. The
coordinator is its mechanical **committer**. A human is author only when the
bound record contains the actual human act. This preserves SR-140, LLR-173 and
TC-167 unchanged; no new actor registry or `approval_actors` reader is proposed.
For an automatic turn, the canonical machine author is derived only from the
actual committed ADJUDICATE log's provider, roster row, model, session id and
invocation identity, all bound to the turn; configured or ambient Git identity
is not evidence. A human author requires a bound real human act through the
existing manual primary path. Missing, mismatched, merely asserted or
human-looking automatic identity refuses publication and surfaces the turn.

Minimum pending record:

```toml
version = 1
turn = "<WI>-<base>"
wi = "<WI>"
base = "<40-hex primary commit>"
primary_branch = "<configured integration branch>"
primary_root = "<stable repository identity>"
proposal_spec_blob = "<git blob id of initial queued spec>"
scope = ["<exact Adjudicates ids, or typed brief scope>"]
registry_blobs = { "<live registry path>" = "<git blob id>" }
approved_blobs = { "<snapshot registry path>" = "<git blob id>" }
```

Creation refuses another pending turn or duplicate WI/base record. The proposal
blob is the immutable starting proposal, not a demand that the live spec blob
remain equal after judgment. Resume re-resolves primary and refuses missing,
duplicate, mismatched, dirty or stale-registry bindings; it also requires the
frontmatter and definition outside `## Approval` and `## Dispositions` to equal
the initial proposal. Those two sections may grow through judgment. Git computes
the resulting full non-record candidate identity after they are authored, and
existing review evidence binds that actual candidate. The pending record is
immutable; existing committed verdict files alone add progress.

Minimum `## Approval` payload:

```toml
version = 1
turn = "<WI>-<base>"
base = "<40-hex primary commit>"
proposal = "<base plus initial registry/spec identities from turn.toml>"
[[decision]]
registry = "<live registry path>"
row = "<row id>"
classification = "approve|equivalent|return|uncertain|meaning"
before = { "<cell>" = "<registry blob identity containing the before cell>" }
after = { "<cell>" = "<registry blob identity containing the after cell>" }
evidence = ["<committed judgment/review ref>"]
[[absorption]]
registry = "<registry path>"
row = "<row id>"
cells = { "<cell>" = { before = "<registry blob identity>", after = "<registry blob identity>" } }
judgment = "<accepted committed judgment ref>|UNJUDGED"
state = "approved-change|below-approval-rider"

[[impact]]
id = "<affected stable id>"
path = "<tracked path containing the use/reference>"
source_blob = "<git blob id at the reviewed candidate>"
disposition = "amend|retain|regenerate|history-unchanged"
evidence = ["<reviewed reason or implementation/test reference>"]
```

For the selected queued spec's own `(id, path)` census pair only,
`source_blob` is the turn's immutable `proposal_spec_blob`, because placing the
candidate blob id inside that candidate's `## Approval` section would require a
self-referential Git blob. Primary validation already proves that the spec's
frontmatter and definition outside `## Approval` and `## Dispositions` remain
equal to that proposal, while the final review binds the actual candidate
sections. Every other impact pair uses its reviewed-candidate blob. The census
still includes the queued-spec pair; this changes its representable identity,
not its coverage or approval force.

The candidate-wide census excludes only a path for which
`kitlib.verdict.is_record_path(path)` is true and Git proves the path was first
created after `turn.base`. Such a current-turn judgment, review or invocation
record is evidence produced by this decision and cannot be an input whose blob
the same decision must already contain. A record path that existed at or before
`turn.base` remains in the census like every other preexisting historical ID
use, even when it is historical evidence; no earlier reference is dropped or
reclassified merely because its path is record-only. The selected queued spec
rule above remains separate because that spec is not a record path.

`approve` is first approval; `equivalent` accepts unchanged meaning; `meaning`
requires completed ID-use impact review before acceptance; `return` and
`uncertain` accept no cells and hold the baseline. Each copied file lists every
changed Approved row/cell with an accepted judgment. Every Drafted rider is
listed `below-approval-rider` and stays Drafted. Any pending Approved-cell drift
outside accepted scope, or any `UNJUDGED`, blocks that whole file. This payload
is WI-596's ledger shape and single rule home.

If a requested approval cannot copy its whole registry because that ledger has
an `UNJUDGED` or out-of-scope changed cell, the adjudicator records `return` for
the approval, with zero accepted cells and no Status or snapshot effect.
Apparent-equivalence observations remain findings, not accepted judgment refs.
The same atomic RETURN closes with a concrete reanchor or corrective
continuation whose dependencies preserve the existing scoped WI owners. A
later reanchor independently judges the complete exact scope; it may cite the
RETURN as evidence but cannot reuse it as approval. A malformed or inconsistent
publication request is instead a mechanical refusal: the turn remains pending
for REWORK, where the request may be corrected to RETURN plus that continuation.

The `impact` rows cover the machine census of every tracked use of every
meaning-changing ID. Historical pairs use `history-unchanged` and are never
rewritten or treated as current approval; each live pair names a concrete
retain, amend or regenerate disposition. The verifier requires exact set
equality between censused and recorded `(id,path)` pairs and refuses duplicate,
missing or extra entries. This checks accidental drift with existing Git blob
identity; it adds no new cryptographic scheme and does not require future
implementation or test completion before the design judgment.

## Surgical cell amendments

Only the quoted fragments change. Every byte outside a shown replacement stays
as live, including the large retained mechanisms, rationales, trace links,
statuses, tiers and evidence lists.

### LLR-140 `Detail`

Replace:

> whether an adjudication lane owes a verdict at all is docs/process.toml
> [attestation] adjudication_review, read through the one function the loop's
> round scheduler also reads - over the same input, since which copy of a
> branch's spec answers for it when both the terminal and the active home carry
> one is decided by a single declared precedence (terminal first: it is what the
> closing session did) that both callers ask for rather than each walking the
> homes in its own order.

With:

> whether an adjudication turn owes a verdict at all is docs/process.toml
> [attestation] adjudication_review, read through the one function the loop's
> round scheduler also reads. For ordinary work that reader retains terminal-
> before-active branch precedence. For adjudication it reads the queued spec and
> bound primary-turn record; a pending turn resumes before selection, and the
> terminal spec plus its verified publication commit is the sole completed
> form.

Append before `ff-only trunk advance`:

> Adjudication is not passed to claim or integrate_one: while the same station
> lock is held, the coordinator invokes the review engine in process in the
> primary checkout, passing the resolved root, WI, turn identity, candidate and
> lock-held fact explicitly. The pending turn blocks claim, merge and direct
> integration until it returns or publishes atomically.

No ordinary claim, merge, audit, legacy-verdict or bar clause changes.

### LLR-152 `Detail`

Replace:

> The kind's lane runs NO product bar (integrate._lane_bar_directives +
> _refresh_bar: the refresh still merges trunk in, runs the trunk step and
> commits a verified Bar-Green attestation whose summary reads no-bar honestly)
> because its outputs are Status cells and the work registry, nothing a product
> bar can speak to; a mixed batch or unreadable frontmatter fails TOWARD the bar.

With:

> The kind runs as a primary in-process turn under the existing exclusive
> station lock, leaving its WI queued and creating no worktree, branch or claim.
> Its final mechanical projection runs NO product bar when the exact staged
> effects are confined to the queued spec's reviewed `## Approval` bytes,
> in-scope registry cells, named byte-identical snapshot files, that spec's move
> to `docs/archive/work/complete/`, parsed successor specs and id-watermark, and
> only generated paths already declared by the trunk step; the
> publication records that no-bar result honestly. A product effect, mixed
> scope or unreadable frontmatter fails TOWARD the bar.

Replace the final sentence fragment `for this row's lane` with `for this turn`
and replace `the refresh passes` with `the publication check passes`. Exclusive
rank 1 and the scheduling-independent `bar` key remain unchanged.

### LLR-153 `Detail`

Replace:

> Drafts-not-mints: a merged adjudication row's ## Dispositions fenced-toml
> drafts mint at ITS merge, validated loudly.

With:

> Drafts-not-mints: an adjudication turn's ## Dispositions fenced-toml drafts
> mint in ITS final primary publication, validated loudly. The same intake
> writer first derives a stage-only, deterministic projection from the bound
> `## Approval` bytes, exact candidate and scope: permitted Status changes,
> byte-identical snapshots, the queued-to-terminal move, successor specs and
> id-watermark, plus only paths already in the trunk-step generated set. The
> coordinator commits that one projection
> atomically; `return` and `uncertain` decisions include no snapshot, and a
> `meaning` decision includes none until its impact review is accepted. A stale
> candidate, malformed draft, out-of-scope effect or UNJUDGED absorbed cell
> refuses before allocation or staging. When UNJUDGED or out-of-scope drift
> makes a requested whole-file approval unpublishable, the adjudicator may
> revise the request to `return` with zero accepted cells and a concrete
> dependency-preserving continuation; that RETURN closes atomically without a
> Status or snapshot effect, and its findings are evidence rather than approval
> for the later complete-scope reanchor.

Replace `The mint commit mirrors the claim's bookkeeping shape` with:

> An ordinary mint commit retains the claim bookkeeping shape; adjudication
> completion is the terminal spec plus its matching publication commit, so a
> restart neither needs a journal state nor allocates again.

Every existing trigger, watermark, context-block, approval-level and
idempotence clause remains unchanged.

### LLR-154 `Detail`

Append:

> The same held slot also owns branchless adjudication publication. It remains
> held from primary-turn admission through judgment, required review and the
> intake writer's stage-only final projection. The scoped no-product-bar and
> strictness directives apply to that projection directly; no lane refresh is
> manufactured. A refusal leaves the queued spec and pending record for resume
> before any other selection.

The existing post-merge intake arm remains byte-for-byte unchanged.

### LLR-158 `Detail`

Replace:

> lane_approval_refusal — the judgement over that reader — refuses a lane
> signing a NEED as readily as one signing an LLR.

With:

> lane_approval_refusal — the judgment over that reader — refuses every WI
> branch signing a NEED as readily as one signing an LLR, regardless of safety
> class. It also refuses every WI-branch snapshot or approval-ledger change,
> including an amendment with no Status flip. The only positive writer is the
> held primary turn's intake projection, which must bind the accepted decision,
> exact row scope and complete absorb ledger and must stage each snapshot as a
> byte-identical copy beside its approval effects.

The comparison basis, cell classes, four readers, withdrawal subtraction and
registry partition remain unchanged.

### LLR-167 `Detail`

Replace:

> `agent_loop.session_body` is the single fork BOTH routing arms take, so a
> claimed adjudication row gets the same brief whether or not a routing registry
> is configured.

With:

> the primary adjudication turn calls the same `agent_loop.session_body` review
> engine in process for BOTH routing arms, passing the designated primary root,
> queued WI, unique turn identity, primary base, candidate tree identity,
> declared scope and already-held lock explicitly, so every route receives the
> same bound brief without a worktree or branch.

Append:

> A blank-Brief adjudication receives a generic primary judgment assignment
> bound to the same turn, WI, base, candidate and scope and naming its verdict
> path. It contains no claim, branch, model-side close or snapshot instruction.
> A declared brief whose assembler fails remains HELD; it never takes this
> blank-Brief route. Ordinary non-adjudication work keeps its worker assignment,
> and there is no legacy adjudication-worker context.

Append:

> The committed verdict names that turn and exact candidate. A snapshot/live
> difference is evidence for semantic comparison and never approval by itself.

All assembler-specific derivation, all-or-none and refusal clauses remain
unchanged. WI-603 already owns LLR-167's earlier live drift; its brief must be
expanded to the combined exact before/after rather than silently replacing its
pending question.

### LLR-207 `Detail`

Retain every identity-fold, path-byte, logged-round, phase-count, trailer,
refresh, ordinary branch, fail-closed and evidence-tier clause. Make only these
carrier substitutions:

1. Replace the paragraph beginning `THE SECOND DISPOSABLE CLASS` through the
   paragraph's mechanical-close refusal cases with:

   > THE SECOND VERIFIED CARRIER is the primary adjudication publication. Its
   > attestation binds the queued WI, unique turn, primary base, reviewed
   > candidate and exact reviewed `## Approval` bytes. The verifier independently derives the
   > allowed final projection: only accepted scoped Status/snapshot effects, that
   > queued spec's exact existing close transformation, parsed successor specs and
   > id-watermark, plus only generated paths already declared by the trunk step.
   > The snapshot must equal live in that commit and
   > every absorbed changed cell must be accepted in the bound ledger. The
   > carrier maps the resulting tree to the reviewed candidate only when every
   > derived byte agrees; a hand-written subject, wrong WI or turn, stale
   > candidate, extra or missing path, cross-WI close, malformed successor,
   > partial snapshot or unreviewed decision refuses toward more review. This is
   > a verified projection, not a broad disposable-path class.

   The exact close transformation uses the existing `spec_move` rules: move the
   queued spec to `docs/archive/work/complete/`, clear `specref`, insert the
   machinery's fixed `## Deliverable` before `## Context`, and apply only the
   link rebasing `spec_move` derives. The verifier independently derives those
   bytes; “close” permits no arbitrary spec edit.

2. Replace branch-only inputs in the adjudication dial/scheduler paragraphs
   (`closed-lane repository`, dual active/terminal copies, and adjudication lane
   closing) with the queued spec + bound pending turn input and terminal spec +
   verified publication output. Keep branch precedence tests for ordinary work.

3. Append:

   > A pending turn is resumed from committed verdict evidence before queue
   > selection. Git atomicity gives the only crash boundary: before the final
   > commit the queued spec and pending record remain; after it the terminal spec
   > and verified carrier establish completion. No publication phase marker is
   > read.

Remove the adjudication mechanical-close writer/peel from `CodeSymbol`; add the
primary-turn publication attestor. Do not change the ordinary refresh peel.

### TC-146 `Method`

Preserve the existing rank, bar-key and fail-toward-bar cases. Replace only the
adjudication-lane case with:

> a queued adjudication runs in primary with no worktree, branch or claim; it
> drains and excludes all other writers through publication, records the scoped
> no-product-bar result, resumes a pending turn before selection, and derives
> completion only from its terminal spec and verified publication commit.

### TC-147 `Method`

Preserve every existing intake trigger, context, approval-level, refusal,
dedupe and allocation case. Replace `a merged adjudication row's ## Dispositions
drafts mint at its merge` with:

> a primary adjudication's dispositions, exact accepted Status/snapshot effects,
> queued-to-terminal move, successors and generated records are derived by the
> stage-only writer and land in one atomic publication; stale, out-of-scope,
> malformed or UNJUDGED input stages nothing; a crash before it leaves pending
> work and a crash after it derives complete without a duplicate id.

### TC-148 `Method`

Preserve the ordinary merge/intake and idle-loop cases. Add:

> Drive a branchless adjudication under the same integration slot and assert no
> claim, merge or direct integration interleaves; the stage-only publication
> receives the scoped bar directive, and each refusal leaves one resumable
> pending turn with no partial commit.

### TC-153 `Method`

Preserve every existing drift-basis case. Add:

> Drive ordinary and adjudication-class WI branches attempting snapshots,
> approval-ledger writes, first approvals and amendment-only snapshot changes;
> all refuse. Drive the held primary writer against accepted exact scope and the
> full seven-registry census, listing each changed Approved cell as accepted or
> UNJUDGED and every Drafted rider below approval, then against returned, stale,
> extra-cell and UNJUDGED
> inputs; only the first stages a byte-identical snapshot projection.

### TC-161 `Method`

Preserve every assembler, prompt-slot, digest, refusal and first-approval case.
Replace lane-root assertions with:

> Run each brief through the in-process primary engine and assert its record
> binds the queued WI, unique turn, primary base, exact candidate and scope;
> changing any binding stales the result, and the verdict alone performs no
> approval write. Drive a blank-Brief adjudication and assert its generic
> primary judgment assignment names the bound verdict path and contains no
> claim, branch, model-side close or snapshot instruction. A failed declared
> assembler remains HELD, while ordinary non-adjudication work still receives
> its worker assignment.

### TC-205 `Method`

Preserve every existing identity, raw-path, logged-reviewer, phase, verdict,
trailer, record-only, ordinary refresh/branch and fail-toward-review case. Replace
only adjudication mechanical-close cases with:

> Drive the primary publication writer against the verifier. Exact accepted
> Status/snapshot/queued-close/successor/generated bytes carry the review from
> candidate to final tree; forged subject, wrong WI/turn, stale candidate, extra
> or missing path, cross-WI close, malformed successor, partial snapshot and
> unreviewed decision each fail toward more review. Kill before and after the
> atomic commit and prove pending resume versus one derived completion and no
> duplicate mint.

## SR-140, LLR-173 and TC-167: preserved meaning

No cell change is proposed. The approval commit's author remains the actual
adjudicator; Git's committer remains the coordinator publisher. Automated
publication must set author identity from the bound adjudication session. A
human author is permitted only with bound evidence of that human act. Existing
TC-167 must gain implementation tests for distinct author/committer and false
human attribution, but its normative method need not change because it already
requires the acting reviewer to be queryable from the commit.

Concrete proof cases: a model route's logged session identity becomes Git
author while the coordinator is committer; changing either the author or bound
session/route makes verification refuse; a human author without a committed
human act refuses and a real bound human act passes. Every success still meets
the seven-registry byte-identical mirror and explicit-seed rules.

## Concrete boundary tests

- Create the exact `turn.toml`, then attempt a second turn, duplicate WI/base,
  wrong primary branch/root, changed spec/live/snapshot blob, dirty primary,
  claim, merge and direct integration. Each refuses and leaves it byte-identical.
- Kill after `turn.toml`, after a verdict, and after one of two review phases.
  Restart resumes the same turn before queue selection and draws only missing
  evidence. Kill after final commit; terminal spec + verified publication draws
  nothing.
- Assert the no-bar allowlist is only `## Approval`, in-scope live registry
  cells, named snapshots, the one queued-to-complete move, parsed successors and
  id-watermark, and the existing trunk-step generated set. One generated product
  path or ordinary-WI effect invokes the product bar. Its attestation names turn,
  candidate, projection digest, checked paths and result.
- Parse every decision value. `return`/`uncertain` accept zero cells; `meaning`
  without accepted impact evidence blocks. Duplicate rows, missing identities,
  stale or foreign evidence, and scope beyond `Adjudicates` refuse.
- For each of seven snapshot registries drive accepted drift, UNJUDGED drift,
  out-of-scope drift and a Drafted rider. Any UNJUDGED/out-of-scope Approved cell
  blocks the file; a listed rider remains below approval.
- Drive a requested equivalent approval with another scoped WI's UNJUDGED drift:
  the approval projection refuses and remains pending. Revise its decision to
  RETURN with zero accepted cells and a continuation that depends on the named
  scope owners: it closes atomically with no Status/snapshot write. Prove the
  later complete-scope reanchor re-judges every cell and treats the RETURN
  findings only as evidence, never as accepted judgment.
- Commit verdict/review files without publication and assert snapshots, Status,
  queued spec and watermark remain unchanged.
- At admission, after verdict, after review and before commit, attempt claim,
  merge, direct integration and another primary turn. Each sees the held owner
  and refuses; each may proceed only after atomic close.

## Tracked stable-ID reference census

Produced with `git grep -l` over tracked files and the 16 IDs below, with the
literal path `OWNER_SCRATCHPAD.md` excluded from Git's pathspec. Classification
was path-based: live source/working records, immutable history/evidence, and
generated views.

| ID | Live | History | Generated |
|---|---:|---:|---:|
| SR-140 | 10 | 44 | 2 |
| LLR-140 | 8 | 67 | 2 |
| LLR-152 | 5 | 9 | 2 |
| LLR-153 | 3 | 11 | 2 |
| LLR-154 | 4 | 10 | 2 |
| LLR-158 | 5 | 60 | 2 |
| LLR-167 | 11 | 16 | 4 |
| LLR-173 | 5 | 20 | 2 |
| LLR-207 | 5 | 99 | 2 |
| TC-146 | 2 | 10 | 1 |
| TC-147 | 3 | 32 | 1 |
| TC-148 | 2 | 10 | 1 |
| TC-153 | 3 | 11 | 1 |
| TC-161 | 11 | 15 | 2 |
| TC-167 | 3 | 7 | 1 |
| TC-205 | 3 | 93 | 1 |

Supplemental parent/interface census requested by review, as total tracked path
counts from the same `git grep -l` command:

```text
SR-144=93 SR-146=56 SR-148=74 SR-156=72 SR-174=31 SR-178=33
IF-090=31 IF-091=37 IF-123=22 IF-124=19 IF-127=29 IF-128=21 IF-129=16 IF-175=82
```

Machine-produced live path/ID inventory:

```text
docs/decisions-for-review-2026-08-29-slices-4-6.md|TC-161
docs/handbacks/WI-451-wi451-sr-retier-campaign.md|SR-140
docs/if-tc-coverage-allow|TC-161
docs/repo-lock.md|LLR-167,TC-161
docs/requirements/components.toml|LLR-207
docs/requirements/interfaces.toml|LLR-173,LLR-207,SR-140,TC-161
docs/requirements/low-level-requirements.toml|LLR-140,LLR-152,LLR-153,LLR-154,LLR-158,LLR-167,LLR-173,LLR-207,SR-140,TC-146,TC-147,TC-148,TC-153,TC-161,TC-167,TC-205
docs/requirements/open-items.toml|LLR-152,LLR-158,TC-153
docs/requirements/system-requirements.toml|SR-140
docs/runtime-flows.md|LLR-140,LLR-152,LLR-153,LLR-154
docs/status.md|LLR-167
docs/test/test-cases.toml|LLR-140,LLR-152,LLR-153,LLR-154,LLR-158,LLR-167,LLR-173,LLR-207,SR-140,TC-146,TC-147,TC-148,TC-153,TC-161,TC-167,TC-205
docs/work/active/wi-605-adjudicate-sr-161-llr-183-ow/WI-605-adjudicate-sr-161-llr-183-ow.md|LLR-167
docs/work/handback/wi-605-control-interruption-llr-snapshot.patch|LLR-167,TC-161
docs/work/handback/wi-605-control-retry-interruption.patch|LLR-167
docs/work/queued/WI-596-the-anchoring-copy-s-absorb-le.md|LLR-140,LLR-158,LLR-207,TC-147,TC-205
docs/work/queued/WI-603-adjudicate-llr-167-approved.md|LLR-167
project-trajectory/scripts/acceptance_record.py|LLR-158
project-trajectory/scripts/agent_loop.py|LLR-140
project-trajectory/scripts/gen_verdict_rollup.py|LLR-140
project-trajectory/scripts/integrate.py|LLR-140,LLR-154
project-trajectory/scripts/schedule.py|LLR-152
project-trajectory/scripts/score_reviews.py|LLR-140
project-trajectory/scripts/trace.py|LLR-167,TC-161
project-trajectory/scripts/trace_text.py|SR-140
tests/test_dashboard_size_budget.py|SR-140
tests/test_id_watermark.py|LLR-167,TC-161
tests/test_module_size_ratchet.py|LLR-167,TC-161
tests/test_trace.py|SR-140
tests/test_trace_rules.py|LLR-173,SR-140
tests/test_traj_parse.py|SR-140
tests/test_traj_views.py|LLR-173,TC-167
tests/test_trajectory_arch.py|TC-161
```

### Per-live-reference disposition

- Live governing registries and interfaces: independently judge the exact
  fragments and affected IF contracts before implementation. SR-140/LLR-173
  remain unchanged. Regenerate component derivations afterward.
- `runtime-flows.md`, `repo-lock.md`, `status.md`, decisions and coverage allow:
  update forward-looking carrier statements only after approval; preserve any
  decision or exception whose substance still applies.
- WI-603: expand its LLR-167 before/after evidence to the combined proposal.
  WI-596 remains the only absorb-ledger owner. WI-605 and its two patches remain
  preserved incident evidence, never executable instructions.
- Implementation files: change only the symbols traced by their LLRs; preserve
  ordinary branch paths and delete adjudication compatibility exceptions.
- Tests: retain every case the surgical TC amendments say to preserve and add
  the new primary-turn cases; ratchet/trace tests only update expected references.
- Generated views: regenerate from accepted sources; never hand-edit.
- All 514 history path references counted above remain immutable evidence under their
  original meanings. Approved snapshot copies stay unchanged until the eventual
  independently reviewed approval publication.

Individual live-reference disposition:

- Live SR/LLR/TC/interface/component registries: inspect the supplemental parent
  and IF set above; amend only proposed fragments; preserve SR-140/LLR-173/TC-167.
- `integrate.py`, `agent_loop.py`, `schedule.py`, `acceptance_record.py`: change
  traced carriers only; retain `lane_approval_refusal` and delete its actor-class
  exception. `intake.py` stays IF-090's writer and `kitlib/verdict.py` IF-175's
  shared evidence reader.
- `gen_verdict_rollup.py`/`score_reviews.py`: preserve ordinary LLR-140 behavior;
  consume primary scope only if accepted LLR-207/IF-175 requires it.
- `trace.py`, `trace_text.py`, dashboard/trace/ratchet tests: registry/render
  references only; update expected accepted text or symbols, never authority.
- `runtime-flows.md` changes only its adjudication carrier; `repo-lock.md`,
  interface/CLI references and knowledge files change only affected live seams.
- WI-603 receives the combined LLR-167 delta. WI-596 owns `## Approval`
  absorption. WI-605 and its patches remain incident evidence, not instructions.
- Open-items, allow files, decisions and handbacks preserve rulings; revise only
  forward instructions naming the retired carrier after independent judgment.
- Generated views regenerate after accepted sources. Snapshots and all archived,
  review, log and iteration history remain untouched.

## WI-605 supervisor migration

WI-605 is the one owner-authorized exception needed to enter the corrected
carrier. Under the tracked pause, an explicit supervisor migration moves the
same WI-605 spec from
`docs/work/active/wi-605-adjudicate-sr-161-llr-183-ow/` back to queued and
records that holder transfer in one reviewed repair commit. After that repair
is frozen and the tracked pause is removed in the launch-base commit, the first
supported dispatcher admission creates the immutable primary `turn.toml` for
WI-605. It is not preminted in the repair commit: `turn.base` must be the clean
post-repair, post-pause-removal primary launch base that the dispatcher actually
selects. The migration report records the old branch name and clean HEAD
`668edaf49896608e48bc6ff3cec014840312476a`, every committed review/iteration
record, both preserved interruption patches and their hashes, the primary
baseline, and which proposed snapshot/ledger effects are rejected versus which
successor drafts remain evidence.

The original ref is preserved under its existing name and never renamed,
deleted, reset, merged or treated as executable approval. Removing the active
claim is an explicit transfer of the same open WI's exclusive holder to the
pending primary turn. It creates no terminal complete/partial result, no second
WI-605 copy, no parked hidden ref and no ordinary compatibility route. The
migration verifier requires exactly one WI-605 spec after the move, in queued,
and the pending record points to that initial proposal and the preserved report.
The stopped-lane close doctrine remains unchanged for every ordinary stop; this
one transition is justified by the owner handoff's explicit instruction to
migrate the active adjudication lane to primary while preserving its branch and
evidence. I found no handoff instruction requiring a different valid transition.

After migration, WI-605 follows the same primary-turn contract. Its prior
rounds are historical evidence, not accepted cells; its current judgment starts
from the authoritative primary snapshots and independently records any usable
finding or successor in `## Approval`/`## Dispositions` before publication.

## Judgment questions

Independent review must decide whether each fragment preserves every omitted
live clause, whether the LLR-207 projection is narrow and independently
re-derived enough to bind the final tree without hiding semantic work, whether
Git author/committer faithfully preserves SR-140, and whether combining the
pending LLR-167 amendment is a stable-ID impact resolution. A MEANING verdict is
not approval, and this proposal itself authorizes no implementation.
