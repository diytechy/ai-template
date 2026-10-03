## 2026-10-03 — wave 8 (coordinator): WI-747 lands

Resumed from [the wave-7 handoff](../handoff-2026-10-03-wave7-coordinator.md). Reviews
for this wave: [reviews/2026-10-03-wave8/](../reviews/2026-10-03-wave8/).

### WI-747 lands: rubric-first observation judgement on a closed-work cadence

Sol built it at `dfe92989`. Sonnet 5.5 found it NOT YET SOUND: the `stage-gate`
re-judge trigger had no production caller
([r1](../reviews/2026-10-03-wave8/sonnet-wi747-r1.md)). The Sol
fix round made `intake.py rejudge --checkpoint` accept `stage-gate` (red 6 failed,
then green) and extracted `rejudge.checkpoint_for`. The coordinator committed it at
`d4f991a0` with two corrections:

- SR-215's requirement cell stays free of the command. The fix prompt had asked
  for it, and ruling R2 forbids a requirement cell naming a concrete artifact.
  The command lives in LLR-293.
- `checkpoint_for` is tagged LLR-254, which owns `rejudge.py`, not LLR-255, and it
  joins LLR-254's `code_symbol` inside that row's pending amendment.

Sonnet 5.5 found `d4f991a0` SOUND ([r2](../reviews/2026-10-03-wave8/sonnet-wi747-r2.md)),
with four minors:

- Three were folded in at the landing: the `_cmd_rejudge` docstring, the
  `REJUDGE_CELLS` comment, and an assertion that `merge` stays first in
  `CHECKPOINTS`.
- LLR-255 is left as is: it is incomplete about stage-gate, not false.

Landing:

- Registries were merged table by table; trunk and the lane added disjoint ids.
- The watermark was raised by `--bump-ids`.
- The lane's RESYNC entry was re-anchored at `122816da`, and its fix-round entry was
  folded in, because that entry was anchored at a lane-only sha.
- PROCESS.md: 93,016 -> 94,466 (+1,450, the WI-747 rule), re-stamped in the
  byte-budget skill (4,444 bytes, cap 5,000) and its two mirrors.

### Spine-acts batch N (WI-766, WI-767): returned; one successor drafted

An independent Claude Opus 5.5 adjudicator sat over both briefs WI-747's merge
minted. It approved nothing and re-attested nothing.

- **WI-766** (amendment), `MEANING rows=9`. SR-215 and LLR-254 read "No result is
  due immediately", inverting PROCESS.md's rule. SR-215's acceptance carried a rule
  no check observes. TC-248 dropped the release item's required-and-named check,
  and TC-247 dropped the draft-naming check. TC-036, TC-055, TC-209, TC-210 and
  TC-211 are blessable, but they could not be re-anchored while TC-248 stayed
  unblessed.
- **WI-767** (first approval), `RETURN rows=4`. LLR-293 carried intake's CLI
  entries, LLR-294 an unobservable creation rule, and TC-306 an Expected
  contradicting its Method. TC-279 was not rendered by the composer (the WI-667
  gap) and stays Drafted.

Sonnet cross-reviewed two rounds:

- [r1](../reviews/2026-10-03-wave8/sonnet-batch-n-r1.md): the drafts gave the six
  TC rows no landing path, deferred the stage-gate question in a circle, and kept
  the trace finding they cited.
- [r2](../reviews/2026-10-03-wave8/sonnet-batch-n-r2.md): TC-307 was stranded, the
  two sittings were unordered, LLR-255 was ambiguous, and the gate prompt had no
  verifier.
- The adjudicator answered each finding in new commits. The coordinator checked
  the third revision against r2's four findings.

The result is ONE successor in WI-766's Dispositions, covering every returned row
plus a required stage-gate step in the shipped gate-advance skill, pinned by a
test under TC-248. WI-767 points at it.

Coordinator commitments recorded in that draft:

- carry TC-036, TC-055, TC-209, TC-210 and TC-211 into the successor's amendment
  adjudication, and TC-307 (and TC-279, after WI-667) into its first approval;
- sit both in one combined act (batch-M style).

Any act copying the LLR or TC registry is refused until LLR-254, LLR-255 and the
drifted TC rows are re-attested. So WI-667's own adjudications wait for that
sitting, or join it.

Lesson: two Sonnet code reviews of WI-747 judged the code against its requirement
text, and neither caught the requirement text itself contradicting the rule. The
spine adjudicator did.

### WI-667 lands: assumption-only observation cases in both briefs; the checklist confirms assumptions

Sol built it as the owner's 2026-10-02 ruling narrowed it (no census arm). Red was
4 failed and 3 passed; the 3 passes assert absence and pass vacuously before the
change. Green was 7 passed. Sonnet 5.5 found it SOUND at `24cd3b91`
([review](../reviews/2026-10-03-wave8/sonnet-wi667.md)). It probed the composer's
dial, scope, Approved and dangling-DA refusals, and diffed the checklist
before and after (byte-identical except the new section).

At the commit:

- The hook refused the lane until `gen_release_checklist.main`'s baseline row was
  removed (85 -> under 15). A full `--restamp` would also have rewritten the SLOC
  column of a dozen unrelated rows, so only the named row was deleted.

At the landing, three of Sonnet's minors were folded in:

- the plan's supersession note cites WI-667 by id;
- the RESYNC entry names the prompt-catalogue regeneration;
- SR-033's rationale states its SN-043 derivation, and its `sn_refs` gains SN-043.

Follow-up: Sonnet's MAJOR, outside the grant, is that the evidence ladder (ruling
item 1) is still rendered and still required by approved rows. It is filed as its
own row.

### Batch N lands; WI-770 building; WI-771 filed; WI-697 still held

The batch-N verdict lane landed (`e4a44886`), and intake minted the drafted
successor as WI-770. Sol is building it from the draft's byte-exact cells.

WI-771 is filed by hand (the coordinator's trunk commit): drop the assumption
evidence ladder, the owner-ruled follow-up to WI-667's review. It needs WI-770 and
builds only after WI-770's combined sitting acts, since its amendments drift the
same registries.

WI-697 (TC-279's first judgement) stays held. Its brief now composes, but the
inspection procedure records TC-279's first result "once the case is approved",
and TC-279 is still Drafted. Its first approval joins the combined sitting.

That sitting, after WI-770 lands, covers:

- the amendment adjudication WI-770's merge mints;
- the first approval WI-770's merge mints, with TC-307 and TC-279 carried in;
- TC-036, TC-055, TC-209, TC-210 and TC-211 carried into the amendment;
- WI-768 (SR-033; the SR copy is blocked while SR-215 drifts);
- WI-769 (LLR-295, LLR-296, TC-308..TC-310; the LLR and TC copies are blocked
  likewise).

### WI-770 lands: the SR-215 cadence rows reworked; the gate prompts the stage-gate re-judge

Sol applied WI-766's draft. All 19 replacement cells were checked mechanically
against the spec. Red: 6 failed (the doc pin and five rubric assertions; the
fired-trigger assertion already held, so it was a coverage gap). Green: 6 passed.

The sandbox refused the `.agents` mirror, so the coordinator synced it with
`bootstrap.py --dest . --sync`.

Sonnet 5.5 found it SOUND at `719dcaeb`
([review](../reviews/2026-10-03-wave8/sonnet-wi770.md)). It checked:

- the nine protected rows are md5-identical;
- no production code changed and no Status flipped;
- the skill paragraph is placed and worded exactly as drafted;
- TC-311 is true of its test.

At the landing, the RESYNC entry was re-anchored at the parent, `00467fc7`.

Next is the combined sitting this merge's adjudications open (see the plan above).

### Spine-acts batch O (WI-768, WI-769, WI-772, WI-773): act seq 22

One independent Claude Opus 5.5 adjudicator sat over four briefs and took one
combined act. The coordinator carried two sets of rows in:

- TC-036, TC-055, TC-209, TC-210 and TC-211 into WI-772;
- TC-307 and TC-279 into WI-773.

The act:

- **Re-attested (11):** SR-215, SR-033, LLR-254, LLR-255, TC-247, TC-248, TC-036,
  TC-055, TC-209, TC-210 and TC-211.
- **Approved (7):** LLR-293, LLR-294, LLR-295, TC-307, TC-311, TC-279 and TC-308.
- **Returned (4):** TC-306 (LLR-293's refusals untested), LLR-296 (it lists every
  assumption-naming test case, where SR-033 says observation cases), TC-309
  (LLR-295's two refusals untested) and TC-310.

The snapshot used one combined ref per registry (`WI-769+WI-773`) and was not
refused. The pre-commit hook twice refused stale derived views until the
adjudicator regenerated them into the act.

Sonnet's cross-review ([r1](../reviews/2026-10-03-wave8/sonnet-batch-o-r1.md))
found the act right and every ruling sound, but blocked the draft on two points:

- Its one code change imported `assumption_rules` into `gen_release_checklist`
  across components with no declared seam (`check_trajectory --strict` ERROR,
  reproduced on a scratch copy).
- TC-055 had been re-attested while its `expected` still stated the old cadence.

The adjudicator revised the draft at `83c2f292`:

- IF-200's requestors gain `gen_release_checklist`;
- exact replacements for TC-055's `expected` and SR-215's overclaiming rationale;
- an exact TC-306 refusal test;
- dated addenda recording both misses.

The coordinator confirmed the seam fix mechanically: `check_trajectory --strict`
on a scratch copy exits 0 with the requestor edit, and ERRORs without it. That
replaced a second Sonnet round. Act seq 22 stands; TC-055's prose is corrected
through the follow-up lane, whose merge re-adjudicates it.

SN-043's need-text amendment (WI-667) is the owner's to re-attest, beside SN-003,
SN-008, SN-009 and SN-025.

### WI-774 lands: batch O's returned rows reworked; TC-055 and SR-215 corrected

Sol applied WI-773's draft. Red: 1 failed (the checklist named an automated TC as a
method). Six new tests pinned behaviour that already held, closing coverage gaps.
Sonnet 5.5 found it SOUND at `cca8c710`
([review](../reviews/2026-10-03-wave8/sonnet-wi774.md)): the cells match the draft,
IF-200 changed in `requestors` only, and `check_trajectory --strict` is clean.

### WI-697: round 1 NEEDS-JUDGEMENT; round 2's readers done; cut over

The coordinator's first draw for TC-279 counted only docstring `Implements:` parts
(423). The independent Opus judge recorded nothing, `NEEDS-JUDGEMENT`, on lane
`build/wi-697` at `53912f68`. The kit's harvest, `gen_arch_map.declaration_sites`,
finds 516 parts. The 93 missing ones were module headers, module-level blocks and
comment-linked functions.

All five round-1 statements agreed with their rows. The judge noted that
`sn_all_ids`' reader misdescribed one branch (short of B1).

Round 2 redrew with the same seed rule:

- The population is the harvest's distinct (file, enclosing symbol) pairs,
  restricted to sites naming a live spine id. One hit was a test-fixture string
  naming LLR-900/901, rows that do not exist. That rule was stated after the
  unrestricted draw surfaced the hit, and both draws are kept.
- Five fresh Sonnet readers stated each part, all with high confidence.

The statements, draws and scripts are in
`C:/Projects/ai-template.wt/wi-697-notes/` (outside the repo). The judging is
handed to the next coordinator.

### Cutover (owner, 2026-10-03)

The owner directed a new handoff: the next coordinator builds with Claude Opus at
medium effort and reviews with Codex Luna (`gpt-6-luna`) at high effort. See
[handoff-2026-10-03-wave8-coordinator.md](../handoff-2026-10-03-wave8-coordinator.md).

### Resumed under the new roles; WI-697 lands: TC-279's first result, a pass

The session resumed from the wave-8 handoff.

- `.claude/agents/kit-builder.md` now exists: Claude Opus with `effort: medium`.
  The key is confirmed in the Claude Code subagent docs.
- A fresh independent Opus judge took WI-697's round 2 and recorded a pass on the
  five sampled parts. It ruled that the coordinator's post-draw restriction was
  not B2, on a better ground than the coordinator gave: the dropped fixture string
  was never a part, it sorts last, and the next seeded draw yields the same sample.
  So a fixed skip-a-non-part rule gives this sample.
- Codex Luna (high) cross-reviewed it through `luna_review.sh`, the first real run
  of the launcher, and found it SOUND
  ([review](../reviews/2026-10-03-wave8/luna-wi697.md)). It reproduced both draws
  and the six-item sequence, and the lane was unchanged. `git worktree add` is
  blocked inside the Luna sandbox (read-only shared metadata), so Luna used
  scratch script copies instead.

Findings filed for later, not acted on:

- `_render_drill`'s trace-bar branch has no recorded reason.
- `declaration_sites` harvests `Implements:` text inside test-fixture strings.
- The procedure should state its skip rule before a draw.
- TC-279's result section is an input of TC-209, TC-210 and TC-211.

A red on trunk, introduced and fixed by the coordinator: the cutover commit
`3879545d` appended an observation-rubric index to `docs/rubrics/README.md`. That
file is a byte-copy of the template's boilerplate
(`test_dogfooded_boilerplate_matches_template`), and the commit ran only
`check_docs`, not the smoke tier, so trunk was red from `3879545d` until this
landing. The README is restored to the template's bytes. The index moves to
`docs/README.md`, whose stale "resume from the September 26 handoff" pointer now
defers to `status.md`.
