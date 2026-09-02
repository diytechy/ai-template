### REVIEW-A — WI-572 — Round 029 — 2026-09-02 — supervisor-drawn verification (independent Opus)

Verification of the round-028 rework at tip `94b77a26` (`d5b3e124..94b77a26`), same
worktree. Nothing was edited except this file; no commits, no state-changing git.

## What I verified

### The SN extension, driven at the merge slot

Three scaffold lanes built from `tests/integrate_fixtures.claim_repo`, each seeded
with a `Drafted` SN row (TOML carrier), a `Drafted` SR row and a `Drafted` interface
row, then run through `integrate._approval_act_refusal`:

```
--- sn-flip     acts: [{'registry': 'docs/requirements/stakeholder-needs.toml', 'id': 'SN-001',
                        'act': 'flip', 'before': 'Drafted', 'after': 'Approved'}]
    refusal: ... A lane AUTHORS `Drafted` SN/SR/LLR/TC rows and AMENDS their cell text;
             in those four spine registries it does not flip a `Status` into `Approved`/`Founded` ...
--- sn-born     acts: [{... 'id': 'SN-002', 'act': 'born', 'before': '', 'after': 'Approved'}]
    refusal: (same, naming SN-002)
--- iface-flip  acts: []            refusal: None
```

So the SN flip AND the born-`Approved` SN row are both refused by name, at the real
rung, on both carriers (my scaffold uses `stakeholder-needs.toml`; the shipped test
uses the `.csv` carrier — the walk resolves each side independently, and I drove both).
The off-spine tier stays out. **No accidental widening**, checked two ways: on the same
three lanes `staged_spine_amendments` and `staged_drafted_rows` both return `[]` for
the SN deltas, and `grep` shows the only consumers of the widened name are the reader
itself and its two tests — `intake.py:1924,2044,2243` and `check_trajectory.py:4124`
still read `SPINE_CSVS`, unchanged.

**Held-rung mint.** Driven through the shipped helpers
(`test_intake.amended_repo` with the `seed` hook, dial set by `set_process_key`):

```
acts: [{'registry': '.../stakeholder-needs.csv', 'id': 'SN-001', 'act': 'flip', 'before': 'Drafted', 'after': 'Approved'}]
drafted (mint universe): []
held     -> minted: ([], None)
released -> minted: ([], None)
```

Both of the fragment's two stated reasons hold, and I drove the released case the
shipped test does not (see MINOR 2).

**Exhaustiveness pin.** `APPROVAL_ACT_CSVS = ['...system-requirements.toml',
'...low-level-requirements.toml', 'docs/test/test-cases.toml',
'...stakeholder-needs.toml']`, `OUTSIDE_THE_APPROVAL_ACT = ['...interfaces.toml',
'...external.toml', '...components.toml']`; against `baseline_snapshot.SNAPSHOTTED`:
`exhaustive: True disjoint: True subset: True`. `stakeholder-needs.toml` moved across,
so the pin is still a closed statement.

The premise the extension rests on is true, not asserted: `spine_carrier.SPINE_TABLE`
is `{"SN-ID": "need", "SR-ID": "requirement", "LLR-ID": "design", "TC-ID": "test"}` —
SN is a spine tier. And the "owner's own sitting is unaffected" claim is structurally
right: the refusal is only reached from `integrate._approval_act_refusal` over a lane
branch's merge delta; a hand-made trunk commit passes through no such slot.

### The four round-028 findings

1. **Complexity reason (MAJOR).** `docs/complexity-baseline:134` is back to bare
   `plan_round.py	_advance	18	18` — the copied reason DELETED, not re-stamped, and no
   row moved upward in this diff (`git diff d5b3e124 94b77a26 -- docs/complexity-baseline`
   is that one line). `check_complexity: OK - 201 row(s) over 15, unchanged from baseline`.
   The eight true absorbed-from-trunk reasons are untouched. **Fixed.**
2. **Archived record (MAJOR).** Now "It amended three rows ... `LLR-158`'s
   `code_symbol`/`Detail` ..., `LLR-136`'s `Detail` (also left `Approved`; the
   `wi_convert.read_specs` repair) and `IF-091`'s requestors", and
   "`staged_spine_amendments` reports `LLR-136` and `LLR-158`". Re-derived at the tip:
   `staged_approval_acts(4d0b972d, 94b77a26)` -> `[]`,
   `lane_approval_refusal` -> `None`, `staged_spine_amendments` -> `LLR-136`, `LLR-158`.
   Arm 4 of the Deliverable was also re-worded to SN/SR/LLR/TC + the OI-30 D3 exclusion,
   and matches the code. **Fixed, and the correction is itself true.**
3. **Byte stamps (MINOR).** `wc -c` vs the table, all three guard copies byte-identical
   at 4,831: `PROCESS.md` stamped 88,365 / measured **88,365**; `PROCESS_OPTIONS.md`
   stamped 186,421 / measured **186,421**; guard 4,831 / **4,831** (cap 5,000, headroom
   169 — the fragment's arithmetic checks out); capped `AGENTS.template.md` 9,980 and
   `CLAUDE.md` 7,886 unchanged. The +866 and +181 figures in the fragment both reconcile
   against `git show 83b8ec80|d5b3e124:...`. **Fixed** — with one attribution error, MINOR 1.
4. **The third WHOLESALE site (MINOR).** `baseline_snapshot.py:152-157` now states the
   WI-571 scoped rule in `copy_live`'s own words. `grep -rn WHOLESALE` over live files
   leaves the copy-scope plan's historical quotation and `acceptance_record.py:1047`
   ("at a signing", which a `--seed` still is). **Fixed.**

### Doctrine, and the deviation record

Every surface that said SR/LLR/TC now says SN/SR/LLR/TC and names OI-30 D3 for the
off-spine three: `PROCESS_OPTIONS.md:458` (table row) and `:470-481` (mechanism 1),
`gate-advance/SKILL.md:106` and `:111-119` — whose DevStg-Reqs bullet flips from "only
the SR half is MECHANICALLY held" to "BOTH are mechanically held", which is now what
the code does — in all three copies, plus the plan's §2a row and the WI record.
`PROCESS.md` §4 needed no edit ("a spine row's `Status` flip"), and none was made.
The fragment's "Round-028 rework" section states the deviation AS one, with the reason
(SN is a spine tier; DevStg-Reqs is the held rung; the section-as-state exclusion was
retired by the `status` cell), why `APPROVAL_ACT_CSVS` is a separate constant rather
than a widened `SPINE_CSVS`, and why the off-spine three stay out.

### Instruments at this tip

- `pytest -q -n auto -m smoke` (run ONCE): **`1463 passed, 4 skipped in 20.36s`**, exit 0.
- `pytest -q tests/test_acceptance_record.py tests/test_intake.py
  tests/test_integrate_admission.py tests/test_trajectory_staged.py
  tests/test_baseline_snapshot.py tests/test_adjudicate_brief.py` -> **`238 passed in 47.79s`**.
- `ruff format --check project-trajectory/scripts tests` -> **`231 files already formatted`**.
- `ruff check` (0.15.22) -> 3 errors, ALL pre-existing: `F401` in `tests/test_agent_loop.py`,
  `tests/test_trace_hats.py`, `F841` in `tests/test_trajectory_holdban.py` — none of the three
  files is touched by this branch, and the same 3 errors reproduce on a `git archive` of the
  integration base `4d0b972d`. Not attributed to this diff.
- `check_complexity.py` -> `OK - 201 row(s) over 15, unchanged from baseline`.

Observation, not a finding: Deliverable arm 5's test enumeration ("four at the trigger")
was not re-counted when the SN test joined `tests/test_intake.py` (five first-approval
cases there now). It reads as a description of the cases the row added rather than a
census, and nothing in it is false, so I record it here rather than as a finding.

## Findings

- [MINOR] project-trajectory/skills/byte-budget-guard/SKILL.md:49 (and the identical `.claude/` and `.agents/` copies) -> the re-stamped row attributes the `PROCESS.md` growth to "**+10** WI-572 round-027 rework (§4 wording)" -> session 027 committed nothing — `07822536 telemetry: session wi-572-...-027 BUILD NO-COMMIT`, as did 025 and 026; the +10 landed in `d5b3e124` (`git show 83b8ec80:project-trajectory/PROCESS.md | wc -c` = 88,355 vs `d5b3e124` = 88,365), which is session 024's rework of REVIEW round 023. The byte NUMBERS in all three rows are exact — only the round label is wrong, and it points a future reader at a session whose own telemetry says it changed nothing -> re-word to "the round-023 rework (session 024)" in all three copies -> author.

- [MINOR] tests/test_intake.py:404-411 -> the mint half's inline comment says "The mint half: held rung, nothing minted. Then released, still nothing — the mint's universe is `SPINE_CSVS`, unchanged by this round", but the test drives only the HELD case: it calls `set_process_key(root2, "attestation", "human_approval_through", kit_ladder.STAGE_NEEDS)` and asserts `minted == []`, and never releases the dial -> the neighbouring `test_a_held_rung_mints_no_first_approval_row` shows the house standard for exactly this ("...and the SAME delta on a released dial does mint" via `_released(root)`), so the omission is a departure from the file's own pattern. I drove the missing half myself and the claim is TRUE — `_released(root)` then `intake.intake_after_merge` returns `([], None)` — so this is an unexercised claim, not a false one; but it is the second of the docstring's "two independent reasons" that nothing pins, and if the mint universe were widened later, only the held reason would fail the test -> add the `_released(root)` half (two lines, mirroring the neighbour), or drop the sentence -> author. (Construction-first: no new guard — this is one existing test gaining the assertion its own comment already claims, inside the module that owns the trigger.)

VERDICT: APPROVE findings=2
