"""TC-156 / TC-161 — the human-ratification boundary PROJECTION (SR-142/SR-144).

`tests/test_attest.py` proves the routing predicate: `requires_human(tier,
boundary)` answers one cell. This module proves the other half of those two
requirements — what an owner SEES and what therefore BLOCKS:

  * the sixteen cells (four boundary values x four spine tiers) are driven end
    to end, from `docs/config.toml` through `attest.ratification_projection` to
    the pill printed on `docs/open-items.html`, and the view is asserted to
    agree with the router cell by cell rather than with a table copied here;
  * the out-of-range value renders NO matrix. The schema default it falls back
    to is not what the adopter wrote, and a printed matrix is read as the
    configured one — so a silently-defaulted table is worse than a blank;
  * a full-spine review request survives a real PROCESS RESTART (recorded by one
    interpreter, read by another), shows its reason and its asker on the
    generated surface, blocks the declared checkpoint, and closes only through a
    recorded human decision event;
  * an input that could not be read never renders the word that means "go" —
    a corrupted ledger reads NOT CERTIFIED and exits non-zero, not "clear".

The refusals are driven as hard as the happy path, because every one of them is
a place where this surface could tell a human the wrong thing about what they
personally owe.
"""

import json
import re

import pytest
from conftest import SCRIPTS, load_script, run_py

ATTEST = load_script("attest")
GI = load_script("gen_open_items")

# The inclusive table of decisions §1, written out rather than computed: a
# generated expectation would agree with a generated implementation for the
# wrong reason. 0 = SN only ... 3 = the whole spine.
BOUNDARY_TABLE = {
    0: ("human", "adjudicator", "adjudicator", "adjudicator"),
    1: ("human", "human", "adjudicator", "adjudicator"),
    2: ("human", "human", "human", "adjudicator"),
    3: ("human", "human", "human", "human"),
}
TIERS = ("SN", "SR", "LLR", "TC")

SR_HEADER = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,"
    "Priority,Verification,Status,Phase,Workstream\n"
)
LLR_HEADER = (
    "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status,Component,Phase\n"
)
TC_HEADER = (
    "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,"
    "Status,Phase\n"
)
OI_HEADER = (
    "OI-ID,Title,Status,Raised,OneLine,Decision,BlastRadius,Options,"
    "Recommendation,WI-Refs,RuledDate,RulingRef\n"
)

# Deliberately VERIFIED rows: this suite is about the boundary card, and a
# Draft/Modified row would send `trace.reattest_model` into git archaeology that
# proves nothing here (test_gen_open_items.py owns that half).
SR_ROW = (
    "SR-001,Addition,SN-001,shall add two numbers,because,criteria,,M,Test,"
    "Verified,1,core\n"
)
LLR_ROW = "LLR-001,SR-001,Pure adder,src/demo,add,two numbers -> sum,(see TC),Implemented,CMP-001,1\n"
TC_ROW = (
    'TC-001,SR-001;LLR-001,Unit,"call add",Smoke,"a=1; b=2","the sum",Yes,'
    "tests/test_demo.py,Verified,1\n"
)
SN_MD = """# Stakeholder Needs

| SN-ID | Need (plain language) | Why it matters | Priority | Acceptance intent |
|---|---|---|---|---|
| SN-001 | A team can add two numbers. | It is the demo need. | M | add(1,2) gives 3. |
"""


def write_config(root, boundary=None, policy=None, schema=1):
    """A `docs/config.toml` declaring only the attestation dials under test.

    Written as TEXT rather than through the loader: the point of the sweep is
    that the value an adopter typed reaches the pill, so the fixture must start
    where the adopter does."""
    lines = ["schema = {}".format(schema), "", "[attestation]"]
    if boundary is not None:
        lines.append("human_ratification_through = {}".format(boundary))
    if policy is not None:
        lines.append('final_full_spine_review = "{}"'.format(policy))
    (root / "docs" / "config.toml").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
    )


def repo(tmp_path, boundary=None, policy=None, oi_rows="", schema=1):
    """A minimal repo carrying exactly what the owner surface reads."""
    docs = tmp_path / "docs"
    (docs / "requirements").mkdir(parents=True, exist_ok=True)
    (docs / "test").mkdir(parents=True, exist_ok=True)
    (docs / "requirements" / "stakeholder-needs.md").write_text(
        SN_MD, encoding="utf-8", newline="\n"
    )
    (docs / "requirements" / "system-requirements.csv").write_text(
        SR_HEADER + SR_ROW, encoding="utf-8", newline="\n"
    )
    (docs / "requirements" / "low-level-requirements.csv").write_text(
        LLR_HEADER + LLR_ROW, encoding="utf-8", newline="\n"
    )
    (docs / "test" / "test-cases.csv").write_text(
        TC_HEADER + TC_ROW, encoding="utf-8", newline="\n"
    )
    (docs / "requirements" / "open-items.csv").write_text(
        OI_HEADER + oi_rows, encoding="utf-8", newline="\n"
    )
    if boundary is not None or policy is not None or schema != 1:
        write_config(tmp_path, boundary, policy, schema)
    return tmp_path


# The tier rows of the rendered card. Anchored on the exact emitted markup so a
# card that stopped emitting the pill fails here rather than passing on a
# substring that happens to survive elsewhere on the page.
TIER_ROW_RE = re.compile(
    r'<span class="rid">(SN|SR|LLR|TC)</span>'
    r'<span class="pill(?: ratify)?">'
    r"(human ratification required|an adjudicator may enact)</span>"
    r'<span class="hint">([^<]*)</span>'
)
DECIDER = {
    "human ratification required": "human",
    "an adjudicator may enact": "adjudicator",
}


def rendered(root):
    return GI.render(root)


def tier_pills(page):
    """`{tier: decider}` as the generated view actually states it."""
    return {tier: DECIDER[label] for tier, label, _hint in TIER_ROW_RE.findall(page)}


def tier_hints(page):
    return {tier: hint for tier, _label, hint in TIER_ROW_RE.findall(page)}


def attest_cli(root, *args):
    """One `attest.py` run as its OWN process — the restart proof needs a fresh
    interpreter holding no state from the run that wrote the event."""
    return run_py([SCRIPTS / "attest.py", "--root", str(root), *args], cwd=root)


def record_request(root, reason="pre-release full-spine review", by="owner"):
    proc = attest_cli(root, "--request", reason, "--by", by)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    match = re.search(r"recorded review request ([0-9a-f]{16})", proc.stdout)
    assert match, proc.stdout
    return match.group(1)


# --- TC-156: the boundary matrix, driven end to end --------------------------
# Parameters: boundary 0 | 1 | 2 | 3 | out-of-range
@pytest.mark.parametrize("boundary", sorted(BOUNDARY_TABLE))
def test_each_boundary_projects_the_declared_matrix(tmp_path, boundary):
    root = repo(tmp_path, boundary=boundary)
    projection = ATTEST.ratification_projection(root)
    assert projection["findings"] == []
    assert projection["boundary"] == boundary
    assert [e["tier"] for e in projection["tiers"]] == list(TIERS)
    assert tuple(e["decider"] for e in projection["tiers"]) == BOUNDARY_TABLE[boundary]


@pytest.mark.parametrize("boundary", sorted(BOUNDARY_TABLE))
def test_the_matrix_is_built_on_the_router_never_beside_it(tmp_path, boundary):
    # The sixteen cells again, but asserted against `requires_human` itself:
    # a projection carrying its own copy of the table could drift from the
    # predicate a caller actually routes with, and nobody would see it.
    root = repo(tmp_path, boundary=boundary)
    for entry in ATTEST.ratification_projection(root)["tiers"]:
        assert entry["requires_human"] is ATTEST.requires_human(
            entry["index"], boundary
        ), entry


@pytest.mark.parametrize("boundary", sorted(BOUNDARY_TABLE))
def test_the_generated_view_states_the_same_matrix(tmp_path, boundary):
    # The projection half of SR-142: what an OWNER sees. A boundary the router
    # honours but the surface renders differently is the failure this closes.
    root = repo(tmp_path, boundary=boundary)
    pills = tier_pills(rendered(root))
    assert pills == dict(zip(TIERS, BOUNDARY_TABLE[boundary]))
    assert "attestation.human_ratification_through" in rendered(root)


def test_an_absent_config_projects_the_schema_default(tmp_path):
    # Absent is not a finding — it is the declared default, and the surface must
    # say which number it is rather than leaving the band blank.
    root = repo(tmp_path)
    projection = ATTEST.ratification_projection(root)
    assert projection["findings"] == []
    assert projection["boundary"] == ATTEST.DEFAULT_BOUNDARY
    assert projection["policy"] == ATTEST.DEFAULT_FINAL_REVIEW
    assert tier_pills(rendered(root)) == dict(
        zip(TIERS, BOUNDARY_TABLE[ATTEST.DEFAULT_BOUNDARY])
    )


@pytest.mark.parametrize("boundary", [4, -1, 99])
def test_an_out_of_range_boundary_refuses_and_renders_no_matrix(tmp_path, boundary):
    # The out-of-range permutation. The loader resolves a refused key to the
    # schema DEFAULT, so the danger is not a crash — it is a plausible-looking
    # table that is not the one the adopter declared.
    root = repo(tmp_path, boundary=boundary)
    projection = ATTEST.ratification_projection(root)
    assert projection["boundary"] is None
    assert projection["tiers"] == []
    assert any(
        "attestation.human_ratification_through" in f for f in projection["findings"]
    ), projection["findings"]
    page = rendered(root)
    assert "REFUSED" in page and "not shown" in page
    assert tier_pills(page) == {}, "a refused dial must not render a matrix"


def test_an_unsupported_schema_refuses_the_whole_document(tmp_path):
    # A document-level finding makes every resolved value a default standing in
    # for text nobody could read, so the dials go with it.
    root = repo(tmp_path, boundary=2, schema=99)
    projection = ATTEST.ratification_projection(root)
    assert projection["boundary"] is None
    assert any("schema" in f for f in projection["findings"]), projection["findings"]


def test_a_finding_on_an_unrelated_dial_does_not_refuse_the_matrix(tmp_path):
    # The negative half: scoping the refusal list is what keeps the one line
    # that changes what a human owes from being buried under the whole config
    # report, which `config_query` already prints.
    root = repo(tmp_path, boundary=2)
    (root / "docs" / "config.toml").write_text(
        "schema = 1\n\n[attestation]\nhuman_ratification_through = 2\n\n"
        "[policy]\npush = 'nobody'\n",
        encoding="utf-8",
        newline="\n",
    )
    projection = ATTEST.ratification_projection(root)
    assert projection["findings"] == []
    assert projection["boundary"] == 2


@pytest.mark.parametrize("boundary", [-1, 4, "1", None, True, 1.0])
def test_tier_routing_refuses_an_out_of_range_boundary_by_name(boundary):
    with pytest.raises(ValueError) as exc:
        ATTEST.tier_routing(boundary)
    assert "REFUSED" in str(exc.value)
    assert "human ratification boundary" in str(exc.value)
    assert repr(boundary) in str(exc.value)


def test_the_tier_rows_count_the_rows_actually_waiting(tmp_path):
    # "Which tiers owe a human ratification" is only actionable with a queue
    # length beside it: a tier routed to the human with nothing waiting owes
    # nothing today.
    root = repo(tmp_path, boundary=3)
    assert tier_hints(rendered(root))["SR"] == "1 row(s) awaiting a decision"
    ATTEST.seed(root, root / "docs", by="test")
    assert tier_hints(rendered(root))["SR"] == "0 row(s) awaiting a decision"
    (root / "docs" / "requirements" / "system-requirements.csv").write_text(
        SR_HEADER + SR_ROW.replace("two numbers", "three numbers"),
        encoding="utf-8",
        newline="\n",
    )
    projection = ATTEST.ratification_projection(root)
    assert {e["tier"]: e["pending"] for e in projection["tiers"]} == {
        "SN": 0,
        "SR": 1,
        "LLR": 0,
        "TC": 0,
    }


def test_the_cli_boundary_arm_prints_every_tier(tmp_path):
    root = repo(tmp_path, boundary=2)
    proc = attest_cli(root, "--boundary")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    for tier, decider in zip(TIERS, BOUNDARY_TABLE[2]):
        assert "attest: {} ".format(tier) in proc.stdout
        assert "-> {} -".format(decider) in proc.stdout
    assert proc.stdout.count("-> human -") == 3
    assert proc.stdout.count("-> adjudicator -") == 1


def test_the_cli_boundary_arm_refuses_an_out_of_range_dial(tmp_path):
    root = repo(tmp_path, boundary=4)
    proc = attest_cli(root, "--boundary")
    assert proc.returncode == 1, proc.stdout
    assert "REFUSED" in proc.stderr
    assert "human_ratification_through" in proc.stderr
    assert "-> human" not in proc.stdout, "no table may be printed for a refused dial"


# --- TC-161: the durable final-review request --------------------------------
# Parameters: recorded | after-restart | closed | persistent-policy
def test_a_recorded_request_is_on_disk_as_one_event(tmp_path):
    root = repo(tmp_path)
    request_id = record_request(root, "release 2.0 sweep")
    lines = (
        (root / "docs" / "events" / "review-requests.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    )
    assert len(lines) == 1
    event = json.loads(lines[0])
    assert event["kind"] == "review-request" and event["id"] == request_id
    assert event["reason"] == "release 2.0 sweep" and event["by"] == "owner"


def test_the_request_survives_a_real_process_restart(tmp_path):
    # The whole of SR-144: the process that recorded the ask is GONE. A fresh
    # interpreter replays the ledger and reaches the same answer, which is
    # exactly the moment an in-memory or launcher-flag ask would have vanished.
    root = repo(tmp_path)
    request_id = record_request(root)
    listing = attest_cli(root, "--open")
    assert listing.returncode == 0, listing.stdout + listing.stderr
    assert request_id in listing.stdout and "owner" in listing.stdout


def test_an_open_request_blocks_the_declared_checkpoint(tmp_path):
    root = repo(tmp_path)
    assert attest_cli(root, "--checkpoint").returncode == 0
    request_id = record_request(root, "the ask that must not be walked past")
    blocked = attest_cli(root, "--checkpoint")
    assert blocked.returncode == 1, blocked.stdout
    assert "CHECKPOINT BLOCKED" in blocked.stdout
    assert request_id in blocked.stdout
    assert "walked past" in blocked.stdout


def test_the_request_appears_in_the_owner_view_with_its_reason_and_asker(tmp_path):
    root = repo(tmp_path)
    request_id = record_request(root, "the auditor asked for a full read", by="ada")
    page = rendered(root)
    assert request_id in page
    assert "the auditor asked for a full read" in page
    assert "ada" in page
    assert "BLOCKED" in page
    assert "No open full-spine review request" not in page


def test_only_a_recorded_human_decision_closes_it(tmp_path):
    root = repo(tmp_path)
    request_id = record_request(root)
    # An unattributed close is refused: only a recorded HUMAN decision closes a
    # request, and a decision with no `by` records nobody.
    unattributed = attest_cli(root, "--decide", request_id)
    assert unattributed.returncode == 1
    assert "--by" in unattributed.stderr
    assert attest_cli(root, "--checkpoint").returncode == 1, "still open"

    closed = attest_cli(root, "--decide", request_id, "--by", "owner")
    assert closed.returncode == 0, closed.stdout + closed.stderr
    clear = attest_cli(root, "--checkpoint")
    assert clear.returncode == 0, clear.stdout
    assert "checkpoint clear" in clear.stdout
    page = rendered(root)
    assert "No open full-spine review request" in page
    assert "BLOCKED" not in page
    # Closing is an APPEND, never an edit: both events are still on disk.
    assert (
        len(
            (root / "docs" / "events" / "review-requests.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        )
        == 2
    )


def test_the_persistent_policy_blocks_without_any_request_event(tmp_path):
    root = repo(tmp_path, policy="always")
    assert ATTEST.review_requests(root) == []
    blocked = attest_cli(root, "--checkpoint")
    assert blocked.returncode == 1, blocked.stdout
    assert "final_full_spine_review=always" in blocked.stdout
    page = rendered(root)
    assert "BLOCKED" in page and "final_full_spine_review=always" in page


def test_the_never_policy_leaves_the_checkpoint_clear(tmp_path):
    # The negative half of the dial: a policy that blocks unconditionally would
    # make the whole checkpoint meaningless.
    root = repo(tmp_path, policy="never")
    clear = attest_cli(root, "--checkpoint")
    assert clear.returncode == 0, clear.stdout
    assert "final_full_spine_review=never" in rendered(root)


def test_a_request_still_blocks_under_the_never_policy(tmp_path):
    # The two sources are INDEPENDENT: a one-shot ask must not be silenced by
    # the persistent policy it exists to override.
    root = repo(tmp_path, policy="never")
    record_request(root, "more often than the policy asks")
    assert attest_cli(root, "--checkpoint").returncode == 1


# --- the fail-closed direction ------------------------------------------------
def test_a_corrupted_ledger_is_never_reported_as_a_clear_checkpoint(tmp_path):
    root = repo(tmp_path)
    record_request(root)
    ledger = root / "docs" / "events" / "review-requests.jsonl"
    ledger.write_text(
        ledger.read_text(encoding="utf-8").replace('"reason"', '"resaon"'),
        encoding="utf-8",
        newline="\n",
    )
    projection = ATTEST.ratification_projection(root)
    assert projection["findings"], "a ledger that will not read must be a finding"
    assert projection["block"] is None, "the block reason is unknown, not absent"
    page = rendered(root)
    assert "NOT CERTIFIED" in page
    assert "checkpoint clear" not in page
    refused = attest_cli(root, "--checkpoint")
    assert refused.returncode == 1, refused.stdout
    assert "REFUSED" in refused.stderr


def test_an_empty_tree_projects_the_default_rather_than_a_refusal(tmp_path):
    # Absent is not a finding — a repo that has adopted neither the config nor
    # the ledger still gets an answer, which is what makes the kit a no-op until
    # an adopter has an opinion.
    projection = GI.boundary_projection(tmp_path / "nowhere")
    assert projection["boundary"] == ATTEST.DEFAULT_BOUNDARY
    assert projection["findings"] == [] and projection["requests"] == []


def test_the_card_renders_every_finding_and_never_certifies(tmp_path):
    # The degrade path the generator owns: the page still renders, and it says
    # WHY the band is thin instead of dropping it silently.
    card = GI._boundary_card(
        {
            "boundary": None,
            "policy": None,
            "tiers": [],
            "requests": [],
            "block": None,
            "findings": ["the ledger is unreadable", "and a second problem"],
        }
    )
    assert card.count("REFUSED") == 2, "every finding renders, never just the first"
    assert "the ledger is unreadable" in card and "a second problem" in card
    assert "NOT CERTIFIED" in card


def test_registry_prose_is_escaped_on_the_boundary_card(tmp_path):
    # A reason string is arbitrary human text landing on the one document a
    # human rules from; an unescaped tag would eat the rest of the card.
    root = repo(tmp_path)
    record_request(root, "<script>alert(1)</script> please review")
    page = rendered(root)
    assert "<script>alert(1)</script>" not in page
    assert "&lt;script&gt;" in page


def test_the_added_band_keeps_the_view_freshness_gated(tmp_path):
    # The property the module already had and this slice must not break: the
    # render is a pure function of the committed tree, and the stamped
    # attestation baseline still rides on the output.
    root = repo(tmp_path)
    record_request(root)
    assert GI.render(root) == GI.render(root)
    proc = run_py([SCRIPTS / "gen_open_items.py", "--root", str(root)], cwd=root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    check = run_py(
        [SCRIPTS / "gen_open_items.py", "--root", str(root), "--check"], cwd=root
    )
    assert check.returncode == 0, check.stdout + check.stderr
    assert GI.BASELINE_RE.search(GI.read_view(root / "docs" / "open-items.html"))
