"""HANDOFF 4.5.4, hand edits after the `git mv`s, r47b and n47b.

The settings' cause keys name the fields as strings, so they follow the fields
(`commit_checks`, `marker`). The retired `[bars]` keys `review` and `red_mark`
are spellings of the retired section and stay wherever they name it:
`_moved(profile, "review")`, the fixtures that declare `[bars]`, and the
refusal text. The retired-section test took one parameter for both before;
it takes the field and the retired key apart now.
"""

P = "project-trajectory/scripts/"
EF = P + "kitlib/expected_failure.py"
T = "tests/test_expected_failure.py"

EDITS = [
    # --- the reader --------------------------------------------------------------
    (
        EF,
        "needs from the lane at `lane`: `review`, the shell\n"
        "    line of the check suite a commit must pass; `red_mark`, the declared\n",
        "needs from the lane at `lane`: `commit_checks`, the\n"
        "    shell line of the check suite a commit must pass; `marker`, the declared\n",
    ),
    (EF, 'causes["review"]', 'causes["commit_checks"]', 3),
    (EF, 'causes["red_mark"]', 'causes["marker"]', 2),
    (EF, '"" if "review" in causes else', '"" if "commit_checks" in causes else'),
    (EF, 'settings.refusal("red_mark")', 'settings.refusal("marker")'),
    (
        P + "integrate.py",
        'settings.refusal("review", "red_mark")',
        'settings.refusal("commit_checks", "marker")',
    ),
    (
        P + "kitlib/config.py",
        '    "red_rounds_max",\n',
        '    "commit_check_failure_cap",\n',
    ),
    # --- tests -------------------------------------------------------------------
    (T, 'refusal("review", "red_mark")', 'refusal("commit_checks", "marker")', 5),
    (T, 'NAMED, "red_mark", MARKER_AT', 'NAMED, "marker", MARKER_AT', 6),
    (T, ', "review", NAME_AT', ', "commit_checks", NAME_AT', 8),
    (T, 'NAMED, "review", SUITE_AT', 'NAMED, "commit_checks", SUITE_AT', 6),
    # fixture values: a suite's shell line, not the retired word for checks
    (T, "run the bar", "run the checks", 8),
    (T, '"review = the old bar"', '"review = the old suite"'),
    (
        T,
        '@pytest.mark.parametrize(\n'
        '    "key, policy, at",\n'
        "    [\n"
        '        ("red_mark", None, MARKER_AT + "the section is absent"),\n'
        '        ("review", None, NAME_AT + "the file is absent"),\n'
        '        ("review", NAMED, SUITE_AT + "the section is absent"),\n'
        "    ],\n",
        '@pytest.mark.parametrize(\n'
        '    "field, old, policy, at",\n'
        "    [\n"
        '        ("marker", "red_mark", None, MARKER_AT + "the section is absent"),\n'
        '        ("commit_checks", "review", None, NAME_AT + "the file is absent"),\n'
        '        ("commit_checks", "review", NAMED, SUITE_AT + "the section is absent"),\n'
        "    ],\n",
    ),
    (
        T,
        "def test_a_retired_bars_section_is_never_read_and_is_named(tmp_path, key, policy, at):\n",
        "def test_a_retired_bars_section_is_never_read_and_is_named(\n"
        "    tmp_path, field, old, policy, at\n"
        "):\n",
    ),
    (
        T,
        "    assert settings.causes[key].startswith(at)\n"
        "    assert RETIRED.format(key) in settings.causes[key]\n"
        "    assert RETIRED.format(key) in settings.refusal(key)\n"
        "    # A `[bars]` holding only the other key says nothing about this one.\n"
        '    other = "red_mark" if key == "review" else "review"\n'
        '    _declare(tmp_path, _section("bars", other + " = the old value"))\n'
        '    assert "[bars]" not in kef.read_commit_check_settings(tmp_path).causes[key]\n',
        "    assert settings.causes[field].startswith(at)\n"
        "    assert RETIRED.format(old) in settings.causes[field]\n"
        "    assert RETIRED.format(old) in settings.refusal(field)\n"
        "    # A `[bars]` holding only the other key says nothing about this one.\n"
        '    other = "red_mark" if old == "review" else "review"\n'
        '    _declare(tmp_path, _section("bars", other + " = the old value"))\n'
        '    assert "[bars]" not in kef.read_commit_check_settings(tmp_path).causes[field]\n',
    ),
    (
        "tests/conftest.py",
        "# name is the reader's, `CommitCheckSettings.red_mark`, not the retired `[bars]` section's.",
        "# name is the reader's, `CommitCheckSettings.marker`, not the retired `[bars]` section's.",
    ),
    (
        "tests/test_commit_check_failure_cap.py",
        "module): it is a pure unit of `kitlib.config.red_rounds_max` over a temp file,",
        "module): it is a pure unit of `kitlib.config.commit_check_failure_cap` over a temp file,",
    ),
    # --- rows ----------------------------------------------------------------------
    (
        "docs/requirements/low-level-requirements.toml",
        'code_symbol = "red_rounds_max/_process_toml_at/',
        'code_symbol = "commit_check_failure_cap/_process_toml_at/',
    ),
]
