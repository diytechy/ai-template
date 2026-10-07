"""WI-841: a lane's Done-when change is blessed IN THE LANE.

A lane may edit its own Done-when (the commit is never refused), and an
adjudicator, not a guard, blesses the change before what consumes the
Done-when uses it. The one predicate (`kitlib.done_when.blessing_owed`) is
asked at the lane's next build dispatch (`agent_loop.build_hold`, through
`worker_endstate`), at a hand close (`integrate.py done-when-hold`, the
pre-commit hook's `done-when-blessed` step) and at the merge slot
(`integrate._done_when_refusal`); a verdict line or an owner ruling that binds
the exact text's digest releases all three, and a text changed after it holds
them again. At merge, intake mints the goalposts row only for an uncovered
close. One combined sitting composes every pending in-lane judgement.

Each fixture is a real git repository: trunk `main` holds the claim under
`docs/work/active/wi-007/`, and the lane is a linked worktree on `wi-007`, the
shape every hold point reads.
"""

import os
import subprocess
import sys

import pytest
from conftest import env_gate_skipif, load_script, pin_autocrlf, skip_without_env_gates

pytestmark = env_gate_skipif("git")

ab = load_script("adjudicate_brief")
agent_loop = load_script("agent_loop")
integrate = load_script("integrate")
intake = load_script("intake")
trace = load_script("trace")

from kitlib import done_when as kdone  # noqa: E402  (scripts/ is on the path)

WI = "WI-007"
BRANCH = "wi-007"
SPEC = "WI-007-thing.md"
DONE_WHEN = (
    "\n## Done-when\n\n"
    "- The widget renders at 60 fps on the reference box.\n"
    "- A test pins the empty-frame refusal.\n"
)
NARROWED = DONE_WHEN.replace("60 fps", "30 fps")


def _git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.strip()


def _spec(body):
    return (
        '+++\nid = "{}"\ntitle = "Widget"\nworkstream = "ws"\n'
        'sr_refs = ["SR-001"]\nsafety_class = "ordinary"\n+++\n\n'
        "## Context\n\nA widget.\n{}".format(WI, body)
    )


def _write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def _commit(root, message):
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", message)
    return _git(root, "rev-parse", "HEAD")


def _trunk(tmp_path):
    """`main` with the claim of WI-007 under `active/wi-007/` committed."""
    skip_without_env_gates("git")
    root = tmp_path / "trunk"
    root.mkdir(parents=True)
    _git(root, "init", "-q")
    pin_autocrlf(root)
    for key, value in (
        ("user.email", "t@example.com"),
        ("user.name", "T"),
        ("commit.gpgsign", "false"),
    ):
        _git(root, "config", key, value)
    _git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    _write(root, "seed.txt", "seed\n")
    _write(root, "docs/stack.ini", "[generated]\nPROJECT_STATE.html = trajectory\n")
    _write(
        root,
        trace.WATERMARK,
        trace.render_watermark({s: 0 for s in trace.WATERMARK_SPACES}),
    )
    _commit(root, "seed")
    _write(root, "docs/work/active/{}/{}".format(BRANCH, SPEC), _spec(DONE_WHEN))
    _commit(root, "claim: {} -> active/{} (bookkeeping)".format(WI, BRANCH))
    return root


def _lane(tmp_path, body=NARROWED):
    """`(trunk, lane)`: the lane worktree with its Done-when edited to `body`
    and committed (the edit commit itself is never refused)."""
    trunk = _trunk(tmp_path)
    lane = tmp_path / "lane"
    _git(trunk, "worktree", "add", "-q", "-b", BRANCH, str(lane))
    if body is not None:
        _write(lane, "docs/work/active/{}/{}".format(BRANCH, SPEC), _spec(body))
        _commit(lane, "edit the Done-when")
    return trunk, lane


def _digest(body=NARROWED):
    return kdone.digest(WI, _spec(DONE_WHEN), _spec(body))


_VERDICT_REL = "docs/reviews/{}/001-ADJUDICATE-x.md".format(BRANCH)


def _bless(lane, line, bound=True):
    """Commit `line` as the lane's verdict. Unless a binding was written first
    (`_bind`), the verdict is bound as the route that ran the call records an
    accepted single-kind done-when verdict (round 11); `bound=False` leaves
    it unbound."""
    _write(lane, _VERDICT_REL, line + "\n")
    binding = lane / ab.ksitting.requested_path(_VERDICT_REL)
    if bound and not binding.exists():
        text = ab.ksitting.render_requested("done-when", ("done-when",), "accepted")
        _write(lane, ab.ksitting.requested_path(_VERDICT_REL), text)
    _commit(lane, "verdict")


def _worker(lane):
    return {
        "train": BRANCH,
        "assigned": [WI],
        "base": agent_loop.default_base(lane),
        "rows": {WI: {"WI-ID": WI, "SafetyClass": "ordinary"}},
        "rework": "",
        "adjudication_owed": "",
    }


_BUILD_PLAN = {"is_review": False, "is_critique": False, "brief": ""}


def _dispatch_hold(lane, plan=None, worker=None):
    """What the loop does at the ONE dispatch point (round 18): routing (here
    stubbed to `plan`, a build by default) selects the next session and
    `routed_session` asks the hold. The hold's `(code, label, reason)` when the
    dispatch is held, None when the routed plan goes out."""
    from types import SimpleNamespace

    plan = dict(plan or _BUILD_PLAN)
    worker = worker or _worker(lane)
    ctx = SimpleNamespace(root=lane, worker=worker)
    original = agent_loop.route_session
    agent_loop.route_session = lambda *_a, **_k: plan
    try:
        out = agent_loop.routed_session(ctx, 1, WI, "001", "", 0)
    finally:
        agent_loop.route_session = original
    if out is plan:
        return None
    assert out == agent_loop.EXIT_NEEDS_HUMAN, out
    return agent_loop.build_hold(lane, worker)


def _stage_close(lane, dest="docs/archive/work/complete"):
    """Move the spec where a close puts it: `spec_move`'s terminal home under
    the archive by default (round 2, MAJOR 1), or the legacy one named."""
    src = "docs/work/active/{}/{}".format(BRANCH, SPEC)
    (lane / dest).mkdir(parents=True, exist_ok=True)
    _git(lane, "mv", src, "{}/{}".format(dest, SPEC))


def _merge_refusal(trunk, lane):
    _stage_close(lane)
    _git(lane, "commit", "-qm", "close {}".format(WI))
    return integrate._done_when_refusal(trunk, BRANCH, [WI])


# --- the hold: dispatch, hand close, merge ------------------------------------


def test_an_edit_with_no_verdict_holds_the_dispatch_and_the_close(tmp_path):
    trunk, lane = _lane(tmp_path)
    held = _dispatch_hold(lane)
    assert held is not None and held[:2] == (agent_loop.EXIT_NEEDS_HUMAN, "HELD")
    assert _digest() in held[2] and "60 fps" in held[2] and "30 fps" in held[2]
    _stage_close(lane)
    staged = integrate.staged_done_when_refusal(lane)
    assert staged and _digest() in staged
    assert integrate.main(["--root", str(lane), "done-when-hold"]) == 1
    _git(lane, "commit", "-qm", "close")
    merged = integrate._done_when_refusal(trunk, BRANCH, [WI])
    assert merged and merged.endswith("nothing was merged")


def test_an_unchanged_or_only_ticked_done_when_holds_nothing(tmp_path):
    ticked = DONE_WHEN.replace("- The", "- [x] The").replace(
        "box.", "box. — LANDED tests/test_widget.py::test_fps"
    )
    trunk, lane = _lane(tmp_path, body=ticked)
    assert _dispatch_hold(lane) is None
    assert _merge_refusal(trunk, lane) is None


@pytest.mark.parametrize(
    "dest",
    (
        "docs/archive/work/complete",
        "docs/archive/work/partial",
        "docs/archive/work/cancelled",
        "docs/work/complete",
    ),
)
def test_a_hand_close_into_any_terminal_home_is_held(tmp_path, dest):
    """Round 2, MAJOR 1: `spec_move` closes into the archive, so a hand close
    there is the ordinary one and must be held like the legacy home."""
    _trunk_root, lane = _lane(tmp_path)
    _stage_close(lane, dest)
    assert kdone.staged_closes(lane) == [(BRANCH, WI)]
    assert integrate.staged_done_when_refusal(lane)


def test_the_edit_commit_itself_is_not_held_by_the_hook(tmp_path):
    _trunk_root, lane = _lane(tmp_path, body=None)
    _write(lane, "docs/work/active/{}/{}".format(BRANCH, SPEC), _spec(NARROWED))
    _git(lane, "add", "-A")
    assert integrate.staged_done_when_refusal(lane) is None


@pytest.mark.parametrize("outcome", ("CLARITY", "BLESSED", "SUCCESSOR"))
def test_a_covering_verdict_releases_the_dispatch_and_the_close(tmp_path, outcome):
    trunk, lane = _lane(tmp_path)
    _bless(lane, "DONE-WHEN: {} changes=2 digest={}".format(outcome, _digest()))
    assert _dispatch_hold(lane) is None
    _stage_close(lane)
    assert integrate.staged_done_when_refusal(lane) is None
    _git(lane, "commit", "-qm", "close")
    assert integrate._done_when_refusal(trunk, BRANCH, [WI]) is None


def test_an_owner_ruling_binding_the_digest_releases_and_an_unseen_one_does_not(
    tmp_path,
):
    trunk, lane = _lane(tmp_path)
    entry = (
        "[decision.D-001]\n"
        'decided = "WI-007 renders at 30 fps."\nalternative = "60 fps."\n'
        'reversal_cost = "One line."\nwhy_not_escalated = "Owner ruled."\n'
        'review = ""\ndone_when = "{}"\n'.format(_digest())
    )
    _write(lane, "docs/decisions/wi-007.toml", entry)
    _commit(lane, "decisions: the ruling, not yet seen")
    assert _dispatch_hold(lane) is not None, "an entry the owner has not seen"
    _write(lane, "docs/decisions/wi-007.toml", entry + 'owner = "confirmed"\n')
    _commit(lane, "decisions: the owner confirms")
    assert _dispatch_hold(lane) is None
    assert _merge_refusal(trunk, lane) is None


def test_a_confirmed_ruling_still_carrying_the_retired_reviewed_key_does_not_release(
    tmp_path,
):
    """An entry still carrying the retired `reviewed` key reads as NOT YET
    SEEN whatever its `owner` says (kitlib.decisions), so its matching digest
    covers nothing and the hold stands."""
    from kitlib import decisions as kdecisions

    trunk, lane = _lane(tmp_path)
    entry = (
        "[decision.D-001]\n"
        'decided = "WI-007 renders at 30 fps."\nalternative = "60 fps."\n'
        'reversal_cost = "One line."\nwhy_not_escalated = "Owner ruled."\n'
        'review = ""\ndone_when = "{}"\nowner = "confirmed"\n'
        "{} = true\n".format(_digest(), kdecisions.RETIRED_KEY)
    )
    _write(lane, "docs/decisions/wi-007.toml", entry)
    _commit(lane, "decisions: confirmed, but carrying the retired key")
    assert _digest() not in kdone.covering(lane, "HEAD")
    held = _dispatch_hold(lane)
    assert held is not None and _digest() in held[2]
    assert _merge_refusal(trunk, lane) is not None


def test_changing_the_text_after_a_verdict_holds_again(tmp_path):
    trunk, lane = _lane(tmp_path)
    _bless(lane, "DONE-WHEN: BLESSED changes=2 digest={}".format(_digest()))
    assert _dispatch_hold(lane) is None
    again = NARROWED.replace("30 fps", "20 fps")
    _write(lane, "docs/work/active/{}/{}".format(BRANCH, SPEC), _spec(again))
    _commit(lane, "edit the Done-when again")
    held = _dispatch_hold(lane)
    assert held is not None and _digest(again) in held[2]
    assert _merge_refusal(trunk, lane) is not None


def test_an_adjudication_row_is_never_held_at_dispatch(tmp_path):
    _trunk_root, lane = _lane(tmp_path)
    worker = _worker(lane)
    worker["rows"][WI]["SafetyClass"] = "adjudication"
    assert agent_loop.build_hold(lane, worker) is None


# --- the done-when brief ------------------------------------------------------


def _row(brief, scope):
    return {"WI-ID": "WI-900", "Brief": brief, "Adjudicates": scope}


def test_the_done_when_brief_binds_the_digest_the_holds_compute(tmp_path):
    _trunk_root, lane = _lane(tmp_path)
    text, why = ab.compose(lane, _row("done-when", WI), "docs/reviews/v.md")
    assert why is None, why
    assert _digest() in text and "60 fps" in text and "30 fps" in text
    assert "WI: WI-900" in text
    assert "done-when" in ab.BRIEF_PROMPTS and "done-when" in ab.ROUTED


def test_the_done_when_brief_carries_the_specs_context(tmp_path):
    """Round 2, MAJOR 4: the template asks whether the change keeps the purpose
    the Context states, so two specs with opposite purposes brief differently."""
    _trunk_root, lane = _lane(tmp_path)
    text, why = ab.compose(lane, _row("done-when", WI), "v.md")
    assert why is None, why
    assert "A widget." in text
    path = lane / "docs/work/active/{}/{}".format(BRANCH, SPEC)
    path.write_text(
        _spec(NARROWED).replace("A widget.", "The frame rate is a tunable target."),
        encoding="utf-8",
        newline="\n",
    )
    _commit(lane, "a different purpose")
    other, why = ab.compose(lane, _row("done-when", WI), "v.md")
    assert why is None and "tunable target" in other and other != text


def test_the_done_when_brief_refuses_an_unchanged_done_when(tmp_path):
    _trunk_root, lane = _lane(tmp_path, body=None)
    _text, why = ab.compose(lane, _row("done-when", WI), "v.md")
    assert "no change to judge" in why


def test_the_done_when_verdict_grammar(tmp_path):
    good = tmp_path / "good.md"
    good.write_text("DONE-WHEN: CLARITY changes=1 digest=sha256:ab\n", "utf-8")
    assert ab.verdict_refusal("done-when", good) is None
    bad = tmp_path / "bad.md"
    bad.write_text("DONE-WHEN: CLARITY changes=1\n", "utf-8")
    assert "omits digest" in ab.verdict_refusal("done-when", bad)


# --- one combined sitting per lane checkpoint ----------------------------------


def _fake_spine_assemblers(monkeypatch):
    """The amendment and first-approval assemblers, stubbed to their slot sets
    and recording the scope each was handed; the done-when one stays real."""
    seen = {}

    def amendment(_root, row):
        seen["amendment"] = row["Adjudicates"]
        return {"baseline": "B", "rows": "- LLR LLR-1 drifted", "aftermath": "A"}, None

    def first(_root, row):
        seen["first-approval"] = row["Adjudicates"]
        return {
            "chain": "- TC TC-1 [AWAITING FIRST APPROVAL]",
            "baseline": "B",
            "registries": "R",
            "approves_rows": "   - R covers TC-1",
        }, None

    monkeypatch.setitem(ab._ASSEMBLERS, "amendment", amendment)
    monkeypatch.setitem(ab._ASSEMBLERS, "first-approval", first)
    return seen


def test_a_combined_sitting_composes_each_kind_from_its_own_brief(
    tmp_path, monkeypatch
):
    _trunk_root, lane = _lane(tmp_path)
    seen = _fake_spine_assemblers(monkeypatch)
    scope = "amendment:LLR-1;first-approval:TC-1;done-when:{}".format(WI)
    text, why = ab.compose(lane, _row("combined", scope), "docs/reviews/s.md")
    assert why is None, why
    assert seen == {"amendment": "LLR-1", "first-approval": "TC-1"}
    order = [text.index("=== SECTION `## {}`".format(k)) for k in ab.COMBINABLE]
    assert order == sorted(order)
    assert "the `## done-when` section of docs/reviews/s.md" in text
    assert "kinds=amendment;first-approval;done-when" in text
    assert _digest() in text
    assert "combined" in ab.ROUTED


def test_a_combined_sitting_refuses_whole_when_a_section_cannot_compose(
    tmp_path, monkeypatch
):
    _trunk_root, lane = _lane(tmp_path, body=None)
    _fake_spine_assemblers(monkeypatch)
    scope = "amendment:LLR-1;done-when:{}".format(WI)
    text, why = ab.compose(lane, _row("combined", scope), "s.md")
    assert text is None and "the done-when section" in why
    _text, why = ab.compose(lane, _row("combined", "LLR-1"), "s.md")
    assert "not `<kind>:<id>`" in why


SITTING = (
    "## amendment\n\n- [CLARITY] LLR-1 Detail -> a -> a -> same\n\n"
    "VERDICT: CLARITY rows=1\n\n"
    "## first-approval\n\nOUTCOME: APPROVE rows=1\n\n"
    "## done-when\n\nDONE-WHEN: BLESSED changes=2 digest={}\n\n"
    "SITTING: JUDGED kinds=amendment;first-approval;done-when\n"
)


KINDS = ("amendment", "first-approval", "done-when")


def test_a_combined_verdict_is_parsed_section_by_section(tmp_path):
    path = tmp_path / "s.md"
    path.write_text(SITTING.format(_digest()), "utf-8")
    assert ab.verdict_refusal("combined", path, kinds=KINDS) is None
    path.write_text(SITTING.format(_digest()).replace("OUTCOME: APPROVE", "OK"))
    assert "(## first-approval)" in ab.verdict_refusal("combined", path, kinds=KINDS)
    path.write_text(SITTING.format(_digest()).replace(";done-when", ""))
    assert "requested" in ab.verdict_refusal("combined", path, kinds=KINDS)
    path.write_text(SITTING.format(_digest()).replace("## done-when\n", ""))
    refusal = ab.verdict_refusal("combined", path, kinds=KINDS)
    assert "carries the section(s)" in refusal


def test_a_combined_verdict_must_judge_exactly_the_kinds_its_sitting_requested(
    tmp_path,
):
    """Round 2, MAJOR 5: an empty sitting line no longer validates vacuously,
    and a verdict that drops a requested kind from both its line and its
    headings is refused against what the sitting asked."""
    path = tmp_path / "s.md"
    path.write_text("SITTING: JUDGED kinds=;\n", "utf-8")
    assert ab.verdict_refusal("combined", path, kinds=KINDS)
    assert ab.verdict_refusal("combined", path, kinds=())
    dropped = (
        "## amendment\n\nVERDICT: CLARITY rows=1\n\nSITTING: JUDGED kinds=amendment\n"
    )
    path.write_text(dropped, "utf-8")
    assert "requested" in ab.verdict_refusal("combined", path, kinds=KINDS)
    assert ab.verdict_refusal("combined", path, kinds=("amendment",)) is None
    # With no requested kinds to judge against, a combined verdict is refused.
    assert "requested" in ab.verdict_refusal("combined", path)


def test_the_coordinator_reads_the_requested_kinds_from_the_composed_brief(
    tmp_path, monkeypatch
):
    _trunk_root, lane = _lane(tmp_path)
    _fake_spine_assemblers(monkeypatch)
    scope = "amendment:LLR-1;done-when:{}".format(WI)
    text, why = ab.compose(lane, _row("combined", scope), "s.md")
    assert why is None, why
    assert ab.requested_kinds(text) == ("amendment", "done-when")


def test_a_combined_verdicts_done_when_section_is_acted_on(tmp_path):
    """The done-when section's line is the blessing: the holds read it from the
    one sitting's file as from a sitting of its own."""
    trunk, lane = _lane(tmp_path)
    _bind(lane, KINDS)
    _bless(lane, SITTING.format(_digest()))
    assert _dispatch_hold(lane) is None
    assert _merge_refusal(trunk, lane) is None


def test_both_new_classes_are_accepted_by_the_coordinator_entry_point():
    cli = load_script("coordinator_adjudicate")
    args = cli._parser().parse_args(
        ["adjudicate", "--brief-file", "b", "--brief", "combined", "--wi", WI]
        + ["--verdict", "v"]
    )
    assert args.brief == "combined"
    for brief in ("done-when", "combined"):
        assert brief in ab.BRIEF_PROMPTS


def test_this_repo_retains_both_new_classes():
    keep = load_script("session_keep")
    from conftest import ROOT

    retained = keep.keep_config(ROOT).retain_for
    assert "done-when" in retained and "combined" in retained


# --- at merge: the goalposts row is the safety net ----------------------------


def _merged(tmp_path, verdict=None, bound=None):
    """`(root, before, after)`: one repo whose merge commit closes WI-007 with
    the narrowed Done-when, carrying `verdict` under the review records, and
    `bound` - a combined sitting's requested kinds - as the binding the entry
    point writes beside it (round 10)."""
    root = _trunk(tmp_path)
    before = _git(root, "rev-parse", "HEAD")
    (root / "docs/work/active" / BRANCH / SPEC).unlink()
    _write(root, "docs/archive/work/complete/" + SPEC, _spec(NARROWED))
    if verdict:
        rel = "docs/reviews/{}/001-ADJUDICATE-x.md".format(BRANCH)
        _write(root, rel, verdict)
        brief, kinds = ("combined", bound) if bound else ("done-when", ("done-when",))
        binding = ab.ksitting.render_requested(brief, kinds, "accepted")
        _write(root, ab.ksitting.requested_path(rel), binding)
    return root, before, _commit(root, "integrate: merge " + BRANCH)


def _intake(root, before, after):
    return intake.intake_after_merge(root, before, after, {WI: "merged"}, BRANCH)


def test_at_merge_an_uncovered_close_mints_the_goalposts_row(tmp_path):
    root, before, after = _merged(tmp_path)
    minted, refusal = _intake(root, before, after)
    assert refusal is None, refusal
    assert len(minted) == 1
    body = (root / minted[0][1]).read_text(encoding="utf-8")
    assert 'brief = "done-when"' in body and WI in body


def test_at_merge_a_covered_close_mints_nothing(tmp_path):
    line = "DONE-WHEN: CLARITY changes=2 digest={}\n".format(_digest())
    root, before, after = _merged(tmp_path, verdict=line)
    minted, refusal = _intake(root, before, after)
    assert refusal is None and minted == []


def test_at_merge_a_successor_verdict_mints_its_own_draft(tmp_path):
    verdict = (
        "DONE-WHEN: SUCCESSOR changes=2 digest={}\n\n## Dispositions\n\n"
        '```toml\ntitle = "Render the widget at 60 fps"\n```\n\n'
        "The 60 fps half the lane dropped.\n".format(_digest())
    )
    root, before, after = _merged(tmp_path, verdict=verdict)
    minted, refusal = _intake(root, before, after)
    assert refusal is None, refusal
    assert len(minted) == 1
    body = (root / minted[0][1]).read_text(encoding="utf-8")
    assert "Render the widget at 60 fps" in body
    empty = "DONE-WHEN: SUCCESSOR changes=2 digest={}\n".format(_digest())
    root, before, after = _merged(tmp_path / "again", verdict=empty)
    minted, refusal = _intake(root, before, after)
    assert minted == [] and "no ## Dispositions draft" in refusal


def test_the_hold_points_share_one_predicate():
    """No hold point re-derives the rule: each reads `lane_hold`."""
    for module, name in (
        (agent_loop, "build_hold"),
        (integrate, "_done_when_refusal"),
        (integrate, "staged_done_when_refusal"),
    ):
        source = getattr(module, name).__code__.co_names
        assert "lane_hold" in source, name
    assert os.path.basename(kdone.__file__) == "done_when.py"


def _draft(title):
    return '## Dispositions\n\n```toml\ntitle = "{}"\n```\n\nIts scope.\n\n'.format(
        title
    )


def test_at_merge_a_combined_successor_mints_the_done_when_sections_own_draft(
    tmp_path,
):
    """Round 2, MAJOR 3: a combined verdict whose first-approval section
    carries a RETURN draft BEFORE the done-when section's SUCCESSOR draft. The
    merge mints the done-when section's own draft, never the first one."""
    verdict = (
        "## first-approval\n\nOUTCOME: RETURN rows=1\n\n"
        + _draft("Rework TC-1")
        + "## done-when\n\nDONE-WHEN: SUCCESSOR changes=2 digest={}\n\n".format(
            _digest()
        )
        + _draft("Render the widget at 60 fps")
        + "SITTING: JUDGED kinds=first-approval;done-when\n"
    )
    bound = ("first-approval", "done-when")
    root, before, after = _merged(tmp_path, verdict=verdict, bound=bound)
    minted, refusal = _intake(root, before, after)
    assert refusal is None, refusal
    bodies = [(root / rel).read_text(encoding="utf-8") for _wid, rel in minted]
    assert len(bodies) == 1 and "Render the widget at 60 fps" in bodies[0]
    assert "Rework TC-1" not in bodies[0]


def test_at_merge_an_ambiguous_successor_section_refuses(tmp_path):
    """Two Dispositions sections in the done-when section of a valid sitting
    are ambiguous: the mint refuses rather than pick one."""
    twice = (
        "## done-when\n\nDONE-WHEN: SUCCESSOR changes=2 digest={}\n\n".format(_digest())
        + _draft("One")
        + _draft("Two")
        + "SITTING: JUDGED kinds=done-when\n"
    )
    root, before, after = _merged(tmp_path, verdict=twice, bound=("done-when",))
    minted, refusal = _intake(root, before, after)
    assert minted == [] and "ambiguous" in refusal


def test_at_merge_a_successor_line_outside_its_section_blesses_nothing(tmp_path):
    """Round 9: a SUCCESSOR line under another kind's heading leaves the
    `## done-when` section without its machine line, so the sitting is
    invalid and blesses nothing (SR-232): the close is uncovered and the merge
    mints the goalposts row, never the stray line's draft."""
    misplaced = (
        "## amendment\n\nVERDICT: CLARITY rows=1\n"
        "DONE-WHEN: SUCCESSOR changes=2 digest={}\n\n".format(_digest())
        + _draft("One")
        + "## done-when\n\nnothing\n\nSITTING: JUDGED kinds=amendment;done-when\n"
    )
    root, before, after = _merged(tmp_path, verdict=misplaced)
    minted, refusal = _intake(root, before, after)
    assert refusal is None and len(minted) == 1, (minted, refusal)
    body = (root / minted[0][1]).read_text(encoding="utf-8")
    assert 'brief = "done-when"' in body and "One" not in body.split("+++")[1]


def test_a_combined_rows_tokens_scope_each_kinds_act():
    """Round 2, MAJOR 2: the act scopes read a combined row's `<kind>:<id>`
    tokens for their own kind through the same readers a single-kind row
    uses; the act-taking cases are in tests/test_snapshot_readers.py."""
    ar = load_script("acceptance_record")
    combined = [
        (
            "WI-900.md",
            {
                "brief": "combined",
                "adjudicates": ["first-approval:TC-001", "amendment:LLR-001"]
                + ["done-when:WI-007"],
            },
        )
    ]
    assert ar.first_approval_scope(combined) == {"TC-001"}
    assert ar.amendment_scope(combined) == {"LLR-001"}
    only = [("WI-901.md", {"brief": "combined", "adjudicates": ["amendment:SR-1"]})]
    assert ar.first_approval_scope(only) is None


# --- round 4: an ABSENT claim is released, an UNREADABLE one is held ----------

UNREADABLE = "0" * 40  # a revision no repository holds


def test_an_absent_claim_is_released_at_every_hold_point(tmp_path):
    """ABSENT: the revision reads, and no spec of the row sits under
    `active/<branch>/` there (a row never claimed through this lane): there is
    no claimed Done-when, so there is nothing to bless."""
    trunk, lane = _lane(tmp_path)
    base = agent_loop.default_base(lane)
    assert kdone.claim_copy(lane, base, "wi-999", WI) == (None, None)
    assert kdone.lane_hold(lane, "HEAD", base, "wi-999", [WI]) is None


def test_an_unreadable_claim_is_held_naming_why(tmp_path):
    """UNREADABLE: the claim's revision (or its copy) cannot be read, so
    whether the lane moved its Done-when is unknown: every hold point holds,
    naming why, rather than failing open."""
    _trunk_root, lane = _lane(tmp_path)
    text, why = kdone.claim_copy(lane, UNREADABLE, BRANCH, WI)
    assert text is None and "cannot be read" in why
    _text, why = kdone.claim_copy(lane, None, BRANCH, WI)
    assert "cannot be read" in why
    held = kdone.lane_hold(lane, "HEAD", UNREADABLE, BRANCH, [WI])
    assert held and "cannot be read" in held and WI in held
    worker = _worker(lane)
    worker["base"] = UNREADABLE
    end = agent_loop.build_hold(lane, worker)
    assert end and end[:2] == (agent_loop.EXIT_NEEDS_HUMAN, "HELD")
    assert "cannot be read" in end[2]


def test_a_review_session_is_never_held(tmp_path):
    """The next session is a review (the review queue is open): it reads the
    Done-when as evidence, and is not held; the build after it is."""
    _trunk_root, lane = _lane(tmp_path)
    review = dict(_BUILD_PLAN, is_review=True)
    assert _dispatch_hold(lane, plan=review) is None
    critique = dict(_BUILD_PLAN, is_critique=True)
    assert _dispatch_hold(lane, plan=critique) is None
    assert _dispatch_hold(lane) is not None


def test_the_merge_refusal_names_the_digest_and_the_changes(tmp_path):
    trunk, lane = _lane(tmp_path)
    refusal = _merge_refusal(trunk, lane)
    assert refusal and _digest() in refusal
    assert "60 fps" in refusal and "30 fps" in refusal
    assert "sha256:" in _digest() and len(_digest()) == len("sha256:") + 16


def test_at_merge_an_unreadable_claim_refuses_the_mint(tmp_path):
    root, _before, after = _merged(tmp_path)
    minted, refusal = _intake(root, UNREADABLE, after)
    assert minted == [] and refusal and "cannot be read" in refusal


def test_at_merge_an_absent_claim_mints_nothing_and_says_so(tmp_path, capsys):
    root, before, after = _merged(tmp_path)
    minted, refusal = intake.intake_after_merge(
        root, before, after, {WI: "merged"}, "wi-999"
    )
    assert refusal is None and minted == []
    assert "did not run" in capsys.readouterr().err


def test_the_done_when_brief_refuses_an_unreadable_claim(tmp_path, monkeypatch):
    _trunk_root, lane = _lane(tmp_path)
    monkeypatch.setattr(ab.ac, "default_base", lambda _root: UNREADABLE)
    text, why = ab.compose(lane, _row("done-when", WI), "v.md")
    assert text is None and "cannot be read" in why


def test_the_done_when_brief_refuses_a_spec_with_no_context(tmp_path):
    _trunk_root, lane = _lane(tmp_path)
    path = lane / "docs/work/active/{}/{}".format(BRANCH, SPEC)
    path.write_text(
        _spec(NARROWED).replace("## Context\n\nA widget.\n", ""),
        encoding="utf-8",
        newline="\n",
    )
    _commit(lane, "no context")
    text, why = ab.compose(lane, _row("done-when", WI), "v.md")
    assert text is None and "## Context" in why


def test_the_done_when_brief_reads_a_closed_rows_claim_from_its_claim_commit(
    tmp_path,
):
    """After the merge (the goalposts row a merge minted) the claim is the copy
    the claim commit added, the newest commit adding the spec under active/."""
    root, _before, _after = _merged(tmp_path)
    claim = _git(root, "log", "-1", "--format=%H", "--grep=claim: ")
    text, why = ab.compose(root, _row("done-when", WI), "v.md")
    assert why is None, why
    assert "the claim copy at the claim commit {}".format(claim[:10]) in text
    assert _digest() in text and "archive/work/complete" in text


def test_the_done_when_brief_clips_a_long_context_at_its_stated_limit(tmp_path):
    _trunk_root, lane = _lane(tmp_path)
    long_context = "\n".join("line {}".format(n) for n in range(1, 151))
    path = lane / "docs/work/active/{}/{}".format(BRANCH, SPEC)
    path.write_text(
        _spec(NARROWED).replace("A widget.", long_context),
        encoding="utf-8",
        newline="\n",
    )
    _commit(lane, "a long context")
    text, why = ab.compose(lane, _row("done-when", WI), "v.md")
    assert why is None, why
    limit = ab.CANDIDATE_CLIP
    assert (
        "line {}\n".format(limit) in text and "line {}\n".format(limit + 1) not in text
    )
    assert "clipped at {} lines".format(limit) in text


# --- round 7: the CURRENT side, test runs, and the merge-time covers ---------


def test_an_unreadable_current_spec_is_held_naming_why(tmp_path):
    """The lane's own copy read at a revision that cannot be read: whether the
    Done-when changed is unknown, so the hold holds, as for an unreadable claim."""
    _trunk_root, lane = _lane(tmp_path)
    base = agent_loop.default_base(lane)
    path, text, why = kdone.spec_at(lane, UNREADABLE, BRANCH, WI)
    assert (path, text) == (None, None) and "cannot be read" in why
    held = kdone.lane_hold(lane, UNREADABLE, base, BRANCH, [WI])
    assert held and "cannot be read" in held and WI in held


def test_a_claimed_row_whose_spec_is_gone_from_the_lane_is_held(tmp_path):
    """A claim present, and no copy of the spec in the lane at all (neither
    under active/<branch>/ nor in a closed folder): the claimed Done-when is
    gone, which no close accounts for, so the lane is held, naming it."""
    _trunk_root, lane = _lane(tmp_path)
    _git(lane, "rm", "-q", "docs/work/active/{}/{}".format(BRANCH, SPEC))
    _commit(lane, "the spec deleted")
    held = _dispatch_hold(lane)
    assert held and "no copy of its spec" in held[2]


def test_a_lane_that_deletes_its_done_when_section_owes_a_blessing(tmp_path):
    """Every claimed item reads as changed, so the deletion is a scope move the
    holds see, with its own digest."""
    _trunk_root, lane = _lane(tmp_path, body="\n## Deliverable\n\nNone.\n")
    held = _dispatch_hold(lane)
    assert held is not None
    assert held[2].count("at claim, no longer present as written") == 2
    no_section = _spec("\n## Deliverable\n\nNone.\n")
    assert kdone.changes(_spec(DONE_WHEN), no_section) == [
        ("changed", item) for item in kdone.items(_spec(DONE_WHEN))
    ]


def test_a_test_run_is_never_held(tmp_path):
    """A held lane (an unblessed edit, its next build held) still runs its
    tests: nothing in the test runner reads the hold, so the suite's evidence
    stays free to gather."""
    _trunk_root, lane = _lane(tmp_path)
    assert _dispatch_hold(lane) is not None
    _write(lane, "tests/test_evidence.py", "def test_runs():\n    assert True\n")
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"]
        + ["tests/test_evidence.py"],
        cwd=str(lane),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "1 passed" in proc.stdout


def test_at_merge_a_blessed_cover_mints_nothing(tmp_path):
    line = "DONE-WHEN: BLESSED changes=2 digest={}\n".format(_digest())
    root, before, after = _merged(tmp_path, verdict=line)
    minted, refusal = _intake(root, before, after)
    assert refusal is None and minted == []


def test_at_merge_a_successor_verdict_with_no_draft_refuses(tmp_path):
    line = "DONE-WHEN: SUCCESSOR changes=2 digest={}\n".format(_digest())
    root, before, after = _merged(tmp_path, verdict=line)
    minted, refusal = _intake(root, before, after)
    assert minted == [] and "no ## Dispositions draft" in refusal


# --- round 9: only a VALID verdict blesses; unrequested sections refuse -------

REJECTED_SITTING = (
    "## amendment\n\n- [CLARITY] LLR-1 Detail -> a -> a -> same\n\n"
    "## done-when\n\nDONE-WHEN: BLESSED changes=2 digest={}\n\n"
    "SITTING: JUDGED kinds=amendment;done-when\n"
)


def test_a_rejected_combined_sitting_blesses_nothing(tmp_path):
    """Sol final MAJOR 1: the done-when section's line matches, but the
    amendment section has no machine line, so the sitting is refused whole
    (SR-232) and its Done-when line releases no hold and covers no close."""
    trunk, lane = _lane(tmp_path)
    text = REJECTED_SITTING.format(_digest())
    probe = tmp_path / "probe.md"
    probe.write_text(text, encoding="utf-8")
    kinds = ("amendment", "done-when")
    assert ab.verdict_refusal("combined", probe, kinds=kinds)
    _bless(lane, text)
    assert _digest() not in kdone.covering(lane, "HEAD")
    assert _dispatch_hold(lane) is not None
    _stage_close(lane)
    assert integrate.staged_done_when_refusal(lane)
    _git(lane, "commit", "-qm", "close")
    assert integrate._done_when_refusal(trunk, BRANCH, [WI])
    root, before, after = _merged(tmp_path / "merged", verdict=text)
    minted, refusal = _intake(root, before, after)
    assert refusal is None and len(minted) == 1, (minted, refusal)


def test_an_unrequested_section_refuses_the_combined_verdict(tmp_path):
    """Sol final MAJOR 2: a sitting that requested `amendment` alone, whose
    verdict also carries a `## red-tc` section, is refused: any `## <kind>`
    heading counts, and every section not requested refuses."""
    path = tmp_path / "s.md"
    path.write_text(
        "## amendment\n\nVERDICT: CLARITY rows=1\n\n"
        "## red-tc\n\nOUTCOME: DRAFTED cases=1 drafts=1\n\n"
        "SITTING: JUDGED kinds=amendment\n",
        encoding="utf-8",
    )
    refusal = ab.verdict_refusal("combined", path, kinds=("amendment",))
    assert refusal and "red-tc" in refusal


def test_a_valid_sitting_with_an_unrequested_section_blesses_nothing(tmp_path):
    """The same rule at the hold: a done-when section inside a sitting that
    carries an extra kind's section is not a valid verdict, so it covers
    nothing."""
    _trunk_root, lane = _lane(tmp_path)
    _bless(
        lane,
        "## done-when\n\nDONE-WHEN: BLESSED changes=2 digest={}\n\n"
        "## red-tc\n\nOUTCOME: DRAFTED cases=1 drafts=1\n\n"
        "SITTING: JUDGED kinds=done-when\n".format(_digest()),
    )
    assert _digest() not in kdone.covering(lane, "HEAD")
    assert _dispatch_hold(lane) is not None


# --- round 10: parse, don't validate; the requested kinds are bound ----------


def _bind(lane, kinds, brief="combined", outcome="accepted"):
    """The binding the routes write: the sitting's requested kinds at
    reservation and the outcome the route that ran the call records,
    beside the verdict, committed."""
    ksitting = load_script("adjudicate_brief").ksitting
    rel = "docs/reviews/{}/001-ADJUDICATE-x.md".format(BRANCH)
    text = ksitting.render_requested(brief, kinds, outcome)
    _write(lane, ksitting.requested_path(rel), text)
    _commit(lane, "bind the requested kinds")


def test_a_sitting_missing_a_requested_kind_blesses_nothing(tmp_path):
    """Sol final2 MAJOR 1: the brief requested `amendment;done-when`; the
    verdict judges only the done-when section and names only it. Against its
    BOUND requested kinds it is invalid, so it releases nothing."""
    _trunk_root, lane = _lane(tmp_path)
    _bind(lane, ("amendment", "done-when"))
    _bless(
        lane,
        "## done-when\n\nDONE-WHEN: BLESSED changes=2 digest={}\n\n"
        "SITTING: JUDGED kinds=done-when\n".format(_digest()),
    )
    assert _digest() not in kdone.covering(lane, "HEAD")
    assert _dispatch_hold(lane) is not None


def test_an_incomplete_second_machine_line_blesses_nothing(tmp_path):
    """Sol final2 MAJOR 2: two DONE-WHEN lines, the first complete with an old
    digest, the second the current digest without `changes=`. A verdict
    carries exactly one complete machine line, so neither line counts."""
    _trunk_root, lane = _lane(tmp_path)
    _bless(
        lane,
        "DONE-WHEN: BLESSED changes=1 digest=sha256:0000000000000000\n"
        "DONE-WHEN: BLESSED digest={}\n".format(_digest()),
    )
    assert _digest() not in kdone.covering(lane, "HEAD")
    assert _dispatch_hold(lane) is not None
    path = tmp_path / "v.md"
    path.write_text(
        "DONE-WHEN: BLESSED changes=1 digest={0}\nDONE-WHEN: BLESSED changes=1"
        " digest={0}\n".format(_digest()),
        encoding="utf-8",
    )
    assert "exactly one" in ab.verdict_refusal("done-when", path)


def test_a_bound_sitting_that_judges_every_requested_kind_blesses(tmp_path):
    """The positive arm: the bound kinds are judged, each section complete."""
    _trunk_root, lane = _lane(tmp_path)
    _bind(lane, ("amendment", "done-when"))
    _bless(
        lane,
        "## amendment\n\n- [CLARITY] LLR-1 Detail -> a -> a -> same\n\n"
        "VERDICT: CLARITY rows=1\n\n"
        "## done-when\n\nDONE-WHEN: BLESSED changes=2 digest={}\n\n"
        "SITTING: JUDGED kinds=amendment;done-when\n".format(_digest()),
    )
    assert _digest() in kdone.covering(lane, "HEAD")
    assert _dispatch_hold(lane) is None


def test_an_unbound_sitting_blesses_nothing(tmp_path):
    """A combined sitting whose requested kinds were never bound cannot be
    judged against what was asked, so it covers nothing."""
    _trunk_root, lane = _lane(tmp_path)
    _bless(lane, SITTING.format(_digest()), bound=False)
    assert _digest() not in kdone.covering(lane, "HEAD")


def test_the_entry_point_binds_the_requested_kinds_beside_the_verdict(tmp_path):
    """Round 10: at reservation the entry point writes the sitting's brief and
    requested kinds beside the verdict, exclusively; a combined brief naming
    no kinds refuses, and a refused call's release removes both files."""
    cli = load_script("coordinator_adjudicate")
    verdict = tmp_path / "reviews" / "001-ADJUDICATE-x.md"
    assert cli.reserve_verdict(verdict) is None
    brief = "SITTING: JUDGED kinds=amendment;done-when\n"
    assert cli.bind_requested(verdict, "combined", brief) is None
    binding = ab.ksitting.requested_path(verdict)
    assert ab.ksitting.read_requested(open(binding, encoding="utf-8").read()) == (
        "combined",
        ("amendment", "done-when"),
        "pending",
    )
    assert cli.bind_requested(verdict, "combined", brief), "exclusive"
    cli._release(verdict)
    assert not verdict.exists() and not os.path.exists(binding)
    assert cli.bind_requested(tmp_path / "v.md", "combined", "no line")
    single = tmp_path / "s.md"
    assert cli.bind_requested(single, "done-when", "") is None
    text = open(ab.ksitting.requested_path(single), encoding="utf-8").read()
    assert ab.ksitting.read_requested(text) == ("done-when", ("done-when",), "pending")


# --- round 11: acceptance is a recorded fact ---------------------------------

ROUTE = "ANTHROPIC-OPUS-STRONG"
_AGENTS = (
    '[agent.ANTHROPIC-OPUS-STRONG]\nfamily = "ANTHROPIC"\n'
    'model = "claude-opus-5-5"\nversion = "5.5"\ntier = "strong"\n'
    'cmd_template = "claude -p --model {model}"\nenv = ""\nnotes = "test row"\n'
)


def _entry_point_call(lane, monkeypatch, code, timed_out, text, result=""):
    """Run the coordinator's real entry point on the lane, only the model
    call replaced: the session writes and commits `text` as its verdict,
    then exits `code` (or times out)."""
    from types import SimpleNamespace

    cli = load_script("coordinator_adjudicate")
    _write(lane, "docs/process.toml", "[adjudicator]\ncontext_reset_pct = 0\n")
    _write(lane, "docs/agents.toml", _AGENTS)
    _write(lane, "docs/agents-enabled", ROUTE + "\n")
    _write(lane, "brief.md", "judge the Done-when")
    _commit(lane, "route inputs")
    verdict = lane / "docs/reviews/{}/001-ADJUDICATE-x.md".format(BRANCH)

    def call(_request):
        verdict.write_text(text, encoding="utf-8")
        _commit(lane, "the session's verdict")
        return SimpleNamespace(code=code, timed_out=timed_out, text=result)

    monkeypatch.setattr(cli.session_service, "call", call)
    monkeypatch.setattr(cli.session_service, "adjudication_keep", lambda _r: None)
    args = SimpleNamespace(
        root=lane,
        brief_file=lane / "brief.md",
        brief="done-when",
        wi=WI,
        verdict=verdict,
        route=ROUTE,
        timeout=60,
    )
    return cli.adjudicate(args), verdict


@pytest.mark.parametrize("code,timed_out", ((1, False), (0, True)))
def test_a_failed_calls_verdict_releases_nothing(
    tmp_path, monkeypatch, code, timed_out
):
    """Sol final3 MAJOR 2, through the real entry point: the session committed
    a matching BLESSED verdict, then the call failed or timed out. The route
    records the binding FAILED, so the verdict covers nothing."""
    _trunk_root, lane = _lane(tmp_path)
    line = "DONE-WHEN: BLESSED changes=2 digest={}\n".format(_digest())
    returned, verdict = _entry_point_call(lane, monkeypatch, code, timed_out, line)
    assert returned == 1
    binding = ab.ksitting.requested_path(verdict)
    assert ab.ksitting.read_requested(open(binding, encoding="utf-8").read())[2] == (
        "failed"
    )
    assert _digest() not in kdone.covering(lane, "HEAD")
    assert _dispatch_hold(lane) is not None


def test_an_accepted_calls_verdict_releases(tmp_path, monkeypatch):
    """The positive arm: a call that exits 0 with a valid verdict is recorded
    ACCEPTED by the route that ran it, and only then covers."""
    _trunk_root, lane = _lane(tmp_path)
    line = "DONE-WHEN: BLESSED changes=2 digest={}\n".format(_digest())
    returned, verdict = _entry_point_call(lane, monkeypatch, 0, False, line)
    assert returned == 0
    binding = ab.ksitting.requested_path(verdict)
    assert ab.ksitting.read_requested(open(binding, encoding="utf-8").read())[2] == (
        "accepted"
    )
    assert _digest() in kdone.covering(lane, "HEAD")
    assert _dispatch_hold(lane) is None


def test_another_brief_classes_verdict_covers_nothing_and_never_raises(tmp_path):
    """Sol final3 MAJOR 3: a valid DISPOSITION verdict, bound and accepted,
    whose prose carries a fenced Done-when example. A class the reader does
    not cover is simply not a Done-when blessing - no KeyError at dispatch."""
    _trunk_root, lane = _lane(tmp_path)
    _bind(lane, ("disposition",), brief="disposition")
    _bless(
        lane,
        "OUTCOME: COMPLETE successors=0\n\nExample:\n```\n"
        "DONE-WHEN: BLESSED changes=2 digest={}\n```\n".format(_digest()),
    )
    assert _digest() not in kdone.covering(lane, "HEAD")
    assert _dispatch_hold(lane) is not None


@pytest.mark.parametrize("valid,outcome", ((True, "accepted"), (False, "failed")))
def test_the_loop_route_records_its_verdicts_outcome(tmp_path, valid, outcome):
    """The loop is the other route that runs adjudications: after validating
    its session's verdict it records the outcome through the same writer and
    commits the binding, so the holds read the recorded fact."""
    _trunk_root, lane = _lane(tmp_path)
    line = "DONE-WHEN: BLESSED changes=2 digest={}\n".format(_digest())
    _write(lane, _VERDICT_REL, line if valid else "no machine line\n")
    _commit(lane, "the session's verdict")
    plan = {"brief": "done-when", "verdict_path": lane / _VERDICT_REL}
    worker = {"adjudication_owed": ""}
    # A call that succeeded: exit 0, within its deadline.
    plan["call_ok"] = True  # run_iteration's record of a call that succeeded
    agent_loop.adjudication_bookkeeping(plan, worker, None, False, None, 0, lane)
    text = (lane / ab.ksitting.requested_path(_VERDICT_REL)).read_text(encoding="utf-8")
    assert ab.ksitting.read_requested(text)[2] == outcome
    assert _git(lane, "status", "--porcelain") == "", "the binding is committed"
    assert (_digest() in kdone.covering(lane, "HEAD")) is valid


@pytest.mark.parametrize("code,timed_out", ((1, False), (0, True)))
def test_the_loop_records_a_failed_calls_verdict_failed(tmp_path, code, timed_out):
    """Sol final4 MAJOR 1, through `session_bookkeeping`: the session committed
    a matching BLESSED verdict, then exited 1 or timed out. One rule for both
    routes: accepted only when the CALL succeeded and the verdict validates."""
    from types import SimpleNamespace

    _trunk_root, lane = _lane(tmp_path)
    line = "DONE-WHEN: BLESSED changes=2 digest={}\n".format(_digest())
    _write(lane, _VERDICT_REL, line)
    _commit(lane, "the verdict, committed before the call failed")
    plan = {"brief": "done-when", "verdict_path": lane / _VERDICT_REL, "route_id": "r"}
    ctx = SimpleNamespace(
        root=lane,
        worker={"adjudication_owed": ""},
        managed=False,
        run=SimpleNamespace(routing=None),
    )
    outcome, _errored = agent_loop.classify_outcome(
        "", timed_out, "RUNNING", True, {}, code
    )
    launched = SimpleNamespace(code=code, timed_out=timed_out, text="")
    plan["call_ok"] = agent_loop.session_service.call_succeeded(launched)
    agent_loop.session_bookkeeping(
        ctx, plan, outcome, code, ["c"], "HEAD", "", 0, "s", WI
    )
    text = (lane / ab.ksitting.requested_path(_VERDICT_REL)).read_text(encoding="utf-8")
    assert ab.ksitting.read_requested(text)[2] == "failed"
    assert _digest() not in kdone.covering(lane, "HEAD")
    assert _dispatch_hold(lane) is not None


_ERROR_RESULT = '{"type": "result", "is_error": true}'


def test_a_call_reporting_an_error_is_failed_on_both_routes(tmp_path, monkeypatch):
    """Sol final5 MAJOR 1: exit 0, a committed valid BLESSED verdict, and the
    CLI's result reporting `is_error`. `classify_outcome` shows COMMITTED, but
    the call failed: `session_service.call_succeeded`, the one derivation both
    routes share, reads the real signals, so both record FAILED."""
    from types import SimpleNamespace

    svc = agent_loop.session_service
    assert svc.call_succeeded(SimpleNamespace(code=0, timed_out=False, text=""))
    for code, timed_out, text in (
        (1, False, ""),
        (0, True, ""),
        (0, False, _ERROR_RESULT),
    ):
        failed = SimpleNamespace(code=code, timed_out=timed_out, text=text)
        assert not svc.call_succeeded(failed), (code, timed_out, text)
    # The loop, through session_bookkeeping as run_iteration calls it.
    _trunk_root, lane = _lane(tmp_path / "loop")
    line = "DONE-WHEN: BLESSED changes=2 digest={}\n".format(_digest())
    _write(lane, _VERDICT_REL, line)
    _commit(lane, "the verdict, committed by a call that then reported an error")
    plan = {"brief": "done-when", "verdict_path": lane / _VERDICT_REL, "route_id": "r"}
    ctx = SimpleNamespace(
        root=lane,
        worker={"adjudication_owed": ""},
        managed=False,
        run=SimpleNamespace(routing=None),
    )
    outcome, errored = agent_loop.classify_outcome(
        "", False, "RUNNING", True, {"type": "result", "is_error": True}, 0
    )
    assert (outcome, errored) == ("COMMITTED", True)
    launched = SimpleNamespace(code=0, timed_out=False, text=_ERROR_RESULT)
    plan["call_ok"] = svc.call_succeeded(launched)  # as run_iteration records it
    agent_loop.session_bookkeeping(ctx, plan, outcome, 0, ["c"], "HEAD", "", 0, "s", WI)
    text = (lane / ab.ksitting.requested_path(_VERDICT_REL)).read_text(encoding="utf-8")
    assert ab.ksitting.read_requested(text)[2] == "failed"
    assert _dispatch_hold(lane) is not None
    # The coordinator's entry point, the same call result.
    _trunk2, lane2 = _lane(tmp_path / "entry")
    returned, verdict = _entry_point_call(
        lane2, monkeypatch, 0, False, line, result=_ERROR_RESULT
    )
    binding = open(ab.ksitting.requested_path(verdict), encoding="utf-8").read()
    assert returned == 1 and ab.ksitting.read_requested(binding)[2] == "failed"
    assert _digest() not in kdone.covering(lane2, "HEAD")


def test_a_refused_reservation_leaves_a_binding_it_does_not_own(tmp_path):
    """Sol final5 MAJOR 2: a binding already sits beside an absent verdict
    path. The reservation succeeds, the exclusive binding creation refuses,
    and the cleanup removes only what THIS call created - its empty
    reservation - leaving the other binding untouched."""
    cli = load_script("coordinator_adjudicate")
    verdict = tmp_path / "reviews" / "001-ADJUDICATE-x.md"
    verdict.parent.mkdir(parents=True)
    binding = (
        tmp_path / "reviews" / ("001-ADJUDICATE-x.md" + ab.ksitting.REQUESTED_SUFFIX)
    )
    binding.write_text("brief = done-when\nkinds = done-when\n", encoding="utf-8")
    assert cli.reserve_verdict(verdict) is None
    assert cli.bind_requested(verdict, "done-when", "")
    cli._release(verdict, bound=False)
    assert not verdict.exists() and binding.exists()


def test_a_failed_call_is_recorded_failed_without_reading_its_verdict(
    tmp_path, monkeypatch
):
    """LLR-306's narration made true: on a failed call the route records
    FAILED and never reads the verdict the call left behind."""
    _trunk_root, lane = _lane(tmp_path)
    _write(lane, _VERDICT_REL, "DONE-WHEN: BLESSED changes=2 digest=x\n")
    _commit(lane, "the verdict")

    def never(*_a, **_k):
        raise AssertionError("a failed call's verdict was read")

    monkeypatch.setattr(ab, "verdict_refusal", never)
    monkeypatch.setattr(ab, "_read", never)
    outcome, why = ab.record_outcome(
        lane, lane / _VERDICT_REL, "done-when", ("done-when",), False, "s"
    )
    assert outcome == "failed" and "call failed" in why


def test_a_failed_loop_call_keeps_its_obligation_and_reads_no_verdict(
    tmp_path, monkeypatch
):
    """Sol final7 MAJOR 2: with the call failed, the session still committed
    a valid Done-when verdict. Completion uses the SAME decision the route
    records: the obligation stays owed (so the worker cannot finish DONE and
    the re-sit is not lost), the binding records failed, and the verdict the
    failed call left behind is never read."""
    _trunk_root, lane = _lane(tmp_path)
    line = "DONE-WHEN: BLESSED changes=2 digest={}\n".format(_digest())
    _write(lane, _VERDICT_REL, line)
    _commit(lane, "the verdict, committed before the call failed")

    def never(*_a, **_k):
        raise AssertionError("a failed call's verdict was read")

    monkeypatch.setattr(agent_loop.adjudicate_brief, "verdict_refusal", never)
    plan = {"brief": "done-when", "verdict_path": lane / _VERDICT_REL, "call_ok": False}
    worker = {"adjudication_owed": ""}
    agent_loop.adjudication_bookkeeping(plan, worker, None, False, None, 0, lane)
    assert worker["adjudication_owed"], "a failed call keeps its obligation"
    text = (lane / ab.ksitting.requested_path(_VERDICT_REL)).read_text(encoding="utf-8")
    assert ab.ksitting.read_requested(text)[2] == "failed"


def test_the_loop_route_accepts_a_combined_sitting_on_its_bound_kinds(
    tmp_path, monkeypatch
):
    """Sol final8 MAJOR 1: the loop composes a claimed `combined` row with
    requested kinds `amendment;done-when`. It binds those kinds beside the
    verdict at composition, as the coordinator's entry point does at
    reservation, and records the call against the SAME binding, so a valid
    combined verdict is accepted, clears the obligation and blesses."""
    _trunk_root, lane = _lane(tmp_path)
    _fake_spine_assemblers(monkeypatch)
    for kind in ("amendment", "first-approval"):  # the loop's own module copy
        loop_assemblers = agent_loop.adjudicate_brief._ASSEMBLERS
        monkeypatch.setitem(loop_assemblers, kind, ab._ASSEMBLERS[kind])
    assigned = _worker(lane)
    row = _row("combined", "amendment:LLR-1;done-when:" + WI)
    row["SafetyClass"] = "adjudication"
    assigned["rows"][WI] = row
    reviews = lane / "docs/reviews/wi-007"
    body, verdict, hold, brief = agent_loop.session_body(
        lane, assigned, WI, "001", "abcdef0", reviews, {}
    )
    assert hold is None and brief == "combined", (hold, brief)
    binding = ab.ksitting.requested_path(verdict)
    bound = ab.ksitting.read_requested(open(binding, encoding="utf-8").read())
    assert bound == ("combined", ("amendment", "done-when"), "pending")
    text = (
        "## amendment\n\n- [CLARITY] LLR-1 same\n\nVERDICT: CLARITY rows=1\n\n"
        "## done-when\n\nDONE-WHEN: BLESSED changes=2 digest={}\n\n"
        "SITTING: JUDGED kinds=amendment;done-when\n".format(_digest())
    )
    verdict.write_text(text, encoding="utf-8")
    _commit(lane, "the session's combined verdict")
    plan = {"brief": brief, "verdict_path": verdict, "call_ok": True}
    worker = {"adjudication_owed": ""}
    agent_loop.adjudication_bookkeeping(plan, worker, None, False, None, 0, lane)
    bound = ab.ksitting.read_requested(open(binding, encoding="utf-8").read())
    assert bound == ("combined", ("amendment", "done-when"), "accepted")
    assert worker["adjudication_owed"] == ""
    assert _digest() in kdone.covering(lane, "HEAD")


def test_a_build_after_a_dirty_completed_lane_is_held_at_dispatch(tmp_path):
    """Sol final9 MAJOR (a): a completed `WI:` trailer plus substantive
    uncommitted residue - `worker_endstate` defers (the dirty-tree arm) and
    routing selects a BUILD; the hold at the dispatch point holds it."""
    _trunk_root, lane = _lane(tmp_path)
    _write(lane, "src/work.py", "x = 1\n")
    _git(lane, "add", "-A")
    _git(lane, "commit", "-qm", "work\n\nWI: " + WI)
    _write(lane, "src/residue.py", "y = 2\n")
    worker = _worker(lane)
    assert agent_loop.worker_endstate(lane, worker, False, False, 0) is None
    held = _dispatch_hold(lane, worker=worker)
    assert held and held[:2] == (agent_loop.EXIT_NEEDS_HUMAN, "HELD")


def test_a_resumed_blocked_lanes_first_build_is_held_at_dispatch(tmp_path):
    """Sol final9 MAJOR (b): a resumed lane carrying a `Blocked-WI:` trailer
    is not short-circuited on its first iteration, so routing selects a BUILD;
    the hold at the dispatch point holds it."""
    _trunk_root, lane = _lane(tmp_path)
    _write(lane, "src/work.py", "x = 1\n")
    _git(lane, "add", "-A")
    _git(lane, "commit", "-qm", "blocked\n\nBlocked-WI: " + WI + "\nBlockRef: OI-1")
    worker = _worker(lane)
    end = agent_loop.worker_endstate(
        lane, worker, False, False, 0, allow_block_exit=False
    )
    assert end is None
    held = _dispatch_hold(lane, worker=worker)
    assert held and held[:2] == (agent_loop.EXIT_NEEDS_HUMAN, "HELD")


# --- round 19: machine lines are parsed strictly per physical line ----------

_COMPLETE = {
    "done-when": "DONE-WHEN: BLESSED changes=2 digest={}",
    "amendment": "VERDICT: CLARITY rows=1",
    "first-approval": "OUTCOME: APPROVE rows=1",
}


def _split_line(kind):
    """The complete machine line with its label carried onto the NEXT line."""
    keyword, rest = _COMPLETE[kind].format(_digest()).split(": ", 1)
    return "{}:\n{}\n".format(keyword, rest)


def _with_bare_extra(kind):
    """A complete machine line followed by a bare keyword line at EOF."""
    line = _COMPLETE[kind].format(_digest())
    return "{}\n{}:\n".format(line, line.split(":", 1)[0])


@pytest.mark.parametrize("kind", ("done-when", "amendment", "first-approval"))
@pytest.mark.parametrize("shape", (_split_line, _with_bare_extra))
def test_a_malformed_machine_line_invalidates_the_verdict(tmp_path, kind, shape):
    """Sol final10 MAJOR: a keyword whose label sits on the next line, or a
    bare second keyword line, makes the verdict invalid - single-kind and
    inside a combined sitting - because every physical line whose first token
    is a machine keyword counts, complete or not."""
    single = tmp_path / "single.md"
    single.write_text(shape(kind), encoding="utf-8")
    assert ab.verdict_refusal(kind, single), shape.__name__
    combined = tmp_path / "combined.md"
    other = "amendment" if kind != "amendment" else "first-approval"
    sections = {kind: shape(kind), other: _COMPLETE[other].format(_digest()) + "\n"}
    kinds = tuple(sorted(sections))
    combined.write_text(
        "".join("## {}\n\n{}\n".format(k, sections[k]) for k in kinds)
        + "SITTING: JUDGED kinds={}\n".format(";".join(kinds)),
        encoding="utf-8",
    )
    assert ab.verdict_refusal("combined", combined, kinds=kinds), shape.__name__


@pytest.mark.parametrize("shape", (_split_line, _with_bare_extra))
def test_a_malformed_done_when_line_releases_no_hold(tmp_path, shape):
    """The same shapes through the holds: recorded ACCEPTED is not enough -
    the one parser every reader uses rejects them, so nothing is covered."""
    _trunk_root, lane = _lane(tmp_path)
    _bless(lane, shape("done-when").rstrip("\n"))
    assert _digest() not in kdone.covering(lane, "HEAD")
    assert _dispatch_hold(lane) is not None


def test_a_machine_keyword_outside_every_section_invalidates_a_sitting(tmp_path):
    """A complete DONE-WHEN line placed before the first section heading is
    still a machine line of a requested kind: a second one invalidates."""
    path = tmp_path / "s.md"
    line = _COMPLETE["done-when"].format(_digest())
    path.write_text(
        "{0}\n\n## done-when\n\n{0}\n\nSITTING: JUDGED kinds=done-when\n".format(line),
        encoding="utf-8",
    )
    assert ab.verdict_refusal("combined", path, kinds=("done-when",))
