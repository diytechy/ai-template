"""outcome.py — the frozen scope, the immutable attempt record, and the
classification a partial attempt owes (SR-147..SR-150; TC-165..TC-169).

What is actually at stake here is that a branch cannot mark its own homework.
Three separate properties make that true, and each is driven on the shape that
would break it rather than on the shape that works:

  * **the scope is frozen at claim** (TC-166/TC-167) — the digest must survive
    the two things an honest close really does (fill `## Deliverable`, and let
    `spec_move` rebase the spec's own links one directory shallower) and must
    NOT survive an edit to a frontmatter cell or an obligation section. Both
    directions are driven, because a freeze that refuses honest closes is
    abandoned within a week and a freeze that excuses everything was never a
    freeze;
  * **one event per attempt** (TC-168) — the second write is refused BY ATTEMPT
    KEY, not by payload equality, so a lane that changed its mind cannot leave
    two live verdicts;
  * **exactly-once remediation** (TC-165) — the same failure observed twice is
    one event, and the normalisation that makes that true is driven with the
    parts that genuinely vary between observers (absolute paths, timings, shas,
    ANSI colour) present in one copy and absent from the other.

The git fixtures are REAL repositories, for the same reason `test_integrate.py`
gives: every fact this module reads comes off a tree or a commit message, so a
fake would test the wrong thing. The fixture helpers are copied from that
module's shapes rather than imported — no test module in this suite imports
another, and conftest is not this module's to extend.
"""

import hashlib
import json
import subprocess

import pytest
from conftest import (
    env_gate_skipif,
    load_script,
    skip_without_env_gates,
)

pytestmark = env_gate_skipif("git")

outcome = load_script("outcome")
integ = load_script("integrate")

T_BASE = 1_000_000
T_CODE = 1_000_100
T_LATER = 1_000_200


def _sha(seed):
    """A syntactically valid 40-hex commit id for the pure-unit tests. Named
    rather than inlined so an assertion reads as "the claim base", not as a
    wall of hex."""
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()


CLAIM_BASE = _sha("claim-base")
BRANCH_TIP = _sha("branch-tip")
OTHER_TIP = _sha("other-tip")
SCOPE = "0123456789abcdef"


# --- fixtures: real git repos (the tests/test_integrate.py shapes) ------------


def _git(root, *args, env=None):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def _commit(root, message, when=None):
    import os

    env = dict(os.environ)
    if when is not None:
        stamp = "@{} +0000".format(when)
        env["GIT_AUTHOR_DATE"] = stamp
        env["GIT_COMMITTER_DATE"] = stamp
    _git(root, "add", "-A", env=env)
    _git(root, "commit", "-qm", message, env=env)


def git_repo(root, branch="main"):
    """A committed git repo on `branch`. Identity is repo-local and signing is
    off, so a developer's global `commit.gpgsign` cannot wedge the fixture."""
    skip_without_env_gates("git")
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "symbolic-ref", "HEAD", "refs/heads/" + branch)
    (root / "seed.txt").write_text("seed\n", encoding="utf-8", newline="\n")
    _commit(root, "seed", when=T_BASE)
    return root


def spec_text(
    wid="WI-401",
    title="Widget",
    specref="seed.txt",
    sr_refs=("SR-001",),
    needs=(),
    safety="ordinary",
    context="Precedent: [the seed](../../seed.txt).",
    deliverable="",
):
    """One work-item spec in `wi_convert.py`'s format.

    The `## Context` block carries a RELATIVE link on purpose: it is the body
    section the mint writes, it is frozen, and it is exactly what
    `spec_move.move_spec` rewrites when the spec changes directory — so a
    fixture without one could not tell a real freeze from a vacuous one."""
    lines = [
        'id = "{}"'.format(wid),
        'title = "{}"'.format(title),
        'workstream = "ws"',
        "sr_refs = [{}]".format(", ".join('"{}"'.format(s) for s in sr_refs)),
        "needs = [{}]".format(", ".join('"{}"'.format(n) for n in needs)),
        'safety_class = "{}"'.format(safety),
        "order = 0",
    ]
    if specref:
        lines.append('specref = "{}"'.format(specref))
    text = "+++\n" + "".join(ln + "\n" for ln in lines) + "+++\n"
    if context:
        text += "\n## Context\n\n" + context + "\n"
    if deliverable:
        text += "\n## Deliverable\n\n" + deliverable + "\n"
    return text


def write_spec(root, where, wid="WI-401", slug="widget", **kw):
    """Write `docs/work/<where>/<wid>-<slug>.md`; return its path.

    `newline="\\n"` explicitly — a fixture that takes the platform default
    cannot test the platform (WI-337)."""
    path = root / "docs" / "work" / where / "{}-{}.md".format(wid, slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(spec_text(wid, **kw), encoding="utf-8", newline="\n")
    return path


def declare_generated(root):
    """Declare the §5.2 generated set, the way the shipped stack.ini template
    does — the claim folds `trunk_step --regen` into its commit, so an
    undeclared repo produces a claim commit touching an undeclared path."""
    ini = root / "docs" / "stack.ini"
    ini.parent.mkdir(parents=True, exist_ok=True)
    text = ini.read_text(encoding="utf-8") if ini.exists() else ""
    if "[generated]" not in text:
        text += ("\n" if text and not text.endswith("\n") else "") + (
            "[generated]\nPROJECT_STATE.html = trajectory\n"
        )
    ini.write_text(text, encoding="utf-8", newline="\n")


def claim_repo(tmp_path, wi="WI-401", **spec_kw):
    """A trunk repo whose `docs/work/` spec folder IS the work-item registry."""
    git_repo(tmp_path)
    write_spec(tmp_path, "queued", wi, **spec_kw)
    declare_generated(tmp_path)
    _commit(tmp_path, "file " + wi, when=T_CODE)
    return tmp_path


# --- TC-166: the scope digest (SR-148 / LLR-172) ------------------------------


@pytest.mark.smoke
def test_tc166_unchanged_and_close_field_share_a_digest_frozen_field_does_not():
    """TC-166, all three permutations in one place because the claim is a
    COMPARISON: unchanged and close-field must agree, frozen-field must not.

    `close-field` is driven as the two edits a legitimate terminal move really
    makes — filling `## Deliverable` and the link rebase `spec_move` performs on
    the way to a shallower directory — rather than as an abstract "some field",
    because those are the two that would have made this rung unusable."""
    unchanged = spec_text()
    close_field = spec_text(
        deliverable="Shipped the widget.",
        context="Precedent: [the seed](../seed.txt).",
    )
    frozen_field = spec_text(needs=["WI-400"])

    assert outcome.scope_digest(unchanged) == outcome.scope_digest(close_field)
    assert outcome.scope_digest(unchanged) != outcome.scope_digest(frozen_field)
    assert outcome.scope_diff(unchanged, close_field) == []
    assert outcome.scope_diff(unchanged, frozen_field) == ["front:needs"]


@pytest.mark.smoke
@pytest.mark.parametrize(
    "kw,region",
    [
        ({"wid": "WI-402"}, "front:id"),
        ({"title": "Something else"}, "front:title"),
        ({"specref": "docs/specs/other.md"}, "front:specref"),
        ({"sr_refs": ("SR-002",)}, "front:sr_refs"),
        ({"needs": ("WI-9",)}, "front:needs"),
        ({"safety": "spine"}, "front:safety_class"),
        ({"context": "Precedent: [something else](../../other.md)."}, "body:Context"),
    ],
)
def test_tc166_every_declared_frozen_cell_is_actually_frozen(kw, region):
    """SR-148's acceptance names the frozen region cell by cell — identity,
    references, acceptance definition, predecessors, safety class. A digest that
    covered "most" of them would be a freeze nobody could rely on, so each is
    driven on its own and the refusal must name that cell and only that cell."""
    assert outcome.scope_diff(spec_text(), spec_text(**kw)) == [region]


@pytest.mark.smoke
def test_tc166_a_deleted_obligation_section_counts_as_a_change():
    """Narrowing by DELETION is the cheapest way to make a completion claim
    true, so a region present on one side only must differ — a comparison that
    walked the shared keys alone would call this identical."""
    assert outcome.scope_diff(spec_text(), spec_text(context="")) == ["body:Context"]


@pytest.mark.smoke
def test_tc166_a_crlf_checkout_digests_as_the_lf_one_does():
    """Line endings are a property of the checkout, not of the text: the claim
    is read off trunk's working tree and the terminal copy off a git blob, so a
    Windows checkout must not read as a scope change (WI-337)."""
    lf = spec_text()
    assert outcome.scope_digest(lf.replace("\n", "\r\n")) == outcome.scope_digest(lf)


@pytest.mark.smoke
def test_tc166_a_link_retarget_is_not_excused_by_the_depth_normalisation():
    """The mutation proof for `_depth_free_links`: it exists to excuse the
    ritual's depth rebase, and it must excuse NOTHING else — a link pointed at a
    different file still differs even when both spellings share a depth."""
    before = spec_text(context="See [x](../../docs/specs/x.md).")
    same_target_deeper = spec_text(context="See [x](../../../docs/specs/x.md).")
    other_target = spec_text(context="See [x](../../docs/specs/y.md).")
    assert outcome.scope_diff(before, same_target_deeper) == []
    assert outcome.scope_diff(before, other_target) == ["body:Context"]


@pytest.mark.smoke
def test_tc166_the_close_may_clear_the_specref_and_may_not_repoint_it():
    """The one place two shipped rules collide, and the resolution pinned in
    both directions.

    SR-148 freezes the references; the spec-lifecycle rule R-F says a TERMINAL
    work item CLEARS its `SpecRef` and archives the spec — and the kit's own
    close ritual does exactly that. Freeze it flatly and every honest close
    refuses; drop it from the frozen set and a branch may repoint its own
    acceptance document at whatever it happened to build. Only the CLEARING is
    excused, so both rules hold; the digest still binds the cell whole, because
    the claim-time RECORD has to be a complete statement of the obligation."""
    claimed = spec_text(specref="docs/specs/WI-401.md")
    cleared = spec_text(specref=None, deliverable="Shipped.")
    repointed = spec_text(specref="docs/specs/WI-999.md", deliverable="Shipped.")

    assert outcome.scope_change(claimed, cleared) == []
    assert outcome.scope_change(claimed, repointed) == ["front:specref"]
    # ... and the DIGEST is untouched by the allowance: it still covers the
    # cell, so the recorded claim-time scope names the acceptance document.
    assert outcome.scope_digest(claimed) != outcome.scope_digest(cleared)
    assert outcome.scope_diff(claimed, cleared) == ["front:specref"]


@pytest.mark.smoke
def test_tc166_an_emptied_specref_is_the_same_clearing_as_a_deleted_one():
    """Rule R-F's terminal clearing has TWO legal spellings and the excuse has to
    cover both. `check_trajectory` reads `(r.get("SpecRef") or "").strip()` and
    `wi_convert.frontmatter_pairs` says outright that "absent and empty mean the
    same thing in this registry" — so excusing only the deletion made
    `scope_change` the one piece of code in the program that told them apart, and
    it refused the merge of an honest close. `docs/work/complete` is full of
    specs closed with `specref = ""`.

    The direction is still one-way: a REPOINT is not a clearing."""
    claimed = spec_text(specref="docs/specs/WI-401.md")
    closed = "\n## Deliverable\n\nShipped.\n"
    deleted = claimed.replace('specref = "docs/specs/WI-401.md"\n', "") + closed
    emptied = claimed.replace('specref = "docs/specs/WI-401.md"', 'specref = ""')
    repointed = claimed.replace("WI-401.md", "WI-999.md") + closed
    assert deleted != claimed and emptied != claimed

    assert outcome.scope_change(claimed, deleted) == []
    assert outcome.scope_change(claimed, emptied + closed) == []
    assert outcome.scope_change(claimed, repointed) == ["front:specref"]


@pytest.mark.smoke
def test_tc166_a_markdown_heading_quoted_inside_a_fence_is_not_a_section():
    """`## Deliverable` is the close's own record and specs QUOTE markdown in it
    all the time. A scanner blind to code fences reads a quoted `## Steps` as a
    real heading: it mints a frozen region the claim-time copy never had (or, if
    the quoted name repeats a real one, appends the post-fence remainder onto
    that frozen region) and the merge is refused over a section nobody edited.

    The discrimination is the other half: a heading OUTSIDE a fence is still a
    section, so the fence-awareness excuses quoting and nothing else."""
    claimed = spec_text()
    quoted_new = spec_text(
        deliverable=(
            "Shipped it. The template section now reads:\n\n"
            "```markdown\n## Steps\n\n1. run it\n```\n"
        )
    )
    quoted_frozen = spec_text(
        deliverable=(
            "Shipped it:\n\n```markdown\n## Context\n\nQuoted, not written.\n```\n\nDone."
        )
    )
    forged = spec_text(deliverable="Shipped it.\n\n## Steps\n\n1. run it")

    assert outcome.scope_change(claimed, quoted_new) == []
    assert outcome.scope_change(claimed, quoted_frozen) == []
    assert outcome.scope_digest(claimed) == outcome.scope_digest(quoted_frozen)
    assert outcome.scope_change(claimed, forged) == ["body:Steps"]


@pytest.mark.smoke
def test_tc166_the_clearing_allowance_covers_that_cell_and_no_other():
    """The mutation proof for `CLOSE_CLEARED_KEYS`: a DELETED cell is excused
    only for the one key R-F mandates. Deleting `needs` or `safety_class` at
    close is narrowing the obligation, and reads as one."""
    claimed = spec_text(needs=["WI-400"], safety="spine")
    without_needs = claimed.replace('needs = ["WI-400"]\n', "")
    without_class = claimed.replace('safety_class = "spine"\n', "")
    assert without_needs != claimed and without_class != claimed
    assert outcome.scope_change(claimed, without_needs) == ["front:needs"]
    assert outcome.scope_change(claimed, without_class) == ["front:safety_class"]


@pytest.mark.smoke
def test_tc166_a_spec_without_frontmatter_refuses_by_name():
    """A spec with no frontmatter declares no scope, and hashing its body anyway
    would freeze nothing while reporting a digest."""
    with pytest.raises(ValueError) as excinfo:
        outcome.scope_digest("## Deliverable\n\nno fence here\n")
    assert "REFUSED" in str(excinfo.value) and "frontmatter fence" in str(excinfo.value)


# --- TC-168: one immutable outcome event per attempt (SR-149 / LLR-174) -------


def _facts():
    return {
        "files": ["src/widget.py", "tests/test_widget.py"],
        "commits": [_sha("work-1")],
        "checks": [("lint", "PASS"), ("tests", "FAILED 2 of 40")],
        "blockers": ["the fixture needs a second station"],
        "unmet": ["AC-2: the widget does not round-trip"],
        "rationale": "Two of forty tests do not pass; the remaining scope is AC-2.",
    }


@pytest.mark.smoke
@pytest.mark.parametrize("word", outcome.OUTCOMES)
def test_tc168_each_worker_outcome_writes_one_event_carrying_the_facts(tmp_path, word):
    """TC-168 permutations complete | cancelled | partial. Each writes exactly
    one event carrying BOTH commits and the scope digest, and the checks land
    with their exact result strings rather than as a derived pass/fail bit."""
    event, refusals = outcome.write_outcome(
        tmp_path, "WI-401", word, CLAIM_BASE, BRANCH_TIP, SCOPE, **_facts()
    )
    assert refusals == []
    assert event["kind"] == "outcome" and event["outcome"] == word
    assert event["claim_base"] == CLAIM_BASE and event["branch_tip"] == BRANCH_TIP
    assert event["scope"] == SCOPE
    assert event["checks"] == [
        {"step": "lint", "result": "PASS"},
        {"step": "tests", "result": "FAILED 2 of 40"},
    ]
    lines = (
        (tmp_path / "docs/events/outcomes.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    )
    assert len(lines) == 1
    assert json.loads(lines[0]) == event


@pytest.mark.smoke
def test_tc168_a_second_write_for_the_same_attempt_is_refused(tmp_path):
    """The duplicate permutation, driven on the write worth refusing: not a
    byte-identical replay (which the content-derived id would already collapse)
    but a lane that recorded `partial` and then wants to record `complete`. Two
    live verdicts for one attempt is precisely the "which one is it" question
    this event exists to delete."""
    first, refusals = outcome.write_outcome(
        tmp_path, "WI-401", "partial", CLAIM_BASE, BRANCH_TIP, SCOPE
    )
    assert refusals == []

    second, refusals = outcome.write_outcome(
        tmp_path, "WI-401", "complete", CLAIM_BASE, OTHER_TIP, SCOPE
    )
    assert second is None
    assert len(refusals) == 1
    assert "REFUSED" in refusals[0] and "WI-401" in refusals[0]
    assert first["id"] in refusals[0]
    # and the ledger is untouched — a refusal that had already appended would be
    # the exact defect it reports.
    assert (
        len(
            (tmp_path / "docs/events/outcomes.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        )
        == 1
    )


@pytest.mark.smoke
def test_tc168_a_second_attempt_of_the_same_wi_is_a_different_event(tmp_path):
    """The mutation proof for the attempt key: it is `(wi, claim_base)`, so a
    genuinely new claim of the same id writes its own event. Keying on the id
    alone would make the second attempt unrecordable."""
    outcome.write_outcome(tmp_path, "WI-401", "partial", CLAIM_BASE, BRANCH_TIP, SCOPE)
    event, refusals = outcome.write_outcome(
        tmp_path, "WI-401", "complete", _sha("second-claim"), OTHER_TIP, SCOPE
    )
    assert refusals == [] and event is not None
    assert (
        len(
            (tmp_path / "docs/events/outcomes.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        )
        == 2
    )


@pytest.mark.smoke
def test_tc168_the_id_is_content_derived_and_ignores_the_timestamp(tmp_path):
    """Contracts §2's whole load-bearing property: the id is the digest of the
    payload with `id` and `ts` removed, so observing one fact at two times is
    not two events and any holder of the payload can re-derive the id rather
    than trusting the ledger."""
    early, _ = outcome.write_outcome(
        tmp_path,
        "WI-401",
        "complete",
        CLAIM_BASE,
        BRANCH_TIP,
        SCOPE,
        ts="2026-01-01T00:00:00Z",
        **_facts(),
    )
    late, _ = outcome.write_outcome(
        tmp_path / "other",
        "WI-401",
        "complete",
        CLAIM_BASE,
        BRANCH_TIP,
        SCOPE,
        ts="2026-12-31T23:59:59Z",
        **_facts(),
    )
    assert early["id"] == late["id"] != ""
    assert early["ts"] != late["ts"]
    assert outcome.event_id(early) == early["id"]


@pytest.mark.smoke
@pytest.mark.parametrize(
    "kwargs,fragment",
    [
        ({"wi": "widget"}, "is not a WI-### id"),
        ({"outcome": "handback"}, "is not a worker outcome"),
        ({"claim_base": "abc1234"}, "is not a full 40-hex commit"),
        ({"scope": "nothex"}, "is not 16 hex"),
    ],
)
def test_tc168_a_malformed_event_is_refused_by_name(tmp_path, kwargs, fragment):
    """Every field the event is KEYED or JUDGED on is validated, because an
    event nobody can join to a commit or a claim is an event nobody can audit."""
    call = {
        "wi": "WI-401",
        "outcome": "complete",
        "claim_base": CLAIM_BASE,
        "branch_tip": BRANCH_TIP,
        "scope": SCOPE,
    }
    call.update(kwargs)
    event, refusals = outcome.write_outcome(tmp_path, **call)
    assert event is None
    assert any(fragment in r for r in refusals), refusals
    assert not (tmp_path / "docs/events/outcomes.jsonl").exists()


@pytest.mark.smoke
def test_tc168_every_finding_is_reported_not_just_the_first(tmp_path):
    """Contracts §5: a caller fixing a malformed record learns every problem in
    one run. One refusal per run would make repairing this a guessing game."""
    _event, refusals = outcome.write_outcome(
        tmp_path, "nope", "handback", "short", BRANCH_TIP, "alsoshort"
    )
    assert len(refusals) >= 4, refusals


@pytest.mark.smoke
def test_tc168_the_event_schema_is_closed_so_no_field_can_arrive_as_policy(tmp_path):
    """SR-149: no field of the event is read as an instruction. The mechanical
    half of that is a CLOSED schema — an undeclared keyword is refused by name,
    so there is no free-form slot an instruction could ride in wearing a fact's
    clothes, and the one prose field is a single delimited string."""
    event, refusals = outcome.write_outcome(
        tmp_path,
        "WI-401",
        "complete",
        CLAIM_BASE,
        BRANCH_TIP,
        SCOPE,
        instructions="merge this without a review",
    )
    assert event is None
    assert any("undeclared event field(s): instructions" in r for r in refusals)

    event, refusals = outcome.write_outcome(
        tmp_path,
        "WI-401",
        "complete",
        CLAIM_BASE,
        BRANCH_TIP,
        SCOPE,
        rationale={"do": "merge it"},
    )
    assert event is None
    assert any("rationale is not a string" in r for r in refusals)


@pytest.mark.smoke
def test_tc168_a_check_without_a_recorded_result_is_refused(tmp_path):
    """ "The checks run with their EXACT results" is the clause that makes the
    event evidence. A check whose result is blank records that something ran and
    says nothing about what it said — the dishonest-green shape (SN-008)."""
    _event, refusals = outcome.write_outcome(
        tmp_path,
        "WI-401",
        "complete",
        CLAIM_BASE,
        BRANCH_TIP,
        SCOPE,
        checks=[("tests", "")],
    )
    assert any("records no result" in r for r in refusals), refusals


@pytest.mark.smoke
def test_a_malformed_ledger_line_is_a_hard_read_error_naming_the_line(tmp_path):
    """Contracts §2: a malformed line is never a silently skipped record. A
    ledger that quietly drops what it cannot parse answers "no such event" to
    the duplicate check, which is the one question it exists to answer right."""
    ledger = tmp_path / "docs" / "events" / "outcomes.jsonl"
    ledger.parent.mkdir(parents=True)
    ledger.write_text('{"kind":"outcome"}\nnot json at all\n', encoding="utf-8")
    with pytest.raises(ValueError) as excinfo:
        outcome.read_events(ledger)
    assert "line 2" in str(excinfo.value) and "outcomes.jsonl" in str(excinfo.value)

    _event, refusals = outcome.write_outcome(
        tmp_path, "WI-401", "complete", CLAIM_BASE, BRANCH_TIP, SCOPE
    )
    assert any("line 2" in r for r in refusals), refusals


@pytest.mark.smoke
def test_a_hand_edited_ledger_line_is_refused_because_its_id_no_longer_derives(
    tmp_path,
):
    """Contracts §2's third property — "a reader can verify the ledger rather
    than trusting it" — is only true if a reader actually does it. Without the
    re-derivation the stale id sat in the line, unchecked, while the edited
    payload was read as authoritative.

    Driven on the edit that defeats the module's central rung rather than on a
    flipped verdict: tampering with `claim_base` makes `write_outcome`'s
    `(wi, claim_base)` scan miss, so a SECOND outcome lands for one attempt —
    exactly the "which one is it" state the event exists to delete."""
    first, refusals = outcome.write_outcome(
        tmp_path, "WI-401", "partial", CLAIM_BASE, BRANCH_TIP, SCOPE
    )
    assert refusals == [] and first is not None
    ledger = tmp_path / "docs/events/outcomes.jsonl"
    ledger.write_text(
        ledger.read_text(encoding="utf-8").replace(CLAIM_BASE, _sha("forged")),
        encoding="utf-8",
        newline="\n",
    )

    with pytest.raises(ValueError) as excinfo:
        outcome.read_events(ledger)
    assert "line 1" in str(excinfo.value) and "does not derive" in str(excinfo.value)

    second, refusals = outcome.write_outcome(
        tmp_path, "WI-401", "complete", CLAIM_BASE, OTHER_TIP, SCOPE
    )
    assert second is None
    assert any("does not derive" in r for r in refusals), refusals

    # The guard is on PRESENCE, like attest's: a line carrying no id has no id
    # to disagree with, so a hand-written fixture is still readable.
    idless = tmp_path / "idless.jsonl"
    idless.write_text('{"kind":"outcome"}\n', encoding="utf-8", newline="\n")
    assert outcome.read_events(idless) == [{"kind": "outcome"}]


def test_a_fresh_scaffold_carries_every_terminal_status_directory(scaffold):
    """STATUS IS THE DIRECTORY, so a declared status with no directory is a
    vocabulary the scaffold cannot express. `partial` was declared everywhere the
    scripts read it — `SPEC_STATUS_DIRS`, `TERMINAL_STATUSES`,
    `outcome.OUTCOMES` — and scaffolded nowhere.

    Driven by BOOTSTRAPPING a scaffold rather than by reading the table, which is
    the only way this class of defect has ever been caught here."""
    work = scaffold / "docs" / "work"
    missing = [word for word in outcome.OUTCOMES if not (work / word).is_dir()]
    assert missing == [], sorted(p.name for p in work.iterdir())
    assert (work / "partial" / ".gitkeep").is_file()


# --- TC-165: exactly-once remediation (SR-147 / LLR-171) ----------------------


# A red `check.py` tail in the shape the harness really prints. `observer`
# parameterises exactly what differs between two runs of ONE failure over one
# checkout: the console's colour, the clock, the timings, a sha in the banner,
# and the path separator a Windows run prints where a POSIX one prints `/`.
def failure_text(
    root, posix=False, colour=True, secs="12.48", assertion="widget(2) == 4"
):
    sep = "/" if posix else ("\\" if "\\" in str(root) else "/")
    home = str(root).replace("\\", "/") if posix else str(root)
    head = "\x1b[31mFAIL\x1b[0m" if colour else "FAIL"
    stamp = "2026-08-08T04:15:02Z" if colour else "2026-08-09T22:00:41Z"
    sha = "9f2c1ab0d4e" if colour else "44bc9910f7a"
    return (
        "{} step tests (gate G2)\n"
        "  {}{}tests{}test_widget.py:42: AssertionError\n"
        "  assert {}\n"
        "  1 failed, 39 passed in {}s at {} (tree {})\n".format(
            head, home, sep, sep, assertion, secs, stamp, sha
        )
    )


def _tree_of(root):
    """A REAL tree id for the fixture — the identity a failure is keyed on has
    to come off git, or the test would be pinning a string this suite invented."""
    return _git(root, "rev-parse", "HEAD^{tree}").strip()


def test_tc165_one_red_bar_mints_one_event_and_a_repeat_mints_none(tmp_path):
    """TC-165, all four permutations on one tree.

    `first` mints. `repeat` is the SAME failure seen by a different observer —
    another machine, another checkout path, another clock, colour off — and must
    mint nothing, because the identity is a property of the failure and not of
    who watched it. `different-step` and `different-fingerprint` each mint one
    more, which is the half that stops the dedup from swallowing real defects.
    """
    root = git_repo(tmp_path)
    tree = _tree_of(root)
    seen_once = failure_text(root)
    seen_again = failure_text(root, posix=True, colour=False, secs="31.02")

    first, refusals = outcome.failure_event(root, tree, "tests", seen_once, gate="G2")
    assert refusals == [] and first["fingerprint"]

    repeat, refusals = outcome.failure_event(root, tree, "tests", seen_again, gate="G2")
    assert repeat is None
    assert len(refusals) == 1 and first["id"] in refusals[0]
    assert "exactly-once" in refusals[0]

    other_step, refusals = outcome.failure_event(root, tree, "lint", seen_once)
    assert refusals == [] and other_step["id"] != first["id"]

    other_failure, refusals = outcome.failure_event(
        root, tree, "tests", failure_text(root, assertion="widget(3) == 9")
    )
    assert refusals == []
    assert other_failure["fingerprint"] != first["fingerprint"]

    ledger = (root / "docs/events/failures.jsonl").read_text(encoding="utf-8")
    assert len(ledger.splitlines()) == 3


def test_tc165_a_different_tree_is_a_different_failure(tmp_path):
    """The tree is in the key so a failure is attributable to CODE. The same
    step failing the same way on a tree somebody has since changed is a new
    fact, not a rerun of the old one."""
    root = git_repo(tmp_path)
    first_tree = _tree_of(root)
    (root / "seed.txt").write_text("moved on\n", encoding="utf-8", newline="\n")
    _commit(root, "change the tree", when=T_LATER)

    text = failure_text(root)
    one, _ = outcome.failure_event(root, first_tree, "tests", text)
    two, refusals = outcome.failure_event(root, _tree_of(root), "tests", text)
    assert refusals == [] and one["id"] != two["id"]


def test_tc165_a_relative_root_fingerprints_as_the_absolute_one_does(
    tmp_path, monkeypatch
):
    """`.` is the ordinary spelling of "this repo", and the substitution took the
    caller's spelling literally: every PERIOD in the harness text became `<root>`
    (`test_widget<root>py:42`, `in 12<root><dur>`), the excerpt persisted in that
    state, and the real checkout path was never erased at all — so ONE failure
    minted TWO events depending only on how the observer spelled the root.

    Driven as the exactly-once property itself, because that is what breaks: the
    second observation must be refused as the same failure."""
    root = git_repo(tmp_path).resolve()
    monkeypatch.chdir(root)
    tree = _tree_of(root)
    text = failure_text(root)

    normalised = outcome.normalise_failure(".", text)
    assert str(root) not in normalised and "<root>" in normalised
    assert "test_widget.py:42" in normalised
    assert "<dur>" in normalised

    # The same over-substitution one level up: `/` and `C:\` are separators, not
    # prefixes, so a root that resolves to one is skipped rather than erased.
    assert "<root>" not in outcome.normalise_failure("/", text)

    absolute, refusals = outcome.failure_event(root, tree, "tests", text, gate="G2")
    assert refusals == [] and "<root>" in absolute["excerpt"]
    relative, refusals = outcome.failure_event(".", tree, "tests", text, gate="G2")
    assert relative is None
    assert len(refusals) == 1 and "exactly-once" in refusals[0]


@pytest.mark.smoke
def test_tc165_the_normalisation_keeps_what_makes_two_failures_different(tmp_path):
    """The mutation proof for `normalise_failure`: it must erase the observer
    and nothing else. Counts, assertion text and file/line references survive,
    because folding two defects into one event is the failure direction that
    silently loses a bug."""
    normalised = outcome.normalise_failure(tmp_path, failure_text(tmp_path))
    assert "\x1b[" not in normalised
    assert "12.48s" not in normalised and "2026-08-08" not in normalised
    assert str(tmp_path) not in normalised and "<root>" in normalised
    assert "test_widget.py:42" in normalised
    assert "assert widget(2) == 4" in normalised
    assert "1 failed, 39 passed" in normalised
    assert outcome.normalise_failure(
        tmp_path, failure_text(tmp_path)
    ) == outcome.normalise_failure(
        tmp_path, failure_text(tmp_path, posix=True, colour=False, secs="31.02")
    )


@pytest.mark.smoke
@pytest.mark.parametrize(
    "args,fragment",
    [
        (("nope", "tests", "FAIL step tests\n"), "is not a full 40-hex tree id"),
        ((_sha("t"), "", "FAIL step tests\n"), "the failing step is unnamed"),
        ((_sha("t"), "tests", "   "), "the failure output is empty"),
    ],
)
def test_tc165_an_unkeyable_failure_is_refused_rather_than_minted(
    tmp_path, args, fragment
):
    """An event whose key cannot be formed would collapse every anonymous
    failure onto one id — the opposite of exactly-once."""
    event, refusals = outcome.failure_event(tmp_path, *args)
    assert event is None
    assert any(fragment in r for r in refusals), refusals
    assert not (tmp_path / "docs/events/failures.jsonl").exists()


# --- TC-169: the partial classification (SR-150 / LLR-175) -------------------


def branch_with_changes(tmp_path):
    """A branch touching three product directories plus a bookkeeping one — the
    2026-08-03 incident's shape, where the wanted and unwanted changes rode in
    together and nothing forced anyone to separate them."""
    root = git_repo(tmp_path)
    (root / "src").mkdir()
    (root / "src" / "keep.py").write_text("KEPT = 1\n", encoding="utf-8", newline="\n")
    _commit(root, "seed src", when=T_BASE)
    _git(root, "checkout", "-q", "-b", "wi-401")
    (root / "src" / "keep.py").write_text("KEPT = 2\n", encoding="utf-8", newline="\n")
    (root / "src" / "extra").mkdir()
    (root / "src" / "extra" / "rejected.py").write_text(
        "BAD = True\n", encoding="utf-8", newline="\n"
    )
    (root / "docs" / "notes").mkdir(parents=True)
    (root / "docs" / "notes" / "half-done.md").write_text(
        "# half\n", encoding="utf-8", newline="\n"
    )
    write_spec(root, "partial", "WI-401", deliverable="Reached AC-1 only.")
    _commit(root, "the work so far", when=T_CODE)
    _git(root, "checkout", "-q", "main")
    return root


def test_tc169_an_unclassified_group_is_refused_by_name(tmp_path):
    """SR-150's whole point. The refusal has to NAME the group, because "this
    branch is unclassified" is not something an adjudicator can act on, and a
    green merge over an unnamed remainder is the incident being re-run."""
    root = branch_with_changes(tmp_path)
    groups, refusals = outcome.classify_groups(
        root, "wi-401", {"src": "keep", "src/extra": "discard"}
    )
    assert sorted(groups) == ["docs/notes", "src", "src/extra"]
    assert len(refusals) == 1
    assert "docs/notes" in refusals[0] and "keep/discard/quarantine" in refusals[0]


def test_tc169_a_fully_classified_branch_is_accepted(tmp_path):
    """The other direction, which matters just as much: a classification that
    covers every group must pass cleanly, or the rung is a wall rather than a
    gate."""
    root = branch_with_changes(tmp_path)
    _groups, refusals = outcome.classify_groups(
        root,
        "wi-401",
        {"src": "keep", "src/extra": "quarantine", "docs/notes": "discard"},
    )
    assert refusals == []


def test_tc169_bookkeeping_is_not_a_change_group_anyone_classifies(tmp_path):
    """The spec move and the log fragments ARE the record being kept. Asking an
    adjudicator to label them would invite a `discard` that reverts the
    classification itself."""
    root = branch_with_changes(tmp_path)
    groups, _refusals = outcome.classify_groups(root, "wi-401", {})
    assert not any(g.startswith("docs/work") for g in groups), groups


def test_tc169_a_label_for_a_group_the_branch_does_not_have_is_refused(tmp_path):
    """A stale classification is a ruling about a different diff. Accepting it
    would let a branch change after adjudication and merge on the old verdict."""
    root = branch_with_changes(tmp_path)
    _groups, refusals = outcome.classify_groups(
        root,
        "wi-401",
        {
            "src": "keep",
            "src/extra": "discard",
            "docs/notes": "keep",
            "src/gone": "discard",
        },
    )
    assert len(refusals) == 1 and "src/gone" in refusals[0]


def test_tc169_an_unknown_label_is_refused_rather_than_treated_as_keep(tmp_path):
    """Fail closed. A typo that read as `keep` would land rejected code exactly
    the way the incident did."""
    root = branch_with_changes(tmp_path)
    _groups, refusals = outcome.classify_groups(
        root,
        "wi-401",
        {"src": "revert", "src/extra": "discard", "docs/notes": "keep"},
    )
    assert len(refusals) == 1 and "'revert'" in refusals[0]


def test_tc169_a_truncated_name_status_stream_refuses_instead_of_classifying(tmp_path):
    """`handback.diff_records`' lesson, re-proven on this copy: a stream ending
    mid-record is a SHORT READ, not an empty diff. Classifying a partial file
    list would rule on some of the branch and leave the rest unruled."""
    assert outcome.diff_records(["R100", "old.py"]) is None
    assert outcome.diff_records(["M", "a.py", "R100", "old.py", "new.py"]) == [
        ("M", ["a.py"]),
        ("R100", ["old.py", "new.py"]),
    ]


def test_tc169_each_label_has_the_effect_it_names(tmp_path):
    """The three enactment permutations, driven on what the tree looks like
    afterwards rather than on what the function returned:

      keep       the change is still there;
      discard    no code is left behind;
      quarantine the code is reverted AND its diff survives as a `.patch`, which
                 is bar-inert by its extension — the RULED red arm, per group.
    """
    root = branch_with_changes(tmp_path)
    base = _git(root, "merge-base", "wi-401", "main").strip()
    groups, refusals = outcome.classify_groups(
        root,
        "wi-401",
        {"src": "keep", "src/extra": "quarantine", "docs/notes": "discard"},
        base=base,
    )
    assert refusals == []

    _git(root, "checkout", "-q", "wi-401")
    actions, refusals = outcome.apply_classification(
        root,
        base,
        "wi-401",
        groups,
        {"src": "keep", "src/extra": "quarantine", "docs/notes": "discard"},
    )
    assert refusals == []
    assert actions["src"] == "keep"
    assert actions["docs/notes"] == "discard"
    assert actions["src/extra"].startswith("quarantine:")

    # keep — the branch's edit stands.
    assert (root / "src" / "keep.py").read_text(encoding="utf-8") == "KEPT = 2\n"
    # discard — nothing left behind.
    assert not (root / "docs" / "notes" / "half-done.md").exists()
    # quarantine — the code is gone, the record is not, and the record is inert.
    assert not (root / "src" / "extra" / "rejected.py").exists()
    patch = root / actions["src/extra"].split(":", 1)[1]
    assert patch.is_file() and patch.suffix == ".patch"
    assert "BAD = True" in patch.read_text(encoding="utf-8")


def test_tc169_two_groups_whose_names_slug_alike_keep_two_records(tmp_path):
    """`group_key` is a posix DIRECTORY, so a group legitimately contains `/` —
    and the patch name folded `/`, space, `+` and every non-ASCII character to
    `-`. `src/a/b` and `src-a-b` therefore named ONE file, and the second write
    overwrote the first: two `quarantine` labels, two reverts, and one record on
    disk. Quarantine exists to keep the record, so losing one silently is the
    label doing the opposite of what it says.

    Hyphenated path segments are not exotic — 75 of this repo's 106 tracked
    directories carry one."""
    root = git_repo(tmp_path)
    _git(root, "checkout", "-q", "-b", "wi-401")
    nested = root / "src" / "a" / "b"
    flat = root / "src-a-b"
    nested.mkdir(parents=True)
    flat.mkdir()
    (nested / "nested.txt").write_text("NESTED\n", encoding="utf-8", newline="\n")
    (flat / "flat.txt").write_text("FLAT\n", encoding="utf-8", newline="\n")
    _commit(root, "two groups that slug alike", when=T_CODE)

    base = _git(root, "merge-base", "wi-401", "main").strip()
    labels = {"src/a/b": "quarantine", "src-a-b": "quarantine"}
    groups, refusals = outcome.classify_groups(root, "wi-401", labels, base=base)
    assert refusals == [] and sorted(groups) == ["src-a-b", "src/a/b"]

    actions, refusals = outcome.apply_classification(
        root, base, "wi-401", groups, labels
    )
    assert refusals == []
    one = root / actions["src/a/b"].split(":", 1)[1]
    two = root / actions["src-a-b"].split(":", 1)[1]
    assert one != two
    assert "NESTED" in one.read_text(encoding="utf-8")
    assert "FLAT" in two.read_text(encoding="utf-8")


def test_tc169_the_enactment_refuses_a_group_that_reached_it_unlabelled(tmp_path):
    """`classify_groups` is what proves a classification COMPLETE; the enactment
    refuses rather than defaulting, so a caller that skipped the proof cannot
    quietly get keep-everything."""
    root = branch_with_changes(tmp_path)
    base = _git(root, "merge-base", "wi-401", "main").strip()
    groups, _ = outcome.classify_groups(root, "wi-401", {}, base=base)
    _git(root, "checkout", "-q", "wi-401")
    actions, refusals = outcome.apply_classification(
        root, base, "wi-401", groups, {"src": "keep"}
    )
    assert actions == {"src": "keep"}
    assert len(refusals) == 2
    assert all("reached the enactment unlabelled" in r for r in refusals)


# --- TC-167: the claim-time record and the terminal comparison (LLR-173) -----


def _close_to(root, branch, directory, name="WI-401-widget.md", new_text=None):
    """The worker's terminal move, performed the way the ritual performs it —
    `spec_move.move_spec`, so the spec's own links really are rebased and the
    freeze is compared against what an honest close produces, not against a
    bare `git mv` that leaves the body untouched."""
    spec_move = load_script("spec_move")
    _git(root, "checkout", "-q", branch)
    _touched, refusal = spec_move.move_spec(
        root,
        "docs/work/active/{}/{}".format(branch, name),
        "docs/work/{}/{}".format(directory, name),
        new_text=new_text,
    )
    assert refusal is None, refusal
    _commit(root, "close: WI-401 -> {}".format(directory), when=T_LATER)
    _git(root, "checkout", "-q", "main")


def test_tc167_a_byte_identical_terminal_move_is_accepted(tmp_path):
    """The claim records each spec's frozen digest in the claim commit; the
    WHOLE close ritual — the link-aware move, the `## Deliverable` rule R-A
    requires, and the `SpecRef` clearing rule R-F requires — must clear the
    rung. A freeze that refused the ritual the rest of the kit mandates would be
    turned off within a week."""
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    claimed = (root / "docs/work/active/wi-401/WI-401-widget.md").read_text(
        encoding="utf-8"
    )
    _close_to(
        root,
        "wi-401",
        "complete",
        new_text=claimed.replace('specref = "seed.txt"\n', "")
        + "\n## Deliverable\n\nShipped the widget.\n",
    )

    specs = integ._claimed_specs(root, "wi-401")
    assert integ._scope_at_claim(root, "wi-401", specs) is None


def test_tc167_a_repointed_specref_is_refused_where_a_cleared_one_is_not(tmp_path):
    """The other half of the R-F reconciliation, driven end to end: the close
    may RETIRE the acceptance pointer and may not SWAP it. Without this, a
    branch could point its own acceptance document at whatever it happened to
    build and merge on it."""
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    claimed = (root / "docs/work/active/wi-401/WI-401-widget.md").read_text(
        encoding="utf-8"
    )
    _close_to(
        root,
        "wi-401",
        "complete",
        new_text=claimed.replace('specref = "seed.txt"', 'specref = "docs/stack.ini"')
        + "\n## Deliverable\n\nShipped something else.\n",
    )

    specs = integ._claimed_specs(root, "wi-401")
    refusal = integ._scope_at_claim(root, "wi-401", specs)
    assert refusal is not None and "front:specref" in refusal


def test_tc167_a_close_that_empties_its_specref_clears_the_merge_ladder(tmp_path):
    """The same R-F clearing in its other legal spelling, driven on the live
    ladder rather than on `scope_change` alone — because the refusal a branch
    actually hits is `_scope_at_claim`'s, and no earlier rung reads `specref`."""
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    claimed = (root / "docs/work/active/wi-401/WI-401-widget.md").read_text(
        encoding="utf-8"
    )
    _close_to(
        root,
        "wi-401",
        "complete",
        new_text=claimed.replace('specref = "seed.txt"', 'specref = ""')
        + "\n## Deliverable\n\nShipped the widget.\n",
    )

    specs = integ._claimed_specs(root, "wi-401")
    assert integ._scope_at_claim(root, "wi-401", specs) is None


def test_tc167_a_terminal_move_that_edited_the_scope_is_refused_by_region(tmp_path):
    """The permutation the requirement exists for: a branch narrowing its own
    obligation. The refusal must name the REGION, because "the scope changed"
    sends a reviewer to diff a whole file while `front:sr_refs` sends them to
    the line."""
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    claimed = (root / "docs/work/active/wi-401/WI-401-widget.md").read_text(
        encoding="utf-8"
    )
    _close_to(
        root,
        "wi-401",
        "complete",
        new_text=claimed.replace('sr_refs = ["SR-001"]', "sr_refs = []")
        + "\n## Deliverable\n\nShipped what was left.\n",
    )

    specs = integ._claimed_specs(root, "wi-401")
    refusal = integ._scope_at_claim(root, "wi-401", specs)
    assert refusal is not None
    assert "FROZEN scope" in refusal and "front:sr_refs" in refusal
    assert "WI-401" in refusal


def test_tc167_the_claim_commit_carries_the_record_the_comparison_reads(tmp_path):
    """LLR-173's record half, asserted on the artifact rather than inferred from
    the behaviour: the digest is in the claim commit, it is the digest of the
    spec AS CLAIMED (post-move, because the move rebases links), and it is
    re-derivable by anyone holding that blob."""
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    message = _git(root, "log", "-1", "--format=%B", "wi-401")
    claimed = (root / "docs/work/active/wi-401/WI-401-widget.md").read_text(
        encoding="utf-8"
    )
    assert "Scope-At-Claim: WI-401={}".format(outcome.scope_digest(claimed)) in message


def test_tc167_a_partial_close_goes_through_the_same_freeze(tmp_path):
    """`partial/` is a declared outcome directory, so an attempt that stopped is
    held to the same freeze as one that shipped — which is what stops "we only
    got this far" from being written as "this is all it ever asked for"."""
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    claimed = (root / "docs/work/active/wi-401/WI-401-widget.md").read_text(
        encoding="utf-8"
    )
    _close_to(
        root,
        "wi-401",
        "partial",
        new_text=claimed.replace("Widget", "Half a widget")
        + "\n## Deliverable\n\nReached AC-1 only.\n",
    )

    specs = integ._claimed_specs(root, "wi-401")
    refusal = integ._scope_at_claim(root, "wi-401", specs)
    assert refusal is not None and "front:title" in refusal


def _pre_record_claim(root, branch="wi-401", name="WI-401-widget.md"):
    """The claim a PRE-RECORD integrator produced, built by hand: the queued spec
    moved into `active/<branch>/` on TRUNK by a commit whose message carries no
    `Scope-At-Claim:` trailer, with the branch cut from it.

    By hand because `integrate.claim` cannot produce this shape any more, and
    that is precisely the point — the migration allowance covers claims this code
    never wrote. Amending a REAL claim commit is not a stand-in for it: that
    leaves a record on trunk, which is the attack below, not the migration."""
    src = (root / "docs/work/queued" / name).relative_to(root).as_posix()
    dest = (root / "docs/work/active" / branch / name).relative_to(root).as_posix()
    (root / "docs/work/active" / branch).mkdir(parents=True, exist_ok=True)
    _git(root, "mv", src, dest)
    _commit(root, "claim: WI-401 -> active/{} (old form)".format(branch), when=T_CODE)
    _git(root, "branch", branch)


def test_tc167_a_claim_with_no_recorded_scope_stands_the_rung_down(tmp_path):
    """The migration allowance, stated as a test so its narrowness is pinned: a
    branch claimed before this record existed has nothing to compare against,
    and hanging it would break the property every outcome depends on — every
    lane ends in a merge. The allowance can only weaken the rung to yesterday's
    behaviour; it can never accept a change that WAS recorded."""
    root = claim_repo(tmp_path)
    _pre_record_claim(root)
    _close_to(
        root, "wi-401", "complete", new_text='+++\nid = "WI-401"\ntitle = "X"\n+++\n'
    )

    specs = integ._claimed_specs(root, "wi-401")
    assert integ._scope_at_claim(root, "wi-401", specs) is None


@pytest.mark.parametrize("attack", ["amend", "delete-and-re-add"])
def test_tc167_a_branch_may_not_stand_the_freeze_down_by_losing_its_own_record(
    tmp_path, attack
):
    """SR-148's freeze may not be stood down by the branch it constrains.

    Both attacks reach the migration allowance the same way — make
    `_claim_commit` resolve to a commit with no trailer — and they differ only in
    how. `amend` rewrites the branch's copy of the claim commit (trunk keeps the
    original); `delete-and-re-add` leaves the original standing as the branch's
    own ancestor and puts a newer adder in front of it. Either way the branch
    then narrows `sr_refs`, which the control tests above prove is refused when
    the record is intact.

    "No record" therefore has to mean "no record was ever written", not "the
    commit this branch presents does not carry one" — the second is a fact the
    branch authors, and a freeze whose stand-down the constrained party can
    author is not a freeze."""
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    rel = "docs/work/active/wi-401/WI-401-widget.md"
    _git(root, "checkout", "-q", "wi-401")
    claimed = (root / rel).read_text(encoding="utf-8")
    if attack == "amend":
        _git(
            root,
            "commit",
            "-q",
            "--amend",
            "--no-edit",
            "-m",
            integ._claim_subject("WI-401", "wi-401"),
        )
    else:
        _git(root, "rm", "-q", rel)
        _commit(root, "wip: park the spec", when=T_CODE)
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(claimed, encoding="utf-8", newline="\n")
        _commit(root, "wip: restore the spec", when=T_CODE)
    _git(root, "checkout", "-q", "main")
    _close_to(
        root,
        "wi-401",
        "complete",
        new_text=claimed.replace('sr_refs = ["SR-001"]', "sr_refs = []")
        + "\n## Deliverable\n\nShipped what was left.\n",
    )

    specs = integ._claimed_specs(root, "wi-401")
    refusal = integ._scope_at_claim(root, "wi-401", specs)
    assert refusal is not None, attack
    assert "scope record" in refusal and "SR-148" in refusal
