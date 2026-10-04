# ADJUDICATE (amendment, round 2): WI-791, twelve amended rows at db891d7f

An independent spine adjudicator (Claude Opus) re-judged this amendment after fix round 2. It
made none of the changes it judges; in round 1 it wrote the fixes this round applies
(`001-ADJUDICATE-AMENDMENT-ab06150.md`), and it judges here whether they landed as required.
It also judges the three details that round 1 flagged as owed outside its rows. The judgement used the
kit brief recomposed at db891d7f, read in the lane as the owner directed on 2026-10-03 (S11).
The anchor is unchanged: `docs/archive/last_approved/`, with system-requirements at 1fda46ed,
low-level-requirements at 439a2bb0 and test-cases at a9791303.

## What fix round 2 changed, checked

A cell-by-cell comparison of ab061501 and db891d7f finds exactly these moves:

- LLR-118, LLR-153, LLR-158, LLR-167, LLR-271 and LLR-278: `detail`.
- LLR-245: `detail` and `sr_refs`.
- TC-153: `method`.
- TC-240: `method`, `expected`, `verifies` and `evidence`.
- TC-278: `method` and `evidence`.

No `Status` moved, no system-requirements cell moved, and no script changed.

- Fixes 1-7: each cell named in round 1 equals, byte for byte, the replacement round 1 built:
  LLR-153, LLR-158, LLR-245 and LLR-278 `detail`; TC-153 `method`; TC-278 `method` and
  `evidence`; TC-240 `method`, `expected` and `evidence`. LLR-245 `sr_refs` is
  `["SR-207", "SR-228"]`, and TC-240 `verifies` is `["SR-207", "SR-228", "LLR-245"]`.
- The tests: the four tests round 1 prescribed are in `tests/test_snapshot_readers.py` and
  `tests/test_baseline_snapshot.py`, byte for byte. The narrowed assertion is in place.

## Baseline and mutation probes

The probes ran on a fresh scratch export of db891d7f (`git archive`, outside the lane). Each was
reverted before the next, and the lane was never touched.

Baseline at db891d7f, all passed:

- held-rung and scope readers: 12 passed;
- verdict ledger: 6 passed;
- open-items: 50 passed;
- adjudicate brief: 67 passed;
- needs and stakeholders: 9 passed.

The round-1 survivors, re-run against the lane's own tests:

| # | Mutation | Result |
|---|---|---|
| M2 | a conflicting tag: the last one wins | caught (`..._row_ruled_both_ways_reads_MEANING_and_is_refused`) |
| M5 | only a MEANING ruling refused | caught (`..._verdict_does_not_rule_is_refused`, `..._verdict_is_unreadable_is_refused`) |
| M11 | an absolute path outside the repository admitted | caught (`test_a_verdict_outside_the_repository_is_refused`) |
| M12 | a verdict without `--reattests` admitted | caught (the narrowed assertion) |

Round 1's caught probes stand, because db891d7f changed no code and only added tests: M1, M3,
M6b, M7, M8, M9, M10, M13 and M13b.

New probes, one per clause the three new details state:

| # | Mutation | Clause it breaks | Result |
|---|---|---|---|
| P1 | the audit list ordered oldest first | LLR-118 "newest first" | **survived** |
| P2 | no "None recorded" state | LLR-118 "or states None recorded" | caught |
| P3 | the audit block dropped from the page | LLR-118 "renders the owner audit list" | caught |
| P4 | DA and SUR dropped from the unchained tiers | LLR-167 "need, assumption and surrogate scopes" | **survived** |
| P5 | unchained rows not bounded by the scope | LLR-167 "renders their drifted approved cells" (the scoped rows') | **survived** |
| P6 | the held arms swapped: CLARITY told to recommend, MEANING to re-attest | LLR-167 "takes its held-rung arm from adjudication_action" | **survived** |
| P7 | tier_owing walks only the first tier | LLR-271 "applies owing_rows to an explicit ordered set of tiers" | caught (`test_a_drifted_approved_stakeholder_is_reported_and_briefed`) |

P6 is the one that matters most. The brief would tell a session to re-attest a MEANING row on a
held rung, and to stop on a CLARITY row. The held-rung merge rule would still refuse that
re-attestation, but the instruction the judge reads would be the opposite of the ruling, and no
test would notice.

The tests prescribed below in Fixes 8 and 9 were run on the same scratch export. They pass on
the unmutated code (3 passed) and kill P1, P4, P5 and P6.

## Rulings

- [MEANING] LLR-118 detail -> before: gen_open_items renders the pending decisions and the Draft/Modified chains, with the stamp, the empty-state and the mask contracts, and owns no second opinion -> after: the same, plus verdict_reattest_block renders the owner's audit list of every act-ledger entry naming a verdict, newest first, or states None recorded -> not the same: a new rendered list. The sentence is accurate to the code, and P2 and P3 are caught. But "newest first" is verified by nothing (P1 survives: the one test has a single verdict-naming act), and TC-123, the row's test case, names the test in its evidence while its method describes no audit list. RETURN: the row's own text needs no change; Fix 8.
- [MEANING] LLR-153 detail -> the round-1 anchor obligations -> those obligations, with the widened trigger (a), the routed traced cells as the code declares them, the archive sweep, the write-nothing flip arms and adjudication_action's three arms -> not the same: the arms and the walk moved. It is Fix 1 byte for byte, restores every clause the first rewrite dropped, and is accurate to the code; M7, M8 and M9 are caught. I bless it.
- [MEANING] LLR-158 detail -> the round-1 anchor obligations -> the same, with SPINE_CSVS read by the drafted-row reader and its mint only, and AMENDMENT_CSVS (an alias of APPROVAL_ACT_CSVS) walked by staged_spine_amendments for the warn and the amendment mint, Hat-Refs silent on SN, DA and SUR -> not the same: the amendment universe widened. It is Fix 2 byte for byte, keeps every clause the code keeps, and is verified by TC-153 as now written; M8 and M9 are caught. I bless it.
- [MEANING] LLR-167 detail -> before: the brief selection, the assemblers and their refusals, and amendment_values over reattest_model's rows bounded by scope -> after: the same, plus _unchained_amended_rows renders the drifted approved cells of need, assumption and surrogate scopes through tier_owing, and the held-rung aftermath takes its arm from adjudication_action -> not the same: two new behaviours. The sentence is accurate to the code. But three of its clauses are verified by nothing: the assumption and surrogate tiers (P4), the scope bound on those rows (P5), and which verdict gets which held-rung arm (P6). TC-161's method describes none of them, though its evidence names two tests. RETURN: the row's own text needs no change; Fix 9.
- [MEANING] LLR-245 detail, sr_refs -> the round-1 anchor obligations -> the same, plus --verdict: verdict_rel normalizes, _refuse_verdict refuses a verdict with no re-attested row, outside the repository or naming no file, and the act ledger records the normalized verdict; it traces SR-228 too -> not the same: the verdict argument is new. It is Fix 3 byte for byte, accurate to the code, and verified by TC-240 as now written; M10, M11, M12 and M13 are caught. I bless it.
- [MEANING] LLR-271 detail -> before: the need and stakeholder tiers compared with their recorded copy through owing_rows and needs_owing -> after: the same, plus tier_owing as the generic form that needs_owing delegates to, walking an explicit ordered set of tiers -> not the same: a new reader entry point. It is accurate to the code: needs_owing is tier_owing over NEED_TIERS, so TC-269's need and stakeholder cases exercise it, and P7 is caught. Its use by the amendment brief is LLR-167's to verify. I bless it.
- [MEANING] LLR-278 detail, title -> the round-1 anchor obligations (scope refusal only) -> the same, plus the held-rung refusal read at trunk's tip: a row below approval or absent, an act naming no verdict, or a verdict not ruling the row CLARITY is refused, MEANING winning a conflicting tag -> not the same: a new refusal. It is Fix 4 byte for byte, and every clause is pinned: M1, M2, M3, M5 and M6b are caught. I bless it.
- [CLARITY] SR-178 acceptance_criteria -> any artifact whose text moved from its recorded copy is reported, a stakeholder need included -> the same, naming stakeholder needs, assumptions and surrogates -> the same obligation, as ruled in round 1: assumptions and surrogates were already recorded artifacts (SNAPSHOTTED, SNAPSHOT_TIERS), so the first clause already covered them.
- [MEANING] TC-147 method -> the round-1 anchor method (the flip arms enact) -> the write-nothing arms, the unreadable dial or stage held, adjudication_action's arms, and the need, assumption and surrogate mint -> not the same, as ruled in round 1. Every clause is pinned by a named test, and M7, M8 and M9 are caught. I bless it.
- [MEANING] TC-153 method, verifies, evidence -> the drift half verifying SR-178 and LLR-158 -> the same, plus IF-091, with the method now stating the amendment-walk constant test and the staged need-amendment test -> not the same: the claimed scope widened. It is Fix 5 byte for byte, the method now describes every test the evidence names, and M8 and M9 are caught. I bless it.
- [MEANING] TC-240 method, expected, verifies, evidence -> the row-level refresh refusal over every compared tier, for SR-207 -> the same, plus SR-228: a named verdict recorded in the act ledger in repository-relative form, and three verdict refusals -> not the same: a new verified behaviour and parent. It is Fix 7 byte for byte, and M10, M11, M12 and M13 are caught. I bless it.
- [MEANING] TC-278 expected, method, evidence -> scope refusal and mixed acts, for SR-178 -> the same, plus the held-rung arm for SR-228: read at trunk's tip; refused without a verdict, below approval, with a MEANING verdict, a verdict not ruling the row, an unreadable verdict or a conflicting tag; CLARITY merges -> not the same: a new arm. It is Fix 6 byte for byte, and M1, M2, M3, M5, M6b and M13b are caught. I bless it.

VERDICT: MEANING rows=12

## Aftermath: nothing re-anchored this round

Two of the twelve rows are returned, so under the owner's in-lane direction no act is taken.
The ten settled rows are LLR-153, LLR-158, LLR-245, LLR-271, LLR-278, SR-178, TC-147, TC-153,
TC-240 and TC-278. They wait for the lane's single act after the re-judge.

The act could not anchor them yet in any case. The low-level-requirements copy is refused while
LLR-118 and LLR-167 carry drifted approved text that the act does not name.

Fixes 8 and 9 amend TC-123 and TC-161, whose approved text has not moved until now. Those two
rows therefore join the round-3 amendment scope.

## Required fixes (to be applied in this lane, then re-judged)

Each replacement is the WHOLE cell value, byte-exact, between the fences (one line, no trailing
newline). Every other cell of every row stays byte-exact. LLR-118 and LLR-167 themselves need no
change.

### Fix 8: TC-123 `method`, `evidence`, and one test (for LLR-118)

`method`, with one sentence appended:

```
Drive gen_open_items over temp repos: assert a pending registry row renders as a brief and a RULED row does not; that Drafted AND Modified spine rows both surface (approval owed vs re-attest owed) while an Approved row does not; that a section with no changed cells says what is true — no cell differs from the approved snapshot, the row's own Status asking for a human — and never CHECK THE BASELINE nor nothing-changed; that --check bites on drift as a plain regenerate-and-compare, with no baseline stamp left in the view to re-read (the machine-local mask retired with the dispatcher); that the whole thing is vacuous with neither registry nor view; that registry prose is HTML-escaped; that the word diff marks only what moved and the percentage counts words not whitespace; and that the theme tokens equal the dashboard's emitted values (a drift guard, not an extraction). It also drives verdict_reattest_block: every act-ledger entry naming a verdict is listed newest first with its re-attested rows and its verdict file, an entry naming none is left out, a ledger with no such entry reads None recorded, and the rendered page carries the list.
```

`evidence`:

```
tests/test_gen_open_items.py; tests/test_gen_open_items_render.py::test_a_verdict_reattestation_stays_listed_on_the_owner_surface; tests/test_gen_open_items_render.py::test_the_verdict_audit_list_is_newest_first
```

Add this test to `tests/test_gen_open_items_render.py`, after
`test_a_verdict_reattestation_stays_listed_on_the_owner_surface`. It uses only that module's
`load_script`, is `ruff format` clean, passes at db891d7f and kills P1:

```python
def test_the_verdict_audit_list_is_newest_first():
    """LLR-118: the owner's audit list shows the newest verdict-naming act
    first."""
    gi = load_script("gen_open_items")
    acts = [
        {
            "seq": 2,
            "date": "2026-10-03",
            "approved": [],
            "reattested": ["SN-003"],
            "verdict": "docs/reviews/a.md",
        },
        {
            "seq": 5,
            "date": "2026-10-04",
            "approved": [],
            "reattested": ["SN-009"],
            "verdict": "docs/reviews/b.md",
        },
    ]
    block = gi.verdict_reattest_block(acts)
    assert block.index("act 5") < block.index("act 2"), block
```

### Fix 9: TC-161 `method`, `evidence`, a constant and two tests (for LLR-167)

`method`: its last sentence, "What a MEANING verdict owes next is derived from the declared
approval dial.", is replaced by two sentences. The scope bound and the arm mapping are what the
tests below pin.

```
Drive the real loop against a fake agent CLI over throwaway git repos for the disposition, red-TC and amendment briefs, and capture what the session was actually handed: the brief its row declares rather than the worker assignment. Assert the session writes the typed verdict line the brief demands to the path the brief named and commits it under the row's result trailer, ending the run done; that a session committing the trailer with no verdict, or with a label outside the brief's closed enum, does not complete; that a row whose declared brief cannot be filled is held for a human, with no session run, the reason printed and nothing committed under the row; and that a row declaring no brief builds from the worker assignment. Compose each routed brief in process and assert each slot carries its real derivation: for the disposition brief, the lane's report verbatim, the closed spec and the commit facts; for the red-TC brief, the live census joined to each TC row's Method, Expected and Evidence and to the obligation its targets name; for the consolidation brief, the whole cluster, the other open rows, the cited SR and LLR text (a stated literal when the cluster cites none), the overlap findings, the recorded and current digest pairs and what earlier consolidations absorbed; for the first-approval brief, the whole chain of each SR holding a scoped row, the scoped `Drafted` rows marked as the question, a held or out-of-scope row labelled as not this session's and contributing no registry, an unrelated chain left out, the derived `--approves` argument rendered as one shell command with the rows each token covers named once, and closing instructions that forbid stopping before the approval commit when any row is approved. Assert no `{slot}` survives in the composed disposition, red-TC, amendment and first-approval text. Then drive the refusals, each returning its reason and never a partial brief: a clean close with no per-close report, a report with no typed `commit_range`, a census that has come clean, a TC row missing a listed cell, a target with no normative text; a first-approval, amendment or consolidation row declaring no `Adjudicates` scope, a first approval whose scoped rows are all settled, gone from the spine or held for the owner, and an amendment none of whose scoped rows still differs from its approved copy; a consolidation with no `Digests` cell, a cluster row no longer queued, and a cluster whose overlap has dissolved. Pin the discriminator: two rows with an identical SpecRef and different declared `Brief` cells compose differently. Pin the routing both ways: the routed set equals the shipped set and each routed brief names a shipped template, every brief a mint declares is shipped and every routed brief is declared by a mint, a row declaring `conflict`, which the kit no longer ships, refuses as an unknown brief, and an absent or unknown brief refuses. Pin each brief's typed verdict grammar: a well-formed line is accepted, and an absent file, a missing machine line, an out-of-enum label or a missing counter is refused with its reason. Pin the amendment arm's scope: the amendment mint writes the rows it routes as the row's `Adjudicates` scope, and a one-row mint's brief renders that row alone while another row's unadjudicated drift stays out of it, and a row hanging under two SRs is rendered once. The amendment arm covers two seams: IF-124, the `last_approved` baseline read - the brief carries the snapshot as its anchor, naming for each registry shown the commit that last wrote that registry's copy rather than the newest write anywhere in the snapshot, only approved cells reach the judge, and with no snapshot the brief holds and says FIRST APPROVAL rather than fabricating an anchor; and IF-075, the re-attestation model its before/after listing is read from. The amendment arm also renders a need, assumption or surrogate row in its scope with its drifted approved cells before and after, and leaves out a drifted row of those tiers that the scope does not name. What each verdict owes next is derived from the declared approval dial: on a released rung the re-attestation is the session's and names no verdict, and on a held rung a CLARITY verdict is re-attested naming its verdict while a MEANING verdict stops for the owner, never the other way round.
```

`evidence`:

```
tests/test_adjudicate_brief.py::test_a_need_scoped_amendment_row_composes_with_its_before_and_after; tests/test_adjudicate_brief.py::test_a_held_rung_CLARITY_verdict_is_the_sessions_reattestation; tests/test_adjudicate_brief.py::test_assumption_and_surrogate_scoped_amendment_rows_compose_within_their_scope; tests/test_adjudicate_brief.py::test_the_held_aftermath_gives_each_verdict_its_own_arm; tests/test_adjudicate_brief.py
```

Add these to `tests/test_adjudicate_brief.py`, after
`test_a_held_rung_CLARITY_verdict_is_the_sessions_reattestation`. They use only that module's
own names (`re`, `ab`, `baseline_snapshot`, `set_process_key`, `_spine_repo`, `_am_row`,
`_need_amendment_repo`), are `ruff format` clean, pass at db891d7f and kill P4, P5 and P6:

```python
_ASSUMPTION_TOML = (
    "[assumption.DA-001]\n"
    'effect_at = ["B-001"]\n'
    'assumption = "{}"\n'
    'holds_when = "always"\n'
    'obstacle = "never"\n'
    'status = "Approved"\n'
    "\n[surrogate.SUR-001]\n"
    'name = "the stand-in"\n'
    'emulates = ["EXT-001"]\n'
    'description = "{}"\n'
    'status = "Approved"\n'
)


def test_assumption_and_surrogate_scoped_amendment_rows_compose_within_their_scope(
    tmp_path,
):
    """LLR-167: an assumption- or surrogate-scoped amendment row composes with
    the drifted row's approved cells before and after, and only the rows its
    Adjudicates scope names are rendered."""
    repo = _spine_repo(tmp_path)
    path = repo / "docs" / "requirements" / "assumptions.toml"
    path.write_text(
        _ASSUMPTION_TOML.format("it holds", "old stand-in"), encoding="utf-8"
    )
    baseline_snapshot.copy_live(repo, seed=True)
    path.write_text(
        _ASSUMPTION_TOML.format("it holds, mostly", "new stand-in"), encoding="utf-8"
    )
    values, why = ab.amendment_values(repo, _am_row(Adjudicates="DA-001;SUR-001"))
    assert why is None, why
    shown = re.findall(r"^- (\S+) (\S+)", values["rows"], re.M)
    assert shown == [("DA", "DA-001"), ("SUR", "SUR-001")], values["rows"]
    assert "it holds, mostly" in values["rows"] and "old stand-in" in values["rows"]
    values, why = ab.amendment_values(repo, _am_row(Adjudicates="DA-001"))
    assert why is None, why
    shown = re.findall(r"^- (\S+) (\S+)", values["rows"], re.M)
    assert shown == [("DA", "DA-001")], values["rows"]


def test_the_held_aftermath_gives_each_verdict_its_own_arm(tmp_path):
    """LLR-167: on a held rung the aftermath tells a CLARITY verdict to
    re-attest naming its verdict, and a MEANING verdict to stop for the
    owner, never the other way round."""
    repo = _need_amendment_repo(tmp_path)
    set_process_key(repo, "attestation", "human_approval_through", "DevStg-Needs")
    values, why = ab.amendment_values(repo, _am_row(Adjudicates="SN-001"))
    assert why is None, why
    clarity, meaning = values["aftermath"].split("A MEANING verdict on them", 1)
    assert "--verdict" in clarity, clarity
    assert "the signature is the owner's" not in clarity, clarity
    assert "the signature is the owner's" in meaning, meaning
    assert "--verdict" not in meaning, meaning
```

## Observations carried from round 1 (no fix required by this verdict)

- **The unknown-tier fail-safe is unpinned (M4).** No row states it.
- **TC-147's expected cell names SR-174 only**, although its `verifies` cell includes SR-228.
- **The S11 in-lane route never reaches this lane's merge-slot rule.** `held_reattest_refusal`
  runs only for a lane whose every claimed spec declares `safety_class = "adjudication"`, so
  an in-lane act on a held rung never meets it. That belongs to the S11 plan; it is moot here,
  because the dial releases SR, LLR and TC.
