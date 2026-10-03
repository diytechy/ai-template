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
