"""check_docs.py: the hand-written doc set stays navigable — broken intra-repo
links fail, orphan docs warn (fail only with --strict-orphans), the root README
must state the `PROJECT-VISION:` tag exactly once (process.md §4 G1's
mechanizable half), and the git-gated staleness pass degrades to a clean skip
(process.md §3 "The doc set must stay navigable")."""

from conftest import ROOT, SCRIPTS, load_script, run_py


def _add_must_need(scaffold, sid="SN-005"):
    """Append a real Must-priority need to the scaffold's SN registry.

    A scaffold carries the TOML carrier since the cutover, where
    a need is a table and its priority a FIELD — no "contiguous with the core
    table so the column parser sees it" any more, which is one of the shapes the
    markdown carrier forced. The legacy arm stays exercised where a fixture
    deliberately writes markdown."""
    reg = scaffold / "docs" / "requirements" / "stakeholder-needs.toml"
    reg.write_text(
        reg.read_text(encoding="utf-8")
        + '\n[need.{}]\nkind = "core"\nneed = "Do the thing"\n'
        'why = "matters"\npriority = "M"\nacceptance = "it works"\n'.format(sid),
        encoding="utf-8",
    )


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


def test_parse_doc_requires_exact_inline_code_closer(tmp_path):
    check = load_script("check_docs")
    doc = tmp_path / "d.md"
    doc.write_text("``code` [real](real.md)\n", encoding="utf-8")
    dests = [dest for _ln, dest in check.parse_doc(doc)["links"]]
    assert dests == ["real.md"]


def test_parse_doc_strips_multiline_inline_code_span(tmp_path):
    check = load_script("check_docs")
    doc = tmp_path / "d.md"
    doc.write_text("``quoted\n[not real](missing.md)``\n", encoding="utf-8")
    assert check.parse_doc(doc)["links"] == []


def test_parse_doc_ignores_links_inside_spec_frontmatter(tmp_path):
    # A `docs/work/` spec opens with typed TOML, and a `title` that QUOTES a
    # markdown link is describing one, not making one. Parsed as body it became a
    # broken link to a file nobody meant to exist (two of the four the v3 merge
    # carried). The body's real link on the SAME doc must survive the strip, and
    # its line number must not shift.
    check = load_script("check_docs")
    doc = tmp_path / "WI-1-x.md"
    doc.write_text(
        '+++\nid = "WI-1"\ntitle = "strands [WI-n](specs/WI-n.md) on archive"\n'
        "+++\n\nBody cites [real](real.md).\n",
        encoding="utf-8",
    )
    assert check.parse_doc(doc)["links"] == [(6, "real.md")]


def test_parse_doc_keeps_frontmatter_links_when_fence_is_unclosed(tmp_path):
    # Fails in the SAFE direction: a malformed fence declares no frontmatter, so
    # it cannot become a way to hide a real link from the check.
    check = load_script("check_docs")
    doc = tmp_path / "d.md"
    doc.write_text('+++\ntitle = "see [x](missing.md)"\n\nbody\n', encoding="utf-8")
    assert [dest for _ln, dest in check.parse_doc(doc)["links"]] == ["missing.md"]


def test_parse_doc_only_treats_a_first_line_fence_as_frontmatter(tmp_path):
    # `+++` mid-document is prose (or a thematic break), never a frontmatter open.
    check = load_script("check_docs")
    doc = tmp_path / "d.md"
    doc.write_text("intro\n+++\n[x](missing.md)\n+++\n", encoding="utf-8")
    assert [dest for _ln, dest in check.parse_doc(doc)["links"]] == ["missing.md"]


def test_frontmatter_fence_matches_the_spec_loader(tmp_path):
    # The sync that matters: check_docs decides where frontmatter ENDS, and
    # agent_common.parse_spec_frontmatter decides where the DATA ends. Let them
    # drift and one starts existence-checking the other's values. Pinned on the
    # constant AND on agreement over a real spec's body.
    check = load_script("check_docs")
    common = load_script("agent_common")
    assert check.SPEC_FENCE == common.SPEC_FENCE
    text = '+++\nid = "WI-1"\ntitle = "[a](b.md)"\n+++\nbody [real](real.md)\n'
    _data, body = common.parse_spec_frontmatter(text, "WI-1-x.md")
    blanked = check.blank_frontmatter(text)
    # Everything the loader calls BODY survives the blanking, byte for byte.
    assert blanked.endswith(body)
    # ...and everything above it is gone, with the line count preserved.
    assert blanked.count("\n") == text.count("\n")
    assert "[a](b.md)" not in blanked


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


def test_ignore_glob_spans_directories(scaffold):
    # The house glob convention (orphans-allow, declared-absences) is fnmatch
    # with `*` SPANNING separators, and --ignore must match it: one
    # `docs/work/*` covers every nested status directory of the spec-folder
    # registry, whose bodies are historical records rather than navigable
    # prose. The mutation half is the nested path: Path.match (the previous
    # implementation) passes the flat case and silently missed this one.
    nested = scaffold / "docs" / "work" / "archive"
    nested.mkdir(parents=True, exist_ok=True)  # the scaffold ships the dirs
    (nested / "WI-001-old.md").write_text(
        '+++\nid = "WI-001"\n+++\n\n## Deliverable\n\n[stale](gone.md)\n',
        encoding="utf-8",
    )
    fails = run_py(["scripts/check_docs.py"], cwd=scaffold)
    assert fails.returncode == 1  # scanned -> the broken link is caught
    passes = run_py(["scripts/check_docs.py", "--ignore", "docs/work/*"], cwd=scaffold)
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
    # End-to-end: a Must need still at DRAFT does NOT force a README citation
    # (it is unratified); the check stays green. Draft-ness is `kind` now, not a
    # heading — the carrier cutover retired section-as-state,
    # which is what stopped a prose mention under a heading from re-drafting an
    # attested need.
    reg = scaffold / "docs" / "requirements" / "stakeholder-needs.toml"
    reg.write_text(
        reg.read_text(encoding="utf-8")
        + '\n[need.SN-050]\nkind = "draft"\nneed = "drafted must"\n'
        'why = "matters"\npriority = "M"\nacceptance = "x"\n',
        encoding="utf-8",
    )
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # ...and the same need at `core` DOES force it — otherwise this test would
    # pass on a check that had simply stopped looking.
    reg.write_text(
        reg.read_text(encoding="utf-8").replace('kind = "draft"', 'kind = "core"'),
        encoding="utf-8",
    )
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "SN-050" in proc.stdout


# --- harness wiring ----------------------------------------------------------


def test_harness_wires_stale_into_doc_navigability():
    # check.py passes --stale to the doc-navigability step (warn-only) so the
    # lying-map heuristic runs inside the harness.
    src = (SCRIPTS / "check.py").read_text(encoding="utf-8")
    i = src.index("check_docs.py")
    # 1000, not 600: the arg list carries the docs/work scoping comment (Phase
    # 2c) and now the docs/handbacks one too (SR-144) between the ignores and
    # --stale. The window is a readability bound on the search, not a claim
    # about the file — widen it when a reason is added, never drop it.
    assert "--stale" in src[i : i + 1000]


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


def test_git_commit_lookup_batches_tracked_paths_and_skips_untracked(tmp_path):
    check = load_script("check_docs")
    import subprocess

    repo = tmp_path
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "config", "user.email", "t@example.com"],
        check=True,
    )
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "T"], check=True)
    tracked = repo / "nested" / "Thing.txt"
    tracked.parent.mkdir()
    tracked.write_text("tracked\n", encoding="utf-8")
    unicode_path = repo / "nested" / "naïve.txt"
    unicode_path.write_text("unicode path\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "nested"], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-q", "-m", "tracked"], check=True
    )
    untracked = repo / "untracked.txt"
    untracked.write_text("not committed\n", encoding="utf-8")

    lookup = check.git_commit_lookup(repo)
    assert lookup is not None
    assert isinstance(lookup(tracked), int)
    assert lookup("nested/Thing.txt") == lookup(tracked)
    assert lookup(unicode_path) == lookup(tracked)
    assert lookup(untracked) is None
    assert lookup(repo.parent / "outside.txt") is None


def test_git_commit_lookup_runs_one_history_process(tmp_path, monkeypatch):
    check = load_script("check_docs")
    calls = []

    class Result:
        returncode = 0
        stdout = "\x1e200\n\none.md\ntwo.py\n\x1e100\n\none.md\n"

    def fake_run(argv, **_kwargs):
        calls.append(argv)
        return Result()

    monkeypatch.setattr(check.shutil, "which", lambda _name: "git")
    monkeypatch.setattr(check.subprocess, "run", fake_run)
    lookup = check.git_commit_lookup(tmp_path)

    assert lookup(tmp_path / "one.md") == 200
    assert lookup(tmp_path / "two.py") == 200
    assert lookup(tmp_path / "missing.txt") is None
    assert len(calls) == 1
    log_index = calls[0].index("log")
    assert calls[0][1:3] == ["-c", "core.quotePath=false"]
    assert calls[0][log_index:] == [
        "log",
        "--format=%x1e%ct",
        "--name-only",
        "--no-renames",
    ]


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


def _write_open_items(scaffold, rows):
    """The open-items REGISTRY (WI-322) — S-3's brief source since the markdown
    surface retired."""
    path = scaffold / "docs" / "requirements" / "open-items.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "OI-ID,Title,Status,Raised,OneLine,Decision,BlastRadius,Options,"
        "Recommendation,WI-Refs,RuledDate,RulingRef\n" + rows,
        encoding="utf-8",
    )


def test_oi_coherence_both_directions(scaffold):
    # S-3: a Needs-<human> OI with no brief warns; a briefed OI never named in
    # status.md warns; an In-flight OI needs NO brief; all warn-only (exit 0).
    _write_status(scaffold, _STATUS_SHAPED)
    _write_open_items(
        scaffold,
        "OI-1,decide the flag,pending,,,...,,,,,,\n"
        "OI-8,stale ruled item,pending,,,...,,,,,,\n",
    )
    proc = run_py(["scripts/check_docs.py"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "OI-9: a Needs-<human> item" in proc.stdout  # missing brief
    assert "OI-8: briefed in requirements/open-items.csv" in proc.stdout  # orphan
    assert "OI-1" not in proc.stdout  # coherent id is quiet
    assert "OI-2" not in proc.stdout  # in-flight needs no brief


def test_oi_coherence_vacuous_without_open_items(scaffold):
    # S-3 is opt-in: without the registry it is silent (the other status rules
    # stay live). WI-322: a RULED row is likewise not a brief — it is history —
    # so a queue of only ruled rows is the same vacuum.
    _write_status(scaffold, _STATUS_SHAPED)
    oi = scaffold / "docs" / "requirements" / "open-items.csv"
    if oi.exists():
        oi.unlink()
    proc = run_py(["scripts/check_docs.py"], cwd=scaffold)
    assert proc.returncode == 0
    assert "OI-9" not in proc.stdout


def test_oi_coherence_retires_under_generated_marker(scaffold):
    # WI-202: once status.md carries a `<!-- BEGIN GENERATED STATUS -->` block,
    # its open-items list is PROJECTED from the open-items registry by
    # gen_trajectory --status, so the S-3 coherence check stands down (the
    # status-map freshness gate is the invariant). The SAME incoherence that
    # fires without the marker (a missing brief AND an orphan brief) is silent.
    marked = "# Status\n\n<!-- BEGIN GENERATED STATUS -->\n" + _STATUS_SHAPED.split(
        "\n", 1
    )[1].replace("## Scope", "<!-- END GENERATED STATUS -->\n\n## Scope")
    _write_status(scaffold, marked)
    _write_open_items(
        scaffold,
        "OI-1,decide the flag,pending,,,...,,,,,,\n"
        "OI-8,stale ruled item,pending,,,...,,,,,,\n",
    )
    proc = run_py(["scripts/check_docs.py"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # both S-3 directions stand down under the marker
    assert "Needs-<human> item" not in proc.stdout
    assert "orphan brief" not in proc.stdout
    # S-1/S-2 still guard the hand-authored region: an order violation still warns
    _write_status(
        scaffold,
        "# Status\n\n## Scope\n\n- Goal\n\n"
        "<!-- BEGIN GENERATED STATUS -->\n- **Open items:** none\n"
        "<!-- END GENERATED STATUS -->\n",
    )
    proc = run_py(["scripts/check_docs.py"], cwd=scaffold)
    assert "Open items after ## Scope" in proc.stdout


# --- expected-live-orphan taxonomy + the no-new-orphan ratchet (WI-228) --------
# repo-review-2026-07-18 M-07: docs/orphans-allow declares expected live-orphan
# CLASSES (retained evidence). A classified orphan stops warning individually and
# never fails; only a *newly introduced* orphan outside every class still trips
# the warning / --strict-orphans failure — the ratchet, baselining history.


def _write_orphans_allow(scaffold, text):
    (scaffold / "docs" / "orphans-allow").write_text(text, encoding="utf-8")


def test_declared_class_suppresses_expected_orphan(scaffold):
    # A doc matching a docs/orphans-allow glob is an EXPECTED live-orphan: it is
    # dropped from the per-doc warnings (an aggregate `note` replaces them) and is
    # never named individually — the noise reduction M-07 asks for.
    (scaffold / "docs" / "reviews").mkdir(parents=True, exist_ok=True)
    (scaffold / "docs" / "reviews" / "003-REVIEW-A.md").write_text(
        "# Review\n\nRetained round evidence.\n", encoding="utf-8"
    )
    _write_orphans_allow(scaffold, "# reviews\ndocs/reviews/*\n")
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # classified: never named in an individual orphan line (default or strict)...
    assert "docs/reviews/003-REVIEW-A.md" not in proc.stdout
    # ... and folded into the aggregate note instead.
    assert "expected live-orphan(s) matched docs/orphans-allow" in proc.stdout


def test_orphan_outside_declared_classes_is_the_ratchet(scaffold):
    # THE RATCHET: an orphan matching no declared class is GENUINE — it warns by
    # default and fails under --strict-orphans exactly as before. A class for
    # OTHER paths does not grandfather a newly introduced undiscoverable doc.
    _write_orphans_allow(scaffold, "docs/reviews/*\n")
    (scaffold / "docs" / "new-note.md").write_text(
        "# New\n\nNobody links here.\n", encoding="utf-8"
    )
    warn = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert warn.returncode == 0, warn.stdout + warn.stderr
    assert (
        "WARN - orphan doc (no path from an entry root): docs/new-note.md"
        in warn.stdout
    )
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
    assert (
        "FAIL - orphan doc (no path from an entry root): docs/new-note.md"
        in strict.stdout
    )


def test_expected_orphan_never_fails_even_under_strict(tmp_path):
    # "Baseline the residue, never fail history": an EXPECTED live-orphan is
    # exempt from failure even under --strict-orphans (a genuine orphan is not).
    # A bare docs tree (no root README) keeps the vision/inventory checks quiet,
    # so the ONLY orphan here is the classified review — strict stays green.
    docs = tmp_path / "docs"
    (docs / "reviews").mkdir(parents=True)
    (docs / "reviews" / "003-REVIEW-A.md").write_text("# R\n", encoding="utf-8")
    (docs / "orphans-allow").write_text("docs/reviews/*\n", encoding="utf-8")
    proc = run_py(
        [SCRIPTS / "check_docs.py", "--root", tmp_path, "--strict-orphans"],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "orphan doc" not in proc.stdout  # neither WARN nor FAIL for it
    assert "expected live-orphan(s) matched docs/orphans-allow" in proc.stdout


def test_absent_orphans_allow_is_todays_behavior(scaffold):
    # Downstream unchanged: with no docs/orphans-allow there is no class
    # suppression — a lonely doc warns individually and the `note` never appears
    # (the kit must not surprise an existing repo).
    #
    # The absence is CONSTRUCTED, not inherited: since Phase 2c-i a fresh
    # scaffold SHIPS a docs/orphans-allow (declaring docs/work/* — a work spec
    # is a registry entry, not a page anyone navigates to). A test that read the
    # fixture's absence would have silently stopped testing absence at all the
    # moment the scaffold gained the file, which is exactly what it did.
    (scaffold / "docs" / "orphans-allow").unlink()
    (scaffold / "docs" / "lonely.md").write_text("# Lonely\n", encoding="utf-8")
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (
        "WARN - orphan doc (no path from an entry root): docs/lonely.md" in proc.stdout
    )
    assert "expected live-orphan" not in proc.stdout


def test_declared_class_still_link_checks_the_doc(scaffold):
    # Non-goal untouched (no change to broken-link semantics): classifying a doc
    # as an expected orphan silences only the orphan noise — a broken link inside
    # it still fails the run.
    (scaffold / "docs" / "reviews").mkdir(parents=True, exist_ok=True)
    (scaffold / "docs" / "reviews" / "003-REVIEW-A.md").write_text(
        "# R\n\nSee [gone](nowhere-review.md).\n", encoding="utf-8"
    )
    _write_orphans_allow(scaffold, "docs/reviews/*\n")
    proc = run_py(
        ["scripts/check_docs.py", "--ignore", "docs/test/report.md"], cwd=scaffold
    )
    assert proc.returncode == 1
    assert "broken link -> nowhere-review.md" in proc.stdout


def test_load_orphan_classes_reads_declared_file(tmp_path):
    # The declared-file idiom (like docs/status-lint): `#` comments and blanks
    # dropped, one glob per remaining line; absent file => [] (unchanged default).
    check = load_script("check_docs")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "orphans-allow").write_text(
        "# a comment\n\ndocs/reviews/*\n  docs/specs/WI-*.md  \n", encoding="utf-8"
    )
    assert check.load_orphan_classes(tmp_path, "docs") == [
        "docs/reviews/*",
        "docs/specs/WI-*.md",
    ]
    assert check.load_orphan_classes(tmp_path / "nope", "docs") == []


def test_partition_orphans_splits_on_declared_globs():
    # `*` spans separators (fnmatch), so docs/reviews/* covers the subtree; an
    # unmatched path stays genuine; no patterns => everything genuine (unchanged).
    check = load_script("check_docs")
    orphans = [
        "docs/reviews/003-REVIEW-A.md",
        "docs/specs/WI-175.md",
        "docs/new-note.md",
    ]
    genuine, expected = check.partition_orphans(
        orphans, ["docs/reviews/*", "docs/specs/WI-*.md"]
    )
    assert genuine == ["docs/new-note.md"]
    assert expected == ["docs/reviews/003-REVIEW-A.md", "docs/specs/WI-175.md"]
    assert check.partition_orphans(orphans, []) == (orphans, [])


# --- the meta-repo dogfood: zero unexplained residue (REVIEW-A rework) ---------
# REVIEW-A flagged that a hardcoded "48" census in the WI-228 spec is untraceable
# — the count is a moving target by construction (48 when drafted, 63 at
# integration). The requirement's real acceptance criterion is COUNT-INDEPENDENT:
# every live orphan on the meta tree is classified, zero unexplained residue.
# This mechanizes exactly that, dogfooding the ratchet on the kit's own tree — it
# goes red the moment an unclassified orphan lands, whatever the census count is.


def test_meta_repo_has_zero_unexplained_orphans():
    # Run check_docs against the REAL meta root under --strict-orphans (matching
    # the harness's --ignore for the generated, gitignored trace composite). Exit
    # 0 means every live orphan is covered by a declared docs/orphans-allow class:
    # the count-independent Done-when. No census NUMBER is asserted (that would
    # re-introduce the fragile baseline the review objected to) — only the
    # invariant that the residue is empty and the aggregate note is doing its job.
    proc = run_py(
        [
            SCRIPTS / "check_docs.py",
            "--root",
            ROOT,
            "--ignore",
            "docs/test/report.md",
            # The registry is data, not prose — same scope the harness declares
            # in check.py's doc-navigability step (Phase 2c flip).
            "--ignore",
            "docs/work/*",
            "--strict-orphans",
        ],
        cwd=ROOT,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # No genuine orphan is ever named as a finding (WARN or FAIL) on the meta tree.
    assert "orphan doc (no path from an entry root)" not in proc.stdout
    # ... and the census is non-empty: the classified evidence is folded into the
    # aggregate note, proving suppression is actually happening (not vacuously 0).
    assert "expected live-orphan(s) matched docs/orphans-allow" in proc.stdout
