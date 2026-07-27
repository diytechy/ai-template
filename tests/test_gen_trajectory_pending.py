"""The pending-owner-actions projection (WI-234), as DERIVED (WI-322).

`gen_trajectory.pending_block` is a pure projection of DURABLE state — never the
out/dispatch journal cache (§11):

  (a) `blocked` WI rows carrying a BlockRef (the attestation/ratification page),
      with the `git show <train>:<path>` read path when the doc lives only on a
      train branch (the WI-229 shape);
  (b) source-conflict records under refs/llm/conflict/* (WI-232): train + paths;
  (c) quarantined trains (a reservation whose train branch is missing / whose
      metadata is unreadable), re-derived from the durable refs;
  (d) the run-state `ask:` line when docs/run-state reads NEEDS-HUMAN.

Each regression builds a temp git repo and asserts on the DERIVATION: the line
appears, its pointer is right, and resolving the state drops it.

WI-322 retired the markdown surface this used to splice into, so twelve tests
whose subject WAS the splice (marker pairs, CRLF round-trip, the hand-authored
region staying byte-untouched, the freshness compare and its machine-local mask)
went with the code they guarded — porting them would have guarded nothing. Their
live successors are in `tests/test_gen_open_items.py`, against the generated
view: the mask, the staleness bite, and the vacuous-non-adopter posture.
"""

import subprocess

from conftest import ROOT, SCRIPTS, load_script, run_py

_dispatch = load_script("agent_loop").agent_dispatch


class _Journal:
    """A minimal stand-in for the dispatch journal: records .event() calls."""

    def __init__(self):
        self.events = []

    def event(self, name, **kw):
        self.events.append((name, kw))


WI_HEADER = (
    "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable,"
    "SpecRef,BuildTier,SafetyClass,BlockRef\n"
)

# Hand-authored briefs + the generated marker block, mirroring the shipped
# OPEN_ITEMS.template.md tail. The intro + OI-1 above the marker must never be
# rewritten by regeneration.
HAND = (
    "# Open items — owner decision briefs\n\n"
    "Hand-authored intro paragraph — this text MUST stay byte-identical.\n\n"
    "## OI-1 — a real pending decision\n\n"
    "- **One-line:** rule the thing.\n"
    "- **Recommendation:** do it soon.\n"
)
OPEN_ITEMS = (
    HAND + "\n---\n\n"
    "<!-- Generated pending-owner-actions projection (WI-234) — do NOT hand-edit. -->\n\n"
    "## Pending owner actions (generated)\n\n"
    "<!-- BEGIN GENERATED PENDING -->\n"
    "placeholder — to be regenerated\n"
    "<!-- END GENERATED PENDING -->\n"
)

BEGIN = "<!-- BEGIN GENERATED PENDING -->"
END = "<!-- END GENERATED PENDING -->"


def _git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def _init(repo, wis_body="WI-001,Seed,scripts,,,done,seeded,,,,\n"):
    (repo / "docs" / "requirements").mkdir(parents=True)
    (repo / "docs" / "requirements" / "work-items.csv").write_text(
        WI_HEADER + wis_body, encoding="utf-8"
    )
    (repo / "docs" / "requirements" / "open-items.csv").write_text(
        OPEN_ITEMS, encoding="utf-8"
    )
    _git(repo, "init")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")


def _block(repo):
    """The derivation itself. Asserting on `pending_block` rather than on a
    rendered file keeps these regressions about WHAT IS PENDING — the question
    they were written to answer — independent of whichever surface renders it."""
    return load_script("gen_trajectory").pending_block(repo)


def _commit_tree_ref(repo, ref, message):
    """Create `ref` pointing at an off-history commit whose message is `message`
    (the reservation/conflict record shape record_conflict/reserve_traincar use)."""
    tree = _git(repo, "rev-parse", "HEAD^{tree}").stdout.strip()
    sha = _git(repo, "commit-tree", tree, "-p", "HEAD", "-m", message).stdout.strip()
    _git(repo, "update-ref", ref, sha)
    return sha


# --- (a) blocked row with a BlockRef on a train branch -------------------------


def test_blocked_row_projects_with_train_read_path(tmp_path):
    # A blocked WI whose BlockRef doc lives ONLY on a train branch projects one
    # line carrying the `git show <train>:<path>` read path.
    _init(
        tmp_path,
        "WI-001,Seed,scripts,,,done,seeded,,,,\n"
        "WI-050,Split,requirements,,,blocked,,,,high-risk,docs/ratify/WI-050.md\n",
    )
    # Freeze the ratify doc on a train branch; it is ABSENT from the dev tree.
    train = "llm/train/p0-g3-WI-050-abcd"
    _git(tmp_path, "checkout", "-q", "-b", train)
    (tmp_path / "docs" / "ratify").mkdir()
    (tmp_path / "docs" / "ratify" / "WI-050.md").write_text(
        "frozen plan\n", encoding="utf-8"
    )
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "freeze plan")
    _git(tmp_path, "checkout", "-q", "master")
    # (git's default branch may be master or main; normalize.)
    if _git(tmp_path, "rev-parse", "--verify", "master").returncode != 0:
        _git(tmp_path, "checkout", "-q", "main")

    body = _block(tmp_path)
    assert "WI-050" in body
    assert "git show {}:docs/ratify/WI-050.md".format(train) in body

    # Resolving (unblock the row) drops the line on the next regeneration.
    wi = tmp_path / "docs" / "requirements" / "work-items.csv"
    wi.write_text(
        wi.read_text(encoding="utf-8").replace(
            ",blocked,,,,high-risk,docs/ratify/WI-050.md", ",done,delivered,,,,"
        ),
        encoding="utf-8",
    )
    assert "WI-050" not in _block(tmp_path)


def test_blocked_row_with_dev_tree_doc_cites_the_plain_path(tmp_path):
    # When the BlockRef doc IS present in the dev tree, cite the plain path (no
    # git-show read path needed).
    _init(
        tmp_path,
        "WI-001,Seed,scripts,,,done,seeded,,,,\n"
        "WI-051,Split,requirements,,,blocked,,,,high-risk,docs/ratify/WI-051.md\n",
    )
    (tmp_path / "docs" / "ratify").mkdir()
    (tmp_path / "docs" / "ratify" / "WI-051.md").write_text("plan\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "plan on dev")
    body = _block(tmp_path)
    assert "`docs/ratify/WI-051.md`" in body
    assert "git show" not in body


# --- (b) source-conflict records under refs/llm/conflict/* ---------------------


def test_conflict_record_projects_train_and_paths(tmp_path):
    _init(tmp_path)
    _commit_tree_ref(
        tmp_path,
        "refs/llm/conflict/p0-g3-WI-060-c0de",
        '{"train": "p0-g3-WI-060-c0de", "tip": "x", "ihead": "y", '
        '"paths": "src/a.py, docs/b.md"}',
    )
    body = _block(tmp_path)
    assert "p0-g3-WI-060-c0de" in body
    assert "src/a.py, docs/b.md" in body
    assert "Source conflict" in body

    # Clearing the conflict record drops the line.
    _git(tmp_path, "update-ref", "-d", "refs/llm/conflict/p0-g3-WI-060-c0de")
    assert "p0-g3-WI-060-c0de" not in _block(tmp_path)


# --- (c) quarantined trains ----------------------------------------------------


def test_quarantined_train_projects_reason(tmp_path):
    # A reservation whose train branch is MISSING is quarantined
    # (reservation-without-branch), re-derived from the durable refs.
    _init(tmp_path)
    _commit_tree_ref(
        tmp_path,
        "refs/llm/reservations/WI-070",
        '{"train": "p0-g3-WI-070-9999", "wis": ["WI-070"], "base": "deadbeef"}',
    )
    body = _block(tmp_path)
    assert "p0-g3-WI-070-9999" in body
    assert "WI-070" in body
    assert "Quarantined" in body

    # Retiring the train (delete the reservation) drops the line.
    _git(tmp_path, "update-ref", "-d", "refs/llm/reservations/WI-070")
    assert "p0-g3-WI-070-9999" not in _block(tmp_path)


def test_readable_reservation_with_branch_is_not_quarantined(tmp_path):
    # A well-formed reservation whose train branch EXISTS is in-flight, not a
    # pending owner action — it must NOT project.
    _init(tmp_path)
    train = "p0-g3-WI-071-1111"
    _git(tmp_path, "branch", "llm/train/" + train)
    _commit_tree_ref(
        tmp_path,
        "refs/llm/reservations/WI-071",
        '{{"train": "{}", "wis": ["WI-071"], "base": "x"}}'.format(train),
    )
    assert "WI-071" not in _block(tmp_path)


# --- (d) the run-state NEEDS-HUMAN ask -----------------------------------------


def test_needs_human_runstate_ask_projects(tmp_path):
    _init(tmp_path)
    (tmp_path / "docs" / "run-state").write_text(
        "NEEDS-HUMAN\nask: attest the frozen plan on the train\n", encoding="utf-8"
    )
    body = _block(tmp_path)
    assert "NEEDS-HUMAN" in body
    assert "attest the frozen plan on the train" in body


def test_running_runstate_does_not_project(tmp_path):
    _init(tmp_path)
    (tmp_path / "docs" / "run-state").write_text("RUNNING\n", encoding="utf-8")
    body = _block(tmp_path)
    assert "None — no durable owner action is pending" in body


# --- (e) Draft / Modified spine rows (WI-316) ----------------------------------

BOM = bytes([0xEF, 0xBB, 0xBF])
SR_HEADER = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status,Phase,Area\n"
)


def _write_srs(repo, body):
    (repo / "docs" / "requirements" / "system-requirements.csv").write_text(
        SR_HEADER + body, encoding="utf-8"
    )


def test_modified_sr_projects_reattest_owed_with_brief_pointer(tmp_path):
    # A Modified SR (post-attestation amendment) projects one pure-region line:
    # re-attest owed, both flips named, pointing at the before/after brief. The
    # -000 example row is inert, exactly like every other projection source.
    _init(tmp_path)
    _write_srs(
        tmp_path,
        'SR-000,EXAMPLE,,"r","x","a",,C,Test,Modified,1,\n'
        'SR-004,Gate derivation,SN-001,"r","x","a",,C,Test,Modified,2,\n',
    )
    body = _block(tmp_path)
    assert "SR-004" in body and "re-attest owed" in body
    assert "Gate derivation" in body and "phase 2" in body
    assert "--ratify modified" in body
    assert "`Modified`→`Verified`" in body and "`Planned`" in body
    assert "SR-000" not in body  # the example row never projects
    # The line sits in the PURE region (above the machine-local label), so the
    # freshness gate byte-compares it.
    assert body.index("SR-004") < body.index("Machine-local advisory")


def test_draft_sr_projects_ratification_owed(tmp_path):
    # A Draft SR projects a ratification-owed line pointing at the per-SR
    # hierarchy brief — Draft rows never surfaced in open-items before WI-316.
    _init(tmp_path)
    _write_srs(tmp_path, 'SR-007,New need,SN-001,"r","x","a",,C,Test,Draft,3,\n')
    body = _block(tmp_path)
    assert "SR-007" in body and "ratification owed" in body
    assert "--ratify SR-007" in body


def test_bommed_registry_still_projects(tmp_path):
    # Adversarial-review F4: a BOM'd SR registry (the realistic Excel
    # round-trip) glued the BOM to the SR-ID header and silently hid every
    # Draft/Modified line — the projection read "None pending" while a
    # re-attest was owed. read_rows now reads utf-8-sig.
    _init(tmp_path)
    body = SR_HEADER + 'SR-004,Gate derivation,SN-001,"r","x","a",,C,Test,Modified,2,'
    (tmp_path / "docs" / "requirements" / "system-requirements.csv").write_bytes(
        BOM + (body + chr(10)).encode("utf-8")
    )
    assert "SR-004" in _block(tmp_path)


def test_verified_sr_does_not_project_and_flip_drops_the_line(tmp_path):
    # A Verified SR projects nothing; flipping Modified->Verified (the re-attest)
    # drops the line on the next regeneration — the projection is stateless.
    _init(tmp_path)
    _write_srs(
        tmp_path, 'SR-004,Gate derivation,SN-001,"r","x","a",,C,Test,Modified,2,\n'
    )
    assert "SR-004" in _block(tmp_path)
    _write_srs(
        tmp_path, 'SR-004,Gate derivation,SN-001,"r","x","a",,C,Test,Verified,2,\n'
    )
    body = _block(tmp_path)
    assert "SR-004" not in body
    assert "None — no durable owner action is pending" in body


def test_dispatcher_regenerates_pending_at_terminal(tmp_path):
    # _regenerate_pending (called after run-state is written at the terminal
    # decision) refreshes the projection, capturing the NEEDS-HUMAN ask.
    _init(tmp_path)
    (tmp_path / "docs" / "run-state").write_text(
        "NEEDS-HUMAN\nask: attest the plan\n", encoding="utf-8"
    )
    journal = _Journal()
    _dispatch._regenerate_pending(tmp_path, journal)
    body = _block(tmp_path)
    assert "attest the plan" in body
    assert not any(name == "pending-regen-failed" for name, _ in journal.events)


def test_dispatcher_regenerate_pending_is_vacuous_without_surface(tmp_path):
    # A non-adopter (no docs/open-items.md) is a silent no-op — the terminal
    # path never crashes and journals nothing.
    (tmp_path / "docs").mkdir(parents=True)
    journal = _Journal()
    _dispatch._regenerate_pending(tmp_path, journal)
    assert journal.events == []


# --- (a′) the stranded-train attestation shape (WI-229; the review CRITICAL) ---


def _freeze_on_train(repo, wi, train, base_sha):
    """Freeze a ratify doc on a fresh train branch with a blank-line-separated
    `Blocked-WI:` trailer block — the exact WI-229 `9fed833` shape git's own
    trailer parser drops (so the line-regex read is what surfaces it). Leaves the
    checkout back on the default branch."""
    default = _git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    _git(repo, "checkout", "-q", "-b", "llm/train/" + train)
    (repo / "docs" / "ratify").mkdir(exist_ok=True)
    (repo / "docs" / "ratify" / (wi + ".md")).write_text(
        "**State:** AWAITING OWNER ATTESTATION\n", encoding="utf-8"
    )
    _git(repo, "add", "-A")
    body = (
        "{0}: freeze the migration plan\n\n"
        "Blocked-WI: {0}\n\n"
        "BlockRef: docs/ratify/{0}.md#owner-attestation-hard-stop\n\n"
        "Train: {1}\n\nBase: {2}\n"
    ).format(wi, train, base_sha)
    _git(repo, "commit", "-q", "-m", body)
    _git(repo, "checkout", "-q", default)


def test_stranded_train_attestation_projects_with_read_path(tmp_path):
    # A reserved WI whose row is still QUEUED (never marked blocked) but whose
    # train carries a Blocked-WI trailer + a frozen ratify doc must project one
    # attestation line with the `git show <train>:<path>` read path. This is the
    # WI-229 shape the review's CRITICAL flagged.
    _init(
        tmp_path,
        "WI-001,Seed,scripts,,,done,seeded,,,,\n"
        "WI-080,Migrate,requirements,,,queued,,,,high-risk,\n",
    )
    base = _git(tmp_path, "rev-parse", "HEAD").stdout.strip()
    train = "p0-g3-WI-080-abcd"
    _freeze_on_train(tmp_path, "WI-080", train, base)
    _commit_tree_ref(
        tmp_path,
        "refs/llm/reservations/WI-080",
        '{{"train": "{}", "wis": ["WI-080"], "base": "{}"}}'.format(train, base),
    )
    body = _block(tmp_path)
    assert "WI-080" in body
    assert "awaiting owner attestation" in body.lower()
    assert "git show llm/train/{}:docs/ratify/WI-080.md".format(train) in body

    # Resolve: the trailer WI's registry row flips to done -> the line drops.
    wi = tmp_path / "docs" / "requirements" / "work-items.csv"
    wi.write_text(
        wi.read_text(encoding="utf-8").replace(
            "WI-080,Migrate,requirements,,,queued,,,,high-risk,",
            "WI-080,Migrate,requirements,,,done,migrated,,,,",
        ),
        encoding="utf-8",
    )
    assert "WI-080" not in _block(tmp_path)


def test_stranded_not_double_listed_when_row_is_also_blocked(tmp_path):
    # A WI whose row IS blocked-with-BlockRef and whose train also carries the
    # trailer projects exactly once (source (a) wins; (a′) dedupes on the id).
    _init(
        tmp_path,
        "WI-001,Seed,scripts,,,done,seeded,,,,\n"
        "WI-081,Migrate,requirements,,,blocked,,,,high-risk,docs/ratify/WI-081.md\n",
    )
    base = _git(tmp_path, "rev-parse", "HEAD").stdout.strip()
    train = "p0-g3-WI-081-abcd"
    _freeze_on_train(tmp_path, "WI-081", train, base)
    _commit_tree_ref(
        tmp_path,
        "refs/llm/reservations/WI-081",
        '{{"train": "{}", "wis": ["WI-081"], "base": "{}"}}'.format(train, base),
    )
    # Exactly one listing line for the id (the `- **WI-081**` bullet prefix); the
    # id also recurs inside that line's train/path pointer, so count the prefix.
    assert _block(tmp_path).count("**WI-081**") == 1


# --- (b) unreadable conflict record -------------------------------------------


def test_unreadable_conflict_record_is_surfaced(tmp_path):
    _init(tmp_path)
    # A conflict ref pointing at a commit whose message is NOT JSON.
    _commit_tree_ref(tmp_path, "refs/llm/conflict/p0-g3-WI-090-bad", "not json at all")
    body = _block(tmp_path)
    assert "Unreadable conflict record" in body
    assert "p0-g3-WI-090-bad" in body


# --- (c) unreadable-reservation-metadata quarantine ---------------------------


def test_unreadable_reservation_metadata_projects_quarantine(tmp_path):
    _init(tmp_path)
    _commit_tree_ref(tmp_path, "refs/llm/reservations/WI-095", "totally not json")
    body = _block(tmp_path)
    assert "Quarantined reservation" in body
    assert "WI-095" in body
