+++
id = "WI-781"
title = "Assert the re-judge brief's chain order and the release checklist's registry bytes"
workstream = "process"
sr_refs = ["SR-146", "SR-215", "SR-033"]
specref = "docs/archive/work/complete/WI-780-adjudicate-tc-309-tc-310-s.md"
buildtier = "quick"
priority = 2
safety_class = "spine"
+++

## Context

Drafted by WI-780 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

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

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-033 [project-trajectory/scripts/gen_release_checklist.py :: main] tests: (see TC-033) — Release checklist generator
- LLR-162 [project-trajectory/scripts/prompts.py :: load/fill/strict_check/digest/catalog_rows/preflight] tests: TC-157 — Prompts as loaded files, catalogued and fingerprinted
- LLR-163 [project-trajectory/scripts/agent_session.py :: split_cmd/build_argv] tests: TC-157 — Argv arrays, and the adjudicator as a routed phase
- LLR-164 [project-trajectory/scripts/gen_prompt_catalog.py :: render/main] tests: TC-192 — The generated prompt catalogue and its freshness gate
- LLR-167 [project-trajectory/scripts/adjudicate_brief.py :: compose/disposition_values/red_tc_values/consolidate_values/amendment_values/first_approval_values] tests: TC-161 — The adjudicator briefs' evidence, and the refusal that keep…
- LLR-254 [project-trajectory/scripts/rejudge.py :: observation_test_cases/checkpoint_for/checkpoint_drafts/_open_rejudge/due_cases/BRIEF/CHECKPOINTS] tests: - — The checkpoint re-judge decision

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency
- CMP-009 W4 Human & adopter surfaces: downstream-resync

### Interface seams via the touched modules
- IF-018 scripts/gen_release_checklist -> external:downstream adopter: file docs/release-checklist.md — human-verified rows use `- [ ] <ID> — <what to confirm> (refs)`; assumption confi…
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-034 docs/requirements/ -> scripts/gen_release_checklist;external:downstream adopter: file None
- IF-041 external:agent CLI <- scripts/agent_session: cli headless invocation; the prompt on stdin
- IF-050 scripts/derive_stage -> scripts/check;scripts/agent_common;scripts/check_trajectory;scripts/traj_parse;scripts/intake: file docs/stage — key = value fields plus a sha256 fingerprint of the declared inputs
- IF-053 scripts/schedule <- scripts/census;scripts/dispatch;scripts/intake: call load_wis · _load, frontier, kind_of · SAFETY_CLASSES — the symbols census, dispatch and intake take; no write…
