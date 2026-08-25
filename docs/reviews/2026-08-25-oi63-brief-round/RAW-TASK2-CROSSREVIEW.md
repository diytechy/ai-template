# RAW - TASK 2, the cross-review

Unedited final message from `OPENAI-SOL` (`gpt-5.6-sol`, `codex exec`),
2026-08-25, executing TASK 2 of [BRIEF.md](BRIEF.md). 181,716 tokens.
Adjudication: [RESUME.md](RESUME.md).

---

# OPENAI-SOL cross-review — WI-516 second opinion

1. **QUALIFIED — The spot-check supports the broad finding, but not every clause classification.** I independently reviewed 15 live rows: six `Provides`, nine `Consumes`; three pure-restatement rows, five large-remainder rows, and four heavy-non-crossing rows. Result: **12 AGREE, 3 DISAGREE**.

| Family | Row | Independent classification and comparison |
|---|---|---|
| Provides | `IF-020` | **AGREE.** Pure restatement. stdin, `permissionDecision`, exit 2, the policy dial, and fail-open behavior are all in `LLR-040`. Evidence: `interfaces.toml:378`; `low-level-requirements.toml:422-427`; verdict `:225`. |
| Provides | `IF-050` | **DISAGREE.** The producer, record fields, fingerprint, and `--check` are restatement of `LLR-186`. The kept clause, *“every consumer reads it through kitlib.stage.read_stage”*, is not a valid consumer-obligation remainder as written: `kitlib/stage.py` explicitly says display consumers parse the recorded file directly and do **not** use `read_stage`. It is a false universal requiring correction, not relocation as-is. Evidence: `interfaces.toml:744`; `low-level-requirements.toml:1930-1936`; `kitlib/stage.py:45-55,675-696`; verdict `:228`. |
| Provides | `IF-061` | **DISAGREE.** The three artifact destinations are real written-artifact remainder. But *“legacy work-items.csv rows via dual-write”* is a false crossing claim, while allocation over IDs in both homes remains live compatibility behavior. The verdict correctly notices staleness but combines this as `X`; it should be split into deletion-worthy rot plus a live crossing guarantee. CSV append retired at `plan_artifacts.py:183-185`; current filing is spec-only at `:332-337`. Evidence: `interfaces.toml:456`; verdict `:227`. |
| Provides | `IF-080` | **AGREE.** `LLR-140` covers the operational contract; the `SS1.2/SS2.3` citation is provenance, not a crossing fact. Evidence: `interfaces.toml:980`; `low-level-requirements.toml:1377-1383`; verdict `:234`. |
| Provides | `IF-115` | **AGREE.** Selection, signature, and all-or-nothing assembly are restatement; the caller’s hold-for-human rule is substantive and otherwise homeless. The verdict also correctly flags its contradiction with `LLR-167`, which says refusal falls back to the worker assignment. It must be adjudicated before relocation. Evidence: `interfaces.toml:1352`; `low-level-requirements.toml:1704-1710`; verdict `:239`. |
| Provides | `IF-135` | **AGREE.** `SR-020`/`LLR-020` state scan-and-block only. Git’s argv/stdin calling convention, stderr range, exit semantics, and `--no-verify` bypass are real remainder. Evidence: `interfaces.toml:1580`; `system-requirements.toml:118-125`; `low-level-requirements.toml:211-216`; verdict `:242`. |
| Consumes | `IF-025` | **AGREE.** Pure restatement across the module’s AST-inventory, interface-loader, and dependency-diagram surfaces. Evidence: `interfaces.toml:492`; `gen_arch_map.py:2-22,230-235,992-1003`; verdict `:256`. |
| Consumes | `IF-038` | **AGREE.** Pure restatement of `SR-043`, including the three dial values, launcher override, and fail-open posture. Evidence: `interfaces.toml:619`; `system-requirements.toml:289-296`; verdict `:268`. |
| Consumes | `IF-056` | **AGREE.** Loader identities and the crossing are recoverable; never-disagree/ship-together are substantive guarantees; sibling and split history is non-crossing rationale. Evidence: `interfaces.toml:812`; verdict `:281`. |
| Consumes | `IF-071` | **AGREE.** The scheduler frontier is restatement; one-ranker and empty-frontier degradation are real guarantees; import-location and sibling distinctions are non-crossing. The guarded runtime import is indeed in `traj_parse`, while `traj_panels`’ separate direct import is constants-only. Evidence: `interfaces.toml:884`; `traj_parse.py:40-55`; `traj_panels.py:8-29,1159-1174`; verdict `:284`. |
| Consumes | `IF-098` | **DISAGREE.** The verdict assigns 219 characters to remainder, including the tuple and purity. Those are recoverable from precisely the R2 surface the method admits: `catalog_rows()`’s public one-line docstring states `(key, file, slots, digest)`, and `render()`’s states that it is pure. Only the negative *“and nothing else”* and resulting never-disagree guarantee plausibly remain. The exact corrected span requires remeasurement. Evidence: `interfaces.toml:1154`; `prompts.py:226-238`; `gen_prompt_catalog.py:76-90`; verdict `:302`. |
| Consumes | `IF-112` | **AGREE.** The carrier read is recoverable; the remaining 330 characters are migration-defect history, not a crossing fact. Evidence: `interfaces.toml:1317`; verdict `:314`. |
| Consumes | `IF-116` | **AGREE.** The watermark API and loud refusal are recoverable; the two mint formulae and caller-side ordering are substantive crossing rules; the sibling comparison is rationale. Evidence: `interfaces.toml:1363`; `trace.py:912-943,1347-1378`; `plan_artifacts.py:214-246,296-337`; verdict `:317`. |
| Consumes | `IF-117` | **AGREE.** The live `module_bindings` design is restatement. The obsolete oracle comparison and count are rationale/rot, not valid remainder. Evidence: `interfaces.toml:1375`; `low-level-requirements.toml:1857-1863`; verdict `:318`. |
| Consumes | `IF-127` | **AGREE.** Names/endpoints are recoverable; lazy import, one-model/two-renderers, and empty-model refusal remain implementation-held guarantees. Evidence: `interfaces.toml:1493`; `adjudicate_brief.py:396-428`; verdict `:326`. |

2. **REFUTED — A consumer-side obligation is not structurally unplaceable in a provider-side header.** Provider-owned API contracts routinely state caller preconditions and required handling. `IF-115` can say that `(None, reason)` requires the caller to hold for a human; `IF-116` can state that callers bump only after the artifact exists. What a provider header cannot do is keep consumer implementation synchronized automatically. That is an ownership/enforcement weakness, not an inability to state the rule. The stronger structural answer is to split provider behavior from a consumer-owned obligation where necessary. The taxonomy itself shows `F` is an overlapping ownership axis—`IF-116` is `D,B,F` and `IF-124` is `F,D`—not a separate clause kind. OI-63’s absolute claim at `open-items.toml:2428` and its statement that four rows carry this as their “WHOLE remainder” at `:2455` are overstated.

3. **QUALIFIED — The taxonomy captures real content, but it is not a clean set of ten peer categories.** `D` typed shape, `G` posture, and the non-crossing `M/X` class are genuine distinctions. `E` closed vocabulary and `I` calling convention are subtypes of typed shape; `H` compatibility is an overlay on behavior; `F` classifies which party is bound rather than what kind of fact the clause contains. None is inherently relabelled restatement, but membership still requires checking R1–R5 first. `IF-098` demonstrates that the pass did not always do that consistently. Evidence: taxonomy at `if-contract-verdicts.md:106-135`.

4. **REFUTED — OI-63 contains two internal presentation errors.**

   - Option (b) says **21** rows are pure restatement (`open-items.toml:2440`); the verdict table yields **19**, matching `:2422` and `:2463`.
   - The blast-radius opening says every option other than (a) crosses the kit/instance line (`:2431`), while option (d) explicitly says it needs no kit change (`:2444`). That “every other option” claim is false for the recommended option.

5. **CONFIRMED — The WI-516 table’s arithmetic is internally exact.**

| Population | Rows | Characters | Restatement | Remainder | Non-crossing | Rows with remainder |
|---|---:|---:|---:|---:|---:|---:|
| Provides | 19 | 10,278 | 7,805 = 75.9% | 2,180 = 21.2% | 293 = 2.9% | 16 = 84.2% |
| Consumes | 89 | 33,717 | 20,500 = 60.8% | 6,795 = 20.2% | 6,422 = 19.0% | 55 = 61.8% |
| Combined | 108 | 43,995 | 28,305 = 64.3% | 8,975 = 20.4% | 6,715 = 15.3% | 71 = 65.7% |

The table also yields exactly **19** rows with `remainder=0, non-crossing=0` and **18** with `remainder=0, non-crossing>0`. “Non-trivial length” has no defined threshold; operationally, 18 means zero-remainder/non-crossing-only.

The WI-512 dossier independently re-sums to 27 rows, 7,385 original characters, 908 remainder characters over 11 rows, hence 87.7%/12.3% and 40.7%. One supporting inconsistency does not affect OI-63’s quoted figures: WI-512’s per-row `new` column totals **2,605**, not the reported **2,613** (`2026-08-24-wi512-contract-generalization.md:33-42,62-90`). The claimed 2,613 equals 1,705 crossing plus 908 remainder, so one per-row `new` value or that crossing subtotal is eight characters off.

These sums confirm the table’s arithmetic, not the semantic accuracy of every partition; the three spot-check disagreements qualify the exact character percentages.

6. **CONFIRMED — Both rot exhibits are real.**

   - `IF-117` falsely speaks of *“the committed module map”* in the present tense. `docs/architecture.md` is absent and explicitly retired in `docs/declared-absences:124`; `gen_arch_map.py:12-13,149` says the same.
   - Its claim that *“the sym: tier keeps reading the artifact”* is false. `load_symbol_oracle` calls `gen_arch_map.scan_inventory` directly (`check_doc_refs.py:281-307`).
   - Its **149** count is stale: the live design registry contains exactly **184** `[design.LLR-*]` rows.
   - `IF-055` names deleted `SCHED_*` constants (`interfaces.toml:801`). No such definitions remain in `schedule.py`; the checker’s own design note records that the concurrency program deleted them (`trace.py:552-567`). This exhibit is confirmed as well.

7. **QUALIFIED — The recommendation is directionally supported.** Option (d)-then-re-ask remains the best-supported reading: the heavy-non-crossing sample (`IF-056`, `IF-071`, `IF-112`, `IF-117`) independently confirms that substantial contract prose is rationale, history, or implementation placement that relocation cannot solve. Moving that content to `rationale`, the log, or deletion addresses the field-boundary problem before choosing a home for genuine crossing facts. However, the exact 15.3% should not be treated as independently validated, and option (c)’s “strong second” case should not rely on the refuted claim that caller obligations cannot be stated provider-side. The family split still makes (c) plausible, but not uniquely compelled.

**Verdict:** The measurement **stands, with qualifications, as a basis for ruling OI-63**. Its arithmetic, population-level direction, non-crossing finding, and rot evidence survive review. It is strong enough to support (d)-then-re-ask. Before using the exact remainder percentages or the consumer-obligation argument to choose among relocation options, correct **21 → 19**, reconcile the WI-512 eight-character discrepancy, and re-adjudicate at least `IF-050`, `IF-061`, and `IF-098`.
