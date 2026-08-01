"""The pending-owner-actions projection (WI-234), as DERIVED (WI-322).

`gen_trajectory.pending_block` is a pure projection of committed-tree state:

  (a) `blocked` WI rows carrying a BlockRef (the attestation/ratification page);
  (e) Draft/Modified SR rows (WI-316) owing a ratification / re-attest;
  (f) the tracked `docs/work/pause` declaration (concurrency-restructure §5.6).

(The dispatcher-era sources — refs/llm conflict records, quarantined trains,
stranded-train attestations, the run-state ask, and the machine-local advisory
split — retired with the dispatcher at Phase 5; their tests went with them.)

Each regression builds a temp git repo and asserts on the DERIVATION: the line
appears, its pointer is right, and resolving the state drops it.

WI-322 retired the markdown surface this used to splice into, so twelve tests
whose subject WAS the splice (marker pairs, CRLF round-trip, the hand-authored
region staying byte-untouched, the freshness compare and its machine-local mask)
went with the code they guarded — porting them would have guarded nothing. Their
live successors are in `tests/test_gen_open_items.py`, against the generated
view: the staleness bite and the vacuous-non-adopter posture.
"""

import subprocess

from conftest import load_script

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


def _spec(repo, sub, wid, slug, status_extra="", body=""):
    d = repo / "docs" / "work" / sub
    d.mkdir(parents=True, exist_ok=True)
    text = '+++\nid = "{}"\ntitle = "{}"\n{}+++\n{}'.format(
        wid, slug, status_extra, body
    )
    (d / "{}-{}.md".format(wid, slug)).write_text(text, encoding="utf-8")


def _init(repo, extra_specs=()):
    """A seeded repo whose registry is the spec folder (the one home since
    Phase 5): one done item plus any `(sub, wid, slug, frontmatter, body)`
    tuples in `extra_specs`."""
    (repo / "docs" / "requirements").mkdir(parents=True)
    _spec(repo, "complete", "WI-001", "seed", body="\n## Deliverable\n\nseeded\n")
    for sub, wid, slug, front, body in extra_specs:
        _spec(repo, sub, wid, slug, front, body)
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


# --- (a) blocked row with a BlockRef --------------------------------------


def test_blocked_row_with_dev_tree_doc_cites_the_plain_path(tmp_path):
    # Blocked is DERIVED (queued + blockref, Phase 5): the projection cites
    # the plain BlockRef path.
    _init(
        tmp_path,
        [("queued", "WI-051", "split", 'blockref = "docs/ratify/WI-051.md"\n', "")],
    )
    (tmp_path / "docs" / "ratify").mkdir()
    (tmp_path / "docs" / "ratify" / "WI-051.md").write_text("plan\n", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "plan on dev")
    body = _block(tmp_path)
    assert "`docs/ratify/WI-051.md`" in body
    assert "git show" not in body


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


# --- (f) the tracked pause declaration, docs/work/pause -----------------------
# `docs/concurrency-restructure.md` §5.6: status generation surfaces the open
# pause so it is a visible accruing cost, never a forgotten one. Committed-tree
# pure — the declared `since` renders verbatim, never an age from a clock.


def _pause(repo, body):
    (repo / "docs" / "work").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "work" / "pause").write_text(body, encoding="utf-8")


def test_no_pause_file_projects_no_bullet(tmp_path):
    _init(tmp_path)
    body = _block(tmp_path)
    assert "Paused" not in body
    assert "None — no durable owner action is pending" in body


def test_tracked_pause_projects_reason_and_declared_since(tmp_path):
    _init(tmp_path)
    _pause(tmp_path, 'reason = "draining for the audit"\nsince = "2026-07-29"\n')
    body = _block(tmp_path)
    assert "- **Paused since 2026-07-29** — draining for the audit." in body
    # Unpausing is a deletion; the projection is stateless, so the line clears.
    (tmp_path / "docs" / "work" / "pause").unlink()
    assert "Paused" not in _block(tmp_path)


def test_tracked_pause_without_since_omits_the_stamp(tmp_path):
    _init(tmp_path)
    _pause(tmp_path, 'reason = "draining for the audit"\n')
    assert "- **Paused** — draining for the audit." in _block(tmp_path)


def test_malformed_pause_still_projects_fail_closed(tmp_path):
    # A pause file we cannot read is still a pause: it projects the same loud
    # message the coordinator's reader returns, routing the owner to the fix.
    gt = load_script("gen_trajectory")
    _init(tmp_path)
    for bad in ("not toml at all\n", 'since = "2026-07-29"\n', "reason = 7\n"):
        _pause(tmp_path, bad)
        assert "- **Paused** — {}.".format(gt.PAUSE_MALFORMED) in _block(tmp_path)


def test_pause_malformed_text_matches_the_coordinator_reader():
    # One message, two readers: gen_trajectory copies the constant rather than
    # importing the coordinator layer, so pin the copies equal.
    assert (
        load_script("gen_trajectory").PAUSE_MALFORMED
        == load_script("agent_common").PAUSE_MALFORMED
    )


def test_pause_projection_is_deterministic(tmp_path):
    # No clock anywhere in the derivation: two reads of the same tree are
    # byte-identical, which is what the freshness gate depends on.
    _init(tmp_path)
    _pause(tmp_path, 'reason = "draining"\nsince = "2026-07-29"\n')
    assert _block(tmp_path) == _block(tmp_path)
