#!/usr/bin/env python3
"""Shared coordinator primitives, extracted VERBATIM from agent_loop.py
(WI-218 slice C — a file split, not a rewrite; behaviors and WI history
unchanged). The session engine (agent_loop) and the serial integrator
(integrate.py) both stand on this layer:

  - the typed exit codes + `END_STATES`;
  - `git`/`head_sha`/`head_sha_full` and the dirty-tree family (owner-only
    scratchpad exemption, WI-203);
  - the declared-surface reads — `read_declared`, `pause_reason`, the WI-148
    blackout window — and the stop banner + Current State excerpt;
  - the per-worktree coordinator lock (kernel advisory lock; the held
    descriptor lives HERE, in this module's `_LOCK_FD`, so every caller
    shares one lock namespace);
  - worker-assignment primitives (`WI_TOKEN_RE`, `sanitize_train`,
    `parse_wi_list`, `load_wi_registry`, `train_evidence`)
    and the small CSV/ref readers;
  - `parse_map`, `preflight` (launchability refusal, SR-027), and the
    session-log family (size-bounded logs, the regenerated iteration index,
    the telemetry commit).

agent_loop re-exports the names it historically exposed, so its public
surface is unchanged. Stdlib only, Python 3.11+, Windows/POSIX.

Contracts: IF-065 — the interface seam this module declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-065: the shared coordinator primitives the session engine and the
    serial integrator both stand on. The typed exit codes and `END_STATES`; the
    `git` / `head_sha` / `head_sha_full` wrappers and the dirty-tree family; the
    declared-surface reads (`declared_policy`, `read_agent_loop_config`,
    `pause_reason`, the blackout window) and `stop_banner`; the per-worktree
    kernel advisory lock, whose held descriptor lives HERE so every caller in a
    process shares one lock namespace and `acquire_lock` / `release_lock` cannot
    disagree about what is held; the worker-assignment primitives
    (`WI_TOKEN_RE`, `sanitize_train`, `parse_wi_list`, `load_wi_registry`,
    `train_evidence`); `parse_map`; `preflight`, the launchability refusal; and
    the session-log family — size-bounded logs, the regenerated iteration index
    and the telemetry commit — with the generated run-state write. The names
    were extracted verbatim and `agent_loop` re-exports every historical one, so
    this layer adds a home without changing a public surface.
"""

import datetime
import hashlib
import errno
import os
import re
import shutil
import socket
import subprocess
import sys
import time
import tomllib
from pathlib import Path

# THE SHIPPED SHARED-HELPER PACKAGE (owner ruling D-8, `OI-16`, executed
# WI-448): one home for behaviours this module used to spell out itself — the
# declared-policy line reader, the `docs/work/` spec-folder registry reader, and
# (WI-498 slice 0) the stage ladder's closed rung vocabulary.
# It replaces the F5 rule, which had licensed those copies unbounded and left
# `tests/test_rule_sync.py` pinning them equal by value. Run as a subprocess
# this script's own dir is sys.path[0] so a plain import resolves; the guard
# covers an in-process import (a test) whose sys.path does not yet carry
# scripts/ — the same sanctioned-sibling idiom the engines use for each other.
try:
    from kitlib import config as _kitconfig
    from kitlib import ladder as _kitladder
    from kitlib import registry as _kitregistry
    from kitlib import secret_classes as _kitsecrets
    from kitlib import spine as _kitspine
    from kitlib import stage as _kitstage
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from kitlib import config as _kitconfig
    from kitlib import ladder as _kitladder
    from kitlib import registry as _kitregistry
    from kitlib import secret_classes as _kitsecrets
    from kitlib import spine as _kitspine
    from kitlib import stage as _kitstage

# This module's own directory, so `spine_stage_of` can spawn the sibling
# `derive_stage.py` on a fingerprint miss without importing it.
_SCRIPTS_DIR = Path(__file__).resolve().parent

# Sibling scripts (the WI-218 split): preflight validates the AGENT_CMD
# template through the headless session layer. The guard covers an in-process
# import (a test) whose sys.path doesn't yet carry scripts/ — the same
# sanctioned-sibling-import idiom agent_loop uses.
try:
    from agent_session import build_argv, split_cmd
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from agent_session import build_argv, split_cmd
# Size bounds for the tracked per-session log (the Q13d "size-bounded" cap):
# the head shows how the session started, the capped tail how it ended — the
# part that explains the outcome. The raw unbounded stream goes to the
# gitignored out/run-logs/ for local debugging.
LOG_HEAD_LINES = 60


LOG_TAIL_LINES = 400


LOG_MAX_BYTES = 65536


# The terminal end states a session/loop outcome may carry. (Their old durable
# home, the dispatcher-generated `docs/run-state` file, retired with the
# dispatcher at concurrency-restructure Phase 5 — the stop banner and exit
# codes carry the outcome now.) NEEDS-HUMAN's one-line ask is the stop
# banner's headline (WI-127).
END_STATES = ("DONE", "BLOCKED", "NEEDS-HUMAN")


EXIT_DONE = 0


EXIT_PREFLIGHT = 2


EXIT_BLOCKED = 3


EXIT_STALL = 4


EXIT_WAITING = 5


EXIT_BUDGET = 6


EXIT_NEEDS_HUMAN = 7


EXIT_PAUSED = 8


# REVIEW OWED (C2, docs/plans/2026-08-30-stall-guard-plan.md): the build is
# committed but a review verdict could not be drawn — every route on the
# reviewer ladder errored, hung or was cooled. Deliberately NOT a decided
# worker outcome (dispatch._WORKER_OUTCOMES): the lane parks with its work,
# like a crash, and the next cycle resumes it to draw the round — finished
# work is never handed back over a reviewer outage (owner direction
# 2026-08-30). Appended at the END of the exit alphabet; 10 stays retired.
EXIT_REVIEW_OWED = 9


# (EXIT_TRAIN_END = 10 retired with session grouping — WI-383, §A6.1: it ended a
# PACKED assignment early when the §7 continuation re-check refused the next
# constituent, and nothing packs. The number stays retired rather than reused —
# an exit code is a contract with every launcher and log that ever read it.)


# The FB3 owner-only path(s): OWNER_SCRATCHPAD.md is free-form owner notes the
# human edits continuously (check_docs.py drops it from doc discovery the same
# way — check_docs.SCRATCHPAD). Because it is tracked and perpetually edited, an
# owner-only-dirty tree is NOT interrupted-session residue: it must not fire the
# WI-076 resume note or flip the done detection (WI-203). Mirrored, not imported
# — importing the doc-checker into the coordinator would add a CMP-008→CMP-007
# edge + an IF seam for one fixed filename; the name is a bootstrap contract
# (test_bootstrap asserts the scaffold ships it), so the mirror cannot drift.
OWNER_ONLY_PATHS = ("OWNER_SCRATCHPAD.md",)


# The one-word declared-policy reader (the legacy docs/push-policy, …): the
# first non-empty, non-comment line, or `default` when nothing is declared. ONE
# HOME since WI-448 — this name used to carry its own literal copy of a rule four
# other modules also spelled out (`subagent_gate`, and `_first_declared_line` in
# bootstrap/check_privacy/check_trajectory), pinned equal by tests because D-7
# could only contain the drift, not remove it. Re-exported under its own
# long-standing name; the reader for the LEGACY half of the SN-028 dual-read
# window, while new policy reads go through `declared_policy` below, which
# prefers `docs/process.toml`.
#
# `docs/gate` USED TO HEAD THAT LIST AND WAS NEVER READ THROUGH HERE (corrected
# WI-498 slice 4, the gate schedule map's reader E): it is a deliberate NON-row in
# `PROCESS_KEYS` twenty lines below, and every live gate reader spelled its own
# one-line parse out locally. A documented reader that no call site uses is worse
# than none — it makes a scheduling map of the file look one reader deeper than it
# is.
read_declared = _kitconfig.read_declared


# --- SN-028: docs/process.toml, the one policy home ---------------------------
# THE MIGRATION TABLE, stated once. Each row maps a legacy one-word file under
# docs/ to the `[section] key` in docs/process.toml that replaced it, and the
# type the TOML value carries. Three readers stand on this single statement —
# the value reader, the mixed-config refusal, and bootstrap's converter — so a
# key can never be migrated in one of them and forgotten in another.
#
# NOT here, deliberately (each documented in process.toml.template's header):
# docs/stack.ini (adopter-owned product toolchain), docs/work/pause and
# docs/agents-enabled (presence-as-semantics), docs/stage (a generated cache).
# The six check-enablement toggles USED to be a fourth exception; the owner
# overturned that on 2026-08-11 and they are rows below.
PROCESS_TOML = "process.toml"

PROCESS_KEYS = {
    "push-policy": ("policies", "push", "str"),
    "review-policy": ("policies", "review_rounds", "int"),
    "privacy-check": ("policies", "privacy_check", "bool"),
    "secrets-scan": ("policies", "secrets_scan", "bool"),
    "privacy-review": ("policies", "privacy_review", "str"),
    "guardrails-policy": ("policies", "guardrails", "str"),
    "blackout": ("policies", "blackout", "str"),
    # The gate-authority dial retired into the ORDINAL below at SN-029. The
    # legacy `docs/gate-policy` FILE is still read (an un-migrated repo keeps
    # working), and the enum key is still type-checked if a repo hand-wrote it,
    # but nothing SHIPS it any more — see PROCESS_ONLY_KEYS.
    "gate-policy": ("attestation", "gate_policy", "str"),
    # The six CHECK-ENABLEMENT toggles, folded in by the 2026-08-11 overturn of
    # WI-423 ("far better to tie those into process.toml and key them all to on
    # / true"). They belong in THIS table, not PROCESS_ONLY_KEYS: each had a
    # legacy one-word file, so each can be double-declared, and the mixed-config
    # refusal + `--migrate-config` conversion both key off these rows.
    #
    # Only `live-status` is read through `declared_policy` — the other five are
    # read by scripts that import nothing of this layer and carry their own
    # local `tomllib` read (F5, no shared `_kitcommon.py`). Their rows are here
    # anyway, because the refusal and the migration are this module's job
    # wherever the VALUE is read: a checker that reads its own key must still
    # not run beside a legacy file nobody converted.
    "trajectory-check": ("checks", "trajectory_check", "bool"),
    "interfaces-check": ("checks", "interfaces_check", "bool"),
    "components-check": ("checks", "components_check", "bool"),
    "okf-export": ("checks", "okf_export", "bool"),
    "live-status": ("checks", "live_status", "bool"),
    "subagent-gate": ("checks", "subagent_gate", "str"),
}

# Dials with NO legacy one-word file — born in docs/process.toml, so they can
# never be double-declared and appear here rather than in PROCESS_KEYS. They
# still need the type check: the failure PROCESS_KEYS' check exists to stop (a
# quoted `review_rounds` reading as "no review required") applies verbatim to a
# `human_approval_through`, whose wrong value reads as the conservative
# default with no diagnostic and looks exactly like a repo that never set it.
#
# IT IS A `str` SINCE WI-493: the dial names a `DevStg-*` rung, not a 0-4 tier
# ordinal. The type check alone is therefore much weaker than it was — every
# typo is still a `str` — which is why the VOCABULARY check below exists and
# why it, not the type, is now the arm that catches a bad dial.
PROCESS_ONLY_KEYS = {
    ("attestation", "human_approval_through"): "str",
    ("attestation", "keep_nondependent"): "bool",
    ("attestation", "final_review"): "str",
    ("attestation", "complete_review"): "str",
    ("attestation", "complete_sample_rate"): "int",
    # The reverse back-link coverage bar (OI-42 ruled (e), WI-486). It sits in
    # `[checks]` beside six BOOLEANS and is an INT, which is exactly why it
    # needs the type check: its reader
    # (`gen_arch_map.read_backlink_min`) answers 0 — report-only — for anything
    # it cannot read as an int in range, so a hand-written
    # `backlink_coverage_min = "50"` would silently disarm a bar the repo
    # believes it declared. That reader is deliberately quiet (a threshold has
    # no conservative default to fail toward); this table is where it gets loud.
    ("checks", "backlink_coverage_min"): "int",
}

# Dials whose value must also fall in a RANGE. Out of range is refused rather
# than clamped: `101` is not "the strictest bar", it is a value nobody can
# satisfy, and `-1` reads as a bar that can never fire.
PROCESS_KEY_RANGES = {
    ("checks", "backlink_coverage_min"): (0, 100),
}

# Dials whose value must come from a CLOSED VOCABULARY. This replaced
# `human_approval_through`'s `(0, 4)` range row at WI-493, and it is the
# same guarantee carried on the new value's own terms: the retired range refused
# `-1` because that single input reads as LESS human involvement than the owner
# asked for, and a misspelled rung does exactly the same thing — it is
# unrecognized, so it falls to a default rather than to what was meant. Refused
# here, loudly, and fallen back on conservatively at the reader
# (`approval_through`). Populated lazily below, where the rung vocabulary
# is in scope.
PROCESS_KEY_VOCAB = {}

# THE MIGRATION WINDOW: for a re-keyed dial, the exact set of PREVIOUS values
# the reader still translates. Filled below from the translation table itself,
# so the window and the translation cannot come to disagree about which old
# values are honoured.
#
# WHY A VALUE SET AND NOT A TYPE. Declaring "the old TYPE is still accepted"
# was tried first and was wrong in a way worth recording: it accepted every
# int, so `human_approval_through = -1` — the single input the retired
# `(0, 4)` range row existed to refuse, because it is the one that reads as
# LESS human involvement than the owner asked for — stopped being refused at
# all. A migration window must be exactly as wide as the migration.
#
# Without the window at all, `config_conflicts` — a HARD refusal consulted by
# dispatch, intake and integrate — would refuse an adopter's committed
# `human_approval_through = 4` the moment they took the kit upgrade, on a
# dial `approval_through` reads perfectly well. The signal for a legacy
# value is the reader's WARNING, once per run, naming the migrator; the refusal
# stays reserved for values nothing can honour.
PROCESS_KEY_LEGACY_VALUES = {}

# The two keys the git hooks match in pure sh (M-42 fail-closed). Named here
# because the cross-parser agreement test (tests/test_process_config.py) is
# driven from this tuple: for every one of these keys the hooks' ERE and
# `tomllib` must return the SAME answer over a table of adversarial file
# shapes. A claim of agreement that no test drives is how the two parsers
# diverge.
GREPPABLE_KEYS = ("privacy_check", "privacy_review")

# THE GREPPABLE SHAPE, and why it is a CHECKED contract rather than a
# convention. The git hooks read this file in pure sh so a Python-less box
# still fails closed (M-42) — which means two grammars read one file, and two
# grammars WILL disagree unless the file's shape is narrowed to where they
# cannot. TOML is far more expressive than a `grep -E` can follow: a dotted key
# (`policies.privacy_check = true`), an inline table (`policies = { … }`), a
# key in a multi-line string, a key under the wrong section header — every one
# of those parses to something `tomllib` sees and the hook does not, or the
# reverse. Each is a silent flip of the privacy gate.
#
# So the file is CONSTRAINED and the constraint is enforced: one `key = value`
# per line, under a bare `[section]` header, no dotted keys, no inline tables,
# no multi-line strings. `process_shape_findings` refuses anything else, and
# the hooks fail CLOSED (a declared key they cannot prove `false` reads as ON)
# so the residual is loud rather than permissive.
_SECTION_RE = re.compile(r"^\s*\[([^]]*)\]\s*(#.*)?$")
_KEY_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$")
_MULTILINE_RE = re.compile(r'"""|\'\'\'')


def _process_toml_path(docs):
    return Path(docs) / PROCESS_TOML


def process_config(docs):
    """The parsed `docs/process.toml` as a dict of sections, or `{}` when the
    file is absent, unreadable or malformed.

    FAILS CLOSED on a malformed file in the same shape `tracked_pause` does —
    `except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError)` — rather
    than `read_declared`'s narrower `except OSError`, which lets a BOM'd or
    mis-encoded policy file crash the coordinator while degrading everywhere
    else. `config_conflicts` reports the malformation loudly; this returns `{}`
    so a caller that only wants a value gets the DEFAULT, never a half-parse.

    Implements: SR-137, SR-139, LLR-155
    """
    data = read_toml(_process_toml_path(docs))
    return data if isinstance(data, dict) else {}


def read_toml_text(text):
    """`tomllib.loads(text)`, or None when it does not parse. The TEXT twin of
    `read_toml` — `handback.read_report` has already extracted a `+++` block
    and has no file left to hand over."""
    try:
        return tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None


def read_toml(path):
    """`tomllib.loads` of `path`, or None when it is absent, unreadable,
    mis-encoded or malformed — the module's ONE tracked-TOML read.

    Extracted because `process_config` and `tracked_pause` had it verbatim, and
    the F5 cross-script sanction covers copies between INDEPENDENTLY COPYABLE
    scripts, never two copies inside one file (WI-347). The union of failure
    modes is deliberate: a caller that cannot tell "absent" from "malformed"
    apart on the return value must not be reading policy, and both callers
    below distinguish them by their own second read."""
    try:
        if not path.is_file():
            return None
        # utf-8-SIG: a BOM is not legal TOML, so `tomllib` would raise on a
        # file some editors write by default — while the git hooks' sh read is
        # unaffected by a BOM at offset 0 and would keep acting on the same
        # file. The two readings must not diverge over an invisible byte.
        return tomllib.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return None


def _coerce(value, kind):
    """A TOML value rendered in the STRING vocabulary every legacy consumer
    already speaks, so the migration changes no downstream comparison. A bool
    renders `true`/`false`; an int renders its digits; a string passes through.

    A value of the WRONG TOML type returns None — never a substituted default.
    That distinction is load-bearing: `review_rounds = "2"` (a plausible hand
    edit, since every other value in `[policies]` is quoted) once silently
    became the integrator's `"0"` default, i.e. NO review verdict required, on
    a repo whose owner had just asked for two. A type mismatch is a REFUSAL
    (`config_conflicts` reports it and the three guarded entry points stop),
    not a value."""
    if value is None:
        return None
    if kind == "bool":
        return ("true" if value else "false") if isinstance(value, bool) else None
    if kind == "int":
        if isinstance(value, bool) or not isinstance(value, int):
            return None
        return str(value)
    if isinstance(value, bool) or not isinstance(value, str):
        return None
    return value


def process_shape_findings(docs):
    """Refusal strings for a `docs/process.toml` written in a shape the git
    hooks' pure-sh read cannot follow (see the constants above).

    Checks the file as LINES, not as parsed TOML, because what is being
    verified is precisely that the two readings agree: a dotted key, an inline
    table, a multi-line string or a key outside a `[section]` all parse fine
    and are all invisible-or-worse to a `grep -E`. Only the greppable keys are
    enforced this strictly — the rest of the file is Python-read only.

    Implements: SR-137, SR-139, LLR-155
    """
    path = _process_toml_path(docs)
    if not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as exc:
        return ["docs/{} cannot be read: {}".format(PROCESS_TOML, exc)]
    out = []
    if _MULTILINE_RE.search(text):
        out.append(
            "docs/{} contains a multi-line string. The git hooks read this "
            "file line-by-line in pure sh (M-42), and a key inside a "
            "multi-line string is a key they will act on. Use single-line "
            "values only.".format(PROCESS_TOML)
        )
    section = None
    for lineno, raw in enumerate(text.splitlines(), 1):
        head = _SECTION_RE.match(raw)
        if head:
            section = head.group(1).strip()
            continue
        out.extend(_line_shape_findings(raw, lineno, section))
    return out


def _line_shape_findings(raw, lineno, section):
    """The per-line half of `process_shape_findings` — split out so neither
    half sits at the C901 ceiling, and because the loop above is about
    SECTIONS while this is about KEYS."""
    line = raw.strip()
    if not line or line.startswith("#") or "=" not in line:
        return []
    # The dotted-key test runs BEFORE the key match, not inside it: a dotted
    # key does not match `_KEY_RE` at all, so a check placed after it is
    # unreachable — which is what a first cut of this function did, and the
    # shape it silently let through is the one that flips the gate.
    if "." in line.split("=", 1)[0]:
        return [
            "docs/{}:{} uses a DOTTED key ({}). One `key = value` per line "
            "under a bare [section] header — a dotted key is invisible to the "
            "hooks' keyed read.".format(PROCESS_TOML, lineno, line)
        ]
    key = _KEY_RE.match(raw)
    if key is None:
        return []
    name, value = key.group(1), key.group(2)
    out = []
    if value.startswith("{"):
        out.append(
            "docs/{}:{} uses an INLINE TABLE ({}). The hooks cannot read one; "
            "write each key on its own line.".format(PROCESS_TOML, lineno, name)
        )
    if name in GREPPABLE_KEYS and section != "policies":
        out.append(
            "docs/{}:{} declares the hook-read key `{}` under [{}], not "
            "[policies]. Python would ignore it and the hooks would act on it "
            "— the two must never disagree about a security gate.".format(
                PROCESS_TOML, lineno, name, section or "(no section)"
            )
        )
    return out


def declared_policy(docs, legacy_name, default):
    """The value of one policy dial, `docs/process.toml` first.

    `legacy_name` is the legacy file's basename (`"push-policy"`, …) — the key
    of `PROCESS_KEYS` — so every call site names the dial it already named and
    the migration table does the rest. Returns the value in the same STRING
    vocabulary the legacy file carried, so no comparison downstream changes.

    Precedence, and only two tiers by design: the TOML when the file declares
    that key, else the legacy one-word file, else `default`. There is NO third
    "both" tier — a repo carrying both sources is refused by `config_conflicts`
    at preflight rather than silently resolved (SN-028 / plan §11.8), because a
    mixed config is exactly the state where two readers disagree about the same
    policy and neither is wrong.
    """
    section, key, kind = PROCESS_KEYS[legacy_name]
    table = process_config(docs).get(section)
    if isinstance(table, dict) and key in table:
        value = _coerce(table[key], kind)
        # A wrong-typed value is NOT silently a default here — `config_conflicts`
        # refuses it upstream, and this fall-through only ever runs on a path
        # that already declined to refuse (a caller outside the three guarded
        # entry points). Falling to the legacy file / default keeps such a
        # caller working rather than crashing it.
        if value is not None:
            return value
    return read_declared(Path(docs) / legacy_name, default)


# --- SN-029: the human-approval level, as an ORDINAL ----------------------
# THE DIAL, and why it replaces a three-value enum. `attended | single-approve |
# autonomous` answered "who approves" with three words that four independent
# tables then re-interpreted, each with its own fail-safe direction. What the
# dispatcher actually needs is an ORDINAL comparison — is the tier this row sits
# at still human-held? — and an enum cannot express "TCs are human-held but LLRs
# are not", which is the distinction the eight-rung stage ladder exists to make.
#
# THE LEGACY TRANSLATION, stated as all THREE dials rather than as a level.
# The enum's three words were never one axis: each of them bundled a tier hold,
# a drain policy and an end-of-run hold, which is precisely why four tables had
# to re-interpret the same word. Translating to a level alone loses two of the
# three facts — the shape of the original SN-029 bug, where `single-approve`
# became "level 2" and so silently acquired a per-tier hold it never had.
#
#   attended       every tier is the human's; lanes drain at an approval
#   single-approve  LLM review through DevStg-Reqs+DevStg-Tests, ONE human sitting
#                  at the close — so NO per-tier hold (level 0), a final read,
#                  and the non-dependent work kept running that distinguished it
#   autonomous     every bar but the owner's final read closes on a recorded
#                  LLM verdict
LEGACY_APPROVAL = {
    "attended": {
        "human_approval_through": _kitladder.STAGE_RELEASE,
        "keep_nondependent": False,
        "final_review": "always",
    },
    "single-approve": {
        "human_approval_through": _kitstage.BELOW,
        "keep_nondependent": True,
        "final_review": "always",
    },
    "autonomous": {
        "human_approval_through": _kitstage.BELOW,
        "keep_nondependent": True,
        "final_review": "off",
    },
}

# --- THE RE-KEY (WI-493, OI-21 shape (ii), folded into WI-498 slice 5) ---------
# THE DIAL MOVED, DELIBERATELY, and the block below this one used to say the
# opposite. OI-21 ruled shape (i) — keep the 0-4 ordinal and MAP it onto the
# ladder through a declared `DIAL_HOLDS` table — and named this conversion as
# shape (ii), available to supersede (i). The owner exercised that clause; the
# stage unification is where it lands, because the reason (i) was ever needed is
# the reason it is now unnecessary.
#
# WHY THE MAPPING TABLE COULD RETIRE RATHER THAN BE RE-KEYED. `DIAL_HOLDS`
# existed to bridge TWO vocabularies: an ordinal counting approvable TIERS and a
# ladder of labelled RUNGS. Shape (i)'s own argument against the retired
# `stage < level` arithmetic was that it compared two different ladders that
# happened to line up. Under one vocabulary there is only one ladder, so the
# comparison stops being a coincidence and becomes the definition: the dial names
# the HIGHEST rung a human still approves, and every rung AT OR BELOW it is held.
# That is the exact mirror of the at-or-above rule slice 2 gave check selection.
#
# EQUIVALENCE DRIVEN BEFORE THE TABLE WAS DELETED, not asserted after: all five
# former levels hold precisely the same rung sets under the ordinal rule
# (0 -> 0 rungs, 1 -> 2, 2 -> 4, 3 -> 5, 4 -> 8). The old table's most
# hand-reasoned property — that `DevStg-Boundary` rides `DevStg-Needs` and
# `DevStg-Arch` rides `DevStg-Reqs`, chosen because it errs toward MORE human
# involvement — falls out of the ordering for free, because each inserted rung
# sits immediately above the rung it was made to ride. `tests/test_approval_
# level.py` pins the equivalence permutation by permutation.
#
# WHAT THE RE-KEY BUYS BEYOND THE VOCABULARY: three settings the ordinal could
# not express. `DevStg-Needs`, `DevStg-Reqs`, `DevStg-Tests` and `DevStg-Impl`
# are now legal dial values with obvious meanings (hold Needs but not Boundary;
# hold through Reqs but not the partition; and so on). The old dial had five
# notches for eight rungs and the three it could not name were unreachable
# rather than forbidden.
#
# "NOTHING IS HUMAN-HELD" IS `DevStg-Below`, not a fourth kind of value. It is
# the sentinel `kitlib.stage` already declares for "below every rung", used here
# in exactly that sense: set the dial below the ladder and no rung is at or below
# it. A magic word like `"none"` would have been a second vocabulary in the one
# place this program exists to remove one.
APPROVAL_DIAL_RUNGS = frozenset(_kitladder.LADDER_RUNGS) | {_kitstage.BELOW}

# Declared UP THERE with the other dial tables and filled HERE, because the
# vocabulary is this module's own and the table is read by the shared
# validator. One value, one home.
PROCESS_KEY_VOCAB[("attestation", "human_approval_through")] = APPROVAL_DIAL_RUNGS

# The 0-4 ordinal an unmigrated repo still declares. READ, TRANSLATED AND
# WARNED — not refused: the value is a dial in an adopter's committed
# `process.toml`, and refusing it would stop their loop dead on a kit upgrade
# for a spelling. `bootstrap.py --migrate-config` rewrites it in place, and the
# warning names that command. There is no clamping arm: an int outside 0-4 was
# malformed before the re-key and is malformed after it.
LEGACY_DIAL_ORDINALS = {
    0: _kitstage.BELOW,
    1: _kitladder.STAGE_BOUNDARY,
    2: _kitladder.STAGE_ARCH,
    3: _kitladder.STAGE_LLREQS,
    4: _kitladder.STAGE_RELEASE,
}

PROCESS_KEY_LEGACY_VALUES[("attestation", "human_approval_through")] = frozenset(
    LEGACY_DIAL_ORDINALS
)

# Fail toward MORE human involvement on anything unreadable: a dial nobody can
# parse must not silently hand approval authority to the loop. The top rung
# is the conservative end — it holds every rung there is.
APPROVAL_FALLBACK = _kitladder.STAGE_RELEASE

# The dial's RETIRED KEY NAME (WI-499, owner-ruled 2026-08-21). A repo
# scaffolded before this rename still carries this spelling in
# `[attestation]`; `approval_through` below reads it as a loud fallback,
# mirroring the read-translate-warn shape WI-493 used for the retired 0-4
# ordinal. `bootstrap.py --migrate-config` (`_migrate_dial_key_name`) is the
# one-time fix that ends the warning.
LEGACY_ATTESTATION_KEY = "human_ratification_through"


def legacy_approval(word, key):
    """One dial's value under a legacy `gate-policy` word, or None when the word
    is not one of the three. The single home for the translation, so the
    migrator and the fallback readers cannot disagree about what a word meant."""
    return LEGACY_APPROVAL.get(str(word).strip().lower(), {}).get(key)


def approval_through(docs):
    """`[attestation] human_approval_through` as a `DevStg-*` rung.

    The HIGHEST rung a human still approves; every rung at or below it is held
    (`human_holds`). `DevStg-Below` means nothing is held — the loop approves
    every rung itself. `DevStg-Release`, the shipped default, holds everything.

    Falls back through the legacy `gate-policy` enum, then to `DevStg-Release`.

    A LEGACY 0-4 INT IS TRANSLATED AND WARNED, not refused (WI-493). See
    `LEGACY_DIAL_ORDINALS`: an adopter's committed dial must not stop their loop
    on a kit upgrade, and the warning names the migrator that fixes it. An int
    OUTSIDE 0-4 was malformed before the re-key and stays malformed.

    AN UNRECOGNIZED VALUE IS MALFORMED, NOT COERCED — the same reasoning the
    out-of-range int always took, and it matters more now that the vocabulary is
    open-looking. `"devstg-arch"`, `"Arch"` or a rung from a newer kit takes the
    conservative fallback rather than a best guess, because every wrong guess
    here fails in the direction of LESS human involvement.
    (`config_conflicts` refuses it loudly upstream; this is the behaviour for
    callers that did not run that gate.)

    Implements: SR-137, SR-139, LLR-155
    """
    table = process_config(docs).get("attestation")
    if isinstance(table, dict):
        value = table.get("human_approval_through")
        used_legacy_key = False
        if value is None and "human_approval_through" not in table:
            # WI-499: the key itself was retired, not just a value it once
            # held. A repo that never ran `--migrate-config` still carries
            # the old spelling — read it, warn once per call, and translate
            # exactly as if it had arrived under the live key.
            value = table.get(LEGACY_ATTESTATION_KEY)
            used_legacy_key = value is not None
        if isinstance(value, str) and value.strip() in APPROVAL_DIAL_RUNGS:
            if used_legacy_key:
                print(
                    "agent_common: [attestation] {} is RETIRED - reading it "
                    "as `human_approval_through` (WI-499). Run `python "
                    "project-trajectory/scripts/bootstrap.py --migrate-config "
                    "--dest .` from your kept kit checkout to rewrite the "
                    "key.".format(LEGACY_ATTESTATION_KEY),
                    file=sys.stderr,
                )
            return value.strip()
        if isinstance(value, int) and not isinstance(value, bool):
            rung = LEGACY_DIAL_ORDINALS.get(value)
            if rung is not None:
                print(
                    # ASCII ONLY, deliberately. This prints from a LIBRARY
                    # path, so no caller is guaranteed to have run
                    # `utf8_console()` first; an em-dash here reaches a cp1252
                    # console as a replacement character in a message whose
                    # whole job is to be read and acted on.
                    "agent_common: [attestation] {} = {} is the RETIRED 0-4 "
                    "ordinal{} - reading it as `{}` (WI-493{}). Run `python "
                    "project-trajectory/scripts/bootstrap.py --migrate-config "
                    "--dest .` from your kept kit checkout to rewrite "
                    "it.".format(
                        LEGACY_ATTESTATION_KEY
                        if used_legacy_key
                        else "human_approval_through",
                        value,
                        " under a RETIRED key name too (WI-499)"
                        if used_legacy_key
                        else "",
                        rung,
                        "+WI-499" if used_legacy_key else "",
                    ),
                    file=sys.stderr,
                )
                return rung
            return APPROVAL_FALLBACK
        if value is not None:
            return APPROVAL_FALLBACK
    legacy = legacy_approval(
        declared_policy(docs, "gate-policy", "attended"),
        "human_approval_through",
    )
    return APPROVAL_FALLBACK if legacy is None else legacy


# --- OI-21 -> WI-493: THE DIAL AND THE LADDER ARE ONE VOCABULARY --------------
# THE DIAL MOVED. It was the APPROVABLE-TIER ORDINAL 0-4 SN-029 defined (0 =
# nothing held, 1 = SNs, 2 = ...and SRs, 3 = ...and LLRs, 4 = ...and TCs), mapped
# onto the eight rungs by a declared `DIAL_HOLDS` table under OI-21 shape (i).
# WI-493 executed shape (ii): it now names a `DevStg-*` rung directly, and the
# table retired because there is no longer a second vocabulary to map from. The
# full argument, the driven equivalence and what the change buys are recorded at
# the re-key block above `APPROVAL_DIAL_RUNGS`.
#
# WHAT DID *NOT* MOVE, and this is the part OI-21 was emphatic about: the dial
# still says WHICH SPINE RUNGS a human approves. It was NOT re-keyed to artifact
# DEPTH. Re-keying approval to the depth and tier of the artifact touched is a
# change to WHEN A HUMAN IS RE-ENGAGED whose wrong-answer direction is silently
# LESS human involvement, so it is decided on its own — once IF/CMP maturity
# joins the approvable fold — and never defaulted here.
#
# WHERE THE TWO INSERTED RUNGS LAND is no longer a decision this module makes.
# `DevStg-Boundary` and `DevStg-Arch` produce artifacts (IF and CMP rows) that
# are not approvable TIERS, so the old ordinal had no notch for them and the
# table had to choose: each was held whenever the rung BELOW it was held —
# Boundary rides Needs, Arch rides Reqs — chosen because it errs toward MORE
# human involvement. Under the at-or-below rule that choice falls out of the
# LADDER ORDER for free, because each inserted rung sits immediately above the
# rung it was made to ride. The hand-reasoned property became a structural one.
#
# `LADDER_RUNGS` names the whole closed vocabulary — not just the held subset —
# because "is this a rung I recognize" and "is this rung held" are different
# questions, and `human_holds` must answer the first CONSERVATIVELY. Without it
# an unrecognized label (`""`, a typo, a rung from a newer kit) would compare as
# an ordinal lookup failure rather than as a hold.
#
# IT USED TO BE A LITERAL RESTATEMENT HERE (WI-498 slice 0 ended that). The
# reason given was the F5 no-shared-module rule — this module could not import
# the derivation engine — so the eight strings were spelled out again and pinned
# equal by tests/test_approval_level.py. F5 was replaced by owner ruling D-8
# (`OI-16`): the vocabulary now has ONE home in `kitlib`, which this module
# already imports, and the pin retired with the restatement it guarded. Drift is
# unrepresentable rather than detected — the WI-448 declared-line precedent.
LADDER_RUNGS = _kitladder.LADDER_RUNGS


# THE OFF-SPINE SIBLING OF THE DIAL (owner ruling OI-30 D3, 2026-08-15).
#
# `human_approval_through` governs the SPINE tiers. The off-spine registries
# that carry an off-spine `status` cell — `interfaces.toml`, `external.toml`,
# `components.toml` — were governed by PROSE ONLY: their headers said the cells
# were the owner's to flip, and at any dial below 4 nothing refused a loop
# session that wrote `approved`.
#
# THE RULED SHAPE IS DERIVED, NOT DECLARED, and the owner's question is why:
# *"I thought this would follow the dev-stage directly? Why build a new enum?"*
# The proposal on the table was a new `[attestation] human_approval_registries`
# list; it was OVERTURNED because the registry-to-rung association ALREADY
# EXISTS in `spine_rules` — `boundary_incomplete` gates DevStg-Boundary on
# `external.toml`'s approvals, and `arch_incomplete` gates DevStg-Arch on the
# component registry. So the association is existing fact, and a second
# declaration of it would be a rival answer that agrees until someone edits one.
#
# NO NEW KEY AND NO NEW ENUM: authority over a status cell in registry R is
# whether R's stage rung is human-held under the EXISTING dial — derived rather
# than declared. WHICH registries that holds is the dial's answer, not a fixed
# list: at a dial holding every rung it is all of them, at this repo's none.
#
# AN UNMAPPED APPROVAL-CARRYING REGISTRY IS HELD. The map is small and the
# registries are optional, so "I do not know which rung governs this" must
# resolve toward more human involvement, exactly as `human_holds` resolves an
# unreadable dial and an unrecognized rung.
APPROVAL_RUNGS = {
    "external": "DevStg-Boundary",
    "interfaces": "DevStg-Arch",
    "components": "DevStg-Arch",
}


# THE SPINE SIBLING OF THE TABLE ABOVE (owner ruling 2026-09-01, WI-572).
#
# Same question, same fail-safe, different registries: which DevStg rung is a
# SPINE row approved INTO, so the dial can answer whether that tier's `Status`
# flip is the loop's act or the owner's. Keyed by registry STEM
# (`spine_carrier.stem`) rather than by tier letter because the two callers
# both hold a registry path and neither holds a tier — and because a stem
# survives a carrier change, which a `.toml` suffix would not.
#
# IT LIVES HERE BECAUSE IT HAS TWO CONSUMERS AND THEY MUST NOT DISAGREE. The
# mint (`intake._released_drafted_rows`) uses it to decide which Drafted rows a
# merge hands to an adjudicator; the brief
# (`adjudicate_brief.first_approval_values`) uses it to decide which of the rows
# it re-resolves LIVE that adjudicator may actually flip. It was two tables for
# one commit — a registry-keyed one in `intake` and a tier-keyed one in
# `adjudicate_brief` — and the brief's copy was consulted only for the
# amendment arm's aftermath, so the first-approval arm derived its `--approves`
# argument with no dial filter at all: at any dial holding a spine rung the
# brief rendered the owner's held rows as this session's to approve. One table
# with one predicate is what makes that unrepresentable rather than detected.
SPINE_APPROVAL_RUNGS = {
    "docs/requirements/system-requirements": _kitladder.STAGE_REQS,
    "docs/requirements/low-level-requirements": _kitladder.STAGE_LLREQS,
    "docs/test/test-cases": _kitladder.STAGE_TESTS,
}


def human_holds(docs, stage):
    """Is work at spine `stage` still the HUMAN's to approve?

    The one comparison every consumer makes, stated once. `stage` is
    `spine_rules.spine_stage`'s `DevStg-<Label>` answer — the rung currently in
    work — and a rung the declared level holds surfaces rather than dispatching.

    THE COMPARISON IS AN ORDINAL ON THE ONE LADDER (OI-21 -> WI-493). It reads through
    the ONE ladder. The dial names the highest rung a human still approves, so
    every rung AT OR BELOW it is held — the mirror of the at-or-above rule that
    selects checks. The form retired at OI-21 was `stage < level` over two
    DIFFERENT integer ladders, correct only while they happened to line up, and
    the shape retired at WI-493 was the table that bridged them; what makes the
    comparison sound now is that there is one ladder. That old coincidence is what
    the 2026-08-12 rung insert nearly broke, silently, in the direction of less
    human involvement.

    BOTH ENDS OF THE LADDER ARE ABSOLUTE, and they are now spelled as the values
    they always meant. `DevStg-Release` — the shipped default — holds everything
    including the close, because it is the top rung and everything is at or below
    it. `DevStg-Below` is the sentinel for "nothing is human-held": set below the
    ladder, no rung is at or below it. Only a dial between the two consults the
    stage at all.

    AN UNREADABLE STAGE IS HELD, and so is an UNRECOGNIZED rung label — the same
    conservative direction as an unreadable level. Note the deliberate asymmetry
    with `kitlib.ladder.stage_ord`, which RAISES on an unknown label: there, an
    unknown stage means the ladder moved under a cached value and the operator
    must see it; here, the question is who approves, and the only safe answer to
    "I do not recognize this rung" is "the human does".

    Implements: SR-137, SR-139, LLR-155
    """
    dial = approval_through(docs)
    if dial == _kitstage.BELOW:
        return False
    if dial == _kitladder.STAGE_RELEASE:
        return True
    if stage not in LADDER_RUNGS:
        return True
    return _kitladder.stage_ord(stage) <= _kitladder.stage_ord(dial)


def human_approves(docs, registry):
    """May only a HUMAN move the `status` cell of this off-spine `registry`?

    True means HELD — the cell is the owner's, in a reviewed Status-change
    commit. The mirror of `human_holds`, and deliberately the same shape: one
    predicate, one home, consulting one table.

    `registry` is the registry's STEM as the repo names it — `"interfaces"`,
    `"external"`, `"components"` — not a path, because the caller that knows it
    is a work item's action rather than a file reader.

    THREE ARMS, and only the third is new thinking:
      * MAPPED and its rung is human-held under `human_approval_through`
        -> True (held). At this repo's `DevStg-Needs` dial that is none.
      * MAPPED and its rung is not held -> False (a loop session may write it,
        because the project has declared that rung machine-approvable).
      * UNMAPPED -> True (held), FAIL-SAFE. A status-carrying registry nobody has
        associated with a rung is one nobody has ruled on, and the only safe
        answer to that is "the human does".

    THE WRITER-SIDE CONTRACT, stated here because this predicate is the only
    home for it. Any path that would set an off-spine `status` to `Approved` MUST
    consult this first and refuse when it answers True. Today the kit ships no
    such automated writer — off-spine approvals are hand-edited — so the
    live consumers are the dispatcher's attestation/gate arm (`dispatch.
    _kind_action`, which surfaces rather than dispatching a WI whose action
    would move a held registry's approvals) and `intake`'s snapshot/flip path,
    which is where the first machine writer would land. That is the honest
    statement of scope: the predicate is enforced where a writer exists, and it
    exists so the next writer cannot be added without meeting it."""
    rung = APPROVAL_RUNGS.get((registry or "").strip().lower())
    if rung is None:
        return True
    return human_holds(docs, rung)


def human_approves_spine(docs, registry):
    """May only a HUMAN flip this SPINE `registry`'s rows `Drafted` ->
    `Approved`? True means HELD.

    The spine mirror of `human_approves`, and deliberately the same three arms
    and the same fail-safe: mapped-and-held -> True, mapped-and-released ->
    False, UNMAPPED -> True. An approval-carrying registry nobody has associated
    with a rung is one nobody has ruled on, and the only safe answer to that is
    "the human does".

    `registry` is the registry's STEM as `SPINE_APPROVAL_RUNGS` keys it —
    `spine_carrier.stem("docs/test/test-cases.toml")`. Callers pass the stem
    rather than the path so the carrier suffix is normalised in the one module
    that owns "what a registry path is", not re-derived here.

    THE READER-SIDE CONTRACT, the half `human_approves` states for writers.
    Anything that tells a session which rows it may approve MUST filter through
    this — not only the path that mints the row, but every path that later
    re-resolves the population and renders it. The two are separated by a merge
    and a claim (`intake._released_drafted_rows` mints; `adjudicate_brief.
    first_approval_values` re-resolves live at composition time), and a filter
    applied at only one of them is a filter the brief does not have."""
    rung = SPINE_APPROVAL_RUNGS.get(str(registry or "").strip())
    if rung is None:
        return True
    return human_holds(docs, rung)


def final_review(docs):
    """Does the run stop for a FINAL human read even when the level let it
    close? `True` for the declared `"always"`, `False` for anything else.

    The separate end-of-run hold, split out from the ordinal because it is
    flipped far more often than the level is — and because conflating them
    would mean you could not ask for a closing read without also holding every
    tier. Defaults to holding: the shipped template declares `"always"`, and an
    unreadable value takes the same conservative direction every other dial in
    this module takes."""
    table = process_config(docs).get("attestation")
    if isinstance(table, dict):
        value = table.get("final_review")
        if isinstance(value, str):
            return value.strip().lower() != "off"
    legacy = legacy_approval(
        declared_policy(docs, "gate-policy", "attended"), "final_review"
    )
    return legacy != "off"


def complete_review(docs):
    """`(mode, rate)` for adjudicating a CLEAN close — `"off" | "sample" |
    "always"` and the sampling denominator.

    `partial` and `cancelled` closes are ALWAYS adjudicated: each carries a
    claim about what was not delivered, and a claim is what an adjudicator is
    for. A green close already passed the declared bar and the review rounds,
    so gating every one of them would rebuild the verdict gate under a new
    name — but never looking at any of them means the review rounds are the
    only thing that ever judged the work. The sample is the middle.

    An unreadable mode falls to `"sample"` (the shipped default) and a
    non-positive or unreadable rate to 4, because the failure that matters here
    is silently adjudicating NOTHING."""
    table = process_config(docs).get("attestation")
    mode, rate = "sample", 4
    if isinstance(table, dict):
        declared = table.get("complete_review")
        if isinstance(declared, str) and declared.strip().lower() in (
            "off",
            "sample",
            "always",
        ):
            mode = declared.strip().lower()
        n = table.get("complete_sample_rate")
        if isinstance(n, int) and not isinstance(n, bool) and n > 0:
            rate = n
    return mode, rate


def keep_nondependent(docs):
    """The orthogonal dial the ordinal cannot carry: may other lanes keep
    running while an approval is queued? Defaults FALSE — a queued
    approval drains the station, which is what `attended` and `autonomous`
    both did; only the retired `single-approve` level did otherwise."""
    table = process_config(docs).get("attestation")
    if isinstance(table, dict) and isinstance(table.get("keep_nondependent"), bool):
        return table["keep_nondependent"]
    legacy = legacy_approval(
        declared_policy(docs, "gate-policy", "attended"), "keep_nondependent"
    )
    return bool(legacy)


def spine_stage_of(root):
    """This repo's EFFECTIVE stage, through the common reader
    (`kitlib.stage.read_stage`) — the value `human_holds` compares the declared
    approval dial against, i.e. the input to who may approve.

    THE TRUST INVARIANT IS NOW TRUE BY CONSTRUCTION, and that is the whole point
    of this cut-over (WI-498 slice 5, ruled plan §3). The retired form scraped
    `stage=` off a comment on the generated `docs/gate` and justified itself by
    saying the file was freshness-gated, "so the cached value is either current
    or the `derived-gate` step is already red". THAT WAS NOT TRUE IN TWO PLACES
    the gate schedule map measured: the freshness step STANDS DOWN on a claimed
    branch, and `agent_loop`/`dispatch` hoist this value once per run and thread
    it down, so a mid-session approval was invisible to every later consumer.
    Both windows close here rather than being re-documented — the reader
    re-fingerprints the declared inputs on every call and derives fresh in memory
    when they have moved. It still never WRITES: regeneration stays the trunk
    regen points' auditable act.

    Returns None when the stage cannot be established at all — no `docs/stage`,
    an unparseable or hand-edited record, or a derivation that would not run.
    `human_holds` reads None as HUMAN-HELD, so every failure direction here ends
    in MORE human involvement, never less. That fail-safe is why this reader
    swallows the derivation error the CLI callers surface."""
    path = Path(root) / _kitstage.STAGE_FILE
    if not path.exists():
        return None
    try:
        record = _kitstage.read_stage(
            Path(root), lambda r: _kitstage.derive_via_subprocess(_SCRIPTS_DIR, r)
        )
    except (_kitstage.DerivationError, ValueError, OSError):
        return None
    stage = record.get("stage")
    return stage if isinstance(stage, str) and stage.startswith("DevStg-") else None


def _legacy_present(docs, legacy_name):
    return (Path(docs) / legacy_name).is_file()


def _in_legacy_window(value, legacy_values):
    """Is `value` EXACTLY one of the retired values a re-keyed dial still honours?

    A FUNCTION, NOT A BARE `in`, AND AN EXACT TYPE TEST, because Python's
    numeric tower makes the obvious spelling wrong three ways and each one fails
    silently — the migration window would swallow a malformed dial that the type
    check exists to name:

      * `True == 1`, so a `true` dial would pass for the ordinal 1 and take the
        window's silent pass instead of the wrong-type refusal it has earned;
      * `2.0 == 2`, so a float dial would too — a wrong-typed value falling
        through to a default with no diagnostic, which IS the failure this
        table's type check was written for;
      * an unhashable value (`[4]`, an inline table) raises `TypeError` from
        `in` against a set — and `config_conflicts` promises its callers it
        returns a list and never raises, because two of the three call it from
        inside an exit-code contract.

    `type(value) is int` refuses all three at once: `bool` and `float` are not
    `int`, and a non-int never reaches the membership test."""
    if type(value) is not int:
        return False
    return value in legacy_values


def _key_value_findings(data, section, key, kind):
    """Type, range and vocabulary findings for ONE declared dial ([] when absent
    or sound).

    Shared by both halves of `config_conflicts` — the legacy-file dials and the
    process.toml-only ones — because "a wrong-typed dial must never fall through
    to a default" is one rule, not two that happen to agree today."""
    table = data.get(section)
    if not (isinstance(table, dict) and key in table):
        return []
    value = table[key]
    legacy_values = PROCESS_KEY_LEGACY_VALUES.get((section, key))
    if legacy_values is not None and _in_legacy_window(value, legacy_values):
        # A value this dial USED to take, which the reader migrates and warns
        # about; refusing it here would be the kit refusing to start over a
        # spelling it already knows how to read. Anything outside the window —
        # including an out-of-range int — falls through to the findings below.
        return []
    if legacy_values is not None and type(value) is int:
        # AN INT OUTSIDE THE WINDOW: still refused, but by a message that names
        # the migration rather than the type. Whoever meets this is the one
        # person whose 0-4 dial was out of range BEFORE the re-key, and telling
        # them "expected str" while the four lines above silently accept 0-4 is
        # accurate and useless.
        return [
            "docs/{} [{}] {} = {!r} is the RETIRED 0-4 ordinal, out of range. "
            "There is no rung it meant, so it reads as the most conservative "
            "setting. Set it to a DevStg-* rung (or `{}` for 'nothing is "
            "human-held'); `bootstrap.py --migrate-config` converts an "
            "IN-range one for you.".format(
                PROCESS_TOML, section, key, value, _kitstage.BELOW
            )
        ]
    if _coerce(value, kind) is None:
        return [
            "docs/{} [{}] {} = {!r} is a {}, expected {} — a wrong-typed "
            "dial must never fall through to a default (a quoted "
            "`review_rounds` once meant NO review verdict was required).".format(
                PROCESS_TOML, section, key, value, type(value).__name__, kind
            )
        ]
    low_high = PROCESS_KEY_RANGES.get((section, key))
    if low_high and not (low_high[0] <= value <= low_high[1]):
        return [
            "docs/{} [{}] {} = {!r} is outside {}-{}. It falls back to the "
            "most conservative setting rather than being clamped: clamping a "
            "negative value would read as 'nothing is human-held' and "
            "silently disarm every approval hold in the repo.".format(
                PROCESS_TOML, section, key, value, low_high[0], low_high[1]
            )
        ]
    vocab = PROCESS_KEY_VOCAB.get((section, key))
    if vocab is not None and str(value).strip() not in vocab:
        # THE LEGACY ORDINAL IS NOT A CONFLICT. `approval_through` reads it,
        # translates it and warns; saying it twice — once as a refusal here and
        # once as a warning there — would make a kit upgrade look like a broken
        # config to a repo whose dial is merely old.
        if isinstance(value, int) and not isinstance(value, bool):
            return []
        return [
            "docs/{} [{}] {} = {!r} names no rung. Legal values are {} (and "
            "`{}` for 'nothing is human-held'). It falls back to the most "
            "conservative setting rather than to what was probably meant: an "
            "unrecognized dial that guessed would read as LESS human "
            "involvement than the owner asked for.".format(
                PROCESS_TOML,
                section,
                key,
                value,
                ", ".join("`{}`".format(r) for r in _kitladder.STAGE_ORDER),
                _kitstage.BELOW,
            )
        ]
    return []


def config_conflicts(docs):
    """The SN-028 MIXED-CONFIG refusal (plan §11.8): refusal strings naming
    every dial declared in BOTH `docs/process.toml` and its legacy one-word
    file, plus one line when process.toml exists but does not parse.

    Returns a LIST and never raises. Three entry points read policy without
    ever passing through `agent_loop.main` — `dispatch.run`, `intake`'s
    adjudication arm and `integrate`'s verdict gate — so the refusal has to
    live where the value is read, not at five call sites; and `dispatch.run`
    sits in the tick loop's caller, where a raised exception would rewrite an
    exit-code contract. Callers fold these into their own refusal lists.

    A downstream adopter never meets this un-aided: `bootstrap.py
    --migrate-config` converts the legacy files and deletes them, and both
    bootstrap and the documented re-sync run it.

    Implements: SR-137, SR-139, LLR-155
    """
    path = _process_toml_path(docs)
    if not path.is_file():
        return []
    data = read_toml(path)
    if not isinstance(data, dict):
        return [
            "docs/{} does not parse — every policy dial would silently read "
            "its default while the git hooks keep acting on the text. Fix the "
            "file; do not delete it.".format(PROCESS_TOML)
        ]
    out = process_shape_findings(docs)
    for (section, key), kind in sorted(PROCESS_ONLY_KEYS.items()):
        out.extend(_key_value_findings(data, section, key, kind))
    for legacy_name in sorted(PROCESS_KEYS):
        section, key, kind = PROCESS_KEYS[legacy_name]
        table = data.get(section)
        if not (isinstance(table, dict) and key in table):
            continue
        out.extend(_key_value_findings(data, section, key, kind))
        if _legacy_present(docs, legacy_name):
            out.append(
                "policy '{}' is declared TWICE - docs/{} [{}] {} and the legacy "
                "docs/{}. Run `python project-trajectory/scripts/bootstrap.py "
                "--migrate-config --dest .` from your kept kit checkout to fold "
                "the legacy file in and delete it; a mixed config is refused, "
                "never resolved by precedence.".format(
                    legacy_name, PROCESS_TOML, section, key, legacy_name
                )
            )
    return out


# The coordinator dials that live once in docs/stack.ini [agent-loop] instead of
# being duplicated across the agent-resume.{cmd,sh,command} launchers (IF-068,
# WI-274 part B). Each maps a stack.ini key to the AGENT_* env slot it now backs.
# `lanes` (WI-381, concurrency-v2 §A4.3) is the dispatcher's worker-lane
# ceiling: the TEMPLATE seeds 2, but an ABSENT key means 1 — docs/stack.ini is
# adopter-owned, so a re-sync never writes the key and a code default of 2
# would upgrade a long-adopted repo into concurrency silently.
AGENT_LOOP_DIALS = ("jobs", "model", "model-map", "lanes")


def read_agent_loop_config(docs):
    """The declared coordinator dials — the ``[agent-loop]`` section of
    ``docs/stack.ini`` (IF-068, WI-274). Returns a dict of the present dial keys
    (``jobs`` / ``model`` / ``model-map`` / ``lanes``) with surrounding
    whitespace stripped;
    an empty value, absent key/section/file, or an unreadable/malformed stack.ini
    all yield ``{}`` for that key (fail-soft — the AGENT_* env slots and the
    built-in defaults still apply, so a repo without the section behaves exactly
    as before, never-breaking).

    This is the DECLARED-FILE tier of the coordinator-dial precedence
    ``CLI flag > AGENT_* env > declared file > built-in default`` that
    ``agent_loop.main`` applies (so a one-dial owner change edits ONE file, not
    the same value in three launchers)."""
    import configparser

    cp = configparser.ConfigParser(interpolation=None)
    try:
        # An absent file -> cp.read returns [] (no exception); a present but
        # malformed/non-UTF-8 file degrades to {} rather than crashing the loop.
        if not cp.read(str(Path(docs) / "stack.ini"), encoding="utf-8"):
            return {}
    except (configparser.Error, OSError, ValueError, UnicodeDecodeError):
        return {}
    if not cp.has_section("agent-loop"):
        return {}
    out = {}
    for key in AGENT_LOOP_DIALS:
        if cp.has_option("agent-loop", key):
            val = cp.get("agent-loop", key).strip()
            if val:
                out[key] = val
    return out


def resolve_coordinator_dials(args, docs):
    """``(model, model_map)`` for the session engine, each resolved by the
    IF-068 precedence ``CLI flag > AGENT_* env > declared file > built-in
    default`` (WI-274 part B). ``args.model``/``args.model_map`` are ``None``
    when their flag was not passed; an empty env or declared value falls
    through (the launchers' "empty slot = default" convention, so the env path
    keeps working unchanged). Kept OUT of ``agent_loop.main`` so that hot
    function's complexity does not grow (the ratchet's escape hatch). (The
    ``jobs`` dial retired with the parallel dispatcher at
    concurrency-restructure Phase 5; a declared ``[agent-loop] jobs`` value is
    ignored.)"""
    dials = read_agent_loop_config(docs)
    model = (
        args.model
        if args.model is not None
        else (os.environ.get("AGENT_MODEL") or dials.get("model", ""))
    )
    model_map = (
        args.model_map
        if args.model_map is not None
        else (os.environ.get("AGENT_MODEL_MAP") or dials.get("model-map", ""))
    )
    return model, model_map


# What a `docs/work/pause` we cannot parse says. Fail-CLOSED: a broken pause
# file must never read as "not paused", and the message routes the human to the
# only two fixes. gen_trajectory.py carries a byte-identical copy (it does not
# import this coordinator layer); a test pins the two equal.
PAUSE_MALFORMED = "<malformed docs/work/pause — fix or delete it>"


def tracked_pause(docs_dir):
    """The **tracked** pause declaration — `docs/work/pause`
    (`docs/concurrency-restructure.md` §5.6). One meaning, and no scope field
    because one meaning needs none: **pause = stop claiming.** Everything in
    flight finishes, integrates, and archives — a traincar always unloads, so a
    pause never strands finished work on a branch; the only thing that stops an
    unload is the integrator's own refusal (red bar, missing verdict), which is
    the gate working, not the pause.

    Presence pauses. An **unpause is a tracked deletion commit** — which is the
    point of tracking the file: it survives clones, the reason is diffable
    history instead of a stale local note, and resuming is auditable.

    TOML, two keys: `reason` (free text) and `since` (a declared stamp, carried
    verbatim — never an age computed from a clock). Returns
    ``{"reason": ..., "since": ...}``, or ``None`` when the file is absent;
    `since` missing renders ``""``. Unparseable TOML or a missing `reason`
    returns a paused dict carrying `PAUSE_MALFORMED` — see above."""
    path = Path(docs_dir) / "work" / "pause"
    if not path.is_file():
        return None
    # `read_toml` folds absent into unreadable; the `is_file` guard above is
    # what keeps "no pause declared" (None) apart from "a pause declared in a
    # file we cannot parse" (PAUSED, malformed) — the fail-closed direction.
    data = read_toml(path)
    if not isinstance(data, dict) or not isinstance(data.get("reason"), str):
        return {"reason": PAUSE_MALFORMED, "since": ""}
    since = data.get("since")
    if since is None:
        since = ""
    elif not isinstance(since, str):
        since = str(since)  # a bare TOML date/int stamps as its ISO/decimal text
    return {"reason": data["reason"], "since": since}


def pause_reason(lane):
    """A declared **graceful-pause** request: pause the loop at the next session
    boundary. Return contract, unchanged and depended on by every caller:
    `None` = not paused; a string = paused, `""` when the declaration carries no
    reason. Presence is the whole contract — an unpause is a reviewed deletion
    commit of the one home, the TRACKED `lane/work/pause` (concurrency-
    restructure §5.6), read via `tracked_pause`. (The legacy untracked
    `lane/pause` half, WI-147, retired with the dispatcher at Phase 5.)

    Implements: SR-156, LLR-138
    """
    tracked = tracked_pause(lane)
    return None if tracked is None else tracked["reason"]


# --- WI-286: the harness interpreter (shared root .venv, floor-checked) --------
# A dispatcher train worktree has no .venv of its own, so a bare `python`/`pytest`
# run there resolves whatever is ambient on PATH (run 20260723T0202 inherited
# Python 3.8, below the floor): a below-floor idiom then passes locally and only
# fails in CI, and the pinned dev tools (requirements-dev.txt) may be absent. The
# fix is to run the harness under the repo's OWN .venv — the pinned ≥3.11
# toolchain — shared into each worktree by absolute path (the dispatcher points a
# worker's PATH at it and sets the integrator bar's {py} to it), plus a preflight
# so a below-floor interpreter is caught before it can produce a false green.

# The kit's Python floor (WI-262/WI-270; the setup scripts enforce the same
# `sys.version_info >= (3, 11)`). An adopter deliberately targeting an older
# product runtime lowers this alongside setup.{sh,ps1}'s own check.
MIN_PYTHON = (3, 11)


def venv_python(root):
    """Absolute path (a Path) to the repo's own .venv interpreter, or None when
    absent. Probes both layouts the kit's launchers do (check.sh, the pre-commit
    hook): POSIX `.venv/bin/python` and a Windows-created `.venv/Scripts/
    python.exe`, so a venv created on either OS is found from either (WI-286)."""
    root = Path(root)
    for rel in ("bin/python", "Scripts/python.exe"):
        cand = root / ".venv" / rel
        if cand.is_file():
            return cand
    return None


def harness_python(root):
    """The interpreter the test harness (pytest + the pinned dev tools) should run
    under for a worktree session: the repo's own .venv when present (shared by
    absolute path — one pinned ≥3.11 toolchain, no per-worktree install).
    Returns a str path — a bar runner substitutes it for {py} so the bar runs
    under the floor-satisfying interpreter even when the caller was itself
    launched on ambient Python (WI-286).

    The ambient `sys.executable` fallback is a DEFENSIVE default only (a
    stdlib-only resolver must return SOMETHING), and it is the honest answer
    ONLY for a repo that has not declared the pinned toolchain. A repo that has
    is refused UPSTREAM by `harness_floor_failures` below - integrate.py calls
    it before the bar - so a declared repo never reaches this fallback
    (WI-361; the dispatcher-era gate this replaces died at Phase 5)."""
    py = venv_python(root)
    return str(py) if py else sys.executable


def interpreter_version(exe):
    """(major, minor) of the interpreter at `exe`, or None when it cannot be run.
    `exe` None or equal to this process's own sys.executable reads sys.version_info
    directly (no subprocess); any other path is probed by RUNNING it, so a stale
    .venv reports its real version rather than this process's (WI-286)."""
    if exe is None or str(exe) == sys.executable:
        return sys.version_info[:2]
    try:
        proc = subprocess.run(
            [
                str(exe),
                "-c",
                "import sys;print(sys.version_info[0],sys.version_info[1])",
            ],
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
        )
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    parts = proc.stdout.split()
    try:
        return (int(parts[0]), int(parts[1]))
    except (ValueError, IndexError):
        return None


def harness_floor_failures(root):
    """WI-286/WI-361: a singleton list with a floor message when the interpreter
    the harness would run under is not a floor-satisfying, PINNED root .venv,
    else []. A tree without the repo's own .venv resolves ambient PATH (run
    20260723T0202 inherited 3.8), so a below-floor idiom passes locally and only
    fails in CI - and an ambient-MODERN interpreter is the worse half, clearing
    the version floor while lacking the pinned dev tools the bar assumes, which
    makes its green FALSE. integrate.py is the refusing seam: it calls this
    before the composed-tree bar rather than running the bar on ambient Python.

    ARMING BOUNDARY: the floor guards only a repo that DECLARES the pinned
    toolchain - concretely, one carrying `requirements-dev.txt` at its root. A
    repo without that declaration (a fresh scaffold, a test fixture, an adopter
    on another stack) never sees this refusal and keeps `harness_python`'s
    ambient fallback: there is no pin to hold it to, so refusing would enforce a
    contract it never opted into.

    Once armed it FAILS CLOSED on three shapes:

    - **no runnable root .venv at all** - absent, or a present-but-incomplete/
      corrupt layout (`venv_python` finds no interpreter). This must NOT fall
      back to the ambient interpreter (REVIEW-A MAJOR on WI-286);
    - a .venv whose interpreter cannot be run to report a version;
    - a below-floor .venv (< MIN_PYTHON).

    Returned as a LIST so a caller folds it into existing refusals with `+`."""
    if not (Path(root) / "requirements-dev.txt").is_file():
        return []
    floor = "{}.{}".format(*MIN_PYTHON)
    py = venv_python(root)
    if py is None:
        return [
            "no runnable ./.venv interpreter found under {} (absent, or an "
            "incomplete/corrupt .venv layout). This repo declares a pinned "
            "toolchain (requirements-dev.txt), so the harness - tests plus those "
            "pinned dev tools - must run under the repo's OWN Python {}+ .venv, "
            "NOT the ambient interpreter, which may clear the version floor yet "
            "lack the pinned tools and produce a false green. Run scripts/"
            "dev-setup --install to create ./.venv (WI-286/WI-361).".format(root, floor)
        ]
    ver = interpreter_version(py)
    if ver is None:
        return [
            "the ./.venv interpreter ({}) could not be run to check its version "
            "- recreate it (scripts/dev-setup --install; WI-286/WI-361).".format(py)
        ]
    if ver < MIN_PYTHON:
        return [
            "the repo ./.venv is Python {}.{} - below the {} floor. The harness "
            "(tests plus pinned dev tools) must run under a floor-satisfying "
            "interpreter, or a below-floor idiom passes locally and only fails in "
            "CI. Run scripts/dev-setup --install to (re)create ./.venv at Python "
            "{}+ (WI-286/WI-361).".format(ver[0], ver[1], floor, floor)
        ]
    return []


def _declared_test_command(ini, py=None):
    """The repo's declared test command as a tokenized argv, read from a
    docs/stack.ini path — the stack-schema home a bar runner reads so it runs
    the bar the repo actually declares. Mirrors check.py's stack schema rather
    than importing it — the OWNER_ONLY_PATHS precedent above: a CMP-008→CMP-007
    import for one small read would owe an IF seam; the tests pin it against
    drift. The kit schema is `[product] test` (with {py}/{src}/{tests} the same
    placeholders check.py fills), with the legacy raw `[stack] test` as a
    fallback. Returns None only when NEITHER key is present (a genuinely
    stackless profile → the caller legitimately skips); otherwise the argv —
    possibly [] for a declared-but-empty command, which the caller treats as a
    misconfiguration, not a skip (WI-285: a declared-but-unread key must not
    silently pass). Raises ValueError on an unreadable profile. `{py}` is `py`
    when given (the integrator points it at the repo's floor-satisfying .venv —
    WI-286), else this process's own interpreter."""
    import configparser

    cp = configparser.ConfigParser(interpolation=None)
    try:
        cp.read_string(Path(ini).read_text(encoding="utf-8-sig", errors="replace"))
    except (configparser.Error, OSError) as exc:
        raise ValueError(str(exc)) from exc
    if cp.has_section("product") and cp.has_option("product", "test"):
        subs = {
            "py": py or sys.executable,
            "src": cp.get("paths", "src", fallback="src"),
            "tests": cp.get("paths", "tests", fallback="tests"),
        }
        argv = []
        for tok in split_cmd(cp.get("product", "test")):
            for key, val in subs.items():
                tok = tok.replace("{" + key + "}", val)
            argv.append(tok)
        return argv
    if cp.has_section("stack") and cp.has_option("stack", "test"):
        return split_cmd(cp.get("stack", "test"))  # legacy raw: no substitution
    return None


# --- WI-148: weekday blackout window ------------------------------------------
# A declared `docs/blackout` policy: first non-comment line `HH:MM-HH:MM` (UTC),
# active Mon–Fri. Inside the window the coordinator starts no new session (the
# in-flight one already wrapped, the same graceful semantic as docs/pause) — it
# waits out the window, then resumes automatically, so a single walk-away launch
# survives the blackout. An absent/empty/malformed file, or `start == end`,
# disables it (byte-identical to a repo that never had the file — never-breaking);
# a fresh scaffold ships `12:00-12:00`, i.e. DISABLED but written in window
# SHAPE, so an adopter reads the format off the line they edit and inherits
# nobody else's hours (owner ruling 2026-08-11, WI-433).
BLACKOUT_RE = re.compile(r"^\s*(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})\s*$")


def parse_blackout(line):
    """Parse a `HH:MM-HH:MM` blackout line into `(start_min, end_min)` — minutes
    past UTC midnight — or `None` when absent/empty/malformed (an out-of-range
    hour or minute is malformed). Deliberately does NOT apply the `start == end`
    disable rule; the caller (blackout_wake) does, so the parse and the policy
    stay separately testable."""
    m = BLACKOUT_RE.match(line or "")
    if not m:
        return None
    sh, sm, eh, em = (int(g) for g in m.groups())
    if sh > 23 or eh > 23 or sm > 59 or em > 59:
        return None
    return (sh * 60 + sm, eh * 60 + em)


def blackout_wake(line, now):
    """Seconds until the current UTC weekday blackout window ends, or `None` when
    a new session is NOT blacked out at `now` — the file is absent/empty/
    malformed, the window is disabled (`start == end`), it is the weekend (the
    window is Mon–Fri only), or `now` falls outside the window. The window is
    half-open `[start, end)`: a session starting exactly at `end` is already
    clear (so 12:00–19:00 blocks 12:00 through 18:59 and releases at 19:00). A
    window whose start is after its end wraps past UTC midnight, honored on its
    start weekday. `now` is a naive UTC datetime (datetime.utcnow())."""
    win = parse_blackout(line)
    if win is None:
        return None
    start, end = win
    if start == end:
        return None  # the disable form
    if now.weekday() >= 5:  # Sat/Sun — the window is weekdays only
        return None
    minute = now.hour * 60 + now.minute
    inside = start <= minute < end if start < end else (minute >= start or minute < end)
    if not inside:
        return None
    wake = now.replace(hour=end // 60, minute=end % 60, second=0, microsecond=0)
    if wake <= now:  # a wrap window's end is tomorrow morning
        wake += datetime.timedelta(days=1)
    return int((wake - now).total_seconds())


# --- WI-261: blackout pause feedback (banner + countdown heartbeat) --------------
# The window SEMANTICS live in blackout_wake above; these render the WAIT so a
# walk-away launch reads as deliberately paused, not hung. All three are pure /
# injectable so the terminal feedback is testable without a real multi-second
# sleep. The scaffold's default cadence between countdown heartbeats (seconds).
BLACKOUT_HEARTBEAT_SEC = 300


def _fmt_hms(seconds):
    """Whole seconds as a compact `Hh Mm Ss`, dropping leading zero units but
    always keeping seconds: 25200 -> '7h 0m 0s', 90 -> '1m 30s', 45 -> '45s'."""
    seconds = int(seconds)
    hours, rem = divmod(seconds, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return "{}h {}m {}s".format(hours, minutes, secs)
    if minutes:
        return "{}m {}s".format(minutes, secs)
    return "{}s".format(secs)


def blackout_banner(window, resume_at, wake_seconds, policy_file="docs/blackout"):
    """The multi-line terminal banner shown when the coordinator holds a NEW
    session for the declared blackout window (WI-261). Pure: names the policy
    file, the raw `HH:MM-HH:MM` UTC `window`, its weekday-only scope, the resume
    time (`resume_at`, a naive UTC datetime), and how long the wait is
    (`wake_seconds`), so an unattended launch reads as deliberately WAITING, not
    hung. Returns the banner as one string (no trailing newline)."""
    bar = "=" * 70
    return "\n".join(
        [
            bar,
            "agent_loop: BLACKOUT — holding; no new session starts yet.",
            "  policy file : {}".format(policy_file),
            "  window      : {} UTC  (weekday-only, Mon–Fri; weekends run)".format(
                (window or "").strip()
            ),
            "  resuming at : {} UTC  (in ~{})".format(
                resume_at.strftime("%H:%M"), _fmt_hms(wake_seconds)
            ),
            "  honored by  : the agent-resume -> agent_loop path (waits in place)",
            "The loop is WAITING, not hung; it resumes automatically.",
            bar,
        ]
    )


def blackout_countdown_line(remaining_seconds, resume_at):
    """One countdown-heartbeat line emitted every BLACKOUT_HEARTBEAT_SEC while
    waiting out a blackout, so an unattended launch visibly ticks down rather
    than looking hung (WI-261). Pure: names the remaining wait and the UTC resume
    time (`resume_at`, a naive UTC datetime)."""
    return "agent_loop: blackout — ~{} remaining, resuming {} UTC.".format(
        _fmt_hms(remaining_seconds), resume_at.strftime("%H:%M")
    )


def blackout_wait(
    wake_seconds, window, resume_at, emit, sleep, interval=BLACKOUT_HEARTBEAT_SEC
):
    """Emit the blackout banner, then wait `wake_seconds` in `interval`-second
    steps, emitting a countdown heartbeat after each step (never a redundant one
    at zero, where the loop resumes). `emit(line)` prints a line and
    `sleep(secs)` waits — both injected so the feedback is deterministic under
    test with a captured `emit` and a no-op `sleep` (no real multi-second delay).
    The WAIT itself is unchanged: the total time slept is exactly `wake_seconds`
    (an interval <= 0 degenerates to a single full-length sleep, never a spin)."""
    emit(blackout_banner(window, resume_at, wake_seconds))
    remaining = int(wake_seconds)
    while remaining > 0:
        step = interval if 0 < interval < remaining else remaining
        sleep(step)
        remaining -= step
        if remaining > 0:
            emit(blackout_countdown_line(remaining, resume_at))


# --- WI-181: explicit worker assignment (LLR-061) --------------------------------
# A worker is one agent_loop process driving one claimed assignment on one
# branch in one worktree (the §2.3 claim model since concurrency-restructure
# Phase 5). Its inputs are explicit CLI arguments (never a lane file) and its
# result is committed evidence read back through git trailers.


WI_TOKEN_RE = re.compile(r"^WI-\d+$")

# (SANCTIONED_TRAIN_SUBJECT_PREFIXES and the WI-282 commit-msg trailer floor
# retired with the dispatcher at concurrency-restructure Phase 5.)

# The terminal work-item Statuses — no further build is owed (WI-267; the
# won't-build half respelled `cancelled` and given its own folder by WI-384).
# Mirrors check_trajectory.TERMINAL_STATUSES, kept inline here rather than
# imported: the F5 self-contained-script rule keeps agent_common stdlib-only (it
# never pulls a sibling engine). A worker must never build a WI in either state.
# SR-144 adds `partial`: a worker must refuse an assignment whose spec has
# already closed early exactly as it refuses one that shipped or was cancelled.
TERMINAL_STATUSES = ("done", "cancelled", "partial")


def sanitize_train(name):
    """A session tag becomes a log-file prefix and a reviews/ subdirectory,
    so restrict it to a safe slug (alnum + `.`/`-`/`_`, starts alphanumeric)
    — `--train` can then never traverse the tree. Returns the name or raises
    ValueError (preflight surfaces the message)."""
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name or ""):
        raise ValueError(
            "session tag {!r} must be a slug matching [A-Za-z0-9][A-Za-z0-9._-]* "
            "(starts alphanumeric; no path separators)".format(name)
        )
    return name


def parse_wi_list(spec):
    """The ordered assigned-WI list from a `;`/`,`/whitespace-joined --wi value.
    Raises ValueError on an empty list, a malformed token, or a duplicate —
    a broken assignment must fail preflight, never half-run."""
    out = []
    for tok in re.split(r"[;,\s]+", (spec or "").strip()):
        if not tok:
            continue
        if not WI_TOKEN_RE.match(tok):
            raise ValueError(
                "--wi token {!r} is not a WI-### id (got --wi {!r})".format(tok, spec)
            )
        if tok in out:
            raise ValueError("--wi names {} twice".format(tok))
        out.append(tok)
    if not out:
        raise ValueError("--wi carries no WI-### id (got {!r})".format(spec))
    return out


# --- the spec-folder registry reader: ONE home since WI-448 -------------------
# `docs/work/<status>/WI-###-<slug>.md` — one Markdown spec per work item, its
# STATUS encoded as the DIRECTORY (docs/concurrency-restructure.md §2.1). The
# 270-line reader that used to sit here VERBATIM, and identically in the other
# two of schedule.py, check_trajectory.py and agent_common.py, now lives once in
# `kitlib/registry.py`: owner ruling D-8 (`OI-16`, inversion confirmed
# 2026-08-13) retired the F5 no-shared-module rule that had licensed the copies.
#
# RE-EXPORTED under the names this module has always carried, so no call site
# and no test that reads `agent_common.<name>` changes with the move. The names are
# listed one per line rather than star-imported because this module's public
# surface is a fact its readers check, not a wildcard.
WI_COLUMNS = _kitregistry.WI_COLUMNS
SPEC_SCALARS = _kitregistry.SPEC_SCALARS
SPEC_LISTS = _kitregistry.SPEC_LISTS
SPEC_STATUS_DIRS = _kitregistry.SPEC_STATUS_DIRS
SPEC_FENCE = _kitregistry.SPEC_FENCE
SPEC_DELIVERABLE = _kitregistry.SPEC_DELIVERABLE
SPEC_HANDBACK = _kitregistry.SPEC_HANDBACK
SPEC_CONTEXT = _kitregistry.SPEC_CONTEXT
spec_work_dir = _kitregistry.spec_work_dir
spec_files = _kitregistry.spec_files
parse_spec_frontmatter = _kitregistry.parse_spec_frontmatter
parse_spec_status = _kitregistry.parse_spec_status
parse_spec_id = _kitregistry.parse_spec_id
parse_spec_deliverable = _kitregistry.parse_spec_deliverable
parse_spec_row = _kitregistry.parse_spec_row
read_spec_rows = _kitregistry.read_spec_rows


def load_registry_rows(root):
    """The work-item rows from the one registry home, `docs/work/` (the spec
    folder; status = directory). The CSV home retired at concurrency-
    restructure Phase 5 (RULING-4: no CSV in any form); an absent folder reads
    as an empty registry, the non-adopter posture."""
    work_dir = spec_work_dir(Path(root) / "docs" / "requirements" / "work-items.csv")
    return read_spec_rows(work_dir) if work_dir.is_dir() else []


def load_wi_registry(root):
    """{WI-ID: raw row dict} from the worktree's tracked WI registry — the
    checked-out copy on the train branch, so a worker reads the same registry
    state its base commit fixed. Malformed/duplicate ids are skipped (the
    validator's finding, not the worker's crash). Reads whichever home is
    authoritative via `load_registry_rows`; the rows are the same 18 keys either
    way, so every caller of this map is unaffected by the migration."""
    rows = load_registry_rows(root)
    out = {}
    for r in rows:
        wid = (r.get("WI-ID") or "").strip()
        if WI_TOKEN_RE.match(wid) and wid not in out:
            out[wid] = r
    return out


# The trailer-evidence log format (shared by the worker- and dispatcher-side
# readers). The leading "T" sentinel keeps the first field intact through
# git()'s stdout .strip() — a commit whose WI field is empty would otherwise
# lose its leading tab and shift every field left.
TRAILER_EVIDENCE_FMT = (
    "T%x09"
    "%(trailers:key=WI,valueonly,separator=;)%x09"
    "%(trailers:key=Blocked-WI,valueonly,separator=;)%x09"
    "%(trailers:key=BlockRef,valueonly,separator=;)"
)


def latest_trailer_evidence(log_out):
    """Fold a newest-first trailer log (TRAILER_EVIDENCE_FMT) into
    (built:set, blocked:map) where each WI is claimed by its LATEST trailer
    ONLY — the two buckets are disjoint. A newer `WI:` completion supersedes an
    older `Blocked-WI:` for the same id (a CURED blocker), and a newer
    `Blocked-WI:` supersedes an older `WI:` (the block is newer truth). `git
    log` emits newest-first, so the FIRST commit that names a WI (in either
    trailer) fixes its verdict; within one commit a completion wins. `blocked`
    maps a still-blocked WI to its committed BlockRef ('' when omitted)."""
    built, blocked, seen = set(), {}, set()
    for line in log_out.splitlines():
        parts = (line.split("\t")[1:] + ["", "", ""])[:3]
        for tok in (x.strip() for x in parts[0].split(";")):
            if WI_TOKEN_RE.match(tok) and tok not in seen:
                seen.add(tok)
                built.add(tok)
        refs = [t.strip() for t in parts[2].split(";")]
        for j, tok in enumerate(t.strip() for t in parts[1].split(";")):
            if WI_TOKEN_RE.match(tok) and tok not in seen:
                seen.add(tok)
                blocked[tok] = refs[j] if j < len(refs) else ""
    return built, blocked


def train_evidence(root, base):
    """(built, blocked) read from the train branch's committed trailers in
    base..HEAD: `built` is the set of WI ids whose LATEST trailer is the `WI:`
    completion; `blocked` maps a still-blocked `Blocked-WI:` id to its
    `BlockRef:` value (empty string when the commit omitted one). Per WI the
    newest trailer wins, so a resumed worker whose gate now passes supersedes
    its own earlier block by committing `WI:` (WI-239). This is the worker's
    one result channel — recovery reconstructs the same facts from git alone."""
    code, out = git(
        root, "log", "--format=" + TRAILER_EVIDENCE_FMT, "{}..HEAD".format(base)
    )
    if code != 0:
        return set(), {}
    return latest_trailer_evidence(out)


def _clip(text, limit):
    """Bound a prompt block: head lines up to `limit`, with an elision marker."""
    lines = (text or "").splitlines()
    if len(lines) <= limit:
        return "\n".join(lines)
    return "\n".join(lines[:limit] + ["… ({} more lines)".format(len(lines) - limit)])


# The per-worktree coordinator lock is a kernel ADVISORY lock (fcntl.flock on
# POSIX, msvcrt.locking on Windows) held on out/agent-loop.lock for this
# process's lifetime. The OS releases it automatically when the process exits —
# INCLUDING a crash or SIGKILL — so there is no stale-pid file to reason about
# and no PID-reuse hazard: the freed lock is simply available to the next run.
# The pid/host/stamp written into the file are human-readable DIAGNOSTICS only,
# never the liveness signal. The held descriptor lives in a module global so it
# (and thus the lock) stays open until release_lock / process exit.
_LOCK_FD = None


def _host():
    """This machine's name, for the lock file's human-readable diagnostics."""
    try:
        return socket.gethostname()
    except OSError:
        return ""


# On Windows the CRT lock is MANDATORY — it blocks other processes from reading
# the locked bytes — so we lock a single byte far beyond any real content. The
# human-readable diagnostics in bytes 0..N stay readable (e.g. git staging this
# file if a repo forgot to gitignore out/), while two coordinators still contend
# on the same byte range. POSIX flock is advisory and whole-descriptor, so it
# needs no offset games.
_WIN_LOCK_OFFSET = 1 << 40


def _take_os_lock(fd):
    """Take a non-blocking exclusive advisory lock on `fd`, raising OSError when
    another process already holds it. Platform-split, stdlib only."""
    if os.name == "nt":
        import msvcrt

        os.lseek(fd, _WIN_LOCK_OFFSET, os.SEEK_SET)
        try:
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        finally:
            os.lseek(fd, 0, os.SEEK_SET)
    else:
        import fcntl

        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)


# Errnos that mean "this filesystem cannot do advisory locks" (a network / exotic
# mount — flock returns these) as opposed to "the lock is held" (EWOULDBLOCK /
# EAGAIN / EACCES). On these we degrade to a warning instead of failing closed;
# every other error stays a refusal, so an unknown failure never silently drops
# the guard (fail-safe). Built via getattr so a name absent on a platform is just
# skipped.
_UNSUPPORTED_LOCK_ERRNOS = frozenset(
    getattr(errno, name)
    for name in ("ENOLCK", "ENOSYS", "EOPNOTSUPP", "ENOTSUP")
    if hasattr(errno, name)
)


def _read_holder(lock_path):
    """The holder's diagnostic line (pid host stamp) for an error message, or ''
    — best-effort; a mandatory Windows lock may block the read, which is fine."""
    try:
        return lock_path.read_text(encoding="utf-8").strip().replace("\n", " ")
    except OSError:
        return ""


def dispatch_lock_path(root):
    """The DISPATCH lock's one home: ``out/agent-loop.lock`` under `root`.

    The per-checkout coordinator lock the plain-launch dispatcher holds for its
    process lifetime (agent_loop `_coordinator_lock`) — and, since WI-381
    (concurrency-v2 §A4.1), the lock `integrate claim` REQUIRES: admission is
    the dispatcher's scheduling decision, so a hand claim while a dispatcher's
    lanes are live is unrepresentable (the lock cannot be taken), while a hand
    claim on an idle station still works. One path builder, because the holder
    and the requirer must name the same file by construction."""
    return Path(root) / "out" / "agent-loop.lock"


def _open_lock_fd(lock_path):
    """Open the lock file and try the kernel advisory lock, non-blocking:
    `(fd, None)` when locked, `(fd, exc)` when NOT — with the descriptor left
    OPEN either way, because the two callers disagree about what a failure
    keeps: `acquire_lock`'s degraded-filesystem arm writes diagnostics through
    it, while integrate.py's dispatch-lock rung (WI-381) closes it and
    refuses. One home for the open flags (O_BINARY keeps the diagnostic
    newlines untranslated on Windows)."""
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_RDWR | os.O_CREAT
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    fd = os.open(str(lock_path), flags, 0o644)
    try:
        _take_os_lock(fd)
    except OSError as exc:
        return fd, exc
    return fd, None


def acquire_lock(lock_path):
    """Take the per-worktree coordinator lock, or return an error string.

    Prevents two coordinators grinding the same checkout — a double-launch or a
    cron overlap — the one collision the branch guard can't catch (both would
    sit on the same llm/<track> branch in one worktree). The lock is a kernel
    advisory lock the OS grants atomically and releases on exit *or crash*, so a
    dead run never wedges the next one (no pid reasoning, no timer). Cross-host
    on a shared filesystem is best-effort only: flock over NFS is unreliable, so
    this guards one checkout on one host — the common and important case. A
    filesystem that cannot lock at all (ENOLCK/ENOTSUP) degrades to a warning and
    runs unguarded rather than fail-closed on a legitimate run.

    Implements: SR-027, LLR-029, LLR-030
    """
    global _LOCK_FD
    fd, exc = _open_lock_fd(lock_path)
    if exc is not None:
        if os.name != "nt" and exc.errno in _UNSUPPORTED_LOCK_ERRNOS:
            # This filesystem cannot do advisory locks (a network / exotic mount).
            # Degrade to a warning and proceed WITHOUT the guard rather than block
            # a legitimate run: the single-checkout guarantee is only lost on a
            # mount that never supported it, and the branch guard + git history
            # still backstop. Keep fd open (diagnostics written below) so the file
            # still records who is here.
            print(
                "agent_loop: WARNING - {} is on a filesystem that does not "
                "support advisory locks (errno {}); running WITHOUT the "
                "one-coordinator-per-checkout guard.".format(lock_path, exc.errno),
                file=sys.stderr,
            )
        else:
            os.close(fd)
            return (
                "another coordinator holds {} — refusing to run two in one "
                "worktree (held by: {}). It clears itself when that run exits; "
                "wait for it, or delete the file only if you are sure that run "
                "is gone.".format(lock_path, _read_holder(lock_path) or "unknown")
            )
    # We hold the lock: overwrite the diagnostics (a crashed predecessor may have
    # left its own). Best-effort — the OS lock, not this content, is the guard.
    try:
        os.ftruncate(fd, 0)
        os.write(
            fd,
            "{}\n{}\n{}\n".format(
                os.getpid(), _host(), time.strftime("%Y-%m-%d %H:%M:%S")
            ).encode("utf-8"),
        )
    except OSError:
        pass
    _LOCK_FD = fd
    return None


def release_lock(lock_path=None):
    """Drop the coordinator lock: closing the descriptor releases the OS lock.
    Idempotent, and a no-op if we never held it; the OS would release on exit
    regardless (the crash path relies on exactly that). `lock_path` is accepted
    for the atexit call signature but unused — the held descriptor is the
    authority, so a reclaimed-then-exited predecessor never disturbs a successor."""
    global _LOCK_FD
    if _LOCK_FD is not None:
        try:
            os.close(_LOCK_FD)
        except OSError:
            pass
        _LOCK_FD = None


def parse_map(spec):
    """Parse a KEY=value phase map — shared by --model-map/--cmd-map/--prompt-map/
    --tier-map/--prefer-map: "P0=model-a,strong=model-b" -> {"P0": "model-a",
    "strong": "model-b"}."""
    mapping = {}
    for pair in (spec or "").replace(";", ",").split(","):
        pair = pair.strip()
        if not pair:
            continue
        if "=" not in pair:
            raise ValueError("--model-map entry without '=': {}".format(pair))
        phase, _, model = pair.partition("=")
        mapping[phase.strip()] = model.strip()
    return mapping


_SPLIT_RE = re.compile(r"[;,\s]+")


def _read_csv_rows(path):
    """CSV rows of `path` as dicts, or [] (absent/unreadable). utf-8-sig so an
    Excel-written BOM can't rename the first header key (a BOM'd
    work-items.csv split the dispatcher's and the worker's view of the same
    registry, and a BOM'd system-requirements.csv silently vacated the
    critique gate — repo-review 2026-07-21 M-23); errors=replace so a stray
    byte degrades, never crashes (the declared-reader idiom). A real file
    handle (newline="") also keeps quoted multi-line cells parseable, unlike
    the old splitlines() feed."""
    try:
        text = Path(path).read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return []
    return _kitspine.csv_rows(text)


def _refs(cell):
    return [t for t in _SPLIT_RE.split((cell or "").strip()) if t]


def git(root, *args):
    """Run git in the repo; returns (returncode, text).

    On success `text` is stdout-stripped and byte-identical to the raw call —
    every success-path caller parses stdout (`rev-parse`, `status --porcelain`,
    trailer reads). But git reports hook rejections and fatal errors on STDERR,
    so on a NONZERO exit the stripped stderr is appended to stdout (newline-joined
    when both are non-empty); otherwise every failure detail a failed call feeds
    a park/quarantine reason (via `_failure_tail`) would be blank (WI-233)."""
    proc = subprocess.run(
        ["git", "-C", str(root)] + list(args),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,
    )
    out = (proc.stdout or "").strip()
    if proc.returncode != 0:
        err = (proc.stderr or "").strip()
        if err:
            out = out + "\n" + err if out else err
    return proc.returncode, out


# WI-240 -> WI-398: the harness/hook banner shape a structured failure prints —
# a `=== <step> : <cmd> ===` banner per step, then that step's output, then a
# `  {STATUS}  <step>  <detail>` line — PLUS check.py's closing summary block,
# which re-prints every step's status after a bare `====...` rule at any --jobs.
_FAILTAIL_FAIL_RE = re.compile(r"^\s*FAIL\s")
_FAILTAIL_BANNER_RE = re.compile(r"^\s*=== ")
_FAILTAIL_RULE_RE = re.compile(r"^\s*={8,}\s*$")


def _failure_tail(out, budget=600):
    """The FAILING part of a harness/git output, bounded to `budget` chars.

    Park/quarantine/journal details once kept only the leading 200 chars — the
    HEAD — so a multi-step hook failure journaled the FIRST (passing) banner and
    cut the actual error (the WI-229 blocked-disposition loop). WI-240's answer
    — the LAST `  FAIL  <step>` line, walked back to the nearest banner — broke
    on a full check.py run: the closing summary RE-prints every step's status,
    so the last FAIL was always the summary copy, the nearest banner above it
    the LAST step's, and the extracted window was summary rows — the failing
    step's own output structurally never reached a refusal, at any --jobs
    (WI-398; the WI-387 refresh red cost three lost diagnoses of one failure).

    Now the FIRST `  FAIL  <step>` line names the failing step, and the window
    is that step's OWN `=== <step> :` banner down to the next banner or the
    summary rule, with the anchoring FAIL line appended when it sits outside
    the window (the --jobs 1 shape, where statuses print only in the summary).
    No banner names the step -> the nearest banner above that FAIL line; no
    FAIL marker at all -> the TAIL of the output; always tail-bounded, so the
    error survives even when the window is long."""
    text = (out or "").rstrip()
    if not text:
        return ""
    lines = text.splitlines()
    fail_idx = next(
        (i for i, ln in enumerate(lines) if _FAILTAIL_FAIL_RE.match(ln)), None
    )
    if fail_idx is None:
        return text[-budget:].lstrip()
    block = _own_step_window(lines, fail_idx)
    if block is None:
        # No banner names the step (a bare git/tool failure): the WI-240
        # window, anchored on the FIRST FAIL rather than the summary's copy.
        start = 0
        for j in range(fail_idx - 1, -1, -1):
            if _FAILTAIL_BANNER_RE.match(lines[j]):
                start = j
                break
        block = lines[start : fail_idx + 1]
    return "\n".join(block)[-budget:].lstrip()


def _own_step_window(lines, fail_idx):
    """The failing step's OWN banner-to-end block, or None (`_failure_tail`).

    `lines[fail_idx]` is a `  FAIL  <step>  <detail>` line; the window is the
    first `=== <step> : ` banner (startswith, not an interpolated regex — step
    names carry regex metacharacters, "tests+coverage") down to the next banner
    or the summary rule, with the anchoring FAIL line appended when it sits
    outside the window (the --jobs 1 shape). None when the line carries no step
    name or no banner names it, so the caller keeps its bounded fallback.

    Known limit (WI-398 REVIEW-A finding 1, pinned by WI-405): both anchors
    trust line SHAPE, so bar-shaped text EMBEDDED in a step's own captured
    output — a quoted FAIL row, a quoted banner, a nested scaffold bar naming
    another step — can silently misanchor the window onto a passing step's
    text; deliberately not parsed away (WI-398's scope guard), and on the
    refresh path the kept full log (out/run-logs/refresh-refused-<branch>.log)
    is the authority."""
    parts = lines[fail_idx].split()
    if len(parts) < 2:
        return None
    marker = "=== {} : ".format(parts[1])
    start = next(
        (j for j, ln in enumerate(lines) if ln.lstrip().startswith(marker)), None
    )
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if _FAILTAIL_BANNER_RE.match(lines[j]) or _FAILTAIL_RULE_RE.match(lines[j]):
            end = j
            break
    block = lines[start:end]
    if not start <= fail_idx < end:
        block = block + [lines[fail_idx]]
    return block


def head_sha(root):
    """Short HEAD sha, or None on a zero-commit repo (guarded rev-parse)."""
    code, out = git(root, "rev-parse", "--short", "HEAD")
    return out if code == 0 and out else None


def working_tree_dirty(root):
    """The `git status --porcelain` lines — one per uncommitted path (a rename is
    a single 'R  old -> new' entry, an untracked file a single '?? path' entry),
    or [] on a clean tree or a non-repo. Read through git() (text,
    errors=replace) so an odd byte in a path degrades rather than crashes (the
    sibling encoding-safe idiom). Used once at loop start to surface
    interrupted-session residue (WI-076)."""
    code, out = git(root, "status", "--porcelain")
    if code != 0:
        return []
    return [ln for ln in out.splitlines() if ln.strip()]


def _porcelain_path(line):
    """The repo-relative path a `git status --porcelain` line names — the
    destination side of a rename/copy (`R  old -> new`), surrounding quotes
    stripped — used to match a dirty line against OWNER_ONLY_PATHS. Splits the
    XY status token off the front rather than assuming a fixed column width (a
    leading blank status column may or may not survive to here)."""
    body = line.strip()
    if " -> " in body:
        return body.split(" -> ", 1)[1].strip().strip('"')
    parts = body.split(None, 1)  # status token, then the path
    return (parts[1] if len(parts) == 2 else body).strip().strip('"')


def substantive_working_tree_dirty(root):
    """`working_tree_dirty` minus the FB3 owner-only paths (OWNER_ONLY_PATHS) —
    the view the loop's WI-076 resume note (loop start) and done detection use,
    so a tree whose ONLY changes are the owner scratchpad (perpetually edited,
    never the loop's or a worker's deliverable) reads clean and the interrupted-
    residue signal fires only on genuine residue. The raw primitive stays
    available for a caller that wants every uncommitted path (WI-203)."""
    return [
        ln
        for ln in working_tree_dirty(root)
        if _porcelain_path(ln) not in OWNER_ONLY_PATHS
    ]


def current_state_excerpt(status_path, max_lines=40):
    """The '## Current State' section of a status.md — the root dispatcher's or
    a track lane's own — the pending asks a stopping coordinator must surface in
    its exit banner."""
    try:
        lines = status_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return "({} not found — no asks to surface)".format(status_path)
    section, collecting = [], False
    for ln in lines:
        if ln.startswith("## "):
            if collecting:
                break
            collecting = ln.strip().lower().startswith("## current state")
            continue
        if collecting:
            section.append(ln)
    if not section:
        return "({} has no '## Current State' section)".format(status_path)
    section = [ln for ln in section if ln.strip()][:max_lines]
    return "\n".join(section)


def bounded_transcript(output):
    """Head + capped tail of a session transcript (the tracked-log bound)."""
    lines = output.splitlines()
    if len(lines) > LOG_HEAD_LINES + LOG_TAIL_LINES:
        elided = len(lines) - LOG_HEAD_LINES - LOG_TAIL_LINES
        lines = (
            lines[:LOG_HEAD_LINES]
            + [
                "",
                "[... {} line(s) elided — full stream in out/run-logs/ ...]".format(
                    elided
                ),
                "",
            ]
            + lines[-LOG_TAIL_LINES:]
        )
    text = "\n".join(lines)
    encoded = text.encode("utf-8", "replace")
    if len(encoded) > LOG_MAX_BYTES:
        keep = LOG_MAX_BYTES // 2
        text = (
            encoded[:keep].decode("utf-8", "ignore")
            + "\n[... byte cap hit — full stream in out/run-logs/ ...]\n"
            + encoded[-keep:].decode("utf-8", "ignore")
        )
    return text


# THE CREDENTIAL CLASS VOCABULARY'S ONE HOME (WI-520). Derived from
# `kitlib.secret_classes.SECRET_CLASSES` — the same table
# `check_privacy.py`'s enforcement floor reads — so a class this redactor
# claims can no longer silently diverge from what the floor scans for. This
# closes the measured gap: a PEM private-key block used to reach this tuple
# as an "unknown token shape" (this function's own licensed gap, below) when
# it is in fact a known, compiled class one sibling module over; it is now
# `private key header`'s entry in the shared table, redacted here like every
# other declared class.
_SECRET_RES = tuple(
    cls.redact_pattern
    for cls in _kitsecrets.SECRET_CLASSES
    if cls.redact_pattern is not None
)


def redact_secrets(text):
    """Best-effort redaction of well-known credential shapes, applied before a
    transcript is committed to tracked history (docs/iteration/*.log): a CLI
    auth error echoing a key otherwise lands in permanent history with only
    push-policy between it and publication (repo-review 2026-07-21 M-19).
    The shapes are `kitlib.secret_classes`' redact-side classes (WI-520).
    Deliberately imperfect — unknown token shapes pass through, and the raw
    unredacted stream stays in gitignored out/run-logs/ for debugging."""
    hits = 0
    for rx in _SECRET_RES:
        text, n = rx.subn("[REDACTED]", text)
        hits += n
    return text, hits


def prompt_fingerprint(text):
    """A short, stable fingerprint of a rendered prompt — `sha256:` + 12 hex.

    Identification, not authentication: it answers "did these two sessions see
    the same instruction?" and "did the template change between these rows?"
    without keeping every rendered prompt on disk. Taken over the text as
    launched, so a slot fill that changed the prompt shows even when the
    template did not."""
    if text is None:
        return ""
    digest = hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()
    return "sha256:" + digest[:12]


def write_session_log(iter_dir, meta, transcript):
    """Write the tracked, size-bounded per-session log: a `# key: value`
    metadata header (what the index is regenerated from) + the transcript
    (credential shapes redacted — see redact_secrets).

    Implements: SR-176, LLR-177
    """
    transcript, redacted = redact_secrets(transcript)
    iter_dir.mkdir(parents=True, exist_ok=True)
    header = ["# agent-loop session log — written by scripts/agent_loop.py"]
    for key in (
        "session",
        "date",
        "train",
        "base",
        "phase",
        "wi",
        "model",
        "guardrails",
        "outcome",
        "commits",
        "tokens",
        "cost-usd",
        "wall-secs",
        "api-secs",
        "turns",
        "ttft-secs",
        "cache-read",
        "cache-create",
        "effort",
        "fast",
        "prompt-chars",
        # SN-026 (plan §11.7): WHICH TEMPLATE, and WHAT IT RENDERED TO.
        # `prompt-chars` alone answers "how big was it", which is the least
        # interesting question about a prompt. A prompt is now a reviewable
        # FILE (§8's externalization), so the useful telemetry is a pointer to
        # the source and a fingerprint of the result: two sessions that
        # disagree can be compared without keeping every rendered prompt on
        # disk, and a template edit becomes visible as a hash change across
        # otherwise identical rows. Truncated sha256 — this identifies, it does
        # not authenticate, and a full digest per row would dominate the header.
        "prompt-template",
        "prompt-sha",
        # Which deadline ended a TIMEOUT session — "wall" or "idle" (C3), ""
        # for every session that finished on its own. The label makes the two
        # kill classes distinguishable in telemetry without a transcript read.
        "timeout",
        # "relaxed" when a review verdict was drawn same-family under the C5
        # fallback rung (heterogeneity relaxed, recorded, never silent); ""
        # for every other session.
        "heterogeneity",
        "exit-code",
        # WI-535 (docs/plans/2026-08-29-adjudicator-session-retention-plan.md
        # §3.3, telemetry first, retention dial off): the CLI's own session
        # id and context occupancy/window/percent, per family — "" wherever
        # today's one-shot call doesn't report it (family_context_telemetry).
        "session-id",
        "context-used",
        "context-window",
        "context-pct",
    ):
        header.append("# {}: {}".format(key, meta.get(key, "")).rstrip())
    if redacted:
        header.append("# redacted: {} credential-shaped token(s)".format(redacted))
    header.append("# ---")
    # A worker's log name is prefixed with its train id (WI-181): two parallel
    # workers' committed session logs must never collide at integration.
    name = "{}-{}.log".format(meta["session"], meta["stamp"])
    if meta.get("train"):
        name = "{}-{}".format(meta["train"], name)
    path = iter_dir / name
    path.write_text(
        "\n".join(header) + "\n" + bounded_transcript(transcript) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def read_log_meta(path):
    """Parse the `# key: value` metadata header of one session log."""
    meta = {}
    try:
        with open(str(path), encoding="utf-8", errors="replace") as fh:
            for _ in range(32):
                line = fh.readline()
                if not line or line.startswith("# ---"):
                    break
                m = re.match(r"#\s*([\w-]+):\s*(.*)", line)
                if m:
                    meta[m.group(1)] = m.group(2).strip()
    except OSError:
        pass
    return meta


def per_turn_pace(meta):
    """API seconds per turn from a log's header meta — the like-for-like speed
    number across sessions of different lengths (a 100-turn build and a
    25-turn review compare honestly here, not on wall time). Empty when either
    field is absent (pre-WI-119 logs, errored sessions)."""
    try:
        api, turns = float(meta.get("api-secs", "")), float(meta.get("turns", ""))
    except ValueError:
        return ""
    return "{:.1f}".format(api / turns) if turns else ""


def per_turn_context(meta):
    """Average context carried per turn (cache-read tokens / turns, humanized
    to k) — the "how much is it re-reading every step" complexity number the
    per-session totals hide. Empty when the fields are absent."""
    try:
        read, turns = float(meta.get("cache-read", "")), float(meta.get("turns", ""))
    except ValueError:
        return ""
    return "{:.0f}k".format(read / turns / 1000.0) if turns else ""


def regenerate_index(docs_dir):
    """Rebuild docs/iteration_index.md from the docs/iteration/*.log metadata
    headers — generated, never hand-maintained (the kit's standing rule), so
    it survives manual log pruning and answers "which session did this"."""
    iter_dir = docs_dir / "iteration"
    rows = []
    for log in sorted(iter_dir.glob("*.log")):
        meta = read_log_meta(log)
        if not meta.get("session"):
            continue
        rows.append(
            "| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} "
            "| {} | [{}](iteration/{}) |".format(
                meta.get("session", ""),
                meta.get("date", ""),
                meta.get("phase", "") or "—",
                meta.get("wi", "") or "—",
                meta.get("model", "") or "—",
                meta.get("outcome", ""),
                meta.get("commits", "") or "—",
                meta.get("tokens", "") or "—",
                meta.get("cost-usd", "") or "—",
                meta.get("wall-secs", "") or "—",
                meta.get("api-secs", "") or "—",
                meta.get("turns", "") or "—",
                per_turn_pace(meta) or "—",
                per_turn_context(meta) or "—",
                # WI-535: the adjudicator-retention plan's telemetry-first
                # column — the CLI's own reported context occupancy, "—" on
                # every family/CLI call that doesn't report it yet.
                "{}%".format(meta["context-pct"]) if meta.get("context-pct") else "—",
                log.name,
                log.name,
            )
        )
    text = (
        "# Iteration index\n\n"
        "_Generated by `scripts/agent_loop.py` from the `docs/iteration/*.log`\n"
        "metadata headers — regenerated every session, never hand-edited. The\n"
        "collated human-review record is `log.md`; this index is the quick\n"
        '"which session did this" pointer (process-options.md "Unattended\n'
        'operation")._\n\n'
        "| # | Date | Phase | WI | Model | Outcome | Commits | Tokens | Cost USD "
        "| Wall s | API s | Turns | s/turn | Ctx/turn | Ctx % | Log |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
        + "\n".join(rows)
        + "\n"
    )
    (docs_dir / "iteration_index.md").write_text(text, encoding="utf-8", newline="\n")


def commit_telemetry(root, session, label, paths):
    """Commit the coordinator's own bookkeeping in its own `telemetry:` commit,
    right after it is written — so it never rides the next session's work commit
    or dangles in the tree (WI-137, the session-021 defect-shape). Stages only
    the named bookkeeping paths (the iteration log + regenerated index, the
    review scoreboard); the reviewer's verdict files commit themselves. Honors
    the hooks and is best-effort: nothing staged, or a hook veto, leaves the
    files in the tree exactly as before — never fatal, so the fix can only help
    (a walk-away run that today dangles telemetry keeps working either way)."""
    rels = []
    for p in paths:
        try:
            rels.append(os.path.relpath(str(p), str(root)))
        except ValueError:
            continue  # a path on another drive (Windows) — skip, never crash
    if not rels:
        return
    code, out = git(root, "status", "--porcelain", "--", *rels)
    if code != 0 or not out.strip():
        return  # unchanged bookkeeping — no empty commit
    code, staged = git(root, "diff", "--cached", "--name-only", "--", *rels)
    pre_staged = set(staged.splitlines()) if code == 0 else set()
    git(root, "add", "--", *rels)
    msg = "telemetry: session {} {}".format(session, label)
    code, out = git(root, "commit", "-q", "-m", msg, "--", *rels)
    if code != 0:
        # "Exactly as before" covers the index too: a veto must not leave the
        # bookkeeping staged for the next session's work commit to swallow.
        # Unstage only what this add staged; anything already staged stays.
        fresh = [r for r in rels if r.replace(os.sep, "/") not in pre_staged]
        if fresh:
            git(root, "reset", "-q", "--", *fresh)
        print(
            "agent_loop: telemetry commit skipped (session {}): {}".format(
                session, _failure_tail(out) or "hook veto or nothing staged"
            ),
            file=sys.stderr,
        )


def next_session_number(iter_dir, train=None):
    """Next NNN, continuing across coordinator restarts. A worker's numbering
    is scoped to its train prefix (WI-181) — parallel session numbers cannot
    collide because the (train, session) pair is the aggregation key."""
    pattern = re.compile(r"{}-(\d+)-".format(re.escape(train)) if train else r"(\d+)-")
    highest = 0
    if iter_dir.is_dir():
        for log in iter_dir.glob("*.log"):
            m = pattern.match(log.name)
            if m:
                highest = max(highest, int(m.group(1)))
    return highest + 1


def _iter_dir_list(iter_dirs):
    """Normalize the phase_draw_ordinal argument to a list of Paths — a single
    Path/str (the attended single-dir case) or an already-assembled iterable
    (the cross-train `draw_iter_dirs` list)."""
    if isinstance(iter_dirs, (str, Path)):
        return [Path(iter_dirs)]
    return [Path(d) for d in iter_dirs]


def phase_draw_ordinal(iter_dirs, phase):
    """The 0-based CROSS-TRAIN draw ordinal for `phase` (WI-263, repo-review
    M-31): how many PRIOR sessions — across EVERY train, not just this one —
    already ran this exact phase, counted from the durable session-log
    `# phase:` headers and de-duplicated by log filename across `iter_dirs`.
    This keys the weighted-rotation draw so each phase advances its OWN rotation
    (the global per-train session counter strides — a round is BUILD + REVIEW-A +
    REVIEW-B [+ CRITIQUE] — and would alias against the weight sum, starving
    weight-1 candidates) AND so the long-run provider frequency converges to the
    declared weights ACROSS trains (advertised weight 4 drawn ~4x as often — true
    across trains, not only within one multi-round train). WI-236 counted only
    THIS train's prefix, so a freshly minted train drew slot 0 deterministically
    and the weights were inert across trains (M-31); the caller now passes the
    durable aggregate — the PRIMARY worktree's committed docs/iteration plus this
    worker's own in-flight logs (see `draw_iter_dirs`). Reads existing state only
    (the logs already record the phase); no new durable store, no randomness.
    Empty phase / absent dirs -> 0 (the first draw)."""
    if not phase:
        return 0
    seen = set()
    count = 0
    for iter_dir in _iter_dir_list(iter_dirs):
        if not iter_dir.is_dir():
            continue
        for log in iter_dir.glob("*.log"):
            # De-dup by filename: the same committed log can appear in both the
            # primary aggregate and the local worktree (a train branched from the
            # development checkout carries its history); a session's log name is
            # unique ((train, session, stamp)), so first sighting counts it once.
            if log.name in seen:
                continue
            seen.add(log.name)
            if read_log_meta(log).get("phase", "") == phase:
                count += 1
    return count


def worktree_records(root):
    """Parsed `git worktree list --porcelain` records as (path, branch) pairs,
    in git's own order — the MAIN checkout always first (WI-263); branch is
    None when that worktree is detached. [] when git cannot answer (not a
    repo, git missing) — each caller chooses its own fail direction. The one
    porcelain walk, shared so the primary-checkout reader and the
    integrator's holder lookup cannot drift apart."""
    code, out = git(root, "worktree", "list", "--porcelain")
    if code != 0:
        return []
    records, path, branch = [], None, None
    for line in out.splitlines():
        if line.startswith("worktree "):
            if path is not None:
                records.append((path, branch))
            path = line[len("worktree ") :].strip()
            branch = None
        elif line.startswith("branch refs/heads/"):
            branch = line[len("branch refs/heads/") :].strip()
    if path is not None:
        records.append((path, branch))
    return records


def primary_worktree_root(root):
    """The MAIN (primary) worktree of `root`'s repo — the FIRST entry of
    `git worktree list --porcelain`, which git always lists ahead of the linked
    worktrees (WI-263). A dispatched worker runs agent_loop inside a linked TRAIN
    worktree; this is how it reaches the durable cross-train iteration aggregate
    that lives on the primary checkout. Returns a Path, or None when git can't
    answer (not a repo, git missing) — the caller then falls back to its local
    dir, so a draw never crashes."""
    records = worktree_records(root)
    if not records or not records[0][0]:
        return None
    return Path(records[0][0])


def draw_iter_dirs(root, local_iter_dir):
    """The iteration directories `phase_draw_ordinal` must union for a cross-train
    draw (WI-263, repo-review M-31). The old draw filtered same-phase logs by this
    train's own filename PREFIX, so the ordinal counted only the current train and
    reset every train — the declared weights never materialized across trains. A
    train branches from `integration_head`, so its LOCAL `docs/iteration` (in the
    linked worktree) already carries prior INTEGRATED trains' logs; dropping the
    prefix filter counts those. But the local dir is frozen at the branch base, so
    it MISSES a sibling train that integrates mid-flight (past this base), and the
    first-ever trains have no prior logs at all. The DURABLE cross-train aggregate
    that closes both gaps is the PRIMARY worktree's committed `docs/iteration` —
    the development checkout every INTEGRATED train's logs land on disk in
    (materialized by `publish_integration` -> `_sync_worktree`). Return that
    primary dir FIRST (its committed history is the authority for the filename
    de-dup) plus the local dir, whose not-yet-integrated in-flight logs keep the
    WITHIN-train rotation advancing between integrations. When the primary IS this
    root (an attended single-repo run, no linked worktree) the two coincide and
    only the one dir is returned."""
    local = Path(local_iter_dir)
    primary = primary_worktree_root(root)
    if primary is None:
        return [local]
    shared = primary / "docs" / "iteration"
    if _same_dir(shared, local):
        return [local]
    return [shared, local]


def _same_dir(a, b):
    """Whether two paths name the same directory, tolerant of symlinks and a
    not-yet-created dir (macOS /tmp -> /private/tmp; a fresh worktree). A wrong
    answer is only a lost optimization — `phase_draw_ordinal` de-dups by filename
    regardless — so any error just answers "different"."""
    try:
        return a.resolve() == b.resolve()
    except OSError:
        return a == b


def preflight(root, template, args):
    """Refuse to start iteration 1 on a broken footing. Returns the list of
    failures (empty = go).

    Implements: SR-027, LLR-027
    """
    failures = []
    if not template.strip():
        failures.append(
            "no agent command wired yet: fill the AGENT_CMD slot in "
            "agent-resume.cmd + agent-resume.sh (or pass --agent-cmd / set "
            "the AGENT_CMD env var). Example:\n"
            "    claude -p --model {model} --output-format json "
            "--dangerously-skip-permissions\n"
            "  (no {prompt} = the prompt is piped to the CLI's stdin — immune "
            "to OS command-line caps and Windows batch-shim shell re-parsing; "
            "a .cmd/.bat shim with {prompt} is refused, so use stdin or a "
            "native executable).\n"
            "  The permission-bypass flag is YOUR consent to unattended "
            "edits; leave it out to be prompted."
        )
        return failures  # nothing else is checkable without a command
    try:
        argv, _ = build_argv(template, "model", "prompt")
    except ValueError as exc:
        failures.append("cannot parse AGENT_CMD: {}".format(exc))
        return failures
    exe = argv[0]
    if not (shutil.which(exe) or Path(exe).exists()):
        failures.append(
            "agent CLI not found: {!r} is not on PATH. Install it (or fix "
            "AGENT_CMD), then re-run.".format(exe)
        )
    code, _ = git(root, "rev-parse", "--git-dir")
    if code != 0:
        failures.append(
            "{} is not a git repository — the loop reads commits as its "
            "progress signal.".format(root)
        )
    else:
        # SN-028: the mixed-config refusal rides the launchability preflight —
        # the one rung EVERY coordinator launch passes. The three entry points
        # that bypass agent_loop.main (dispatch, intake, integrate) each fold
        # `config_conflicts` into their own refusal, so no reader can be
        # reached through a half-migrated config.
        failures.extend(config_conflicts(root / "docs"))
        enabled = (
            declared_policy(root / "docs", "privacy-check", "false").lower() == "true"
        )
        if enabled:
            # Single-source the exempt allowlist: let check_privacy.py judge the
            # author email (it self-skips when the gate is off, so this fails
            # only on a genuinely private author on a privacy-checked repo).
            proc = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).resolve().parent / "check_privacy.py"),
                    "--root",
                    str(root),
                    "--author",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            if proc.returncode != 0:
                failures.append(
                    "privacy-check author identity violated: an unattended run "
                    "would commit every session under a private identity. "
                    + (proc.stderr or proc.stdout or "").strip()
                )
    # --- worker assignment preflight (WI-181, LLR-061) -----------------------
    # Re-grounded on the §2.3 claim model at concurrency-restructure Phase 5:
    # --wi alone is a full assignment (the session tag defaults to the current
    # branch name); --train survives as the optional explicit tag. A worker
    # still fails CLOSED off a branch — a claim is a branch, so a detached
    # HEAD is an unverifiable checkout.
    wi_spec = getattr(args, "wi", None)
    train = getattr(args, "train", None)
    if train and not wi_spec:
        failures.append(
            "--train is the worker session tag and needs the assignment; "
            "got --train without --wi"
        )
    if (wi_spec or train) and getattr(args, "interactive", False):
        failures.append(
            "--wi/--train is an unattended worker assignment; it cannot be "
            "combined with --interactive."
        )
    if wi_spec and not failures:
        try:
            assigned = parse_wi_list(wi_spec)
            if train:
                sanitize_train(train)
        except ValueError as exc:
            failures.append(str(exc))
        else:
            code, branch = git(root, "branch", "--show-current")
            if code != 0 or not branch:
                failures.append(
                    "a worker assignment runs on its claimed branch "
                    "(`integrate.py claim`), but this worktree's branch could "
                    "not be determined (detached HEAD, or git older than "
                    "2.22) — check the branch out first."
                )
            wi_rows = load_wi_registry(root)
            for wid in assigned:
                row = wi_rows.get(wid)
                if row is None:
                    failures.append(
                        "assigned {} is not in the docs/work/ registry on "
                        "this branch — a worker never builds an untracked "
                        "WI.".format(wid)
                    )
                elif (row.get("Status") or "").strip().lower() in TERMINAL_STATUSES:
                    # WI-267: a WI CANCELLED mid-assignment is terminal too — a
                    # worker must never build a WON'T-BUILD row. The scheduler
                    # never freshly dispatches a cancelled WI, but an owner can
                    # cancel one already leased to a worker; this closes that
                    # narrow mid-flight race the done-only check missed.
                    status = (row.get("Status") or "").strip().lower()
                    failures.append(
                        "assigned {} is already {} — a terminal status "
                        "(done/cancelled); a stale assignment, so the dispatcher "
                        "must re-derive the frontier.".format(wid, status)
                    )
    return failures


def stop_banner(status_path, label, detail=""):
    print("\n=== coordinator stopping: {} ===".format(label))
    if detail:
        print(detail)
    print("--- pending state ({} Current State) ---".format(status_path))
    print(current_state_excerpt(status_path))
    print(
        "--- end-of-run evidence: {0} | {1} | {2} ---".format(
            status_path,
            status_path.parent / "log.md",
            status_path.parent / "iteration_index.md",
        )
    )


# The console guard's one home is the shipped package (WI-448 / D-8); this
# module already imports `kitlib.config` under its guard above, so the alias
# rides that import rather than adding an unguarded second one.
_utf8_console = _kitconfig.utf8_console


def head_sha_full(root):
    """Full HEAD sha (reservation bases are exact, never abbreviated)."""
    code, out = git(root, "rev-parse", "HEAD")
    return out if code == 0 else ""
