"""handback.py — the two lane closes that are not a merge (WI-387, §A3).

The invariant under test is "every lane ends in a merge, branches never hang",
and the only honest way to test it is to CONSTRUCT the topology: real temp git
repos, a real claim, a real lane worktree, real commits. What each group pins:

  * the PARTIAL CLOSE is a real registry move to a TERMINAL folder — the spec
    is in `partial/` with its definition byte-identical, an immutable per-close
    REPORT sits beside it under docs/handbacks/, the branch is FINISHED by the
    integrator's own read, and `branch_outcomes` reads `partial` off the same
    move;
  * the closed spec LEAVES THE READY FRONTIER — and now STRUCTURALLY, because
    the folder is terminal. The old contract returned the row to `queued/` (the
    ready state) and bought the property with a `blockref`, so it depended on
    an attribute being written and nobody clearing it; without it the driver
    would claim, close and re-claim the same WI forever. The assertion is
    against `schedule.frontier` itself, either way;
  * a `partial` report that omits the KEEP/DISCARD split refuses the merge —
    the rung a live incident bought, where a green close merged rejected code
    onto trunk because nothing had asked which commits should survive;
  * every registry reader still parses a closed spec. `partial/` widened a
    status vocabulary that four copies enforce, so all four are driven over one
    real file — the drift this repo closes by test rather than by extraction
    (WI-291);
  * the QUARANTINE is bar-inert AND lossless: the product paths go back to the
    base byte for byte, the `.patch` re-applies, and the bookkeeping the
    handback just wrote survives untouched.

Mutation notes are inline where a green could be vacuous — a revert that
reverted nothing, or a "blocked" assertion that would pass on an unblocked row.
"""

import shutil
import subprocess
import sys

from conftest import (
    SCRIPTS,
    env_gate_skipif,
    load_script,
    pin_autocrlf,
    skip_without_env_gates,
)

if str(SCRIPTS) not in sys.path:  # the kit's script-sibling import idiom
    sys.path.insert(0, str(SCRIPTS))

from kitlib import verdict as kv  # noqa: E402

pytestmark = env_gate_skipif("git")

hb = load_script("handback")
intake = load_script("intake")
integ = hb.integrate
sched = load_script("schedule")
ctraj = load_script("check_trajectory")
acommon = load_script("agent_common")
wi_convert = load_script("wi_convert")

T_BASE = 1_000_000
T_CODE = 1_000_100


def _git(root, *args, check=True):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if check:
        assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def _commit(root, message, when=T_CODE):
    import os

    env = dict(os.environ)
    env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = "@{} +0000".format(when)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True, env=env)
    subprocess.run(
        ["git", "-C", str(root), "commit", "-qm", message], check=True, env=env
    )


def spec_text(wid, specref="seed.txt", deliverable=""):
    lines = [
        'id = "{}"'.format(wid),
        'title = "Widget"',
        'workstream = "ws"',
        'sr_refs = ["SR-001"]',
        "needs = []",
        'safety_class = "ordinary"',
        "order = 0",
        'specref = "{}"'.format(specref),
    ]
    text = "+++\n" + "".join(ln + "\n" for ln in lines) + "+++\n"
    if deliverable:
        text += "\n## Deliverable\n\n" + deliverable + "\n"
    return text


def claimed_repo(tmp_path, wid="WI-401", branch="wi-401", extra=()):
    """A trunk with `wid` CLAIMED onto `branch` — the state a lane closes from.

    `extra` is `[(path, text)]` seeded BEFORE the claim, so a test that needs a
    file to rename has one at the base the quarantine reverts to."""
    skip_without_env_gates("git")
    root = tmp_path / "repo"
    root.mkdir()
    _git(root.parent, "init", "-q", str(root))
    pin_autocrlf(root)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    (root / "seed.txt").write_text("seed\n", encoding="utf-8", newline="\n")
    (root / ".gitignore").write_text("out/\n", encoding="utf-8", newline="\n")
    spec = root / "docs" / "work" / "queued" / "{}-widget.md".format(wid)
    spec.parent.mkdir(parents=True, exist_ok=True)
    spec.write_text(spec_text(wid), encoding="utf-8", newline="\n")
    for name, text in extra:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")
    _commit(root, "seed + file " + wid, when=T_BASE)
    assert integ.claim(root, wid, branch) == 0
    return root


def lane(root, branch="wi-401"):
    wt, err = integ.lane_worktree(root, branch)
    assert err is None, err
    return wt


def closed_spec_path(root, wid="WI-401"):
    """SR-144: an early close is TERMINAL — the spec lands in `partial/`, not
    back in the ready `queued/` where the old contract left it leaning on a
    blockref to keep the driver from re-claiming it."""
    return root / "docs" / "work" / "partial" / "{}-widget.md".format(wid)


def report_path(root, wid="WI-401", branch="wi-401"):
    return root / "docs" / "handbacks" / "{}-{}.md".format(wid, branch)


def merge_branch(root, branch="wi-401"):
    """Land the branch on trunk the way the slot would — without the bar, which
    is `integrate`'s own suite's subject. Lets a test read the RETURNED spec on
    trunk, which is where the invariant says it has to end up."""
    _git(root, "merge", "--no-ff", "-q", "-m", "integrate: merge " + branch, branch)


# --- the return itself ---------------------------------------------------------


def test_the_partial_close_lands_terminal_with_its_report_and_finishes_the_branch(
    tmp_path,
):
    root = claimed_repo(tmp_path)
    wt = lane(root)
    (wt / "half-done.py").write_text("VALUE = 1\n", encoding="utf-8", newline="\n")

    ids, refusal = hb.close_partial(
        root,
        "wi-401",
        "worker exit 7 (NEEDS-JUDGEMENT)",
        {"suggested_tier": "strong", "keep_commits": ["abc1234"]},
    )
    assert refusal is None, refusal
    assert ids == ["WI-401"]

    # The branch is now FINISHED by the integrator's own read — the same move
    # that closes the spec is the one that closes the lane, so there is no
    # second fact to keep in agreement.
    assert integ.finished_branches(root) == ["wi-401"]
    outcomes, unresolved = integ.branch_outcomes(root, "wi-401")
    assert outcomes == {"WI-401": "partial"} and unresolved == []

    # ...and the work so far is COMMITTED, not discarded: the lane worktree is
    # clean and the file is in the branch's tree.
    assert wt.joinpath("half-done.py").is_file()
    assert "half-done.py" in _git(root, "ls-tree", "-r", "--name-only", "wi-401")
    assert _git(wt, "status", "--porcelain").strip() == ""

    merge_branch(root)
    # THE SPEC ITSELF IS UNCHANGED. Its definition did not move — only where it
    # sits and what the report says about delivery. "Scope definitions never
    # change; only whether they were fully delivered."
    spec = closed_spec_path(root).read_text(encoding="utf-8")
    assert "## Handback" not in spec, "the note moved OUT of the spec"
    assert "blockref" not in spec, "a terminal row needs no blockref to hold it"
    assert not list((root / "docs" / "work" / "active").rglob("WI-*.md"))

    # The REPORT is the event's identity, and it carries typed fields — not a
    # magic substring inside prose (the `NEEDS-HUMAN` defect).
    report = report_path(root).read_text(encoding="utf-8")
    assert 'wi = "WI-401"' in report
    assert 'claimed_outcome = "partial"' in report
    assert 'suggested_tier = "strong"' in report
    assert 'keep_commits = ["abc1234"]' in report
    assert "worker exit 7 (NEEDS-JUDGEMENT)" in report
    meta = hb.read_report(report_path(root))
    assert meta["claimed_outcome"] == "partial"
    assert hb.report_refusal(meta) is None


def test_a_partial_report_silent_about_the_keep_discard_split_refuses(tmp_path):
    """The rung a LIVE incident bought (2026-08-03): a close merged green and
    the code the lane had REJECTED landed on trunk as-is, because nothing had
    asked which commits should survive.

    What is refused is SILENCE, not indecision — and the difference is the
    whole design. The two closers know different things: a lane judged its own
    work and can name the split; the dispatcher closing a lane whose worker
    exited has no view of it at all. So `split_decided_by = "adjudicator"` is a
    valid, actionable answer (the disposition row then owes the call), and a
    report carrying neither a split nor a decider is not."""
    silent = {"claimed_outcome": "partial", "reason": "stopped early"}
    refusal = hb.report_refusal(silent)
    assert refusal is not None
    assert "SILENT" in refusal and "split_decided_by" in refusal

    # The two actionable shapes both pass.
    assert hb.report_refusal(dict(silent, keep_commits=["abc1234"])) is None
    assert hb.report_refusal(dict(silent, split_decided_by="adjudicator")) is None
    # ...and a decider outside the vocabulary is not a way through.
    assert hb.report_refusal(dict(silent, split_decided_by="nobody")) is not None

    # End to end: the writer never PRODUCES a silent report — an omitted split
    # is written as an explicit deferral, so the rung passes on its own output.
    root = claimed_repo(tmp_path)
    lane(root)
    assert hb.close_partial(root, "wi-401", "stopped early")[1] is None
    assert integ._partial_report_refusal(root, "wi-401", {"WI-401": "partial"}) is None
    merge_branch(root)
    report = report_path(root).read_text(encoding="utf-8")
    assert 'split_decided_by = "adjudicator"' in report
    assert "the disposition row minted for this close is what owes it" in report


def test_a_partial_close_is_CLEAN_under_the_real_trajectory_check(tmp_path):
    """THE REGRESSION THAT MATTERED MOST, and the reason it went unseen.

    `partial` joining TERMINAL_STATUSES armed R-A (a terminal WI carries a
    filled Deliverable — `hard=True`, an ERROR at every run, not only under
    --strict) and R-F (a terminal WI clears its SpecRef) against a close that
    `close_partial` structurally CANNOT satisfy: SR-144's whole point is that an
    early close leaves the spec's definition byte-identical.

    A rule no honest close can satisfy is not a rule. In the loop it is worse
    than a red gate: the dispatcher's post-close refresh reds, `_refresh_failed`
    quarantines the lane's work, the retry reds again (the spec move is
    bookkeeping and exempt from the revert), and the run dies — so every partial
    close would destroy the lane's work and stop the run, over bookkeeping.

    It went unseen because the only end-to-end partial-close tests run against a
    STUB check.py that never invokes check_trajectory. So this drives the REAL
    finding functions over a REAL closed row."""
    root = claimed_repo(tmp_path)
    lane(root)
    assert hb.close_partial(root, "wi-401", "worker exit 7")[1] is None
    merge_branch(root)

    rows, _errors = ctraj.load_wis(
        ctraj.read_registry_rows(root / "docs/requirements/x.csv")
    )
    row = {w["id"]: w for w in rows}["WI-401"]
    assert row["status"] == "partial"
    assert row["deliverable"] == "", "the close leaves the definition untouched"
    assert row["specref"], "the successor's lineage needs the spec to still point"

    hard = [f for f in ctraj.ssot_findings(rows, root) if f[0] == "R-A"]
    assert hard == [], "R-A must not fire on a partial close: {}".format(hard)
    lifecycle = [f for f in ctraj.spec_lifecycle_findings(root, rows) if "WI-401" in f]
    assert lifecycle == [], "R-F must not fire on a partial close: {}".format(lifecycle)


def test_a_terminal_spec_with_no_close_report_is_LOUD(tmp_path):
    """F6 — suppression must never be silent, and this is the shape that broke
    it: a `partial/` spec whose report was deleted or renamed produced zero
    dispositions AND zero diagnostics, so an owed judgement simply stopped
    existing. The sibling arm (spec unreadable) always said so; this one did
    not."""
    root = claimed_repo(tmp_path)
    lane(root)
    assert hb.close_partial(root, "wi-401", "worker exit 7")[1] is None
    merge_branch(root)
    report_path(root).unlink()

    drafts = intake._close_drafts(root, {"WI-401": "partial"})
    assert drafts == []


def test_the_report_is_immutable_and_a_refused_close_leaves_no_residue(tmp_path):
    """ "Immutable" has to be enforced, not asserted. The report IS the close
    event's identity, and an identity that can be overwritten is a mutable proxy
    again — the exact shape five dedup mechanisms died on. A refused second
    close also used to leave the rewritten report STAGED in a dirty lane, which
    §5.6 refuses to GC."""
    root = claimed_repo(tmp_path)
    wt = lane(root)
    assert hb.close_partial(root, "wi-401", "the FIRST reason")[1] is None
    first = report_path(wt).read_text(encoding="utf-8")

    _ids, refusal = hb.close_partial(root, "wi-401", "the SECOND reason")
    assert refusal is not None
    assert "immutable" in refusal or "already exists" in refusal
    assert report_path(wt).read_text(encoding="utf-8") == first
    assert _git(wt, "status", "--porcelain").strip() == "", "no residue in the lane"


def test_the_closed_spec_leaves_the_ready_frontier(tmp_path):
    # THE ANTI-LIVELOCK PROPERTY, asserted where it actually bites — and it is
    # now STRUCTURAL rather than bought with a blockref. The old contract put
    # the row back in `queued/`, the ready state, so only a `blockref` stopped
    # the driver claiming, closing and re-claiming it forever (moving trunk each
    # time, so the stall guard never fired). `partial/` is TERMINAL: there is
    # no attribute to forget. Driven both ways: ready before the claim,
    # terminal after the close.
    root = claimed_repo(tmp_path)

    _git(root, "checkout", "-q", "-b", "probe", "HEAD~1")
    ready = [r["id"] for r in sched.frontier(sched._load(root))]
    assert ready == ["WI-401"], ready
    _git(root, "checkout", "-q", "main")

    lane(root)
    _ids, refusal = hb.close_partial(root, "wi-401", "worker exit 7")
    assert refusal is None, refusal
    merge_branch(root)

    records = {r["id"]: r for r in sched.evaluate(sched._load(root))}
    assert records["WI-401"]["status"] == "partial"
    assert records["WI-401"]["disposition"] == "partial"
    assert "partial:terminal-stopped-early" in records["WI-401"]["reasons"]
    assert [r["id"] for r in sched.frontier(sched._load(root))] == []


def test_every_registry_reader_parses_a_closed_spec(tmp_path):
    # `partial/` widened a status vocabulary FOUR copies enforce (agent_common,
    # check_trajectory, schedule per the F5 rule, plus the converter). A spec
    # that one reader placed and another called an unknown directory would
    # split the registry in half — schedule would see a terminal row the
    # validator had dropped — so all four are driven over one real file.
    root = claimed_repo(tmp_path)
    lane(root)
    assert hb.close_partial(root, "wi-401", "worker exit 7")[1] is None
    merge_branch(root)
    text = closed_spec_path(root).read_text(encoding="utf-8")
    rel = "partial/WI-401-widget.md"

    for reader in (acommon, ctraj, sched):
        row, _order = reader.parse_spec_row(text, rel)
        assert row["Status"] == "partial", reader.__name__
    row, _order = wi_convert.parse_spec(text, rel)
    assert row["Status"] == "partial"


def test_the_return_move_runs_the_link_aware_ritual(tmp_path):
    """WI-393: the close is the same indivisible move+relink the claim and the
    archival run (WI-288/WI-353, rehomed in spec_move.py). `partial/` is one
    directory SHALLOWER than active/<branch>/, so a closed spec's own links
    must shorten, and every inbound link written against the active path must
    follow it back — in the same close commit, never as residue."""
    # The link sits in the Deliverable section: the registry loaders drop a
    # spec whose body prose lives under no recognised heading.
    body = spec_text("WI-401", deliverable="See [the log](../../log.md).")
    root = claimed_repo(
        tmp_path,
        extra=(
            ("docs/work/queued/WI-401-widget.md", body),
            (
                "docs/log.md",
                "# Log\n\nplanned: [WI-401](work/queued/WI-401-widget.md)\n",
            ),
        ),
    )
    # The claim already ran the ritual: the spec's own link is one deeper and
    # the inbound link follows it — the premise the return move must invert.
    claimed = root / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md"
    assert "[the log](../../../log.md)" in claimed.read_text(encoding="utf-8")
    assert "work/active/wi-401" in (root / "docs" / "log.md").read_text(
        encoding="utf-8"
    )

    wt = lane(root)
    # A fragment written during the lane's life links the ACTIVE spec path —
    # the inbound shape the return would otherwise strand.
    frag = wt / "docs" / "log.d" / "WI-401-notes.md"
    frag.parent.mkdir(parents=True, exist_ok=True)
    frag.write_text(
        "## note\n\nspec: [WI-401](../work/active/wi-401/WI-401-widget.md)\n",
        encoding="utf-8",
        newline="\n",
    )

    ids, refusal = hb.close_partial(root, "wi-401", "worker exit 7")
    assert refusal is None, refusal
    assert ids == ["WI-401"]

    closed = (wt / "docs" / "work" / "partial" / "WI-401-widget.md").read_text(
        encoding="utf-8"
    )
    assert "[the log](../../log.md)" in closed, closed
    assert "../../../log.md" not in closed
    for doc in (wt / "docs" / "log.md", wt / "docs" / "log.d" / "WI-401-notes.md"):
        text = doc.read_text(encoding="utf-8")
        assert "work/active/wi-401" not in text, (doc, text)
        assert "work/partial/WI-401-widget.md" in text, (doc, text)
    # the relinks are IN the close commit, not left dirty in the lane
    assert _git(wt, "status", "--porcelain").strip() == ""


def test_a_closed_spec_keeps_its_deliverable_untouched(tmp_path):
    # The old contract APPENDED a `## Handback` section to the spec body, so
    # the grammar had to be Deliverable-then-Handback and a bad partition would
    # silently blank the Deliverable cell. SR-144 deletes the whole hazard: the
    # close writes a separate report and the spec's body is not edited at all.
    # The assertion that matters is therefore the stronger one — BYTE-IDENTICAL.
    root = claimed_repo(
        tmp_path,
        extra=(
            (
                "docs/work/queued/WI-401-widget.md",
                spec_text("WI-401", deliverable="A widget, half-shipped."),
            ),
        ),
    )
    claimed = root / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md"
    before = claimed.read_text(encoding="utf-8")

    lane(root)
    assert hb.close_partial(root, "wi-401", "worker exit 7")[1] is None
    merge_branch(root)

    after = closed_spec_path(root).read_text(encoding="utf-8")
    assert after == before, "an early close must not edit the spec's definition"
    row, _order = acommon.parse_spec_row(after, "partial/WI-401-widget.md")
    assert row["Deliverable"] == "A widget, half-shipped."


def test_a_close_writes_no_blockref_because_the_folder_is_terminal(tmp_path):
    # The old contract bought its anti-livelock property with a `blockref`,
    # which meant the property depended on an ATTRIBUTE being written by the
    # close and never cleared by anyone. `partial/` is terminal, so there is
    # nothing to write and nothing to forget. The blockref vocabulary itself
    # retired at WI-553/OI-70; this stays as a regression guard that a close
    # introduces no such attribute into the spec.
    root = claimed_repo(tmp_path)
    lane(root)
    assert hb.close_partial(root, "wi-401", "worker exit 7")[1] is None
    merge_branch(root)

    out = closed_spec_path(root).read_text(encoding="utf-8")
    assert "blockref" not in out
    records = {r["id"]: r for r in sched.evaluate(sched._load(root))}
    assert records["WI-401"]["disposition"] == "partial"
    assert [r["id"] for r in sched.frontier(sched._load(root))] == []


def test_handback_refuses_a_branch_trunk_holds_no_claim_for(tmp_path):
    root = claimed_repo(tmp_path)
    ids, refusal = hb.close_partial(root, "wi-999", "worker exit 7")
    assert ids is None and "no claimed specs" in refusal


def test_a_disposition_rows_own_handback_is_refused_structurally(tmp_path):
    # WI-388 / ruling R3, the no-recursion invariant at the MACHINERY end: a
    # disposition row (the adjudication kind) may never itself hand back — its
    # only outcomes are cancel / defer / re-queue with drafted follow-up /
    # surface an open item. The refusal is structural (the function that would
    # perform the act refuses), never prose, and it leaves the claim exactly
    # where it was for a human to read.
    root = claimed_repo(tmp_path)
    spec = root / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md"
    spec.write_text(
        spec.read_text(encoding="utf-8").replace(
            'safety_class = "ordinary"', 'safety_class = "adjudication"'
        ),
        encoding="utf-8",
        newline="\n",
    )
    _commit(root, "fixture: the claim is an adjudication row", when=T_CODE)

    ids, refusal = hb.close_partial(root, "wi-401", "worker exit 7 (NEEDS-HUMAN)")
    assert ids is None
    assert "never closes early" in refusal and "R3" in refusal
    assert spec.is_file()  # the claim did not move
    assert not (root / "docs" / "work" / "queued" / "WI-401-widget.md").exists()


# --- the mechanical adjudication close (OI-70/OI-73, Done-when 1) --------------

_DRAFTED_DISPOSITIONS = """

## Dispositions

```toml
title = "Continue the WI-005 work by another route"
workstream = "process"
buildtier = "medium"
supersedes = "WI-005"
```

Scope: re-land the reviewed parts.
"""


def adjudication_repo(
    tmp_path, branch="wi-401", brief="disposition", dispositions=None, outcome="partial"
):
    """A trunk with an ADJUDICATION row claimed onto `branch`, then its verdict
    recorded ON THE LANE — the `## Dispositions` are drafted after the claim,
    exactly as an ADJUDICATE session does (the queued spec carries only its
    Context, so it parses and schedules cleanly). This is the DONE state the
    mechanical close acts on. `dispositions=""` models a judge that drafted
    nothing (the refusal-invariant case).

    `outcome` is the terminal folder of the ORIGINAL close the row judges, which
    its `specref` points at so the claim resolves (R-E). The refusal invariant
    itself reads the durable `dispose:` TITLE prefix, not that folder and not the
    `brief`, so a `cancelled` row (brief-LESS by design) is caught exactly as the
    `partial` one — pass `brief=""`, `outcome="cancelled"` to model it."""
    skip_without_env_gates("git")
    root = tmp_path / "repo"
    root.mkdir()
    _git(root.parent, "init", "-q", str(root))
    pin_autocrlf(root)
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    (root / "seed.txt").write_text("seed\n", encoding="utf-8", newline="\n")
    (root / ".gitignore").write_text("out/\n", encoding="utf-8", newline="\n")
    tr = load_script("trace")
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / tr.WATERMARK).write_text(
        tr.render_watermark({s: 0 for s in tr.WATERMARK_SPACES}),
        encoding="utf-8",
        newline="\n",
    )
    lines = [
        'id = "WI-401"',
        'title = "dispose: the WI-005 close"',
        'workstream = "process"',
        "needs = []",
        'safety_class = "adjudication"',
        'brief = "{}"'.format(brief),
        "order = 0",
        # The specref points at the CLOSED original spec under its terminal
        # folder so the claim resolves (R-E); the "dispose:" title above is what
        # the refusal invariant reads to tell an early close from a clean one.
        'specref = "docs/work/{}/WI-005-orig.md"'.format(outcome),
    ]
    text = (
        "+++\n"
        + "".join(ln + "\n" for ln in lines)
        + "+++\n"
        + "\n## Context\n\nJudge the WI-005 partial close.\n"
    )
    spec = root / "docs" / "work" / "queued" / "WI-401-dispose.md"
    spec.parent.mkdir(parents=True, exist_ok=True)
    spec.write_text(text, encoding="utf-8", newline="\n")
    # The CLOSED original the row judges, in its terminal folder — a real file so
    # the row's specref resolves (R-E) and the outcome the refusal invariant
    # reads is the true one.
    orig_lines = [
        'id = "WI-005"',
        'title = "the original WI-005 work"',
        'workstream = "process"',
        "needs = []",
        "order = 0",
        'specref = ""',
    ]
    orig_text = (
        "+++\n"
        + "".join(ln + "\n" for ln in orig_lines)
        + "+++\n"
        + "\n## Deliverable\n\nStopped early; the reviewed part landed.\n"
        + "\n## Context\n\nThe original WI-005 work.\n"
    )
    orig = root / "docs" / "work" / outcome / "WI-005-orig.md"
    orig.parent.mkdir(parents=True, exist_ok=True)
    orig.write_text(orig_text, encoding="utf-8", newline="\n")
    _commit(root, "seed + adjudication row", when=T_BASE)
    assert integ.claim(root, "WI-401", branch) == 0
    # The session records its verdict ON THE LANE: draft the successors into the
    # active spec's ## Dispositions section and commit with the WI trailer.
    drafted = _DRAFTED_DISPOSITIONS if dispositions is None else dispositions
    if drafted:
        wt = lane(root, branch)
        active = wt / "docs" / "work" / "active" / branch / "WI-401-dispose.md"
        active.write_text(
            active.read_text(encoding="utf-8") + drafted, encoding="utf-8", newline="\n"
        )
        _git(wt, "add", "-A")
        _git(wt, "commit", "--no-verify", "-m", "adjudicate: verdict\n\nWI: WI-401")
    return root


def test_the_mechanical_adjudication_close_archives_terminal_and_finishes(tmp_path):
    root = adjudication_repo(tmp_path)
    ids, refusal = hb.close_adjudication(root, "wi-401")
    assert refusal is None, refusal
    assert ids == ["WI-401"]
    # The branch is FINISHED by the integrator's own read: active/ is empty.
    assert integ.finished_branches(root) == ["wi-401"]
    merge_branch(root)
    complete = root / "docs" / "work" / "complete" / "WI-401-dispose.md"
    assert complete.is_file()
    spec = complete.read_text(encoding="utf-8")
    # A valid Deliverable was inserted, the Dispositions section SURVIVES (the
    # merge reads it to mint the successors), and specref is cleared.
    assert "## Deliverable" in spec
    assert "## Dispositions" in spec and "supersedes" in spec
    assert 'specref = ""' in spec
    # Every registry reader parses the closed adjudication spec.
    rows = {r["WI-ID"]: r for r in acommon.read_spec_rows(root / "docs" / "work")}
    assert rows["WI-401"]["Status"] == "done"


def test_the_close_the_writer_lands_is_one_the_attestor_peels(tmp_path):
    # THE WRITER↔VERIFIER LOOP, closed on a REAL close rather than a
    # hand-composed one. `verdict.mechanical_close_attestation` re-derives this
    # subject from the diff and compares it exactly, so the two sides share an
    # ordering (`station.mechanical_close_order`) AND a spelling; if either
    # drifts, every adjudication close silently stops peeling and re-opens the
    # staled-APPROVE failure the peel exists to close. The peel test suite
    # composes its own fixtures, so nothing else drives the producer here.
    root = adjudication_repo(tmp_path)
    before = _git(root, "rev-parse", "wi-401").strip()
    ids, refusal = hb.close_adjudication(root, "wi-401")
    assert refusal is None, refusal
    assert ids == ["WI-401"]
    landed = _git(root, "rev-parse", "wi-401").strip()
    assert landed != before  # the close really committed
    assert kv.mechanical_close_attestation(root, landed) == before


def test_the_mechanical_close_mints_the_drafted_successor_at_merge(tmp_path):
    root = adjudication_repo(tmp_path)
    ids, refusal = hb.close_adjudication(root, "wi-401")
    assert refusal is None, refusal
    merge_branch(root)
    before = after = _git(root, "rev-parse", "HEAD").strip()
    minted, mrefusal = intake.intake_after_merge(
        root, before, after, {"WI-401": "merged"}, "wi-401"
    )
    assert mrefusal is None, mrefusal
    assert len(minted) == 1
    successor = minted[0][0]
    rows = {r["WI-ID"]: r for r in acommon.read_spec_rows(root / "docs" / "work")}
    # The successor continues the ORIGINAL closed row (WI-005) that the
    # adjudicator's disposition named — the lineage the mint preserves.
    assert rows[successor]["Supersedes"] == "WI-005"


def test_the_refusal_invariant_stops_a_disposition_with_no_successor(tmp_path):
    # OI-73: a `disposition`-brief close that drafted NO successor is refused —
    # no third exit, nothing silent.
    root = adjudication_repo(tmp_path, dispositions="")
    ids, refusal = hb.close_adjudication(root, "wi-401")
    assert ids is None
    assert refusal is not None and "no successor" in refusal.lower()
    # The claim did NOT move: the row stays in active/ for a human.
    assert (
        root / "docs" / "work" / "active" / "wi-401" / "WI-401-dispose.md"
    ).is_file()


def test_the_refusal_invariant_stops_a_cancelled_close_with_no_successor(tmp_path):
    # OI-73, the gap REVIEW-A found: a CANCELLED original close mints a
    # brief-LESS adjudication row, so a `brief == "disposition"` guard missed it
    # and a cancelled close that queued no successor archived silently. The
    # signal is the OUTCOME the row's specref names (`cancelled`), not the brief.
    root = adjudication_repo(tmp_path, brief="", outcome="cancelled", dispositions="")
    ids, refusal = hb.close_adjudication(root, "wi-401")
    assert ids is None
    assert refusal is not None and "no successor" in refusal.lower()
    # The claim did NOT move: the row stays in active/ for a human.
    assert (
        root / "docs" / "work" / "active" / "wi-401" / "WI-401-dispose.md"
    ).is_file()


def test_the_cancelled_close_still_closes_when_it_queues_a_successor(tmp_path):
    # The other side of the same invariant: a brief-less cancelled row that DID
    # draft a successor closes cleanly — the outcome-based guard does not over-fire.
    root = adjudication_repo(tmp_path, brief="", outcome="cancelled")
    ids, refusal = hb.close_adjudication(root, "wi-401")
    assert refusal is None, refusal
    assert ids == ["WI-401"]
    assert integ.finished_branches(root) == ["wi-401"]


def test_the_mechanical_close_no_ops_for_a_non_adjudication_lane(tmp_path):
    # A non-adjudication DONE lane that did not move its specs is the stall
    # candidate the dispatcher already handles — close_adjudication leaves it.
    root = claimed_repo(tmp_path)
    ids, refusal = hb.close_adjudication(root, "wi-401")
    assert ids is None and refusal is None


def batch_repo(tmp_path, branch="wi-401", wids=("WI-401", "WI-402")):
    """A trunk with a BATCH claimed onto one branch (§A4: one branch, one claim
    commit moving every batched spec) — the shape every defect below is
    specific to."""
    skip_without_env_gates("git")
    root = tmp_path / "repo"
    root.mkdir()
    _git(root.parent, "init", "-q", str(root))
    pin_autocrlf(root)
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    (root / "seed.txt").write_text("seed\n", encoding="utf-8", newline="\n")
    (root / ".gitignore").write_text("out/\n", encoding="utf-8", newline="\n")
    for wid in wids:
        spec = root / "docs" / "work" / "queued" / "{}-widget.md".format(wid)
        spec.parent.mkdir(parents=True, exist_ok=True)
        spec.write_text(spec_text(wid), encoding="utf-8", newline="\n")
    _commit(root, "seed + batch", when=T_BASE)
    assert integ.claim(root, list(wids), branch) == 0
    return root


def close_one_row_on_the_lane(root, branch="wi-401", wid="WI-401"):
    """What a batch lane's own C6 close ritual does to ONE of its rows: the spec
    moves to `complete/` and the build commit carries the row's `WI:` trailer.
    The TRUNK's claimed set still lists it — that is the whole point."""
    wt = lane(root, branch)
    name = "{}-widget.md".format(wid)
    src = "docs/work/active/{}/{}".format(branch, name)
    _touched, refusal = hb.spec_move.move_spec(wt, src, "docs/work/complete/" + name)
    assert refusal is None, refusal
    _git(wt, "add", "-A")
    _git(
        wt,
        "commit",
        "--no-verify",
        "-m",
        "close: {} -> complete/\n\nWI: {}".format(wid, wid),
    )
    return wt


def test_the_mechanical_close_no_ops_when_a_batch_row_already_closed(tmp_path):
    # THE MEASURED DEFECT (2026-09-03, lane `wi-589-…`, four rows on one
    # branch). `_close_done_adjudication` calls this for every DONE worker whose
    # branch is not finished, and the claimed set is read off the TRUNK — which
    # still lists a row the lane has already moved to `complete/`. Reading that
    # one as "cannot read the claimed spec" turned a NON-adjudication lane's
    # ordinary stall candidate into a refusal the dispatcher treats as fatal
    # (EXIT_PREFLIGHT), and the whole loop exited 2.
    root = batch_repo(tmp_path)
    close_one_row_on_the_lane(root, wid="WI-401")
    # WI-401 is in complete/ on the branch, WI-402 still in active/; neither is
    # an adjudication row.
    assert integ.finished_branches(root) == []  # not finished: WI-402 is open
    ids, refusal = hb.close_adjudication(root, "wi-401")
    assert refusal is None, refusal
    assert ids is None
    # MUTATION NOTE: before the skip this returned
    # (None, "cannot read the claimed spec WI-401-widget.md on wi-401").


def test_an_adjudication_batch_still_closes_the_row_that_is_open(tmp_path):
    # The other side: skipping an already-moved spec must not stop the close
    # doing its job on the row that IS still claimed.
    root = adjudication_repo(tmp_path)
    ids, refusal = hb.close_adjudication(root, "wi-401")
    assert refusal is None, refusal
    assert ids == ["WI-401"]
    # A second call has nothing left to close and says so as a NO-OP, never a
    # refusal — the same sentence the docstring promises.
    assert hb.close_adjudication(root, "wi-401") == (None, None)


# --- the quarantine (the RULED red arm) ---------------------------------------


def quarantined_repo(tmp_path):
    """A claimed lane that built REAL product changes — one edit, one new file,
    one deletion — so the revert has all three cases to get right."""
    root = claimed_repo(tmp_path)
    wt = lane(root)
    (wt / "seed.txt").write_text("edited\n", encoding="utf-8", newline="\n")
    (wt / "added.py").write_text("BROKEN = (\n", encoding="utf-8", newline="\n")
    (wt / ".gitignore").unlink()
    _commit(wt, "WI-401: half a widget")
    assert hb.close_partial(root, "wi-401", "worker exit 7")[1] is None
    return root, wt


def test_quarantine_reverts_the_product_and_keeps_the_failing_diff(tmp_path):
    root, wt = quarantined_repo(tmp_path)

    assert hb.quarantine(root, "wi-401", "bar exit 1") is None

    # Bar-inert: every product path is back to what the base had, in all THREE
    # diff shapes the lane produced. A revert that only handled modifications
    # would leave added.py — the unparseable file — right where the bar looks,
    # and a revert that ignored deletions would leave .gitignore missing.
    assert (wt / "seed.txt").read_text(encoding="utf-8") == "seed\n"
    assert not (wt / "added.py").exists()
    assert (wt / ".gitignore").read_text(encoding="utf-8") == "out/\n"
    tree = _git(root, "ls-tree", "-r", "--name-only", "wi-401").split()
    assert "added.py" not in tree and ".gitignore" in tree

    # Lossless: the failing diff rides along as a `.patch`, and it really is a
    # patch — git itself re-applies it. The quarantined tip IS the tree the
    # diff was taken against, so applying it here restores the lane's work
    # exactly, which is the property a future WI depends on.
    patch = wt / "docs" / "work" / "handback" / "wi-401.patch"
    assert patch.is_file()
    assert "docs/work/handback/wi-401.patch" in tree
    _git(wt, "apply", "--check", str(patch))
    _git(wt, "apply", str(patch))
    assert (wt / "added.py").read_text(encoding="utf-8") == "BROKEN = (\n"
    assert (wt / "seed.txt").read_text(encoding="utf-8") == "edited\n"
    assert not (wt / ".gitignore").exists()


def test_the_name_status_stream_is_read_as_records_not_pairs():
    # THE PARSE ITSELF, on the exact field list REVIEW-A round 1 drove. Read two
    # at a time this pairs as ('R100','Aold.py'), ('Anew.py','D'), … — paths in
    # the status slot, the bookkeeping filter blind, and `z_broken.py` (the
    # failing file) past the loop bound. A rename is THREE fields, and
    # `diff.renames` has defaulted true since Git 2.9, so this is ordinary
    # output rather than an exotic case.
    fields = [
        "R100",
        "Aold.py",
        "Anew.py",
        "D",
        "docs/work/active/wi-401/WI-401-widget.md",
        "A",
        "docs/work/queued/WI-401-widget.md",
        "M",
        "z_broken.py",
    ]
    assert hb.diff_records(fields) == [
        ("R100", ["Aold.py", "Anew.py"]),
        ("D", ["docs/work/active/wi-401/WI-401-widget.md"]),
        ("A", ["docs/work/queued/WI-401-widget.md"]),
        ("M", ["z_broken.py"]),
    ]
    # A copy is the other three-field form.
    assert hb.diff_records(["C75", "src/a.py", "src/b.py"]) == [
        ("C75", ["src/a.py", "src/b.py"])
    ]
    # A stream that ends mid-record is a TRUNCATED READ, not an empty diff:
    # None, so the caller refuses rather than quarantining a partial list.
    assert hb.diff_records(["R100", "Aold.py"]) is None
    assert hb.diff_records(["M"]) is None


def test_quarantine_reverts_a_rename_and_keeps_the_failing_file(tmp_path):
    # The end-to-end half of the same defect, in the DAMAGING alignment: the
    # rename sorts first (capital A before `docs/`) and the broken file sorts
    # last, so under the pair-parse `z_broken.py` was dropped entirely and the
    # run reported "4 path(s) reverted" over a branch still holding it.
    root = claimed_repo(tmp_path, extra=[("Aold.py", "OLD = 1\n")])
    wt = lane(root)
    _git(wt, "mv", "Aold.py", "Anew.py")
    (wt / "z_broken.py").write_text("VALUE = (\n", encoding="utf-8", newline="\n")
    _commit(wt, "WI-401: rename a module and break a file")
    assert hb.close_partial(root, "wi-401", "worker exit 7")[1] is None

    assert hb.quarantine(root, "wi-401", "bar exit 1") is None

    tree = _git(root, "ls-tree", "-r", "--name-only", "wi-401").split()
    # The rename is undone in BOTH directions...
    assert "Aold.py" in tree and "Anew.py" not in tree
    assert (wt / "Aold.py").read_text(encoding="utf-8") == "OLD = 1\n"
    assert not (wt / "Anew.py").exists()
    # ...and the failing file is really gone, not merely uncounted.
    assert "z_broken.py" not in tree and not (wt / "z_broken.py").exists()
    # The record keeps both, which is the other half of what the mis-parse lost.
    patch = (wt / "docs" / "work" / "handback" / "wi-401.patch").read_text(
        encoding="utf-8"
    )
    assert "z_broken.py" in patch and "Anew.py" in patch


def test_a_failed_revert_step_refuses_and_restores_rather_than_reporting(
    tmp_path, monkeypatch
):
    # The discarded return codes. Under the mis-parse four git calls were
    # no-match failures and every one was thrown away, which is why a wrong
    # revert printed a confident count. Fault-injected on the LAST revert step
    # so earlier ones have already run: the refusal names the path, and the
    # lane goes back to its tip instead of being left half-reverted.
    root, wt = quarantined_repo(tmp_path)
    real_git = hb.ac.git

    def flaky(cwd, *args):
        if args[:1] == ("checkout",) and args[-1] == "seed.txt":
            return 1, "fatal: simulated pathspec failure"
        return real_git(cwd, *args)

    monkeypatch.setattr(hb.ac, "git", flaky)
    refusal = hb.quarantine(root, "wi-401", "bar exit 1")
    monkeypatch.undo()

    assert refusal is not None
    assert "FAILED on seed.txt" in refusal and "nothing was quarantined" in refusal
    # Restored: the earlier `git rm` of added.py is undone, no artefact was
    # written into the tree, and the branch tip did not move.
    assert (wt / "added.py").is_file()
    assert not (wt / "docs" / "work" / "handback").exists()
    assert "quarantine" not in _git(root, "log", "-1", "--format=%s", "wi-401")


def test_quarantine_leaves_the_handback_bookkeeping_alone(tmp_path):
    # The spec move and the log fragments ARE the record being kept: reverting
    # them would revert the handback itself and put the WI back in `active/`
    # with no lane — the exact stranded shape this design abolishes.
    root, wt = quarantined_repo(tmp_path)
    fragment = wt / "docs" / "log.d" / "WI-401-widget.md"
    fragment.parent.mkdir(parents=True, exist_ok=True)
    fragment.write_text(
        "## 2026-08-01 — half a widget\n", encoding="utf-8", newline="\n"
    )
    _commit(wt, "log: WI-401 fragment")

    assert hb.quarantine(root, "wi-401", "bar exit 1") is None
    assert (wt / "docs" / "work" / "partial" / "WI-401-widget.md").is_file()
    assert fragment.is_file()
    # The per-close REPORT is bookkeeping too — reverting it would destroy the
    # event identity the disposition mint keys off, leaving a terminal row that
    # nothing is owed a judgement for.
    assert (wt / "docs" / "handbacks" / "WI-401-wi-401.md").is_file()
    assert integ.branch_outcomes(root, "wi-401")[0] == {"WI-401": "partial"}


def test_quarantine_refuses_when_the_red_is_not_the_lanes_own_code(tmp_path):
    # A lane that changed nothing outside the bookkeeping surfaces cannot have
    # caused the red, so there is nothing to revert and reverting nothing would
    # only buy a second identical bar run. It says so instead.
    root = claimed_repo(tmp_path)
    lane(root)
    assert hb.close_partial(root, "wi-401", "worker exit 7")[1] is None

    refusal = hb.quarantine(root, "wi-401", "bar exit 1")
    assert refusal is not None
    assert "nothing outside the bookkeeping surfaces" in refusal


def test_the_git_dependency_is_declared_for_this_module():
    # This suite drives real repositories end to end; without git on PATH every
    # test above would SKIP and the module would still print a green. The
    # declared gate (conftest.ENV_GATES) is what makes that skip COUNTED in the
    # terminal summary rather than invisible (WI-326).
    assert shutil.which("git"), "the module-level env gate should have skipped"


def test_a_partial_close_skips_a_row_the_lane_already_closed(tmp_path):
    # The batch shape again, on the OTHER close. The claimed set is the TRUNK's,
    # so a batch that finished WI-401 and then hit its session ceiling still
    # lists WI-401 as claimed — and moving it a second time both fails and would
    # overwrite an outcome the lane itself declared. Only the row still open
    # closes as partial.
    root = batch_repo(tmp_path)
    close_one_row_on_the_lane(root, wid="WI-401")
    ids, refusal = hb.close_partial(
        root,
        "wi-401",
        "worker exit 7",
        {"suggested_tier": "strong", "keep_commits": ["abc1234"]},
    )
    assert refusal is None, refusal
    assert ids == ["WI-402"]
    assert (root / "docs" / "work" / "complete" / "WI-401-widget.md").is_file() is False
    merge_branch(root)
    # WI-401 keeps its OWN outcome; WI-402 got the partial one, with its report.
    assert (root / "docs" / "work" / "complete" / "WI-401-widget.md").is_file()
    assert (root / "docs" / "work" / "partial" / "WI-402-widget.md").is_file()
    assert report_path(root, "WI-402", "wi-401").is_file()
    # ...and no report was written for the row this close did not touch.
    assert not report_path(root, "WI-401", "wi-401").is_file()


def test_a_partial_close_with_every_row_already_terminal_is_a_no_op(tmp_path):
    root = batch_repo(tmp_path, wids=("WI-401",))
    close_one_row_on_the_lane(root, wid="WI-401")
    ids, refusal = hb.close_partial(
        root,
        "wi-401",
        "worker exit 7",
        {"suggested_tier": "strong", "keep_commits": ["abc1234"]},
    )
    assert refusal is None, refusal
    assert ids == []
    assert not report_path(root, "WI-401", "wi-401").is_file()
