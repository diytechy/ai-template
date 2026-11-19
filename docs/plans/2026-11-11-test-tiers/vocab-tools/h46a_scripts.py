"""HANDOFF 10.6, hand edits in the kit scripts, against the text after r46a and n46a.

The passed-checks record's sentences, the CLI parser, the messages, the
failed-checks record (4.5.1), and the Review-Verdict trailer, which the code
also called an "attestation" and which is a trailer (the code's own word for
it) everywhere else.
"""

P = "project-trajectory/scripts/"
V = P + "kitlib/verdict.py"
I = P + "integrate.py"
L = P + "agent_loop.py"
M = P + "kitlib/red_mark.py"

EDITS = [
    # ---------------------------------------------------------------- verdict.py
    (V, "which is why the\nempty attestation carrier `commit_telemetry` writes",
        "which is why the\nempty trailer carrier `commit_telemetry` writes"),
    (V, "    `branch_trailers` the verified attestations on\n",
        "    `branch_trailers` the verified trailers on\n"),
    (V, "`read_passed_checks` / `passed_checks` / `tests_digest` the bar\n"
        "    attestation grammar, its verifier and the one tests digest; and\n"
        "    `commit_passed_checks` the review walk: a verified `review` record whose",
        "`read_passed_checks` / `passed_checks` / `tests_digest` the passed-checks\n"
        "    record's grammar, its verifier and the one tests digest; and\n"
        "    `commit_passed_checks` the review walk: a verified `commit` record whose"),
    (V, "first verified record deciding, so another bar or another digest refuses",
        "first verified record deciding, so another set or another digest refuses"),
    (V, "    the red record a build's session log header carries, keyed by the build",
        "    the failed-checks record a build's session log header carries, keyed by the build"),
    (V, "one, and `failed_rounds` the count: the distinct red builds since the last",
        "one, and `failed_rounds` the count: the distinct failed builds since the last"),
    (V, "    read as its own attestation, and the kit's convention",
        "    read as its own trailer, and the kit's convention"),
    (V, "# The `Checks-Passed:` attestation, VERIFIED against git. The label comes from\n"
        "# `station` so the writer (`format_passed_checks`) and this verifier share one\n"
        "# spelling rather than two literals that must agree. The bar set is closed:\n"
        "# `review` is a build round's record of green, `landing` and `none` are the\n"
        "# station refresh's (the adjudication arm runs no bar and says so).\n",
        "# The passed-checks record, `Checks-Passed:`, VERIFIED against git. The label\n"
        "# comes from `station` so the writer (`format_passed_checks`) and this\n"
        "# verifier share one spelling rather than two literals that must agree. The\n"
        "# set of checks is closed: `commit` is a build round's record that its commit\n"
        "# checks passed, `landing` and `none` are the station refresh's (the\n"
        "# adjudication arm runs no checks and says so).\n"),
    (V, "    The bar is attested to a TREE, and this is where that sentence is made",
        "    The checks are recorded against a TREE, and this is where that sentence is made"),
    (V, "    So the trailer NAMES what it attests, and `passed_checks` verifies it",
        "    So the trailer NAMES what it records, and `passed_checks` verifies it"),
    (V, "    It raises on a bar outside `CHECK_SETS`, so the writer cannot emit a line",
        "    It raises on a set of checks outside `CHECK_SETS`, so the writer cannot emit a line"),
    (V, '"unknown bar {!r}; the set is {}"', '"unknown checks {!r}; the set is {}"'),
    (V, "    \"\"\"`(PassedChecks, None)` for `rev`'s verified `Checks-Passed:` attestation,\n",
        "    \"\"\"`(PassedChecks, None)` for `rev`'s verified `Checks-Passed:` record,\n"),
    (V, "    An attestation is the message's ONE line starting with the label at column\n"
        "    0 (a quoted or indented line is a quotation, two lines attest no single\n"
        "    bar), matching the grammar in full, naming a bar in `CHECK_SETS`, and whose",
        "    A record is the message's ONE line starting with the label at column\n"
        "    0 (a quoted or indented line is a quotation, two lines record no single\n"
        "    set), matching the grammar in full, naming a set in `CHECK_SETS`, and whose"),
    (V, "    \"\"\"The verified fields of `rev`'s `Checks-Passed:` attestation as a\n",
        "    \"\"\"The verified fields of `rev`'s `Checks-Passed:` record as a\n"),
    (V, "    a `Review-Verdict:` attestation must land even when the bookkeeping it rides",
        "    a `Review-Verdict:` trailer must land even when the bookkeeping it rides"),
    (V, "    \"\"\"`(attested sha, None)` when `rev`, or a commit beneath it that only\n"
        "    record-only commits separate from it, carries a verified `review`\n"
        "    attestation whose tests digest is `tests_digest(tests)`; else `(None,",
        "    \"\"\"`(recorded sha, None)` when `rev`, or a commit beneath it that only\n"
        "    record-only commits separate from it, carries a verified `commit`\n"
        "    record whose tests digest is `tests_digest(tests)`; else `(None,"),
    (V, "    commit above an attested commit needs no new bar. The first verified record\n"
        "    it meets decides: another bar, a refresh's `landing` included, is refused",
        "    commit above a recorded commit needs no new bar. The first verified record\n"
        "    it meets decides: another set, a refresh's `landing` included, is refused"),
    (V, '"{} has no verified attestation ({}), and it changes non-record "',
        '"{} has no verified passed-checks record ({}), and it changes non-record "'),
    (V, '"no verified attestation within {} record-only commits"',
        '"no verified passed-checks record within {} record-only commits"'),
    (V, '"{} carries a verified `{}` attestation, not a `review` one"',
        '"{} carries a verified `checks={}` record, not a `checks=commit` one"'),
    (V, "\"{}'s review attestation is for tests={}, but the round's tests \"",
        "\"{}'s commit record is for tests={}, but the round's tests \""),
    (V, "    `branch_trailers` for the commit an attestation rides.",
        "    `branch_trailers` for the commit a trailer rides."),
    (V, "# --- the red record: the commit checks that refused a build, and the count -----------\n"
        "\n"
        "# A red result is written into a session log's header, keyed by the build\n"
        "# commit whose tip the bar refused:",
        "# --- the failed-checks record: the commit checks that refused a build, and the count ---\n"
        "\n"
        "# A failed run of the commit checks is written into a session log's header,\n"
        "# keyed by the build commit whose tip they refused:"),
    (V, "the header fields of a red\n    record.",
        "the header fields of a\n    failed-checks record."),
    (V, '"a red record names a 40-hex build sha, not {!r}"',
        '"a failed-checks record names a 40-hex build sha, not {!r}"'),
    (V, "for a session log's red record, else None.",
        "for a session log's failed-checks record, else None."),
    (V, "    \"\"\"The lane's consecutive red review-bar rounds and the last bar summary.\"\"\"",
        "    \"\"\"The lane's consecutive failed commit-check rounds and the last summary.\"\"\""),
    (V, "    \"\"\"The consecutive red review-bar rounds `base..branch` records, as a\n",
        "    \"\"\"The consecutive failed commit-check rounds `base..branch` records, as a\n"),
    (V, "    the last green, and it resets the count.",
        "    the last pass, and it resets the count."),
    (V, "and each red record whose build sha is not\n    an ancestor of that green counts. DISTINCT shas give the count, so a red\n",
        "and each failed-checks record whose build sha is\n    not an ancestor of that pass counts. DISTINCT shas give the count, so a failure\n"),
    (V, "A log git cannot show counts as one red keyed by\n    its path (unless the commit that added it is beneath the green):",
        "A log git cannot show counts as one failure keyed\n    by its path (unless the commit that added it is beneath the pass):"),
    (V, "    \"\"\"The summary of the red record `base..branch`'s session logs hold for the",
        "    \"\"\"The summary of the failed-checks record `base..branch`'s session logs hold for the"),
    (V, "for the red one session log records, read at\n    the commit `added` that added it, else None. A readable log keys its red\n    by the build sha and is dated by it; a log git cannot show keys one red by",
        "for the failure one session log records, read\n    at the commit `added` that added it, else None. A readable log keys its\n    failure by the build sha and is dated by it; a log git cannot show keys one failure by"),
    (V, "carrying a verified `review`\n    attestation, \"\" when none does,",
        "carrying a verified `commit`\n    record, \"\" when none does,"),
    (V, "    \"\"\"The lane's last review record in `base..branch`:",
        "    \"\"\"The lane's last commit record in `base..branch`:"),
    (V, "branch's RAW tree instead filed the attestation under a key",
        "branch's RAW tree instead filed the trailer under a key"),
    (V, "    newest attestation for that tree.\n\n    A SEQUENCE, not one attestation per tree, and the type is the fix. One tree\n    carries more than one attestation whenever",
        "    newest trailer for that tree.\n\n    A SEQUENCE, not one trailer per tree, and the type is the fix. One tree\n    carries more than one trailer whenever"),
    (V, "the evidence and the attestation\n    as disagreeing",
        "the evidence and the trailer\n    as disagreeing"),
    (V, "would reject every honest attestation on", "would reject every honest trailer on"),
    (V, "    # is the order a reader means by \"the latest attestation\".",
        "    # is the order a reader means by \"the latest trailer\"."),
    # -------------------------------------------------------------- integrate.py
    (I, "VERIFIES the `Checks-Passed:` attestation\n", "VERIFIES the `Checks-Passed:` record\n"),
    (I, "  attest     a build round's own record of green (WI-956): in the lane\n",
        "  record-checks\n             a build round's own passed-checks record (WI-956): in the lane\n"),
    (I, "against the lane's last review\n             record (`kitlib.red_mark`, WI-996)",
        "against the lane's last commit\n             record (`kitlib.red_mark`, WI-996)"),
    (I, "             through the one producer the refresh commits through. A\n             `review` attestation is never peeled",
        "             through the one producer the refresh commits through. A\n             `commit` record is never peeled"),
    (I, "Phase 4 inventory). The bar is attested to a TREE, and the attestation NAMES\nthat tree:",
        "Phase 4 inventory). The checks are recorded against a TREE, and the record NAMES\nthat tree:"),
    (I, "    last review record over the same set naming it, and committing nothing on",
        "    last commit record over the same set naming it, and committing nothing on"),
    (I, "# The refresh commit's attestation, its subject grammar",
        "# The refresh commit's passed-checks record, its subject grammar"),
    (I, "reroll-until-green, a\n    contradicted attestation) are all", "reroll-until-green, a\n    contradicted trailer) are all"),
    (I, "is a forged or mis-stamped\n    # attestation, and a merge slot", "is a forged or mis-stamped\n    # trailer, and a merge slot"),
    (I, "    # THE NEWEST attestation at this tree,", "    # THE NEWEST trailer at this tree,"),
    (I, "tree can leave the newest attestation reading rounds=N-1",
        "tree can leave the newest trailer reading rounds=N-1"),
    (I, "(REVIEW-A round 033). An\n    # attestation cannot UNDERSTATE",
        "(REVIEW-A round 033). A\n    # trailer cannot UNDERSTATE"),
    (I, '"while the round files say APPROVE rounds={} - the attestation "',
        '"while the round files say APPROVE rounds={} - the trailer "'),
    (I, "into itself and attest a composition that never happened, and an attest\n    would move",
        "into itself and record checks for a composition that never happened, and\n    `record-checks` would move"),
    (I, "    # the attested commit by an `add -A` that ran after it.",
        "    # the recorded commit by an `add -A` that ran after it."),
    (I, '"the refresh commit does not verify as a refresh attestation; "\n            "nothing is attested and the branch is restored",',
        '"the refresh commit does not verify as a refresh\'s passed-checks "\n            "record; nothing is recorded and the branch is restored",'),
    (I, '"trailer NAMES what it attests - the tree the bar saw,',
        '"trailer NAMES what it records - the tree the bar saw,'),
    (I, "    the refresh commit still attests THIS tree", "    the refresh commit still records THIS tree"),
    (I, 'return True, "", "no-bar (adjudication, §A5.2)"',
        'return True, "", "no checks run (adjudication, §A5.2)"'),
    (I, "    \"\"\"The one producer of a `Checks-Passed:` attestation: `(sha, None)`, or\n"
        "    `(None, (reason, output))` with nothing committed. `refresh` calls it for\n"
        "    `landing` / `none` and `record-checks` for `review`",
        "    \"\"\"The one producer of a `Checks-Passed:` record: `(sha, None)`, or\n"
        "    `(None, (reason, output))` with nothing committed. `refresh` calls it for\n"
        "    `landing` / `none` and `record-checks` for `commit`"),
    (I, "The commit then has to verify as that attestation, so a",
        "The commit then has to verify as that record, so a"),
    (I, '("the {} commit was refused by its own floor".format(checks), out)',
        '("the checks={} commit was refused by its own floor".format(checks), out)'),
    (I, '"the {} commit does not verify as its own attestation - the "',
        '"the checks={} commit does not verify as its own record - the "'),
    (I, '"commit hook?); nothing is attested and the branch is "',
        '"commit hook?); nothing is recorded and the branch is "'),
    (I, "    \"\"\"Why the bar's run attests nothing, or None:",
        "    \"\"\"Why the bar's run records nothing, or None:"),
    (I, '("staged", "attest") if checks == "commit"', '("staged", "record-checks") if checks == "commit"'),
    (I, '"longer matches {}: {}) - nothing is attested; the index is set back to "',
        '"longer matches {}: {}) - nothing is recorded; the index is set back to "'),
    (I, "against the lane's last\n    review record over its own base,", "against the lane's last\n    commit record over its own base,"),
    (I, "\"the lane's last review record\")", "\"the lane's last commit record\")"),
    (I, "    \"\"\"The attest commit's message:", "    \"\"\"The record-checks commit's message:"),
    (I, '"attestation line".format(CHECKS_PASSED)', '"record line".format(CHECKS_PASSED)'),
    (I, '"attest writes only the commit checks\' record, `review` "',
        '"record-checks writes only the commit checks\' record, `commit` "'),
    (I, '"attest REFUSED for {} - {}"', '"record-checks REFUSED for {} - {}"', 2),
    (I, '"attest REFUSED for {} - {}:\\n{}"', '"record-checks REFUSED for {} - {}:\\n{}"'),
    (I, 'print("integrate: attested {} - commit checks @ {}".format(branch, sha[:10]))',
        'print("integrate: recorded the commit checks for {} @ {}".format(branch, sha[:10]))'),
    (I, "    carries the bar's attestation FOR THAT TIP.", "    carries the passed-checks record FOR THAT TIP."),
    (I, '"its tip carries a verified `{}` {} attestation; the merge slot "\n'
        '                "requires `landing` or `none`".format(found.checks, CHECKS_PASSED)',
        '"its tip carries a verified {} record for checks={}; the merge "\n'
        '                "slot requires `landing` or `none`".format(CHECKS_PASSED, found.checks)'),
    (I, '    p_att = sub.add_parser(\n'
        '        "attest", help="commit the staged work carrying a commit-checks record"\n'
        '    )\n'
        '    p_att.add_argument("--branch", required=True)\n'
        '    p_att.add_argument("--bar", required=True, choices=["review"])\n'
        '    p_att.add_argument("--message-file")\n',
        '    p_rec = sub.add_parser(\n'
        '        "record-checks",\n'
        '        help="commit the staged work carrying a passed-checks record of its commit checks",\n'
        '    )\n'
        '    p_rec.add_argument("--branch", required=True)\n'
        '    p_rec.add_argument("--checks", required=True, choices=["commit"])\n'
        '    p_rec.add_argument("--message-file")\n'),
    (I, '    if args.op == "attest":\n', '    if args.op == "record-checks":\n'),
    # -------------------------------------------------------------- agent_loop.py
    (L, "    # A round that derives NO attestation is SAID SO, once,",
        "    # A round that derives NO trailer is SAID SO, once,"),
    (L, '"review round: no Review-Verdict attestation derived"',
        '"review round: no Review-Verdict trailer derived"'),
    (L, '    if plan.get("bar_red"):\n        ctx.worker["rework"] = plan["bar_red"]',
        '    if plan.get("checks_failed"):\n        ctx.worker["rework"] = plan["checks_failed"]'),
    (L, 'schedule_review_round(ctx, plan.get("attested") or after)',
        'schedule_review_round(ctx, plan.get("passed") or after)'),
    (L, "Green leaves the attested commit on `plan` for the round's\n"
        "    range; red writes the red record into this session's own log header and",
        "Green leaves the recorded commit on `plan` for the round's\n"
        "    range; red writes the failed-checks record into this session's own log header and"),
    (L, '    plan["attested"], plan["bar_red"] = passed, red',
        '    plan["passed"], plan["checks_failed"] = passed, red'),
    (L, "row's derived set, and its range is pointed at that attested commit.",
        "row's derived set, and its range is pointed at that recorded commit."),
    (L, "    each committed red record.\n", "    each committed failed-checks record.\n"),
    (L, "A red carries the red record keyed by\n    the build commit `build`.",
        "A failure carries the failed-checks record\n    keyed by the build commit `build`."),
    (L, '    meta["outcome"] = "RED" if refusal else "GREEN"',
        '    meta["outcome"] = "FAILED" if refusal else "PASSED"'),
    # -------------------------------------------------------------- red_mark.py
    (M, "command, the other value an attestation needs.", "command, the other value a passed-checks record needs."),
    (M, "and its attestation's green commit checks are that test's",
        "and its record of passing commit checks is that test's"),
    (M, "lane's last review record over the same test set,", "lane's last commit record over the same test set,"),
    (M, '    """What an attestation needs from the lane at `lane`:',
        '    """What a passed-checks record needs from the lane at `lane`:'),
    (M, '"no review record stands for the marked tree"', '"no commit record stands for the marked tree"'),
    (M, "    None. The reference is the newest verified review record in",
        "    None. The reference is the newest verified commit record in"),
    (M, "so the lane's last review record is \"", "so the lane's last commit record is \""),
    (M, "\"the lane's last review record {}\"", "\"the lane's last commit record {}\""),
    (M, "which carries no review record\"", "which carries no commit record\""),
    # -------------------------------------------------------------- others
    (P + "kitlib/station.py", "`CHECKS_PASSED` is the one attestation\n    label the refresh",
        "`CHECKS_PASSED` is the passed-checks\n    record's label the refresh"),
    (P + "kitlib/station.py", "#: The one attestation label the refresh and `record-checks` share,",
        "#: The passed-checks record's label, which the refresh and `record-checks` share,"),
    (P + "kitlib/station.py", "#: the tree and the work commit it attests so both",
        "#: the tree and the work commit it records so both"),
    (P + "kitlib/station.py", "the attestor's recomposition no longer matches",
        "the peel's recomposition no longer matches"),
    (P + "kitlib/__init__.py", "the passed-checks record trailer label,", "the passed-checks record's label,"),
    (P + "agent_common.py", "`trailer` is the round's `Review-Verdict:` ATTESTATION (OI-76 alternative C,\n"
        "    the `Checks-Passed:` pattern), and it changes one rule: an attestation must land",
        "`trailer` is the round's `Review-Verdict:` TRAILER (OI-76 alternative C,\n"
        "    the `Checks-Passed:` pattern), and it changes one rule: a trailer must land"),
    (P + "agent_common.py", "carrying a `Review-Verdict:` attestation on a commit", "carrying a `Review-Verdict:` trailer on a commit"),
    (P + "agent_common.py", "`src.py` into the attestation's carrier, driven.", "`src.py` into the trailer's carrier, driven."),
    (P + "agent_brief.py", "or None when there is nothing to\n    attest (no merged verdict,",
        "or None when there is nothing to\n    record (no merged verdict,"),
    (P + "agent_brief.py", "Stamping the unpeeled value filed the attestation under a key",
        "Stamping the unpeeled value filed the trailer under a key"),
    (P + "agent_brief.py", "    commit attests nothing the round file did not already claim;",
        "    commit records nothing the round file did not already claim;"),
    (P + "dispatch.py", "or a contradicted\n    attestation — and none", "or a contradicted\n    trailer — and none"),
    (P + "dispatch.py", "# A lane's own refresh (or a hand refresh) already attested this\n            # exact tip",
        "# A lane's own refresh (or a hand refresh) already recorded the\n            # landing checks for this exact tip"),
    (P + "dispatch.py", "        # half-attested.\n", "        # half-refreshed.\n"),
    (P + "review_brief.py", "    prints the attested commit and that digest.", "    prints the recorded commit and that digest."),
    (P + "review_brief.py", "a reviewed commit with no such attestation (the refusal\n    names the commit, the cause and the attest command)",
        "a reviewed commit with no such record (the refusal\n    names the commit, the cause and the record-checks command)"),
    (P + "review_brief.py", '"checkout (staging the work it attests, or nothing for an empty attestation "',
        '"checkout (staging the work it records, or nothing for an empty record "'),
    (P + "review_set.py", "never from whoever asks for the\nattestation.", "never from whoever asks for the\nrecord."),
]
