# 002 — ADJUDICATE (independent, Claude Opus) — WI-806 amended approved rows at `78d90c70`

Adjudicator: independent Claude Opus. I wrote none of WI-806's code or rows.
Anchors: `docs/archive/last_approved/` for LLR and TC, copied at `7e001ccc`.
Live `1832b889..78d90c70` differs from them only in LLR-173, LLR-245, LLR-298,
the new LLR-302 and TC-173. The basis, the mutation probes and the code read are
`001-ADJUDICATE-78d90c7.md`'s; this file adds only what bears on the amendments.

## Basis (probed, not trusted)

- **LLR-245's dropped subtraction is a no-op only through an invariant the row
  does not state.** The code: `_approval_transition(before, row)` is
  `not _claims_approval(before) and _claims_approval(row)`, and
  `_ledger_live_rows` absorbs a row only when `_claims_approval(before)`, so a
  flipped row is never absorbed and subtracting flips changed nothing (D-006,
  confirmed). But the row's own definition, "approved text drifted from the
  recorded copy", reads just as naturally as "a live row claiming approval
  whose text differs from its copy". Every row being flipped is that: a
  `Drafted` row amended since its copy, now `Approved`. Under that reading the
  new text refuses every first approval of an amended row unless it is also
  named in `--reattests`. The old text could not be read that way, because it
  subtracted the flips explicitly. SR-207 itself keeps the leg ("neither
  approves nor re-attests").
- **LLR-173's new sentence overclaims.** "the text it records is committed
  earlier" covers every registry the copy records, and that includes the
  interface, external and component registries. `APPROVAL_ACT_CSVS`
  (`acceptance_record.py:213`) excludes them, so an act commit may change an
  interface row's text beside the record and pass. That is D-001, named by the
  builder for the owner. The sentence also restates LLR-302's decision rather
  than pointing at it, and TC-167 (LLR-173's only TestRef) does not verify it.
- **LLR-173's new rationale is imprecise.** "that walk reads the text commit":
  the walk returns the newest commit at which the row reads `Verified`. For an
  approved row that is amended, every commit qualifies and the walk returns
  HEAD. For a re-flipped row it returns the act commit or later. Neither is
  "the text commit". The old rationale was still true and did not sanction
  amend-plus-flip; it named it as the walk's precondition.
- **TC-173's evidence misses four of LLR-302's clauses.** In 001's probes, M1
  (add or remove), M2 (hook wiring) and M3 (slot ladder) are killed only by
  uncited nodes. The root-commit clause is held only by the uncited
  `test_a_first_commit_has_nothing_before_it`. The replacement cites the whole
  text-then-act file, the shape WI-803's TC-069 landed with.
- **Replacement text checked** on the probe copy: `trace.py --strict` gives
  integrity 0 with unchanged counts, and `check_vocab` is clean.

## Rulings

- [RETURN] LLR-173 detail -> before: the record's copy contract, unanchored rule, three refusals, git-derived stamp and SR-140's two record fields; nothing about when the recorded text was committed -> after: adds "The copy rides an act whose approval-act registry rows change only Status and are neither added nor removed; the text it records is committed earlier." -> MEANING. A copy taken in an amend-plus-flip commit satisfied the old text and fails the new. I would not bless it as written: the sentence overclaims for the off-spine registries (D-001), restates LLR-302's decision, and is unverified by TC-167. The `rationale` change is clarity in obligation but imprecise (see Basis), so it is replaced too. Replacement cells (the detail differs from the live text only in that one sentence, now a pointer):
  - `detail`:
```text
The approval RECORD SR-140 requires, sited: LLR-158's comparison basis (SR-178's drift rule) and LLR-178's mirror invariant (SR-179's refusal) are its two readers, and what make it worth recording. copy_live(root, seed=False) mirrors the snapshotted registries (the four spine tiers, interfaces/external/components, which carry human-only approval and state cells, and assumptions) BYTE FOR BYTE into docs/archive/last_approved/, preserving repo-relative paths so spine_carrier.resolve/carriers/stem resolve under the snapshot root verbatim, carrier fallback included; the stale other-carrier file for a stem is deleted in the same act, or the next read raises "exists under BOTH carriers". The approval-act rows' text the copy records was committed before the act that writes the copy, which changes only their Status and adds or removes none (LLR-302); the off-spine registries the copy also records are outside that ordering. Whole files rather than extracted rows is what makes "snapshot file == live file at the copy commit" DECIDABLE - LLR-178 carries that mirror invariant - and it is also what makes the UNANCHORED rule decidable, because the copy keeps each row's own Status cell, so a live row claiming approval whose snapshot copy reads below it is an approval that never rode a copy. unanchored_findings asks that of every tier SNAPSHOT_TIERS lists, the needs file's needs and stakeholders included, and reads the needs registry's copy under its legacy markdown carrier as present. Three refusals are load-bearing and each is the opposite of a convenient degrade: copy_live REFUSES to CREATE the directory without seed=True, because the first snapshot blesses whatever text is in the tree and must ride the owner's reviewed signing commit (reachable only from `intake.py snapshot --seed`); load_all returns None for an absent directory and RAISES on a file that exists and will not parse, because {} and None are opposite claims and the empty one reads as "re-bless everything with no diff shown"; and rows_for is the ONE place the None sentinel is collapsed, so no caller invents its own `or {}`. is_drifted/drifted_cells delegate the cell comparison to LLR-158's split_changed_cells and arm on the APPROVED half only. stamp() is advisory and derived FROM GIT rather than from a file, so it can never quietly become the ledger this mechanism replaced; every arm degrades to ("", ""). SR-140's two remaining record fields come from the same two places and neither is a cell: the TRANSITION is the copy's Status read against live's (the comparison above), and the ACTING REVIEWER is the AUTHOR of the commit that wrote the copy - which is why the copy must ride the approval commit and why the author is queried from git rather than stamped, since a stamped reviewer is a claim and a commit author is a record. unanchored_findings joins the integrity failure set, so it fails the always-on --strict-integrity floor at every stage; it is vacuous until the record holds a registry, so a tree that has signed nothing is never redded by it.
```

  - `rationale`:
```text
The baseline had to leave git history. The derivation it replaces walked the registry for the newest commit at which a row read Verified. That walk can only return a commit at which the row already reads Verified, and an amended row either keeps that Status through its amendment or regains it in an act committed after its text, so the commit it returns already carries the text under judgement and its diff is empty BY CONSTRUCTION on exactly the rows a sitting exists to judge. A snapshot on disk is a baseline OUTSIDE the live file, which is the one thing a walk over the live file can never be. docs/archive/ is the placement rather than an accident: check_vocab.EXEMPT_GLOBS already exempts it, and the snapshot legitimately holds the PREVIOUS vocabulary, so anywhere else reds the vocabulary enforcer on every signing. The design's own argument for whole-file copies is that a human can open the record and `git diff` it - a record only a script can read is a record only a script can audit.
```

- [RETURN] TC-173 method/expected -> before: the mirror-invariant suite, items (a) to (e), satisfying SR-179 via LLR-178 -> after: adds (f), the text-then-act suite, and "satisfies LLR-302 by exercising the same two-tree refusal at the hook and lane landing" -> MEANING (a new acceptance condition and a new row verified). I would not bless it as written: (f) and `evidence` leave LLR-302's add/remove, hook-wiring, slot-ladder and root-commit clauses unverified (M1, M2 and M3 survive the cited nodes). `expected` is right as amended and stays. Replacement cells; `verifies` (`SR-179;LLR-178;SR-140;LLR-302`) is correct and stays:
  - `method`:
```text
Run the mirror-invariant half of the baseline-snapshot suite over real temp repos - the half TC-167 no longer covers, which is the record's own contents. (a) A clean copy passes, so the rule is silent on the legitimate act it exists to permit. (b) A HAND-EDITED record file fails, and (c) a PARTIAL copy fails - the two forgeries the single byte-identity comparison catches without a second detector. (d) THE DELETION ASYMMETRY, both arms executed rather than argued: a record file deleted WHILE THE REST OF THE RECORD STANDS fails (the cheap laundering - removing the page the unanchored rule reads), while deleting the WHOLE record is SILENT (retirement and wholesale replacement are legitimate). (e) The prose README inside the record is exempt, because it is not a recorded registry and has no live counterpart to be identical to. (f) Run the text-then-act suite over real temp repos: a commit that writes the record while changing an approval-act row's cell other than Status, a traced cell included, or adding or removing such a row, is refused, while a commit that writes no record is not judged; text followed by a Status-and-copy act passes; the pre-commit hook runs the step and the merge slot's ladder consults the rung; a no-verify lane commit is refused at the landing; a merge, a refresh merge included, is judged by what neither parent carried, and a merge's own text beside the record is still refused; a squash is admitted only when every commit it folds in passes; a commit whose parent the repository cannot read, and a diff git cannot read, are reported rather than skipped; and a root commit passes.
```

  - `evidence`:
```text
tests/test_baseline_snapshot.py::test_a_clean_copy_satisfies_the_mirror_invariant; tests/test_baseline_snapshot.py::test_a_HAND_EDITED_snapshot_fails_the_mirror_invariant; tests/test_baseline_snapshot.py::test_a_PARTIAL_copy_fails_the_mirror_invariant; tests/test_baseline_snapshot.py::test_a_snapshot_file_DELETED_while_the_record_STANDS_fails_the_mirror; tests/test_baseline_snapshot.py::test_deleting_the_WHOLE_record_is_SILENT; tests/test_baseline_snapshot.py::test_the_README_is_prose_and_is_exempt_from_the_mirror; tests/test_text_then_act.py
```

  - (f)'s last two arms (an unreadable parent, an unreadable diff) need the two
    tests 001 lists under "Owed to the builder". The whole-file evidence covers
    them once they are added. Until then those arms are claimed without a test,
    so the text lands with the tests or not at all.
- [RETURN] LLR-245 detail -> before: absorbed rows minus the rows the act flips minus the rows named by --reattests -> after: absorbed rows minus the rows named by --reattests -> MEANING. The two agree only if "absorbed" excludes flipped rows by definition, and the cell's definition ("approved text drifted from the recorded copy") does not say so. A correct implementation of the old text (subtracting flips) fails the new one under that cell's natural reading. Fail toward meaning. The code is right, and the fix states the invariant the deletion relies on. Replacement cell (only the parenthetical changes):
  - `detail`:
```text
refresh_refusal computes, per registry, the absorbed rows (rows whose recorded copy claims approval and whose approved cells moved or which the live registry no longer carries; a row the act flips has a copy below approval, so it is never absorbed) minus the rows named by --reattests, and refuses while that set is non-empty; naming a registry in --approves no longer clears its other rows. _refusal_text lists every such row and cell, with no cap. parse_reattests reads comma-separated row ids, and intake.py snapshot gains --reattests and --verdict, the verdict file that ruled the re-attested rows: verdict_rel spells it repository-relative with forward slashes, making an absolute path under the repository relative, and _refuse_verdict refuses a verdict named without --reattests, an absolute path outside the repository, and a path naming no file in the tree. The act's record stamps the re-attested ids beside the approvals, and its act ledger entry records the normalized verdict. The two snapshot tests that pin the old any-flip-authorizes-the-file behaviour change with it, since that behaviour is the one this row removes. The rule covers every tier in SNAPSHOT_TIERS, including the frame's three tiers, the assumptions registry's two and the needs file's two (needs and stakeholders), so an act copying the needs registry is refused while an approved need's text moved unread, and --reattests names a need or a stakeholder to re-anchor it.
```

  - `code_symbol` (`+_ledger_live_rows`) is a traced cell. It matches the
    helper's `Implements: SR-207, LLR-245` tag.

## Not ruled here, and owing no act

- **LLR-298** changed only `code_symbol` (`+_commit_parents`,
  `+_each_lane_commit`), a traced cell. It is true of the code (both carry
  `Implements: SR-148, LLR-298`), not drift by `is_drifted`, and not in the
  brief.

## Terra's refusal to amend TC-167: upheld

TC-167 verifies SR-140 through LLR-173's record contract: vacuity, the seed
guard, the copy contract, unanchored in both directions, and the CLI. None of
that moved, and none of its text offers amend-plus-flip. The new two-tree policy
is LLR-302's and is verified by TC-173. With LLR-173's sentence made a pointer
(above), LLR-173 states no clause TC-167 would owe. Had Terra's overclaiming
sentence stood, LLR-173 would carry a claim its only TestRef does not verify.
That is a second reason for the replacement, not a reason to amend TC-167.

## SN-029 (the owner's row; for the coordinator to file)

- **Does `acceptance` become untrue when this lands? Yes, in one appositive.**
  "Text that has moved away from what was accepted surfaces regardless of any
  Status movement, the one signal the sanctioned amend-and-flip path would
  otherwise hide" calls amend-and-flip sanctioned. After WI-806 a commit that
  carries text together with the record is refused at the hook and the slot.
  The normative half, that moved text surfaces regardless of Status, stays true
  and needed.
- **Terra's text** ("the one signal a Status transition would otherwise hide")
  is true, but it keeps a premise clause that only makes sense to a reader who
  knows the history. I recommend deleting the appositive instead:

  ```text
  Text that has moved away from what was accepted surfaces regardless of any Status movement, so an AMENDED requirement drops the derived stage exactly as a newly introduced one does.
  ```
- **The `why` cell goes stale the same way.** "— precisely the sanctioned path
  an amendment detector ignores — so the blessed way to amend an attested
  requirement is invisible to every consumer". The owner may want "— which no
  sanctioned path now does — so an amendment to an attested requirement is
  invisible to every consumer".
- Two older staleness points are outside this WI. `acceptance`'s "a digest of
  that row's normative cells" predates the whole-file copy. `why`'s "an SN has
  no Status cell" is untrue now that needs carry `status`. Both belong in the
  same owner sitting.

## Aftermath (not taken; the coordinator gates the act on the code review)

LLR and TC sit on a rung the declared gate authority releases. All three
returned rows are MEANING rows that I would bless with the replacement cells. The
sequence:

1. The replacement cells (here and in 001) land byte-exact in a text commit,
   with the two owed tests.
2. A fresh ruling on the landed text.
3. Then one act commit, changing only `Status`: LLR-302 flips `Drafted` to
   `Approved`, and the three rows are re-attested.

```text
python scripts/intake.py snapshot --approves "docs/requirements/low-level-requirements.toml=WI-806;docs/test/test-cases.toml=WI-806" --reattests LLR-173,LLR-245,TC-173 --verdict docs/reviews/wi-806-text-then-act/<the fresh amendment verdict>.md
```

VERDICT: MEANING rows=3
