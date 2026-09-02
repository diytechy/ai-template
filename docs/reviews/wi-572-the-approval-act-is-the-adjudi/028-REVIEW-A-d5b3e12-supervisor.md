### REVIEW-A — WI-572 — Round 028 — 2026-09-02 — supervisor-drawn (independent Opus, hostile brief)

Scope `4d0b972d..d5b3e124` (work tip; only telemetry commits follow). Rework for
round 023 is `83b8ec80..d5b3e124`. Nothing in the tree was edited except this file.

## What I verified

### Round 023's five findings, claim by claim

**MAJOR 1 (`SPINE_CSVS` blind to the four other snapshotted tiers).** The rework
took the review's SECOND remedy — narrow the doctrine — and closed the set rather
than widening the rung. Driven at the real merge slot on four scaffold lanes built
from `tests/integrate_fixtures.claim_repo` (`integrate._approval_act_refusal`):

```
--- sn        adjudication_lane= False   refusal: None
--- iface     adjudication_lane= False   refusal: None
--- sn-snap   adjudication_lane= False   refusal: wi-401 performs an APPROVAL ACT ...
--- sr-control adjudication_lane= False  refusal: wi-401 performs an APPROVAL ACT ...
SNAPSHOTTED: ['docs/requirements/stakeholder-needs.toml', 'docs/requirements/system-requirements.toml', 'docs/requirements/low-level-requirements.toml', 'docs/test/test-cases.toml', 'docs/requirements/interfaces.toml', 'docs/requirements/external.toml', 'docs/requirements/components.toml']
SPINE_CSVS: ['docs/requirements/system-requirements.toml', 'docs/requirements/low-level-requirements.toml', 'docs/test/test-cases.toml']
OUTSIDE:    ['docs/requirements/stakeholder-needs.toml', 'docs/requirements/interfaces.toml', 'docs/requirements/external.toml', 'docs/requirements/components.toml']
```

So: an SN flip and an `interfaces.toml` flip still merge clean, an SN flip that
also writes `SNAPSHOT_DIR` is refused (the snapshot arm is registry-blind), and the
SR control still bites. That is now what the doctrine SAYS, on all three surfaces
the finding named — `PROCESS.md:421` ("a spine row's `Status` flip"),
`PROCESS_OPTIONS.md:458` ("**Never on a spine row**") plus the new
`PROCESS_OPTIONS.md:470-478` bound paragraph, and `gate-advance/SKILL.md:106-117`
(all three skill copies identical), which now says the SN half of DevStg-Reqs rests
on the procedure alone. The refusal text itself was narrowed too ("in those three
registries", `acceptance_record.py:710`). The closure property is real and pinned:
`SPINE_CSVS | OUTSIDE_THE_APPROVAL_ACT == SNAPSHOTTED`, exhaustive and disjoint
(`tests/test_acceptance_record.py::test_no_snapshotted_tier_can_go_unseen_by_the_approval_rung`),
and the deliberate half is driven on a real git tree
(`::test_an_off_spine_status_flip_is_not_the_act_this_rung_refuses`). The doctrine
and the rung now agree; the UNCOVERED half the review named is covered. **Fixed.**

**MAJOR 2 (unquoted `{registries}`).** Composed the live brief
(`adjudicate_brief.compose` on THIS repo, `Adjudicates="LLR-205;TC-199"`) and handed
the rendered argument to a real shell:

```
2. Take the anchoring snapshot in the SAME commit: `python scripts/intake.py snapshot --approves "docs/requirements/low-level-requirements.toml=this adjudication;docs/test/test-cases.toml=this adjudication"`. ... KEEP THE QUOTES: ...
CMD ARG: "docs/.../low-level-requirements.toml=this adjudication;docs/test/test-cases.toml=this adjudication"
bash tokenisation of the arg alone: 'docs/.../low-level-requirements.toml=this adjudication;docs/test/test-cases.toml=this adjudication\n'  (ONE argument)
```

`intake.py:800`'s placeholder line is quoted the same way. The pin
(`test_the_rendered_snapshot_command_survives_a_shell`) is bite-proofed both ways —
it asserts the premise (`";" in command`) and that the same string unquoted counts
as TWO commands. **Fixed.**

**MAJOR 3 (`{registries}` derived from everything offered, not what was approved).**
The remedy taken is the review's first option: a new `{approves_rows}` slot maps each
`;`-token to its row ids, and template step 2 states the DROP rule. Driven live:

```
registries:  'docs/requirements/low-level-requirements.toml=this adjudication;docs/test/test-cases.toml=this adjudication'
approves_rows:
    - `docs/requirements/low-level-requirements.toml=this adjudication` covers LLR-205
    - `docs/test/test-cases.toml=this adjudication` covers TC-199
```

and the merge slot's own arms driven directly
(`acceptance_record.adjudication_approval_refusal`, scope `{LLR-205, TC-199}`, one
LLR flip): token kept -> `snapshot WIDENED to docs/test/test-cases.toml without an
approved row` + a per-arm `Remedy —` paragraph; token dropped -> `None`; flip with no
snapshot -> `was approved WITHOUT its anchoring snapshot`; foreign row -> `TC-999 is
OUTSIDE ... scope`. The de-dup regression the rework mentions is real
(`_render_chain` now accumulates a per-registry ordered set;
`test_a_row_hanging_under_two_SRs_is_named_once_in_its_token`). The structural
residual the review named (the scope is typed before the verdict exists) is stated,
not silently closed — acceptable, it was flagged as out of scope. **Fixed as offered.**

**MINOR 4 (complexity re-stamp).** Reasons were added rather than the rows repaired —
again the option the review offered. I re-measured the ABSORBED claim independently:
`git archive 4d0b972d | tar -x` into a scratch tree, then
`check_complexity.py --root <base>` over that untouched tree FAILS on exactly
`baseline_snapshot::_authorised_registries`, `baseline_snapshot::copy_live 19 -> 21`,
`dispatch::_advance 16 -> 20`, `gen_open_items::_none_declaration_findings`,
`handback::close_adjudication`, `intake::_disposition_drafts 21 -> 25`,
`intake::_replace_inbound_edges`, `trace::_cell_diff_lines`. Eight of the nine
reasons are TRUE and now verifiable. The ninth is not — see MAJOR 1 below. At the
tip `check_complexity: OK - 201 row(s) over 15, unchanged from baseline`.

**MINOR 5 (the two generators still said WHOLESALE).** `trace.py:3981-3987`,
`gen_open_items.py:806-812` and the regenerated `docs/ratify/CURRENT.md:11` now state
the WI-571-scoped rule. `grep -rn WHOLESALE` over live files leaves three hits: the
copy-scope PLAN (a historical quotation, correct), `acceptance_record.py:1047` ("at a
signing", defensible), and `baseline_snapshot.py:153` — see MINOR 4 below. **Fixed at
the two sites named; one residual.**

### Earlier rounds' fixes — no regression

Ran the six covering modules at the tip: `pytest -q tests/test_integrate_station.py
tests/test_integrate_admission.py tests/test_acceptance_record.py
tests/test_adjudicate_brief.py tests/test_intake.py tests/test_wi_convert.py` ->
`199 passed in 54.49s`. The named arms all still have live, named pins and passed:
the `format_approves`/`parse_approves` `;` round trip; the dial filter
(`test_the_first_approval_brief_never_hands_the_judge_a_HELD_row`,
`test_a_held_rung_mints_no_first_approval_row`); the terminal instruction branching
(`test_the_first_approval_brief_cannot_stop_before_its_approved_act`,
`test_the_MEANING_aftermath_is_DERIVED_from_the_dial_not_left_to_the_judge`); the
demotion feeding the trigger (`test_a_status_only_withdrawal_mints_first_approval_adjudication`,
and `_approval_act` returns None on a de-approval by construction); the
adjudication-lane exemption bounded to the adjudicated rows and TESTED (six scope
cases at `_approval_act_refusal`, driven again above).

### Instruments on this tree

- `pytest -q -n auto -m smoke` (once): **`1463 passed, 4 skipped in 20.85s`**, exit 0
  — well inside the 60 s ceiling.
- `check_trajectory.py` (non-strict): exit **0**, `clean (569 work item(s), 527 done
  (93%), 21 cancelled, graph acyclic)`; only the pre-existing shared-spec-of-record WARNs.
- `trace.py --strict-integrity`: exit **0**, `SN=27 SR=76 LLR=188 TC=187 orphans=2
  integrity=0 ... provenance-findings=1 paraphrase-advisories=3` — identical to round 023's.
- `check_docs.py --root . --stale`: exit **0**, `OK - 1218 doc(s), 1586 intra-repo
  link(s), 0 broken (1 orphan warning(s))`; only link-mtime hints.
- `gen_prompt_catalog.py --check`: `fresh (8 prompts)`, exit 0.

**The `wi_convert` README defect (round 012 MAJOR) IS fixed by this lane.**
`read_specs` now takes its population from `spec_paths` (`wi_convert.py:608-632`), so
`docs/work/cancelled/README.md` is residue to both sides. Driven on the live tree with
`docs/work/active/` drained (it is: the branch's own claim directory is empty):
`read_specs(docs/work)` -> `rows: 24`, `cancelled/README seen: False`, and
`test_wi_convert.py -k round_trips` -> `3 passed`. The smoke tier above is therefore
green in the post-close state, not merely behind a `drained-stop`.

### Byte budgets (`wc -c` at the tip vs the guard's stamps)

| file | stamped | measured | delta |
|---|---|---|---|
| `PROCESS.md` | 88,355 | **88,365** | +10 |
| `PROCESS_OPTIONS.md` | 185,555 | **186,240** | +685 |
| `AGENTS.template.md` | 9,980 | 9,980 | 0 (cap 10,000) |
| `CLAUDE.md` | 7,886 | 7,886 | 0 (cap 8,500) |
| `byte-budget-guard/SKILL.md` | 4,982 | 4,982 | 0 (cap 5,000) |

Both capped rows and the guard's own row are exact; both WATCHED rows are stale by
the rework's own growth. The growth itself IS flagged with deltas and reasons in the
fragment (lines 932-934), so the reporting duty is met; the table was not re-stamped.
See MINOR 3.

### The record (`docs/archive/work/complete/WI-572-the-approval-act-is-the-adjudi.md`)

`## Deliverable` precedes `## Context`. Arms 1-5 re-read against the tip: every
mechanism claim I could drive is true (the scoped ban, the closed bound, the derived
and now-quoted `--approves`, the per-arm remedy, the `wi_convert` repair, the test
counts — I counted the six scope cases and the five new regressions). The fragment
`docs/log.d/WI-572-approval-act-adjudicator-only.md` carries the pre-ruling census
(1 worker-lane flip at `580df781`, 4 born-`Approved` lanes) with `fig:` provenance on
it (line 25) and the file-level `Deferred open items: none` (line 349). One Context
claim is stale — MAJOR 2 below. I also re-derived the lane's own compliance:
`lane_approval_refusal(4d0b972d, d5b3e124)` -> `None`, `staged_approval_acts` -> `[]`,
`staged_drafted_rows` -> `[]`. The standing constraint is honoured.

## Findings

- [MAJOR] docs/complexity-baseline:134 -> the reason added to `plan_round.py::_advance` is FALSE in both of its factual claims: it says "16 -> 20" and "measured over the untouched tree at the WI-572 integration base 4d0b972d, where `check_complexity` already FAILED on this row" -> the row is `18 18` at 4d0b972d and `18 18` at d5b3e124 (`git diff 4d0b972d d5b3e124 -- docs/complexity-baseline` shows the LINE changing only by the appended reason), and `check_complexity.py --root <archive of 4d0b972d>` does NOT list `plan_round.py::_advance` among its nine FAILs — it names `dispatch.py::_advance 16 -> 20`, whose text this reason appears to have been copied from. The eight other reasons this commit added are verifiably true; this one attaches an absorbed-trunk-debt story to a row that neither moved nor failed, in the one file whose header rule is "a row is a DEBT STATEMENT, NOT AN APPROVAL" and whose loosening round 023 required to be a reviewed act -> delete the reason from line 134 (the row carries no debt this branch absorbed), leaving the eight true ones -> author. (Construction-first: no guard is proposed. The reason column is free text that `--restamp` neither writes nor checks, which is why a copied sentence is representable; the smallest change that would make it unconstructible is for `--restamp` to WRITE the measured `before -> after` into the reason it stamps, so the numbers in the prose and the numbers in the row have one producer — worth a follow-up row, not this one.)

- [MAJOR] docs/archive/work/complete/WI-572-the-approval-act-is-the-adjudi.md:124-130 -> the Context's compliance attestation says "It amended two rows its own code made stale — `LLR-158`'s `code_symbol`/`Detail` ... and `IF-091`'s requestors" and "`staged_spine_amendments` reports `LLR-158`" -> at the tip the branch amends THREE registry rows, and the reader reports TWO: driving this row's own reader over its own delta, `staged_spine_amendments(4d0b972d, d5b3e124)` returns `LLR-136` (approved cell `Detail`) and `LLR-158` (approved `Detail`, traced `CodeSymbol`). `LLR-136` is `Approved`, was re-pointed at `a68cc52a` and amended again in `d5b3e124` (the `wi_convert.read_specs` repair), and is correctly recorded in the FRAGMENT (lines 585, 979) and in `d5b3e124`'s own commit message — only the archived WI record, which is the durable artifact, under-reports it. The attestation's conclusion (no flip, no snapshot, amendment permitted) is unaffected and true; the enumeration of which Approved spine rows this lane touched is not -> name `LLR-136` alongside `LLR-158` in both sentences, and say "three rows" -> author.

- [MINOR] project-trajectory/skills/byte-budget-guard/SKILL.md:49-50 -> both WATCHED baselines are stale at the tip and their "Latest change" cells describe the PREVIOUS round: `PROCESS.md` stamped 88,355 vs measured 88,365, `PROCESS_OPTIONS.md` stamped 185,555 vs measured 186,240 (`wc -c`; and `git show 83b8ec80:...` confirms both stamps were exact before this rework, so the drift is this commit's) -> the skill's own rule is "NOTHING PINS THESE ... so re-stamp on the way past", and round 023 verified every stamped number as exact, so this is a regression in the row the guard exists to keep honest — though the deltas ARE flagged with reasons in the fragment (lines 932-934), which is the reporting half of the duty -> re-stamp both Baseline cells to 88,365 / 186,240 and re-word the two "Latest change" cells to this round's edit -> author. (Construction-first: this is the exact failure `tests/test_bootstrap.py::test_capped_doc_baselines_match_the_real_sizes` was written for after the 2026-08-21 M-7 finding — it pins the CAPPED rows' Baseline cells against `wc -c` and leaves the watched half unpinned. The smallest change that makes this class of drift unrepresentable rather than re-detectable is to extend that same test over the watched table it already parses; that is a one-test edit in an existing home, but it is a guard, so it belongs to a follow-up row rather than to this diff.)

- [MINOR] project-trajectory/scripts/baseline_snapshot.py:153 -> the module's own `SNAPSHOT_DIR` comment still states the pre-WI-571 rule — "it is REPLACED WHOLESALE at each approval, never migrated in place" -> false since the copy was scoped, and contradicted 636 lines below by `copy_live`'s own docstring ("a refresh copies ONLY the registry a `Status` move happened in plus every registry `approves` names ... a registry OUTSIDE the act's scope is not touched at all"). This is the same retired sentence round 023 MINOR 5 found, at a third site the finding did not name; the reader most likely to trust it is the next author of this module. (`acceptance_record.py:1047` says "replaced WHOLESALE at a signing", which a `--seed` still is, so I do not call that one false.) -> re-word line 152-154 to the scoped statement, matching the docstring -> author.

VERDICT: CHANGES-REQUESTED findings=4
