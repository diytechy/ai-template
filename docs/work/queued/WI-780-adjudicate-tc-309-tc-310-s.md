+++
id = "WI-780"
title = "adjudicate: TC-309, TC-310 - spine row(s) authored Drafted on merged trunk ae702b7..758519d await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = "docs/test/test-cases.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["TC-309", "TC-310"]
+++

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- TC-309 amended in `docs/test/test-cases.toml` (Evidence, Expected, Method)
- TC-310 amended in `docs/test/test-cases.toml` (Expected, Method)

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.

## Dispositions

Verdict: `docs/reviews/wi-780-adjudicate-tc-309-tc-310-s/001-ADJUDICATE-022a33d.md`
(TC-309 and TC-310 returned; none approved). One lane carries both returned
rows: both are Drafted rows in the test-case registry, and one first-approval
sitting can judge them together.

```toml
title = "Assert the re-judge brief's chain order and the release checklist's registry bytes"
workstream = "process"
buildtier = "quick"
safety_class = "spine"
sr_refs = ["SR-146", "SR-215", "SR-033"]
priority = 2
```

TC-309: LLR-295 (Approved) says the re-judge brief "shows the observation
instruction beneath its assumption chain", and TC-309's Expected says the
brief composes "under" the chain. Neither its Method nor its test asserts the
order: with the case text moved above the chain,
`test_rejudge_shows_assumption_only_case` still passes. The code is correct
(`chain + [text]`). Fix the row's text and add one order assertion.

TC-310: its Method says "assert the source registry remains byte-identical",
but `generate` compares `read_text()` (newline-translated text) to the string
it wrote. On Windows, rewriting the registry from CRLF to LF still passes. The
automated-case exclusion is proved only through the exact substring
`(method: TC-279)`. The row's text is right; fix the test only.

Each cell below is replaced whole with the text given. Write it byte-exact
apart from TOML escaping.

**TC-309 (rework, Drafted).** Two cells:
- `method` -> `Compose the re-judge template for a due assumption-only case with no Verifies; assert its assumption id, statement, falsifier and standing appear above the observation case and its Method. The same case citing an assumption the registry does not declare refuses composition naming that assumption, and the same case with no Method, no Expected or no MaxAge refuses naming that cell; none returns a brief.`
- `expected` -> `The complete re-judge brief shows the observation case beneath its assumption chain, and an undeclared assumption or a missing Method, Expected or MaxAge refuses with its reason.`

**TC-309's test.** In `tests/test_assumption_observation_briefs.py`,
`test_rejudge_shows_assumption_only_case`: directly after the existing line
`assert "- TC-279 — observes DA-011" in text`, add:

    case_at = text.index("- TC-279 — observes DA-011")
    for shown in (
        "DA-011",
        "A new reader understands the code.",
        "A reader cannot explain the code.",
        "Standing**: active",
    ):
        assert text.index(shown) < case_at

**TC-310's test (the row's cells do not change).** In
`tests/test_release_assumptions.py`:
- In `generate`, replace the three lines

      monkeypatch.setattr(sys, "argv", ["gen_release_checklist", "--docs", str(docs)])
      monkeypatch.setattr(release, "_rejudge_checklist_line", lambda root: "rejudge")
      release.main()

  and the `if rows is not None:` block after them (the `read_text(...) == rows`
  assertion) with:

      registry = docs / "requirements/assumptions.toml"
      before = registry.read_bytes() if rows is not None else None
      monkeypatch.setattr(sys, "argv", ["gen_release_checklist", "--docs", str(docs)])
      monkeypatch.setattr(release, "_rejudge_checklist_line", lambda root: "rejudge")
      release.main()
      if rows is not None:
          assert registry.read_bytes() == before

- In `test_assumptions_section_and_marker`, directly before its last line
  (the assertion on "a person sets"), add the line

      assert "TC-280" not in text

**Prohibitions.**
- The only registry edits are TC-309's `method` and `expected`. Every other
  cell of every row stays byte-identical, including TC-309's `evidence`, every
  cell of TC-310, LLR-295, LLR-296, TC-308 and SR-215.
- Do not flip any Status. TC-309 and TC-310 stay `Drafted`; their approval is
  the adjudication their merge mints.
- No production code changes. `project-trajectory/scripts/adjudicate_brief.py`
  and `project-trajectory/scripts/gen_release_checklist.py` stay byte-identical.
- Change nothing else in either test module. Rename no test: TC-309's and
  TC-310's `evidence` cells name the existing node ids.
- Do not touch the evidence-ladder rendering; that is WI-771's.
- No RESYNC entry: nothing shipped to an adopter changes.

**Bar.** The commit bar, plus `pytest -q -p no:cacheprovider
tests/test_assumption_observation_briefs.py tests/test_release_assumptions.py`
(8 passed in the adjudicator's reverted trial at 022a33d5). Also
`trace.py --strict`: only LLR-292's pre-existing `minimal` finding may remain.
In the same trial, `check_trajectory.py --strict` exited 0. With TC-309 and
TC-310 flipped as a test, the only new findings were the approval-record ones
that an act's snapshot clears. Paste the real output.
