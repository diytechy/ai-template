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


SN_HEADER = "SN-ID,Need,Why,Acceptance,Status\n"


def write_sn(root, status="Drafted"):
    """The need tier's own carrier row — the tier `APPROVAL_ACT_CSVS` added at
    WI-572 REVIEW-A round 028, and the one the human-approval dial holds."""
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "stakeholder-needs.csv").write_text(
        SN_HEADER + 'SN-001,"the need","why","ac",{}\n'.format(status),
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


def amended_repo(tmp_path, amend, seed=None):
    """A repo whose second commit amends the attested spine per `amend`;
    returns `(root, before_sha, after_sha)`. `seed`, when given, writes extra
    rows into the BASE side, so `amend` reads as a change to an existing row
    rather than as a born one."""
    root = git_repo(tmp_path)
    write_sr(root)
    write_llr(root)
    if seed is not None:
        seed(root)
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


# --- trigger (a2): the Drafted rows a lane hands over -------------------------
#
# Owner ruling 2026-09-01. A work lane authors `Drafted` spine rows and its merge
# is REFUSED if it approves them, so every merge that adds or amends one leaves
# text waiting on an approval nobody gave. The mirror of trigger (a), off the
# same two-tree walk.


def _released(root):
    """Release every spine rung to the loop — the dial state this trigger needs.
    `DevStg-Needs` is what this repo itself runs: the owner holds Needs and
    nothing above it."""
    set_process_key(
        root, "attestation", "human_approval_through", kit_ladder.STAGE_NEEDS
    )


def test_a_drafted_row_mints_one_first_approval_adjudication(tmp_path):
    root, before, after = amended_repo(
        tmp_path, lambda r: write_sr(r, requirement="fresh draft", status="Drafted")
    )
    _released(root)
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "wi-003")
    assert refusal is None, refusal
    assert len(minted) == 1
    wid, relpath = minted[0]
    row = queued_rows(root)[wid]
    assert row["SafetyClass"] == "adjudication"
    # The BRIEF cell is what routes the session (adjudicate_brief.BRIEF_PROMPTS);
    # deriving it from the SpecRef would be ambiguous, so it is typed.
    assert row["Brief"] == "first-approval"
    # ...and the SCOPE cell beside it, which is what stops the brief's live
    # re-derivation from asking a wider question than this merge asked
    # (WI-572 REVIEW-A). Typed for the same reason `Brief` is: the ids are in
    # the Title too, and prose carrying control flow is the WI-417 fold.
    assert row["Adjudicates"] == "SR-001"
    assert "FIRST APPROVAL" in row["Title"] and "SR-001" in row["Title"]
    text = (root / relpath).read_text(encoding="utf-8")
    assert "## Context" in text
    assert "SR-001 amended" in text
    assert "read each row's WHOLE CHAIN" in text  # the outcomes, not just the list
    # ...and the AMENDMENT trigger stayed silent on the same delta: the row left
    # `Approved`, so no approved text moved behind anyone's back.
    assert "meaning-or-clarity" not in text


def test_a_status_only_withdrawal_mints_first_approval_adjudication(tmp_path):
    # Approved -> Drafted refuses no merge because it blesses nothing, but the
    # resulting row is awaiting approval again. The same two-tree reader must
    # therefore hand it to trigger (a2), even when no content cell moved.
    root, before, after = amended_repo(
        tmp_path, lambda r: write_sr(r, status="Drafted")
    )
    _released(root)
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "wi-003")
    assert refusal is None, refusal
    assert len(minted) == 1
    wid, relpath = minted[0]
    assert queued_rows(root)[wid]["Brief"] == "first-approval"
    text = (root / relpath).read_text(encoding="utf-8")
    assert "SR-001 amended" in text


def test_a_lane_flipping_a_STAKEHOLDER_NEED_is_refused_and_mints_nothing(tmp_path):
    """SN is a SPINE tier, so a WORK LANE flipping `SN-001` Drafted -> Approved
    is refused BY NAME (WI-572 REVIEW-A round 028).

    Until this round the refusal walked `SPINE_CSVS` — SR/LLR/TC — only, so the
    one tier the human-approval dial holds for the owner (`DevStg-Needs`, the
    rung THIS repo runs held) was the one a lane could bless on its way past.
    That is the worst case of the act the owner's 2026-09-01 ruling moved to the
    adjudicator, not an exempt one, so `APPROVAL_ACT_CSVS` now adds the need
    registry. The three OFF-SPINE registries stay out — their approval cells are
    OI-30 D3's, not this rung's — and the exhaustiveness pin in
    `tests/test_acceptance_record.py` keeps that boundary a deliberate edit.

    THE REFUSAL IS KEYED TO A WORK LANE'S MERGE, NOT TO THE COMMIT. It is read
    at `integrate._approval_act_refusal` over the merge delta of a branch the
    station is landing, and an adjudication lane is exempted within its recorded
    scope. The owner's own sitting — flipping an SN row by hand in a reviewed
    commit ON TRUNK — never reaches that slot and is unaffected: there is no
    lane merge to refuse. This test therefore drives the reader directly, which
    is the same reading the slot performs, and asserts nothing about a trunk
    commit's admissibility.

    The second half is the dial's: even released of the refusal, no adjudication
    is minted over the flip. Two independent reasons, both intended — the rung
    is HELD here (`human_approval_through = DevStg-Needs`, so the loop may not
    approve needs at all), and the first-approval mint's universe was left at
    `SPINE_CSVS` on purpose, because widening the MINT is a separate decision
    from widening the REFUSAL and this round made only the second."""
    acceptance_record = load_script("acceptance_record")
    root, before, after = amended_repo(
        tmp_path, lambda r: write_sn(r, status="Approved")
    )
    # The base side must carry the Drafted row for this to be a FLIP rather than
    # a born row; `amended_repo` commits its baseline before calling `amend`.
    assert "stakeholder-needs" in "".join(
        p for p, _ in acceptance_record.APPROVAL_ACT_CSVS
    )

    acts = acceptance_record.staged_approval_acts(root, before, after)
    assert [(a["id"], a["act"]) for a in acts] == [("SN-001", "born")], acts
    refusal = acceptance_record.lane_approval_refusal(root, before, after)
    assert refusal and "SN-001" in refusal, refusal
    assert "stakeholder-needs" in refusal
    assert "SN/SR/LLR/TC" in refusal

    # ...and the same flip made on a row that EXISTED Drafted reads as a flip.
    (tmp_path / "flip").mkdir()
    root2, before2, after2 = amended_repo(
        tmp_path / "flip",
        lambda r: write_sn(r, status="Approved"),
        seed=lambda r: write_sn(r, status="Drafted"),
    )
    acts2 = acceptance_record.staged_approval_acts(root2, before2, after2)
    assert [(a["id"], a["act"], a["before"], a["after"]) for a in acts2] == [
        ("SN-001", "flip", "Drafted", "Approved")
    ], acts2
    assert "SN-001" in (
        acceptance_record.lane_approval_refusal(root2, before2, after2) or ""
    )

    # The mint half: held rung, nothing minted. Then released, still nothing —
    # the mint's universe is `SPINE_CSVS`, unchanged by this round.
    set_process_key(
        root2, "attestation", "human_approval_through", kit_ladder.STAGE_NEEDS
    )
    minted, mint_refusal = intake.intake_after_merge(root2, before2, after2, {}, "b")
    assert mint_refusal is None, mint_refusal
    assert minted == []


def test_a_held_rung_mints_no_first_approval_row(tmp_path):
    # The ruling's own boundary, and the half that keeps this from pre-empting a
    # signature the owner owes: the adjudicator acts only on rungs the dial
    # RELEASES. A held tier still surfaces through the approval brief, exactly
    # as it does today, and minting here would either duplicate that surface or
    # invite a session to approve past the human.
    root, before, after = amended_repo(
        tmp_path, lambda r: write_sr(r, requirement="fresh draft", status="Drafted")
    )
    set_process_key(
        root, "attestation", "human_approval_through", kit_ladder.STAGE_RELEASE
    )
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "wi-003")
    assert refusal is None, refusal
    assert minted == []
    # ...and the SAME delta on a released dial does mint, so the silence above
    # is the dial and not an inert trigger.
    _released(root)
    again, refusal2 = intake.intake_after_merge(root, before, after, {}, "wi-003")
    assert refusal2 is None, refusal2
    assert len(again) == 1


def test_the_first_approval_mint_is_one_row_and_idempotent(tmp_path):
    # ONE row per merge however many rows it hands over (the trigger-(a) shape),
    # and the derived title carries the sha pair, so the CLI recovery re-run
    # finds it by exact-title dedup and mints nothing twice.
    def amend(r):
        # The two shapes a lane produces: an existing row amended below
        # approval, and a brand-new decomposition row AUTHORED `Drafted`.
        write_sr(r, requirement="fresh draft", status="Drafted")
        (r / "docs" / "requirements" / "low-level-requirements.csv").write_text(
            LLR_HEADER
            + 'LLR-001,SR-001,Core,src/d.py,f,"the detail","why",TC-001,Approved,'
            "CMP-001,1\n"
            + 'LLR-002,SR-001,Extra,src/e.py,g,"the new detail","why",TC-002,'
            "Drafted,CMP-001,1\n",
            encoding="utf-8",
            newline="\n",
        )

    root, before, after = amended_repo(tmp_path, amend)
    _released(root)
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "b")
    assert refusal is None, refusal
    assert len(minted) == 1
    title = queued_rows(root)[minted[0][0]]["Title"]
    assert "SR-001" in title and "LLR-002" in title

    again, refusal2 = intake.intake_after_merge(root, before, after, {}, "b")
    assert refusal2 is None, refusal2
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

    Scope: only the amended clause; the untouched acceptance arm is excluded.
- a list item the successor must keep as a list item
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
    # The adjudicator's scope prose after the block rides into the minted
    # Context verbatim: the cells alone carry no boundary or exclusion, and a
    # successor whose Context is only the provenance line silently widens or
    # narrows the adjudicated work (WI-544 review round 2, 2026-08-30).
    spec = (root / minted[0][1]).read_text(encoding="utf-8")
    assert "Drafted by WI-008" in spec
    # Verbatim means verbatim: Markdown-significant whitespace (an indented
    # first line, a list item) survives — only the fence-delimiting newlines go
    # (WI-544 review round 3).
    assert (
        "\n    Scope: only the amended clause; the untouched acceptance arm is "
        "excluded.\n- a list item the successor must keep as a list item\n"
    ) in spec


def test_a_drafted_successor_keeps_its_supersedes_lineage_at_the_mint():
    # LLR-161: `supersedes` is the one cell that keeps partial work's thread
    # across the id change. `_draft_row` accepted the key (via `_DRAFT_KEYS`)
    # and the row schema has the column, yet the writer dropped it — WI-545,
    # minted from WI-542's draft on 2026-08-30, carried no lineage at all.
    row = intake._draft_row(
        "WI-999",
        {"title": "successor", "supersedes": "WI-521", "kind": "ordinary"},
    )
    assert row["Supersedes"] == "WI-521"
    assert (
        intake._draft_row("WI-998", {"title": "fresh", "kind": "ordinary"})[
            "Supersedes"
        ]
        == ""
    )


_SUPERSEDING = """
## Deliverable

Adjudicated: WI-005 stopped early; a successor continues the work by another route.

## Dispositions

```toml
title = "Continue the WI-005 work by another route"
workstream = "scripts"
buildtier = "medium"
supersedes = "WI-005"
```
"""


def test_the_mint_replaces_inbound_edges_of_the_superseded_row(tmp_path):
    # OI-73 arm 4: minting a successor carrying `supersedes` REPLACES the
    # superseded row's inbound hard `needs` edges, in the same commit — the
    # WI-541 -> WI-540 strand (a live dependent left waiting on a terminal row)
    # becomes unrepresentable rather than a hand repair.
    root = git_repo(tmp_path)
    write_sr(root)
    write_spec(
        root, "partial", "WI-005", slug="returned", body="\n## Deliverable\n\nstopped\n"
    )
    write_spec(
        root, "queued", "WI-006", slug="dependent", specref="seed.txt", needs=["WI-005"]
    )
    # A soft edge and an unrelated dependent must be left ALONE.
    write_spec(
        root, "queued", "WI-007", slug="soft-dep", specref="seed.txt", needs=["~WI-005"]
    )
    write_spec(
        root,
        "complete",
        "WI-008",
        slug="adjudicate",
        safety_class="adjudication",
        body=_SUPERSEDING,
    )
    _commit(root, "setup", when=T_CODE)
    before = after = _rev(root)
    minted, refusal = intake.intake_after_merge(
        root, before, after, {"WI-008": "merged"}, "wi-008"
    )
    assert refusal is None, refusal
    assert len(minted) == 1
    successor = minted[0][0]
    rows = queued_rows(root)
    # the HARD edge is re-pointed at the successor...
    assert rows["WI-006"]["Predecessors"] == successor
    # ...the SOFT edge is advisory ordering and is left on the terminal row...
    assert rows["WI-007"]["Predecessors"] == "~WI-005"
    # ...and the successor carries the lineage.
    assert rows[successor]["Supersedes"] == "WI-005"


def test_the_mint_repoints_a_multiline_crlf_needs_value_surgically(tmp_path):
    """OI-77: parsed TOML decides the edge even when its source spans lines.

    The source locator must ignore a convincing assignment inside a quoted
    value, retain the comment after the real array, and leave every byte outside
    that one value alone. CRLF is part of that preservation contract.
    """
    root = git_repo(tmp_path)
    write_sr(root)
    write_spec(
        root, "partial", "WI-005", slug="returned", body="\n## Deliverable\n\nstopped\n"
    )
    dependent = write_spec(
        root, "queued", "WI-006", slug="dependent", specref="seed.txt", needs=["WI-005"]
    )
    before = (
        '+++\r\nid = "WI-006"\r\ntitle = "dependent"\r\n'
        'note = """quoted source text:\r\nneeds = ["WI-404"]\r\nend"""\r\n'
        '# the real dependency follows\r\nneeds = [\r\n  "WI-005",\r\n]'
        ' # retain this inline comment\r\nspecref = "seed.txt"\r\n+++\r\n'
        "\r\n## Context\r\n\r\nretain the body exactly\r\n"
    )
    dependent.write_text(before, encoding="utf-8", newline="")
    write_spec(
        root,
        "complete",
        "WI-008",
        slug="adjudicate",
        safety_class="adjudication",
        body=_SUPERSEDING,
    )
    _commit(root, "setup", when=T_CODE)

    minted, refusal = intake.intake_after_merge(
        root, _rev(root), _rev(root), {"WI-008": "merged"}, "wi-008"
    )

    assert refusal is None, refusal
    successor = minted[0][0]
    after = dependent.read_bytes()
    old_value = b'[\r\n  "WI-005",\r\n]'
    expected = before.encode().replace(old_value, '["{}"]'.format(successor).encode())
    assert after == expected
    assert b"\n" not in after.replace(b"\r\n", b"")
    assert queued_rows(root)["WI-006"]["Predecessors"] == successor


def test_parsed_semantics_select_the_quoted_root_key_over_a_nested_key(tmp_path):
    """Quoted keys are valid TOML; a nested namesake is not the root cell."""
    dependent = write_spec(tmp_path, "queued", "WI-006", slug="dependent")
    before = (
        '+++\nid = "WI-006"\ntitle = "dependent"\n"needs" = ["WI-005"]\n'
        '[metadata]\nneeds = ["WI-404"]\n+++\n'
    )
    dependent.write_text(before, encoding="utf-8", newline="")

    changed = intake._replace_inbound_edges(tmp_path, ["WI-005"], ["WI-101"])

    assert changed == [("queued/WI-006-dependent.md", ["WI-005"], [])]
    assert dependent.read_text(encoding="utf-8") == before.replace(
        '"needs" = ["WI-005"]', '"needs" = ["WI-101"]'
    )


def test_a_cr_only_dependency_edit_refuses_before_any_mint_effect(tmp_path):
    """An unlocatable parsed edge refuses without cleaning unrelated work."""
    root = git_repo(tmp_path)
    write_sr(root)
    write_spec(
        root, "partial", "WI-005", slug="returned", body="\n## Deliverable\n\nstopped\n"
    )
    dependent = write_spec(
        root, "queued", "WI-006", slug="dependent", specref="seed.txt", needs=["WI-005"]
    )
    cr_only = dependent.read_text(encoding="utf-8").replace("\n", "\r")
    dependent.write_text(cr_only, encoding="utf-8", newline="")
    write_spec(
        root,
        "complete",
        "WI-008",
        slug="adjudicate",
        safety_class="adjudication",
        body=_SUPERSEDING,
    )
    _commit(root, "setup", when=T_CODE)
    local = root / "unrelated-local-work.txt"
    local.write_text("keep\n", encoding="utf-8")

    minted, refusal = intake.intake_after_merge(
        root, _rev(root), _rev(root), {"WI-008": "merged"}, "wi-008"
    )

    assert minted == []
    assert "CR-only line endings are unsupported" in refusal
    assert local.read_text(encoding="utf-8") == "keep\n"
    assert dependent.read_bytes() == cr_only.encode()
    assert not list((root / "docs/work/queued").glob("WI-009-*.md"))


_CONSOLIDATING = """
## Deliverable

Adjudicated: WI-005, WI-006 and WI-007 overlap; one successor carries all three.

## Dispositions

```toml
title = "One row for the three overlapping scopes"
workstream = "scripts"
buildtier = "medium"
supersedes = ["WI-005", "WI-006", "WI-007"]
```
"""


def test_a_consolidation_re_points_every_dependent_of_every_absorbed_row(tmp_path):
    """The list-valued `supersedes` (2026-09-02 restructure plan §1.5): three
    absorbed rows, two dependents each, ONE successor. Every hard edge lands on
    the successor exactly once, and a dependent that named TWO of the absorbed
    rows carries the successor a single time — the de-duplication is the point,
    because a `needs` list with a repeated token is a malformed row the mint
    would have written itself."""
    root = git_repo(tmp_path)
    write_sr(root)
    for absorbed in ("WI-005", "WI-006", "WI-007"):
        write_spec(
            root, "queued", absorbed, slug="absorbed", specref="seed.txt", needs=[]
        )
    dependents = {
        "WI-010": ["WI-005"],
        "WI-011": ["WI-005"],
        "WI-012": ["WI-006"],
        "WI-013": ["WI-006"],
        "WI-014": ["WI-007"],
        # The sixth names TWO of the absorbed rows at once.
        "WI-015": ["WI-007", "WI-005"],
    }
    for dep, needs in dependents.items():
        write_spec(
            root, "queued", dep, slug="dependent", specref="seed.txt", needs=needs
        )
    # Left ALONE: a soft edge, and a dependent of a row nobody absorbed.
    write_spec(
        root, "queued", "WI-016", slug="soft", specref="seed.txt", needs=["~WI-005"]
    )
    write_spec(
        root, "queued", "WI-017", slug="elsewhere", specref="seed.txt", needs=["WI-016"]
    )
    write_spec(
        root,
        "complete",
        "WI-020",
        slug="consolidate",
        safety_class="adjudication",
        body=_CONSOLIDATING,
    )
    _commit(root, "setup", when=T_CODE)
    before = after = _rev(root)
    minted, refusal = intake.intake_after_merge(
        root, before, after, {"WI-020": "merged"}, "wi-020"
    )
    assert refusal is None, refusal
    assert len(minted) == 1
    successor = minted[0][0]
    rows = queued_rows(root)
    for dep in ("WI-010", "WI-011", "WI-012", "WI-013", "WI-014"):
        assert rows[dep]["Predecessors"] == successor, dep
    # Two absorbed predecessors, ONE successor token — not two.
    assert rows["WI-015"]["Predecessors"] == successor
    assert rows["WI-016"]["Predecessors"] == "~WI-005"
    assert rows["WI-017"]["Predecessors"] == "WI-016"
    # The lineage cell is the `;`-joined list, in the verdict's own order.
    assert rows[successor]["Supersedes"] == "WI-005;WI-006;WI-007"


def test_one_row_split_across_three_successors_repoints_to_all_three(tmp_path, capsys):
    """The topology the live 2026-09-02 restructure actually minted, which the
    one-successor guard above cannot see: ONE absorbed row split across THREE
    successors.

    The dependent must end holding the UNION — the work it was waiting for now
    lives in three places, so waiting on one of them is waiting on a third of
    the contract while the rest sits unblocked. The verdict is therefore
    resolved set-against-set, ONE write per dependent, and the message names
    every successor rather than announcing three separate re-points.

    Three controls make that assertion mean something. A dependent of a row
    nobody absorbed is untouched. A SUCCESSOR is not a dependent even when its
    own `needs` hard-names the absorbed row — re-pointing that edge would hand
    the row a wait on ITSELF that nothing can ever clear and no validator
    reports. And a row that names a successor for its OWN reasons gains
    nothing: "names a sibling" is not evidence of a rewritten edge."""
    root = tmp_path
    write_spec(root, "queued", "WI-005", slug="absorbed", specref="seed.txt", needs=[])
    write_spec(
        root, "queued", "WI-010", slug="dependent", specref="seed.txt", needs=["WI-005"]
    )
    write_spec(
        root, "queued", "WI-011", slug="elsewhere", specref="seed.txt", needs=["WI-010"]
    )
    # Names successor 1 on PURPOSE — it never held an edge on the absorbed row.
    write_spec(
        root, "queued", "WI-012", slug="onpurpose", specref="seed.txt", needs=["WI-101"]
    )
    for successor in ("WI-101", "WI-102", "WI-103"):
        write_spec(
            root,
            "queued",
            successor,
            slug="successor",
            specref="seed.txt",
            # The successor itself still hard-names what it absorbed, and
            # WI-103 additionally names an earlier SIBLING.
            needs=["WI-005"] if successor != "WI-103" else ["WI-005", "WI-101"],
            supersedes="WI-005",
        )
    intake._apply_supersedes(
        root, [(succ, ["WI-005"]) for succ in ("WI-101", "WI-102", "WI-103")]
    )
    rows = queued_rows(root)
    assert rows["WI-010"]["Predecessors"] == "WI-101;WI-102;WI-103"
    assert rows["WI-011"]["Predecessors"] == "WI-010"
    assert rows["WI-012"]["Predecessors"] == "WI-101"
    # A successor never waits on the row it absorbs: the token is DROPPED, not
    # kept (a hard edge onto a row this close archives is a wait nothing clears)
    # and not replaced (that would be an edge onto itself). WI-103's edge onto
    # its sibling WI-101 is ordering it declared, and stays.
    assert rows["WI-101"]["Predecessors"] == ""
    assert rows["WI-102"]["Predecessors"] == ""
    assert rows["WI-103"]["Predecessors"] == "WI-101"
    # ONE message, naming the whole verdict.
    said = [
        line for line in capsys.readouterr().out.splitlines() if "re-pointed" in line
    ]
    assert said == [
        "intake: re-pointed queued/WI-010-dependent.md's edge(s) "
        "WI-005 -> WI-101;WI-102;WI-103"
    ]


def test_a_dependent_of_two_absorbed_rows_ends_with_the_union(tmp_path):
    """Overlapping verdicts: WI-005 goes to WI-101+WI-102, WI-006 to
    WI-102+WI-103, and one dependent names BOTH absorbed rows.

    The two verdicts are different, so they are two writes — and the second
    reads the first one's file. Each replaces only its OWN absorbed tokens, so
    the dependent ends holding the union of the two successor sets with WI-102,
    which is in both, appearing exactly once."""
    root = tmp_path
    for absorbed in ("WI-005", "WI-006"):
        write_spec(
            root, "queued", absorbed, slug="absorbed", specref="seed.txt", needs=[]
        )
    write_spec(
        root,
        "queued",
        "WI-010",
        slug="dependent",
        specref="seed.txt",
        needs=["WI-005", "WI-006"],
    )
    for successor, absorbed in (
        ("WI-101", ["WI-005"]),
        ("WI-102", ["WI-005", "WI-006"]),
        ("WI-103", ["WI-006"]),
    ):
        write_spec(
            root,
            "queued",
            successor,
            slug="successor",
            specref="seed.txt",
            needs=[],
            supersedes=";".join(absorbed),
        )
    intake._apply_supersedes(
        root,
        [
            ("WI-101", ["WI-005"]),
            ("WI-102", ["WI-005", "WI-006"]),
            ("WI-103", ["WI-006"]),
        ],
    )
    assert queued_rows(root)["WI-010"]["Predecessors"] == "WI-101;WI-102;WI-103"


def test_the_mint_handles_new_successors_across_multiple_repoint_groups(tmp_path):
    """Preflight and apply agree when apply also sees canonical new rows."""
    root = git_repo(tmp_path)
    write_sr(root)
    for absorbed in ("WI-005", "WI-006"):
        write_spec(root, "partial", absorbed, slug="returned")
    write_spec(
        root,
        "queued",
        "WI-010",
        slug="dependent",
        specref="seed.txt",
        needs=["WI-005", "WI-006"],
    )
    dispositions = """
## Deliverable

Adjudicated: two returned rows continue across three successors.

## Dispositions

```toml
title = "First WI-005 successor"
supersedes = "WI-005"
needs = ["WI-005"]
```

```toml
title = "Shared successor"
supersedes = ["WI-005", "WI-006"]
needs = ["WI-005", "WI-006"]
```

```toml
title = "Last WI-006 successor"
supersedes = "WI-006"
needs = ["WI-006"]
```
"""
    write_spec(
        root,
        "complete",
        "WI-020",
        slug="adjudicate",
        safety_class="adjudication",
        body=dispositions,
    )
    _commit(root, "setup", when=T_CODE)

    minted, refusal = intake.intake_after_merge(
        root, _rev(root), _rev(root), {"WI-020": "merged"}, "wi-020"
    )

    assert refusal is None, refusal
    successors = [wi_id for wi_id, _rel in minted]
    assert successors == ["WI-021", "WI-022", "WI-023"]
    rows = queued_rows(root)
    assert rows["WI-010"]["Predecessors"] == ";".join(successors)
    assert [rows[wi_id]["Predecessors"] for wi_id in successors] == ["", "", ""]


def test_a_one_id_supersedes_string_is_unchanged_by_the_list_form():
    """The string spelling every disposition writes keeps its exact behaviour —
    one id in, one id in the cell, no list bracket anywhere. The two shapes meet
    in `supersedes_ids` and are indistinguishable after it."""
    one = intake._draft_row(
        "WI-999", {"title": "s", "supersedes": "WI-521", "kind": "ordinary"}
    )
    listed = intake._draft_row(
        "WI-999", {"title": "s", "supersedes": ["WI-521"], "kind": "ordinary"}
    )
    assert one["Supersedes"] == listed["Supersedes"] == "WI-521"
    assert intake.supersedes_ids("WI-521") == ["WI-521"]
    # The WRITER's own form round-trips through the reader: `_draft_row` joins
    # the ids with `;`, and a reader that took that cell back as ONE token would
    # hand `_supersedes_refusal` a value it must reject as "not a WI-### id".
    joined = intake._draft_row(
        "WI-997",
        {"title": "s", "supersedes": ["WI-558", "WI-559"], "kind": "ordinary"},
    )["Supersedes"]
    assert joined == "WI-558;WI-559"
    assert intake.supersedes_ids(joined) == ["WI-558", "WI-559"]
    assert intake._supersedes_refusal(joined, "at", {"WI-558", "WI-559"}) is None
    assert intake.supersedes_ids(["WI-1", "WI-2", "WI-1"]) == ["WI-1", "WI-2"]
    assert intake.supersedes_ids(None) == intake.supersedes_ids("") == []
    assert (
        intake._draft_row("WI-998", {"title": "fresh", "kind": "ordinary"})[
            "Supersedes"
        ]
        == ""
    )


def test_a_supersedes_naming_a_non_wi_token_or_a_dead_row_refuses(tmp_path):
    """Both halves of the lineage refusal. A token that is not a `WI-###` id
    matches no dependent's `needs`, so the re-point is a silent no-op; an id
    that is no live row means the verdict named a row that does not exist, and
    for a CONSOLIDATION that leaves one of the rows it meant to absorb queued
    beside its own successor. Shape is refused where the block is parsed;
    liveness at the mint, which is the rung that holds the registry."""
    at = "docs/work/complete/WI-020-x.md: ## Dispositions block 1"
    shape = intake._draft_refusal(
        {"title": "s", "supersedes": ["WI-005", "the other one"]}, at.split(":")[0], 1
    )
    assert shape is not None and "WI-### id" in shape and "the other one" in shape
    # The same list, all WI-shaped, passes the shape rung...
    assert (
        intake._draft_refusal(
            {"title": "s", "supersedes": ["WI-005", "WI-6"]}, at.split(":")[0], 1
        )
        is None
    )
    # ...and is refused at the mint when one of them is no live row.
    live = intake._mint_shape_refusal(
        {"title": "s", "supersedes": ["WI-005", "WI-006"]},
        "intake at merge of wi-020",
        {"WI-005"},
    )
    assert live is not None and "WI-006" in live and "no live registry row" in live
    assert (
        intake._mint_shape_refusal(
            {"title": "s", "supersedes": ["WI-005", "WI-006"]},
            "intake at merge of wi-020",
            {"WI-005", "WI-006"},
        )
        is None
    )
    # With no registry to read, liveness is not asserted — shape still is.
    assert (
        intake._mint_shape_refusal({"title": "s", "supersedes": ["WI-005"]}, "x")
        is None
    )
    assert intake._mint_shape_refusal({"title": "s", "supersedes": ["nope"]}, "x")


def test_the_authoring_boundary_refuses_a_joined_supersedes_string():
    """The hand-authored `## Dispositions` grammar is the DOCUMENTED one: a
    string names exactly one id, several ids are a TOML list.

    `supersedes_ids` splits on `;` so the cell `_draft_row` WRITES round-trips
    through the reader that refuses it — a machine tolerance. Read at the
    authoring boundary it would silently bless a third spelling beside the two
    `prompts/adjudicate-disposition.template.md` documents, and a grammar with
    an undocumented form is one nobody can check a block against."""
    where = "docs/work/complete/WI-020-x.md"
    joined = intake._draft_refusal(
        {"title": "s", "supersedes": "WI-558;WI-559"}, where, 1
    )
    assert joined is not None and "exactly ONE" in joined and "TOML list" in joined
    comma = intake._draft_refusal({"title": "s", "supersedes": "WI-1, WI-2"}, where, 1)
    assert comma is not None and "exactly ONE" in comma
    # The two documented spellings are untouched.
    assert (
        intake._draft_refusal({"title": "s", "supersedes": "WI-558"}, where, 1) is None
    )
    assert (
        intake._draft_refusal(
            {"title": "s", "supersedes": ["WI-558", "WI-559"]}, where, 1
        )
        is None
    )
    # And a whole block goes the same way, through the real parser.
    _drafts, refusal = intake.parse_dispositions(
        'x\n## Dispositions\n\n```toml\ntitle = "s"\nsupersedes = "WI-558;WI-559"\n```\n',
        where,
    )
    assert refusal is not None and "exactly ONE" in refusal


def test_superseding_an_already_restructured_row_refuses_at_the_mint():
    """Lineage does not CHAIN. A row that is already `restructured` was absorbed
    by somebody else, and continuing it would build A -> B -> C: a reader
    following A's permanent record lands on a second archived row instead of on
    the live thread. The validator refuses to RECORD that shape
    (`_restructured_lineage_findings`); this is the same rule at the authoring
    boundary, where the mint holds the registry that can tell."""
    absorbed = {"WI-005"}
    chained = intake._mint_shape_refusal(
        {"title": "s", "supersedes": ["WI-005"]},
        "intake at merge of wi-020",
        {"WI-005", "WI-006"},
        absorbed,
    )
    assert chained is not None and "ALREADY restructured" in chained
    # A live row, and every other terminal, still passes.
    assert (
        intake._mint_shape_refusal(
            {"title": "s", "supersedes": ["WI-006"]},
            "intake at merge of wi-020",
            {"WI-005", "WI-006"},
            absorbed,
        )
        is None
    )


def test_a_frontmatter_supersedes_list_reads_back_as_the_joined_cell(tmp_path):
    """The read side of the two spellings (restructure plan §1.5): a spec whose
    frontmatter writes `supersedes` as a TOML LIST reads as the `;`-joined cell,
    through the shipped loader AND through the converter — one cell shape, so no
    reader downstream learns a second one. A bare string still reads verbatim."""
    write_spec(
        root := git_repo(tmp_path),
        "queued",
        "WI-030",
        slug="listed",
        supersedes=["WI-005", "WI-006"],
    )
    write_spec(root, "queued", "WI-031", slug="stringy", supersedes="WI-007")
    acommon = load_script("agent_common")
    rows = {r["WI-ID"]: r for r in acommon.read_spec_rows(root / "docs" / "work")}
    assert rows["WI-030"]["Supersedes"] == "WI-005;WI-006"
    assert rows["WI-031"]["Supersedes"] == "WI-007"
    listed = (root / "docs/work/queued/WI-030-listed.md").read_text(encoding="utf-8")
    parsed, _order = wi_convert.parse_spec(listed, "queued/WI-030-listed.md")
    assert parsed["Supersedes"] == "WI-005;WI-006"
    # And a list of NON-strings is still refused, the same as a bare non-string:
    # the tolerance is for the shape, never for what is inside it.
    with pytest.raises(wi_convert.ConvertError):
        wi_convert.parse_spec(
            listed.replace('supersedes = ["WI-005", "WI-006"]', "supersedes = [1, 2]"),
            "queued/WI-030-listed.md",
        )


def _adjudicated_early_close(root, outcome, brief):
    """A merged adjudication row judging an `outcome` (partial/cancelled) close
    that queued NO successor. It models the SELF-close reality: specref is
    CLEARED (the row already moved itself to complete/ following the close
    ritual), so the durable "dispose:" title prefix — not `brief`, not specref —
    is what the refusal invariant reads. `brief=""` models the cancelled arm,
    which is brief-LESS by design and which the old `brief`-only guard missed."""
    write_sr(root)
    kw = {
        "safety_class": "adjudication",
        "title": "dispose: the {} close of WI-005".format(outcome),
        "specref": "",  # the self-close CLEARS specref — the title is the signal
    }
    if brief:
        kw["brief"] = brief
    write_spec(
        root,
        "complete",
        "WI-008",
        slug="adjudicate",
        body="\n## Deliverable\n\nOUTCOME: {} successors=0\n".format(outcome.upper()),
        **kw,
    )
    _commit(root, "merged with no successor", when=T_CODE)


def test_a_disposition_row_with_no_successor_is_refused(tmp_path):
    # OI-70/OI-73 refusal invariant: an adjudication row judging a partial/
    # cancelled close that queues NO successor is refused at the close — an OI
    # alone no longer discharges it, and there is no third exit. The merge
    # stands; the mint refuses and the run stops for a human.
    root = git_repo(tmp_path)
    _adjudicated_early_close(root, "partial", brief="disposition")
    before = after = _rev(root)
    minted, refusal = intake.intake_after_merge(
        root, before, after, {"WI-008": "merged"}, "wi-008"
    )
    assert minted == []
    assert refusal is not None and "successor" in refusal


def test_a_cancelled_close_with_no_successor_is_refused_at_merge(tmp_path):
    # The gap REVIEW-A found: a CANCELLED close mints a brief-LESS adjudication
    # row, so the old `brief == "disposition"` merge guard never fired and it
    # merged silently. The outcome its specref names (`cancelled`) is the signal.
    root = git_repo(tmp_path)
    _adjudicated_early_close(root, "cancelled", brief="")
    before = after = _rev(root)
    minted, refusal = intake.intake_after_merge(
        root, before, after, {"WI-008": "merged"}, "wi-008"
    )
    assert minted == []
    assert refusal is not None and "successor" in refusal


def write_open_items(root):
    """A minimal TOML open-items registry — the carrier the OI mint appends to."""
    path = root / "docs" / "requirements" / "open-items.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# open-items registry\n", encoding="utf-8", newline="\n")
    return path


_HUMAN_OWED = """
## Deliverable

Adjudicated: the remaining question is the owner's to answer.

## Dispositions

```toml
title = "Continue once the owner rules the boundary"
workstream = "scripts"
buildtier = "medium"
supersedes = "WI-005"
open_item = "Does the retention window include partial closes?"
```
"""


def test_the_close_mints_a_pending_oi_that_gates_the_successor(tmp_path):
    # OI-73 exit (B): a human-owed answer becomes a PENDING open item minted
    # from the watermark's OI space, and its id lands in the queued successor's
    # needs — the ruling gates readiness, not adjudicator restraint. No
    # standalone OI exit: the OI is always a dependency of a successor.
    root = git_repo(tmp_path)
    write_sr(root)
    write_open_items(root)
    write_spec(
        root, "partial", "WI-005", slug="returned", body="\n## Deliverable\n\nstopped\n"
    )
    write_spec(
        root,
        "complete",
        "WI-008",
        slug="adjudicate",
        safety_class="adjudication",
        body=_HUMAN_OWED,
    )
    _commit(root, "setup", when=T_CODE)
    before = after = _rev(root)
    minted, refusal = intake.intake_after_merge(
        root, before, after, {"WI-008": "merged"}, "wi-008"
    )
    assert refusal is None, refusal
    assert len(minted) == 1
    successor = minted[0][0]
    # the successor hard-depends on the minted OI id...
    rows = queued_rows(root)
    preds = rows[successor]["Predecessors"]
    assert preds.startswith("OI-"), preds
    # ...and that OI is a real, PENDING row in the registry.
    tr = load_script("trace")
    states = tr.open_item_states(root)
    assert states.get(preds) == "pending"


def test_the_oi_mint_refuses_on_a_non_toml_registry(tmp_path):
    # A downstream repo without a TOML open-items registry keeps its
    # hand-authored path rather than getting a malformed row — the mint refuses
    # loudly (all-or-nothing) instead of writing nowhere.
    root = git_repo(tmp_path)
    write_sr(root)  # no open-items registry at all
    # The row the draft supersedes has to EXIST — the mint's lineage rung refuses
    # a `supersedes` naming no live row, and would otherwise pre-empt the
    # open-items refusal this test is about.
    write_spec(
        root, "partial", "WI-005", slug="returned", body="\n## Deliverable\n\nstopped\n"
    )
    write_spec(
        root,
        "complete",
        "WI-008",
        slug="adjudicate",
        safety_class="adjudication",
        body=_HUMAN_OWED,
    )
    _commit(root, "setup", when=T_CODE)
    before = after = _rev(root)
    minted, refusal = intake.intake_after_merge(
        root, before, after, {"WI-008": "merged"}, "wi-008"
    )
    assert minted == []
    assert refusal is not None and "open-items" in refusal


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
    # `Owner` and `Channel` are the required endpoint/typing cells since OI-67.
    # The `Contract` column stays because it is the LEGACY cell an adopter's
    # registry still carries, and `_seam_lines` falls back to it when a row
    # states no `Data` — this fixture is the only place that fallback runs.
    (req / "interfaces.csv").write_text(
        "IF-ID,Owner,Consumers,Channel,Contract,Version,"
        "Status,Component,Notes\n"
        'IF-001,scripts/widget,scripts/check,cli,"widget CLI: exits 1 on '
        'a bad widget",v1,Approved,CMP-001,\n',
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


def test_an_absorbed_row_is_not_briefed_to_its_successor_as_refuted(tmp_path):
    """The reason the fourth terminal word exists (2026-09-02 restructure plan
    §1.6). `context_block`'s first section tells a later row on the same SRs
    "do not re-propose the refuted" and names each CANCELLED precedent with its
    reason. A consolidation absorbs rows into a successor, so filing an absorbed
    row as `cancelled` would brief the successor against the very scope it was
    minted to carry. The join is keyed on `cancelled` alone, and this is the
    driven proof: same registry, same SRs, one row moved from `cancelled/` to
    `restructured/` — the precedent section goes away."""
    root = context_repo(tmp_path)
    acommon = load_script("agent_common")
    row = next(
        r
        for r in acommon.read_spec_rows(root / "docs" / "work")
        if r["WI-ID"] == "WI-005"
    )
    # The control: as a CANCELLED row, WI-002 is briefed as refuted precedent.
    text = intake.context_block(root, row, None)
    assert "do not re-propose the refuted" in text
    assert "WI-002" in text

    # Re-file the SAME row as restructured — absorbed, not refuted.
    src = root / "docs" / "work" / "cancelled" / "WI-002-refuted.md"
    dest = root / "docs" / "archive" / "work" / "restructured" / "WI-002-refuted.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        src.read_text(encoding="utf-8").replace(
            "cancelled: REFUTED - proposed navigation with no driving necessity",
            "Restructured into WI-005.",
        ),
        encoding="utf-8",
        newline="\n",
    )
    src.unlink()
    rows = acommon.read_spec_rows(root / "docs" / "work")
    assert {r["WI-ID"]: r["Status"] for r in rows}["WI-002"] == "restructured"
    text = intake.context_block(root, row, rows)
    assert "do not re-propose the refuted" not in text, text
    assert "WI-002 (cancelled)" not in text, text


def test_a_restructured_row_mints_no_disposition(tmp_path):
    """A restructure is not a CLOSE, so it owes no judgement: the verdict that
    absorbed the row has already been made and already named the successor, and
    a disposition over it would ask an adjudicator to re-judge a verdict.
    `_closed_spec`'s directory set is the mechanism — `restructured/` is in no
    caller's set — and the sweep's folder→outcome map does not name it either,
    because it is a terminal STATE and not a lane OUTCOME."""
    root = git_repo(tmp_path)
    write_sr(root)
    path = root / "docs" / "archive" / "work" / "restructured" / "WI-005-absorbed.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        spec_text(
            "WI-005",
            safety_class="ordinary",
            body="\n## Deliverable\n\nRestructured into WI-009.\n",
        ),
        encoding="utf-8",
        newline="\n",
    )
    _commit(root, "the consolidation filed WI-005", when=T_CODE)
    # The early-close arm cannot see it at all...
    assert intake._closed_spec(root, "WI-005") is None
    # ...nor can the clean-close spot check, and the sweep names three folders.
    assert intake._closed_spec(root, "WI-005", dirs=("complete",)) is None
    assert "restructured" not in intake.SWEEP_OUTCOMES
    # ...but the id IS taken: the mint sweeps both roots, so the watermark can
    # never re-issue a number an absorbed row still holds.
    assert intake.next_wi_id(root) == "WI-006"


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


def test_a_declaration_header_on_the_csv_carrier_still_locates_the_row(tmp_path):
    """OI-67: a registry CSV may open with a `#` declaration header, and the ONE
    comment-skipping reader (`kitlib.spine.csv_body`) strips it before the header
    row for every kit loader. This locator read its CSV carrier RAW, so the
    comment's first line became `rows[0]` — no `Status` column in it, every
    staged row read as ABSENT, and the brief reported nothing to adjudicate over
    a registry that stages two rows."""
    root = _policy_repo(tmp_path, kit_stage.BELOW)
    sr_csv = root / "docs" / "requirements" / "system-requirements.csv"
    plain, _ = intake._locate_spine_rows(root, {"SR-001", "SR-002"})
    sr_csv.write_text(
        "# the system-requirements registry — the OI-67 declaration header\n"
        "# Contracts: IF-999\n"
        "\n" + sr_csv.read_text(encoding="utf-8"),
        encoding="utf-8",
        newline="\n",
    )
    located, tables = intake._locate_spine_rows(root, {"SR-001", "SR-002"})
    assert sorted(located) == ["SR-001", "SR-002"]
    rel, status, row, status_ix = located["SR-001"]
    assert status == "Drafted" and row[0] == "SR-001" and row[status_ix] == "Drafted"
    # ...the header the locator indexed is the REAL one, not the comment...
    assert tables[rel][1][0][0] == "SR-ID"
    # ...and the answer is identical to the same registry without the header.
    assert {k: v[:2] for k, v in located.items()} == {
        k: v[:2] for k, v in plain.items()
    }


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


def test_a_row_that_absorbed_a_sibling_is_still_re_pointed_for_the_rest(tmp_path):
    """Round-3 finding: the non-dependent decision is PER TOKEN, not per row.
    WI-050 absorbed WI-006 and hard-needs WI-005; WI-100 absorbs both. WI-050
    is not a dependent for WI-006 (dropped) but IS one for WI-005 (re-pointed
    to WI-100) - left alone, it would wait on a row this close archives."""
    root = tmp_path
    for absorbed in ("WI-005", "WI-006"):
        write_spec(
            root, "queued", absorbed, slug="absorbed", specref="seed.txt", needs=[]
        )
    write_spec(
        root,
        "queued",
        "WI-050",
        slug="half-sibling",
        specref="seed.txt",
        needs=["WI-005", "WI-006"],
        supersedes="WI-006",
    )
    write_spec(
        root,
        "queued",
        "WI-100",
        slug="successor",
        specref="seed.txt",
        needs=[],
        supersedes="WI-005;WI-006",
    )
    intake._apply_supersedes(root, [("WI-100", ["WI-005", "WI-006"])])
    assert queued_rows(root)["WI-050"]["Predecessors"] == "WI-100"


def test_the_re_point_message_names_only_the_edges_the_row_held(tmp_path, capsys):
    """Round-3 finding: the announcement names the tokens THIS row carried,
    never the whole absorbed group."""
    root = tmp_path
    for absorbed in ("WI-005", "WI-006"):
        write_spec(
            root, "queued", absorbed, slug="absorbed", specref="seed.txt", needs=[]
        )
    write_spec(
        root, "queued", "WI-010", slug="dependent", specref="seed.txt", needs=["WI-005"]
    )
    write_spec(
        root,
        "queued",
        "WI-101",
        slug="successor",
        specref="seed.txt",
        needs=[],
        supersedes="WI-005;WI-006",
    )
    intake._apply_supersedes(root, [("WI-101", ["WI-005", "WI-006"])])
    said = [
        line for line in capsys.readouterr().out.splitlines() if "re-pointed" in line
    ]
    assert said == [
        "intake: re-pointed queued/WI-010-dependent.md's edge(s) WI-005 -> WI-101"
    ]


def test_a_joined_string_inside_a_list_is_refused_at_the_authoring_boundary():
    """Round-3 finding: the strict authoring grammar applies to every string,
    inside a list too - `["WI-558;WI-559"]` is the joined spelling in a hat."""
    refusal = intake._authored_supersedes_refusal(["WI-558;WI-559"], "at")
    assert refusal and "exactly ONE WI-### id per string" in refusal
    assert intake._authored_supersedes_refusal(["WI-558", "WI-559"], "at") is None


# --- the consolidation cells and their lineage refusal (restructure plan §1.3) --


def test_the_mint_writes_the_digests_cell_the_census_computes():
    """The recursion guard is a CELL. A cell the census computes and the writer
    drops is a guard that never holds: every idle tick would read "nobody has
    judged this queue state" and mint the same row again."""
    row = intake._draft_row(
        "WI-042",
        {
            "title": "adjudicate queue overlap",
            "kind": "adjudication",
            "brief": "consolidate",
            "adjudicates": ["WI-010", "WI-011"],
            "digests": "aaaa1111bbbb|cccc2222dddd",
        },
    )
    assert row["Digests"] == "aaaa1111bbbb|cccc2222dddd"
    assert row["Brief"] == "consolidate"
    assert row["Adjudicates"] == "WI-010;WI-011"
    # ...and empty on a draft that names none, never a placeholder.
    assert intake._draft_row("WI-043", {"title": "ordinary"})["Digests"] == ""


def test_the_mint_refuses_a_draft_that_absorbs_a_consolidations_own_successor():
    """`_supersedes_refusal`'s absorbed arm and this one are DIFFERENT failures
    and neither substitutes: that one refuses CONTINUING a row somebody already
    absorbed (a lineage chain), this refuses ABSORBING a row an earlier
    consolidation MINTED — overturning that judgement, which is a
    RETURN-TO-DRAFT for the owner and never a second machine mint."""
    registry = [
        {"WI-ID": "WI-005", "Status": "restructured", "Supersedes": "", "Title": "a"},
        {"WI-ID": "WI-101", "Status": "queued", "Supersedes": "WI-005", "Title": "b"},
        {"WI-ID": "WI-102", "Status": "queued", "Supersedes": "", "Title": "c"},
    ]
    ok = [{"title": "fine", "supersedes": ["WI-102"]}]
    assert intake._pre_mint_refusal(ok, "the census", registry) is None
    bad = [{"title": "overturn", "supersedes": ["WI-101"]}]
    refusal = intake._pre_mint_refusal(bad, "the census", registry)
    assert refusal and "WI-101" in refusal and "RETURN-TO-DRAFT" in refusal
    assert "the census" in refusal


# --- the `sweep` CLI: a range sweep is the merge slot's call, not a repo scan --
#
# The supervising session's out-of-band range (2026-09-04) could not use this
# subcommand: a bare sweep also walks the three terminal folders, so on a repo
# with years of closes under docs/archive/work/* every one of them was
# reconsidered on top of a two-commit range. The range shape now runs triggers
# (a)/(a2) and nothing else; `--with-terminal` asks the scan back.


def sweep_repo(tmp_path):
    """`(root, before, after)`: a trunk whose range amends an approved SR, and
    which ALSO carries - outside that range - a handed-back spec in `partial/`
    owed a disposition. The two populations a sweep must keep apart."""
    root, before, after = amended_repo(
        tmp_path, lambda r: write_sr(r, requirement="the AMENDED text")
    )
    write_spec(root, "partial", "WI-005", slug="returned", specref="seed.txt")
    write_close_report(root, "WI-005", "wi-005", tier="strong")
    _commit(root, "an early close, landed after the range", when=T_LATER)
    return root, before, after


def _sweep(root, *extra):
    return intake.main(["--root", str(root), "sweep", *extra])


def _minted_specrefs(root):
    return {r["SpecRef"].replace("\\", "/") for r in queued_rows(root).values()}


def _adjudications(root):
    return [r for r in queued_rows(root).values() if r["SafetyClass"] == "adjudication"]


def _subject(root):
    return _git(root, "log", "-1", "--pretty=%s")


def test_a_range_sweep_mints_the_range_and_touches_no_terminal_folder(tmp_path, capsys):
    root, before, after = sweep_repo(tmp_path)
    assert _sweep(root, "--before", before, "--after", after) == 0
    out = capsys.readouterr().out
    minted = _adjudications(root)
    # The mint's own per-row line, then the count — no second listing.
    assert "minted {} at".format(minted[0]["WI-ID"]) in out
    assert "sweep minted 1 row(s)." in out
    assert len(minted) == 1, [r["Title"] for r in minted]
    assert "SR-001" in minted[0]["Title"]
    # The terminal population is UNJUDGED: no disposition points at the
    # handed-back spec, which the bare sweep would have minted.
    assert not any("work/partial/WI-005" in ref for ref in _minted_specrefs(root))
    # The default mint subject names the range, not a branch.
    assert "sweep {}..{}".format(before, after) in _subject(root)


def test_a_range_sweep_run_twice_mints_nothing_the_second_time(tmp_path, capsys):
    root, before, after = sweep_repo(tmp_path)
    assert _sweep(root, "--before", before, "--after", after) == 0
    capsys.readouterr()
    assert _sweep(root, "--before", before, "--after", after) == 0
    assert "nothing to mint." in capsys.readouterr().out
    assert len(_adjudications(root)) == 1


def test_with_terminal_asks_the_terminal_scan_back(tmp_path):
    root, before, after = sweep_repo(tmp_path)
    assert _sweep(root, "--before", before, "--after", after, "--with-terminal") == 0
    assert len(_adjudications(root)) == 2
    assert any("work/partial/WI-005" in ref for ref in _minted_specrefs(root))


def test_a_custom_branch_label_names_the_mint_subject(tmp_path):
    root, before, after = sweep_repo(tmp_path)
    argv = ("--before", before, "--after", after, "--branch", "oob-lane")
    assert _sweep(root, *argv) == 0
    assert "oob-lane" in _subject(root)


def test_a_bare_sweep_still_walks_the_terminal_folders(tmp_path, capsys):
    root, _before, _after = sweep_repo(tmp_path)
    assert _sweep(root) == 0
    assert "sweep minted 1 row(s)." in capsys.readouterr().out
    assert any("work/partial/WI-005" in ref for ref in _minted_specrefs(root))
