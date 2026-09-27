"""gen_open_items.py — the generated owner decision surface (WI-322, OI-10 (b)).

`docs/open-items.md` is retired: decision briefs are ROWS in
`docs/requirements/open-items.csv`, and this generator renders them — plus every
spine row owing an approval (`Drafted`) or a re-attest (`Modified`), with a
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

The cases that call the generator's functions in-process (the renderers, the
theme guards, the deferral declarations) live in test_gen_open_items_render.py,
in the per-commit smoke tier; this module drives the generator as a subprocess
over git-committed fixtures and runs at slice/phase close and in CI.
"""

import re
import shutil
import subprocess

from conftest import ROOT, SCRIPTS, load_script, pin_autocrlf, run_py

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
    pin_autocrlf(root)  # WI-461/WI-465; see conftest.pin_autocrlf
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
    approval, an amended row owes a re-attest, and a view that renders only
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


def test_drafted_child_under_approved_undrifted_sr_owes(tmp_path):
    """The OI-61-sitting gap
    (docs/log.d/2026-08-23-oi61-rule-and-spine-approval.md): `owes()` used to
    test the SR row's own `Status` alone, so a `Drafted` LLR/TC hanging off an
    `Approved`, undrifted SR reached no surface — the drift arm cannot catch it
    either, since a row below approval has made no claim to fall from. Widened:
    the chain is asked too, and the pill says WHY."""
    sr = (
        "SR-020,Stable parent,SN-001,shall hold,because,criteria,,C,Test,Approved,1,W\n"
    )
    root = repo(tmp_path, sr_rows=sr)
    _git_init(root)
    _approve(root)
    # The SR is untouched after the snapshot — no drift. A brand-new `Drafted`
    # LLR is added under it: never approved, absent from the snapshot.
    llr = "LLR-020,SR-020,A new child,mod.py,sym,detail,TC-020,Drafted,CMP-001,1\n"
    (root / "docs" / "requirements" / "low-level-requirements.csv").write_text(
        LLR_HEADER + llr, encoding="utf-8"
    )
    assert gen(root).returncode == 0
    page = html_of(root)
    assert 'id="SR-020-attest"' in page and "approval owed" in page
    assert "LLR-020" in page and "Drafted" in page and "never approved" in page


def test_approved_child_under_approved_sr_does_not_owe(tmp_path):
    """The negative half: an `Approved` child under an `Approved`, undrifted SR
    owes nothing — the widening must not turn every settled chain row into a
    false positive."""
    sr = (
        "SR-021,Stable parent,SN-001,shall hold,because,criteria,,C,Test,Approved,1,W\n"
    )
    llr = "LLR-021,SR-021,A child,mod.py,sym,detail,TC-021,Approved,CMP-001,1\n"
    root = repo(tmp_path, sr_rows=sr, llr_rows=llr)
    _git_init(root)
    _approve(root)
    assert gen(root).returncode == 0
    page = html_of(root)
    assert 'id="SR-021-attest"' not in page
    assert "no SR owes an approval or a re-attest" in page


def test_drafted_child_unchanged_since_snapshot_still_owes(tmp_path):
    """A `Drafted` row can sit in `docs/archive/last_approved/` byte-identical to
    its current text — `intake.py snapshot` copies every registry wholesale, not
    only approved rows — so the widened arm cannot rely on a cell diff to notice
    it; it has to ask `Status` directly, independent of whether anything moved."""
    sr = (
        "SR-022,Stable parent,SN-001,shall hold,because,criteria,,C,Test,Approved,1,W\n"
    )
    llr = "LLR-022,SR-022,A child,mod.py,sym,detail,TC-022,Drafted,CMP-001,1\n"
    root = repo(tmp_path, sr_rows=sr, llr_rows=llr)
    _git_init(root)
    _approve(root)  # snapshots the Drafted LLR too, unchanged
    assert gen(root).returncode == 0
    page = html_of(root)
    assert 'id="SR-022-attest"' in page and "approval owed" in page
    assert "No cell differs from the approved snapshot" in page


def test_drafted_row_cells_are_not_labelled_approved(tmp_path):
    """OI-71 defect 1, the HTML half — this view and the `--approve modified`
    markdown brief must agree (IF-074). A `Drafted` TC that drifted in both an
    approved-class cell (`Method`) and a traced-class cell (`Evidence`) used to
    render its `Method` change under the §A5.1 heading `approved — re-attestation
    owed`, keyed on the cell's COLUMN class alone — a re-attestation window on a
    row that was never approved. It owes a FIRST approval wholesale."""
    sr = (
        "SR-023,Stable parent,SN-001,shall hold,because,criteria,,C,Test,Approved,1,W\n"
    )
    tc = "TC-023,SR-023,Unit,drive the old path,Smoke,a=1,sum,Yes,old-ev,Drafted,1\n"
    root = repo(tmp_path, sr_rows=sr, tc_rows=tc)
    _git_init(root)
    _approve(root)  # snapshots the Drafted TC with its old Method/Evidence
    # Amend both a Method (approved-class) and an Evidence (traced-class) cell,
    # still Drafted: both groups would be non-empty on the approved path, so the
    # split heading would show — unless the row's Drafted status collapses it.
    (root / "docs" / "test" / "test-cases.csv").write_text(
        TC_HEADER
        + "TC-023,SR-023,Unit,drive the NEW path,Smoke,a=1,sum,Yes,new-ev,Drafted,1\n",
        encoding="utf-8",
    )
    assert gen(root).returncode == 0
    page = html_of(root)
    assert "TC-023" in page and "never approved" in page
    assert "<ins>NEW</ins>" in page  # the change is still shown, via word_diff
    assert "approved — re-attestation owed" not in page


# --- the SR-177 gap: the anchor SR's own text, unconditional and never -----
# --- hidden behind the "Collapse unchanged text" toggle --------------------


def test_anchor_sr_requirement_and_rationale_render_unconditionally_and_visibly(
    tmp_path,
):
    """The owner's report, verbatim (2026-08-24): opening open-items.html and
    looking at SR-177, the requirement text itself was nowhere on the page.

    It WAS on the page — inside `.ctx`, which is `display:none` until the
    toolbar's "Collapse unchanged text" box (checked by default) is cleared —
    for exactly the shape SR-177 is: `Approved`, undrifted, its amendment
    living entirely in a `Drafted` child. The anchor block must render the
    SR's own Requirement/Rationale OUTSIDE `.ctx`, before it, so it is visible
    on load with no interaction."""
    sr = (
        "SR-030,Stable parent,SN-001,shall report the DISTINCTIVE requirement,"
        "because DISTINCTIVE rationale,criteria,,C,Test,Approved,1,W\n"
    )
    llr = "LLR-030,SR-030,A new child,mod.py,sym,detail,TC-030,Drafted,CMP-001,1\n"
    root = repo(tmp_path, sr_rows=sr, llr_rows=llr)
    _git_init(root)
    _approve(root)
    assert gen(root).returncode == 0
    page = html_of(root)
    card_start = page.index('id="SR-030-attest"')
    ctx_start = page.index('class="ctx"', card_start)
    anchor_slice = page[card_start:ctx_start]
    assert "DISTINCTIVE requirement" in anchor_slice
    assert "DISTINCTIVE rationale" in anchor_slice
    # ...and it is not ALSO duplicated inside the collapsed remainder — one
    # visible copy, not a visible one plus a hidden one.
    assert page.count("DISTINCTIVE requirement") == 1
    assert page.count("DISTINCTIVE rationale") == 1


def test_anchor_requirement_truncates_above_threshold_not_below(tmp_path):
    """Long-cell sanity: a cell above the 1,500-char threshold truncates with
    an explicit marker; a cell comfortably below it renders untouched."""
    long_req = "A" * 1600
    short_req = "B" * 100
    sr_rows = "SR-031,Long,SN-001,{},because,criteria,,C,Test,Approved,1,W\n".format(
        long_req
    ) + "SR-032,Short,SN-001,{},because,criteria,,C,Test,Approved,1,W\n".format(
        short_req
    )
    llr_rows = (
        "LLR-031,SR-031,child,mod.py,sym,detail,TC-031,Drafted,CMP-001,1\n"
        "LLR-032,SR-032,child,mod.py,sym,detail,TC-032,Drafted,CMP-001,1\n"
    )
    root = repo(tmp_path, sr_rows=sr_rows, llr_rows=llr_rows)
    _git_init(root)
    _approve(root)
    assert gen(root).returncode == 0
    page = html_of(root)
    assert "more chars — read the registry row" in page
    assert "A" * 1500 in page
    assert "A" * 1600 not in page
    assert "B" * 100 in page


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


# --- A3 closure, extended here (WI-470, SR-052 coverage remainder) -----------
# `test_a3_every_painted_vocabulary_member_is_explained_in_words`
# (test_traj_render_sweeps.py) sweeps gen_trajectory's declared palette dicts —
# this module has no such dict to enumerate; its colour-differentiated idioms
# (the diff marks, the approve/re-attest pills) were held apart by comment
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


def test_a3_kind_pills_are_never_distinguished_by_colour_alone(tmp_path):
    """The `.pill.approve` / `.pill` pair (`_KIND_LABELS`) is the render-level
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
    approval_texts = set(re.findall(r'<span class="pill approve">([^<]*)</span>', page))
    plain_texts = set(re.findall(r'<span class="pill">([^<]*)</span>', page))
    assert approval_texts, "no approval-kind pill rendered — the sweep is vacuous"
    assert plain_texts, "no plain-kind pill rendered — the sweep is vacuous"
    collide = approval_texts & plain_texts
    assert not collide, (
        "a colour-differentiated pill kind shares its wording with a "
        "differently-coloured kind — colour alone would be all that told "
        "them apart: {}".format(collide)
    )


def test_the_view_names_its_authority(tmp_path):
    """If the view and `trace.py --approve` ever disagree, the brief wins and the
    view is the bug. That is only useful if the page SAYS so where a reader
    ruling from it can see it."""
    repo(tmp_path, oi_rows=PENDING_OI)
    assert gen(tmp_path).returncode == 0
    page = html_of(tmp_path)
    assert "reattest_model" in page and "authoritative" in page


def test_the_footer_names_reattests_for_blessing_an_amendment(tmp_path):
    """Blessing an amendment re-copies a row that still reads `Approved`, so no
    flip carries it, and a bare `intake.py snapshot` refuses it. The footer's
    instruction has to name the row, or it hands the owner a refusal."""
    repo(tmp_path, oi_rows=PENDING_OI)
    assert gen(tmp_path).returncode == 0
    assert "intake.py snapshot --reattests &lt;ROW-ID&gt;" in html_of(tmp_path)


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
    """122-REVIEW-A named a real gap: the whole-section empty state used to
    claim no Drafted/Modified SPINE ROW while the model selected SRs only, so a
    Drafted LLR under an Approved SR was invisible AND actively denied. That
    gap is CLOSED (the OI-61-sitting widening,
    docs/log.d/2026-08-23-oi61-rule-and-spine-approval.md) — a Drafted LLR now
    surfaces directly, so this fixture no longer reaches the empty state at
    all; `test_drafted_child_under_approved_undrifted_sr_owes` covers that.
    What remains to guard here is the TRULY vacuous state — nothing Drafted
    anywhere, nothing drifted — and that its wording states the widened
    contract honestly rather than the pre-widening SR-only caveat."""
    repo(
        tmp_path,
        sr_rows="SR-007,Settled,SN-001,shall,because,criteria,,C,Test,Approved,1,W\n",
    )
    assert gen(tmp_path).returncode == 0
    page = html_of(tmp_path)
    assert "<strong>SR</strong>" in page and "<strong>LLR</strong>" in page
    assert "snapshot-drift" in page  # drift is still one route in
    assert "reaches this view DIRECTLY" in page  # ...but Drafted no longer needs it
    assert "spine row — nothing owes" not in page  # the refuted claim stays gone


def test_retired_markdown_surface_is_reported(tmp_path):
    """122-REVIEW-A: a resynced adopter keeps docs/open-items.md, whose generated
    block nothing writes any more — it can assert a stale owner action with every
    gate green. Warn-only: the migration is the owner's, and failing would red a
    repo midway through it."""
    root = repo(tmp_path, oi_rows=PENDING_OI)
    assert gen(root).returncode == 0
    (root / "docs" / "open-items.md").write_text(
        "# Open items\n\n- **WI-999** blocked, awaiting approval\n",
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


# --- OI-41 ARM 2 + ARM 3: what a deferral declares, and what an empty queue
# --- contradicts. Both are WARN-FIRST by the ruling — they print, they never
# --- move this step's exit code, which stays the freshness verdict.


def _log_d(root, name, body):
    d = root / "docs" / "log.d"
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_text(body, encoding="utf-8")
    return root


# --- OI-70 ARM 4 (WI-553): a `none` declaration cross-checked for TRUTH, not
# --- merely presence — a fragment that writes `none` while its own scope cites a
# --- PENDING open item is contradicted. Warn-first, position-is-scope, fail-soft.


def test_the_all_clear_prints_MEASURED_counts_not_a_literal(tmp_path):
    """MAJOR-6's second arm: the reassurance used to be a hardcoded sentence, so
    it read identically whether the measurement had found nothing or had failed
    to run. Every disarming path (a dropped line, an unreadable declaration)
    produces the same empty findings list, which is exactly when the counts
    matter."""
    root = repo(tmp_path, oi_rows=RULED_OI)
    (root / "docs" / "provenance-allow").write_text(
        "SR-001 Rationale added 2026-08-16 -- OI-5: a hyphen, not an em dash.\n",
        encoding="utf-8",
    )
    _log_d(root, "WI-1-none.md", "## s\n\nDeferred open items: none\n")
    proc = gen(root, "--check")
    assert "0 parsed entries" in proc.stdout, proc.stdout
    assert "1 unreadable declaring line(s)" in proc.stdout, proc.stdout
    assert "1 fragment declaration(s) read, 1 of them `none`" in proc.stdout


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


# --- WI-518: the off-spine census, the HTML half of the two renderers over
# `trace.offspine_census_rows` — see tests/test_trace_briefs.py for the
# markdown half and docs/log.d/2026-08-24-oi62-rule-and-spine-approval.md
# (MAJOR-2) for the gap both close.


def test_offspine_census_names_the_interfaces_registry_in_the_html_view(tmp_path):
    snap = load_script("baseline_snapshot")
    root = tmp_path / "repo"
    for rel in snap.SNAPSHOTTED:
        src = ROOT / rel
        if not src.is_file():
            continue
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
    (root / "docs" / "requirements" / "open-items.csv").write_text(
        OI_HEADER, encoding="utf-8"
    )
    snap.copy_live(root, seed=True)
    if_path = root / "docs" / "requirements" / "interfaces.toml"
    data = if_path.read_bytes()
    # The prose `contract` cell left the row at OI-67; the typed `data` cell is
    # the one a census amendment is driven through now.
    # Keyed on the cell's SHAPE (the `data = "..."` line of IF-001's block),
    # never on its text: a re-worded cell must not red a census test.
    m = re.search(rb'(?ms)^\[interface\.IF-001\]\n.*?^(data = ".*?")$', data)
    assert m, "fixture: IF-001's data cell not found"
    needle = m.group(1)
    if_path.write_bytes(
        data.replace(needle, needle[:-1] + b" (amended)" + needle[-1:], 1)
    )
    proc = gen(root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    html = html_of(root)
    assert "docs/requirements/interfaces.toml" in html
    assert "1 changed, 0 added, 0 removed" in html
    # The same copy triggers as the markdown census (see
    # tests/test_trace_briefs.py for where each is driven behaviourally).
    assert "a row in it moves into approval or arrives approved" in html
    assert "<code>--reattests</code> names one of its rows" in html
    assert "moves or <code>--approves</code> names it" not in html
    assert "when its own Status moves" not in html
    # No-change off-spine tiers render nothing.
    assert "docs/requirements/components.toml" not in html
    assert "docs/requirements/external.toml" not in html


def test_offspine_census_is_silent_in_the_html_view_when_nothing_changed(tmp_path):
    snap = load_script("baseline_snapshot")
    root = tmp_path / "repo"
    for rel in snap.SNAPSHOTTED:
        src = ROOT / rel
        if not src.is_file():
            continue
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
    (root / "docs" / "requirements" / "open-items.csv").write_text(
        OI_HEADER, encoding="utf-8"
    )
    snap.copy_live(root, seed=True)
    proc = gen(root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    html = html_of(root)
    assert "offspine-note" not in html
    assert "docs/requirements/interfaces.toml" not in html
