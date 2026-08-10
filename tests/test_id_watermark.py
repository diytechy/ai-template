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
    # An ABSOLUTE pin, not the derivation restated. `WATERMARK_SPACES` is built
    # as `set(ID_PATTERNS) | {SN,WI,OI,DP}`, so asserting exactly that is a
    # tautology: adding a bogus space to ID_PATTERNS would leave it PASSING,
    # which is the one scenario it is supposed to catch. Name the spaces.
    assert set(TRACE.WATERMARK_SPACES) == {
        "SR",
        "LLR",
        "TC",
        "PB",
        "REPO",
        "MOD",
        "PART",
        "ASSET",
        "CMP",
        "IF",
        "SN",
        "WI",
        "OI",
        "DP",
    }
    # ...and hold the derivation to it, so a registry added to ID_PATTERNS
    # without a mark row reds HERE rather than going silently unguarded.
    assert set(TRACE.ID_PATTERNS) <= set(TRACE.WATERMARK_SPACES)


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


def _wi_repo(tmp_path, existing=(), mark=None):
    work = tmp_path / "docs" / "work" / "queued"
    work.mkdir(parents=True)
    for n in existing:
        (work / "WI-{:03d}-x.md".format(n)).write_text(
            '+++\nid = "WI-{:03d}"\n+++\n'.format(n), encoding="utf-8"
        )
    (tmp_path / "docs" / "requirements").mkdir(parents=True, exist_ok=True)
    TRACE.bump_watermark(tmp_path)
    if mark is not None:
        path = tmp_path / TRACE.WATERMARK
        marks = TRACE.read_watermark(tmp_path)
        marks["WI"] = mark
        path.write_text(TRACE.render_watermark(marks), encoding="utf-8")
    return tmp_path


def test_the_mint_does_not_reissue_a_deleted_id(tmp_path):
    # THE POINT OF THE WHOLE MECHANISM. Under D-4 a superseded row is DELETED,
    # so `max(live) + 1` hands its number straight back out — and a reused id
    # silently re-points every commit message and archived document citing it.
    INTAKE = load_script("intake")
    root = _wi_repo(tmp_path, existing=(5,))
    assert INTAKE.next_wi_id(root) == "WI-006"
    # D-4: WI-005 is superseded and its spec removed.
    (root / "docs" / "work" / "queued" / "WI-005-x.md").unlink()
    assert TRACE.live_max_ids(root).get("WI", 0) == 0  # the live tree forgot it
    assert TRACE.read_watermark(root)["WI"] == 5  # the mark did not
    assert INTAKE.next_wi_id(root) == "WI-006"  # NOT WI-005


def test_the_mint_still_respects_a_live_id_above_the_mark(tmp_path):
    # The mark is a FLOOR, not an override: a spec present but somehow above the
    # mark must still not be re-issued while the mark catches up.
    INTAKE = load_script("intake")
    root = _wi_repo(tmp_path, existing=(9,), mark=3)
    assert INTAKE.next_wi_id(root) == "WI-010"


def test_the_mint_refuses_when_the_mark_is_missing(tmp_path):
    # A mint with no record of what has been allocated is the one operation that
    # must not proceed on a guess, so the reader's refusal is NOT caught.
    import pytest

    INTAKE = load_script("intake")
    root = _wi_repo(tmp_path, existing=(5,))
    (root / TRACE.WATERMARK).unlink()
    with pytest.raises(ValueError, match="is missing"):
        INTAKE.next_wi_id(root)


def test_the_rules_are_actually_WIRED_INTO_the_integrity_floor(tmp_path):
    # THE GAP THE REVIEW FOUND. Every other test here calls `watermark_findings`
    # directly, so deleting the one line in `main()` that appends it to
    # `findings.integrity` left all of them green — and the whole argument for
    # this design is that the rules run in trace.py's always-on
    # `--strict-integrity` floor rather than behind a toggle or a G3 gate.
    # So drive the CLI and assert the finding reaches the EXIT CODE.
    from conftest import SCRIPTS, run_py

    reg = tmp_path / "docs" / "requirements"
    reg.mkdir(parents=True)
    (reg / "system-requirements.csv").write_text(
        "SR-ID,Title\nSR-009,t\n", encoding="utf-8"
    )
    marks = {s: 0 for s in TRACE.WATERMARK_SPACES}
    (tmp_path / TRACE.WATERMARK).write_text(
        TRACE.render_watermark(marks), encoding="utf-8"
    )
    proc = run_py(
        [SCRIPTS / "trace.py", "--root", str(tmp_path), "--strict-integrity"],
        cwd=tmp_path,
    )
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "id watermark stands at 0" in (proc.stdout + proc.stderr)
    # And the finding names the command that fixes it — an unfollowable
    # instruction on an every-commit check is how a check earns the ignore.
    assert "--bump-ids" in (proc.stdout + proc.stderr)


def test_a_malformed_file_does_not_let_the_writer_discard_the_record(tmp_path):
    # The blocker: `bump_watermark` used to catch read_watermark's refusal and
    # start from `{}`, so the documented remediation (`--bump-ids`, named in the
    # reader's own error text) DESTROYED every mark for an already-deleted id —
    # the one thing in this repo that cannot be recomputed.
    import pytest

    root = _repo(tmp_path, marks={s: 0 for s in TRACE.WATERMARK_SPACES} | {"SR": 300})
    path = root / TRACE.WATERMARK
    path.write_text(
        path.read_text(encoding="utf-8") + "<<<<<<< HEAD\n", encoding="utf-8"
    )
    with pytest.raises(ValueError):
        TRACE.bump_watermark(root)
    # The file is untouched — the record survives the failed write.
    assert "SR = 300" in path.read_text(encoding="utf-8")


def test_a_hand_raised_mark_is_a_finding(tmp_path):
    # Nothing else bounds a mark upward, so one edited digit would retire that
    # space's guard forever while passing every other rule.
    root = _repo(tmp_path, marks={s: 0 for s in TRACE.WATERMARK_SPACES} | {"SR": 5000})
    previous = {s: 0 for s in TRACE.WATERMARK_SPACES}
    assert any(
        "nothing justifies more than 1" in f
        for f in TRACE.watermark_findings(root, previous)
    )


def test_headroom_left_by_a_deleted_row_stays_legal(tmp_path):
    # The upper bound must not punish the mechanism's whole purpose: a mark
    # ABOVE the live max is exactly what a deleted id looks like.
    root = _repo(tmp_path, marks={s: 0 for s in TRACE.WATERMARK_SPACES} | {"SR": 9})
    previous = {s: 0 for s in TRACE.WATERMARK_SPACES} | {"SR": 9}
    assert TRACE.watermark_findings(root, previous) == []


def test_a_ragged_csv_row_does_not_crash_the_scan(tmp_path):
    # Surplus cells land under DictReader's `None` key as a LIST; reading
    # row.values() exploded on it and took the whole trace run down with it,
    # including structure_findings — the check built for exactly this input.
    root = _repo(tmp_path, marks={s: 0 for s in TRACE.WATERMARK_SPACES})
    (root / "docs" / "requirements" / "system-requirements.csv").write_text(
        "SR-ID,Title\nSR-001,ok\n,note,EXTRA\n", encoding="utf-8"
    )
    assert TRACE.live_max_ids(root)["SR"] == 1


def test_a_reference_column_before_the_id_column_does_not_hide_the_id(tmp_path):
    # `live_max_ids` used to take the first id-SHAPED cell, so a registry whose
    # first column is a reference yielded the CITATION and never the row's own
    # id — leaving that number unmarked and therefore free. Under-counting is
    # the one direction this scan must not fail in.
    root = _repo(tmp_path, marks={s: 0 for s in TRACE.WATERMARK_SPACES})
    (root / "docs" / "requirements" / "interfaces.csv").write_text(
        "IF-ID,SR-Refs,Contract\nIF-900,SR-001,x\n", encoding="utf-8"
    )
    assert TRACE.live_max_ids(root)["IF"] == 900


def test_force_never_overwrites_a_live_repos_marks(tmp_path):
    # `bootstrap --force` re-lays every scaffold file. For every OTHER target
    # that costs at most re-doing an edit — they are templates to fill, or are
    # regenerable from the tree. The watermark is the only one whose content is
    # HISTORY (which ids were allocated and then deleted), so forcing the
    # fresh-scaffold marks over a live repo frees every id above them and
    # nothing can rebuild what was lost.
    from conftest import KIT, run_py

    dest = tmp_path / "repo"
    dest.mkdir()
    run_py([KIT / "scripts" / "bootstrap.py", "--dest", str(dest)], cwd=tmp_path)
    mark = dest / TRACE.WATERMARK
    mark.write_text(
        mark.read_text(encoding="utf-8").replace("SR = 0", "SR = 146"),
        encoding="utf-8",
    )
    run_py(
        [KIT / "scripts" / "bootstrap.py", "--dest", str(dest), "--force"],
        cwd=tmp_path,
    )
    assert "SR = 146" in mark.read_text(encoding="utf-8")
