"""gen_open_items.py — the generated owner decision surface (WI-322, OI-10 (b)).

`docs/open-items.md` is retired: decision briefs are ROWS in
`docs/requirements/open-items.csv`, and this generator renders them — plus every
spine row owing a ratification (`Draft`) or a re-attest (`Modified`), with a
word-level before/after — into `docs/open-items.html`.

What these guard, in the order the surface can fail a reader:

  * the briefs render, and a RULED row does not (it is history, not a decision);
  * `Draft` AND `Modified` both surface — "new or changed requirement rows
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
import sys

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
    return (root / "docs" / "open-items.html").read_text(encoding="utf-8")


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


def test_draft_and_modified_rows_both_surface(tmp_path):
    """ "New or changed" is the requirement: a Draft row owes a first
    ratification, a Modified row owes a re-attest, and a view that renders only
    one of them silently drops half the owner's queue."""
    repo(
        tmp_path,
        sr_rows=(
            "SR-001,A drafted need,SN-001,shall do the new thing,because,"
            "criteria,,C,Test,Draft,1,W\n"
            "SR-002,An amended need,SN-001,shall do the changed thing,because,"
            "criteria,,C,Test,Modified,1,W\n"
        ),
    )
    assert gen(tmp_path).returncode == 0
    page = html_of(tmp_path)
    assert 'id="SR-001-attest"' in page and "ratification owed" in page
    assert 'id="SR-002-attest"' in page and "re-attest owed" in page
    # A Draft row has no attested baseline BY DEFINITION — say so, don't imply a
    # missing git history.
    assert "awaiting its FIRST ratification" in page


def test_verified_rows_are_not_in_the_queue(tmp_path):
    # The negative half of the two guards above: a settled row owes nothing and
    # must not appear, or the surface cries wolf on every spine row.
    repo(
        tmp_path,
        sr_rows="SR-003,A settled need,SN-001,shall,because,criteria,,C,Test,Verified,1,W\n",
    )
    assert gen(tmp_path).returncode == 0
    page = html_of(tmp_path)
    assert "SR-003" not in page
    assert "nothing owes a ratification or a re-attest" in page


def test_empty_diff_section_says_check_the_baseline(tmp_path):
    """The lesson from the stale-brief defect: an auto-derived baseline that
    sits AFTER the amendment renders a section with no cells. That must read as
    'check the baseline', never as 'nothing changed' — a confident blank in
    front of a human about to attest is how two of six rows got blessed unseen."""
    verified = (
        "SR-004,No visible delta,SN-001,shall,because,criteria,,C,Test,Verified,1,W\n"
    )
    root = repo(tmp_path, sr_rows=verified)
    subprocess.run(["git", "init", "-q", str(root)], check=True)
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
            "seed",
        ],
        check=True,
    )
    # Flip to Modified WITHOUT amending anything else — the pre-regime streak's
    # shape: the real amendment (if any) landed before the newest still-Verified
    # revision, so the auto-baseline finds no delta.
    (root / "docs" / "requirements" / "system-requirements.csv").write_text(
        SR_HEADER + verified.replace(",Verified,", ",Modified,"), encoding="utf-8"
    )
    assert gen(root).returncode == 0
    page = html_of(root)
    assert "check the baseline" in page.lower()
    assert "Re-run with" in page
    # The negative half: it must NOT read as a settled, blessable row.
    assert "nothing changed" not in page.lower()


def test_check_bites_on_drift_and_reproduces_the_stamped_baseline(tmp_path):
    root = repo(tmp_path, oi_rows=PENDING_OI)
    assert gen(root).returncode == 0
    assert gen(root, "--check").returncode == 0, "fresh output must pass its own gate"
    out = root / "docs" / "open-items.html"
    out.write_text(
        html_of(root).replace("Pick a licence", "Pick a LICENCE"), encoding="utf-8"
    )
    stale = gen(root, "--check")
    assert stale.returncode == 1 and "STALE" in stale.stdout
    # The file DECLARES the baseline it was rendered against, so --check
    # re-renders with the same one instead of comparing against a different
    # history — without it, --since would be a flag whose output no gate could
    # ever reproduce.
    gi = load_script("gen_open_items")
    assert gi.BASELINE_RE.search(html_of(root)) is not None


def test_check_masks_the_machine_local_region(tmp_path):
    """M-10/WI-266's rule, inherited: refs/llm/* facts do not transport with
    clone or push, so byte-comparing them would read STALE in any second clone."""
    root = repo(tmp_path, oi_rows=PENDING_OI)
    assert gen(root).returncode == 0
    gi = load_script("gen_open_items")
    page = html_of(root)
    start = page.index(gi.LOCAL_BEGIN) + len(gi.LOCAL_BEGIN)
    end = page.index(gi.LOCAL_END)
    tampered = (
        page[:start] + "\n<p>a conflict only THIS machine can see</p>\n" + page[end:]
    )
    (root / "docs" / "open-items.html").write_text(tampered, encoding="utf-8")
    assert gen(root, "--check").returncode == 0, "machine-local drift must not gate"
    # The negative half: drift OUTSIDE that region still bites.
    (root / "docs" / "open-items.html").write_text(
        tampered.replace("Pick a licence", "Pick another licence"), encoding="utf-8"
    )
    assert gen(root, "--check").returncode == 1


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
    system, so every theme token this module declares must carry the same value
    the dashboard emits. Extracting them would edit gen_trajectory and re-red
    `perceptual-stale` for a refactor — this catches the drift instead."""
    gi = load_script("gen_open_items")
    gt = load_script("gen_trajectory")
    template = gt.HTML_TEMPLATE.template
    root_block = re.search(r":root \{(.*?)\n  \}", template, re.S).group(1)
    dark_block = re.search(
        r"@media \(prefers-color-scheme: dark\) \{\s*:root \{(.*?)\}", template, re.S
    ).group(1)
    for theme, block in (("light", root_block), ("dark", dark_block)):
        declared = dict(re.findall(r"(--[\w-]+):\s*(#[0-9a-fA-F]{3,8})", block))
        for token, value in gi.THEME[theme].items():
            assert token in declared, (theme, token, "dashboard no longer declares it")
            assert declared[token].lower() == value.lower(), (
                theme,
                token,
                declared[token],
                value,
            )
        # the view's own CSS must use the value it claims to mirror
        assert value.lower() in gi.CSS.lower(), (theme, token, value)


def test_the_view_names_its_authority(tmp_path):
    """If the view and `trace.py --ratify` ever disagree, the brief wins and the
    view is the bug. That is only useful if the page SAYS so where a reader
    ruling from it can see it."""
    repo(tmp_path, oi_rows=PENDING_OI)
    assert gen(tmp_path).returncode == 0
    page = html_of(tmp_path)
    assert "reattest_model" in page and "authoritative" in page
