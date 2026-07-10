#!/usr/bin/env python3
"""Subagent spawn gate — deny-by-default fan-out control for unattended runs.

A Claude Code `PreToolUse` hook (SR-043; realizes SN-006 "a walk-away run stays
safe" + SN-012 "opt-in"). During an unattended coordinator run a driver session
can spawn subagents freely, which multiplies cost and loosens oversight; this
gate refuses or defers each spawn per a declared policy, with the override held
by the human who launched the run — not the model.

**Supervision, not security** (stated honestly, like every hook in this kit): a
model that can edit files can remove this. It is a bounded-fan-out guardrail for
an unattended run, not a sandbox.

Policy — `docs/subagent-gate`, first declared line (the shared declared-policy
parse): `off` (or absent) allows everything, `ask` defers each spawn to
approval, `deny` refuses. The env override `SUBAGENT_GATE=allow` — set in the
launcher environment, which the model cannot write — bypasses the gate for a
deliberately-supervised run.

**Fail open with a paper trail:** any error (unreadable payload, missing repo)
allows the call and logs the reason, because a broken gate must never wedge the
tools. Every decision appends to `docs/subagent-gate.log`.

Materialized per-agent by `bootstrap.py --agents claude` (wired as a PreToolUse
hook in `.claude/settings.json.example`); the agent-neutral floor stays git+CI.
Adapted — stdlib re-implementation — from brefledev/stop-subagent-fanout (MIT).
"""

import json
import os
import sys
from pathlib import Path

# Claude Code's subagent-spawn tools. A tool not in this set is never gated
# (the hook defers), so the gate touches only fan-out, nothing else.
SPAWN_TOOLS = {"Task", "Agent"}
LOG_NAME = "subagent-gate.log"


def read_declared(path):
    """First non-comment, non-blank line lowercased, or "" — the same
    declared-policy parse the hooks and agent_loop use (kept local per the F5
    small-loader rule; no sibling import).

    Contract:
      Inputs:  path: path-like to a declared-policy file (may not exist)
      Outputs: str — the policy token, lowercased; "" if absent/unreadable/empty
    """
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    for raw in text.splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            return line.lower()
    return ""


def decide(tool_name, policy, override):
    """Pure decision core for one tool call.

    Contract:
      Inputs:  tool_name: str          (the PreToolUse tool name)
               policy: str             (docs/subagent-gate token; "" = off)
               override: str           (SUBAGENT_GATE env value, lowercased)
      Outputs: (decision, reason) where decision in
               {allow, ask, deny, defer}; `defer` = not a spawn tool, not our
               business. An unrecognized policy value resolves to `ask` (the
               safer direction, never harder than the explicit `deny`).
    Implements: SR-043, LLR-040
    """
    if tool_name not in SPAWN_TOOLS:
        return "defer", "not a spawn tool"
    if override == "allow":
        return "allow", "SUBAGENT_GATE=allow override (human-set)"
    if policy in ("", "off"):
        return "allow", "gate off (docs/subagent-gate)"
    if policy == "deny":
        return "deny", "subagent spawns are denied (docs/subagent-gate: deny)"
    if policy == "ask":
        return "ask", "subagent spawn needs approval (docs/subagent-gate: ask)"
    return "ask", "unrecognized docs/subagent-gate value {!r}; asking".format(policy)


def emit(decision, reason):
    """Map a decision to PreToolUse stdout + an exit code, returning the code.

    `allow`/`ask`/`deny` print the `hookSpecificOutput.permissionDecision`
    payload; `deny` also exits 2 (the belt-and-suspenders channel some Claude
    Code versions read). `defer` prints nothing and exits 0 — proceed normally.
    """
    if decision == "defer":
        return 0
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": decision,
                    "permissionDecisionReason": reason,
                }
            }
        )
    )
    return 2 if decision == "deny" else 0


def log_decision(root, tool_name, decision, reason):
    """Append one tab-separated decision to docs/subagent-gate.log (best-effort;
    the paper trail must never block a call, so an OSError is swallowed)."""
    try:
        with open(
            Path(root) / "docs" / LOG_NAME, "a", encoding="utf-8", newline="\n"
        ) as handle:
            handle.write("{}\t{}\t{}\n".format(tool_name, decision, reason))
    except OSError:
        pass


def main(argv=None):
    """Read the PreToolUse payload on stdin, decide, emit, log. Fails OPEN on any
    error (allows + logs) so a broken gate never wedges the agent's tools.
    Implements: SR-043, LLR-040
    """
    root = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        tool_name = payload.get("tool_name") or payload.get("toolName") or ""
        policy = read_declared(Path(root) / "docs" / "subagent-gate")
        override = (os.environ.get("SUBAGENT_GATE") or "").strip().lower()
        decision, reason = decide(tool_name, policy, override)
    except Exception as exc:  # noqa: BLE001 — deliberate fail-OPEN; see module doc
        log_decision(root, "?", "allow", "gate error, failing open: {}".format(exc))
        return 0
    if decision != "defer":
        log_decision(root, tool_name, decision, reason)
    return emit(decision, reason)


if __name__ == "__main__":
    sys.exit(main())
