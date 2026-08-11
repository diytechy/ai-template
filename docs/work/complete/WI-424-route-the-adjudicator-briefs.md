+++
id = "WI-424"
title = "Route each ADJUDICATE session to its own adjudicator brief - the four templates are authored, shipped, catalogued, and consumed by NOTHING. SN-032 moved the loop's prompts into files and authored four adjudicator briefs (adjudicate-amendment, adjudicate-disposition, adjudicate-conflict, adjudicate-red-tc); SN-026 gave adjudication rows their own routed phase, tier and cross-family rule. The seam between them was never built: agent_loop.route_session composes EVERY non-review session from the generic worker prompt, so an adjudication row routes to a strong cross-family model and then receives an implementer's instructions. The judge is briefed as a builder. TWO THINGS THIS ROW MUST DECIDE, and the second is why it was not done inside the program that found it. (1) THE DISCRIMINATOR: which of the four briefs a row wants is a typed fact, and the row does not currently carry it - the options are a new frontmatter key (honest, but a schema change across three F5-synced loaders), or derivation from the SpecRef cell (a spine CSV means amendment, a terminal spec means disposition, test-cases.csv means red TC), which costs nothing but infers rather than declares. Prefer the declared field unless the schema cost is real. (2) THE SLOTS: each brief demands assembled EVIDENCE - adjudicate-amendment wants {baseline} and {rows}, adjudicate-conflict wants {mechanical}, {open_rows}, {spine} and {digests}, adjudicate-disposition wants {report} and {evidence}. Those are real derivations (a baseline diff via trace._attested_baseline, the queue-conflict findings, a spine excerpt), and a half-filled brief is WORSE than the generic prompt: a judge's brief with hollow sections reads as though the evidence was looked for and found wanting. Fill every slot faithfully or leave the template unrouted. Done when: an adjudication row's session provably receives its own brief (fake-CLI prompts.txt capture, one test per template), the typed verdict line each brief demands is written to the declared path, and no slot is filled with a placeholder."
workstream = "scripts"
specref = ""
buildtier = "strong"
safety_class = "ordinary"
+++

## Deliverable

Two of the four adjudicator briefs are ROUTED and wired end to end; two are
left on the worker assignment with the derivation each is missing named in
`adjudicate_brief.py`'s header. The seam is
[`project-trajectory/scripts/adjudicate_brief.py`](../../../project-trajectory/scripts/adjudicate_brief.py)
(new) plus `agent_loop.session_body`, the one fork BOTH routing arms take —
managed and single-model, because which brief a claimed row gets is a property
of the ROW, not of whether a routing registry happens to be configured.

**(1) The discriminator: DECLARED, and the schema cost was measured, not
assumed.** A new column `Brief` (frontmatter `brief`), written by `intake` at
every adjudication mint. The spec said *prefer the declared field unless the
schema cost is real*; the cost is real but bounded, and the cheap alternative
is not merely inferior — it is **unsound**:

- `intake._amendment_drafts` sets `specref = records[0]["registry"]`, and
  `ROUTED_TRACED_CELLS` routes a test-case `Verifies` change. So an amendment
  to a TC row and a red-TC census row carry the **same** `SpecRef`
  (`docs/test/test-cases.toml`) — and those two briefs give contradictory
  instructions (one forbids touching a registry; the other asks for a `Status`
  cell to be judged). `records[0]` is also arbitrary when a batch spans
  registries. Under SpecRef derivation, wiring red-tc at all would ship a live
  mis-route. Pinned by `test_the_discriminator_is_the_declared_cell_not_the_specref`.
- Deriving from the Title is the `NEEDS-HUMAN` fold this repo wrote in blood
  (WI-417) — prose carrying control flow.

*Measured cost of the declared field:* the three F5-synced loaders
(`agent_common`/`check_trajectory`/`schedule`, two schema tables each, +10
lines verbatim per copy), `wi_convert.COLUMNS`+`SCALAR_FIELDS`,
`plan_artifacts.WI_HEADER`, `registries/work-items.template.csv`,
`intake._draft_row`, the `WI-000` template + its byte-identical dogfood copy,
and five module-size baselines. **No downstream migration**: the WI CSV is
retired (`check_trajectory` treats a stray one as an integrity error), so no
adopter holds a registry to widen. `intake._DRAFT_KEYS` is deliberately NOT
extended — `_draft_refusal` already refuses a hand-drafted
`safety_class = "adjudication"`, so no human authors this cell. This is the
`Supersedes` precedent applied verbatim, including its stated reason: *"a real
column, not a frontmatter-only key, because `intake` writes successors through
`wi_convert.write_spec_file`, which serializes from this table."*

**(2) The slots — the derivation map, and the two refusals.**

| Brief | Slot | Producing derivation |
|---|---|---|
| disposition | `{spec}` | `SpecRef` (typed cell) → the closed spec, verbatim |
| disposition | `{report}` | closed spec's id → `docs/handbacks/<id>-*.md`, newest, verbatim (SR-144: the report IS the event's identity) |
| disposition | `{evidence}` | the report's TYPED `commit_range` → `git log --oneline` + `git diff --name-status`, clipped at the declared 80 lines |
| red-tc | `{tcs}` | `dispatch.red_tc_census(root)` RE-RUN live → `dispatch.parse_red_tc` → the TC registry row's Verifies/Status/Method/Expected/Evidence |
| red-tc | `{spine}` | the parsed targets → SR `Requirement` / LLR `Detail` rows |
| all | `{verdict}` | `agent_loop.fresh_verdict_path` |
| all | `{wi}` | the row's own id — the result trailer (see below) |

**`amendment` is UNROUTED, and this is the finding.** Its `{rows}` slot names
`trace.reattest_model` as its producer, which selects SRs whose Status is
`Modified`. But `check_trajectory.staged_spine_amendments` — the function that
MINTS these rows — fires only when `head_status == cur_status == "verified"`
and no owning SR is flagged. **The two populations are disjoint by
construction**, so the declared producer returns nothing for exactly the rows
that exist. Worse, `{baseline}` wants *"the accepted anchor this diff is
measured against"*, and `trace._attested_baseline` (its own documented blind
spot) walks to the newest commit where the SR read `Verified` — for an
amend-without-flip row that is **the amendment commit itself**, i.e. the text
under judgement dressed as the accepted anchor. That is precisely the failure
the WI's own Context warns about. The row still DECLARES
`brief = "amendment"`; routing it is one `_ASSEMBLERS` entry away once the
anchor question is answered. **Owed:** a typed carrier for the `before..after`
pair (it exists today only inside the Title string) and a ruling on what an
un-flipped amendment's anchor IS.

**`conflict` is UNROUTED**: nothing mints a queue-conflict adjudication row at
all (`check_trajectory.queue_conflict_findings` is a warn that never becomes a
row), so there is no session to brief; and `{digests}` names a scope+spine
digest pair no function computes. Its notes also advertise a shared-`exclusive`
pre-filter signal that `queue_conflict_findings` does not implement.

**Fill in full or refuse.** Every assembler returns `(values, None)` or
`(None, reason)` — no placeholder, no `(none found)` filler. An unfillable
brief falls back to the worker assignment and PRINTS the reason (the
no-silent-swap rule). The clean-close spot-check arm
(`intake._complete_spot_checks`) writes no report, so it refuses by design.

**The templates gained the result trailer.** Committed trailers are the worker
contract's ONLY result channel (`agent_loop.worker_endstate`), and an
adjudicator brief is not the assignment that would otherwise have carried the
protocol — wired without it, a session writes and commits its verdict and the
row **never closes**. All four briefs now end with `` `WI: {wi}` `` (a new
declared slot; `CATALOG.md` regenerated). Found by the end-to-end test, not by
reading.

**Tests** — `tests/test_adjudicate_brief.py`, 16 tests, in the smoke tier
(1.6 s): the two routed briefs assembled from real fixtures, the fake-CLI
`prompts.txt` capture proving a claimed row's session receives ITS OWN brief
and lands the typed verdict line at the declared path, the fallback proving
the printed refusal, and the unrouted pair pinned as unrouted on purpose.

*Deviation from spec:* none in scope. Two things the spec did not anticipate
were required and are recorded above — the result trailer, and the amendment
brief's producer being structurally unable to serve it.

**The spine rows were mandatory, not optional.** `adjudicate_brief.py` first
shipped without one, and `test_meta_component_top_view_smoke` fails hard on it:
the meta suite asserts ZERO uncontained modules and containment is computed
from LLR `Component` cells. LLR-167 (SR-146/145/142, CMP-004) + TC-161, both
`Draft` at phase 5 like their parents.

*Observations filed, not fixed here (`CLAUDE.md`: surface a smell, don't fix it
inline):*

- `check_trajectory.module_components` does NOT split a `;`-joined `Module`
  cell — it normalizes the whole string into one key. So a multi-module LLR
  contains **neither** module. LLR-095 carries that latent shape today
  (harmless only because both its modules are contained by other rows).
- The `WI-000` frontmatter-key list was missing `adjudication` from the
  `safety_class` vocabulary (fixed here, since `brief` is meaningless without
  it) and is still missing `bar` and `supersedes` — pre-existing, not opened.
- `adjudicate-conflict`'s dispatcher notes advertise a shared-`exclusive`
  pre-filter signal that `queue_conflict_findings` does not implement.

 of the 2026-08-08 mechanized-loop program
(and independently by that program's own P4/P5 review agent), as MAJOR: *"all
four adjudicator templates are dead assets; every non-review session, including
`ADJUDICATE`, receives the generic worker template."* Verified — the four
`prompts.ADJUDICATE_*` constants have zero references outside `prompts.py`, and
`agent_loop.route_session` calls `worker_prompt` unconditionally on the
non-review branch.

**Why this was filed rather than fixed in that pass.** The program's own §8
scoped *authoring* the templates, and authoring is what shipped. Wiring them
needs the two decisions in the title, and the second one has teeth: the whole
point of these briefs is that **a judge's brief never contains the claim under
judgement** (the generalized WI-418 rule, `prompts/README.md`). A brief whose
`{evidence}` slot is filled with something thin does not fail loudly — it reads
as a completed investigation that found nothing, which is the most expensive
way for this machinery to be wrong.

Until this lands, the cost is bounded and visible: adjudication rows route to
the right MODEL at the right TIER with the right cross-family rule, and get an
implementer's prose. That is a worse brief, not a wrong verdict path — the
disposition's own `## Context` still carries the outcomes and the READ-IT-FIRST
instruction that intake derives.
