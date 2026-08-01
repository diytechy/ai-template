## 2026-08-01 — WI-391 cancelled: the specs-of-record mirror is refuted, not built

**Outcome: CANCELLED.** WI-391 asked for concurrency-v2 §B2's second sentence —
specs-of-record mirror the terminal folders, so a spec's location answers
shipped-or-cancelled without opening it. It was measured, prototyped and
**refuted** rather than built. Two independent review rounds confirmed it: round
1 `APPROVE findings=6` (`2a4c9642`), round 2 `CHANGES-REQUESTED findings=4`
against the write-up, with the decision itself not reopened.

The row is `cancelled/`, not parked in `queued/` with a `blockref`, because
**under both options open at OI-11 — strike the sentence or restate it — this
row's work does not happen.** Its own fate is settled even though the design
text's is not, and `cancelled/` is exactly the won't-build-with-the-reason state
WI-384 built. The reason lives in the spec's `## Deliverable`, which is the home
a cancelled row's reason is *supposed* to have — so the record needed no new
grammar.

**Observed en route, and it drove the disposition: a `queued` + `blockref` park
never self-releases.** `blocked` is derived as `queued` plus a `blockref`, and
the blocker's own state is never consulted — so flipping OI-11 to `ruled` would
**not** have returned WI-391 to the frontier. The row would have sat parked with
nobody assigned to close it. This is a property of the registry, not a one-off:
a `blockref` is a **label, not a subscription**, so any park taken to "wait for a
decision" needs a human to come back and unpark it. Filed as **WI-395** rather
than left as an observation in a log entry — this row is its worked example, and
the cost of the silence is already one mis-taken disposition.

**What was measured.** Stated as this row's own convention, because conventions
differ enough between readers that the intake's totals are best treated as
superseded: the literal string `archive/specs/<name>.md` in
`*.md`/`*.py`/`*.csv`/`*.html` occurs **156 times across 31 files** at
`2a4c9642`, and **154 across 30** at `0b4774f0` — the delta is exactly this row's
own review file, one new file carrying two occurrences, a fair demonstration
that the reference surface accretes faster than a migration could be scheduled.
`docs/log.md` (untouched by this branch) holds **119 occurrences on 101 lines**,
of which **92 are markdown link targets** covering **57 unique targets by
full-string key** — 55 by basename, 55 fragment-stripped, 57
basename-plus-fragment, so **57 is the maximum by any key**.

**A correction recorded rather than quietly fixed.** An earlier draft reported
"61 unique targets" against those 92, and when a reviewer challenged it I
*defended* it before re-measuring. It is wrong: 61 is the number of unique names
among `docs/log.md`'s **119 all-occurrences**, a different and larger population
than its 92 link targets. The figure was briefly asserted as verified against a
correction, which is worse than inheriting a wrong number from the intake, so it
is written down here.

The relocation cost is larger than any literal-string count, because a relocation
rewrites **resolved** links: **124 inbound targets across 25 files** resolved by
path (the WI-288 rule), plus **91 outbound links across 43 of the 111 files**
that a one-level-deeper move rebases (the WI-353 defect) — about **215 targets**
against the intake's 101.

**Why it was refuted.** Not cost — the one-time migration was prototyped as a dry
run at ~70 lines, precisely to remove the "too expensive" defence, and that
prototype also settles the rebuild-a-relinker question: one-time beats rebuilding
machinery for a move that happens once. The argument is structural, and it is a
measurement rather than an analogy:

- **Not total.** A folder is derived data and needs a total function from state
  to location. This one is undefined for **16 of 111** archived specs — 15 shared
  effort docs (a first-class shape per the `docs/specs/` README lifecycle) plus
  `WI-300-sr052-binding.2026-07-26.md`, whose name does not match `_own_spec`'s
  own `WI-###.<date>.md` glob. A mapping whose own reader cannot name a file is
  not a mapping.
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
  glob, and the archived-spec glob in `tests/test_trajectory_specs.py` (line 511)
  would each have to **widen** to recurse — the required code change is to
  *ignore* the distinction. The `docs/archive/specs/*` entry in
  `docs/orphans-allow` (line 50) survives untouched only because fnmatch `*`
  spans separators.

**What review corrected.** Round 1, six findings, all taken: the intake figures
are unreproducible and must not be reported as "reproduced exactly"; the split is
92/3/16, not 93/3/15; the structural argument led with its weakest evidence and
was restructured to lead with the totality/regenerator measurement; the
one-time-vs-recurring distinction had to be stated, since the
enforcement-layer-maintaining-enforcement-layer objection would otherwise have
sunk this session's own follow-up; and the proposed remedy for the two
`declared-absences` entries was **wrong** — deleting them adds **+2 dangling**
references under `check_doc_refs --strict`, because the WI-391 spec's own title
names both paths and survives cancellation. They are **restated**, not deleted.
Round 2, four findings, all taken: the unique-target figure above, the
disposition (cancel, do not park), an OI-11 that argued its own recommendation
too hard, and an unenforceable cross-row promise, dropped.

**Filed, and all four outlive this row.**

- **OI-11** ([`docs/requirements/open-items.csv`](../requirements/open-items.csv))
  — whether §B2's sentence is **struck** or **restated**, `Status=pending`. It is
  a decision about the **design text only**, and says so: WI-391 is already
  cancelled under either answer, so nobody rules on this expecting to unblock a
  build. Both options are argued at comparable weight, including the honest case
  *for* striking — the kit's own state-it-once-and-link principle — and the
  recommendation (restate) sits once, in the recommendation cell.
- **WI-393** — rehome the link-aware archival ritual (WI-288's inbound relink,
  WI-353's outbound rebase and their two shared primitives), deleted with
  `agent_dispatch.py` at Phase 5 (`31ad569d`) and never rehomed. Spec archival is
  an unassisted `git mv` again. Driven evidence: from a 4-broken-link baseline, a
  probe spec plus an inbound link left it at 4; a bare `git mv` into the archive
  took it to **8**, of which 3 are WI-353's defect verbatim and 1 is WI-288's
  (`docs/archive/` is exempt from the orphan check only, not the broken-link
  check). Constraint-shaped — one indivisible ritual no caller can do two thirds
  of — so §0 reaches it, and unlike WI-391 it has driving necessity.
- **WI-396** — `check_doc_refs` is structurally blind to a suffixed reference
  into `project-trajectory/`, the half of this repo that is the product. Filed
  small, with the limiter that the gap cannot reach an adopting repo.
- **WI-395** — the `blockref` gap above, filed with its two honest readings and
  neither of them ruled: either the derivation consults the blocker's state, so a
  park releases itself (costing a cross-registry read in a deliberately
  self-contained `schedule.py`, plus a new dangling-blockref failure mode needing
  its own rule), or parks are human-swept and the `WI-000` exemplar and process
  text must **say so**. What is wrong today is not the choice but the silence:
  the mechanism implies a subscription it does not provide.

**Two parallel lanes minted the same WI id.** This row and the `wi-378` lane were
each told to file a new WI in the same wave; both mints read `docs/work/` on
their own branch, neither could see the other's new row, and both correctly
returned **WI-392**. The row filed here was renumbered to **WI-393**. First
*observed* instance of the id-reservation hazard §B3 discusses — that section was
ruled on a hypothetical, and this is the evidence. In both directions: the
composed tree **would** have caught it, because the duplicate-id guard reads the
whole registry. The system works; it works later than a reservation would.

**A citation trap that fired twice on this branch, recorded here rather than in
a commit body.** `check_doc_refs` reads a `path:line` token as a path, so the
line suffix makes it name a file that does not exist. It convicted three
citations in this fragment, then — after that lesson — one more in WI-395, and
then a third time inside **WI-396, the row filed to document the defect**, where
the asymmetry reproduced verbatim in the sentence describing it. This repo's
convention is to keep line numbers **out of the path token** and put them in
prose. Three occurrences on one branch, the last while writing about the first
two, makes it a pattern rather than carelessness — and a commit message is not
one of the working surfaces, so it belongs on one.

The same episode exposed a real defect, and my first account of it was **wrong in
a way that flipped the conclusion**. I recorded that the shipped
`project-trajectory/…` half of the citation "classifies as kit-relative and lands
in the untraced bucket". It does not: it **never reaches classification**. Driven
— `is_path_shaped("project-trajectory/work/WI-000.template.md:40-41")` is
`False` while the `docs/` twin is `True`, and the counter settles it, since
writing both as `path:line` reports `1 dangling · 887 untraced`, the same 887 as
a clean run, where a bucketed token would have made it 888. The cause is
`is_path_shaped`: with a `:40-41` suffix nothing ends in a path extension, so
everything falls to `PATH_PREFIXES`, which enumerates the **downstream** layout
and lists `registries/`, `skills/` and `ci/` *without* the `project-trajectory/`
prefix they actually live under here. An accidental blind spot, not a deliberate
exemption — the kit-relative rule fires only on tokens that are already
path-shaped, so it neither defends nor can close this. Filed as **WI-396**, with
the honest limiter that `project-trajectory/` does not exist downstream, so no
adopter inherits the gap.

**Where §0 would have caught this, and where it would not.** The reviewer's
reading, which is the sharper version of the lesson: this is the process working,
one step later than §0 prescribes. The intake said *at filing*, in its own words,
that the row "deletes no machinery, closes no raise path and makes no bad state
unrepresentable" and "must justify itself on the navigation benefit alone" — and
§0 prescribes asking *"what constraint would make this unrepresentable?"* at
**filing**, "where the cost is still comparable". Applied then, the answer was
already "none, by the row's own admission". So the filing was correct given the
ruling it inherited, and refutation is exactly what a claimed row is for; the
available improvement is only about **where the question gets asked**, not about
whether this row should have been written.

**Bars.** Full suite, `ruff check .`, `ruff format --check .`,
`check_trajectory.py --strict`, `check_doc_refs.py --strict` — all green in the
session report. The one standing red is `test_this_repo_is_not_a_work_branch`,
expected in a worktree. `docs/open-items.html` is deliberately **not** on this
branch: `gen_open_items.py` is one of `trunk_step.py`'s regen steps, so the trunk
lane regenerates it, and a generated view committed here went stale within the
same session the moment the registry changed again.

**Byte deltas on budgeted files:** none — `AGENTS.template.md`, `PROCESS.md` and
`PROCESS_OPTIONS.md` untouched.
