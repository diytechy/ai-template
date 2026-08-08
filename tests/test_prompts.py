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

Plus the downstream path the declared-absence line promises: a bootstrapped
scaffold gets every template, and `prompts.py` loads them from there.
"""

import re

import pytest
from conftest import KIT, SCRIPTS, load_script, run_py

pr = load_script("prompts")
plan_briefs = load_script("plan_briefs")


# --- the catalogue ------------------------------------------------------------


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
    pr.ADJUDICATE_CONFLICT,
    pr.ADJUDICATE_RED_TC,
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


def test_a_scaffold_gets_every_template_and_loads_them_from_there(tmp_path):
    """The `prompts/` declared-absence says this repo's own home is
    project-trajectory/prompts/ and the SCAFFOLD destination is <repo>/prompts/.
    That promise is worth exactly as much as this test: bootstrap a real
    scaffold, point the loader at it, and load every key."""
    dest = tmp_path / "repo"
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", dest], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr

    scaffolded = dest / "prompts"
    assert (scaffolded / "README.md").is_file()
    for filename in pr.KIT_PROMPTS.values():
        assert (scaffolded / filename).is_file(), filename

    # And the loader resolves them from a scaffold's layout, where scripts/ is
    # at the repo root so KIT is the repo root itself.
    scaffold_pr = load_script("prompts")
    scaffold_pr.PROMPTS = scaffolded
    assert scaffold_pr.preflight() == []
    assert scaffold_pr.load(scaffold_pr.WORKER) == pr.load(pr.WORKER)
