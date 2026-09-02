## 2026-09-01 — WI-572: the approval act is the adjudicator's, on trunk

**Spec of record:** `../plans/2026-09-01-approval-act-adjudicator-only.md`
(the owner's ruling, 2026-09-01, recorded in
`../log.md` from `2026-09-01-owner-ruling-approval-act.md`). Serialized behind
WI-571 (the copy-scope row); both touch `intake.py` / `baseline_snapshot.py`.

**In one line:** a worker lane may author `Drafted` spine rows and amend cell
text, but the approval act — the `Status` flip into `Approved`/`Founded` and
the `docs/archive/last_approved/` copy that anchors it — is the adjudicator's,
performed on the serial trunk side.

### The baseline this row is measured against

Every commit that moved an `"Approved"` string in a spine registry before the
ruling, classified by where it happened:

- **1 worker-lane flip** — `580df781` (WI-508 slice 6), whose next review round
  returned CHANGES-REQUESTED against exactly those flips.
- **4 lanes minted rows born `Approved`**, skipping the brief entirely —
  `8848f6fb` (WI-483), `ad2222df` (WI-500), `69e4a854` (WI-501), `0cfb2e6f`
  (WI-507).
- The rest were trunk sittings or the pre-ladder rename.

fig: 17 commits, classified by subject; `git log --format='%h|%s'
-S'"Approved"' fd86e47f -- docs/requirements/system-requirements.toml
docs/requirements/low-level-requirements.toml docs/test/test-cases.toml
docs/requirements/system-requirements.csv
docs/requirements/low-level-requirements.csv docs/test/test-cases.csv`
at `fd86e47f`.

### Deliverables

**1. A lane's merge is refused when its delta performs an approval act.**
`acceptance_record.staged_approval_acts` reports a `Status` crossing INTO
`Approved`/`Founded` and a row that arrives already claiming one;
`lane_approval_refusal` words the refusal, naming each row, its registry, the
shape of act, and every `docs/archive/last_approved/` file the branch wrote.
`integrate._approval_act_refusal` is the rung, beside `_minted_id_refusal`
whose shape it copies exactly — the merge base, and the ladder placement.

Construction-first, as the plan required: `staged_spine_amendments` already
diffs the merged commit and EXEMPTS a row whose Status moved; the new reader
reports precisely that exempted set. All three readers (plus
`staged_drafted_rows`) now share ONE two-tree walk, `_spine_row_sides`,
extracted rather than copied. Verified against the record itself: the reader
reproduces the census above exactly — four flips at `580df781`, and the
born-`Approved` rows of all four lanes.

The judgement lives in `acceptance_record`, not in the merge slot, on LLR-178's
separation: the coordinator that merges is not the reader that decides what a
spine delta did. That also kept `integrate.py`'s size bump to a new rung's
irreducible core.

**2. The first-approval adjudication arm.** If a lane may not approve what it
authored, something must. `intake._first_approval_drafts` (trigger a2) mints ONE
`brief = "first-approval"` adjudication per merge over the `Drafted` rows the
delta added or amended — the exact mirror of trigger (a), one section below it.
`APPROVAL_RUNG` names the DevStg rung each spine tier is approved into so the
dial can answer whether that tier is loop-held; a rung the dial HOLDS is not
minted (the owner approves those, through the approval brief, as today), and an
unmapped tier is held.

`prompts/adjudicate-first-approval.template.md` is the fifth adjudicator brief,
with `adjudicate_brief.first_approval_values` behind it and its own verdict
grammar (`OUTCOME: APPROVE|RETURN rows=N`). The brief renders each row's WHOLE
CHAIN, which is the owner's stated reason the act is the adjudicator's — so
`trace.reattest_model`'s `chain_of` closure became the public
`trace.spine_chain` + `chain_buckets`. The model's own `rows` list carries only
what changed or is `Drafted`: the right answer to the re-attest brief's question
and exactly the wrong one here, where the settled parent and the passing sibling
test ARE the evidence.

`integrate._adjudication_lane` exempts the actor the ruling names. The
concurrency half the owner asked for was **already built** and is not
re-implemented: an adjudication row is not `ordinary`, so
`dispatch._branch_exclusive` already runs its lane alone. The ruling is what
points the act at that guarantee.

**3. The amendment arm's aftermath is stated and true.** The template's closing
"the flip, if one is owed, is the mechanical tool's act, not yours" went false
when OI-45 (b) retired that tool, so a MEANING verdict on a loop-held rung ended
at a brief nobody was owed. Replaced by a DERIVED `{aftermath}` slot
(`adjudicate_brief._aftermath`), which reads the declared gate authority for the
tiers actually shown and tells the session whether the re-attestation is its own
act or the owner's — rather than leaving it to read and interpret a dial
mid-verdict. `prompts/CATALOG.md` regenerated.

**4. The doctrine says it once.** PROCESS.md §4 gains one clause in its fixed
points and links to PROCESS_OPTIONS.md "Who performs the approval act" (the
ruling, its two reasons, the division-of-labour table the owner asked for in
§2a, and the three holding mechanisms). OI-45 (b) gains the narrowing sentence.
`gate-advance` names the acceptor its procedure was already addressed to;
`spine-authoring` opens with "authoring is not approving"; `worker.template.md`
gains the NEVER clause and its close ritual now says "minted or amended". The
two reference surfaces follow the mechanism they describe:
`docs/enforcement-audit.md` gains the rule's row (with its three-fold honest
residue), and `docs/registry-machinery-reference.md` records the other half of
the amendment walk, plus the narrowing on the `Founded` row's OI-45 citation.

**5. Tests**, all in the modules' existing style: five at the merge slot, four
at the reader, three at the trigger, five at the brief.

### Deviations from the plan

- **The refusal points at PROCESS.md §4, not at the plan.** The plan's
  done-when 1 says the refusal "points at this plan". It is shipped kit code:
  a downstream repo has no `docs/plans/2026-09-01-...`, and CLAUDE.md's
  copy-ready rule refuses a token that cites a record the adopter can never
  read. PROCESS.md §4 ships, and now carries the ruling.
- **The adjudication runs as an exclusive claimed lane, not as a bare
  trunk-side session.** The plan says "on the serial trunk side as an exclusive
  lane". Read literally as "commits directly on trunk", that would be a new
  execution mode; read against this repo's vocabulary, an adjudication row is
  already claimed, already runs alone (`dispatch._branch_exclusive`), and
  already merges through the serial fail-closed queue. So the ruling's
  substance — a work lane never approves, only an adjudication does, and two
  acts cannot overlap — is delivered by exempting the adjudication lane rather
  than by building a second path.
- **A bare withdrawal mints nothing.** A row moved `Approved` -> `Drafted` with
  no text change is not carried to the first-approval trigger: the lane's
  recorded call already answers it, and minting there would ask an adjudicator
  to undo a deliberate withdrawal. A withdrawn row whose text then moves DOES
  reach the surface; both halves are pinned.
- **One correction outside the row's own scope.** PROCESS.md §4's snapshot
  sentence still said the copy is "replaced wholesale at each approval", which
  WI-571 made false. It is the sentence this row was editing, so leaving a
  known-false clause in place was worse than the one-clause fix.

### Ratchets re-stamped (each with its reason, in the commit that earned it)

`integrate.py` 1,270 -> 1,298 (two stamps: the rung, then its exemption);
`intake.py` 1,179 -> 1,255 (trigger a2); `bootstrap.py` 1,652 -> 1,657 (the
MAPPING row); `trace.py:reattest_model` complexity DOWN 19 -> 13, recorded in
the same commit as the extraction that earned it. Byte-watched:
`PROCESS.md` 87,871 -> 88,355, `PROCESS_OPTIONS.md` 181,369 -> 185,060, and
byte-budget-guard's own row to 4,906 (cap 5,000).

### Not done here

The plan's §2a table row "Surfaces to the owner" says rows above the threshold
do NOT surface to the owner. That is the *consequence* of this row, not a
separate surface change: `trace.py --approve modified` still renders every
`Drafted` chain, held or released. Narrowing the owner's brief to the held rungs
alone is a real follow-on and is deliberately not taken here — it would change
what the owner sees at a sitting, which is the owner's call, not a side effect
of moving who acts.

The plan's §2a consequence — that the six MEANING rows of the WI-566 amendment
adjudication are this arm's first re-attestation case — is a trunk-side act on a
future adjudication, not something this lane may perform.

Deferred open items: none — the ruling this row executes is already recorded,
and the owner-brief narrowing above is named here as a candidate follow-on
rather than a decision owed back.
