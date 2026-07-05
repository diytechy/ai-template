"""check_docs.py: the hand-written doc set stays navigable — broken intra-repo
links fail, orphan docs warn (fail only with --strict-orphans), the root README
must state the `PROJECT-VISION:` tag exactly once (process.md §4 G1's
mechanizable half), and the git-gated staleness pass degrades to a clean skip
(process.md §3 "The doc set must stay navigable")."""

import re

from conftest import SCRIPTS, load_script, run_py


def _add_must_need(scaffold, sid="SN-005"):
    """Append a real Must-priority need to the scaffold's SN registry, contiguous
    with the core-needs table so the priority-column parser sees it."""
    reg = scaffold / "docs" / "requirements" / "stakeholder-needs.md"
    out = []
    for line in reg.read_text(encoding="utf-8").splitlines():
        out.append(line)
        if line.startswith("| SN-000 |"):
            out.append("| {} | Do the thing | matters | M | it works |".format(sid))
    reg.write_text("\n".join(out) + "\n", encoding="utf-8")


def _set_inventory(scaffold, body):
    """Replace the README sn-inventory section body (markers kept)."""
    r = scaffold / "README.md"
    text = re.sub(
        r"<!-- sn-inventory -->.*<!-- /sn-inventory -->",
        "<!-- sn-inventory -->\n" + body + "\n<!-- /sn-inventory -->",
        r.read_text(encoding="utf-8"),
        flags=re.S,
    )
    r.write_text(text, encoding="utf-8")


# --- CLI behaviour on a real scaffold ---------------------------------------


def test_clean_scaffold_passes(scaffold):
    # A fresh scaffold has no broken links; its standalone docs are orphan
    # WARNINGS only, so the harness floor stays green out of the box.
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "check_docs: OK" in proc.stdout
    assert "0 broken" in proc.stdout


def test_broken_file_link_fails(scaffold):
    (scaffold / "docs" / "guide.md").write_text(
        "# Guide\n\nSee [the design](design-notes.md).\n", encoding="utf-8"
    )
    proc = run_py(["scripts/check_docs.py"], cwd=scaffold)
    assert proc.returncode == 1
    assert "broken link -> design-notes.md" in proc.stdout
    assert "target not found" in proc.stdout


def test_broken_anchor_fails(scaffold):
    (scaffold / "docs" / "guide.md").write_text(
        "# Guide\n\n## Real Section\n\nJump to [nowhere](#ghost-section).\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/check_docs.py"], cwd=scaffold)
    assert proc.returncode == 1
    assert "broken link -> #ghost-section" in proc.stdout
    assert "no such anchor in this doc" in proc.stdout


def test_valid_anchor_link_passes(scaffold):
    # A correct same-file anchor (GitHub heading slug) is not a broken link;
    # the doc is still an orphan warning, but the run is green.
    (scaffold / "docs" / "guide.md").write_text(
        "# Guide\n\n## My Section\n\nBack to [it](#my-section).\n", encoding="utf-8"
    )
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "0 broken" in proc.stdout


def test_orphan_warns_by_default_and_fails_when_strict(scaffold):
    # A doc nothing links to is unreachable from the entry roots.
    (scaffold / "docs" / "lonely.md").write_text(
        "# Lonely\n\nNo one links here.\n", encoding="utf-8"
    )
    warn = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert warn.returncode == 0, warn.stdout + warn.stderr
    assert "WARN - orphan doc" in warn.stdout
    assert "docs/lonely.md" in warn.stdout

    strict = run_py(
        [
            "scripts/check_docs.py",
            "--ignore",
            "docs/test/report.md",
            "--strict-orphans",
        ],
        cwd=scaffold,
    )
    assert strict.returncode == 1
    assert "FAIL - orphan doc" in strict.stdout


def test_reachable_doc_is_not_orphan(scaffold):
    # Linking the new doc from an entry root (AGENTS.md) clears the warning.
    (scaffold / "docs" / "guide.md").write_text(
        "# Guide\n\nContent.\n", encoding="utf-8"
    )
    agents = scaffold / "AGENTS.md"
    agents.write_text(
        agents.read_text(encoding="utf-8") + "\n\nSee [the guide](docs/guide.md).\n",
        encoding="utf-8",
    )
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "docs/guide.md" not in proc.stdout  # neither broken nor orphaned


def test_ignore_drops_doc_from_scan(scaffold):
    # --ignore removes a doc from the scanned set entirely (the harness uses it
    # for the generated docs/test/report.md), so its own links aren't checked.
    (scaffold / "docs" / "generated.md").write_text(
        "[stale](gone.md)\n", encoding="utf-8"
    )
    fails = run_py(["scripts/check_docs.py"], cwd=scaffold)
    assert fails.returncode == 1  # the broken link is caught when scanned
    passes = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/generated.md"], cwd=scaffold
    )
    assert passes.returncode == 0, passes.stdout + passes.stderr


# --- the PROJECT-VISION tag (process.md §4 G1's mechanizable half) ------------


def test_missing_vision_tag_fails(scaffold):
    # The scaffolded README carries the singleton tag; a README rewritten
    # without it loses the canonical vision statement and the run goes red.
    (scaffold / "README.md").write_text("# proj\n\nNo vision here.\n", encoding="utf-8")
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 1
    assert "missing the PROJECT-VISION: tag" in proc.stdout


def test_duplicate_vision_tag_fails(scaffold):
    # The tag is a singleton: a second statement is a re-authored variant —
    # other docs must point at the tag, never restate it.
    readme = scaffold / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8") + "\n**PROJECT-VISION:** again.\n",
        encoding="utf-8",
    )
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 1
    assert "2 PROJECT-VISION: tags" in proc.stdout


def test_vision_tag_in_code_is_not_a_statement(scaffold):
    # Quoting the convention in a code span or fence isn't stating a vision:
    # the scaffold README keeps its one real tag and the run stays green.
    readme = scaffold / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8")
        + "\nThe tag is `PROJECT-VISION:`.\n\n```\nPROJECT-VISION: quoted\n```\n",
        encoding="utf-8",
    )
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_no_root_readme_warns_not_fails(tmp_path):
    # A bare doc tree with no README stays usable: the vision check degrades to
    # a warning (missing README is a louder, different problem).
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a.md").write_text("# A\n", encoding="utf-8")
    proc = run_py([SCRIPTS / "check_docs.py", "--root", tmp_path], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "tag check skipped" in proc.stdout


def test_staleness_skips_without_git(tmp_path):
    # --stale must degrade gracefully where git isn't available or the tree
    # isn't a work tree: it skips, it doesn't fail. tmp_path is not a git repo.
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a.md").write_text("# A\n", encoding="utf-8")
    proc = run_py(
        [SCRIPTS / "check_docs.py", "--root", tmp_path, "--stale"], cwd=tmp_path
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "staleness check skipped" in proc.stdout


# --- the README SN inventory (opt-in coverage; process.md §4 G1) --------------


def test_inventory_clean_scaffold_passes(scaffold):
    # The template ships the sn-inventory section citing the -000 placeholder,
    # and the scaffold registry has only SN-000, so both directions are satisfied.
    assert "<!-- sn-inventory -->" in (scaffold / "README.md").read_text(
        encoding="utf-8"
    )
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_inventory_uncovered_must_fails(scaffold):
    # A Must need the README cites nowhere fails: a requirements add pulls on
    # the README (the whole point of the coverage direction).
    _add_must_need(scaffold, "SN-005")
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 1
    assert "SN-005 (Must/Should) is covered by no sn-inventory bullet" in proc.stdout


def test_inventory_bad_citation_fails(scaffold):
    # A bullet citing an id absent from the registry is a broken citation.
    _set_inventory(scaffold, "- **X** — does x (SN-099)")
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 1
    assert "cites SN-099, absent from the needs registry" in proc.stdout


def test_inventory_absent_section_is_opt_in(scaffold):
    # No sn-inventory section -> the check is silent even with an uncovered Must
    # need (opt-in by presence). Removing the markers proves it.
    _add_must_need(scaffold, "SN-005")
    r = scaffold / "README.md"
    r.write_text(
        re.sub(
            r"<!-- sn-inventory -->.*<!-- /sn-inventory -->",
            "",
            r.read_text(encoding="utf-8"),
            flags=re.S,
        ),
        encoding="utf-8",
    )
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_registry_needs_parses_priority(tmp_path):
    # -000 excluded from both sets; Could and priority-less (edge-case) rows are
    # in the existence set but not the Must/Should floor.
    check = load_script("check_docs")
    reg = tmp_path / "stakeholder-needs.md"
    reg.write_text(
        "# Needs\n\n"
        "| SN-ID | Need | Priority | Acceptance |\n"
        "|---|---|---|---|\n"
        "| SN-000 | example | M | x |\n"
        "| SN-001 | must | M | x |\n"
        "| SN-002 | should | S | x |\n"
        "| SN-003 | could | C | x |\n\n"
        "## Edge cases\n\n"
        "| SN-ID | Scenario | Expected |\n"
        "|---|---|---|\n"
        "| SN-004 | boom | handled |\n",
        encoding="utf-8",
    )
    all_ids, must_should = check._registry_needs(reg)
    assert all_ids == {"SN-001", "SN-002", "SN-003", "SN-004"}
    assert must_should == {"SN-001", "SN-002"}


# --- harness wiring ----------------------------------------------------------


def test_harness_wires_stale_into_doc_navigability():
    # check.py passes --stale to the doc-navigability step (warn-only) so the
    # lying-map heuristic runs inside the harness.
    src = (SCRIPTS / "check.py").read_text(encoding="utf-8")
    i = src.index("check_docs.py")
    assert "--stale" in src[i : i + 200]


def test_harness_runs_doc_navigability_at_g1(scaffold):
    # G1's only step is doc-navigability; a broken link must fail that gate.
    (scaffold / "docs" / "guide.md").write_text(
        "# Guide\n\n[missing](nope.md)\n", encoding="utf-8"
    )
    proc = run_py(["scripts/check.py", "--gate", "G1"], cwd=scaffold)
    assert proc.returncode != 0
    assert "doc-navigability" in proc.stdout
    assert "RESULT: FAIL" in proc.stdout


# --- importable units (no subprocess) ---------------------------------------


def test_slugify_matches_github_style():
    check = load_script("check_docs")
    assert check.slugify("Hello World") == "hello-world"
    # Removed punctuation leaves the gaps -> the GitHub double hyphen.
    assert check.slugify("3. Traceability & anti-duplication") == (
        "3-traceability--anti-duplication"
    )
    assert check.slugify("`code` and *emphasis*") == "code-and-emphasis"


def test_parse_doc_scope():
    # Links inside code (inline + fenced) and images are out of scope; external
    # links are captured here but skipped by the link checker.
    check = load_script("check_docs")
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "doc.md"
        p.write_text(
            "# Title & More\n"
            "[real](other.md)\n"
            "![pic](image.png)\n"
            "[ext](https://example.com)\n"
            "`[incode](nope.md)`\n"
            "```\n[fenced](nope.md)\n```\n",
            encoding="utf-8",
        )
        info = check.parse_doc(p)
    dests = [dest for _, dest in info["links"]]
    assert "other.md" in dests
    assert "https://example.com" in dests
    assert "image.png" not in dests  # image skipped
    assert "nope.md" not in dests  # inline-code + fenced skipped
    assert "title--more" in info["anchors"]


def test_find_stale_uses_injected_commit_times(tmp_path):
    # find_stale's git dependency is injected as a path->epoch callable, so the
    # comparison logic is unit-testable without real commits.
    check = load_script("check_docs")
    doc = tmp_path / "guide.md"
    doc.write_text("Implements [the module](mod.py); see [other](peer.md).\n", "utf-8")
    (tmp_path / "mod.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "peer.md").write_text("# Peer\n", encoding="utf-8")
    parsed = {doc.resolve(): check.parse_doc(doc)}
    root = tmp_path.resolve()

    times = {doc.resolve(): 100, (tmp_path / "mod.py").resolve(): 200}
    stale = check.find_stale(parsed, root, lambda p: times.get(p))
    # The source file changed after the doc -> flagged; the doc-to-doc link is
    # never a staleness signal (too noisy).
    assert [s[2] for s in stale] == ["mod.py"]

    times[doc.resolve()] = 300  # doc now newer than everything -> clean
    assert check.find_stale(parsed, root, lambda p: times.get(p)) == []


def test_git_commit_lookup_none_outside_work_tree(tmp_path):
    check = load_script("check_docs")
    # A bare temp dir is not a git work tree (and the call also returns None
    # when git isn't installed) -> staleness is skipped.
    assert check.git_commit_lookup(tmp_path) is None
