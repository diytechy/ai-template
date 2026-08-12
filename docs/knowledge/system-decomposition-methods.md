# System decomposition methods: partitioning system I/O into components

**retrieved:** 2026-08-12. This pack answers the open question in
[`docs/repo-lock.md`](../repo-lock.md) §0/§8.6 ("work the partition as an
*optimization over system I/O*, present it; the ruling stays the owner's") and
the owner's framing: lay out the system's inputs/outputs first, then break
that into components with internal signals, minimizing what crosses a
boundary. It surveys the principled decomposition methods and names the one
that fits this kit's registries — `components.csv` (`CMP-###`, the boundary)
and `interfaces.csv` (`IF-###`, every signal typed discrete vs variable, with
an `SR-Refs` column already joining each interface to its requirements). This
is advisory input to that ruling, not the ruling itself.

## Recommendation

Treat the existing `interfaces.csv` `SR-Refs` join as a **bipartite
incidence structure** — each SR (or LLR) is a *hyperedge* over the signals
(candidate `IF-###` rows, or finer sub-signals) it reads or writes — and
search for a partition of signals into `CMP` clusters that **minimizes the
number of requirements whose hyperedge is cut** (spans more than one
cluster). This is the same object as an **N2 diagram** (every candidate
signal on the diagonal, a requirement's touch an off-diagonal mark) and the
same objective as classical **DSM clustering** (Thebeau/IGTA): "lay out I/O,
then cluster to make the off-diagonal sparse outside blocks" *is* N2 +
DSM-clustering, not a metaphor for it. Prefer the **hypergraph-cut** framing
(§1 below) over plain-graph Newman modularity (§3): modularity needs a
resolution parameter and degrades on small, sparse graphs like this kit's
(~100 rows), while a hypergraph cut is exactly "how many `IF-###` rows would
this partition force" — the quantity the owner wants small. Run it as a
**ranker over candidate partitions**, never an autonomous decision-maker: a
human still picks the cluster count, names each cluster, and can override
the math on grounds it cannot see (below).

## The objective functions

### 1. Hypergraph cut / connectivity — the primary fit

Model signals as nodes and each requirement as a hyperedge `e` over the
signals it touches. The standard VLSI/EDA **connectivity metric**
(Fiduccia–Mattheyses, hMETIS) is

```
cost = Σ_e  w_e · (λ(e) − 1)
```

`λ(e)` = number of distinct clusters hyperedge `e` spans; `w_e` an optional
weight (1, or the SR's priority). `λ(e) − 1` is exactly the number of
cross-boundary interfaces that requirement forces into existence, so
minimizing `cost` directly minimizes interface-registry size and hidden
coupling. Don't collapse a hyperedge to pairwise edges first — it distorts
the cost (see "Failed or bounded approaches").

### 2. DSM clustering — Thebeau / IGTA `TotalCost`

The classical product-architecture form, if you first collapse the incidence
matrix to a signal×signal DSM (edge weight = shared-requirement count).
Thebeau (2001) formalized modularization as minimizing:

```
TotalCost = Σ_k IntraClusterCost_k + ExtraClusterCost
IntraClusterCost_k = size_k^pow_cc · Σ_{i,j ∈ cluster k} DSM(i,j)
ExtraClusterCost   = N^pow_cc      · Σ_{i,j in different clusters} DSM(i,j)
```

`N` = total signals; `pow_cc` (~1–2) penalizes large clusters so the search
doesn't collapse to one giant cluster (secondary sources agree on this shape
but vary on exact exponent placement — verify against a primary
implementation before using specific values numerically). IGTA/IGTA+ optimize
this by repeatedly re-bidding one element into its best-fit cluster — the
same stochastic hill-climb the sketch below uses. Pairwise special case of
objective 1; prefer 1 whenever a requirement spans 3+ signals (the common
case here).

### 3. Graph modularity — why it is *not* the default here

```
Q = (1/2m) Σ_vw [A_vw − k_v·k_w / 2m] · δ(c_v, c_w)
```

`A` = adjacency matrix, `k_v` = node `v`'s degree, `m` = edge count, `δ` = 1
iff `v,w` share a cluster. Has a spectral solver (leading eigenvector of
`B = A − kk^T/2m`) and a well-known failure mode, the **resolution limit**:
it cannot resolve communities below a scale set by the *whole* graph's edge
count, merging distinct small clusters on a graph this size (Fortunato &
Barthélemy) — and it discards the hyperedge structure a multi-signal
requirement carries. Fine as a sanity metric on a chosen partition, not as
the search objective.

### 4. Normalized cut — when cluster count is fixed

`NCut(A,B) = cut(A,B)/assoc(A,V) + cut(A,B)/assoc(B,V)`, relaxing to the
eigenproblem `L x = λ D x` (`L = D − W`, the Laplacian). Sidesteps
modularity's resolution limit but keeps its graph-only caveat; useful when a
fixed, size-balanced cluster count matters more than a minimum interface
count.

### 5. Axiomatic Design's diagonal/triangular test — grading, not searching

Suh's independence axiom **grades a partition after the fact**; it is not a
search objective. Build the requirement×signal (FR×DP) design matrix: an
*uncoupled* design is diagonal (each requirement depends on one cluster —
best), a *decoupled* design is triangular (a sequential order fixes it —
acceptable), a *coupled* design is full (every requirement touches every
cluster — cannot be changed one piece at a time). Run it on any candidate
partition as a check: does reordering clusters make the matrix
block-triangular?

### 6. Coupling/cohesion (fan-in/fan-out) — a tie-break metric

Classical structured-design coupling, useful to break ties between
equal-cut-cost partitions — a per-component form from one industrial
N2-derived optimizer: `Coupling(component) = 1 − 1/(d_i + 2·c_i + d_o +
2·c_o + w + r)` (`d`=data params, `c`=control params, `i/o`=in/out,
`w`=fan-out, `r`=fan-in; lower is better, sum over components). Discrete-
vs-variable signal typing (the OI-14 narrowing) is orthogonal to all six
objectives — it constrains what an `IF` row's `Contract` cell says, not
which side of a boundary a signal belongs on.

## A stdlib-only proposer (sketch)

Given `signals` (candidate `IF`/sub-signal ids) and `requirements` (SR/LLR id
→ signal ids touched, read off `interfaces.csv`'s `SR-Refs` inverted),
propose a `k`-cluster partition by stochastic hill-climbing on objective 1.
No dependency beyond `random`.

```python
import random

def cut_cost(assign: dict, requirements: dict) -> int:
    """Sum over requirements of (distinct clusters touched - 1)."""
    cost = 0
    for sig_ids in requirements.values():          # SR-ID -> {signal ids}
        cost += len({assign[s] for s in sig_ids}) - 1
    return cost

def propose_partition(signals, requirements, k, iters=20000, seed=0):
    """Thebeau/IGTA-style stochastic hill-climb, hypergraph-cut objective.
    signals: list of signal ids. requirements: SR-ID -> set(signal ids).
    Returns (best_assignment, best_cost); caller sweeps k and reruns seeds."""
    rng = random.Random(seed)
    sig_list = list(signals)
    assign = {s: rng.randrange(k) for s in sig_list}
    best_cost = cut_cost(assign, requirements)
    best = dict(assign)
    for _ in range(iters):
        s = rng.choice(sig_list)
        old, new = assign[s], rng.randrange(k)
        if new == old:
            continue
        assign[s] = new
        cost = cut_cost(assign, requirements)
        if cost <= best_cost:            # accept sideways moves off plateaus
            if cost < best_cost:
                best_cost, best = cost, dict(assign)
        else:
            assign[s] = old              # revert the worsening move
    return best, best_cost

# Caller sweeps k and several seeds, keeps the lowest cost per k, and hands
# the human a small (k, cost) shortlist — never auto-commits to components.csv.
```

Cheap enough — `O(Σ|requirement signal-sets|)` per evaluation — for
thousands of iterations and several restarts in well under a second at this
kit's registry sizes; no need for `scipy`/`networkx`/METIS bindings.

## What stays human judgment

- **Cluster count `k`.** The math reports cost across a swept range; it does
  not pick "the right" number of components — the same resolution-limit
  problem as §3, made explicit instead of hidden in a default.
- **Naming and meaning.** A minimum-cut partition is unlabeled signal groups;
  assigning `CMP-###` names, `Category`, `Notes` is a semantic act.
- **Volatility (Parnas).** Information-hiding decomposition groups by *what
  is likely to change together*, not by what co-occurs in today's
  requirements — a structurally optimal cut can still split a design
  decision that changes as a unit; only a human holds that judgment.
- **Signal granularity.** Whether "one signal" is a whole `IF` row's
  contract or one field/flag/exit-code within it is a modeling choice made
  before the matrix exists, not something the algorithm derives.
- **Non-structural constraints.** Team ownership, deployment/procurement
  boundaries, existing `PartOf` nesting, and physical components can
  override a lower-cost cut for reasons outside the matrix.
- **Ties and local optima.** The problem is NP-hard (partitions grow as a
  Bell number); the hill-climb finds *a* good partition, not provably *the*
  best. Per `docs/repo-lock.md` §0 the partition itself "stays the owner's"
  regardless of what a proposer scores best.

## Failed or bounded approaches

- **LLM freestyle decomposition with no scored objective.** LLM+DSM-objective
  work (`arXiv:2604.28018`) reaches near-reference partitions within ~30
  iterations *only when the objective is explicit* — and found that adding
  domain knowledge to the prompt **impairs** performance on complex DSMs (a
  semantic-alignment mismatch), a concrete instance of the failure mode the
  owner is trying to avoid by asking for a mathematical objective.
- **Clique-expanding a hyperedge before clustering** (turning each
  multi-signal requirement into pairwise DSM edges to reuse plain-graph
  tools) distorts the true cut cost — use a native hypergraph objective
  (§1) or an FM/hMETIS-family algorithm instead.
- **Raw modularity maximization as the default** — its resolution limit
  merges genuinely distinct small clusters at this graph size, and it
  discards the hyperedge structure this data actually has.
- **Treating the proposer's output as final.** Every method above ranks
  candidates; it does not decide — "what stays human judgment" above is
  most of the actual decision, not optional cleanup.

## Sources (retrieved 2026-08-12)

- Thebeau, R. (2001), *Knowledge Management of System Interfaces and
  Interactions for Product Development Processes*, MIT SM thesis — the
  `TotalCost`/IGTA objective. Implementation: [dsmclustering](https://github.com/davidelasi/dsmclustering);
  write-up: [Sookocheff, simulated annealing](https://sookocheff.com/post/dsm/clustering-a-dsm-using-simulated-annealing/).
- Borjesson & Hölttä-Otto, *Improved Clustering Algorithm for Design
  Structure Matrix* (IGTA+). [ResearchGate](https://www.researchgate.net/publication/267489785_Improved_Clustering_Algorithm_for_Design_Structure_Matrix).
- Yu, Wei et al. (2013), *A module generation algorithm for product
  architecture based on component interactions and strategic drivers*,
  Research in Engineering Design — `IntraClusterCost`/`ExtraClusterCost`.
  [Springer](https://link.springer.com/article/10.1007/s00163-013-0164-2).
- *Recovery of Architecture Module Views using an Optimized Algorithm Based
  on Design Structure Matrices*. [arXiv:1709.07538](https://arxiv.org/pdf/1709.07538).
- *Design Structure Matrix Modularization with Large Language Models*.
  [arXiv:2604.28018](https://arxiv.org/html/2604.28018) — LLM+objective
  hybrid; the domain-knowledge-impairs-complex-DSM finding.
- Girvan & Newman (2002), *Community structure in social and biological
  networks*, PNAS 99(12):7821-7826, [doi](https://www.pnas.org/doi/10.1073/pnas.122653799);
  Newman (2006), *Modularity and community structure in networks*, PNAS
  103(23):8577-8582, [doi](https://www.pnas.org/doi/10.1073/pnas.0601602103) —
  the `Q` formula and its spectral solver; also [Wikipedia, Modularity (networks)](https://en.wikipedia.org/wiki/Modularity_(networks)).
- Fortunato & Barthélemy (2007), *Resolution limit in community detection*,
  PNAS 104(1):36-41, [doi](https://www.pnas.org/doi/10.1073/pnas.0605965104).
- Shi & Malik (2000), *Normalized Cuts and Image Segmentation*, IEEE TPAMI
  22(8):888-905. Walkthroughs: [CMU 10-701](https://www.cs.cmu.edu/~aarti/Class/10701/slides/Lecture21_2.pdf),
  [York EECS4414](https://www.eecs.yorku.ca/~papaggel/courses/eecs4414/docs/lectures/07-spectral.pdf).
- Parnas, D.L. (1972), *On the Criteria To Be Used in Decomposing Systems
  into Modules*, CACM 15(12):1053-1058, [doi](https://dl.acm.org/doi/10.1145/361598.361623);
  summary: [the morning paper](https://blog.acolyer.org/2016/09/05/on-the-criteria-to-be-used-in-decomposing-systems-into-modules/).
- Suh, N.P. (1990), *The Principles of Design*, Oxford University Press —
  the independence axiom and the diagonal/triangular/coupled design matrix.
  Applied treatment: [NASA, Axiomatic Design of Space Life Support Systems](https://ntrs.nasa.gov/api/citations/20170010336/downloads/20170010336.pdf).
- NASA, *Systems Engineering Handbook* (SP-2016-6105 Rev2) — the N2 diagram
  method, "lay out I/O, then decompose recursively."
  [PDF](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf).
- Danilovic & Browning (2007), *Managing complex product development
  projects with design structure matrices and domain mapping matrices* — the
  Domain Mapping Matrix, the bipartite two-domain form this kit's
  signal×requirement incidence instantiates.
  [PDF](https://web.mit.edu/deweck/Public/SDM/Danilovic_Browning_MDM_2007.pdf).
- Papa & Markov, *Hypergraph Partitioning and Clustering* — survey covering
  Kernighan-Lin/Fiduccia-Mattheyses, the `λ−1` connectivity metric, and
  clique-expansion distortion. [PDF](https://web.eecs.umich.edu/~imarkov/pubs/book/part_survey.pdf).
- Samares Engineering, *Coupling optimization of logical architecture using
  genetic algorithm* — an N2-derived coupling metric optimized by GA, the
  closest published analog to "lay out I/O, then optimize the breakdown."
  [Blog post](https://www.samares-engineering.com/en/2020/07/31/part-5-coupling-optimization-of-logical-architecture-using-genetic-algorithm/).
