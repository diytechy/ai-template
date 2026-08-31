## 2026-08-31 — sitting: the unpause and the first live lanes of the stall-guard machinery — WI-547, WI-549, WI-535, WI-538 merged, WI-540 closed partial and disposed; what the new rituals did and did not do

The first unattended run after the tracked pause came off: seven loop runs,
with supervisor sittings between them, merged four rows and put the C1–C7
mechanisms of the stall-guard plan
([2026-08-30-stall-guard-plan.md](../plans/2026-08-30-stall-guard-plan.md)) on
live lanes for the first time. Deliverables: four merged rows with their
compiled WI-level verdicts ([WI-547](../reviews/WI-547-REVIEW-A.md),
[WI-549](../reviews/WI-549-REVIEW-A.md),
[WI-535](../reviews/WI-535-REVIEW-A.md),
[WI-538](../reviews/WI-538-REVIEW-A.md)); WI-540 closed **partial** by the
dispatcher, its product diff quarantined to a patch and its artefact merged,
then disposed by WI-550 — PARTIAL upheld, one successor drafted to re-land that
patch at strong tier; one trunk-lane kit fix (`out/agent-loop.lock` joins the
declared unload residue, `a49b38e2`); six decisions on record (40–45 in
[decisions-for-review-2026-08-31.md](../decisions-for-review-2026-08-31.md));
and fifteen kit findings, none of them fixed, all filed below.

### What happened, in order

**Unpause and re-measure (00:28–00:31).** Box quiet at 5–9 % CPU; the smoke
tier re-measured — decision 33's owed reading — at 1426 passed / 6 skipped in
26.65 s, enforce 25.2 s vs 60 s, the budget untouched.
<!-- fig: cmd="python -m pytest -q -n auto -m smoke && python scripts/check_smoke_budget.py --mode enforce" rev=c7433820 -->
`docs/work/pause` deleted in `c7433820`; `agent-resume.cmd` launched with
`--wait-on-limit 14400`.

**Runs 1–2 — WI-547 (00:31–00:58; decisions 40–41).** Session 001 ADJUDICATE on
Opus ruled `VERDICT: CLARITY rows=17` in 96 s (`6162a342`), then exited `DONE`
reporting "review round approved" with none drawn (finding A). The resume
derived "review owed (committed evidence: built, no verdict for HEAD)" and drew
REVIEW-A on OPENAI-TERRA (`APPROVE 0`, 97 s); the next resume derived it AGAIN,
the loop's own telemetry commit (`cc424d0a`) having moved HEAD past the verdict,
and burned a second identical round (finding B); the dispatcher's trunk-unmoved
stall ended the run at exit 4 — no handback, no partial close. The supervisor
closed the row (`881b95b8`), took the verdict round last and got a MINOR on the
closure wording (SR-111/SR-112 had dropped their C-MNT-7 sentences, not just a
label), corrected `6627abe1`, compiled four rounds (`0de46d6a`). Run 2 merged it
(`efac96c4`) — then UNLOAD INCOMPLETE: the C6 shed had removed all three
`out/run-logs/` streams, proven live, but `out/agent-loop.lock`, the loop's own
coordinator lock that `release_lock` never unlinks, was not a declared residue
name (finding E). Fixed on the trunk lane in `a49b38e2` with fixture and test.
<!-- fig: cmd="python -m pytest -q -n auto -m smoke && python scripts/check_smoke_budget.py --mode enforce" rev=a49b38e2 -->

**Run 3 and the hand merge — WI-549 (01:00–01:12; decision 42).** The medium
Opus worker on the ordinary brief audited WI-548's close and closed its own row
in one 285 s session (`541fa96e`) — the C6 worker close ritual's first live
proof, so the lane could finish on its own — then exited `DONE` without a round
(finding A); the drain stopped on the absent WI-level verdict (exit 1).
Supervisor: TERRA round (`APPROVE 0`, 156 s, `f906fd75`), compiled `bcf071e1`.
Run 4's startup did not merge the finished lane — a drain runs only before an
exclusive claim or at station exit, and WI-535 had been claimed over it
(`0302c4f0`), finding F — and merging by hand, the first refresh REFUSED: the
new claim commit conflicted with the lane's earlier station refresh, which my
record commits had buried. Remedy: reset to pre-refresh `deba0489`, cherry-pick
the record commits back, let the slot redo its refresh — merged `1553f22f`,
**unloaded clean**, proving the `a49b38e2` fix on a lane holding exactly the
lock plus a stream.

**Run 4 — WI-535, seven sessions (01:06–02:16).** Two sonnet BUILD sessions
where the brief asks for one: session 001's build (`75982195`) carried no `WI:`
trailer and left the spec in `active/`, so BUILD was re-dispatched; 002 closed
it properly (`2e85725d`). Here the in-process review schedule DID fire — round 1
on TERRA, CHANGES-REQUESTED, one MAJOR: `family_context_telemetry` matched the
first `modelUsage` entry on input/output alone, so a subagent entry with equal
counts but different cache usage could be attributed as the session. The rework
routed to `[DESIGN-CHECK]` OPENAI-SOL at strong effort, which ran the worker
brief and did the rework itself (`90d8a778`, 1501 s, the
`implementer-touched-review-path` tripwire raised — finding G); the three
follow-on sonnet BUILD sessions then had nothing to do: NO-COMMIT ×3 into the C1
stall, exit 4 — and the dispatcher took the right branch, "exited 4 but its
specs are already out of `active/` … the drain merges it rather than handing
back". The drain refreshed (bar PASS 11 at `913e7bbe`) and stopped at exit 1 —
cause recorded as **not** the verdict gate but "integrate: REFUSED - the trunk
working tree is dirty": I had appended decisions 41–42 to a tracked file while
the loop ran (finding H).

**Closing WI-535 (02:22–02:31).** Post-rework round on TERRA `APPROVE 0`, 241 s
(`4d00d330`); compiled `be6cb9ef`; merged by hand through the slot (`fc26bfca`
bar PASS 11, `033cf804`), unloaded clean with eight streams plus the lock.
Decisions 41–42 committed (`60d2c830`); run 5 claimed WI-538 (`ea28176f`).

**Run 5 — WI-538, eleven sessions (02:31–04:53).** Session 001 (Opus medium,
1424 s) landed Context and the fragment (`f7e3ac40`, no trailer); 002 built the
armed `[step:complexity]` gate and re-based the module ratchet to SLOC
(`63fe83f6`, also no trailer); 003 and 004 were NO-COMMIT — each launched the
full suite in the BACKGROUND and ended its turn, and the harness killed the run
with it (finding J); 005 closed the row with the trailer (`7fe441ee`), one
no-commit session short of the C1 stall. Then three rounds, each with a rework:
a MINOR on a ratchet/sensor docstring; a MAJOR on LLR-206's stale Detail plus
baseline tabs; then `escalate: swap-implementer — 2 consecutive failed review
gates` moved BUILD to OPENAI-TERRA, whose session committed the fix
(`e26ab033`) **and** a file named like a round (`010-REVIEW-A-e26ab03.md`,
"re-review approval" — finding K, `189490e4`), after which the cross-family
round on Opus returned APPROVE with one MINOR. The drain then refreshed RED on
approval-fresh: the LLR-206 amendment had staled `docs/ratify/CURRENT.md`, which
the brief names only for minted or re-statused rows (finding L). Exit 1.

**Finishing WI-538 (04:53–05:26).** The supervisor regenerated the brief
(`f1d0fd67`), then took the verdict rounds last: a MAJOR on the baseline
re-stamp raising two cognitive ceilings against the downward-only contract —
kept and reasoned rather than restored, the decomposition left to WI-545
(`3275b371`, decision 43); a MINOR on blank-reason rows still carrying a
terminal tab, 178 of them in the pre-change five-field form (`4288c3fa`); then
`APPROVE 0` (012-REVIEW-A-4288c3f, 212 s). Compiled from the six genuine rounds
with the implementer's file excluded and the exclusion stated inside
(`b37df3b4`); merged `3933bb11` after bar PASS 11 at `0512de54` — the armed
complexity step ran inside it — unloaded clean (the third). Decisions 43–44
committed `3d048f04`.

**Run 6 — WI-540, eleven sessions, closed partial (05:13–08:05).** The strong
Opus worker shipped the adjudicator session-retention layer inert at dial 0 in
one forty-minute session (`df5a2863`, IF-174 minted, `WI:` trailer present) but
did not close the row. Round 1 on TERRA: CHANGES-REQUESTED, three MAJOR and
three MINOR, with the `implementer-touched-review-path` tripwire — whose
page-human escalation re-armed DESIGN-CHECK rather than stopping the run. That
design-check on OPENAI-SOL hit the OpenAI usage limit mid-session (ERROR,
1947 s, reset 08:40 UTC), and **the C4 probe fired live for the first time**:
`probe [OPENAI-SOL]: unreachable, cooled ~900s` — no session burned. The
re-route to OPENCODE-KIMI committed a rework addressing all six findings
(`223cd88a`), ran the full suite foreground, went silent, and **the C3 idle
deadline killed it at 900 s** — the second live C3 proof. Sessions 005–007 each
verified the rework, ran the full suite, and lost it to the harness's ten-minute
cap pushing the run into the background: NO-COMMIT ×3 → the C1 stall → a partial
close of work whose own Deliverable read complete (`a83418f5`, `d3fadb42`,
handback written) — findings J and M. The §A3 quarantine reverted the lane to a
bar-inert artefact (`ee13eb37`, the 3876-line diff saved under
`docs/work/handback/`) but took `docs/id-watermark` down with it, IF 174 → 173,
and a mark only rises: registry-integrity red on the reverted tree,
approval-fresh beside it (finding N), run 6 exit 1. Supervisor repair
`10f789ff`; merged `9bb80db9` as `WI-540=partial` (bar PASS 11 at `3241f790`);
intake minted the disposition row WI-550 (`61293c6d`). The unload was held by
worker scratch files under `out/` (foreign names, refused correctly) plus a
lane-side `out/integrate.lock`; unloaded by hand.

**Run 7 — WI-550, the disposition (07:52 onward).** The medium Opus adjudicator
ruled in 364 s: `OUTCOME: PARTIAL successors=1` — the partial upheld, the
handback report judged to undersell reviewed progress, the DESIGN-CHECK gate
named as the proximate blocker, one strong-tier successor drafted to re-land the
patch (IF-174 is burned, so it re-lands from the saved diff). **The adjudicator
closed its own row** (`9aa2158b`) — the disposition brief's C6 ritual, live —
then exited `DONE` with no round drawn (finding A once more). The drain went red
on approval-fresh although the lane touched no registry: the brief's provenance
line is read from history, so the copy regenerated on the WI-540 lane read stale
on trunk after its merge (finding O); fixed by a trunk-lane regen (`ada265fd`).
The verdict rounds were the supervisor's, and they met both outage classes at
once: OPENAI-TERRA answered its usage limit in 4 s; OPENCODE-GROK went silent
and the helper's own idle deadline cut it at 902 s with no verdict (a first
attempt had already died with this session's ten-minute tool cap). That is the
C5 case by the owner's direction — an independent Opus reviewer, heterogeneity
relaxed and RECORDED: ANTHROPIC-OPUS-STRONG returned `APPROVE findings=1` (285 s;
the successor draft's prose sat before its toml block, so
`intake.parse_dispositions` minted `scope=''` — confirmed with the parser and
corrected in `e8e49cda`) and, on the correction, `APPROVE findings=0` (330 s).
Compiled with the relaxed heterogeneity and its reason stated inside
(`40363d32`); refresh onto `ada265fd` bar PASS 11 at `6493d80f`; merged
`7e44e155`, **unloaded clean (the fourth)**; intake minted the successor
**WI-551** (`250b663c`) with the rationale in its Context. Decisions 45–46 and
the re-armed pause landed together (`8e94ca33`); the loop was not relaunched.

### What the new machinery did on its first live lanes

- **C1 route-aware stall** — HELD. No partial close on a reviewer or no-op
  session; where a build stall did close a lane partial (WI-540) the work was
  genuinely uncommitted. Runs 1 and 4 ended on the *dispatcher-level* stall,
  which ends the run, not the lane.
- **C2 review-owed** — fired constantly, but only as the resume derivation:
  never exit 9, never an `out/review-owed` marker. It re-owes on the loop's own
  telemetry commits (finding B).
- **C3 idle deadline** — fired live once: OPENCODE-KIMI went silent after its
  full-suite run and was killed at 900 s (TIMEOUT), its uncommitted fragment
  edit lost. Exactly what it is for.
- **C4 probe** — printed once, and only where designed: `probe [OPENAI-SOL]:
  unreachable, cooled ~900s` after that route ERRORed on the usage limit. Every
  other route had a clean history, so no probe was drawn.
- **C5 relaxed same-family rung** — never drawn by the loop (no lane reached a
  review draw while both other families were down); exercised by hand on WI-550
  and recorded in its compiled verdict.
- **C6 worker close ritual** — the Opus WI-549 worker closed in one session, the
  sonnet WI-535 worker in its second, the Opus WI-538 worker in its fifth, and
  the strong Opus WI-540 worker never. It is NOT in the amendment brief, so
  WI-547 was closed by the supervisor (finding C).
- **C6 disposition close** — fired for WI-550: the adjudicator ruled and closed
  its own row in the same session.
- **C6 unload shed** — four clean unloads (WI-549, WI-535, WI-538, WI-550) once
  the lock joined the declared set; one held by WI-540's worker scratch files
  plus a lane-side `out/integrate.lock`, unloaded by hand.
- **C7 brief slots** — rendered fine; rounds ran 80–1089 s wall.
  <!-- fig: cmd="agent_loop session lines (`session NNN: … wall=`) and review_once.py's `exit … wall` print" rev=ada265fd -->
- **Escalation ladder** — both upper rungs observed: the implementer swap after
  two consecutive failed review gates (WI-538, BUILD off Opus to TERRA), and
  page-human on a fired tripwire re-arming DESIGN-CHECK rather than stopping the
  run (WI-540).

### Kit findings for the owner

- **A.** The in-process review schedule does not fire after an ADJUDICATE
  session (WI-547, WI-549, WI-550 all exited `DONE` with none drawn); it does
  fire after a BUILD session.
- **B.** C2's "no verdict for HEAD" compares against the raw branch tip, so the
  loop's own telemetry commits re-owe a round on every resume of an
  approved-but-unclosed lane. It should peel record commits as the slot does.
- **C.** Only the disposition brief got the C6 close step; the amendment,
  conflict and red-TC briefs did not, so those lanes cannot finish on their own.
- **D.** The dispatcher-level stall ends the RUN (exit 4), not the lane; with one
  lane in flight that is the only bound on B.
- **E.** `out/agent-loop.lock` was missing from the declared unload residue —
  fixed on trunk (decision 40); `out/integrate.lock` is the same class, still
  undeclared.
- **F.** A lane finishing between runs waits for the next exclusive claim or
  station exit; by design, but the trunk then moves under its old refresh commit.
- **G.** DESIGN-CHECK runs the worker brief and does the rework itself, so the
  follow-on BUILD sessions have nothing to do, the stall budget burns, and the
  rework commit reaches the drain unreviewed.
- **H.** Supervisor error: never touch a tracked trunk file while the loop runs —
  it dirtied the trunk and became the recorded cause of a run stop.
- **I.** A later lane amended a TERMINAL spec (`partial/WI-521`, +12 lines) and
  nothing refused it; a closed partial is meant to be a byte-identical record.
- **J.** The full suite (~12 min) exceeds the worker tool's ten-minute foreground
  cap, so a worker backgrounds it and is killed with its turn: NO-COMMIT. Three
  such sessions are the C1 stall — two lost on WI-538, a partial close on
  WI-540. The brief must direct a bounded/batched form.
- **K.** An implementer wrote a `NNN-REVIEW-A-<sha>.md` file under the review
  path; the scoreboard's tripwire did not name it on the following round.
- **L.** An AMENDMENT of an `Approved` cell also stales the approval brief, but
  the brief names the regeneration only for minted or re-statused rows.
- **M.** A no-commit stall on work that is built, trailered and believed complete
  still closes the row partial — the D6 class, open.
- **N.** Kit defect: the §A3 bar-inert revert takes `docs/id-watermark` back down
  (IF 174 → 173), but a mark only rises — the reverted lane can never pass
  registry-integrity. A minted id is burned; the revert must leave it alone.
- **O.** The approval brief's provenance line is history-dependent: regenerated
  on a lane it reads current there and stale on trunk after the merge, so the
  NEXT lane's refresh reds with no registry change of its own.

**Figures.** Smoke tier across this sitting's supervisor commits: 1426 passed,
6 skipped in 26.65 s (enforce 25.2 s) at the unpause; 24.88 / 25.1 s at
`a49b38e2`; 25.93 / 27.5 s at `60d2c830`; 22.97 / 28.2 s at `3d048f04`;
25.79 / 22.5 s at `ada265fd` — all inside the 60 s budget, and every lane bar
was PASS 11/11 at its in-slot refresh.
<!-- fig: cmd="python -m pytest -q -n auto -m smoke && python scripts/check_smoke_budget.py --mode enforce" rev=ada265fd -->
The full unfiltered suite on the drained trunk at `ada265fd`: **3192 passed,
15 skipped in 643.91 s** (0:10:43), exit 0, on a quiet box.
<!-- fig: cmd="python -m pytest -q -n auto" rev=ada265fd -->
(OPENCODE-KIMI's in-lane reading on WI-540 was 3163 passed, 86 skipped, 3 failed
in 708 s — the sibling-import red its own rework then fixed.)
One transient: the budget step of the pause commit `8e94ca33` read 93.0 s OVER
while its own tier had just run in 28.04 s; re-measured a minute later on a 7 %
box at 23.3 s within. Recorded, not acted on — one machine is one data point
and the budget is not moved to fit a busy moment.
<!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=8e94ca33 -->

Deferred open items: none — everything owed the owner is in
[decisions-for-review-2026-08-31.md](../decisions-for-review-2026-08-31.md)
(decisions 40–46 and the findings list) and the RESUME HERE block of
[status.md](../status.md).
