## 2026-08-22 — WI-484 phase 2: the `hat_refs` judgement backfill (item 1 of the six owed)

**Slice 2 of the six-phase program row. The row STAYS ACTIVE.** Item 1 of the
lane's owed list — the judgement backfill phase 1 deliberately did not attempt —
is done. Item 2 (the writer) is examined below and left OWED with its blocker
named; items 3–6 are untouched.

Deferred open items: none — this slice ruled nothing the owner had reserved. The
cell is informative and `traced` at both tiers (WI-484 slice 1's own
classification), the rows it lands on are Approved, and the owner's 2026-08-20
sequencing note ("NOT anticipated to be an attested cell, so it can be tacked on
AFTER the sitting") is what makes that true — verified below rather than assumed.
Item 2's blocker is a design question inside this lane's own phase 2, not a
question needing the owner's judgement, so it is recorded as a lane item.

### The figures

- `hat_refs` present on **72 of 74** SR rows and **9 of 171** LLR rows; **55** SR
  cells and **8** LLR cells written here, the rest pre-existing from slice 1
  (17 SR + `LLR-183`)
  <!-- fig: derived="count of rows whose Hat-Refs cell is non-empty in docs/requirements/{system-requirements,low-level-requirements}.toml at this commit, via spine_carrier.rows_from_toml" -->.
- Coverage advisory, over EFFECTIVE sets: **184 of 245 → 4 of 245** rows
  attributable to no declared perspective
  <!-- fig: cmd="python project-trajectory/scripts/trace.py --root ." rev=69e4a854 -->.
- Declared hats attributed to NO row: **5 → 1**. `CROSS-PLATFORM`,
  `FIRST-RUN-ADOPTER`, `INTEGRITY-RECOVERABILITY` and `PRODUCT-FITNESS` each
  found rows they genuinely derive; **`SAFETY` remains the one hat nothing is
  attributable to**, and that is the honest answer rather than a hole — it is
  the exact call `hats.toml`'s own header leaves open to the owner ("whether
  SAFETY belongs in THIS repo's roster at all, or ships only in the template"),
  and the backfill is now evidence for it rather than an opinion about it
  <!-- fig: cmd="python project-trajectory/scripts/trace.py --root ." rev=69e4a854 -->.
- **160 of the 162 LLR rows with no own cell are covered by INHERITANCE** and
  need none; the two that are not are `LLR-015` and `LLR-037`, the sole children
  of the two rows deliberately left empty below
  <!-- fig: derived="trace.effective_hats(row, sr_rows) over every LLR row at this commit" -->.

So the four uncovered rows are exactly the two calibration rows plus their only
children, which is the derivation reporting correctly: a child inherits nothing
from a parent that records nothing.

### The rule the 55 SR cells were written against

**One rule, stated so the next reviser can falsify a cell rather than re-argue
it: attribute a hat only where THAT HAT'S OWN `listens_for` NAMES A FAILURE THIS
ROW PREVENTS.** Not "which lens could be held up to this row" — nine of the
sixteen hats are `always`, so that reading fills every cell with nine names and
the column stops meaning anything. Read against the 17 rows slice 1 migrated,
this is also what they already do: `SR-024` carries `TEST-ENGINEER` alone even
though `MAINTAINER`, `PERFORMANCE` and `CONSISTENCY` are all unconditional.

Median cell is one name; 15 rows carry two; none carries three. Where the
attribution came out at three, the third was dropped in favour of the row's own
stated primary failure (`SR-138`: the destructive-write and the un-aided-adopter
halves are its rationale's own two arguments, so `SECURITY` — true of the dial it
destroyed — is left to `SR-137`, which states that failure).

### The two calibration rows, read individually — both stay EMPTY

- **`SR-015` — `hat.PERFORMANCE` is NOT attributed.** The cell names the hat in
  order to REFUSE it, and the refusal is argued rather than asserted:
  *"SN-002 is the only basis: hat.PERFORMANCE's failure class is a speed or size
  risk left unassessed, or a budget with no measurement behind it, which says
  nothing about whether a trace reference resolves."* That reasoning is correct
  and survives re-reading. The remaining question is whether some OTHER hat
  bears, and the honest answer is no: the row states a data invariant (every PB
  row's Refs resolve) and deliberately splits the CHECKER off to `SR-157`, so
  `TEST-ENGINEER` — the hat that would otherwise fit — belongs to the row that
  holds the enforcer, not to this one. Empty.
- **`SR-040` — the struck attribution is NOT resurrected.** The cell records two
  lenses (`hat.UX-ENGINEER`, `hat.UNATTENDED-OPS`) that reached a resume-surface
  size tripwire this row NO LONGER CARRIES, and states the disposition itself:
  *"The lenses are not overruled; their subject is gone."* Writing either into
  `hat_refs` would re-point a live cell at a deleted subject — precisely the
  staleness the cell exists to make mechanical. Nothing else bears: what survives
  in the row is per-phase command routing and cross-family review independence,
  and no roster hat's failure class is review independence. Empty.

Both rows also make the wider point the lane measured: a `hat.` regex over
`rationale` matches 19 rows and these are the two extras, wrong in opposite
directions. Nothing in this slice was written by pattern.

### The LLR tier: 8 own refs, and why 162 rows correctly have none

An LLR's effective set is its own refs UNIONED with its SR parents'. So an own
ref is earned only where the design row bears a hat **no parent carries** —
anything else is the copy-down the derivation was built to prevent, and it would
turn re-ruling one SR into a sweep over its children. The eight:

| Row | Own ref | Why the parent does not carry it |
| --- | --- | --- |
| `LLR-021` | `CROSS-PLATFORM` | the hook interpreter probe: a Windows Store alias satisfies a PATH test while exiting nonzero. `SR-019`/`SR-020` are the secrets floor (`SECURITY`, `DATA-PROTECTION`) and their own text calls the probe mechanism, not a second obligation — so the platform lens reaches the design row and stops there. |
| `LLR-079` | `UX-ENGINEER` | responsive output at real widths (mobile CSS present). Its only parent is `SR-070`, the artifact-INTEGRITY row. |
| `LLR-088` | `ACCESSIBILITY` | keyboard descent (Enter/Space) and breadcrumb restoration. `SR-169` is the graph-content row (`UX-ENGINEER`); keyboard operability is `SR-052`'s lens, and this row is not `SR-052`'s child. |
| `LLR-105` | `ACCESSIBILITY` | the WCAG 3:1 UI-boundary contrast floor in both themes, under `SR-054` (usability), which carries the two UX hats and not this one. |
| `LLR-118` | `UX-DESIGNER` | the generated OWNER DECISION surface — a page whose reader is making a ruling on it — under `SR-049`, a derivation-of-the-stage row. |
| `LLR-161` | `INTEGRITY-RECOVERABILITY` | the close ritual's all-or-nothing: the report is written first and EVERY report the call wrote is restored on any refusal, so a multi-spec lane cannot half-close. `SR-144` states the terminal outcome, not the atomicity of writing it. |
| `LLR-164` | `CROSS-PLATFORM` | `--check` compares on NORMALIZED line endings, because a CRLF checkout is not a stale catalogue. `SR-146` is the prompts-are-reviewable-files row (`SECURITY`). |
| `LLR-177` | `SECURITY` | transcript redaction of declared CREDENTIAL shapes. `SR-176` carries `DATA-PROTECTION` — the row is about how a finding is recorded; this one is about the secret itself. |

**Why the other 162 record nothing, by class** (a sentence per class, not per
row, and each is a positive reason rather than an omission):

- **Inheritance already covers it — 160 rows, the overwhelming majority.** The
  design row is the sited mechanism of exactly the obligation its parent states,
  so its effective set IS its parent's and an own ref would be a copy. The whole
  `SR-052`/`SR-053`/`SR-054` rubric-core family, every phase of the `SR-155`
  dual-plan round, and the `SR-157`/`SR-159` checker rows sit here.
- **The row's argument is this repo's ambient design idiom, not a perspective.**
  "One home, don't duplicate", "PURE — text in, rows out, no git",
  "F5-duplicated because bootstrap imports no kit sibling" appear in dozens of
  `detail` cells. Attributing `CONSISTENCY` or `MAINTAINER` on that phrasing
  would fire on roughly a quarter of the tier and make the column noise; the
  idiom is how every row here is written, so it discriminates nothing.
- **Retired or narrowed rows record what a mechanism NO LONGER does** —
  `LLR-037`, `LLR-050`, `LLR-147`, `LLR-157`. There is no live decomposition to
  attribute, and `LLR-037` is additionally the child of a calibration row.
- **Thin siting rows** whose whole `detail` names a function and its contract
  (`LLR-011`, `LLR-022`, `LLR-033`, `LLR-121` and their kind) raise no
  perspective of their own beyond the requirement they site.

### No re-attest window opened — verified against the machinery, not assumed

The cells land on Approved rows, so the classification was checked rather than
trusted. `Hat-Refs` is in `SPINE_TRACED_CELLS` at both tiers, and three
independent readers agree the record is untouched: `baseline_snapshot.
unanchored_findings` returns **0** (it asks about id presence and maturity, not
text), `committed_snapshot_findings` pins its comparison to the snapshot's own
WRITING commit so live moving on afterwards changes nothing, and
`staged_snapshot_findings` is keyed on a snapshot file being IN the commit — this
commit touches none. **`docs/archive/last_approved/` is deliberately NOT
reconciled here**: `baseline_snapshot`'s own header states that the snapshot
being behind live is the signal, and a slice that re-copied it would erase
exactly the evidence a sitting reads.

### The one consequence worth naming: seven new backlog-staleness warns

`backlog_staleness_findings` blames the SR registry by LINE, so inserting a
`hat_refs` line re-dates the whole row: five open WIs (`WI-455`, `WI-500`,
`WI-503`, `WI-508`, `WI-510`) now warn that a cited SR was "amended after the WI
row was last touched". Warn-only, never in the exit code, and each clears with a
content edit to the citing spec. It is not noise to route around — it is the same
granularity question **phase 5** has to answer, and it now has a measured
instance: an informative cell moving reads identically to a normative one moving,
because the clock is a `git blame` line time rather than the `split_changed_cells`
class split the amend-without-flip guard uses. Recorded for phase 5 rather than
patched here.

### Item 2, the writer — EXAMINED AND LEFT OWED, with the blocker named

The slice was authorised to take item 2 only if a small clean change would carry
the write instruction. It will not, and the reason is a real mismatch rather than
a size judgement. `{{HAT_QUESTIONS}}` has exactly one consumer —
`project-trajectory/prompts/dual-plan-planner.template.md` — whose output
contract is *"exactly one markdown table, one row per proposed WI"* with the
columns `Plan-WI | Title | Covers | Interfaces | Predecessors`, and whose
Perspectives section already directs the answer into `## Notes` as a Plan-WI or
an explicit no-finding. **That brief mints no spine row at all**, so a sentence
appended to `hats.brief_block` telling the session to fill `hat_refs` would ship,
into every adopter's planner brief, an instruction its own output contract makes
unfollowable. The session that actually mints SR and LLR rows reads the
`spine-authoring` skill instead — a different surface, with a three-way per-agent
fan-out under `gen_skills_index --check-agents`. Choosing between widening the
Plan-WI output contract and stating the obligation at the spine-authoring tier is
phase 2's design; it is not a one-liner, and guessing it would be worse than the
gap. Item 2 stays owed, now with its blocker written down.

### Gates

Registry-cell work only — no executable code changed, so the commit bar is the
bar (`session-protocol` §3), not the full suite.

- `python -m pytest -q -n auto -m smoke` — **1368 passed, 5 skipped in 55.45s**
  (inside the declared 60 s ceiling on this box; one box is one data point)
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=69e4a854 -->.
- `python project-trajectory/scripts/check_docs.py --root . --stale` — **OK,
  1009 doc(s), 1345 intra-repo link(s), 0 broken (1 orphan warning)**, exit 0
  <!-- fig: cmd="python project-trajectory/scripts/check_docs.py --root . --stale" rev=69e4a854 -->.
- `gen_trajectory.py --check` — dashboard **up to date**; `hat_refs` is not a
  rendered cell, so no surface regenerates for this slice.
  `gen_open_items.py --check` read STALE — **and it read STALE AT HEAD too**, so
  the regeneration folded in here is the previous commit's residue, not this
  slice's: the whole delta is one line, the baseline stamp
  `8848f6fb → 69e4a854`. It rides this commit because the pre-commit hook's
  `open-items` step is a hard gate and greening it by regenerating is the fix,
  where sanctioning the step would not be. What the regenerated view proves is
  the classification: with 63 edited rows in the tree it still renders **"0 spine
  row(s) owing a ratification or a re-attest, across 0 chain row change(s); 0
  row(s) drifted from the approved snapshot"**.
- **`docs/stage` re-derived**, and the hook is what caught it: the record's
  fingerprint is taken over the DECLARED derivation inputs, and the spine
  registries are two of them, so writing an informative cell invalidates the
  fingerprint while changing no derived value. `derive_stage.py --root .`
  re-stamps it — `DevStg-LLReqs`, every field byte-identical, only the hash and
  the as-of line move. Never hand-set (the record is derived), and the
  re-stamp is deliberate rather than a ratchet nudge: it names a real input
  change.
- `check_figures.py --root .` — every `fig:` marker in this fragment carries its
  provenance; the 58 standing warns are pre-existing and none is in this file.
- `python project-trajectory/scripts/trace.py --root . --strict` and
  `check_trajectory.py --root . --strict` both exit 1 on this tree AT HEAD as
  well (`69e4a854`), and the finding sets were DIFFED rather than eyeballed: this
  slice adds no finding to either beyond the seven staleness warns named above
  and the two advisory lines it improves. The two standing reds are the known
  `R-F WI-501` SpecRef carry-over and trace's **15 orphan findings** (integrity
  is 0) — the orphan debt the frontier is already paying down. Neither is this
  slice's, and neither is sanctioned to green it.
