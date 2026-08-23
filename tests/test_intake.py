"""intake.py — the unified trunk-side intake mint (WI-388, concurrency-v2 §A5.2).

The invariant under test is R1 + R3 (log.md Decisions, 2026-08-01): a WI id is
created ONLY by a human trunk commit or this helper — lanes never mint. The
helper has three triggers, all trunk-side, serial by construction, plus the
drafts-not-mints arm:

  (a) an approved-cell (or routed traced-cell) diff on the merged commit, via
      `check_trajectory.staged_spine_amendments(root, before, after)` — mints
      ONE adjudication row whose title + `## Context` list each changed row,
      cell and before/after;
  (b) a merged spec carrying `## Handback` — mints the DISPOSITION row (same
      adjudication kind; outcomes cancel / defer / re-queue with drafted
      follow-up / surface an open item), and NEVER for a handed-back
      adjudication row (the no-recursion invariant, enforced at both ends);
  (c) the dispatcher's empty-frontier gap census — concrete gap-closure rows
      with derived descriptions, deduped against open rows so the ladder can
      not mint the same gap forever;
  (d) drafts-not-mints: a merged adjudication spec's `## Dispositions` section
      (fenced TOML blocks) is parsed HERE and its follow-ups minted at ITS
      merge — an in-lane mint would trip WI-397's R1 rung at the row's own
      merge slot.

Every trigger below is driven red-then-green against the real git plumbing and
the real spec folder — no seam is stubbed.
"""

import subprocess
import tomllib

import pytest
from conftest import (
    env_gate_skipif,
    load_script,
    pin_autocrlf,
    set_process_key,
    skip_without_env_gates,
)

pytestmark = env_gate_skipif("git")

intake = load_script("intake")
ac = load_script("agent_common")
wi_convert = load_script("wi_convert")
# The stage carrier's ONE home since WI-498 slice 1 — imported as a package (not
# via `load_script`, which loads a single `scripts/*.py`); `scripts/` is already
# on sys.path by here, because `load_script` puts it there.
import kitlib.ladder as kit_ladder  # noqa: E402  (after the loads above)
import kitlib.stage as kit_stage  # noqa: E402  (after the loads above)

T_BASE = 1_000_000
T_CODE = 1_000_100
T_LATER = 1_000_200


# --- fixtures (the tests/test_integrate.py shapes, copied per the suite idiom
# that no test module imports another) -----------------------------------------


def _git(root, *args, env=None):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def _commit(root, message, when=None):
    import os

    env = dict(os.environ)
    if when is not None:
        stamp = "@{} +0000".format(when)
        env["GIT_AUTHOR_DATE"] = stamp
        env["GIT_COMMITTER_DATE"] = stamp
    _git(root, "add", "-A", env=env)
    _git(root, "commit", "-qm", message, env=env)


def git_repo(root, branch="main"):
    skip_without_env_gates("git")
    _git(root, "init", "-q")
    pin_autocrlf(root)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "symbolic-ref", "HEAD", "refs/heads/" + branch)
    (root / "seed.txt").write_text("seed\n", encoding="utf-8", newline="\n")
    (root / "docs").mkdir(exist_ok=True)
    (root / "docs" / "stack.ini").write_text(
        "[generated]\nPROJECT_STATE.html = trajectory\n",
        encoding="utf-8",
        newline="\n",
    )
    # Every repo carries an id watermark: `intake.next_wi_id` mints from it, and
    # its reader REFUSES a missing mark rather than degrading to zero (a mint
    # with no record of what has been allocated must not proceed on a guess).
    # Seeded at all-zeros, which is what a repo that has allocated nothing says
    # — the mint's `max(live, mark) + 1` then behaves exactly as it always did
    # for these fixtures, whose ids come from spec FILENAMES. Rendered through
    # trace's own writer so the fixture cannot drift from the reader.
    trace = load_script("trace")
    (root / trace.WATERMARK).write_text(
        trace.render_watermark({s: 0 for s in trace.WATERMARK_SPACES}),
        encoding="utf-8",
        newline="\n",
    )
    _commit(root, "seed", when=T_BASE)
    return root


def _rev(root, ref="HEAD"):
    return _git(root, "rev-parse", ref).strip()


SR_HEADER = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status\n"
)
LLR_HEADER = (
    "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,Rationale,TestRefs,"
    "Status,Component,Phase\n"
)


def write_sr(root, requirement="the original text", status="Approved"):
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "system-requirements.csv").write_text(
        SR_HEADER
        + 'SR-001,Adder,SN-001,"{}","why","ac",,C,Test,{}\n'.format(
            requirement, status
        ),
        encoding="utf-8",
        newline="\n",
    )


def write_llr(root, sr_refs="SR-001", module="src/d.py"):
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "low-level-requirements.csv").write_text(
        LLR_HEADER
        + 'LLR-001,{},Core,{},f,"the detail","why",TC-001,Approved,CMP-001,1\n'.format(
            sr_refs, module
        ),
        encoding="utf-8",
        newline="\n",
    )


def spec_text(wid, title="Thing", body="", **frontmatter):
    lines = ['id = "{}"'.format(wid), 'title = "{}"'.format(title)]
    for key, value in frontmatter.items():
        if isinstance(value, list):
            lines.append(
                "{} = [{}]".format(key, ", ".join('"{}"'.format(v) for v in value))
            )
        else:
            lines.append('{} = "{}"'.format(key, value))
    return "+++\n" + "".join(ln + "\n" for ln in lines) + "+++\n" + body


def write_spec(root, where, wid, slug="thing", **kw):
    path = root / "docs" / "work" / where / "{}-{}.md".format(wid, slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(spec_text(wid, **kw), encoding="utf-8", newline="\n")
    return path


def queued_rows(root):
    """{WI-ID: row} of every queued spec, read back through the real loader."""
    acommon = load_script("agent_common")
    return {
        r["WI-ID"]: r
        for r in acommon.read_spec_rows(root / "docs" / "work")
        if r["Status"] == "queued"
    }


def amended_repo(tmp_path, amend):
    """A repo whose second commit amends the attested spine per `amend`;
    returns `(root, before_sha, after_sha)`."""
    root = git_repo(tmp_path)
    write_sr(root)
    write_llr(root)
    write_spec(root, "queued", "WI-003", specref="seed.txt")
    _commit(root, "attested baseline", when=T_CODE)
    before = _rev(root)
    amend(root)
    _commit(root, "the merged branch's delta", when=T_CODE + 100)
    return root, before, _rev(root)


# --- trigger (a): the approved-cell diff on the merged commit ------------------


def test_a_approved_cell_diff_mints_one_adjudication_row(tmp_path):
    root, before, after = amended_repo(
        tmp_path, lambda r: write_sr(r, requirement="the AMENDED text")
    )
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "wi-003")
    assert refusal is None, refusal
    assert len(minted) == 1
    wid, relpath = minted[0]
    assert wid == "WI-004"  # max existing (WI-003) + 1
    row = queued_rows(root)[wid]
    assert row["SafetyClass"] == "adjudication"
    assert row["BlockRef"] == ""  # work, not a decision brief
    assert row["SR-Refs"] == "SR-001"
    assert "adjudicate" in row["Title"] and "SR-001" in row["Title"]
    # The derived listing: each changed row, cell, and before/after, in the
    # advisory Context section (R-A forbids a filled Deliverable on an open
    # row, so the derived description's long form lives there).
    text = (root / relpath).read_text(encoding="utf-8")
    assert "## Context" in text
    assert "Requirement" in text
    assert "the original text" in text and "the AMENDED text" in text
    # ...and the mint is a trunk COMMIT (bookkeeping): the tree moved.
    assert relpath.replace("\\", "/") in _git(
        root, "ls-tree", "-r", "--name-only", "HEAD"
    )


def test_a_routed_traced_repoint_mints_and_a_silent_traced_edit_does_not(tmp_path):
    # The WI-388 cell ruling, live: LLR SR-Refs routes to adjudication like
    # SN-Refs/Verifies; a Module-only move is silent by ruling — no mint.
    root, before, after = amended_repo(
        tmp_path, lambda r: write_llr(r, sr_refs="SR-002")
    )
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "b")
    assert refusal is None, refusal
    assert len(minted) == 1
    assert "LLR-001" in queued_rows(root)[minted[0][0]]["Title"]

    (tmp_path / "silent").mkdir()
    root2, before2, after2 = amended_repo(
        tmp_path / "silent", lambda r: write_llr(r, module="src/moved/d.py")
    )
    minted2, refusal2 = intake.intake_after_merge(root2, before2, after2, {}, "b")
    assert refusal2 is None, refusal2
    assert minted2 == []


def test_the_amendment_mint_is_idempotent_across_a_rerun(tmp_path):
    # The recovery path re-runs intake for a landed merge (the CLI); the
    # derived title carries the sha pair, so a re-run finds it and mints
    # nothing — no second row for one event.
    root, before, after = amended_repo(
        tmp_path, lambda r: write_sr(r, requirement="the AMENDED text")
    )
    first, _ = intake.intake_after_merge(root, before, after, {}, "b")
    assert len(first) == 1
    again, refusal = intake.intake_after_merge(root, before, after, {}, "b")
    assert refusal is None, refusal
    assert again == []


# --- the deterministic id: max+1 over EVERY declared status directory ----------


def test_the_id_is_max_plus_one_over_every_status_directory(tmp_path):
    root = git_repo(tmp_path)
    write_sr(root)
    write_spec(root, "draft", "WI-003")
    write_spec(root, "queued", "WI-007", specref="seed.txt")
    write_spec(root, "deferred", "WI-004")
    write_spec(root, "cancelled", "WI-009", body="\n## Deliverable\n\nnever\n")
    write_spec(root, "complete", "WI-002", body="\n## Deliverable\n\nshipped\n")
    write_spec(root, "active/wi-012", "WI-012", specref="seed.txt")
    assert intake.next_wi_id(root) == "WI-013"


# --- trigger (b): a merged handback mints the disposition row ------------------


def close_repo(tmp_path, safety="ordinary", tier="strong", branch="wi-005"):
    """A trunk where WI-005 closed EARLY: the spec is terminal in `partial/` and
    its immutable per-close report sits under docs/handbacks/.

    The report — not the spec — is the event's identity (SR-144). The old
    fixture wrote a `## Handback` section into the spec and let the merge sha
    stand in for the event, which is the shape five successive dedup mechanisms
    leaked through."""
    root = git_repo(tmp_path)
    write_sr(root)
    write_spec(
        root,
        "partial",
        "WI-005",
        slug="returned",
        specref="seed.txt",
        safety_class=safety,
    )
    write_close_report(root, "WI-005", branch, tier=tier)
    _commit(root, "the early close landed", when=T_CODE)
    return root


def write_close_report(root, wi, branch, tier="strong", reason="stopped early"):
    """One per-close report, the shape `handback.close_partial` writes."""
    path = root / "docs" / "handbacks" / "{}-{}.md".format(wi, branch)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = (
        "\n".join(
            [
                "+++",
                'wi = "{wi}"',
                'branch = "{branch}"',
                'claimed_outcome = "partial"',
                'reason = "{reason}"',
                'commit_range = "aaa..bbb"',
                'suggested_tier = "{tier}"',
                'keep_commits = ["aaa"]',
                "discard_commits = []",
                "+++",
            ]
        ).format(wi=wi, branch=branch, reason=reason, tier=tier)
        + "\n"
    )
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return path


def test_a_merged_handback_mints_the_disposition_row(tmp_path):
    root = close_repo(tmp_path)
    before = after = _rev(root)
    minted, refusal = intake.intake_after_merge(
        root, before, after, {"WI-005": "partial"}, "wi-005"
    )
    assert refusal is None, refusal
    assert len(minted) == 1
    row = queued_rows(root)[minted[0][0]]
    assert row["SafetyClass"] == "adjudication"
    assert "dispose" in row["Title"] and "WI-005" in row["Title"]
    # The four outcomes are in the row's face, and closing early is NOT one of
    # them. SR-145 retired R3's `re-queue`: a terminal row is never put back on
    # the frontier, so continuing means DRAFTING A SUCCESSOR.
    for outcome in ("cancel", "defer", "draft a successor", "open item"):
        assert outcome in row["Title"]
    assert "re-queue" not in row["Title"]
    # The title keys on the REPORT PATH and nothing else — every token in it is
    # part of the dedup key, and the report is the only one that cannot move.
    assert "docs/handbacks/WI-005-wi-005.md" in row["Title"]
    assert "partial" not in row["Title"], (
        "a MUTABLE field in the title re-mints on an edit (F1/F2)"
    )
    # The tier is the report's TYPED `suggested_tier` field — not a
    # case-folded substring search of a free-prose reason, which is what a typo
    # used to downgrade silently.
    assert row["BuildTier"] == "strong"
    # The spec-of-record is the closed spec itself, terminal in partial/.
    assert row["SpecRef"] == "docs/work/partial/WI-005-returned.md"
    # ...and the row's Context names the REPORT and does not quote the lane.
    body = (root / minted[0][1]).read_text(encoding="utf-8")
    assert "docs/handbacks/WI-005-wi-005.md" in body
    assert "READ IT FIRST" in body
    assert "stopped early" not in body, (
        "a judge's brief must not open with the defendant's own words"
    )


def test_a_merged_handback_mints_from_the_archive_home_too(tmp_path):
    """WI-504 (OI-55 ruled (a)): the closed spec `_closed_spec` finds may now
    be under `docs/archive/work/partial/` — one directory deeper than the
    pre-migration `docs/work/partial/` `close_repo` fixture writes to — and
    the disposition mint must find it there exactly the same way."""
    root = git_repo(tmp_path)
    write_sr(root)
    path = root / "docs" / "archive" / "work" / "partial" / "WI-005-returned.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        spec_text("WI-005", specref="seed.txt", safety_class="ordinary"),
        encoding="utf-8",
        newline="\n",
    )
    write_close_report(root, "WI-005", "wi-005", tier="strong")
    _commit(root, "the early close landed", when=T_CODE)
    before = after = _rev(root)
    minted, refusal = intake.intake_after_merge(
        root, before, after, {"WI-005": "partial"}, "wi-005"
    )
    assert refusal is None, refusal
    assert len(minted) == 1
    row = queued_rows(root)[minted[0][0]]
    assert row["SpecRef"] == "docs/archive/work/partial/WI-005-returned.md"


def test_a_handed_back_adjudication_row_mints_no_second_disposition(tmp_path):
    # The no-recursion invariant at the INTAKE end: a disposition row that
    # somehow lands handed back must not spawn another disposition row.
    root = close_repo(tmp_path, safety="adjudication")
    before = after = _rev(root)
    minted, refusal = intake.intake_after_merge(
        root, before, after, {"WI-005": "partial"}, "wi-005"
    )
    assert refusal is None, refusal
    assert minted == []


def test_a_second_close_of_the_same_row_mints_a_second_disposition(tmp_path):
    # THE STARVATION CLASS, closed structurally. A second close is a SECOND
    # REPORT — a new file with its own path — so the derived title differs and
    # the mint is owed. The five mechanisms this replaces all tried to
    # reconstruct "was this event judged?" from the mutable spec (a merge sha
    # the bare sweep read as symbolic HEAD, the spec's last-touch commit, a
    # digest of a note, an open-disposition state read, field co-occurrence)
    # and every one could silently drop an owed judgement.
    root = close_repo(tmp_path)
    sha1 = _rev(root)
    first, refusal = intake.intake_after_merge(
        root, sha1, sha1, {"WI-005": "partial"}, "wi-005"
    )
    assert refusal is None, refusal
    assert len(first) == 1

    # A genuinely SECOND close of the same row: a new branch, so a new report.
    write_close_report(root, "WI-005", "wi-005-second", tier="medium")
    _commit(root, "a second close of WI-005", when=T_LATER)
    sha2 = _rev(root)
    second, refusal = intake.intake_after_merge(
        root, sha2, sha2, {"WI-005": "partial"}, "wi-005-second"
    )
    assert refusal is None, refusal
    assert len(second) == 1, "the second CLOSE event owes its own disposition"
    titles = {queued_rows(root)[wid]["Title"] for wid, _rel in first + second}
    assert len(titles) == 2, titles


def test_a_second_intake_for_the_same_handback_is_deduped(tmp_path):
    root = close_repo(tmp_path)
    before = after = _rev(root)
    first, _ = intake.intake_after_merge(
        root, before, after, {"WI-005": "partial"}, "wi-005"
    )
    assert len(first) == 1
    again, refusal = intake.intake_after_merge(
        root, before, after, {"WI-005": "partial"}, "wi-005"
    )
    assert refusal is None, refusal
    assert again == []


# --- drafts-not-mints: the ## Dispositions section -----------------------------

DISPOSITIONS = """
## Deliverable

Adjudicated: SR-001's amendment moved scope; follow-up drafted.

## Dispositions

```toml
title = "Re-verify SR-001 against the amended text"
workstream = "scripts"
buildtier = "medium"
planmode = "dual"
specref = "seed.txt"
```
"""


def merged_adjudication_repo(tmp_path, body=DISPOSITIONS):
    root = git_repo(tmp_path)
    write_sr(root)
    write_spec(
        root,
        "complete",
        "WI-008",
        slug="adjudicate",
        safety_class="adjudication",
        body=body,
    )
    _commit(root, "the adjudication row's merge landed", when=T_CODE)
    return root


def test_a_merged_adjudication_rows_dispositions_are_minted_at_its_merge(tmp_path):
    root = merged_adjudication_repo(tmp_path)
    before = after = _rev(root)
    minted, refusal = intake.intake_after_merge(
        root, before, after, {"WI-008": "merged"}, "wi-008"
    )
    assert refusal is None, refusal
    assert len(minted) == 1
    row = queued_rows(root)[minted[0][0]]
    assert row["Title"] == "Re-verify SR-001 against the amended text"
    assert row["BuildTier"] == "medium"
    assert row["SpecRef"] == "seed.txt"
    # planmode = dual IS the deeper-review route — and the kind stays DERIVED
    # from it (single-source): no second hand-set SafetyClass cell.
    assert row["PlanMode"] == "dual"
    assert row["SafetyClass"] == ""


def test_a_malformed_disposition_block_refuses_and_mints_nothing(tmp_path):
    bad = DISPOSITIONS.replace('title = "Re-verify', '= "Re-verify')
    root = merged_adjudication_repo(tmp_path, body=bad)
    before = after = _rev(root)
    minted, refusal = intake.intake_after_merge(
        root, before, after, {"WI-008": "merged"}, "wi-008"
    )
    assert minted == []
    assert refusal is not None and "Dispositions" in refusal


def test_a_draft_declaring_the_adjudication_kind_is_refused(tmp_path):
    # Deeper review is a drafted follow-up with planmode = dual — NEVER a
    # second adjudication row (the amendment's tier-signals clause).
    bad = DISPOSITIONS.replace('planmode = "dual"', 'safety_class = "adjudication"')
    root = merged_adjudication_repo(tmp_path, body=bad)
    before = after = _rev(root)
    minted, refusal = intake.intake_after_merge(
        root, before, after, {"WI-008": "merged"}, "wi-008"
    )
    assert minted == []
    assert refusal is not None and "adjudication" in refusal


# --- the context block (WI-388 clause 4): pure registry joins ------------------


def context_repo(tmp_path):
    """A repo whose registries hold one of EVERY join the context block makes:
    a cancelled precedent with its reason, a pending OI naming kin, the LLR/TC
    code map, a component knowledge pack, an IF seam via the LLR's module, and
    a review record of the precedent row."""
    root = git_repo(tmp_path)
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    write_sr(root)
    (req / "low-level-requirements.csv").write_text(
        LLR_HEADER + 'LLR-001,SR-001,Core,src/widget.py,widget_f,"the detail","why",'
        "TC-001,Approved,CMP-001,1\n",
        encoding="utf-8",
        newline="\n",
    )
    test_dir = root / "docs" / "test"
    test_dir.mkdir(parents=True, exist_ok=True)
    (test_dir / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,"
        "Evidence,Status,Phase\n"
        "TC-001,SR-001;LLR-001,Unit,run it,smoke,,works,Y,tests/test_widget.py,"
        "Approved,1\n",
        encoding="utf-8",
        newline="\n",
    )
    (req / "components.csv").write_text(
        "CMP-ID,Name,Category,Knowledge,State,SupersededBy,PartOf,Notes\n"
        "CMP-001,Widget core,software,docs/knowledge/widgetry,built,,,\n",
        encoding="utf-8",
        newline="\n",
    )
    (req / "interfaces.csv").write_text(
        "IF-ID,Direction,ThisProject,Counterpart,Contract,Req-Refs,Version,"
        "Stability,Status,Component,Notes\n"
        'IF-001,Provides,scripts/widget,scripts/check,"widget CLI: exits 1 on '
        'a bad widget",SR-001,v1,Stable,Active,CMP-001,\n',
        encoding="utf-8",
        newline="\n",
    )
    (req / "open-items.csv").write_text(
        "OI-ID,Title,Status,Raised,OneLine,Decision,BlastRadius,Options,"
        "Recommendation,WI-Refs,RuledDate,RulingRef\n"
        "OI-002,widget premise,pending,2026-08-01,is the widget premise still "
        "true,,,,,WI-005,,\n",
        encoding="utf-8",
        newline="\n",
    )
    reviews = root / "docs" / "reviews"
    reviews.mkdir(parents=True, exist_ok=True)
    (reviews / "WI-002-REVIEW-A.md").write_text(
        "VERDICT: CHANGES-REQUESTED findings=2\n", encoding="utf-8", newline="\n"
    )
    write_spec(
        root,
        "cancelled",
        "WI-002",
        slug="refuted",
        sr_refs=["SR-001"],
        body=(
            "\n## Deliverable\n\ncancelled: REFUTED - proposed navigation "
            "with no driving necessity\n"
        ),
    )
    write_spec(root, "queued", "WI-005", sr_refs=["SR-001"], specref="seed.txt")
    _commit(root, "the joined registries", when=T_CODE)
    return root


def test_the_context_block_renders_from_real_joins_in_failure_cost_order(tmp_path):
    root = context_repo(tmp_path)
    acommon = load_script("agent_common")
    rows = acommon.read_spec_rows(root / "docs" / "work")
    row = next(r for r in rows if r["WI-ID"] == "WI-005")
    text = intake.context_block(root, row, rows)
    # Every join present...
    assert "WI-002" in text and "REFUTED" in text  # precedent WITH ITS REASONS
    assert "OI-002" in text  # pending OI whose WI-Refs intersect
    assert "LLR-001" in text and "src/widget.py" in text and "widget_f" in text
    assert "tests/test_widget.py" in text  # the TC evidence map
    assert "docs/knowledge/widgetry" in text  # LLR.Component -> CMP.Knowledge
    assert "IF-001" in text  # IF seams via LLR.Module
    assert "docs/reviews/WI-002-REVIEW-A.md" in text  # precedent reviews
    # ...in the ruled order (content order by failure cost: the refuted
    # precedent first, premise risk second, then the maps).
    assert (
        text.index("WI-002")
        < text.index("OI-002")
        < text.index("LLR-001")
        < text.index("docs/knowledge/widgetry")
        < text.index("IF-001")
        < text.index("docs/reviews/WI-002-REVIEW-A.md")
    )


def test_the_context_block_is_advisory_never_gating(tmp_path):
    # No registries, no git, a half-empty row: the block answers "" or partial
    # text — never a raise. Advisory means the caller cannot be broken by it.
    (tmp_path / "empty").mkdir()
    assert intake.context_block(tmp_path / "empty", {"WI-ID": "WI-001"}) == ""
    assert (
        intake.context_block(tmp_path / "does-not-exist", {}) == ""
    )  # nothing to join


def test_minted_rows_carry_the_context_block(tmp_path):
    # Consumer 1: minted rows have no spec author, so the mint writes the
    # block into the body at mint — the cancelled precedent's REASON included
    # (the measured WI-391 failure mode: re-proposing the refuted).
    root = context_repo(tmp_path)
    write_sr(root, requirement="the AMENDED text")
    before = _rev(root, "HEAD")
    _commit(root, "the merged delta", when=T_CODE + 100)
    minted, refusal = intake.intake_after_merge(root, before, _rev(root), {}, "b")
    assert refusal is None, refusal
    assert len(minted) == 1
    text = (root / minted[0][1]).read_text(encoding="utf-8")
    assert "## Context" in text
    assert "WI-002" in text and "REFUTED" in text


# --- trigger (c): the gap census mints concrete gap-closure rows ---------------


def test_the_census_mints_gap_rows_and_dedupes_on_rerun(tmp_path):
    root = git_repo(tmp_path)
    write_sr(root)
    (root / "docs" / "work" / "queued").mkdir(parents=True)
    census = [
        "SR-001 is not Approved (Status=Drafted)",
        "SN SN-002 is a draft need (unapproved)",
    ]
    minted, refusal = intake.mint_gap_rows(root, census)
    assert refusal is None, refusal
    assert len(minted) == 2
    rows = queued_rows(root)
    for wid, _rel in minted:
        assert rows[wid]["SafetyClass"] == "ordinary"
        assert rows[wid]["Title"].startswith("close registry gap:")
    # The dispatcher's ladder re-derives the census every idle tick; an open
    # row per gap means the re-run mints NOTHING (no mint loop).
    again, refusal = intake.mint_gap_rows(root, census)
    assert refusal is None, refusal
    assert again == []


# --- the gate-policy arms (ruled decision 2, owner 2026-07-31; §A8) ------------


def _policy_repo(tmp_path, dial):
    """A repo with one Drafted SR, one Approved SR, one Drafted LLR, and the
    declared approval `dial` — the state an adjudication row's cheap
    outcome acts on.

    `dial` IS A `DevStg-*` RUNG SINCE WI-493, not the retired 0-4 ordinal. The
    ordinal would still be READ (the migration window translates it and warns),
    which is exactly why the fixture does not use it: a suite that keeps
    declaring the retired spelling proves the window works and stops proving
    anything about the dial the kit actually ships.

    THE FIXTURE ROWS READ `Drafted` SINCE D-9 STEP 7. They read `Modified`, the
    marker that named "approved text that has since moved" and the one state
    `_apply_flips` ever moved FROM; the word retired with the step, and a
    fixture carrying it would be driving this repo's writer with a value its own
    integrity floor now refuses. `Drafted` is the live below-`Approved` value,
    which is what these fixtures need: a located row that is NOT already at the
    value the act writes."""
    root = git_repo(tmp_path)
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "system-requirements.csv").write_text(
        SR_HEADER
        + 'SR-001,Adder,SN-001,"the text","why","ac",,C,Test,Drafted\n'
        + 'SR-002,Widget,SN-001,"other text","why","ac",,C,Test,Approved\n',
        encoding="utf-8",
        newline="\n",
    )
    (req / "low-level-requirements.csv").write_text(
        LLR_HEADER + 'LLR-001,SR-001,Core,src/d.py,f,"the detail","why",TC-001,Drafted,'
        "CMP-001,1\n",
        encoding="utf-8",
        newline="\n",
    )
    _declare_dial(root, dial)
    _commit(root, "the flagged spine + the declared policy", when=T_CODE)
    return root


# The rung `_declare_dial` records, named because both sides of the comparison
# are read against it: a dial AT or BELOW `DevStg-Tests` holds this repo, and a
# dial above it does not.
FIXTURE_STAGE = kit_ladder.STAGE_TESTS


def _declare_dial(root, dial):
    """Declare BOTH halves of SN-029's comparison: the human-approval dial
    in docs/process.toml, and the spine stage the derived record reports.

    The stage is RECORDED rather than derived from a real spine, because what is
    under test here is the COMPARISON — a fixture that had to build a whole spine
    to move one side of it would be testing spine_rules instead.

    THE CARRIER MOVED AT WI-498 SLICE 5, and this fixture had to move with it.
    `agent_common.spine_stage_of` used to scrape `stage=` off a comment line in
    the generated `docs/gate`; it now goes through `kitlib.stage.read_stage`,
    which re-fingerprints the declared derivation inputs on EVERY call and trusts
    a recorded value only on a match. A fixture still writing `docs/gate`
    therefore declared no stage at all: the reader answered None, `human_holds`
    reads None as HUMAN-HELD (its documented fail-safe), and both arms of the
    comparison silently collapsed onto the same answer — a below-the-dial test
    passing for the reason a held one does.

    So the record is written to `docs/stage` WITH the current fingerprint, which
    is what puts the reader on its recorded fast path. Only `stage` and
    `fingerprint` are written: `parse` addresses fields BY NAME and leaves an
    absent one absent, so a fixture states what it is declaring and nothing
    else."""
    set_process_key(root, "attestation", "human_approval_through", dial)
    path = root / kit_stage.STAGE_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(
            "# DERIVED STAGE (fixture-written; see tests/test_intake.py)\n"
            "stage = {}\n"
            "fingerprint = {}\n".format(
                FIXTURE_STAGE, kit_stage.fingerprint(root, memo=None)
            )
        )


def test_under_attended_adjudication_recommends_and_never_flips(tmp_path, capsys):
    # Ruled decision 2: under `attended` the flip is a Status change that
    # RECOVERS THE GATE — an approval, and approval is the human's act.
    # The helper prepares the brief and touches NOTHING.
    root = _policy_repo(tmp_path, kit_ladder.STAGE_RELEASE)
    before = (root / "docs" / "requirements" / "system-requirements.csv").read_bytes()
    action, flipped, refusal = intake.flip_verified(root, ["SR-001", "LLR-001"])
    assert refusal is None, refusal
    assert action == "recommend"
    assert flipped == []
    out = capsys.readouterr().out
    assert "recommend" in out and "SR-001" in out and "LLR-001" in out
    assert (
        root / "docs" / "requirements" / "system-requirements.csv"
    ).read_bytes() == before


def test_below_the_human_dial_a_NON_FLIPPABLE_row_is_NAMED_not_skipped(tmp_path):
    """D-9 STEP 7, and this test replaces a capability rather than losing one.

    It used to prove the other arm of ruled decision 2: below the human's
    approval dial a recorded LLM verdict carries approval authority, so
    the helper enacted `Modified` -> `Approved`. Step 7 retired `Modified`, the
    ONE state that act ever moved from, and the guard it left behind — a silent
    `continue` over every other status — resolved into an explicit refusal.

    So what is proved here now is the refusal, at the SAME authority level the
    flip used to run at: a located row this act cannot move is NAMED, with its
    status quoted, and NOTHING is written. Fail-closed matters more than the
    lost arm — the alternative resolutions (write to a `Drafted` row, or
    re-bless a drifted `Approved` one) are both WIDER than the silent skip they
    would replace, and widening mechanical approval authority is an owner
    ruling, not a migration step's to take. The writer's own properties did not
    move with the guard and are proved directly below.

    THE TWO DIALS ARE THE RE-KEYED 0 AND 2 (WI-493): `DevStg-Below` is the
    sentinel that holds nothing, and `DevStg-Arch` is BELOW the fixture's
    recorded `DevStg-Tests`, so neither holds this repo and both reach the
    writer's guard. Driving both is what keeps the arm honest — a single
    `DevStg-Below` case would also pass against a `human_holds` that had
    collapsed to a constant False.
    """
    for i, dial in enumerate((kit_stage.BELOW, kit_ladder.STAGE_ARCH)):
        (tmp_path / str(i)).mkdir()
        root = _policy_repo(tmp_path / str(i), dial)
        assert ac.human_holds(root / "docs", ac.spine_stage_of(root)) is False, dial
        sr_csv = root / "docs" / "requirements" / "system-requirements.csv"
        llr_csv = root / "docs" / "requirements" / "low-level-requirements.csv"
        before = (sr_csv.read_bytes(), llr_csv.read_bytes())
        with pytest.raises(SystemExit) as excinfo:
            intake.flip_verified(root, ["SR-001", "LLR-001"])
        msg = str(excinfo.value)
        # The row is NAMED, and so is the status that made it non-flippable.
        assert "LLR-001" in msg and "Drafted" in msg, msg
        assert "Modified" in msg and "step 7" in msg, msg
        # ...and the refusal wrote nothing: it raises before the write loops.
        assert (sr_csv.read_bytes(), llr_csv.read_bytes()) == before


def test_a_row_already_at_the_written_value_is_the_ONE_silent_skip(tmp_path):
    """The other half of the resolved guard: idempotence survives.

    `SR-002` is `Approved` — already at the value this act writes — so it is
    skipped rather than named, and the act reports no flip. That skip is the one
    the old `if status != "Modified": continue` was RIGHT about, and separating
    it from the refusal is the whole content of the step-7 resolution: one
    branch was two unrelated cases wearing one `continue`.
    """
    root = _policy_repo(tmp_path, kit_stage.BELOW)
    sr_csv = root / "docs" / "requirements" / "system-requirements.csv"
    before = sr_csv.read_bytes()
    action, flipped, refusal = intake.flip_verified(root, ["SR-002"])
    assert (action, flipped, refusal) == ("flip", [], None)
    assert sr_csv.read_bytes() == before


SR_TOML = (
    "# The system requirements. Comments here are LOAD-BEARING for this test.\n"
    "\n"
    "[requirement.SR-001]\n"
    'title = "Adder"\n'
    'sn_refs = ["SN-001"]\n'
    'requirement = """the text"""\n'
    'status = "Drafted"\n'
    "phase = 1\n"
    "\n"
    "# a comment BETWEEN rows, which a re-serialisation would delete\n"
    "[requirement.SR-002]\n"
    'title = "Widget"\n'
    'sn_refs = ["SN-001"]\n'
    'status = "Approved"\n'
)

# The registry key the writer tests below pass directly.
# `_rewrite_toml_statuses` resolves the TOML table name from it, so it is
# the writer's real argument rather than a convenience.
SR_REL = "docs/requirements/system-requirements.toml"


def _write(root, text, newline="\n"):
    """Plant `text` as the live TOML SR registry and return its path — the
    four writer tests below share this setup exactly.

    THEY DRIVE `_rewrite_toml_statuses` DIRECTLY SINCE D-9 STEP 7, where they
    used to reach it through `flip_verified`. The properties under test are
    the WRITER's — a line rewrite rather than a re-serialisation, TOML string
    awareness, and the file's own newline style — and not one of them moved at
    step 7. What moved is the POLICY guard above the writer, which now refuses
    every located row (there is no longer a state it can move FROM), so
    routing through it would test the refusal four more times and test the
    writer zero times."""
    req = root / "docs" / "requirements"
    (req / "system-requirements.csv").unlink()
    sr_toml = req / "system-requirements.toml"
    sr_toml.write_text(text, encoding="utf-8", newline=newline)
    return sr_toml


def test_the_flip_rewrites_ONE_LINE_of_the_toml_carrier(tmp_path):
    # Step 4 of the carrier migration: under the TOML carrier the
    # flip is a LINE REWRITE, on bootstrap.set_process_key's pattern. The
    # properties that matter are what a re-serialisation would destroy —
    # comments, ordering, and every untouched byte — so this asserts the file is
    # byte-identical apart from the single status line of the named row.
    root = _policy_repo(tmp_path, kit_stage.BELOW)
    sr_toml = _write(root, SR_TOML)
    before = sr_toml.read_text(encoding="utf-8")

    intake._rewrite_toml_statuses(sr_toml, SR_REL, ["SR-001"])

    after = sr_toml.read_text(encoding="utf-8")
    b, a = before.split("\n"), after.split("\n")
    assert len(b) == len(a)
    moved = [i for i in range(len(b)) if b[i] != a[i]]
    assert len(moved) == 1, [(b[i], a[i]) for i in moved]
    assert (b[moved[0]], a[moved[0]]) == ('status = "Drafted"', 'status = "Approved"')
    # The comments and the untouched row survived, which is the whole reason
    # this is a line rewrite rather than a re-emit.
    assert "# a comment BETWEEN rows" in after
    assert 'status = "Approved"' in after.split("[requirement.SR-002]")[1]
    # ...and it never reached past the row it was asked for: SR-002 read
    # `Approved` before and reads it after, so the file now holds exactly two.
    assert after.count('status = "Approved"') == 2


# A row whose REQUIREMENT PROSE quotes registry syntax — the counterexample the
# adversarial review used to break the first line rewrite. Every line here is
# ordinary registry content; none of it is a key.
SR_TOML_PROSE = (
    "[requirement.SR-001]\n"
    'title = "Adder"\n'
    'requirement = """The row shall record its own state.\n'
    "status = literal prose inside the requirement\n"
    "[requirement.SR-999] is not a table header either.\n"
    'End of requirement."""\n'
    'status = "Drafted"\n'
)


def test_the_flip_is_toml_STRING_aware_not_line_aware(tmp_path):
    """The review's BLOCKER 3, planted verbatim.

    A physical-line rewrite edited a `status = ...` line INSIDE a multi-line
    requirement string, left the row's real status where it was, and returned
    True — so the tool reported an approval it had not made while silently
    rewriting attested requirement text. Two damages from one defect: a false
    record, and a corrupted registry cell.
    """
    root = _policy_repo(tmp_path, kit_stage.BELOW)
    sr_toml = _write(root, SR_TOML_PROSE)

    intake._rewrite_toml_statuses(sr_toml, SR_REL, ["SR-001"])

    after = sr_toml.read_text(encoding="utf-8")
    # The REAL cell moved...
    assert tomllib.loads(after)["requirement"]["SR-001"]["status"] == "Approved"
    # ...and the prose that merely looks like registry syntax is untouched.
    assert "status = literal prose inside the requirement" in after
    assert "[requirement.SR-999] is not a table header either." in after
    assert (
        tomllib.loads(after)["requirement"]["SR-001"]["requirement"]
        == tomllib.loads(SR_TOML_PROSE)["requirement"]["SR-001"]["requirement"]
    )


def test_a_row_with_no_status_key_at_all_REFUSES(tmp_path):
    """The review's MAJOR 5: absent is not "not Modified".

    A row that never carried a status cannot be re-verified, and accepting it as
    an idempotent no-op reports a clean adjudication over a row the registry
    never staged for one. Distinct from the existing test below, which removes
    the line only AFTER locating a Modified row.
    """
    root = _policy_repo(tmp_path, kit_stage.BELOW)
    req = root / "docs" / "requirements"
    (req / "system-requirements.csv").unlink()
    (req / "system-requirements.toml").write_text(
        '[requirement.SR-001]\ntitle = "Adder"\n', encoding="utf-8", newline="\n"
    )
    with pytest.raises(SystemExit) as excinfo:
        intake.flip_verified(root, ["SR-001"])
    assert "no `status`" in str(excinfo.value)
    assert "SR-001" in str(excinfo.value)


def test_a_crlf_registry_keeps_its_line_endings_through_a_flip(tmp_path):
    """The review's MAJOR 6: the writer advertises "every other byte unchanged",
    and a wholesale CRLF -> LF conversion makes a one-word approval a
    whole-file diff — on the registry whose diffs the amendment guard reads."""
    root = _policy_repo(tmp_path, kit_stage.BELOW)
    sr_toml = _write(root, SR_TOML, newline="\r\n")
    before = sr_toml.read_bytes()
    assert before.count(b"\r\n") > 3  # a genuinely CRLF fixture

    intake._rewrite_toml_statuses(sr_toml, SR_REL, ["SR-001"])

    after = sr_toml.read_bytes()
    assert after.count(b"\r\n") == before.count(b"\r\n")
    changed = [
        (b, a) for b, a in zip(before.split(b"\r\n"), after.split(b"\r\n")) if b != a
    ]
    assert changed == [(b'status = "Drafted"', b'status = "Approved"')]


def test_an_lf_registry_is_not_given_crlf_either(tmp_path):
    """The other half of MAJOR 6 — preserving the style must not mean guessing
    it. An LF file stays LF."""
    root = _policy_repo(tmp_path, kit_stage.BELOW)
    sr_toml = _write(root, SR_TOML)
    intake._rewrite_toml_statuses(sr_toml, SR_REL, ["SR-001"])
    assert b"\r\n" not in sr_toml.read_bytes()


def test_a_toml_row_with_no_status_line_refuses_rather_than_claiming_a_flip(tmp_path):
    # The mutation that proves the writer can still fail: a located row whose
    # status line the rewrite cannot find must REFUSE, because reporting a flip
    # that was never written is an approval the registry does not carry.
    root = _policy_repo(tmp_path, kit_stage.BELOW)
    # Plant the defect: the writer is asked for a row whose status LINE is not
    # in the file. It used to be planted by locating the row first and deleting
    # the line behind the locator's back; driving the writer directly says the
    # same thing without routing through the policy guard, which since D-9
    # step 7 refuses every located row before the writer is reached.
    sr_toml = _write(root, SR_TOML.replace('status = "Drafted"\n', ""))
    with pytest.raises(SystemExit) as excinfo:
        intake._rewrite_toml_statuses(sr_toml, SR_REL, ["SR-001"])
    assert "refusing to report a flip that was not written" in str(excinfo.value)


def test_an_unknown_row_id_refuses_the_flip(tmp_path):
    root = _policy_repo(tmp_path, kit_stage.BELOW)
    action, flipped, refusal = intake.flip_verified(root, ["SR-999"])
    assert flipped == []
    assert refusal is not None and "SR-999" in refusal


def test_an_unreadable_dial_or_stage_fails_toward_recommend(tmp_path):
    # Fail toward the human, never toward a machine approval. Every input
    # this rung can fail on resolves the same way: an out-of-vocabulary dial, a
    # stage record with no stage field (a repo that predates the carrier), and
    # an unparseable one all read as HUMAN-HELD.
    root = _policy_repo(tmp_path, kit_ladder.STAGE_RELEASE)
    action, _flipped, refusal = intake.flip_verified(root, ["SR-001"])
    assert refusal is None, refusal
    assert action == "recommend"

    assert intake.adjudication_action(True) == "recommend"
    assert intake.adjudication_action(False) == "flip"

    # The upstream comparison's own failure directions, driven at a MIDDLE dial.
    # THAT IS NOT A DETAIL: at `DevStg-Release` `human_holds` answers True before
    # it ever looks at the stage, so an unreadable-stage assertion made there is
    # VACUOUS — it would pass against a `human_holds` with the fail-safe deleted.
    # At `DevStg-Arch` the fixture's own recorded rung is NOT held, so a True can
    # only have come from the unreadable-stage arm.
    (tmp_path / "middle").mkdir()
    middle = _policy_repo(tmp_path / "middle", kit_ladder.STAGE_ARCH)
    docs = middle / "docs"
    assert ac.spine_stage_of(middle) == FIXTURE_STAGE, "the record must be READ"
    assert ac.human_holds(docs, FIXTURE_STAGE) is False, "the baseline: not held"
    assert ac.human_holds(docs, None) is True, "an unknown stage is human-held"
    assert ac.human_holds(docs, "3") is True, "a non-rung stage is human-held"
    # ...and an unreadable DIAL holds every rung, whatever the stage says. The
    # rung is named rather than read back through `spine_stage_of` because the
    # write above moves the fingerprint, which would send the reader off to
    # re-derive — a different question than the one under test.
    set_process_key(middle, "attestation", "human_approval_through", "four")
    assert ac.approval_through(docs) == kit_ladder.STAGE_RELEASE
    assert ac.human_holds(docs, FIXTURE_STAGE) is True, "a wrong-typed dial holds"
