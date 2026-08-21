"""TC-043 — the subagent spawn gate (SR-043 / LLR-040).

The gate is a Claude PreToolUse hook: OPT-IN, FAIL-OPEN fan-out supervision for
unattended runs, with the override held by the launcher (not the model), and
fail-open so a broken gate never wedges the agent's tools. Exercised two ways:
the pure `decide()` core directly, and `main()` end-to-end as the real hook
(JSON on stdin -> permissionDecision on stdout + exit code).

ABSENCE AND CORRUPTION ARE TESTED SEPARATELY (repo review 2026-08-19, M-13).
Only one of them is a policy: an absent dial means nobody asked for the gate
(`allow`), while a corrupt one means somebody did and the file broke -- and
since OI-46 ruled (1a) (2026-08-20, WI-491) those two routes no longer land on
the same decision either: a present-but-unparseable process.toml now asks
(fail-closed), aligned with the twin readers in check_trajectory.py /
gen_okf.py. Covering them with a single assertion is what let this module's
header claim "deny-by-default" for as long as it did -- nothing forced a
reader to look at what the failure paths actually do.
"""

import json
import subprocess
import sys

from conftest import SCRIPTS, load_script

gate = load_script("subagent_gate")


# --- pure decision core -------------------------------------------------------


def test_deny_policy_refuses_a_spawn():
    assert gate.decide("Task", "deny", "")[0] == "deny"
    assert gate.decide("Agent", "deny", "")[0] == "deny"


def test_ask_policy_defers_to_approval():
    assert gate.decide("Task", "ask", "")[0] == "ask"


def test_off_and_absent_allow():
    assert gate.decide("Task", "off", "")[0] == "allow"
    assert gate.decide("Task", "", "")[0] == "allow"  # absent policy file


def test_launcher_override_beats_deny():
    # The human-set env override wins even under the strictest policy.
    assert gate.decide("Task", "deny", "allow")[0] == "allow"


def test_non_spawn_tool_is_never_gated():
    assert gate.decide("Read", "deny", "")[0] == "defer"
    assert gate.decide("Bash", "deny", "")[0] == "defer"


def test_unrecognized_policy_asks_never_harder_than_deny():
    assert gate.decide("Task", "banana", "")[0] == "ask"


# --- main() as the real hook --------------------------------------------------


def run_hook(payload, cwd, env_extra=None):
    """Invoke the gate as Claude would: JSON on stdin, read stdout + exit code."""
    import os

    env = dict(os.environ)
    env["CLAUDE_PROJECT_DIR"] = str(cwd)
    if env_extra:
        env.update(env_extra)
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "subagent_gate.py")],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=str(cwd),
        env=env,
    )
    return proc


def _write_policy(root, value):
    (root / "docs").mkdir(exist_ok=True)
    (root / "docs" / "subagent-gate").write_text(value + "\n", encoding="utf-8")


def test_hook_denies_and_exits_2(tmp_path):
    _write_policy(tmp_path, "deny")
    proc = run_hook({"tool_name": "Task"}, tmp_path)
    assert proc.returncode == 2
    out = json.loads(proc.stdout)
    assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
    # the paper trail recorded the decision
    log = (tmp_path / "out" / "subagent-gate.log").read_text(encoding="utf-8")
    assert "Task\tdeny" in log


def test_hook_allows_when_off(tmp_path):
    _write_policy(tmp_path, "off")
    proc = run_hook({"tool_name": "Task"}, tmp_path)
    assert proc.returncode == 0
    assert (
        json.loads(proc.stdout)["hookSpecificOutput"]["permissionDecision"] == "allow"
    )


def test_hook_override_allows_under_deny(tmp_path):
    _write_policy(tmp_path, "deny")
    proc = run_hook({"tool_name": "Task"}, tmp_path, {"SUBAGENT_GATE": "allow"})
    assert proc.returncode == 0
    assert (
        json.loads(proc.stdout)["hookSpecificOutput"]["permissionDecision"] == "allow"
    )


def test_hook_defers_non_spawn_tool_silently(tmp_path):
    _write_policy(tmp_path, "deny")
    proc = run_hook({"tool_name": "Read"}, tmp_path)
    assert proc.returncode == 0
    assert proc.stdout.strip() == ""  # defer: no output, proceed normally


def test_hook_fails_open_on_malformed_payload(tmp_path):
    _write_policy(tmp_path, "deny")
    # Not JSON at all — the gate must allow (exit 0) and log the failure, never
    # wedge the tool on a broken payload.
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "subagent_gate.py")],
        input="this is not json",
        capture_output=True,
        text=True,
        cwd=str(tmp_path),
        env={**_env_with_root(tmp_path)},
    )
    assert proc.returncode == 0
    log = (tmp_path / "out" / "subagent-gate.log").read_text(encoding="utf-8")
    assert "failing open" in log


def _env_with_root(root):
    import os

    env = dict(os.environ)
    env["CLAUDE_PROJECT_DIR"] = str(root)
    return env


# --- absence vs corruption: the same `allow`, two different reasons -----------
#
# M-13's remaining half. `test_off_and_absent_allow` above covers the DECLARED
# `off` and the pure-absence route through `decide()`. These pin the policy
# READER's failure paths, which nothing exercised: a broken `process.toml` is
# not the same event as no `process.toml`, and the module documents a
# deliberate divergence from its twins about it.


def _write_process_toml(root, body):
    (root / "docs").mkdir(exist_ok=True)
    (root / "docs" / "process.toml").write_text(body, encoding="utf-8")


def test_absent_process_toml_reads_as_undeclared(tmp_path):
    # Nobody asked for the gate. None means "this file has nothing to say",
    # which is what sends main() on to the legacy one-word fallback.
    assert gate.read_process_policy(tmp_path) is None


def test_corrupt_process_toml_reads_unparseable_not_undeclared(tmp_path):
    # Somebody asked and the file broke. OI-46 ruled (1a), 2026-08-20 (WI-491):
    # this module now aligns with the twins in check_trajectory.py / gen_okf.py,
    # which read an unparseable process.toml as ON (loud) rather than
    # undeclared (quiet). Here "loud" is the UNPARSEABLE sentinel, which
    # decide() resolves to `ask` -- distinct from the plain `None` an absent
    # file returns, so main() does not fall through to the legacy file.
    _write_process_toml(tmp_path, "[checks\nsubagent_gate = ")
    assert gate.read_process_policy(tmp_path) is gate.UNPARSEABLE
    assert gate.decide("Task", gate.UNPARSEABLE, "")[0] == "ask"


def test_corruption_no_longer_falls_through_to_the_legacy_file(tmp_path):
    # Before OI-46, a corrupt process.toml fell through to the legacy file
    # (or, absent that too, a quiet `allow`) -- the ruled asymmetry. Now a
    # present-but-broken process.toml is TERMINAL and fails closed on its own,
    # the same way check_trajectory.py / gen_okf.py never consult a fallback
    # once their own reader reads ON: the legacy file's `deny` is not even
    # reached, and the corrupt dial itself asks rather than silently
    # deferring to whatever else is declared.
    _write_process_toml(tmp_path, "this is not toml {{{")
    _write_policy(tmp_path, "deny")
    proc = run_hook({"tool_name": "Task"}, tmp_path)
    assert proc.returncode == 0
    out = json.loads(proc.stdout)
    assert out["hookSpecificOutput"]["permissionDecision"] == "ask"


def test_garbled_policy_value_asks_and_is_never_a_quiet_off(tmp_path):
    # A non-string dial is RENDERED rather than dropped, so it reaches
    # `decide()`'s unrecognized arm and asks. The failure this forbids is the
    # quiet one: a garbled value on a fan-out guardrail reading as `off`.
    _write_process_toml(tmp_path, "[checks]\nsubagent_gate = 42\n")
    assert gate.read_process_policy(tmp_path) == "42"
    proc = run_hook({"tool_name": "Task"}, tmp_path)
    assert proc.returncode == 0
    out = json.loads(proc.stdout)
    assert out["hookSpecificOutput"]["permissionDecision"] == "ask"
