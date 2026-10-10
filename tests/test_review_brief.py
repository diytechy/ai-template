"""The coordinator's review and critique briefs, rendered from the kit's templates.

WI-852 (the WI-841 retrospective, proposal §4(a), §6, §7.4). The coordinator
hand-wrote each reviewer's brief, so its rounds never carried the kit brief's
failure-class and unrepresentable clauses, and its review files used their own
format, so the generated verdict rollup saw no coordinator lane. Three things
are pinned here, each over a `tmp_path` tree and in-process:

  * a rendered review brief is the kit's reviewer template, strictly filled:
    it carries the failure-class and unrepresentable clauses and the lane's
    facts, and an unfilled slot refuses;
  * the scope critique renders the kit's critique template over the spec, with
    the scope rubric (ruling 2's two questions) as its rubric input;
  * a review filed by the coordinator is a kit round file the rollup reads,
    and a malformed review is refused rather than filed.

The command line's git reads and its success exit codes are driven on a real
git repository in test_review_brief_git.py, which is slow-tier (it spawns git).
"""

import pytest
from conftest import ROOT, load_script

rb = load_script("review_brief")
rollup = load_script("gen_verdict_rollup")
agent_brief = load_script("agent_brief")

BASE = "1" * 40
SHA = "abcdef0" + "2" * 33
SPEC = """+++
id = "WI-900"
title = "A lane under review"
+++

## Done-when

- It works.
"""


def _lane(tmp_path):
    spec = tmp_path / "docs" / "work" / "active" / "wi-900" / "WI-900-a-lane.md"
    spec.parent.mkdir(parents=True)
    spec.write_text(SPEC, encoding="utf-8")
    return tmp_path


def _round(scope="full", findings=None, rubric=None):
    return rb.Round(
        wi="WI-900",
        lane="wi-900",
        base=BASE,
        sha=SHA,
        scope=scope,
        tests=("tests/test_a.py", "tests/test_b.py"),
        scratch="C:/scratch/review-tmp",
        python="C:/venv/python.exe",
        findings=findings,
        rubric=rubric,
    )


# --- the review brief -----------------------------------------------------------


def test_a_rendered_review_brief_carries_the_kit_clauses_and_the_lane_facts(tmp_path):
    text, verdict = rb.render_review(_lane(tmp_path), _round())
    # The kit reviewer template's two clauses the hand brief lacked.
    assert "worst failure classes THIS change admits" in text
    assert "cannot be made UNREPRESENTABLE instead" in text
    assert '§6 "Review threat model"' in text
    # The lane's facts, as fill values.
    # One source for every range the brief states: the reviewed commit.
    assert "git diff {}...{} --".format(BASE, SHA) in text
    assert "...HEAD" not in text
    assert "`git rev-parse HEAD` prints `{}`".format(SHA) in text
    assert "  - WI-900 — A lane under review" in text
    assert "docs/work/active/wi-900/WI-900-a-lane.md" in text
    assert "`{}..{}`".format(BASE, SHA) in text
    assert "FULL-LANE" in text
    # Every path in a command is quoted for PowerShell, the shell the brief
    # names, so a path with a space or a quote stays one argument.
    assert "In PowerShell" in text
    assert "& 'C:/venv/python.exe' -m pytest" in text
    assert "--basetemp 'C:/scratch/review-tmp/wi-900'" in text
    assert "'tests/test_a.py' 'tests/test_b.py'" in text
    spaced = rb.dataclasses.replace(
        _round(), scratch="C:/my scratch/it's", python="C:/Program Files/py.exe"
    )
    text_spaced, _v = rb.render_review(_lane(tmp_path / "spaced"), spaced)
    assert "& 'C:/Program Files/py.exe' -m pytest" in text_spaced
    assert "--basetemp 'C:/my scratch/it''s/wi-900'" in text_spaced
    assert "$env:GIT_CEILING_DIRECTORIES = 'C:/my scratch'" in text_spaced
    assert "do not run the full suite or the smoke tier" in text
    assert "`docs/stack.ini` `[generated]`" in text
    assert "Reviewed: {}".format(SHA) in text
    # The verdict lands outside the repository, for the launcher to file.
    assert verdict == "C:/scratch/review-tmp/wi-900-abcdef0-full-review.md"
    assert "Write your verdict to {} ".format(verdict) in text
    assert "the launcher records the verdict" in text
    # No slot is left in the sent brief.
    assert rb.prompts.slots(text) == set()


def test_a_narrow_round_names_the_findings_it_answers(tmp_path):
    root = _lane(tmp_path)
    prior = root / "docs" / "reviews" / "wi-900" / "001-REVIEW-A-1111111.md"
    prior.parent.mkdir(parents=True)
    prior.write_text("VERDICT: CHANGES-REQUESTED findings=1\n", encoding="utf-8")
    rel = "docs/reviews/wi-900/001-REVIEW-A-1111111.md"
    text, verdict = rb.render_review(root, _round("narrow", findings=rel))
    assert "NARROW round" in text and "FULL-LANE" not in text
    assert rel in text
    assert "a claim under judgement, never the premise" in text
    assert verdict.endswith("-narrow-review.md")


def test_a_narrow_round_without_findings_and_a_full_one_with_them_are_refused():
    with pytest.raises(rb.BriefError, match="narrow"):
        _round("narrow")
    with pytest.raises(rb.BriefError, match="full"):
        _round("full", findings="docs/reviews/x/001-REVIEW-A-1111111.md")
    with pytest.raises(rb.BriefError, match="scope"):
        _round("partial")


def test_a_named_input_that_is_not_there_refuses(tmp_path):
    root = _lane(tmp_path)
    with pytest.raises(rb.BriefError, match="rubric"):
        rb.render_review(root, _round(rubric="docs/rubrics/nope.md"))
    with pytest.raises(rb.BriefError, match="WI-901"):
        rb.render_review(root, rb.dataclasses.replace(_round(), wi="WI-901"))


def test_an_unfilled_slot_refuses_and_no_brief_is_written(
    tmp_path, monkeypatch, capsys
):
    # A template edit that adds a slot the render does not fill must stop the
    # brief, never send it with a hole.
    real = rb.prompts.load

    def with_extra_slot(key, override=None):
        return real(key, override) + "\n{lane_budget}"

    monkeypatch.setattr(rb.prompts, "load", with_extra_slot)
    with pytest.raises(rb.prompts.PromptError, match="unfilled slot.*lane_budget"):
        rb.render_review(_lane(tmp_path), _round())
    # The same refusal through the command line, past the git reads.
    monkeypatch.setattr(
        rb, "lane_commits", lambda root, base, sha: ("wi-900", BASE, SHA)
    )
    out = tmp_path / "brief.md"
    argv = ["review", "--root", str(tmp_path), "--wi", "WI-900", "--base", BASE]
    argv += ["--sha", SHA, "--scope", "full", "--scratch", "C:/scratch"]
    argv += ["--tests", "tests/test_a.py", "--out", str(out)]
    assert rb.main(argv) == 2
    assert "lane_budget" in capsys.readouterr().err
    assert not out.exists()


def test_the_loop_brief_renders_the_new_slot_empty(tmp_path):
    # The loop fills `{round_facts}` with nothing: its own brief is unchanged
    # apart from the recording clause, and never carries a literal slot.
    text = agent_brief.reviewer_prompt({}, "REVIEW-A", "v.md", root=tmp_path)
    assert "{round_facts}" not in text
    assert text.endswith("Do not edit the code you are reviewing.")


def _loop_narrow(root, templates=None):
    return agent_brief.narrow_reviewer_prompt(
        templates or {},
        "REVIEW-A",
        "docs/reviews/wi-900/v.md",
        root=root,
        worker={"assigned": ["WI-900"], "rows": {}, "base": BASE, "train": "wi-900"},
        base=BASE,
        sha=SHA,
        findings="docs/reviews/wi-900/001-REVIEW-A-1111111.md",
    )


def test_the_loop_narrow_round_renders_its_delta_through_the_one_render(tmp_path):
    # WI-847: a loop round that answers an earlier round reads only the round's
    # delta, rendered from the shipped reviewer template through `prompts.fill`
    # with the same narrow range sentence the attended render states.
    root = _lane(tmp_path)
    text = _loop_narrow(root)
    assert "git diff {}...{} --".format(BASE, SHA) in text
    assert "...HEAD" not in text
    rel = "docs/reviews/wi-900/001-REVIEW-A-1111111.md"
    (root / rel).parent.mkdir(parents=True)
    (root / rel).write_text("VERDICT: CHANGES-REQUESTED findings=1\n", "utf-8")
    attended = rb.render_review(root, _round("narrow", findings=rel))[0]
    sentence = agent_brief.narrow_scope_line(BASE, SHA, rel)
    assert sentence in text and sentence in attended
    assert "NARROW round" in text and "FULL-LANE" not in text
    # The loop's reviewer commits its own verdict: no attended recording facts.
    assert "- The launcher records the verdict." not in text
    assert "Write your verdict to docs/reviews/wi-900/v.md" in text
    assert "  - WI-900" in text
    assert rb.prompts.slots(text) == set()


def test_a_loop_narrow_round_refuses_an_override_that_cannot_carry_its_range(
    tmp_path,
):
    # An override without the range slots would send a narrow round the wrong
    # reading scope; the strict fill refuses it instead.
    with pytest.raises(rb.prompts.PromptError, match="unfilled|unknown"):
        _loop_narrow(_lane(tmp_path), {"REVIEW-A": "Review. Write to {verdict}."})


# --- the scope critique ----------------------------------------------------------


def test_the_scope_critique_carries_ruling_twos_questions_and_its_rubric(tmp_path):
    root = _lane(tmp_path)
    rubric = root / "docs" / "rubrics" / "scope-critique.md"
    rubric.parent.mkdir(parents=True)
    rubric.write_bytes((ROOT / "docs" / "rubrics" / "scope-critique.md").read_bytes())
    text = rb.render_critique(
        root, "WI-900", "docs/rubrics/scope-critique.md", "C:/scratch/c.md"
    )
    assert "INDEPENDENT critic" in text
    assert "Write your verdict to C:/scratch/c.md" in text
    assert "### Rubric: docs/rubrics/scope-critique.md" in text
    assert "independently landable deliverable" in text
    assert "authority over a hold, an act or a gate" in text
    assert "docs/work/active/wi-900/WI-900-a-lane.md" in text
    assert rb.prompts.slots(text) == set()


# --- filing a review as a kit round file -----------------------------------------

REVIEW = """Reviewed: {sha}

Verified: drove the change.

- [MAJOR] project-trajectory/scripts/x.py:3 -> wrong -> fix it -> @owner
- [MINOR] tests/test_x.py:9 -> vague -> name it -> @owner

VERDICT: CHANGES-REQUESTED findings=2
"""


def test_a_filed_coordinator_review_appears_in_the_rollup(tmp_path):
    full = rb.file_review(tmp_path, "wi-900", REVIEW.format(sha=SHA), SHA, "full")
    assert full.as_posix().endswith("docs/reviews/wi-900/001-REVIEW-A-abcdef0.md")
    approve = "Reviewed: {}\n\nVERDICT: APPROVE findings=0\n".format(SHA)
    narrow = rb.file_review(tmp_path, "wi-900", approve, SHA, "narrow")
    assert narrow.name == "002-REVIEW-A-abcdef0-narrow.md"
    # Refused before the rollup is rendered, and nothing is filed: a review
    # whose one VERDICT line repeats a field (the shared per-line reader's own
    # refusal, WI-870) or is not exactly the canonical form, or which names
    # the keyword on a second line in any case; and a lane the round reader
    # cannot read as a review scope (a `/` would nest a directory deeper).
    bad_lines = (
        ("VERDICT: APPROVE findings=7 findings=0", "more than once"),
        ("VERDICT: APPROVE findings=0 CHANGES-REQUESTED", "is not exactly"),
        ("VERDICT: APPROVE findings=0 findings = 7", "is not exactly"),
        ("VERDICT: APPROVE findings=0\nverdict: CHANGES-REQUESTED findings=0", "2 VER"),
        ("Verdict: APPROVE findings=0", "is not exactly"),
    )
    for line, why in bad_lines:
        bad = "Reviewed: {}\n\n{}\n".format(SHA, line)
        with pytest.raises(rb.BriefError, match=why):
            rb.file_review(tmp_path, "wi-900", bad, SHA, "full")
    with pytest.raises(rb.BriefError, match="feature/wi-900"):
        rb.file_review(tmp_path, "feature/wi-900", approve, SHA, "full")
    # Nor is the rollup generator's own directory a lane, in any case: on a
    # case-insensitive filesystem `Rollup` is the directory it prunes.
    for lane in ("rollup", "Rollup", "ROLLUP"):
        with pytest.raises(rb.BriefError, match="rollup generator"):
            rb.file_review(tmp_path, lane, approve, SHA, "full")
    assert sorted(p.name for p in (tmp_path / "docs" / "reviews").iterdir()) == [
        "wi-900"
    ]
    assert len(list((tmp_path / "docs" / "reviews" / "wi-900").iterdir())) == 2
    [(path, text)] = rollup.targets(tmp_path)
    assert path.name == "wi-900.md"
    assert "| 1 | REVIEW-A | `abcdef0` | CHANGES-REQUESTED | 2 |" in text
    assert "| 2 | REVIEW-A | `abcdef0` | APPROVE | 0 |" in text


@pytest.mark.parametrize(
    "text, why",
    [
        (REVIEW.format(sha=BASE), "Reviewed"),
        (REVIEW.format(sha=SHA).replace("findings=2", "findings=3"), "findings=3"),
        (REVIEW.format(sha=SHA).replace("findings=2", ""), "omits findings"),
        (REVIEW.format(sha=SHA) + "VERDICT: APPROVE findings=0\n", "exactly one"),
        ("Reviewed: {}\n\nlooks fine\n".format(SHA), "no VERDICT line"),
        # Every VERDICT-labelled line is read whole, not by a prefix match: a
        # count that is not a whole number, a label outside the enum on a
        # second line, and a label that only starts like one all refuse.
        (REVIEW.format(sha=SHA).replace("findings=2", "findings=2.5"), "2.5"),
        (REVIEW.format(sha=SHA) + "VERDICT: NEEDS-HUMAN findings=0\n", "2 VERDICT"),
        (REVIEW.format(sha=SHA).replace("REQUESTED f", "REQUESTEDX f"), "REQUESTEDX"),
        (
            "Reviewed: {}\n\nVERDICT: CHANGES-REQUESTED findings=0\n".format(SHA),
            "no finding",
        ),
    ],
)
def test_a_malformed_review_is_refused_and_nothing_is_filed(tmp_path, text, why):
    with pytest.raises(rb.BriefError, match=why):
        rb.file_review(tmp_path, "wi-900", text, SHA, "full")
    assert not (tmp_path / "docs" / "reviews").exists()


# --- the input refusals the render owns -------------------------------------------


def test_a_round_with_no_tests_refuses():
    with pytest.raises(rb.BriefError, match="tests"):
        rb.dataclasses.replace(_round(), tests=())


def test_an_empty_or_missing_named_input_refuses(tmp_path):
    root = _lane(tmp_path)
    empty = root / "docs" / "empty.md"
    empty.write_text("  \n", encoding="utf-8")
    with pytest.raises(rb.BriefError, match="rubric docs/empty.md is empty"):
        rb.render_review(root, _round(rubric="docs/empty.md"))
    with pytest.raises(rb.BriefError, match="findings file docs/empty.md is empty"):
        rb.render_review(root, _round("narrow", findings="docs/empty.md"))
    with pytest.raises(
        rb.BriefError, match="findings file docs/nope.md cannot be read"
    ):
        rb.render_review(root, _round("narrow", findings="docs/nope.md"))
    with pytest.raises(rb.BriefError, match="rubric docs/empty.md is empty"):
        rb.render_critique(root, "WI-900", "docs/empty.md", "C:/scratch/c.md")


def test_the_critique_render_refuses_a_missing_spec(tmp_path):
    root = _lane(tmp_path)
    rubric = root / "docs" / "rubric.md"
    rubric.write_text("# Rubric\n\nS1 - one.\n", encoding="utf-8")
    with pytest.raises(rb.BriefError, match="no spec for WI-901"):
        rb.render_critique(root, "WI-901", "docs/rubric.md", "C:/scratch/c.md")
