# ADJUDICATE — WI-601 — amendment at f263118

Question judged, per row, and the only one: did the amendment change the
requirement's MEANING, or only its CLARITY?

## The anchor

The rendered brief names its baseline as `docs/archive/last_approved`, "copied
2026-09-06 (commit cde260dd)". That stamp is the newest write anywhere in the
snapshot directory, and cde260dd copied `stakeholder-needs.toml` alone. The copy
this row is measured against is
`docs/archive/last_approved/docs/requirements/low-level-requirements.toml`, last
written at 2e1197fd (2026-09-04) (`git log -1` on that path). The stamp's
imprecision is part of the brief defect filed as WI-646.

## In-scope amended row: adjudicated here, counted (1)

This row's scope is LLR-061, which its title and `## Context` name. Loading both
sides and diffing every key: LLR-061 differs in `detail`, the approved cell the
brief shows, and in `code_symbol`, a traced cell ruled non-attesting (§A5.1).
The traced cell is read here anyway, because a re-anchor copies it too.
`sr_refs`, `title`, `module`, `test_refs`, `status`, `component` and `phase` are
byte-identical, and the row is `Approved` on both sides.

BEFORE, the `detail` cell obliges a builder to assemble the worker prompt from
AGENTS.md, the WI row, its SpecRef, predecessor context, the train diff and any
rework finding, and never from the generated status surface; the rest of the
cell (explicit assignment, collision-safe logs, the retired `--track`, the
branch as the assignment, the trailer result channel) is the same on both sides.

AFTER adds one clause: on a lane claimed with more than one row, the prompt also
names every assigned row with its id, title, SpecRef and walk state (`built`,
`started, not closed`, `this session's focus`, `not started`), taken from the
same two-part completion predicate the walk reads (a committed `WI:` trailer
AND the spec gone from `active/<branch>/`), so the brief never calls a row
`built` that the walk will return to. `code_symbol` gains `assignment_block`,
the symbol that clause names in code, which restates the same change.

- [MEANING] LLR-061 Detail -> the worker prompt carries the focus row's context (AGENTS.md, WI row, SpecRef, predecessors, train diff, rework finding) and never status -> the same, plus, on a multi-row lane, every assigned row with its walk state drawn from the walk's own two-part predicate -> a correct implementation of the BEFORE text (a prompt naming the focus row alone) fails the AFTER text on every lane claimed with two or more rows, and the new clause fixes a state vocabulary and its derivation that the BEFORE text never mentions.

## Rendered, out of scope, excluded from the count (19)

The amendment brief (`adjudicate_brief.amendment_values`) renders every drifted
approved row in the tree, not this row's scope: an amendment mint writes no
typed `Adjudicates` cell, and the assembler does not filter by one. The count
above follows the rule WI-566's review corrected its own verdict to
(`docs/reviews/wi-566-adjudicate-llr-058-llr-144/001-ADJUDICATE-05fb6a3.md`) and
WI-573 applied: a verdict counts its own row's scope. The whole-tree rendering is
filed as WI-646. **The rows below are not adjudicated here and are not counted
by the `VERDICT:` line.**

- SR-024, SR-033, SR-043, SR-052, SR-053, SR-054, SR-111, SR-112, SR-129,
  SR-144, SR-146, SR-147, SR-149, SR-167, SR-175, SR-176, SR-177 (`rationale`
  only): ruled CLARITY at WI-547 (fb0ed7c), WI-593 (ae3d788) and WI-599
  (993e455). Their live text is byte-identical to what WI-593 judged: each row
  was loaded from `ae3d788:docs/requirements/system-requirements.toml` and from
  the working tree, and all seventeen compare equal.
- SR-162 (`rationale`): adjudicated by WI-641.
- LLR-167 (`detail`): adjudicated by WI-603.

## Aftermath: judged blessable, joint re-anchor pending

The design-row tier sits above `human_approval_through = "DevStg-Needs"`, so the
brief's derived aftermath says a MEANING verdict here is re-attested by the
adjudicator, in its own reviewed commit after this verdict. Before that, the
AFTER text was checked as text I would bless:

- **Within its parent.** SR-026 requires a worker to resume "from its explicit
  claimed assignment plus the committed trailer evidence on its branch". Naming
  each claimed row's state, read from committed trailers and the claim
  directory, is that resumption made visible to the session. `worker_prompt`
  gains the claimed-row list as an input and the prompt gains content, but both
  come from the claim and the branch history SR-026 already names; no new actor,
  external input or surface class appears, and the status-surface prohibition
  is unchanged.
- **True of the code at f263118.** `agent_loop.assignment_block` renders the
  block and returns `""` for a one-row lane; `worker_prompt` takes the
  `assigned` list; both the block and the walk read `lane_completion`.
- **Exercised.** TC-061's evidence file, `tests/test_agent_loop_worker.py`,
  drives it: `test_worker_prompt_single_row_carries_no_assignment_block`,
  `test_worker_batch_prompt_names_every_assigned_row_and_its_state` and
  `test_the_brief_never_calls_an_unclosed_row_built` (with its mutation note).

Judged blessable. The re-attestation is the re-anchor itself: a separate commit,
scoped to `docs/requirements/low-level-requirements.toml`, taken once WI-603's
verdict is also recorded. The copy is whole-file, so taking it first would carry
LLR-167's amended text into the record before anyone had ruled on it (spine map
D28).

That copy also takes, as file-scope collateral and not as approvals, the 48
live-only Drafted rows (LLR-210, LLR-211 to LLR-252 and LLR-254 to LLR-258;
LLR-253 was deleted in review and does not exist) and the traced cells that
moved on approved rows since the anchor: thirty-one `module` cells re-pointed
into `project-trajectory/scripts/rendering/`, and the `code_symbol` cells of
LLR-061, LLR-160 (gains `queue_conflict_pairs`) and LLR-167. Traced cells are
non-attesting by ruling (§A5.1), and each of these was read.

## Finding, drafted with WI-603's

TC-061 is the case verifying LLR-061. Its `method` describes the
concurrent-worker contract and does not mention the multi-row block. The block
is tested in the case's own evidence file, so this is a gap in what the case
text claims, not in what is tested. It is folded into the one follow-up drafted
in WI-603's `## Dispositions` and filed as WI-645, beside the matching and larger
gap in TC-161.

VERDICT: MEANING rows=1
