"""The shared Windows job helpers (`kitlib.winjob`).

The module holds the job-object prototypes, the basic-accounting structure and
its reader that the session kill uses. It must import on every platform,
since the kit ships it to POSIX adopters too: kernel32 is touched only when
`win32()` is called. `agent_session` binds the moved names under its old
private names, so a caller reaching `agent_session._win32` or patching
`agent_session._job_active_processes` reaches the one shared definition.
"""

import ctypes
import importlib.util

from conftest import SCRIPTS, load_script

WINJOB = SCRIPTS / "kitlib" / "winjob.py"

ACCOUNTING_FIELDS = [
    "TotalUserTime",
    "TotalKernelTime",
    "ThisPeriodTotalUserTime",
    "ThisPeriodTotalKernelTime",
    "TotalPageFaultCount",
    "TotalProcesses",
    "ActiveProcesses",
    "TotalTerminatedProcesses",
]


def test_the_job_helpers_import_without_loading_kernel32(monkeypatch):
    def refuse(*args, **kwargs):
        raise OSError("kernel32 must not load at import")

    monkeypatch.setattr(ctypes, "WinDLL", refuse, raising=False)
    spec = importlib.util.spec_from_file_location("winjob_fresh_import", WINJOB)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert [name for name, _ in module.JobAccounting._fields_] == ACCOUNTING_FIELDS


def test_agent_session_reaches_the_shared_helpers():
    from kitlib import winjob

    agent_session = load_script("agent_session")
    assert agent_session._win32 is winjob.win32
    assert agent_session._JobAccounting is winjob.JobAccounting
    assert agent_session._job_active_processes is winjob.job_active_processes


def test_the_cpu_reader_sums_user_and_kernel_time(monkeypatch):
    from kitlib import winjob

    class FakeKernel32:
        def QueryInformationJobObject(self, job, cls, info, size, returned):
            struct = info._obj
            struct.TotalUserTime = 12_500_000  # 1.25 s in 100 ns units
            struct.TotalKernelTime = 2_500_000  # 0.25 s
            return 1

    monkeypatch.setattr(winjob, "win32", lambda: (FakeKernel32(), None))
    assert winjob.job_cpu_seconds(object()) == 1.5
