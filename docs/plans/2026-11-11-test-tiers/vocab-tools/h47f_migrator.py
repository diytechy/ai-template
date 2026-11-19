"""HANDOFF 4.5.3, 10.3 step 9: the brief kind `red-tc` is stored in
`docs/process.toml` `[adjudicator] retain_for`, so the migrator's list step
respells it, as it does `first-approval` (10.5 pass 2). One test, the three
rows (Drafted). Run the migrator's `policy` step here after this.
"""

M = "project-trajectory/scripts/migrate_vocabulary.py"
T = "tests/test_migrate_vocabulary.py"
LLR = "docs/requirements/low-level-requirements.toml"
TC = "docs/test/test-cases.toml"

EDITS = [
    (
        M,
        "                                   in `[adjudicator] retain_for`, the brief\n"
        "                                   kind `\"first-approval\"`  ->\n"
        "                                   `\"first-acceptance\"`\n",
        "                                   in `[adjudicator] retain_for`, the brief\n"
        "                                   kinds `\"first-approval\"`  ->\n"
        "                                   `\"first-acceptance\"` and `\"red-tc\"`  ->\n"
        "                                   `\"evidence-gap\"`\n",
    ),
    (
        M,
        "# retained sittings are named by brief kind, and the sitting that takes a row\n"
        "# into acceptance was the kind `first-approval`.\n",
        "# retained sittings are named by brief kind: the sitting that takes a row\n"
        "# into acceptance was the kind `first-approval`, and the one that judges an\n"
        "# evidence gap (a test case left unaccepted under closed work) `red-tc`.\n",
    ),
    (
        M,
        'POLICY_ITEMS = {"adjudicator": {"retain_for": {"first-approval": "first-acceptance"}}}',
        "POLICY_ITEMS = {\n"
        '    "adjudicator": {\n'
        '        "retain_for": {\n'
        '            "first-approval": "first-acceptance",\n'
        '            "red-tc": "evidence-gap",\n'
        "        }\n"
        "    }\n"
        "}",
    ),
    (
        T,
        "@pytest.mark.parametrize(\n"
        '    "text",\n'
        "    (\n"
        "        'attestation = { human_approval_through = \"DevStg-Reqs\" }\\n',",
        "def test_the_retained_evidence_gap_kind_is_respelled_beside_the_others(tmp_path):\n"
        '    """Implements: TC-427"""\n'
        "    text = (\n"
        "        '[adjudicator]\\n'\n"
        "        'retain_for = [\"disposition\", \"red-tc\", \"first-approval\"]  # red-tc\\n'\n"
        "    )\n"
        '    path = _write(tmp_path, "docs/process.toml", text)\n'
        "    assert _run(tmp_path) == 0\n"
        "    assert path.read_text(encoding=\"utf-8\") == (\n"
        "        '[adjudicator]\\n'\n"
        "        'retain_for = [\"disposition\", \"evidence-gap\", \"first-acceptance\"]'\n"
        "        '  # red-tc\\n'\n"
        "    )\n"
        "\n"
        "\n"
        "@pytest.mark.parametrize(\n"
        '    "text",\n'
        "    (\n"
        "        'attestation = { human_approval_through = \"DevStg-Reqs\" }\\n',",
    ),
    (
        LLR,
        "as the brief kind of the sitting that takes a row into acceptance in [adjudicator] retain_for;",
        "as the brief kinds of the sitting that takes a row into acceptance and of the "
        "sitting that judges an evidence gap in [adjudicator] retain_for;",
    ),
    (
        TC,
        "and one holding it in an inline table;",
        "and one holding it in an inline table; a one-line list retaining the "
        "evidence-gap sitting's kind by its earlier name beside the first sitting's;",
    ),
]
