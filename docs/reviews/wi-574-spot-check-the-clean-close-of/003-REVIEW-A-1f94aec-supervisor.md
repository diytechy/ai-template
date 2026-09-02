### REVIEW-A — WI-574 — Round 003 — 2026-09-02 — supervisor-drawn (independent Opus, hostile brief)

Read-only round on `wi-574-spot-check-the-clean-close-of` at HEAD `7a0ab852`
(work tip `1f94aec8`, then telemetry `74fd19c9` and the station refresh onto
trunk `f1212214`). Interpreter `/Users/diytechy/Documents/ai-template/.venv/bin/python`;
this worktree has no `.venv` and none was created. No file outside this round
file was written; no commit, no state-changing git.

The verdict under review is not the WI-572 close — that stands and is not
reopenable here — but WI-574's own act: *is the spot-check's reading true, are
its findings real, and are its two successors executable?*

## What I verified

**Where the verdict lives.** `docs/reviews/wi-574-…/` did not exist before this
file. That is correct, not a gap: the spot-check's verdict belongs in the row's
own `## Deliverable`, and both prior sample spot-checks (WI-549, WI-563) did
exactly that — their `docs/reviews/` directories hold only supervisor-drawn
REVIEW-A rounds like this one. There is no `adjudicate-spot-check` template to
point elsewhere.

**Done-when 1 — lanes cannot approve — DRIVEN, not read.** I built the
`_spine_lane` scaffold and called the shipped rung directly:

- worker lane, `Drafted` → `Approved` on `SR-001`:
  `integrate._approval_act_refusal(root, "wi-401")` returns a refusal opening
  *"wi-401 performs an APPROVAL ACT in its own delta - and the approval act is
  the ADJUDICATOR's, on the serial trunk side, never a work lane's (owner ruling
  2026-09-01; PROCESS.md §4)"*, naming the four spine registries and the
  snapshot directory.
- the same lane minus the flip: returns `None`. So the rung keys on the act, not
  on touching the spine.
- `acceptance_record.APPROVAL_ACT_CSVS` (:144) is `SPINE_CSVS + stakeholder-needs`
  — four tiers, SN included, as the Deliverable claims; `OUTSIDE_THE_APPROVAL_ACT`
  (:165) names the three off-spine registries with the
  `SNAPSHOTTED == APPROVAL_ACT_CSVS + OUTSIDE_THE_APPROVAL_ACT` invariant stated
  in the comment above it.

**Done-when 2 — the first-approval arm, dial-filtered — DRIVEN.** On the same
scaffold, with the merge delta authoring one `Drafted` `SR-001`, I moved the
dial and re-asked:

- `human_approval_through = "DevStg-Needs"` (this repo's live value):
  `human_approves_spine(docs, "docs/requirements/system-requirements")` → `False`
  (released); `intake._first_approval_drafts` → **exactly one** draft,
  `brief = "first-approval"`, `kind = "adjudication"`,
  `adjudicates = ["SR-001"]`, titled *"…await a FIRST APPROVAL; read the whole
  chain, then approve (flip + snapshot) or return with findings"*.
- `human_approval_through = "DevStg-Reqs"` (SR now held): predicate `True`,
  drafts **0**. A held rung mints nothing, as the plan requires.
- The predicate really is single-sourced: `SPINE_APPROVAL_RUNGS`
  (`agent_common.py:809`) has exactly three rows, `human_approves_spine` (:895)
  fails an unmapped registry to HELD, and its only two callers are
  `intake.py:768` (the mint) and `adjudicate_brief.py:517` (the composition).

**Done-when 3 — the stale line.** The prompt BODY of
`adjudicate-amendment.template.md` no longer says the flip is the mechanical
tool's; it states both branches of the MEANING aftermath (released rung →
this session re-anchors with `intake.py snapshot --approves`; held rung → stop
at the verdict, the owner signs), with `{aftermath}` bound at :86 and
`adjudicate_brief._aftermath` at :522. The phrase survives only at :30, inside
the authoring comment, quoted as history to explain why the aftermath is stated
— which is the right place for it, not a leftover.

**Done-when 4, 5, 6 — checked by me, since the record does not.** All three
hold on the merged tree: PROCESS.md §4:421 states the doctrine and links
PROCESS_OPTIONS.md's `### Who performs the approval act` (:427); OI-45 (b)
carries the *NARROWED BY A LATER RULING (owner, 2026-09-01)* sentence;
`gate-advance/SKILL.md` (:101-119) and `spine-authoring/SKILL.md` (:352) both
say who performs the flip; `worker.template.md` has no "re-statused" clause left;
the merge-slot and mint tests exist in `test_integrate_admission.py` /
`test_intake.py` / `test_acceptance_record.py` in the modules' style; and the
compiled WI-572 fragment carries the flip census (1 worker-lane flip, 4
born-`Approved` lanes, `fd86e47f`) with its `fig:` provenance.

**Both findings are real.** `tests/test_derive_stage.py:528`
(`test_this_repo_s_committed_stage_is_current`) asserts the `docs/stage`
fingerprint unconditionally with no branch awareness, while `check.py`'s
counterpart carries the §5.2 work-branch stand-down (`_claimed_work_branch`,
:1882; the stand-down block at :1504-1537). And `trace.py` contains **zero**
occurrences of `human_approves_spine`, so the owner-facing `--approve modified`
population is unfiltered by the dial the adjudication ends now honour. Neither
follow-on appears in any of the eight `docs/work/` folders or in
`docs/requirements/open-items.toml` (the single grep hit is an unrelated
`wi-540` handback patch), and no pending OI asks the narrowing question.

**The two successors parse and are executable.**
`intake.parse_dispositions` returns **two** drafts, no refusal; the first
`kind = "ordinary"` with `buildtier = "quick"`, the second carrying the
`open_item` cell that makes `_inject_open_item` mint a `pending` OI and park the
successor under OI-73 exit (B). Both scopes name a file, a symbol and an
explicit NOT-IN-SCOPE; the first even names the falsifier that matters (still
RED on trunk with a stale `docs/stage`), which is the half a lazy exemption
would drop. Neither instructs any lane to flip a `Status` or to write
`docs/archive/last_approved/` — the second explicitly routes through the
existing `human_approves_spine` rather than a third rung table. Non-duplicative:
WI-575 is the LLR-158 cell correction, WI-570 the typed OI brief, WI-569 the
WI-508 reseal, WI-560 verdict freshness; the two WI-572 rollup MINORs
(a byte-stamp crediting a NO-COMMIT session, an SN test comment claiming an
undriven case) are a different subject. The second is genuinely the owner's —
it changes what a sitting shows — and correctly carries an `open_item` rather
than being ruled here.

**The correction at `1f94aec8` is true.** The overstatement was the "Not a
finding" paragraph calling four `test_wi_convert.py` guards "green" at `e2a8dfcb`
when they had SKIPPED. The four are `:349`, `:362`, `:407`, `:538` — all
`live_csv` consumers whose fixture skips on *"live registry has in-flight claims
… a drained-stop operation"* (`tests/test_wi_convert.py:84-95`), and this row's
own `active/` claim was the in-flight claim. At the tip that claim is drained:
`pytest -q tests/test_wi_convert.py -rs` → **21 passed, 0 skipped**. The
conclusion survives on better evidence, and the correction names the failure
mode rather than quietly restating the claim.

**The Bar is honest — I reproduced it at HEAD, not at the quoted rev.**
`pytest -q -n auto -m smoke` → **1463 passed, 4 skipped in 21.18s** (record:
1463/4 in 20.99s); `check_smoke_budget.py --mode enforce` → **21.3s vs 60s ->
within**, exit 0 (record: 23.9s); `gen_open_items.py --check` → *"open-items
view up to date"*; `check_docs.py --stale` → **OK - 1227 doc(s), 1590 link(s),
0 broken**. I did not re-run the ~10-minute full suite; the two tiers I did run
match the record's numbers within normal box variance.

**Lane hygiene.** `git diff --stat f1212214..HEAD` is eight paths and all of
them are record: the spec's move into `docs/archive/work/complete/`, two
`docs/iteration/` session logs, `docs/log.md`, and the three generated surfaces
(`PROJECT_STATE.html`, `docs/stage`, `docs/status.md`). No script, test,
registry, prompt or plan is touched — correct for a spot-check, whose finding is
a successor and never a fix. `Deliverable` precedes `Context`; `specref = ""`;
`docs/status.md` carries no surviving `WI-574` token; the compiled fragment's
file-level `Deferred open items:` line is present and `gen_open_items --check`
accepts it. The medium `buildtier` was not over-spent: the reading is at symbol
and line, verified at call sites, and I could not find an arm it asserted that
the tree contradicts.

## Findings

**MINOR 1 — one line citation in ~20 is wrong, in the record whose whole subject
is claims that read as verified.** The Deliverable says the snapshot half is
*"worded by its `--name-status` letter through `_SNAPSHOT_ACT` (:606)"*.
`_SNAPSHOT_ACT` is at `acceptance_record.py:573` at every revision on this lane
(`e2a8dfcb`, `1f94aec8`, `HEAD`, and base `f1212214` all agree); :606 is the
`return acts, sorted(_snapshot_acts(out)), None` line in the caller. The claim
it supports is TRUE — I read :573 and the refusal's snapshot wording is driven
above — so this is a pointer defect, not a false claim. Every other citation I
checked resolves exactly: `acceptance_record` :144/:165/:422/:511/:685,
`integrate` :1127/:2425, `intake` :748/:809/:1546/:768, `agent_common`
:809/:895, `adjudicate_brief` :517/:522, `trace` :3076/:3085,
`baseline_snapshot` :273/:300, `wi_convert` :173/:220, the template's :86.
No guard is warranted: a line-number checker over prose would fire on every
legitimate refactor. Fix it in the successor's neighbourhood or leave it —
recorded so the next reader does not lose ten minutes at :606.

**MINOR 2 — half the plan's Done-when is unevidenced, though all of it holds.**
The Deliverable verifies arms 1, 2 and 3 plus the registry bound, and says it
checked *"every arm the row's `## Context` named"* — which is literally true and
is a narrower set than the plan's six. Arms 4 (the doctrine said once, across
PROCESS.md/PROCESS_OPTIONS.md/OI-45(b)/two skills/`worker.template.md`), 5 (the
tests) and 6 (the recorded flip census) appear nowhere in the record. I checked
all three above and all three hold, so the verdict is unaffected and this is not
a missed finding — but a spot-check is read later as the statement of what was
looked at, and a reader cannot tell from this one that the doctrine arm was ever
opened. Construction-first: the remedy is a sentence in the spot-check's own
brief telling the session to enumerate the PLAN's Done-when arms and mark each
checked or not-checked — no new detector, and no mechanism that could false-fire.
Worth carrying into whichever row next touches the spot-check brief rather than
minting a third successor here.

**MINOR 3 — a quoted "real output" line is trimmed of its warning.** The Bar
quotes `check_docs --stale` as *"OK - 1227 doc(s), 1590 intra-repo link(s), 0
broken"*. The actual line at HEAD ends *"…0 broken (1 orphan warning(s))"*, and
two `possibly stale` hints precede it. The orphan is pre-existing and not this
row's; the trim is cosmetic and the exit code is unchanged. But a Bar section
whose contract is verbatim output should not silently drop the parenthetical
that says something is imperfect — that is a small instance of the same class
the row's own correction paragraph names.

**Verdict on the verdict.** "STANDS WITH FINDINGS" is right. Every arm of WI-572
that I could drive, I drove, and the shipped code does what the row asked; the
one genuine defect is the filing gap the spot-check found, and it found it by
looking where the record was silent rather than where the code was loud, which
is what a sample attestation is for. The two successors are the correct
instrument, correctly routed. None of the three findings above touches the
verdict, the successors, or the truth of the record's load-bearing claims.

VERDICT: APPROVE findings=3
