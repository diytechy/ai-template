"""HANDOFF 4.5.2, hand edits after r47a and n47a: the key `bar` is
`checks_stage` (row column `ChecksStage`) wherever it is spelled as a string,
and the sentences that name it.

check.py's flag has been `--stage` since WI-498 slice 2 (the code passes
`--stage`); sentences rewritten here say so instead of the earlier `--gate`.
"""

P = "project-trajectory/scripts/"
R = "docs/requirements/low-level-requirements.toml"

EDITS = [
    # --- the readers' tables -------------------------------------------------
    (
        (P + "kitlib/registry.py", P + "wi_convert.py", P + "plan_artifacts.py"),
        '    "Bar",\n',
        '    "ChecksStage",\n',
    ),
    (
        P + "kitlib/registry.py",
        "    # WI-388: bar declares verification strictness for this row's lane; it\n"
        "    # never affects scheduling. (DevStg-Reqs|DevStg-Tests|DevStg-Impl — integrate.refresh passes it to\n"
        "    # check.py --gate; load_wis deliberately does not parse it.)\n"
        '    ("Bar", "bar"),\n',
        "    # WI-388: checks_stage pins the stage this row's landing checks run at;\n"
        "    # it never affects scheduling. (DevStg-Reqs|DevStg-Tests|DevStg-Impl —\n"
        "    # integrate.refresh passes it to check.py --stage; load_wis deliberately\n"
        "    # does not parse it.)\n"
        '    ("ChecksStage", "checks_stage"),\n',
    ),
    (
        P + "wi_convert.py",
        "    # WI-388: bar declares verification strictness for this row's lane; it\n"
        "    # never affects scheduling. (DevStg-Reqs|DevStg-Tests|DevStg-Impl — integrate.refresh passes it to\n"
        "    # check.py --gate; the scheduler deliberately does not parse it.)\n"
        '    ("Bar", "bar"),\n',
        "    # WI-388: checks_stage pins the stage this row's landing checks run at;\n"
        "    # it never affects scheduling. (DevStg-Reqs|DevStg-Tests|DevStg-Impl —\n"
        "    # integrate.refresh passes it to check.py --stage; the scheduler\n"
        "    # deliberately does not parse it.)\n"
        '    ("ChecksStage", "checks_stage"),\n',
    ),
    (
        "project-trajectory/registries/work-items.template.csv",
        "SafetyClass,PlanMode,Bar,Supersedes",
        "SafetyClass,PlanMode,ChecksStage,Supersedes",
    ),
    # --- intake.py -------------------------------------------------------------
    (
        P + "intake.py",
        "# --- the WI `bar:` vocabulary (OI-21 contract break 3) -------------------------\n"
        "# The bar a work item is held to, in the stage-ladder vocabulary. A WI's `bar:`\n"
        "# frontmatter is a value the AUTHOR writes, so the retired `DevStg-Reqs|DevStg-Tests|DevStg-Impl` tags\n"
        "# translate on read",
        "# --- the WI `checks_stage` vocabulary (OI-21 contract break 3) ------------------\n"
        "# The stage a work item pins its landing checks to, a rung of the stage ladder.\n"
        "# A WI's `checks_stage` is a value the AUTHOR writes, so the retired tags\n"
        "# (`_RETIRED_WI_BARS`, named for the retired bar axis) translate on read",
    ),
    (
        P + "intake.py",
        '    """A `bar:` cell as a canonical `DevStg-*` name ("" when blank).',
        '    """A `checks_stage` cell as a canonical `DevStg-*` name ("" when blank).',
    ),
    (P + "intake.py", '        "bar",\n', '        "checks_stage",\n'),
    (
        P + "intake.py",
        '    stage = normalize_checks_stage(data.get("bar"))\n'
        "    if stage and stage not in WI_CHECKS_STAGES:\n"
        '        return "{} declares bar = {!r} ({}) - nothing minted".format(\n'
        '            at, data.get("bar"), "|".join(WI_CHECKS_STAGES)',
        '    stage = normalize_checks_stage(data.get("checks_stage"))\n'
        "    if stage and stage not in WI_CHECKS_STAGES:\n"
        '        return "{} declares checks_stage = {!r} ({}) - nothing minted".format(\n'
        '            at, data.get("checks_stage"), "|".join(WI_CHECKS_STAGES)',
    ),
    (
        P + "intake.py",
        '    row["Bar"] = normalize_checks_stage(draft.get("bar"))',
        '    row["ChecksStage"] = normalize_checks_stage(draft.get("checks_stage"))',
    ),
    # --- integrate.py ----------------------------------------------------------
    (
        P + "integrate.py",
        "    `gate` (WI-388, the `bar` frontmatter key) pins check.py's --gate: a row\n"
        "    claimed to deliver evidence at a level still bars at that level if\n"
        "    docs/gate moves mid-flight. None keeps check.py on its own derived-gate\n"
        "    read, exactly as before.",
        "    `stage` (WI-388, the `checks_stage` frontmatter key) pins check.py's\n"
        "    --stage: a row claimed to deliver evidence at a stage is still checked\n"
        "    at that stage if the derived stage moves mid-flight. None keeps\n"
        "    check.py on its own derived-stage read, exactly as before.",
    ),
    (
        P + "integrate.py",
        "# The `bar` frontmatter key's vocabulary (WI-388; the stage-ladder names since\n"
        "# OI-21): bar declares verification strictness for this row's lane; it never\n"
        "# affects scheduling.",
        "# The `checks_stage` frontmatter key's vocabulary (WI-388; the stage-ladder\n"
        "# names since OI-21): it pins the stage this row's landing checks run at; it\n"
        "# never affects scheduling.",
    ),
    (
        P + "integrate.py",
        "# A WI `bar:` is AUTHOR-WRITTEN, so the retired tags translate on read (OI-21",
        "# A WI `checks_stage` is AUTHOR-WRITTEN, so the retired tags translate on read (OI-21",
    ),
    (
        P + "integrate.py",
        '    """A `bar:` cell as a canonical `DevStg-*` name ("" when blank), retired tags',
        '    """A `checks_stage` cell as a canonical `DevStg-*` name ("" when blank), retired tags',
    ),
    (
        P + "integrate.py",
        '    """The claimed row\'s say over the refresh bar (WI-388): `(skip, gate,\n'
        "    refusal)`.",
        '    """The claimed row\'s say over the refresh bar (WI-388): `(skip, stage,\n'
        "    refusal)`.",
    ),
    (
        P + "integrate.py",
        "    * `gate` — that row's `bar` key (one of DevStg-Reqs, DevStg-Tests,\n"
        "      DevStg-Impl), handed to check.py --gate. None when it declares none.\n"
        "    * `refusal` — a malformed bar value. Refused loudly rather than silently\n"
        "      barred at whatever the derived gate happens to read (the drift the key\n"
        "      exists to pin);",
        "    * `stage` — that row's `checks_stage` key (one of DevStg-Reqs,\n"
        "      DevStg-Tests, DevStg-Impl), handed to check.py --stage. None when it\n"
        "      declares none.\n"
        "    * `refusal` — a malformed `checks_stage`. Refused loudly rather than\n"
        "      silently checked at whatever the derived stage happens to read (the\n"
        "      drift the key exists to pin);",
    ),
    (
        P + "integrate.py",
        '        declared = _normalize_checks_stage(meta.get("bar"))',
        '        declared = _normalize_checks_stage(meta.get("checks_stage"))',
    ),
    (
        P + "integrate.py",
        '                "{} declares bar = {!r} ({}), which is not one of {} - the bar "\n'
        "                \"key declares verification strictness for this row's lane (it \"\n",
        '                "{} declares checks_stage = {!r} ({}), which is not one of {} - "\n'
        "                \"the key pins the stage this row's landing checks run at (it \"\n",
    ),
    (
        P + "integrate.py",
        '                    branch, str(meta.get("bar")), name, "|".join(_CHECKS_STAGES)',
        '                    branch, str(meta.get("checks_stage")), name, "|".join(_CHECKS_STAGES)',
    ),
    (
        P + "integrate.py",
        "    # claimed rows' say over the bar (WI-388): the adjudication no-bar arm\n"
        "    # and the `bar` strictness pin, both read before anything runs so a\n"
        "    # malformed key refuses with the lane untouched.",
        "    # claimed rows' say over the bar (WI-388): the adjudication no-bar arm\n"
        "    # and the `checks_stage` pin, both read before anything runs so a\n"
        "    # malformed key refuses with the lane untouched.",
    ),
    # --- tests -------------------------------------------------------------------
    (
        ("tests/integrate_fixtures.py", "tests/test_dispatch.py"),
        "        lines.append('bar = \"{}\"'.format(checks_stage))",
        "        lines.append('checks_stage = \"{}\"'.format(checks_stage))",
    ),
    (
        "tests/test_plan_artifacts.py",
        '"EstTokens,SafetyClass,PlanMode,Bar,Supersedes,',
        '"EstTokens,SafetyClass,PlanMode,ChecksStage,Supersedes,',
    ),
    (
        "tests/test_wi_convert.py",
        '    """WI-388: the `Bar` column (bar declares verification strictness for this\n'
        "    row's lane; it never affects scheduling) crosses the round trip like any\n",
        '    """WI-388: the `ChecksStage` column (the stage this row\'s landing checks\n'
        "    run at; it never affects scheduling) crosses the round trip like any\n",
    ),
    (
        "tests/test_wi_convert.py",
        '    rows = [_row("WI-001", Status="queued", Bar="DevStg-Tests")]\n'
        "    back = _round_trip(tmp_path, rows)\n"
        '    assert back[0]["Bar"] == "DevStg-Tests"',
        '    rows = [_row("WI-001", Status="queued", ChecksStage="DevStg-Tests")]\n'
        "    back = _round_trip(tmp_path, rows)\n"
        '    assert back[0]["ChecksStage"] == "DevStg-Tests"',
    ),
    ("tests/test_wi_loader_sync.py", '        "Bar": "",\n', '        "ChecksStage": "",\n', 5),
    (
        "tests/test_wi_loader_sync.py",
        "        # The WI-388 strictness key, carried where the cells most likely to be\n"
        "        # lost in translation live: bar declares verification strictness for\n"
        "        # this row's lane; it never affects scheduling.\n"
        '        "Bar": "DevStg-Tests",\n',
        "        # The WI-388 checks-stage key, carried where the cells most likely to\n"
        "        # be lost in translation live: it pins the stage this row's landing\n"
        "        # checks run at; it never affects scheduling.\n"
        '        "ChecksStage": "DevStg-Tests",\n',
    ),
    (
        "tests/test_wi_loader_sync.py",
        "        # in translation\" row as `Bar`:",
        "        # in translation\" row as `ChecksStage`:",
    ),
    (
        "tests/test_wi_loader_sync.py",
        '    """The WI-388 `bar` column crosses both representations and all three F5\n'
        "    readers together (the loader tables gain the column as one edit): bar\n"
        "    declares verification strictness for this row's lane; it never affects\n"
        "    scheduling",
        '    """The WI-388 `ChecksStage` column crosses both representations and all\n'
        "    three F5 readers together (the loader tables gain the column as one\n"
        "    edit): it pins the stage this row's landing checks run at; it never\n"
        "    affects scheduling",
    ),
    (
        "tests/test_wi_loader_sync.py",
        '        assert by_id["WI-002"]["Bar"] == "DevStg-Tests"\n'
        '        assert by_id["WI-001"]["Bar"] == ""\n'
        "    # Never a scheduling input: the WI dicts the frontier is computed from\n"
        "    # carry no bar key at all — structurally, not by convention.\n"
        "    for wi in sched.load_wis(sched.read_spec_rows(work_dir)):\n"
        '        assert "bar" not in wi',
        '        assert by_id["WI-002"]["ChecksStage"] == "DevStg-Tests"\n'
        '        assert by_id["WI-001"]["ChecksStage"] == ""\n'
        "    # Never a scheduling input: the WI dicts the frontier is computed from\n"
        "    # carry no checks_stage key at all — structurally, not by convention.\n"
        "    for wi in sched.load_wis(sched.read_spec_rows(work_dir)):\n"
        '        assert "checks_stage" not in wi',
    ),
    (
        "tests/test_wi_loader_sync.py",
        "    readers together — the twin of the `bar` guard above, and for the same",
        "    readers together — the twin of the `checks_stage` guard above, and for the same",
    ),
    (
        "tests/test_wi_loader_sync.py",
        "    Like `bar` it is NOT a scheduling input",
        "    Like `checks_stage` it is NOT a scheduling input",
    ),
    (
        "tests/test_wi_loader_sync.py",
        "    Not a scheduling input either, for the `bar`/`brief` reason:",
        "    Not a scheduling input either, for the `checks_stage`/`brief` reason:",
    ),
    (
        "tests/test_integrate_station.py",
        "    shapes the claimed spec (the WI-388 bar/no-bar tests declare `bar=` or",
        "    shapes the claimed spec (the WI-388 bar/no-bar tests declare `checks_stage=` or",
    ),
    (
        "tests/test_integrate_station.py",
        "# 5b.2-wi388 — the adjudication no-bar arm and the `bar` strictness key",
        "# 5b.2-wi388 — the adjudication no-bar arm and the `checks_stage` key",
    ),
    (
        "tests/test_integrate_station.py",
        "    # WI-388 (5): an optional frontmatter `bar = DevStg-Reqs|DevStg-Tests|DevStg-Impl`\n"
        "    # pins the lane's verification strictness — the refresh passes it to check.py\n"
        "    # as --stage (WI-498 slice 2 re-keyed the flag; the three VALUES are ladder\n"
        "    # rungs and are unchanged), so a row claimed to deliver evidence at a level\n"
        "    # still bars at that level if the derived value moves mid-flight.",
        "    # WI-388 (5): an optional frontmatter `checks_stage = DevStg-Reqs|DevStg-Tests|\n"
        "    # DevStg-Impl` pins the stage the lane's landing checks run at — the refresh\n"
        "    # passes it to check.py as --stage (WI-498 slice 2 re-keyed the flag; the\n"
        "    # three VALUES are ladder rungs and are unchanged), so a row claimed to\n"
        "    # deliver evidence at a stage is still checked at that stage if the derived\n"
        "    # value moves mid-flight.",
    ),
    (
        "tests/test_integrate_station.py",
        "    # The complement, so the key cannot be mistaken for a default: an undeclared\n"
        "    # bar leaves check.py on its own derived-stage read, exactly as before.",
        "    # The complement, so the key cannot be mistaken for a default: an undeclared\n"
        "    # checks_stage leaves check.py on its own derived-stage read, exactly as before.",
    ),
    (
        "tests/test_integrate_station.py",
        "    # Fail closed and loud: a typo'd bar silently ignored would bar at whatever\n"
        "    # docs/gate happens to read — the exact drift the key exists to pin.",
        "    # Fail closed and loud: a typo'd checks_stage silently ignored would check\n"
        "    # at whatever stage the repository derives — the exact drift the key exists\n"
        "    # to pin.",
    ),
    (
        "tests/test_integrate_station.py",
        '    assert "bar" in refusal and "G9" in refusal',
        '    assert "checks_stage" in refusal and "G9" in refusal',
    ),
    (
        "tests/test_dispatch.py",
        "    # THE WI PINS ITS OWN `bar:` SINCE THE OI-30 D2 CEILING,",
        "    # THE WI PINS ITS OWN `checks_stage` SINCE THE OI-30 D2 CEILING,",
    ),
    (
        "tests/test_dispatch.py",
        "    # sail through a green bar. The `bar:` frontmatter key (WI-388) is exactly",
        "    # sail through a green bar. The `checks_stage` frontmatter key (WI-388) is exactly",
    ),
    (
        "tests/test_stage_ladder.py",
        '    """The WI `bar:` key is read by two modules, each with its own copy of the',
        '    """The WI `checks_stage` key is read by two modules, each with its own copy of the',
    ),
    (
        "tests/test_stage_ladder.py",
        "    The KEY is still spelled `bar:`, and that is the last adopter-authored\n"
        "    surface carrying the retired word. Renaming it is a migration entry of its\n"
        "    own and is deliberately NOT folded in here (no WI spec in this repo sets it,\n"
        '    so nothing is wrong today — only old-flavoured)."""',
        "    The KEY was spelled `bar:` until the vocabulary migration of 2026-11, the\n"
        "    last adopter-authored surface carrying the retired word; it is\n"
        '    `checks_stage` now, and `migrate_vocabulary.py` rewrites the earlier key."""',
    ),
    # --- rows ----------------------------------------------------------------------
    (
        R,
        "The optional `bar = DevStg-Reqs|DevStg-Tests|DevStg-Impl` frontmatter key rides the "
        "same directive read: bar declares verification strictness for this row's lane; it "
        "never affects scheduling (load_wis deliberately does not parse it) - the refresh "
        "passes that one row's declared value to check.py --gate and refuses a malformed one "
        "loudly.",
        "The optional `checks_stage = DevStg-Reqs|DevStg-Tests|DevStg-Impl` frontmatter key "
        "rides the same directive read: it pins the stage this row's landing checks run at; "
        "it never affects scheduling (load_wis deliberately does not parse it) - the refresh "
        "passes that one row's declared value to check.py --stage and refuses a malformed one "
        "loudly.",
    ),
    (
        R,
        'title = "The adjudication kind: rank-1 slot + no-bar arm + the bar strictness key"',
        'title = "The adjudication kind: rank-1 slot + no-bar arm + the checks-stage key"',
    ),
    (
        R,
        "carry the adjudication no-bar arm and the bar strictness pin to _run_bar's --gate.",
        "carry the adjudication no-bar arm and the checks-stage pin to _run_bar's --stage.",
    ),
    (
        "docs/specs/WI-1001.md",
        "A row's `bar` key pins",
        "A row's `checks_stage` key pins",
    ),
]
