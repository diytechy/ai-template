"""Phase-anchor and approval-brief decisions from check_trajectory.

Split byte-for-byte from ``test_trajectory_arch`` at WI-545's phase behavior
boundary. The architecture seam/component rules stay in the source module;
phase-event and phase-approval evidence lives here.

check_vocab: allow-file — phase fixtures intentionally exercise the retired
``[phase]-[g1|g2|reqs|tests]`` read spellings beside the canonical rung form.
"""

import sys

from conftest import SCRIPTS, load_script

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from kitlib import stage as kitstage  # noqa: E402

# --- WI-093: the phase-anchor archetype + phase-drop detector ------------------
# The derived-gate model (docs/archive/specs/derived-gate-model.2026-07-20.md
# §7/§9.3): a phase's pre-dev batch is a WI whose Title carries a phase-anchor
# tag; the phase reading BELOW the rung its closed anchor recorded warns to open
# a new phase-anchor WI. RE-KEYED TO THE STAGE AXIS by WI-498 slice 4 — the
# anchor records a LADDER RUNG and the current reading comes from `docs/stage`'s
# `per-phase-live`. All warn-first; the logic is unit-tested via load_script.


def _wis(ct, rows):
    return ct.load_wis(rows)[0]


def test_phase_anchors_parse_and_duplicate_warn():
    ct = load_script("check_trajectory")
    wis = _wis(
        ct,
        [
            {
                "WI-ID": "WI-201",
                "Title": "[v2]-[g1] structure v2 reqs",
                "Status": "done",
            },
            {
                "WI-ID": "WI-202",
                "Title": "[v2]-[g2] decompose v2",
                "Predecessors": "WI-201",
                "Status": "queued",
            },
            {
                "WI-ID": "WI-203",
                "Title": "[v2]-[g2] a duplicate g2",
                "Status": "queued",
            },
            {"WI-ID": "WI-204", "Title": "an ordinary WI", "Status": "queued"},
        ],
    )
    anchors, warns = ct.phase_anchors(wis)
    assert ("v2", "DevStg-LLReqs") in anchors and ("v2", "DevStg-Impl") in anchors
    assert anchors[("v2", "DevStg-Impl")]["id"] == "WI-202"  # first wins
    # The RETIRED `[phase]-[g2]` spelling still PARSES (the ~20 committed anchors
    # carry it and D-4 refuses re-pointing history), but the message names the
    # CANONICAL spelling, because what it is asking for is a NEW row.
    assert any("duplicate phase anchor [v2]-[DevStg-Impl]" in w for w in warns)


def test_the_CANONICAL_anchor_spelling_parses_to_the_same_rungs():
    """Both retired spellings and the canonical one land on ONE rung per level,
    or a phase would carry two independent anchor sets.

    THE TRANSLATION IS BY MEANING AND THE SPELLINGS ARE A TRAP, which is the
    whole reason this is a table and not a string manipulation: `[p]-[reqs]`
    records `DevStg-LLReqs` (the rung the phase stands at once its requirements
    are approved), NOT `DevStg-Reqs` (the rung it has just left), and
    `[p]-[tests]` records `DevStg-Impl`, NOT `DevStg-Tests`. Both are off by two
    rungs from the spelling, in the direction that would make the detector fire
    on healthy phases."""
    ct = load_script("check_trajectory")
    wis = _wis(
        ct,
        [
            {"WI-ID": "WI-301", "Title": "[v9]-[reqs] structure", "Status": "done"},
            {
                "WI-ID": "WI-302",
                "Title": "[v9]-[tests] decompose",
                "Predecessors": "WI-301",
                "Status": "queued",
            },
        ],
    )
    anchors, warns = ct.phase_anchors(wis)
    assert set(anchors) == {("v9", "DevStg-LLReqs"), ("v9", "DevStg-Impl")}
    assert warns == []
    # The canonical form is the rung itself, and it lands on the same keys.
    canonical = _wis(
        ct,
        [
            {
                "WI-ID": "WI-321",
                "Title": "[v9]-[DevStg-LLReqs] structure",
                "Status": "done",
            },
            {
                "WI-ID": "WI-322",
                "Title": "[v9]-[DevStg-Impl] decompose",
                "Predecessors": "WI-321",
                "Status": "queued",
            },
        ],
    )
    canon_anchors, canon_warns = ct.phase_anchors(canonical)
    assert set(canon_anchors) == set(anchors)
    assert canon_warns == []
    # ...and a phase spelled BOTH ways is one anchor set, so the changeover
    # collision is caught rather than silently doubling the phase's anchors.
    mixed = _wis(
        ct,
        [
            {"WI-ID": "WI-311", "Title": "[v9]-[g1] old", "Status": "done"},
            {"WI-ID": "WI-312", "Title": "[v9]-[reqs] new", "Status": "queued"},
        ],
    )
    _, mixed_warns = ct.phase_anchors(mixed)
    assert any("duplicate phase anchor [v9]-[DevStg-LLReqs]" in w for w in mixed_warns)


def test_a_phase_anchor_naming_no_rung_at_all_warns_rather_than_parsing():
    """The canonical form admits any `DevStg-*` token, so the token set is no
    longer closed by the regex — a title naming a rung this ladder does not have
    must be REFUSED loudly, not folded into some neighbour."""
    ct = load_script("check_trajectory")
    wis = _wis(
        ct,
        [{"WI-ID": "WI-331", "Title": "[v9]-[DevStg-Nonsense] x", "Status": "done"}],
    )
    anchors, warns = ct.phase_anchors(wis)
    assert anchors == {}
    assert any("is not a rung on the stage ladder" in w for w in warns)


def test_phase_anchor_higher_rung_without_lower_predecessor_warns():
    ct = load_script("check_trajectory")
    wis = _wis(
        ct,
        [
            {"WI-ID": "WI-201", "Title": "[v3]-[g1] x", "Status": "done"},
            {"WI-ID": "WI-202", "Title": "[v3]-[g2] y", "Status": "queued"},  # no pred
        ],
    )
    _, warns = ct.phase_anchors(wis)
    assert any("does not list its [v3]-[DevStg-LLReqs]" in w for w in warns)


def _write_stage(root, per_phase_live, stage="DevStg-Impl"):
    """A `docs/stage` carrying `per_phase_live`, written through the REAL
    renderer so the fixture cannot drift from the parser."""
    (root / "docs").mkdir(parents=True, exist_ok=True)
    record = {
        "stage": stage,
        "stage-ord": kitstage.order(stage),
        "stage-of": 8,
        "floored": False,
        "settled-stage": stage,
        "live-stage": stage,
        "phase": 1,
        "per-phase": dict(per_phase_live),
        "per-phase-live": dict(per_phase_live),
        "drafted": 0,
        "fingerprint": "sha256:" + "0" * 64,
    }
    (root / "docs" / "stage").write_text(
        kitstage.render(record, "abc1234", "2026-08-21"),
        encoding="utf-8",
        newline="\n",
    )


def _pin_reader(monkeypatch, root):
    """Short-circuit the common reader to the RECORDED values of the fixture.

    The detector reads through `derive_stage.read`, which recomputes the
    fingerprint over the declared inputs and derives fresh on a miss — correct in
    production and useless for a fixture that wants to state a per-phase reading
    directly. Patching that ONE call is the seam; the file format, the parse and
    the comparison are all real."""
    derive_stage = load_script("derive_stage")
    text = (root / "docs" / "stage").read_text(encoding="utf-8")
    monkeypatch.setitem(sys.modules, "derive_stage", derive_stage)
    monkeypatch.setattr(derive_stage, "read", lambda _root: kitstage.parse(text))


def test_phase_drop_detector_warns(tmp_path, monkeypatch):
    ct = load_script("check_trajectory")
    # v2 closed at [g2] (recorded reach DevStg-Impl) but v2 now reads
    # DevStg-Tests — a TC went back to Drafted, i.e. reopened content.
    _write_stage(tmp_path, {"v1": "DevStg-Impl", "v2": "DevStg-Tests"})
    _pin_reader(monkeypatch, tmp_path)
    wis = _wis(
        ct,
        [
            {"WI-ID": "WI-210", "Title": "[v2]-[g1] x", "Status": "done"},
            {
                "WI-ID": "WI-211",
                "Title": "[v2]-[g2] y",
                "Predecessors": "WI-210",
                "Status": "done",
            },
        ],
    )
    warns = ct.phase_findings(tmp_path, wis)
    assert any(
        "phase 'v2' dropped to DevStg-Tests" in w and "[v2]-[DevStg-Impl]" in w
        for w in warns
    ), warns
    # Back at DevStg-Impl: no drop warn (the phase re-earned its anchor's reach).
    _write_stage(tmp_path, {"v1": "DevStg-Impl", "v2": "DevStg-Impl"})
    _pin_reader(monkeypatch, tmp_path)
    assert ct.phase_findings(tmp_path, wis) == []


def test_phase_findings_vacuous_without_anchors(tmp_path, monkeypatch):
    ct = load_script("check_trajectory")
    # a phase below every rung but NO anchor records a close
    _write_stage(tmp_path, {"v1": "DevStg-Below"})
    _pin_reader(monkeypatch, tmp_path)
    wis = _wis(ct, [{"WI-ID": "WI-220", "Title": "ordinary", "Status": "queued"}])
    assert ct.phase_findings(tmp_path, wis) == []


# --- WI-146(b): the approval-brief hierarchy-view lint --------------------
# An open-items ROW whose decision is a `[phase]-[g1|g2]` approval should
# name the generated batch-scoped hierarchy view rather than hand-copy rows.
# Warn-first (never a gate fail); vacuous without such a brief. WI-322 moved the
# briefs from markdown sections into `docs/requirements/open-items.csv`, so the
# lint reads rows and the evidence it accepts is a view PATH in the cell.

_OI_HEADER = (
    "OI-ID,Title,Status,Raised,OneLine,Decision,BlastRadius,Options,"
    "Recommendation,WI-Refs,RuledDate,RulingRef\n"
)


def _write_open_items(root, rows):
    (root / "docs" / "requirements").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "requirements" / "open-items.csv").write_text(
        _OI_HEADER + rows, encoding="utf-8"
    )
    return root


def _oi_row(oid, decision, title="a decision", status="pending"):
    return '{},{},{},,,"{}",,,,,,\n'.format(oid, title, status, decision)


def test_approval_brief_without_view_warns(tmp_path):
    ct = load_script("check_trajectory")
    _write_open_items(
        tmp_path,
        _oi_row("OI-20", "approve the [v3]-[g2] dashboard batch.")
        + _oi_row("OI-21", "something else, no anchor here."),
    )
    warns = ct.approval_brief_findings(tmp_path)
    # Exactly the approval brief warns; the unrelated row does not.
    assert len(warns) == 1
    assert warns[0].startswith("OI-20:")
    assert "hierarchy view" in warns[0]


def test_approval_brief_with_generator_command_only_warns(tmp_path):
    # A bare `trace.py --approve` command mention is NOT proof the view exists and
    # is carried — the brief must name the generated view (WI-146 REVIEW-A).
    ct = load_script("check_trajectory")
    _write_open_items(
        tmp_path,
        _oi_row(
            "OI-20",
            "approve the [v3]-[g2] batch. Hierarchy: run trace.py --approve v3.",
        ),
    )
    warns = ct.approval_brief_findings(tmp_path)
    assert len(warns) == 1 and warns[0].startswith("OI-20:")


def test_approval_brief_with_view_link_is_silent(tmp_path):
    ct = load_script("check_trajectory")
    _write_open_items(
        tmp_path,
        _oi_row(
            "OI-20", "approve the [v3]-[g2] batch. See the tree: docs/ratify/v3-g2.md."
        ),
    )
    assert ct.approval_brief_findings(tmp_path) == []


def test_approval_brief_lint_is_vacuous_off_the_pending_queue(tmp_path):
    ct = load_script("check_trajectory")
    # No registry at all -> nothing to check.
    assert ct.approval_brief_findings(tmp_path) == []
    # An approval word with no [phase]-[g*] anchor -> not a brief.
    _write_open_items(tmp_path, _oi_row("OI-30", "whether to approve a policy change."))
    assert ct.approval_brief_findings(tmp_path) == []
    # ...an anchor with no approval language -> also not a brief.
    _write_open_items(tmp_path, _oi_row("OI-31", "sequence [v3]-[g2] after v2 work."))
    assert ct.approval_brief_findings(tmp_path) == []
    # ...and a RULED row is history, not a pending decision, so it never warns
    # even when it carries both (the negative half WI-322 added).
    _write_open_items(
        tmp_path,
        _oi_row("OI-32", "approve the [v3]-[g2] batch.", status="ruled"),
    )
    assert ct.approval_brief_findings(tmp_path) == []
