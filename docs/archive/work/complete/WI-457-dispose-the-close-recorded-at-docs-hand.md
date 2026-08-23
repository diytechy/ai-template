+++
id = "WI-457"
title = "dispose: the close recorded at docs/handbacks/WI-451-wi451-sr-retier-campaign.md - cancel / defer / draft a successor / surface an open item (a disposition row never closes early; R3)"
workstream = "process"
buildtier = "medium"
safety_class = "adjudication"
brief = "disposition"
+++

## Deliverable

Closed DONE 2026-08-15. The `WI-451` lane's `partial` claim is **CONFIRMED** —
no override, no cancellation, no deferral, no new open item. Tested against the
three ways it could have been wrong and failing all three: not an under-claim
(the report's `## Not delivered` list was genuinely outstanding at close), not
an over-claim (149 → 64 rows, 26 tombstones deleted, 73 demotions needing zero
new design rows, `Area` retired, 62 of 115 IF rows re-pointed — verified), and
not silent on the keep/discard split (11 keeps named, 0 discards, decided by
the lane, all 11 on trunk). Successors named and already minted: **`WI-458`**
(complete) carries the five unruled findings, both flagged crossings and
SR-165's chain; **`WI-459`** (complete) carries crossing ownership;
**`WI-460`** (open) carries the second top-down read and adversarial round 2,
and gains `supersedes = "WI-451"` here as the only successor still open. The
report's sequencing instruction — rule the five findings before any
interface-registry work — was checked and **honored** (`2026-08-15b` preceded
`2026-08-15e`; the 11 IF rows moved once). Nothing is owed by the closed row;
`WI-451` stays terminal in `docs/work/partial/`, byte-identical, its report
untouched. Full text in this spec's `## Disposition`; reasoning in
`docs/log.md` entry `2026-08-15f`. Provisional under the 2026-08-15
charge-through.

## Context

The closed spec is `docs/work/partial/WI-451-sr-boundary-conformance-pass.md`.

Its per-close report is `docs/handbacks/WI-451-wi451-sr-retier-campaign.md` — READ IT FIRST. The report is the close EVENT's own immutable record: what the lane claims it delivered and did not, the commit range, the keep/discard split, and the review tier it suggests. The lane's claimed outcome is a CLAIM under judgement here, not this row's premise.

Outcomes (R3): cancel / defer / draft a successor / surface an open item. Continuing the work MINTS A SUCCESSOR (drafted in THIS row's `## Dispositions` section, carrying `supersedes`), never a revival of the closed row — a closed row is never re-opened and a scope definition never changes to mean something else. An override moves the byte-identical spec to the corrected terminal folder; the report stays on record as the claim it was. An open item goes to docs/requirements/open-items.toml.

## Disposition

> **Heading singular on purpose — do not "fix" it to `## Dispositions`.**
> `intake.parse_dispositions` partitions on the literal `\n## Dispositions` and
> REFUSES the whole mint when that section carries no fenced TOML draft block.
> This disposition drafts no successor because **the successors already exist**
> (below), so the plural heading would arm a refusal on the next sweep. Same
> note, same reason, on `WI-456`; the `intake.py` defect is recorded in log
> `2026-08-15f` rather than patched inline.

**Disposed 2026-08-15; closed DONE. The lane's `partial` claim is CONFIRMED —
no override, no cancellation, no deferral, no new open item.** Reasoning:
[`docs/log.md`](../../../log.md), entry `2026-08-15f`. **Provisional** under the
owner's 2026-08-15 charge-through and overturnable at the review sitting.

### The claim, judged rather than assumed

The report at
[`docs/handbacks/WI-451-wi451-sr-retier-campaign.md`](../../../handbacks/WI-451-wi451-sr-retier-campaign.md)
claims `partial`. A disposition judges that claim, and there are three ways it
could have been wrong: the lane could have under-claimed (delivered everything
and closed `partial`), over-claimed (`partial` where `cancelled` was honest), or
been silent about the keep/discard split — the silence that merged rejected code
onto trunk on 2026-08-03.

**None applies.**

- **Not an under-claim.** The report's `## Not delivered` names five UNRULED
  findings (H1, H4, H5, M1, M3), two crossing attributions flagged for overrule,
  SR-165's missing design row and test case, a second top-down read, and
  adversarial round 2. Every one of those was genuinely outstanding at close.
- **Not an over-claim.** The `## Delivered` half is verifiable and verified: the
  SR tier went 149 → 64 rows across seven acts, 26 tombstones deleted per D-4,
  73 rows demoted with **zero new design rows needed**, `Area` retired for the
  closed `Aspect` vocabulary, and 62 of 115 interface rows re-pointed. The spine
  closed clean at the claimed measurement.
- **Not silent on the split.** `keep_commits` names 11 shas, `discard_commits`
  is explicitly empty, and `split_decided_by = "lane"`. The adjudicator has
  nothing to override: all 11 are on trunk and every subsequent act has built on
  them.

`partial` is therefore the accurate word, and it was the accurate word at the
time. The close reason — that a partially completed re-tier is within the design
expectation and that modifying attested rows is the point of the exercise rather
than an obstacle to it — is the owner's own 2026-08-15 ruling, and the record
since has borne it out: four attested rows have been moved deliberately, each
named.

### The successors, and what each carries

Continuing work rides successors, never a revival of `WI-451`. All three were
minted from the completion analysis
([`docs/plans/2026-08-15-retier-completion.md`](../../../plans/2026-08-15-retier-completion.md))
**before** this disposition was written, which is why no successor is drafted in
this section: it would mint a fourth row for work already claimed.

| Successor | State | What it carries from the report's `## Not delivered` |
|---|---|---|
| `WI-458` | **complete** (log `2026-08-15b`) | All five unruled findings — H1 (mint SR-166 for B-05's own named observable), H4 (SR-153/SR-059 merged into SR-148), H5 (the tomllib-vs-sh observable given one home), M1 (four mis-tiered rows demoted, two of them attested), M3 (three uncovered needs carried) — plus both flagged crossing attributions examined and CONFIRMED, and SR-165's owed design row and test case minted `Draft` |
| `WI-459` | **complete** (log `2026-08-15f`) | The crossing-ownership question — completion analysis blockers C1/C2, which is sitting-3 decision 8 pulled forward: the regenerated distribution, `OI-29`'s ruling recorded, and an owner named for each of B-01/B-02/B-06/B-07 |
| `WI-460` | **open, queued** | The report's two remaining items verbatim: the SECOND top-down read of the re-tiered layer against the six crossings, and ADVERSARIAL ROUND 2 on the settled state (round 1 is spent — the fixes postdate its verdict) |

**`WI-460` carries the machine-readable lineage.** It gains `supersedes =
"WI-451"` in this act, as the only successor still open. `WI-458` and `WI-459`
closed before this disposition existed and carry the lineage in prose only —
recorded as it happened rather than back-stamped, since a closed row's
frontmatter is not the place to invent a history.

### The sequencing rule the report warned about — HONORED

The report's sharpest instruction was *"rule the five findings BEFORE any
interface-registry work,"* on pain of re-pointing 11 interface rows twice. The
order actually executed was `WI-458` (log `2026-08-15b`) and only then the
interface rework (log `2026-08-15e`). The 11 rows moved once. Checked, not
assumed.

### What is owed by the closed row

**Nothing.** `WI-451` stays in `docs/work/partial/`, which is terminal; its spec
is byte-identical to what it was at close; the report stays on record as the
claim it was. The suggested review tier (`medium`) is subsumed by `WI-460`'s
adversarial round 2, which is a strictly higher bar on the same subject — noted
rather than run twice.
