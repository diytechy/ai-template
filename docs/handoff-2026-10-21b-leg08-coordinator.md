# Handoff 2026-10-21b (headless leg 08): WI-940 landed; WI-963 holds for the owner; WI-957 through round 1

It replaces [handoff-2026-10-21a-leg07-coordinator.md](handoff-2026-10-21a-leg07-coordinator.md)
as the resume map. Procedure lives in the `coordinator-cycle` skill and its
recipes; this handoff holds state only. Headless leg 08 (loop session
`20261021T045653Z-213020`) landed WI-940. WI-963 went to the owner as
OI-115 (placeholder WI-967). WI-957 was rebased, attested and taken through
counted round 1. It carries no `Overnight: stop` line: WI-957 and WI-953
move without the owner.

## State (trunk `refactor_again`, nothing pushed)

- **Trunk:** OI-115 and WI-967 filed (`072b5723d`; coordinator-2026-10-21
  D-004: WI-940 may land ahead of WI-963). WI-940 landed as `638524428`:
  the bars run the budget step in warn mode, and `run.cmd audit` enforces
  `cpu-seconds` 540, `wall-seconds` 600 and `max-tests` 3140. TC-374 was
  approved (act on the lane), and the job helpers live in
  `kitlib/winjob.py` (IF-302; IF-299 to IF-301 were spent by its floor).
  The sweep minted nothing. WI-968 was filed (`92460fa4f`) and is now
  cancelled at this close-out, its premise refuted (wi-957 D-007).
  `archive/lanes` holds wi-940's tips. The full suite ran once at
  `92460fa4f`: 6885 passed, 33 skipped (912.9 s).
- **Lane `wi-963`** (tip `0ae2c5b60`, base `1ca1caf75`): **holds for the
  owner (OI-115, wi-963 D-011, high risk).**
  - Done so far: the checkpoint sitting 003-ADJUDICATE-9f9b2a8 (accepted);
    the gate (004-REVIEW-A APPROVE, 005-REVIEW-B one MAJOR); dispute
    007-ADJUDICATE-1ae50f4 ruled F1 FIX.
  - The fix1 build is kept as the patch `l8-963-fix1.patch` under the
    scratch root. It applies at `1ae50f4ff` and closes F1 only on unsquashed
    ranges; the fix2 probe is in `fix2-963/`.
  - After the owner rules OI-115: build the routed fix, then re-sit the
    whole set. Before the act, rebase onto WI-940's landing; since WI-940
    landed first, WI-963 re-runs its affected steps over it.
  - The act owed is sitting 003's (never taken).
  - Terra's session: `01a15d9f-feac-7d32-9bb7-6df04e41266b`.
- **Lane `wi-957`** (tip `9a98e067c`, base `638524428`, attested at
  `c033a9890`): counted round 1 filed (001-REVIEW-A 1 MINOR, 002-REVIEW-B
  APPROVE 3 MINOR). **Next**, per D-008's triage:
  - a pre-checkpoint builder stage that tightens three test assertions,
    each confirmed by its mutant;
  - Terra's reconcile (IF-175's data length; SR-241's "only review-record
    changes" wording);
  - the closure check, then one combined sitting (SR-241, LLR-341, TC-371,
    TC-372 first approvals);
  - the convergence map, a re-attestation of the new tip, the gate, the act
    turn and the landing.
  - Every review render needs an attested tip. Attest from the primary:
    `integrate.py --root "$REPO" attest --branch wi-957 --bar review --tests <its four modules>`.
- **Watermark** on trunk: WI 968, SR 240, LLR 340, IF 302, TC 374, OI 115;
  acts to seq 145 (TC-374's).
  - Lane-held ids: wi-957 holds SR-241, LLR-341, TC-371 and TC-372; wi-963
    holds LLR-342 and TC-373.
  - The next lane's Terra floor: SR-242, LLR-343, TC-375, IF-303.
- **Strict lints:** clean on trunk and in both lanes. **No judgement is
  active**; `docs/work/pause` is tracked and unchanged.
- **Scratch:** `C:/Projects/ai-template.wt/review-tmp/2026-10-21-leg07/`
  (leg 08's files are prefixed `l8-`). Keep it until WI-963 and WI-957
  land.

## How to run reviews now

As the `coordinator-cycle` skill and its recipes say: two full-lane
reviewers per round, Codex Sol at medium (REVIEW-A) and Claude Opus at high
(REVIEW-B, launched with the Agent tool's `effort: "high"`), each given
only its rendered brief.

## The queue

The owner's order (coordinator-2026-10-16 D-004, D-006; coordinator-2026-10-17
D-002, D-008), turned toward headless runs (coordinator-2026-10-18 D-004,
D-006), with the owner's 2026-10-20 rulings (coordinator-2026-10-20 D-008 to
D-019) and coordinator-2026-10-21 D-004. Each row that changes machinery
lands alone, after the cycle has run through the last landing's changed
steps (WI-940's warn-mode bars ran through WI-957's attestation and round
1 this leg).

**Only the rows in this table are claimed**, in order and under their
`needs`. When no row in it can move without the owner, the leg closes out
with the `Overnight: stop` line.

| # | Row | Next |
|---|---|---|
| 1 | WI-957 | In its lane: the pre-checkpoint stage, the reconcile, the sitting, the gate, the landing (D-008's triage). Touches the review render; lands alone |
| 2 | WI-953 | WI-902's disposition sitting on the owner's route (D-008): compose the `disposition` brief, append the row's `## Owner route` section verbatim, chained with `&&` (recipes section 1, Adjudication step 1), and check that the brief carries it. Then the successor it drafts: the third plan revision, one confirming critique and the build, before P4 and P5. It needs a claim: one scoped unpause |
| 3 | WI-963 | Held: OI-115 (the owner). After the ruling, see State |
| 4 | WI-958 | After WI-957 lands (hard edge) |
| 5 | WI-960, then WI-961 | Cleared for a claim; built after WI-957 lands (WI-960's soft edge: the same review steps) |
| 6 | WI-850, WI-851, WI-856, WI-878, WI-910, WI-920 | Under their `needs`, each scope-critiqued at its claim (WI-910 as split by D-019) |
| 7 | Filings P3 to P6, P8 | P3 ends in an owner act. P4 and P5 come after WI-953's successor lands; P5's spec asks D-009's question (does the WI space ride the carrier?) and folds in WI-810's "sequential sittings never collide on an id". P6 starts with the W3 dry run. P8 waits on its filing calls |
| 8 | WI-966 | Scope critique and its confirming round, then the claim; it lands before item 10 step 5 |

**Never claimed by a leg:** WI-684 (waits on OI-98, the owner's re-sync),
WI-795 (OI-105, then WI-820), WI-908 (the owner present), WI-964 (the
owner's Mac), WI-827 (attended only; it never lands from a lane), WI-967
(OI-115's placeholder), and every row under `docs/work/deferred/` (D-011,
D-016).

The queue runs in headless legs (the `coordinator-cycle` skill's section 7).

## For the owner

- **Rule OI-115** (WI-963's settlement fix; recommendation (a), a
  preparatory row that makes each act-ledger entry record the registries
  its act copied). It holds WI-963 at its gate tip.
- **Confirm or overrule:**
  - coordinator-2026-10-21 D-004 (high risk: WI-940 landed ahead of WI-963)
    and D-001 (high risk: `[step:smoke]` and CI's `smoke-budget` job in
    warn mode, now landed with WI-940), D-002 and D-003;
  - wi-940 D-009 (high risk: two CPU readers, `create_joined_job` and
    `job_cpu_seconds`, ship in the kit module `kitlib/winjob.py` but serve
    only this repository's step; the sitting named the placement yours or
    the coordinator's) and D-001 to D-011;
  - wi-963 D-011 (high risk) and D-001 to D-010;
  - wi-957 D-005 to D-008;
  - wi-962 D-001 to D-007.
- **Still open from the last handoff:**
  - review the deferred rows' re-scopes (D-016; WI-809 and P4 gate the
    managed loop's unpause);
  - your owner-held rows: WI-827, WI-908, WI-964, and WI-684 and WI-795
    behind their open items;
  - confirm or overrule coordinator-2026-10-20 D-012, D-013 and D-020, and
    D-001 to D-007 (high risk: D-002, D-005, D-006);
  - P8's filing calls; wi-955 D-001 to D-006; wi-956 D-001 to D-010;
  - the named-tests `--basetemp`, SR-227's wording, and the lists before
    them.
- **Push** `refactor_again` and `archive/lanes`.

## Session prompt (paste to start the next session)

```text
You are the ai-template coordinator, running ATTENDED in an interactive
session with the owner. Ask the owner at real decision points; record every
other call in docs/decisions/. Background tasks and notifications are fine
here (this is not a headless leg).

1. Take the lease FIRST, with your transcript so occupancy is readable:
   `python project-trajectory/scripts/coordinator_guard.py take --transcript "$(ls ~/.claude/projects/*/$CLAUDE_CODE_SESSION_ID.jsonl | head -1)"`.
   If the take is refused, report why and stop.
2. Read, in order: CLAUDE.md; docs/status.md; the newest handoff (the one
   status.md's RESUME HERE names), all of it; the Status and every "Owner
   rulings" section of docs/plans/2026-10-11-review-churn/README.md
   (2026-10-11 through revision 37) and its pointer-rules.md; the
   coordinator-cycle skill and its references/recipes.md;
   your memory index (review-churn-program-rulings first).
3. Run reviews the way the handoff's "How to run reviews now" says. It
   overrides the skill where they differ, until batch row B1 lands and the
   skill says the same.
4. Work the handoff's queue table in order: the "pre" trunk fix and the
   baseline manifest (M); file and
   land B1, then the plan gate G, then B2–B4 (B4 is WI-902's reshape), each
   filed on trunk with its scope critique and dispositions first; then
   continue WI-798; then P1–P9 under the dependencies their rows name; then
   re-order leg 03's rows against the plan with the owner. Claim under
   one scoped unpause per batch (a reviewed deletion commit, the claims, a
   byte-identical restore). Cut lanes from trunk's tip and land them one at a
   time. Roles: Claude Opus builds (kit-builder agent, medium); GPT Terra
   (medium) authors spine text in one retained session per lane; Codex Sol
   (medium) and Claude Opus (high) review in parallel (coordinator-2026-10-16
   D-008; the handoff's "How to run reviews now"); the independent adjudicator
   judges spine text and disputes through coordinator_adjudicate.py from the
   lane (set AGENT_CLAUDE_TOKEN_FILE to the token file's path from memory
   first; never read the file), never a sub-agent.
5. Before each landing commit: regenerate the views, run the smoke bar and its
   budget, run trace.py --strict and check_trajectory.py --strict, and read
   the summaries for failures.
6. Close out when `coordinator_guard.py status` reads 40% or more, at the
   latch, or when the owner says so (session-protocol section 4): land or
   safely commit every lane; update docs/status.md (forward-only); write a NEW
   handoff whose `## Session prompt (paste to start the next session)` block is
   this prompt, copied verbatim, keeping the `Overnight: stop` line unless the
   owner asks for headless legs; write a log fragment; fold procedural lessons
   into the coordinator-cycle skill; run the full suite once if code changed;
   commit; then `coordinator_guard.py handback --handoff <the new handoff>`.

Never: push or merge to main; rule an open item or sign an owner-held act;
leave docs/work/pause deleted; read OWNER_SCRATCHPAD.md or the adjudicator's
token file; self-review or adjudicate through a sub-agent; change ~/.claude
settings or install software; bypass a commit hook.
```
