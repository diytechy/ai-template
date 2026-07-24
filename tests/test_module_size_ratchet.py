"""The no-new-monolith ratchet — repo-review-2026-07-22 H-2 (growth sensor).

The per-function complexity ratchet (test_complexity_ratchet.py) freezes how
hard any one function is to read. This is its file-scale sibling: it freezes how
large the kit's biggest scripts are, so the six coordinators the 2026-07-22 deep
review flagged as "beyond maintainable review scale" cannot silently grow while
the real decomposition (WI-280) is deferred.

Any kit script whose line count exceeds THRESHOLD must have an EXACT baseline
entry below. The census may only tighten by default:

- A baselined module grew, or a NEW module crossed THRESHOLD without a baseline:
  the fix is DECOMPOSITION (WI-280), not a baseline bump. A deliberate bump is a
  reviewed baseline edit whose reason lands in the WI/session log — never a
  drive-by. Moving lines into a new module is exactly the intended escape hatch:
  the new module stays under THRESHOLD (or earns its own reviewed baseline) and
  the shrunk one re-stamps downward.
- A module improved below its baseline (or dropped under THRESHOLD, or was
  renamed/removed): re-stamp its entry downward — or delete it — in the same
  commit, so the ratchet only ever tightens.

This is a growth SENSOR, not an approval of the current sizes. WI-280 is the
scoped decomposition that pays this debt down; every entry here is active
architectural debt, not a target.
"""

import pathlib

from conftest import SCRIPTS

# A module larger than this must be baselined. Set above agent_common.py (1223)
# / agent_route.py (1181) so only the six coordinators the review named are
# frozen; a routine edit to a mid-size script does not trip the ratchet, but a
# mid-size script growing into a new monolith does.
THRESHOLD = 1500

# Measured 2026-07-22 (len(text.splitlines()); files end with a newline, so this
# equals `wc -l`). These six are the review's H-2 modules, unchanged since the
# as-found `6a752b4`. Re-stamp DOWNWARD as WI-280 decomposes them.
BASELINE = {
    # +76 (4511 -> 4587), WI-284: the generated Ready-frontier block — the
    # scheduler-derived forward-looking WI list that makes the forward-only
    # cascade structurally impossible (a `done` WI can't linger in status.md).
    # New behaviour, not monolith drift (the reviewed-bump escape the ratchet
    # documents; reason in docs/log.md 2026-07-23). Re-stamp downward with WI-280.
    "gen_trajectory.py": 4587,
    # +11 (3452 -> 3463), WI-284: _regenerate_disposition_artifacts also runs
    # `gen_trajectory.py --status` at integrate/blocked-disposition so a closed
    # id drops from the generated frontier automatically (and the disposition
    # passes its own status-map floor — WI-283's core). Reviewed bump, log 2026-07-23.
    # +70 (3463 -> 3533), WI-287: the integrator's spec close-ritual at done-flip
    # (_wi_specrefs + _archive_closed_specs + the SpecRef='' clear) so a terminal
    # WI clears its SpecRef and archives its spec — no more stranded R-F debt.
    # New behaviour, reviewed bump (log 2026-07-23). Re-stamp downward with WI-280.
    # -1 (3533 -> 3532), WI-285: _run_combined_bar delegates stack.ini
    # test-command resolution to agent_common._declared_test_command (logic moved
    # OUT to that CMP-004 shared-primitives module — no CMP-004→CMP-001 check
    # import) and drops the now-unused `import shlex` — a tightening re-stamp.
    "agent_dispatch.py": 3532,
    "agent_loop.py": 3034,
    "trace.py": 2206,
    "check_trajectory.py": 1926,
    # +1 (1916 -> 1917), WI-279: one MAPPING row registering the new
    # scripts/check_coverage.py kit gate so it ships downstream — a required
    # one-line registration, not monolith growth (the reviewed-bump escape the
    # ratchet documents; not a drive-by). Re-stamp downward with WI-280.
    "bootstrap.py": 1917,
}


def _census():
    """{module_name: line_count} for every kit script over THRESHOLD."""
    census = {}
    for path in sorted(pathlib.Path(SCRIPTS).glob("*.py")):
        lines = len(path.read_text(encoding="utf-8").splitlines())
        if lines > THRESHOLD:
            census[path.name] = lines
    return census


def test_module_sizes_exactly_match_the_committed_baseline():
    census = _census()
    grew = {
        name: (BASELINE.get(name), lines)
        for name, lines in census.items()
        if lines > BASELINE.get(name, 0)
    }
    improved = {
        name: (baseline, census.get(name))
        for name, baseline in BASELINE.items()
        if census.get(name, 0) < baseline
    }
    message = []
    if grew:
        message.append(
            "module(s) grew past baseline — decompose (WI-280), do not bump "
            "(a deliberate bump is a reviewed baseline edit, reason in the log): "
            + "; ".join(
                "{} baseline {} -> now {}".format(
                    name, base or "absent (new monolith)", now
                )
                for name, (base, now) in sorted(grew.items())
            )
        )
    if improved:
        message.append(
            "module(s) shrank below baseline — re-stamp these entries downward "
            "(or delete them if now <= {}) in this same commit: ".format(THRESHOLD)
            + "; ".join(
                "{} baseline {} -> now {}".format(
                    name, base, now if now else "under {}".format(THRESHOLD + 1)
                )
                for name, (base, now) in sorted(improved.items())
            )
        )
    assert not message, "\n".join(message)
