"""gen_trajectory.py --status pending-owner-actions projection (WI-234).

The generated `<!-- BEGIN GENERATED PENDING -->` block in docs/open-items.md is a
pure projection of DURABLE state — never the out/dispatch journal cache (§11):

  (a) `blocked` WI rows carrying a BlockRef (the attestation/ratification page),
      with the `git show <train>:<path>` read path when the doc lives only on a
      train branch (the WI-229 shape);
  (b) source-conflict records under refs/llm/conflict/* (WI-232): train + paths;
  (c) quarantined trains (a reservation whose train branch is missing / whose
      metadata is unreadable), re-derived from the durable refs;
  (d) the run-state `ask:` line when docs/run-state reads NEEDS-HUMAN.

Each regression drives the real script over a temp git repo, proving the line
appears, its pointer is right, resolving the state drops it, the freshness
`--check` fails on a hand-staled block, and the hand-authored briefs above the
markers stay byte-untouched.
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
    (repo / "docs" / "open-items.md").write_text(OPEN_ITEMS, encoding="utf-8")
    _git(repo, "init")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")


def _gen(repo, *args):
    return run_py(
        [SCRIPTS / "gen_trajectory.py", "--root", repo, "--status", *args], cwd=repo
    )


def _block(repo):
    text = (repo / "docs" / "open-items.md").read_text(encoding="utf-8")
    return text.split(BEGIN, 1)[1].split(END, 1)[0]


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

    assert _gen(tmp_path).returncode == 0
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
    assert _gen(tmp_path).returncode == 0
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
    assert _gen(tmp_path).returncode == 0
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
    assert _gen(tmp_path).returncode == 0
    body = _block(tmp_path)
    assert "p0-g3-WI-060-c0de" in body
    assert "src/a.py, docs/b.md" in body
    assert "Source conflict" in body

    # Clearing the conflict record drops the line.
    _git(tmp_path, "update-ref", "-d", "refs/llm/conflict/p0-g3-WI-060-c0de")
    assert _gen(tmp_path).returncode == 0
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
    assert _gen(tmp_path).returncode == 0
    body = _block(tmp_path)
    assert "p0-g3-WI-070-9999" in body
    assert "WI-070" in body
    assert "Quarantined" in body

    # Retiring the train (delete the reservation) drops the line.
    _git(tmp_path, "update-ref", "-d", "refs/llm/reservations/WI-070")
    assert _gen(tmp_path).returncode == 0
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
    assert _gen(tmp_path).returncode == 0
    assert "WI-071" not in _block(tmp_path)


# --- (d) the run-state NEEDS-HUMAN ask -----------------------------------------


def test_needs_human_runstate_ask_projects(tmp_path):
    _init(tmp_path)
    (tmp_path / "docs" / "run-state").write_text(
        "NEEDS-HUMAN\nask: attest the frozen plan on the train\n", encoding="utf-8"
    )
    assert _gen(tmp_path).returncode == 0
    body = _block(tmp_path)
    assert "NEEDS-HUMAN" in body
    assert "attest the frozen plan on the train" in body


def test_running_runstate_does_not_project(tmp_path):
    _init(tmp_path)
    (tmp_path / "docs" / "run-state").write_text("RUNNING\n", encoding="utf-8")
    assert _gen(tmp_path).returncode == 0
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
    assert _gen(tmp_path).returncode == 0
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
    assert _gen(tmp_path).returncode == 0
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
    assert _gen(tmp_path).returncode == 0
    assert "SR-004" in _block(tmp_path)


def test_verified_sr_does_not_project_and_flip_drops_the_line(tmp_path):
    # A Verified SR projects nothing; flipping Modified->Verified (the re-attest)
    # drops the line on the next regeneration — the projection is stateless.
    _init(tmp_path)
    _write_srs(
        tmp_path, 'SR-004,Gate derivation,SN-001,"r","x","a",,C,Test,Modified,2,\n'
    )
    assert _gen(tmp_path).returncode == 0
    assert "SR-004" in _block(tmp_path)
    _write_srs(
        tmp_path, 'SR-004,Gate derivation,SN-001,"r","x","a",,C,Test,Verified,2,\n'
    )
    assert _gen(tmp_path).returncode == 0
    body = _block(tmp_path)
    assert "SR-004" not in body
    assert "None — no durable owner action is pending" in body


# --- freshness + byte-untouched hand-authored region ---------------------------


def test_check_fails_on_a_hand_staled_block(tmp_path):
    _init(tmp_path)
    assert _gen(tmp_path).returncode == 0
    assert _gen(tmp_path, "--check").returncode == 0  # fresh after regen
    # Hand-stale the generated block.
    oi = tmp_path / "docs" / "open-items.md"
    text = oi.read_text(encoding="utf-8")
    staled = text.replace(
        "None — no durable owner action is pending",
        "None — no durable owner action is pending. HAND EDIT",
    )
    assert staled != text
    oi.write_text(staled, encoding="utf-8")
    stale = _gen(tmp_path, "--check")
    assert stale.returncode == 1
    assert "STALE" in stale.stderr


# --- M-10 / WI-266: the freshness gate is a PURE function of the committed tree -


def test_check_ignores_machine_local_ref_drift(tmp_path):
    # M-10/WI-266: refs/llm/* don't transport with clone/push, so a committed
    # open-items.md generated on the dispatch machine carries machine-local
    # advisory lines (conflicts / reservations / quarantines) that a second clone
    # (CI, another machine) cannot reproduce. The --status --check freshness gate
    # must NOT read STALE on that difference alone — only the committed-tree-pure
    # region is gated. (Pre-change, the whole-block byte-compare fails here.)
    _init(tmp_path)
    # Generate WITH a source-conflict ref present — the dispatch machine.
    _commit_tree_ref(
        tmp_path,
        "refs/llm/conflict/p0-g3-WI-060-c0de",
        '{"train": "p0-g3-WI-060-c0de", "tip": "x", "ihead": "y", "paths": "src/a.py"}',
    )
    assert _gen(tmp_path).returncode == 0
    assert "Source conflict" in _block(tmp_path)  # advisory line generated
    assert _gen(tmp_path, "--check").returncode == 0  # fresh on this machine
    # Simulate a second clone: the machine-local ref is GONE, but the committed
    # file still carries the advisory line. Regeneration now omits it — yet the
    # gate must still pass, because that line is excluded from the byte-compare.
    _git(tmp_path, "update-ref", "-d", "refs/llm/conflict/p0-g3-WI-060-c0de")
    assert "Source conflict" in _block(tmp_path)  # committed line untouched
    check = _gen(tmp_path, "--check")
    assert check.returncode == 0, check.stdout + check.stderr


def test_check_fails_on_pure_drift_even_with_machine_local_advisory(tmp_path):
    # The gate still bites the committed-tree-pure region: a hand-edited blocked
    # row (source (a), pure) fails --check even while a machine-local advisory
    # line is present in the same block.
    _init(
        tmp_path,
        "WI-001,Seed,scripts,,,done,seeded,,,,\n"
        "WI-051,Split,requirements,,,blocked,,,,high-risk,docs/ratify/WI-051.md\n",
    )
    (tmp_path / "docs" / "ratify").mkdir()
    (tmp_path / "docs" / "ratify" / "WI-051.md").write_text("plan\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "plan")
    _commit_tree_ref(
        tmp_path,
        "refs/llm/conflict/p0-g3-WI-060-c0de",
        '{"train": "p0-g3-WI-060-c0de", "paths": "src/a.py"}',
    )
    assert _gen(tmp_path).returncode == 0
    assert "Source conflict" in _block(tmp_path)  # advisory present
    assert _gen(tmp_path, "--check").returncode == 0
    # Hand-edit the PURE blocked-row line -> must go STALE.
    oi = tmp_path / "docs" / "open-items.md"
    text = oi.read_text(encoding="utf-8")
    staled = text.replace("attest/ratify", "attest/ratify NOW — HAND EDIT")
    assert staled != text
    oi.write_text(staled, encoding="utf-8")
    stale = _gen(tmp_path, "--check")
    assert stale.returncode == 1
    assert "STALE" in stale.stderr


def test_check_fails_when_the_machine_local_label_drifts(tmp_path):
    # The advisory LABEL is committed-tree-pure (a constant string sitting at the
    # mask boundary, inclusive): hand-editing it must fail --check, so the
    # exclusion stays VISIBLE and cannot be silently deleted or reworded.
    _init(tmp_path)
    assert _gen(tmp_path).returncode == 0
    assert _gen(tmp_path, "--check").returncode == 0
    oi = tmp_path / "docs" / "open-items.md"
    text = oi.read_text(encoding="utf-8")
    assert "Machine-local advisory" in text  # the label is present + gated
    staled = text.replace(
        "Machine-local advisory", "Machine-local advisory (HAND EDIT)"
    )
    assert staled != text
    oi.write_text(staled, encoding="utf-8")
    stale = _gen(tmp_path, "--check")
    assert stale.returncode == 1
    assert "STALE" in stale.stderr


def test_stray_label_above_the_block_cannot_disable_the_pure_gate(tmp_path):
    # A hand-authored line byte-identical to PENDING_LOCAL_LABEL, planted ABOVE
    # the BEGIN marker, must NOT become the mask boundary — else it would split
    # the compare early, drop the ENTIRE committed-tree-pure region, and let a
    # genuine pure-line drift slip through as fresh (a silent gate disable). The
    # mask boundary is anchored WITHIN PENDING_BEGIN..PENDING_END. (Pre-fix
    # whole-document scan: rc 0; anchored: rc 1.)
    label = load_script("gen_trajectory").PENDING_LOCAL_LABEL
    _init(tmp_path)
    assert _gen(tmp_path).returncode == 0
    assert _gen(tmp_path, "--check").returncode == 0
    oi = tmp_path / "docs" / "open-items.md"
    text = oi.read_text(encoding="utf-8")
    # (1) plant the stray label in the hand region above the block (identical in
    #     current and updated, so not itself a drift), and (2) drift a PURE line.
    poisoned = text.replace(BEGIN, label + "\n\n" + BEGIN, 1).replace(
        "None — no durable owner action is pending",
        "None — no durable owner action is pending. PURE DRIFT",
    )
    assert poisoned != text
    assert label in poisoned.split(BEGIN, 1)[0]  # stray label sits ABOVE BEGIN
    oi.write_text(poisoned, encoding="utf-8")
    stale = _gen(tmp_path, "--check")
    assert stale.returncode == 1, stale.stdout + stale.stderr
    assert "STALE" in stale.stderr


def test_hand_authored_region_is_byte_untouched(tmp_path):
    _init(tmp_path)
    # Introduce a real pending action so regeneration rewrites the block.
    (tmp_path / "docs" / "run-state").write_text(
        "NEEDS-HUMAN\nask: rule it\n", encoding="utf-8"
    )
    assert _gen(tmp_path).returncode == 0
    text = (tmp_path / "docs" / "open-items.md").read_text(encoding="utf-8")
    above = text.split(BEGIN, 1)[0]
    # Everything above the BEGIN marker equals the original bytes above it.
    assert above == OPEN_ITEMS.split(BEGIN, 1)[0]
    assert HAND in text


# --- dispatcher terminal-decision regeneration (best-effort) -------------------


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
    assert _gen(tmp_path).returncode == 0
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
    assert _gen(tmp_path).returncode == 0
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
    assert _gen(tmp_path).returncode == 0
    # Exactly one listing line for the id (the `- **WI-081**` bullet prefix); the
    # id also recurs inside that line's train/path pointer, so count the prefix.
    assert _block(tmp_path).count("**WI-081**") == 1


# --- (b) unreadable conflict record -------------------------------------------


def test_unreadable_conflict_record_is_surfaced(tmp_path):
    _init(tmp_path)
    # A conflict ref pointing at a commit whose message is NOT JSON.
    _commit_tree_ref(tmp_path, "refs/llm/conflict/p0-g3-WI-090-bad", "not json at all")
    assert _gen(tmp_path).returncode == 0
    body = _block(tmp_path)
    assert "Unreadable conflict record" in body
    assert "p0-g3-WI-090-bad" in body


# --- (c) unreadable-reservation-metadata quarantine ---------------------------


def test_unreadable_reservation_metadata_projects_quarantine(tmp_path):
    _init(tmp_path)
    _commit_tree_ref(tmp_path, "refs/llm/reservations/WI-095", "totally not json")
    assert _gen(tmp_path).returncode == 0
    body = _block(tmp_path)
    assert "Quarantined reservation" in body
    assert "WI-095" in body


# --- splice hardening: quoted markers, inversion, CRLF -------------------------


def test_indented_quoted_marker_does_not_break_regeneration(tmp_path):
    # A hand-authored brief that QUOTES the marker string on an indented line
    # must not make the splice choke — markers match only as exact full lines.
    (tmp_path / "docs" / "requirements").mkdir(parents=True)
    (tmp_path / "docs" / "requirements" / "work-items.csv").write_text(
        WI_HEADER + "WI-001,Seed,scripts,,,done,seeded,,,,\n", encoding="utf-8"
    )
    quoted = OPEN_ITEMS.replace(
        "- **Recommendation:** do it soon.\n",
        "- **Recommendation:** do it soon.\n"
        "- Example fence, indented:\n\n"
        "      " + BEGIN + "\n      " + END + "\n\n",
    )
    (tmp_path / "docs" / "open-items.md").write_text(quoted, encoding="utf-8")
    proc = _gen(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # The splice targets the column-0 markers only: the generated content lands
    # (checked against the whole file, since the indented quote is a second, inert
    # marker-looking pair), and the indented quote survives byte-for-byte.
    full = (tmp_path / "docs" / "open-items.md").read_text(encoding="utf-8")
    assert "no durable owner action is pending" in full
    assert "      " + BEGIN in full
    assert _gen(tmp_path, "--check").returncode == 0


def test_inverted_markers_fail_closed(tmp_path):
    (tmp_path / "docs" / "requirements").mkdir(parents=True)
    (tmp_path / "docs" / "requirements" / "work-items.csv").write_text(
        WI_HEADER + "WI-001,Seed,scripts,,,done,seeded,,,,\n", encoding="utf-8"
    )
    inverted = HAND + "\n" + END + "\ncontent\n" + BEGIN + "\n"
    (tmp_path / "docs" / "open-items.md").write_text(inverted, encoding="utf-8")
    proc = _gen(tmp_path)
    assert proc.returncode != 0
    assert "inverted" in (proc.stdout + proc.stderr).lower()
    # No silent rewrite: the file is byte-identical.
    assert (tmp_path / "docs" / "open-items.md").read_text(encoding="utf-8") == inverted


def test_duplicated_marker_line_fails_closed(tmp_path):
    (tmp_path / "docs" / "requirements").mkdir(parents=True)
    (tmp_path / "docs" / "requirements" / "work-items.csv").write_text(
        WI_HEADER + "WI-001,Seed,scripts,,,done,seeded,,,,\n", encoding="utf-8"
    )
    dup = OPEN_ITEMS + "\n" + BEGIN + "\nx\n" + END + "\n"
    (tmp_path / "docs" / "open-items.md").write_text(dup, encoding="utf-8")
    proc = _gen(tmp_path)
    assert proc.returncode != 0
    assert "duplicated" in (proc.stdout + proc.stderr).lower()


def test_crlf_file_keeps_crlf_and_hand_region_byte_untouched(tmp_path):
    # A CRLF checkout must round-trip: regeneration preserves \r\n and leaves the
    # hand-authored region byte-identical (byte-untouched on autocrlf).
    _init(tmp_path)
    (tmp_path / "docs" / "run-state").write_text(
        "NEEDS-HUMAN\nask: rule it\n", encoding="utf-8"
    )
    oi = tmp_path / "docs" / "open-items.md"
    crlf_bytes = OPEN_ITEMS.replace("\n", "\r\n").encode("utf-8")
    oi.write_bytes(crlf_bytes)
    hand_above = crlf_bytes.split(BEGIN.encode(), 1)[0]
    assert _gen(tmp_path).returncode == 0
    after = oi.read_bytes()
    assert b"\r\n" in after and b"\n" not in after.replace(b"\r\n", b"")
    assert after.split(BEGIN.encode(), 1)[0] == hand_above
    assert _gen(tmp_path, "--check").returncode == 0  # byte-fresh after regen


def test_template_placeholder_matches_empty_projection(tmp_path):
    # The shipped template's placeholder block MUST equal the empty projection,
    # else a fresh scaffold trips STALE on its first status-map gate (regression:
    # the rework changed the lead text and the template lagged).
    gen = load_script("gen_trajectory")
    (tmp_path / "docs").mkdir()
    empty = gen.pending_block(tmp_path)
    template = (ROOT / "project-trajectory" / "OPEN_ITEMS.template.md").read_text(
        encoding="utf-8"
    )
    block = template.split(BEGIN, 1)[1].split(END, 1)[0].strip("\n")
    assert block == empty


def test_absent_marker_pair_is_vacuous(tmp_path):
    # An open-items.md without the marker pair is left untouched (opt-in), and
    # --status --check passes vacuously.
    (tmp_path / "docs").mkdir(parents=True)
    (tmp_path / "docs" / "open-items.md").write_text(
        "# Open items\n\n## OI-1\n", encoding="utf-8"
    )
    assert _gen(tmp_path).returncode == 0
    assert _gen(tmp_path, "--check").returncode == 0
    assert (tmp_path / "docs" / "open-items.md").read_text(encoding="utf-8") == (
        "# Open items\n\n## OI-1\n"
    )
