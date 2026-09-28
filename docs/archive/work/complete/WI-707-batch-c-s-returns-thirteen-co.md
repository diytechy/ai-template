+++
id = "WI-707"
title = "Batch C's returns: thirteen Coincident waivers (re-word or re-parent), SR-223 with TC-290, SR-224's lens (SN-005 is the owner's), TC-272's tier"
workstream = "process"
sr_refs = ["SR-011", "SR-015", "SR-024", "SR-031", "SR-033", "SR-040", "SR-111", "SR-112", "SR-129", "SR-147", "SR-149", "SR-174", "SR-177", "SR-223", "SR-224"]
specref = ""
buildtier = "quick"
priority = 3
safety_class = "spine"
bar = "DevStg-Reqs"
+++

## Deliverable

Built by one builder in three commits with three Codex Sol rounds (wave-5
arbitration rulings 46 and 47), SOUND at 4396d734. It carries spine-acts
batch C's folded returns.

- **The thirteen waivers**, judged by approved SR-193's test (the
  specification alone delivers its needs):
  - Six pass after re-wording or re-parenting: SR-011 (SN-001), SR-031
    (SN-028), SR-040 (SN-026), SR-112 (SN-005), SR-147 (SN-002) and SR-149
    (SN-010). `sn_refs` were re-pointed where the old parent's outcome could
    not carry the row, and the "Realizes" sentences of SR-011, SR-031,
    SR-040 and SR-149 name the cited need in its own words.
  - Seven contribute one part of a need that several requirements deliver
    together, so they cannot honestly waive: SR-015, SR-024, SR-033,
    SR-111, SR-129, SR-174 and SR-177. They drop `coincident` and stay
    unclassified, SR-193's third state, reported without failing. SR-111's
    and SR-174's rationale now say what they contribute. The tier has no
    class for joint delivery, so the question is the owner's: **OI-97**
    (recommendation (a), a declared joint-delivery class).
- **SR-223 and TC-290.** TC-290 gains arm (c): no guardrail payload ships,
  and with only the default core present every roster model receives it.
  The planted states went red. SR-223's last clause is narrowed to what that
  arm observes, because the kit's roster template names models by design.
  SR-223 and SR-225, labelled derived rows, stay unclassified for the same
  reason as the seven.
- **TC-272** is Smoke over its in-memory arm, and the new Full TC-297
  carries the two slow-module pointers.
- **Not done:** SR-224 is byte-exact. It waits on the owner's SN-005
  applicability tags, which are a need.

## Context

Drafted by WI-695 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

VERDICT THIS CONTINUES: the file above. THE TEST every waiver was held to:
does the requirement's effect ALONE deliver the outcome its cited need
ACTUALLY STATES? A waiver passes the assumption gates (`boundary_gate_findings`,
`crossing_gate_findings`, the interface-form gate) the moment it is filled,
so a waiver that writes the row's own effect back into the need buys a gate
pass on a claim the need never made.

IN SCOPE — thirteen cells, each amended in place with status left Approved (a
`Coincident` cell is approved content, LLR-225), or one `SN-Refs` re-point
where the honest parent already exists (a traced cell), then the amendment
adjudication the merge's sweep mints, then an act copying the SR registry
that names the thirteen beside the sixty-six blessed cells.

1. `SR-015.coincident`: SN-002 asks for a trustworthy, mechanically verified SN->SR->LLR->TC chain with zero orphans and no malformed or duplicate id; it names no budget row. The waiver's "a budget row a reviewer can trace to what it constrains" is the row's own effect written back into the need. Remedy: state the need's actual outcome and argue how a resolvable PB reference serves it, or re-parent the off-spine PB tier to the need that asks for budgets.
2. `SR-024.coincident`: SN-002 asks for a verified chain; it says nothing about dimensional or permutation coverage, hand-listed or generated. The waiver restates the row as the need. Remedy: an honest waiver against SN-002's stated outcome, or a parent that asks for generated coverage (none does today, which makes this a derived-requirement candidate to label).
3. `SR-031.coincident`: SN-004 asks for explicit gates whose bar is mechanical and SN-005 for one definition of passing enforced agent-neutrally; neither says "one declared value per policy dial, read the same way by every enforcer". That sentence is SN-028's ("a single hand-edited, machine-read file ... the two readings are pinned equal"). Remedy: cite SN-028 and re-word the waiver to it.
4. `SR-033.coincident`: SN-004 asks that a gate pass only when its mechanical bar is met; it says nothing about warn-tier budgets reaching a reader, which is the row's effect restated. Remedy: a waiver stating the release checklist as the release gate's declared bar as the release act reads it, under SN-004's own words, or a parent that asks for the checklist (SN-008's honest verdict is nearer than SN-004).
5. `SR-040.coincident`: SN-006 asks for an unattended, resumable run that never waits for input, reports its failures clearly and stays within declared limits; it does not ask for per-phase command routing or a surfaced reviewer dial. Remedy: re-parent to SN-026 (selection per job and per capability level, where routing lives) or re-word the waiver to SN-006's stated outcome and say which part of it the routing carries.
6. `SR-112.coincident`: SN-012 asks that small changes stay cheap and opt-in layers cost a non-user nothing; a checked per-agent skill fan-out is not an opt-in layer and "paying only for what it uses" is not what a generated copy delivers. Remedy: an honest waiver (the fan-out keeps the one-source rule cheap to maintain) or a parent that asks for the per-agent copies (SN-005's same playbook is nearer).
7. `SR-129.coincident`: SN-002 asks for a verified requirement spine and SN-012 for right-sizing; neither asks that a work-item registry's cells survive a change of representation. Remedy: re-parent to SN-025 (the tracked work-item state the loop derives its next work from) or re-word the waiver to what the cited needs state.
8. `SR-174.coincident`: SN-008 asks for an honest pass verdict and SN-025 for next work derived from tracked state with two readers dispatching the same work; neither says "ids a reader can trust to name one thing". The nearest stated outcome is SN-002's "a malformed/duplicate id fails at any stage". Remedy: cite SN-002 or re-word the waiver to SN-025's deterministic-dispatch clause, which unique allocation serves.
9. `SR-177.coincident`: SN-027 asks for ready work fanning out across bounded lanes with serialized landing; it does not ask whether the lanes pay off, and a report gates nothing and delivers no fan-out. Remedy: a waiver that states SN-027's outcome as SR-156's and this row as a measurement of it from the run's own telemetry relying on no outside party, with the PERFORMANCE lens named as its derivation.
10. `SR-011.coincident`: SN-001's re-sync clause (a re-sync never clobbers the repo's own files) is delivered by the row alone, but SN-007 asks that the kit stay traceable and tested through every change, and an idempotent re-run delivers none of that; the waiver is silent on SN-007, so the row's effect alone does not deliver the outcome one of its cited needs states. Remedy: drop the SN-007 citation (a traced-cell re-point; SN-001 alone is the honest parent) or extend the waiver with how the re-run serves SN-007, if it does.
11. `SR-111.coincident`: SN-001's re-sync is delivered only in part: a recorded kit base is a precondition of picking up updates, not the re-sync outcome the need states, and SN-007's trace-and-test outcome is not delivered by a version stamp at all; the waiver names a precondition as the outcome and is silent on SN-007. Remedy: re-word the waiver to what the stamp delivers of SN-001 (the base a re-sync reads, written by the generator) and drop or argue the SN-007 citation.
12. `SR-147.coincident`: SN-002's mechanical verification is delivered only as its precondition (one parseable carrier is what the verifier reads, which the waiver itself says), and SN-012's right-sizing outcome is not delivered by a carrier migration; the waiver is silent on SN-012. Remedy: re-word the waiver to SN-002's stated outcome and how the carrier makes the strict check possible, and drop or argue the SN-012 citation.
13. `SR-149.coincident`: SN-010's honest documentation is a fair reading for a retired-vocabulary report, but SN-004 asks that a team advance only through explicit gates whose mechanical bar is met, and a report of retired tags in authored surfaces delivers no gate outcome; the waiver is silent on SN-004. Remedy: drop the SN-004 citation (SN-010 alone is the honest parent) or extend the waiver with how the row serves SN-004, if it does.

FOLDED IN by the coordinator (wave-5 ruling 45), each as its adjudicator drafted it:

From WI-702's verdict:

The adjudication is recorded at
`docs/reviews/wi-702-adjudicate-llr-279-llr-280/001-ADJUDICATE-1d84d77c.md`,
governing line `OUTCOME: RETURN rows=8`: five rows approved and flipped in
batch C's narrowed act (LLR-279, LLR-280, LLR-281, TC-289, TC-291), three
returned with every cell byte-exact (SR-223, SR-224, TC-290). One draft
covers the three: two of the fixes are a test arm and a need's tag, the third
is the re-judging that follows.


VERDICT THIS CONTINUES: the file above. Every code symbol of LLR-280 and
LLR-281 resolves and every pointer of TC-290 and TC-291 passed on the tree at
1d84d77c; the returns are about what the cells CLAIM.

IN SCOPE — three rows, then a first-approval adjudication of the three.

1. `TC-290`: add a third arm, THE SHIPPED SET, asserting that the kit tree's
   `docs/guardrails/` holds no `core.<substring>.md` beside `core.md` (the
   kit ships no payload and names no model), with its pointer in Evidence
   and its sentence in Method; or, if the owner prefers, narrow SR-223's
   last acceptance clause and TC-290's Expected together. Either way the
   Expected's "Satisfies SR-223 AcceptanceCriteria" must be true of every
   clause.
2. `SR-223`: unchanged text unless the clause is narrowed under item 1;
   re-judged once TC-290 reaches the clause. Fill its `Coincident` cell (it
   cites no assumption and is reported unclassified) in the same amendment,
   under the test WI-695's second sitting states.
3. `SR-224`: THE OWNER'S HALF FIRST — SN-005's `tags` carry `shell` alone,
   and FIRST-RUN-ADOPTER's `when` fires on `scripts`, `templates` or
   `process`; SN-005 is the playbook need, so `process` is the honest tag.
   That is a needs-tier amendment on the owner's brief, not this lane's.
   Once it lands and `hats.py applicable` over SN-005's tags lists
   FIRST-RUN-ADOPTER, SR-224 is re-judged on its unchanged text; fill its
   `Coincident` cell in the same act. If the owner declines the tag, the row
   needs a lens that does reach SN-005 or a different parent.

OUT OF SCOPE: LLR-279, LLR-280, LLR-281, TC-289 and TC-291 (approved and
anchored by batch C's act); SN-026's acceptance (the verdict advises against
widening it).

From WI-694's verdict:

The adjudication is recorded at
`docs/reviews/wi-694-adjudicate-llr-271-llr-272/001-ADJUDICATE-1d84d77c.md`,
governing line `OUTCOME: RETURN rows=10`: nine rows approved (LLR-271,
LLR-272, LLR-273, LLR-277, LLR-278, TC-269, TC-270, TC-271, TC-278) and one
returned with every cell byte-exact (TC-272). One draft, one cell; the
coordinator may fold it into an open item rather than mint it.


VERDICT THIS CONTINUES: the file above. Every one of TC-272's five evidence
pointers resolves and passed on the tree at 1d84d77c (three in
`tests/test_spine_carrier.py`, fast batch; two in
`tests/test_snapshot_readers.py`, slow batch), and LLR-277, the design row it
verifies, is approved: the return is about what the Tier cell CLAIMS, not
what the tests do.

IN SCOPE — one row, then a first-approval adjudication of it.

1. `TC-272.tier` reads `Smoke` while
   `tests/test_snapshot_readers.py::test_the_snapshot_history_reader_takes_the_needs_carrier_from_the_file`
   and
   `tests/test_snapshot_readers.py::test_a_markdown_needs_file_is_compared_like_a_toml_one`
   sit in a `tests/conftest.py` `SLOW_MODULES` member, so the Method's
   "the record's history reader ..." and "A scaffold whose needs file is
   markdown ..." arms do not run in the per-commit tier the cell claims. The
   assignment's rule and batch B's TC-204 return (WI-681, remedied by the
   TC-204/TC-274 split in WI-616) apply to the same fact. Remedy, either:
   (a) SPLIT — keep TC-272 at `Smoke` over the three in-memory pointers and
   the three in-memory sentences of its Method, and author a Full case
   (Verifies `SR-147;LLR-277;IF-112`, Level Integration, Evidence the two
   slow pointers) carrying the history-reader and markdown-scaffold
   sentences; or (b) RE-TIER — set `tier = "Full"` and keep the case whole.
   (a) keeps the carrier rule's cheap half in the commit bar, which is where
   a sniffing regression would be caught first, so it is the better of the
   two. Every other cell of TC-272 stands as adjudicated.

OUT OF SCOPE: LLR-277 (approved in this act; its chain reads incomplete until
this lands, which the derived stage carries), and the tier advisory class
LLR-260 reports for Full cases over fast modules elsewhere.

OUT OF SCOPE: the sixty-six blessed waivers (re-attested by a later act on the
verdict as it stands, SR-180 among them: the third sitting found it serves SN-003 through its own
skipped-with-reason clause for units the declared stack profile has no resolution rule for, as well as
SN-002, so its waiver holds for every need it cites); SR-223 and SR-224's empty cells (WI-702's return).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-011 [project-trajectory/scripts/bootstrap.py :: copy_kit_files/--force + write_kit_version] tests: (see TC-011) — Idempotent write + kit-version stamp
- LLR-015 [project-trajectory/scripts/trace.py :: analyze] tests: (see TC-015) — PB back-link resolution
- LLR-024 [project-trajectory/scripts/gen_cases.py :: main] tests: (see TC-024) — Permutation expander
- LLR-025 [project-trajectory/scripts/gen_skills_index.py :: main] tests: (see TC-025) — Skills index generator
- LLR-031 [project-trajectory/scripts/check_privacy.py :: _first_declared_line] tests: (see TC-031) — Shared declared-line parse
- LLR-033 [project-trajectory/scripts/gen_release_checklist.py :: main] tests: (see TC-033) — Release checklist generator

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency
- CMP-009 W4 Human & adopter surfaces: downstream-resync

### Interface seams via the touched modules
- IF-001 scripts/trace -> scripts/check: stdout orphan, integrity, status and advisory findings, printed whole for the harness to relay
- IF-145 scripts/trace -> scripts/check: exit-code 0 clean · 1 a finding under --strict, an integrity finding under --strict-integrity, or a stale brief under -…
- IF-146 scripts/trace -> external:downstream adopter: file docs/test/report.md — metric counts, the orphan and finding lists, the joined SN -> SR -> LLR -> TC forest
- IF-166 scripts/trace -> external:downstream adopter: file docs/test/report.html — a self-contained collapsible <details> tree of the SN -> SR -> LLR -> TC forest, writ…
- IF-005 scripts/check_privacy -> scripts/check: stdout one line per leak: <location>: [<label>] <excerpt>, then one summary line naming the scan and the armed layers
- IF-148 scripts/check_privacy -> scripts/check: exit-code 0 clean or both layers off · 1 one or more findings in the tracked-file sweep
