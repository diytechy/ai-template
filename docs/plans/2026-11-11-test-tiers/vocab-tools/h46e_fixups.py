"""HANDOFF 10.6, last hand edits: what the residue scan after r46a to h46b found,
and two tests that pin the cut (D3): a line in the earlier trailer form is no
passed-checks record, and a log header in the earlier form is no
failed-checks record. They name the earlier spellings on purpose, as
test_migrate_vocabulary does (10.7 item 4: the detector must let them).
"""

V = "project-trajectory/scripts/kitlib/verdict.py"
TC = "docs/test/test-cases.toml"

EDITS = [
    # `bar=` here is the work-item key a station spec declares (4.5.2), not the trailer's field
    ("tests/test_integrate_station.py", "the WI-388 bar/no-bar tests declare `checks=` or",
                                        "the WI-388 bar/no-bar tests declare `bar=` or"),
    (V, "and never satisfies the merge slot. The old line without `checks=` is not\n        read at all.",
        "and never satisfies the merge slot. A line in an earlier grammar is not\n        read at all."),
    (V, "An unreadable\n    commit, or the old grammar without `checks=`, is not one: no legacy path.",
        "An unreadable\n    commit, or a line in an earlier grammar, is not one: no legacy path."),
    ("tests/test_review_brief_git.py",
     '"""Commit the staged work carrying the older `Checks-Passed:` grammar, with no\n    `checks=` field: a line no reader verifies."""',
     '"""Commit the staged work carrying a `Checks-Passed:` line with no\n    `checks=` field: a line no reader verifies."""'),
    ("tests/test_passed_checks.py",
     "    # The old grammar, on a refresh subject, with a true tree and parent: it is\n"
     "    # not read at all (no legacy path), so the refresh verifier refuses it too.",
     "    # A line with no `checks=` field, on a refresh subject, with a true tree\n"
     "    # and parent: it is not read at all, so the refresh verifier refuses it too."),
    ("project-trajectory/scripts/agent_common.py",
     "        # WI-958: a red commit checks' record, keyed by the build commit it\n"
     "        # refused (kitlib.verdict.format_failed_record); empty on every other log.\n",
     "        # WI-958: the failed-checks record, keyed by the build commit the commit\n"
     "        # checks refused (kitlib.verdict.format_failed_record); empty on every\n"
     "        # other log.\n"),
    # ---------------------------------------------------------- the cut, pinned
    ("tests/test_passed_checks.py",
     "    grandparent = _rev(root, honest + \"^1\")\n"
     "    sha, _tree, _parent = _commit_naming(root, lambda t, p: _line(t, grandparent))\n"
     "    assert kv.passed_checks(root, sha) is None\n",
     "    grandparent = _rev(root, honest + \"^1\")\n"
     "    sha, _tree, _parent = _commit_naming(root, lambda t, p: _line(t, grandparent))\n"
     "    assert kv.passed_checks(root, sha) is None\n"
     "\n"
     "\n"
     "def test_a_line_in_the_earlier_trailer_form_is_not_a_passed_checks_record(tmp_path):\n"
     "    \"\"\"Implements: TC-205\"\"\"\n"
     "    # The vocabulary cut (2026-11-16): the record was once written\n"
     "    # `Bar-Green: ... bar=review`. A line in that form, naming its own tree\n"
     "    # and parent on a refresh subject, reads as no record at all: there is no\n"
     "    # reader for the earlier spelling, so a lane whose tip carries one records\n"
     "    # its checks again before a review or a merge.\n"
     "    root = _repo(tmp_path)\n"
     "    assert kv.passed_checks(root, _honest(root)) is not None\n"
     "    sha, _tree, _parent = _commit_naming(\n"
     "        root,\n"
     "        lambda t, p: \"Bar-Green: tree={} work={} bar=review tests=none old\".format(t, p),\n"
     "        subject=_refresh_subject(),\n"
     "    )\n"
     "    passed, cause = kv.read_passed_checks(root, sha)\n"
     "    assert passed is None and \"carries 0 `Checks-Passed:` lines\" in cause, cause\n"
     "    assert kv.refresh_passed_checks(root, BRANCH, sha) is None\n"),
    ("tests/test_agent_loop_review_gate.py",
     "    short = kverdict.format_failed_record(sha, \"bar failed:\\n  one line\")\n"
     "    assert short[\"checks-summary\"] == \"bar failed: one line\"\n",
     "    short = kverdict.format_failed_record(sha, \"bar failed:\\n  one line\")\n"
     "    assert short[\"checks-summary\"] == \"bar failed: one line\"\n"
     "\n"
     "\n"
     "def test_a_header_in_the_earlier_form_is_not_a_failed_checks_record():\n"
     "    \"\"\"Implements: TC-379\"\"\"\n"
     "    # TC-379. The vocabulary cut (2026-11-16): the record was once written\n"
     "    # `# bar-red:` / `# bar-summary:`. A header in that form is no record, so\n"
     "    # a log holding one counts toward nothing and the failure count restarts\n"
     "    # at the cut, as the passed-checks record that would reset it is cut too.\n"
     "    sha = \"b\" * 40\n"
     "    old = \"# bar-red: {}\\n# bar-summary: bar failed\\n# ---\\n\".format(sha)\n"
     "    assert kverdict.parse_failed_record(old) is None\n"
     "    new = old.replace(\"# bar-red:\", \"# checks-failed:\").replace(\"bar-summary\", \"checks-summary\")\n"
     "    assert kverdict.parse_failed_record(new) == (sha, \"bar failed\")\n"),
    (TC, "tests/test_passed_checks.py::test_a_wrong_parent_is_not_a_passed_checks_record;",
         "tests/test_passed_checks.py::test_a_wrong_parent_is_not_a_passed_checks_record; "
         "tests/test_passed_checks.py::test_a_line_in_the_earlier_trailer_form_is_not_a_passed_checks_record;"),
    (TC, 'evidence = "tests/test_agent_loop_review_gate.py::test_an_interrupted_red_is_rechecked_once_at_the_draw_and_counted_once; ',
         'evidence = "tests/test_agent_loop_review_gate.py::test_an_interrupted_red_is_rechecked_once_at_the_draw_and_counted_once; '
         'tests/test_agent_loop_review_gate.py::test_a_header_in_the_earlier_form_is_not_a_failed_checks_record; '),
]
