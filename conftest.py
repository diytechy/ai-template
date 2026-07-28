"""Root conftest: bound what a test run costs THIS MACHINE.

WHAT THIS DOES AND DOES NOT GUARANTEE — read this before quoting it. Two claims
have already been wrong here, in OPPOSITE directions (127-REVIEW-A refuted "every
concurrent run shares ONE ceiling"; 128-REVIEW-A then refuted the over-correction,
"a second run from a different PROCESS TREE gets its own"). The rule is not about
process trees:

  * ON WINDOWS, ONE RUN AND EVERY PROCESS IT SPAWNS — controller, xdist workers,
    and the subprocesses the slow tier launches per test — is held under a
    single hard CPU-rate cap. Job membership is inherited, so this holds
    unconditionally. It is also the guarantee that matters, because the problem
    being solved is that a worker count does not bound processes.
  * WHETHER A SECOND CONCURRENT RUN SHARES THAT CEILING DEPENDS ON THE HOST, and
    specifically on whether something has already put it in a job object.
    `AssignProcessToJobObject` succeeds when the process is in NO job, or when
    the target job is empty or already in that process's parent job chain. So:
      - nothing has jobbed the second run (a plain shell on a plain desktop) —
        it JOINS the named job and the two runs really do share one ceiling;
      - something has (a sandbox, a container, a CI agent, an IDE that jobs its
        children) — it CANNOT join, falls back to a private job at the same
        percent, and says so on stderr. Two such runs total 2x the cap.
    Neither outcome is universal, which is exactly why the first two versions of
    this paragraph were both false. `tests/test_cpu_cap.py` pins the parts that
    ARE universal by CONSTRUCTING the topology: first tree shares, a child
    inherits, and a process already in its own job falls back to a private
    ceiling that carries the same hard rate.
  * IF THE OS REFUSES ALTOGETHER the run is UNCAPPED, with a warning.
  * ON POSIX there is no cap at all — `os.nice(5)` is a priority bump, which
    changes who wins a contended CPU, not how much of the machine is used.

So the honest one-liner is "a test run does not run away with the machine", not
"N concurrent suites total 50%".

Two levers, because they answer two different questions, and the first one alone
does not keep a desktop usable:

  1. `pytest_xdist_auto_num_workers` — how many xdist workers ONE run asks for.
  2. `pytest_configure` — a hard ceiling on what one run's whole process TREE
     may consume.

Why (1) is not enough, measured 2026-07-27 on this 24-thread box:

  * A worker count bounds workers, not PROCESSES. The slow tier is
    subprocess-per-test by design (SLOW_MODULES; `tests/test_trace.py` alone has
    ~70 subprocess sites), so a 12-worker run measured **42 python + 4 git
    processes live at mean 59% / max 74% CPU**. Half the workers is not half the
    machine.
  * It is per-process, so it does nothing about concurrency — and (2) only
    sometimes does. Parallel WI dispatch makes concurrent suites normal: each
    train worktree runs its own. What (2) guarantees there is that each run is
    individually bounded, and that a run which could not join the shared job
    says so; whether they share is the host's answer, not this file's.

So (2) applies a **named Windows job object with a hard CPU rate cap**. The job
bounds the tree regardless of how many processes it spawns; the NAME is what
lets a run's own descendants land in it. Proven with a deterministic burner: 24
spinners measured 100% CPU uncapped and 37.5% mean / 47% max under a 25% cap.

Plus a priority drop, which is what actually keeps the UI smooth: the ceiling
says how much the tests may take, `BelowNormal` says they yield it the moment
anything in the foreground wants it. On POSIX the priority drop is the whole of
it.

Dial: `PYTEST_CPU_CAP` — a percent, or `off`/`0`/`100` to disable. CI sets it
off (ephemeral runners, nobody's desktop, and a wall-clock smoke-budget job).

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

    # Prefer the NAMED job so this run's own descendants (xdist workers, the
    # slow tier's per-test subprocesses) land in it. A concurrent run from
    # another tree will NOT join it — see the module docstring; that limit is
    # Windows', not a bug here, and the fallback below is what it costs.
    shared = k32.CreateJobObjectW(None, JOB_NAME)
    if not shared:
        raise ctypes.WinError(ctypes.get_last_error())
    if capped(shared):
        _JOB_HANDLE = shared
    else:
        # Windows refuses to assign an ALREADY-JOBBED process into a job that is
        # neither empty nor in its own parent job chain, so a run that something
        # else has already put in a job (a sandbox, a container, a CI agent) gets
        # ERROR_ACCESS_DENIED here once another run has populated the named job.
        # A run that is in NO job joins it fine — which is why "different process
        # tree" was the wrong way to describe this (128-REVIEW-A). An
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
            "this run is already inside another job object, so it could not join "
            "the shared {!r} job and is capped at {}% ON ITS OWN rather than "
            "sharing one ceiling (concurrent runs can then total more than "
            "{}%)".format(JOB_NAME, percent, percent)
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
