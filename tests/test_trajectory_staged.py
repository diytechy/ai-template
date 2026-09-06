"""check_trajectory.py — the git-effect (--staged) and git-time recovery checks
(WI-277: split verbatim from tests/test_trajectory.py by behavior boundary).

The --staged warn family (S1 no-validation-delta, WI-316 spine-amend-without-
flip incl. the BOM case, the WI-068 critique-loop ratchet), the WI-205
backlog-staleness and WI-243 critique-staleness git-time warns, and the
concurrency-restructure §5.4 latest-critique selection-by-git-time tests —
everything here builds a real git repo and asserts on effect or recovery. The
WI-280 `_render_surface_paths` pair rides along: it pins the file set the
critique-staleness warn watches, so it belongs beside that warn's own tests.
"""

import csv
import os
import shutil
import subprocess


from conftest import (
    ROOT,
    SCRIPTS,
    load_script,
    pin_autocrlf,
    run_py,
    skip_without_env_gates,
)

wi_convert = load_script("wi_convert")
RENDER_SHARED = (
    "gen_trajectory.py",
    "traj_display.py",
    "traj_parse.py",
    "traj_status.py",
)


# The registry-fixture writers below are copied from tests/test_trajectory.py
# rather than imported — no test module in this suite imports another, and
# conftest is not this module's to extend (the suite idiom test_integrate.py's
# `git_repo` states; WI-277 kept it when splitting the monolith).
# The fixture bodies below stay CSV-SHAPED — one line per work item, cells in one
# of these two column orders — because a table is how a registry fixture reads.
# The registry's one HOME is the `docs/work/` spec folder (concurrency-restructure
# Phase 5, RULING-4: the CSV home retired, and a work-items.csv left on disk is
# now itself an integrity error), so the writers below map each line through the
# format's own writer instead of writing a CSV.
WI_COLUMNS = "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable"
# ...plus the SpecRef column (S1) — used by the SSOT-rule tests. (A BlockRef
# column retired with the blockref vocabulary at WI-553/OI-70.)
SR_WI_COLUMNS = WI_COLUMNS + ",SpecRef"
SR_HEADER = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status\n"
)

# `active/<branch>/` is the only status two levels deep and the branch is the
# integrator's, so a fixture writing an active row has to name one.
ACTIVE_BRANCH = "wi-fixture"


def _wi_rows(body, columns):
    """`body`'s lines as full 17-column registry rows, read with `csv` so a
    quoted cell parses exactly as it did when the body WAS the file."""
    names = columns.split(",")
    rows = []
    for cells in csv.reader(body.splitlines()):
        if not cells or not cells[0].strip():
            continue
        row = dict.fromkeys(wi_convert.COLUMNS, "")
        row.update(dict(zip(names, cells)))
        rows.append(row)
    return rows


def _write_spec_row(work, row, order):
    """Write one row as its spec file under `work`.

    Everything goes through `wi_convert`, the format's single writer — except the
    directory for an `active` row, which that writer deliberately does not know:
    the integrator's BRANCH names `active/<branch>/`, so a fixture supplies one
    and reuses the same renderer for the file itself."""
    if (row.get("Status") or "").strip() != "active":
        return wi_convert.write_spec_file(work, row, order=order)
    text = wi_convert.FENCE + "\n"
    text += wi_convert.render_frontmatter(wi_convert.frontmatter_pairs(row, order))
    text += wi_convert.FENCE + "\n"
    if row.get("Deliverable"):
        text += wi_convert.DELIVERABLE_PREFIX + row["Deliverable"] + "\n"
    path = work / "active" / ACTIVE_BRANCH / wi_convert.spec_filename(row)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def write_wis(root, body, columns=WI_COLUMNS):
    """Write the work-item registry — the `docs/work/` spec folder — from the
    CSV-shaped `body`, one spec file per line.

    The folder is REPLACED on every call: one call writes the whole registry, so
    a test that re-writes it (a status flip) MOVES the item's file rather than
    leaving a second copy in the old status directory. Two rows sharing an id
    stay two files (their titles differ, so their slugs do), which is what keeps
    the duplicate-id integrity error reachable."""
    work = root / "docs" / "work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    for order, row in enumerate(_wi_rows(body, columns), 1):
        _write_spec_row(work, row, order)
    return root


def run_traj(root, *extra):
    return run_py([SCRIPTS / "check_trajectory.py", "--root", root, *extra], cwd=root)


def write_wis_sr(root, body):
    """`write_wis` for a `body` that also fills the SpecRef cell."""
    return write_wis(root, body, SR_WI_COLUMNS)


def write_spec(root, rel, *headings):
    """Create an in-repo spec file so a SpecRef resolves (R-E).

    `headings` become `##` sections, so a `path#anchor` SpecRef citing one of
    them resolves on BOTH halves (WI-354). A caller that passes none is testing
    the path half only and must not cite an anchor."""
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    body = "# spec\n" + "".join("\n## {}\n".format(h) for h in headings)
    p.write_text(body, encoding="utf-8")


# --- S1: the no-validation-delta warn (--staged) -------------------------------


def _init_followup_repo(root):
    """A git repo whose HEAD has WI-001 done (delivered SR-001) and WI-002 open,
    with WI-002 then closed as a follow-up on the same SR in the working tree.
    Returns the git runner; the caller stages the pieces under test."""
    skip_without_env_gates("git")
    git = shutil.which("git")

    def run_git(*a):
        return subprocess.run(
            [git, "-C", str(root), *a], capture_output=True, text=True
        )

    run_git("init")
    pin_autocrlf(root)  # WI-461/WI-465; see conftest.pin_autocrlf
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    write_wis_sr(
        root,
        "WI-001,First,scripts,SR-001,,done,delivered SR-001,\n"
        "WI-002,Follow-up,scripts,SR-001,WI-001,active,,docs/specs/WI-002.md\n",
    )
    run_git("add", "-A")
    run_git("commit", "-m", "init")
    # Close WI-002 in the working tree (a follow-up on SR-001, already delivered).
    write_wis_sr(
        root,
        "WI-001,First,scripts,SR-001,,done,delivered SR-001,\n"
        "WI-002,Follow-up,scripts,SR-001,WI-001,done,patched the code,\n",
    )
    return run_git


def test_staged_no_validation_delta_warns(tmp_path):
    # Closing a follow-up WI on an already-delivered SR while touching neither the
    # TC registry nor a test file warns: the fix did not land in the chain.
    run_git = _init_followup_repo(tmp_path)
    run_git("add", "docs/work")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "validation chain did not change" in proc.stderr
    assert "WI-002" in proc.stderr


def test_staged_no_warn_when_a_test_changes(tmp_path):
    # The same close, but a test file is also staged -> the chain changed, no warn.
    run_git = _init_followup_repo(tmp_path)
    (tmp_path / "tests").mkdir(exist_ok=True)
    (tmp_path / "tests" / "test_fix.py").write_text("# covers the fix\n", "utf-8")
    run_git("add", "docs/work", "tests/test_fix.py")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "validation chain did not change" not in proc.stderr


def test_staged_is_a_no_op_outside_git(tmp_path):
    # No git repo -> --staged is a silent no-op (warn-first, never a crash).
    write_wis_sr(tmp_path, "WI-001,A,scripts,,,active,,docs/specs/WI-001.md\n")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "validation chain" not in proc.stderr


# --- WI-316: the amend-without-flip warn (--staged, warn-first) -----------------

_SPINE_SR_HEADER = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status,Phase,Aspect,Hat-Refs\n"
)


def _sr_row(req="the original attested text", status="Approved", hats="hat.MAINTAINER"):
    # `Hat-Refs` is carried by the fixture rather than by a second header
    # because WI-484 phase 5's arm reads it on the SAME rows the WI-316 warn
    # scans — two fixtures would let the two guards drift apart in the tests
    # exactly where they must not in the code.
    return 'SR-001,Adder,SN-001,"{}","why","ac",,C,Test,{},1,,{}\n'.format(
        req, status, hats
    )


def _init_spine_repo(root):
    """A git repo whose HEAD holds SR-001 Approved. Returns the git runner."""
    skip_without_env_gates("git")
    git = shutil.which("git")

    def run_git(*a):
        return subprocess.run(
            [git, "-C", str(root), *a], capture_output=True, text=True
        )

    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "system-requirements.csv").write_text(
        _SPINE_SR_HEADER + _sr_row(), encoding="utf-8"
    )
    run_git("init")
    pin_autocrlf(root)  # WI-461/WI-465; see conftest.pin_autocrlf
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    run_git("add", "-A")
    run_git("commit", "-m", "attested baseline")
    return run_git


def _amend_sr(root, req, status):
    (root / "docs" / "requirements" / "system-requirements.csv").write_text(
        _SPINE_SR_HEADER + _sr_row(req, status), encoding="utf-8"
    )


def test_staged_spine_amend_without_flip_warns(tmp_path):
    # Amending an Approved SR's content cells while Status stays Approved warns,
    # naming the row and the changed cells — the write-time discipline the
    # RE-ATTESTATION-PENDING commit-message prose never had (process.md §7).
    run_git = _init_spine_repo(tmp_path)
    _amend_sr(tmp_path, "the AMENDED text", "Approved")
    run_git("add", "-A")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SR-001" in proc.stderr
    assert "Requirement" in proc.stderr
    # THE MESSAGE MOVED AT D-9 STEP 7 and the assertion moves with it. It told
    # the author to set the `Modified` re-attest marker; that marker retired,
    # so it now names the two real outcomes — re-attest in this commit, or the
    # change rides as snapshot drift until the next sitting.
    assert "SNAPSHOT DRIFT" in proc.stderr
    assert "intake.py snapshot" in proc.stderr
    # ...and it no longer names a value the closed enum cannot hold.
    assert "Modified re-attest marker" not in proc.stderr


def test_staged_spine_amend_with_a_status_move_is_silent(tmp_path):
    # The same amendment WITH the row's Status MOVING in the same commit is a
    # deliberate call the guard does not second-guess: no warn.
    # Mutation-proves the warn keys on the STATUS STAYING PUT, not on the diff.
    # It drove `Modified` until D-9 step 7 retired that value; `Drafted` is the
    # live word for the same deliberate act (the author un-blessed the row),
    # and the guard's rule — `head_status != cur_status` — is unchanged.
    run_git = _init_spine_repo(tmp_path)
    _amend_sr(tmp_path, "the AMENDED text", "Drafted")
    run_git("add", "-A")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SNAPSHOT DRIFT" not in proc.stderr


def test_staged_child_amend_needs_its_own_flip_not_the_parents(tmp_path):
    # A row's Status answers for its OWN cells (owner ruling 2026-08-17m):
    # amending an LLR and flipping the LLR ITSELF in the same commit is the
    # sanctioned path — no warn. Flipping the OWNING SR instead (the retired
    # chain reading's sanction) no longer silences the child: its text changed
    # while its own Status still claims approval, so it warns whatever the
    # parent does.
    run_git = _init_spine_repo(tmp_path)
    llr_h = "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status\n"
    llr_csv = tmp_path / "docs" / "requirements" / "low-level-requirements.csv"

    def write_llr(detail, status="Approved"):
        llr_csv.write_text(
            llr_h
            + 'LLR-001,SR-001,Core,src/d.py,f,"{}",(see TC),{}\n'.format(
                detail, status
            ),
            encoding="utf-8",
        )

    write_llr("the original detail")
    run_git("add", "-A")
    run_git("commit", "-m", "attested chain")

    # (1) amend the LLR + move the LLR's OWN status -> silent (its status
    # moved). `Drafted` since D-9 step 7 retired `Modified`; the guard reads
    # "did this row's status change", not which word it changed to.
    write_llr("the AMENDED detail", "Drafted")
    run_git("add", "-A")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SNAPSHOT DRIFT" not in proc.stderr

    # (2) the same LLR amendment left Approved -> the child warns, even with
    # the owning SR's status moved in the same commit (the exemption the
    # retired chain reading used to grant).
    write_llr("the AMENDED detail")
    _amend_sr(tmp_path, "the original attested text", "Drafted")
    run_git("add", "-A")
    proc2 = run_traj(tmp_path, "--staged")
    assert proc2.returncode == 0, proc2.stdout + proc2.stderr
    assert "LLR-001" in proc2.stderr
    assert "re-attest it in this commit" in proc2.stderr


def test_staged_spine_warn_survives_a_bom(tmp_path):
    # Adversarial-review F4: a committed BOM survives `git show` and glued to
    # the id column, silently DISABLING the guard (fails open). The parse now
    # strips it; the amend-without-flip warn must still fire on a BOM'd repo.
    run_git = _init_spine_repo(tmp_path)
    csv_path = tmp_path / "docs" / "requirements" / "system-requirements.csv"
    csv_path.write_bytes(
        bytes([0xEF, 0xBB, 0xBF]) + (_SPINE_SR_HEADER + _sr_row()).encode("utf-8")
    )
    run_git("add", "-A")
    run_git("commit", "-m", "BOM'd attested baseline")
    csv_path.write_bytes(
        bytes([0xEF, 0xBB, 0xBF])
        + (_SPINE_SR_HEADER + _sr_row("the AMENDED text", "Approved")).encode("utf-8")
    )
    run_git("add", "-A")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SR-001" in proc.stderr
    assert "SNAPSHOT DRIFT" in proc.stderr


def test_staged_spine_new_row_and_status_only_flip_are_silent(tmp_path):
    # A NEW row is not an amendment; a Status-only change (e.g. the approval
    # flip Drafted->Approved with no content delta) made a deliberate call the
    # warn does not second-guess. Both stay silent.
    run_git = _init_spine_repo(tmp_path)
    csv_path = tmp_path / "docs" / "requirements" / "system-requirements.csv"
    csv_path.write_text(
        _SPINE_SR_HEADER
        + _sr_row()
        + 'SR-002,New req,SN-001,"fresh","why","ac",,C,Test,Approved,1,,hat.MAINTAINER\n',
        encoding="utf-8",
    )
    run_git("add", "-A")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "re-attest marker" not in proc.stderr


# --- WI-572: the APPROVAL ACT half of the same walk ---------------------------
#
# Owner ruling 2026-09-01: the `Status` flip into `Approved`/`Founded` and the
# `docs/archive/last_approved/` copy that anchors it are the ADJUDICATOR's, on
# the serial trunk side; a worker lane authors `Drafted` rows and amends text.
# `staged_spine_amendments` above EXEMPTS a row whose Status moved ("a
# deliberate call this does not second-guess"); `staged_approval_acts` reports
# exactly that exempted set, off the same two-tree walk, so the pair covers the
# delta and neither can be the only reader of a row.


def _sr_at(root, run_git, *rows, message=None):
    """Write the SR registry to `rows` and, when `message` is given, commit it."""
    (root / "docs" / "requirements" / "system-requirements.csv").write_text(
        _SPINE_SR_HEADER + "".join(rows), encoding="utf-8"
    )
    run_git("add", "-A")
    if message:
        run_git("commit", "-m", message)


def test_a_status_flip_into_approved_is_read_as_an_approval_act(tmp_path):
    # The shape the ruling names first, and the one the record actually holds:
    # a lane moved four spine rows Drafted -> Approved in its own delta
    # (`580df781`, WI-508 slice 6), and the next review round returned
    # CHANGES-REQUESTED against exactly those flips. Driven over a COMMIT RANGE,
    # because that is where the merge slot asks — the branch tip against the
    # merge base, not the index.
    run_git = _init_spine_repo(tmp_path)
    _sr_at(tmp_path, run_git, _sr_row(status="Drafted"), message="author the row")
    _sr_at(tmp_path, run_git, _sr_row(status="Approved"), message="approve it")
    ar = load_script("acceptance_record")

    acts = ar.staged_approval_acts(tmp_path, "HEAD~1", "HEAD")
    assert [(a["id"], a["act"], a["before"], a["after"]) for a in acts] == [
        ("SR-001", "flip", "Drafted", "Approved")
    ]
    # The amendment reader is SILENT on the same delta — that is the exemption
    # this reader exists to pick up, asserted rather than assumed.
    assert ar.staged_spine_amendments(tmp_path, "HEAD~1", "HEAD") == []


def test_a_row_born_approved_is_read_as_an_approval_act(tmp_path):
    # The second measured shape: four lanes (WI-483, WI-500, WI-501, WI-507)
    # minted rows that ARRIVED `Approved`, skipping the approval brief entirely.
    # There is no Status to have moved, so a flip-only reading would miss every
    # one of them; the row's absence on the base side IS the act.
    run_git = _init_spine_repo(tmp_path)
    born = (
        'SR-002,New req,SN-001,"fresh","why","ac",,C,Test,Approved,1,,hat.MAINTAINER\n'
    )
    _sr_at(tmp_path, run_git, _sr_row(), born, message="mint a born-Approved row")
    ar = load_script("acceptance_record")

    acts = ar.staged_approval_acts(tmp_path, "HEAD~1", "HEAD")
    assert [(a["id"], a["act"], a["after"]) for a in acts] == [
        ("SR-002", "born", "Approved")
    ]


def test_born_and_withdrawn_drafted_rows_reach_first_approval_not_refusal(tmp_path):
    # THE OTHER HALF, which is what makes the rung a rule rather than a ban on
    # touching the spine. A lane may author `Drafted` rows and may WITHDRAW a
    # claim: neither blesses text, so neither owes a snapshot and neither
    # refuses a merge. A reader that reported these would refuse the very work
    # the ruling leaves to the lane.
    run_git = _init_spine_repo(tmp_path)
    drafted = (
        'SR-002,New req,SN-001,"fresh","why","ac",,C,Test,Drafted,1,,hat.MAINTAINER\n'
    )
    _sr_at(
        tmp_path,
        run_git,
        _sr_row(status="Drafted"),  # SR-001 Approved -> Drafted: a de-approval
        drafted,  # SR-002 arrives Drafted: authoring, not approving
        message="author one row, withdraw another",
    )
    ar = load_script("acceptance_record")

    assert ar.staged_approval_acts(tmp_path, "HEAD~1", "HEAD") == []
    # Both resulting Drafted rows are seen by the first-approval reader. The
    # withdrawal blesses nothing and therefore remains absent from the refusal,
    # but it cannot be treated as approval: the adjudicator must re-approve it.
    drafted_rows = ar.staged_drafted_rows(tmp_path, "HEAD~1", "HEAD")
    assert [(r["id"], r["act"], r["changed"]) for r in drafted_rows] == [
        ("SR-001", "amended", {}),
        ("SR-002", "added", {}),
    ]

    # ...and a `Drafted` row whose TEXT then moves DOES reach that surface,
    # which preserves the ordinary below-approval amendment classification.
    _sr_at(
        tmp_path,
        run_git,
        _sr_row("the AMENDED draft text", status="Drafted"),
        drafted,
        message="amend the withdrawn row",
    )
    amended = ar.staged_drafted_rows(tmp_path, "HEAD~1", "HEAD")
    assert [(r["id"], r["act"]) for r in amended] == [("SR-001", "amended")]
    assert "Requirement" in amended[0]["changed"]


def test_the_lane_refusal_names_every_act_and_the_snapshot_write(tmp_path):
    # The refusal a merging lane actually reads. It must be ACTIONABLE — each
    # row id, which registry, which shape of act, and every snapshot file the
    # branch wrote — and it must name the rule and the remedy, because a lane
    # told only "refused" re-runs the same commit.
    run_git = _init_spine_repo(tmp_path)
    _sr_at(tmp_path, run_git, _sr_row(status="Drafted"), message="author the row")
    snap = tmp_path / "docs" / "archive" / "last_approved" / "docs" / "requirements"
    snap.mkdir(parents=True)
    (snap / "system-requirements.csv").write_text(
        _SPINE_SR_HEADER + _sr_row(status="Approved"), encoding="utf-8"
    )
    _sr_at(tmp_path, run_git, _sr_row(status="Approved"), message="approve + anchor")
    ar = load_script("acceptance_record")

    refusal = ar.lane_approval_refusal(tmp_path, "HEAD~1", "HEAD")
    assert refusal is not None
    assert "SR-001 flipped Drafted -> Approved" in refusal
    assert "docs/requirements/system-requirements.csv" in refusal
    assert (
        "wrote docs/archive/last_approved/docs/requirements/system-requirements.csv"
        in refusal
    )
    assert "the approval act is the ADJUDICATOR's" in refusal
    assert "Leave the rows `Drafted`" in refusal  # the remedy, not just the verdict
    # The green half of the same fixture: the AUTHORING commit is admitted.
    assert ar.lane_approval_refusal(tmp_path, "HEAD~2", "HEAD~1") is None


# --- WI-380: the §A5.1 approved-vs-traced cell split ---------------------------
#
# Owner ruling 2026-07-31 (docs/concurrency-v2.md §A5.1): only what is APPROVED
# arms the re-attest warn. Traceability is TRACED, and a traced-only edit must
# stay silent — WI-280 paid four review rounds and a DevStg-Impl->DevStg-Tests gate drop for 19
# `Module` pointers that followed moved code and altered no requirement.

_SPINE_LLR_HEADER = (
    "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,Rationale,TestRefs,"
    "Status,Component,Phase,Hat-Refs\n"
)
_SPINE_TC_HEADER = (
    "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,"
    "Status,Phase\n"
)


def _write_child_registries(root, llr_cells, tc_cells):
    """Write LLR-001 / TC-001 (both `Approved`, both owned by the Approved
    SR-001 of `_init_spine_repo`) from the two cell dicts, so a test states only
    the cells it is varying."""
    llr = dict(
        {
            "LLR-ID": "LLR-001",
            "SR-Refs": "SR-001",
            "Title": "Core",
            "Module": "src/d.py",
            "CodeSymbol": "f",
            "Detail": "the original detail",
            "Rationale": "why",
            "TestRefs": "TC-001",
            "Status": "Approved",
            "Component": "CMP-001",
            "Phase": "1",
            "Hat-Refs": "hat.MAINTAINER",
        },
        **llr_cells,
    )
    tc = dict(
        {
            "TC-ID": "TC-001",
            "Verifies": "SR-001",
            "Level": "Unit",
            "Method": "the original method",
            "Tier": "smoke",
            "Parameters": "n=1",
            "Expected": "the original expectation",
            "Automated": "Y",
            "Evidence": "tests/test_d.py",
            "Status": "Approved",
            "Phase": "1",
        },
        **tc_cells,
    )
    req = root / "docs" / "requirements"
    (req / "low-level-requirements.csv").write_text(
        _SPINE_LLR_HEADER
        + ",".join(llr[k] for k in _SPINE_LLR_HEADER.strip().split(","))
        + "\n",
        encoding="utf-8",
    )
    test_dir = root / "docs" / "test"
    test_dir.mkdir(parents=True, exist_ok=True)
    (test_dir / "test-cases.csv").write_text(
        _SPINE_TC_HEADER
        + ",".join(tc[k] for k in _SPINE_TC_HEADER.strip().split(","))
        + "\n",
        encoding="utf-8",
    )


def _init_full_spine_repo(root):
    """`_init_spine_repo` plus an attested LLR-001 + TC-001 in HEAD."""
    run_git = _init_spine_repo(root)
    _write_child_registries(root, {}, {})
    run_git("add", "-A")
    run_git("commit", "-m", "attested chain")
    return run_git


def test_staged_spine_traced_cells_do_not_arm_the_reattest_warn(tmp_path):
    # THE WI-380 CASE. Every traced cell of all three registries moves at once —
    # the SR's SN-Refs/Phase/Aspect, the LLR's Module/CodeSymbol/TestRefs/
    # Component/Phase (literally the WI-280 shape), the TC's Verifies/Evidence/
    # Automated/Phase — with every approved cell and every Status untouched.
    # Silence is the whole point: before this split each of these armed the warn
    # exactly as if requirement prose had changed (mutation-proof: reverting
    # `spine_cell_class` to "everything but Status is approved" reds this).
    run_git = _init_full_spine_repo(tmp_path)
    (tmp_path / "docs" / "requirements" / "system-requirements.csv").write_text(
        _SPINE_SR_HEADER
        + 'SR-001,Adder,SN-009,"the original attested text","why","ac",,C,'
        "Test,Approved,4,unattended-loop,hat.MAINTAINER\n",
        encoding="utf-8",
    )
    _write_child_registries(
        tmp_path,
        {
            "Module": "src/moved/d.py",
            "CodeSymbol": "renamed_f",
            "TestRefs": "TC-002",
            "Component": "CMP-009",
            "Phase": "4",
        },
        {
            "Verifies": "LLR-001",
            "Evidence": "tests/moved/test_d.py",
            "Automated": "N",
            "Phase": "4",
        },
    )
    run_git("add", "-A")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "re-attest marker" not in proc.stderr


def test_staged_spine_approved_child_cells_still_arm_the_reattest_warn(tmp_path):
    # The complement, so the narrowing cannot be mistaken for a disabling: the
    # LLR's `Detail`/`Rationale` and the TC's `Method`/`Expected` are approved,
    # and amending them with the owning SR left Approved still warns per row.
    run_git = _init_full_spine_repo(tmp_path)
    _write_child_registries(
        tmp_path,
        {"Detail": "the AMENDED detail", "Rationale": "a different why"},
        {"Method": "a different method", "Expected": "a different expectation"},
    )
    run_git("add", "-A")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "LLR-001: approved cell(s) Detail, Rationale amended" in proc.stderr
    assert "TC-001: approved cell(s) Expected, Method amended" in proc.stderr


def test_staged_spine_unknown_column_falls_to_approved(tmp_path):
    # THE FAIL-SAFE. A column in NEITHER §A5.1 list — one added to a registry
    # after the ruling was written — must arm the warn, not fall through it: a
    # spurious window is seen and dismissed, a missed window is seen by nobody.
    # This is the direction an allowlist-only design would have gotten wrong.
    run_git = _init_spine_repo(tmp_path)
    (tmp_path / "docs" / "requirements" / "system-requirements.csv").write_text(
        _SPINE_SR_HEADER.rstrip("\n")
        + ",Novelty\n"
        + _sr_row().rstrip("\n")
        + ",the NEW cell\n",
        encoding="utf-8",
    )
    run_git("add", "-A")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SR-001: approved cell(s) Novelty amended" in proc.stderr


def test_spine_cell_split_classifies_every_shipped_column():
    # The other half of the fail-safe, and the one that keeps it HONEST: the
    # residual is silent by construction, so a new column could ride in on it
    # unnoticed forever. This pins that it cannot — every column of this repo's
    # live registries AND of the blank forms the kit ships must be classified
    # explicitly, or ruled out as the id/Status key. Adding a column to a
    # registry therefore fails HERE, at the ruling, rather than quietly.
    # The COLUMN SET comes from the carrier now, not from a header line: under
    # TOML `csv.reader` would hand back `['[requirement.SR-001]']` and the check
    # would pass having classified nothing. `spine_carrier.columns` answers the
    # same question for whichever carrier is live.
    ct = load_script("check_trajectory")
    carrier = load_script("spine_carrier")
    surfaces = []
    for rel, id_col in ct.SPINE_CSVS:
        surfaces.append((rel, id_col, ROOT / rel))
        surfaces.append(
            (
                rel,
                id_col,
                ROOT
                / "project-trajectory"
                / "registries"
                / os.path.basename(rel).replace(".toml", ".template.toml"),
            )
        )
    for rel, id_col, path in surfaces:
        assert path.is_file(), path
        columns = carrier.columns(path, id_col)
        assert columns, path  # an empty column set would classify nothing
        unclassified = {c for c in columns if c not in (id_col, "Status")}
        # Asked through the PUBLIC RULE rather than by indexing the tables: the
        # tables are keyed by a path that carries a carrier suffix, and the rule
        # is what every caller actually goes through.
        unclassified = {
            c
            for c in unclassified
            if c
            not in set(ct.SPINE_APPROVED_CELLS[rel]) | set(ct.SPINE_TRACED_CELLS[rel])
        }
        assert not unclassified, (
            "{}: column(s) {} are classified by NEITHER half of the §A5.1 split "
            "in check_trajectory.py — rule them approved or traced".format(
                path, sorted(unclassified)
            )
        )
    # And the two halves must not overlap: a cell cannot be both.
    for rel, _ in ct.SPINE_CSVS:
        assert not (
            set(ct.SPINE_APPROVED_CELLS[rel]) & set(ct.SPINE_TRACED_CELLS[rel])
        ), rel


def test_the_two_wi388_cell_rulings_are_recorded_in_the_split():
    # WI-388's intake from WI-380 REVIEW-A finding 3: the two live cells §A5.1
    # does not name, RULED at WI-388 rather than left to the residual.
    #   * LLR `SR-Refs` -> TRACED, routed to adjudication like its two pointer
    #     siblings (`SN-Refs`, `Verifies`): re-pointing which SR owns a
    #     decomposition row changes no attested prose on either side, and
    #     whether the re-point moved scope is exactly adjudication's judgement.
    #   * SR `SupersededBy` -> APPROVED. That half is now VACUOUS by a later
    #     ruling: the SR-tier column retired with the supersession tombstone
    #     class (D-4, 2026-08-14b), so there is no cell left to classify. The
    #     LLR `SR-Refs` half below is the live half, and it is the one this
    #     re-tier leans on hardest — 83 rows were re-pointed at new owning SRs
    #     under exactly the traced/adjudication routing it pins.
    # Asked through `spine_cell_class`, the rule every caller goes through, and
    # asked under BOTH carrier suffixes: the tables are keyed by a path that
    # carries one, and a lookup miss reads `approved` — which would silently
    # re-arm the window WI-388 ruled these cells out of. The CMP registry's own
    # `SupersededBy` is a separate rule and is unaffected.
    ct = load_script("check_trajectory")
    for suffix in (".csv", ".toml"):
        llr = "docs/requirements/low-level-requirements" + suffix
        sr = "docs/requirements/system-requirements" + suffix
        assert ct.spine_cell_class(llr, "SR-Refs") == "traced", suffix
        assert ct.spine_cell_class(sr, "SN-Refs") == "traced", suffix
    llr = "docs/requirements/low-level-requirements.toml"
    sr = "docs/requirements/system-requirements.toml"
    assert "SR-Refs" in ct.SPINE_TRACED_CELLS[llr]
    assert "SR-Refs" not in ct.SPINE_APPROVED_CELLS[llr]
    # The retired SR-tier column is absent from BOTH halves — not silently
    # re-classified into one of them.
    assert "SupersededBy" not in ct.SPINE_APPROVED_CELLS[sr]
    assert "SupersededBy" not in ct.SPINE_TRACED_CELLS[sr]


def test_staged_llr_sr_refs_repoint_is_traced_not_a_reattest_warn(tmp_path):
    # The ruled behaviour, driven: an LLR re-pointed at a different owning SR
    # stays SILENT at the amend-without-flip warn (traced, per the WI-388
    # ruling above) but does NOT vanish — the amendment record carries it in
    # the traced half, which is where the intake mint routes it (§A5.1: a
    # changed pointer routes to adjudication, never straight to a window).
    run_git = _init_full_spine_repo(tmp_path)
    _write_child_registries(tmp_path, {"SR-Refs": "SR-002"}, {})
    run_git("add", "-A")
    ct = load_script("check_trajectory")
    assert ct.staged_spine_findings(tmp_path) == []
    amendments = ct.staged_spine_amendments(tmp_path)
    llr_records = [a for a in amendments if a["id"] == "LLR-001"]
    assert len(llr_records) == 1
    assert llr_records[0]["approved"] == {}
    assert llr_records[0]["traced"] == {"SR-Refs": ("SR-001", "SR-002")}


def test_staged_spine_amendments_expose_the_traced_half_for_adjudication(tmp_path):
    # The SEAM WI-388 consumes. The warn is silent on a traced-only edit, but
    # the change must not VANISH — adjudication is what decides whether a
    # re-pointed SN-Refs moved scope, and it needs the row, the cell and the
    # before/after. Asserts the structured return directly, in-process.
    run_git = _init_spine_repo(tmp_path)
    (tmp_path / "docs" / "requirements" / "system-requirements.csv").write_text(
        _SPINE_SR_HEADER + _sr_row().replace("SN-001", "SN-009"), encoding="utf-8"
    )
    run_git("add", "-A")
    ct = load_script("check_trajectory")
    amendments = ct.staged_spine_amendments(tmp_path)
    assert [(a["registry"], a["id"]) for a in amendments] == [
        ("docs/requirements/system-requirements.csv", "SR-001")
    ]
    assert amendments[0]["approved"] == {}
    assert amendments[0]["traced"] == {"SN-Refs": ("SN-001", "SN-009")}
    assert ct.staged_spine_findings(tmp_path) == []


def test_staged_spine_amendments_read_a_commit_range_not_only_the_index(tmp_path):
    # REVIEW-A finding 2. The seam's RECORD was consumable but its SCAN was not
    # callable where §A5.2 puts the trigger: adjudication is minted from a trunk
    # COMMIT, and the scan was index-vs-HEAD, so once the change was committed
    # the same call returned [] and WI-388's dispatcher would have got nothing.
    # Driven both sides of the commit: the default (index) view correctly goes
    # quiet once nothing is staged, and the rev-range view answers.
    run_git = _init_spine_repo(tmp_path)
    (tmp_path / "docs" / "requirements" / "system-requirements.csv").write_text(
        _SPINE_SR_HEADER + _sr_row().replace("SN-001", "SN-009"), encoding="utf-8"
    )
    run_git("add", "-A")
    run_git("commit", "-m", "re-point SN-Refs")
    ct = load_script("check_trajectory")

    assert ct.staged_spine_amendments(tmp_path) == []  # nothing staged, by design
    ranged = ct.staged_spine_amendments(tmp_path, "HEAD~1", "HEAD")
    assert [(a["registry"], a["id"]) for a in ranged] == [
        ("docs/requirements/system-requirements.csv", "SR-001")
    ]
    assert ranged[0]["approved"] == {}
    assert ranged[0]["traced"] == {"SN-Refs": ("SN-001", "SN-009")}

    # The approved half survives the same trip — a rev range is not a second,
    # weaker scan: it is the same rules read against two commits.
    (tmp_path / "docs" / "requirements" / "system-requirements.csv").write_text(
        _SPINE_SR_HEADER + _sr_row("the AMENDED text", "Approved"), encoding="utf-8"
    )
    run_git("add", "-A")
    run_git("commit", "-m", "amend the Requirement")
    ranged2 = ct.staged_spine_amendments(tmp_path, "HEAD~1", "HEAD")
    assert list(ranged2[0]["approved"]) == ["Requirement"]


# --- WI-484 phase 5: the Hat-Refs arm (OI-33's surviving residue) --------------
#
# A row whose APPROVED cells move while its `Hat-Refs` cell does not has been
# amended without re-examining which perspectives bear on it — and the component
# and knowledge views are DERIVED from that cell, so the derived artifact stays
# perfectly fresh while answering from the old lenses. Warn-first, same home and
# same amendment set as the WI-316 guard, comparison by CELL CLASS.


def test_amending_approved_cells_without_moving_hat_refs_warns(tmp_path):
    # The fire case. `Requirement` moves, `Hat-Refs` does not.
    run_git = _init_spine_repo(tmp_path)
    _amend_sr(tmp_path, "the AMENDED text", "Approved")
    run_git("add", "-A")
    ct = load_script("check_trajectory")
    found = ct.staged_hat_refs_findings(tmp_path)
    assert len(found) == 1, found
    assert "SR-001: approved cell(s) Requirement amended while Hat-Refs" in found[0]
    # Both arms of the guard fire on this row — the second arm is an ADDITION,
    # not a re-spelling of the first.
    assert ct.staged_spine_findings(tmp_path)
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "perspective record did not" in proc.stderr


def test_hat_refs_arm_is_silent_when_only_traced_cells_move(tmp_path):
    # THE REGRESSION CASE, and it is a MEASURED one: WI-484's phase-2 backfill
    # wrote `Hat-Refs` on 55 SR rows and raised seven warns on a neighbouring
    # check that blames the registry by LINE, because a blame time cannot tell
    # an approved cell from a traced one. This arm must be silent on exactly
    # that edit — writing the informative cell itself, and any other traced-only
    # move — or it would re-create the defect it was designed against.
    run_git = _init_spine_repo(tmp_path)
    (tmp_path / "docs" / "requirements" / "system-requirements.csv").write_text(
        _SPINE_SR_HEADER + _sr_row(hats="hat.MAINTAINER;hat.SECURITY"),
        encoding="utf-8",
    )
    run_git("add", "-A")
    ct = load_script("check_trajectory")
    assert ct.staged_hat_refs_findings(tmp_path) == []
    assert ct.staged_spine_findings(tmp_path) == []
    # ...and the same for a traced cell that is NOT Hat-Refs: an SN-Refs
    # re-point moves no approved cell, so there is no substance to have
    # outrun the perspective record.
    (tmp_path / "docs" / "requirements" / "system-requirements.csv").write_text(
        _SPINE_SR_HEADER + _sr_row().replace("SN-001", "SN-009"), encoding="utf-8"
    )
    run_git("add", "-A")
    assert ct.staged_hat_refs_findings(tmp_path) == []


def test_hat_refs_arm_is_silent_when_the_cell_moves_with_the_amendment(tmp_path):
    # The discharged case: substance and perspective record move together, which
    # is the behaviour the warn asks for. The WI-316 arm still fires (the prose
    # amendment still owes a human read) — the two arms answer different
    # questions and must not be collapsed.
    run_git = _init_spine_repo(tmp_path)
    (tmp_path / "docs" / "requirements" / "system-requirements.csv").write_text(
        _SPINE_SR_HEADER + _sr_row("the AMENDED text", "Approved", "hat.SECURITY"),
        encoding="utf-8",
    )
    run_git("add", "-A")
    ct = load_script("check_trajectory")
    assert ct.staged_hat_refs_findings(tmp_path) == []
    assert ct.staged_spine_findings(tmp_path)


def test_hat_refs_arm_is_vacuous_where_a_row_has_no_baseline(tmp_path):
    # HONEST VACUITY, both shapes, inherited from the amendment set rather than
    # re-litigated: a row minted in this very commit has nothing to compare, and
    # a row below approval has blessed nothing to amend behind a human's back.
    # Neither is coverage, and neither is a hole this arm can close.
    run_git = _init_spine_repo(tmp_path)
    csv_path = tmp_path / "docs" / "requirements" / "system-requirements.csv"
    csv_path.write_text(
        _SPINE_SR_HEADER
        + _sr_row()
        + 'SR-002,New req,SN-001,"fresh","why","ac",,C,Test,Approved,1,,\n',
        encoding="utf-8",
    )
    run_git("add", "-A")
    ct = load_script("check_trajectory")
    assert ct.staged_hat_refs_findings(tmp_path) == []  # no baseline: not guarded

    # A Drafted row amended under Drafted: below approval on both sides.
    run_git("commit", "-m", "mint SR-002")
    csv_path.write_text(
        _SPINE_SR_HEADER
        + _sr_row()
        + 'SR-002,New req,SN-001,"rewritten","why","ac",,C,Test,Drafted,1,,\n',
        encoding="utf-8",
    )
    run_git("add", "-A")
    assert [f for f in ct.staged_hat_refs_findings(tmp_path) if "SR-002" in f] == []


def test_hat_refs_arm_is_silent_on_a_tier_that_carries_no_such_column(tmp_path):
    # STRUCTURAL SCOPE, not an allowlist. `Hat-Refs` is classified at the SR and
    # LLR tiers; the TC tier has no such column, and an absent column classes
    # `approved` under the fail-safe residual — so without this scoping every
    # amended test case would warn about a cell its registry does not have.
    # Driven in one commit against an LLR that DOES fire, so the test cannot
    # pass by the arm being silent everywhere.
    run_git = _init_full_spine_repo(tmp_path)
    _write_child_registries(
        tmp_path,
        {"Detail": "the AMENDED detail"},
        {"Method": "a different method"},
    )
    run_git("add", "-A")
    ct = load_script("check_trajectory")
    found = ct.staged_hat_refs_findings(tmp_path)
    assert [f.split(":")[0] for f in found] == ["LLR-001"], found


# --- the carrier cutover ------------------------------------------------------
# The spine moves from CSV to TOML. Every check below reads a registry through
# `git show`, so each one has a revision where the live carrier does not exist.
# These drive the hazard rather than assert around it.


def _cutover(root, run_git, message="cut the carrier over to TOML"):
    """Convert the repo's spine to TOML and commit the swap the way the real
    cutover must land it: the `.toml` written and the `.csv` DELETED together,
    in ONE commit. Two homes for one fact is the thing the kit forbids, and a
    two-commit cutover would leave a revision where both are authoritative."""
    migrate_carrier = load_script("migrate_carrier")
    findings, written = migrate_carrier.convert(root, write=True)
    assert findings == [], findings
    for path in written:
        legacy_csv = path.with_suffix(".csv")
        if legacy_csv.exists():
            legacy_csv.unlink()
    run_git("add", "-A")
    run_git("commit", "-m", message)
    return written


def test_the_cutover_commit_is_checked_by_the_amendment_guard_not_exempt_from_it(
    tmp_path,
):
    # Because each side resolves its carrier independently, a diff ACROSS the
    # cutover reads CSV on the old side and TOML on the new one and compares
    # cells. A lossless cutover is therefore SILENT here - and that silence is
    # evidence, produced by a guard that would have spoken, rather than the
    # guard being blind to the one commit that rewrites every row it watches.
    run_git = _init_spine_repo(tmp_path)
    ct = load_script("check_trajectory")
    _cutover(tmp_path, run_git)
    assert ct.staged_spine_amendments(tmp_path, "HEAD~1", "HEAD") == []


def test_text_smuggled_into_the_cutover_commit_is_caught(tmp_path):
    # The mutation that proves the silence above is not vacuous. Same cutover,
    # with one approved cell quietly rewritten in the same commit - the exact
    # shape a carrier migration invites, because 400-odd rows all change at once
    # and no reviewer diffs them by eye. The guard names the row and the cell.
    run_git = _init_spine_repo(tmp_path)
    ct = load_script("check_trajectory")
    migrate_carrier = load_script("migrate_carrier")
    findings, written = migrate_carrier.convert(tmp_path, write=True)
    assert findings == []
    toml_path = next(p for p in written if p.name.startswith("system-requirements"))
    toml_path.write_text(
        toml_path.read_text(encoding="utf-8").replace(
            "the original attested text", "text nobody agreed to"
        ),
        encoding="utf-8",
    )
    (tmp_path / "docs" / "requirements" / "system-requirements.csv").unlink()
    run_git("add", "-A")
    run_git("commit", "-m", "cut the carrier over to TOML")

    amendments = ct.staged_spine_amendments(tmp_path, "HEAD~1", "HEAD")
    # The record names the row's NEW home — the cutover commit touches both
    # carrier paths (it deletes one and adds the other), and the file a reader
    # can open afterwards is the TOML one. What the check is FOR is the pair
    # below: the smuggled cell, named, with both sides of the change.
    assert [(a["registry"], a["id"]) for a in amendments] == [
        ("docs/requirements/system-requirements.toml", "SR-001")
    ]
    assert amendments[0]["approved"] == {
        "Requirement": ("the original attested text", "text nobody agreed to")
    }


# --- WI-068: the critique-loop ratchet (--staged, warn-first) ------------------

CRITIQUE_SR_ROW = (
    'SR-050,Render realism,SN-001,"The render shall look realistic.",'
    '"Subjective.","Judged against docs/rubrics/render.md.",,S,Critique,Approved\n'
)


def _init_critique_close_repo(tmp_path, verdict="CHANGES-REQUESTED findings=2"):
    """A git repo with a Verification=Critique SR-050, a committed CRITIQUE verdict
    file, and WI-050 (on SR-050) closed queued->done in the working tree."""
    skip_without_env_gates("git")
    git = shutil.which("git")

    def run_git(*a):
        return subprocess.run(
            [git, "-C", str(tmp_path), *a], capture_output=True, text=True
        )

    run_git("init")
    pin_autocrlf(tmp_path)  # WI-461/WI-465; see conftest.pin_autocrlf
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "system-requirements.csv").write_text(SR_HEADER + CRITIQUE_SR_ROW, "utf-8")
    reviews = tmp_path / "docs" / "reviews"
    reviews.mkdir(parents=True, exist_ok=True)
    (reviews / "001-CRITIQUE.md").write_text(
        "- [MAJOR] render.png -> B1 seam artifact at the mesh join -> reseat -> @owner\n"
        "VERDICT: " + verdict + "\n",
        encoding="utf-8",
    )
    write_wis_sr(
        tmp_path, "WI-050,Render,scripts,SR-050,,active,,docs/specs/WI-050.md\n"
    )
    run_git("add", "-A")
    run_git("commit", "-m", "init")
    # Close WI-050 (the Critique WI) in the working tree.
    write_wis_sr(tmp_path, "WI-050,Render,scripts,SR-050,,done,shipped the render,\n")
    return run_git


def test_critique_ratchet_warns_and_holds(tmp_path):
    # Closing a Critique WI while the latest CRITIQUE verdict is CHANGES-REQUESTED,
    # touching neither the TC registry, the tests dir, nor a docs/rubrics/ file ->
    # warn (the fix landed in the artifact, not the chain).
    run_git = _init_critique_close_repo(tmp_path)
    run_git("add", "docs/work")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "latest CRITIQUE verdict is CHANGES-REQUESTED" in proc.stderr
    assert "WI-050" in proc.stderr
    # Add a rubric anchor (touch docs/rubrics/) -> the chain changed -> HOLDS.
    (tmp_path / "docs" / "rubrics").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "rubrics" / "render.md").write_text(
        "# render\n- B2 a newly-found failure mode\n", encoding="utf-8"
    )
    run_git("add", "docs/work", "docs/rubrics/render.md")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "latest CRITIQUE verdict" not in proc.stderr


def test_critique_ratchet_silent_when_verdict_approves(tmp_path):
    # The latest CRITIQUE verdict is APPROVE -> no warn even with no chain delta.
    run_git = _init_critique_close_repo(tmp_path, verdict="APPROVE findings=0")
    run_git("add", "docs/work")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "latest CRITIQUE verdict" not in proc.stderr


# --- WI-205: the backlog-staleness warn (warn-only, git-driven, silent off-git)
# An open WI whose cited SR row or SpecRef target was amended AFTER the WI row was
# last touched is re-flagged for a driven re-validation. Fixtures pin commit times
# via GIT_*_DATE so the strictly-newer compare is deterministic (two commits in the
# same wall-clock second would otherwise tie and never warn).

SR_ROW_V1 = 'SR-001,Feature SR,SN-001,"The system shall do X.",R,AC,,M,Test,Drafted\n'
SR_ROW_V2 = (
    'SR-001,Feature SR,SN-001,"The system shall do X and Y.",R,AC,,M,Test,Drafted\n'
)


def _write_sr_row(root, row):
    """Write a system-requirements.csv carrying a single raw SR row."""
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "system-requirements.csv").write_text(SR_HEADER + row, encoding="utf-8")


def _staleness_git(tmp_path):
    """A git runner whose commits can be stamped at a chosen epoch (`at=`), so the
    committer-time compare the staleness check reads is deterministic."""
    skip_without_env_gates("git")
    git = shutil.which("git")
    base = dict(os.environ)

    def run_git(*a, at=None):
        env = base
        if at is not None:
            env = dict(base)
            stamp = "@{} +0000".format(at)
            env["GIT_AUTHOR_DATE"] = stamp
            env["GIT_COMMITTER_DATE"] = stamp
        return subprocess.run(
            [git, "-C", str(tmp_path), *a], capture_output=True, text=True, env=env
        )

    run_git("init")
    pin_autocrlf(tmp_path)  # WI-461/WI-465; see conftest.pin_autocrlf
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    return run_git


def _init_amended_sr_repo(tmp_path, status="active"):
    """A git repo where WI-001 (given status) cites SR-001, both committed at
    t=1000, then SR-001's row text is amended at t=2000 — the SR row is strictly
    newer than the WI row (the staleness precondition)."""
    run_git = _staleness_git(tmp_path)
    _write_sr_row(tmp_path, SR_ROW_V1)
    write_wis_sr(
        tmp_path,
        "WI-001,Feature,scripts,SR-001,,{},,docs/specs/WI-001.md\n".format(status),
    )
    write_spec(tmp_path, "docs/specs/WI-001.md")
    run_git("add", "-A")
    run_git("commit", "-m", "init", at=1000)
    # A real active lane carries its branch ref; cut it so the WI-553 hold-by-
    # rename detector stays silent (a ref-less active claim is the banned hold).
    if status == "active":
        run_git("branch", ACTIVE_BRANCH, "HEAD")
    _write_sr_row(tmp_path, SR_ROW_V2)
    run_git("add", "-A")
    run_git("commit", "-m", "amend SR-001", at=2000)
    return run_git


def test_backlog_staleness_amended_sr_warns(tmp_path):
    # A cited SR amended after the WI row was filed -> the WI is re-flagged.
    _init_amended_sr_repo(tmp_path)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WI-001: cites SR-001 amended after the WI row was last touched" in (
        proc.stderr
    )


def _reaffirm_spec(root, wid, note):
    """Re-affirm one work item the folder-registry way: a reviewed edit to its
    OWN spec text, FILENAME unchanged.

    The filename is the subtlety this fixture has to respect. The Title drives
    it, so editing the Title RENAMES the file — and a rename is exactly what
    `_path_commit_time(row_history=True)` filters out on purpose, so that a
    status MOVE cannot re-date a row nobody re-validated. The re-affirmation
    therefore rides in the frontmatter as a dated comment: a real content edit,
    at the same path, changing no cell."""
    (spec,) = (root / "docs" / "work").rglob(wid + "-*.md")
    spec.write_text(
        spec.read_text(encoding="utf-8").replace(
            "+++\n", "+++\n# {}\n".format(note), 1
        ),
        encoding="utf-8",
        newline="\n",
    )


def test_backlog_staleness_wi_touched_after_amend_is_quiet(tmp_path):
    # Re-affirming (any reviewed edit to the WI row, here at t=3000, after the SR
    # amendment) re-dates it and clears the warn.
    run_git = _init_amended_sr_repo(tmp_path)
    _reaffirm_spec(tmp_path, "WI-001", "re-affirmed 2026-07-17")
    run_git("add", "-A")
    run_git("commit", "-m", "re-affirm WI-001", at=3000)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "amended after the WI row" not in proc.stderr


def test_backlog_staleness_specref_edit_warns(tmp_path):
    # The SpecRef target edited after the WI row was last touched -> re-flagged.
    run_git = _staleness_git(tmp_path)
    _write_sr_row(tmp_path, SR_ROW_V1)
    write_wis_sr(
        tmp_path, "WI-001,Feature,scripts,SR-001,,active,,docs/specs/WI-001.md\n"
    )
    write_spec(tmp_path, "docs/specs/WI-001.md")
    run_git("add", "-A")
    run_git("commit", "-m", "init", at=1000)
    (tmp_path / "docs" / "specs" / "WI-001.md").write_text(
        "# spec v2\n", encoding="utf-8"
    )
    run_git("add", "-A")
    run_git("commit", "-m", "edit spec", at=2000)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (
        "WI-001: its SpecRef docs/specs/WI-001.md changed after the WI row"
        in proc.stderr
    )
    assert "amended after the WI row" not in proc.stderr


def test_backlog_staleness_off_git_is_silent(tmp_path):
    # No git repo -> no blame basis -> no warn, no crash (best-effort off-git).
    _write_sr_row(tmp_path, SR_ROW_V2)
    write_wis_sr(
        tmp_path, "WI-001,Feature,scripts,SR-001,,active,,docs/specs/WI-001.md\n"
    )
    write_spec(tmp_path, "docs/specs/WI-001.md")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "amended after the WI row" not in proc.stderr
    assert "changed after the WI row" not in proc.stderr


def test_backlog_staleness_deferred_is_exempt(tmp_path):
    # A deferred WI citing an amended SR is EXEMPT (it re-enters via an owner
    # un-defer, itself the driven look) -> no warn.
    _init_amended_sr_repo(tmp_path, status="deferred")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "amended after the WI row" not in proc.stderr


def test_backlog_staleness_never_errors_under_strict(tmp_path):
    # The warn stays warn-only even under --strict (exit 0 with the finding).
    _init_amended_sr_repo(tmp_path)
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WI-001: cites SR-001 amended after the WI row was last touched" in (
        proc.stderr
    )


# --- WI-243: the perceptual re-fire warn (git-time staleness, warn-first) -------


def _init_critique_staleness_repo(
    tmp_path, ev_at=1000, render_at=2000, verdict="APPROVE findings=0"
):
    """A git repo with a Verification=Critique SR-050, a CRITIQUE evidence file
    committed at `ev_at`, a done WI-050 (so the full check reaches the perceptual
    warn, past the no-work-items early return), and a render-surface file
    `scripts/gen_trajectory.py` committed at `render_at`. `render_at > ev_at` is
    the staleness precondition. The checker locates the generator via its
    `scripts/gen_trajectory.py` fallback (its `__file__`-co-located primary path
    is the real repo tree, not under tmp_path)."""
    run_git = _staleness_git(tmp_path)
    _write_sr_row(tmp_path, CRITIQUE_SR_ROW)
    reviews = tmp_path / "docs" / "reviews"
    reviews.mkdir(parents=True, exist_ok=True)
    (reviews / "001-CRITIQUE.md").write_text(
        "VERDICT: " + verdict + "\n", encoding="utf-8"
    )
    write_wis_sr(tmp_path, "WI-050,Render,scripts,SR-050,,done,shipped,\n")
    run_git("add", "-A")
    run_git("commit", "-m", "init", at=ev_at)
    scripts = tmp_path / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    (scripts / "gen_trajectory.py").write_text(
        "# dashboard generator\n", encoding="utf-8"
    )
    run_git("add", "-A")
    run_git("commit", "-m", "touch render surface", at=render_at)
    return run_git


def test_critique_staleness_warns_at_commit_bar_when_render_surface_newer(tmp_path):
    # The render surface changed after the latest CRITIQUE -> the perceptual stamp
    # is stale. At the commit bar (non-strict) it is a WARN, not an error (exit 0).
    _init_critique_staleness_repo(tmp_path)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "perceptual-stale SR-050" in proc.stderr
    assert "scripts/gen_trajectory.py" in proc.stderr


def test_critique_staleness_quiet_when_evidence_is_newer(tmp_path):
    # A fresh critique (evidence committed AFTER the render change) re-dates the
    # evidence and clears the warn.
    _init_critique_staleness_repo(tmp_path, ev_at=2000, render_at=1000)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "perceptual-stale" not in proc.stderr


def test_critique_staleness_off_git_is_silent(tmp_path):
    # No git repo -> no commit-time basis -> no warn, no crash (best-effort).
    _write_sr_row(tmp_path, CRITIQUE_SR_ROW)
    reviews = tmp_path / "docs" / "reviews"
    reviews.mkdir(parents=True, exist_ok=True)
    (reviews / "001-CRITIQUE.md").write_text(
        "VERDICT: APPROVE findings=0\n", encoding="utf-8"
    )
    write_wis_sr(tmp_path, "WI-050,Render,scripts,SR-050,,done,shipped,\n")
    (tmp_path / "scripts").mkdir(parents=True, exist_ok=True)
    (tmp_path / "scripts" / "gen_trajectory.py").write_text("# gen\n", encoding="utf-8")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "perceptual-stale" not in proc.stderr


def test_critique_staleness_vacuous_without_a_critique_sr(tmp_path):
    # A non-Critique SR pays nothing, even with a newer render surface.
    run_git = _staleness_git(tmp_path)
    _write_sr_row(tmp_path, SR_ROW_V1)  # Verification=Test
    reviews = tmp_path / "docs" / "reviews"
    reviews.mkdir(parents=True, exist_ok=True)
    (reviews / "001-CRITIQUE.md").write_text(
        "VERDICT: APPROVE findings=0\n", encoding="utf-8"
    )
    write_wis_sr(tmp_path, "WI-001,Feature,scripts,SR-001,,done,shipped,\n")
    run_git("add", "-A")
    run_git("commit", "-m", "init", at=1000)
    (tmp_path / "scripts").mkdir(parents=True, exist_ok=True)
    (tmp_path / "scripts" / "gen_trajectory.py").write_text("# gen\n", encoding="utf-8")
    run_git("add", "-A")
    run_git("commit", "-m", "render", at=2000)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "perceptual-stale" not in proc.stderr


def test_critique_staleness_fails_closed_under_strict(tmp_path):
    # FAIL-CLOSED (WI-243, owner 2026-07-20): under --strict (the DevStg-Impl gate) a stale
    # render surface is an ERROR (exit 1), not just a warn — it cannot reach green.
    _init_critique_staleness_repo(tmp_path)
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "ERROR - perceptual-stale SR-050" in proc.stderr


# --- concurrency-restructure §5.4: critique selection is by TIME, not by name ---
#
# Flat review artifacts leave the serial `NNN-CRITIQUE.md` counter (a next-number
# race under concurrency) for branch-scoped `WI-<n>-CRITIQUE.md`. Both generations
# live in `docs/reviews/` and do not sort against each other, so
# `_latest_critique_file` picks the newest by git commit time, falling back to
# mtime off git and to the filename (greatest wins) on a tie.


def _write_critiques(root, *named_at):
    """Write `docs/reviews/<name>` verdict files, stamping each at a chosen mtime
    epoch — the off-git rung of the selection ladder, made deterministic."""
    reviews = root / "docs" / "reviews"
    reviews.mkdir(parents=True, exist_ok=True)
    for name, when in named_at:
        path = reviews / name
        path.write_text("VERDICT: APPROVE findings=0\n", encoding="utf-8")
        os.utime(path, (when, when))
    return reviews


def test_latest_critique_picks_newer_wi_scoped_name_off_git(tmp_path):
    # Mixed generations, no git: the branch-scoped file is the newer one -> wins
    # (the legacy name sorts ABOVE it lexicographically, so name order would lose).
    ct = load_script("check_trajectory")
    _write_critiques(tmp_path, ("123-CRITIQUE.md", 1000), ("WI-45-CRITIQUE.md", 2000))
    assert ct._latest_critique_file(tmp_path).name == "WI-45-CRITIQUE.md"


def test_latest_critique_picks_legacy_name_when_it_is_the_newer_one(tmp_path):
    # The reverse ordering: the rule is time, not name SHAPE — a legacy numbered
    # critique still wins while it is the freshest evidence.
    ct = load_script("check_trajectory")
    _write_critiques(tmp_path, ("123-CRITIQUE.md", 2000), ("WI-45-CRITIQUE.md", 1000))
    assert ct._latest_critique_file(tmp_path).name == "123-CRITIQUE.md"


def test_latest_critique_reads_git_time_not_filename_order(tmp_path):
    # The case the old highest-number rule got WRONG: the LOWER-named critique is
    # committed LATER, so it is the live verdict. Both files carry the SAME mtime,
    # so only the git rung can tell them apart (mtime would tie, and the name
    # tie-break would then pick the stale 900-).
    ct = load_script("check_trajectory")
    run_git = _staleness_git(tmp_path)
    _write_critiques(tmp_path, ("900-CRITIQUE.md", 1000))
    run_git("add", "-A")
    run_git("commit", "-m", "the old high-numbered critique", at=1000)
    _write_critiques(tmp_path, ("100-CRITIQUE.md", 1000))
    run_git("add", "-A")
    run_git("commit", "-m", "a fresh low-numbered critique", at=2000)
    assert ct._latest_critique_file(tmp_path).name == "100-CRITIQUE.md"


def test_latest_critique_tie_breaks_deterministically_on_name(tmp_path):
    # Equal times (the ordinary batch: two critiques in one commit) still select
    # ONE file — the greatest filename — and the same one on every call.
    ct = load_script("check_trajectory")
    _write_critiques(tmp_path, ("WI-45-CRITIQUE.md", 1500), ("WI-46-CRITIQUE.md", 1500))
    picked = {ct._latest_critique_file(tmp_path).name for _ in range(3)}
    assert picked == {"WI-46-CRITIQUE.md"}


# --- WI-280: the dashboard render SURFACE is the whole generator family ---------


def test_render_surface_covers_the_whole_generator_family():
    """`_render_surface_paths` feeds the render-critique-staleness warn: a
    `Verification=Critique` SR whose judged render surface changed after the
    verdict must re-fire. WI-280 split every EMITTER out of gen_trajectory.py
    into HTML emitter modules, so a facade-only surface would leave that warn
    running and always passing — the exact silent-green shape the warn exists
    to prevent. This pins the family, both because the change was unguarded
    (round-1 review, MINOR) and because the failure mode is invisible: nothing
    else goes red when the surface silently narrows."""
    ct = load_script("check_trajectory")
    paths = ct._render_surface_paths(ROOT)
    assert paths, "vacuous — the surface resolved to nothing"

    scripts_rel = "project-trajectory/scripts/"
    for name in RENDER_SHARED:
        assert scripts_rel + name in paths, (name, paths)
    # Every HTML emitter in the rendering package must be watched.
    siblings = sorted(
        p.name
        for p in (ROOT / "project-trajectory" / "scripts" / "rendering").glob("*.py")
        if p.name != "__init__.py"
    )
    assert siblings, "premise gone: no rendering emitters to watch"
    for name in siblings:
        assert scripts_rel + "rendering/" + name in paths, (name, paths)
    # Deterministic order, so the emitted warn text is stable.
    assert paths == sorted(dict.fromkeys(paths)) or paths[0].endswith(
        "gen_trajectory.py"
    ), paths


def test_render_surface_fallback_arm_finds_both_scaffold_homes(tmp_path):
    """The `except ValueError` arm — the checker is not under `root` (a
    downstream tool pointing at another repo). Both scaffold layouts resolve:
    the kit's own `project-trajectory/scripts/` and a bootstrapped repo's bare
    `scripts/`. Driven with a synthetic root so the real tree cannot mask a
    regression."""
    ct = load_script("check_trajectory")
    for home in ("project-trajectory/scripts", "scripts"):
        root = tmp_path / home.replace("/", "_")
        d = root / home
        d.mkdir(parents=True)
        for name in RENDER_SHARED:
            (d / name).write_text("", encoding="utf-8")
        package = d / "rendering"
        package.mkdir()
        for name in ("__init__.py", "traj_graph.py", "traj_render.py"):
            (package / name).write_text("", encoding="utf-8")
        paths = ct._render_surface_paths(root)
        for name in RENDER_SHARED:
            assert home + "/" + name in paths, (name, paths)
        assert home + "/rendering/traj_graph.py" in paths, (home, paths)
        assert home + "/rendering/traj_render.py" in paths, (home, paths)
