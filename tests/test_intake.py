"""intake.py — the unified trunk-side intake mint (WI-388, concurrency-v2 §A5.2).

The invariant under test is R1 + R3 (log.md Decisions, 2026-08-01): a WI id is
created ONLY by a human trunk commit or this helper — lanes never mint. The
helper has three triggers, all trunk-side, serial by construction, plus the
drafts-not-mints arm:

  (a) a ratified-cell (or routed traced-cell) diff on the merged commit, via
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

from conftest import env_gate_skipif, load_script, skip_without_env_gates

pytestmark = env_gate_skipif("git")

intake = load_script("intake")
wi_convert = load_script("wi_convert")

T_BASE = 1_000_000
T_CODE = 1_000_100


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


def write_sr(root, requirement="the original text", status="Verified"):
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
        + 'LLR-001,{},Core,{},f,"the detail","why",TC-001,Verified,CMP-001,1\n'.format(
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


# --- trigger (a): the ratified-cell diff on the merged commit ------------------


def test_a_ratified_cell_diff_mints_one_adjudication_row(tmp_path):
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


def handback_repo(tmp_path, safety="ordinary"):
    root = git_repo(tmp_path)
    write_sr(root)
    write_spec(
        root,
        "queued",
        "WI-005",
        slug="returned",
        specref="seed.txt",
        safety_class=safety,
        blockref="docs/work/queued/WI-005-returned.md",
        body=(
            "\n## Handback\n\nReturned unfinished from lane `wi-005`: worker "
            "exit 7 (NEEDS-HUMAN)\n"
        ),
    )
    _commit(root, "the handback merge landed", when=T_CODE)
    return root


def test_a_merged_handback_mints_the_disposition_row(tmp_path):
    root = handback_repo(tmp_path)
    before = after = _rev(root)
    minted, refusal = intake.intake_after_merge(
        root, before, after, {"WI-005": "handback"}, "wi-005"
    )
    assert refusal is None, refusal
    assert len(minted) == 1
    row = queued_rows(root)[minted[0][0]]
    assert row["SafetyClass"] == "adjudication"
    assert "dispose" in row["Title"] and "WI-005" in row["Title"]
    # The four outcomes are in the row's face, and hand-back is NOT one of them.
    for outcome in ("cancel", "defer", "re-queue", "open item"):
        assert outcome in row["Title"]
    # A NEEDS-HUMAN reason class routes the judgement to the strong tier.
    assert row["BuildTier"] == "strong"
    # The spec-of-record is the returned spec itself.
    assert row["SpecRef"] == "docs/work/queued/WI-005-returned.md"


def test_a_handed_back_adjudication_row_mints_no_second_disposition(tmp_path):
    # The no-recursion invariant at the INTAKE end: a disposition row that
    # somehow lands handed back must not spawn another disposition row.
    root = handback_repo(tmp_path, safety="adjudication")
    before = after = _rev(root)
    minted, refusal = intake.intake_after_merge(
        root, before, after, {"WI-005": "handback"}, "wi-005"
    )
    assert refusal is None, refusal
    assert minted == []


def test_a_second_intake_for_the_same_handback_is_deduped(tmp_path):
    root = handback_repo(tmp_path)
    before = after = _rev(root)
    first, _ = intake.intake_after_merge(
        root, before, after, {"WI-005": "handback"}, "wi-005"
    )
    assert len(first) == 1
    again, refusal = intake.intake_after_merge(
        root, before, after, {"WI-005": "handback"}, "wi-005"
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
        "TC-001,Verified,CMP-001,1\n",
        encoding="utf-8",
        newline="\n",
    )
    test_dir = root / "docs" / "test"
    test_dir.mkdir(parents=True, exist_ok=True)
    (test_dir / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,"
        "Evidence,Status,Phase\n"
        "TC-001,SR-001;LLR-001,Unit,run it,smoke,,works,Y,tests/test_widget.py,"
        "Verified,1\n",
        encoding="utf-8",
        newline="\n",
    )
    (req / "components.csv").write_text(
        "CMP-ID,Name,Category,Knowledge,State,SupersededBy,PartOf,DetailDoc,"
        "Notes\n"
        "CMP-001,Widget core,software,docs/knowledge/widgetry,built,,,,\n",
        encoding="utf-8",
        newline="\n",
    )
    (req / "interfaces.csv").write_text(
        "IF-ID,Direction,ThisProject,Counterpart,Contract,SR-Refs,Version,"
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
        "SR-001 is not Verified (Status=Draft)",
        "SN SN-002 is a draft need (unratified)",
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


def _policy_repo(tmp_path, level):
    """A repo with one Modified SR, one Verified SR, one Modified LLR, and the
    declared gate-policy `level` — the state an adjudication row's cheap
    outcome (no scope moved -> re-verify) acts on."""
    root = git_repo(tmp_path)
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "system-requirements.csv").write_text(
        SR_HEADER
        + 'SR-001,Adder,SN-001,"the text","why","ac",,C,Test,Modified\n'
        + 'SR-002,Widget,SN-001,"other text","why","ac",,C,Test,Verified\n',
        encoding="utf-8",
        newline="\n",
    )
    (req / "low-level-requirements.csv").write_text(
        LLR_HEADER
        + 'LLR-001,SR-001,Core,src/d.py,f,"the detail","why",TC-001,Modified,'
        "CMP-001,1\n",
        encoding="utf-8",
        newline="\n",
    )
    (root / "docs" / "gate-policy").write_text(
        level + "\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "the flagged spine + the declared policy", when=T_CODE)
    return root


def test_under_attended_adjudication_recommends_and_never_flips(tmp_path, capsys):
    # Ruled decision 2: under `attended` the flip is a Status change that
    # RECOVERS THE GATE — a ratification, and ratification is the human's act.
    # The helper prepares the brief and touches NOTHING.
    root = _policy_repo(tmp_path, "attended")
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


def test_under_single_ratify_and_autonomous_the_flip_is_enacted(tmp_path):
    # The other arm: at those levels an LLM verdict already carries
    # ratification authority, so the helper flips Modified -> Verified — and
    # ONLY the Status cells move (the registries stay byte-identical
    # elsewhere; a re-run is an idempotent no-op).
    for i, level in enumerate(("single-ratify", "autonomous")):
        (tmp_path / str(i)).mkdir()
        root = _policy_repo(tmp_path / str(i), "x")  # placeholder level
        (root / "docs" / "gate-policy").write_text(
            level + "\n", encoding="utf-8", newline="\n"
        )
        import csv as _csv

        sr_csv = root / "docs" / "requirements" / "system-requirements.csv"
        with sr_csv.open(newline="", encoding="utf-8") as fh:
            before_rows = list(_csv.DictReader(fh))
        action, flipped, refusal = intake.flip_verified(root, ["SR-001", "LLR-001"])
        assert refusal is None, refusal
        assert action == "flip"
        assert flipped == ["LLR-001", "SR-001"]
        with sr_csv.open(newline="", encoding="utf-8") as fh:
            after_rows = list(_csv.DictReader(fh))
        # ONLY the named row's Status cell moved; every other cell of every
        # row is exactly what it was (cell-exact — and byte-identical on the
        # live registries, where quoting is by necessity; measured).
        for b, a in zip(before_rows, after_rows):
            for col in b:
                if b["SR-ID"] == "SR-001" and col == "Status":
                    assert (b[col], a[col]) == ("Modified", "Verified")
                else:
                    assert b[col] == a[col], (b["SR-ID"], col)
        llr = (root / "docs" / "requirements" / "low-level-requirements.csv").read_text(
            encoding="utf-8"
        )
        assert "Modified" not in llr
        again = intake.flip_verified(root, ["SR-001", "LLR-001"])
        assert again == ("flip", [], None)  # idempotent: nothing left Modified


def test_an_unknown_row_id_refuses_the_flip(tmp_path):
    root = _policy_repo(tmp_path, "autonomous")
    action, flipped, refusal = intake.flip_verified(root, ["SR-999"])
    assert flipped == []
    assert refusal is not None and "SR-999" in refusal


def test_an_unknown_policy_level_fails_toward_recommend(tmp_path):
    # Fail toward the human, never toward a machine ratification.
    root = _policy_repo(tmp_path, "some-future-level")
    action, _flipped, refusal = intake.flip_verified(root, ["SR-001"])
    assert refusal is None, refusal
    assert action == "recommend"
    assert intake.adjudication_action("attended") == "recommend"
    assert intake.adjudication_action("single-ratify") == "flip"
    assert intake.adjudication_action("autonomous") == "flip"
