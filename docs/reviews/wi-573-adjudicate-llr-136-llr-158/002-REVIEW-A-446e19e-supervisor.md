### REVIEW-A — WI-573 — Round 002 — 2026-09-02 — supervisor-drawn (independent Opus, hostile brief)

Branch `wi-573-adjudicate-llr-136-llr-158`, base `07cbabb50a8c`, tip `446e19ea`
(station refresh over the mechanical close `02a92f22`). Read-only review: no
file but this one was written.

## What I verified

**The two MEANING rulings — both correct, independently re-derived.** I read the
WI-572 amendment (`git diff 4d0b972d..07cbabb5 -- docs/requirements/low-level-requirements.toml`)
against the tree at the tip, not against the verdict's summary of it.

- `LLR-136` `Detail`. The before text ends at the converter's write side and its
  four refusals. The after text ADDS two binding statements. Both are real
  obligations, and both are live in the tree: `wi_convert.py:513`
  `spec_paths = _kitregistry.spec_files`, consumed by `read_specs`
  (`wi_convert.py:608`, walking `spec_paths(work_dir)` at :632) — so the read
  side's population IS the write side's re-export, not a second walk; and the
  `COLUMNS` pin is asserted literally at `tests/test_wi_convert.py:671`
  (`assert tuple(wi_convert.COLUMNS) == registry.WI_COLUMNS`, with the field
  maps pinned two lines below). A converter conforming to the old text could
  carry its own read-side walk and its own unpinned column list and be correct;
  under the new text each is a defect. Obligation moved → MEANING.
- `LLR-158` `Detail`. The before text obliges ONE function (`split_changed_cells`
  and its exclusions). The after text obliges a shared two-tree walk
  (`_spine_row_sides`, `acceptance_record.py:422`), FOUR named consumers, an
  exempts-vs-reports invariant with the de-approval subtraction (:520-566), the
  single per-row judgement in `_approval_act`, and a declared registry partition.
  An implementation satisfying the old text (each reader walking the tree itself)
  fails the new one outright. MEANING, and not a close call.

**The finding that governs the aftermath — I reproduced it against the code, and
it is real.** The amended cell's final clause states *"every reader here walks
`SPINE_CSVS`, the three spine registries … the four other registries a snapshot
anchors are listed in `OUTSIDE_THE_APPROVAL_ACT`, and the two lists are pinned as
one exhaustive, disjoint statement against `baseline_snapshot.SNAPSHOTTED`."*
In the tree at `07cbabb5`:

- `staged_approval_acts` walks `APPROVAL_ACT_CSVS` — `SPINE_CSVS` PLUS
  `stakeholder-needs.toml` (`acceptance_record.py:144`, docstring at :540-541,
  call at :558) — and `lane_approval_refusal` consumes that same delta (:702).
  Two of the four readers do NOT walk `SPINE_CSVS`.
- `OUTSIDE_THE_APPROVAL_ACT` holds THREE registries (:165-169), not four.
- The pinned identity is `SNAPSHOTTED == APPROVAL_ACT_CSVS +
  OUTSIDE_THE_APPROVAL_ACT` (:162), not `SPINE_CSVS + …`. `SNAPSHOTTED` is seven
  (`baseline_snapshot.py:190-198`); 7 − 3 = 4 is exactly the arithmetic the stale
  clause preserves from before the round-028 widening.

So the cell is false on three independent counts, and the row's `code_symbol`
omits `APPROVAL_ACT_CSVS` consistently with the same miss. The withhold rests on
a defect, not on a preference.

**The withhold is contract-sanctioned.** `project-trajectory/prompts/adjudicate-amendment.template.md`
states the released-rung arm and its exception in one sentence: *"If a row's new
text is NOT one you would bless, do not re-anchor it: draft the corrective work
in a `## Dispositions` section of this row's own spec."* The
`{aftermath}` slot (`adjudicate_brief._aftermath`, :522-556) told this session the
LLR tier is RELEASED. The session recorded a concrete finding against the amended
text and returned it. The blanket withhold across BOTH rows is also right rather
than lazy: `copy_live` mirrors whole registry FILES (`baseline_snapshot.py:792-804`;
the WI-571 scoping narrows which files, never which rows), so `LLR-136` cannot be
anchored out of `low-level-requirements.toml` without `LLR-158` riding along.

**Lane hygiene — clean.** `git diff --name-only 07cbabb5..HEAD -- docs/archive/last_approved
docs/requirements docs/test` is EMPTY: no registry cell, no `Status`, no snapshot
file was touched. The four commits are verdict → aftermath draft → telemetry →
mechanical close, with `WI: WI-573` on both content commits. The close is
well-formed: `## Deliverable` precedes `## Context` (so
`check_trajectory.parse_spec_deliverable` does not clip it to empty), `specref = ""`,
spec in `docs/work/complete/`. `docs/status.md` and `docs/stage` moved only as the
generated close (the WI-573 row dropped from the ready frontier; `docs/stage`
re-stamped `as-of 02a92f22`) — that is the machinery, not a hand edit.

**Dispositions parse.** `intake.parse_dispositions` returns exactly ONE row, no
refusal: `kind=spine`, `buildtier=medium`, `priority=2`,
`specref=docs/requirements/low-level-requirements.toml`, `bar=DevStg-Reqs`, with a
scope that names the cell, the clause, the three code citations, the archaeology
(`d5b3e124` written, `94b77a26` widened) and an explicit OUT OF SCOPE fencing the
design ruling. Executable.

**Routing.** MEDIUM was adequate and then some — the verdict cites line numbers,
distinguishes the 2 in-scope rows from the 25 carried by other rows with the
WI-566/WI-547 verdicts named, and did the git archaeology that turns "the cell
disagrees with the code" into "the cell is stale". No finding.

## Findings

**1 — MAJOR — the drafted successor routes the withheld re-anchor to an actor the
shipped guard refuses, so the anchor still has no executable owner.** The
`## Dispositions` scope closes with *"ALSO IN SCOPE — the anchor … take the
re-attestation this adjudication withheld: `python
project-trajectory/scripts/intake.py snapshot --approves
"docs/requirements/low-level-requirements.toml=<this row's id>"` in its own
reviewed commit."* That row mints with `safety_class = "spine"`, so
`integrate._adjudication_lane` (`integrate.py:1120-1124`, which requires EVERY
claimed spec's `safety_class` to be `adjudication`) classifies it as an ORDINARY
LANE, and `merge_approval_refusal` sends it to `lane_approval_refusal`. That
reader refuses on any `SNAPSHOT_DIR` file in the delta — its docstring is
explicit: a lane *"does not write `SNAPSHOT_DIR`"*, and `approval_delta` feeds it
the `--name-status` walk of that directory (`acceptance_record.py:733-737`,
refusal assembled at :745-760). The successor's merge will therefore hard-refuse
on the very commit the disposition instructs it to make. Worse, it is the same
separation this whole arm exists for: that lane AUTHORS the corrected `LLR-158`
text, so having it bless its own write is precisely what the 2026-09-01 ruling
moved to the adjudicator. The correct route is already built and needs no new
machinery: the lane corrects the cell and the `code_symbol` and stops; its
amendment of an Approved row stages a `staged_spine_amendments` hit, which mints
an amendment adjudication at that lane's merge, and THAT trunk-side adjudicator —
released rung, no defect left to find — takes `intake.py snapshot --approves`.
*Construction-first:* no guard is owed. `lane_approval_refusal` already catches
this and would catch it loudly; the defect is in the drafted scope, and the
remedy is to rewrite the "ALSO IN SCOPE — the anchor" paragraph in the closed
spec's `## Dispositions` to say the anchor is taken by the amendment adjudication
minted at that successor's merge, not on the successor's own lane. Fixing it
before merge costs one paragraph; discovering it after the mint costs a refused
merge and a re-scope of a `Drafted`-below-approval row.

**2 — MINOR — the session's record exists only in `docs/reviews/`; the compiled
log will carry nothing.** No fragment was written under `docs/log.d/` (the
directory holds only `README.md` at the tip), so `trunk_step.py` compiles no
entry for this adjudication and `docs/log.md` will never mention that two
Approved LLR rows were ruled MEANING and left deliberately un-anchored. The
`## Deliverable` on the closed spec is the dispatcher's generic mechanical text —
it names neither `VERDICT: MEANING rows=2` nor the withhold. Nothing in the
record is FALSE, which is why this is not a MAJOR, but the session-protocol
obligation (`skills/session-protocol/SKILL.md:130-145`) includes the file-level
`Deferred open items:` declaration, and there is no line to carry it: this
session ends owing an act nobody has yet been assigned (see finding 1), which is
exactly what that line exists to surface. Add a
`docs/log.d/WI-573-adjudicate-llr-136-llr-158.md` fragment stating the two
rulings, the withhold and its reason, and a `Deferred open items:` line. (WI-566
set the same precedent; if the intent is that mechanically-closed adjudication
rows owe no fragment, that belongs in the skill as a stated exemption rather than
as a silent pattern.)

**3 — MINOR — one imprecise sentence in the verdict.** *"Both stay drifted and
keep surfacing on the owner's re-attestation brief."* The LLR rung is RELEASED to
the loop — that is what the `{aftermath}` slot told this session, and it is why
the re-attestation was the session's own act to withhold. The drift does keep
surfacing (`trace.reattest_model` feeds `gen_open_items.py:855`, so it is visible
rather than silent), but calling that surface the OWNER's brief reads as though a
human signature were pending, when what is pending is a loop-side act. Word it as
the re-attestation surface, not the owner's.

VERDICT: CHANGES-REQUESTED findings=3
