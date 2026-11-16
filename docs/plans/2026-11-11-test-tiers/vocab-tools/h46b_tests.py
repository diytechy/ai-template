"""HANDOFF 10.6, hand edits in the tests, against the text after r46a, n46a,
r46b and r46c: the assertions on reworded messages, the CLI's new flag and
value, the producer's renamed argument, the record's values, and the comments
the phrase rules could not reach. Two S6 leftovers ("the attested spine",
"the attested baseline": the acceptance) are fixed on the way.
"""

T = "tests/"
GATE = T + "test_agent_loop_review_gate.py"
REC = T + "test_integrate_record_checks.py"
ST = T + "test_integrate_station.py"
PC = T + "test_passed_checks.py"
RB = T + "test_review_brief_git.py"

EDITS = [
    # ---------------------------------------------------------- the loop's gate
    (GATE, '"""The loop\'s review gate and its red-round cap (WI-958).\n\n'
           "A managed worker draws a review only over a tip its declared commit checks\n"
           "recorded as passed.",
           '"""The loop\'s review gate and its commit-check failure cap (WI-958).\n\n'
           "A managed worker draws a review only over a tip whose declared commit checks\n"
           "are recorded as passed."),
    (GATE, "with no attestation and no red\n    record:", "with no passed-checks record and no\n    failed-checks record:"),
    (GATE, "    # `review` attestation commit, and the review round is drawn after it.",
           "    # `commit` record commit, and the review round is drawn after it."),
    (GATE, "carries no\n    # attestation runs the commit checks once at the draw:",
           "carries no\n    # passed-checks record runs the commit checks once at the draw:"),
    (GATE, "    # tail. A verified green attestation resets it.", "    # tail. A verified passed-checks record resets it."),
    (GATE, "left with neither an attestation nor a failed-checks record",
           "left with neither a passed-checks record nor a failed-checks record"),
    (GATE, '"# outcome: RED\\n# checks-failed:', '"# outcome: FAILED\\n# checks-failed:'),
    (GATE, '"outcome": "RED" if red else "COMMITTED",', '"outcome": "FAILED" if red else "COMMITTED",'),
    (GATE, '"-m", "attest\\n\\n" + line)', '"-m", "record-checks\\n\\n" + line)'),
    (GATE, "the newest verified review\n    # attestation resets it,", "the newest verified commit\n    # record resets it,"),
    (GATE, '"attest REFUSED - CAUSE-AT-HEAD:', '"record-checks REFUSED - CAUSE-AT-HEAD:', 2),
    (GATE, '"""The verified attestations on the lane, newest first."""',
           '"""The verified passed-checks records on the lane, newest first."""'),
    (GATE, "so the draw attests again rather than trusting it.", "so the draw records the checks again rather than trusting it."),
    # ---------------------------------------------------------- record-checks
    (REC, '@pytest.mark.parametrize("route", ["attest", "refresh"])',
          '@pytest.mark.parametrize("route", ["record-checks", "refresh"])'),
    (REC, '    if route == "attest":\n', '    if route == "record-checks":\n', 2),
    (REC, 'run = _record_checks if route == "attest" else', 'run = _record_checks if route == "record-checks" else'),
    (REC, "a bar that moves the index is not attested,", "a bar that moves the index records nothing,"),
    (REC, '"record-checks", "--branch", BRANCH, "--bar"]', '"record-checks", "--branch", BRANCH, "--checks"]'),
    (REC, 'proc = run_py(argv + ["review"], cwd=root)', 'proc = run_py(argv + ["commit"], cwd=root)', 2),
    (REC, "    # attested commit, and one that derives another set refuses here.",
          "    # recorded commit, and one that derives another set refuses here."),
    # ---------------------------------------------------------- station
    (ST, "  * **the attestation cannot be forged** — a hand-written bar-green trailer,",
         "  * **the passed-checks record cannot be forged** — a hand-written Checks-Passed trailer,"),
    (ST, '"""Every commit on `branch` carrying the bar-green trailer, tip-first."""',
         '"""Every commit on `branch` carrying the Checks-Passed trailer, tip-first."""'),
    (ST, "# the attestation is still there; trunk moved", "# the record is still there; trunk moved"),
    (ST, '# "Attested to a TREE, not to a run" (§A2):', '# "Recorded against a TREE, not a run" (§A2):'),
    (ST, '"the attested spine + the stub harness"', '"the accepted spine + the stub harness"'),
    (ST, "still commits a\n    # verified Checks-Passed attestation (the slot's contract),",
         "still commits a\n    # verified passed-checks record (the slot's contract),"),
    (ST, 'assert "no-bar" in passed[1]', 'assert "no checks run" in passed[1]'),
    (ST, 'assert ready and "no-bar" in why', 'assert ready and "no checks run" in why'),
    (ST, "    # left it — no refresh commit, no attestation, and therefore",
         "    # left it — no refresh commit, no passed-checks record, and therefore"),
    (ST, "# 5b.5 — the attestation is a BINDING, not a string", "# 5b.5 — the passed-checks record is a BINDING, not a string"),
    (ST, "the branch's own, and attested a composition that never happened.",
         "the branch's own, and recorded checks for a composition that never happened."),
    (ST, "# A real merge of trunk, barred and attested — the ordinary refresh outcome.",
         "# A real merge of trunk, barred and recorded — the ordinary refresh outcome."),
    (ST, "names the bar it ran (`landing`, or `no-bar`\n# on the adjudication arm)",
         "names the checks it ran (`landing`, or `none`\n# on the adjudication arm)"),
    (ST, '"""Wrap `integrate._record_checks_commit`; return the list of bars its calls name,',
         '"""Wrap `integrate._record_checks_commit`; return the list of check sets its calls name,'),
    (ST, '    bars = []\n\n    def spy(*args, **kwargs):\n'
         '        bars.append(inspect.signature(real).bind(*args, **kwargs).arguments["bar"])',
         '    named = []\n\n    def spy(*args, **kwargs):\n'
         '        named.append(inspect.signature(real).bind(*args, **kwargs).arguments["checks"])'),
    (ST, '    monkeypatch.setattr(integ, "_record_checks_commit", spy)\n    return bars\n',
         '    monkeypatch.setattr(integ, "_record_checks_commit", spy)\n    return named\n'),
    (ST, "    # A refresh that ran the declared bar attests the `landing` bar, with no",
         "    # A refresh that ran the declared bar records `checks=landing`, with no"),
    (ST, "    # The adjudication arm runs no bar (§A5.2), and its attestation says so in\n"
         "    # the bar field rather than only in the free-text summary.",
         "    # The adjudication arm runs no bar (§A5.2), and its record says so in\n"
         "    # the `checks=` field rather than only in the free-text summary."),
    (ST, "    # Both refresh arms reach the one producer and name their bar to it,",
         "    # Both refresh arms reach the one producer and name their checks to it,"),
    (ST, "    bars = _producer_spy(monkeypatch)\n", "    named = _producer_spy(monkeypatch)\n", 2),
    (ST, '    assert bars == ["landing", "no-bar"]', '    assert named == ["landing", "none"]'),
    (ST, "    # The two routes that write an attestation share one producer: `record-checks`\n"
         "    # names `review` to it,",
         "    # The two routes that write a passed-checks record share one producer:\n"
         "    # `record-checks` names `commit` to it,"),
    (ST, '    assert bars == ["review", "landing"]', '    assert named == ["commit", "landing"]'),
    # ---------------------------------------------------------- the record's own tests
    (PC, "and it is an attestation only when it is the message's one column-0 label line,",
         "and it is a passed-checks record only when it is the message's one column-0 label line,"),
    (PC, '@pytest.mark.parametrize("bar", ["commit", "landing", "none"])',
         '@pytest.mark.parametrize("checks", ["commit", "landing", "none"])'),
    (PC, '@pytest.mark.parametrize("bar", ["landing", "none"])', '@pytest.mark.parametrize("checks", ["landing", "none"])'),
    (PC, "    # attestation, not one: the label counts only as the line's first bytes.",
         "    # record, not one: the label counts only as the line's first bytes."),
    (PC, "    # Two true lines naming two bars: the message attests no single bar, so it\n    # attests none.",
         "    # Two true lines naming two sets: the message records no single set, so it\n    # records none."),
    # ---------------------------------------------------------- review render
    (RB, "that attestation, written by the kit's own `Checks-Passed:` writer,",
         "that record, written by the kit's own `Checks-Passed:` writer,"),
    (RB, 'assert "has no verified attestation" in err, err', 'assert "has no verified passed-checks record" in err, err'),
    (RB, "the record still naming the parent it was attested over.", "the record still naming the parent it was recorded over."),
    (RB, '_passed_checks_tip(root, "attested over the tip")', '_passed_checks_tip(root, "recorded over the tip")'),
    (RB, 'assert "a verified `landing` attestation, not a `review` one" in err, err',
         'assert "a verified `checks=landing` record, not a `checks=commit` one" in err, err'),
    (RB, "    # one that never reads the record names no attested commit.", "    # one that never reads the record names no recorded commit."),
    (RB, 'assert "no verified attestation within 64 record-only commits" in err, err',
         'assert "no verified passed-checks record within 64 record-only commits" in err, err'),
    # ---------------------------------------------------------- others
    (T + "test_hooks_on_routes.py", "    # with the hooks on this record-checks run runs its bar",
                                    "    # with the hooks on this record-checks call runs its bar"),
    (T + "test_hooks_on_census.py", '(SCRIPTS / "integrate.py", "attest", "root", ()),',
                                    '(SCRIPTS / "integrate.py", "record_checks", "root", ()),'),
    (T + "integrate_fixtures.py", "the station protocol — refresh, attestation,", "the station protocol — refresh, passed-checks record,"),
    (T + "test_dispatch.py", "# The attestation constant has ONE home;", "# The trailer's label has ONE home;"),
    (T + "test_dispatch.py", "    # attestation for exactly that tree.", "    # record for exactly that tree."),
    (T + "test_dispatch.py", "    # attestation, so the slot could not merge it even if something tried.",
                             "    # record, so the slot could not merge it even if something tried."),
    (T + "test_handback.py", "    # writer and the attestor share one composer", "    # writer and the peel share one composer"),
    (T + "test_check_smoke_budget.py", "the ones an\n    attestation runs (`review`) are", "the ones\n    `integrate.py record-checks` runs (`review`) are"),
    (T + "test_prompts.py", '"marker `[product] expected_failure_marker` declares, attested before the "',
                            '"marker `[product] expected_failure_marker` declares, recorded before the "'),
    (T + "test_prompts.py", "    # attest route. Adequacy witness:", "    # record-checks route. Adequacy witness:"),
    (T + "test_red_mark.py", "shell line, the other value an attestation needs:", "shell line, the other value a passed-checks record needs:"),
    (T + "test_red_mark.py", 'assert "the marker refuses an attestation and a refresh alike" in contract',
                             'assert "the marker refuses a record-checks run and a refresh alike" in contract'),
    (T + "test_traj_panels.py", "the refresh card carries the shipped attestation", "the refresh card carries the shipped passed-checks record's"),
    (T + "test_integrate_admission.py", '"spine: the attested baseline"', '"spine: the accepted baseline"'),
]
