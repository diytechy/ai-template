"""TC-204 (CLI half) — the SR-163 mapping-purpose checker driven as a subprocess.

The in-process unit module (test_mapping_purpose.py) grades the checker's
functions directly and stays in the commit smoke bar, where it is cheap. This
module drives the SHIPPED `gen_arch_map.py --mapping-purpose` command the way an
adopter's `stack.ini` would — a real interpreter subprocess — so a regression
that unwired the CLI mode is caught end-to-end: were the checker left defined but
reachable only from the test suite, adding an unmapped/unresolved/missing/stale
inventory entry in a real repo would produce no SR-163 report or gate, and these
assertions would fail. Kept SEPARATE and re-tiered into conftest.SLOW_MODULES for
the same reason test_check_complexity_cli.py is: each case pays interpreter
startup, so it is the subprocess-dominated class the per-commit bar drops and the
slice/phase-close + CI run exercises in full.
"""

from pathlib import Path

from conftest import ROOT, load_script, run_py

gen_arch_map = load_script("gen_arch_map")

_GAM = Path(gen_arch_map.__file__)


def test_cli_mapping_purpose_is_green_over_the_real_repo():
    # Warn-first: the real inventory carries warn-class rows (the burn-down) but
    # no gate-class finding, so the delivered command exits 0 and reports every
    # class on stdout.
    got = run_py([_GAM, "--mapping-purpose", "--root", str(ROOT)], cwd=ROOT)
    assert got.returncode == 0, got.stderr
    out = got.stdout + got.stderr
    for cls in gen_arch_map.MAPPING_FINDING_POLICY:
        assert "mapping purpose: {} —".format(cls) in out
    assert "unmapped_file" in out  # the burn-down remainder is reported, not hidden


def test_cli_mapping_purpose_gates_when_destinations_are_absent(tmp_path):
    # Point --root at a root missing every declared destination: the checker's
    # gate-class `missing_file` arm fires, so the shipped command exits 1 and the
    # report lands on stderr. The end-to-end proof the gate is WIRED — the same
    # delivered path a real missing/stale defect would trip.
    red = run_py([_GAM, "--mapping-purpose", "--root", str(tmp_path)], cwd=tmp_path)
    assert red.returncode == 1
    assert "GATE" in red.stderr and "missing_file" in red.stderr
