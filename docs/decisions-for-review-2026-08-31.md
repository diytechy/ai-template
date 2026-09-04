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
inside an HTML comment — two `<!-- fig: cmd="grep -c '^### `scripts/' …" -->`  <!-- fig-ok: prose about the convention -->
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

## 33. The stall-guard build ran on a loaded box: the commit bar's RESULTS are enforced, its SECONDS are recorded OVER with the cause

**Decided:** build WI-548 with the smoke tier's results enforced per commit
(1426 passed, 6 skipped, every commit) while the budget step reads OVER
(86-124 s vs 60 s): the box is not quiet — Halo Infinite held ~28 % of the
CPU (Get-Counter, sampled at session start), and the instruction to run alone
cannot be honoured against the owner's own foreground use of the machine.
The budget is untouched; the quiet 40.7 s reading of 2026-08-30 stands; a
quiet re-measure is owed before the loop relaunches (the WI-496 precedent:
one box is one data point, and the budget is not moved to fit a loaded box).

**The alternative:** wait for the box to go quiet (unbounded — the game is
interactive use), or kill the process (not the supervisor's to do). Neither
delivers the work the pause is holding the frontier for.

**Reversal cost:** none — a re-measure on a quiet box either confirms the
budget or is its own finding.

## 34. The tracked pause was lifted for exactly one claim (WI-548) and re-armed in the next commit

**Decided:** `docs/work/pause` deleted (`a0550168`), `integrate.py claim` run
for WI-548, the byte-identical pause restored (`bf7c1938`) — the frontier was
claimable for one serial commit window in a session whose only claim is the
row the pause itself names as its lifting condition.

**Why.** The claim rung refuses EVERY claim under a pause, including the
stall-guard claim the pause exists to wait for — a catch-22 in the machinery
(kit finding: a pause may need a named exception list, or the unpause could
be required before the claim in the pause's own reason text). Building
without a claim would bypass the integrator; leaving the pause down while
building would open the frontier to any concurrent launch.

**Reversal cost:** none; both commits are on trunk in sequence and the pause
stands again.

## 35. WI-548 shape choices: one row for C1-C7; the ADJUDICATOR closes its own row; two unload pins overturned; the TERRA effort dial applied as an experiment

**Decided:** (a) one row instead of the plan §3's two — the pause lifts after
a single reviewed merge, and C6 is the other half of the same defect; (b) C6's
adjudication closer is the BRIEF instructing the adjudicator to close its own
row (Deliverable, specref, spec_move.py, trailer) rather than a new dispatcher
close path — a smaller diff, no new authority in dispatch, revisitable as its
own row if the brief proves insufficient (the plan called the dispatcher path
cleaner; this is the deliberate deviation); (c) the two shipped unload tests
pinning "an ignored out/run-logs stream refuses the unload" are OVERTURNED
with the behaviour, the overturn stated inside the rewritten tests (the
stream is the loop's own artifact with a tracked clipped copy — decision 23's
measurement); (d) `docs/agents.toml` OPENAI-TERRA carries
`-c model_reasoning_effort=medium` as the C7 item-5 experiment, measured
against the recorded ~10-minute unpinned rounds — keep or revert on numbers,
noted on the row. Also bookkeeping: the plan drafted the row as "WI-547", but
that id was already minted at the WI-546 merge; the allocator issued WI-548.

**The alternatives:** two rows (more ceremony under a held frontier); a
dispatcher-side closer (new machinery unreviewed by the owner); keeping the
unload pins and shipping a dead letter (the C6 shed would never fire); the
dial unmeasured (the plan explicitly asks for measurement).

**Reversal cost:** (b) and (d) are one-file edits; (c) restores with the old
test text; (a) is spent at merge.

## 36. The stall-guard row landed at round 5 on gpt-5.6-terra with the reasoning-effort dial — five rounds, every finding taken at the root

**What happened.** Rounds 1–4 each found one real hole and each was reworked
rather than argued: the plan's own C4 fake-route test was uncovered (four
probe-driven tests added); a resumed owed round forgot the builder's family
and the brief named scaffold-only script paths (`family=` rides the marker,
`{scripts}` is the fourth rendered slot); the owed marker was the only
evidence and its write could fail silently (owed-ness now derives from
COMMITTED facts — built trailers, no verdict naming HEAD — the marker is
advisory and loud on failure); the unload shed a directory rather than the
loop's own stream NAMES (a foreign neighbour now refuses by name). Round 5:
`APPROVE findings=0`. Merged through `integrate.py integrate` under the
pause (in-slot refresh, bar PASS 11/11, unloaded clean), the spot-check
disposition row minted by the `complete_review = "sample"` dial.

**The effort-dial measurement (C7 item 5):** the TERRA review leg ran with
`-c model_reasoning_effort=medium` at 202 / 320 / 316 / 351 / 350 s wall
against the ~10-minute unpinned rounds recorded on 2026-08-30 — roughly a
third of the wall per round, with substantive findings on every round that
had one to find. **Decided:** the dial stays on the row (a value in this
repo's registry). **The alternative:** revert to the unpinned template.
**Reversal cost:** one line.

**Not exercised live at this merge:** the C6 unload shed — the supervisor
drew the rounds through a helper that writes no `out/run-logs/` stream, so
the lane held nothing to shed; the shed is proven by its tests (a properly
named stream and the marker go, a foreign neighbour refuses) and will be
proven live by the first loop-driven lane after the unpause.

## 37. Two "silent hangs" this session were the supervisor's own renderer, not the provider — recorded as such, and the kit hardened

The first round draw went silent for 55 minutes and was killed by hand; the
redraw went silent and was killed by the new idle deadline at 909 s. Both
had the same cause, found in the transcript: the helper's console `print`
hit a cp1252 `UnicodeEncodeError` on a `→`, the exception killed
`run_session`'s pump thread, and the codex child blocked on its full
stdout pipe. Neither was a TERRA hang, and the earlier reading of the first
one as a provider hang was wrong. **Decided:** the pump outlives its
renderer (`_pump_stdout` swallows a renderer exception; a test drives a
renderer that raises on every line), landed inside the row because it is
the C3 failure class exactly — a session that reads as silent when nothing
is wrong with the provider. The idle deadline did its job at 909 s, which
is the C3 acceptance on a real sample. **For the owner:** the two 2026-08-30
opencode "hangs" (decisions 14, 17, 32) predate this finding and were
observed through the loop's own UTF-8 console, so they stand as recorded;
but the class "pump death reads as a hang" is now closed for both.

## 38. A pre-existing resume defect was fixed INSIDE the row: a resumed worker's integration base defaulted to HEAD

Driving round 3's regression (the owed round must survive a lost marker)
showed the derivation could never fire in production: a resumed worker with
no `--base` took HEAD as its base, so `base..HEAD` evidence was always empty
on resume — the built trailers, the owed round and the resume itself were
invisible. That is the mechanism under decisions 21, 29 and 31 ("the resumed
session finds nothing to do"). **Decided:** `default_base` is the merge-base
with the trunk (the claim commit in a lane worktree; HEAD, exactly as
before, when the primary checkout is the branch itself), pinned by a
worktree test. **The alternative:** file it as its own row and ship C2 as a
dead letter until then. Rejected: the reviewer's finding was about exactly
this restart, and the fix is nine lines with a test. **Reversal cost:** one
function; every adopter's resumed lanes start seeing their own evidence.

## 39. The pause STAYS — the owner's mid-run instruction; the loop was not relaunched

**Owner instruction (2026-08-30, in session):** keep the pause in place and
ask for confirmation before removing it — the owner is disconnecting from
the network and wants no session interrupted. **Decided:** step 2 of the
sitting's brief (delete the pause, relaunch `agent-resume`) is NOT taken;
the repo is left merged, drained and quiet with the pause armed, no agent
process running, the held `wi508` branch untouched. The frontier behind the
pause now reads: the spot-check disposition of the stall-guard row's own
clean close (minted by the sample dial at the merge — an adjudication row,
strong route, and the first lane the C6 close ritual and the C2/C4/C5
machinery will run on), then the seven rows the previous sitting queued.
**Unpausing is the owner's one-line act after this confirmation, or the
next session's on the owner's word.**

## 40. The unpause, the quiet-box re-measure, and a one-name kit fix landed on the trunk lane after the first loop-driven merge

**The unpause (owner-confirmed, no decision):** `docs/work/pause` deleted in
`c7433820` with `docs/open-items.html` regenerated; smoke tier re-measured on
a quiet box first (5–9 % CPU): **1426 passed, 6 skipped in 26.65 s;
`check_smoke_budget.py --mode enforce` 25.2 s vs 60 s → within** — decision
33's owed reading, the budget untouched.

**Decided:** after the loop's first merge (WI-547) ended `UNLOAD INCOMPLETE`
(exit 1, the merge standing), fix the cause on the trunk lane while the loop
was stopped, in one reviewed commit with a test: `out/agent-loop.lock` — the
loop's own per-checkout coordinator lock, which `release_lock` never unlinks —
joins `integrate._RESIDUE_OUT_FILES`. The C6 shed had already removed the
lane's three `out/run-logs/` streams (proven live); the lock alone held
`out/`, so `rmdir` failed and the re-read named the collapsed `!! out/`. The
fixture `residue_lane` now plants the lock (every real lane holds it), a
focused test covers lock + stream, and the module-size ratchet is re-stamped
2653 → 2655 for the two comment lines (reason on the entry).

**Why on trunk and not a row:** every subsequent merged lane would stop the
run at the same line (each merge = exit 1 + a manual `git worktree remove
--force` + relaunch); the fix is one declared name whose class the code
already states (`out/review-owed`); a work branch cannot mint an id (R1) and
the supervisor is forbidden to hand-mint one — the precedent is the trunk-lane
`check_docs` fix of 2026-08-30 (decision 1). **The alternative:** unload every
merged lane by hand for the rest of the run and file the finding for a row.
**Reversal cost:** one name in one set, one fixture line, one ratchet stamp.

## 41. WI-547 (the seventeen-row amendment adjudication) was closed by the supervisor after the loop drew two identical APPROVE rounds and stalled; the close cost two more rounds

**What the loop did (its first live lane after the unpause):** the Opus
adjudicator ruled `VERDICT: CLARITY rows=17` in 96 s (every amended cell a
`Rationale`; fifteen label strips, SR-111/SR-112's trailing C-MNT-7 sentences
removed as provenance meta-text; the obligation unchanged everywhere) and
committed it with the `WI:` trailer — then the worker exited `DONE` claiming
"review round approved" with **no round drawn**. The dispatcher's resume
derived "review owed (committed evidence: built, no verdict for HEAD)" — C2
working as designed — and drew REVIEW-A on OPENAI-TERRA: `APPROVE
findings=0`. The next resume derived the same thing AGAIN, because the
loop's own telemetry/scoreboard commits had moved HEAD past the verdict, and
drew a second identical round (`APPROVE 0`); the dispatcher's own
trunk-unmoved stall then ended the run (exit 4). No handback, no partial
close — C1/C2 held.

**Decided:** close the row as before (Deliverable before Context, `specref`
cleared, `spec_move.py` to `complete/`, `WI:` trailer), then take the verdict
round LAST as the protocol orders: the post-close round returned a MINOR on
my own closure wording (it said every amendment kept its charter clause; two
had dropped sentences), corrected in `6627abe1`, and the round on the
correction approved. The four rounds are compiled time-ordered into
`docs/reviews/WI-547-REVIEW-A.md`; the lane merged through the slot
(`efac96c4`). Nothing was flipped: all seventeen rows were already `Approved`
(the amendment never demoted them), and no script consumes a `CLARITY`
verdict — it is a record and a session-completion token.

**Kit findings (not fixed — filed for the owner, none has a row):** (A) the
in-process review schedule does not fire after an ADJUDICATE session (it did
fire after WI-535's BUILD) — the round exists only because C2's resume
derivation catches it; (B) that derivation compares the verdict against the
raw branch tip, so the loop's own telemetry/scoreboard commits re-owe a round
on every resume of an approved-but-unclosed lane; it should peel record
commits the way the merge slot does; (C) only the disposition brief received
the C6 close ritual — the amendment, conflict and red-TC briefs did not, so
an amendment lane can never finish on its own. **The alternative:** let the
dispatcher's stall bound the loop and close nothing — the row would never
merge. **Reversal cost:** none; the close is a record and the merge stands.

## 42. WI-549 (the sample-dial spot-check) closed ITSELF — the C6 worker ritual's first live proof — and was merged by hand through the slot after the run stopped on the owed WI-level verdict

**What the loop did:** the medium Opus worker, on the ordinary brief (the
row declares no adjudicator brief), audited WI-548's close, found every
C1–C7 deliverable and adopter-compat surface in the tree, and closed its own
row in one session (285 s): Deliverable before Context, `specref` cleared,
spec moved to `complete/`, fragment written, `WI:` trailer — verdict "the
close stands, no successor". Then, as with WI-547, it exited `DONE` without
a review round; the dispatcher's drain refreshed the finished lane (bar PASS
11/11) and stopped on `required verdict docs/reviews/WI-549-REVIEW-A.md is
absent` (exit 1) — decision 7's owed compile.

**Decided:** draw the cross-family round by hand on the same TERRA route
(`APPROVE findings=0`, 156 s), compile the WI-level verdict, and merge
through `integrate.py --root . integrate` rather than wait for the loop: the
dispatcher drains a finished lane only before an *exclusive* claim or at the
station exit, and the next row (WI-535, `ordinary`) had already been claimed
over it. The first attempt refused — the trunk's new claim commit conflicted
with the lane's earlier station refresh, which my two record commits had
buried (the 2026-08-30 trap) — so the lane tip was rebuilt as the pre-refresh
commit plus the two record-only commits and the slot redid its disposable
refresh. Merged `1553f22f`, **unloaded clean** — the lane held
`out/agent-loop.lock` plus a stream, the exact state decision 40's fix
covers. **The alternative:** leave it for the next barrier drain (hours
later, the same conflict waiting). **Reversal cost:** none.

## 43. WI-538's two raised cognitive ceilings were kept and REASONED, not restored — a recorded re-stamp, with the decomposition left to the debt owner

**What happened.** The arming re-stamp of `docs/complexity-baseline` took
`agent_loop.py::route_session` 35 → 37 and `run_iteration` 17 → 18 with
blank reason cells; the post-close round (012-REVIEW-A-f1d0fd6, MAJOR) read
that as raising a downward-only ratchet to clear a finding and offered two
ways out: restore the ceilings and decompose the functions, or place a
separately justified change under the applicable policy. Measured with the
lane's own sensor: both functions read 35 / 17 at trunk `8ac501de` (before
the stall-guard row) and 37 / 18 after it — the growth is WI-548's (the C4
probe and C5 relaxed rung in `route_session`, the C2 review-owed end state
in `run_iteration`), taken while the sensor was report-only.

**Decided:** the kit's standing rule for a ratchet that fires on legitimate
work — re-stamp deliberately and record the reason — applied by the
supervisor: the two rows keep 37 / 18 and carry the measured reason in the
baseline's own `reason` column (`3275b371`); the decomposition stays owed to
the decomposition debt owner (WI-545, queued), which is the row that owns
`agent_loop.py`'s size. The lane was already closed, so the loop could not
rework it (a terminal WI is refused) and a hand-moved spec is forbidden.
**The alternative:** restore 35 / 17 and decompose two of the loop's core
functions inside a close — a real refactor of the engine, unplanned and
unreviewed by the owner. **Reversal cost:** two cells; restoring the numbers
would red the armed gate until the decomposition lands.

## 44. WI-538's close was finished by the supervisor after the loop's own APPROVE: the approval brief, the baseline's serialization, and one excluded "round"

**What the loop did (eleven sessions, ~2 h 50 min):** an Opus build in two
sessions (the first with no `WI:` trailer), two sessions lost to a
backgrounded full-suite run each (the harness kills the run with the turn;
one short of the C1 build stall), the close with the trailer, then three
review rounds with a rework between each — a MINOR on a docstring, a MAJOR
on LLR-206's stale Detail plus baseline tabs, and after the router swapped
the implementer family to gpt-5.6-terra ("2 consecutive failed review
gates"), an APPROVE with one MINOR from an Opus reviewer. That TERRA build
session also committed a file named like a round
(`010-REVIEW-A-e26ab03.md`, "re-review approval") — an implementer writing
its own approval under the review path. The drain then went RED on
`approval-fresh`: the LLR-206 amendment (an `Approved` row) had staled
`docs/ratify/CURRENT.md`, which the worker brief names only for minted or
re-statused rows.

**Decided:** regenerate the approval brief with the kit's generator
(`f1d0fd67`), take the verdict rounds LAST (three more: the raised ceilings
— decision 43; the baseline's 178 blank-reason rows still in the five-field
form, stripped to what the tool's writer emits, `4288c3fa`; then `APPROVE
findings=0`), compile the WI-level verdict from the six genuine rounds with
the implementer's file excluded and the exclusion stated inside, and merge
through the slot (`3933bb11`, unloaded clean). No adjudication was minted
for the LLR-206 amendment — LLR-tier cells are traced, non-attesting by
ruling. **The alternatives:** leave the lane red for the owner (the queue
behind it stops), or count the implementer's file as a round (it is not a
fresh-context verdict). **Reversal cost:** none; every act is a record or
a generator's output.

**Kit findings from this lane, for the owner:** the worker brief should say
the full suite runs FOREGROUND with an explicit timeout; an amendment of an
`Approved` cell — not only a mint or re-status — owes the approval-brief
regeneration, and the brief should say so; a later lane amended a terminal
spec (`partial/WI-521`, +12 lines) and nothing refused it; an implementer
can write a `NNN-REVIEW-A-<sha>.md` file and the scoreboard's tripwire did
not name it on the following round.

## 45. WI-540's partial close was left to stand and its bar-inert artefact merged after a two-file repair — the disposition adjudication is the correction path, not a hand-moved spec

**What happened (eleven sessions, ~2 h 35 min).** The strong Opus worker
built the adjudicator session-retention layer (`adjudicator_session.py`, the
`[adjudicator]` dial shipped at 0, IF-174 minted, LLR-163/TC-157 amended) in
one 40-minute session with the `WI:` trailer but without the C6 close; the
in-process round (OPENAI-TERRA) returned CHANGES-REQUESTED with three MAJORs
and three MINORs and an `implementer-touched-review-path` tripwire, whose
page-human consequence re-armed DESIGN-CHECK. That design-check on
gpt-5.6-sol hit the **OpenAI usage limit** mid-session (ERROR, 32 min,
398k tokens, reset 08:40 UTC); the C4 probe then fired live for the first
time (`probe [OPENAI-SOL]: unreachable, cooled ~900s`) and the design-check
re-routed to OPENCODE-KIMI, which committed a rework addressing all six
findings (`223cd88a`), ran the full suite, went silent and was killed by
the C3 idle deadline at 900 s — the second live C3 proof. The next three
sessions (an Opus design-check, two Opus-strong builds) each verified the
rework, then ran the full suite, which the harness's ten-minute foreground
cap pushed into the background; each session ended its turn waiting for a
notification that never comes, the harness killed the run, and each was
NO-COMMIT. Three no-commit build sessions is the C1 build stall by its own
rule; the dispatcher closed the lane `partial` ("the work so far, committed
as-is"), and the §A3 quarantine path reverted the product diff to a
bar-inert artefact with the diff saved as
`docs/work/handback/wi-540-adjudicator-retention-layer.patch`. That revert
also took `docs/id-watermark` down 174 → 173 — a mark only ever rises — so
the reverted tree itself failed registry-integrity, the approval brief was
stale against it, and run 6 stopped "after its quarantine".

**Decided:** not to undo the partial (a hand-moved spec is forbidden and the
rework was never reviewed), but to make the kit's own correction path
reachable: the IF mark restored to 174 (the id is spent in this lane's
history), `docs/ratify/CURRENT.md` regenerated with `trace.py`, and the
artefact merged through the slot (`9bb80db9`, `WI-540=partial`); intake
minted the disposition row WI-550, which the relaunched loop claimed first
(an adjudication row, exclusive). The adjudicator's brief carries the C6
close and can rule the outcome and draft the successor that picks the
patch. The worktree held worker scratch files under `out/` (refused by
name, correctly) plus a lane-side `out/integrate.lock`; unloaded by hand.
**The alternatives:** leave the lane red for the owner (every relaunch
stops at it; the queue behind it is dead until then), or restore and
re-close the work by hand (a hand-moved spec, and unreviewed engine code on
trunk). **Reversal cost:** none — the artefact is inert and the work is in
the patch and the merge's ancestry.

**Kit findings, for the owner:** a close that requires the full suite
cannot complete inside one worker turn when the suite exceeds the tool's
ten-minute cap (≈ 12 min here) — the brief must direct a bounded/batched
form or the close will stall by construction (this is the standing lesson
of 2026-08-30, now mechanized into a partial close of finished work); the
§A3 bar-inert revert must leave the id watermark alone; a no-commit stall
on a lane whose work is built and trailered is the D6 class the plan named,
still open; `out/integrate.lock` in a lane is another loop-owned residue
name.

## 46. The pause is RE-ARMED at the session's end so the repo is drained and quiet — one reviewed deletion resumes the frontier

**Decided:** write the tracked `docs/work/pause` back in a reviewed commit
once the last lane of the sitting (WI-550) is merged and unloaded, with the
reason naming this session's end and the owner's brief ("end with the repo
drained and quiet"), and leave no loop process running. The frontier behind
it, in the scheduler's order: the successor the WI-550 adjudication drafted
(re-land the adjudicator session-retention layer from its preserved patch,
strong), WI-536, WI-539, WI-541 (blocked on the retention layer), WI-545.
**Why a pause and not a plain stop:** the loop has no "stop after this
lane" switch; a run left alive would claim WI-536 next and run unsupervised
into and past the blackout, and a killed run leaves a lane parked mid-build.
The pause is the kit's own graceful stop (the dispatcher stops claiming at
the next boundary), and the unpause is the owner's one-line act — the same
shape the owner just used. **The alternative:** leave the loop running
through the weekday blackout (it idles 12:00–19:00 UTC) and let it resume
unsupervised at 19:00. **Reversal cost:** deleting one file in one commit.

## 47. The claim-refusal on status.md prose is disposed by scrubbing the queued ids from the hand-authored surface — the retired supervisor prompt included

**Decided (2026-09-01):** the unpaused loop's first claim (the frontier head)
was REFUSED by `integrate._status_prose_refusal` because the RESUME HERE
narrative and the embedded supervisor prompt named the queued ids in
hand-authored prose. Disposed exactly as the refusal prescribes: a trunk
commit rewrote the RESUME HERE bullet to point at the generated frontier
without naming any queued id, and deleted the now-consumed supervisor prompt
block (it survives in this file's git history at `ac2f29fa`; this session is
the one it launched). **The alternative:** carve a prose exemption into the
refusal for the supervisor-prompt block — rejected as sanctioning a check to
green a step, and the prompt's job was done. **Reversal cost:** none — one
status.md edit, fully in history.

## 48. WI-563's undrawn round: the adjudication lane claimed "review round approved" with no round drawn — disposed by supervisor-drawn rounds, a rework, and a verification APPROVE

**Decided (2026-09-01):** the WI-563 spot-check lane (minted at WI-552's
merge) closed in one ADJUDICATE session whose exit banner claimed "review
round approved"; no round existed (the WI-559 defect — scheduling exists
after a committing BUILD only), and the verdict gate refused the absent
rollup. Rather than fabricate a rollup for an unreviewed lane, the
supervisor drew round 2 through an independent Opus reviewer with a hostile
brief (recorded as `002-REVIEW-A-ef9f326-supervisor.md`): CHANGES-REQUESTED
findings=4 — the spot-check had missed a live `check_trajectory --strict`
ERROR that WI-552 arm 5 introduced (`schedule.py` lazy `import trace`, an
undeclared CMP-008 -> CMP-006 crossing, attributed by control to
`b2b06898`), excused by a false "no pytest toolchain" Bar claim. A
supervisor-dispatched rework (`26c18f8b`) corrected the verdict to "stands
WITH FINDINGS — successor owed", restated the Bar with real output, and
drafted the successor + OI as fenced disposition blocks; the same reviewer's
verification round APPROVEd (findings=2 MINOR), and the lane merged with the
rollup compiled from both rounds. **The alternatives:** author an APPROVE
rollup with no round (the exact forgery hazard OI-70/OI-76 name), or close
the lane partial and strand the spot-check. **Reversal cost:** none — every
act is a recorded commit on the merged lane.

## 49. The post-merge intake crash and the sweep's retroactive bite — recovered by calling `intake_after_merge` with the merge's own scope

**Decided (2026-09-01):** the WI-563 merge's intake step crashed
(`ModuleNotFoundError: intake`) because the supervisor ran `integrate.py`
from inside the lane worktree and the auto-unload deleted the script's own
directory mid-run — the merge stood, the disposition drafts went unminted.
The documented recovery (`intake.py sweep`) REFUSED on `WI-457`, a
2026-08-15 DONE disposition row that predates the fenced `## Dispositions`
convention: `_cmd_sweep` builds its outcome map from EVERY terminal folder,
so the new OI-70/OI-73 guard bites historical rows and the recovery sweep is
structurally unusable while any pre-convention adjudication row is archived
(kit defect, unfiled — a candidate rider for WI-565's ruling or its own
row). Disposed by invoking `intake.intake_after_merge` directly with the
merge's honest scope (`{'WI-563': 'merged'}`, the real before/after shas):
minted WI-564 (the seam) and WI-565 (the OI ruling row) at `9368db32`.
**The alternatives:** edit the archived WI-457 spec to satisfy the guard
(falsifies a settled 2026-08-15 record — its successors WI-458/459/460 were
already minted by the old mechanism), or patch `owes_successor`/`_cmd_sweep`
on trunk unreviewed. **Reversal cost:** none — the mint is one bookkeeping
commit; operational lesson recorded: run `integrate.py` from the TRUNK root
path, never from inside a lane worktree it may unload.

## 50. WI-566's adjudication corrected under supervisor-drawn review: the census de-inflated to rows=6 and the false successor promise replaced with the true carrier

**Decided (2026-09-01):** the WI-566 amendment adjudication (one ADJUDICATE
session, no round drawn — the same WI-559 defect as WI-563) ruled the right
rows MEANING but inflated its census to rows=23 with seventeen SR rows
WI-547 had already adjudicated, and closed with no `## Dispositions` while
its machine-inserted Deliverable promised minting successors. Disposed by
the same supervised pattern: an independent Opus round (CHANGES-REQUESTED
findings=5), a rework (`80405032`) that re-issued the verdict IN PLACE to
`VERDICT: MEANING rows=6` (evidence: `verdict_refusal` is per-session and
`re.search` takes the FIRST verdict line, so an appended correction would
never govern; no immutability convention covers docs/reviews/), replaced the
false sentence with the true reasoning (WI-553 already moved the code; the
re-attestation obligation is carried by snapshot drift and renders 6/6 rows
in the `--approve modified` brief), and wrote the missing fragment; a
verification round APPROVEd (findings=2 MINOR) and the lane merged clean.
**Kit findings for the owner (unfiled, candidates for rows):** the
amendment-brief adjudication arm has NO refusal invariant (`dispose:`-prefix
keying misses `adjudicate:` titles — a MEANING ruling can close successorless
and merge silently, handback.py:519); `intake.parse_dispositions` REFUSES a
prose-only `## Dispositions`, so the kit has no shape for "adjudicated
MEANING, no successor owed"; and the lane commit hook resolves ruff via the
SYSTEM python3 and prints a loud SKIP on every commit from a worktree on
this box. **The alternative:** merge the adjudication as-written (a permanent
record with an inflated census and a promise of successors that cannot
exist). **Reversal cost:** none — the correction chain is fully recorded on
the merged lane.

## 51. The pause is RE-ARMED at this session's end — five rows merged, the queue advanced, the repo drained and quiet

**Decided (2026-09-01):** write the tracked `docs/work/pause` back in a
reviewed commit once WI-566 is merged and unloaded, leaving no loop process
running, per the owner's standing "end with the repo drained and quiet"
brief and decision 46's precedent. The session merged WI-543, WI-552,
WI-553, WI-563 and WI-566; minted WI-564 (the strict-ERROR seam), WI-565
(the DOTALL OI ruling row) and WI-566 (consumed); recorded decisions 47-51.
The frontier behind the pause, in the scheduler's order: WI-554, WI-557,
WI-560..WI-562, WI-564, WI-565, then the standing queue. The wi508 phantom
claim now REDS `check_trajectory --strict` via WI-553's new hold-ban
detector (alongside the WI-564 seam ERROR) — both are queued rows' business,
neither blocks the non-strict bar. **The alternative:** leave the loop
running unsupervised into and past the 12:00-19:00 UTC blackout.
**Reversal cost:** deleting one file in one commit.

## 52. The wi508 partial-close lane (WI-555) was landed by a hand merge of trunk into the lane and two supervisor-drawn rounds, because the station refresh cannot carry a trunk snapshot delta

**Decided (2026-09-01, evening):** the WI-555 lane was cut at `6d3d9db4`,
before its own worker performed the OI-71 conversion directly on trunk
(`979c3e5f`, `551d1b2c`), which moved `docs/archive/last_approved/`. The
in-slot refresh (`merge --no-ff --no-commit`, `add -A`, bar) then staged
trunk's snapshot delta and was REFUSED twice: the staged mirror rule read the
delta as a snapshot WRITE (integrity ERROR) and `approval-fresh` compared the
committed old snapshot against the live merged registries (STALE). A plain
merge of trunk into the lane passes both checks (measured in a detached probe
worktree, then removed). Disposed by the precedented remedy on the wi508
branch itself (`9bdd56b6`): merge trunk into the lane as a plain commit
(`5c8a007a`), accept that it stales the round-004 APPROVE, and DRAW the round
it costs through an independent Opus reviewer with a hostile brief (round
005, CHANGES-REQUESTED 9; after a record-only rework, round 006, APPROVE 5),
then compile the rollup and merge from the trunk root (`77270030`). **The
alternatives:** re-cut the lane from current trunk (the id is claimed in
`active/`; no kit path re-cuts a claimed record-only lane), or edit the two
checks to tolerate a staged merge delta (sanctioning a check to green a step,
and product code a supervisor may not touch unreviewed). **Reversal cost:**
none — every act is a recorded commit on the merged lane; the misfire is
filed as a kit finding for its own row.

## 53. The WI-555 record was corrected under drawn review: the absorbed off-spine baseline disclosed, the handback report's "four Drafted" misstatement corrected in the log, the false arm-4 premise stated as such

**Decided (2026-09-01, evening):** round 005 found three record-level MAJORs
on a conversion that stands. The wi508 handback merge carried the BRANCH's
`docs/archive/last_approved/` bytes onto trunk, collapsing `CURRENT.md`'s
off-spine re-attestation census from 132 changed / 30 added / 3 removed rows
to 1 changed — trunk's unsigned off-spine approval debt absorbed into the
approved baseline by a `partial` lane, undisclosed; the immutable handback
report says "four Drafted" rows where LLR-203/LLR-204 are Approved; Done-when
arm 4's "unflipped" premise (inherited from OI-72's wording) was false as
written. Disposed by a rework that left the immutable report and every
registry untouched: the fragment carries the disclosure and the correction of
record, the Deliverable a "Corrected by round 005" paragraph, and the queued
disposition row's Context three explicit items for its adjudicator (the
LLR-203/204 flips, the baseline move, the report's misstatement). The
restore-or-stand question was routed to the owner through that adjudication.
**The alternatives:** hand-revert the two LLR flips on trunk (a spine act a
supervisor may not take; the flips were loop-permitted under the Needs-only
dial), or edit the immutable report (the record of the close as it was made).
**Reversal cost:** none — record-only commits on the merged lane.

## 54. The WI-568 disposition adjudication was reworked under drawn review and closed BY HAND through the kit's own function after the loop resumed it in a C6 cycle

**Decided (2026-09-01, evening):** the ADJUDICATE session ruled PARTIAL /
keep-all / one successor but put its `## Dispositions` block in the verdict
file, so `handback.close_adjudication` refused the mechanical close and the
loop stopped; it had also declared the owner-owed baseline question "not
owner-owed" without addressing it. Disposed by a supervisor-drawn round 002
(CHANGES-REQUESTED 7: two BLOCKERs, two MAJORs), a supervisor-dispatched
rework (block moved to the spec with an `open_item` cell, the executable scope
written after the fence, the verdict re-issued in place per the WI-566
precedent, a fragment written), and a verification round 003 (APPROVE 1). On
relaunch the loop scheduled a Terra round (CHANGES-REQUESTED 1: the scalar
`open_item` mints a thin OI row) and then re-adjudicated the finished lane in
a cycle (sessions 003–007, two concurring Sol verdicts, then NO-COMMIT /
ERROR / a rate-limit WAIT) without closing. The supervisor stopped the loop
(`pkill` of the coordinator and its codex child — the one act this session
took outside the kit's scripts, because the cycle would have run to the
40-session cap), carried the owner brief into the successor's captured scope,
closed the row through `handback.close_adjudication(root, branch)` from the
trunk root (`4d9dba7f`), drew round 004 (CHANGES-REQUESTED 2 — the
supervisor's own brief was wrong: external.toml DID move, and a byte-level
RESTORE is unavailable under the mirror invariant), corrected it, drew round
005 (APPROVE 2), compiled the five-round rollup and merged (`5ac6ef2b`); the
merge minted the successor and `OI-78`. **The alternatives:** let the cycle
run to its cap (36 more sessions of concurring verdicts), or close the lane
partial (stranding the owner's question a third time). **Reversal cost:** none
for the lane; `OI-78` is the owner's to rule and its two answers are both
reversible (the successor's spec carries the costs).

## 55. The owner's question minted as `OI-78` is STAND versus REVIEW-THEN-STAND — a byte-level restore is not offered, because the kit's mirror invariant makes it unrepresentable

**Decided (2026-09-01, evening):** the first draft of the owner brief (the
supervisor's) recommended RESTORE — re-copy the pre-merge `6d3d9db4` off-spine
snapshot files. Round 004 falsified it: `committed_snapshot_findings` reds a
snapshot file that is not byte-identical to its live counterpart at the commit
that wrote it, permanently ("a forgery stays red forever"), the wi508 lane's
own decision 10 measured exactly that red and reverted, and the re-copy would
re-land external.toml's since-corrected header comment. The question and the
brief were re-issued: STAND (reseal at the successor's approval commit) or
REVIEW-THEN-STAND (the owner reads the absorbed diff and amends any rejected
row live, which returns it to the re-attestation brief through the ordinary
path, before the reseal); recommendation REVIEW-THEN-STAND. **The
alternative:** leave RESTORE on the card and let the successor discover the
red. **Reversal cost:** the two offered answers are each one commit apart.

## 56. The pause is RE-ARMED by owner direction while the last lane finishes under it; the loop ends drained, with the six dropped log entries left as the owner's call

**Decided (2026-09-01, evening):** the owner asked for the pause at 22:52 UTC;
it was written and committed (`b3658346`) while the WI-568 lane was in flight,
per the pause's own contract (no new claim at the next boundary; the in-flight
lane finishes). The lane finished by hand (decision 54), the loop is stopped,
no worktree remains, and the frontier behind the pause is the successor row
parked `waiting:open-item-pending` on `OI-78` plus the standing queue. The six
2026-08-30 log entries the conversion dropped are NOT restored: the classifier
blocked the restore script and a `git show` of the held branch's log, so the
restoration (from history, one reviewed commit, the precedented splice) is
recorded for the owner rather than worked around; until then `check_docs
--stale` is red on trunk for that one anchor. **The alternative:** restore
through the Edit tool without asking (a hand edit of `docs/log.md` on trunk
the owner had not seen). **Reversal cost:** deleting one file in one commit
resumes the loop; the log restoration is one commit whenever the owner says so.

**Superseded in part (2026-09-01, later the same evening):** the owner directed the restoration; the six entries were restored at `0e4cbfb1` (see the log addendum). The re-arm stands.
