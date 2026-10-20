"""The prompt templates as FILES, and the strict fill (plan §8).

Three things are pinned here, and each one is a defect this repo has already
paid for:

  * **The move is byte-preserving.** The worker / reviewer / critique briefs
    moved out of `agent_loop.py` string constants into `prompts/*.template.md`,
    and the text a session receives did not change by one byte. Several phrases
    in those briefs are asserted as CONTIGUOUS substrings elsewhere in the
    suite, and the fake-CLI harness tells a reviewer session from a worker one
    by matching `Write your verdict to (\\S+)` — so a re-wrap fails a dozen
    tests in confusing ways rather than with a prompt-text message.

  * **The fill is strict in both directions.** An unknown key and an unfilled
    slot both raise. A brief never ships with a hole where a redacted input
    belongs, and a template edit that drops a slot fails loudly instead of
    silently sending a session less context than its author believes.

  * **The authoring rules are enforced, not hoped** — every judging template
    ends in a machine-typed verdict line drawn from a closed enum, and no
    judging template carries the judged party's self-assessment. Both rules are
    measured: a magic substring in free prose once selected a review tier (so a
    typo downgraded the judgement), and derived prose injected at claim time
    once opened a judge's brief with the defendant's own verdict.

The downstream path the declared-absence line promises (a bootstrapped
scaffold gets every template, and `prompts.py` loads them from there) is
driven in test_prompts_driven.py.
"""

import re

import pytest
from conftest import KIT, ROOT, load_script

pr = load_script("prompts")
plan_briefs = load_script("plan_briefs")
review_brief = load_script("review_brief")
adjudicate_brief = load_script("adjudicate_brief")


# --- the catalogue ------------------------------------------------------------


def test_disposition_brief_makes_the_successor_the_open_items_placeholder():
    # WI-790: the minted id lands in the successor's `needs`, the successor is
    # the item's placeholder on the queue, and the ruling updates it in the
    # same commit (OI-102 Q1: its Done-when gains the decided criteria).
    text = pr.load(pr.ADJUDICATE_DISPOSITION)
    assert "writes its id into the successor's `needs`" in text
    assert "the successor is the open item's PLACEHOLDER on the queue" in text
    assert "queued but blocked until the owner rules" in text
    assert "`docs/requirements/open-items.toml#OI-NNN`" in text
    assert "Ruling the item updates the successor in the same commit" in text
    assert "`wi_refs`" not in text


def test_every_declared_prompt_key_has_a_shipped_file():
    # The map is the contract: a key with no file is a session that cannot
    # launch, and a file with no key is prose nothing sends.
    for key, filename in pr.KIT_PROMPTS.items():
        assert (KIT / "prompts" / filename).is_file(), key
    shipped = {p.name for p in (KIT / "prompts").glob("*.template.md")}
    mapped = set(pr.KIT_PROMPTS.values()) | set(plan_briefs.HAT_KEYS.values())
    assert shipped == mapped, "every shipped template must be reachable by a key"


def test_preflight_is_clean_and_bites_on_a_missing_file(tmp_path, monkeypatch):
    assert pr.preflight() == []
    # The bite: point the loader at an empty dir and every key must refuse BY
    # NAME. A guard nobody has seen fail is not a guard.
    monkeypatch.setattr(pr, "PROMPTS", tmp_path)
    refusals = pr.preflight()
    assert len(refusals) == len(pr.KIT_PROMPTS)
    assert all("cannot read" in r for r in refusals)
    assert any(pr.WORKER in r for r in refusals)


def test_an_unknown_key_refuses_by_name():
    with pytest.raises(pr.PromptError) as exc:
        pr.load("NO-SUCH-PROMPT")
    assert "unknown prompt key" in str(exc.value)


# --- the byte-preserving move -------------------------------------------------


def test_the_three_engine_briefs_load_and_carry_their_load_bearing_clauses():
    worker = pr.load(pr.WORKER)
    reviewer = pr.load(pr.REVIEWER)
    critique = pr.load(pr.CRITIQUE)

    # The worker's structural lines — the fake CLIs parse these with regexes.
    assert "- WI: {wi} — {title}" in worker
    assert (
        "- Branch: {train} (its claim is docs/work/active/{train}/; integration "
        in worker
    )
    assert "base {base})" in worker
    assert "    WI: {wi}" in worker

    # The reviewer's two byte-exact "bones" (they span source-concatenation
    # boundaries in the constant this replaced — a re-wrap breaks them).
    assert (
        "a leaked self-assessment collapses review finding-rates several-fold"
        in reviewer
    )
    assert "VERDICT: APPROVE|CHANGES-REQUESTED findings=N" in reviewer
    assert "REAL shipped code paths" in reviewer
    assert "worst failure classes THIS change admits" in reviewer

    assert "INDEPENDENT critic" in critique
    assert "{brief}" in critique and "{verdict}" in critique


def test_the_briefs_finding_grammar_names_the_parsers_severities():
    # WI-888: the severities a brief tells its reviewer to write are the set
    # the one finding parser reads, so the two cannot drift: the grammar is
    # composed here from `score_reviews.SEVERITIES`, never retyped. The two
    # briefs whose verdicts that parser reads carry it, and so does the method's
    # own statement of the review block.
    severities = load_script("score_reviews").SEVERITIES
    grammar = "- [{}] ".format("|".join(severities))
    for key in (pr.REVIEWER, pr.CRITIQUE):
        assert grammar in pr.load(key), key
    assert grammar in (KIT / "PROCESS.md").read_text(encoding="utf-8")


def test_the_reviewer_brief_carries_the_construction_first_clause():
    # WI-567: the finding contract requires, for any remedy that ADDS a check,
    # guard, warn, or invariant, one clause naming why the defect cannot be made
    # unrepresentable instead — citing the vendored `antidote` skill rather than
    # restating it (CLAUDE.md, "Dogfood the philosophy"). Warn-first: it binds
    # the remedy's WORDING, never the verdict, and the MINOR/`for clarity` arm
    # and trust-boundary validation are exempt. Pinned here the same way the
    # other reviewer load-bearing clauses are, so an edit that quietly drops the
    # discipline reds a test instead of a review round.
    reviewer = pr.load(pr.REVIEWER)
    assert "cannot be made UNREPRESENTABLE instead" in reviewer
    assert "the `antidote` skill" in reviewer
    # The exemptions are load-bearing — dropping either re-opens the failure the
    # plan's §2 warns against (a gate, or over-reach onto every MINOR).
    assert "MINOR `for clarity`" in reviewer
    assert "validation at a genuine trust boundary" in reviewer
    assert "REACHABLE bad state the design could have made unreachable" in reviewer


def test_the_reviewer_brief_names_the_work_items_own_spec_as_the_spec_of_record():
    # Specs live in the work-item files under docs/work/; `docs/specs/` holds
    # only its README and inert example in a scaffold, so a brief sending the
    # reviewer there sends it to an empty folder. No shipped prompt may still
    # point at `docs/specs` as where open work lives.
    reviewer = pr.load(pr.REVIEWER)
    assert "each work item's own spec file under docs/work/" in reviewer
    assert "`specref` target where that points elsewhere" in reviewer
    for key in sorted(pr.KIT_PROMPTS):
        assert "docs/specs" not in pr.load(key), key


def test_the_reviewer_and_worker_briefs_link_the_guard_rule_and_restate_nothing():
    # The rule for when a guard is owed has one home, PROCESS.md §3. Both the
    # judge and the builder are pointed at it by its bullet name; neither copies
    # its trust-boundary list, which is what would drift.
    heading = '§3 "When a guard is owed"'
    process = (KIT / "PROCESS.md").read_text(encoding="utf-8")
    assert process.count("**When a guard is owed.**") == 1
    for key in (pr.REVIEWER, pr.WORKER):
        text = pr.load(key)
        assert heading in text, key
        assert "a file on disk, the network" not in text, key


# The shipped briefs that judge a review finding: the reviewer's, and the
# adjudicator's dispute brief that rules a contested one (WI-865).
FINDING_JUDGING_BRIEFS = (pr.REVIEWER, pr.ADJUDICATE_DISPUTE)

# The convergence stance's severity bound on a new finding (WI-911).
CONVERGENCE_BOUND = (
    "count a new finding as BLOCKER or MAJOR only when it is a fail-open "
    "path, data loss or a Done-when gap that a supported workflow or the "
    "kit's own routes reach, and every other new finding as MINOR"
)


def test_the_reviewer_brief_links_the_review_threat_model_and_restates_nothing():
    # The review threat model has one home, PROCESS.md §6: a finding whose
    # reproduction needs a compromised or contrived host is dismissed, never
    # answered with code. The reviewer brief points at it by its bold-lead
    # name; no shipped brief copies its example list, which is what would
    # drift from the home.
    process = (KIT / "PROCESS.md").read_text(encoding="utf-8")
    lead = "**Review threat model.**"
    assert process.count(lead) == 1
    start = process.index(lead)
    end = process.find("\n\n", start)
    paragraph = " ".join(process[start : end if end != -1 else None].split())
    for clause in (
        "the content agents write into the repository",
        "supported configurations",
        "regressions of supported behavior",
        "the host itself compromised or contrived",
        "is out of scope",
        "dismissed in one recorded line",
        "by whoever rules the finding",
        "in the response to the review verdict",
        "delegated-decisions record too, when the run keeps one",
        "never answered with code",
    ):
        assert clause in paragraph, clause
    for key in FINDING_JUDGING_BRIEFS:
        assert '§6 "Review threat model"' in pr.load(key), key
    examples = (
        "fake or hostile binary",
        "depends on the working directory",
        "changed by another process mid-call",
        "a tampered OS or tool",
    )
    for key in sorted(pr.KIT_PROMPTS):
        brief = " ".join(pr.load(key).split())
        for example in examples:
            assert example not in brief, (key, example)


def test_the_review_threat_model_dismisses_contrived_scenarios_and_gates_every_class():
    # The owner's ruling of 2026-10-13: a contrived, improbable scenario is
    # dismissed like a contrived host, severity tracks plausibility and
    # impact, and reachability gates a fail-open, data-loss or security path
    # as it gates any other; whoever rules a finding re-grades a mislabel.
    process = (KIT / "PROCESS.md").read_text(encoding="utf-8")
    start = process.index("**Review threat model.**")
    paragraph = " ".join(process[start : process.find("\n\n", start)].split())
    for clause in (
        "A finding whose reproduction needs a contrived, improbable scenario is "
        "dismissed the same way (owner ruling 2026-10-13)",
        "a hand act the process forbids (rewinding the trunk branch, skipping "
        "or disabling a hook, hand-editing a generated view or a ruled record)",
        "or ordinary tools run in an order no supported workflow or kit route produces",
        "Severity tracks plausibility and impact, not ingenuity, and "
        "reachability gates every class: a fail-open, data-loss or security "
        "path counts only when a supported workflow or the kit's own routes "
        "reach it; a rare or contrived path is MINOR at most, or dismissed as "
        "above.",
        "Whoever rules a finding re-grades a mislabelled BLOCKER or MAJOR.",
    ):
        assert clause in paragraph, clause


def test_a_spec_promise_reaches_only_what_supported_routes_produce():
    # The owner's ruling of 2026-10-15: a spec's promise over an input space
    # is bounded by what supported workflows and the kit's own routes
    # produce, stated once in the review threat model; the dispute brief
    # weighs a scenario's plausibility under it, and a cheap fix for a
    # contrived scenario is still dismissed.
    process = (KIT / "PROCESS.md").read_text(encoding="utf-8")
    start = process.index("**Review threat model.**")
    paragraph = " ".join(process[start : process.find("\n\n", start)].split())
    assert (
        "A spec's promise over an input space reaches only what supported "
        "workflows and the kit's own routes produce: hand-edited kit-written "
        "state, a hand-chosen name alias (case, trailing dots and the like) "
        "and a sub-second timing window lie outside it unless the spec names "
        "them as inside, so a finding that needs one is not stated behaviour."
    ) in paragraph
    dispute = " ".join(pr.load(pr.ADJUDICATE_DISPUTE).split())
    assert (
        "Weigh how plausible each finding's scenario is under that paragraph, "
        "a spec's promise included: whether a supported workflow or the kit's "
        "own routes reach it, not only whether the host is compromised or the "
        "fix is cheap. A cheap fix for a contrived scenario is still DISMISS."
    ) in dispute


def test_the_coordinator_skill_gates_the_confirming_round_by_reachability():
    # The coordinator's own copy of the confirming-round rule carries the same
    # reachability gate, and its triage step dismisses a contrived scenario
    # and re-grades a mislabel as the review threat model rules.
    skill = (KIT / "skills" / "coordinator-cycle" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    flat = " ".join(skill.split())
    for clause in (
        "A new finding blocks the claim only if it is fail-open, data loss or a "
        "Done-when gap, and a supported workflow or the kit's own routes reach "
        "it;",
        "compromised or contrived host, or a contrived scenario, in one recorded line",
        "re-grade a mislabelled BLOCKER or MAJOR there too.",
    ):
        assert clause in flat, clause


def test_a_lane_writes_its_tc_rows_and_tests_before_its_code():
    # WI-955: Terra's change set, TC rows included, precedes build round 1,
    # whose first deliverable is the tests under one evidence class each; the
    # old order (rows after the first build, a single plan owing no intent
    # turn) is gone from the skill and its recipes, and the spine-authoring
    # reference states the same order.
    cycle = KIT / "skills" / "coordinator-cycle"
    skill = " ".join(
        word
        for name in ("SKILL.md", "references/recipes.md")
        for word in (cycle / name).read_text(encoding="utf-8").split()
    )
    for clause in (
        "TC rows included, before build round 1",
        "Build round 1's first deliverable is the tests, committed alone before "
        "the code",
        "@pytest.mark.xfail(strict=True, raises=(AssertionError, "
        "pytest.fail.Exception))",
        "The code commit removes the marks",
        "with a stated adequacy witness, the wrong implementation it would "
        "catch, written in the test itself (its docstring or a comment)",
        "The intent set, committed before build round 1, already names it",
        "the independently checkable evidence its declared method names",
        "A test that fits none is named, with its disposition, in the lane's "
        "decisions record before the code commit.",
    ):
        assert clause in skill, clause
    for gone in (
        "after the first build",
        "owes no intent turn",
        "wi-918 D-002",
        "The builder builds the first round",
        "was drafted at intent, no round proposed row text",
        "the rest of the set follows the round",
    ):
        assert gone not in skill, gone
    # The order is the point: Terra's set, then the tests, then the code.
    assert (
        skill.index("Dispatch Terra once to author the **whole change set**")
        < skill.index("Build round 1's first deliverable")
        < skill.index("The builder then builds the code")
    )
    in_lane = " ".join(
        (KIT / "skills" / "spine-authoring" / "references" / "in-lane.md")
        .read_text(encoding="utf-8")
        .split()
    )
    assert "TC rows are authored with their LLRs before the build" in in_lane
    assert "the tests and symbols the build will create" in in_lane
    assert "Write the row text against settled code" not in in_lane
    assert in_lane.index("**Author it before the build.**") < in_lane.index(
        "**Amend the row text against settled code.**"
    )


def test_the_terra_brief_has_an_intent_form_before_build_round_1():
    # The spine author's brief serves the intent turn, before any build, as
    # well as the checkpoint: at intent it presumes no built code, no change
    # list and no diff, and its trace fields name what the build will create.
    # The checkpoint form keeps its slots, so its fill is unchanged.
    path = ROOT / "scripts" / "coordinator" / "terra-spine-prompt.template.md"
    text = path.read_text(encoding="utf-8")
    brief = " ".join(text.split())
    for clause in (
        "At the intent turn (the change list below reads `none`), before build "
        "round 1, no code, tests or docs are built yet",
        "There is no builder's change list and no code diff to read",
        "At a checkpoint turn, a Claude Opus builder has built the code, tests "
        "and docs in this lane",
        "At intent, a test-case row's evidence and an LLR's `code_symbol` name "
        "the tests and symbols the build will create",
        "they bind at the checkpoint's reconcile",
        "At a checkpoint, a test-case row's evidence names test functions that exist",
        "`check_doc_refs --strict` binds the symbol and fails on a row none of "
        "whose symbols exists yet, so an intent set binds by the checkpoint's "
        "reconcile",
    ):
        assert clause in brief, clause
    assert "A Claude Opus builder has built the code" not in brief
    assert "only WARNs on a symbol not yet written" not in brief
    slots = set(re.findall(r"@([A-Z_]+)@", text))
    assert slots == {
        "WI",
        "LANE",
        "BASE",
        "SPEC",
        "CHANGES",
        "WTROOT",
        "PY",
        "LANE_SLUG",
        "TESTS",
    }
    recipes = " ".join(
        (KIT / "skills" / "coordinator-cycle" / "references" / "recipes.md")
        .read_text(encoding="utf-8")
        .split()
    )
    assert "At the intent turn fill `CHANGES=none`" in recipes


def test_both_builder_briefs_search_before_minting_a_file_or_function():
    # WI-955: the producer side of the reviewer's duplication question.
    sentence = (
        "Search for an existing home before creating a file or function, and "
        "name the nearest existing home you considered"
    )
    worker = " ".join(pr.load(pr.WORKER).split())
    builder = " ".join(
        (ROOT / ".claude" / "agents" / "kit-builder.md")
        .read_text(encoding="utf-8")
        .split()
    )
    assert sentence in worker
    assert sentence in builder


def test_the_dispute_brief_offers_successor_and_never_for_a_convergence_class_finding():
    # WI-911: the sitting may move a real finding to a row of its own, filed
    # on trunk at the landing, but never a convergence-class one.
    text = " ".join(pr.load(pr.ADJUDICATE_DISPUTE).split())
    assert (
        "RULING: <id> SUCCESSOR <what the successor row must do, on the same line>"
        in text
    )
    assert (
        "A convergence-class finding (a fail-open path, data loss or a gap in the "
        "work item's Done-when) is never ruled SUCCESSOR: rule it FIX, or "
        "ESCALATE it." in text
    )
    assert _RECORD_ID.findall(pr.load(pr.ADJUDICATE_DISPUTE)) == []


def test_the_reviewer_brief_ties_severity_to_reachability_and_classifies_out_of_set_inputs():
    # WI-911 (review-churn rulings 1 and 4): a BLOCKER or MAJOR needs a
    # reachable scenario, and the reviewer, not the set's author, decides
    # whether an out-of-set input is a note (fail-closed) or a finding.
    text = " ".join(pr.load(pr.REVIEWER).split())
    for clause in (
        "Tie severity to reachability: a BLOCKER or MAJOR states a scenario "
        "reachable in normal use, and a fail-open, data-loss or security path "
        "counts only when a supported workflow or the kit's own routes reach "
        "it; a rare or contrived path is MINOR at most, or dismissed under "
        '{process_doc} §6 "Review threat model".',
        "An input outside the spec's declared set is yours to classify, not "
        "the set author's: one the change fails closed on is a "
        "coverage-extension note, written as prose outside the finding lines "
        "with no severity tag, so it never moves the count; one the change "
        "fails open on stays a finding at its severity.",
    ):
        assert clause in text, clause
    # Beside the threat-model sentence, restating none of its examples.
    threat = '§6 "Review threat model" sets. Tie severity to reachability'
    assert threat in text


def test_the_reviewer_brief_states_the_convergence_stance():
    # WI-911 (revisions 8 and 33): a convergence round reads no earlier
    # verdict, confirms each fix by its pre-fix-failing test or checkable
    # evidence, checks Done-when coverage and regressions, and tags each new
    # BLOCKER or MAJOR; the verdict grammar is unchanged.
    text = " ".join(pr.load(pr.REVIEWER).split())
    for clause in (
        "CONVERGENCE STANCE, only for a round whose round facts below say it "
        "runs in the convergence stance:",
        "read no earlier verdict and no record of one (nothing under "
        "docs/reviews/ or docs/decisions/, no filed plan critique, and no lane "
        "commit message, since those cite earlier rounds), and find each fix's "
        "pre-fix code from the diff and its test files' own history, through a "
        "command that prints no commit message (`git log -p --format=%h "
        "{trunk}..{head} -- <paths>`, each patch under its short hash alone), "
        "never from commit subjects;",
        "confirm each fix through its regression test failing on the pre-fix "
        "code, or, for a fix with no executable test, through independently "
        "checkable evidence (the corrected text at the cited site, or an "
        "inspection record)",
        "check each Done-when item's coverage, and look for regressions",
        "end each new BLOCKER or MAJOR finding line with "
        "`convergence-class: yes` (a fail-open path, data loss or a Done-when "
        "gap) or `convergence-class: no`",
        "The tag is advice to the dispute sitting, which alone defers a finding.",
        "The verdict's grammar, its word and its findings count are unchanged.",
    ):
        assert clause in text, clause
    # A new finding blocks only when it is a reachable convergence class; the
    # bound sits inside the convergence paragraph, not in the ordinary text.
    lead = "CONVERGENCE STANCE, only for a round whose round facts below say"
    assert CONVERGENCE_BOUND in text, CONVERGENCE_BOUND
    assert text.index(CONVERGENCE_BOUND) > text.index(lead)
    # A history command that prints commit messages would show the reviewer
    # the records the same sentence sets aside.
    assert "`git log -p`" not in text
    assert len(MACHINE_LINE.findall(pr.load(pr.REVIEWER))) == 1
    assert pr.load(pr.REVIEWER).count("Write your verdict to") == 1


def test_the_convergence_render_excludes_every_record_of_earlier_findings():
    # WI-911 (review-churn revision 8): the records that
    # summarize earlier findings are outside a convergence brief's own diff
    # command, the way the round files are outside every round's, so a
    # convergence round cannot read them by running it; the template's
    # command, which ordinary and loop rounds read, keeps the decisions record
    # and the plan's critiques. The rendered and git-driven arms are in
    # test_review_brief.py and test_review_brief_git.py.
    text = pr.load(pr.REVIEWER)
    command = re.search(r"`(git diff \{trunk\}\.\.\.\{head\} -- [^`]+)`", text)
    assert command, "the reviewer brief states no reading-scope command"
    ordinary = command.group(1)
    records = ("docs/decisions", "docs/plans/*/critique-*")
    assert ordinary.count(review_brief._RECORDS_EXCLUDE) == 1
    assert [r for r in records if r in ordinary] == []
    converging = ordinary.replace(
        review_brief._RECORDS_EXCLUDE, review_brief._CONVERGENCE_EXCLUDES
    )
    for record in ("docs/reviews",) + records:
        assert "':(exclude){}'".format(record) in converging, record


def test_the_llr_questions_ask_for_contract_voice_and_keep_the_trace_cells_binding():
    # WI-911 (review-churn ruling 5, revisions 35 and 36): section 3 asks for
    # an LLR's contract, names no implementation carrier, and keeps the
    # traced cells binding while the schema requires them.
    home = (KIT / "prompts" / "spine-questions.md").read_text(encoding="utf-8")
    section = home[home.index("## 3. At LLR and TC") :]
    flat = " ".join(section.split())
    assert "LLRs name modules and symbols by design" not in home
    for clause in (
        "**An LLR states its contract in words that survive a refactor.**",
        "the inputs it takes, the outcome it produces and where it refuses",
        "It names no implementation carrier (a code file, function or symbol), "
        "and §0's naming rule says which tiers may name a shipped boundary "
        "artifact.",
        "Do not launder a concrete name upward into the SR",
        "they stay filled and binding while the schema requires them "
        "(`trace.py --strict-schema` requires both; `check_doc_refs --strict` "
        "binds the symbol), so never return a row for keeping them.",
        "No `shall` in an LLR",
    ):
        assert clause in flat, clause
    bullet = section[: section.index("- **A child adds detail.**")]
    assert _RECORD_ID.findall(bullet) == [] and "item 5" not in bullet


NAMING_RULE = (
    "may be named at the LLR and TC tiers only; SN and SR rows name no file in "
    "any cell, acceptance and rationale included."
)


def test_every_tier_receives_the_one_naming_rule():
    # WI-911 (review-churn ruling 5): the file-naming
    # rule is held once, in the every-tier section, so the real composer hands
    # an SN or SR sitting the same rule as an LLR or TC one, and no tier is
    # still told to keep a file name in acceptance or behind a waiver.
    home = (KIT / "prompts" / "spine-questions.md").read_text(encoding="utf-8")
    flat_home = " ".join(home.split())
    assert flat_home.count(NAMING_RULE) == 1
    every_row = flat_home[flat_home.index("## 0. Every row") : flat_home.index("## 1.")]
    assert NAMING_RULE in every_row
    for tier in ("SN", "SR", "LLR", "TC"):
        text, why = adjudicate_brief.tier_questions({tier})
        assert why is None, why
        flat = " ".join(text.split())
        assert NAMING_RULE in flat, tier
        for stale in ("current-carrier evidence", "the waiver goes in `why`"):
            assert stale not in flat, (tier, stale)


def test_the_record_at_event_rule_has_one_home():
    # WI-911 (review-churn ruling 2): PROCESS.md §3 states it once, directly
    # after "When a guard is owed".
    process = (KIT / "PROCESS.md").read_text(encoding="utf-8")
    lead = "- **Record a decision where it is made.**"
    assert process.count(lead) == 1
    guard = process.index("- **When a guard is owed.**")
    after = process.index("\n- **", guard + 1)
    assert process[after + 1 :].startswith(lead)
    rule = " ".join(process[after:].split("\n- **")[1].split())
    assert "recorded by the step that makes it, in the commit where it is made" in rule
    assert "checked against that commit's parent" in rule
    assert "never recomputes the decision from history or from current state" in rule


def test_the_fan_out_rule_has_one_home_and_no_brief_or_skill_restates_it():
    # PROCESS.md §6 keeps both delegation kinds, names tiers, and forbids
    # fan-out from the judging sessions. A copy in a prompt or a shipped skill
    # would be a second home, and the first edit to the rule would miss it.
    process = (KIT / "PROCESS.md").read_text(encoding="utf-8")
    assert process.count("**Fan-out — two kinds, both kept, named by tier.**") == 1
    rule = "adjudication session never fans"
    assert process.count(rule) == 1
    texts = {key: pr.load(key) for key in pr.KIT_PROMPTS}
    for skill in sorted((KIT / "skills").glob("*/SKILL.md")):
        texts[skill.parent.name] = skill.read_text(encoding="utf-8")
    for name, text in texts.items():
        assert "never fans out" not in text and rule not in text, name


# The ids of this repository's own records. A kit-shipped brief that cites one
# sends an adopter to a record that does not exist in their repository.
_RECORD_ID = re.compile(r"\b(?:WI|SN|SR|LLR|TC|IF|OI|CMP|PB|PART|ASSET|REPO)-\d+\b")


def test_the_worker_brief_sent_body_cites_no_record_of_this_repository():
    # What survives the comment strip is what an adopter's session reads; the
    # measured evidence behind its rules lives in the dispatcher notes, where
    # the kit keeps its own history.
    raw = (KIT / "prompts" / pr.KIT_PROMPTS[pr.WORKER]).read_text(encoding="utf-8")
    body = pr.load(pr.WORKER)
    assert _RECORD_ID.findall(body) == []
    assert "concurrency-restructure" not in body
    notes = raw[: raw.find("-->")]
    assert "WI-540" in notes and "WI-538" in notes


def test_the_worker_close_bar_points_at_its_homes_instead_of_restating_it():
    # The bar is declared in two homes every scaffold carries: the step table
    # check.py selects at the rung in docs/stage, and the test tier selector in
    # docs/stack.ini [tiers]. A restatement naming a wall-time budget told a
    # scaffold's worker to run a budget its repo does not declare.
    worker = pr.load(pr.WORKER)
    assert "`check.py`'s step table" in worker
    assert "`docs/stack.ini` `[tiers]`" in worker
    assert "wall-time budget" not in worker
    template = (KIT / "stack.ini.template").read_text(encoding="utf-8")
    assert "\n[tiers]\n" in template


def test_the_worker_brief_carries_the_standing_state_ritual():
    # WI-506 (OI-57 ruled (b)): the worker gains a standing-state contract —
    # write the log.d fragment + the spec's own Context/Deliverable edits
    # BEFORE heavy verification, so a session killed or reaped mid-verification
    # leaves a resumable record rather than silent, uncommitted residue. Pinned
    # here the same way the reviewer/critique load-bearing clauses are, so an
    # edit that quietly drops the instruction reds a test instead of a review.
    worker = pr.load(pr.WORKER)
    assert "Standing-state discipline" in worker
    assert "before spending effort on heavy verification" in worker
    assert "not a one-shot write at the end" in worker


def test_the_worker_brief_points_at_the_spine_linked_tests_and_the_bar():
    # The inner loop and the bar are two different runs: while iterating, the
    # tests the spine links to the module being changed (derived by `trace.py
    # --tests-for`, never a hand-kept map or a file-name guess); before every
    # commit, the commit bar, whatever the inner loop said.
    worker = pr.load(pr.WORKER)
    assert "While iterating, run the tests the spine links to the module" in worker
    assert "{scripts}/trace.py --tests-for <module>" in worker
    assert "run the commit bar before every commit" in worker


def test_the_worker_brief_never_leaks_into_a_judge_brief():
    # The negative assertion the review/critique suites make from the other
    # side: no shared preamble may put the worker's framing in a judge's brief.
    worker_only = "assume no human is watching"
    assert worker_only in pr.load(pr.WORKER)
    for key in (pr.REVIEWER, pr.CRITIQUE):
        assert worker_only not in pr.load(key), key


def test_dispatcher_notes_are_stripped_and_the_body_starts_the_prompt():
    raw = (KIT / "prompts" / pr.KIT_PROMPTS[pr.REVIEWER]).read_text(encoding="utf-8")
    assert "DISPATCHER NOTES" in raw
    body = pr.load(pr.REVIEWER)
    assert "DISPATCHER NOTES" not in body
    assert body.startswith("You are an INDEPENDENT reviewer")


# --- the strict fill ----------------------------------------------------------


def test_fill_is_strict_in_both_directions():
    tmpl = "hello {name}, see {place}"
    assert pr.fill("T", tmpl, {"name": "a", "place": "b"}) == "hello a, see b"

    with pytest.raises(pr.PromptError) as unfilled:
        pr.fill("T", tmpl, {"name": "a"})
    assert "unfilled slot(s) place" in str(unfilled.value)

    with pytest.raises(pr.PromptError) as unknown:
        pr.fill("T", tmpl, {"name": "a", "place": "b", "extra": "c"})
    assert "unknown slot(s) extra" in str(unknown.value)


def test_a_slot_value_containing_braces_passes_through_verbatim():
    # The unfilled check reads the TEMPLATE's slot set, never the output, so a
    # value that happens to look like a slot is data, not a hole.
    out = pr.fill("T", "x {name}", {"name": "{place}"})
    assert out == "x {place}"


def test_doubled_braces_are_not_slots():
    assert pr.slots("literal {{not_a_slot}} and a real {one}") == {"one"}


# --- the authoring rules (plan §8, prompts/README.md) -------------------------

JUDGING = (
    pr.REVIEWER,
    pr.CRITIQUE,
    pr.ADJUDICATE_AMENDMENT,
    pr.ADJUDICATE_DISPOSITION,
    pr.ADJUDICATE_CONSOLIDATE,
    pr.ADJUDICATE_RED_TC,
    pr.ADJUDICATE_REJUDGE,
)

# A machine line: one closed enum, on its own line, with a typed counter. The
# rule exists because a magic substring in free prose (`NEEDS-HUMAN`) was once
# the ONLY input selecting a disposition's review tier — no constant, no
# validation, and a typo silently downgraded the judgement.
MACHINE_LINE = re.compile(r"^\s*(VERDICT|OUTCOME): [A-Z-]+(\|[A-Z-]+)+ [a-z]+=", re.M)


@pytest.mark.parametrize("key", JUDGING)
def test_every_judging_brief_ends_in_one_machine_typed_verdict_line(key):
    text = pr.load(key)
    hits = MACHINE_LINE.findall(text)
    assert len(hits) == 1, "{}: expected exactly one machine line, found {}".format(
        key, len(hits)
    )


@pytest.mark.parametrize("key", JUDGING)
def test_no_judging_brief_asks_for_the_judged_partys_self_assessment(key):
    # The generalized WI-418 rule. A judge's brief may NAME these surfaces to
    # forbid them (the reviewer brief does); what it must never do is slot one
    # in. So the check is on the SLOTS, which are what actually carry content.
    text = pr.load(key)
    for slot in pr.slots(text):
        assert slot not in {
            "status",
            "log",
            "notes",
            "self_assessment",
            "session_log",
        }, "{}: slot {{{}}} would carry a self-assessment into a judge's brief".format(
            key, slot
        )


@pytest.mark.parametrize("key", sorted(pr.KIT_PROMPTS))
def test_every_template_declares_its_slots_in_its_dispatcher_notes(key):
    # Rule 1: a slot is NAMED and BOUNDED. The notes block is where a clip is
    # declared, so every slot the body uses must at least appear there — a
    # brief whose caller silently truncates is one whose author cannot know
    # what the session read.
    raw = (KIT / "prompts" / pr.KIT_PROMPTS[key]).read_text(encoding="utf-8")
    notes = raw[: raw.find("-->")] if "-->" in raw else ""
    for slot in sorted(pr.slots(pr.load(key))):
        assert "{" + slot + "}" in notes, "{}: slot {{{}}} is undeclared".format(
            key, slot
        )


def test_the_worker_template_carries_no_stray_brace():
    # Rule 7: worker.template.md is filled with str.format, so a literal brace
    # raises at session-composition time — after preflight, inside a live run.
    text = pr.load(pr.WORKER)
    stripped = pr.SLOT_RE.sub("", text).replace("{{", "").replace("}}", "")
    assert "{" not in stripped and "}" not in stripped


# --- provenance ----------------------------------------------------------------


def test_digest_is_stable_across_line_endings():
    # The telemetry field must not report a model change on every clone: the
    # same template checked out CRLF and LF is the same prompt.
    lf = "line one\nline two\n"
    crlf = "line one\r\nline two\r\n"
    assert pr.digest(lf) == pr.digest(crlf)
    assert pr.digest(lf) != pr.digest("line one\nline three\n")
    assert pr.digest(lf).startswith("sha256:")


def test_catalog_rows_cover_every_key():
    rows = pr.catalog_rows()
    assert [r[0] for r in rows] == sorted(pr.KIT_PROMPTS)
    for _key, filename, _slots, dig in rows:
        assert filename.endswith(".template.md")
        assert dig.startswith("sha256:")


def test_cli_list_and_check(capsys):
    assert pr.main(["check"]) == 0
    assert pr.main(["list"]) == 0
    out = capsys.readouterr().out
    assert pr.WORKER in out and "worker.template.md" in out


# --- the downstream path the declared-absence line promises --------------------
# It bootstraps a real scaffold, so it lives in test_prompts_driven.py, outside
# the per-commit smoke tier.
