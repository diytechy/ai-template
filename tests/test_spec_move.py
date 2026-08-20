"""spec_move.py — the link-aware spec-move ritual (WI-393, rehoming WI-288/WI-353).

The ritual under test is ONE INDIVISIBLE OPERATION: move a spec file, redirect
every INBOUND markdown link whose target resolves to the vacated path (WI-288),
and re-relativise the moved file's OWN outbound links against its new directory
(WI-353) — no caller can perform two thirds of it. All four functions lived in
`agent_dispatch.py` and were deleted with it at concurrency-restructure Phase 5
(31ad569d) without being rehomed; WI-391 REVIEW-A (2026-08-01) reproduced both
defects live (a bare `git mv` of a probe spec took the broken-link count from 4
to 8), so these tests restore the ORIGINAL guard shape, including the mutation
twin: the same fixture moved WITHOUT the rebase must FAIL the real check_docs,
so the guard demonstrably reproduces the defect it fixes.

The discipline pinned here is the originals' own: link TEXT untouched and only
the TARGET redirected, `#fragment`s carried, external/protocol-relative/bare-
anchor targets left alone, root-relative targets excused only in the rebase
half, and line endings preserved via `newline=''` so a CRLF checkout is not
silently relaid to LF (the WI-234/WI-337 lesson).
"""

import subprocess

from conftest import SCRIPTS, load_script, pin_autocrlf, run_py, skip_without_env_gates

sm = load_script("spec_move")


# --- fixtures -------------------------------------------------------------------


def _spec_with_links(repo):
    """A live spec carrying one link at each depth, an anchor, an absolute path
    and an http URL — the shapes that must be rewritten and the shapes that must
    not (the WI-353 fixture, restored verbatim)."""
    (repo / "docs" / "specs").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "requirements").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "log.md").write_text(
        "# Log\n\n## Anchor\n\ntext\n", encoding="utf-8"
    )
    (repo / "docs" / "specs" / "SIBLING.md").write_text("# Sibling\n", encoding="utf-8")
    (repo / "docs" / "requirements" / "work-items.csv").write_text(
        "WI-ID\n", encoding="utf-8"
    )
    (repo / "PROCESS.md").write_text("# Process\n", encoding="utf-8")
    body = (
        "# WI-001\n\n"
        "- same dir: [sib](SIBLING.md)\n"
        "- explicit same dir: [sib2](./SIBLING.md)\n"
        "- one up: [log](../log.md)\n"
        "- one up with anchor: [anchor](../log.md#anchor)\n"
        "- two up: [process](../../PROCESS.md)\n"
        "- sideways: [wis](../requirements/work-items.csv)\n"
        "- external: [ext](https://example.invalid/docs/specs/WI-001.md)\n"
        "- fragment: [frag](#WI-001)\n"
    )
    path = repo / "docs" / "specs" / "WI-001.md"
    path.write_text(body, encoding="utf-8")
    return path


ARCHIVED = "docs/archive/specs/WI-001.2026-01-01.md"


def _archive(repo):
    """The archival move through the REAL indivisible operation."""
    touched, err = sm.move_spec(repo, "docs/specs/WI-001.md", ARCHIVED)
    assert err is None, err
    return touched


# --- the inbound half (WI-288): redirect every link to the vacated path ---------


def test_move_relinks_inbound_links_from_every_depth(tmp_path):
    """Archival must redirect inbound markdown links, or it strands a dangling
    link — the live 2026-07-24 failure, where a train's own docs/log.md entry
    linked the spec it was closing and the break only surfaced on the composed
    tree as a red check_docs. Resolution is by resolved PATH, so all three
    depths are covered by one rule, and each replacement is re-relativised to
    its own file's directory."""
    repo = tmp_path
    _spec_with_links(repo)
    (repo / "docs" / "reviews").mkdir(parents=True)
    (repo / "docs" / "log.md").write_text(
        "# Log\n\n## Anchor\n\nWI-001 landed, spec [WI-001](specs/WI-001.md) refers.\n"
        "With a fragment too: [anchor](specs/WI-001.md#done-when).\n",
        encoding="utf-8",
    )
    (repo / "docs" / "reviews" / "001-REVIEW-A.md").write_text(
        "Judged against [the spec](../specs/WI-001.md).\n", encoding="utf-8"
    )
    (repo / "README.md").write_text(
        "Root link: [spec](docs/specs/WI-001.md)\n"
        "Untouched: [ext](https://example.com/specs/WI-001.md) [frag](#specs)\n",
        encoding="utf-8",
    )
    _archive(repo)

    log = (repo / "docs" / "log.md").read_text(encoding="utf-8")
    # link TEXT preserved, only the TARGET redirected (the repo convention)
    assert "[WI-001](archive/specs/WI-001.2026-01-01.md)" in log
    assert "[anchor](archive/specs/WI-001.2026-01-01.md#done-when)" in log
    # one level deeper: re-relativised, not copied verbatim
    review = (repo / "docs" / "reviews" / "001-REVIEW-A.md").read_text(encoding="utf-8")
    assert "[the spec](../archive/specs/WI-001.2026-01-01.md)" in review
    # from the repo root the target keeps its docs/ prefix
    readme = (repo / "README.md").read_text(encoding="utf-8")
    assert "[spec](docs/archive/specs/WI-001.2026-01-01.md)" in readme
    # an external URL that merely *contains* the path, and a bare fragment, are
    # left exactly alone
    assert "[ext](https://example.com/specs/WI-001.md)" in readme
    assert "[frag](#specs)" in readme


def test_relink_preserves_crlf_and_skips_unrelated_files(tmp_path):
    """The rewrite must not convert a CRLF checkout to LF (the WI-234 splice
    discipline), and a file with no matching link must not be rewritten at all."""
    repo = tmp_path
    _spec_with_links(repo)
    crlf = repo / "docs" / "crlf.md"
    with crlf.open("w", encoding="utf-8", newline="") as fh:
        fh.write("line one\r\nsee [s](specs/WI-001.md)\r\n")
    other = repo / "docs" / "other.md"
    with other.open("w", encoding="utf-8", newline="") as fh:
        fh.write("nothing here\r\nlinks [x](other.md)\r\n")
    before = other.read_bytes()

    touched = _archive(repo)

    raw = crlf.read_bytes()
    assert b"[s](archive/specs/WI-001.2026-01-01.md)" in raw
    # every newline is still CRLF: strip the CRLFs and no bare LF may remain
    assert b"\r\n" in raw and b"\n" not in raw.replace(b"\r\n", b"")
    assert other.read_bytes() == before  # byte-identical, not rewritten
    assert "docs/crlf.md" in touched
    assert "docs/other.md" not in touched


# --- the outbound half (WI-353): rebase the moved file's own links --------------


def test_move_rebases_the_moved_specs_own_links(tmp_path):
    _spec_with_links(tmp_path)
    _archive(tmp_path)
    text = (tmp_path / ARCHIVED).read_text(encoding="utf-8")
    # Each relative link now resolves from one directory deeper.
    assert "](../../specs/SIBLING.md)" in text
    assert "](../../log.md)" in text
    assert "](../../log.md#anchor)" in text, "the #fragment must survive"
    assert "](../../../PROCESS.md)" in text
    assert "](../../requirements/work-items.csv)" in text
    # ...and the shapes that do not depend on the holding directory are untouched.
    assert "](https://example.invalid/docs/specs/WI-001.md)" in text
    assert "](#WI-001)" in text
    # The link TEXT is never touched.
    for label in ("[sib]", "[log]", "[anchor]", "[process]", "[wis]", "[ext]"):
        assert label in text
    # A root-relative target resolves independently of the holding directory, so
    # moving the file cannot break it — excused in the REBASE half only (the
    # inbound half must still consider it: moving the TARGET can break it).
    assert (
        sm._rebased_link_target("/docs/log.md", "docs/specs", "docs/archive/specs")
        is None
    )
    assert sm._resolvable_link("/docs/log.md") is not None


def test_the_rebase_is_a_no_op_when_the_directory_does_not_change(tmp_path):
    path = _spec_with_links(tmp_path)
    before = path.read_text(encoding="utf-8")
    assert (
        sm._rebase_moved_spec_links(
            tmp_path, [("docs/specs/WI-001.md", "docs/specs/WI-001.md")]
        )
        == []
    )
    assert path.read_text(encoding="utf-8") == before


def test_the_rebase_preserves_crlf(tmp_path):
    """The WI-234 splice discipline on the MOVED file itself."""
    (tmp_path / "docs" / "specs").mkdir(parents=True)
    (tmp_path / "docs" / "log.md").write_text("# Log\n", encoding="utf-8")
    crlf = "# WI-001\r\n\r\n[log](../log.md)\r\n"
    with (tmp_path / "docs" / "specs" / "WI-001.md").open(
        "w", encoding="utf-8", newline=""
    ) as fh:
        fh.write(crlf)
    touched, err = sm.move_spec(tmp_path, "docs/specs/WI-001.md", ARCHIVED)
    assert err is None, err
    with (tmp_path / ARCHIVED).open("r", encoding="utf-8", newline="") as fh:
        out = fh.read()
    assert "](../../log.md)" in out
    assert "\r\n" in out, "CRLF was rewritten to LF"
    assert "\n" not in out.replace("\r\n", ""), "a lone LF was introduced"


# --- the guard and its mutation twin (the WI-393 deliverable's own bar) ---------


def test_the_archived_spec_passes_check_docs(tmp_path):
    """The end-to-end assertion the WI is actually about: run the REAL link
    checker over the result. Without the rebase this reported six broken links."""
    _spec_with_links(tmp_path)
    _archive(tmp_path)
    proc = run_py([SCRIPTS / "check_docs.py", "--root", tmp_path], cwd=tmp_path)
    assert "0 broken" in proc.stdout + proc.stderr, proc.stdout + proc.stderr


def test_without_the_rebase_the_same_fixture_is_broken(tmp_path):
    """The mutation twin, run against the shipped move rather than a hand-edit:
    move the file the way archival does but skip the ritual, and the same
    fixture must FAIL check_docs. A guard whose defect it cannot reproduce is
    not a guard."""
    src = _spec_with_links(tmp_path)
    dest = tmp_path / "docs" / "archive" / "specs" / "WI-001.2026-01-01.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    src.replace(dest)  # the move alone — no rebase, no inbound redirect
    proc = run_py([SCRIPTS / "check_docs.py", "--root", tmp_path], cwd=tmp_path)
    out = proc.stdout + proc.stderr
    assert "0 broken" not in out, out
    assert "broken link" in out, out


def test_both_halves_of_the_ritual_still_run(tmp_path):
    """The indivisible-ritual rule (WI-288, extended by WI-353): one call runs
    the INBOUND redirect and the OUTBOUND rebase — neither is reachable alone."""
    _spec_with_links(tmp_path)
    (tmp_path / "docs" / "log.md").write_text(
        "# Log\n\n## Anchor\n\nsee [spec](specs/WI-001.md)\n", encoding="utf-8"
    )
    _archive(tmp_path)
    log = (tmp_path / "docs" / "log.md").read_text(encoding="utf-8")
    assert "](archive/specs/WI-001.2026-01-01.md)" in log, log
    text = (tmp_path / ARCHIVED).read_text(encoding="utf-8")
    assert "](../../log.md)" in text


# --- the rewritten move (the handback shape) ------------------------------------


def test_a_move_with_new_text_still_runs_the_whole_ritual(tmp_path):
    """A caller whose move REWRITES the file on the way (handback.py's returned
    spec) gets the same indivisible ritual: the supplied text lands at the
    destination, then both halves run on the moved pair."""
    root = tmp_path
    (root / "docs" / "work" / "active" / "wi-9").mkdir(parents=True)
    (root / "docs" / "log.md").write_text(
        "see [spec](work/active/wi-9/WI-9-x.md)\n", encoding="utf-8"
    )
    src = root / "docs" / "work" / "active" / "wi-9" / "WI-9-x.md"
    src.write_text("+++\n+++\n[log](../../../log.md)\n", encoding="utf-8")
    new_text = (
        "+++\nblockref = 'docs/work/queued/WI-9-x.md'\n+++\n[log](../../../log.md)\n"
    )
    touched, err = sm.move_spec(
        root,
        "docs/work/active/wi-9/WI-9-x.md",
        "docs/work/queued/WI-9-x.md",
        new_text=new_text,
    )
    assert err is None, err
    assert not src.exists()
    out = (root / "docs" / "work" / "queued" / "WI-9-x.md").read_text(encoding="utf-8")
    assert "blockref" in out, "the supplied text is what moved"
    # queued/ is one directory SHALLOWER than active/<branch>/, so the rebase
    # must shorten the target rather than deepen it.
    assert "[log](../../log.md)" in out
    log = (root / "docs" / "log.md").read_text(encoding="utf-8")
    assert "[spec](work/queued/WI-9-x.md)" in log


# --- refusals and the expected-relink oracle ------------------------------------


def test_a_missing_source_is_a_refusal_not_a_traceback(tmp_path):
    touched, err = sm.move_spec(tmp_path, "docs/specs/GONE.md", ARCHIVED)
    assert touched is None
    assert "GONE.md" in err


def test_an_existing_destination_is_a_refusal(tmp_path):
    _spec_with_links(tmp_path)
    dest = tmp_path / ARCHIVED
    dest.parent.mkdir(parents=True)
    dest.write_text("already here\n", encoding="utf-8")
    touched, err = sm.move_spec(tmp_path, "docs/specs/WI-001.md", ARCHIVED)
    assert touched is None
    assert "exists" in err


def test_expected_relink_is_the_pure_oracle_of_the_inbound_half(tmp_path):
    """`expected_relink` answers "what would this file say after the redirect"
    without touching disk — the oracle `integrate._abandoned_claim` uses to
    convict or excuse a relinked doc inside a crashed claim's one commit."""
    remap = {"docs/specs/WI-001.md": "docs/archive/specs/WI-001.2026-01-01.md"}
    text = "see [spec](specs/WI-001.md#a) and [ext](https://x/specs/WI-001.md)\n"
    out = sm.expected_relink(text, "docs", remap)
    assert "[spec](archive/specs/WI-001.2026-01-01.md#a)" in out
    assert "[ext](https://x/specs/WI-001.md)" in out
    # a file the redirect would not touch comes back byte-identical
    assert sm.expected_relink("plain [x](other.md)\n", "docs", remap) == (
        "plain [x](other.md)\n"
    )


# --- the CLI (the worker's by-hand close and archival moves) --------------------


def test_the_cli_archive_mode_computes_the_dated_destination(tmp_path):
    _spec_with_links(tmp_path)
    (tmp_path / "docs" / "log.md").write_text(
        "# Log\n\n## Anchor\n\nsee [spec](specs/WI-001.md)\n", encoding="utf-8"
    )
    proc = run_py(
        [
            SCRIPTS / "spec_move.py",
            "--root",
            tmp_path,
            "--archive",
            "docs/specs/WI-001.md",
            "--date",
            "2026-01-01",
        ],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (tmp_path / ARCHIVED).is_file()
    log = (tmp_path / "docs" / "log.md").read_text(encoding="utf-8")
    assert "](archive/specs/WI-001.2026-01-01.md)" in log


def test_the_cli_moves_src_to_an_explicit_dest(tmp_path):
    (tmp_path / "docs" / "work" / "active" / "wi-1").mkdir(parents=True)
    src = tmp_path / "docs" / "work" / "active" / "wi-1" / "WI-1-x.md"
    src.write_text("[log](../../../log.md)\n", encoding="utf-8")
    (tmp_path / "docs" / "log.md").write_text("# Log\n", encoding="utf-8")
    proc = run_py(
        [
            SCRIPTS / "spec_move.py",
            "--root",
            tmp_path,
            "docs/work/active/wi-1/WI-1-x.md",
            "docs/work/complete/WI-1-x.md",
        ],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = (tmp_path / "docs" / "work" / "complete" / "WI-1-x.md").read_text(
        encoding="utf-8"
    )
    assert "[log](../../log.md)" in out


def test_the_cli_refuses_a_missing_source_nonzero(tmp_path):
    proc = run_py(
        [SCRIPTS / "spec_move.py", "--root", tmp_path, "--archive", "docs/specs/NO.md"],
        cwd=tmp_path,
    )
    assert proc.returncode != 0
    assert "NO.md" in proc.stdout + proc.stderr


# --- git integration: the move is staged when the tree is a repo ----------------


def _seeded_repo(repo):
    """A committed git repo rooted at `repo`, with a `_git` runner returned."""

    def _git(*args):
        proc = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        return proc.stdout

    _git("init", "-q")
    pin_autocrlf(repo)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git("config", "user.email", "t@example.com")
    _git("config", "user.name", "T")
    _git("config", "commit.gpgsign", "false")
    return _git


def test_inside_a_git_repo_the_move_is_a_staged_git_mv(tmp_path):
    """`git mv` inside the worktree so the caller's `git add -A` (or the CLI
    user's closing commit) stages the move as a move; a plain rename is the
    fallback for an untracked file or a non-repo tree (the WI-287 shape)."""
    skip_without_env_gates("git")
    repo = tmp_path
    _git = _seeded_repo(repo)
    _spec_with_links(repo)
    _git("add", "-A")
    _git("commit", "-qm", "seed")
    touched, err = sm.move_spec(repo, "docs/specs/WI-001.md", ARCHIVED)
    assert err is None, err
    tracked = _git("ls-files").split()
    assert ARCHIVED in tracked
    assert "docs/specs/WI-001.md" not in tracked


def test_the_move_stages_the_working_tree_content_not_the_stale_index_blob(tmp_path):
    """THE WI-408 FIELD DEFECT, in the exact shape it fired (WI-401's close,
    2026-08-02): the worker filled the spec's `## Deliverable` — an UNSTAGED
    working-tree edit — and then ran the ritual for the close move. `git mv`
    moves the working file but stages the rename FROM THE INDEX, so the staged
    destination blob was the stale pre-edit content and the just-written
    Deliverable silently vanished from the close commit; it was caught only
    because git's rename-similarity read 100% where the edit should have
    lowered it, and repaired by amending. The contract pinned here: after
    `move_spec`, the destination's STAGED blob carries the source's
    WORKING-TREE content, byte-for-byte.

    The fixture spec deliberately carries NO rewritable links (fragment and
    external only), so the rebase half cannot mask the defect by re-adding the
    destination as one of its own rewrites — exactly the WI-401 spec shape."""
    skip_without_env_gates("git")
    repo = tmp_path
    _git = _seeded_repo(repo)
    spec = repo / "docs" / "work" / "active" / "wi-9" / "WI-9-x.md"
    spec.parent.mkdir(parents=True)
    spec.write_text(
        "+++\nid = 'WI-9'\n+++\n\n"
        "see [frag](#done-when) and [ext](https://example.invalid/spec.md)\n",
        encoding="utf-8",
    )
    _git("add", "-A")
    _git("commit", "-qm", "seed")
    # The close shape: fill the Deliverable and do NOT stage it.
    with spec.open("a", encoding="utf-8", newline="") as fh:
        fh.write("\n## Deliverable\n\nShipped 2026-08-02; totals quoted.\n")
    touched, err = sm.move_spec(
        repo, "docs/work/active/wi-9/WI-9-x.md", "docs/work/complete/WI-9-x.md"
    )
    assert err is None, err
    staged = _git("show", ":docs/work/complete/WI-9-x.md")
    assert "Shipped 2026-08-02; totals quoted." in staged, (
        "the unstaged Deliverable vanished from the staged blob (the stale-index"
        " defect): " + staged
    )
    # No half-staged residue either: the staged blob IS the working-tree file.
    on_disk = (repo / "docs" / "work" / "complete" / "WI-9-x.md").read_text(
        encoding="utf-8"
    )
    assert staged == on_disk
