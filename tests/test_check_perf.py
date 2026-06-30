"""check_perf.py: the kit-owned, stdlib comparator for performance budgets
(process.md §9). It compares product-emitted metrics against the budgets
registry + a committed baseline — absolute breach and regression — gating only
hard (Gate=fail) breaches in the run tier, and degrades to a skip when metrics
or budgets are absent.
"""

import json

from conftest import load_script, make_minimal_project, run_py

PB_HEADER = "PB-ID,Metric,Refs,Budget,Unit,Tolerance,Direction,Tier,Gate,Owner,Notes\n"


def pb_row(
    pid,
    budget,
    tol="10%",
    direction="lower-better",
    tier="Full",
    gate="fail",
    refs="SR-001",
):
    return "{},Metric {},{},{},MiB,{},{},{},{},Integration,note\n".format(
        pid, pid, refs, budget, tol, direction, tier, gate
    )


def write_budgets(root, *rows):
    (root / "docs" / "requirements" / "performance-budgets.csv").write_text(
        PB_HEADER + "".join(rows), encoding="utf-8"
    )


def write_metrics(root, data):
    (root / "docs" / "test" / "perf-metrics.json").write_text(
        json.dumps(data), encoding="utf-8"
    )


def write_baseline(root, data):
    (root / "docs" / "test" / "perf-baseline.json").write_text(
        json.dumps(data), encoding="utf-8"
    )


def perf_report(root):
    return (root / "docs" / "test" / "perf-report.md").read_text(encoding="utf-8")


# --- CLI behavior on a real scaffold -----------------------------------------


def test_no_real_budgets_passes(scaffold):
    # A fresh scaffold has only the PB-000 placeholder -> nothing to compare.
    proc = run_py(["scripts/check_perf.py"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "no performance budgets" in proc.stdout


def test_budgets_present_but_no_metrics_skips(scaffold):
    write_budgets(scaffold, pb_row("PB-001", 500))
    proc = run_py(["scripts/check_perf.py", "--tier", "full"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SKIP" in proc.stdout and "no metrics" in proc.stdout


def test_absolute_breach_fails_when_gate_fail(scaffold):
    write_budgets(scaffold, pb_row("PB-001", 500, gate="fail", tier="Full"))
    write_metrics(scaffold, {"PB-001": 560})
    proc = run_py(["scripts/check_perf.py", "--tier", "full"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "FAIL" in proc.stdout and "PB-001" in proc.stdout
    assert "exceeds budget 500MiB" in perf_report(scaffold)


def test_absolute_breach_only_warns_when_gate_warn(scaffold):
    write_budgets(scaffold, pb_row("PB-001", 500, gate="warn", tier="Full"))
    write_metrics(scaffold, {"PB-001": 560})
    proc = run_py(["scripts/check_perf.py", "--tier", "full"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARN" in proc.stdout


def test_within_tolerance_regression_passes(scaffold):
    write_budgets(scaffold, pb_row("PB-001", 1000, tol="10%", gate="fail"))
    write_baseline(scaffold, {"PB-001": 500})
    write_metrics(scaffold, {"PB-001": 540})  # +8% < 10%, and well under budget
    proc = run_py(["scripts/check_perf.py", "--tier", "full"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "OK" in proc.stdout


def test_regression_beyond_tolerance_fails_when_gate_fail(scaffold):
    # Under the absolute budget (1000) but +20% over baseline 500 (> 10% band).
    write_budgets(scaffold, pb_row("PB-001", 1000, tol="10%", gate="fail"))
    write_baseline(scaffold, {"PB-001": 500})
    write_metrics(scaffold, {"PB-001": 600})
    proc = run_py(["scripts/check_perf.py", "--tier", "full"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "regressed vs baseline 500MiB" in perf_report(scaffold)


def test_tier_scopes_which_budgets_gate(scaffold):
    # A Release-tier Gate=fail breach is out of scope at full (passes) and in
    # scope at release (fails) — size gates at full, runtime warns at release.
    write_budgets(scaffold, pb_row("PB-001", 500, tier="Release", gate="fail"))
    write_metrics(scaffold, {"PB-001": 560})
    at_full = run_py(["scripts/check_perf.py", "--tier", "full"], cwd=scaffold)
    assert at_full.returncode == 0, at_full.stdout + at_full.stderr
    at_release = run_py(["scripts/check_perf.py", "--tier", "release"], cwd=scaffold)
    assert at_release.returncode == 1, at_release.stdout + at_release.stderr


def test_update_baseline_writes_file(scaffold):
    write_budgets(scaffold, pb_row("PB-001", 500))
    write_metrics(scaffold, {"PB-001": 488, "PB-002": 12})
    proc = run_py(["scripts/check_perf.py", "--update-baseline"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    saved = json.loads(
        (scaffold / "docs" / "test" / "perf-baseline.json").read_text(encoding="utf-8")
    )
    assert saved == {"PB-001": 488.0, "PB-002": 12.0}


def test_harness_runs_perf_at_g3(scaffold):
    # A hard-gated breach must fail the G3 gate through check.py's perf step.
    make_minimal_project(scaffold)
    write_budgets(scaffold, pb_row("PB-001", 500, gate="fail", tier="Full"))
    write_metrics(scaffold, {"PB-001": 560})
    proc = run_py(["scripts/check.py", "--gate", "G3", "--tier", "full"], cwd=scaffold)
    assert proc.returncode != 0
    assert "perf-budgets" in proc.stdout
    assert "RESULT: FAIL" in proc.stdout


def test_perf_step_is_process_layer_in_list(scaffold):
    proc = run_py(["scripts/check.py", "--gate", "G3", "--list"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert any(
        "perf-budgets" in ln and "[process]" in ln for ln in proc.stdout.splitlines()
    )


# --- importable units (no subprocess) ----------------------------------------


def test_evaluate_covers_absolute_regression_tier_and_skip():
    check = load_script("check_perf")
    budgets = [
        # lower-better, over budget, Gate=fail, Full tier
        {
            "PB-ID": "PB-1",
            "Budget": "500",
            "Unit": "MiB",
            "Tolerance": "10%",
            "Direction": "lower-better",
            "Tier": "Full",
            "Gate": "fail",
        },
        # higher-better, below budget, Gate=warn
        {
            "PB-ID": "PB-2",
            "Budget": "1000",
            "Unit": "ops",
            "Tolerance": "5%",
            "Direction": "higher-better",
            "Tier": "Full",
            "Gate": "warn",
        },
        # Release tier -> out of scope at full
        {
            "PB-ID": "PB-3",
            "Budget": "10",
            "Unit": "GiB",
            "Tolerance": "5%",
            "Direction": "lower-better",
            "Tier": "Release",
            "Gate": "fail",
        },
        # No measurement -> SKIP
        {
            "PB-ID": "PB-4",
            "Budget": "100",
            "Unit": "MiB",
            "Tolerance": "10%",
            "Direction": "lower-better",
            "Tier": "Full",
            "Gate": "fail",
        },
    ]
    metrics = {"PB-1": 560, "PB-2": 900, "PB-3": 99}
    results = {r["pid"]: r for r in check.evaluate(budgets, metrics, {}, "full")}
    assert results["PB-1"]["status"] == "FAIL"  # absolute breach, gate fail
    assert results["PB-2"]["status"] == "WARN"  # higher-better breach, gate warn
    assert "PB-3" not in results  # release row not in scope at full
    assert results["PB-4"]["status"] == "SKIP"  # no metric


def test_regression_uses_direction_and_tolerance():
    check = load_script("check_perf")
    row = {
        "PB-ID": "PB-1",
        "Budget": "",
        "Unit": "MiB",
        "Tolerance": "10%",
        "Direction": "lower-better",
        "Tier": "Full",
        "Gate": "fail",
    }
    base = {"PB-1": 500}
    # +8% is inside the band; +20% is outside.
    assert check.evaluate([row], {"PB-1": 540}, base, "full")[0]["status"] == "OK"
    assert check.evaluate([row], {"PB-1": 600}, base, "full")[0]["status"] == "FAIL"
    # No baseline -> regression can't be computed (and no budget) -> OK.
    assert check.evaluate([row], {"PB-1": 600}, {}, "full")[0]["status"] == "OK"


def test_parse_tolerance_and_in_tier():
    check = load_script("check_perf")
    assert check.parse_tolerance("10%") == ("pct", 0.10)
    assert check.parse_tolerance("5") == ("abs", 5.0)
    assert check.parse_tolerance("") is None
    assert check.in_tier("Full", "full") is True
    assert check.in_tier("Release", "full") is False
    assert check.in_tier("Release", "all") is True
    assert check.in_tier("", "smoke") is False  # blank defaults to Full


def test_update_baseline_merges_and_preserves(tmp_path):
    check = load_script("check_perf")
    baseline = tmp_path / "perf-baseline.json"
    baseline.write_text(json.dumps({"PB-1": 100.0, "PB-9": 9.0}), encoding="utf-8")
    changes = check.update_baseline(baseline, {"PB-1": 120.0, "PB-2": 5.0})
    saved = json.loads(baseline.read_text(encoding="utf-8"))
    # PB-1 updated, PB-2 added, PB-9 (not measured) preserved.
    assert saved == {"PB-1": 120.0, "PB-2": 5.0, "PB-9": 9.0}
    assert ("PB-1", 100.0, 120.0) in changes


# --- release checklist surfacing (process.md §9) -----------------------------


def test_release_checklist_lists_perf_budgets(scaffold):
    # The warn-tier runtime budgets never fail the gate, so the human release
    # checklist is where they get a tick-box (gen_release_checklist.py §9).
    write_budgets(scaffold, pb_row("PB-001", 512, gate="warn", tier="Release"))
    proc = run_py(["scripts/gen_release_checklist.py"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PB=1" in proc.stdout
    checklist = (scaffold / "docs" / "release-checklist.md").read_text(encoding="utf-8")
    assert "Performance budgets within allocation" in checklist
    assert "PB-001" in checklist and "≤ 512MiB" in checklist
