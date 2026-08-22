"""`kitlib.stage` — the declared inputs, their fingerprint, the `docs/stage`
format, and THE COMMON READER (TC-180).

WI-498 slice 1. The contract under test is the one the ruled plan §§2-3 states:
a reader recomputes the fingerprint of the DECLARED inputs on every call, trusts
the recorded record only on a match, derives fresh in memory otherwise, and
NEVER writes. That contract is what closes the two stale windows the schedule map
found — the claimed-branch lane where the freshness step stands down, and the
once-per-run hoist in the loop — by construction rather than by scheduling, so
the tests here drive the construction, not the schedule.

Five of the deep-check's nine corner cases are answered at this level, because
they are properties of the carrier rather than of a spine: the sentinel's
participation in ordering, the truncation refusal, the cross-ladder refusal, the
mid-process input change, and the CRLF invariance. The other four need real
registry rows and live in `test_derive_stage.py`.
"""

import io
from pathlib import Path
from unittest import mock

import pytest
from conftest import SCRIPTS, load_script  # noqa: F401  (puts scripts/ on sys.path)

from kitlib import ladder, stage


# --- a tree carrying the declared inputs --------------------------------------
def _tree(tmp_path, **overrides):
    """A tmp root with every declared input present and trivially filled.

    Content is written as BYTES on purpose: `write_text` translates `\\n` to the
    platform newline on Windows, which would make a test that means to write LF
    and a test that means to write CRLF both write CRLF — the CRLF test below
    would then pass vacuously on the one platform it exists for."""
    for declared, suffixes in stage.DECLARED_INPUTS:
        path = tmp_path / (declared + suffixes[0])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(overrides.get(declared, b"# empty\n"))
    return tmp_path


def _record(**over):
    base = {
        "stage": ladder.STAGE_TESTS,
        "stage-ord": 5,
        "stage-of": 8,
        "floored": False,
        "settled-stage": ladder.STAGE_TESTS,
        "live-stage": ladder.STAGE_REQS,
        "phase": 3,
        "per-phase": {"1": ladder.STAGE_TESTS, "3": stage.BELOW},
        "per-phase-live": {"1": ladder.STAGE_TESTS, "3": ladder.STAGE_REQS},
        "drafted": 2,
        "fingerprint": "sha256:" + "0" * 64,
    }
    base.update(over)
    return base


# --- corner case 4: the sentinel orders without raising -----------------------
def test_DevStg_Below_participates_in_ordering_without_raising():
    """`ladder.stage_ord` RAISES on the sentinel and must keep doing so — the
    ladder has no rung below Needs and must not grow one. But per-phase values
    genuinely carry it, so the ordering those values need lives here, degrading
    the sentinel to -1 in exactly ONE place. (The bar axis grew three private
    tables doing this; that is the shape being avoided.)"""
    with pytest.raises(ValueError):
        ladder.stage_ord(stage.BELOW)

    assert stage.order(stage.BELOW) == -1
    assert stage.order(stage.BELOW) < stage.order(ladder.STAGE_NEEDS)
    for rung in ladder.STAGE_ORDER:
        assert stage.order(rung) == ladder.stage_ord(rung)
    # and it still refuses what it cannot order
    with pytest.raises(ValueError):
        stage.order("DevStg-Nonsense")


# --- corner case 5: a malformed rung fails honestly ---------------------------
@pytest.mark.parametrize(
    "label",
    ["DevStg-Impl-2", "DevStg-Release-Candidate", "DevStg-Reqs-v2"],
)
def test_a_hyphenated_label_is_REFUSED_not_truncated_to_a_valid_rung(label):
    """THE DEFECT THIS REPLACES, driven. `agent_common.spine_stage_of` matched
    `stage=(DevStg-[A-Za-z]+)\\b`, and `\\b` matches AT A HYPHEN — so a cache
    carrying `DevStg-Impl-2` returned `DevStg-Impl`: a confident answer, on the
    wrong rung, for a label the kit had never defined. Latent only because no rung
    is compound today, and the ladder's own design explicitly provides for
    inserting one.

    The refusal must be a REFUSAL, not a different truncation: assert both that it
    raises AND that no valid rung is a prefix-answer anywhere in the message
    path."""
    assert label.split("-")[0] + "-" + label.split("-")[1] in ladder.LADDER_RUNGS
    with pytest.raises(ValueError) as excinfo:
        stage.require_rung(label)
    assert label in str(excinfo.value)

    # ... and through the file parser, which is the path a cache actually takes.
    text = "\n".join(
        "{} = {}".format(k, label if k == "stage" else v)
        for k, v in [("stage", ""), ("fingerprint", "sha256:x")]
    )
    with pytest.raises(ValueError):
        stage.parse(text)


# --- corner case 6: a cross-ladder / bar-vocabulary token is refused ----------
@pytest.mark.parametrize(
    "token", ["DevStg-Below", "all", "", "DevStg-", "DevStg-Impl2"]
)
def test_a_token_that_is_not_a_rung_is_refused_by_the_stage_reader(token):
    """The stage reader accepts the eight rungs and nothing else. That covers the
    bar vocabulary's non-shared members (`DevStg-Below`, and the harness's `all`),
    the empty string, and anything rung-shaped but unknown.

    WHAT IT CANNOT COVER, stated so the test is not read as claiming more than it
    does: `DevStg-Reqs`, `DevStg-Tests` and `DevStg-Impl` are legal on BOTH the
    retired bar ladder and this one with DIFFERENT ordinals, so no value-level
    guard can separate them — the deep-check's Q2(iii-b). What contains that is
    carriage (distinct keys in distinct files) until slice 2 deletes the other
    axis."""
    with pytest.raises(ValueError):
        stage.require_rung(token)


def test_the_sentinel_is_refused_as_a_HEADLINE_but_legal_per_phase():
    with pytest.raises(ValueError, match="sentinel"):
        stage.require_rung(stage.BELOW)
    record = stage.parse(stage.field_block(_record()))
    assert record["per-phase"] == {"1": ladder.STAGE_TESTS, "3": stage.BELOW}


# --- the effective-stage fold -------------------------------------------------
def test_a_phase_with_nothing_settled_does_not_lower_the_fold():
    """The core of corner case 1, at the fold level: a phase carrying the
    sentinel has earned no rung and therefore holds no opinion. Folding it in
    would drop the repo to the floor the moment one draft opened a phase."""
    got, floored = stage.effective_stage({"1": ladder.STAGE_TESTS, "2": stage.BELOW})
    assert (got, floored) == (ladder.STAGE_TESTS, False)


def test_the_fold_is_a_MIN_over_the_phases_that_earned_something():
    """Min, not max. A max would be a high-water reading, and process.md §4 rules
    that one may only be shown BESIDE the honest value, never as it."""
    got, _ = stage.effective_stage(
        {"1": ladder.STAGE_TESTS, "2": ladder.STAGE_LLREQS, "3": ladder.STAGE_IMPL}
    )
    assert got == ladder.STAGE_LLREQS


def test_an_empty_fold_is_the_FLOOR_and_never_raises():
    """Corner case 3 at the fold level — a fresh scaffold, an empty spine and an
    all-draft repo all arrive here, and all three need a defined SELECTION
    meaning. Below the floor nothing is selected by an at-or-above rule, so the
    run would go green because no check ran."""
    assert stage.effective_stage({}) == (stage.FLOOR, True)
    assert stage.effective_stage({"1": stage.BELOW}) == (stage.FLOOR, True)


def test_a_reading_below_the_floor_is_floored_and_SAYS_SO():
    got, floored = stage.effective_stage({"1": ladder.STAGE_NEEDS})
    assert (got, floored) == (stage.FLOOR, True)
    assert stage.order(got) > stage.order(ladder.STAGE_NEEDS)


# --- the file format ----------------------------------------------------------
def test_render_parse_round_trips_every_compared_field():
    record = _record()
    text = stage.render(record, as_of="abc1234", date="2026-08-21")
    back = stage.parse(text)
    assert back is not None
    for key in stage.FIELDS:
        assert key in back, key
    assert back["stage"] == record["stage"]
    assert back["fingerprint"] == record["fingerprint"]


def test_the_as_of_stamp_is_NOT_part_of_the_compared_block():
    """It carries the revision, which moves on every commit. Comparing it would
    report the file stale the instant it was committed — the reason `docs/gate`
    excludes its own stamp too."""
    record = _record()
    one = stage.render(record, as_of="aaaaaaa", date="2026-08-21")
    two = stage.render(record, as_of="bbbbbbb", date="2026-08-22")
    assert one != two
    assert stage.field_block(record) in one
    assert stage.field_block(record) in two


def test_the_reader_returns_ONE_RECORD_SHAPE_whichever_path_it_took(tmp_path):
    """THE DEFECT THIS PINS, found by review during the slice and fixed here: the
    parsed record carried every field as a STRING while the derived record
    carried real types. A consumer's `record["floored"]` was then `False` on the
    fresh path and the non-empty string `"no"` on the recorded path — which is
    TRUE — and `record["phase"]` was an int or a numeral depending on whether a
    cache happened to be current.

    That is the worst shape a bug can take here: the recorded path is the one
    that almost always runs, so the wrong branch would surface only after a spine
    edit. A cache must be INVISIBLE to its readers except in speed."""
    root = _tree(tmp_path)
    derived = _record()

    def deriver(_root):
        return dict(derived)

    fresh = stage.read_stage(root, deriver)
    (root / stage.STAGE_FILE).parent.mkdir(parents=True, exist_ok=True)
    (root / stage.STAGE_FILE).write_text(
        stage.render(fresh, "rev", "2026-08-21"), encoding="utf-8"
    )
    recorded = stage.read_stage(root, deriver)
    assert recorded["source"] == "recorded" and fresh["source"] == "derived"

    for key in stage.FIELDS:
        assert type(recorded[key]) is type(fresh[key]), key
        assert recorded[key] == fresh[key], key


def test_a_file_with_no_stage_field_parses_as_None_rather_than_raising():
    """A scaffold that has never derived, or a pre-migration tree. The reader
    then derives fresh and `--check` asks for the one-time generation — the same
    smooth-transition path `spine_rules` gives a legacy hand-set gate."""
    assert stage.parse("# just a header\n") is None
    assert stage.parse("") is None


# --- the fingerprint ----------------------------------------------------------
def test_the_declared_input_set_is_stated_once_and_resolves_by_carrier(tmp_path):
    root = _tree(tmp_path)
    resolved = stage.input_paths(root)
    assert len(resolved) == len(stage.DECLARED_INPUTS)
    assert all(path is not None for _, path in resolved)

    # the same logical input on its OTHER carrier still resolves, and the
    # fingerprint moves because WHICH carrier answered is part of the fold
    before = stage.fingerprint(root, memo=None)
    (root / "docs/requirements/system-requirements.toml").unlink()
    (root / "docs/requirements/system-requirements.csv").write_text(
        "# empty\n", encoding="utf-8"
    )
    assert stage.input_paths(root)[1][1].name == "system-requirements.csv"
    assert stage.fingerprint(root, memo=None) != before


def test_an_ABSENT_input_is_a_fingerprint_VALUE_not_a_gap(tmp_path):
    """A registry appearing or disappearing changes the derivation — a repo that
    adopts no components registry simply never sits at the Arch rung — so absence
    has to move the fingerprint exactly as an edit does."""
    root = _tree(tmp_path)
    before = stage.fingerprint(root, memo=None)
    (root / "docs/requirements/components.toml").unlink()
    assert stage.fingerprint(root, memo=None) != before


# --- corner case 9: CRLF invariance -------------------------------------------
def test_the_fingerprint_is_INVARIANT_under_CRLF_working_tree_churn(tmp_path):
    """A Windows working tree carries CRLF where the index holds LF. A
    fingerprint that flipped on line endings would report every cross-platform
    checkout stale — stale-noise, on a mechanism whose whole value is that a
    mismatch means something."""
    lf = _tree(
        tmp_path / "lf", **{"docs/requirements/stakeholder-needs": b"a = 1\nb = 2\n"}
    )
    crlf = _tree(
        tmp_path / "crlf",
        **{"docs/requirements/stakeholder-needs": b"a = 1\r\nb = 2\r\n"},
    )
    assert (crlf / "docs/requirements/stakeholder-needs.toml").read_bytes() != (
        lf / "docs/requirements/stakeholder-needs.toml"
    ).read_bytes()
    assert stage.fingerprint(lf, memo=None) == stage.fingerprint(crlf, memo=None)


def test_content_still_moves_the_fingerprint(tmp_path):
    """The companion conviction test — LF-normalizing must not have made the
    fingerprint blind to a real edit."""
    root = _tree(tmp_path)
    before = stage.fingerprint(root, memo=None)
    (root / "docs/requirements/stakeholder-needs.toml").write_text(
        "changed\n", encoding="utf-8"
    )
    assert stage.fingerprint(root, memo=None) != before


def test_process_toml_is_NOT_an_input(tmp_path):
    """Owner ruling 2026-08-21 (amending plan §2): dials govern who may ratify,
    not what stage is derived — and an over-inclusive fingerprint costs a red
    commit bar after every policy-dial edit, not "milliseconds". A process.toml
    edit must not move the fingerprint."""
    root = _tree(tmp_path)
    before = stage.fingerprint(root, memo=None)
    (root / "docs" / "process.toml").write_text("dial = 1\n", encoding="utf-8")
    assert stage.fingerprint(root, memo=None) == before


def test_a_SECOND_CARRIER_beside_a_declared_input_is_REFUSED(tmp_path):
    """The dual-carrier hole (ROUND-SOL-RAW 6), and it was the sharp shape of
    the fingerprint's one blind spot.

    `input_paths` accepted the FIRST existing suffix and stopped, so a
    conflicting second carrier beside a fingerprinted registry was never hashed.
    The fingerprint therefore did not move, `read_stage` matched it and returned
    the RECORDED stage, and the derivation that would have refused the two-home
    state — `spine_carrier.resolve`, which raises on exactly this — was never
    reached. The forbidden state was both reachable and invisible.

    It now refuses at the fingerprint, which is the earliest honest point: the
    derived stage READS this file, so a reader must not be able to answer from a
    cache whose input set is ambiguous."""
    root = _tree(tmp_path)
    assert stage.fingerprint(root, memo=None)  # single carrier: fine
    declared, suffixes = stage.DECLARED_INPUTS[1]  # system-requirements
    assert len(suffixes) > 1, "this input must admit two carriers for the test"
    (root / (declared + suffixes[1])).write_bytes(b"# the stale half\n")
    with pytest.raises(SystemExit) as excinfo:
        stage.fingerprint(root, memo=None)
    assert "BOTH carriers" in str(excinfo.value)
    # ...and the refusal names both files, so the remedy is unambiguous.
    assert suffixes[0] in str(excinfo.value) and suffixes[1] in str(excinfo.value)


def test_every_file_the_DERIVATION_READS_is_a_declared_input(tmp_path):
    """THE INVERSE DEFECT, which nothing guarded (ROUND-OPUS 7).

    The existing pin is one-directional by construction: `test_process_toml_is_
    NOT_an_input` proves a NAMED file is not an input. Nothing proved an UNNAMED
    file is not one — and that is the expensive direction. The over-inclusive
    error costs a spurious re-derivation (a red commit bar, which is how the
    process.toml ruling got made). The under-inclusive error costs a PERMANENT
    false green: the moment `load_spine` reads a registry `DECLARED_INPUTS` does
    not name, the fingerprint stops covering it, `read_stage` matches on a hash
    that ignores every edit to it, and every consumer returns a stale stage
    forever — with `derive_stage --check` passing, because it compares the same
    uncovered fingerprint.

    So: run the real derivation under a read-audit and assert the set of files
    it actually opened is a SUBSET of `input_paths(root)`.

    THE TREE IS BAITED, and it has to be or the guard is vacuous. An audit over
    a tree containing ONLY the declared inputs can never catch anything: the
    undeclared read would be a miss on a file that does not exist. So the
    fixture plants every other registry the kit ships under `docs/` — starting
    with `interfaces.toml`, the obvious future candidate (a spine registry the
    ladder does not yet read, while two rungs already key on off-spine ones) —
    and the audit fails if the derivation touches any of them. Verified
    non-vacuous by mutation: teaching `load_spine` to read `interfaces.toml`
    reds this test.
    """
    spine_rules = load_script("spine_rules")
    root = _tree(tmp_path)
    # THE BAIT: every registry the kit ships that is NOT a declared input.
    bait = [
        "docs/requirements/interfaces.toml",
        "docs/requirements/performance-budgets.csv",
        "docs/requirements/open-items.toml",
        "docs/requirements/hats.toml",
        "docs/requirements/assets.csv",
        "docs/requirements/procurement.csv",
        "docs/process.toml",
        "docs/stack.ini",
    ]
    declared_names = {d for d, _s in stage.DECLARED_INPUTS}
    for rel in bait:
        assert not any(rel.startswith(d) for d in declared_names), (
            rel + " IS a declared input — it cannot serve as bait"
        )
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"# bait: reading this must fail the audit\n")

    declared = {p.resolve() for _d, p in stage.input_paths(root) if p is not None}
    assert declared, "the fixture must present at least one declared input"

    opened = []
    real_open = io.open

    def _audit(file, *args, **kwargs):
        try:
            opened.append(Path(file).resolve())
        except TypeError:  # a file descriptor, not a path — not a registry read
            pass
        return real_open(file, *args, **kwargs)

    with mock.patch("io.open", _audit), mock.patch("builtins.open", _audit):
        spine_rules.load_spine(root / "docs")

    under_docs = {p for p in opened if p.is_relative_to((root / "docs").resolve())}
    undeclared = sorted(
        str(p.relative_to(root.resolve())) for p in under_docs - declared
    )
    assert not undeclared, (
        "load_spine read {} file(s) under docs/ that DECLARED_INPUTS does not "
        "name, so the fingerprint no longer covers every input and a stale read "
        "becomes permanent: {}. Add each to DECLARED_INPUTS in the same change "
        "that taught the derivation to read it.".format(len(undeclared), undeclared)
    )


# --- corner case 7: a mid-process input change -------------------------------
def test_the_reader_returns_FRESH_values_when_an_input_changes_mid_process(tmp_path):
    """THE HOISTING WINDOW, CLOSED BY CONSTRUCTION. `agent_loop` and `dispatch`
    read the stage once per run and thread it down, so a mid-session ratification
    was invisible for the rest of the run. Verification per CALL is what removes
    that window — including across the per-process memo, which is keyed on
    path+size+mtime and must never be mistaken for the freshness truth."""
    root = _tree(tmp_path)
    calls = []

    def deriver(_root):
        calls.append(1)
        return _record(stage=ladder.STAGE_LLREQS)

    first = stage.read_stage(root, deriver)
    assert first["source"] == "derived"
    (root / stage.STAGE_FILE).parent.mkdir(parents=True, exist_ok=True)
    (root / stage.STAGE_FILE).write_text(
        stage.render(first, "rev", "2026-08-21"), encoding="utf-8"
    )

    # recorded and fresh: no derivation
    assert stage.read_stage(root, deriver)["source"] == "recorded"
    assert len(calls) == 1

    # an input moves IN THE SAME PROCESS: the next reader sees it
    (root / "docs/requirements/system-requirements.toml").write_text(
        "# a requirement landed\n", encoding="utf-8"
    )
    again = stage.read_stage(root, deriver)
    assert again["source"] == "derived"
    assert len(calls) == 2


def test_the_fingerprint_FAST_PATH_actually_skips_the_derivation(tmp_path):
    """The cost argument the plan makes — the fingerprint is a fast path that lets
    a fresh reader SKIP the parse, so the net scan count goes DOWN — is only true
    if the skip is real. Counted, not assumed."""
    root = _tree(tmp_path)
    calls = []

    def deriver(_root):
        calls.append(1)
        return _record()

    record = stage.read_stage(root, deriver)
    (root / stage.STAGE_FILE).parent.mkdir(parents=True, exist_ok=True)
    (root / stage.STAGE_FILE).write_text(
        stage.render(record, "rev", "2026-08-21"), encoding="utf-8"
    )
    for _ in range(5):
        assert stage.read_stage(root, deriver)["source"] == "recorded"
    assert len(calls) == 1, "the recorded fast path re-derived"


def test_READERS_NEVER_WRITE(tmp_path):
    """The committed file is load-bearing HISTORY (the phase-drop and tier signals
    are deltas of it), so a reader that healed it on disk would rewrite that
    history from whichever process happened to look first — on claimed branches
    and in CI, where the freshness step is deliberately stood down."""
    root = _tree(tmp_path)
    path = root / stage.STAGE_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    stale = stage.render(_record(fingerprint="sha256:stale"), "rev", "2026-08-21")
    path.write_text(stale, encoding="utf-8")

    got = stage.read_stage(root, lambda _r: _record(stage=ladder.STAGE_IMPL))
    assert got["source"] == "derived"
    assert got["stage"] == ladder.STAGE_IMPL
    assert path.read_text(encoding="utf-8") == stale, "the reader wrote the file"

    # and the absent-file case writes nothing either
    path.unlink()
    stage.read_stage(root, lambda _r: _record())
    assert not path.exists()


def test_a_hand_edited_record_RAISES_rather_than_healing_silently(tmp_path):
    """The two failure directions are deliberately different. A file with no stage
    field is a file this kit did not write and re-derives; a file that carries a
    stage which is not a rung is a hand edit or a ladder that moved under a cached
    value, and both are the loud case (`ladder.stage_ord`'s ruled direction: the
    wrong-answer direction of a silent default is LESS human involvement)."""
    root = _tree(tmp_path)
    path = root / stage.STAGE_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        stage.render(_record(), "rev", "2026-08-21").replace(
            "stage = DevStg-Tests", "stage = DevStg-Impl-2"
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        stage.read_stage(root, lambda _r: _record())


def test_the_module_imports_no_sibling(tmp_path):
    """The one asserted rule of the package. Restated here at the module's own
    site because `test_bootstrap.py`'s AST sweep is glob-driven and silent about
    which module it covered."""
    import ast

    tree = ast.parse((SCRIPTS / "kitlib" / "stage.py").read_text(encoding="utf-8"))
    tops = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            tops.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            tops.add(node.module.split(".")[0])
    siblings = {p.stem for p in SCRIPTS.glob("*.py")}
    assert not (tops & siblings), sorted(tops & siblings)
