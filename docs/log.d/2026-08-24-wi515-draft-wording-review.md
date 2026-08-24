## 2026-08-24 — WI-515: the cross-family wording round on the approval-pending Drafted text

**Why.** The owner, in-session: *"The text on these items that need approval
still seems pretty heavy. Can you spin up an openai terra review to suggest
more simplified wording and accept suggestions that still fit the intent of the
SR?"*

**Provider, and no substitution.** Routed by PROVIDER, not gateway:
`OPENAI-TERRA` — model `gpt-5.6-terra`, `codex exec --model {model}
--dangerously-bypass-approvals-and-sandbox`, the row `docs/agents.toml`
declares and `docs/agents-enabled` lists (its presence being the consent
surface). The entry the owner named exists, so nothing was substituted. Probed
live before the real dispatch (a one-token prompt on stdin returned `PONG`
through `--output-last-message`); `codex-cli 0.144.4` on this box. Four batches,
prompt on stdin, each row carrying its anchor SR's `Requirement` and
`AcceptanceCriteria` as the intent anchor. The four raw returns are committed
unedited beside the dossier.

**The population, and what was editable.** The nineteen `Drafted` chain rows on
`docs/ratify/CURRENT.md` — nine LLR `Title`/`Detail`, ten TC `Method`/`Expected`
— were the editable set: they carry no approval, so re-wording them needs no
warrant. The nine anchor SRs and `LLR-041`'s drifted cell are `Approved` and
were sent as context only; nothing was applied to them.

**The adjudication, every suggestion confirmed or refuted.**
- fig: 38 suggestions over 19 rows — 21 ACCEPTED (5 amended), 17 REJECTED
  (counted from the four raw returns in
  [../reviews/2026-08-24-draft-wording-round/](../reviews/2026-08-24-draft-wording-round/),
  dispositioned row-by-row in that folder's `RESUME.md`).
- fig: the reviewable population 29,441 -> 25,564 characters, **-13.2%**
  (`len()` over the `title`/`detail` and `method`/`expected` cells of the 19
  `Drafted` rows, HEAD `4ecc4fc3` versus the working tree).
- fig: nine LLR `Title` cells -28% to -67%; the convention that argued for them
  is measured, not stylistic — over the 175 approved LLR rows the title median
  is **36** characters, 146 are under 60 and only 4 reach 90, while these nine
  ran 63-137 (`statistics.median` over
  `docs/requirements/low-level-requirements.toml`, this revision).
- fig: `docs/ratify/CURRENT.md` 67,180 -> 62,667 bytes (`wc -c`, HEAD versus
  the working tree) — smaller even while now carrying a before/after pair per
  re-worded row, which is the brief's declared design for a `Drafted` row that
  differs from the snapshot, and which vanishes at the approval that re-seeds
  it.

Fourteen of the seventeen rejections are three classes, not seventeen
judgements: every `Expected` suggestion replaced the registry-wide one-line
pointer with a 400-600 character restatement of its own `Method`; five `Method`
rewrites promoted the anchor SR's acceptance criteria into the case as executed
steps no `Evidence` entry covers; and `TC-182`'s rewrite drove a
seam-signal-compatibility case that `LLR-187` — the row it verifies — states has
no executable form. The five amendments restored guards a cut would have taken
(`LLR-193`, `LLR-199`) or removed content the reviewer INVENTED or imported from
the parent (`LLR-194`, `LLR-196`, and `LLR-194`'s title).

**Gates.** Registry text only — no executable code touched, so no full suite is
owed. Commit bar, run and pasted:

```
python -m pytest -q -n auto -m smoke      -> 1323 passed, 5 skipped in 21.64s
python scripts/check_smoke_budget.py --mode enforce
                                          -> 22.5s vs 60s budget -> within
python project-trajectory/scripts/check_docs.py --root . --stale
                                          -> OK - 1064 doc(s), 0 broken
python project-trajectory/scripts/check_trajectory.py --strict
                                          -> clean (512 work item(s))
python project-trajectory/scripts/trace.py --strict-integrity
                                          -> integrity=0, drafts=19,
                                             provenance-findings=1,
                                             paraphrase-advisories=3
```

The last line is the acceptance gate for the new text and the number
specifically watched: shortening a child `Detail` RAISES its lexical overlap
with its parent, so `paraphrase-advisories` could have grown. It did not — it is
the same three pre-existing rows (`LLR-007`, `LLR-020`, `LLR-027`), and
`provenance-findings` is the same pre-existing `LLR-197`. Every accepted text
was screened for the vague and open-ended vocabulary and for the citation-frame
shapes before it was applied, and no LLR `Detail` gained a "shall".

**Nothing was approved.** No `Status` cell moved, the
`docs/archive/last_approved` snapshot was not re-seeded, and the nineteen rows
still owe the owner's act. Surfaces regenerated so he signs the NEW text:
`docs/ratify/CURRENT.md`, `docs/open-items.html`, `docs/stage`,
`PROJECT_STATE.html`.

**Deviations from spec:** none.

**Byte deltas on budgeted files:** none — no budgeted file touched.

Deferred open items: none — the owner's approval act was already queued before
this row and is unchanged by it; the two things the round surfaced about
`Approved` text (the reviewer's repeated "the parent already states it" cuts,
and `LLR-041`) are listed for the owner in the dossier and neither needs a
ruling to proceed.
