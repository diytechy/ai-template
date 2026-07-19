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

from conftest import SCRIPTS, load_script, run_py

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
