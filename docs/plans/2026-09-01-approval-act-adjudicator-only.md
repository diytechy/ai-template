# The approval act belongs to the adjudicator, on the serial trunk side: lanes author Drafted rows, a first-approval adjudication flips and snapshots them

**Status:** plan of record for the row minted against it. Authored 2026-09-01
(evening supervised session) from the owner's ruling made in session and
recorded in the log (`docs/log.d/2026-09-01-owner-ruling-approval-act.md`,
compiled), after two independent research passes over the rulings record
and the mechanism (their findings are quoted in that entry).

## 1. The ruling, and the problem it answers

**Ruled (owner, 2026-09-01):** approval acts on spine rows — the `Status`
flip `Drafted` → `Approved` (and on to `Founded`) at every rung the dial
leaves loop-held, and the `docs/archive/last_approved/` snapshot that
anchors it — are the **adjudicator's alone**, performed on the serial trunk
side, never by the worker lane that authored the rows. Two reasons, both the
owner's: **context** — the adjudicator reads the whole chain, which a single
work item does not hold; and **concurrency** — two worker lanes touching the
spine can conflict at merge, and the snapshot must not move across a
workstream, whereas a serial trunk-side act cannot conflict.

What the record said before this ruling (established 2026-09-01):

- Authority was keyed to the rung dial alone (`human_approval_through =
  "DevStg-Needs"`; PROCESS.md §4 "who accepts an advance is the repo's
  declared gate authority"), and OI-45 (b)'s sentence — "fully expected that
  an LLM session or adjudicator flips a row's Status to Approved" — was
  written with a whole-chain session in mind but reads as licensing any lane.
- Nothing mechanical refused a worker-lane flip: no hook, check or prompt
  consults the actor or the branch before a `Status` write, and the worker
  prompt anticipates one ("if this WI re-statused spine rows, regenerate the
  approval brief"). A flip in the same commit as an amendment even silences
  the amend-without-flip signal.
- History: first approvals were trunk sittings (the owner's 2026-08-24
  sitting; three trunk sessions) except one worker-lane flip (`580df781`,
  WI-508 slice 6, delegated in intent to the adjudicator, performed by the
  lane), whose next round returned CHANGES-REQUESTED against exactly those
  flips; and four lanes (WI-483, WI-500, WI-501, WI-507) minted rows born
  `Approved`, skipping the brief entirely.
- The amendment adjudicator's brief ends "the flip, if one is owed, is the
  mechanical tool's act, not yours" — but OI-45 (b) retired that tool
  (`intake._apply_flips` writes nothing, permanently), so a MEANING verdict
  today ends at the owner's brief, contradicting the "loop-held" doctrine.

## 2. What this is NOT

- Not a change to the dial or to which rungs are human-held. The owner still
  holds Needs; the adjudicator acts only on rungs the dial releases, and a
  held rung still surfaces to the owner exactly as today.
- Not a re-litigation of OI-45 (b): the mechanical writer stays retired. The
  adjudication session performs the flip as a reviewed commit on trunk; no
  hook or step regenerates a snapshot.
- Not a change to the amendment arm's MEANING/CLARITY question, only to what
  follows a MEANING verdict on a loop-held rung (the same session may
  re-approve; a held rung goes to the owner).
- Not a revert of the wi508 flips (OI-78 ruled STAND; WI-568 ruled keep).
- The copy-scope row (`docs/plans/2026-09-01-snapshot-copy-scope.md`) stays:
  scoping WHAT one act copies and moving WHERE the act happens are
  independent, and both are wanted. This row is serialized behind it because
  both touch `intake.py` / `baseline_snapshot.py`.

## 2a. Division of labour — the work lane versus the adjudicator (owner, 2026-09-01)

The owner asked for this stated plainly, because the record never did, and
the wi508 lane fell through the gap. The rule the row ships must say, in the
worker brief, the adjudicator briefs and PROCESS.md, exactly this:

| | The work lane (a WI's worker session) | The adjudicator (a trunk-side, exclusive adjudication session) |
|---|---|---|
| Authors spine rows | Yes — new SR/LLR/TC rows are written **Drafted**, with their chain links, rationale and evidence cells filled. | No. |
| Amends spine text | Yes — any cell, on any row, including Approved rows; the row's Status is left alone. | No; it may RETURN a row with findings, never rewrite it. |
| Flips Status (Drafted → Approved → Founded) | **Never.** A flip in a lane's delta refuses the merge. | Yes, on the rungs the dial releases, in its own reviewed commit on trunk, after reading the whole chain. |
| Writes `docs/archive/last_approved/` | **Never.** | Yes — the snapshot is taken in the same commit as the flip, scoped to the registries the act covers (the copy-scope row). |
| Judges a post-approval amendment | No; it records what it changed and why in its fragment. | Yes — MEANING or CLARITY; on a released rung a MEANING verdict is followed by its own re-attestation (flip + snapshot) in the same session; on a held rung the row goes to the owner's brief. |
| Surfaces to the owner | Only through the ordinary channels (a `## Dispositions` open item, a fragment's deferral). | Only what the dial holds (today: Needs) and what it cannot rule (an `open_item` it mints with a full brief). Rows above the threshold do NOT surface to the owner; the adjudicator is the approving authority for them, which is why it must hold the whole chain. |
| Concurrency | Runs in parallel with other lanes; may not hold the spine. | Exclusive on trunk; nothing else claims while it runs, so two acts cannot conflict and the snapshot moves only there. |

Consequence the owner named on reading the six MEANING rows of the WI-566
amendment adjudication (2026-09-01: "meaning appears consistent"): those
rows sit above the approval threshold, so they should not have had to wait
on the owner at all — under this plan they are the first-approval arm's
first re-attestation case, performed on trunk with the owner's read on
record, not a signature the owner owes.

## 3. Done-when

1. **Lanes cannot approve.** A worker branch's merge is REFUSED (fail-closed,
   by name) when its spine delta flips any `Status` to `Approved`/`Founded`
   or mints a row born `Approved`/`Founded`, or writes
   `docs/archive/last_approved/`. The refusal names the row ids and points
   at this plan. Construction-first: the `staged_spine_amendments` reader
   already diffs the merged commit's approved cells; the refusal reads the
   same diff, so no second detector is added. Lanes author `Drafted` rows and
   amend text; that is unchanged.
2. **A first-approval adjudication arm exists.** At a lane's merge, when the
   spine delta adds or amends `Drafted` rows on a rung the dial releases,
   intake mints ONE adjudication row (the existing trigger-(a) shape, a new
   `brief = "first-approval"`) whose brief renders the whole chain of each row
   (parent SR, sibling LLRs, the TCs, the re-attestation surface) and asks
   the one question: approve or return with findings. Its ADJUDICATE session
   runs on the serial trunk side as an exclusive lane; its APPROVE performs
   the flip and takes the snapshot (`intake.py snapshot`, scoped per the
   copy-scope row) in its own reviewed commit; a return drafts a successor
   for the authoring row's follow-up through the existing `## Dispositions`
   mechanism. Held rungs are not minted here — they surface to the owner as
   today.
3. **The amendment arm's aftermath is stated and true.** After a MEANING
   verdict on a loop-held rung, the same adjudication session re-approves
   (flip + snapshot in its reviewed commit) or returns; on a held rung the
   row goes to the owner's brief. The stale "mechanical tool's act" line in
   `adjudicate-amendment.template.md` is replaced by that statement, and
   `prompts/CATALOG.md` regenerated.
4. **The doctrine says it once.** PROCESS.md §4 (byte-budgeted: the smallest
   edit that states "the approval act is the adjudicator's, on trunk; a lane
   authors Drafted rows") with the fuller text in PROCESS_OPTIONS.md; OI-45
   (b)'s row gains one clarifying sentence naming this ruling; the
   `spine-authoring` and `gate-advance` skills say who performs the flip;
   `worker.template.md`'s "if this WI re-statused spine rows" clause is
   retired.
5. **Tests** in the modules' existing style: a lane delta with a flip is
   refused at the merge slot; a born-Approved row is refused; a Drafted-row
   delta mints exactly one first-approval adjudication with the chain in its
   brief; the adjudication's APPROVE lands the flip and a scoped snapshot on
   trunk; the amendment arm's MEANING aftermath on a released rung
   re-approves in-session.
6. **Recorded so the effect is measurable:** the fragment states the flip
   census before this row (1 worker-lane flip, 4 born-Approved lanes, from
   `git log -S'"Approved"'` on the registries at `fd86e47f`) as the baseline,
   carries `fig:` provenance on it and a file-level `Deferred open items:`
   line.

## 4. Evidence trail

The ruling entry named above; OI-45 (b) (`docs/requirements/open-items.toml`);
the 2026-08-21 owner session (dial); PROCESS.md §4; `adjudicate-amendment.template.md`;
`intake.adjudication_action` / `_apply_flips` (retired arm); the WI-508
partial spec's DELEGATED section and slice-6 entry; `580df781` and
`003-REVIEW-A-f179a0b.md` under `docs/reviews/wi508-architectural-remap/`;
the copy-scope plan.
