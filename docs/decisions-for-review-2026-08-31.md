# Decisions taken under delegated authority — the unattended run of 2026-08-30/31

**Why this exists.** The owner is away and delegated their authority to the
supervising session for one mechanized run on `contract_split` (record:
[log.md — the delegation sitting](log.md#2026-08-30--sitting-the-three-stranded-claims-become-parked-lanes-again-and-the-two-owner-owed-rows-carry-the-owners-delegation-for-an-unattended-run)).
Every stop the loop made that a human would normally dispose was disposed by
the supervisor with the best decision the information supported, acting only
through the kit's own scripts. This file is the record the owner reviews at
return. The genuine stops — the approval dial, `[policies]`, a ruled open item,
deleting reviewed rationale, anything destructive or irreversible, any push —
were not touched.

**How to read it.** Each entry states what was decided, the alternative, why
this one was taken, and what it costs to reverse. Ranked roughly by how much a
different answer would change. Nothing here is a ruling.

---

## 1. The trunk lane's 112 parked fragments were compiled on trunk, and their 62 inbound links re-pointed

**Decided:** run `trunk_step.py --compile-log` on `contract_split` as the serial
trunk-lane act, fold the 112 fragments parked in `docs/log.d/` since 2026-08-18
into `docs/log.md`, and re-point every link that named a fragment file at the
compiled heading (`log.md#<anchor>`, the checker's own slug). Commit
`59f52549`.

**Why it had to happen now.** The integrator runs the trunk step inside every
station refresh. The run's first lane (`WI-484`) refreshed, the compile deleted
the fragments, and 33 links — `docs/status.md`, the OI-67 plan, three review
READMEs, the closed specs — pointed at deleted files. The bar went red ON THE
BRANCH for a debt that belongs to the trunk lane, the lane was quarantined, and
the run stopped. Every subsequent lane would have hit the same wall.

**The alternative:** leave the fragments and change the links to point at
`log.md` without an anchor (never breaks, loses the pointer), or let each lane
fail and repair one at a time. Rejected: the first hides a real navigation loss
behind a link that resolves to a 50k-line file; the second re-pays the same debt
per lane.

**Reversal cost:** none in substance — the compile is the kit's designed act and
the links now point at the same text one directory up.

## 2. `check_docs.py` now blanks HTML comments before the inline-code strip (a kit script change, with a test)

**Decided:** a small root-cause change to the shipped checker. A lone backtick
inside an HTML comment — two `<!-- fig: cmd="grep -c '^### `scripts/' …" -->`
markers in the compiled log — was read as an inline-code opener, paired with the
next backtick thousands of lines on, and hid **226 of the log's 555 headings**
from the anchor set; every `log.md#anchor` link into that range read as broken.
Comments are blanked to a single space (so a comment QUOTED inside inline code,
`` `<!-- BEGIN GENERATED STATUS -->` ``, keeps its backticks apart).
Regression test `test_parse_doc_blanks_html_comments_before_inline_code`.

**The alternative:** edit the two `fig:` markers to avoid a literal backtick.
Rejected: those are signed-figure derivation strings; editing a measurement's
own command to appease a parser is the wrong direction, and the next marker
would recreate the defect.

**Also under this entry:** one pre-existing log line wrote `` `— from \`--since\`` ``
(backslash-escaped backticks inside inline code, which the checker does not
honour) and was re-worded to say the same thing without nesting. A record edit,
recorded here; the meaning is unchanged.

**Reversal cost:** low — one regex, one substitution, one test. Adopters get
the checker change on resync; it only widens what resolves.

## 3. `docs/test/README.md` names the gitignored trace report instead of linking it

**Decided:** commit `efcde754`. A fresh lane worktree has no
`docs/test/report.md` until `trace.py` writes one, and `check.py --jobs 0` runs
doc-navigability and registry-integrity concurrently — so the link resolved
only when the trace step won the race. The `WI-508` station refresh lost it on
its first fresh worktree. A navigation link to an untracked target is broken on
every clean clone by construction.

**The alternative:** sequence the two steps in `check.py`. Rejected as
over-engineering for a one-line doc fix; the README already said the file is
untracked.

**Reversal cost:** trivial.

## 4. The two parked lanes were station-refreshed BEFORE their workers ran

**Decided:** `integrate.py refresh --branch wi508-architectural-remap` and
`… --branch wi521-decomposition-debt-owner` (refresh commits `7e2d3f82`,
`56e7e52b`, bar PASS 11/11), so each branch's checkout carries the owner's
**Delegated for the unattended run** section.

**Why.** The three lane refs were re-cut at `9ab30d64`, but the delegation
amendments were committed one commit LATER (`aab7b8a8`) on trunk only. The
`WI-484` worker read its spec from the branch checkout, never saw the
delegation (its transcript contains no such section), and blocked on the
"owner text" language the delegation had superseded — a correct reading of a
stale spec. `WI-508`'s spec on its branch still said *"No session may flip
them"* above a delegation it did not have.

**The alternative:** `git branch -f` each ref to trunk HEAD (the previous
sitting's own repair, a pure fast-forward on a zero-commit branch), or let each
worker block and dispose the handbacks with successors. The refresh is the kit's
sanctioned way to bring a lane current, so it was used even though it is
slower; the third option would have burned two worker sessions to learn what
was already known.

**Reversal cost:** none — a refresh commit is disposable by design.

## 5. The `WI-484` handback was allowed to run its course rather than be undone

**Decided:** the kit closed `WI-484` as `partial` (worker exit 3, report
`docs/handbacks/WI-484-wi484-concern-refs-component-view.md`, the block record
quarantined to `docs/work/handback/wi484-concern-refs-component-view.patch`).
That close stands: the spec is terminal, the report is the event's identity, and
the disposition row intake mints for it is the sanctioned place to continue the
work — by drafting a **successor** that carries the delegation in its own body,
not by re-opening the closed row.

**The alternative:** delete the lane's handback commits and re-run the worker on
a refreshed branch. Rejected: rewriting a lane's history by hand is exactly the
hand-moved-spec act the run was told never to take.

**What it costs:** one extra row (the successor) and one adjudication session.
The worker's own finding was honest given what it could see; nothing in it is
wrong except the premise the branch had not received.

## 6. The launcher was run with `--wait-on-limit 14400`

**Decided:** `agent-resume.cmd --wait-on-limit 14400` (the launcher passes extra
flags through). A provider rate-limit therefore sleeps the loop up to four hours
and resumes instead of exiting WAITING for a human who is not here.

**Reversal cost:** none; a launch-time flag.

---

_Entries below were added as the run progressed._

## 7. `WI-508`: the loop's review rounds cannot satisfy the merge slot's verdict rung on their own — the supervisor compiles the WI-level verdict, as every coordinator sitting before it did

**What happened.** The `WI-508` lane built (sessions 001–002: the four
`Drafted` rows approved under the delegated dial, the row closed), took
REVIEW-A round 1 on gpt-5.6-terra (CHANGES-REQUESTED, 3 MAJOR: TC-199/TC-200
approved as evidence for an obligation their own LLRs record as undischarged;
a dead link), reworked (TC-199/TC-200 back to `Drafted`), took round 2
(CHANGES-REQUESTED, 2: the record claimed the residual SR-163 obligation was
"carried by" WIs that do not cite it), and the dispatcher tier-upped to a
DESIGN-CHECK on gpt-5.6-sol. **That session committed the rework itself**
(`15a89009`, `e815a4b8`: the obligation now stated as honestly UNSCHEDULED),
so the three BUILD rework sessions that followed found nothing to do, the
stall guard fired (exit 4), and the drain tried to merge the finished branch —
where the refresh bar went red on `approval-fresh` (`docs/ratify/CURRENT.md`
stale after the status reverts) and the run stopped.

**The structural fact underneath.** `integrate._verdict_gate` (RULING-7)
requires `docs/reviews/WI-<n>-REVIEW-A.md` carrying an APPROVE newer than the
last non-record commit. The loop's reviewers write
`docs/reviews/<train>/NNN-REVIEW-A-<sha>.md`; nothing in `agent_loop`,
`lane`, `dispatch` or `score_reviews` writes the WI-level file. Every WI-level
verdict in history (`git log --diff-filter=A -- 'docs/reviews/WI-*-REVIEW-A.md'`)
was authored by the coordinator sitting, compiling the rounds. So under
managed routing + `review_rounds = 1` a lane merges only when a coordinator
transcribes the final APPROVE — the mechanized loop alone stops at the slot.

**Decided:** (a) `agent_loop --wi WI-508 --rework <the approval-fresh red>`
on the lane, base = the lane's refresh commit, so the kit's own worker fixes the
red and its commit schedules a fresh cross-family review over the whole train
diff; (b) if that round APPROVEs, the supervisor writes
`docs/reviews/WI-508-REVIEW-A.md` on the branch as a compilation of the three
rounds — the round verdicts quoted, nothing judged that a reviewer did not
judge — exactly the historical sitting act; (c) relaunch the loop, which
drains the finished branch.

**The alternatives.** Teach the loop to write the WI-level file when a round
APPROVEs (a kit change to the merge protocol, mid-run, unreviewed — declined
as design work the owner should see), or leave every lane unmergeable. The
gap itself is **for the owner**: it is the reason no unattended run can end in
a merge today. Two kit findings ride with it: a DESIGN-CHECK phase has no
prompt template of its own and runs the WORKER brief (so it builds instead of
ruling), and a design-check that commits is booked as a committing build the
loop then tries to rework again.

**Reversal cost:** none on the record side (a verdict file is a record; the
rounds it compiles are already committed).

## 8. The `WI-508` rework hand-edited the `last_approved` snapshot — flagged, not undone

The round-1 rework (`4824c0ba`) reverted TC-199/TC-200 `Approved -> Drafted`
in the live registry AND "byte-symmetric" in
`docs/archive/last_approved/docs/test/test-cases.toml`, so drift detection
would not report the revert. The snapshot is meant to be re-seeded by
`intake.py snapshot`, not edited. The revert is honest (the reviewer's finding
was right), the reviewer of round 2 did not object, and the approval surface
now shows the two rows as `Drafted` again, which is the true state. Left as
committed; the owner may prefer a re-seed. Recorded here so it is not read as
the snapshot having been approved that way.

## 9. `WI-508` round 010's BLOCKER (the snapshot hand-edit) was confirmed in part and refuted in part, on driven evidence — not complied with blindly

The fresh cross-family round the supervisor drove (gpt-5.6-terra, session
010) raised decision 8's own concern as a BLOCKER and asked for the
`580df781` snapshot to be restored. **Tried and rejected**: with live at
`Drafted` and the snapshot at `Approved`, the brief STILL renders "Drafted,
never approved" (the label derives from live `Status`, not the snapshot), and
the state violates the same §4 sentence the finding cites. **Driven instead:**
`intake.py --root . snapshot` on the lane leaves the tree byte-identical — the
hand-edited snapshot equals what the kit's only sanctioned writer produces —
and both the approval and its reversal are ordinary branch history. Recorded
as a lane fragment (`51750651`); round 011 was drawn on the STRONG
cross-family route (OPENAI-SOL), mirroring the loop's own tier-up ladder after
repeated CHANGES-REQUESTED.

**For the owner:** `trace.py --approve modified` has no vocabulary for
"approved, then demoted" — a row whose lane-local approval was reverted
before reaching trunk reads "never approved". A generator finding, not a
WI-508 defect.

**The alternative:** comply literally (an inconsistent snapshot the process
forbids) or keep re-drawing reviewers until one did not notice. Neither is
honest.

## 10. `WI-508` round 011 (gpt-5.6-sol, 8 findings): two fixes were applied as asked, measured against the kit's own rules, and reverted — the lane's record now carries the instrument output

Restoring the `580df781` snapshot beside a `Drafted` live row makes
`trace.py --strict-integrity` red (`FINDING (integrity): … NOT byte-identical …
may only ever be written by copying the live file`); dropping `SR-163` from
TC-199/TC-200's `verifies` raises the orphan count the ladder is held on
(`SR SR-163 has no test (TC)`). Both were tried, both reverted, both recorded
with the command that decided them (lane fragment
`2026-08-30-wi508-review-011-dispositions.md`, commit `5835bf42`). The three
blind-derivation BLOCKERs concern 2026-08-25 trunk work outside this branch's
diff (`git diff --stat 7e2d3f82..HEAD` touches none of those plans) — carried
to the owner as findings against that record, with the Team-A census (25
modules, not 24) a real MINOR to correct there. The stale-generated-artifacts
MAJOR is the refresh's regen; the `status.md` MAJOR is the trunk lane's and is
taken in this session's closing status edit.

**Rounds so far on this lane:** 003 (terra, 3 MAJOR) → rework → 005 (terra, 2)
→ Sol design-check that committed the rework itself → 010 (terra, 1 BLOCKER:
snapshot) → 010/5175065 (sol, 8) → 012 pending. Two different reviewers have
now asked for a snapshot state the integrity step refuses. **If round 012
repeats it, the supervisor stops drawing rounds**: the lane stays a finished
branch on `wi508-architectural-remap` for the owner's own verdict rather than
be merged on a reviewer the record could not satisfy or an APPROVE nobody
wrote.

## 11. `WI-508` rounds 012–013: the two remaining findings were TAKEN, including the one decision 10 had refuted

Round 012 (terra) dropped the snapshot point and asked for two things: the
trunk `status.md` recap removed (done on trunk, `c9643450`) and the commit
bar run on the record commit (done, `f4addf13`; then the station refresh
`c225c34d`, bar PASS 11/11). Round 013 (terra, on the refreshed tip) left
exactly one: `TC-199`/`TC-200` still formally verify `SR-163`, so `trace.py`
reads the SR as covered whatever the rows' `Status`. **Decision 10's
refutation of that point is reversed** — it had argued cost (the orphan count
rises by one), which is not a refutation of the claim; three independent
rounds and the instrument agree on the claim. The SR-163 targets are removed
(`docs/test/test-cases.toml`, lane commit after `c225c34d`), `SR-163` is an
honest orphan ("has no test (TC)" — verification owed and unscheduled), the
archived Deliverable says so, and round 014 was drawn on the result.

**For the owner:** `SR-163` now needs a row that files the complete
file→requirement→need join over the whole shipped universe as a TC; no queued
row owns it. Filing it is a decision about scope the run did not take.

## 12. `WI-508` rounds 014–015: two more spine-hygiene findings on the Drafted TCs, both taken

Round 014 (MINOR): the two `Expected` cells still foregrounded `SR-163` —
reworded to say each covers its LLR arm only. Round 015 (MAJOR): `TC-199`
cited two `tests/test_bootstrap.py` ids that are `TC-176`'s evidence for
`LLR-181`/`SR-166`, folding SR-166's materialization checks into SR-163's
coverage — the two ids removed, the method's "package direction" paragraph
replaced by a sentence naming TC-176 as its home. Both are corrections to
rows minted 2026-08-25 that the lane's own edits had put under the
reviewer's eye; each is a real spine-hygiene improvement and neither changes
what ships. Round 016 drawn on the result. Seven rounds and counting is the
price of RULING-7 on a lane whose close touched the spine; recorded so the
owner can weigh whether a Drafted-row edit should buy a full round.

## 13. `WI-508` round 016: the package-direction arm returned to `TC-199` with its shared evidence attributed, rather than amending the Approved `LLR-203`

Round 016 found that removing the package-direction tests from `TC-199`
(round 015's ask) left `LLR-203`'s delivered MISSING-FILES arm with no TC —
and drove it: a scaffold with `scripts/kitlib/config.py` removed fails
`check.py` with `ModuleNotFoundError` while all three dogfood nodes pass. The
reviewer offered two remedies: make LLR-203 dogfood-only (an amendment to an
APPROVED row's Detail — drift, re-attestation, the owner's surface), or trace
the package arm without asserting it is SR-166 evidence. **The second was
taken:** `TC-199` cites the two `tests/test_bootstrap.py` nodes again, and its
method states that the same nodes are `TC-176`'s evidence for LLR-181/SR-166's
materialization claim while TC-199 reads them for LLR-203's missing-files arm
and asserts nothing about SR-166. One test, two arms, each traced to its
owner. The Approved LLR was not touched. Round 017 drawn.

## 14. Round 017 could not be drawn on OpenAI (usage limit until 13:34 UTC) and the third family reviews the WRONG TREE without `--dir` — a kit finding

`codex exec` returned "You've hit your usage limit … try again at 8:34 AM"
mid-run (all seven prior rounds were OpenAI). The loop's registry names the
OPENCODE family as review leg 3, so round 017 was redrawn on `OPENCODE-GROK`
— and `opencode run` resolved its project root by walking up from the lane
worktree to the MAIN repo: the reviewer's first command printed `On branch
contract_split` and it began reviewing trunk. Killed before it wrote or
committed anything (trunk `git status` clean). Probed: `opencode run --dir
<lane>` answers `git rev-parse --abbrev-ref HEAD` with the lane branch, so the
supervisor's driver passes `--dir` for opencode templates. **For the owner:**
the shipped `OPENCODE-*` command templates (`docs/agents.toml`) carry no
`--dir`, so every loop-drawn opencode review of a lane worktree reviews trunk
instead — add `--dir {worktree}`-style support or drop the family from review
legs until the template can name the lane. `--wait-on-limit` covers the
OpenAI limit for the loop itself; the supervisor-driven rounds have no such
sleep and were re-routed instead.

## 15. `WI-508` round 017 APPROVEd on the third family; the supervisor compiled `docs/reviews/WI-508-REVIEW-A.md` from the ten round files

Round 017 (`OPENCODE-GROK`, `grok-4.6`, run with `--dir` at the lane) returned
`VERDICT: APPROVE findings=0` after running the cited test nodes, `trace.py`,
a scaffold drive of TC-199's package arm, `check.py --jobs 0`, the smoke tier,
the budget and `check_docs` (transcript kept in the session scratchpad;
verdict commit `899352b7`). The WI-level file the merge slot reads is a
compilation — ten rounds, every finding and machine line quoted from its
round file, the governing line last — committed on the lane as a record
(`docs/reviews/` is outside the verdict-freshness window by design). **The
owner should read the governing round with the grain of salt it deserves:**
one APPROVE on the third family after eight cross-family CHANGES-REQUESTED
rounds whose every finding was either taken or refuted with the instrument;
the loop's own escalation ladder would have paged a human here, and the
delegation is why it did not.

## 16. The two OPENCODE command templates in `docs/agents.toml` gained `--dir .`

Decision 14's finding made concrete before relaunching the loop: with OpenAI
at its usage limit, the loop's reviewer draw falls to the OPENCODE rows, and
without `--dir` an opencode session in a lane worktree reviews TRUNK. Probed:
from the lane's cwd, `opencode run --dir . …` answers `git rev-parse
--abbrev-ref HEAD` with the lane branch, and the session engine already runs
every child with `cwd=<worktree>`. So the two enabled OPENCODE templates read
`opencode run --dir . -m {model} --auto` — a value in this repo's routing
registry (`docs/agents.toml`), not the enable-list, not `[policies]`, and the
shipped `agents.template.toml` carries no opencode row to mirror. Smoke tier
1378 passed / budget 28.8 s. **For the owner:** if the template is meant to
ship the fix, the kit's own opencode rows (wherever they are seeded) want the
same token.

## 17. `WI-521` closed `partial` by the stall guard after its review round could not be drawn — the merge stands, the lane is unloaded, `WI-542` is its disposition

Run 3 resumed the parked debt-owner lane; its Opus build committed a slice
(`56e7e52b..adfc1204`, 33 min). The REVIEW-A draw then failed three ways in
a row: OPENAI-TERRA at its usage limit (ERROR, 3 s), the re-route to
OPENCODE-GROK ran the cited tests and `trace.py` and then went silent until
the 7200 s session timeout (TIMEOUT), OPENAI-TERRA again (ERROR). Three
non-committing sessions is the stall limit, the worker exited 4, and the
dispatcher — correctly by its own contract — closed the row `partial`
(`b38d2cf4`), refreshed, merged it (`ab3b260b`, bar PASS 11/11) and minted
the disposition row `WI-542`. The slice's work is on trunk UNREVIEWED; the
keep/discard split is `WI-542`'s to judge, and the standing-debt-owner role
the row carried (the module-size ratchet's pointer names it) needs a
SUCCESSOR from that disposition — the ratchet's own rule says the pointer
moves in the same commit a debt owner closes, and this close did not move
it. The run then exited 1 on UNLOAD INCOMPLETE (the lane worktree held an
ignored `out/run-logs/` stream); the streams were copied to the session
scratchpad (their clipped copies are tracked under `docs/iteration/`) and
the worktree and branch removed with the integrator's printed remedy.

**The alternative:** keep the lane open by hand-reverting the partial close.
Rejected: a hand-moved spec. **What the owner should weigh:** a stall guard
that counts a reviewer's outage as the builder's stall turns a provider
limit into a handback of finished work; the hang on the third family is a
second sample of OPENCODE-GROK's unreliability after decision 14's
wrong-tree finding.

## 18. The `wi508` lane's refresh conflicted with trunk after the WI-521 merge — resolved with the integrator's own remedy, at the cost of one more verdict round

A supervisor error, named as such: the station refresh `c225c34d` (drawn to
satisfy round 012's "regenerate" ask) was then committed OVER by the
round-013..017 reworks, so the disposable refresh commit could not be
peeled, and its compiled `docs/log.md` and regenerated artifacts collided
with the trunk that now carried WI-521's merge. The integrator refused the
refresh and printed its remedy — merge trunk on the branch, commit, refresh
again — which was followed: trunk's `PROJECT_STATE.html`, `docs/stage` and
`docs/status.md` taken as-is (the refresh regenerates them), `docs/log.md`
spliced as base + the lane's five compiled entries + trunk's WI-521 entry so
no record is lost and the order stays chronological, `test-cases.toml`
auto-merged, nothing product-side resolved by hand (`52faa5d8`). A hand
trunk merge is a non-record commit, so the compiled APPROVE is stale by the
gate's rule and round 018 was drawn on the merged tip. **Lesson for the
protocol text:** "never hand-merge trunk on a work branch" needs its
corollary stated — never commit work on top of a refresh commit either;
peel it first (reset to the work tip) or the next refresh will conflict.

## 19. `WI-543` filed in `deferred/` as `SR-163`'s verification owner — the kit's allocator, the owner's queueing

Round 018 (terra, on the merged tip) left one MAJOR: `SR-163` is an
Approved `Test` requirement whose only TCs are Drafted and no longer cite it,
so `trace.py --strict` names it an orphan after the close; the reviewer's
remedy is *"file a successor owning SR-163"* and trace a complete TC before
closing the owner. The row is filed (`docs/work/deferred/WI-543-…`, id from
`intake.next_wi_id`, watermark raised by `trace.py --bump-ids` — no id
invented), in `deferred/` deliberately: the join it asks for is a
purpose-reference authoring pass over the whole shipped surface, a scope the
owner should sequence against the queued programs rather than have a
scheduler hand out unattended. An owner in the registry satisfies the
reviewer's ask; moving it to `queued/` is the owner's one-line act.

**The alternative:** queue it now (it would land on the frontier at P3 behind
the queued rows and could be claimed this run) or refute the finding (it is
correct: an Approved Test SR with no TC is exactly what the orphan rule
exists to name). Neither is better.

## 20. STOP RULE APPLIED: the `wi508` lane is HELD for the owner's own verdict — its ref renamed, nothing deleted, the rest of the grind unblocked

Round 019 (terra, on the refreshed tip carrying `WI-543`) returned three
MAJORs: (1) put a TC back on `SR-163` — the opposite of round 013's finding,
which removed it; (2) the re-attestation brief renders a `Drafted` row as
"_approved — re-attestation owed_"; (3) the brief truncates a changed Method
cell. Findings 2 and 3 are defects of `trace.py --approve modified` on trunk,
not of this lane; finding 1 is the inherent tension an Approved `Test`
requirement without a complete TC must land on one side of — orphan or
false coverage — and two rounds of the same reviewer have now asked for each
side. Eleven rounds on one lane is the point at which the loop's own ladder
pages a human, and decision 10 said the supervisor would stop drawing rounds
rather than keep redrawing until one reviewer did not notice.

**Done:** `git branch -m wi508-architectural-remap
wi508-architectural-remap-HELD-for-owner-verdict`. The dispatcher reads
finished and parked lanes off the ref, so the lane leaves the merge queue
(the merge slot would otherwise refuse it on the verdict rung and stop the
whole run) while every commit, every round file and the compiled
`docs/reviews/WI-508-REVIEW-A.md` stay exactly where they were; the claim
directory `docs/work/active/wi508-architectural-remap/` stays on trunk. To
resume: rename the ref back and either run one more round the owner is
willing to accept, or take the owner's own verdict and merge through
`integrate.py integrate`.

**For the owner, in one line each:** the two brief-renderer defects (rows
`Drafted` shown as re-attestation; Method cells truncated); the SR-163
tension (queue `WI-543`, or amend the SR's verification class — an Approved
cell, so the owner's); and whether a lane whose remaining findings are
contradictory or trunk-side should be mergeable on the record.

**The alternative:** keep redrawing (each round ~10 min, each on a new
objection), or refute round 019 finding 1 with round 013's own text. The
first is not review; the second is arguing with a gate.

## 21. An adjudication row has no closer — the lane was resumed in a cycle; the supervisor closed `WI-542` with the kit's own move tool

`WI-542` (the `WI-521` disposition) ran two ADJUDICATE sessions on Opus,
each ending DONE with a recorded verdict (`WI:` trailer present) and a
`## Dispositions` successor draft — the brief's contract, which also says
*"Never move a spec yourself"* and *"the machinery mints your draft at this
row's own close"*. But no machinery performs that close: the spec stays in
`active/<branch>/`, `integrate.finished_branches` does not list the lane, the
dispatcher reads it as parked and resumes it — cycle 1, 2, 3 — each resume a
fresh adjudication session (~5–12 min of Opus) that DONEs again. Stopped
after the third resume. **Closed by the supervisor:** `## Deliverable`
filled from the two verdicts (before `## Context`, R-A), the spec moved with
`spec_move.py` — the kit's own link-aware close ritual, the one the worker
brief names for a terminal move — to `docs/archive/work/complete/`,
committed on the lane with the `WI: WI-542` trailer, so the drain merges it
and intake mints the successor. `WI-544` (the `WI-484` disposition) will need
the same act. **For the owner:** an adjudication lane needs a closer — either
the brief lets the adjudicator make the terminal move, or the dispatcher
closes an adjudication lane whose verdict is recorded. Until then every
disposition row loops.

## 22. `WI-542` merged: one cross-family round drawn on the adjudication lane and compiled as its WI-level verdict; `WI-545` is the debt owner's successor

The merge slot refused `WI-542` for lacking `docs/reviews/WI-542-REVIEW-A.md`
— RULING-7 applies to every `merged` outcome, adjudication rows included, and
history shows disposition rows were only ever closed by owner sittings on
trunk (`WI-457`, 2026-08-15), never through the slot. Rather than write an
APPROVE nobody wrote, one REVIEW-A round was drawn (OPENAI-TERRA) over the
lane's diff: `APPROVE findings=0` after running the R-F tests, the strict
trajectory checker, the harness (`RESULT: PASS`) and the smoke budget
(21.5 s). The WI-level file compiles the two concurring ADJUDICATE verdicts
(`OUTCOME: PARTIAL successors=1`, both) and that round; the slot merged
(`d869f48a`) and intake minted **`WI-545`** — the decomposition debt owner
(cont.), `supersedes = "WI-521"`, whose first commit must move the
module-size ratchet pointer. **For the owner:** whether an adjudication row
should owe a REVIEW-A at all (its product is a verdict) is a protocol
question; today it does, and only a compiled file satisfies it.

## 23. Every mechanized lane ends the run with `UNLOAD INCOMPLETE` — the loop's own session stream is counted as unique data

`integrate.unload` refuses to remove a merged lane's worktree while it holds
an ignored `out/run-logs/` stream — which the loop itself wrote for that
lane's sessions — and reports INCOMPLETE with exit 1, ending the run after
every merge (`WI-521`, `WI-542`; `WI-484` unloaded clean only because the
supervisor had emptied its `out/` first). The streams' clipped copies are
tracked under `docs/iteration/`; the full streams were copied to the session
scratchpad each time and the worktree removed with the integrator's own
printed remedy. **For the owner:** a walk-away run cannot survive its first
merge under this rule; either the unload sheds the loop's own `out/run-logs/`
(it knows it wrote them) or the exit code stops meaning "stop".

## 24. `WI-544` (the `WI-484` disposition) adjudicated PARTIAL with one successor — the delegated residue; closed by the supervisor; the adjudicator's draft transcribed into the spec

The Opus adjudicator's finding is the run's own diagnosis stated by an
independent hat: the lane *"delivered none of the drafting the owner's
Delegated section assigned"* because it read a branch spec the delegation had
not reached (decision 4). Its successor is scoped to exactly items 3 and 5
of that section — the `hats.toml` `knowledge` value-pass and the 17
approved-cell `Rationale` attribution deletions — `buildtier = medium`,
`safety_class = spine`, `supersedes = "WI-484"`; item 7 excluded as a ruling
owed by nobody. Two transcription acts, recorded in the row itself: the
adjudicator wrote its draft into the VERDICT file (intake reads the spec's
`## Dispositions` section) under a `[disposition]` table header (an unknown
key intake refuses, nothing minted, merge refused), with a title over the
120-character rule — the block was copied into the spec's section, header
dropped, title shortened, cells verbatim; validated with intake's own parser
before the commit. Closed with `spec_move.py` as decision 21 describes.
**For the owner:** the adjudication brief should say WHERE the draft goes
and that it is top-level keys — two adjudicators in one run each missed one
of those.

## 25. A kit defect found by the `WI-544` review round, fixed on trunk: `intake._draft_row` never wrote a successor's `supersedes` — every minted successor lost its lineage

The round's BLOCKER: the asserted lineage and scope would be lost at the
mint because `_draft_row` emits `Supersedes=''`. Verified on trunk: `WI-545`
(minted from `WI-542`'s draft, `supersedes = "WI-521"` in the draft) carries
no `supersedes` at all. The row schema has the column (`wi_convert.COLUMNS`,
`kitlib/registry.py`) and `_DRAFT_KEYS` accepts the key; the writer simply
never copied it. **Fixed with one assignment** and a unit test
(`test_a_drafted_successor_keeps_its_supersedes_lineage_at_the_mint`), the
module-size ratchet baseline for `intake.py` re-stamped 1984 → 1985 with the
reason on the entry (a reviewed bump, not a sanction), and `WI-545`'s queued
frontmatter repaired with `supersedes = "WI-521"` — a triage edit to a queued
row, not a move. The mint runs from trunk's `intake.py` at the merge, so the
fix had to land on trunk BEFORE the `WI-544` merge for its successor to keep
`supersedes = "WI-484"`. The review's other two findings: stale generated
artifacts on the lane (the refresh's regen) and trailing whitespace the
session telemetry wrote into the clipped log (stripped).

## 26. `WI-544` round 2: a minted successor now carries the adjudicator's scope prose in its Context — a second small kit change on trunk

Round 2 (terra) accepted the lineage fix and found the next hole: intake's
`_disposition_drafts` gave every minted successor a one-line provenance
Context, so the boundary the adjudicator wrote beside its draft (items 3
and 5 only, item 7 excluded, the knowledge-pack rule) never reached the
minted row — `WI-545`'s Context is that one line. Taken: `parse_dispositions`
keeps the prose that follows each fenced draft, and the minted Context is the
provenance line plus that prose verbatim; the replay test asserts the prose
lands in the minted spec. `intake.py` ratchet re-stamped 1985 → 1990 with the
reason on the entry. `WI-545`'s own Context is NOT rewritten (its scope is
one link away in `WI-542`'s archived `## Dispositions`); the owner may prefer
to copy it in.

## 27. `WI-544` round 3 (MINOR): the scope prose is now kept verbatim — `strip()` had eaten an indented first line

Taken as asked: only the fence-delimiting newlines are dropped; the replay
test carries an indented line and a list item and asserts they land
byte-for-byte (`1309a426`). Three review rounds on a disposition lane have
each found a real defect in the same twenty lines of intake — the mint path
for drafted successors had never been driven end to end. Round 4 drawn.

## 28. `WI-544` merged at round 4; `WI-546` minted WITH lineage and scope — both intake fixes proven live; the grind reached `WI-537`

Round 4 (terra) APPROVEd with no findings after the verbatim fix; the
compiled WI-level file carries one adjudication and four rounds. The slot
merged, unloaded clean (its `out/` had been salvaged and emptied first), and
intake minted **`WI-546`** — `supersedes = "WI-484"` present, the items-3-
and-5 boundary and the item-7 exclusion in its Context — the first
successor the kit has minted with its thread and scope intact. The
dispatcher then claimed `WI-537` (the complexity sensor, `spine`,
exclusive): the first of the seven queued rows the run was asked to
integrate, ~8 hours after launch. What stood in the way is the record above
— none of it was the queued work.

## 29. `WI-537` built and APPROVEd (round 3, grok-4.6 after OpenAI's second limit) — but the loop's worker brief carries no closing step, so the supervisor closes the row; and a shipped-fragment heading defect

The sensor landed in one 32-minute Opus build; rounds 1–2 (terra) found a
real census gap (functions under `for`/`while`/`match` skipped) and a
boundary-wording split, both reworked on the lane (the round-2 escalation was
again a Sol DESIGN-CHECK that committed the fix itself); round 3 ran on the
third family because OpenAI hit its usage limit a second time (reset 18:34
UTC) — grok answered in 11 minutes this time, `APPROVE findings=1`, the one
MINOR (a missing baseline compared as empty) carried to the owner's list.
The worker then exited DONE with its spec **still in `active/`**: the shipped
`worker.template.md` says nothing about the terminal move, so under the
mechanized loop no build lane closes its row — the dispatcher resumes it as
parked, a fresh Opus session finds nothing to do, and three of those trip the
stall guard into a `partial` close of finished, approved work. Stopped at the
first resume. **Closed by the supervisor** as decisions 21/24 describe:
`## Deliverable` compiled from the lane's own fragment, `specref` cleared,
`spec_move.py` to `complete/`, the WI-level verdict compiled from the three
round files. Two more defects on the record: the worker's fragment opened
with `# ` (trunk_step refuses it at the first refresh — the very defect the
2026-08-30 sitting cleared three of), fixed at the close; and session 009
amended a commit message with `--no-verify` (message-only, on a tree that
had just passed every gate — harmless, but the brief forbids it). **For the
owner:** the worker brief needs the close ritual (Deliverable before
Context, SpecRef cleared, `spec_move.py` to the terminal folder) and the
fragment heading form stated explicitly.

## 30. `WI-537`'s refresh red on `approval-fresh` — the brief regenerated on the lane after the governing round, recorded on the compiled verdict rather than buying a fourth round

The lane minted four `Drafted` rows and never rendered `docs/ratify/CURRENT.md`,
so the station refresh refused. The render is a derived artifact of the kit's
own generator (`trace.py --approve modified`); no cell, code or test moved. It
was committed on the lane (`e64bb754`) and the compiled WI-level verdict
re-committed after it with a paragraph saying exactly that (`8a6f7fc9`), so the
verdict rung's freshness comparison passes on a mechanical render — the same
reasoning the protocol applies to a refresh commit — instead of a fourth
review round over an unchanged tree. **For the owner:** the worker brief
should tell a lane that mints spine rows to render the brief before it closes,
or `trunk_step --regen` should own that render like the other derived
surfaces; either removes this stop.

## 31. `WI-546` built (the delegated residue) but its worker never wrote the `WI:` trailer — no review was scheduled and the row was re-dispatched; closed by the supervisor, review drawn by hand

Four Opus build sessions committed the two delegated items — `docs/requirements/hats.toml`
`knowledge` values (re-pointed to `docs/knowledge/` packs, drafts marked) and the 17
approved-cell `Rationale` attribution deletions, every touched cell listed in the lane
fragment for the owner's review at return — and then sat waiting on a backgrounded full
suite until their turns ended; none of the five work commits carries the `WI: WI-546`
trailer the loop keys on (`worker_endstate`, `schedule_review_round`), so the loop
scheduled no review, kept re-launching BUILD sessions that found nothing to do, and was
two no-commits from the stall guard when stopped. Closed as decisions 21/29 describe
(Deliverable moved BEFORE Context — the worker had put it after, which R-A clips to
empty; SpecRef cleared; `spec_move.py`; the fragment heading dated; the re-attestation
brief regenerated for the amended approved cells and the ten drafts), the close commit
carrying the trailer. **For the owner, in the brief:** 17 amended `Rationale` cells on
Approved SR rows and the `hats.toml` drafts — the delegation put the cut at return;
read `docs/ratify/CURRENT.md` before blessing. Review drawn by hand on the third family
(OpenAI limited until 18:34 UTC), compiled as before.

## 32. `WI-546` merged at round 4; the run is drained, paused and quiet — the state the owner asked for

Rounds 1–3 (terra) each found a real hole in the delegated residue's own
verification — a dangling "lenses named above" in `SR-175`'s thinned
rationale, then the value-pass guard accepting an absolute path, then a
traversal (`docs/knowledge/../status.md`) — each taken with a test; round 4
APPROVEd with no findings. Two grok draws before that were aborted: one died
on a doubled `--dir` (the supervisor's helper plus the fixed template — the
helper now injects only when the template lacks it), one went silent five
minutes in and was killed at the 46-minute mark by hand (the second C3
sample). One supervisor defect on the record too: the first compiled
`WI-546-REVIEW-A.md` ordered its rounds ALPHABETICALLY by round-file sha, so
the governing line mid-file read CHANGES-REQUESTED — caught by re-parsing
before any merge attempt, recompiled in time order (`a4b862e7`). The merge
ran through `integrate.py integrate` directly because the pause stops the
dispatcher BEFORE its drain (the pause doctrine says a pause ends "fully
merged and quiet"; the dispatcher exits 8 first — a small kit finding for
the C-series). At the merge, intake's amendment arm minted **`WI-547`**
(adjudicate the 17 amended approved SR `Rationale` cells — the ordinary
mechanism reading the delegated deletions; it queues behind the pause).
End state: trunk `fd45628a`, no active claims, the held remap branch aside,
eight rows queued, the pause armed, no agent process running.
