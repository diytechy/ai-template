# The verdict record, and what stopped the queue moving on its own

**Status:** plan only — a question put to the owner plus the findings behind it.
Nothing in the kit is changed by this document.
**Written:** 2026-08-31, by the supervising session of the delegated unattended run,
at the owner's request ("is `docs/reviews/WI-<n>-REVIEW-A.md` the right way to
document a verdict? Is there a better alternative?" — and: document the other
items that stopped the queue from moving forward automatically).
**Read at:** branch `contract_split`, trunk `53240d51`, over the seven loop runs of
2026-08-31. Every claim below was observed live that night or read out of the
code; the record is [the sitting](../log.md) (findings A–O) and
[decisions-for-review-2026-08-31.md](../decisions-for-review-2026-08-31.md) 40–46.

**The breakdown is the owner's** — this plan names shapes and trade-offs, not
work items. Ids are minted by the frontier, never here.

---

## 0. The incident, in one paragraph

Seven `agent-resume` launches merged four rows and closed a fifth partial. Not
one launch got past a single lane: every run ended at exit 1 or 4 and needed a
supervisor to draw a review round, compile a verdict file, merge through the
slot by hand, and relaunch. The queue advanced **one row per human intervention**
for nine hours. One cause recurs under most of the stops, and it is the subject
of §1; the rest are in §2.

## 1. The question: is `docs/reviews/WI-<n>-REVIEW-A.md` the right carrier?

**No — and the strongest argument against it is the kit's own doctrine.**

### 1.1 What the gate actually needs

`integrate._verdict_gate` (`integrate.py:1262-1302`) establishes one predicate
per merged work item, and nothing more:

> under `review_rounds >= 1`, this WI received an independent fresh-context
> review whose governing verdict is `APPROVE`, and that verdict is **not older
> than the branch's last non-record commit**.

Everything else in the file — the prose, the round-by-round history, the
"governing verdict" section this session's compiles wrote — is for a human
reader, not for the gate.

### 1.2 What exists today

| artifact | who writes it | what binds it to the tree it judged | who reads it |
|---|---|---|---|
| `docs/reviews/<train>/NNN-REVIEW-A-<sha7>.md` | the reviewer session the loop routed and logged | the **reviewed sha in its own filename**, and `fresh_verdict_path` (`agent_loop.py:938-954`) unlinks any file planted at that path before the session runs | `score_reviews` (advisory scoreboard) — **and nobody else** |
| `docs/reviews/<train>/scoreboard.txt` | `score_reviews.py` | nothing; explicitly advisory | the escalation policy |
| **`docs/reviews/WI-<n>-REVIEW-A.md`** | **nothing in the kit** | **nothing** | **the merge gate, exclusively** |

Three defects follow, and they are independent of each other.

**(a) Nobody writes it, so every lane stops.** Two references to that path exist
in the whole kit and both are reads inside the gate. Every WI-level verdict in
this repo's history was hand-compiled by a coordinator sitting. A mechanized
lane can therefore build, review, rework and close itself perfectly and still
not merge: `required verdict ... is absent`, exit 1, run over. That is the
stopper, and it fired on four of the seven runs.

**(b) It is a hand-maintained paraphrase of evidence that already exists.** The
kit refuses this shape everywhere else: twelve artifacts are declared in
`docs/stack.ini [generated]` with a regenerator and a `--check` (the dashboard,
the CLI and interface references, the approval brief, the derived stage…), and
`PROCESS.md` states the rule as *generated, not hand-maintained*. The verdict
rollup restates the round files and is in neither category — not generated, not
checked, not even declared.

**(c) The trust is inverted, and this is the serious one.** The round file is
the artifact with an anti-forgery story: its name binds it to the sha it judged,
its writer is the session the loop selected and logged, and a `telemetry:
session <train>-NNN REVIEW-A COMMITTED` commit records that the round happened.
The rollup has none of that — it is prose at a fixed path — and it is the **only**
thing the gate consults. A file containing one line, `VERDICT: APPROVE
findings=0`, authored by anyone with commit access and no round behind it,
clears the rung. This session wrote four of them; nothing verified a single one
against the rounds it claimed to summarize. The related live observation is
finding K: a **BUILD** session on `WI-538` wrote
`010-REVIEW-A-e26ab03.md` ("re-review approval") — an implementer writing an
approval into the review path. Today that file is harmless because the gate
ignores round files; under a naive auto-compile it would become a counted round.

### 1.3 The alternatives

**A. Keep the file; have the loop compile it.** Smallest diff: at the moment the
loop already prints `review round: merged=APPROVE margin=… tripwires=…
heterogeneity=…`, it holds every input — the round paths, the reviewed sha, the
tripwires — so it can write the rollup there. Fixes (a). Does **not** fix (b) or
(c): the artifact stays hand-editable and the gate keeps trusting the summary
rather than the evidence.

**B. Delete the rollup; the gate reads the round files.** The evidence is
already structured: one file per round, a parsed `VERDICT:` line
(`score_reviews.parse_verdict`, which already accepts arbitrary text), a sha in
the name, commit times for ordering. The gate's predicate becomes a computation
over the round set — governing = latest by commit time; freshness = the same
`code_time` comparison it already does; provenance = the round file must be the
one a logged reviewer session produced (which closes K). Fixes (a), (b) and (c).
Costs: the "governing verdict" convention (time-ordered, last one wins) becomes
code instead of a human's care; a human loses the single-file summary unless one
is generated.

**C. Carry the machine half as a commit trailer, keyed to the tree.** The kit
already has this exact pattern and the merge slot already verifies one:
`Bar-Green: tree=<40 hex> work=<40 hex> <summary>` (`integrate.py:196`,
`:1125`), which is how a refresh proves *this bar ran on this tree*. A
`Review-Verdict: APPROVE rounds=N tree=<sha> heterogeneity=<…>` trailer on the
round's own commit would make the verdict tree-bound by construction, dissolve
the freshness comparison entirely (a verdict names the tree it judged; a later
commit simply has no verdict), and leave the findings prose where it belongs —
in the round file, as evidence. Costs: a trailer cannot hold prose, so it is
only ever the machine half; and adopters' wrappers that grep the review path
would need the RESYNC note.

**D. git notes / refs.** Rejected without much thought: invisible in a file
tree, easily lost across merges and clones, and this repo is deliberately
file-based so that a human can audit it with `cat`.

### 1.4 Recommendation

**B, with C as the attestation and a generated rollup for the human — in that
order of importance.** Concretely:

1. The gate stops requiring a hand-authored file and computes its predicate over
   the round files of the branch's train, restricted to rounds a **logged
   reviewer session** produced (the telemetry commit is the anchor; an
   implementer-written file in the review path is not a round).
2. The round's verdict is stamped as a `Review-Verdict:` trailer naming the
   reviewed tree, exactly as `Bar-Green:` names the barred tree. Freshness stops
   being a timestamp comparison and becomes an identity: the verdict either
   names this tree or it does not.
3. If a human-readable per-WI rollup is still wanted — and it is genuinely
   useful; this session read them — it becomes a **generated** artifact with a
   regenerator and a `--check`, declared in `docs/stack.ini [generated]` like
   every other derived file. Never hand-authored, never trusted by the gate.

What stays the human's: nothing changes about who *approves*. The rung still
demands an independent fresh-context verdict; this only changes which artifact
carries it and who may author that artifact.

**The one thing worth arguing about before building:** whether "governing =
latest round by commit time" is the right rule in code. It is what the
convention already does by hand, but it means a later CHANGES-REQUESTED always
beats an earlier APPROVE (correct) *and* that a re-run round after a
non-substantive edit can silently promote a stale APPROVE (today a human notices;
a rule must decide). Options: last-by-time (today's convention), or
last-by-tree-identity under C (a verdict that does not name the current tree does
not count at all, which is stricter and needs no ordering rule).

## 2. The other things that stopped the queue

Ordered by how much they cost on the night. Each is stated as *what happened →
where → the shape of a fix*, not as a work item.

### 2.1 An adjudication lane gets no review round in-process (finding A)

`WI-547`, `WI-549` and `WI-550` each exited `DONE` reporting "review round
approved" with **no round drawn**. A BUILD session schedules its round
(`dispatch: review-policy 1 -> scheduling review round`); an ADJUDICATE session
does not. The round happens only because the C2 resume derivation later notices
the lane owes one — i.e. by accident of a restart.
**Shape:** whatever schedules the round after a committing BUILD should schedule
it after a committing ADJUDICATE; the banner must not claim a round that was
never drawn.

### 2.2 C2 re-owes a round on the loop's own telemetry commits (finding B)

On `WI-547` the review-owed derivation fired twice and drew two identical
`APPROVE findings=0` rounds, because the loop's own `telemetry:` and
`scoreboard` commits had moved HEAD past the verdict. The merge slot already
solves this — it excludes `docs/reviews` and `docs/log.d` when computing
`code_time` (`integrate.py:1280-1286`) — and the resume derivation does not.
**Shape:** one definition of "the last commit that could invalidate a verdict",
used by both. `docs/iteration/` belongs in the exclusion set too.

### 2.3 Three briefs carry no close step (finding C)

`WI-548` gave the C6 close ritual to `worker.template.md` and
`adjudicate-disposition.template.md` only. `adjudicate-amendment`,
`adjudicate-conflict` and `adjudicate-red-tc` did not get it, so those lanes
**cannot finish themselves** — `WI-547` was closed by the supervisor for exactly
this reason, and it is the same "resumed forever, each resume a fresh judge
finding nothing to judge" defect D6 that C6 was written to close.
**Shape:** the close ritual is one paragraph; either every adjudicator brief
carries it, or the dispatcher closes an adjudication lane whose verdict commit
carries the `WI:` trailer (the path `WI-548` decision 35(b) deliberately did not
take, revisitable now that the brief path has been tried).

### 2.4 The full suite does not fit in a worker's turn (findings J, M) — this one closed a finished row as partial

`WI-540`'s sessions 005, 006 and 007 each verified the rework, started the full
unfiltered suite, and were told by the harness that a foreground wait was
blocked; each backgrounded the run, ended its turn to await a notification, and
was killed with the turn. Three NO-COMMIT sessions is the C1 build stall by its
own rule, so the dispatcher closed a row whose work was **built, trailered, and
believed complete by three independent sessions** into `partial/` — then the
§A3 quarantine reverted 3876 lines to a patch file. The suite is ~11 minutes
(3192 passed / 15 skipped / 643.9 s on trunk); the tool's foreground cap is 10.
`WI-538` lost two sessions the same way.
**Shape:** the close ritual must name a bar a worker can actually complete —
the commit bar (smoke + budget + docs) at close, with the full suite run by the
lane's *refresh* (which already runs the full declared bar inside the slot,
outside any session's turn), or a declared batched form. A close instruction
that cannot be executed in one turn is a stall generator.

### 2.5 `approval-fresh` reds a lane that changed no registry (findings L, O)

Two distinct causes, one symptom:
- **L:** `WI-538`'s rework amended `LLR-206`, an `Approved` row. The worker
  brief names the approval-brief regeneration only for a lane that *minted or
  re-statused* spine rows, so nobody regenerated it and the drain went red. An
  **amendment** of an approved cell stales the brief exactly as a mint does.
- **O:** `docs/ratify/CURRENT.md` carries an "Approval provenance: the last
  commit to move a `Status` cell is `<sha>`" line derived from history. The copy
  the `WI-540` lane regenerated was current *there* and stale on **trunk** the
  moment it merged, so the next lane's refresh (`WI-550`, which touched no
  registry at all) went red for a staleness it did not cause.
**Shape:** for L, one sentence in the brief. For O, either the provenance line
stops being history-derived, or the trunk step regenerates the brief after a
merge that touched it — the same way the trunk lane already owns every other
generated artifact.

### 2.6 The bar-inert revert lowers a monotone counter (finding N) — kit defect

`dispatch._refresh_or_quarantine`'s §A3 path reverted `WI-540`'s product diff to
a patch file, and took `docs/id-watermark` back with it: `IF 174 -> 173`. A
watermark only ever rises — a spent id must stay spent — so the reverted tree
**could never pass `registry-integrity`**, and the run stopped again on the very
artefact the ruling created to be inert.
**Shape:** the revert must exclude the watermark (and anything else monotone by
contract). A minted id is burned whether or not its row survives.

**A second consequence, found while counting the rounds for §4:** the same
revert deleted the lane's *review evidence* — `002-REVIEW-A-bb31d58.md` and the
scoreboard went with the product diff, so `WI-540` is the one merged row on
trunk with **zero** round files, and the disposition adjudicator had to judge a
close whose review it could not read. `docs/reviews/` is a record path
everywhere else in the machinery (the merge slot excludes it from the freshness
comparison precisely because it is not code). The revert should treat it, and
`docs/log.d/`, the way it already treats the handback report: evidence of what
happened survives the reverting of what was done.

### 2.7 Residue and drain mechanics (findings E, F)

- `out/agent-loop.lock` was missing from the declared unload residue, so **every**
  merged lane ended `UNLOAD INCOMPLETE`; fixed on trunk this session (decision
  40, with a test and the fixture gap closed). `out/integrate.lock` is the same
  class and is still undeclared. Worker *scratch* files under `out/` were
  correctly refused by name — but no brief tells a worker where scratch belongs,
  so it will recur.
- The dispatcher drains only before an **exclusive** claim or at station exit,
  so a lane finished between runs waits while an ordinary claim advances trunk
  over it — and its earlier station-refresh commit then conflicts. This is
  documented behaviour, not a defect, but it is a trap for any supervisor who
  finishes a lane by hand (it cost one lane rebuild tonight).

### 2.8 DESIGN-CHECK runs the worker brief and does the rework itself (finding G)

Seen on `WI-535` and `WI-540`: the design-check session commits the rework, so
the follow-on BUILD sessions have nothing to do, burn the stall budget, and the
rework reaches the drain unreviewed. Raised on 2026-08-30 and still open; §2.4
makes it worse, because those empty BUILD sessions are exactly the ones that
then stall.

### 2.9 Adjacent, named, not queue-blocking

A later lane amended a **terminal** spec (`docs/work/partial/WI-521…`, +12 lines)
and nothing refused it, though a closed partial is meant to be a byte-identical
record keyed by its handback report (finding I).

## 3. Sequencing (shapes, not rows)

1. **The verdict record** (§1) — the design decision is the owner's; the build
   after it is one change to the gate plus a generated rollup. Everything else
   in this list is smaller than it and none of it unblocks the queue alone.
2. **The close-ritual set** (§2.3 + §2.4) — the briefs, together: every
   adjudicator brief closes, and the close bar is one a worker can finish.
3. **The freshness definitions** (§2.2 + §2.5) — one home for "what invalidates
   a verdict", and the approval brief's staleness rules.
4. **The revert's monotone exclusion** (§2.6) — small, isolated, provable.
5. **Residue + scratch** (§2.7) — `out/integrate.lock`, and a line in the worker
   brief naming where scratch goes.

§2.1 rides with 1 or 2, whichever touches the scheduling arm.

## 4. The acceptance, stated as a measurement

Not "the findings are addressed" but: **one `agent-resume` launch merges at
least three consecutive queued rows with zero supervisor commits and zero hand
merges**, on a box where the full suite takes ~11 minutes. Tonight's number was
zero — every merge on the night was mine. A run that reaches three has actually
been fixed; a run that reaches one has not.

Secondary readings worth keeping, with the night's numbers as the baseline
(`WI-547 / WI-549 / WI-535 / WI-538 / WI-550`, counted off the merged tree):
reviewer rounds spent per merged row — **4 / 1 / 2 / 6 / 2** (`WI-538` carries a
seventh round-shaped file its own implementer wrote, §1.2(c)); supervisor commits
per merged row — **3 / 1 / 1 / 4 / 2**, plus eight trunk-lane commits belonging
to no row. The target for both is zero supervisor commits; the round counts are
a policy question (§5), not a defect.

## 5. Out of scope, named

- Whether `complete_review = "sample"` should keep drawing spot-check
  adjudications while the queue is this slow (a dial, the owner's).
- The goalpost-moving class — a new small MINOR on each round of the same lane
  (`WI-538` took six rounds this way). Policy, recorded in decisions 12–20 of
  the previous run, not a defect to fix here.
- The reasoning-effort dial and the routing preferences (decision 36).

## 6. Adopter compatibility

The gate's contract is adopter-visible: a downstream repo may hold
hand-authored `docs/reviews/WI-<n>-REVIEW-A.md` files today, and its wrappers
may grep them. Any change under §1 needs a `RESYNC_PACK.md` entry and a
migration window in which the gate accepts **either** the round-file evidence or
a legacy rollup, warning on the legacy path — the same shape the config
migration used. The trailer under alternative C is additive and costs an adopter
nothing until their loop writes one. §2.3–§2.7 are prompt text, one declared
name, and two small code rules; all ship on the next resync with no adopter
action.
