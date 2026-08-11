"""Dogfood-sync: pin THIS repo's structure to the template it ships (WI-242).

The kit's product is the template in ``project-trajectory/``; this repo also
*uses* that template on itself. The governing rule (CLAUDE.md principles):

    VALUES may diverge between template and instance (owner dials, filled rows,
    enabled sets); STRUCTURE must not (schema headers, launcher command
    contracts, declared-section shapes).

This module is the enforcer. It asserts, for the live repo, that:

  * each live registry's COLUMN VOCABULARY agrees with its template's, by the
    rule its carrier makes checkable — an ordered superset for the CSV
    registries, a key-set containment for the TOML spine (see
    ``test_spine_template_declares_every_key_the_live_registry_uses``, which
    states why the direction had to invert);
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
import tomllib

import pytest

from conftest import ROOT, load_script

CARRIER = load_script("spine_carrier")

# --- census: live registry -> its shipped template ---------------------------
REGISTRIES = {
    # work-items left this census at the Phase 2c authority flip: the live
    # registry is the docs/work/ spec folder (whose exemplar is byte-pinned in
    # BOILERPLATE_COPIES below), and the CSV template survives only as the
    # legacy-format reference wi_convert.py migrates from — its schema is
    # pinned by test_wi_convert and test_plan_artifacts, not by a live copy.
    #
    # The three SPINE tiers left it at the carrier cutover: they
    # are TOML now, have no header to order, and are held by the key-set rule
    # below instead. Only the registries that stayed CSV are checked here.
    "docs/requirements/components.csv": "components.template.csv",
    "docs/requirements/interfaces.csv": "interfaces.template.csv",
    # WI-322 / 122-REVIEW-A: the new owner-decision registry was the ONE shipped
    # registry whose header was not locked to its live counterpart. Drifting
    # Status/Raised/OneLine in the template passed all 23 dogfood tests, and a
    # scaffold on that template then rendered "the owner queue is empty" for a
    # registry holding two pending decisions — exit 0, gate green, silent wrong
    # content on the surface a human rules from.
    "docs/requirements/open-items.csv": "open-items.template.csv",
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


# --- the spine's TOML carrier: a KEY-SET rule, not an ordered header ----------
# (The three tiers below moved carrier; `components`, `interfaces` and
# `open-items` did not, and stay on the ordered rule above.)
SPINE_REGISTRIES = {
    "docs/requirements/system-requirements.toml": (
        "system-requirements.template.toml",
        "requirement",
        "SR-ID",
    ),
    "docs/requirements/low-level-requirements.toml": (
        "low-level-requirements.template.toml",
        "design",
        "LLR-ID",
    ),
    "docs/test/test-cases.toml": ("test-cases.template.toml", "test", "TC-ID"),
}


def _toml_keys(path, table):
    """The union of keys the rows of one TOML registry set. UNION, never
    intersection: an absent key is a legitimately empty cell on an individual
    row, so a column exists in the registry iff SOME row uses it."""
    rows = tomllib.loads(path.read_text(encoding="utf-8"))[table]
    return {k for row in rows.values() for k in row}


def registry_key_drift(template_keys, live_keys, schema_keys, vocabulary):
    """None when template, live registry and the SCHEMA OF RECORD agree, else a
    message naming the first disagreement.

    THREE LEGS, because two could not close the loop. The first shipped rule
    compared only template against live, and that pair has a blind spot with a
    live example: `permutations` is declared by the template and used by NO live
    SR row, so it exists on exactly one side — and DELETING it from the template
    left both sides agreeing, silently. A rule whose two legs can both move
    together is not an anchor.

    `spine_carrier.SPINE_TIER_KEYS` is the third leg and the durable one: a
    STATED per-tier schema that neither the template nor the registry can edit
    by accident. The three rules:

      * template keys == the schema — the template is the copy-ready form OF the
        schema, so a dropped key and an invented key are both drift (this is the
        direction the two-leg rule could not see);
      * live keys ⊆ the schema — a registry may leave any column unused, but it
        may not invent one nobody shipped;
      * schema keys ⊆ the carrier VOCABULARY — nothing declared can be a cell
        the loader would silently drop on the way through.
    """
    missing = sorted(schema_keys - template_keys)
    if missing:
        return (
            "template no longer declares key(s) %s the tier schema states"
            % ",".join(missing)
        )
    invented = sorted(template_keys - schema_keys)
    if invented:
        return "template declares key(s) %s absent from the tier schema" % ",".join(
            invented
        )
    undeclared = sorted(live_keys - schema_keys)
    if undeclared:
        return "live registry uses key(s) %s the tier schema states nowhere" % ",".join(
            undeclared
        )
    unknown = sorted(schema_keys - set(vocabulary))
    if unknown:
        return "tier schema states key(s) %s the carrier cannot map" % ",".join(unknown)
    return None


@pytest.mark.parametrize("live_rel", sorted(SPINE_REGISTRIES))
def test_spine_template_declares_every_key_the_live_registry_uses(live_rel):
    """The TOML analogue of the ordered-header rule — and it had to INVERT.

    Under CSV the LIVE file declared its own schema in a header, so "template
    header is an ordered subsequence of the live header" was checkable and
    order meant something. TOML has neither: there is no header, key order in a
    table is not semantic, and an absent key IS the empty cell. So the live
    registry no longer declares a column it does not use — `Permutations` is
    the live case today, a column the CSV header carried with all 147 cells
    empty and which simply does not exist under TOML. Holding the live side to
    "declares every template column" would red on that legitimate state, and
    the only way to keep it green would be to stop checking, which is the
    "green hides a skipped check" failure SN-008 forbids.

    What survives is the same class of drift, anchored to a STATED schema
    (`spine_carrier.SPINE_TIER_KEYS`) rather than to whichever of the two
    artifacts happens to move. It is not vacuous: it caught two real drifts the
    ordered rule allowed by construction (the SR template had never declared
    `SupersededBy`, live since WI-229; the LLR template's `Component` cell was
    blank, so the converted template lost the column the CSV header had
    declared) — and the anchor closes the hole the first replacement still had,
    where dropping a template-only key like `permutations` passed.
    """
    tmpl_name, table, id_col = SPINE_REGISTRIES[live_rel]
    live = _toml_keys(ROOT / live_rel, table)
    tmpl = _toml_keys(TEMPLATE_DIR / tmpl_name, table)
    schema = set(CARRIER.SPINE_TIER_KEYS[id_col])
    assert live, live_rel  # a registry with no rows would make this vacuous
    assert schema, id_col  # ...and an empty schema would pass everything
    drift = registry_key_drift(tmpl, live, schema, CARRIER.SPINE_COLUMN)
    assert drift is None, "%s: %s" % (live_rel, drift)


def test_the_live_spine_carries_more_than_the_template_example(tmp_path):
    """The rule above is only worth having if the live registries are real.

    Guards against the shape where both sides shrink to the `-000` example and
    every containment holds trivially."""
    for live_rel, (_t, table, _id) in SPINE_REGISTRIES.items():
        rows = tomllib.loads((ROOT / live_rel).read_text(encoding="utf-8"))[table]
        assert len(rows) > 10, live_rel


# --- bite-proofs: each check FAILS on a mutated scratch copy -------------------
def test_bite_removed_live_registry_column():
    live = _header(ROOT / "docs/requirements/interfaces.csv")
    tmpl = _header(TEMPLATE_DIR / "interfaces.template.csv")
    assert registry_header_drift(tmpl, live) is None  # clean today
    mutated = [c for c in live if c != "Status"]  # owner drops a live column
    drift = registry_header_drift(tmpl, mutated)
    assert drift is not None and "Status" in drift


def test_bite_the_spine_key_rule_fails_on_a_planted_defect(tmp_path):
    """DRIVEN AGAINST REAL PLANTED DEFECTS, in temp copies of the real files —
    because a containment rule that cannot be made to fail is the vacuous green
    this suite exists to refuse.

    FOUR mutations, one per leg of the rule. The third is the one that matters
    most: the first replacement for the ordered-header rule PASSED it. Dropping
    `permutations` from the template moved the only side that declared it, and
    with nothing else to compare against, both sides agreed about a column that
    had quietly stopped being shipped. That is the shape SN-008 forbids, found
    in the replacement rather than in the thing it replaced.
    """
    live_rel = "docs/requirements/system-requirements.toml"
    tmpl_name, table, id_col = SPINE_REGISTRIES[live_rel]
    live_src = (ROOT / live_rel).read_text(encoding="utf-8")
    tmpl_src = (TEMPLATE_DIR / tmpl_name).read_text(encoding="utf-8")
    schema = set(CARRIER.SPINE_TIER_KEYS[id_col])

    live_copy = tmp_path / "live.toml"
    tmpl_copy = tmp_path / "tmpl.toml"

    def verdict(live_text, tmpl_text, schema_keys=None):
        live_copy.write_text(live_text, encoding="utf-8")
        tmpl_copy.write_text(tmpl_text, encoding="utf-8")
        return registry_key_drift(
            _toml_keys(tmpl_copy, table),
            _toml_keys(live_copy, table),
            schema if schema_keys is None else schema_keys,
            CARRIER.SPINE_COLUMN,
        )

    # Clean today, so every failure below is the mutation and not the fixture.
    assert verdict(live_src, tmpl_src) is None

    def _plant(text, header, line='owner_hat = "Systems"'):
        """Insert a line under `header`'s TABLE — matched at the start of a
        line, because both files MENTION the header inside a comment and a naive
        first-occurrence replace corrupts that comment instead."""
        out, planted = [], False
        for text_line in text.split("\n"):
            out.append(text_line)
            if not planted and text_line == header:
                out.append(line)
                planted = True
        assert planted, header
        return "\n".join(out)

    # (1) a live row quietly grows a column nobody shipped.
    drift = verdict(_plant(live_src, "[requirement.SR-001]"), tmpl_src)
    assert drift is not None and "owner_hat" in drift

    # (2) the template invents a key the schema does not state.
    drift = verdict(live_src, _plant(tmpl_src, "[requirement.SR-000]"))
    assert drift is not None and "owner_hat" in drift

    # (3) THE DROP DIRECTION — the hole the two-leg rule had. `permutations` is
    # declared by the template and used by NO live row, so removing it from the
    # template leaves template and live agreeing; only the stated schema still
    # remembers it.
    assert "permutations" in schema
    assert "permutations" not in _toml_keys(ROOT / live_rel, table), (
        "permutations is now used by a live row — re-pick a template-only key, "
        "or this mutation stops exercising the drop direction"
    )
    dropped = "\n".join(
        line for line in tmpl_src.split("\n") if not line.startswith("permutations = ")
    )
    drift = verdict(live_src, dropped)
    assert drift is not None and "permutations" in drift

    # (4) the schema itself states a key the carrier vocabulary cannot map, so a
    # scaffold would write cells the loader silently drops.
    drift = verdict(live_src, tmpl_src, schema_keys=schema | {"owner_hat"})
    assert drift is not None and "owner_hat" in drift


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
    check_trajectory SSOT findings, the critique dials, and the plan modes.

    Phase 5 note: ``critique_control`` takes a repo root and now reads only the
    ``docs/work/`` home, so over these CSV-only scratch roots it returns the
    default and contributes a CONSTANT. The width-neutrality claim rests on the
    three row-dict consumers; the dial stays in the tuple so a consumer that
    starts disagreeing across widths is still caught wherever it reads from."""
    schedule = load_script("schedule")
    ct = load_script("check_trajectory")
    al = load_script("agent_loop")
    pr = load_script("plan_runner")
    reg = root / "docs" / "requirements" / "work-items.csv"

    with reg.open(encoding="utf-8-sig", newline="") as fh:
        srows = list(csv.DictReader(fh))
    sched = tuple(
        # Both classifier axes (WI-383): a width change must move neither the
        # concurrency answer nor the rank, and reading only one would miss half.
        (
            rec["id"],
            rec["disposition"],
            rec["concurrency"],
            rec["rank"],
            rec["priority"],
        )
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
    reading a new column positionally.

    The optional cells are CLEARED in both shapes before comparing: that is
    the guarantee under test (an *empty* new cell), and a live row may now
    legitimately use one — WI-275's ``Priority=1`` (2026-07-23) was the
    column's first use, and a deliberate priority is *supposed* to change the
    schedule. A consumer reading a new column positionally still corrupts the
    core ten and fails here regardless of cell content."""
    # The live rows come from the registry's one home, the docs/work/ folder
    # (Phase 5: the CSV home retired), read through the validator's own loader —
    # which derives that folder from the CSV path it is still handed.
    ct_live = load_script("check_trajectory")
    live_rows = ct_live.read_registry_rows(ROOT / "docs/requirements/work-items.csv")
    wide_header = _header(TEMPLATE_DIR / "work-items.template.csv")
    optional = [c for c in wide_header if c not in _OLD_HEADER]
    rows = [
        {**{c: (r.get(c) or "") for c in wide_header}, **{c: "" for c in optional}}
        for r in live_rows
    ]

    legacy_root = tmp_path / "legacy"
    wide_root = tmp_path / "wide"
    _write_registry(legacy_root, _render(rows, _OLD_HEADER))
    _write_registry(wide_root, _render(rows, wide_header))

    assert _consumer_signature(legacy_root) == _consumer_signature(wide_root)


# test_live_work_items_header_matches_template_exactly retired at the Phase 2c
# flip: there is no live work-items CSV to compare. The 17-column schema stays
# pinned from both sides — wi_convert.COLUMNS against the shipped template
# (test_wi_convert) and plan_artifacts.WI_HEADER against the same template
# (test_plan_artifacts) — so the contract survives without a live copy.


# --- scaffold coverage: every bootstrap MAPPING destination exists here or is a
# declared omission (WI-251). The specs-README postmortem: docs/specs/ predated
# WI-053's spec-of-record machinery, the two boilerplate files were never
# backfilled, and 0/58 live specs carried the close-ritual boxes the absent
# exemplar stated — a one-time audit is not an invariant, so this walk is.

# dest -> one-line reason, owner-triaged 2026-07-20 (WI-251) and MOVED to a
# declared file by WI-308: `docs/declared-absences` is now the one home, because
# `check_doc_refs.py` needs the same facts (prose naming a path this repo
# declares it does not carry is untraced, not rot) and the kit's anti-duplication
# rule says state it once. The seam is the FILE, not an import — the checker is a
# stdlib-only kit script and must not reach into a test module. An entry whose
# destination MATERIALIZES must be removed (asserted below): the list can only
# shrink, never silently mask a backfill — except a `LIFECYCLE:`-marked reason,
# which declares a path whose presence is a legal state (WI-369; the marker is
# documented in the file's own header).
SCAFFOLD_OMISSIONS = load_script("check_doc_refs").load_declared_absences(
    ROOT / "docs" / "declared-absences"
)


def _stale_declared_absences(entries, exists):
    """Declared entries that have materialized, `LIFECYCLE:` rows exempt.

    The exemption is the MARKER's, not a general soft-pass: an unmarked entry
    that exists is stale wherever it appears (WI-369 — asserting absence of
    the lifecycle paths deadlocked the parallel-claims queue, since every
    composed tree holds the other branches' claim dirs)."""
    return [
        d
        for d, reason in entries.items()
        if not reason.startswith("LIFECYCLE:") and exists(d)
    ]


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
    # LIFECYCLE rows are exempt while present (their presence is the declared
    # legal state); everything else keeps the exact guard.
    stale = _stale_declared_absences(SCAFFOLD_OMISSIONS, lambda d: (ROOT / d).exists())
    assert not stale, "SCAFFOLD_OMISSIONS entries now materialized: {}".format(
        ", ".join(stale)
    )


def test_bite_lifecycle_exemption_is_marker_scoped():
    # Bite-proof both directions on a synthetic pair: the marked row is exempt
    # even when present, and the SAME situation unmarked is still flagged — so
    # the exemption cannot silently widen into a general soft-pass.
    entries = {
        "docs/ghost": "retired surface; recreating it must trip the guard",
        "docs/claim-dir": "LIFECYCLE: present only while work is claimed",
    }
    assert _stale_declared_absences(entries, lambda d: True) == ["docs/ghost"]
    assert _stale_declared_absences(entries, lambda d: False) == []


def test_the_lifecycle_rows_carry_the_marker():
    # The two lifecycle paths must stay marked in docs/declared-absences: an
    # edit dropping the marker re-arms the materialize-guard on a path that
    # legally exists mid-claim/mid-pause, which is the WI-369 deadlock.
    assert SCAFFOLD_OMISSIONS["docs/work/active"].startswith("LIFECYCLE:")
    assert SCAFFOLD_OMISSIONS["docs/work/pause"].startswith("LIFECYCLE:")


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


# --- dogfooded scaffold boilerplate: byte-identical to its template ------------
# 109-REVIEW-A MINOR: the MAPPING walk gates EXISTENCE; these four copies also
# carry the "STRUCTURE must not drift" intent, and — placeholder-free verbatim
# copies — their strongest cheap pin is byte identity (the gen_skills_index
# per-agent-copy idiom). A deliberate divergence would demote the entry to the
# header-superset treatment above, with the reason recorded here.
BOILERPLATE_COPIES = {
    "docs/work/queued/WI-000-example.md": "project-trajectory/work/WI-000.template.md",
    "docs/specs/README.md": "project-trajectory/specs/README.template.md",
    "docs/specs/WI-000.md": "project-trajectory/specs/WI-000.template.md",
    "docs/rubrics/README.md": "project-trajectory/rubrics/README.template.md",
    "docs/rubrics/rubric-000.md": "project-trajectory/rubrics/rubric-000.template.md",
}


@pytest.mark.parametrize("live_rel,tmpl_rel", sorted(BOILERPLATE_COPIES.items()))
def test_dogfooded_boilerplate_matches_template(live_rel, tmpl_rel):
    assert (ROOT / live_rel).read_bytes() == (ROOT / tmpl_rel).read_bytes(), (
        "{} drifted from {} — re-copy it (or demote this entry with a recorded "
        "reason)".format(live_rel, tmpl_rel)
    )
