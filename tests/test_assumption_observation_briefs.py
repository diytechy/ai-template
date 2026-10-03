"""Assumption-only cases remain visible at both adjudication checkpoints."""

from conftest import load_script, set_process_key

ab = load_script("adjudicate_brief")
carrier = load_script("spine_carrier")


def assumption_repo(tmp_path):
    requirements = tmp_path / "docs/requirements"
    requirements.mkdir(parents=True)
    (requirements / "assumptions.toml").write_text(
        '[assumption.DA-011]\nassumption = "A new reader understands the code."\n'
        'falsifier = "A reader cannot explain the code."\n'
        'status = "Approved"\nstanding = "active"\n',
        encoding="utf-8",
    )
    tests = tmp_path / "docs/test"
    tests.mkdir()
    (tests / "test-cases.toml").write_text(
        '[test.TC-279]\nassumption_refs = ["DA-011"]\n'
        'method = "Ask a new reader."\nexpected = "The reader explains it."\n'
        'max_age = 90\nautomated = "No"\nstatus = "Drafted"\n'
        'evidence = "docs/test/inspection.md"\ntier = "Release"\n',
        encoding="utf-8",
    )
    set_process_key(tmp_path, "attestation", "human_approval_through", "DevStg-Needs")
    return tmp_path


def assert_chain(text):
    assert "DA-011" in text
    assert "A new reader understands the code." in text
    assert "A reader cannot explain the code." in text
    assert "Standing**: active" in text
    assert "TC-279" in text
    assert "Ask a new reader." in text


def test_first_approval_shows_assumption_only_case(tmp_path):
    root = assumption_repo(tmp_path)
    text, reason = ab.compose(
        root,
        {"WI-ID": "WI-001", "Brief": "first-approval", "Adjudicates": "TC-279"},
        "verdict.md",
    )
    assert reason is None, reason
    assert_chain(text)
    assert "TC TC-279 [AWAITING FIRST APPROVAL]" in text
    assert "docs/test/test-cases.toml=WI-001" in text
    assert "docs/requirements/assumptions.toml=WI-001" not in text


def test_rejudge_shows_assumption_only_case(tmp_path, monkeypatch):
    root = assumption_repo(tmp_path)
    case = carrier.load(root / "docs/test/test-cases.toml", "TC-ID")[0]
    monkeypatch.setattr(ab.rejudge, "checkpoint_for", lambda *a: "release")
    monkeypatch.setattr(
        ab.rejudge, "due_cases", lambda *a, **kw: [{"tc": "TC-279", "row": case}]
    )
    monkeypatch.setattr(ab.rejudge, "explain", lambda d: "No result recorded.")
    text, reason = ab.compose(
        root,
        {"WI-ID": "WI-002", "Brief": "rejudge", "Adjudicates": "TC-279"},
        "verdict.md",
    )
    assert reason is None, reason
    assert_chain(text)
    assert "- TC-279 — observes DA-011" in text
