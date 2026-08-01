## 2026-08-01 — WI-391 handed back: the specs-of-record mirror is refuted, not built

**Outcome: HANDBACK.** WI-391 asked for concurrency-v2 §B2's second sentence —
specs-of-record mirror the terminal folders, so a spec's location answers
shipped-or-cancelled without opening it. It was measured, prototyped and
**refuted** rather than built. An independent review confirmed the refutation
(`APPROVE findings=6`, `2a4c9642`) and strengthened it. The row returns to
`queued/` with `blockref = "OI-11"` — it refutes an owner-ruled sentence, so the
owner rules it, not the driver.

**What was measured.** Stated as a convention, because conventions differ enough
between readers that the intake's totals are best treated as superseded: the
literal string `archive/specs/<name>.md` in `*.md`/`*.py`/`*.csv`/`*.html`
occurs **156 times across 31 files** at `2a4c9642` (154/30 at `0b4774f0` — the
delta is [this row's own review file](../reviews/WI-391-REVIEW-A.md), a live
demonstration that the reference surface accretes faster than a migration could
be scheduled). `docs/log.md` holds **119 occurrences on 101 lines, 92 of them
markdown link targets over 61 unique targets** (71 unique repo-wide). The
intake's 154/30/101 could not be reproduced under any convention tried, here or
at the commit that wrote them; every count taken here runs **at or above** the
intake's, so the error direction strengthens the conclusion. One sub-figure the
review read as misattributed — log.md's `61 unique` — *does* reproduce here and
is reported as measured rather than as the review had it.

The relocation cost is larger than any literal-string count, because a
relocation rewrites **resolved** links: **124 inbound targets across 25 files**
resolved by path (the WI-288 rule), plus **91 outbound links across 43 of the
111 files** that a one-level-deeper move rebases (the WI-353 defect) — about
**215 targets**, 92 of them in the append-compiled `docs/log.md`.

**Why it was refuted.** Not cost — the one-time migration was prototyped as a
dry run at ~70 lines, and one-time beats rebuilding a relinker for a move that
happens once. Cost was measured precisely to remove the "too expensive" defence.
The argument is structural, and it is a measurement, not an analogy:

- **Not total.** A folder is derived data and needs a total function from state
  to location. This one is undefined for **16 of 111** archived specs — 15
  shared effort docs (a first-class shape per `docs/specs/README.md`) plus
  `WI-300-sr052-binding.2026-07-26.md`, whose name does not match `_own_spec`'s
  own `WI-###.<date>.md` glob.
- **Contradictory.** `research-knowledge.2026-07-29.md` is cited by WI-138 and
  WI-145 (`complete`) and by WI-158 (`cancelled`); R-F archives a shared doc when
  its *last* open citer closes, so both folders are correct for it.
- **No regenerator.** `gen_trajectory.py` contains the string `archive` **zero**
  times, so no freshness gate could hang off the derived location — it would be
  hand-maintained derived data, which the generated-not-hand-maintained rule
  forbids.
- **Already answered by location.** For the 92 attributable specs,
  `docs/work/complete/` vs `docs/work/cancelled/` answers shipped-or-cancelled
  one directory over. The split is **92 complete / 3 cancelled**, so the mirror
  answers "shipped" 97% of the time for a question one `ls docs/work/` answers.
- **No consumer.** `check_trajectory`'s `ARCHIVE_SPECS_DIR`, `_own_spec` and its
  glob, and `tests/test_trajectory_specs.py:511` would each have to **widen** to
  recurse — the required code change is to *ignore* the distinction.
  `docs/orphans-allow:50` survives untouched only because fnmatch `*` spans
  separators.

**What the review corrected.** Six findings, all taken: the intake figures are
unreproducible and must not be reported as "reproduced exactly"; the split is
92/3/16, not 93/3/15; the structural argument led with its weakest evidence (an
analogy to `disposition`) and was restructured to lead with the
totality/regenerator measurement; the
enforcement-layer-maintaining-enforcement-layer objection would have sunk this
session's own follow-up, so the one-time-vs-recurring distinction is now stated
explicitly; and the proposed remedy for the two `declared-absences` entries was
**wrong** — deleting them adds **+2 dangling** references under
`check_doc_refs --strict`, because the WI-391 spec's own title text names both
paths and survives any disposition. They are **restated**, not deleted.

**Filed.**

- **OI-11** ([`requirements/open-items.csv`](../requirements/open-items.csv)) —
  whether §B2's sentence is **struck** or **restated**, `Status=pending`, both
  options with honest FOR/AGAINST, blast radius stated truthfully (a design
  sentence, a queued row, two `declared-absences` entries; nothing in
  `docs/archive/specs/` moves either way). Recommendation: **restate, don't
  strike** — the goal is sound and already met by the registry half, unmeetable
  for the 16 by any folder layout, and striking would delete an owner ruling and
  leave no record of why, so the tidy-up gets re-proposed.
- **WI-393** — rehome the link-aware archival ritual (WI-288's inbound relink,
  WI-353's outbound rebase, and their two shared primitives), all deleted with
  `agent_dispatch.py` at Phase 5 (`31ad569d`) and never rehomed. Spec archival is
  an unassisted `git mv` again. Driven evidence: from a 4-broken-link baseline, a
  probe spec plus an inbound link left it at 4; a bare `git mv` into the archive
  took it to **8**, of which 3 are WI-353's defect verbatim and 1 is WI-288's
  (`docs/archive/` is exempt from the orphan check only, not the broken-link
  check). Constraint-shaped — one indivisible ritual no caller can do two thirds
  of — so §0 reaches it, and unlike WI-391 it has driving necessity.

**Observed: two parallel lanes minted the same WI id, and nothing on either
branch could have caught it.** This row and the `wi-378` lane were each told to
file a new WI in the same wave; both mints read `docs/work/` on their own branch,
neither branch could see the other's new row, and both correctly returned
**WI-392**. The row filed here was renumbered to **WI-393**. This is the first
*observed* instance of the id-reservation hazard §B3 discusses — that section was
ruled on the strength of a hypothetical, and this is the evidence. Worth stating
in both directions: the composed tree **would** have caught it, because the
duplicate-id guard reads the whole registry, so the collision surfaces at merge
rather than silently. The system works; it works later and more expensively than
a reservation would.

**Deviation from spec.** The handback record was directed into a `## Handback`
**body** section. That shape is **not representable yet**:
`parse_spec_deliverable` accepts only an empty body or exactly one
`## Deliverable` section (a bare `## Handback` raises), and a filled
`Deliverable` on an open row is an **R-A hard error**. WI-387 is building that
shape in a live worktree, so it was not pre-empted here; the record went into the
spec's `title` — this repo's shipped idiom for long spec prose — with a note
saying where it belongs. **WI-387 should relocate it when the section lands.**

**Bars.** Full suite, `ruff check .`, `ruff format --check .`,
`check_trajectory.py --root . --strict`, `check_doc_refs.py --root . --strict`,
`gen_open_items.py --check` — all recorded in the session report. The one
standing red is `test_this_repo_is_not_a_work_branch`, expected in a worktree.

**Byte deltas on budgeted files:** none — `AGENTS.template.md`, `PROCESS.md` and
`PROCESS_OPTIONS.md` untouched.
