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
from conftest import load_script
from traj_fixtures import gen, html_of, make_repo


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
    'SR-009,Late,SN-001,"Shall late.",R,"late",,M,Test,Verified\n'
    'SR-000,Example,SN-001,"Shall example.",R,"example",,M,Test,Draft\n'
    'SR-002,Middle,SN-001,"Shall middle.",R,"middle",,M,Test,Modified\n'
    'NOTE,Not a requirement,SN-001,"Shall not.",R,"nope",,M,Test,Draft\n'
    'SR-001,First,SN-001,"Shall first.",R,"first",,M,Test,Verified\n'
)

SCRAMBLED_LLRS = (
    "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status\n"
    'LLR-007,SR-001,Late,src/m,add,"late",(see TC),Planned\n'
    'LLR-000,SR-001,Example,src/m,add,"example",(see TC),Planned\n'
    "NOTE,SR-001,Not an LLR,src/m,add,nope,(see TC),Planned\n"
    'LLR-001,SR-001,First,src/m,add,"first",(see TC),Planned\n'
)

SCRAMBLED_TCS = (
    "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Status\n"
    "TC-005,LLR-001,Unit,call add,Smoke,a=5,ok,Yes,Verified\n"
    "NOTE,LLR-001,Unit,not a case,Smoke,a=0,ok,Yes,Draft\n"
    "TC-000,LLR-001,Unit,call add,Smoke,a=0,ok,Yes,Draft\n"
    "TC-001,LLR-001,Unit,call add,Smoke,a=1,ok,Yes,Verified\n"
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
    # (an example row owes no ratification); the icicle and the maturity counts
    # render whatever the registry holds.
    d_srs, d_llrs, d_tcs = gt._spine(root)
    assert "SR-000" in [r["SR-ID"] for r in d_srs]
    assert "LLR-000" in [r["LLR-ID"] for r in d_llrs]
    assert "TC-000" in [r["TC-ID"] for r in d_tcs]
    # And the rule reaches its real caller: SR-000 is `Draft`, so a leaked
    # example row would invent a ratification the owner does not owe.
    pending = gt._spine_pending(root)
    assert pending, "the Draft/Modified SRs must still project"
    assert not any("SR-000" in line for line in pending)
    assert any("SR-002" in line for line in pending)  # Modified -> re-attest


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
