#!/usr/bin/env python3
"""Subagent spawn gate — OPT-IN, FAIL-OPEN fan-out supervision for unattended runs.

NAMED FOR WHAT IT DOES, not for what a fan-out control usually does. This header
read "deny-by-default" until the 2026-08-19 repo review (M-13) measured the
behaviour against the sentence: an ABSENT policy allows, an `off` policy allows,
an unreadable `process.toml` allows, and any internal error allows — every one of
those by design and pinned by tests. Nothing here denies until a human writes
`deny`. The old headline described the opposite posture, which is the most
expensive kind of comment to be wrong: a reader budgeting risk would have
credited this module with a refusal it never makes. Whether the fail posture
SHOULD invert is an owner call, deliberately not taken here.

A Claude Code `PreToolUse` hook (SR-043; realizes SN-006 "a walk-away run stays
safe" + SN-012 "opt-in"). During an unattended coordinator run a driver session
can spawn subagents freely, which multiplies cost and loosens oversight; this
gate refuses or defers each spawn per a declared policy, with the override held
by the human who launched the run — not the model.

**Supervision, not security** (stated honestly, like every hook in this kit): a
model that can edit files can remove this. It is a bounded-fan-out guardrail for
an unattended run, not a sandbox.

Policy — `docs/process.toml` `[checks] subagent_gate` since the 2026-08-11
overturn of WI-423, else (SN-028 migration window) the legacy one-word
`docs/subagent-gate`: `off` (or undeclared) allows everything, `ask` defers each
spawn to approval, `deny` refuses. It ships VISIBLE at `"off"` — an opt-in dial
readable without being armed. The env override `SUBAGENT_GATE=allow` — set in
the launcher environment, which the model cannot write — bypasses the gate for a
deliberately-supervised run.

**Fail open with a paper trail:** any error (unreadable payload, missing repo)
allows the call and logs the reason, because a broken gate must never wedge the
tools. Every decision appends to `out/subagent-gate.log` (gitignored cache).

Materialized per-agent by `bootstrap.py --agents claude` (wired as a PreToolUse
hook in `.claude/settings.json.example`); the agent-neutral floor stays git+CI.
Adapted — stdlib re-implementation — from brefledev/stop-subagent-fanout (MIT).

Contracts: IF-020, IF-038 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.toml).
"""

import json
import os
import sys
import tomllib
from pathlib import Path

# Claude Code's subagent-spawn tools. A tool not in this set is never gated
# (the hook defers), so the gate touches only fan-out, nothing else.
SPAWN_TOOLS = {"Task", "Agent"}
LOG_NAME = "subagent-gate.log"
# The policy's home since the 2026-08-11 overturn of WI-423, and the one-word
# file it replaced — still read as the SN-028 migration-window fallback.
POLICY = "docs/process.toml [checks] subagent_gate"
LEGACY_POLICY = "docs/subagent-gate"


def read_process_policy(root):
    """`[checks] subagent_gate` out of `docs/process.toml`, lowercased, or None
    when this file has nothing to say (fall through to the legacy one-word
    file).

    A LOCAL reader, per the F5 independently-copyable-script rule that already
    keeps `read_declared` here rather than importing a sibling — the cost the
    2026-08-11 overturn of WI-423 priced and accepted. A non-string value is
    rendered rather than dropped, so it reaches `decide`'s "unrecognized …
    asking" arm: a garbled dial on a fan-out guardrail must be loud, never a
    quiet `off`.

    THE ONE PLACE THIS READER DELIBERATELY DIFFERS from the twin in
    `check_trajectory.py` / `gen_okf.py`: an UNPARSEABLE process.toml reads as
    *undeclared* here, where those two read it as ON. Their failure mode is a
    check that silently stops running; this module's is the opposite — see
    "fail OPEN with a paper trail" above. Failing an unreadable file to `ask`
    would defer every spawn in an unattended run, which is the wedge this
    module exists not to be. `tests/test_rule_sync.py` pins all three copies —
    including this divergence — by value (D-7).

    Contract:
      Inputs:  root: path-like repo root
      Outputs: str | None — the policy token, lowercased; None if undeclared
    """
    path = Path(root) / "docs" / "process.toml"
    if not path.is_file():
        return None
    try:
        # utf-8-sig: a BOM is not legal TOML but is invisible to a shell read.
        data = tomllib.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return None
    table = data.get("checks")
    value = table.get("subagent_gate") if isinstance(table, dict) else None
    return None if value is None else str(value).strip().lower()


def read_declared(path):
    """First non-comment, non-blank line lowercased, or "" (kept local per the
    F5 small-loader rule; no sibling import).

    The LINE-SELECTION rule (skip blank/comment lines, take the first
    survivor) is the one `agent_common.read_declared` and the three
    `_first_declared_line` copies (bootstrap.py, check_privacy.py,
    check_trajectory.py) also apply — pinned equal in tests/test_rule_sync.py.
    This copy diverges from all four in two ways, BOTH deliberate, not just
    the casing the name implies: the result is LOWERCASED (this module
    compares the token against a closed, case-folded vocabulary), and the
    not-declared sentinel is `""` rather than `None` (`decide()` below
    documents its own `policy` param as `"" = off`, so this reader has to
    hand back `""` to compose with that contract without a None-check at
    every call site). Neither is a bug to harmonize away.

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
               policy: str             (the [checks] subagent_gate token, or
                                        the legacy file's; "" = off)
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
        return "allow", "gate off ({})".format(POLICY)
    if policy == "deny":
        return "deny", "subagent spawns are denied ({}: deny)".format(POLICY)
    if policy == "ask":
        return "ask", "subagent spawn needs approval ({}: ask)".format(POLICY)
    return "ask", "unrecognized {} value {!r}; asking".format(POLICY, policy)


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
    """Append one tab-separated decision to out/subagent-gate.log (best-effort;
    the paper trail must never block a call, so an OSError is swallowed).
    out/ is the kit's gitignored cache home: writing under tracked docs/ made
    every spawn decision substantive working-tree dirt — blocking worker DONE
    ("a dirty tree is not done") and eventually committing the log as junk
    (repo-review 2026-07-21 M-21)."""
    try:
        out_dir = Path(root) / "out"
        out_dir.mkdir(parents=True, exist_ok=True)
        with open(out_dir / LOG_NAME, "a", encoding="utf-8", newline="\n") as handle:
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
        policy = read_process_policy(root)
        if policy is None:
            policy = read_declared(Path(root) / LEGACY_POLICY)
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
