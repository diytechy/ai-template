"""gen_trajectory.py — the source loaders and the git/subprocess effects seam
(WI-277: split verbatim from tests/test_gen_trajectory.py along the WI-280
production seams; this module's subject is `traj_parse.py`).

Everything upstream of a pixel: the as-of stamp read from git (and the
determinism that survives its absence off-git), the WI-346 one-and-only spine
loader — equivalence with the inline filters it replaced, in file order, and the
example-row drop only when asked — and `run_captured`, the single capture helper,
whose five keywords and off-git degrade are pinned through a subprocess shim.

The shim patches `gt.traj_parse.subprocess`: WI-280 moved the effects seam out of
the facade, so patching `gt.subprocess` would now silently miss.
"""

import csv
import re
import subprocess
import sys

import pytest
from conftest import ROOT, load_script, pin_autocrlf
from traj_fixtures import FRAME, gen, html_of, make_repo, write_frame


def test_asof_stamp_from_git_and_excluded_from_check(tmp_path):
    # WI-039: the as-of line derives from the last source-touching COMMIT
    # (never now(), so generation stays deterministic), is visible in the
    # shell, and is excluded from the --check byte-compare — a stamp-only
    # difference (the artifact committed one commit behind its sources' last
    # touch) must not read as stale.
    import subprocess

    make_repo(tmp_path)

    def git(*args):
        return subprocess.run(
            ["git", "-C", str(tmp_path), *args], capture_output=True, text=True
        )

    git("init")
    pin_autocrlf(tmp_path)  # WI-461/WI-465; see conftest.pin_autocrlf
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "T")
    git("add", "-A")
    git("commit", "-q", "-m", "sources")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert 'class="asof">state as of commit ' in text
    # Simulate the artifact carrying a previous stamp: content equal, stamp not.
    (tmp_path / "PROJECT_STATE.html").write_text(
        re.sub(
            r'(class="asof">state as of commit )[0-9a-f]+',
            r"\g<1>0000000",
            text,
        ),
        encoding="utf-8",
    )
    proc = gen(tmp_path, "--check")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_no_git_means_no_stamp_and_stays_deterministic(tmp_path):
    # Outside a git repo the stamp is simply absent — no crash, no wall clock.
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    assert 'class="asof"></p>' in html_of(tmp_path)


# --- WI-346: the one local spine loader + the one capture helper ---------------
# Three functions (`arch_icicle`, `spine_stats`, `_spine_pending`) each re-derived
# the SR/LLR/TC `read_rows(...) if id.startswith(...)` triple, and `_asof`/`_git`
# each spelled out the same five subprocess capture keywords — nine sanctioned
# census blocks (`spine-load-repeat`, `subprocess-capture`). Extracted to
# `_spine(root, skip_example=False)` and `_run_captured(argv)`.

# Deliberately NOT id-sorted, and deliberately noisy: a scrambled file order, a
# `-000` example row in the middle, and a row whose id carries no tier prefix.
# ROW ORDER IS THE CONTRACT — the icicle links each row to its FIRST listed
# parent and lays blocks out in arrival order, and `--check` byte-compares the
# render, so a sort or a set/dict round-trip inside the loader is a silent
# artifact change. A sorted fixture could not see that.
SCRAMBLED_SRS = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status\n"
    'SR-009,Late,SN-001,"Shall late.",R,"late",,M,Test,Approved\n'
    'SR-000,Example,SN-001,"Shall example.",R,"example",,M,Test,Drafted\n'
    'SR-002,Middle,SN-001,"Shall middle.",R,"middle",,M,Test,Drafted\n'
    'NOTE,Not a requirement,SN-001,"Shall not.",R,"nope",,M,Test,Drafted\n'
    'SR-001,First,SN-001,"Shall first.",R,"first",,M,Test,Approved\n'
)

SCRAMBLED_LLRS = (
    "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status\n"
    'LLR-007,SR-001,Late,src/m,add,"late",(see TC),Approved\n'
    'LLR-000,SR-001,Example,src/m,add,"example",(see TC),Approved\n'
    "NOTE,SR-001,Not an LLR,src/m,add,nope,(see TC),Approved\n"
    'LLR-001,SR-001,First,src/m,add,"first",(see TC),Approved\n'
)

SCRAMBLED_TCS = (
    "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Status\n"
    "TC-005,LLR-001,Unit,call add,Smoke,a=5,ok,Yes,Approved\n"
    "NOTE,LLR-001,Unit,not a case,Smoke,a=0,ok,Yes,Drafted\n"
    "TC-000,LLR-001,Unit,call add,Smoke,a=0,ok,Yes,Drafted\n"
    "TC-001,LLR-001,Unit,call add,Smoke,a=1,ok,Yes,Approved\n"
)


def _scrambled_spine(root):
    """A registry whose three spine files are out of id order and carry both a
    `-000` example and a non-prefixed row."""
    req = root / "docs" / "requirements"
    req.mkdir(parents=True)
    (root / "docs" / "test").mkdir(parents=True)
    (req / "system-requirements.csv").write_text(SCRAMBLED_SRS, encoding="utf-8")
    (req / "low-level-requirements.csv").write_text(SCRAMBLED_LLRS, encoding="utf-8")
    (root / "docs" / "test" / "test-cases.csv").write_text(
        SCRAMBLED_TCS, encoding="utf-8"
    )
    return root


def test_spine_loader_equals_the_former_inline_filters_in_file_order(tmp_path):
    root = _scrambled_spine(tmp_path)
    gt = load_script("gen_trajectory")

    # The three comprehensions the three call sites each carried before WI-346,
    # transcribed from the pre-extraction source — but reading the fixture's
    # file with `csv.DictReader` DIRECTLY rather than through a kit reader.
    # That independence is the whole point of the check and it now matters more,
    # not less: since the carrier cutover the loader resolves TOML-or-CSV, so a
    # `want` side built on the same resolver would compare the loader with
    # itself. The fixture writes the legacy carrier, and stdlib reads it.
    def _want(rel, id_col):
        with (root / rel).open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        return [r for r in rows if (r.get(id_col) or "").startswith(id_col[:-3])]

    want_srs = _want("docs/requirements/system-requirements.csv", "SR-ID")
    want_llrs = _want("docs/requirements/low-level-requirements.csv", "LLR-ID")
    want_tcs = _want("docs/test/test-cases.csv", "TC-ID")
    srs, llrs, tcs = gt._spine(root)
    # Whole-row equality: the loader must hand back the rows themselves, not a
    # projection — every call site reads columns the loader never names.
    assert srs == want_srs
    assert llrs == want_llrs
    assert tcs == want_tcs
    # Order spelled out, so a regression reads as the scramble it broke rather
    # than as an opaque list mismatch. `-000` survives the DEFAULT load.
    assert [r["SR-ID"] for r in srs] == ["SR-009", "SR-000", "SR-002", "SR-001"]
    assert [r["LLR-ID"] for r in llrs] == ["LLR-007", "LLR-000", "LLR-001"]
    assert [r["TC-ID"] for r in tcs] == ["TC-005", "TC-000", "TC-001"]


def test_spine_loader_drops_example_rows_only_when_asked(tmp_path):
    root = _scrambled_spine(tmp_path)
    gt = load_script("gen_trajectory")
    srs, llrs, tcs = gt._spine(root, skip_example=True)
    # `-000` gone from all three tiers, everything else still in file order.
    assert [r["SR-ID"] for r in srs] == ["SR-009", "SR-002", "SR-001"]
    assert [r["LLR-ID"] for r in llrs] == ["LLR-007", "LLR-001"]
    assert [r["TC-ID"] for r in tcs] == ["TC-005", "TC-001"]
    # The default keeps them: only the pending projection owes the `-000` rule
    # (an example row owes no approval); the icicle and the maturity counts
    # render whatever the registry holds.
    d_srs, d_llrs, d_tcs = gt._spine(root)
    assert "SR-000" in [r["SR-ID"] for r in d_srs]
    assert "LLR-000" in [r["LLR-ID"] for r in d_llrs]
    assert "TC-000" in [r["TC-ID"] for r in d_tcs]
    # And the rule reaches its real caller: SR-000 is `Drafted`, so a leaked
    # example row would invent an approval the owner does not owe.
    pending = gt._spine_pending(root)
    assert pending, "the Drafted SRs must still project"
    assert not any("SR-000" in line for line in pending)
    # SR-002 read `Modified` -> re-attest until D-9 step 7 retired the marker. It
    # reads `Drafted` now: the projection's second arm is snapshot DRIFT, which
    # needs a seeded snapshot this loader fixture has no business carrying, so
    # the Drafted arm is what keeps a NON-example row projecting here — which is
    # the property under test (SR-000 must not leak into it).
    assert any("SR-002" in line for line in pending)


class _SubprocessShim:
    """Stands in for gen_trajectory's `subprocess` binding so a spy never
    mutates the real stdlib module out from under the rest of the suite."""

    DEVNULL = subprocess.DEVNULL

    def __init__(self, run):
        self.run = run


def test_run_captured_states_the_five_keywords_and_degrades_off_git(
    tmp_path, monkeypatch
):
    gt = load_script("gen_trajectory")
    # 1. The contract itself — all five keywords, stated once. Dropping
    #    `errors="replace"` alone reintroduces the L-25 crash on exactly the
    #    rare input nobody tests with, so pin the kwargs, not just the result.
    seen = {}

    def spy(argv, **kwargs):
        seen.update(kwargs)
        return subprocess.run(argv, **kwargs)

    # WI-280: `_run_captured` resolves `subprocess` in traj_parse's namespace now,
    # so patch the module the call looks in (gt.traj_parse is the cached instance).
    monkeypatch.setattr(gt.traj_parse, "subprocess", _SubprocessShim(spy))
    proc = gt._run_captured([sys.executable, "-c", "print('hi')"])
    assert seen == {
        "capture_output": True,
        "text": True,
        "encoding": "utf-8",
        "errors": "replace",
        "stdin": subprocess.DEVNULL,
    }
    assert proc.stdout.strip() == "hi"  # captured + decoded, not bytes/None

    # 2. No child at all: `_run_captured` deliberately does NOT swallow the
    #    OSError — the callers own the degrade, which is what lets a future
    #    caller see a failure this helper has no business deciding about.
    def boom(argv, **kwargs):
        raise OSError("no git here")

    monkeypatch.setattr(gt.traj_parse, "subprocess", _SubprocessShim(boom))
    with pytest.raises(OSError):
        gt._run_captured(["git", "--version"])
    # ...and both callers degrade to their empty forms rather than propagate.
    # (No registry is seeded: `_git`/`_asof` read git, not the work items.)
    assert gt._git(tmp_path, "rev-parse", "HEAD") == (1, "")
    assert gt._asof(tmp_path) == ""

    # 3. Real git, no repo: the other off-git shape (a child that RUNS and
    #    fails). tmp_path is not a work tree, so git exits nonzero.
    monkeypatch.undo()
    code, out = gt._git(tmp_path, "rev-parse", "--verify", "--quiet", "HEAD")
    assert code != 0 and out.strip() == ""
    assert gt._asof(tmp_path) == ""


# --- WI-455: `frame_context`, the depth-0 frame as a read model ----------------


def test_frame_context_is_none_without_a_declared_frame(tmp_path):
    # The registry's own applies-when: a project that never declares a boundary
    # simply does not create the file, and the reader says so with None rather
    # than an empty-but-present frame the view would render as a blank picture.
    gt = load_script("gen_trajectory")
    assert gt.traj_parse.frame_context(tmp_path) is None


def test_frame_context_drops_the_blank_form_s_example_rows(tmp_path):
    # A freshly bootstrapped scaffold HAS the file — the blank form, all of whose
    # rows end `-000`. Same rule as every other tier: example rows are not data.
    gt = load_script("gen_trajectory")
    write_frame(
        tmp_path,
        (
            ROOT / "project-trajectory" / "registries" / "external.template.toml"
        ).read_text(encoding="utf-8"),
    )
    assert gt.traj_parse.frame_context(tmp_path) is None


def test_frame_context_joins_the_tie_backs_and_keeps_id_order(tmp_path):
    gt = load_script("gen_trajectory")
    write_frame(tmp_path, FRAME)
    (tmp_path / "docs" / "requirements" / "interfaces.toml").write_text(
        """[interface.IF-001]
owner = "src/m"
consumers = ["external:downstream adopter"]
channel = "cli"
status = "Drafted"
interface_to_external = "B-01"

[interface.IF-002]
owner = "external:git"
consumers = ["src/m"]
channel = "git"
status = "Drafted"
notes = "No tie-back: git is not a party of its own here."
""",
        encoding="utf-8",
    )
    frame = gt.traj_parse.frame_context(tmp_path)
    assert [e["id"] for e in frame["entities"]] == ["EXT-001", "EXT-002"]
    assert [c["id"] for c in frame["crossings"]] == ["B-01", "B-02"]
    by_id = {c["id"]: c for c in frame["crossings"]}
    # the realization is JOINED from interfaces.toml, with the side it ties on...
    assert by_id["B-01"]["realized_by"] == [("IF-001", "out")]
    # ...and a crossing nothing realizes stays declared, not dropped
    assert by_id["B-02"]["realized_by"] == []
    # the entity name resolves for display without the frame row restating it
    assert by_id["B-01"]["entity_name"] == "Downstream adopter"
    # the untied `external:` endpoint carries the reason its own row records
    assert [(u["id"], u["endpoint"]) for u in frame["untied"]] == [
        ("IF-002", "external:git")
    ]
    assert frame["untied"][0]["reason"].startswith("No tie-back")


def test_frame_context_reads_this_repo_s_own_locked_frame():
    # The meta repo's own frame, pinned as data rather than as a picture: the
    # locked depth-0 table is 4 parties, 4 crossings and 3 relationships, `B-02`
    # is the one crossing deliberately left unrealized (SR-140's condition, stated
    # in the registry header), and WI-455 slice 2's adjudication left exactly
    # three `external:` rows tied back to nothing, each with its reason on the row.
    gt = load_script("gen_trajectory")
    frame = gt.traj_parse.frame_context(ROOT)
    assert len(frame["entities"]) == 4
    assert [c["id"] for c in frame["crossings"]] == ["B-01", "B-02", "B-04", "B-05"]
    assert len(frame["relationships"]) == 3
    by_id = {c["id"]: c for c in frame["crossings"]}
    assert by_id["B-02"]["realized_by"] == []
    # the two rows slice 2 gave a facing, and the largest bundle in the frame
    assert {"IF-080", "IF-081"} <= {i for i, _side in by_id["B-05"]["realized_by"]}
    assert [u["id"] for u in frame["untied"]] == ["IF-032", "IF-036", "IF-041"]
    assert all(u["reason"].startswith("No tie-back") for u in frame["untied"])
