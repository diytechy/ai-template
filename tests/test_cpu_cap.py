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
    job = k32.OpenJobObjectW(JOB_OBJECT_QUERY, False, root_conftest.JOB_NAME)
    assert job, "the named job {!r} does not exist — the cap was never created".format(
        root_conftest.JOB_NAME
    )
    inside = wintypes.BOOL()
    assert k32.IsProcessInJob(k32.GetCurrentProcess(), job, ctypes.byref(inside))
    # The claim under test: the cap covers whichever process is running this —
    # controller or worker — and therefore every subprocess they spawn.
    assert inside.value, "this pytest process is OUTSIDE the capped job"
    info = RATE()
    ok = k32.QueryInformationJobObject(
        job,
        JobObjectCpuRateControlInformation,
        ctypes.byref(info),
        ctypes.sizeof(info),
        None,
    )
    assert ok, ctypes.WinError(ctypes.get_last_error())
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
