"""prompt_render.py — the one strict renderer over externalized prompt assets
(SR-155/SR-156/SR-157, TC-176..TC-179).

The value of moving prompt prose out of Python is only real if two things hold:
the move was FAITHFUL (the load-bearing clauses survived it), and the renderer
REFUSES a malformed brief instead of launching one. Both are tested here at
least as hard as the happy path, because both failures are silent — a launched
session answers confidently either way, and nothing downstream can tell a brief
with a hole in it from a brief without one.

TC-176 permutations: complete | unknown-slot | missing-slot | unrendered |
golden.
TC-177 permutations: permitted | prohibited-self-assessment |
prohibited-via-allowed-slot.
TC-178 permutations: repeat | edited-template.
TC-179 permutations: generated.
"""

import json
import re

import pytest
from conftest import KIT, SCRIPTS, load_script, run_py

PR = load_script("prompt_render")
CONFIG = load_script("config")

PROMPTS = KIT / "prompts"

# The seven templates this slice owns. The dual-plan trio shipped earlier and is
# deliberately not re-litigated here.
SHIPPED = (
    ("implementer", "worker.md"),
    ("reviewer", "reviewer.md"),
    ("critic", "critique.md"),
    ("adjudicate-amendment", "adjudicate-amendment.md"),
    ("adjudicate-disposition", "adjudicate-disposition.md"),
    ("adjudicate-conflict", "adjudicate-conflict.md"),
    ("adjudicate-red-test", "adjudicate-red-test.md"),
)

ADJUDICATORS = tuple(name for name, _ in SHIPPED if name.startswith("adjudicate-"))

FIXTURE_TEMPLATE = """<!-- ============================================================
DISPATCHER NOTES (delete this block before sending the prompt)

A fixture template. Slots: {{ALPHA}} = the first value; {{BETA}} = the second.
============================================================ -->

Alpha is {{ALPHA}}.

Beta is {{BETA}}.
"""

# What the fixture must render to, byte for byte, forever.
GOLDEN = "Alpha is one.\n\nBeta is two.\n"

CONFIG_TEXT = """schema = 1

[prompts.implementer]
template = "prompts/fixture.md"
required_slots = ["ALPHA"]
output_schema = "worker-v1"

[prompts.reviewer]
template = "prompts/fixture.md"
required_slots = ["ALPHA", "BETA"]
allowed_sources = ["registry", "diff"]
prohibited_sources = ["self-assessment"]
output_schema = "review-v1"
"""


def make_repo(tmp_path, config_text=CONFIG_TEXT, template=FIXTURE_TEMPLATE):
    """A repo root holding docs/config.toml and prompts/fixture.md."""
    (tmp_path / "docs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "config.toml").write_text(
        config_text, encoding="utf-8", newline="\n"
    )
    (tmp_path / "prompts").mkdir(parents=True, exist_ok=True)
    if template is not None:
        (tmp_path / "prompts" / "fixture.md").write_text(
            template, encoding="utf-8", newline="\n"
        )
    return tmp_path


def decl_for(tmp_path, job="implementer"):
    decl, findings = PR.declaration(make_repo(tmp_path), job)
    assert findings == [], findings
    return decl


def shipped_declaration(job, filename, **kw):
    """A Declaration pointing straight at a shipped kit template, so the
    as-launched assertions do not depend on a repo declaring it yet."""
    return PR.Declaration(
        job=job,
        template="project-trajectory/prompts/" + filename,
        path=PROMPTS / filename,
        required_slots=kw.get("required_slots", ()),
        allowed_sources=kw.get("allowed_sources", ()),
        prohibited_sources=kw.get("prohibited_sources", ()),
        output_schema=kw.get("output_schema", "fixture-v1"),
    )


def body_of(filename):
    text = PR.canonical_text((PROMPTS / filename).read_text(encoding="utf-8"))
    return PR.strip_dispatcher_block(text)


def notes_of(filename):
    """The dispatcher-notes block, i.e. everything the render throws away."""
    text = PR.canonical_text((PROMPTS / filename).read_text(encoding="utf-8"))
    return text[: len(text) - len(PR.strip_dispatcher_block(text))]


def normalized(text):
    """Whitespace-insensitive comparison text.

    The move re-wrapped the prose; it did not change it. Collapsing every run of
    whitespace to one space is the declared boundary of "faithful": word order,
    punctuation and wording must match, line breaks need not."""
    return " ".join(text.split())


def as_slots(constant):
    """A Python-format prompt constant with its `{name}` slots rewritten to the
    `{{NAME}}` convention, so it can be compared against the template that
    replaced it."""
    return re.sub(r"\{(\w+)\}", lambda m: "{{" + m.group(1).upper() + "}}", constant)


def keys(findings):
    return [f.key for f in findings]


def reasons(findings):
    return " ".join(f.reason for f in findings)


# --- TC-176: the strict render ------------------------------------------------
def test_complete_slot_set_renders(tmp_path):
    """complete — every slot supplied, so the render succeeds."""
    rendered, findings = PR.render(decl_for(tmp_path), {"ALPHA": "one", "BETA": "two"})
    assert findings == []
    assert rendered.text == GOLDEN


def test_render_deletes_the_dispatcher_notes_block(tmp_path):
    rendered, findings = PR.render(decl_for(tmp_path), {"ALPHA": "one", "BETA": "two"})
    assert findings == []
    assert "DISPATCHER NOTES" not in rendered.text
    assert "<!--" not in rendered.text


def test_unknown_slot_refuses_and_names_it(tmp_path):
    """unknown-slot — a key the template has no slot for."""
    rendered, findings = PR.render(
        decl_for(tmp_path), {"ALPHA": "one", "BETA": "two", "GAMMA": "three"}
    )
    assert rendered is None
    assert keys(findings) == ["implementer.GAMMA"]
    assert "is not a slot of prompts/fixture.md" in reasons(findings)


def test_missing_required_slot_refuses_and_says_it_was_required(tmp_path):
    """missing-slot — a declared required slot nobody supplied."""
    rendered, findings = PR.render(decl_for(tmp_path), {"BETA": "two"})
    assert rendered is None
    assert keys(findings) == ["implementer.ALPHA"]
    assert "REQUIRED slot" in reasons(findings)


def test_missing_optional_slot_also_refuses_as_a_hole(tmp_path):
    """A slot the declaration did not mark required is still a hole; the message
    just does not call it REQUIRED."""
    rendered, findings = PR.render(decl_for(tmp_path), {"ALPHA": "one"})
    assert rendered is None
    assert keys(findings) == ["implementer.BETA"]
    assert "declared slot" in reasons(findings)


def test_every_slot_problem_is_reported_in_one_run(tmp_path):
    """A refusal list, not a first refusal — a caller fixing a brief learns all
    of it in one pass (contracts §5)."""
    rendered, findings = PR.render(decl_for(tmp_path), {"GAMMA": "three"})
    assert rendered is None
    assert sorted(keys(findings)) == [
        "implementer.ALPHA",
        "implementer.BETA",
        "implementer.GAMMA",
    ]


def test_required_slot_absent_from_the_template_is_drift(tmp_path):
    """The declaration and the reviewed prose have moved apart — its own
    finding, because supplying the slot would not fix it."""
    config_text = CONFIG_TEXT.replace(
        'required_slots = ["ALPHA"]', 'required_slots = ["ALPHA", "OMEGA"]'
    )
    decl, _ = PR.declaration(
        make_repo(tmp_path, config_text=config_text), "implementer"
    )
    rendered, findings = PR.render(decl, {"ALPHA": "one", "BETA": "two"})
    assert rendered is None
    assert keys(findings) == ["implementer.OMEGA"]
    assert "have drifted" in reasons(findings)


def test_placeholder_carried_in_by_a_value_refuses(tmp_path):
    """unrendered — the only way a `{{...}}` reaches the output is inside a slot
    value, so the refusal names the carrier."""
    rendered, findings = PR.render(
        decl_for(tmp_path), {"ALPHA": "one", "BETA": "see {{ALPHA}}"}
    )
    assert rendered is None
    assert keys(findings) == ["implementer.ALPHA"]
    assert "survived the render, carried in by slot BETA" in reasons(findings)


def test_golden_render_is_byte_stable(tmp_path):
    """golden — the same template and the same inputs produce the same bytes,
    on any OS. A CRLF value must not change them."""
    decl = decl_for(tmp_path)
    once, _ = PR.render(decl, {"ALPHA": "one", "BETA": "two"})
    twice, _ = PR.render(decl, {"ALPHA": "one", "BETA": "two"})
    crlf, _ = PR.render(decl, {"ALPHA": "one", "BETA": "two\r\nlines"})
    lf, _ = PR.render(decl, {"ALPHA": "one", "BETA": "two\nlines"})
    assert once.text.encode("utf-8") == GOLDEN.encode("utf-8")
    assert twice.text == once.text
    assert crlf.text == lf.text


def test_a_crlf_template_renders_the_same_bytes(tmp_path):
    """The golden survives a checkout that wrote the template with CRLF."""
    root = make_repo(tmp_path)
    path = root / "prompts" / "fixture.md"
    path.write_bytes(FIXTURE_TEMPLATE.replace("\n", "\r\n").encode("utf-8"))
    decl, _ = PR.declaration(root, "implementer")
    rendered, findings = PR.render(decl, {"ALPHA": "one", "BETA": "two"})
    assert findings == []
    assert rendered.text == GOLDEN


def test_a_value_carrying_regex_escapes_survives_verbatim(tmp_path):
    """A diff or a harness log full of backslashes goes in as written — the
    trap a string `re.sub` replacement would have sprung."""
    value = r"C:\path\1 and \g<0> and \\ done"
    rendered, findings = PR.render(decl_for(tmp_path), {"ALPHA": "one", "BETA": value})
    assert findings == []
    assert value in rendered.text


def test_missing_template_file_refuses_naming_the_path(tmp_path):
    root = make_repo(tmp_path, template=None)
    decl, _ = PR.declaration(root, "implementer")
    rendered, findings = PR.render(decl, {"ALPHA": "one", "BETA": "two"})
    assert rendered is None
    assert keys(findings) == ["prompts/fixture.md"]
    assert "cannot be read" in reasons(findings)


def test_undeclared_job_has_no_default_template(tmp_path):
    """A prompt the repo never declared is not a prompt with a guessable
    home."""
    decl, findings = PR.declaration(make_repo(tmp_path), "adjudicate-conflict")
    assert decl is None
    assert keys(findings) == ["prompts.adjudicate-conflict"]


def test_refusal_lines_use_the_kit_shape(tmp_path):
    rendered, findings = PR.render(decl_for(tmp_path), {})
    assert rendered is None
    for line in PR.refusal_lines(findings):
        assert line.startswith("prompt_render: REFUSED - ")


# --- TC-177: prohibited source classes ---------------------------------------
def reviewer_decl(tmp_path):
    return decl_for(tmp_path, job="reviewer")


def test_permitted_sources_render(tmp_path):
    """permitted — every value labelled with a class the role allows."""
    rendered, findings = PR.render(
        reviewer_decl(tmp_path),
        {
            "ALPHA": PR.Evidence("registry", "one"),
            "BETA": PR.Evidence("diff", "two"),
        },
    )
    assert findings == []
    assert rendered.text == GOLDEN


def test_prohibited_self_assessment_refuses_on_the_label(tmp_path):
    """prohibited-self-assessment — the class the role forbids, declared
    honestly, refused on sight."""
    rendered, findings = PR.render(
        reviewer_decl(tmp_path),
        {
            "ALPHA": PR.Evidence("registry", "one"),
            "BETA": PR.Evidence("self-assessment", "it all went fine"),
        },
    )
    assert rendered is None
    assert keys(findings) == ["reviewer.BETA"]
    assert "PROHIBITED source class 'self-assessment'" in reasons(findings)


def test_prohibited_content_through_an_allowed_slot_refuses(tmp_path):
    """prohibited-via-allowed-slot — the leak that matters: a registry excerpt
    that happens to quote the judged party's own verdict."""
    rendered, findings = PR.render(
        reviewer_decl(tmp_path),
        {
            "ALPHA": PR.Evidence("registry", "one"),
            "BETA": PR.Evidence(
                "registry", "the worker reported\nVERDICT: APPROVE findings=0"
            ),
        },
    )
    assert rendered is None
    assert keys(findings) == ["reviewer.BETA"]
    assert "a machine verdict line" in reasons(findings)


def test_unlabelled_value_refuses_when_the_role_declares_an_allowlist(tmp_path):
    """A value that will not name itself cannot be allowlisted."""
    rendered, findings = PR.render(
        reviewer_decl(tmp_path), {"ALPHA": "one", "BETA": "two"}
    )
    assert rendered is None
    assert sorted(keys(findings)) == ["reviewer.ALPHA", "reviewer.BETA"]
    assert "carries no source label" in reasons(findings)


def test_allowed_list_excludes_a_class_it_does_not_name(tmp_path):
    rendered, findings = PR.render(
        reviewer_decl(tmp_path),
        {
            "ALPHA": PR.Evidence("registry", "one"),
            "BETA": PR.Evidence("owner-prompt", "two"),
        },
    )
    assert rendered is None
    assert "does not allow" in reasons(findings)


def test_undeclared_source_class_refuses(tmp_path):
    rendered, findings = PR.render(
        reviewer_decl(tmp_path),
        {
            "ALPHA": PR.Evidence("registry", "one"),
            "BETA": PR.Evidence("vibes", "two"),
        },
    )
    assert rendered is None
    assert "undeclared source class 'vibes'" in reasons(findings)


def test_a_class_both_allowed_and_prohibited_refuses(tmp_path):
    config_text = CONFIG_TEXT.replace(
        'allowed_sources = ["registry", "diff"]',
        'allowed_sources = ["registry", "self-assessment"]',
    )
    decl, _ = PR.declaration(make_repo(tmp_path, config_text=config_text), "reviewer")
    findings = PR.check_sources(decl, {})
    assert keys(findings) == ["prompts.reviewer"]
    assert "evidence and contraband at once" in reasons(findings)


def test_the_residue_check_tolerates_the_templates_own_prose():
    """The reviewer template CONTAINS the words it forbids — its redaction
    clause says "self-assessment" and its output contract prints a VERDICT
    line. Presence would refuse every reviewer render ever launched; only a
    count above the template's own baseline is a leak."""
    decl = shipped_declaration(
        "reviewer",
        "reviewer.md",
        required_slots=("VERDICT",),
        allowed_sources=("registry",),
        prohibited_sources=("self-assessment",),
    )
    rendered, findings = PR.render(
        decl, {"VERDICT": PR.Evidence("registry", "docs/reviews/tag/WI-1.md")}
    )
    assert findings == [], findings
    assert "self-assessment" in rendered.text
    assert "VERDICT: APPROVE|CHANGES-REQUESTED" in rendered.text


def test_the_residue_check_catches_a_marker_formed_at_the_join():
    """A value that is clean on its own and forms a marker where it meets the
    template's prose — invisible to the per-value scan, caught by the render."""
    decl = PR.Declaration(
        job="reviewer",
        template="fixture",
        path=None,
        required_slots=(),
        allowed_sources=(),
        prohibited_sources=("self-assessment",),
        output_schema="fixture-v1",
    )
    body = "VERDICT{{TAIL}}\n"
    rendered = PR.Rendered(
        job="reviewer",
        template="fixture",
        text="VERDICT: APPROVE\n",
        body=body,
        template_text=body,
    )
    findings = PR.check_sources(decl, {"TAIL": ": APPROVE"}, rendered=rendered)
    assert keys(findings) == ["prompts.reviewer"]
    assert "a machine verdict line" in reasons(findings)


def test_check_sources_runs_on_inputs_alone_without_a_render(tmp_path):
    findings = PR.check_sources(
        reviewer_decl(tmp_path), {"BETA": PR.Evidence("self-assessment", "x")}
    )
    assert keys(findings) == ["reviewer.BETA"]


# --- TC-178: provenance -------------------------------------------------------
def test_repeated_render_yields_one_prompt_hash(tmp_path):
    """repeat — two renders of one template with one input record one hash."""
    decl = decl_for(tmp_path)
    first, _ = PR.render(decl, {"ALPHA": "one", "BETA": "two"})
    second, _ = PR.render(decl, {"ALPHA": "one", "BETA": "two"})
    assert PR.provenance(first) == PR.provenance(second)
    assert PR.provenance(first).job == "implementer"
    assert PR.provenance(first).template == "prompts/fixture.md"


def test_a_different_input_changes_only_the_prompt_hash(tmp_path):
    decl = decl_for(tmp_path)
    first, _ = PR.render(decl, {"ALPHA": "one", "BETA": "two"})
    other, _ = PR.render(decl, {"ALPHA": "one", "BETA": "three"})
    assert PR.provenance(first).template_sha256 == PR.provenance(other).template_sha256
    assert PR.provenance(first).prompt_sha256 != PR.provenance(other).prompt_sha256


def test_editing_the_template_changes_the_template_hash(tmp_path):
    """edited-template — including an edit confined to the dispatcher notes,
    which are reviewed prose too."""
    root = make_repo(tmp_path)
    decl, _ = PR.declaration(root, "implementer")
    before, _ = PR.render(decl, {"ALPHA": "one", "BETA": "two"})
    (root / "prompts" / "fixture.md").write_text(
        FIXTURE_TEMPLATE.replace("A fixture template.", "A fixture template, edited."),
        encoding="utf-8",
        newline="\n",
    )
    after, _ = PR.render(decl, {"ALPHA": "one", "BETA": "two"})
    assert PR.provenance(before).template_sha256 != PR.provenance(after).template_sha256
    assert PR.provenance(before).prompt_sha256 == PR.provenance(after).prompt_sha256


def test_a_trailing_blank_line_does_not_move_a_hash(tmp_path):
    """The hashing rule: an editor's final-newline habit must not make two
    provenance records disagree for a reason no reader can see."""
    root = make_repo(tmp_path)
    decl, _ = PR.declaration(root, "implementer")
    before, _ = PR.render(decl, {"ALPHA": "one", "BETA": "two"})
    (root / "prompts" / "fixture.md").write_text(
        FIXTURE_TEMPLATE + "\n\n", encoding="utf-8", newline="\n"
    )
    after, _ = PR.render(decl, {"ALPHA": "one", "BETA": "two"})
    assert PR.provenance(before) == PR.provenance(after)


def test_provenance_is_hashes_not_prompts(tmp_path):
    decl = decl_for(tmp_path)
    rendered, _ = PR.render(decl, {"ALPHA": "one", "BETA": "two"})
    record = PR.provenance(rendered)._asdict()
    assert sorted(record) == ["job", "prompt_sha256", "template", "template_sha256"]
    assert "Alpha is one" not in json.dumps(record)


# --- TC-179: the generated catalog -------------------------------------------
def test_catalog_lists_every_declared_job_once(tmp_path):
    """generated — one row per declared prompt, carrying what the declaration
    and the file actually say."""
    root = make_repo(tmp_path)
    rows, findings = PR.catalog(root)
    assert findings == []
    assert [r.job for r in rows] == ["implementer", "reviewer"]
    reviewer = [r for r in rows if r.job == "reviewer"][0]
    assert reviewer.template == "prompts/fixture.md"
    assert reviewer.allowed == ("registry", "diff")
    assert reviewer.prohibited == ("self-assessment",)
    assert reviewer.output_schema == "review-v1"
    assert reviewer.template_sha256 == PR.sha256_of(PR.canonical_text(FIXTURE_TEMPLATE))


def test_catalog_hash_tracks_the_file(tmp_path):
    """A generated catalog cannot drift from the templates it lists."""
    root = make_repo(tmp_path)
    before, _ = PR.catalog(root)
    (root / "prompts" / "fixture.md").write_text(
        FIXTURE_TEMPLATE + "\nOne more clause.\n", encoding="utf-8", newline="\n"
    )
    after, _ = PR.catalog(root)
    assert before[0].template_sha256 != after[0].template_sha256


def test_catalog_keeps_the_row_for_a_missing_template(tmp_path):
    """The worst answer to "which prompt is broken?" is an omitted row."""
    root = make_repo(tmp_path, template=None)
    rows, findings = PR.catalog(root)
    assert [r.template_sha256 for r in rows] == [PR.MISSING_HASH, PR.MISSING_HASH]
    assert keys(findings) == ["prompts/fixture.md", "prompts/fixture.md"]


def test_catalog_table_renders_every_declared_column(tmp_path):
    rows, _ = PR.catalog(make_repo(tmp_path))
    table = PR.catalog_table(rows)
    header = table.splitlines()[0]
    for column in PR.CATALOG_COLUMNS:
        assert column in header
    assert table.count("\n") == len(rows) + 1
    assert "review-v1" in table
    assert "self-assessment" in table


def test_catalog_is_empty_without_declarations(tmp_path):
    rows, findings = PR.catalog(make_repo(tmp_path, config_text="schema = 1\n"))
    assert rows == []
    assert findings == []


# --- the move was faithful ----------------------------------------------------
# The three constants still live in agent_loop.py (the runtime cutover is a
# later slice). While both exist, the templates are pinned against them: a
# rewrite dressed as a move fails here, naming the prose that went missing.
AGENT_LOOP = load_script("agent_loop")

MOVED = (
    ("worker.md", "WORKER_PROMPT"),
    ("reviewer.md", "REVIEWER_PROMPT"),
    ("critique.md", "CRITIQUE_PROMPT"),
)


@pytest.mark.parametrize("filename,constant", MOVED)
def test_moved_template_carries_the_whole_constant(filename, constant):
    original = normalized(as_slots(getattr(AGENT_LOOP, constant)))
    assert original in normalized(body_of(filename))


REVIEWER_CLAUSES = (
    # Redaction — the reason independent review finds anything.
    "Do NOT read or trust the implementer's own session notes or "
    "self-assessment — a leaked self-assessment collapses review finding-rates "
    "several-fold.",
    # Adversarial posture.
    "Assume the implementer was careful but missed something, and hunt for it.",
    "Drive the diff's REAL shipped code paths",
    "An APPROVE must mean you tried to break it and failed",
    "believe nothing you did not observe",
    "This is an INDEPENDENT parallel review — do not debate another reviewer.",
)


@pytest.mark.parametrize("clause", REVIEWER_CLAUSES)
def test_reviewer_template_keeps_its_load_bearing_clauses(clause):
    assert normalized(clause) in normalized(body_of("reviewer.md"))


CRITIQUE_CLAUSES = (
    # The rubric anchors — what stops a critic inventing its own standard.
    "judged ONLY against the WRITTEN RUBRIC below — never a fresh opinion of "
    "your own, and never a lax test case",
    "score it against the rubric's numbered anchors",
    "each CITING a rubric anchor id (B1/G2/…)",
    "must propose it as a new `B#` anchor for the rubric (the accumulation rule)",
    # Redaction.
    "Do NOT read or trust the implementer's session notes, docs/status.md, "
    "docs/log.md, or any self-assessment",
    "you NEVER edit the spine or the artifact yourself",
)


@pytest.mark.parametrize("clause", CRITIQUE_CLAUSES)
def test_critique_template_keeps_its_load_bearing_clauses(clause):
    assert normalized(clause) in normalized(body_of("critique.md"))


WORKER_CLAUSES = (
    "this assignment is your whole scope",
    "Do not resume from docs/status.md",
    "NEVER edit root coordination truth on this branch",
    "End your FINAL commit for this WI with the trailer",
)


@pytest.mark.parametrize("clause", WORKER_CLAUSES)
def test_worker_template_keeps_its_load_bearing_clauses(clause):
    assert normalized(clause) in normalized(body_of("worker.md"))


# --- the shipped templates' shape --------------------------------------------
@pytest.mark.parametrize("job,filename", SHIPPED)
def test_shipped_template_has_a_dispatcher_block_that_is_stripped(job, filename):
    text = PR.canonical_text((PROMPTS / filename).read_text(encoding="utf-8"))
    assert text.lstrip().startswith("<!--")
    assert "DISPATCHER NOTES (delete this block before sending the prompt)" in text
    assert "<!--" not in body_of(filename)


@pytest.mark.parametrize("job,filename", SHIPPED)
def test_shipped_template_declares_every_slot_it_uses(job, filename):
    """The declared slot list is the contract an assembler reads; a slot the
    notes do not name is a slot nobody knows how to fill."""
    notes = notes_of(filename)
    for slot in sorted(PR.template_slots(body_of(filename))):
        assert "{{" + slot + "}}" in notes, slot


@pytest.mark.parametrize("job,filename", SHIPPED)
def test_shipped_template_links_the_authoring_rules(job, filename):
    assert "README.md in this directory" in normalized(notes_of(filename))


@pytest.mark.parametrize("job,filename", SHIPPED)
def test_shipped_template_body_has_no_python_format_slots(job, filename):
    """`{name}` is prose here, and the renderer will not fill it — a leftover
    from the move would ship a literal brace pair to a model."""
    assert re.search(r"(?<!\{)\{[a-z_]+\}", body_of(filename)) is None


@pytest.mark.parametrize("job,filename", SHIPPED)
def test_shipped_template_renders_with_its_slots_filled(job, filename):
    """The as-launched assertion: every shipped template fills, strips its
    notes, and holds no placeholder."""
    decl = shipped_declaration(job, filename)
    slots = {name: "(fixture)" for name in PR.template_slots(body_of(filename))}
    rendered, findings = PR.render(decl, slots)
    assert findings == [], findings
    assert "{{" not in rendered.text
    assert "DISPATCHER NOTES" not in rendered.text
    assert rendered.text.endswith("\n")


@pytest.mark.parametrize("job", ADJUDICATORS)
def test_every_adjudicator_declares_the_insufficient_evidence_verdict(job):
    """A judge that guesses when the evidence is thin is worse than one that
    stops, because nothing downstream can tell the two apart."""
    body = body_of(job + ".md")
    assert "insufficient-evidence" in body
    assert re.search(r"(?m)^VERDICT: .*insufficient-evidence", body)
    assert re.search(r"(?m)^MISSING: ", body)


@pytest.mark.parametrize("job", ADJUDICATORS)
def test_every_adjudicator_says_what_it_must_not_assume(job):
    assert "## What you must not assume" in body_of(job + ".md")


def test_the_four_adjudicators_are_genuinely_different_documents():
    """Not one template with a mode flag: different evidence, different verdict
    vocabularies, different prose."""
    bodies = {job: body_of(job + ".md") for job in ADJUDICATORS}
    verdicts = {}
    for job, body in bodies.items():
        line = re.search(r"(?m)^VERDICT: (.+)$", body).group(1)
        verdicts[job] = frozenset(line.split("|"))
    assert len(set(verdicts.values())) == len(ADJUDICATORS)
    slots = {job: PR.template_slots(body) for job, body in bodies.items()}
    assert len(set(frozenset(s) for s in slots.values())) == len(ADJUDICATORS)


def test_adjudicate_disposition_never_asks_for_the_workers_rationale():
    """SR-156, the reason this template is its own document: the brief carries
    the outcome ENUM and the record, never the defendant's account of itself."""
    body = body_of("adjudicate-disposition.md")
    assert "RATIONALE" not in PR.template_slots(body)
    assert "You have not been shown the worker's own account" in normalized(body)
    assert "the claim under judgement, not evidence for it" in normalized(body)


def test_adjudicate_disposition_declares_the_prohibition_to_its_dispatcher():
    notes = notes_of("adjudicate-disposition.md")
    assert "worker-rationale" in notes
    assert "PROHIBITED" in notes


def test_the_prompts_readme_states_the_rules_once():
    readme = (PROMPTS / "README.md").read_text(encoding="utf-8")
    for filename in [f for _, f in SHIPPED]:
        assert "(" + filename + ")" in readme
    assert "stdin" in readme
    assert "insufficient-evidence" in readme


# --- the declared source-class table -----------------------------------------
def test_every_declared_source_class_has_a_description():
    for cls in PR.SOURCE_CLASSES:
        assert cls.what.strip()
        assert cls.name == cls.name.lower()


def test_the_prohibitable_classes_carry_content_markers():
    """Label discipline is the primary control; markers are the backstop, and
    the classes a judging role actually forbids must have them."""
    marked = {c.name for c in PR.SOURCE_CLASSES if c.markers}
    assert {"self-assessment", "worker-rationale", "rival-plan"} <= marked


def test_worker_rationale_markers_catch_a_serialized_outcome_event():
    decl = PR.Declaration(
        job="adjudicate-disposition",
        template="fixture",
        path=None,
        required_slots=(),
        allowed_sources=(),
        prohibited_sources=("worker-rationale",),
        output_schema="fixture-v1",
    )
    event = json.dumps({"kind": "outcome", "rationale": "I ran out of time"})
    findings = PR.check_sources(decl, {"BRANCH_COMMITS": event})
    assert keys(findings) == ["adjudicate-disposition.BRANCH_COMMITS"]
    assert "serialized rationale field" in reasons(findings)


# --- the CLI ------------------------------------------------------------------
def test_cli_render_writes_the_prompt_to_stdout(tmp_path, capsys):
    """Prompts travel on stdin: the command writes the prompt to stdout for the
    caller to pipe, and the slots arrive in a FILE, never in argv."""
    root = make_repo(tmp_path)
    slots = tmp_path / "slots.json"
    slots.write_text(
        json.dumps({"ALPHA": "one", "BETA": "two"}), encoding="utf-8", newline="\n"
    )
    code = PR.main(
        [
            "--root",
            str(root),
            "render",
            "--job",
            "implementer",
            "--slots",
            str(slots),
        ]
    )
    out = capsys.readouterr()
    assert code == 0
    assert out.out == GOLDEN
    assert out.err == ""


def test_cli_render_accepts_labelled_evidence_from_the_slots_file(tmp_path, capsys):
    root = make_repo(tmp_path)
    slots = tmp_path / "slots.json"
    slots.write_text(
        json.dumps(
            {
                "ALPHA": {"source": "registry", "text": "one"},
                "BETA": {"source": "self-assessment", "text": "two"},
            }
        ),
        encoding="utf-8",
        newline="\n",
    )
    code = PR.main(
        ["--root", str(root), "render", "--job", "reviewer", "--slots", str(slots)]
    )
    out = capsys.readouterr()
    assert code == 1
    assert out.out == ""
    assert "prompt_render: REFUSED - reviewer.BETA" in out.err


def test_cli_catalog_prints_the_generated_table(tmp_path, capsys):
    code = PR.main(["--root", str(make_repo(tmp_path)), "catalog"])
    out = capsys.readouterr()
    assert code == 0
    assert "| Job | Template |" in out.out
    assert "implementer" in out.out


def test_cli_check_passes_on_a_coherent_declaration(tmp_path, capsys):
    code = PR.main(["--root", str(make_repo(tmp_path)), "check"])
    out = capsys.readouterr()
    assert code == 0
    assert "prompt_render: OK, 2 declared prompt(s)" in out.out


def test_cli_check_reports_a_missing_template(tmp_path, capsys):
    code = PR.main(["--root", str(make_repo(tmp_path, template=None)), "check"])
    out = capsys.readouterr()
    assert code == 1
    assert "prompt_render: REFUSED - prompts/fixture.md" in out.err


def test_cli_with_no_subcommand_prints_help(capsys):
    assert PR.main([]) == 2
    assert "usage" in capsys.readouterr().out


# --- the documented usage is RUN, not just written ----------------------------
# A Usage block is a claim about the CLI, and an unrun claim rots: both scripts
# below documented `--root` AFTER the subcommand while their parsers register it
# as a global option, so every documented invocation died with
# `error: unrecognized arguments: --root .` and exit 2. Nothing caught it because
# nothing ever ran the docstring.
#
# `schedule.py` rides along here rather than in a suite of its own: it carries
# the identical defect in the identical shape, and this is the only module that
# drives a documented Usage block at all.
USAGE_SCRIPTS = ("prompt_render.py", "schedule.py")

# Docstring shorthand -> a real argument. `[optional]` brackets are documentation,
# not shell syntax, so the drive keeps what is inside them: the optional part is
# exactly where the ordering defect lived.
USAGE_TOKENS = {"JOB": "implementer", "N": "1", "text|json": "text"}


def documented_invocations(script):
    """Every `python scripts/<name>.py ...` line of a script's module docstring."""
    doc = load_script(script[: -len(".py")]).__doc__ or ""
    return [
        line.strip()
        for line in doc.splitlines()
        if line.strip().startswith("python scripts/" + script)
    ]


def usage_argv(line, root, slots):
    argv = []
    for token in line.split("#", 1)[0].replace("[", "").replace("]", "").split()[2:]:
        if token == ".":
            argv.append(str(root))
        elif token == "FILE":
            argv.append(str(slots))
        else:
            argv.append(USAGE_TOKENS.get(token, token))
    return argv


@pytest.mark.parametrize("script", USAGE_SCRIPTS)
def test_every_documented_invocation_is_accepted_by_the_parser(script, tmp_path):
    """Run what the docstring says to run.

    The bar is deliberately the PARSER's verdict, not the command's: an empty
    registry or a missing declaration is a legitimate non-zero answer, while
    `unrecognized arguments` means the documented form cannot be typed at all.
    """
    root = make_repo(tmp_path)
    slots = tmp_path / "slots.json"
    slots.write_text(
        json.dumps({"ALPHA": "one", "BETA": "two"}), encoding="utf-8", newline="\n"
    )
    lines = documented_invocations(script)
    assert lines, "{} documents no invocation to check".format(script)
    for line in lines:
        proc = run_py([SCRIPTS / script] + usage_argv(line, root, slots), cwd=root)
        output = proc.stdout + proc.stderr
        assert "unrecognized arguments" not in output, (line, output)
        assert proc.returncode != 2, (line, output)


# --- the config seam ----------------------------------------------------------
def test_the_declared_prompt_vocabulary_is_the_configs(tmp_path):
    """Eleven declared prompts: the six jobs, the four adjudicator briefs, and
    `dual-plan-critic` (contracts §1). This module never invents a twelfth.

    The eleventh is not a flourish. The kit ships TWO critic templates —
    `critique.md` (the artifact critique loop) and `dual-plan-critic.template.md`
    (the planning hat) — and with one `critic` slot between them, whichever
    template lost the slot was undeclared: nothing could render it and
    `prompt_render check` could not see it existed.
    """
    assert len(CONFIG.PROMPTS) == 11
    for job in ADJUDICATORS:
        assert job in CONFIG.PROMPTS
    assert "dual-plan-critic" in CONFIG.PROMPTS


def test_declarations_surface_a_broken_config(tmp_path):
    root = make_repo(tmp_path, config_text="schema = 1\n[prompts.nobody]\n")
    decls, findings = PR.declarations(root)
    assert decls == {}
    assert keys(findings) == ["prompts.nobody"]
