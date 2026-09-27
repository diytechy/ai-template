#!/usr/bin/env python3
"""check_assumption_gate.py — the assumption gate's four check steps.

    python scripts/check_assumption_gate.py --step <step> [--root .]

WHAT IT GATES. A requirement states what the system does at its own boundary;
the claim about the world that carries it to a stakeholder's need is an
assumption row it cites, or a `Coincident` waiver saying its own specification
is the outcome. The traceability check REPORTS where that argument is missing.
With `docs/process.toml` `[checks] assumption_gate = true`, these steps FAIL
on it instead, each at the rung where the question can first be answered
honestly (`check.py` places them):

  assumption-gate       DevStg-Boundary  each requirement not recorded
                                          coincident cites approved, active
                                          assumptions that reach its
                                          stakeholders (SR-205)
  crossing-allocation   DevStg-Boundary  each interface-form requirement's
                                          crossings are coincident or bridged
                                          by a cited assumption landing on
                                          them (SR-212's Boundary arm)
  interface-allocation  DevStg-Arch      each interface-form requirement is
                                          reached by a boundary interface, and
                                          each reaching one is coincident or
                                          bridged by a cited assumption
                                          (SR-212's Arch arm)
  assumption-evidence   DevStg-Release   each relied-on assumption has current
                                          evidence that supports a positive
                                          claim, or an accepted risk that has
                                          not reopened (SR-206)

WHY OFF MEANS ADVISORY, NOT SILENT. With the setting absent or off the step
prints the same findings as advisories and passes, so a project weighing the
gate sees exactly what turning it on would fail before it does.

WHAT IT NEVER TOUCHES. The findings are the step's alone: the derived stage
never reads them and its single release producer stays the harness evidence
verdict (spine map D16). The rules are `assumption_rules.py`'s, pure; this
module reads the registries, the observation records and the approval acts
once, and hands them in.

Implements: SR-205, SR-206, SR-212, LLR-242, LLR-243, LLR-244

Contracts: IF-230 — the seam this module declares (process.md §8; row of record
in docs/requirements/interfaces.toml).

Contract IF-230: the assumption gate's steps, as a command.
    `check_assumption_gate.py --step <STEPS member> [--root <dir>]` prints one
    line per finding, `FAIL: <finding>` with the gate on (`[checks]
    assumption_gate = true`) or `ADVISORY: <finding>` otherwise, then a summary
    line naming the step, and exits 1 when a finding FAILS, else 0. It reads
    the registries under `<root>/docs`, and for `assumption-evidence` the
    observation records, the suite's evidence record and the approval acts
    accepting risks; it writes nothing. `check.py` runs it as the built-in
    steps of the same names.

Python 3.11+, stdlib only; Windows + POSIX.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import assumption_rules as rules  # noqa: E402
import record_observation  # noqa: E402
import trace  # noqa: E402
from kitlib import config as kitconfig  # noqa: E402

# The four steps, in ladder order; `check.py` names each a built-in step.
# Implements: SR-205, LLR-242
STEPS = (
    "assumption-gate",
    "crossing-allocation",
    "interface-allocation",
    "assumption-evidence",
)


def _evidence_findings(root, reg):
    """SR-206's findings: the evidence levels, the current passing cases and
    each accepted risk's reading, read once, then judged. Read whatever the
    frame declares: SR-206 exempts no project from the release gate, so an
    evidencing case's inputs are digested with no crossing declared too."""
    ev = record_observation.evidence_inputs(
        root, reg.tcs, reg.das, reg.bifs, framed=True
    )
    reads = (ev["records"], ev["suite_proof"], ev["digests"])
    levels = {d["DA-ID"]: rules.evidence_level(d, reg.tcs, *reads) for d in reg.das}
    current = [t for t in reg.tcs if rules.result_current(t, *reads)]
    # The risk is read as though nothing evidenced the assumption: the gate
    # consults it only once the evidence has not counted.
    risks = {
        d["DA-ID"]: rules.accepted_risk_state(
            d,
            rules.LEVEL_SPECIFIED,
            ev["views"].get(d["DA-ID"]),
            reg.sn_needs,
            reg.tcs,
            ev["records"],
        )
        for d in reg.das
    }
    return rules.release_gate_findings(reg.das, reg.srs, levels, risks, current)


def step_findings(root, step):
    """The findings `step` reports for the project at `root`.

    Implements: SR-205, SR-206, SR-212, LLR-242, LLR-243, LLR-244
    """
    reg = trace.load_registries(Path(root) / "docs")
    if step == "assumption-gate":
        reach = rules.reach_gaps(
            reg.das, reg.srs, reg.sn_needs, reg.stks, reg.exts, reg.bifs, reg.surs
        )
        return rules.boundary_gate_findings(
            reg.srs, reg.das, reg.surs, reach, bool(reg.bifs)
        )
    if step == "crossing-allocation":
        return rules.crossing_gate_findings(reg.srs, reg.das, reg.bifs)
    if step == "interface-allocation":
        return rules.interface_form_gate_findings(reg.srs, reg.ifs, reg.llrs)
    return _evidence_findings(root, reg)


def main(argv=None):
    """The command: judge one step and print it as failures or advisories.

    Implements: SR-205, LLR-242
    """
    kitconfig.utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--step", required=True, choices=STEPS, help="the step to run")
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    args = ap.parse_args(argv)
    root = Path(args.root)
    enabled = kitconfig.assumption_gate_enabled(root / "docs")
    findings = step_findings(root, args.step)
    kind = "FAIL" if enabled else "ADVISORY"
    for line in findings:
        print("{}: {}".format(kind, line))
    print(
        "{}: {} finding(s), the assumption gate is {}{}".format(
            args.step,
            len(findings),
            "on" if enabled else "off",
            "" if enabled else " ([checks] assumption_gate), so none fails",
        )
    )
    return 1 if enabled and findings else 0


if __name__ == "__main__":
    sys.exit(main())
