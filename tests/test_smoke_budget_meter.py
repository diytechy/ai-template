"""The smoke budget step's real CPU meters, read over stand-in tiers.

The in-process cases (tests/test_check_smoke_budget.py) stand the meter in.
These read the real one: on Windows the job the step creates and joins, on
POSIX `getrusage(RUSAGE_CHILDREN)`. On Windows the step joins its own process
to that job for good, so every case runs the step in a subprocess driver: a
short script that loads the step by path, points it at a temporary stack.ini
and a stand-in tier, and calls `main(["--mode", "warn"])`. The test reads
`CPU <x> s` off the verdict line. Every burn is a CPU burn (a loop until
`time.process_time()` reaches its target), never a sleep. This module is in
tests/conftest.py SLOW_MODULES: its cases start interpreters and burn CPU.
"""

import json
import re
import subprocess
import sys
import time
import uuid

import pytest
from conftest import ROOT, SCRIPTS

STEP = ROOT / "scripts" / "check_smoke_budget.py"

windows_only = pytest.mark.skipif(
    sys.platform != "win32", reason="job objects are Windows-only"
)
posix_only = pytest.mark.skipif(
    sys.platform == "win32", reason="getrusage is the POSIX meter"
)

BURN = (
    "import time\n"
    "def burn(seconds):\n"
    "    end = time.process_time() + seconds\n"
    "    while time.process_time() < end:\n"
    "        pass\n"
)

DRIVER = (
    "import importlib.util, pathlib, sys\n"
    "spec = importlib.util.spec_from_file_location('csb', {step!r})\n"
    "step = importlib.util.module_from_spec(spec)\n"
    "spec.loader.exec_module(step)\n"
    "step.STACK_INI = pathlib.Path({ini!r})\n"
    "step.smoke_argv = lambda cp: [sys.executable, {tier!r}]\n"
    "sys.exit(step.main(['--mode', 'warn']))\n"
)

# The stand-in tier: it burns, then starts and waits on a grandchild of the
# step that burns too.
GRANDCHILD_TIER = (
    BURN + "import subprocess, sys\n"
    "burn(0.5)\n"
    "subprocess.run([sys.executable, '-c', {grandchild!r}], check=True)\n"
)


def _driver(tmp_path, tier_source):
    """Write the stand-in tier, a stack.ini with roomy limits, and the
    driver; return the driver's argv."""
    tier = tmp_path / "tier.py"
    tier.write_text(tier_source, encoding="utf-8")
    ini = tmp_path / "stack.ini"
    ini.write_text(
        "[smoke-budget]\ncpu-seconds = 1000\nwall-seconds = 1000\nmax-tests = 1\n",
        encoding="utf-8",
    )
    driver = tmp_path / "driver.py"
    driver.write_text(
        DRIVER.format(step=str(STEP), ini=str(ini), tier=str(tier)),
        encoding="utf-8",
    )
    return [sys.executable, str(driver)]


def _cpu_reading(stdout):
    match = re.search(r"smoke budget: CPU (\d+(?:\.\d+)?) s", stdout)
    assert match, stdout
    return float(match.group(1))


def _read_grandchild_tier(tmp_path):
    grandchild = BURN + "burn(0.5)\n"
    argv = _driver(tmp_path, GRANDCHILD_TIER.format(grandchild=grandchild))
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return _cpu_reading(proc.stdout)


@windows_only
def test_a_windows_reading_counts_the_exited_grandchild(tmp_path):
    assert _read_grandchild_tier(tmp_path) >= 1.0


@posix_only
def test_a_posix_reading_counts_a_waited_grandchild(tmp_path):
    assert _read_grandchild_tier(tmp_path) >= 1.0


JOINED_JOB_DRIVER = (
    BURN + "import subprocess, sys\n"
    "sys.path.insert(0, {scripts!r})\n"
    "from kitlib import winjob\n"
    "job = winjob.create_joined_job()\n"
    "burn(0.4)\n"
    "subprocess.run([sys.executable, '-c', {child!r}], check=True)\n"
    "print(winjob.job_cpu_seconds(job))\n"
)


@windows_only
def test_a_joined_job_counts_an_exited_grandchild(tmp_path):
    # The driver burns, then waits on a child that waits on a burning
    # grandchild; both have exited when the driver reads its job.
    grandchild = BURN + "burn(0.4)\n"
    child = "import subprocess, sys\nsubprocess.run([sys.executable, '-c', {!r}], check=True)\n".format(
        grandchild
    )
    driver = tmp_path / "joined.py"
    driver.write_text(
        JOINED_JOB_DRIVER.format(scripts=str(SCRIPTS), child=child), encoding="utf-8"
    )
    proc = subprocess.run(
        [sys.executable, str(driver)], capture_output=True, text=True, timeout=120
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert float(proc.stdout.strip().splitlines()[-1]) >= 0.8


# The stand-in tier for the outside-process case: it applies the root
# conftest's cap under the environment the step gave it, then holds a ready
# file until the test writes a go file, and burns its own 0.3 s.
CAPPED_TIER = (
    BURN + "import importlib.util, os, sys, time, types\n"
    "stub = types.ModuleType('pytest')\n"
    "stub.hookimpl = lambda *a, **k: (lambda f: f)\n"
    "sys.modules['pytest'] = stub\n"
    "spec = importlib.util.spec_from_file_location('_root_conftest', {conftest!r})\n"
    "conftest = importlib.util.module_from_spec(spec)\n"
    "spec.loader.exec_module(conftest)\n"
    "conftest.JOB_NAME = {name!r}\n"
    "conftest._bound_windows(50)\n"
    "open({ready!r}, 'w').close()\n"
    "while not os.path.exists({go!r}):\n"
    "    time.sleep(0.02)\n"
    "burn(0.3)\n"
)

# The outsider, started by the test and so outside the step's job: it opens
# the conftest's job by name, tries to join it, and burns 1.0 s.
OUTSIDER = (
    BURN + "import ctypes, json, sys\n"
    "sys.path.insert(0, {scripts!r})\n"
    "from kitlib import winjob\n"
    "k32, _ = winjob.win32()\n"
    "job = k32.CreateJobObjectW(None, {name!r})\n"
    "existed = ctypes.get_last_error() == 183\n"
    "joined = bool(k32.AssignProcessToJobObject(job, k32.GetCurrentProcess()))\n"
    "burn(1.0)\n"
    "print(json.dumps({{'existed': existed, 'joined': joined}}))\n"
)

TIER_BURN = 0.3
STATED_MARGIN = 0.5


def _wait_for(path, proc, seconds=60):
    deadline = time.monotonic() + seconds
    while not path.exists():
        assert proc.poll() is None, proc.communicate()
        assert time.monotonic() < deadline, "the stand-in tier never got ready"
        time.sleep(0.02)


@windows_only
def test_an_outside_process_cannot_raise_a_reading(tmp_path):
    name = "ai-template-pytest-outsider-{}".format(uuid.uuid4().hex)
    ready, go = tmp_path / "ready", tmp_path / "go"
    tier = CAPPED_TIER.format(
        conftest=str(ROOT / "conftest.py"), name=name, ready=str(ready), go=str(go)
    )
    driver = subprocess.Popen(
        _driver(tmp_path, tier),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        _wait_for(ready, driver)
        outsider = subprocess.run(
            [sys.executable, "-c", OUTSIDER.format(scripts=str(SCRIPTS), name=name)],
            capture_output=True,
            text=True,
            timeout=120,
        )
    finally:
        go.touch()
    out, err = driver.communicate(timeout=120)
    assert outsider.returncode == 0, outsider.stdout + outsider.stderr
    seen = json.loads(outsider.stdout.strip().splitlines()[-1])
    assert driver.returncode == 0, out + err
    assert not seen["existed"], "the tier's cap job was open to the outsider by name"
    assert _cpu_reading(out) < TIER_BURN + STATED_MARGIN, out
