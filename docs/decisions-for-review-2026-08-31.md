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
