"""The root conftest's machine-share bound (2026-07-27, owner-directed).

Why this exists as a test at all: the cap is the kind of thing that silently
stops working. A wrong flag constant, a truncated handle, an env typo — each
leaves a suite that runs perfectly while saturating the developer's desktop,
which is exactly the failure it was added to prevent, and nothing else in the
repo would notice.

Two halves, and the split matters:

  * `_requested_cap` is a pure function, so its parsing is tested exhaustively
    and everywhere — including CI, where the cap itself is deliberately off.
  * The APPLIED cap is asserted against the live process: this test asks the OS
    what limit the running pytest process is actually under. Asserting the
    constant we passed in would prove nothing about whether Windows accepted it,
    and the first version of this code was rejected by Windows for a wrong flag
    while looking entirely correct.
"""

import ctypes
import importlib.util
import os
import subprocess
import sys

import pytest
from conftest import ROOT

if sys.platform == "win32":
    from ctypes import wintypes


def _load_root_conftest():
    """The REPO-ROOT conftest, loaded by path.

    A plain `import conftest` cannot reach it: `tests/conftest.py` already owns
    that module name in `sys.modules`, so the import silently returns the test
    package's conftest and every assertion below would test the wrong file."""
    spec = importlib.util.spec_from_file_location(
        "_root_conftest", ROOT / "conftest.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


root_conftest = _load_root_conftest()

JobObjectCpuRateControlInformation = 15
JOB_OBJECT_CPU_RATE_CONTROL_ENABLE = 0x1
JOB_OBJECT_CPU_RATE_CONTROL_HARD_CAP = 0x4


def test_the_declared_default_is_half_the_machine():
    """The default is the PROMISE, so it is pinned like a ratchet baseline.

    Everything else here compares against `DEFAULT_CAP_PERCENT` itself, which
    made those assertions self-referential: raising the default to 90 kept the
    whole module green while quietly withdrawing the guarantee it exists to
    make (owner's constraint, 2026-07-27: a test run must not throttle this
    machine or any other personal machine). Changing the dial is legitimate —
    change it HERE too, deliberately, with the reason in the session log."""
    assert root_conftest.DEFAULT_CAP_PERCENT == 50


def test_cap_parsing_covers_the_dial(monkeypatch):
    """Every value a person might set, including the ones meant to disable it."""
    cases = {
        "": root_conftest.DEFAULT_CAP_PERCENT,  # unset -> the default bound
        "off": None,
        "none": None,
        "no": None,
        "0": None,
        "100": None,  # "all of it" IS no cap; don't install a no-op job
        "OFF": None,  # case-insensitive, because a human types this
        " 35 ": 35,  # tolerate whitespace from a shell export
        "35": 35,
        "1": 1,
        "99": 99,
        "-5": None,  # nonsense range -> no cap rather than an OS error
        "150": None,
        "banana": root_conftest.DEFAULT_CAP_PERCENT,  # unparseable -> the default
    }
    for raw, expected in cases.items():
        monkeypatch.setenv("PYTEST_CPU_CAP", raw)
        assert root_conftest._requested_cap() == expected, raw
    monkeypatch.delenv("PYTEST_CPU_CAP")
    assert root_conftest._requested_cap() == root_conftest.DEFAULT_CAP_PERCENT


def test_pytest_still_runs_when_xdist_is_absent():
    """The root conftest must not be able to kill a run that lacks xdist.

    `pytest_xdist_auto_num_workers` is xdist's hookspec, so declaring it
    unconditionally makes pluggy reject the conftest — `PluginValidationError:
    unknown hook` — and pytest dies before collecting a single test. That is not
    a hypothetical: it shipped, and it broke `-p no:xdist` and any environment
    that never installed xdist. `@pytest.hookimpl(optionalhook=True)` is the fix
    and this is its guard.

    Found only because a test was run with git off PATH to exercise an unrelated
    skip; every ordinary invocation in this repo loads xdist and hid it.

    Collects a REPO test, not a temp one: pytest loads conftests from the
    collected file's ancestors, so a probe written into `tmp_path` never loads
    the root conftest and the guard passes no matter how broken that file is.
    The first version of this test did exactly that and survived its own
    mutation."""
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:xdist",
            "--collect-only",
            "tests/test_smoke_budget.py",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    out = proc.stdout + proc.stderr
    assert "PluginValidationError" not in out, out
    assert "INTERNALERROR" not in out, out
    assert proc.returncode == 0, out


def test_worker_count_is_half_the_box_and_defers_to_an_explicit_setting(monkeypatch):
    monkeypatch.delenv("PYTEST_XDIST_AUTO_NUM_WORKERS", raising=False)
    assert root_conftest.pytest_xdist_auto_num_workers(None) == max(
        1, (os.cpu_count() or 2) // 2
    )
    # The negative half: an explicit setting wins, so `ptc` (and CI) still rule.
    monkeypatch.setenv("PYTEST_XDIST_AUTO_NUM_WORKERS", "3")
    assert root_conftest.pytest_xdist_auto_num_workers(None) is None


@pytest.mark.skipif(sys.platform != "win32", reason="job objects are Windows-only")
@pytest.mark.skipif(
    root_conftest._requested_cap() is None,
    reason="cap disabled for this run (PYTEST_CPU_CAP) — CI does this deliberately",
)
def test_this_live_process_runs_under_the_hard_cap_it_asked_for():
    """Ask the OS, not the code, what this process is limited to.

    Asks about the job BY NAME, deliberately. The obvious form —
    `QueryInformationJobObject(NULL, ...)`, "whatever job I am in" — reports the
    *immediate* job, and under an xdist run every worker sits in a nested job, so
    it answered `ControlFlags=0` and failed while the cap was working perfectly.
    `IsProcessInJob` against our own handle asks the question that matters: is
    THIS process inside THAT job. It holds for the controller and for every
    worker, which is the claim the cap makes.

    A pass means the cap survived the round trip through Windows; the
    `0x2`-instead-of-`0x4` bug this replaced passed every code-level check and
    was rejected by the OS at runtime."""

    class RATE(ctypes.Structure):
        _fields_ = [
            ("ControlFlags", wintypes.DWORD),
            ("CpuRate", wintypes.DWORD),
        ]

    JOB_OBJECT_QUERY = 0x0004
    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.OpenJobObjectW.restype = wintypes.HANDLE
    k32.OpenJobObjectW.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR]
    k32.IsProcessInJob.argtypes = [
        wintypes.HANDLE,
        wintypes.HANDLE,
        ctypes.POINTER(wintypes.BOOL),
    ]
    k32.GetCurrentProcess.restype = wintypes.HANDLE
    k32.QueryInformationJobObject.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
        ctypes.c_void_p,
    ]
    # The claim is "this process runs under a hard cap at the configured rate",
    # NOT "this process is in that specific job" — there are two legitimate ways
    # to be capped and an assertion on only one of them fails a working run:
    #   shared  — assigned to the named job (this run's own tree; workers inherit)
    #   private — a different process tree already owned the named job, so the
    #             conftest fell back to a private job with the same rate
    # This is an OR over those two, deliberately: it asserts the RATE, and is
    # silent about which job supplies it. Which branch you land in — and the fact
    # that the second one is NOT a shared ceiling — is pinned separately, by
    # test_a_second_independent_run_gets_its_own_ceiling. Read that one before
    # believing anything here about concurrency (127-REVIEW-A MAJOR 2: the
    # comment here used to say "checking both", which reads as "asserts both").
    me = k32.GetCurrentProcess()
    named = k32.OpenJobObjectW(JOB_OBJECT_QUERY, False, root_conftest.JOB_NAME)
    inside = wintypes.BOOL()
    in_named = bool(
        named and k32.IsProcessInJob(me, named, ctypes.byref(inside)) and inside.value
    )
    info = RATE()
    ok = k32.QueryInformationJobObject(
        named if in_named else None,  # NULL = "the job I am in" (the fallback)
        JobObjectCpuRateControlInformation,
        ctypes.byref(info),
        ctypes.sizeof(info),
        None,
    )
    assert ok, "this process is under no job with CPU rate control: {}".format(
        ctypes.WinError(ctypes.get_last_error())
    )
    assert info.ControlFlags & JOB_OBJECT_CPU_RATE_CONTROL_ENABLE, hex(
        info.ControlFlags
    )
    # The half that catches a WEIGHT_BASED (0x2) mis-set: without HARD_CAP the
    # tree is free to use the whole box whenever the box is otherwise idle,
    # which is precisely the situation a developer notices.
    assert info.ControlFlags & JOB_OBJECT_CPU_RATE_CONTROL_HARD_CAP, hex(
        info.ControlFlags
    )
    assert info.CpuRate == root_conftest._requested_cap() * 100, info.CpuRate


# --- What the named job does and does NOT buy (127-REVIEW-A BLOCKER 1/MAJOR 2) -
# The conftest used to promise that "every pytest process — other runs, other
# worktrees — joins the SAME job and shares ONE ceiling". Nothing tested it, and
# it is false: Windows only permits assignment when the target job is EMPTY or in
# the process's own parent job chain, so the SECOND concurrent run cannot join a
# job another tree has already populated. This guard measures both halves of the
# real behaviour so the documentation can be checked against something.

_PROBE = """
import ctypes, importlib.util, os, sys, time
from ctypes import wintypes
spec = importlib.util.spec_from_file_location("_rc", sys.argv[1] + "/conftest.py")
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)
rc.JOB_NAME = sys.argv[2]          # a name unique to this test, so the probe is
warned = []                        # independent of the live pytest run's job
rc._warn = lambda m: warned.append(m)
rc._bound_windows(50)
k32 = ctypes.WinDLL("kernel32", use_last_error=True)
k32.GetCurrentProcess.restype = wintypes.HANDLE
k32.OpenJobObjectW.restype = wintypes.HANDLE
k32.OpenJobObjectW.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR]
k32.IsProcessInJob.argtypes = [wintypes.HANDLE, wintypes.HANDLE,
                               ctypes.POINTER(wintypes.BOOL)]
named = k32.OpenJobObjectW(0x0004, False, rc.JOB_NAME)
inside = wintypes.BOOL()
shared = bool(named and k32.IsProcessInJob(k32.GetCurrentProcess(), named,
                                           ctypes.byref(inside)) and inside.value)
print(("SHARED" if shared else "PRIVATE") + " warned=" + str(len(warned)), flush=True)
if len(sys.argv) > 3 and sys.argv[3] == "hold":
    if len(sys.argv) > 4 and sys.argv[4] == "spawn-child":
        # A CHILD inherits job membership, which is the property that IS real.
        import subprocess
        child = subprocess.run([sys.executable, __file__, sys.argv[1], sys.argv[2]],
                               capture_output=True, text=True)
        print("CHILD " + child.stdout.strip(), flush=True)
    time.sleep(30)
"""


@pytest.mark.skipif(sys.platform != "win32", reason="job objects are Windows-only")
def test_a_second_independent_run_gets_its_own_ceiling(tmp_path):
    """Two concurrent runs do NOT total the cap — they total twice it.

    This is the corrected claim, and it is pinned in both directions so neither
    half can rot into a tautology:

      * the FIRST tree reports `SHARED` — proving the named job is real and the
        probe can observe membership. Without this half, a bug that made every
        process fall back would satisfy the assertion below vacuously.
      * a SECOND, INDEPENDENT tree, started while the first still holds the job,
        reports `PRIVATE` and emits the shortfall warning.
      * a CHILD of the first tree reports `SHARED` — the tree-wide ceiling that
        the mechanism genuinely delivers, and the only sharing it delivers.

    Uses a job name unique to this test: the live pytest run already owns
    `JOB_NAME`, so probes reusing it would inherit membership from their parent
    and report `SHARED` no matter what the code did.
    """
    probe = tmp_path / "probe.py"
    probe.write_text(_PROBE, encoding="utf-8")
    job_name = "ai-template-pytest-test-{}".format(os.getpid())
    args = [sys.executable, str(probe), str(ROOT), job_name]

    holder = subprocess.Popen(
        args + ["hold", "spawn-child"], stdout=subprocess.PIPE, text=True
    )
    try:
        first = holder.stdout.readline().strip()
        assert first.startswith("SHARED"), (
            "the first tree did not create/join the named job, so the rest of "
            "this test proves nothing: {!r}".format(first)
        )
        child = holder.stdout.readline().strip()
        assert child.startswith("CHILD SHARED"), (
            "a child did not inherit the job — the tree-wide ceiling, which is "
            "the one property actually promised: {!r}".format(child)
        )

        second = subprocess.run(args, capture_output=True, text=True, timeout=60)
        assert second.stdout.strip().startswith("PRIVATE"), (
            "a second independent tree unexpectedly SHARED the ceiling. If "
            "Windows has started allowing this, the conftest docstring and "
            "docs/status.md must be widened back — do not just relax this "
            "assertion: {!r}".format(second.stdout)
        )
        # It must also SAY so: a silent downgrade of a resource guarantee is how
        # the false claim survived a live run in the first place.
        assert second.stdout.strip().endswith("warned=1"), second.stdout
    finally:
        holder.kill()
        holder.wait()
