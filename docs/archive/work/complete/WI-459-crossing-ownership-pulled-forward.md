+++
id = "WI-459"
title = "Crossing ownership, pulled forward out of sitting 3 (decision 8): answer for each of B-01/02/04/05/06/07 which SRs and IFs realize it and who owns each gap - now that the deferral's first condition is MET (Boundary-Refs populated on all 64 rows). The measured answer is a FINDING, not a formality: B-05 carries 55 of 70 references (79%) while B-06 and B-07 carry one each, and FOUR of six crossings (B-01, B-02, B-06, B-07) are realized by no interface row at all. Decide whether B-05 is under-decomposed or the imbalance is real - the registry does not distinguish those readings today, and the difference decides whether the re-tier is finished."
workstream = "process"
sr_refs = ["SR-137", "SR-139"]
needs = ["WI-458"]
buildtier = "strong"
safety_class = "adjudication"
priority = 2
+++

## Deliverable

Closed DONE 2026-08-15. The six-crossing table regenerated on the current tree
(65 boundary references across 59 SR rows, 0 uncovered: B-01 5 / B-02 2 /
B-04 6 / **B-05 50 (77%)** / B-06 1 / B-07 1, with 0 / 0 / 1 / 7 / 0 / 0
realizing interface rows) and recorded per crossing with its SR list and IF
list. The recorded figures were stale AND off by one row; re-deriving found
that `WI-458`'s six removed boundary references came **entirely** out of B-05,
which is the mechanical support `OI-29`'s ruling (b) did not have. Four
verdicts: B-01 an interface SHOULD realize it, owner `SR-019`/`SR-020` (the
port exists as IF-040/042/043's hooks but models the internal call, never the
contract git holds it to); B-02 NO interface should realize it today, owner
`SR-140` if and when its attestation anchor ships; B-06 and B-07 an interface
SHOULD realize each, owners `SR-151` and `SR-152` (no IF row has a CI workflow
at either endpoint). Fifth finding recorded: B-04 is only half realized and no
advisory reports it. Sitting-3 §0.3 ledger row 8 marked closed-by-this-row. The
IF-side re-key stays D-3's and is stated, not executed. Full verdict text in
this spec's `## Close`; reasoning in `docs/log.md` entry `2026-08-15f`. All of
it PROVISIONAL under the 2026-08-15 charge-through; no Status or `approval`
cell moved.

## Context

Sitting-3 ledger decision 8 was ruled **DEFERRED** (`2026-08-14d`), re-landing
by name *"after slice 2 populates `Boundary-Refs` + the D-3 re-key."* It asks
verbatim: *"for each of B-01/02/04/05/06/07, which SRs and IFs realize it, and
who owns closing each gap."*

- **Condition 1 is MET** — `Boundary-Refs` is populated on all 64 SR rows
  (0 uncovered), which is exactly the state the deferral named.
- **Condition 2 is NOT** — the IF tie-back re-key is D-3's, still unexecuted on
  the `wi455-architecture-retirement` lane. That is why this row is scoped to
  the **SR side plus the measurement**, and hands the IF side to D-3 rather
  than racing it.

**The owner expected decision 8 might "effectively dissolve in the full
re-tier," and recorded it so it would re-land either way. It has not
dissolved.** Measured on merged trunk:

| Crossing | SRs referencing it | Interfaces realizing it |
|---|---|---|
| B-01 | 5 | **0** |
| B-02 | 2 | **0** |
| **B-05** | **55** | 7 |
| B-04 | 6 | 1 |
| B-06 | **1** | **0** |
| B-07 | **1** | **0** |

## Why this is pulled OUT of sitting 3 rather than left in it

This is a **tiering and grouping** question — the re-tier's own stated purpose —
not a vocabulary or ratification question, which is what the rest of sitting 3
is (decisions 5/6/7 are the D-9 + D12 status program, ruled to run as one
sequence with the ratification wave). Leaving it there files the sharpest
re-tier finding under a sitting about status words.

**Pulling it forward REMOVES work from sitting 3; it adds none.** Nothing here
flips a Status, closes an enum, or touches the ratification wave.

## The question to rule, and it is genuinely open both ways

A partition in which one cell holds four fifths of the population is not
classifying — it is a default with five exceptions. Two readings, and the
registry does not distinguish them:

- **B-05 is under-decomposed.** Supporting evidence: it already required a
  *sixth* bucket, minted at ruling `2026-08-14c` (the "package-wide property"
  class), to absorb four rows that fit none of its five. A bucket set that
  needed widening once may need it again.
- **The frame is right and the imbalance is real.** This repo's product
  genuinely is one package crossing one boundary; the other five crossings are
  thin because the repo is thin there, and forcing balance would manufacture
  structure.

Raised for the owner as `OI-29`.

## Done-when

- The six-row table above is regenerated at execution time (do not trust these
  figures — re-derive) and recorded with each crossing's SR list and IF list.
- The B-05 question is ruled: under-decomposed (with the decomposition) or real
  (with the reason stated, so a later reader does not re-open it).
- Each of B-01, B-02, B-06 and B-07 has a named owner for its missing
  realization, or a recorded statement that no interface should realize it.
- The IF-side re-key stays D-3's; this row states what D-3 must produce, and
  does not execute it.
- Sitting 3's §0.3 ledger row 8 is marked closed-by-this-row, so the sitting
  does not carry a decision that has already been made.

## Close

**Closed DONE 2026-08-15.** Reasoning and the full verdict text:
[`docs/log.md`](../../../log.md), entry `2026-08-15f`. **Everything here is
PROVISIONAL** — executed under the owner's 2026-08-15 charge-through, and
overturnable at the review sitting. No Status, `approval` or attestation cell
moved.

### 1. The table, REGENERATED on the current tree

Re-derived from `docs/requirements/system-requirements.toml`
(`boundary_refs`) and `docs/requirements/interfaces.toml`
(`interface_from_external` / `interface_to_external`) at `SN=27 SR=59 LLR=154
TC=149`, **65 boundary references across 59 rows, 0 rows uncovered**:

| Crossing | Dir | SRs | share | IFs | The SRs | The IFs |
|---|---|---|---|---|---|---|
| B-01 | in | 5 | 8% | **0** | SR-017 SR-018 SR-019 SR-020 SR-137 | — |
| B-02 | in | 2 | 3% | **0** | SR-139 SR-140 | — |
| B-04 | out | 6 | 9% | 1 | SR-017 SR-018 SR-019 SR-020 SR-043 SR-137 | IF-020 |
| **B-05** | out | **50** | **77%** | 7 | SR-006 007 009 010 011 015 022 024 026 027 028 031 032 033 034 035 036 040 046 049 052 053 054 070 111 112 113 114 129 138 139 144 146 147 148 149 150 154 155 156 157 158 159 160 161 162 163 164 165 166 | IF-013 IF-014 IF-015 IF-016 IF-017 IF-018 IF-048 |
| B-06 | in | 1 | 2% | **0** | SR-151 | — |
| B-07 | out | 1 | 2% | **0** | SR-152 | — |

**The figures in this spec's `## Context` and in `OI-29` were stale and are
superseded** — they read `SR=64`, 70 references, B-05 = 55 (79%). Measured at
`cc43a5d4~1` (the state those were taken against) the truth was 65 rows / 71
references / B-05 = 56; the recorded table was off by one row. Re-deriving was
the right instruction.

**The delta WI-458 made is itself the finding.** Between `cc43a5d4~1` and
HEAD the SR layer lost 6 rows and 6 boundary references — **all six came out of
B-05.** B-01, B-02, B-04, B-06 and B-07 are byte-identical before and after:
5 / 2 / 6 / 1 / 1, unchanged. A demotion pass aimed at mis-tiered rows drained
the large crossing and did not touch a single thin one.

### 2. The B-05 question — RULED, and the ruling now has mechanical support

`OI-29` was **RULED (b) by the owner in session, 2026-08-15: the imbalance is
REAL**, because the template package *is* the product — *"I expect a
significant amount of SR definition to be output to the template package which
is the entire point of this development space."* The ruling carries two riders
in the owner's own words: later decomposition and churn **may** re-balance the
distribution, and the premise weakens if that outflow to the package ever
stops. Not re-opened here; recorded so a later reader does not re-litigate it.

What this row adds is evidence the ruling did not have: the mechanical test
`OI-29` itself proposed — *"a category that keeps needing new cells to hold its
exceptions is describing one thing, not five"* — has now been run once, in the
opposite direction, by WI-458. Six references left B-05 and none left anywhere
else. B-05 absorbs and sheds; the other five crossings are inert because the
repo is thin there. That is (b)'s prediction, observed.

### 3. The four unrealized crossings — one verdict each

Four crossings are realized by no interface row, which `trace.py --strict`
reports as an advisory (*"boundary crossing(s) realized by NO interface row:
B-01, B-02, B-06, B-07 — decision 6's question, deferred by ruling; reported,
never gated"*). **The `owner` cell lands on the IF row, so every "owner" named
below is the SR that the realizing row must name in its `owner` cell.**

**B-01 — governed writes in. AN INTERFACE SHOULD REALIZE IT. Owner: `SR-019`
(commit half) and `SR-020` (push half).** The crossing's own text names its
port — *"admitted ONLY through the git hook floor"* — and the port exists in
the registry three times over: `IF-040` (pre-commit → check), `IF-042`
(pre-commit → trace), `IF-043` (pre-push → check_privacy). Every one of them
models the hook's INTERNAL call (hook → script) and none models the contract
git holds it to, which is the crossing itself: git invokes the hook, a nonzero
exit refuses the write. So the gap is not a missing surface, it is a missing
*facing* — the rows describe the floor's composition and never its admission.
The mechanical confirmation that this is the right attribution is that those
three rows already carry `owner = SR-019 / SR-019 / SR-020`, and SR-019 and
SR-020 are exactly two of the five SRs that name B-01. **Recommended shape for
D-3, smallest first:** add `interface_from_external = "B-01"` **and**
`interface_to_external = "B-04"` to IF-040/IF-042/IF-043 — one crossing pair,
because the hook floor admits the write and emits the verdict in the same act,
which is precisely what `external.toml` records when it puts *"the verdict
halves of BIF-006 and BIF-026"* in B-04. The alternative, if D-3 judges that a
row with two internal endpoints must not carry a tie-back, is one new
`hooks/pre-commit <-> external:git` row and one `hooks/pre-push <-> external:git`
row. **This row does not execute either; D-3 does.**

**B-02 — authority in. NO INTERFACE SHOULD REALIZE IT TODAY, and the condition
under which that changes is named. Conditional owner: `SR-140`.** Authority —
rulings, attestations, Status flips — has no port of its own. It enters as
CONTENT on B-01's write path: a human edits a Status cell and commits, and the
hook floor admits that write exactly as it admits any other. A crossing the
frame declares to carry *meaning* rather than *mechanism* is realized by no
interface without that being a gap, and minting a row for it would manufacture
a surface that does not exist. The condition that would change the answer is
concrete and already on the books: `SR-140` requires each acceptance to be
recorded on the accepted artifact's own row (commit + digest of the normative
cells + transition + acting reviewer). **If and when that recorder/validator
ships, its contract IS an admission surface for authority** — it can refuse an
attestation whose digest does not match — and at that moment B-02 gains a
realizing row owned by `SR-140`. `SR-139` and `SR-140` are both `Planned`
today, which is the honest reason the row cannot be authored now: there is
nothing to state a contract about.

**B-06 — hosted CI trigger in. AN INTERFACE SHOULD REALIZE IT. Owner:
`SR-151`.** No IF row in the registry has a CI workflow at either endpoint —
not `.github/workflows/test.yml`, not `.github/workflows/canary.yml`, not the
shipped `project-trajectory/ci/check.yml`. The crossing is real (this repo's
hosted matrix runs on every push) and it is simply unmodelled. The realizing
row is the workflow's trigger contract: which events fire it, what OS × Python
matrix it declares, and which harness entry point at which tier each moment
maps to via `docs/stack.ini [ci-tiers]`. **One strain surfaced rather than
smoothed over, for the sitting:** `SR-151`'s text is written about *"the
shipped reference CI workflow"* — delivered content, which is B-05's
description — while its `boundary_refs` names only B-06. Both readings are
defensible (the artifact is delivered; the observable is at the CI crossing)
and the cell is not touched here. It is flagged so the sitting can rule it, and
`SR-151` is `Draft`, so nothing is attested either way.

**B-07 — hosted CI verdict out. AN INTERFACE SHOULD REALIZE IT. Owner:
`SR-152`.** Same absence, other direction, and it is the load-bearing half:
`SR-019` states in its own requirement text that the local hook floor is
bypassable (`git commit --no-verify`) and therefore *"discharges 'no unchecked
write enters governed state' only as a PAIR with the hosted re-run of the same
bar (SR-151/SR-152)"*. So B-07 is not a decorative crossing — it is the
backstop half of B-01's own validity argument, and it is currently realized by
nothing. The realizing row is the job-verdict contract: the harness's exit
carried through to the job's, plus a step log naming every step's outcome with
no silently skipped required step. `SR-152` is `Draft`.

### 4. A fifth finding, recorded because the sweep produced it

**B-04 is only HALF realized, and no advisory reports that**, because
`trace.py` asks whether a crossing has *any* realizing row, never whether it
has one per thing it carries. `B-04.carries` names two: *"hook-floor
accept/reject **and** subagent_gate PreToolUse allow/deny."* Only the second
has a row (`IF-020`). The first is the same missing facing as B-01's, and the
B-01 recommendation above closes both at once — which is why they are one
recommendation and not two.

Related and left for D-3 rather than acted on: the interface rework's new
`external:` markers make the candidate set mechanical for the first time. 13
rows carry an `external:` endpoint; 8 of them already tie back (7 to B-05, 1 to
B-04) and **5 do not** — `IF-032` (check_privacy ↔ external:git), `IF-036`
(check_vendored ↔ external:upstream docs), `IF-041` (agent_session ↔ external:agent
CLI), `IF-080` and `IF-081` (integrate / trunk_step ↔ external:downstream
adopter). IF-080 and IF-081 look like plain B-05 omissions. The other three are
judgement calls about whether consuming an external tool is a crossing of this
system's boundary at all. **D-3's, stated here so the re-key has the list.**

### 5. What D-3 must produce (this row does not execute it)

The IF-side re-key belongs to the `wi455-architecture-retirement` lane. From
this row it inherits, as direction and not as instruction: tie-backs for B-01
and B-04's hook-floor half on IF-040/IF-042/IF-043 (or two new external-facing
hook rows); two new rows for B-06 and B-07 owned by SR-151 and SR-152; the
five untied `external:` rows adjudicated; and B-02 deliberately left with no
row, carrying the SR-140 condition as its recorded reason so the next reader
does not file it as an omission.

**Done-when, against the spec:** table regenerated and recorded with per-crossing
SR and IF lists ✓; the B-05 question ruled and the reason recorded ✓ (`OI-29`
(b), plus the WI-458 delta as new supporting evidence); each of B-01/B-02/B-06/
B-07 carries a named owner or a recorded statement that no interface should
realize it ✓; the IF-side re-key left to D-3 with its output stated ✓; sitting
3's §0.3 ledger row 8 marked closed-by-this-row ✓.
