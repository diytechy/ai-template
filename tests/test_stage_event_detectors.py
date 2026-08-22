"""The two EVENT detectors, re-keyed to the stage axis — the DECISIONS
(WI-498 slice 4).

The ruled plan's §5 item 4, and the design record's §2.5 finding that made it a
slice rather than a second axis: *the clearance-needing behaviours reduce to
events plus one derivation rule* — the phase-drop detector and the tier signal
both need the HISTORY of one value, not a second vocabulary.

Two detectors, two very different starting conditions:

  * **the phase-drop detector** worked, on the bar axis, and had to be re-keyed
    without inventing signal it cannot have. Its hard questions are the ANCHOR
    TRANSLATION — a closed anchor records a level in a retired vocabulary whose
    spellings OVERLAP the ladder's, two rungs off in both rows — and the
    ABSTENTION, because three of the eight rungs are decided repo-wide and a
    per-phase reading landing on one of them is unattributable.
  * **the tier signal was DEAD** and had been since the derived-gate migration
    (queued as WI-497, folded here). It read `splitlines()[0]` of `docs/gate` —
    the static header — so it answered False unconditionally and
    `tier_signal`'s `strong` arm was unreachable.

THIS MODULE IS THE IN-PROCESS HALF and stays in the commit bar by the
in-process default. Its sibling `test_stage_event_detectors_driven.py` carries
everything that needs a real bootstrapped scaffold or a real git repo — the
`test_kitlib_stage` / `test_derive_stage` split of slice 1, applied again for
the same declared reason.
"""

import sys

from conftest import SCRIPTS, load_script

# `kitlib` is a PACKAGE UNDER scripts/, which nothing puts on `sys.path` until
# the first `load_script` call — so a module-level `from kitlib import ...` in a
# test file resolves only when some earlier-collected module happens to have
# called it first. That held by accident until an xdist worker collected this
# module first (WI-498 slice 4). Stated explicitly here rather than inherited.
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from kitlib import ladder, stage as kitstage  # noqa: E402

CT = load_script("check_trajectory")
DS = load_script("derive_stage")
AC = load_script("agent_common")


# --- THE ANCHOR TRANSLATION ---------------------------------------------------
def test_the_anchor_translation_is_by_MEANING_and_the_spellings_are_the_trap():
    """The one decision in this slice a mechanical re-key would have got wrong.

    `_ANCHOR_REACH` maps a closed anchor's token to the rung the phase STANDS AT
    once that anchor closes. Both legacy tokens share a spelling with a ladder
    rung and neither means it:

      `[p]-[reqs]`  requirement structuring — the phase's SRs are authored AND
                    ratified, which clears `spine_stage`'s `any(is_drafted(sr))`
                    test. The phase has just LEFT DevStg-Reqs; where it lands is
                    DevStg-LLReqs, two rungs up.
      `[p]-[tests]` decomposition — LLRs and TCs authored and non-Drafted, which
                    clears the LLReqs AND Tests predicates. The phase lands on
                    DevStg-Impl, one rung above the Tests spelling.

    Taking the spelling would have recorded a reach BELOW the phase's real
    standing, which makes the drop detector under-report — the direction that
    loses the event the detector exists for. This is the deep-check's own warning
    ("three spellings are shared between the axes, so a mechanical remap is
    unsafe") reduced to a table."""
    assert CT._ANCHOR_REACH["reqs"] == ladder.STAGE_LLREQS
    assert CT._ANCHOR_REACH["g1"] == ladder.STAGE_LLREQS
    assert CT._ANCHOR_REACH["tests"] == ladder.STAGE_IMPL
    assert CT._ANCHOR_REACH["g2"] == ladder.STAGE_IMPL
    # ...and the shared spellings are exactly what it does NOT map to.
    assert CT._ANCHOR_REACH["reqs"] != ladder.STAGE_REQS
    assert CT._ANCHOR_REACH["tests"] != ladder.STAGE_TESTS


def test_the_legacy_anchors_are_TRANSLATED_not_re_recorded():
    """A phase anchor is a WI TITLE — the committed record of what a closed work
    item did — so the retired spellings are accepted forever on the READ side
    and the canonical rung spelling is what a new row takes. Same treatment the
    `g1`/`g2` changeover already gave, one generation on."""
    for token in ("g1", "g2", "reqs", "tests"):
        assert CT.PHASE_ANCHOR_RE.match("[v1]-[{}] x".format(token)), token
    for rung in ladder.STAGE_ORDER:
        assert CT.PHASE_ANCHOR_RE.match("[v1]-[{}] x".format(rung)), rung
        assert CT._anchor_reach(rung) == rung
    # Titles are prose, so the regex is case-insensitive; the reach folds back
    # onto the canonical spelling rather than being handed to `require_rung`,
    # which is deliberately exact.
    assert CT._anchor_reach("devstg-impl") == ladder.STAGE_IMPL
    assert CT._anchor_reach("DevStg-Nope") is None


def test_the_two_anchor_patterns_accept_THE_SAME_TOKEN_SET():
    """`PHASE_ANCHOR_RE` (anchored at a Title's start) and `RATIFY_ANCHOR_RE`
    (mid-cell, for the brief lint) are deliberately separate patterns over one
    vocabulary. Held equal here rather than by a comment, because the comment is
    what drifted at the last changeover."""
    tokens = ["g1", "g2", "reqs", "tests"] + list(ladder.STAGE_ORDER)
    for token in tokens:
        title = "[v1]-[{}] x".format(token)
        assert bool(CT.PHASE_ANCHOR_RE.match(title)) is bool(
            CT.RATIFY_ANCHOR_RE.search("... {} ...".format(title))
        ), token


# --- THE LIVE-VS-SETTLED SPLIT ------------------------------------------------
def _stage_file(root, per_phase, per_phase_live, stage=ladder.STAGE_IMPL):
    (root / "docs").mkdir(parents=True, exist_ok=True)
    record = {
        "stage": stage,
        "stage-ord": kitstage.order(stage),
        "stage-of": ladder.STAGE_OF,
        "floored": False,
        "settled-stage": stage,
        "live-stage": stage,
        "phase": 1,
        "per-phase": dict(per_phase),
        "per-phase-live": dict(per_phase_live),
        "drafted": 1,
        "fingerprint": "sha256:" + "0" * 64,
    }
    (root / "docs" / "stage").write_text(
        kitstage.render(record, "abc1234", "2026-08-21"), encoding="utf-8"
    )
    return record


def _pin_reader(monkeypatch, record):
    import sys

    monkeypatch.setitem(sys.modules, "derive_stage", DS)
    monkeypatch.setattr(DS, "read", lambda _root: record)


def _closed_anchor(phase="v1", token="g2"):
    return CT.load_wis(
        [
            {
                "WI-ID": "WI-401",
                "Title": "[{}]-[{}] decompose".format(phase, token),
                "Status": "done",
            }
        ]
    )[0]


def test_the_detector_reads_the_LIVE_per_phase_field_not_the_settled_one(
    tmp_path, monkeypatch
):
    """THE DESIGN DECISION OF THIS HALF OF THE SLICE, driven from both sides.

    This is an EVENT detector: the event is "new or reopened content entered a
    phase whose anchor is closed", and a Drafted or re-Drafted row IS that event.
    The headline `stage` / `per-phase` fields exclude drafts BY CONSTRUCTION —
    slice 1's C-01 fix, which exists precisely so one draft cannot collapse
    SELECTION — so keying detection on them would make the detector blind to
    exactly its own subject.

    The fixture states the divergence the two fields exist to carry: settled says
    the phase is still at Impl (nothing ratified has moved), live says it is back
    at Tests (a TC is in redraft). Keying on `per-phase` finds nothing; keying on
    `per-phase-live` finds the event."""
    settled = {"v1": ladder.STAGE_IMPL}
    live = {"v1": ladder.STAGE_TESTS}
    record = _stage_file(tmp_path, settled, live)
    _pin_reader(monkeypatch, record)
    warns = CT.phase_findings(tmp_path, _closed_anchor())
    assert any("dropped to DevStg-Tests" in w for w in warns), warns

    # The counterfactual: had it read the SETTLED field, the same tree is silent.
    record_settled_only = dict(record, **{"per-phase-live": settled})
    _pin_reader(monkeypatch, record_settled_only)
    assert CT.phase_findings(tmp_path, _closed_anchor()) == []


def test_SELECTION_still_reads_the_settled_value(tmp_path, monkeypatch):
    """The other half of the split, stated so the two cannot be conflated later:
    the detector's move to the live reading changes nothing about what SELECTS
    checks. `phase_stages` reads `per-phase-live`; the headline `stage` the
    harness keys on is untouched by it."""
    record = _stage_file(
        tmp_path, {"v1": ladder.STAGE_IMPL}, {"v1": ladder.STAGE_TESTS}
    )
    _pin_reader(monkeypatch, record)
    assert CT.phase_stages(tmp_path) == {"v1": ladder.STAGE_TESTS}
    assert record["stage"] == ladder.STAGE_IMPL


# --- THE ABSTENTION -----------------------------------------------------------
def test_a_repo_global_rung_makes_the_detector_ABSTAIN_and_SAY_SO(
    tmp_path, monkeypatch
):
    """The only part of the re-key that is not a direct translation.

    `DevStg-Arch` is decided by the repo's COMPONENT registry, which is passed
    whole to every per-phase call, so when a phase reads it EVERY phase reads it
    and none of them is reporting anything about its own content. Concluding "new
    or reopened content entered phase v1" from that value would be a fabricated
    attribution — arithmetically true, causally invented.

    And it says so. The schedule map's standing criticism of this detector was
    that it "silently drops what it cannot parse", going vacuous where a reader
    would assume it was clean; an abstention that announces itself is the
    correction to that, not a second defect."""
    record = _stage_file(
        tmp_path,
        {"v1": ladder.STAGE_ARCH, "v2": ladder.STAGE_ARCH},
        {"v1": ladder.STAGE_ARCH, "v2": ladder.STAGE_ARCH},
    )
    _pin_reader(monkeypatch, record)
    wis = CT.load_wis(
        [
            {"WI-ID": "WI-401", "Title": "[v1]-[g2] a", "Status": "done"},
            {"WI-ID": "WI-402", "Title": "[v2]-[g2] b", "Status": "done"},
        ]
    )[0]
    warns = CT.phase_findings(tmp_path, wis)
    assert not any("dropped to" in w for w in warns), warns
    stood = [w for w in warns if "stood down" in w]
    assert len(stood) == 1, warns
    assert "v1, v2" in stood[0] and ladder.STAGE_ARCH in stood[0]


def test_the_abstention_covers_EXACTLY_the_repo_global_rungs(tmp_path, monkeypatch):
    """The rung set is a declared list, so it is pinned against what the detector
    actually does with each of the eight rungs: the three repo-global ones
    abstain, the five phase-owned ones are compared."""
    anchor_reach = ladder.STAGE_IMPL
    for rung in ladder.STAGE_ORDER:
        record = _stage_file(tmp_path, {"v1": rung}, {"v1": rung})
        _pin_reader(monkeypatch, record)
        warns = CT.phase_findings(tmp_path, _closed_anchor())
        if rung in kitstage.REPO_GLOBAL_RUNGS:
            assert any("stood down" in w for w in warns), rung
            assert not any("dropped to" in w for w in warns), rung
        elif kitstage.order(rung) < kitstage.order(anchor_reach):
            assert any("dropped to" in w for w in warns), rung
        else:
            assert warns == [], rung


# --- THE READER SEAM ----------------------------------------------------------
def test_the_detector_degrades_to_vacuous_rather_than_raising(tmp_path):
    """This module runs in the shipped pre-commit hook, so every failure mode of
    the stage read has to cost the drop half only. Three of them: no stage file
    at all, an unparseable one, and a `docs/stage` whose value is not a rung
    (which `kitlib.stage.parse` RAISES on, by its own ruled direction — that is
    the `derived-stage` step's finding to report, not an advisory detector's to
    crash the hook over)."""
    (tmp_path / "docs").mkdir()
    assert CT.phase_findings(tmp_path, _closed_anchor()) == []
    (tmp_path / "docs" / "stage").write_text("not a stage file\n", encoding="utf-8")
    assert CT.phase_findings(tmp_path, _closed_anchor()) == []
    # The retired tag below is the INPUT being proven rejected, not a use of it.
    retired = "stage = G3\n"  # check_vocab: allow
    (tmp_path / "docs" / "stage").write_text(retired, encoding="utf-8")
    assert CT.phase_findings(tmp_path, _closed_anchor()) == []


# --- WI-497'S SIBLING SWEEP + THE DEAD READER CORRECTION ----------------------
def _string_constants(path):
    """Every string literal in a module EXCEPT its docstrings.

    Prose has to be excluded or these pins invert: the clearest way to record a
    retired defect is to NAME it, and a grep-shaped test then reds on the comment
    that explains why the code is gone."""
    import ast

    tree = ast.parse(path.read_text(encoding="utf-8"))
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)):
            doc = ast.get_docstring(node, clean=False)
            if doc is not None:
                docstrings.add(id(node.body[0].value))
    return [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and id(node) not in docstrings
    ]


def _splitlines_zero_sites(path):
    """`[lineno]` of every `<expr>.splitlines()[0]` in a module — the WI-497
    defect SHAPE, read off the AST rather than grepped, so a docstring naming the
    idiom (this module, and `intake._stage_moved`'s own record of the defect) is
    not mistaken for one."""
    import ast

    out = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if not isinstance(node, ast.Subscript):
            continue
        target, index = node.value, node.slice
        if not (isinstance(index, ast.Constant) and index.value == 0):
            continue
        if (
            isinstance(target, ast.Call)
            and isinstance(target.func, ast.Attribute)
            and target.func.attr == "splitlines"
        ):
            out.append(node.lineno)
    return out


def test_no_kit_script_takes_splitlines_0_of_a_GENERATED_file():
    """WI-497's sweep instruction, mechanized so it stays swept.

    The defect class is "read line 0 of a file whose line 0 is a generated
    header". Two `splitlines()[0]` sites survive in the kit and neither is in
    that class: both read the FIRST LINE OF GIT COMMAND OUTPUT, where line 0 is
    the value by the command's own contract. They are named here so a third site
    has to be judged rather than inherited."""
    allowed = {
        "integrate.py": "int(git rev-list --count output)",
        "trunk_step.py": "int(git command output)",
    }
    hits = {
        path.name
        for path in sorted(SCRIPTS.rglob("*.py"))
        if _splitlines_zero_sites(path)
    }
    assert hits == set(allowed), sorted(hits)


def test_read_declared_is_not_documented_as_a_docs_gate_reader():
    """The schedule map's reader E: `read_declared` was documented in two places
    as "still the reader for `docs/gate`" and called on that file by nothing. The
    function is untouched — it is the live reader for the legacy half of the
    SN-028 dual-read window — and only the false claim is gone."""
    from kitlib import config as kitconfig

    retired = "still the reader for"
    assert retired not in (kitconfig.read_declared.__doc__ or "")
    assert retired not in (SCRIPTS / "agent_common.py").read_text(encoding="utf-8")
    assert kitconfig.read_declared is AC.read_declared
    # ...and `docs/gate` is still the deliberate NON-row it always was, which is
    # WHY no call site could ever have reached it through `declared_policy`.
    assert "gate" not in AC.PROCESS_KEYS


def test_the_two_cut_over_modules_hold_no_docs_gate_PATH_at_all():
    """The cut-over, pinned at the modules rather than described in a log entry.
    `check_trajectory` was `docs/gate`'s reader H (the phase-drop detector) and
    `intake` was reader D (the tier signal); neither holds a path to the file
    now. Both still EXPLAIN it in prose, which is why this reads string literals
    and not lines."""
    for name in ("check_trajectory.py", "intake.py"):
        literals = [s for s in _string_constants(SCRIPTS / name) if "docs/gate" in s]
        assert literals == [], (name, literals)
