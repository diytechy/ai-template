"""The consolidation, driven END TO END on a real repository (the 2026-09-02
backlog-restructure plan §1, acceptance §4).

`tests/test_consolidate.py` pins the decision half — digests, clusters, guards,
the typed verdict block, the text transforms — with no repository at all. This
module pins the half that only a repository can answer: does the census MINT the
row, does the close ENACT the verdict, and does the queue end in the state the
plan describes?

THE SPINE OF IT, in one test: mint a `consolidate` row over a cluster of three
queued rows, render its brief, apply a `CONSOLIDATE absorbs=A;B;C` verdict
through the close and the merge, and assert the three rows landed in
`archive/work/restructured/` with the successor's `supersedes` naming them — and
that the census refuses a second consolidate while the first is pending.

WHERE THE TWO HALVES OF THE CLOSE LIVE, because the split is deliberate and a
reader will otherwise look for the archival in the wrong place.
`handback._consolidation_close` enacts everything that needs no id that does not
yet exist (the hard edge, the return to draft); the absorbed rows' move into
`restructured/` is `intake._archive_absorbed`, at the MINT, because their whole
Deliverable is `Restructured into WI-<successor>.` and that id is allocated by
`_mint` at the row's merge — and because `_supersedes_refusal` refuses a
`supersedes` naming an already-`restructured` row, so archiving earlier would
make the mint refuse its own successor.
"""

import subprocess

from conftest import env_gate_skipif, load_script, pin_autocrlf, skip_without_env_gates

pytestmark = env_gate_skipif("git")

hb = load_script("handback")
intake = load_script("intake")
consolidate = load_script("consolidate")
ab = load_script("adjudicate_brief")
acommon = load_script("agent_common")
integ = hb.integrate
trace = load_script("trace")

T_BASE = 1_000_000


def _git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def _commit(root, message, when=T_BASE):
    import os

    env = dict(os.environ)
    env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = "@{} +0000".format(when)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True, env=env)
    subprocess.run(
        ["git", "-C", str(root), "commit", "-qm", message], check=True, env=env
    )


def _spec(wid, title, specref="docs/plans/one.md", needs="[]", done="Ship the thing."):
    return (
        "+++\n"
        'id = "{}"\n'
        'title = "{}"\n'
        'workstream = "process"\n'
        "sr_refs = []\n"
        "needs = {}\n"
        'safety_class = "ordinary"\n'
        'buildtier = "medium"\n'
        'specref = "{}"\n'
        "+++\n"
        "\n## Context\n\nThe {} context.\n"
        "\n## Done-when\n\n1. {}\n"
    ).format(wid, title, needs, specref, wid, done)


def cluster_repo(tmp_path, extra_rows=()):
    """A trunk whose queue holds THREE rows commissioned by one plan (so the
    pre-filter clusters them) plus one unrelated row."""
    skip_without_env_gates("git")
    root = tmp_path / "repo"
    root.mkdir()
    _git(root.parent, "init", "-q", str(root))
    pin_autocrlf(root)
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    (root / ".gitignore").write_text("out/\n", encoding="utf-8", newline="\n")
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / trace.WATERMARK).write_text(
        trace.render_watermark(dict({s: 0 for s in trace.WATERMARK_SPACES}, WI=410)),
        encoding="utf-8",
        newline="\n",
    )
    (root / "docs" / "stack.ini").write_text(
        "[generated]\n", encoding="utf-8", newline="\n"
    )
    plans = root / "docs" / "plans"
    plans.mkdir(parents=True, exist_ok=True)
    (plans / "one.md").write_text("# one\n", encoding="utf-8", newline="\n")
    (plans / "other.md").write_text("# other\n", encoding="utf-8", newline="\n")
    queued = root / "docs" / "work" / "queued"
    queued.mkdir(parents=True, exist_ok=True)
    # The spec-of-record every minted consolidation points at (`consolidate.
    # SPECREF`): the queue IS its subject, so the forward bridge resolves to the
    # document defining what the queue's statuses mean. `integrate.claim`
    # refuses a SpecRef that does not resolve to an in-repo FILE (R-E), so the
    # fixture ships it exactly as `bootstrap.MAPPING` does.
    (queued.parent / "README.md").write_text(
        "# the work registry\n", encoding="utf-8", newline="\n"
    )
    for wid, title in (
        ("WI-401", "harden the widget"),
        ("WI-402", "test the widget"),
        ("WI-403", "document the widget"),
    ):
        (queued / "{}-{}.md".format(wid, wid.lower())).write_text(
            _spec(wid, title, done="Deliver {}.".format(wid)),
            encoding="utf-8",
            newline="\n",
        )
    (queued / "WI-409-elsewhere.md").write_text(
        _spec("WI-409", "something else", specref="docs/plans/other.md"),
        encoding="utf-8",
        newline="\n",
    )
    for name, text in extra_rows:
        (queued.parent / name).parent.mkdir(parents=True, exist_ok=True)
        (queued.parent / name).write_text(text, encoding="utf-8", newline="\n")
    _commit(root, "seed the queue")
    return root


def _rows(root):
    return {r["WI-ID"]: r for r in acommon.read_spec_rows(root / "docs" / "work")}


DISPOSITIONS = """
## Dispositions

```toml
title = "The widget, whole"
workstream = "process"
buildtier = "medium"
supersedes = ["WI-401", "WI-402", "WI-403"]
```

Scope: one row for the widget - hardening, tests and documentation together.
Deliberately excluded: the unrelated WI-409 scope.
"""

VERDICT = """
## Consolidation

```toml
outcome = "consolidate"
```
"""


def _record_verdict(root, branch, body):
    """What an ADJUDICATE session does on the lane: write its typed blocks into
    its OWN spec and commit with the result trailer."""
    wt, err = integ.lane_worktree(root, branch)
    assert err is None, err
    active = wt / "docs" / "work" / "active" / branch
    spec = sorted(active.glob("WI-*.md"))[0]
    spec.write_text(
        spec.read_text(encoding="utf-8") + body, encoding="utf-8", newline="\n"
    )
    _git(wt, "add", "-A")
    _git(wt, "commit", "--no-verify", "-m", "adjudicate: the verdict\n\nWI: recorded")
    return wt


def _merge(root, branch):
    _git(root, "merge", "--no-ff", "-q", "-m", "integrate: merge " + branch, branch)
    head = _git(root, "rev-parse", "HEAD").strip()
    return head


def test_the_census_mints_one_row_and_refuses_a_second_while_it_is_pending(tmp_path):
    """Plan §4's first two measurements, on a real tree: a queue with an
    overlapping cluster mints EXACTLY ONE `consolidate` row, and running the
    census again on that same queue mints nothing."""
    root = cluster_repo(tmp_path)
    minted, refusal = intake.mint_consolidation(root, busy=False)
    assert refusal is None, refusal
    assert len(minted) == 1, minted
    wid, rel = minted[0]
    row = _rows(root)[wid]
    assert row["SafetyClass"] == "adjudication"
    assert row["Brief"] == "consolidate"
    assert row["Priority"] == "9"
    assert sorted(row["Adjudicates"].split(";")) == ["WI-401", "WI-402", "WI-403"]
    assert "WI-409" not in row["Adjudicates"]
    assert consolidate.parse_digests(row["Digests"])[0]
    assert (root / rel).is_file()

    # ...and again on the same queue: nothing. Two guards would each stop it
    # here, so the reason is checked rather than only the count — a pending
    # judgement AND a queue state already judged.
    again, refusal = intake.mint_consolidation(root, busy=False)
    assert refusal is None and again == []
    draft, why = consolidate.census_draft(root)
    assert draft is None and "never stacks" in why


def test_the_brief_composes_from_the_minted_row(tmp_path):
    root = cluster_repo(tmp_path)
    minted, refusal = intake.mint_consolidation(root, busy=False)
    assert refusal is None, refusal
    row = _rows(root)[minted[0][0]]
    text, why = ab.compose(root, row, root / "docs" / "reviews" / "v.md")
    assert why is None, why
    for wid in ("WI-401", "WI-402", "WI-403"):
        assert wid in text
    assert "- WI-409" in text  # the other open rows, as evidence
    assert ab.NO_SPINE in text  # the cluster cites no SR: STATED, never blank
    assert "CONSOLIDATE" in text


def test_a_consolidate_verdict_absorbs_its_cluster_end_to_end(tmp_path):
    """THE WHOLE ARC. Mint over three queued rows, claim, record a CONSOLIDATE
    verdict, close, merge, mint — then assert the queue ended where the plan
    says: three rows in `restructured/` naming the successor, one successor
    superseding all three, and the census silent afterwards."""
    root = cluster_repo(tmp_path)
    minted, refusal = intake.mint_consolidation(root, busy=False)
    assert refusal is None, refusal
    judge_id = minted[0][0]
    branch = judge_id.lower()
    assert integ.claim(root, judge_id, branch) == 0
    _record_verdict(root, branch, DISPOSITIONS + VERDICT)

    ids, refusal = hb.close_adjudication(root, branch)
    assert refusal is None, refusal
    assert ids == [judge_id]
    before = _git(root, "rev-parse", "HEAD").strip()
    after = _merge(root, branch)
    successors, refusal = intake.intake_after_merge(
        root, before, after, {judge_id: "merged"}, branch
    )
    assert refusal is None, refusal
    assert len(successors) == 1, successors
    successor = successors[0][0]

    rows = _rows(root)
    # 1. Every absorbed row is TERMINAL, in the fourth terminal folder, with the
    #    one-line Deliverable naming the successor and its scope text intact.
    for wid in ("WI-401", "WI-402", "WI-403"):
        assert rows[wid]["Status"] == "restructured", wid
        spec = root / "docs" / "archive" / "work" / "restructured"
        hit = sorted(spec.glob(wid + "-*.md"))
        assert hit, wid
        text = hit[0].read_text(encoding="utf-8")
        assert "Restructured into {}.".format(successor) in text
        assert "The {} context.".format(wid) in text  # scope text untouched
        assert 'specref = "docs/plans/one.md"' in text  # kept, like `partial`
        assert rows[wid]["Deliverable"] == "Restructured into {}.".format(successor)
    # 2. The successor names all three, in ONE list-valued cell.
    assert sorted(rows[successor]["Supersedes"].split(";")) == [
        "WI-401",
        "WI-402",
        "WI-403",
    ]
    # 3. Its Context carries the verdict's scope prose verbatim.
    body = (root / "docs" / "work" / "queued").glob(successor + "-*.md")
    text = sorted(body)[0].read_text(encoding="utf-8")
    assert "one row for the widget" in text.lower()
    # 4. The unrelated row is untouched.
    assert rows["WI-409"]["Status"] == "queued"
    # 5. The census is silent afterwards: the queue changed, but the only
    #    overlap left involves the consolidation's OWN successor (plan §4).
    draft, why = consolidate.census_draft(root)
    assert draft is None, draft
    assert "nothing to consolidate" in why


def test_the_close_refuses_by_name_when_an_absorbed_row_was_claimed(tmp_path):
    """The census guard makes this a race only a hand claim can produce (plan
    §1.5) — and when it happens the close refuses rather than archiving a row a
    lane is building."""
    root = cluster_repo(tmp_path)
    minted, _ = intake.mint_consolidation(root, busy=False)
    judge_id = minted[0][0]
    branch = judge_id.lower()
    assert integ.claim(root, judge_id, branch) == 0
    assert integ.claim(root, "WI-402", "wi-402") == 0
    _record_verdict(root, branch, DISPOSITIONS + VERDICT)
    ids, refusal = hb.close_adjudication(root, branch)
    assert ids is None
    assert refusal and "WI-402" in refusal and "no longer queued" in refusal


def test_queue_with_edge_writes_the_hard_needs_edge(tmp_path):
    """The reader the retired conflict brief promised and never got."""
    root = cluster_repo(tmp_path)
    minted, _ = intake.mint_consolidation(root, busy=False)
    judge_id = minted[0][0]
    branch = judge_id.lower()
    assert integ.claim(root, judge_id, branch) == 0
    _record_verdict(
        root,
        branch,
        '\n## Consolidation\n\n```toml\noutcome = "queue-with-edge"\n'
        'edges = ["WI-402 needs WI-401"]\n```\n',
    )
    ids, refusal = hb.close_adjudication(root, branch)
    assert refusal is None, refusal
    assert ids == [judge_id]
    _merge(root, branch)
    rows = _rows(root)
    assert rows["WI-402"]["Predecessors"] == "WI-401"
    assert rows["WI-401"]["Predecessors"] == ""
    assert rows["WI-402"]["Status"] == "queued"  # queued, not absorbed


def test_return_to_draft_moves_the_row_back_with_the_finding_quoted(tmp_path):
    root = cluster_repo(tmp_path)
    minted, _ = intake.mint_consolidation(root, busy=False)
    judge_id = minted[0][0]
    branch = judge_id.lower()
    assert integ.claim(root, judge_id, branch) == 0
    _record_verdict(
        root,
        branch,
        '\n## Consolidation\n\n```toml\noutcome = "return-to-draft"\n'
        'returns = ["WI-403"]\n'
        'finding = "WI-403 re-proposes what WI-390 already refuted."\n```\n',
    )
    ids, refusal = hb.close_adjudication(root, branch)
    assert refusal is None, refusal
    _merge(root, branch)
    rows = _rows(root)
    assert rows["WI-403"]["Status"] == "draft"
    spec = sorted((root / "docs" / "work" / "draft").glob("WI-403-*.md"))[0]
    text = spec.read_text(encoding="utf-8")
    assert "> WI-403 re-proposes what WI-390 already refuted." in text
    assert "The WI-403 context." in text  # its own scope survives the return
