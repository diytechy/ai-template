# Inspection procedures

These are the durable procedures for the three drafted decomposition
inspections and one sampled assumption inspection, one section per subject. Each result subsection stays explicit
until a reviewer records the person, date, and result. Results below distinguish
completed document inspections from an incomplete positive sample; none is an
artifact approval or a machine-coverage result.

## Critique acceptance provenance inspection

Read one complete Critique acceptance record against the applicable SN/SR
intent. Confirm the fresh non-author reviewer session, the written rubric and
its intent sources, and a numbered rubric-anchor id for every verdict and
finding. Then read an abnormal record with one or more of reviewer, rubric,
intent basis, or anchor citation missing. Record each missing field as an
Inspection finding, including a rubric copied from the verifying TC without
independent derivation from the SN/SR intent. This procedure checks process and
provenance; it does not make the Critique judgment about artifact quality.

### Critique acceptance provenance inspection result

**PASS — 2026-09-06, [fresh Opus 5/high Inspection](../reviews/2026-09-06-oi85-inspection-structured-opus.md).** The inspector read the actual
[Critique closure](../reviews/2026-09-06-oi85-record-closure-structured-opus.md)
and its linked invocation. It identified fresh non-author review identity,
rubric revision/intent sources and coverage of all five numbered anchors. It reported all four
missing facts in the abnormal record and rejected the fully populated
TC-copied rubric. This establishes record process/provenance; artifact quality
and Drafted-row approval remain separate.

## Requirement and interface counterpart review inspection

Read one reviewed change record where a requirement or interface side changed.
Confirm that it names the changed side and affected counterpart, carries the
corresponding change or an explicit justification for retaining it, and records
an independent semantic decision. Then inspect an abnormal record in which all
ids, endpoints, and references resolve but the counterpart meaning is absent.
Record a finding. A reference-existence result alone cannot discharge this
procedure.

### Requirement and interface counterpart review inspection result

**PASS — 2026-09-06, [fresh Opus 5/high Inspection](../reviews/2026-09-06-oi85-inspection-structured-opus.md).** The inspector read the actual
[scoped H3 record](../ai-template-redesign-2026-09-05-codex/DECOMPOSITION-AMENDMENTS.md#implementation-review-subject-2026-09-06),
IF-011/IF-164, LLR-035/LLR-198 and SR-168/SR-070. It identified the retained
counterparts and the independent counterpart semantic judgment, and rejected the
reference-only counterexample. The separate
[P9R source review](../reviews/2026-09-06-oi85-p9r-selector-structured-opus.md)
checks facade compatibility against source; the document inspector did not
execute that source.

## Decomposition proportionality inspection

Read one actual completed decomposition review record, the declared hats roster,
and the decomposition brief used by that review. Resolve the applicable hats,
confirm that the brief presents every applicable hat's question and that the
review record names each hat's outcome. Confirm the required spine remains the
scope boundary, then inspect the complete reviewed chain and a small chain
containing a child that only paraphrases or duplicates a parent's decision or
verification. A missing applicable-hat outcome or a child within a required tier
with no independent decision or verification purpose is an Inspection finding.
Record why further splitting stops at the independent-value boundary. This
procedure uses the existing brief and review record and does not impose a
row-count threshold, extra depth, new record carrier, or machine coverage check.

### Decomposition proportionality inspection result

**FAIL — 2026-10-26, [fresh Codex Sol Inspection](../reviews/wi-976/019-REJUDGE-28a0309.md),**
recorded through `record_observation.py` as TC-211's observation of that date,
under the procedure as amended by WI-976. The sample was the WI-976
checkpoint sitting 016 (its brief and verdict, as TC-211's `inputs` name
them), with that lane's sittings 004, 010, 011, 012 and 015 as chain evidence.
Applicability, the brief's questions and the verdict's outcomes pass (eleven
applicable hats, each question presented and each outcome named), the
returned rows were all re-sat, each retained child has an independent
purpose, and the procedure identifies both abnormal inputs. It fails on one
MAJOR finding: the verdict does not record why further splitting stops,
which its brief asked for (rubric R2; SR-186's acceptance).

**PASS — 2026-10-03,** recorded as the observation
`docs/test/observations/TC-211.2026-10-03T210347Z.toml`, under the procedure
as it then read.

**Historical INCOMPLETE — 2026-09-06, [earlier Opus 5/high Inspection](../reviews/2026-09-06-oi85-inspection-structured-opus.md).** That inspector accepted the
independent purposes of SR-184/SR-185/SR-186 and their direct Inspection cases,
read the stopping reason, and rejected the paraphrasing child. The procedure
then required a machine-produced SR-161 perspective record that did not exist,
as LLR-183 then stated. The owner ruling of 2026-09-06, re-affirmed on
2026-10-13 (`docs/log.d/2026-10-25-wi976-sn036-ruling.md`), replaced that
obligation with the existing hat-by-hat review path, and LLR-183 was amended
accordingly. The earlier result remains incomplete for the procedure it
actually executed; the ruling itself supplies no test result.

## Sampled new-reader inspection

A sampled observation of an assumption, not of a requirement: it can falsify
DA-011, that what a random sample of the code's parts shows about its
readability holds for the parts the sample did not reach. Draw five parts at
random from the source the declared readability and structure measures cover,
never parts their authors choose, a part being one function, class or
module-level block with its own back-link. Give each to a reader who has not
worked on it: a person, or a fresh model session that did not author the part,
told which. The reader reads only the part's code and the records it links to,
through the generated views, and states what the part does and why it exists,
without asking its author. Record each statement beside the part's linked
requirement and design rows, and judge whether the two agree. Sampling reads
that source scope and its linked rows; re-judgement follows TC-279's declared
trigger and the [observation rule](../../project-trajectory/PROCESS.md#observation-judgement).

A reader who cannot say what the part does or why it exists, or whose
statement contradicts the linked rows, is a failing sample and falsification
evidence against DA-011, whatever the other samples show. A passing sample
bounds discovery; it does not show the assumption holds for the parts it did
not reach.

### Sampled new-reader inspection result

**PASS (sample only) — 2026-10-03, round 2, [WI-697 Claude Opus 5.5 adjudication](../reviews/wi-697-re-judge-tc-279-no-result-rec/002-ADJUDICATE-f2bc66c.md); [sample record](../reviews/wi-697-re-judge-tc-279-no-result-rec/SAMPLE-r2-f2bc66c.md).**
Recorded through `record_observation.py`. This pass establishes nothing
about the parts the sample did not reach.

**The draw.** The population is every function, class, module-level block or
module header that `gen_arch_map.declaration_sites` encloses an `Implements:`
line to, under the `[paths]` roots in `docs/stack.ini`: 516 parts. The seed is
trunk HEAD `f2bc66c1`, fixed by rule. One drawn key was not a part. It was a
line inside a test-fixture string (`tests/test_trajectory_arch.py`
`MOD_A_SRC`) naming rows that do not exist. It was skipped, and the next
seeded draw was taken. That is exactly the draw the coordinator's after-the-fact
live-id restriction produced. The adjudicator ruled the skip a population rule
rather than a selection. It did not adopt the live-id proxy as the definition
of a part.

All five readers were fresh Claude Sonnet 5.5 sessions that did not author
their part and were told so. Each read the part and its linked rows, from the
registry files rather than the generated views, a deviation that is recorded
and does not break R1.

**The five statements:**

- `gen_arch_map.MAPPING_FINDING_POLICY` (SR-163, LLR-276): the one declared
  warn-versus-gate table, missing and stale gating, unresolved and unmapped
  warning, so the burn-down needs no flag day. **Agrees.**
- `session_service.KeepWarmer` (SR-227, LLR-270): a one-turn keep-warm ping
  that runs on its own thread under a warm lease and is recorded only over a
  clean trunk, so the cache stays warm without blocking the scheduler or
  racing an adjudication. **Agrees.**
- `consolidate.close_refusal` (SR-220, LLR-210): the pre-close gate, whose
  six refusals run in a fixed order so that the refusal names the row.
  **Agrees.**
- `gen_release_checklist._rejudge_checklist_line` (SR-215, LLR-255): the
  release checklist's required re-judge item, with the due count read through
  rejudge's pure decision and never shown as zero. **Agrees.**
- `traj_render._render_drill` (SR-054, LLR-100): the drill markup with its
  breadcrumb nav and controller, the never-without-a-way-back return path.
  **Agrees.** The reader could not say why only two drills get the trace bar.
  No linked row records that reason; it is surfaced as a finding, not ruled B1.

No reader failed to explain its part, and none contradicted its rows.

**Round 1 (superseded draw, no result).**
[001-ADJUDICATE-f2bc66c.md](../reviews/wi-697-re-judge-tc-279-no-result-rec/001-ADJUDICATE-f2bc66c.md),
[sample](../reviews/wi-697-re-judge-tc-279-no-result-rec/SAMPLE-f2bc66c.md).
Round 1 drew from 423 functions and classes with an `Implements:` docstring.
That frame left out module headers, module-level blocks and comment-linked
functions, about a fifth of the back-linked parts, so no result was recorded.
Its five readers all agreed with their rows. On part 3, `kitlib.spine.sn_all_ids`,
one branch was misstated. Round 1 ruled that short of B1, and round 2 does not
revisit it. A person may still overrule that ruling and record `fail`.

## Bounded abnormal inputs for the OI-85 inspection

These are synthetic counterexamples for the procedures above. They do not amend
live requirements or impersonate actual reviews. The positive subjects are the
real scoped amendment record and its independently logged Critique; the
inspector must identify the exact versions it reads.

- **Missing provenance:** verdict `APPROVE`; reviewer/session not recorded;
  rubric not named; no SN/SR intent basis; no numbered anchor citations.
  This one abnormal record deliberately omits all four required facts.
- **Copied rubric:** a synthetic reviewer `fixture-reviewer`, session
  `fixture-session`, records `APPROVE` at anchor `R1` against synthetic rubric
  `fixture-rubric revision 1`. The record names SN-024 and SR-184 as intent
  sources, but states that the rubric was copied verbatim from the verifying
  TC-209 method without reading or independently deriving from those parents.
  Every provenance slot is populated; the declared derivation is still invalid.
- **Reference-only counterpart:** a synthetic change says IF-011's stale
  result is now exit 2, while LLR-035/SR-168/SR-070 and callers retain the
  existing behavior. Its review says only that all named IDs and endpoints
  resolve and therefore the change passes. It records neither a corresponding
  behavioral change nor a reason why retaining it preserves meaning.
- **Missing perspective outcome:** the actual completed review record with one
  applicable hat's outcome omitted, while the applicable-hat brief and all other
  outcomes remain. The Inspection must identify that omitted applicable hat.
- **Paraphrasing child:** the actual SR-186→TC-211 chain gains an unminted
  candidate child saying “the process shall keep decomposition proportionate,”
  verified by the same Inspection judgment without another decision or case.
  Its only stated purpose is to make the chain look more detailed. This adds
  no independent decision or verification purpose within a required tier.

The historical incomplete result records what that earlier inspection examined.
A later TC-211 execution inspects the actual completed review record and records
its own reviewer, date, subject and findings; the owner ruling itself supplies
no Inspection result.
