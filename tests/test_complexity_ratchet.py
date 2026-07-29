"""The no-new-complexity ratchet — WI-225 (repo-review-2026-07-18 H-02, slice A).

The per-function C901 census of the kit scripts must EXACTLY match the
committed baseline below (measured 2026-07-18; the census had grown
50 -> 51 -> 52 across well-reviewed remediation passes because nothing
failed on it).

When this test fails:

- A function grew past its baseline, or a new over-limit function appeared:
  the fix is SIMPLIFICATION, not a baseline bump. A deliberate bump is a
  reviewed baseline edit whose reason lands in the WI/session log — never a
  drive-by.
- A function improved below its baseline (or was renamed/removed): re-stamp
  its entry downward — or delete it — in the same commit, so the ratchet
  only ever tightens by default.

WI-226 completed the first dispatcher split; the remaining baseline is active
architectural debt and any further decomposition needs its own scoped WI.
"""

import os
import re
import subprocess
import sys

import pytest
from conftest import SCRIPTS

pytestmark = pytest.mark.skipif(
    __import__("importlib").util.find_spec("ruff") is None,
    reason="needs ruff (dev dependency)",
)

# Pinned explicitly so the ratchet cannot drift with ruff's defaults.
MAX_COMPLEXITY = 10

BASELINE = {
    ("agent_common.py", "preflight"): 17,
    # (The agent_dispatch.py rows retired with the module at
    # concurrency-restructure Phase 5.)
    # Repo-review 2026-07-21 reviewed bumps (each +1..+3, all fail-closed
    # guards from that review's fix pass — reasons at the marked call sites):
    # agent_loop main gained the M-20 malformed-policy warnings;
    # route_session the M-22 verdict-pre-plant unlinks; session_bookkeeping
    # the H-1 unparseable-verdict fail-closed branches; load_registry the H-4
    # Model-slug refusal; run_session the H-2 interrupt kill-tree handler;
    # sync_agent_skills the M-14 orphan-deletion sweep; run_dual_plan_round
    # the L-29 unfileable-plan PAGE guard.
    ("agent_loop.py", "critique_brief"): 11,
    ("agent_loop.py", "main"): 27,
    ("agent_loop.py", "map_preflight"): 19,
    ("agent_loop.py", "route_intent"): 13,
    # WI-345: 13 -> 11. Both managed arms lost their inline
    # exists/read/parse-verdict branch to `read_verdict`, so the tier decision is
    # all that is left here. Re-stamped DOWNWARD, which is the direction this
    # ratchet exists to hold.
    ("agent_loop.py", "route_session"): 11,
    ("agent_loop.py", "run_iteration"): 23,
    ("agent_loop.py", "session_bookkeeping"): 31,
    ("agent_route.py", "load_registry"): 17,
    ("agent_session.py", "run_session"): 14,
    ("bootstrap.py", "main"): 41,
    ("bootstrap.py", "sync_agent_skills"): 13,
    ("bootstrap.py", "strip_markers"): 14,
    # extra_steps dropped under the limit (WI-279 lifted its [step:] section
    # scan into the shared _step_sections helper) — entry deleted per the
    # ratchet's improvement rule (re-stamp/delete downward in the same commit).
    ("check.py", "main"): 16,
    # `findings_for` dropped under the limit, WI-062: the untraced/dangling
    # classification went OUT to `path_findings` rather than adding three
    # branches to the file walk — decomposition, the escape the ratchet prefers,
    # so the new tier cost this function nothing. Entry deleted per the
    # improvement rule (re-stamp or delete downward in the same commit).
    # WI-322: S-3's brief source moved from a markdown heading parse to the
    # open-items registry, which adds one read + one guard branch and crosses the
    # census threshold. Reviewed entry, log 2026-07-26.
    ("check_docs.py", "check_status_surface"): 13,
    ("check_docs.py", "check_links"): 13,
    ("check_docs.py", "git_commit_lookup"): 12,
    ("check_flows.py", "main"): 12,
    ("check_privacy.py", "main"): 11,
    ("check_privacy.py", "scan_diff_text"): 14,
    ("check_privacy.py", "scan_line"): 13,
    # WI-344 (2026-07-28): `critique_ratchet_findings` (11) and `staged_findings`
    # (12) are DELETED, not bumped — extracting the staged-close preamble
    # (`_staged_wi_registry` / `_newly_closed`) and the chain-touched tail
    # (`_chain_untouched`) dropped both under the limit. This is the direction
    # the ratchet exists to hold: it tightens by default.
    ("check_trajectory.py", "cross_component_findings"): 12,
    ("check_trajectory.py", "interface_findings"): 23,
    # WI-352 reviewed bump 21 -> 22, +1: the completion reconciler is
    # deliberately split across TWO tiers (spec evidence gates, trailer evidence
    # only warns), so main() needs one warn loop beside the gated extend. Folding
    # it into the existing dispatch loop would promote the trailer signal to an
    # error under --strict, which is precisely the deviation the WI argues
    # against. The tier DECISION itself was moved out to
    # `tier_completion_findings` rather than being written as two more branches
    # here — the simplification the ratchet prefers, applied as far as it goes.
    ("check_trajectory.py", "main"): 22,
    # WI-316 (2026-07-26): the amend-without-flip warn — HEAD-vs-index row
    # compare across three registries with owning-SR suppression (the
    # attestation unit sanctions same-commit amend+flip). New guard, reason in
    # the log; a WI-280 decomposition candidate.
    ("check_trajectory.py", "staged_spine_findings"): 20,
    ("gen_arch_map.py", "build_dependency_diagram"): 14,
    ("gen_arch_map.py", "main"): 17,
    ("gen_cases.py", "all_pairs"): 13,
    ("gen_cases.py", "main"): 12,
    ("gen_okf.py", "_doc_title_and_summary"): 13,
    # -4 (29 -> 25), WI-328: the LLR's new Rationale column would have been the
    # FIFTH `if cell: body.append("**Label.** ...")` inside emit, and the ratchet
    # caught it at +1. Extracted as the `field()` helper — the `links()` sibling
    # for plain cells — which removed all five branches instead of adding one.
    # The emitted bundle is byte-identical, so this is a pure shape change.
    ("gen_okf.py", "emit"): 25,
    ("gen_okf.py", "main"): 13,
    ("gen_release_checklist.py", "main"): 20,
    ("gen_trajectory.py", "_okf_nodes"): 15,
    # +3 (20 -> 23), WI-306: the start-collapsed SN root layer above the >3 rule
    # (the T2 density fix) - the panel() extraction plus the tiered branch. A
    # WI-280 decomposition candidate: panel/draw are an extractable unit.
    ("gen_trajectory.py", "arch_icicle"): 23,
    ("gen_trajectory.py", "sw_containment"): 28,
    ("gen_trajectory.py", "when_view"): 15,
    ("plan_coverage.py", "check_plan"): 17,
    ("plan_coverage.py", "main"): 12,
    ("plan_round.py", "record"): 29,
    ("plan_runner.py", "dispatch"): 16,
    ("plan_runner.py", "run_dual_plan_round"): 30,
    # WI-259 reviewed bump 50 -> 53: the verification-basis split went binary ->
    # three-way (mechanized/demonstrated/attested, a new elif branch) and
    # --require-verified was widened to every ratified SR of any method, naming
    # the real method in the finding. Trace decomposition remains a follow-up;
    # the added branches are the honest audit surface.
    # 53 -> 50, WI-065: the TC-`Verifies` rules moved OUT to
    # `tc_citation_findings`, so widening the vocabulary to `IF-###` cost this
    # function nothing and paid three branches back. The escape the ratchet
    # actually prefers — decomposition, not a bump — taken on the very function
    # the WI-259 note above called a follow-up.
    ("trace.py", "analyze"): 50,
    # WI-328/329: six measured form rules over three registries, now homed in the
    # extracted text layer. Flat and table-driven — the branches are the RULES, so
    # collapsing them would hide which rule fired from the message a reader acts on.
    ("trace_text.py", "form_findings"): 14,
    ("trace.py", "mermaid_graph"): 17,
    # 28 -> 27: the L-3 ratify bucketing removed a nested scan (re-stamped
    # downward per the ratchet's improvement rule).
    ("trace.py", "ratify_lines"): 27,
    # WI-316 (2026-07-26): the two new spine-status surfaces — the
    # orphaned-Modified-child warn (SR/LLR/TC owner resolution) and the
    # re-attestation brief emitter (per-SR baseline walk + chain diff +
    # ADDED/REMOVED sections + off-git degrade). New capability, reasons in
    # the log; the brief emitter is a named WI-280 extraction candidate.
    # +2 each (fix pass, 2026-07-26): F8 ownerless-child branches and the F1
    # --since fail-fast guard — both adversarial-review closures.
    ("trace.py", "modified_chain_advisories"): 15,
    # WI-322 split the git archaeology out of the renderer: reattest_lines went
    # prose-only (25 -> 14) and the extracted model carries the branching (21) —
    # one computation, two renderers. WI-347 then took it UNDER the limit
    # entirely (`_full_row_bullets` absorbed the two whole-row render arms), so
    # its entry is DELETED rather than re-stamped, which is what this ratchet
    # asks for once a function drops below THRESHOLD.
    ("trace.py", "reattest_model"): 21,
    ("trace.py", "render_report"): 17,
}

_C901 = re.compile(
    r"^(?P<path>.+?):\d+:\d+: C901 `(?P<name>.+?)` is too complex "
    r"\((?P<complexity>\d+) > \d+\)"
)


def _census():
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "ruff",
            "check",
            "--select",
            "C901",
            "--config",
            "lint.mccabe.max-complexity={}".format(MAX_COMPLEXITY),
            "--output-format",
            "concise",
            "--no-cache",
            str(SCRIPTS),
        ],
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    # 0 = no findings, 1 = findings; anything else is a broken invocation.
    assert proc.returncode in (0, 1), proc.stdout + proc.stderr
    census = {}
    for line in proc.stdout.splitlines():
        match = _C901.match(line.strip())
        if not match:
            continue
        rel = os.path.relpath(match.group("path"), str(SCRIPTS)).replace("\\", "/")
        key = (rel, match.group("name"))
        census[key] = max(census.get(key, 0), int(match.group("complexity")))
    return census


def test_c901_census_exactly_matches_the_committed_baseline():
    census = _census()
    grew = {
        key: (BASELINE.get(key), value)
        for key, value in census.items()
        if value > BASELINE.get(key, 0)
    }
    improved = {
        key: (value, census.get(key))
        for key, value in BASELINE.items()
        if census.get(key, 0) < value
    }
    message = []
    if grew:
        message.append(
            "complexity grew — simplify these (a deliberate bump is a reviewed "
            "baseline edit, reason in the log): "
            + "; ".join(
                "{}:{} baseline {} -> now {}".format(f, n, b or "absent", v)
                for (f, n), (b, v) in sorted(grew.items())
            )
        )
    if improved:
        message.append(
            "complexity improved below baseline — re-stamp these entries "
            "downward (or delete them) in this same commit: "
            + "; ".join(
                "{}:{} baseline {} -> now {}".format(
                    f, n, b, v if v else "under {}".format(MAX_COMPLEXITY + 1)
                )
                for (f, n), (b, v) in sorted(improved.items())
            )
        )
    assert not message, "\n".join(message)
