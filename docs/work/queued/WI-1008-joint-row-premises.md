+++
id = "WI-1008"
title = "SR-033, SR-223 and SR-225 each state the premise their argument rests on, as an assumption or a waiver"
workstream = "requirements"
sr_refs = ["SR-033", "SR-223", "SR-225"]
specref = "docs/plans/2026-11-11-test-tiers/HANDOFF.md#126-progress-log"
buildtier = "medium"
safety_class = "spine"
priority = 3
planmode = "none"
+++

## Context

Filed by hand on 2026-11-18 at the operator's ruling (HANDOFF §11). The joint
requirements read of the same day (§12.6) set each of this repository's eight
joint requirements beside its siblings' arguments. Five are covered by a
sibling's assumption. Three are joint and cite no assumption, and no sibling's
argument covers their own part. Each rests on a premise outside the system that
no row states:

| Row | What it delivers | The premise no row states |
|---|---|---|
| SR-033 | the generated release checklist | the person releasing works through the checklist |
| SR-223 | the guardrails payload vendored for a model | a model follows the guardrails vendored for it |
| SR-225 | the delegated decisions record | a delegated run discloses its decisions truthfully, and the operator reads what is listed |

DA-003 covers the operator's own acceptances, not SR-225's reading. The
boundary gate's joint skip (`8a2e5c686`, SR-205 as amended) lets the three
rows pass, and it stays as built: no check can tell whether a sibling's
argument fits a joint row's part, so the argument has to be written down.

SR-225's second premise depends on where the listing of unseen decisions
lives, which WI-1009 moves off `docs/open-items.html`. WI-1009's scope
critique has not chosen the new surface yet, so SR-225's assumption names no
page. It speaks of the entries "listed as not yet seen", which is SR-225's own
phrase, wherever they are listed. So this row does not wait on WI-1009, and
it declares no `needs`. The two rows touch different cells of SR-225: this
row adds its `da_refs`, and WI-1009 leaves SR-225 as written.

**The delta.** Registry data only. No code, check, interface or component
changes. Three new `Drafted` rows go into `docs/requirements/assumptions.toml`,
DA-018 to DA-020, one per premise. SR-033, SR-223 and SR-225 each gain a
`da_refs` cell citing its own. Each assumption takes effect at B-09, the
operator's read crossing: the checklist is read there, a guarded session's
work is read back there, and the delegated decisions are listed there. B-05,
SR-223's crossing, is never a landing, because no stakeholder meets the kit
there. B-10 belongs to the model provider, which is no stakeholder's party, so
a landing there would reach none of the needs. `da_refs` is a traced cell
(SR-193: changing assumption citations re-opens no acceptance). So the three
requirements stay `Accepted` and owe no re-accept, and the new assumptions owe
their first acceptance.

**One row, one act.** The three premises land together. They share no code
and could land apart, but each is a few lines of registry text, and one
acceptance act judges all three. WI-1010 takes the same act for the other
assumptions, which is why it is ordered after this row.

## Done-when

- [ ] SR-033, SR-223 and SR-225 each cite an assumption in `da_refs` that
      states the premise in the table above, or carry a `coincident` waiver
      that argues why none is needed. Each new assumption row states where it
      takes effect, when it holds, its obstacle and a falsifier, and is
      `Drafted`.
- [ ] The new assumptions are shown for the operator's first acceptance where
      assumptions are rendered today: `trace.py --accept DA-018,DA-019,DA-020`
      (or `--accept assumptions`). `docs/open-items.html` renders no
      assumption until WI-1010 adds them. If a requirement takes a
      `coincident` waiver instead, that cell is accepted text: the row then
      shows as drift on `docs/open-items.html` for the operator's re-accept.
      Their text lands; the act is the operator's.
- [ ] `trace.py --strict` and `check_trajectory.py --strict` are clean.

## Critique dispositions

Round 1 (Gemini Argon, attended, 2026-11-19,
`docs/reviews/2026-11-19-scope-critiques/WI-1008.md`): CHANGES-REQUESTED, two
MAJORs and two MINORs.

- **S4, `planmode`: adopted as `planmode = "none"`.** The row adds no code
  path. It writes three registry rows and three pointer cells, and
  `trace.py --strict` judges every field the rows must carry. A plan would
  restate the Done-when.
- **S5, the delta and the page: adopted.** The Context states the delta:
  registry data only, the three rows and where each takes effect (B-09, and
  why neither B-05 nor B-10), and no code change. The critique's second point
  was right, and it is wider than it said. `gen_open_items.py` renders no
  assumption, and a change to `da_refs` alone leaves `docs/open-items.html`
  byte-identical, because the cell is traced (measured: one `da_refs` cell
  added to SR-033, page regenerated, no byte changed). So under the
  assumption route nothing this row writes reaches the page. The second
  Done-when item is amended to the critique's second option: the new rows are
  shown where assumptions are rendered today, and WI-1010 adds them to the
  page. Adding `WI-1010` to `needs`, the first option, would make a cycle,
  since WI-1010 already declares `needs = ["~WI-1008"]`.
- **S1, landing together: adopted.** The Context records that the three
  premises land in one row, for one acceptance act.
- **S6, the coupling to WI-1009: adopted, by wording.** The Context commits
  to an SR-225 assumption that names no page. So the row declares no
  `needs`.
