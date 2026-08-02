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
