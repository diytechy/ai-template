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
from conftest import KIT, load_script

pr = load_script("prompts")
plan_briefs = load_script("plan_briefs")


# --- the catalogue ------------------------------------------------------------


def test_disposition_brief_gates_the_successor_through_open_item_wi_refs():
    text = pr.load(pr.ADJUDICATE_DISPOSITION)
    assert "lists the successor in the open item's `wi_refs`" in text
    assert "successor stays queued but blocked until the owner rules" in text
    assert "lands its id in the successor's `needs`" not in text


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
