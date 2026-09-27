"""gen_open_items.py's in-process seams: the renderers, the theme guards and
the deferral declarations.

Split out of `test_gen_open_items.py`, verbatim. That module drives the
generator as a subprocess over git-committed fixtures and is registered in
`tests/conftest.py`'s `SLOW_MODULES`; every case here calls the generator's own
functions, over strings or a `tmp_path` tree with no git and no subprocess, so
the open-items view keeps a test in the per-commit smoke tier.
"""

import re

from conftest import load_script
from test_gen_open_items import PENDING_OI, RULED_OI, _log_d, repo


def test_word_diff_marks_only_what_moved(tmp_path):
    gi = load_script("gen_open_items")
    out = gi.word_diff("the quick brown fox", "the quick red fox")
    assert "<del>brown</del>" in out and "<ins>red</ins>" in out
    assert out.count("<del>") == 1 and out.count("<ins>") == 1
    # unchanged runs are wrapped so the view can collapse them
    assert 'class="eq"' in out
    assert gi.changed_percent("a b c d", "a b c d") == 0
    assert gi.changed_percent("a b c d", "w x y z") == 100


def test_open_items_theme_tokens_match_the_dashboard():
    """A drift guard, not an extraction (the WI-291 precedent, and the F5 ruling
    against a shared `_kitcommon`): the two owner surfaces must read as one
    system, so every shared theme token must carry the same value the dashboard
    emits.

    REWORKED after 122-REVIEW-A refuted the first version twice over: its
    `assert value in CSS` sat OUTSIDE the token loop (so it checked one token per
    theme), and it compared against a module-level `THEME` dict that nothing
    rendered from — nine of the twelve EMITTED tokens were rewritten, including
    dark `--text:#444444`, and it stayed green. Both halves are now closed: the
    values are parsed out of the CSS the page actually ships
    (`gen_open_items.theme_tokens`), and every token is asserted."""
    gi = load_script("gen_open_items")
    gt = load_script("gen_trajectory")
    template = gt.HTML_TEMPLATE.template
    blocks = {
        "light": re.search(r":root \{([^}]*)\}", template, re.S).group(1),
        "dark": re.search(
            r"@media \(prefers-color-scheme: dark\) \{\s*:root \{(.*?)\}",
            template,
            re.S,
        ).group(1),
    }
    ours = gi.theme_tokens()
    assert set(ours) == {"light", "dark"}
    checked = 0
    for theme, block in blocks.items():
        dashboard = dict(re.findall(r"(--[\w-]+):\s*(#[0-9a-fA-F]{3,8})", block))
        assert ours[theme], theme  # never vacuous: the parse must find tokens
        for token, value in ours[theme].items():
            assert token in dashboard, (theme, token, "dashboard dropped it")
            assert dashboard[token].lower() == value.lower(), (
                theme,
                token,
                dashboard[token],
                value,
            )
            checked += 1
    assert checked == 2 * len(gi.THEME_TOKENS), checked


def test_theme_drift_guard_reads_the_shipped_css_not_a_mirror():
    """The negative half of the guard above, and the reason it exists: a value
    that appears only in a constant proves nothing about the page. `theme_tokens`
    must read whatever CSS it is handed, so drifting the CSS drifts the guard's
    input rather than leaving it agreeing with a stale mirror."""
    gi = load_script("gen_open_items")
    drifted = gi.CSS.replace("--text:#0f172a", "--text:#444444", 1)
    assert gi.theme_tokens(drifted)["light"]["--text"] == "#444444"
    assert gi.theme_tokens()["light"]["--text"] == "#0f172a"


def test_a3_diff_marks_keep_a_shape_cue_not_colour_alone(tmp_path):
    """The word-diff's `<ins>`/`<del>` are the CSS-level half: the shape cue is
    baked into the rule itself, not into any registry content, so it can be
    pinned directly against the CSS the page ships (the same source
    `theme_tokens` reads — never a mirror that could drift out from under it).
    `<del>` keeps its line-through (a mark visible without colour perception);
    `<ins>` trades the default underline for a box-shadow rule rather than
    leaving colour as the only thing that tells the two apart."""
    gi = load_script("gen_open_items")
    ins_rule = re.search(r"\.diff ins\{([^}]*)\}", gi.CSS, re.S).group(1)
    del_rule = re.search(r"\.diff del\{([^}]*)\}", gi.CSS, re.S).group(1)
    assert "text-decoration:line-through" in del_rule.replace("\n", "").replace(
        "  ", ""
    )
    ins_flat = ins_rule.replace("\n", "").replace("  ", "")
    assert "text-decoration:none" in ins_flat  # the underline is deliberately OFF...
    assert "box-shadow" in ins_flat  # ...replaced by a shape cue, not dropped


def test_unsafe_link_target_is_not_clickable():
    """122-REVIEW-A: `md_inline` emitted a raw href with no scheme allow-list, so
    an agent-authored cell could ship a `javascript:` URL onto the one document a
    human reads. The text still shows — degraded, not dropped."""
    gi = load_script("gen_open_items")
    out = gi.md_inline("[click](javascript:alert(1)) and [ok](docs/x.md)")
    assert 'href="javascript:' not in out
    assert "click (javascript:alert(1))" in out
    assert '<a href="docs/x.md">ok</a>' in out
    # ...and the ordinary shapes still link.
    for target in ("#frag", "../x.md", "https://example.test/x"):
        assert 'href="{}"'.format(target) in gi.md_inline("[t]({})".format(target))


def test_brief_cells_render_BLOCK_structure_not_one_wall():
    """The owner, 2026-08-12: the briefs arrived as "huge blocks of single
    bloated paragraphs". They were not written that way — `md_inline` renders a
    cell as ONE run of text, so paragraphs, bullets and sub-headings were
    flattened on the way to the screen. A RENDERING defect, so the fix belongs
    here rather than in shorter cells (which would have traded away the
    reasoning a ruler needs)."""
    gi = load_script("gen_open_items")
    out = gi.md_block(
        "Opening line\nwrapped by the author.\n\n"
        "### PART A\n"
        "- first, with `code`\n"
        "- second, with **bold**\n\n"
        "Closing."
    )
    assert out.count("<p>") == 2, out
    assert "<h4>PART A</h4>" in out
    assert out.count("<li>") == 2 and "<ul>" in out
    # A hard-wrapped paragraph joins into ONE <p>, never one per source line.
    assert "<p>Opening line wrapped by the author.</p>" in out
    # Inline forms still work INSIDE blocks.
    assert "<code>code</code>" in out and "<strong>bold</strong>" in out


def test_block_renderer_still_escapes_and_still_refuses_unsafe_links():
    """The block path must not become an escape hatch around the two guarantees
    the inline path already makes — 122-REVIEW-A's `javascript:` refusal is on
    the one document a human reads, and it has to hold per-line too."""
    gi = load_script("gen_open_items")
    out = gi.md_block("- <script>alert(1)</script>\n- [click](javascript:alert(1))")
    assert "<script>" not in out and "&lt;script&gt;" in out
    assert 'href="javascript:' not in out
    assert "click (javascript:alert(1))" in out


def test_unknown_block_syntax_degrades_to_visible_text():
    """The renderer knows three block forms. Everything else must still SHOW —
    the same failure direction `_safe_link` chose, because a brief silently
    losing a sentence is worse on a decision surface than one rendering it
    plainly."""
    gi = load_script("gen_open_items")
    out = gi.md_block("| a | b |\n\n> quoted\n\n1. numbered")
    for literal in ("| a | b |", "&gt; quoted", "1. numbered"):
        assert literal in out, (literal, out)


def test_whitespace_only_edit_does_not_fuse_neighbours():
    """122-REVIEW-A: `word_diff` dropped whitespace-only opcodes, so "a  b" ->
    "a b" rendered as "ab" — the reconstructed after-text must be the cell the
    owner is actually blessing."""
    gi = load_script("gen_open_items")
    out = gi.word_diff("a  b", "a b")
    assert re.sub(r"<[^>]+>", "", out) == "a b", out


def test_normalize_survives_the_carrier_change_and_this_is_why(tmp_path):
    """`gen_open_items.normalize` exists because a Windows-authored multi-line
    CSV cell carried a CRLF. TOML retires HALF of that hazard and NOT the other
    half, so the function stays — recorded executably rather than argued.

    RETIRED: a literal CRLF inside a multi-line TOML string is normalised to LF
    by the PARSER (TOML 1.0), so a registry cell can no longer pick one up from
    the editor that wrote it.

    NOT RETIRED, and this is the load-bearing half: the guard also covers the
    *checkout's own* line endings. A clone with `core.autocrlf` on stores the
    generated HTML with CRLF, and a byte-exact freshness compare would then red
    every fresh worktree — which is not a registry fact at all and is untouched
    by which carrier the registry uses. Removing `normalize` would re-break the
    WI-322 rework's detached view worktree.
    """
    gen_oi = load_script("gen_open_items")
    import tomllib

    # (a) the parser really does fold a literal CRLF — the retired half.
    parsed = tomllib.loads('[open_item.OI-1]\r\ndecision = """one\r\ntwo"""\r\n')
    assert parsed["open_item"]["OI-1"]["decision"] == "one\ntwo"

    # (b) ...but a `\r` ESCAPE is still legal TOML, so a cell CAN still hold a
    #     CR — deliberately authored rather than picked up, and still stripped
    #     at `esc`, the one choke point every registry value passes through.
    escaped = tomllib.loads('[open_item.OI-1]\ndecision = "a\\rb"\n')
    assert escaped["open_item"]["OI-1"]["decision"] == "a\rb"
    assert "\r" not in gen_oi.esc("a\rb")

    # (c) the half that keeps the function: a CRLF checkout of the ARTIFACT.
    assert gen_oi.normalize("<p>x</p>\r\n") == gen_oi.normalize("<p>x</p>\n")


def test_a_fragment_declares_the_open_items_it_deferred(tmp_path):
    # ARM 2's grammar is a KEY (`deferred:`) in a declaration position, never a
    # vocabulary of defer-PHRASES — a matcher's precision is a property of the
    # wording it meets, so its error rate cannot be bounded before it ships.
    gi = load_script("gen_open_items")
    root = repo(tmp_path, oi_rows=PENDING_OI)
    _log_d(root, "WI-1-ids.md", "## a session\n\nDeferred open items: OI-4, OI-9\n")
    # The none form — the explicit way to say a zero-pending queue is deliberate,
    # and the shape the live 2026-08-20 fragment already wrote in prose.
    _log_d(
        root,
        "WI-2-none.md",
        "## another\n\nthis fragment backs the claim by declaring what was "
        "deferred: **nothing new was deferred by this session**, all briefs "
        "closed.\n",
    )
    # Fail-soft: a marker carrying neither an id nor a none-word declares
    # NOTHING, so the arm cannot invent a deferral out of ordinary prose.
    _log_d(root, "WI-3-quiet.md", "## third\n\nWI-9 was deferred: it waits on X.\n")
    decls = gi.fragment_declarations(root)
    assert [(d["ids"], d["none"]) for d in decls] == [
        (["OI-4", "OI-9"], False),
        ([], True),
    ]
    assert decls[0]["file"] == "docs/log.d/WI-1-ids.md" and decls[0]["line"] == 3


def test_a_declared_deferral_must_name_a_row_the_owner_has_still_to_rule(tmp_path):
    gi = load_script("gen_open_items")
    root = repo(tmp_path, oi_rows=PENDING_OI + RULED_OI)
    _log_d(root, "WI-1-x.md", "## s\n\nDeferred open items: OI-4, OI-5, OI-77\n")
    states = load_script("trace").open_item_states(root)
    findings = gi.deferral_findings(root, states)
    assert len(findings) == 2, findings
    assert "OI-5" in findings[0] and "reads `ruled`" in findings[0]
    assert "OI-77" in findings[1] and "has no row" in findings[1]
    # OI-4 is pending: a resolving declaration is quiet.
    assert "OI-4" not in " ".join(findings)


def test_a_session_that_defers_silently_passes_clean(tmp_path):
    # THE DECLARED WEAKNESS, ON THE RECORD (the ruling's own words): a
    # declaration cannot catch a session that says nothing. Asserted here so the
    # gap is a documented property rather than a discovery.
    gi = load_script("gen_open_items")
    root = repo(tmp_path, oi_rows=PENDING_OI)
    _log_d(root, "WI-1-silent.md", "## s\n\nA session that mentions OI-4 in passing.\n")
    assert gi.fragment_declarations(root) == []
    assert gi.deferral_findings(root, load_script("trace").open_item_states(root)) == []


def test_a_none_declaration_is_contradicted_by_a_pending_citation(tmp_path):
    # The honest-`none`-over-a-held-lane case OI-70 named: the fragment declares
    # it deferred nothing while its own text still cites a still-pending OI.
    gi = load_script("gen_open_items")
    tr = load_script("trace")
    root = repo(tmp_path, oi_rows=PENDING_OI + RULED_OI)
    _log_d(
        root,
        "WI-1-held.md",
        "## a session\n\nWe kept working around OI-4 all day.\n\n"
        "Deferred open items: none — nothing new here.\n",
    )
    findings = gi.deferral_findings(root, tr.open_item_states(root))
    assert any("OI-4" in f and "declares `none`" in f for f in findings), findings


def test_a_none_declaration_citing_only_a_ruled_or_absent_oi_passes_clean(tmp_path):
    # Fail-soft: a ruled (OI-5) or absent (OI-99) id a `none` fragment mentions is
    # history, not a held decision, so it never contradicts.
    gi = load_script("gen_open_items")
    tr = load_script("trace")
    root = repo(tmp_path, oi_rows=PENDING_OI + RULED_OI)
    _log_d(
        root,
        "WI-2-hist.md",
        "## s\n\nOI-5 was ruled last week and OI-99 never existed; we built on "
        "them.\n\nDeferred open items: none — every question was answered.\n",
    )
    findings = gi.deferral_findings(root, tr.open_item_states(root))
    assert not any("declares `none`" in f for f in findings), findings


def test_a_section_scoped_none_is_judged_only_against_its_own_section(tmp_path):
    # POSITION IS SCOPE (ARM 2's rule, applied to the truth check): a `none`
    # inside one `### ` section is contradicted by a pending cite in THAT section
    # (WI-1), never by one discussed in a different section (WI-2).
    gi = load_script("gen_open_items")
    tr = load_script("trace")
    root = repo(tmp_path, oi_rows=PENDING_OI)
    _log_d(
        root,
        "WI-3-clean.md",
        "## day\n\n### WI-1 — clean\n\nnothing owed here.\n\n"
        "Deferred open items: none — this WI raised nothing.\n\n"
        "### WI-2 — other\n\nwe are still chewing on OI-4.\n",
    )
    # ARM 4 stays silent — OI-4 is cited in WI-2's span, not WI-1's. (The
    # existing scope arm may still note WI-2 carries no declaration; that is a
    # different finding, so this check is ARM-4-specific.)
    assert not any(
        "declares `none`" in f
        for f in gi.deferral_findings(root, tr.open_item_states(root))
    )

    root2 = repo(tmp_path / "two", oi_rows=PENDING_OI)
    _log_d(
        root2,
        "WI-4-held.md",
        "## day\n\n### WI-1 — held\n\nstill waiting on OI-4.\n\n"
        "Deferred open items: none — nothing new.\n\n"
        "### WI-2 — shipped\n\ndone.\n",
    )
    findings = gi.deferral_findings(root2, tr.open_item_states(root2))
    assert any("OI-4" in f and "`WI-1 — held` section" in f for f in findings), findings


def test_the_vacuity_arm_names_the_contradicting_entry(tmp_path):
    # ARM 3 RE-AIMED: not "0 pending is a finding" — the unactionable form the
    # ruling refused — but a COUNT contradicted by a surface that still defers,
    # with the entry NAMED so a reader can discharge it.
    gi = load_script("gen_open_items")
    tr = load_script("trace")
    root = repo(tmp_path, oi_rows=RULED_OI)
    (root / "docs" / "provenance-allow").write_text(
        "SR-001 Rationale added 2026-08-16 — OI-5: ruled, execution owed.\n",
        encoding="utf-8",
    )
    findings = gi.deferral_findings(root, tr.open_item_states(root))
    assert len(findings) == 1 and findings[0].startswith("VACUITY")
    assert "SR-001 Rationale" in findings[0] and "OI-5" in findings[0]
    # ...and it is a COUNT, so one genuinely pending row settles the question.
    repo(tmp_path, oi_rows=RULED_OI + PENDING_OI)
    assert gi.deferral_findings(root, tr.open_item_states(root)) == []


def test_a_SECTION_scoped_declaration_does_not_speak_for_the_whole_fragment(tmp_path):
    """ARM 2's SCOPE rule (2026-08-20, the batch review's MAJOR-7). The day's own
    grind fragment carried twenty per-WI sections and ONE declaration —
    `Deferred open items: none`, true of the section it stood in — while two
    decisions announced in other sections had no rows at all. That is OI-41's
    founding class reproduced inside the artifact built to catch it."""
    gi = load_script("gen_open_items")
    tr = load_script("trace")
    root = repo(tmp_path, oi_rows=PENDING_OI)
    _log_d(
        root,
        "WI-1-grind.md",
        "## a day's grind\n\n"
        "### WI-1 — first\n\nDeferred open items: none — nothing here.\n\n"
        "### WI-2 — second\n\nthe owner ruled something and no row was made.\n",
    )
    decls = gi.fragment_declarations(root)
    assert decls[0]["scope"] == "WI-1 — first", decls
    findings = gi.deferral_findings(root, tr.open_item_states(root))
    assert len(findings) == 1 and "1 of 2 sections" in findings[0], findings
    # The fix is one line of TOP MATTER: a declaration above the first `### `
    # speaks for the whole fragment, because that is where the file's own record
    # is written.
    _log_d(
        root,
        "WI-1-grind.md",
        "## a day's grind\n\nDeferred open items: OI-4\n\n"
        "### WI-1 — first\n\nDeferred open items: none — nothing here.\n\n"
        "### WI-2 — second\n\nthe owner ruled something and no row was made.\n",
    )
    assert any(d["scope"] is None for d in gi.fragment_declarations(root))
    assert gi.deferral_findings(root, tr.open_item_states(root)) == []


def test_a_single_section_fragment_is_never_scope_warned(tmp_path):
    # Narrow by construction: the rule needs at least two sections to have a
    # generalisation to make, and a fragment that declares NOTHING is the arm's
    # ruled weakness rather than this rule's business.
    gi = load_script("gen_open_items")
    tr = load_script("trace")
    root = repo(tmp_path, oi_rows=PENDING_OI)
    _log_d(root, "WI-1-one.md", "## s\n\n### only\n\nDeferred open items: OI-4\n")
    _log_d(root, "WI-2-quiet.md", "## s\n\n### a\n\nx\n\n### b\n\ny\n")
    assert gi.deferral_findings(root, tr.open_item_states(root)) == []


def test_an_ABSENT_registry_with_live_entries_is_a_finding_not_a_silence(tmp_path):
    """MAJOR-6's third arm. `states is None` really is a vacuum — there is no
    count to contradict — but a repo whose exception surface defers into a queue
    that does not exist is the founding class at its strongest, and it was the
    one state that produced nothing at all."""
    gi = load_script("gen_open_items")
    root = repo(tmp_path, oi_rows=None)
    (root / "docs" / "provenance-allow").write_text(
        "SR-001 Rationale added 2026-08-16 — OI-5: ruled, execution owed.\n",
        encoding="utf-8",
    )
    assert load_script("trace").open_item_states(root) is None
    findings = gi.deferral_findings(root, None)
    assert len(findings) == 1 and "has no docs/requirements/open-items" in findings[0]
    # ...and with no entries either, the vacuum is still a vacuum.
    (root / "docs" / "provenance-allow").write_text("", encoding="utf-8")
    assert gi.deferral_findings(root, None) == []
