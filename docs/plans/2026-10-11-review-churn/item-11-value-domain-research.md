<!-- Provenance: research sub-agent (Claude Opus 5.5), 2026-10-12, for F-call 7 of the review-churn plan (revision 15). Sources consulted: Minsky's "Effective ML Revisited" (Jane Street blog), Harper's "Boolean Blindness" (Existential Type), King's "Parse, don't validate" (her blog), Heitmeyer's 2010 Marktoberdorf SCR slides (NRL, text extracted), bibliographic records for Heninger 1980, Heitmeyer/Jeffords/Labaw 1996, Parnas & Madey 1995, Steward 1981, Eppinger & Browning 2012, Sullivan et al. 2001, MacCormack et al. 2006, Kuhn et al. 2004, Ostrand & Balcer 1988, Schroeder & Korel 2000, Cheng/Dumitrescu/Schroeder 2003, Suh's axiomatic-design papers (axiomaticdesign.com, MIT DSpace), INCOSE GtWR summaries, McKinsey's Minto article; in repo: README §11 variant F, spine-questions.md, gen_cases.py, interfaces.toml and the SR template. Read-only research; nothing was built. -->

# Item 11: value domains, sparse boundaries and the descend test (research for F-call 7)

*For the owner. Answers F-call 7 of [`README.md`](README.md) §11, variant F point 8 and F-call 6. Each source is marked **verified** (primary text or an authoritative record read in this session), **record only** (the bibliographic record was confirmed but not the text), or **unverified** (from memory).*

**Short answer.** The names in point 8 are real and mostly attributed correctly. Two corrections: SCR calls its checks **disjointness and coverage**, not completeness, and Harper's post credits Dan Licata with the name "boolean blindness". The best-fitting prior art is **SCR** (Heninger, Heitmeyer, Parnas). Its *mode classes* are the owner's enumerated, problem-oriented states, and its *disjointness and coverage* checks are MECE made mechanical. Its *four-variable model* (Parnas & Madey) is the closest published stopping rule for the descend test: a requirement speaks only of monitored and controlled quantities in the environment, never of the device values a design chooses. For boundaries, the best fit is **information hiding + the Design Structure Matrix** (Parnas; Steward, Eppinger; Sullivan et al. applied the DSM to Parnas's own KWIC example). The **Information Axiom** is not the right measure: it is a probability of meeting a tolerance, not a count of cases. The plan's arithmetic is right per output, but it understates one gain and overstates another:
- The per-output product is the published **input-output relation** idea in combinatorial testing (Schroeder & Korel 2000).
- A component's exhaustive suite is the union of those projections, at least as large as the biggest one. So in the plan's 4×2 example, the component still needs 8 cases.
- Splitting also pays, often by more, where an output is reached only through a **narrower intermediate domain**: a product then becomes a sum.

Two cheap stdlib checks are worth building, both advisory at first:
- an SCR-style disjointness and coverage check over domains declared in the *existing* `set{...}` grammar;
- a DSM over the import graph plus IF file edges, per component.

## 1. Terms and sources

| Term | Source | Status | Best fit for |
|---|---|---|---|
| "Make illegal states unrepresentable" | Yaron Minsky. The phrase is a heading in ["Effective ML Revisited"](https://blog.janestreet.com/effective-ml-revisited/), Jane Street blog, 2011-03-09. That post revisits his 2010 "Effective ML" talk to a Harvard OCaml class. Example: one record of optional fields per connection becomes a variant whose cases carry only their own data. | verified (post); the talk's wording is unverified | One enumeration instead of four booleans; "no value carried twice" |
| Sum vs product types: \|A+B\| = \|A\|+\|B\|, \|A×B\| = \|A\|·\|B\| | Standard type theory, e.g. Pierce, *Types and Programming Languages*, MIT Press 2002, ch. 11 (sums, variants, tuples) | unverified chapter; the arithmetic is textbook | The 16 vs 4 count: four booleans are a product (2⁴); the location is a sum of four unit cases (1+1+1+1) |
| Boolean blindness | Robert Harper, ["Boolean Blindness"](https://existentialtype.wordpress.com/2011/03/15/boolean-blindness/), *Existential Type*, 2011-03-15. Harper credits **Dan Licata** with the name: reducing information "to a bit" loses what the bit meant. | verified | Why a flag that crosses a boundary is a smell |
| Parse, don't validate | Alexis King, [blog post](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/), 2019-11-05. Her two maxims: "Use a data structure that makes illegal states unrepresentable"; "Push the burden of proof upward as far as possible, but no further." | verified | Convert input at the boundary into the closed domain once. Ruling 1's allow-set plus declared rule is the parser. |
| SCR / Parnas tables: mode classes, condition tables, disjointness and coverage | K. Heninger, "Specifying Software Requirements for Complex Systems: New Techniques and Their Application", *IEEE TSE* 6(1):2–13, 1980 (A-7E). C. Heitmeyer, R. Jeffords, B. Labaw, "Automated Consistency Checking of Requirements Specifications", *ACM TOSEM* 5(3):231–261, 1996. The checks are stated in Heitmeyer, ["Requirements Models for System Safety and Security"](https://asimod.in.tum.de/2010/slides/heitmeyer/Heitmeyer2-Markt2010.pdf), Marktoberdorf 2010: **Disjointness**: for each pair of cells in a row, c1 ∧ c2 = false. **Coverage**: c1 ∨ … ∨ cn = true. Together they mean "no ambiguity, no missing cases", so the defined function is total. | slides verified; both papers record only | Closed enumerations (a mode class is one); a mechanical MECE check |
| Four-variable model | D. Parnas, J. Madey, "Functional Documents for Computer Systems", *Sci. Comput. Program.* 25(1):41–61, 1995, doi:10.1016/0167-6423(95)96871-J. Requirements (REQ, NAT) relate **monitored** to **controlled** environmental quantities; IN and OUT map those quantities to device inputs and outputs, which are design. | record only | The descend test (§5) |
| MECE | Barbara Minto, McKinsey, late 1960s; *The Pyramid Principle*, 1985/1987 (dates conflict). [McKinsey alumni article](https://www.mckinsey.com/alumni/news-and-insights/global-news/alumni-news/barbara-minto-mece-i-invented-it-so-i-get-to-say-how-to-pronounce-it). | record only | A consulting heuristic. Cite SCR disjointness and coverage as the checkable form; the formal term is a *partition*. |
| Axiomatic Design: Independence Axiom, Information Axiom, FR–DP design matrix | N. P. Suh, *The Principles of Design*, Oxford UP 1990; *Axiomatic Design: Advances and Applications*, Oxford UP 2001. A **diagonal** matrix is uncoupled, a **triangular** one is decoupled (solvable in order), anything else is coupled. The Information Axiom prefers the least information content, I = log₂(1/p), where p is the probability that the system range falls in the design range. | definitions verified via secondary papers ([MIT DSpace](https://dspace.mit.edu/handle/1721.1/25610), ICAD papers); the books are unverified | Independence Axiom: an output should depend on its own inputs only. Do **not** use the Information Axiom as the case count (§2). |
| Design Structure Matrix and clustering | D. V. Steward, "The Design Structure System", *IEEE Trans. Eng. Mgmt.* EM-28(3):71–74, 1981. S. Eppinger, T. Browning, *Design Structure Matrix Methods and Applications*, MIT Press 2012. Software DSMs: Sullivan, Griswold, Cai, Hallen, "The Structure and Value of Modularity in Software Design", ESEC/FSE 2001, which models Parnas's KWIC designs. MacCormack, Rusnak, Baldwin, *Management Science* 52(7):1015–1030, 2006, which introduces **propagation cost**, the density of the transitive closure. | record only | Placing boundaries; spotting under-decomposition (§3) |
| Information hiding | D. L. Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules", *CACM* 15(12):1053–1058, 1972 | record only | Why a split makes sparse dependency *provable* (§2) |
| Coupling and cohesion | W. Stevens, G. Myers, L. Constantine, "Structured Design", *IBM Systems Journal* 13(2):115–139, 1974. The named levels (data, stamp, **control** coupling …) are elaborated in Yourdon & Constantine, *Structured Design*, 1979. | unverified detail | A boolean passed to select the callee's behaviour is **control coupling**: boolean blindness at a boundary |
| Category-partition method | T. Ostrand, M. Balcer, *CACM* 31(6):676–686, 1988. Categories are split into *choices*. Constraints (properties with `if` selectors, `[error]`, `[single]`) remove infeasible or redundant combinations. | record verified; constraint syntax from course notes only | "Only the valid cases" at test design; an `[error]` choice is the out-of-domain input |
| Combinatorial / pairwise testing | Cohen, Dalal, Fredman, Patton, "The AETG System", *IEEE TSE* 23(7), 1997 (unverified). D. R. Kuhn, D. Wallace, A. Gallo, "Software Fault Interactions and Implications for Software Testing", [*IEEE TSE* 30(6):418–421, 2004](https://csrc.nist.gov/pubs/journal/2004/06/software-fault-interactions-and-implications-for-s/final): faults are triggered by few interacting parameters. NIST SP 800-142 (Kuhn, Kacker, Lei, 2010). | 2004 paper verified | `gen_cases.py` already does this |
| **Input-output relation testing** (missing from the list) | P. Schroeder, B. Korel, "Black-box Test Reduction Using Input-Output Analysis", ISSTA 2000:173–177. C. Cheng, A. Dumitrescu, P. Schroeder, "Generating Small Combinatorial Test Suites to Cover Input-Output Relationships", QSIC 2003:76–82. | records verified; their content is from memory and unverified | **The owner's per-output measure is this idea**: test each output over the inputs that influence it |

**Also missing, and better established in systems engineering:**
- **SysML** value types and *enumerations*, with ports and item flows (OMG SysML; `enum def` in v2). This is the kit's IF row as a typed node joining ports. Unverified clause numbers.
- **Interface control documents** (NASA SE Handbook SP-2016-6105, interface management). Unverified section.
- **Harel statecharts**: "Statecharts: A Visual Formalism for Complex Systems", *Sci. Comput. Program.* 8(3):231–274, 1987. OR-states are sums; **orthogonal (AND) regions are products**. That gives the principled exception: a product of flags is right exactly when the dimensions are truly independent.
- **Equivalence partitioning** (G. Myers, *The Art of Software Testing*, 1979). The cardinality the arithmetic counts is the number of equivalence classes, not of raw values.
- **Exhaustiveness checking** of pattern matches: the compiler's version of SCR coverage.

**Fit, in one line each:**
- One enumeration, no duplicate meaning: Minsky and sum types, with SCR mode classes for the problem-oriented framing.
- Checking an enumeration or a condition table: SCR disjointness and coverage.
- Placing boundaries to minimize permutations: information hiding + DSM, with Schroeder–Korel for the count.
- Decompose describable states: SCR modes and the four-variable model (§5).

## 2. The arithmetic

The plan's measure, "for each output, the product of the cardinalities of the inputs it actually depends on", is the **input-output relation** of Schroeder & Korel. It is sound per output, with four corrections:

1. **Count classes, and count state.** The cardinality of an input is its number of equivalence classes (category-partition *choices*), not its raw values. A component's own mode or state is an input. In SCR, condition tables are indexed by mode class.
2. **The suite size is a union, not a sum.** One test drives all outputs at once. So a component's exhaustive suite covers the union of its per-output projections, and its size is at least max over outputs of ∏|D_i|. In the plan's example, y1 = f(A₄, B₂) and y2 = g(B₂), the component needs **8 cases whether or not it is split**. The 2-case figure holds for y2's own verification and change impact, not for the total. What the split adds is **soundness**: inside one component, "y2 ignores A" is a claim; across a hidden boundary (Parnas), it is structural, so the 2-case test of y2 is a proof rather than a sample. The plan's "provably cannot reach it" is right, but the gain is in proof and blast radius, not in the case count.
3. **The bigger gain is a narrow intermediate domain.** Take an output that depends on X₄, Y₄ and W₃ only through Z = h(X, Y) with |Z| = 2. As one component it needs 4·4·3 = 48 cases. Split at Z, it needs 16 (for h) + 2·3 = 22: **the product becomes a sum**. This is why point 8 is right that intermediate domains must be stated before the split. The gain is sound only if Z is the *whole* channel, with no side path, which is what information hiding and a DSM check guard.
4. **Information content (Suh) is a different quantity.** I = Σ log₂(1/pᵢ) measures the probability of meeting tolerances, not combinatorial size. The kit should not cite it as the measure. The Independence Axiom is the right citation: an uncoupled, diagonal FR–DP matrix is the sparsest dependency.

**A better-founded form** (a synthesis, not a published metric). Take log₂ of the per-output product. Then cost(o) = Σ_{i ∈ deps(o)} log₂|D_i|, the number of bits of input that output reads. Summed over a component's outputs, this is a weighted count of the filled cells in its output × input dependency matrix: Suh's design matrix, or a DSM, weighted by domain size. It is additive, so boundary choices can be compared by summing per component, and it is zero-cost for the cells a split removes. For sampled testing (pairwise, t-way), suite size grows roughly as v^t·log k rather than as the full product (Kuhn et al.; covering-array theory, bound unverified here). Boundaries still help, because they shrink k and v, but less dramatically.

## 3. What the kit could mechanize (stdlib, advisory first)

Existing homes:
- the SR `permutations` cell already uses `gen_cases` grammar (`name=set{a,b,c}`);
- the IF `data` cell is "the finite alphabet when there is one" (`interfaces.toml` header);
- `gen_arch_map.py` already parses imports with `ast`.

The kit's own SR registry has **0** `permutations` cells today, so the value-domain idea has a home that is unused.

| Check | Input from registries | Flags | False-positive risk |
|---|---|---|---|
| **A. Domain well-formedness** | IF `data` alphabets and SR/LLR `set{...}` dimensions | duplicate or case-folded labels; a declared catch-all (UNKNOWN, OTHER) with no declared behaviour, i.e. ruling 1's missing "declared rule for everything else"; **≥2 `bool` dimensions on one cell** as a possible boolean-blindness or control-coupling smell | Low for the first two. High for the bool cluster (orthogonal flags such as `--strict` and `--json` are legitimate product dimensions in the statechart sense), so it should be advisory text, never a gate |
| **B. SCR disjointness and coverage** | A condition table over declared finite domains: rows of conditions over `set{...}` dimensions → output. Today no cell holds one, so this needs an optional structured cell or a table in the contract body. That is a schema addition; **flag for downstream migration** (opt-in). | Enumerate the product of the domains (cheap below about 10⁵ points; ranges need interval splitting at their declared bounds). Flag any point matched by **0 rows** (coverage) or **>1 row with different outputs** (disjointness). | Near zero: the check is exact over what is declared. The real risk is the authoring cost, and a catch-all row that makes coverage trivially true (pair it with check A) |
| **C. DSM per component** | Module → module edges from `gen_arch_map`'s import pass, plus file-channel edges from IF `owner` → `consumers`/`requestors`, grouped by component (the file header under F point 1) | Per component: weakly connected clusters after removing hub modules (in-degree above a set fraction); propagation cost; cycles that cross a component boundary. **Two or more clusters with few cross edges suggests an under-decomposed component.** W3 Autonomy (60 modules, 54 internal seams) is the test case. | Medium to high. Utility hubs glue everything together (hence hub exclusion). Imports miss subprocess calls and file handoffs; IF file rows recover only the authored ones (the README notes the lane's handoffs are mostly files). Report it in the dashboard as a suggestion, never a gate. |
| D. Dependency sparsity per output (§2's measure) | Output → input dependency declarations, which no registry holds | — | Not cheap. Skip until domains exist (point 8's precondition) |

## 4. Vocabulary recommendation for the spine-authoring rubric

1. **Value domain**: the set of values that may cross an interface; part of the kit's *contract*. (Type theory; SysML ValueType.)
2. **Closed enumeration**: a domain listed case by case, each case carrying only its own data. (Sum type; SysML Enumeration; Minsky.)
3. **Disjointness / coverage**: no input satisfies two cases; every input satisfies one. Say these instead of MECE. (SCR, Heitmeyer.)
4. **Mode class**: a named set of problem states the system is in, with transitions between them. The unit of the descend test. (SCR, Heninger 1980.)
5. **Monitored / controlled quantity**: an environmental quantity the system observes or sets. Requirements speak only in these. (Parnas & Madey 1995.)
6. **Information hiding**: a boundary hides a design decision likely to change. (Parnas 1972.)
7. **Control coupling**: a flag passed across a boundary to select the receiver's behaviour. (Stevens, Myers, Constantine 1974.)
8. **Dependency matrix (DSM)**: outputs or elements × what they depend on; uncoupled is diagonal, decoupled is triangular. (Steward 1981; Suh.)
9. **Input-output relation**: the inputs that influence one output; the unit of the case count. (Schroeder & Korel 2000.)
10. **Choice**: one equivalence class of a category; what cardinalities count. (Ostrand & Balcer 1988.)

**Terms to avoid or gloss:**
- ***module***: Parnas and Stevens et al. mean a unit of decomposition (the kit's *component*); the kit means one file. Gloss it whenever citing them.
- ***seam***: Feathers (*Working Effectively with Legacy Code*, 2004) uses it for a place to change behaviour without editing. The kit's sense (an internal interface) differs, so don't cite Feathers for it.
- ***mode*** alone: it collides with CLI `--mode` and with `planmode`. Use *mode class*.
- ***information content***: Suh's is probabilistic, so it reads as the case count when it is not.
- ***completeness***: SCR's word is *coverage*, and "complete" is also an IEEE 29148 / INCOSE characteristic of one requirement.
- ***contract***: in Meyer's Design by Contract it means pre- and postconditions. That is compatible with the kit's usage, but state the kit's meaning once.
- ***MECE***: keep it as a gloss only.

## 5. The descend test (F-call 6)

No source found states "stop at values the stakeholder could only choose on seeing the implementation" verbatim. Three established rules bracket it:
- **SCR / four-variable model (closest).** Requirements are relations between monitored and controlled quantities (REQ, constrained by NAT). The mapping to device values (IN, OUT) is design (Parnas & Madey 1995, record only). A *mode class* is exactly a state the stakeholder can name, with what the system does in it (condition tables) and what moves it on (mode transition table). That matches the owner's step 1 almost word for word.
- **INCOSE Guide to Writing Requirements.**
  - C2 *Appropriate*: "the specific intent and amount of detail of the requirement is appropriate to the level of the entity to which it refers (level of abstraction)" ([INCOSE IS2015 slides](https://www.incose.org/wp-content/uploads/legacy/presentation/IS2015-pdf/2-2-2.pdf)).
  - R31 *solution free*: "avoid stating a solution unless there is rationale for constraining the design. Focus on the problem 'what' rather than the solution 'how'". This wording comes from a third-party summary; check it against GtWR v4.
  - ISO/IEC/IEEE 29148:2018 lists *Appropriate* among its nine characteristics (paywalled; secondary source only).
- **Axiomatic Design (the designer-side rule).** Zigzag "until … the solution to the remaining subproblems is known". Leaf elements "require no further decomposition", and zigzagging repeats "until it is possible to construct the system from the information contained in the system architecture" ([Suh, Italy96](https://axiomaticdesign.com/technology/papers/Italy96.pdf); ICAD 2002). This stops when the *designer* knows the answer; the owner's rule stops when the *stakeholder* can no longer state one. They are complements.

**Refinement from R31's "unless there is rationale":** a number *is* a requirement when the stakeholder can source it today. A cited standard is an example: WCAG's 4.5:1 contrast minimum, from memory. Step 2's test should be "could not state *or source* today".

## Suggested edits to variant F (proposals only)

1. **Point 8, names list:**
   - Change "disjointness and completeness" to SCR's **disjointness and coverage**, citing Heitmeyer et al. 1996.
   - Keep MECE only as a gloss.
   - Add **Parnas & Madey's four-variable model** and **Schroeder & Korel's input-output relations**.
   - Drop the Information Axiom; keep the Independence Axiom.
2. **Point 8, arithmetic:** restate as in §2.
   - Per-output cost is the product of the dependent inputs' choice counts, mode included.
   - A component's suite covers the union of the per-output projections.
   - Splitting pays (a) in proof and blast radius where dependencies get sparser, and (b) in case count where an output is reached through a narrower intermediate domain.
   - Correct the "2 cases instead of 8" sentence accordingly.
3. **Point 8, catch-all:** distinguish an UNKNOWN *problem state*, which needs declared behaviour (ruling 1's declared rule), from an *out-of-domain input*, which is rejected at the boundary (parse, don't validate; category-partition `[error]`). Otherwise UNKNOWN silently absorbs real missing cases and coverage becomes trivially true.
4. **Point 8, the booleans:** name the exception. A product of flags is right where the dimensions are orthogonal (statechart AND-regions). The smell is control coupling, not booleans as such.
5. **F-call 6:**
   - Anchor step 1 in SCR mode classes and the four-variable model.
   - Amend step 2 to "could not state or source today" (INCOSE R31's rationale clause), so standard-mandated numbers stay requirements.
6. **F-call 7 mechanization:** build check A and the coverage/disjointness half of check B over the **existing** `set{...}` grammar and IF `data` alphabets (no new schema for A). Treat C as a dashboard suggestion with hub exclusion. Defer D.
7. **Vocabulary:** adopt §4's list in the spine-authoring rubric, with the *module* and *seam* glosses, before any of it reaches `PROCESS.md`.
