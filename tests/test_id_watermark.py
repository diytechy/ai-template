"""The id watermark: an id is allocated once, for the life of the repo.

Duplicate ids already error (trace.integrity_findings, sn_integrity_findings,
check_trajectory.load_wis). REUSE does not — every one of those reads only the
LIVE tree, so an id freed by deleting its row is invisible and can be minted
again, silently re-pointing every commit message and archived document that
cites it. These tests pin the guard AND its fail-open edges, because a mark that
degrades to "no constraint" is worse than no mark at all: it looks like cover.
"""

from conftest import load_script

TRACE = load_script("trace")


def _repo(tmp_path, marks=None, srs=("SR-001",)):
    """A minimal tree: one spine CSV and (optionally) a watermark file."""
    reg = tmp_path / "docs" / "requirements"
    reg.mkdir(parents=True)
    (reg / "system-requirements.csv").write_text(
        "SR-ID,Title\n" + "".join("{},t\n".format(s) for s in srs), encoding="utf-8"
    )
    if marks is not None:
        (tmp_path / TRACE.WATERMARK).write_text(
            TRACE.render_watermark(marks), encoding="utf-8"
        )
    return tmp_path


def test_every_id_space_is_covered_by_the_mark_file():
    # A space that gains no mark row is a space with no guard, and nothing else
    # would notice. Keyed off ID_PATTERNS so adding a registry there cannot
    # silently exempt it here; the four prose/directory tiers are named because
    # ID_PATTERNS does not know them.
    assert set(TRACE.WATERMARK_SPACES) == set(TRACE.ID_PATTERNS) | {
        "SN",
        "WI",
        "OI",
        "DP",
    }


def test_a_clean_tree_has_no_finding(tmp_path):
    root = _repo(tmp_path, marks={s: 0 for s in TRACE.WATERMARK_SPACES} | {"SR": 1})
    assert TRACE.watermark_findings(root) == []


def test_an_id_above_the_mark_is_a_finding(tmp_path):
    # The rule that guards the tiers with NO mint at all: SR/LLR/TC ids are hand
    # authored, so "you allocated past the mark" is the only thing standing
    # between a deleted id and its silent re-use.
    root = _repo(
        tmp_path,
        marks={s: 0 for s in TRACE.WATERMARK_SPACES} | {"SR": 1},
        srs=("SR-001", "SR-009"),
    )
    (finding,) = TRACE.watermark_findings(root)
    assert "SR-009" in finding and "stands at 1" in finding


def test_a_missing_space_is_a_finding_not_a_free_pass(tmp_path):
    # The writer always emits every space, so this is the HAND-EDIT case: a line
    # deleted from the file must not read as "that space is unconstrained".
    root = _repo(tmp_path, marks={s: 0 for s in TRACE.WATERMARK_SPACES})
    path = root / TRACE.WATERMARK
    path.write_text(
        "\n".join(
            l
            for l in path.read_text(encoding="utf-8").splitlines()
            if not l.startswith("CMP")
        )
        + "\n",
        encoding="utf-8",
    )
    assert any("no mark for CMP" in f for f in TRACE.watermark_findings(root))


def test_an_absent_mark_file_is_an_ERROR_not_an_empty_set(tmp_path):
    # THE fail-open this guard exists to dodge. Every other declared-file reader
    # in the kit returns empty for a missing file, which is right for a floor or
    # an allowlist — absence means "nothing declared". Here absence would mean
    # "no id is taken", freeing every space at once. So it must fail LOUD.
    root = _repo(tmp_path, marks=None)
    (finding,) = TRACE.watermark_findings(root)
    assert "is missing" in finding


def test_a_malformed_line_is_refused_rather_than_skipped(tmp_path):
    # Skipping an unparseable line silently un-marks that one space — the same
    # hole as a missing row, but harder to see.
    root = _repo(tmp_path, marks={s: 0 for s in TRACE.WATERMARK_SPACES})
    path = root / TRACE.WATERMARK
    path.write_text(
        path.read_text(encoding="utf-8").replace("CMP = 0", "CMP: nought"),
        encoding="utf-8",
    )
    (finding,) = TRACE.watermark_findings(root)
    assert "not a `<SPACE> = <int>` line" in finding


def test_a_lowered_mark_is_a_finding(tmp_path):
    # Monotonicity: the one rule that cannot be read from the working tree,
    # because a lowered mark looks exactly like a correct one.
    root = _repo(tmp_path, marks={s: 0 for s in TRACE.WATERMARK_SPACES} | {"SR": 1})
    previous = {s: 0 for s in TRACE.WATERMARK_SPACES} | {"SR": 7}
    assert any(
        "moved DOWN 7 -> 1" in f for f in TRACE.watermark_findings(root, previous)
    )


def test_the_mark_counts_ids_no_loader_joins(tmp_path):
    # Broader than any loader ON PURPOSE: a registry this script never joins, a
    # legacy work-items.csv nothing reads, and a `-000` placeholder all still
    # HOLD their number. Counting extra can only raise the floor; missing
    # something lowers it and frees an id.
    root = _repo(tmp_path)
    (root / "docs" / "requirements" / "work-items.csv").write_text(
        "WI-ID,Title\nWI-777,legacy\n", encoding="utf-8"
    )
    (root / "docs" / "requirements" / "nobody-reads-this.csv").write_text(
        "IF-ID,Contract\nIF-000,placeholder\nIF-042,x\n", encoding="utf-8"
    )
    live = TRACE.live_max_ids(root)
    assert live["WI"] == 777
    assert live["IF"] == 42


def test_bump_only_ever_raises(tmp_path):
    root = _repo(tmp_path, marks={s: 0 for s in TRACE.WATERMARK_SPACES} | {"SR": 9})
    marks, raised = TRACE.bump_watermark(root)
    # Live max is SR-001, well under the mark of 9 — a bump must not pull it down.
    assert marks["SR"] == 9
    assert raised == {}


def test_bump_raises_to_the_live_maximum(tmp_path):
    root = _repo(
        tmp_path, marks={s: 0 for s in TRACE.WATERMARK_SPACES}, srs=("SR-001", "SR-055")
    )
    marks, raised = TRACE.bump_watermark(root)
    assert marks["SR"] == 55 and raised["SR"] == (0, 55)
    # And the written file round-trips through the reader it is written for.
    assert TRACE.read_watermark(root)["SR"] == 55


def test_the_live_repos_own_mark_covers_its_live_ids():
    # The dogfood arm: this repo's committed mark must actually hold.
    from conftest import ROOT

    assert TRACE.watermark_findings(ROOT) == []
