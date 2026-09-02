# The blind minimal-map derivation — what came back (WI-508 slice 2)

_The two returns, the measured agreement between them, and the disclosures both
teams made. The question they were asked is
[`2026-08-25-blind-minimal-map-brief.md`](2026-08-25-blind-minimal-map-brief.md),
recorded before either ran. **Nothing here is adjudicated against the live
layout** — that is the alignment pass, a separate slice and the only role
permitted to read both sides._

> **STANDING CAVEAT — "recorded before either ran" is the authors' account, not
> a fact this repository can evidence.** Added 2026-09-02 (WI-569); the text
> below is unchanged.
>
> The brief and this record first appear in the SAME commit, `64e9bf2a`
> (2026-08-25), so nothing immutably fixed the question before the answers
> existed. The second defect — the instruction-context contamination that broke
> the brief's closed five-file input set — is disclosed by the teams themselves
> in §1 below, which is where a reader should start.
>
> Both defects push the convergence figure the same way, so the agreement
> measured here is an **upper bound**, not a corroboration. The full ruling,
> and why a sterile re-run was not commissioned, is the caveat on
> [`2026-08-25-blind-minimal-map-brief.md`](2026-08-25-blind-minimal-map-brief.md).

The two returns, verbatim as they were written:

- **Team A — outputs-backward:**
  [`2026-08-25-blind-derivation-a-outputs.md`](2026-08-25-blind-derivation-a-outputs.md)
  (24 modules in 6 layers)
- **Team B — obligations clustered by shared signal and failure mode:**
  [`2026-08-25-blind-derivation-b-obligations.md`](2026-08-25-blind-derivation-b-obligations.md)
  (23 modules in 4 bands)

Both derived over the same corpus: **75 SR rows, 27 SN rows, 4 boundary
crossings, 16 hats**. Both returned a complete forward assignment — every SR to
exactly one owning module, 75 assignments, no id assigned twice — which is what
makes the two maps comparable at all.

## 1. THE DISCLOSURE THAT COMES FIRST — blindness was not total, and both teams said so unprompted

Neither agent read one byte of this repository. Both stated it, and both stated
the same limitation on top of it, independently and without being asked:

> the harness injected a description of this repository into the agent's context
> **before the brief arrived** — the project instruction file, and for Team B a
> memory index as well — naming directories and several script filenames.

That is a real weakening of the contract and it is recorded here rather than
discovered later, because a validation exercise whose integrity claim is
overstated is worth less than one whose limits are known. What can be said
precisely:

- **File access was clean.** Both confined every read to the five-file pack by
  absolute path. Neither used a relative path, and both noted that a relative
  path would have landed inside the live repository, since that is the working
  directory.
- **The contamination is names, not structure.** Both checked their module names
  against the injected material and neither reproduced a filename as a module
  name. Team A additionally named four places where its map DIVERGES from what
  recall would have produced, each argued from requirement text.
- **Both refused the same shortcut.** The boundary registry's own `carries` cell
  enumerates delivered script names, and both teams recorded declining to use
  that enumeration as the module list — Team B noting it is the other axis's
  starting point, Team A that its 24-module map deliberately does not mirror it.

**What this costs the exercise, stated plainly:** convergence between A and B is
slightly less independent than it looks, because both saw the same injected
names. It is not worthless — the injected material is a file list, not a module
map or a design tier — but a future run of this method should strip the harness
context, not only the input set. That is a finding about the METHOD and it
belongs to the program, not to either team.

## 2. What each team produced

| | Team A (outputs-backward) | Team B (obligations-clustered) |
| --- | --- | --- |
| modules | **24**, in 6 layers | **23**, in 4 bands |
| mean SRs per module | 3.1 (max 7) | 3.3 (max 8) |
| modules owning no SR | **1** (`F5` Finding & Verdict Shape) | **1** (`M03` Finding & Severity Contract) |
| SRs resisting single ownership | **13** | **11** |
| requirement-level overlaps found | **13** | **14**, plus 5 need/frame obligations with no SR subject at all |

Each defended its count the same way and against the same temptation: a smaller
map is reachable by fusing, and both refused it in writing. Team A's argument is
that the six-way split the boundary registry hands over "reads better and scores
worse", because each of the six independently consumes the same five foundation
signals — six carriers × five behaviours is thirty implementations of five.
Team B's is that its count is held DOWN by three extracted shared stages rather
than by fusion, and that removing them yields "a smaller module count and a
strictly larger system".

## 3. Agreement, measured rather than eyeballed

The two ownership tables were compared as partitions of the same 75 ids. Over
all **2,775** unordered pairs of SRs, the two maps agree on whether the pair
shares a module in **97.2%** of cases (72 pairs together in both, 2,626 apart in
both; 33 together only in A, 44 only in B). The best one-to-one module
correspondence pairs **22 of A's 24 modules with 22 of B's 23** and places
**63 of 75 SRs (84.0%) identically**.

fig: derived="pairwise co-membership over all 2775 unordered pairs of the 75 SR ids, and a greedy best 1:1 module correspondence, computed from the two forward-assignment tables in the sibling records; the reproduction script is §7"

**The single most striking convergence is invisible to that arithmetic.** Team
A's `F5` and Team B's `M03` cannot be matched by SR overlap because **both own
zero SRs** — and they are the same module. Two teams, two opposite axes, each
independently concluded that the system needs one home for *the shape of a
finding, its severity class, strict-mode escalation, vacuity, and how findings
compose into an exit code* — and each independently found that **no requirement
states it**. Team A counts thirteen rows restating the contract; Team B counts
eleven, and points at `SR-158`'s own acceptance conceding the hole in the
corpus's own words: *"A class whose severity is stated at no declaration site is
undeclared, and this row is unsatisfied until it is declared there."*

The one module with no counterpart at all is Team A's `F3` (Repository History
Facts) — every question answered by reading version control, asked once. Team B
distributed those reads. Team A flagged its own thin ownership (one row, nine
consumers) as a corpus finding of the same shape as `F5`.

### The twelve SRs the two maps place differently — listed, not ruled

Each is a place the requirements genuinely underdetermine the boundary, which
is what an axis-diverse pair is for. **These are inputs to the adjudication, not
findings against either map.**

| SR | Team A | Team B | the question underneath |
| --- | --- | --- | --- |
| `SR-006` | step planner | harness bar | is the bar a planner that calls checks, or the checks' own composer? |
| `SR-015` | measurement verdicts | spine rule verdict | does an invariant live with its checker, or with the thing it measures? |
| `SR-019`, `SR-020` | enforcement floor | sensitive-content guard | is the hook the module, or the classifier? |
| `SR-024` | coverage & provenance | registry carrier | is case expansion a coverage act or a row-writing act? |
| `SR-033` | measurement verdicts | state view composition | does a warn-tier budget belong to the comparator or to the surface that shows it? |
| `SR-043` | enforcement floor | run supervision | grouped by moment (a verdict to a session) or by failure direction (this one fails OPEN)? |
| `SR-111` | history facts | package manifest | does the scaffold write a value it did not compute? |
| `SR-113` | scaffold & re-sync | sensitive-content guard | does the floor arm itself, or does setup arm it? |
| `SR-163` | spine rule checks | package manifest | **the inventory, or the join?** |
| `SR-173` | lane & seam | derivation integrity | who owns the regeneration order — the only permitted invoker, or the artifact graph? |
| `SR-174` | lane & seam | registry carrier | who owns identity — the actor allowed to allocate, or the id space? |

`SR-163` is worth naming twice: it is **this program's own traced requirement**,
and the two teams split on exactly the seam slice 1 wrote into the registry —
`LLR-203` (the inventory as the coverage universe) against `LLR-204` (the join
and its declared policy). Independent confirmation that the decomposition cut
along a real line, arrived at by two agents that could not see it.

## 4. What both teams found about the REQUIREMENTS — the side-effect worth as much as the maps

Convergent findings, each reached from both axes independently:

1. **The finding/severity/exit contract has no subject.** Restated in 11–13 rows
   (both lists include `SR-149`, `SR-150`, `SR-157`, `SR-158`, `SR-159`,
   `SR-162`, `SR-163`, `SR-167`, `SR-180`, `SR-181`, `SR-182`), owned by none.
   Team B drafts the missing row's shape.
2. **Derived-copy currency is stated seven or eight times under five different
   names** — freshness, drift, staleness, byte-identical, structural divergence
   (`SR-070`, `SR-022`, `SR-112`, `SR-049`, `SR-146`, `SR-158`, `SR-178`,
   `SR-166`). Both made it one module with many callers; Team A calls it the
   single largest total-behaviour reduction in its map.
3. **Refuse-rather-than-default is stated five to eleven times**, the only real
   variable being the fail-safe direction, which is a per-caller parameter.
4. **The interpreter probe is duplicated BY EXPLICIT RULING** — `SR-160` says so
   in its own text ("it spans two audiences … and parts along that line"). Both
   teams flag it as one behaviour with two callers.
5. **Sensitive-class scanning has already diverged in the field**, and the
   corpus says so: `SR-176` records that the redaction set lacks the PII classes
   the gate adds. Both cite it as the strongest available evidence that this
   overlap class is not theoretical.
6. **Measured-value-versus-baseline is one pipeline with four postures**
   (`SR-167`, `SR-182`, `SR-177`, `SR-033`); the posture belongs in a declared
   cell, not in four homes.
7. **Two rows state one provenance-record shape** — `SR-165`'s own text calls
   itself "the `SR-161` form applied to the partition instead of the perspective
   set".

Team B's axis additionally surfaced what a per-capability decomposition
systematically misses — a clause everywhere, a subject nowhere: **"every degrade
is named, never silent"** (8 rows), **vacuity of an absent optional input** (8
rows), **all-or-nothing durable writing** (5 rows, 5 mechanisms), and **the
pair-level claim** that the local floor plus the hosted re-run together make
(`SR-019` states one half, `SR-152` the other, and no row states the claim). It
also lists five obligations stated in a need or the frame with **no SR subject
at all**, and notes that the boundary registry's own `carries` note concedes the
gap by minting a "sixth capability" for package-wide properties — omitting
`SR-163` and `SR-166` from that class.

## 5. What is NOT concluded here

No module moves. No cell moves. No consolidation is filed off this record. The
maps are one half of a diff whose other half has not been read yet, and every
divergence — between the two maps, or between either map and the live layout —
is a finding to be adjudicated with the legacy side's own recorded rationale
read FIRST. The requirement-level findings in §4 are the exception only in that
they are about the corpus both teams DID read; they still enter the program as
candidates, not as work.

## 6. What the next slice takes from here

The alignment pass reads both sides and builds the three-bucket map — matched /
present-only-in-live / present-only-in-derived. Two things it should carry in:

- **Use both derived maps, not one.** The 12 divergences of §3 mark where the
  requirements underdetermine the boundary; a live divergence at one of those
  twelve is weaker evidence than a live divergence where A and B agree.
- **The §4 findings are about the SPINE, not the layout**, and several are
  candidates for a minted requirement rather than a consolidation WI. They
  should not be filed as module work.

## 7. Reproducing §3's figures

```python
import itertools, re
from pathlib import Path
ROW = re.compile(r"^\|\s*(SR-\d+)\s*\|\s*([^|]+?)\s*\|\s*(SR-\d+)?\s*\|\s*([^|]*?)\s*\|\s*$")

def load(path, start, end):
    inside, out = False, {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if start in line: inside = True; continue
        if inside and end in line: break
        if not inside: continue
        m = ROW.match(line)
        if not m: continue
        sr1, mod1, sr2, mod2 = m.groups()
        out[sr1] = mod1.split()[0]
        if sr2: out[sr2] = mod2.split()[0]
    return out

a = load("2026-08-25-blind-derivation-a-outputs.md",
         "## Forward: every SR to exactly one owning module", "Count check")
b = load("2026-08-25-blind-derivation-b-obligations.md",
         "### Every SR to exactly one owning module", "**Count check")
common = sorted(set(a) & set(b))
agree = sum(1 for x, y in itertools.combinations(common, 2)
            if (a[x] == a[y]) == (b[x] == b[y]))
total = len(common) * (len(common) - 1) // 2
print(agree, total, 100.0 * agree / total)
```

The best one-to-one correspondence is the greedy maximum-overlap pairing over
the same two tables; the twelve rows of §3 are the ids it cannot place.
