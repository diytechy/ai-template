"""Root conftest: bound what a test run costs THIS MACHINE.

Two levers, because they answer two different questions, and the first one alone
does not keep a desktop usable:

  1. `pytest_xdist_auto_num_workers` — how many xdist workers ONE run asks for.
  2. `pytest_configure` — a hard ceiling on what the whole process TREE may
     consume, shared across every concurrent run.

Why (1) is not enough, measured 2026-07-27 on this 24-thread box:

  * A worker count bounds workers, not PROCESSES. The slow tier is
    subprocess-per-test by design (SLOW_MODULES; `tests/test_trace.py` alone has
    ~70 subprocess sites), so a 12-worker run measured **42 python + 4 git
    processes live at mean 59% / max 74% CPU**. Half the workers is not half the
    machine.
  * It is per-process. Two concurrent runs are back to 24 workers — the exact
    scenario that motivated the cap. Parallel WI dispatch makes that normal, not
    exceptional: each train worktree runs its own suite.

So (2) applies a **named Windows job object with a hard CPU rate cap**. The job
bounds the tree regardless of how many processes it spawns, and because the job
is NAMED, every pytest process — controller, xdist workers, other runs, other
worktrees — joins the SAME job and shares ONE ceiling. N concurrent suites total
the cap instead of multiplying it. Proven with a deterministic burner: 24
spinners measured 100% CPU uncapped and 37.5% mean / 47% max under a 25% cap.

Plus a priority drop, which is what actually keeps the UI smooth: the ceiling
says how much the tests may take, `BelowNormal` says they yield it the moment
anything in the foreground wants it.

Dial: `PYTEST_CPU_CAP` — a percent, or `off`/`0`/`100` to disable. CI sets it
off (ephemeral runners, nobody's desktop, and a wall-clock smoke-budget job).

POSIX degrades honestly to a `nice` bump: there is no job-object equivalent
without cgroup privileges, and this file must not pretend to a guarantee it
cannot make there.

Never fatal. A machine that refuses any of this gets a warning and a normal test
run — a resource nicety must not be able to red a suite.
"""

import os
import sys

DEFAULT_CAP_PERCENT = 50
JOB_NAME = "ai-template-pytest"

# The job handle must outlive this function or the job is destroyed with its
# last handle; a module global is the lifetime.
_JOB_HANDLE = None


def pytest_xdist_auto_num_workers(config):
    """Half this machine's logical CPUs, leaving the rest for everything else.

    The hookspec is `firstresult=True` (xdist/newhooks.py), so this wins over
    xdist's built-in implementation. Returning None means "no opinion" and
    defers to the next one - which is what reads PYTEST_XDIST_AUTO_NUM_WORKERS,
    so an explicit setting (what `ptc` exports for the duration of a run) still
    overrides this.

    Derived from the current machine, never hardcoded: this file is committed
    and runs on boxes with different core counts.
    """
    if os.environ.get("PYTEST_XDIST_AUTO_NUM_WORKERS"):
        return None

    return max(1, (os.cpu_count() or 2) // 2)


def _requested_cap():
    """The configured ceiling as a percent, or None when disabled."""
    raw = (os.environ.get("PYTEST_CPU_CAP") or "").strip().lower()
    if raw in ("off", "none", "no", "0", "100"):
        return None
    if not raw:
        return DEFAULT_CAP_PERCENT
    try:
        pct = int(raw)
    except ValueError:
        return DEFAULT_CAP_PERCENT
    return pct if 1 <= pct < 100 else None


def _warn(message):
    print("conftest: {} — running without it.".format(message), file=sys.stderr)


def _bound_windows(percent):
    """Join the shared, hard-capped job object; drop to BelowNormal."""
    global _JOB_HANDLE
    import ctypes
    from ctypes import wintypes

    # HARD_CAP is 0x4. 0x2 is WEIGHT_BASED, which takes a Weight of 1..9 and
    # rejects a rate outright (ERROR_INVALID_PARAMETER) — an easy and confusing
    # mis-set, so the value is named rather than inlined.
    ENABLE, HARD_CAP = 0x1, 0x4
    CPU_RATE_INFO_CLASS = 15
    BELOW_NORMAL = 0x00004000

    class RATE(ctypes.Structure):
        _fields_ = [("ControlFlags", wintypes.DWORD), ("CpuRate", wintypes.DWORD)]

    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    # Prototypes are NOT optional on x64: an undeclared HANDLE argument is passed
    # as a 32-bit int, which truncates the handle and fails obscurely.
    k32.CreateJobObjectW.restype = wintypes.HANDLE
    k32.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
    k32.SetInformationJobObject.restype = wintypes.BOOL
    k32.SetInformationJobObject.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
    ]
    k32.AssignProcessToJobObject.restype = wintypes.BOOL
    k32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    k32.GetCurrentProcess.restype = wintypes.HANDLE
    k32.SetPriorityClass.argtypes = [wintypes.HANDLE, wintypes.DWORD]

    # Same name -> the SAME job: this call opens the existing one when another
    # run (or an xdist worker, or another worktree's suite) already made it, which
    # is what makes the ceiling machine-wide instead of per-process.
    job = k32.CreateJobObjectW(None, JOB_NAME)
    if not job:
        raise ctypes.WinError(ctypes.get_last_error())
    info = RATE(ENABLE | HARD_CAP, percent * 100)  # units of 1/100 of a percent
    if not k32.SetInformationJobObject(
        job, CPU_RATE_INFO_CLASS, ctypes.byref(info), ctypes.sizeof(info)
    ):
        raise ctypes.WinError(ctypes.get_last_error())
    if not k32.AssignProcessToJobObject(job, k32.GetCurrentProcess()):
        err = ctypes.get_last_error()
        # 5 = already in this job (a re-entered worker). Not a failure.
        if err != 5:
            raise ctypes.WinError(err)
    k32.SetPriorityClass(k32.GetCurrentProcess(), BELOW_NORMAL)
    _JOB_HANDLE = job


def pytest_configure(config):
    """Bound this run's share of the machine. Warn-only, never fatal."""
    percent = _requested_cap()
    if percent is None:
        return
    try:
        if sys.platform == "win32":
            _bound_windows(percent)
        else:
            # No cgroup-free hard cap exists here; say what this actually is.
            os.nice(5)
    except Exception as exc:  # noqa: BLE001 - a nicety must never red a suite
        _warn("could not bound CPU use ({}: {})".format(type(exc).__name__, exc))
