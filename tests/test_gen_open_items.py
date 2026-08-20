"""gen_open_items.py — the generated owner decision surface (WI-322, OI-10 (b)).

`docs/open-items.md` is retired: decision briefs are ROWS in
`docs/requirements/open-items.csv`, and this generator renders them — plus every
spine row owing a ratification (`Drafted`) or a re-attest (`Modified`), with a
word-level before/after — into `docs/open-items.html`.

What these guard, in the order the surface can fail a reader:

  * the briefs render, and a RULED row does not (it is history, not a decision);
  * `Drafted` AND `Modified` both surface — "new or changed requirement rows
    awaiting a human" is the whole point, and an earlier draft covered only one;
  * an empty section says CHECK THE BASELINE rather than reading as a confident
    "nothing changed" (the failure that shipped a brief missing 2 of 6 rows);
  * the freshness gate bites on drift, MASKS the machine-local region, and
    reproduces the baseline the file was rendered against;
  * the whole thing is vacuous for a repo that never adopts the surface.

Each guard carries its negative half, per the house rule.
"""

import re
import subprocess

from conftest import SCRIPTS, load_script, run_py

SR_HEADER = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Notes,"
    "SafetyClass,Verification,Status,Phase,Workstream\n"
)
LLR_HEADER = (
    "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status,Component,Phase\n"
)
TC_HEADER = (
    "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,"
    "Status,Phase\n"
)
OI_HEADER = (
    "OI-ID,Title,Status,Raised,OneLine,Decision,BlastRadius,Options,"
    "Recommendation,WI-Refs,RuledDate,RulingRef\n"
)


def repo(tmp_path, sr_rows="", oi_rows="", llr_rows="", tc_rows=""):
    """A minimal repo carrying only what the surface reads."""
    docs = tmp_path / "docs"
    (docs / "requirements").mkdir(parents=True, exist_ok=True)
    (docs / "test").mkdir(parents=True, exist_ok=True)
    (docs / "requirements" / "system-requirements.csv").write_text(
        SR_HEADER + sr_rows, encoding="utf-8"
    )
    (docs / "requirements" / "low-level-requirements.csv").write_text(
        LLR_HEADER + llr_rows, encoding="utf-8"
    )
    (docs / "test" / "test-cases.csv").write_text(TC_HEADER + tc_rows, encoding="utf-8")
    (docs / "requirements" / "stakeholder-needs.md").write_text(
        "# SN\n", encoding="utf-8"
    )
    if oi_rows is not None:
        (docs / "requirements" / "open-items.csv").write_text(
            OI_HEADER + oi_rows, encoding="utf-8"
        )
    return tmp_path


def gen(root, *args):
    return run_py([SCRIPTS / "gen_open_items.py", "--root", str(root), *args], cwd=root)


def html_of(root):
    with (root / "docs" / "open-items.html").open(encoding="utf-8", newline="") as fh:
        return fh.read()


def write_view(root, text):
    """Write the view VERBATIM. The generator reads and writes without
    newline translation (a registry cell can hold a CRLF), so a tamper fixture
    that used `write_text` would manufacture drift of its own."""
    with (root / "docs" / "open-items.html").open(
        "w", encoding="utf-8", newline=""
    ) as fh:
        fh.write(text)


def _git_init(root):
    """A committed git repo. History no longer supplies the baseline (D-9 step
    4) but the snapshot's stamp reads git, so the paths still want a checkout."""
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    _git_commit(root, "seed")


def _approve(root):
    """The approval act, in a fixture: copy the spine into
    `docs/archive/last_approved/`. Everything the diff renders is measured
    against what this call captured, so a fixture that amends WITHOUT calling it
    first has no baseline and renders current state — which is a different test."""
    load_script("baseline_snapshot").copy_live(root, seed=True)


def _git_commit(root, message):
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "-c",
            "user.email=t@t",
            "-c",
            "user.name=t",
            "commit",
            "-qm",
            message,
        ],
        check=True,
    )


PENDING_OI = (
    "OI-4,Pick a licence,pending,2026-01-02,rule the licence - rec: Apache-2.0,"
    '"Which OSS licence the kit ships under.","Every downstream copy.",'
    '"Apache-2.0 · MIT","Apache-2.0, for the patent grant.",WI-097,,\n'
)
RULED_OI = (
    "OI-5,An already-ruled question,ruled,2026-01-01,it was ruled,"
    '"Decided long ago.","None now.","(a) · (b)","(a).",WI-001,2026-01-05,'
    "docs/log.md\n"
)


def test_pending_briefs_render_and_ruled_rows_do_not(tmp_path):
    repo(tmp_path, oi_rows=PENDING_OI + RULED_OI)
    proc = gen(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    page = html_of(tmp_path)
    assert 'id="OI-4"' in page and "Pick a licence" in page
    assert "Apache-2.0, for the patent grant." in page  # the recommendation renders
    # ...and the negative half: a ruled row is history, not a pending decision.
    assert 'id="OI-5"' not in page
    assert "An already-ruled question" not in page


def test_draft_and_DRIFTED_rows_both_surface(tmp_path):
    """ "New or changed" is the requirement: a Drafted row owes a first
    ratification, an amended row owes a re-attest, and a view that renders only
    one of them silently drops half the owner's queue.

    THE SECOND ROW IS NOW REACHED BY DRIFT, NOT BY A CELL. It used to read
    `Status = Modified`; D-9 step 7 retired that marker, so an amended row
    still reads `Approved` and the ONLY thing that can put it in this queue is
    the comparison against `docs/archive/last_approved/`. The fixture therefore
    has to approve first and amend after — which is the real sequence, and the
    reason this test is worth more than it was: it now proves the surface can
    see an amendment nothing in the registry announces.
    """
    drafted = (
        "SR-001,A drafted need,SN-001,shall do the new thing,because,"
        "criteria,,C,Test,Drafted,1,W\n"
    )
    approved = (
        "SR-002,An amended need,SN-001,shall do the ORIGINAL thing,because,"
        "criteria,,C,Test,Approved,1,W\n"
    )
    root = repo(tmp_path, sr_rows=drafted + approved)
    _git_init(root)
    _approve(root)
    (root / "docs" / "requirements" / "system-requirements.csv").write_text(
        SR_HEADER + drafted + approved.replace("ORIGINAL", "CHANGED"),
        encoding="utf-8",
    )
    assert gen(root).returncode == 0
    page = html_of(root)
    assert 'id="SR-001-attest"' in page and "approval owed" in page
    assert 'id="SR-002-attest"' in page and "re-attest owed" in page
    # ...and the drifted cell is what the owner is shown, before and after.
    assert "ORIGINAL" in page and "CHANGED" in page


def test_verified_rows_are_not_in_the_queue(tmp_path):
    # The negative half of the two guards above: a settled row owes nothing and
    # must not appear, or the surface cries wolf on every spine row.
    repo(
        tmp_path,
        sr_rows="SR-003,A settled need,SN-001,shall,because,criteria,,C,Test,Approved,1,W\n",
    )
    assert gen(tmp_path).returncode == 0
    page = html_of(tmp_path)
    assert "SR-003" not in page
    assert "no SR owes an approval or a re-attest" in page


def test_an_empty_section_says_what_it_means_instead_of_check_the_baseline(tmp_path):
    """THE SUCCESSOR to `test_empty_diff_section_says_check_the_baseline`
    (D-9 step 4). That test guarded a real hazard: an auto-derived baseline could
    sit AFTER the amendment, so an empty section meant "the baseline is wrong",
    and reading it as "nothing changed" is how two of six rows got blessed
    unseen. A snapshot cannot sit after the amendment it precedes, so the hazard
    is structurally gone and the advice would now be false. The section says
    what is actually true instead."""
    verified = (
        "SR-004,No visible delta,SN-001,shall,because,criteria,,C,Test,Approved,1,W\n"
    )
    root = repo(tmp_path, sr_rows=verified)
    _git_init(root)
    _approve(root)
    # Move the Status DOWN without amending anything else: the row asks for a
    # human by its own Status (`Drafted` owes a first approval) while no cell
    # has moved away from the snapshotted text — which is the exact state this
    # empty section describes. It was reached with `Modified` until D-9 step 7
    # retired that marker; `Drafted` is the surviving value that puts a row in
    # the queue on its own Status rather than on a diff.
    (root / "docs" / "requirements" / "system-requirements.csv").write_text(
        SR_HEADER + verified.replace(",Approved,", ",Drafted,"), encoding="utf-8"
    )
    assert gen(root).returncode == 0
    page = html_of(root)
    assert "No cell differs from the approved snapshot" in page
    assert "its own <code>Status</code> asks for a human" in page
    # The negative halves: neither the retired advice nor a settled reading.
    assert "check the baseline" not in page.lower()
    assert "nothing changed" not in page.lower()


def test_check_bites_on_drift_and_reproduces_the_stamped_baseline(tmp_path):
    root = repo(tmp_path, oi_rows=PENDING_OI)
    assert gen(root).returncode == 0
    assert gen(root, "--check").returncode == 0, "fresh output must pass its own gate"
    write_view(root, html_of(root).replace("Pick a licence", "Pick a LICENCE"))
    stale = gen(root, "--check")
    assert stale.returncode == 1 and "STALE" in stale.stdout
    # The baseline STAMP retired with `--since` (D-9 step 4): the view no longer
    # records the revision it was rendered against, because the baseline is a
    # directory that is identical on every machine and in CI. `--check` is a
    # plain regenerate-and-compare, and the assertion is that it stays one.
    gi = load_script("gen_open_items")
    assert not hasattr(gi, "BASELINE_RE")
    assert "attestation-baseline" not in html_of(root)


# (test_check_masks_the_machine_local_region retired at concurrency-restructure
# Phase 5: the machine-local advisory region — M-10/WI-266's refs/llm/* mask —
# left with the dispatcher, so the whole view is now a pure function of the
# committed tree and the plain drift test above covers the compare.)


def test_vacuous_without_the_registry_or_the_view(tmp_path):
    # A repo that never adopts the surface pays nothing — the same opt-in
    # posture as the markdown block this replaced.
    root = repo(tmp_path, oi_rows=None)
    proc = gen(root, "--check")
    assert proc.returncode == 0 and "vacuous" in proc.stdout
    assert not (root / "docs" / "open-items.html").exists()


def test_word_diff_marks_only_what_moved(tmp_path):
    gi = load_script("gen_open_items")
    out = gi.word_diff("the quick brown fox", "the quick red fox")
    assert "<del>brown</del>" in out and "<ins>red</ins>" in out
    assert out.count("<del>") == 1 and out.count("<ins>") == 1
    # unchanged runs are wrapped so the view can collapse them
    assert 'class="eq"' in out
    assert gi.changed_percent("a b c d", "a b c d") == 0
    assert gi.changed_percent("a b c d", "w x y z") == 100


def test_html_escapes_registry_prose(tmp_path):
    # A brief cell is arbitrary human text; an unescaped `<` would silently eat
    # the rest of the card (or worse, inject markup into the owner's surface).
    repo(
        tmp_path,
        oi_rows="OI-9,Escaping,pending,2026-01-01,rule <b>this</b> & that,"
        '"A <script>alert(1)</script> cell.","None.","(a) · (b)","do (a).",WI-001,,\n',
    )
    assert gen(tmp_path).returncode == 0
    page = html_of(tmp_path)
    assert "<script>alert(1)</script>" not in page
    assert "&lt;script&gt;" in page


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


# --- A3 closure, extended here (WI-470, SR-052 coverage remainder) -----------
# `test_a3_every_painted_vocabulary_member_is_explained_in_words`
# (test_traj_render_sweeps.py) sweeps gen_trajectory's declared palette dicts —
# this module has no such dict to enumerate; its colour-differentiated idioms
# (the diff marks, the ratify/re-attest pills) were held apart by comment
# discipline alone (the module docstring's own claim: "ins/del carries
# line-through + box-shadow ... pills carry words"). These are that closure's
# equivalent for THIS module's own two encodings — each pinned so a future
# edit that quietly drops the non-colour half reds here instead of shipping.
#
# OUT OF SCOPE, stated rather than silently narrowed: `.empty`'s
# `--pending`-coloured left border (the callout accent on an explanatory
# paragraph) is a single accent used for one meaning with nothing competing
# against it — A3 guards against colour doing the work of DISTINGUISHING
# between concepts, and there is only one concept here, always paired with a
# full sentence of prose. Nothing to disambiguate, so nothing to close.


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


def test_a3_kind_pills_are_never_distinguished_by_colour_alone(tmp_path):
    """The `.pill.ratify` / `.pill` pair (`_KIND_LABELS`) is the render-level
    half: the two kinds share the same shape and differ only in `--pending`
    vs `--muted` colour (the CSS above), so a colour-only encoding here would
    be a future edit that let two DIFFERENTLY-coloured kinds render the SAME
    words — nothing in the CSS itself could catch that, only the rendered
    text can. A fixture that owes one of each kind proves both actually
    appear together on one page with distinct wording, not just that the code
    CAN produce distinct wording."""
    drafted = (
        "SR-001,A drafted need,SN-001,shall do the new thing,because,"
        "criteria,,C,Test,Drafted,1,W\n"
    )
    approved = (
        "SR-002,An amended need,SN-001,shall do the ORIGINAL thing,because,"
        "criteria,,C,Test,Approved,1,W\n"
    )
    root = repo(tmp_path, sr_rows=drafted + approved)
    _git_init(root)
    _approve(root)
    (root / "docs" / "requirements" / "system-requirements.csv").write_text(
        SR_HEADER + drafted + approved.replace("ORIGINAL", "CHANGED"),
        encoding="utf-8",
    )
    assert gen(root).returncode == 0
    page = html_of(root)
    ratify_texts = set(re.findall(r'<span class="pill ratify">([^<]*)</span>', page))
    plain_texts = set(re.findall(r'<span class="pill">([^<]*)</span>', page))
    assert ratify_texts, "no ratify-kind pill rendered — the sweep is vacuous"
    assert plain_texts, "no plain-kind pill rendered — the sweep is vacuous"
    collide = ratify_texts & plain_texts
    assert not collide, (
        "a colour-differentiated pill kind shares its wording with a "
        "differently-coloured kind — colour alone would be all that told "
        "them apart: {}".format(collide)
    )


def test_the_view_names_its_authority(tmp_path):
    """If the view and `trace.py --ratify` ever disagree, the brief wins and the
    view is the bug. That is only useful if the page SAYS so where a reader
    ruling from it can see it."""
    repo(tmp_path, oi_rows=PENDING_OI)
    assert gen(tmp_path).returncode == 0
    page = html_of(tmp_path)
    assert "reattest_model" in page and "authoritative" in page


# --- 122-REVIEW-A regressions: one per finding, each proven against the defect --


# (`test_baseline_is_reused_when_no_since_is_passed` retired at D-9 step 4. It
# was 122-REVIEW-A's BLOCKER as a regression: regenerating with no `--since`
# used to fall back to a re-derived baseline and DESTROY the attestation depth
# an owner was about to read — driven, it collapsed 43 chain-row diffs to 18.
# The stamp-and-reuse rule it pinned has no subject any more: there is one
# baseline, it is a directory, and no run can pick a different one.)


def test_crlf_cell_is_stripped_at_the_source(tmp_path):
    """122-REVIEW-A found half of this: `write_text` newline-TRANSLATES, so a
    registry cell holding a CRLF went to disk as CR CR LF and read back as two
    LFs — the view failed `--check` the moment it was generated, permanently.

    The root cause is a CR reaching the emitted HTML at all, and `esc` is the one
    choke point every registry value passes through, so that is where it is
    stripped. Asserted on the FILE, independent of how the compare works — the
    two fixes would otherwise mask each other and neither mutation would bite."""
    root = repo(tmp_path, oi_rows="")
    (root / "docs" / "requirements" / "open-items.csv").write_bytes(
        OI_HEADER.encode("utf-8")
        + b'OI-6,CRLF cell,pending,,one line,"line one,\r\nline two",,,,,,\r\n'
    )
    assert gen(root).returncode == 0
    raw = (root / "docs" / "open-items.html").read_bytes()
    assert b"\r" not in raw, "a CR from a registry cell reached the emitted view"
    assert b"line two" in raw, "...and the cell's content must still be there"
    # ...and the round trip its absence protects.
    assert gen(root, "--check").returncode == 0
    assert gen(root).returncode == 0
    assert gen(root, "--check").returncode == 0


def test_check_is_agnostic_to_the_checkouts_line_endings(tmp_path):
    """The mirror hazard, caught by the WI-322 rework rather than the review: a
    CHECKOUT can carry CRLF line endings by local git convention (a fresh
    worktree on Windows), and a byte-exact compare then reds a file nothing
    touched. Stripping CR at the source cannot help here — the CRs are the
    file's own line endings — so the compare normalizes both sides."""
    root = repo(tmp_path, oi_rows=PENDING_OI)
    assert gen(root).returncode == 0
    assert gen(root, "--check").returncode == 0
    # Simulate the CRLF checkout, byte for byte.
    view = root / "docs" / "open-items.html"
    view.write_bytes(view.read_bytes().replace(b"\n", b"\r\n"))
    assert b"\r\n" in view.read_bytes()
    assert gen(root, "--check").returncode == 0, (
        "a CRLF checkout must not read as stale — nothing about the content changed"
    )
    # The negative half: REAL content drift still bites, CRLF or not.
    view.write_bytes(view.read_bytes().replace(b"Pick a licence", b"Pick a LICENCE"))
    assert gen(root, "--check").returncode == 1


def test_empty_attestation_state_names_only_what_it_checked(tmp_path):
    """122-REVIEW-A: the whole-section empty state claimed no Drafted/Modified
    SPINE ROW while the model selects SRs only — a Drafted LLR under a Approved SR
    is invisible AND was actively denied. Say what was checked."""
    repo(
        tmp_path,
        sr_rows="SR-007,Settled,SN-001,shall,because,criteria,,C,Test,Approved,1,W\n",
        llr_rows=(
            "LLR-007,SR-007,A drafted child,mod.py,sym,detail,(see TC-007),"
            "Drafted,CMP-001,1\n"
        ),
    )
    assert gen(tmp_path).returncode == 0
    page = html_of(tmp_path)
    assert "<strong>SR</strong>" in page
    assert "snapshot-drift" in page  # where the reader is sent instead
    assert "spine row — nothing owes" not in page  # the refuted claim is gone


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


def test_retired_markdown_surface_is_reported(tmp_path):
    """122-REVIEW-A: a resynced adopter keeps docs/open-items.md, whose generated
    block nothing writes any more — it can assert a stale owner action with every
    gate green. Warn-only: the migration is the owner's, and failing would red a
    repo midway through it."""
    root = repo(tmp_path, oi_rows=PENDING_OI)
    assert gen(root).returncode == 0
    (root / "docs" / "open-items.md").write_text(
        "# Open items\n\n- **WI-999** blocked, awaiting ratification\n",
        encoding="utf-8",
    )
    proc = gen(root, "--check")
    assert proc.returncode == 0, "warn-only — it must not red a repo mid-migration"
    assert "still present beside the registry" in proc.stdout
    assert "RESYNC_PACK.md" in proc.stdout  # the recipe's one home (OI-27)
    # The negative half: no stale file, no warning.
    (root / "docs" / "open-items.md").unlink()
    assert "still present" not in gen(root, "--check").stdout


def test_collapse_toggle_is_wired_to_the_unchanged_runs(tmp_path):
    """Done-when V4, which 122-REVIEW-A marked UNCOVERED. Structural, and the
    narrowing is stated rather than hidden: this asserts the toggle EXISTS,
    targets the `.eq` runs the diff emits, and preserves the full text for
    restore. Whether a browser actually collapses them is runtime behaviour no
    stdlib test can drive — that needs the Playwright harness, and asserting it
    here would be the proxy this repo refuses."""
    verified = (
        "SR-008,Amended,SN-001,shall do a thing,because,criteria,,C,Test,Approved,1,W\n"
    )
    root = repo(tmp_path, sr_rows=verified)
    _git_init(root)
    _approve(root)
    # A real amendment, so a real diff renders: the `.eq` runs only exist where
    # unchanged text sits BESIDE a change, which is exactly what the toggle
    # collapses.
    # NO STATUS FLIP SINCE D-9 STEP 7: the row stays `Approved` and reaches the
    # queue by DRIFT alone, which is what an amendment looks like under the new
    # ladder. The diff being rendered is the same one.
    (root / "docs" / "requirements" / "system-requirements.csv").write_text(
        SR_HEADER + verified.replace("a thing", "a DIFFERENT thing"),
        encoding="utf-8",
    )
    assert gen(root).returncode == 0
    page = html_of(root)
    assert 'id="focus"' in page and 'type="checkbox"' in page
    assert ".diff .eq" in page  # the toggle targets the runs the diff emits
    assert "data-full" in page  # ...and keeps the original for restore
    assert 'class="eq"' in page  # ...which the rendered diff really emits


def ctx_blocks(page):
    """The rendered context blocks, each sliced from its opening tag to the next
    structural boundary. A crude split rather than a parser, deliberately: the
    assertions below need to know WHICH block a field landed in, and the kit
    installs nothing to parse HTML with."""
    out = []
    for chunk in page.split('<div class="ctx">')[1:]:
        end = min(
            (
                i
                for i in (chunk.find('<div class="row"'), chunk.find("</article>"))
                if i >= 0
            ),
            default=len(chunk),
        )
        out.append(chunk[:end])
    return out


def test_full_row_context_renders_beside_the_diff_and_complements_it(tmp_path):
    """The owner's 2026-07-27 finding: the surface showed WHICH CELLS MOVED and
    nothing else, so a rewritten `Rationale` arrived with no `Requirement` beside
    it — and "does the existing evidence still verify this row" is a question
    about what the row now SAYS, not only about what changed in it.

    Structural, and the narrowing is stated: this asserts the context is
    RENDERED, is wired to the same control, and complements rather than repeats
    the diff. Whether a browser reveals it on click is runtime behaviour no
    stdlib test can drive (the same boundary the collapse guard states)."""
    verified = (
        "SR-009,Amended reasoning,SN-001,shall hold the ORIGINAL requirement,"
        "because of the old reason,the acceptance criteria,,C,Test,Approved,1,W\n"
    )
    root = repo(tmp_path, sr_rows=verified)
    _git_init(root)
    _approve(root)
    # NO STATUS FLIP SINCE D-9 STEP 7 — the row stays `Approved` and reaches the
    # queue by DRIFT on the amended cell alone.
    (root / "docs" / "requirements" / "system-requirements.csv").write_text(
        SR_HEADER
        + verified.replace("because of the old reason", "because of a NEW reason"),
        encoding="utf-8",
    )
    assert gen(root).returncode == 0
    page = html_of(root)
    blocks = ctx_blocks(page)
    assert blocks, "an amended row rendered no context block"
    block = blocks[0]
    # The context the diff omitted — the requirement the amended rationale argues
    # for, and the criteria that carry its evidence.
    assert "shall hold the ORIGINAL requirement" in block
    assert "the acceptance criteria" in block
    # The negative halves. (a) The changed cell is NOT repeated as a plain field:
    # an unmarked second copy of the text under review is exactly what an
    # attestation must not carry.
    assert ">Rationale<" not in block
    assert "because of a NEW reason" not in block
    # (b) An empty column is not context — `Notes` is blank in the fixture.
    assert ">Notes<" not in block
    # (c) The SR row rendered its own diff, so the card-level fallback block for
    # a chain-only amendment must not also fire.
    assert "itself — no cell of this row changed" not in page
    # Wired to the SAME control as the text collapse, and honest without JS.
    assert "body.ctx-open .ctx" in page and "'ctx-open'" in page
    assert "<noscript><style>.ctx{display:flex;}</style></noscript>" in page


def test_sr_text_renders_when_only_a_child_row_was_amended(tmp_path):
    """An SR can owe a re-attest while nothing but its Status flipped — the whole
    amendment sitting in an LLR or TC beneath it. That section used to open with
    a child-row diff and never state the requirement it hangs from."""
    sr = (
        "SR-010,A stable requirement,SN-001,shall state the THING BEING VERIFIED,"
        "because,criteria,,C,Test,{},1,W\n"
    )
    llr = "LLR-010,SR-010,A child,mod.py,sym,{},TC-010,Approved,CMP-001,1\n"
    root = repo(
        tmp_path, sr_rows=sr.format("Approved"), llr_rows=llr.format("old detail")
    )
    _git_init(root)
    _approve(root)
    # ONLY THE CHILD MOVES SINCE D-9 STEP 7. The SR used to flip to `Modified`
    # to enter the queue; under the new ladder it stays `Approved` and the
    # CHAIN DRIFT pulls it in — which is the same state this test was always
    # about (nothing of the SR itself changed) reached the way it now happens.
    (root / "docs" / "requirements" / "low-level-requirements.csv").write_text(
        LLR_HEADER + llr.format("NEW detail"), encoding="utf-8"
    )
    assert gen(root).returncode == 0
    page = html_of(root)
    assert "SR-010 itself — no cell of this row changed" in page
    assert "shall state the THING BEING VERIFIED" in page
    # The negative half: the fallback states what it is, and does not claim the
    # SR was amended — the LLR is what changed, and it still shows its diff.
    assert "<del>old</del>" in page and "<ins>NEW</ins>" in page


# --- the batch-2 carrier (repo-lock §8.1) -------------------------------------


def test_an_unreadable_decision_queue_refuses_rather_than_rendering_it_empty(tmp_path):
    """THE FALSE GREEN THIS MIGRATION'S SHAPE EXISTS TO REFUSE.

    Under the CSV carrier a malformed registry still parsed into *something*,
    and a registry that vanished parsed into nothing — either way this view
    rendered "0 pending decisions", which on the owner's decision queue reads as
    "nothing is waiting on you". `spine_carrier.load` raises on a carrier that
    exists and will not parse, so the surface refuses to be published wrong.
    """
    root = repo(tmp_path, oi_rows=None)
    (root / "docs" / "requirements" / "open-items.toml").write_text(
        '[open_item.OI-1]\ntitle = "unterminated\n', encoding="utf-8"
    )
    proc = gen(root)
    assert proc.returncode != 0
    assert "does not parse" in (proc.stdout + proc.stderr)


def test_the_view_points_at_whichever_carrier_is_live(tmp_path):
    """The pointer an owner follows to edit a brief must name a file that
    exists. Both arms, because the kit ships to repos on either carrier."""
    root = repo(tmp_path, oi_rows=None)
    (root / "docs" / "requirements" / "open-items.toml").write_text(
        '[open_item.OI-1]\ntitle = "t"\nstatus = "pending"\n', encoding="utf-8"
    )
    assert gen(root).returncode == 0
    assert "docs/requirements/open-items.toml" in html_of(root)
    assert "docs/requirements/open-items.csv" not in html_of(root)

    root2 = repo(tmp_path / "csv", oi_rows="OI-1,t,pending,,,,,,,,,\n")
    assert gen(root2).returncode == 0
    assert "docs/requirements/open-items.csv" in html_of(root2)


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


# --- OI-41 ARM 2 + ARM 3: what a deferral declares, and what an empty queue
# --- contradicts. Both are WARN-FIRST by the ruling — they print, they never
# --- move this step's exit code, which stays the freshness verdict.


def _log_d(root, name, body):
    d = root / "docs" / "log.d"
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_text(body, encoding="utf-8")
    return root


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


def test_the_deferral_arms_print_but_never_move_the_exit_code(tmp_path):
    # Warn-first by the ruling. The exit code of this step stays the FRESHNESS
    # verdict; a contradiction that redded the commit bar would be switched off.
    root = repo(tmp_path, oi_rows=RULED_OI)
    (root / "docs" / "provenance-allow").write_text(
        "SR-001 Rationale added 2026-08-16 — OI-5: ruled, execution owed.\n",
        encoding="utf-8",
    )
    assert gen(root).returncode == 0
    proc = gen(root, "--check")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "VACUITY" in proc.stdout
    assert "up to date" in proc.stdout
