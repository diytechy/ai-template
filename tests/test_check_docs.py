"""check_docs.py: the hand-written doc set stays navigable — broken intra-repo
links fail, orphan docs warn (fail only with --strict-orphans), the root README
must state the `PROJECT-VISION:` tag exactly once (process.md §4 G1's
mechanizable half), and the git-gated staleness pass degrades to a clean skip
(process.md §3 "The doc set must stay navigable")."""

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


def _append_readme(scaffold, text):
    """Append a line to the scaffold README (the check scans the whole file, so a
    citation anywhere counts — no delimiter markers)."""
    r = scaffold / "README.md"
    r.write_text(r.read_text(encoding="utf-8") + "\n" + text + "\n", encoding="utf-8")


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


def test_link_example_in_double_backtick_span_is_not_a_link(scaffold):
    # WI-174: a doc that QUOTES markdown-link syntax as an example wraps it in a
    # double-backtick span — needed because the label itself holds backticks:
    # `` [`foo`](foo.md) ``. That span is code, not a navigational link, so it
    # must not surface as a broken link to foo.md. A single-backtick regex
    # mis-splits the run and leaks a phantom `[](foo.md)`; equal-length matching
    # doesn't. (This is the exact false positive that reddened the meta bar.)
    (scaffold / "docs" / "guide.md").write_text(
        "# Guide\n\nRender the label as a link, e.g. `` [`foo`](foo.md) ``.\n",
        encoding="utf-8",
    )
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "0 broken" in proc.stdout
    assert "foo.md" not in proc.stdout


def test_parse_doc_strips_links_in_multi_backtick_spans(tmp_path):
    # WI-174 (unit): parse_doc strips inline code spans of ANY backtick-run length
    # before extracting links, so a quoted `` [`x`](x.md) `` example is not a link
    # while a real link on the same line still is — the strip stays precise.
    check = load_script("check_docs")
    doc = tmp_path / "d.md"
    doc.write_text(
        "See [real](real.md) but ignore `` [`x`](x.md) `` and `single()`.\n",
        encoding="utf-8",
    )
    dests = [dest for _ln, dest in check.parse_doc(doc)["links"]]
    assert dests == ["real.md"]


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


def test_staleness_prints_hint_not_warn(tmp_path):
    # Staleness is a low-confidence nudge: printed as `hint` (below WARN), never
    # a finding. Needs a git repo with a doc committed BEFORE a non-doc it links.
    import os
    import subprocess

    repo = tmp_path

    def git(*args, when=None):
        env = dict(os.environ)
        if when:
            env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = when
        subprocess.run(
            ["git", "-C", str(repo), *args], check=True, env=env, capture_output=True
        )

    git("init")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "T")
    (repo / "guide.md").write_text("# Guide\n\nSee [mod](mod.py).\n", encoding="utf-8")
    git("add", "guide.md")
    git("commit", "-m", "doc", when="2020-01-01T00:00:00")
    (repo / "mod.py").write_text("x = 1\n", encoding="utf-8")
    git("add", "mod.py")
    git("commit", "-m", "code later", when="2021-01-01T00:00:00")

    proc = run_py([SCRIPTS / "check_docs.py", "--root", repo, "--stale"], cwd=repo)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "hint - possibly stale" in proc.stdout
    assert "mod.py" in proc.stdout
    assert "WARN - possibly stale" not in proc.stdout


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


# --- README need coverage (opt-out, marker-free; process.md §4 G1) ------------


def test_inventory_clean_scaffold_passes(scaffold):
    # A fresh scaffold has only the -000 placeholder in both the README and the
    # registry, so both directions are vacuously satisfied (no markers needed).
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_inventory_uncovered_must_fails_by_default(scaffold):
    # ON by default (opt-out): a real Must need the README cites nowhere fails,
    # with NO sn-inventory markers anywhere — a requirements add pulls on the
    # README (the coverage direction, now the default).
    _add_must_need(scaffold, "SN-005")
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 1
    assert "SN-005 (Must/Should) is cited by no README bullet" in proc.stdout


def test_inventory_bad_citation_fails(scaffold):
    # An SN id cited in the README but absent from the registry is a broken
    # citation (scanned from the whole file, no markers).
    _append_readme(scaffold, "- **X** — does x (SN-099)")
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 1
    assert "README cites SN-099, absent from the needs registry" in proc.stdout


def test_inventory_opt_out_marker_silences(scaffold):
    # Opt-out: an `<!-- sn-inventory: off -->` comment disables the check even
    # with an uncovered Must need — the escape hatch for a repo that doesn't want
    # README-level need tracing.
    _add_must_need(scaffold, "SN-005")
    _append_readme(scaffold, "<!-- sn-inventory: off -->")
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


def test_registry_needs_exempts_draft_section_from_must_floor(tmp_path):
    # SN maturity is section-as-state (derived-gate §4a): a Must need under a
    # "draft" heading is unratified, so it stays out of the Must/Should README
    # floor (existence still holds) until its row is moved up to a ratified section.
    check = load_script("check_docs")
    reg = tmp_path / "stakeholder-needs.md"
    reg.write_text(
        "# Needs\n\n## Core needs\n\n"
        "| SN-ID | Need | Priority | Acceptance |\n"
        "|---|---|---|---|\n"
        "| SN-001 | ratified must | M | x |\n\n"
        "## Draft needs (unratified)\n\n"
        "| SN-ID | Need | Priority | Acceptance |\n"
        "|---|---|---|---|\n"
        "| SN-050 | drafted must | M | x |\n",
        encoding="utf-8",
    )
    all_ids, must_should = check._registry_needs(reg)
    assert all_ids == {"SN-001", "SN-050"}  # the draft SN still exists
    assert must_should == {"SN-001"}  # ... but is exempt from the README floor


def test_inventory_draft_must_need_not_required_in_readme(scaffold):
    # End-to-end: a Must need drafted under a "## Draft needs" heading does NOT
    # force a README citation (it is unratified); the check stays green.
    reg = scaffold / "docs" / "requirements" / "stakeholder-needs.md"
    reg.write_text(
        reg.read_text(encoding="utf-8") + "\n## Draft needs (unratified)\n\n"
        "| SN-ID | Need | Priority | Acceptance |\n"
        "|---|---|---|---|\n"
        "| SN-050 | drafted must | M | x |\n",
        encoding="utf-8",
    )
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


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


# --- the generated OKF bundle is dropped from discovery (WI-066) -------------


def test_okf_bundle_dropped_from_doc_scan(scaffold):
    # WI-066: docs/okf/ is a fully-generated tree whose own gen_okf.py --check
    # owns freshness, so check_docs never lints it — no okf file is counted,
    # orphaned or link-checked. A genuinely-broken NON-okf link is still caught,
    # and a link INTO the bundle still resolves (the files stay on disk).
    from conftest import make_minimal_project

    make_minimal_project(scaffold)
    assert run_py([SCRIPTS / "gen_okf.py"], cwd=scaffold).returncode == 0
    assert (scaffold / "docs" / "okf" / "index.md").exists()  # bundle really on disk

    agents = scaffold / "AGENTS.md"
    agents.write_text(
        agents.read_text(encoding="utf-8")
        + "\n\nSee [the OKF bundle](docs/okf/index.md).\n",
        encoding="utf-8",
    )
    (scaffold / "docs" / "guide.md").write_text(
        "# Guide\n\nSee [gone](nowhere.md).\n", encoding="utf-8"
    )
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 1  # the real broken link fails the run
    assert "broken link -> nowhere.md" in proc.stdout
    # the entire bundle is out of the scan: never counted, orphaned or reported,
    # and the link into it resolved (no broken-link finding for it)
    assert "docs/okf/" not in proc.stdout


def test_okf_bundle_adds_zero_scanned_docs(scaffold):
    # The doc count must not grow when the ~large bundle appears: generating it
    # adds zero scanned docs (proving the whole tree is excluded, not just
    # orphan-suppressed).
    import re

    from conftest import make_minimal_project

    make_minimal_project(scaffold)
    before = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert before.returncode == 0, before.stdout + before.stderr
    assert run_py([SCRIPTS / "gen_okf.py"], cwd=scaffold).returncode == 0
    after = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert after.returncode == 0, after.stdout + after.stderr
    n_before = int(re.search(r"OK - (\d+) doc", before.stdout).group(1))
    n_after = int(re.search(r"OK - (\d+) doc", after.stdout).group(1))
    assert n_after == n_before
    assert "docs/okf" not in after.stdout


# --- the owner scratchpad is exempt entirely (FB3) ---------------------------


def test_scratchpad_exempt_from_scan(scaffold):
    # FB3: OWNER_SCRATCHPAD.md holds free-form owner notes and is dropped from doc
    # discovery entirely — a broken link in it never gates, and it is never
    # counted, orphaned, or link-checked. The scaffold ships it at the root.
    pad = scaffold / "OWNER_SCRATCHPAD.md"
    assert pad.exists(), "bootstrap must scaffold OWNER_SCRATCHPAD.md"
    pad.write_text(
        pad.read_text(encoding="utf-8") + "\nSee [gone](nowhere-owner.md).\n",
        encoding="utf-8",
    )
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "OWNER_SCRATCHPAD.md" not in proc.stdout
    assert "nowhere-owner.md" not in proc.stdout  # its broken link is never checked


# --- the archive keeps link validation but drops orphan/stale noise (FB4) ----


def test_archive_broken_link_still_fails(scaffold):
    # FB4: a dead link in the frozen history still misleads a reader, so archived
    # docs KEEP broken-link validation (only orphan/stale noise is dropped).
    arch = scaffold / "docs" / "archive" / "old-note.md"
    arch.parent.mkdir(parents=True, exist_ok=True)
    arch.write_text("# Old\n\nSee [the design](design-gone.md).\n", encoding="utf-8")
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 1
    assert "broken link -> design-gone.md" in proc.stdout


def test_archive_doc_not_orphaned_but_live_doc_is(scaffold):
    # FB4: an archived doc nothing links to is frozen context, not an orphan; a
    # live doc nothing links to still warns (the orphan floor is unchanged there).
    (scaffold / "docs" / "archive").mkdir(parents=True, exist_ok=True)
    (scaffold / "docs" / "archive" / "frozen.md").write_text(
        "# Frozen\n\nNo one links here.\n", encoding="utf-8"
    )
    (scaffold / "docs" / "live-lonely.md").write_text(
        "# Lonely\n\nNo one links here either.\n", encoding="utf-8"
    )
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "orphan doc" in proc.stdout and "docs/live-lonely.md" in proc.stdout
    assert "docs/archive/frozen.md" not in proc.stdout  # frozen: orphanhood is noise


def test_find_stale_skips_archive_docs(tmp_path):
    # FB4 (unit): find_stale drops archived docs — an archived doc older than a
    # non-doc it links is not a staleness signal, while a live doc still is.
    check = load_script("check_docs")
    root = tmp_path.resolve()
    (tmp_path / "mod.py").write_text("x = 1\n", encoding="utf-8")
    live = tmp_path / "docs" / "guide.md"
    arch = tmp_path / "docs" / "archive" / "hist.md"
    live.parent.mkdir(parents=True, exist_ok=True)
    arch.parent.mkdir(parents=True, exist_ok=True)
    live.write_text("See [mod](../mod.py).\n", encoding="utf-8")
    arch.write_text("See [mod](../../mod.py).\n", encoding="utf-8")
    parsed = {
        live.resolve(): check.parse_doc(live),
        arch.resolve(): check.parse_doc(arch),
    }
    mod = (tmp_path / "mod.py").resolve()
    # Both docs predate the linked source -> both would flag, but the archived one
    # is skipped: only the live doc is reported stale.
    times = {live.resolve(): 100, arch.resolve(): 100, mod: 200}
    flagged = [s[0] for s in check.find_stale(parsed, root, lambda p: times.get(p))]
    assert flagged == ["docs/guide.md"]


def test_archive_stale_hint_suppressed_but_live_still_hinted(tmp_path):
    # FB4 end-to-end (standing in for the meta tree's own --stale run): an archived
    # doc older than a non-doc it links yields NO stale hint, while a live doc in
    # the same repo still does. Needs a git repo with docs committed before code.
    import os
    import subprocess

    repo = tmp_path

    def git(*args, when=None):
        env = dict(os.environ)
        if when:
            env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = when
        subprocess.run(
            ["git", "-C", str(repo), *args], check=True, env=env, capture_output=True
        )

    git("init")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "T")
    (repo / "docs" / "archive").mkdir(parents=True)
    (repo / "docs" / "archive" / "hist.md").write_text(
        "# History\n\nSee [mod](../../mod.py).\n", encoding="utf-8"
    )
    (repo / "docs" / "guide.md").write_text(
        "# Guide\n\nSee [mod](../mod.py).\n", encoding="utf-8"
    )
    git("add", "-A")
    git("commit", "-m", "docs", when="2020-01-01T00:00:00")
    (repo / "mod.py").write_text("x = 1\n", encoding="utf-8")
    git("add", "mod.py")
    git("commit", "-m", "code later", when="2021-01-01T00:00:00")

    proc = run_py([SCRIPTS / "check_docs.py", "--root", repo, "--stale"], cwd=repo)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "hint - possibly stale: docs/guide.md" in proc.stdout
    assert "docs/archive/hist.md" not in proc.stdout  # frozen: staleness is noise


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


# --- status-surface structure (S-1..S-3; warn-only) ---------------------------


_STATUS_SHAPED = """# Status

- **Open items:**
  - **Needs <human>**:
    - OI-1 - decide the flag
    - OI-9 - decide the port
  - **In flight**:
    - OI-2 - pinning the acceptance predicate

## Scope

- **Goal:** the thing
"""


def _write_status(scaffold, text):
    (scaffold / "docs" / "status.md").write_text(text, encoding="utf-8")


def test_scaffold_status_surface_is_clean(scaffold):
    # A fresh scaffold must produce ZERO S-1..S-3 warnings out of the box: the
    # template status.md is under budget, Open items precede Scope, and the
    # OPEN_ITEMS template's OI-1 example matches STATUS.template's.
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 0
    assert "status.md is" not in proc.stdout  # S-1
    assert "Open items" not in proc.stdout  # S-2 (warn text)
    assert "Needs-<human> item" not in proc.stdout  # S-3
    assert "orphan brief" not in proc.stdout  # S-3 reverse


def test_status_budget_warns_but_never_fails(scaffold):
    # S-1 is warn-only by design (the WI-129 stance): over-budget prose warns
    # and the exit code stays 0.
    _write_status(scaffold, "# Status\n" + "filler line\n" * 130)
    proc = run_py(["scripts/check_docs.py"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARN - status.md is 131 lines (budget 120)" in proc.stdout


def test_status_lint_policy_overrides_and_off(scaffold):
    # An integer in docs/status-lint replaces the default budget; the one word
    # `off` silences S-1..S-3 entirely (here: an order violation too).
    _write_status(
        scaffold, "# Status\n\n## Scope\n\n- Goal\n\n- **Open items:** none\n"
    )
    (scaffold / "docs" / "status-lint").write_text("# comment\n200\n", "utf-8")
    proc = run_py(["scripts/check_docs.py"], cwd=scaffold)
    assert "budget 200" not in proc.stdout  # under the raised budget: no S-1
    assert "after ## Scope" in proc.stdout  # S-2 still live
    (scaffold / "docs" / "status-lint").write_text("off\n", encoding="utf-8")
    proc = run_py(["scripts/check_docs.py"], cwd=scaffold)
    assert "after ## Scope" not in proc.stdout
    assert "status.md is" not in proc.stdout


def test_status_order_and_missing_marker_warn(scaffold):
    # S-2: Scope before the Open-items marker warns; a Scope section with no
    # Open-items marker at all also warns.
    _write_status(
        scaffold, "# Status\n\n## Scope\n\n- Goal\n\n- **Open items:** none\n"
    )
    proc = run_py(["scripts/check_docs.py"], cwd=scaffold)
    assert proc.returncode == 0
    assert "Open items after ## Scope" in proc.stdout
    _write_status(scaffold, "# Status\n\n## Scope\n\n- Goal\n")
    proc = run_py(["scripts/check_docs.py"], cwd=scaffold)
    assert "no Open-items marker" in proc.stdout


def test_oi_coherence_both_directions(scaffold):
    # S-3: a Needs-<human> OI with no brief warns; a briefed OI never named in
    # status.md warns; an In-flight OI needs NO brief; all warn-only (exit 0).
    _write_status(scaffold, _STATUS_SHAPED)
    (scaffold / "docs" / "open-items.md").write_text(
        "# Open items\n\n## OI-1 - decide the flag\n\n- **Decision:** ...\n\n"
        "## OI-8 - stale ruled item\n\n- **Decision:** ...\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/check_docs.py"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "OI-9: a Needs-<human> item" in proc.stdout  # missing brief
    assert "OI-8: briefed in open-items.md" in proc.stdout  # orphan brief
    assert "OI-1" not in proc.stdout  # coherent id is quiet
    assert "OI-2" not in proc.stdout  # in-flight needs no brief


def test_oi_coherence_vacuous_without_open_items(scaffold):
    # S-3 is opt-in: deleting open-items.md silences it (the other status
    # rules stay live).
    _write_status(scaffold, _STATUS_SHAPED)
    (scaffold / "docs" / "open-items.md").unlink()
    proc = run_py(["scripts/check_docs.py"], cwd=scaffold)
    assert proc.returncode == 0
    assert "OI-9" not in proc.stdout
