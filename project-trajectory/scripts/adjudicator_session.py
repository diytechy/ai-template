"""The adjudicator session-retention layer (WI-540).

Plan of record: docs/plans/2026-08-29-adjudicator-session-retention-plan.md
(its §3 is this module function-by-function). One home for the layer's
mechanics: the runtime session STORE, the per-family resume-argv ADAPTER, the
per-family OCCUPANCY readers, the drain/reset RULE, and the keep-warm TICK
decision.

SHIPPED INERT. `docs/process.toml [adjudicator] context_reset_pct = 0`
(`agent_common.adjudicator_config(...).enabled == False`) short-circuits every
caller BEFORE it reaches this module — no session id minted, no resume argv, no
store written. Every function here runs only on the ON path, which the owner
turns on and verifies on-box in WI-541 (plan §5 step 4). Until then the OFF path
is byte-for-byte today's one-shot behaviour, and these functions are exercised
by their unit tests alone.

WHAT THIS LAYER IS NOT (plan §6, owner ruling OI-69 (a1)): no long-lived
process, no open stdin, no daemon. An adjudication is still ONE bounded headless
process exactly as today; the only difference when the dial is on is that the
process is launched with its family's *resume* form against a session the
coordinator minted earlier — a retained TRANSCRIPT a bounded process replays,
not a resident actor. SN-016's no-wedge invariant, the walk-away timeout and
IF-064's `run_session` contract are untouched.

stdlib only (CLAUDE.md); a coordinator-layer module, so it may import its
siblings (`agent_common`, `agent_session`) — it is NOT one of the
independently-copyable check scripts the F5 rule governs.
"""

import hashlib
import json
import os
import sys
import uuid
from pathlib import Path

# Sibling scripts, the sanctioned-sibling idiom the coordinator layer uses for
# each other (agent_loop's own import guard): a plain import resolves when the
# loop's dir is sys.path[0]; the fallback covers an in-process test import. Only
# `agent_session` (its `split_cmd`) is needed here; the config reader lives in
# `agent_common` but is called by the LOOP, never by this module.
try:
    import agent_session
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import agent_session

# --- the store's three states (plan §3.1) -------------------------------------
STATE_ACTIVE = "active"
STATE_DRAINING = "draining"
STATE_RETIRED = "retired"

# The per-family reset-percent cap (plan §2). codex's own
# `model_auto_compact_token_limit` is a ≤ 90% cap, so a dial above 85 is clamped
# to 85 (with a logged warning at the call site) and codex's own compaction is
# the backstop; claude's window is far above any sane dial and opencode leaves
# `compaction.auto` on, so neither clamps.
FAMILY_RESET_CAP = {"OPENAI": 85}

# The governing inputs whose change marks a session `draining` (plan §3.4 rule
# 2) — NOT `HEAD` (Sol #10): a session's judgement is only stale if the material
# it judges under changed. Missing files are skipped, so a repo without one of
# them simply hashes fewer inputs; the adjudicate-* prompt templates are folded
# in by the caller through `governing_hash`'s `template_paths` argument.
GOVERNING_INPUT_FILES = (
    "CLAUDE.md",
    "AGENTS.md",
    "GEMINI.md",
    "docs/process.toml",
)


# --- config: the per-family reset-percent clamp -------------------------------
def reset_pct_for_family(cfg, family):
    """The reset percent that applies to `family`, with the codex clamp (plan
    §2). Returns `(pct, clamped)` — `clamped` True when the dial was lowered, so
    the caller can log the warning once rather than silently. An inert config
    (`cfg.enabled == False`) yields `(0, False)`."""
    if not cfg.enabled:
        return 0, False
    cap = FAMILY_RESET_CAP.get((family or "").upper())
    if cap is not None and cfg.context_reset_pct > cap:
        return cap, True
    return cfg.context_reset_pct, False


# --- the session store (plan §3.1) --------------------------------------------
def store_dir(root):
    """`out/adjudicator/` under the repo root — runtime state, gitignored
    (`out/` is already ignored) and per-checkout, like `ctx.raw_dir`."""
    return Path(root) / "out" / "adjudicator"


def store_path(root, family):
    """The store file for one family: `out/adjudicator/<FAMILY>.json`."""
    return store_dir(root) / "{}.json".format((family or "").upper())


def load(root, family):
    """The family's stored record, or None when absent/unreadable/corrupt. A
    corrupt store reads as "no session" — the next launch mints fresh, which is
    always safe (the retained session is an optimisation, never a correctness
    input)."""
    try:
        text = store_path(root, family).read_text(encoding="utf-8")
        record = json.loads(text)
    except (OSError, ValueError):
        return None
    return record if isinstance(record, dict) else None


def save(root, record):
    """Write the record atomically: write-temp + `os.replace` (plan §3.1), so a
    keep-warm tick and an adjudication can never observe a half-written store.
    The caller holds the coordinator lock (Sol #18); this guarantees the file is
    never torn even if that discipline slips."""
    directory = store_dir(root)
    directory.mkdir(parents=True, exist_ok=True)
    path = store_path(root, record["family"])
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(record, sort_keys=True), encoding="utf-8", newline="\n")
    os.replace(tmp, path)


def retire(root, record):
    """Mark a record `retired` and persist it (the reset: "next launch is
    fresh", plan §3.4). The file is KEPT rather than deleted so the next mint can
    read the prior `generation` and increment it — the store counts how often the
    dial fired. A `dict` or None is accepted; None is a no-op."""
    if not isinstance(record, dict):
        return
    record["state"] = STATE_RETIRED
    save(root, record)


def clear(root, family):
    """Delete the family's store file outright — the hard reset. `retire` is the
    normal path (it keeps the generation count); `clear` exists for teardown and
    for a store a caller wants gone entirely. Absent file is a no-op."""
    try:
        store_path(root, family).unlink()
    except OSError:
        pass


def mint(family, route_id, session_id, governing_hash, started, window=""):
    """A fresh `active` store record for a newly minted session (plan §3.1).
    `generation` starts at 1 and rises each time this family's session is reset
    and re-minted, so the telemetry can count how often the dial fires."""
    return {
        "family": (family or "").upper(),
        "route_id": route_id or "",
        "session_id": session_id or "",
        "generation": 1,
        "started": started or "",
        "governing_hash": governing_hash or "",
        "window": window,
        "occupancy": "",
        "pct": "",
        "judged": [],
        "last_used": started or "",
        "state": STATE_ACTIVE,
    }


# --- the resume-argv adapter (plan §3.2) --------------------------------------
def resume_template(family, template, record):
    """Rewrite the one-shot `cmd_template` into its family's mint-or-resume form
    (plan §3.2), returning `(new_template, mint_session_id)`:

    - `record is None` -> MINT. ANTHROPIC gets a fresh `--session-id <uuid4>`
      and `mint_session_id` is that uuid (the id is known before launch); OPENAI
      and OPENCODE add their JSON flag so the id can be captured from the run's
      output afterwards, and `mint_session_id` is "".
    - `record` present -> RESUME against `record["session_id"]`;
      `mint_session_id` is "".

    The rewrite is TOKEN-level and returns a JSON-array template string, which
    `agent_session.split_cmd` parses unambiguously — so `{model}`/`{prompt}`
    placeholders survive for `build_argv`, which runs next and keeps its
    `(argv, stdin_input)` contract (IF-064) untouched."""
    tokens = agent_session.split_cmd(template)
    fam = (family or "").upper()
    session_id = record.get("session_id") if isinstance(record, dict) else None
    if fam == "ANTHROPIC":
        new_tokens, minted = _anthropic_tokens(tokens, session_id)
    elif fam == "OPENAI":
        new_tokens, minted = _codex_tokens(tokens, session_id)
    elif fam == "OPENCODE":
        new_tokens, minted = _opencode_tokens(tokens, session_id)
    else:
        return template, ""
    return json.dumps(new_tokens), minted


def _anthropic_tokens(tokens, session_id):
    """claude: mint appends `--session-id <uuid4>`, resume appends
    `--resume <id>` (plan §3.2). The prompt still rides stdin (the template
    carries no `{prompt}`), unchanged."""
    if session_id:
        return tokens + ["--resume", session_id], ""
    minted = str(uuid.uuid4())
    return tokens + ["--session-id", minted], minted


def _codex_tokens(tokens, session_id):
    """codex: mint adds `--json` (to capture `thread.started.thread_id`); resume
    is `codex exec resume <id> --json …` with **no `-C`** (cwd = repo) and **no
    `--ephemeral`** (plan §3.2). `resume <id>` is inserted right after the `exec`
    subcommand; both strips are defensive (the shipped row carries neither)."""
    tokens = _strip_flag(tokens, "-C", takes_value=True)
    tokens = _strip_flag(tokens, "--ephemeral", takes_value=False)
    if session_id:
        tokens = _insert_after(tokens, "exec", ["resume", session_id])
    return _ensure_flag(tokens, "--json"), ""


def _opencode_tokens(tokens, session_id):
    """opencode: mint adds `--format json`; resume additionally adds
    `--session <id>` (plan §3.2)."""
    tokens = _ensure_pair(tokens, "--format", "json")
    if session_id:
        tokens = tokens + ["--session", session_id]
    return tokens, ""


def _ensure_flag(tokens, flag):
    """`tokens` with `flag` present exactly once (append if absent)."""
    return tokens if flag in tokens else tokens + [flag]


def _ensure_pair(tokens, flag, value):
    """`tokens` with `flag value` present (append the pair if `flag` absent)."""
    return tokens if flag in tokens else tokens + [flag, value]


def _insert_after(tokens, anchor, inserted):
    """`tokens` with `inserted` spliced in right after the first `anchor` token;
    unchanged when `anchor` is absent."""
    if anchor not in tokens:
        return list(tokens)
    at = tokens.index(anchor) + 1
    return tokens[:at] + list(inserted) + tokens[at:]


def _strip_flag(tokens, flag, takes_value):
    """`tokens` with every `flag` removed (and its following value token when
    `takes_value`)."""
    out = []
    skip = False
    for tok in tokens:
        if skip:
            skip = False
            continue
        if tok == flag:
            skip = takes_value
            continue
        out.append(tok)
    return out


# --- dedicated CLI homes (plan §4 route_session env; owner ruling OI-69 (e1)) --
def dedicated_home_env(family, base_env, home_root):
    """The env additions that point a family's CLI at a dedicated home (OI-69
    (e1), applied ONLY once the dial is on): `CLAUDE_CONFIG_DIR` /
    `CODEX_HOME` / `OPENCODE_CONFIG` under `home_root`, plus claude's
    `CLAUDE_CODE_AUTO_COMPACT_WINDOW` left at the model window so provider
    compaction sits far above the kit's own reset (plan §2). Returns a dict to
    merge over `base_env`; the working directory (CLAUDE.md/AGENTS.md/skills)
    is untouched, so everything the kit mandates still loads (the owner's own
    (e) question, answered on record)."""
    fam = (family or "").upper()
    root = Path(home_root)
    env = {}
    if fam == "ANTHROPIC":
        env["CLAUDE_CONFIG_DIR"] = str(root / "claude")
    elif fam == "OPENAI":
        env["CODEX_HOME"] = str(root / "codex")
    elif fam == "OPENCODE":
        env["OPENCODE_CONFIG"] = str(root / "opencode")
    return env


# --- occupancy readers (plan §3.3) --------------------------------------------
def anthropic_occupancy(usage):
    """ANTHROPIC occupancy: the four `usage` counters summed
    (input + cache_read + cache_creation + output) — the SAME canonical tuple
    `agent_loop.family_context_telemetry` already computes for the telemetry
    columns (WI-535), reproduced here as a pure helper so the reset rule has one
    definition to read. Returns 0 when `usage` carries none of them."""
    keys = (
        "input_tokens",
        "output_tokens",
        "cache_read_input_tokens",
        "cache_creation_input_tokens",
    )
    return sum(usage.get(k) or 0 for k in keys) if isinstance(usage, dict) else 0


def codex_occupancy(events):
    """OPENAI occupancy: `token_count.info.last_token_usage.total_tokens` of the
    LAST such event (plan §3.3) — `codex exec --json`'s cumulative usage, read
    from the rollout events. Returns 0 when no event carries it."""
    total = 0
    for event in events or []:
        info = _dig(event, "token_count", "info", "last_token_usage", "total_tokens")
        if isinstance(info, int) and not isinstance(info, bool):
            total = info
    return total


def opencode_occupancy(events):
    """OPENCODE occupancy: the LAST `step_finish` event's
    `part.tokens.total` (plan §3.3). Returns 0 when no event carries it."""
    total = 0
    for event in events or []:
        if event.get("type") != "step_finish":
            continue
        value = _dig(event, "part", "tokens", "total")
        if isinstance(value, int) and not isinstance(value, bool):
            total = value
    return total


def _dig(mapping, *keys):
    """Walk a nested mapping by `keys`, returning None on any miss/non-dict —
    the tolerant reader a best-effort telemetry parse needs."""
    node = mapping
    for key in keys:
        if not isinstance(node, dict):
            return None
        node = node.get(key)
    return node


def pct_of(occupancy, window):
    """`round(occupancy * 100 / window)` when both are positive ints, else "" —
    a missing/zero window is NEVER guessed (plan §2: "a mismatch is logged,
    never guessed")."""
    if isinstance(window, int) and window > 0 and isinstance(occupancy, int):
        return round(occupancy * 100 / window)
    return ""


# --- the governing-inputs hash (plan §3.4 rule 2) -----------------------------
def governing_hash(root, template_paths=()):
    """A sha256 over the governing inputs (plan §3.4 rule 2): CLAUDE.md,
    AGENTS.md, GEMINI.md, docs/process.toml and the adjudicate-* prompt
    templates the caller resolves (`template_paths`) — NOT `HEAD`. A file's
    bytes are folded in under its relpath so a rename is a change; a missing
    file contributes nothing. Deterministic across runs (sorted, path-keyed)."""
    digest = hashlib.sha256()
    root = Path(root)
    paths = [root / rel for rel in GOVERNING_INPUT_FILES] + list(template_paths)
    for path in sorted(set(Path(p) for p in paths), key=lambda p: str(p)):
        try:
            data = Path(path).read_bytes()
        except OSError:
            continue
        digest.update(str(path).encode("utf-8"))
        digest.update(b"\0")
        digest.update(data)
        digest.update(b"\0")
    return digest.hexdigest()


# --- the drain / reset rule (plan §3.4) ---------------------------------------
def drain_reason(record, pct, reset_pct, governing_hash_now, version_now):
    """The reason to mark an `active` session `draining` (plan §3.4), or None to
    leave it active. Checked after every adjudication and before every launch.
    Cresting is NOT closing: this only flips the STATE; retirement waits for a
    clear point (`is_clear_point`).

      1. `pct >= reset_pct` (reset_pct 0 never crests — the OFF sentinel);
      2. the governing-inputs hash changed;
      3. CLI version drift (init version != current --version).

    A session already draining/retired stays as it is (returns None — no second
    reason overwrites the first)."""
    if not isinstance(record, dict) or record.get("state") != STATE_ACTIVE:
        return None
    if reset_pct and isinstance(pct, int) and pct >= reset_pct:
        return "crest {}% >= {}%".format(pct, reset_pct)
    stored_hash = record.get("governing_hash") or ""
    if governing_hash_now and stored_hash and governing_hash_now != stored_hash:
        return "governing-inputs changed"
    stored_version = record.get("cli_version") or ""
    if version_now and stored_version and version_now != stored_version:
        return "cli version drift {} -> {}".format(stored_version, version_now)
    return None


def retire_now_reason(is_error, terminal_ok, reset_on_same_artifact, next_ids, judged):
    """The reason to retire a session IMMEDIATELY, no drain (plan §3.4), or None:

    4. the session is UNUSABLE — `result.is_error`, a non-completed terminal
       reason, or a timeout (`is_error` true or `terminal_ok` false): corrupt
       or lost, so the next launch must be fresh;
    5. `reset_on_same_artifact` is on and the next row's WI or predecessor
       chain (`next_ids`) intersects what this session already `judged`
       (the strict rule-3 posture; default off — OI-69 (b1))."""
    if is_error or not terminal_ok:
        return "session unusable"
    if reset_on_same_artifact and set(next_ids or ()) & set(judged or ()):
        return "same-artifact guard"
    return None


def is_clear_point(pending_chain_ids):
    """True when a `draining` session may be retired now (plan §3.4): the
    adjudicator is at a CLEAR POINT — no rank-1 adjudication row belongs to a
    chain this session is already inside, and no active lane is out on work whose
    close would mint such a row. The caller computes that set; an empty set is
    the clear point. So a review -> worker -> return -> review loop is never cut
    mid-way — a draining session keeps being resumed for the rows that continue
    its chains until nothing of its own is pending."""
    return not pending_chain_ids


# --- keep-warm (plan §3.5; owner ruling OI-69 (c2)) ---------------------------
def keepwarm_due(record, cfg, family, now_epoch, last_used_epoch, work_pending):
    """Whether a keep-warm ping is due for this family's session (plan §3.5).

    ANTHROPIC only, and only when: `keepwarm_minutes > 0`; the session is
    `active`; there is work pending (the rank-1 queue is non-empty or a lane is
    active); and `now - last_used >= keepwarm_minutes`. The ping fires THROUGH
    the blackout (owner ruling OI-69 (c2)) — the earlier plan text that skipped
    it inside the blackout read the arithmetic backwards and is superseded. Other
    families' caches live minutes and are never pinged."""
    if not cfg.enabled or cfg.keepwarm_minutes <= 0:
        return False
    if (family or "").upper() != "ANTHROPIC":
        return False
    if not isinstance(record, dict) or record.get("state") != STATE_ACTIVE:
        return False
    if not work_pending:
        return False
    if not isinstance(last_used_epoch, (int, float)):
        return False
    return (now_epoch - last_used_epoch) >= cfg.keepwarm_minutes * 60
