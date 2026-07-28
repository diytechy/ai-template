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

import pytest

DEFAULT_CAP_PERCENT = 50
JOB_NAME = "ai-template-pytest"

# The job handle must outlive this function or the job is destroyed with its
# last handle; a module global is the lifetime.
_JOB_HANDLE = None


# `optionalhook` because this hookspec exists only while pytest-xdist is loaded.
# Without it, ANY run that lacks xdist — `-p no:xdist`, or an environment that
# never installed it — dies with `PluginValidationError: unknown hook` before a
# single test executes. Found by running a test with git off PATH to exercise an
# unrelated skip guard (WI-333), which is its own lesson: the failure was in the
# most-used file in the repo and every normal invocation hid it.
@pytest.hookimpl(optionalhook=True)
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
    """One line to stderr. The CALLER owns the whole sentence: the fallback path
    is still capped, so a hard-coded "running without it" suffix would have made
    the only visible signal say the opposite of what happened."""
    print("conftest: {}".format(message), file=sys.stderr)


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

    k32.IsProcessInJob.argtypes = [
        wintypes.HANDLE,
        wintypes.HANDLE,
        ctypes.POINTER(wintypes.BOOL),
    ]
    me = k32.GetCurrentProcess()

    def capped(job):
        """Apply the rate limit to `job` and put this process inside it."""
        info = RATE(ENABLE | HARD_CAP, percent * 100)  # units of 1/100 percent
        if not k32.SetInformationJobObject(
            job, CPU_RATE_INFO_CLASS, ctypes.byref(info), ctypes.sizeof(info)
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        inside = wintypes.BOOL()
        if k32.IsProcessInJob(me, job, ctypes.byref(inside)) and inside.value:
            return True  # an xdist worker that inherited it; nothing to do
        return bool(k32.AssignProcessToJobObject(job, me))

    # Prefer the SHARED job: same name -> same job, so concurrent runs and other
    # worktrees land under ONE ceiling instead of one each.
    shared = k32.CreateJobObjectW(None, JOB_NAME)
    if not shared:
        raise ctypes.WinError(ctypes.get_last_error())
    if capped(shared):
        _JOB_HANDLE = shared
    else:
        # Windows refuses to assign a process into a job that is not in its own
        # job hierarchy, so a run launched from a DIFFERENT process tree than the
        # one that created the named job gets ERROR_ACCESS_DENIED here. An
        # earlier version swallowed that as "already in this job" and returned
        # happily, leaving the run completely UNCAPPED while reporting success —
        # the worst outcome available, since the whole point is a guarantee.
        # Fall back to a private job so THIS tree is still bounded, and say so:
        # the ceiling is no longer shared, so N such runs can reach N x the cap.
        private = k32.CreateJobObjectW(None, None)
        if not private or not capped(private):
            raise ctypes.WinError(ctypes.get_last_error())
        _JOB_HANDLE = private
        _warn(
            "the shared {!r} job is owned by another process tree, so this run is "
            "capped at {}% ON ITS OWN rather than sharing one ceiling "
            "(concurrent runs can then total more than {}%)".format(
                JOB_NAME, percent, percent
            )
        )
    k32.SetPriorityClass(me, BELOW_NORMAL)


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
        _warn(
            "could not bound CPU use ({}: {}) — this run is NOT capped.".format(
                type(exc).__name__, exc
            )
        )
