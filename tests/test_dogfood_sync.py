"""Dogfood-sync: pin THIS repo's structure to the template it ships (WI-242).

The kit's product is the template in ``project-trajectory/``; this repo also
*uses* that template on itself. The governing rule (CLAUDE.md principles):

    VALUES may diverge between template and instance (owner dials, filled rows,
    enabled sets); STRUCTURE must not (schema headers, launcher command
    contracts, declared-section shapes).

This module is the enforcer. It asserts, for the live repo, that:

  * each live registry header is an ordered SUPERSET of its template header
    (live-only extensions like the SR ``SupersededBy`` column added in WI-229
    are legal; a *missing* template column is drift);
  * the root ``agent-resume.{sh,cmd,command}`` launchers structurally match
    their templates on the engine-invocation line (normalised for the meta-repo
    ``project-trajectory/`` path prefix + ``--root .`` self-application) and the
    exported ``AGENT_*`` variable-NAME set (template subset of live) — the owner
    DIAL VALUES (AGENT_CMD/AGENT_TIER_MAP/AGENT_JOBS/...) are explicitly free;
  * live ``docs/stack.ini`` declares every SECTION the template declares.

Each drift check is a pure function returning ``None`` (clean) or a message
naming the drifted surface; the bite-proof tests mutate scratch copies to prove
each one fails. A one-time behaviour-neutrality regression proves the WI-242
schema widening (work-items.csv 10 -> 17 columns) is invisible to every
registry consumer — an empty new cell means exactly what the absent column did.

dev-setup is deliberately NOT pinned: unlike the launchers (near-verbatim copies
+ owner dials), the live ``scripts/dev-setup.{sh,ps1,cmd,command}`` are bespoke
meta-repo rewrites (own install ladder, own CLI contract) with no shared
structural line — pinning them would be over-fitting, the exact anti-goal. The
one thing asserted is that they carry no ``agent_loop`` engine line, i.e. the
launcher engine-line pin correctly does not reach them.
"""

import csv
import io
import re

import pytest

from conftest import ROOT, load_script

# --- census: live registry -> its shipped template ---------------------------
REGISTRIES = {
    "docs/requirements/work-items.csv": "work-items.template.csv",
    "docs/requirements/system-requirements.csv": "system-requirements.template.csv",
    "docs/requirements/low-level-requirements.csv": "low-level-requirements.template.csv",
    "docs/requirements/components.csv": "components.template.csv",
    "docs/requirements/interfaces.csv": "interfaces.template.csv",
    "docs/test/test-cases.csv": "test-cases.template.csv",
}
TEMPLATE_DIR = ROOT / "project-trajectory" / "registries"

# The three root launchers vs their kit templates.
LAUNCHERS = {
    "agent-resume.sh": "project-trajectory/scripts/agent-resume.template.sh",
    "agent-resume.cmd": "project-trajectory/scripts/agent-resume.template.cmd",
}
STACK_LIVE = "docs/stack.ini"
STACK_TEMPLATE = "project-trajectory/stack.ini.template"


# --- pure drift checks (reused by both the live assertions and the bite-proofs)
def registry_header_drift(template_header, live_header):
    """None when every template column appears in live in the same relative
    order (an ordered subsequence, so live may add/extend), else a message
    naming the first template column that is missing or out of order."""
    it = iter(live_header)
    for col in template_header:
        if not any(x == col for x in it):
            return "template column %r missing from live header (or out of order)" % col
    return None


def _engine_line(text):
    """The real ``agent_loop.py`` invocation line, skipping comment lines (a
    ``#``/``REM`` comment mentioning the engine in prose is not the contract)."""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or stripped.upper().startswith("REM"):
            continue
        if "agent_loop.py" in line:
            return line
    return None


def _normalize_engine(line):
    """Reduce an agent_loop.py invocation to its structural token tuple: the
    script path is basenamed (the meta-repo runs it from project-trajectory/)
    and a ``--root <x>`` pair is dropped (the meta-repo self-application flag).
    What survives is the interpreter token, ``agent_loop.py``, and the argv
    pass-through (``"$@"`` / ``%*``)."""
    out, skip = [], False
    for t in line.split():
        if skip:
            skip = False
            continue
        if t == "--root":
            skip = True
            continue
        if "agent_loop.py" in t:
            t = re.split(r"[\\/]", t)[-1]
        out.append(t)
    return tuple(out)


def launcher_engine_drift(template_text, live_text):
    tl, ll = _engine_line(template_text), _engine_line(live_text)
    if tl is None or ll is None:
        return "no agent_loop.py engine line found"
    if _normalize_engine(tl) != _normalize_engine(ll):
        return "engine-line drift: template %r vs live %r" % (
            _normalize_engine(tl),
            _normalize_engine(ll),
        )
    return None


def _agent_vars(text):
    """The set of AGENT_* variable names the launcher declares, in either the
    POSIX (``AGENT_X=``) or the cmd (``set "AGENT_X=``) form."""
    names = set()
    for line in text.splitlines():
        m = re.match(r"\s*(AGENT_[A-Z_]+)=", line) or re.match(
            r'\s*set\s+"(AGENT_[A-Z_]+)=', line
        )
        if m:
            names.add(m.group(1))
    return names


def launcher_var_drift(template_text, live_text):
    missing = _agent_vars(template_text) - _agent_vars(live_text)
    if missing:
        return "live launcher missing exported vars: %s" % ",".join(sorted(missing))
    return None


def _sections(text):
    return [m.group(1) for m in re.finditer(r"(?m)^\[([^\]]+)\]", text)]


def stack_section_drift(template_text, live_text):
    live = set(_sections(live_text))
    for s in _sections(template_text):
        if s not in live:
            return "live stack.ini missing template section [%s]" % s
    return None


def _header(path):
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return next(csv.reader(fh))


# --- live assertions ----------------------------------------------------------
@pytest.mark.parametrize("live_rel,tmpl_name", sorted(REGISTRIES.items()))
def test_registry_header_is_template_superset(live_rel, tmpl_name):
    live = _header(ROOT / live_rel)
    tmpl = _header(TEMPLATE_DIR / tmpl_name)
    drift = registry_header_drift(tmpl, live)
    assert drift is None, "%s: %s" % (live_rel, drift)


@pytest.mark.parametrize("live_name,tmpl_rel", sorted(LAUNCHERS.items()))
def test_launcher_structural_match(live_name, tmpl_rel):
    live_text = (ROOT / live_name).read_text(encoding="utf-8")
    tmpl_text = (ROOT / tmpl_rel).read_text(encoding="utf-8")
    assert launcher_engine_drift(tmpl_text, live_text) is None, live_name
    assert launcher_var_drift(tmpl_text, live_text) is None, live_name


def test_launcher_command_wrapper_delegates():
    # The macOS Finder wrapper carries no engine line / dials of its own; its
    # structural contract is that it delegates to agent-resume.sh (both do).
    live = (ROOT / "agent-resume.command").read_text(encoding="utf-8")
    tmpl = (
        ROOT / "project-trajectory/scripts/agent-resume.template.command"
    ).read_text(encoding="utf-8")
    assert "exec ./agent-resume.sh" in live
    assert "exec ./agent-resume.sh" in tmpl


def test_stack_ini_declares_every_template_section():
    live = (ROOT / STACK_LIVE).read_text(encoding="utf-8")
    tmpl = (ROOT / STACK_TEMPLATE).read_text(encoding="utf-8")
    assert stack_section_drift(tmpl, live) is None


def test_dev_setup_carries_no_engine_line_to_pin():
    # dev-setup is a bespoke meta-repo rewrite, not a launcher: it invokes no
    # agent_loop engine, so the engine-line pin correctly does not apply. This
    # records that ruling executably (if a future dev-setup grew an engine line,
    # this flips and forces a deliberate decision about pinning it).
    for name in (
        "scripts/dev-setup.sh",
        "scripts/dev-setup.ps1",
        "scripts/dev-setup.cmd",
        "scripts/dev-setup.command",
    ):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert _engine_line(text) is None, name


# --- bite-proofs: each check FAILS on a mutated scratch copy -------------------
def test_bite_removed_live_registry_column():
    live = _header(ROOT / "docs/requirements/work-items.csv")
    tmpl = _header(TEMPLATE_DIR / "work-items.template.csv")
    assert registry_header_drift(tmpl, live) is None  # clean today
    mutated = [c for c in live if c != "Priority"]  # owner drops a live column
    drift = registry_header_drift(tmpl, mutated)
    assert drift is not None and "Priority" in drift


def test_bite_launcher_engine_line_edit():
    tmpl = (ROOT / "project-trajectory/scripts/agent-resume.template.sh").read_text(
        encoding="utf-8"
    )
    live = (ROOT / "agent-resume.sh").read_text(encoding="utf-8")
    assert launcher_engine_drift(tmpl, live) is None  # clean today
    # someone renames the engine entry point in the launcher
    mutated = live.replace("agent_loop.py", "agent_loop_v2.py")
    assert launcher_engine_drift(tmpl, mutated) is not None
    # or drops the argv pass-through
    mutated2 = live.replace('--root . "$@"', "--root .")
    assert launcher_engine_drift(tmpl, mutated2) is not None


def test_bite_missing_stack_section():
    tmpl = (ROOT / STACK_TEMPLATE).read_text(encoding="utf-8")
    live = (ROOT / STACK_LIVE).read_text(encoding="utf-8")
    assert stack_section_drift(tmpl, live) is None  # clean today
    mutated = re.sub(r"(?m)^\[tiers\].*?(?=^\[|\Z)", "", live, flags=re.DOTALL)
    drift = stack_section_drift(tmpl, mutated)
    assert drift is not None and "tiers" in drift


# --- one-time behaviour-neutrality regression (the WI-242 schema widening) -----
_OLD_HEADER = [
    "WI-ID",
    "Title",
    "Workstream",
    "SR-Refs",
    "Predecessors",
    "Status",
    "Deliverable",
    "SpecRef",
    "BuildTier",
    "SafetyClass",
]


def _write_registry(root, text):
    d = root / "docs" / "requirements"
    d.mkdir(parents=True, exist_ok=True)
    (d / "work-items.csv").write_bytes(text.encode("utf-8"))


def _render(rows, header):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(header)
    for r in rows:
        w.writerow([(r.get(c) or "") for c in header])
    return buf.getvalue()


def _consumer_signature(root):
    """Every registry consumer's output over the work-items.csv at ``root``,
    as one comparable tuple: schedule classification/disposition, the
    check_trajectory SSOT findings, the critique dials, and the plan modes."""
    schedule = load_script("schedule")
    ct = load_script("check_trajectory")
    al = load_script("agent_loop")
    pr = load_script("plan_runner")
    reg = root / "docs" / "requirements" / "work-items.csv"

    with reg.open(encoding="utf-8-sig", newline="") as fh:
        srows = list(csv.DictReader(fh))
    sched = tuple(
        (rec["id"], rec["disposition"], rec["sched_class"], rec["priority"])
        for rec in schedule.evaluate(schedule.load_wis(srows))
    )
    rows = ct.read_rows(reg)
    wis, integ = ct.load_wis(rows)
    ssot = tuple(sorted(ct.ssot_findings(wis, root)))
    crit = al.critique_control(root / "docs", {"WI-201", "WI-238", "WI-242"}, 3)
    modes = tuple(sorted({pr.wi_plan_mode(r) for r in rows}))
    return (sched, ssot, crit, modes, len(integ))


def test_schema_widening_is_behavior_neutral(tmp_path):
    """An empty new cell == the absent column, for every consumer: build a
    legacy 10-column shape and the migrated 17-column shape from the SAME live
    rows and assert identical consumer output. Directly proves the WI-242
    migration is behaviour-neutral, and would catch any consumer that started
    reading a new column positionally."""
    live_text = (ROOT / "docs/requirements/work-items.csv").read_text(encoding="utf-8")
    wide_rows = list(csv.DictReader(io.StringIO(live_text)))

    legacy_root = tmp_path / "legacy"
    wide_root = tmp_path / "wide"
    _write_registry(legacy_root, _render(wide_rows, _OLD_HEADER))
    _write_registry(wide_root, live_text)

    assert _consumer_signature(legacy_root) == _consumer_signature(wide_root)


def test_live_work_items_header_matches_template_exactly():
    # Post-migration the live work-items header is not merely a superset but an
    # exact match of the shipped template header (the widening adopted the full
    # 17-column schema in template order).
    live = _header(ROOT / "docs/requirements/work-items.csv")
    tmpl = _header(TEMPLATE_DIR / "work-items.template.csv")
    assert live == tmpl


# --- scaffold coverage: every bootstrap MAPPING destination exists here or is a
# declared omission (WI-251). The specs-README postmortem: docs/specs/ predated
# WI-053's spec-of-record machinery, the two boilerplate files were never
# backfilled, and 0/58 live specs carried the close-ritual boxes the absent
# exemplar stated — a one-time audit is not an invariant, so this walk is.

# dest -> one-line reason, owner-triaged 2026-07-20 (WI-251). An entry whose
# destination MATERIALIZES must be removed (asserted below) — the list can only
# shrink, never silently mask a backfill.
SCAFFOLD_OMISSIONS = {
    "GEMINI.md": "no Gemini agent in use; OpenCode/KIMI/GROK read AGENTS.md natively",
    "docs/process.md": "the master PROCESS.md lives in project-trajectory/ (status.md non-goal)",
    "docs/process-options.md": "the master PROCESS_OPTIONS.md lives in project-trajectory/ (status.md non-goal)",
    "docs/blackout": "absent = disabled, byte-identical, by the template's own spec",
    "docs/plan.md": "superseded by the trajectory layer + parallel dispatch (WI-252 mutual exclusion)",
    "docs/interfaces.md": "cross-project contract index; skip for a standalone deliverable (its own header)",
    "docs/requirements/performance-budgets.csv": "process.md §9 perf layer not enabled (opt-in, off-spine)",
    "docs/requirements/procurement.csv": "a meta-repo purchases no parts (opt-in, off-spine)",
    "docs/requirements/assets.csv": "a meta-repo ships no binary assets (opt-in, off-spine)",
    "run.cmd": "no product to launch (status.md non-goal; the launchers here are agent-resume.*)",
    "run.sh": "no product to launch (status.md non-goal)",
    "run.command": "no product to launch (status.md non-goal)",
    ".githooks/pre-push": "privacy-checked-repo backstop; docs/privacy-check declares off (owner-ruled out, WI-251)",
    ".github/workflows/check.yml": "test.yml's gate job runs the same check.py at the derived gate",
}


def _mapping_unaccounted():
    """MAPPING destinations neither present, nor kit-served in place, nor
    declared. A dest under scripts/ whose source ships in project-trajectory/
    is the meta-repo's in-place equivalent (CLAUDE.md repo map: the kit runs
    its own scripts from project-trajectory/scripts/, never copies them onto
    itself — that copy would be the drift this module exists to prevent)."""
    bootstrap = load_script("bootstrap")
    out = []
    for src, dst in bootstrap.MAPPING:
        if (ROOT / dst).exists():
            continue
        if dst.startswith("scripts/") and (ROOT / "project-trajectory" / src).exists():
            continue
        if dst in SCAFFOLD_OMISSIONS:
            continue
        out.append(dst)
    return out


def test_scaffold_mapping_covered_or_declared():
    missing = _mapping_unaccounted()
    assert not missing, (
        "bootstrap MAPPING destination(s) neither present, kit-served in place, "
        "nor declared in SCAFFOLD_OMISSIONS (dogfood the file or rule it out "
        "with a reason): {}".format(", ".join(missing))
    )


def test_scaffold_omissions_list_is_current():
    # The honesty half: a declared omission whose destination now EXISTS is a
    # stale entry — remove it, so the list documents only real absences.
    stale = [d for d in SCAFFOLD_OMISSIONS if (ROOT / d).exists()]
    assert not stale, "SCAFFOLD_OMISSIONS entries now materialized: {}".format(
        ", ".join(stale)
    )


def test_bite_scaffold_walk_catches_an_undeclared_absence():
    # Bite-proof: drop a declared omission and the walk must flag its dest.
    bootstrap = load_script("bootstrap")
    dests = {d for _, d in bootstrap.MAPPING}
    assert "docs/plan.md" in dests  # the walk actually covers the probe entry
    without = dict(SCAFFOLD_OMISSIONS)
    del without["docs/plan.md"]
    missing = [
        d
        for _, d in bootstrap.MAPPING
        if not (ROOT / d).exists()
        and not (d.startswith("scripts/"))
        and d not in without
    ]
    assert "docs/plan.md" in missing
