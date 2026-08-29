#!/usr/bin/env python3
"""Subagent spawn gate — OPT-IN, FAIL-OPEN fan-out supervision for unattended runs.

NAMED FOR WHAT IT DOES, not for what a fan-out control usually does. This header
read "deny-by-default" until the 2026-08-19 repo review (M-13) measured the
behaviour against the sentence: an ABSENT policy allows, an `off` policy allows,
an unreadable `process.toml` allowed, and any internal error allows — every one
of those by design and pinned by tests. A `docs/process.toml` that is PRESENT
but does not parse no longer belongs on that list (OI-46 ruled (1a),
2026-08-20 — executed here, WI-491): it now reads `ask`, aligned with the two
twin readers in `check_trajectory.py` / `gen_okf.py`, which have always treated
the same state as ON rather than as a quiet opt-out — three readers, one
direction. Said precisely, because the first cut of this arm was not: it
resolves to the MORE RESTRICTIVE of `ask` and whatever the legacy
`docs/subagent-gate` declares, so a repo carrying both surfaces keeps an
explicit `deny` when the newer file breaks (2026-08-21 review, C-2). "Closes
relative to `allow`" was the whole claim; taking the maximum is what makes it
true in both directions. Nothing here denies until a human writes `deny`, or the
gate cannot tell what the human wrote. The old headline described the opposite
posture, which is the most expensive kind of comment to be wrong: a reader
budgeting risk would have credited this module with a refusal it never makes.
Whether the fail posture on a genuine ABSENCE should also invert stays an owner
call, deliberately not taken here.

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

**Fail open with a paper trail, for what remains open:** a malformed
`PreToolUse` payload or any other internal error still allows the call and logs
the reason, because a broken gate must never wedge the tools (SN-006's relaxed
posture keeps this arm even after OI-46). A PRESENT-but-unparseable
`docs/process.toml` is no longer in that list — see above. Every decision
appends to `out/subagent-gate.log` (gitignored cache); `agent_loop.py`'s launch
banner surfaces its line count (OI-46 ruled (2a), WI-491) so the paper trail is
actually read somewhere, not just written.

Materialized per-agent by `bootstrap.py --agents claude` (wired as a PreToolUse
hook in `.claude/settings.json.example`); the agent-neutral floor stays git+CI.
Adapted — stdlib re-implementation — from brefledev/stop-subagent-fanout (MIT).

Contracts: IF-020, IF-151 — the interface seams this module declares (process.md
§8; rows of record in docs/requirements/interfaces.toml).

Contract IF-020: the PreToolUse hook's verdict. It resolves the declared policy
    for the call and prints a `hookSpecificOutput.permissionDecision` payload
    carrying `allow`, `ask` or `deny` with its reason; `deny` also exits 2,
    every other decision exits 0, and a deferred call prints nothing at all. It
    FAILS OPEN by design: any internal error resolves to `allow` and records
    why, because a broken gate must never wedge the tools. Supervision, not
    security — a model that can edit files can remove this. Every decision
    appends to a gitignored log, best-effort, so the paper trail can never block
    a call.
Contract IF-151: the invocation surface the agent CLI drives. The hook takes no
    arguments; one PreToolUse tool-call JSON object arrives on stdin and only
    `tool_name` (its `toolName` spelling accepted) is read out of it — an empty
    stdin reads as `{}`, and a call naming no spawn tool is not this gate's
    business. A malformed payload never reaches a decision: the read is wrapped,
    so a JSON error allows the call and appends the reason to the log.
"""

import json
import os
import sys
import tomllib
from pathlib import Path

# THE SHIPPED SHARED-HELPER PACKAGE (owner ruling D-8, `OI-16`, executed
# WI-448): the declared-policy line reader this module used to spell out
# itself. Run as a subprocess this script's own dir is sys.path[0] so a plain
# import resolves; the guard covers an in-process import (a test) whose
# sys.path does not yet carry scripts/. THIS MODULE IS A FAIL-OPEN GATE BY
# OWNER RULING (2026-08-11) and the import does not change that: `kitlib` ships
# in bootstrap's MAPPING like every other sibling, so an adopter's copy has it;
# were it ever absent the gate would fail LOUDLY at import rather than silently
# allowing, which is the direction this module already prefers for a defect.
try:
    from kitlib import config as _kitconfig
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from kitlib import config as _kitconfig

# Claude Code's subagent-spawn tools. A tool not in this set is never gated
# (the hook defers), so the gate touches only fan-out, nothing else.
SPAWN_TOOLS = {"Task", "Agent"}
LOG_NAME = "subagent-gate.log"
# The policy's home since the 2026-08-11 overturn of WI-423, and the one-word
# file it replaced — still read as the SN-028 migration-window fallback.
POLICY = "docs/process.toml [checks] subagent_gate"
LEGACY_POLICY = "docs/subagent-gate"

# Sentinel `read_process_policy` returns when `docs/process.toml` is PRESENT
# but does not parse/read — distinct from `None` ("this file has nothing to
# say": absent, or parses fine with no `subagent_gate` key). `decide()` gives
# it its own branch, resolving to `ask` — or to `deny` when the legacy
# `docs/subagent-gate` says so, the more-restrictive rule the 2026-08-21 review
# forced. NOT a None: the legacy file is consulted as a FLOOR, never as the
# policy, so a corrupt process.toml can no longer read as a quiet `off` just
# because the old file said `off`. That is what makes this terminal in the
# sense the twin readers in `check_trajectory.py` / `gen_okf.py` are (OI-46
# ruled (1a), 2026-08-20; WI-491). Never a str, so it can never collide with a
# real — however garbled — policy token.
UNPARSEABLE = object()


def read_process_policy(root):
    """`[checks] subagent_gate` out of `docs/process.toml`, lowercased; None
    when this file has nothing to say (fall through to the legacy one-word
    file); UNPARSEABLE when the file is PRESENT but does not parse or read.

    A LOCAL reader, per the F5 independently-copyable-script rule that already
    keeps `read_declared` here rather than importing a sibling — the cost the
    2026-08-11 overturn of WI-423 priced and accepted. A non-string value is
    rendered rather than dropped, so it reaches `decide`'s "unrecognized …
    asking" arm: a garbled dial on a fan-out guardrail must be loud, never a
    quiet `off`.

    UNTIL OI-46 (WI-491, 2026-08-20) this was the one place this reader
    deliberately differed from the twin in `check_trajectory.py` /
    `gen_okf.py`: an unparseable process.toml read as *undeclared* here, where
    those two read it as ON. That let a corrupted policy file fall through to
    the legacy one-word file (or, absent that too, to a quiet `allow`) — the
    ruled fail-open asymmetry. It now returns UNPARSEABLE instead, which
    `decide()` resolves to `ask`: a garbled `docs/process.toml` is exactly the
    place SN-006's relaxed wording means to bite ("surface to the human only
    where it cannot proceed"), not a place to keep moving.
    `tests/test_rule_sync.py` pins all three copies by value (D-7), now
    including the aligned direction rather than the retired divergence.

    Contract:
      Inputs:  root: path-like repo root
      Outputs: str | None | UNPARSEABLE — the policy token, lowercased; None
               if undeclared (absent file, or file parses with no
               `subagent_gate` key); UNPARSEABLE if the file is PRESENT but
               does not parse/read.
    """
    path = Path(root) / "docs" / "process.toml"
    if not path.is_file():
        return None
    try:
        # utf-8-sig: a BOM is not legal TOML but is invisible to a shell read.
        data = tomllib.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return UNPARSEABLE
    table = data.get("checks")
    value = table.get("subagent_gate") if isinstance(table, dict) else None
    return None if value is None else str(value).strip().lower()


# First non-comment, non-blank line lowercased, or "".
#
# WI-448: this was the fifth literal copy of the declared-LINE rule, and the
# only one whose docstring had to spend a paragraph arguing that its
# divergences were deliberate. The rule now has ONE home
# (`kitlib.config.first_declared_line`) and this name is the ADAPTER over it —
# `read_declared_lower` — so the two divergences survive as a stated contract
# instead of as a copy that has to be pinned equal:
#   1. LOWERCASED — this module compares the token against a closed,
#      case-folded vocabulary ("off"/"ask"/"deny").
#   2. `""`, not None, for undeclared — `decide()` below documents its own
#      `policy` param as `"" = off`, so this reader hands back `""` to compose
#      with that contract without a None-check at every call site.
# Neither is a bug to harmonize away; both are now expressed once, in the
# adapter, rather than re-argued in a duplicate body.
#
# Contract:
#   Inputs:  path: path-like to a declared-policy file (may not exist)
#   Outputs: str — the policy token, lowercased; "" if absent/unreadable/empty
read_declared = _kitconfig.read_declared_lower


def decide(tool_name, policy, override, legacy=""):
    """Pure decision core for one tool call.

    Contract:
      Inputs:  tool_name: str          (the PreToolUse tool name)
               policy: str | UNPARSEABLE (the [checks] subagent_gate token, or
                                        the legacy file's; "" = off;
                                        UNPARSEABLE = docs/process.toml is
                                        PRESENT but did not parse/read)
               override: str           (SUBAGENT_GATE env value, lowercased)
               legacy: str             (the legacy one-word file's token, ""
                                        when absent — consulted ONLY on the
                                        UNPARSEABLE arm)
      Outputs: (decision, reason) where decision in
               {allow, ask, deny, defer}; `defer` = not a spawn tool, not our
               business. An unrecognized policy value resolves to `ask` (the
               safer direction, never harder than the explicit `deny`).
               UNPARSEABLE resolves to the MORE RESTRICTIVE of `ask` and what
               the legacy file declares — OI-46 ruled (1a) aligned this arm
               with its twins (WI-491), and the 2026-08-21 review measured
               that the first cut had turned an operator's explicit `deny`
               into `ask` for a repo carrying both surfaces.
    Implements: SR-043, LLR-040
    """
    if tool_name not in SPAWN_TOOLS:
        return "defer", "not a spawn tool"
    if override == "allow":
        return "allow", "SUBAGENT_GATE=allow override (human-set)"
    if policy is UNPARSEABLE:
        # MORE RESTRICTIVE OF THE TWO, not "the newer surface wins". Relative
        # to `allow` this arm closes, which is what OI-46 (1a) ruled and what
        # the commit that shipped it described; relative to a legacy `deny` it
        # would OPEN — an explicit refusal becoming unreachable the moment
        # process.toml fails to parse, in exactly the both-surfaces-live state
        # `bootstrap.py --migrate-config` exists to serve. A fail-closed arm
        # never loosens a decision the human already wrote down.
        if legacy == "deny":
            return "deny", (
                "docs/process.toml is present but did not parse; {} still "
                "reads `deny` and the parse-failure arm takes the more "
                "restrictive of the two (OI-46 (1a))".format(LEGACY_POLICY)
            )
        return "ask", (
            "docs/process.toml is present but did not parse; asking "
            "(fail-closed, aligned with its twin readers — OI-46 (1a))"
        )
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
        legacy = ""
        if policy is None or policy is UNPARSEABLE:
            legacy = read_declared(Path(root) / LEGACY_POLICY)
        if policy is None:
            policy = legacy
        override = (os.environ.get("SUBAGENT_GATE") or "").strip().lower()
        decision, reason = decide(tool_name, policy, override, legacy)
    except Exception as exc:  # noqa: BLE001 — deliberate fail-OPEN; see module doc
        log_decision(root, "?", "allow", "gate error, failing open: {}".format(exc))
        return 0
    if decision != "defer":
        log_decision(root, tool_name, decision, reason)
    return emit(decision, reason)


if __name__ == "__main__":
    sys.exit(main())
