"""The dashboard's Retired view (SR-226, LLR-287).

The one place that shows the retirement records as a set. A record cannot hold
the commit that deleted its row, since a commit cannot contain its own hash, so
the view reads it from history at render time and says *unknown* where history
cannot answer; and because a clone with less history reads it differently with
no source having moved, the freshness compare ignores it, as it ignores the
as-of stamp.

The resolution cases drive real git repositories (a shallow clone included);
the whole-document cases run the real generator over the shared minimal
project.
"""

import subprocess

from conftest import load_script, pin_autocrlf
from traj_fixtures import gen, html_of, make_repo

rt = load_script("retire")
# The panel is reached through the facade, the one consumer seam of the family.
views = load_script("gen_trajectory")


def _git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, encoding="utf-8"
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def _init(root):
    _git(root, "init", "-q")
    pin_autocrlf(root)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git(root, "config", "user.email", "t@t")
    _git(root, "config", "user.name", "t")


def _commit(root, message="step"):
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", message)
    return _git(root, "rev-parse", "HEAD").strip()


def _record(root, row_id, successor="", reason="Gone."):
    path = root / "docs" / "log.d" / "retired" / (row_id + ".md")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        rt.fragment_text(row_id, "2026-09-28", successor, reason),
        encoding="utf-8",
        newline="\n",
    )
    return path


def _seeded(root):
    (root / "README.md").write_text("# seed\n", encoding="utf-8")
    _init(root)
    return _commit(root, "seed")


# --- (a) the deleting commit is read from history -----------------------------


def test_a_landed_record_reads_its_landing_commit(tmp_path):
    _seeded(tmp_path)
    _record(tmp_path, "SR-002", "SR-003")
    sha = _commit(tmp_path, "retire SR-002")
    (row,) = rt.records(tmp_path)
    assert row == {
        "id": "SR-002",
        "date": "2026-09-28",
        "successor": "SR-003",
        "reason": "Gone.",
        "commit": sha[:7],
    }


def test_an_uncommitted_record_reads_unknown(tmp_path):
    _seeded(tmp_path)
    _record(tmp_path, "SR-002")
    assert rt.records(tmp_path)[0]["commit"] == rt.UNKNOWN


def test_a_record_in_a_root_commit_reads_unknown(tmp_path):
    # A commit with no parent deleted nothing: a squashed history's single
    # commit is not the deleting commit, however the record arrived in it.
    _init(tmp_path)
    _record(tmp_path, "SR-002")
    _commit(tmp_path, "squashed history")
    assert rt.records(tmp_path)[0]["commit"] == rt.UNKNOWN


def test_a_shallow_clone_reads_unknown(tmp_path):
    origin = tmp_path / "origin"
    origin.mkdir()
    _seeded(origin)
    _record(origin, "SR-002")
    _commit(origin, "retire SR-002")
    clone = tmp_path / "clone"
    _git(tmp_path, "clone", "-q", "--depth", "1", origin.as_uri(), str(clone))
    assert rt.records(clone)[0]["commit"] == rt.UNKNOWN


def test_records_come_in_tier_then_number_order(tmp_path):
    for row_id in ("TC-002", "SR-010", "SN-004", "SR-002", "LLR-001"):
        _record(tmp_path, row_id)
    assert [r["id"] for r in rt.records(tmp_path)] == [
        "SN-004",
        "SR-002",
        "SR-010",
        "LLR-001",
        "TC-002",
    ]


# --- (b) the panel ------------------------------------------------------------


def test_no_record_renders_no_tab():
    assert views.retired_panel([], 0) is None
    assert views.retired_panel([], 12) is None


def test_the_panel_renders_one_escaped_row_per_record():
    rows = [
        {
            "id": "SR-002",
            "date": "2026-09-28",
            "successor": "SR-003",
            "reason": "Split <badly> & merged",
            "commit": "abc1234",
        },
        {
            "id": "TC-009",
            "date": "2026-09-29",
            "successor": "",
            "reason": "Obsolete.",
            "commit": rt.UNKNOWN,
        },
    ]
    tab, panel = views.retired_panel(rows, 0)
    assert 'id="tab-retired"' in tab and "Retired" in tab
    body = panel.split("<tbody>", 1)[1]
    assert body.count("<tr>") == 2
    assert "Split &lt;badly&gt; &amp; merged" in panel
    assert "<badly>" not in panel
    assert '<code class="retcommit" data-id="SR-002">abc1234</code>' in panel
    assert '<code class="retcommit" data-id="TC-009">unknown</code>' in panel
    for cell in ("SR-002", "2026-09-28", "SR-003", "TC-009", "Obsolete."):
        assert cell in body
    # A retirement with no successor shows a dash, never an empty cell.
    tc_row = body.split("TC-009", 1)[1].split("</tr>", 1)[0]
    assert "<td>—</td>" in tc_row
    # The caption says what the view is for, and counts nothing it was not given.
    assert "lookup" in panel
    assert "before the record began" not in panel


def test_the_caption_counts_the_ids_retired_before_the_record():
    rows = [{"id": "SR-2", "date": "d", "successor": "", "reason": "r", "commit": "c"}]
    _tab, panel = views.retired_panel(rows, 108)
    assert "108 ids retired before the record began" in panel


# --- (c) the whole document ---------------------------------------------------


def test_the_dashboard_carries_the_tab_only_when_a_record_exists(tmp_path):
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    assert 'id="tab-retired"' not in html_of(tmp_path)

    _record(tmp_path, "SR-009", reason="Retired for the view.")
    proc = gen(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = html_of(tmp_path)
    assert 'id="tab-retired"' in text
    assert "Retired for the view." in text


def _rendered_history(root):
    """A committed project whose page was rendered, and committed, where the
    full history resolved the record's deleting commit."""
    make_repo(root)
    _init(root)
    _commit(root, "sources")
    _record(root, "SR-009")
    sha = _commit(root, "retire SR-009")
    assert gen(root).returncode == 0
    _commit(root, "render")
    return sha


def test_a_fabricated_deleting_commit_is_stale_where_history_answers(tmp_path):
    sha = _rendered_history(tmp_path)
    text = html_of(tmp_path)
    resolved = '<code class="retcommit" data-id="SR-009">{}</code>'.format(sha[:7])
    assert resolved in text
    assert gen(tmp_path, "--check").returncode == 0
    for forged in ("0000000", rt.UNKNOWN):
        (tmp_path / "PROJECT_STATE.html").write_text(
            text.replace(
                resolved,
                '<code class="retcommit" data-id="SR-009">{}</code>'.format(forged),
            ),
            encoding="utf-8",
            newline="\n",
        )
        assert gen(tmp_path, "--check").returncode == 1, forged


def test_a_checkout_that_cannot_resolve_the_commit_accepts_the_page(tmp_path):
    # Rendered with the full history, checked in a depth-one clone that cannot
    # name the landing: the page is fresh, since no source moved.
    origin = tmp_path / "origin"
    origin.mkdir()
    _rendered_history(origin)
    clone = tmp_path / "clone"
    _git(tmp_path, "clone", "-q", "--depth", "1", origin.as_uri(), str(clone))
    assert rt.records(clone)[0]["commit"] == rt.UNKNOWN
    proc = gen(clone, "--check")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_any_other_change_to_a_record_is_stale(tmp_path):
    _rendered_history(tmp_path)
    text = html_of(tmp_path)
    (tmp_path / "PROJECT_STATE.html").write_text(
        text.replace("Gone.", "Gone!"), encoding="utf-8", newline="\n"
    )
    assert gen(tmp_path, "--check").returncode == 1
