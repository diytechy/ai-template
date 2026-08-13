"""WI-438 (OI-24) — the moment->tier table has ONE home, and CI is pinned to it.

SN-005's strongest clause is that the enforcement floor is git plus CI running
*the SAME harness a human runs*. That was true and shipped, and pinned by
nothing: the existing workflow tests assert triggers, pinned action digests and
job names, and one asserts that the reference workflow mentions `check.py` **at
all** — none compares CI against a documented local command.

The measurement that made the clause checkable (OI-24, 2026-08-12) is that "the
same harness" cannot mean one command, because the HUMAN bar is itself tiered by
MOMENT — smoke per commit, the full suite at a work-item/slice close, the
release tier at a tag. So the obligation is **per-moment equivalence**: each CI
trigger runs the same ENTRY POINT and the same TIER the documented bar assigns
to the corresponding moment. The reference workflow already did exactly that;
the mapping simply lived in a YAML comment, where nothing could see it drift.

This module is the pin for the kit's standard one-home-plus-pin shape:

  * the table is DECLARED once, in `[ci-tiers]` — shipped in
    ``project-trajectory/stack.ini.template`` (the adopter-owned toolchain home,
    beside the `[tiers]` expressions it names) and instanced in
    ``docs/stack.ini`` with this repo's own, deliberately different values;
  * the SHIPPED reference workflow is held to the shipped declaration — entry
    point, guard, tier and step label;
  * THIS repo's own workflow is held to its own declaration, so a quiet
    downgrade of the meta-repo's CI is a reviewed edit too.

What this does NOT claim, deliberately (OI-24's honest split): it says nothing
about an ADOPTER's edited copy of the workflow, which is outside this repo's
reach, and it proves one definition of PASSING per moment — not that CI and a
local run are equivalent on all inputs, which is not mechanizable at any price.

The parsing is stdlib string work on two small, hand-written, kit-owned YAML
files. A real YAML parser is not stdlib and would be a dependency row for a job
that is four regexes.
"""

import configparser
import re

from conftest import KIT, ROOT, SCRIPTS, load_script

CHECK = load_script("check")

# The entry point the shipped agent guide documents as THE bar. CI matching this
# string is the "one definition of passing" half of the claim.
HARNESS = "scripts/check.py"

# Everything else the reference workflow is allowed to execute. A second script
# appearing here is exactly the drift this module exists to catch: a CI that
# grows its own checks has grown a second, unreviewed definition of passing.
ALLOWED_INVOCATIONS = frozenset(
    {"scripts/check.py", "scripts/gen_release_checklist.py"}
)

# The workflow expression that selects each declared trigger, normalised on
# whitespace. This is a TRANSLATION table (a YAML guard -> the moment's name),
# not a second copy of the moment->tier mapping: the tiers come only from
# `[ci-tiers]`. An unrecognised guard is a FAILURE, never a shrug — a new guard
# must be named here deliberately, which is the reviewed-edit property.
GUARD_TRIGGER = {
    "github.event_name == 'push' && !startsWith(github.ref, 'refs/tags/')": "push",
    "github.event_name == 'pull_request'": "pull_request",
    "startsWith(github.ref, 'refs/tags/')": "tag",
}

CI_REFERENCE = KIT / "ci" / "check.yml"
CI_THIS_REPO = ROOT / ".github" / "workflows" / "test.yml"
STACK_TEMPLATE = KIT / "stack.ini.template"
STACK_LIVE = ROOT / "docs" / "stack.ini"

# Trigger and tier vocabularies for the one-home guard over the YAML comments.
# `all` is absent from the tier side on purpose: it is too common an English
# word to word-match in prose, and it is not a tier the shipped table declares.
_TRIGGER_WORDS = re.compile(r"\b(pushe?s?|pull[ _]requests?|PRs?|tags?)\b")
_TIER_WORDS = re.compile(r"\b(smoke|full|release)\b")


# --- reading the declaration --------------------------------------------------


def declared(path):
    """The `[ci-tiers]` rows of a stack profile as {trigger: (tier, moment)}.

    Read the way check.py reads the same file (interpolation off, BOM-tolerant).
    Each value is `<tier> | <the human moment it mirrors>`; the moment half is
    required, because a row without it declares a trigger->tier table rather
    than the moment->tier table SN-005's claim is about.
    """
    cp = configparser.ConfigParser(interpolation=None)
    cp.read(path, encoding="utf-8-sig")
    assert cp.has_section("ci-tiers"), "%s declares no [ci-tiers] section" % path
    rows = {}
    for trigger in cp.options("ci-tiers"):
        raw = cp.get("ci-tiers", trigger)
        assert raw.count("|") == 1, (
            "%s [ci-tiers] %s = %r is not the `<tier> | <moment>` row shape "
            "(exactly one `|`)" % (path, trigger, raw)
        )
        tier, sep, moment = raw.partition("|")
        assert sep and moment.strip(), (
            "%s [ci-tiers] %s = %r names no human moment; the row shape is "
            "`<tier> | <moment>`" % (path, trigger, raw)
        )
        rows[trigger] = (tier.strip(), moment.strip())
    assert rows, "%s [ci-tiers] parsed empty" % path
    return rows


# --- reading a workflow -------------------------------------------------------

_STEP = re.compile(
    r"(?m)^\s*-\s+(?:name|uses|run|if|id|env|with|shell|working-directory):"
)


def _step_blocks(text):
    starts = [m.start() for m in _STEP.finditer(text)]
    return [text[a:b] for a, b in zip(starts, starts[1:] + [len(text)])]


def _scalar(block, key):
    """The single-line value of `key:` in a step block, or None."""
    m = re.search(r"(?m)^\s*(?:-\s+)?%s:[ \t]*(.*)$" % key, block)
    return m.group(1).strip() if m else None


def _live_lines(text):
    return [ln for ln in text.splitlines() if not ln.lstrip().startswith("#")]


def _harness_invocations(line):
    """Command-position invocations of the harness on one live line.

    `python <path ending in scripts/check.py>` at the start of the command (or
    after a shell connector) — a line that merely MENTIONS the path (an `echo`,
    a string argument) is not an invocation. The distinction is the point: the
    pin is about what CI RUNS, and `run: echo python scripts/check.py` runs
    nothing.
    """
    body = re.sub(r"^\s*(?:-\s+)?run:\s*", "", line.strip())
    return re.findall(
        r"(?:^|[;&|(]\s*)(?:python3?|py)\s+(\S*%s)\b" % re.escape(HARNESS), body
    )


def _check_py_default_tier():
    """check.py's own `--tier` default, READ from the script rather than
    restated here — a step that passes no tier still runs a definite tier, and
    which one is check.py's business, not this module's."""
    src = (SCRIPTS / "check.py").read_text(encoding="utf-8")
    m = re.search(r'add_argument\(\s*"--tier".*?default="(\w+)"', src, re.DOTALL)
    assert m, "check.py's --tier default is no longer readable from its source"
    return m.group(1)


DEFAULT_TIER = _check_py_default_tier()


def harness_steps(text):
    """Every step that runs the harness, as (step name, `if:` guard, tier).

    The tier is the step's explicit `--tier` or, absent one, check.py's own
    default — so a step that passes no tier is read as the tier it actually
    runs, not as "unknown".
    """
    out = []
    for block in _step_blocks(text):
        for line in _live_lines(block):
            if not _harness_invocations(line):
                continue
            # the LAST --tier wins, because that is what argparse executes — a
            # first-match read would report `--tier smoke --tier all` as smoke
            # while CI runs all.
            tiers = re.findall(r"--tier\s+(\S+)", line)
            out.append(
                (
                    _scalar(block, "name"),
                    _scalar(block, "if"),
                    tiers[-1] if tiers else DEFAULT_TIER,
                )
            )
    return out


# --- the declaration itself ---------------------------------------------------


def test_declared_rows_name_real_tiers_and_known_triggers():
    # A declaration that names a tier check.py does not have would be a table
    # nothing could honour, and the pins below would still "pass".
    for path in (STACK_TEMPLATE, STACK_LIVE):
        for trigger, (tier, _moment) in declared(path).items():
            assert tier in CHECK.TIERS, "%s: %s = %s is not a check.py tier" % (
                path,
                trigger,
                tier,
            )
            assert trigger in set(GUARD_TRIGGER.values()), (
                "%s: unknown CI trigger %r" % (path, trigger)
            )


def test_the_shipped_table_is_the_documented_human_bar():
    # The three moments the process documents, in the order the bar rises. This
    # asserts the shipped VALUES, which is the point of declaring them: the
    # per-commit bar must be the cheap tier and a release must claim the top one,
    # so "CI got faster" can never quietly mean "CI got weaker".
    rows = declared(STACK_TEMPLATE)
    assert {t: v[0] for t, v in rows.items()} == {
        "push": "smoke",
        "pull_request": "full",
        "tag": "release",
    }


# --- the shipped reference workflow, pinned to the shipped declaration --------


def test_reference_workflow_tiers_match_the_declaration():
    # (a) of the OI-24 build: the trigger->tier mapping the workflow actually
    # implements is compared to the declaration, both directions. Failing here
    # is not a request to edit this test — either the workflow drifted, or the
    # scope change belongs in `[ci-tiers]` first.
    rows = declared(STACK_TEMPLATE)
    seen = {}
    for name, guard, tier in harness_steps(CI_REFERENCE.read_text(encoding="utf-8")):
        assert guard, "%s: harness step %r runs at every trigger" % (CI_REFERENCE, name)
        trigger = GUARD_TRIGGER.get(" ".join(guard.split()))
        assert trigger, (
            "unrecognised `if:` guard %r — name the moment it selects in "
            "GUARD_TRIGGER, or fix the workflow" % guard
        )
        assert trigger not in seen, "two harness steps claim the %s moment" % trigger
        seen[trigger] = tier
    assert seen == {t: v[0] for t, v in rows.items()}


def test_reference_workflow_step_labels_agree_with_what_they_run():
    # The step LABELS are the third copy of the mapping a reader meets, and a
    # label is exactly the sort of thing an edit forgets. Each must name the
    # tier it runs and the moment it fires at.
    for name, guard, tier in harness_steps(CI_REFERENCE.read_text(encoding="utf-8")):
        trigger = GUARD_TRIGGER[" ".join(guard.split())]
        label = name.lower().replace("_", " ")
        assert tier in label, "step %r runs --tier %s and does not say so" % (
            name,
            tier,
        )
        assert trigger.replace("_", " ") in label, (
            "step %r fires at the %s moment and does not say so" % (name, trigger)
        )


def test_reference_workflow_runs_the_documented_human_entry_point():
    # (b) of the OI-24 build: ONE definition of passing. The shipped agent guide
    # names `python scripts/check.py` as the bar; every PYTHON entry point the
    # workflow touches must be the harness (or the release-checklist generator
    # the release moment also owes). Honestly: the inventory sees `.py` tokens,
    # so a non-Python check (npm test, a bare shell loop) is outside its reach —
    # that class is an adopter edit, which OI-24 already places out of scope.
    agents = (KIT / "AGENTS.template.md").read_text(encoding="utf-8")
    assert "`python %s`" % HARNESS in agents, (
        "the agent guide no longer documents %s as the human bar; this pin's "
        "reference point moved" % HARNESS
    )
    ci = CI_REFERENCE.read_text(encoding="utf-8")
    invoked = set(re.findall(r"[\w./-]*\.py", "\n".join(_live_lines(ci))))
    assert HARNESS in invoked, "the reference workflow no longer invokes " + HARNESS
    assert invoked <= ALLOWED_INVOCATIONS, (
        "the reference workflow runs checks outside the harness (a second "
        "definition of passing): " + str(sorted(invoked - ALLOWED_INVOCATIONS))
    )


def test_no_job_level_guard_can_disable_a_declared_moment():
    # The step guards above are only meaningful if nothing ABOVE them can veto
    # the whole job: a job-level `if:` on the reference workflow would disable
    # declared moments while every step-level pin stays green. The reference
    # workflow has none, and growing one is a reviewed edit here.
    ci = CI_REFERENCE.read_text(encoding="utf-8")
    assert not re.search(r"(?m)^ {4}if:", ci), (
        "the reference workflow grew a job-level `if:` — a veto above the "
        "step guards the tier pins read; route the condition through the "
        "step guards or name it here deliberately"
    )


def test_the_declared_tag_moment_can_actually_fire():
    # A `tag` row is a claim about a trigger, so the trigger must exist: without
    # `tags:` in the `on: push:` block the release step is unreachable and the
    # mapping above would agree with a workflow that never runs it.
    ci = CI_REFERENCE.read_text(encoding="utf-8")
    assert re.search(r"(?m)^\s+tags:\s*\[", ci), (
        "[ci-tiers] declares a `tag` moment the workflow's `on:` cannot reach"
    )


def test_the_workflow_comments_point_at_the_declaration_and_do_not_restate_it():
    # ONE HOME, enforced. The comment that used to carry the table now points at
    # it; no comment may pair a moment with a tier again, because a prose copy
    # is precisely what drifts silently while the `run:` lines stay green.
    ci = CI_REFERENCE.read_text(encoding="utf-8")
    assert "[ci-tiers]" in ci, "the workflow no longer points at the declaration"
    offenders = [
        ln.strip()
        for ln in ci.splitlines()
        if ln.lstrip().startswith("#")
        and "[ci-tiers]" not in ln
        and _TRIGGER_WORDS.search(ln)
        and _TIER_WORDS.search(ln)
    ]
    assert not offenders, (
        "these comments restate the moment->tier table instead of pointing at "
        "docs/stack.ini [ci-tiers]: " + str(offenders)
    )


# --- this repo's own workflow, pinned to its own declaration ------------------


def test_this_repos_own_gate_never_drops_below_its_declared_tier():
    # .github/workflows/test.yml is NOT the reference workflow's shape and is
    # not forced into it: it is un-tiered on purpose (docs/stack.ini
    # [ci-tiers]), one `gate` job at check.py's default `all` for both triggers,
    # because this repo's product IS the harness. So the guard->trigger
    # recogniser above has nothing to discriminate here — what is worth pinning
    # is the downgrade: a quiet `--tier smoke` on the gate job would shrink the
    # only independent environment the kit gets, and must instead be a reviewed
    # edit to the declaration.
    rows = declared(STACK_LIVE)
    tiers = {t: v[0] for t, v in rows.items()}
    assert set(tiers) == {"push", "pull_request"}, (
        "this repo's workflow fires no other trigger: " + str(sorted(tiers))
    )
    steps = harness_steps(CI_THIS_REPO.read_text(encoding="utf-8"))
    assert len(steps) == 1, "expected exactly one gate step, got " + str(steps)
    _name, guard, tier = steps[0]
    assert guard is None, (
        "the gate STEP grew an `if:` guard (%r) — a step-level veto would "
        "disable the gate while this pin still saw its tier; disabling or "
        "conditioning the gate is a reviewed edit" % guard
    )
    assert set(tiers.values()) == {tier}, (
        "the gate job runs --tier %s; docs/stack.ini [ci-tiers] declares %s"
        % (tier, tiers)
    )
    # The gate JOB's only permitted guard is the known fork-PR dedup (runs on
    # every push; PRs only from forks, because an internal PR's commits already
    # ran at push). An unrecognised job guard is a failure, not a shrug —
    # the GUARD_TRIGGER reviewed-edit property applied one level up.
    ci = CI_THIS_REPO.read_text(encoding="utf-8")
    dedup = (
        "github.event_name == 'push' || "
        "github.event.pull_request.head.repo.full_name != github.repository"
    )
    for m in re.finditer(r"(?m)^ {4}if:[ \t]*(.*)$", ci):
        assert " ".join(m.group(1).split()) == dedup, (
            "unrecognised job-level guard %r in test.yml — name it here "
            "deliberately" % m.group(1)
        )


def test_this_repos_own_gate_runs_the_same_entry_point():
    # The same "one definition of passing" claim, dogfooded: the meta-repo's
    # gate job runs the kit's own check.py, not a hand-rolled command list.
    ci = CI_THIS_REPO.read_text(encoding="utf-8")
    assert any(_harness_invocations(ln) for ln in _live_lines(ci)), (
        "this repo's CI no longer INVOKES its own harness at command position "
        "(a line that merely mentions the path does not count)"
    )


# --- bite proofs: each pin driven RED on a planted defect ----------------------


def test_bite_a_retiered_workflow_step_is_caught():
    rows = {t: v[0] for t, v in declared(STACK_TEMPLATE).items()}
    ci = CI_REFERENCE.read_text(encoding="utf-8")
    seen = {
        GUARD_TRIGGER[" ".join(g.split())]: tier for _n, g, tier in harness_steps(ci)
    }
    assert seen == rows  # clean today
    # someone "optimises" the PR moment down to the cheap tier
    mutated = ci.replace("check.py --tier full", "check.py --tier smoke")
    got = {
        GUARD_TRIGGER[" ".join(g.split())]: tier
        for _n, g, tier in harness_steps(mutated)
    }
    assert got != rows


def test_bite_a_step_that_stops_passing_a_tier_is_read_as_its_real_tier():
    # Dropping the flag does not make the step "unknown" — it makes it `all`,
    # which is what it would actually run, so the comparison still bites.
    ci = CI_REFERENCE.read_text(encoding="utf-8")
    mutated = ci.replace("check.py --tier smoke", "check.py")
    tiers = {g: tier for _n, g, tier in harness_steps(mutated)}
    assert DEFAULT_TIER in tiers.values()
    assert DEFAULT_TIER == "all"


def test_bite_a_second_definition_of_passing_is_caught():
    ci = CI_REFERENCE.read_text(encoding="utf-8")
    mutated = ci.replace(
        "run: python scripts/check.py --tier full",
        "run: python scripts/my_faster_checks.py",
    )
    invoked = set(re.findall(r"[\w./-]*\.py", "\n".join(_live_lines(mutated))))
    assert not invoked <= ALLOWED_INVOCATIONS


def test_bite_a_mentioned_but_not_invoked_harness_is_not_counted():
    # The echo defeat from the adversarial round: a line that PRINTS the
    # command must not satisfy a pin about what CI RUNS.
    assert not _harness_invocations(
        "      run: echo python scripts/check.py --tier full"
    )
    assert _harness_invocations("      run: python scripts/check.py --tier full")
    assert _harness_invocations(
        "      run: python project-trajectory/scripts/check.py --jobs 0"
    )
    assert _harness_invocations("      run: cd repo && python scripts/check.py")


def test_bite_a_duplicate_tier_flag_reads_as_what_argparse_runs():
    # `--tier smoke --tier all` executes all (argparse last-wins); a first-match
    # read would have reported smoke and kept the pin green through a real
    # scope change.
    steps = harness_steps(
        "      - name: sneaky\n"
        "        if: github.event_name == 'pull_request'\n"
        "        run: python scripts/check.py --tier smoke --tier all\n"
    )
    assert [t for _n, _g, t in steps] == ["all"]


def test_bite_a_bare_run_step_cannot_ride_a_neighbours_guard():
    # A `- run:`-first step is its OWN step: it must not glue onto the previous
    # block and inherit its name/guard, which would let an added unguarded
    # harness step hide behind a guarded neighbour.
    text = (
        "      - name: Full suite (pull request)\n"
        "        if: github.event_name == 'pull_request'\n"
        "        run: python scripts/check.py --tier full\n"
        "      - run: python scripts/check.py --tier release\n"
    )
    steps = harness_steps(text)
    assert len(steps) == 2
    assert steps[1][0] is None and steps[1][1] is None  # no name, NO guard


def test_bite_a_restated_table_in_a_comment_is_caught():
    line = "      # cheap smoke on every push, the full suite on PRs."
    assert _TRIGGER_WORDS.search(line) and _TIER_WORDS.search(line)
    # …while the pointer that replaced it, and the prose that legitimately names
    # one or the other, are not offenders.
    for clean in (
        "      # `docs/stack.ini` `[ci-tiers]` declares which tier runs when.",
        "      # raise it if your release tier legitimately runs longer.",
        "      # One live run per ref: stacked pushes cancel the superseded run.",
    ):
        assert not (_TRIGGER_WORDS.search(clean) and _TIER_WORDS.search(clean)), clean
