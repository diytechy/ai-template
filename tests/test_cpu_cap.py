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
import json
import os
import subprocess
import sys

import pytest
from conftest import ROOT, SCRIPTS

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


# --- What the named job does and does NOT buy -------------------------------
# Two wrong claims have been made here, in opposite directions, and this guard
# exists to stop a third.
#
#   1. The original: "every pytest process — other runs, other worktrees — joins
#      the SAME job and shares ONE ceiling." Untested, and false whenever the
#      joining process already sits in an unrelated job (127-REVIEW-A BLOCKER 1).
#   2. The over-correction: "a second run from a different PROCESS TREE gets its
#      own ceiling." Also false, and its guard was ambient-dependent — it passed
#      on a machine whose processes were already jobbed and FAILED on one whose
#      were not, reporting `SHARED` (128-REVIEW-A BLOCKER 1).
#
# The actual Windows rule is about the JOINING PROCESS'S OWN JOB MEMBERSHIP, not
# about process trees: AssignProcessToJobObject succeeds if the process is in no
# job, or if the target job is empty or already in that process's parent job
# chain. So a second run shares the ceiling when nothing has jobbed it, and gets
# its own when something has (a sandbox, a container, a CI agent, another job).
#
# Therefore this test CREATES the topology it measures instead of inheriting it.
# `pre-job` makes the probe join its own anonymous job first, which is the one
# condition under which the fallback is guaranteed — otherwise the outcome
# legitimately depends on the host and no assertion can be universal.

_PROBE = """
import ctypes, importlib.util, os, sys, time
from ctypes import wintypes
spec = importlib.util.spec_from_file_location("_rc", sys.argv[1] + "/conftest.py")
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)
rc.JOB_NAME = sys.argv[2]          # a name unique to this test, so the probe is
warned = []                        # independent of the live pytest run's job
rc._warn = lambda m: warned.append(m)
k32 = ctypes.WinDLL("kernel32", use_last_error=True)
k32.GetCurrentProcess.restype = wintypes.HANDLE
k32.CreateJobObjectW.restype = wintypes.HANDLE
k32.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
k32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
k32.OpenJobObjectW.restype = wintypes.HANDLE
k32.OpenJobObjectW.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR]
k32.IsProcessInJob.argtypes = [wintypes.HANDLE, wintypes.HANDLE,
                               ctypes.POINTER(wintypes.BOOL)]
k32.QueryInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int,
                                          ctypes.c_void_p, wintypes.DWORD,
                                          ctypes.c_void_p]
me = k32.GetCurrentProcess()
if "pre-job" in sys.argv:
    # Put THIS process in its own anonymous job first. Creating and joining an
    # empty job always succeeds, so after this the process is definitely jobbed
    # and the named job is definitely not in its parent chain.
    own = k32.CreateJobObjectW(None, None)
    if not (own and k32.AssignProcessToJobObject(own, me)):
        print("PREJOB-FAILED", flush=True); sys.exit(0)
rc._bound_windows(50)
named = k32.OpenJobObjectW(0x0004, False, rc.JOB_NAME)
inside = wintypes.BOOL()
shared = bool(named and k32.IsProcessInJob(me, named, ctypes.byref(inside))
              and inside.value)

class RATE(ctypes.Structure):
    _fields_ = [("ControlFlags", wintypes.DWORD), ("CpuRate", wintypes.DWORD)]

info = RATE()
# NULL = "the job I am immediately in" — for the fallback that IS the private
# job, which is the ceiling whose rate the old guard never checked.
ok = k32.QueryInformationJobObject(named if shared else None, 15,
                                   ctypes.byref(info), ctypes.sizeof(info), None)
print("{} warned={} flags={} rate={}".format(
    "SHARED" if shared else "PRIVATE", len(warned),
    hex(info.ControlFlags) if ok else "?", info.CpuRate if ok else "?"), flush=True)
if "hold" in sys.argv:
    if "spawn-child" in sys.argv:
        # A CHILD inherits job membership, which is the property that IS real.
        import subprocess
        child = subprocess.run([sys.executable, __file__, sys.argv[1], sys.argv[2]],
                               capture_output=True, text=True)
        print("CHILD " + child.stdout.strip(), flush=True)
    time.sleep(30)
"""


@pytest.mark.skipif(sys.platform != "win32", reason="job objects are Windows-only")
def test_a_run_that_is_already_jobbed_gets_its_own_ceiling(tmp_path):
    """The cap's concurrency behaviour, with the topology CONSTRUCTED not assumed.

    Three assertions, each true on any Windows host:

      * the FIRST tree reports `SHARED` — proving the named job is real and the
        probe can observe membership. Without this, a bug that made everything
        fall back would satisfy the rest vacuously.
      * a CHILD of it reports `SHARED` — job membership is inherited, which is
        the tree-wide ceiling the mechanism genuinely delivers.
      * a process that is ALREADY IN ITS OWN JOB cannot join the populated named
        job: it falls back to a private ceiling, says so, and that private
        ceiling carries the same hard rate. This is the case where two runs
        total twice the cap.

    What is deliberately NOT asserted: what an UNJOBBED second process does. It
    joins the named job and shares the ceiling — which is why the "different
    process tree" phrasing was wrong, and why the previous version of this test
    failed on a host whose processes were not already jobbed while passing here.
    Whether a given machine shares depends on whether something has jobbed the
    run, so no universal assertion exists and the docs must state the condition.
    """
    probe = tmp_path / "probe.py"
    probe.write_text(_PROBE, encoding="utf-8")
    job_name = "ai-template-pytest-test-{}".format(os.getpid())
    args = [sys.executable, str(probe), str(ROOT), job_name]
    # The named topology is the one measured, so a run started with the
    # private job mode (the smoke budget step's tier) does not pass it on.
    env = {k: v for k, v in os.environ.items() if k != "PYTEST_CPU_CAP_JOB"}

    holder = subprocess.Popen(
        args + ["hold", "spawn-child"], stdout=subprocess.PIPE, text=True, env=env
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

        second = subprocess.run(
            args + ["pre-job"], capture_output=True, text=True, timeout=60, env=env
        )
        out = second.stdout.strip()
        assert "PREJOB-FAILED" not in out, "could not construct the topology: " + out
        assert out.startswith("PRIVATE"), (
            "a process already inside its own job joined the populated named "
            "job. Windows documents that as impossible; if it has changed, the "
            "conftest docstring and docs/status.md must be widened — do not "
            "just relax this assertion: {!r}".format(out)
        )
        # It must SAY so — a silent downgrade of a resource guarantee is how the
        # original false claim survived a live run.
        assert "warned=1" in out, out
        # ...and the fallback must actually CAP. The previous guard checked only
        # which job the process landed in, never that the private one carried a
        # rate (128-REVIEW-A).
        assert "flags=0x5" in out, "private fallback is not ENABLE|HARD_CAP: " + out
        assert "rate={}".format(50 * 100) in out, out
    finally:
        holder.kill()
        holder.wait()


# --- The job mode: named (shared) or private --------------------------------
# A caller that meters its own job (the smoke-budget step) needs the tier it
# starts to stay out of the named job, or a concurrent run from another tree
# could join that job and land its CPU in the reading. `PYTEST_CPU_CAP_JOB`
# set to `private` asks for the fallback's construction from the start.


def test_the_job_mode_reads_its_one_value(monkeypatch, capsys):
    reader = root_conftest._requested_job_mode
    cases = {"": "named", "  ": "named", "private": "private", " Private ": "private"}
    for raw, expected in cases.items():
        monkeypatch.setenv("PYTEST_CPU_CAP_JOB", raw)
        assert reader() == expected, raw
    monkeypatch.delenv("PYTEST_CPU_CAP_JOB")
    assert reader() == "named"
    assert capsys.readouterr().err == ""
    # Any other value is named, never fatal, and says which value it ignored.
    monkeypatch.setenv("PYTEST_CPU_CAP_JOB", "shared-please")
    assert reader() == "named"
    err = capsys.readouterr().err
    assert "PYTEST_CPU_CAP_JOB" in err and "shared-please" in err, err


_PRIVATE_PROBE = """
import ctypes, importlib.util, json, sys
from ctypes import wintypes
spec = importlib.util.spec_from_file_location("_rc", sys.argv[1] + "/conftest.py")
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)
rc.JOB_NAME = sys.argv[2]
warned = []
rc._warn = lambda m: warned.append(m)
rc._bound_windows(25)
k32 = ctypes.WinDLL("kernel32", use_last_error=True)
k32.GetCurrentProcess.restype = wintypes.HANDLE
k32.IsProcessInJob.argtypes = [wintypes.HANDLE, wintypes.HANDLE,
                               ctypes.POINTER(wintypes.BOOL)]
k32.GetPriorityClass.argtypes = [wintypes.HANDLE]
me = k32.GetCurrentProcess()
inside = wintypes.BOOL()
ok = k32.IsProcessInJob(me, None, ctypes.byref(inside))
print(json.dumps({"in_a_job": bool(ok and inside.value),
                  "priority": k32.GetPriorityClass(me),
                  "warned": warned}), flush=True)
sys.stdin.readline()  # hold the job open until the test has looked
"""


@pytest.mark.skipif(sys.platform != "win32", reason="job objects are Windows-only")
def test_a_private_run_joins_no_named_job(tmp_path):
    """Under `private` the run is capped in an unnamed job, so the named job
    is never created: the test's own create of that name makes a new object.
    The child holds its job open while the test looks, since a named job dies
    with its last handle."""
    probe = tmp_path / "private_probe.py"
    probe.write_text(_PRIVATE_PROBE, encoding="utf-8")
    job_name = "ai-template-pytest-private-{}".format(os.getpid())
    env = dict(os.environ, PYTEST_CPU_CAP_JOB="private")
    child = subprocess.Popen(
        [sys.executable, str(probe), str(ROOT), job_name],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        env=env,
    )
    try:
        line = child.stdout.readline()
        assert line, "the probe printed nothing"
        report = json.loads(line)
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.CreateJobObjectW.restype = wintypes.HANDLE
        k32.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        k32.CloseHandle.argtypes = [wintypes.HANDLE]
        ctypes.set_last_error(0)
        handle = k32.CreateJobObjectW(None, job_name)
        error = ctypes.get_last_error()
        if handle:
            k32.CloseHandle(handle)
        assert handle, ctypes.WinError(error)
        assert error != 183, "the private run created the named job"  # ALREADY_EXISTS
        assert report["in_a_job"], report
        assert report["priority"] == 0x00004000, report  # BELOW_NORMAL
        assert report["warned"] == [], report  # the private job was asked for
    finally:
        child.stdin.close()
        child.wait(timeout=60)


_RECORDER_PROBE = """
import ctypes, importlib.util, json, sys
sys.path.insert(0, sys.argv[2])
from kitlib import winjob

log = []
recorder_calls = []
RESULTS = {"CreateJobObjectW": 101, "GetCurrentProcess": 7, "IsProcessInJob": 0}


def plain(arg):
    held = getattr(arg, "_obj", None)  # what ctypes.byref points at
    if held is not None and hasattr(held, "CpuRate"):
        return {"flags": held.ControlFlags, "rate": held.CpuRate}
    return arg if arg is None or isinstance(arg, (int, str)) else repr(arg)


class Fn:
    def __init__(self, name):
        self.name = name

    def __call__(self, *args):
        log.append([self.name] + [plain(a) for a in args])
        return RESULTS.get(self.name, 1)


class FakeKernel32:
    def __getattr__(self, name):
        fn = Fn(name)
        setattr(self, name, fn)
        return fn


fake = FakeKernel32()


def recorder():
    recorder_calls.append(1)
    return fake, None


winjob.win32 = recorder
spec = importlib.util.spec_from_file_location("_rc", sys.argv[1] + "/conftest.py")
rc = importlib.util.module_from_spec(spec); spec.loader.exec_module(rc)
rc.JOB_NAME = sys.argv[3]
rc._bound_windows(25)
reach = getattr(rc, "_winjob", None)
same = reach is not None and reach() is sys.modules["kitlib.winjob"]
print(json.dumps({"recorder_calls": len(recorder_calls), "log": log,
                  "same_module": same}), flush=True)
"""


@pytest.mark.skipif(sys.platform != "win32", reason="job objects are Windows-only")
def test_the_root_conftest_takes_its_prototypes_from_the_shared_module(tmp_path):
    """The cap's kernel32 calls go through `kitlib.winjob.win32()`, the one
    prototype set the session kill also uses, never a WinDLL of its own.

    A child replaces `win32` with a recorder over a fake kernel32 and applies
    the cap; the log must hold the cap's calls, in order. It runs in a child
    so a conftest that still builds its own WinDLL joins a real job there,
    not in this test process."""
    probe = tmp_path / "recorder_probe.py"
    probe.write_text(_RECORDER_PROBE, encoding="utf-8")
    job_name = "ai-template-pytest-recorded-{}".format(os.getpid())
    env = {k: v for k, v in os.environ.items() if k != "PYTEST_CPU_CAP_JOB"}
    proc = subprocess.run(
        [sys.executable, str(probe), str(ROOT), str(SCRIPTS), job_name],
        capture_output=True,
        text=True,
        timeout=60,
        env=env,
    )
    assert proc.returncode == 0, proc.stderr
    report = json.loads(proc.stdout)
    assert report["recorder_calls"] >= 1, "the conftest never asked kitlib.winjob"
    wanted = ("CreateJobObjectW", "SetInformationJobObject")
    wanted += ("AssignProcessToJobObject", "SetPriorityClass")
    calls = [entry for entry in report["log"] if entry[0] in wanted]
    assert calls == [
        ["CreateJobObjectW", None, job_name],
        # the class, then ENABLE|HARD_CAP at 25 % in 1/100 percent; the size
        ["SetInformationJobObject", 101, 15, {"flags": 0x5, "rate": 2500}, 8],
        ["AssignProcessToJobObject", 101, 7],
        ["SetPriorityClass", 7, 0x00004000],
    ], report["log"]
    assert report["same_module"], "the conftest reaches another kitlib.winjob"
