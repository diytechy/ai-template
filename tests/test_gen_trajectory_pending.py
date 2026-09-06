"""The pending-owner-actions projection (WI-234), as DERIVED (WI-322).

`pending.pending_block` is a pure projection of committed-tree state:

  (a) `blocked` WI rows carrying a BlockRef (the attestation/approval page);
  (e) Drafted/Modified SR rows (WI-316) owing an approval / re-attest;
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

from conftest import load_script, pin_autocrlf

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
    pin_autocrlf(repo)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")


def _block(repo):
    """The derivation itself. Asserting on `pending_block` rather than on a
    rendered file keeps these regressions about WHAT IS PENDING — the question
    they were written to answer — independent of whichever surface renders it."""
    return load_script("pending").pending_block(repo)


# (A former source (a) `blocked` WI rows carrying a BlockRef retired with the
# blockref vocabulary at WI-553/OI-70 — nothing produces a queued-row blockref
# now, so the owner surface no longer reads a zero-producer source. The spine
# and pause arms below are the two surviving sources.)


# --- (e) Drafted / DRIFTED spine rows (WI-316) ---------------------------------
# The second arm read `Modified` until D-9 step 7 retired the marker; it now
# reads SNAPSHOT DRIFT, which is a property of the live registry against its
# `docs/archive/last_approved/` copy rather than of a cell. These fixtures
# carry no snapshot, so the DRAFTED arm is what they drive; the drift arm has
# its own coverage in tests/test_baseline_snapshot.py, where a snapshot exists.

BOM = bytes([0xEF, 0xBB, 0xBF])
SR_HEADER = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status,Phase,Area\n"
)


def _write_srs(repo, body):
    (repo / "docs" / "requirements" / "system-requirements.csv").write_text(
        SR_HEADER + body, encoding="utf-8"
    )


def test_a_RETIRED_marker_no_longer_projects_a_reattest_line(tmp_path):
    """D-9 STEP 7, pinned in the direction that could otherwise go unnoticed.

    This test used to prove that a `Modified` SR projected a re-attest line
    naming both flips. The marker retired, and what replaced it is SNAPSHOT
    DRIFT — so a row still carrying the retired word projects NOTHING here,
    which is correct (there is no baseline in this fixture to have drifted
    from) and is exactly the silence a migration must not leave unchecked.
    The safety net is elsewhere and is named here so the pair is legible: the
    cell is out-of-vocabulary, so `trace.py --strict-integrity` reds it at
    every gate. A projection going quiet is only acceptable because another
    surface got louder.

    The `-000` example-row rule is re-driven on the live vocabulary, since
    that is the property this fixture uniquely covers.
    """
    _init(tmp_path)
    _write_srs(
        tmp_path,
        'SR-000,EXAMPLE,,"r","x","a",,C,Test,Drafted,1,\n'
        'SR-004,Gate derivation,SN-001,"r","x","a",,C,Test,Modified,2,\n',
    )
    body = _block(tmp_path)
    assert "SR-004" not in body
    assert "SR-000" not in body  # the example row never projects
    assert "None — no durable owner action is pending" in body


def test_draft_sr_projects_approval_owed(tmp_path):
    # A Drafted SR projects an approval-owed line pointing at the per-SR
    # hierarchy brief — Drafted rows never surfaced in open-items before WI-316.
    _init(tmp_path)
    _write_srs(tmp_path, 'SR-007,New need,SN-001,"r","x","a",,C,Test,Drafted,3,\n')
    body = _block(tmp_path)
    assert "SR-007" in body and "approval owed" in body
    assert "--approve SR-007" in body


def test_bommed_registry_still_projects(tmp_path):
    # Adversarial-review F4: a BOM'd SR registry (the realistic Excel
    # round-trip) glued the BOM to the SR-ID header and silently hid every
    # Drafted line — the projection read "None pending" while an approval
    # was owed. read_rows now reads utf-8-sig.
    _init(tmp_path)
    body = SR_HEADER + 'SR-004,Gate derivation,SN-001,"r","x","a",,C,Test,Drafted,2,'
    (tmp_path / "docs" / "requirements" / "system-requirements.csv").write_bytes(
        BOM + (body + chr(10)).encode("utf-8")
    )
    assert "SR-004" in _block(tmp_path)


def test_approved_sr_does_not_project_and_the_flip_drops_the_line(tmp_path):
    # An Approved SR projects nothing; flipping Drafted->Approved (the
    # approval) drops the line on the next regeneration — the projection is
    # stateless. It drove Modified->Approved until D-9 step 7 retired that
    # marker; the surviving flip is the one a Status cell still records.
    _init(tmp_path)
    _write_srs(
        tmp_path, 'SR-004,Gate derivation,SN-001,"r","x","a",,C,Test,Drafted,2,\n'
    )
    assert "SR-004" in _block(tmp_path)
    _write_srs(
        tmp_path, 'SR-004,Gate derivation,SN-001,"r","x","a",,C,Test,Approved,2,\n'
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
    pending = load_script("pending")
    _init(tmp_path)
    for bad in ("not toml at all\n", 'since = "2026-07-29"\n', "reason = 7\n"):
        _pause(tmp_path, bad)
        assert "- **Paused** — {}.".format(pending.PAUSE_MALFORMED) in _block(tmp_path)


def test_pause_malformed_text_matches_the_coordinator_reader():
    # One message, two readers: pending owns the copy consumed by the status
    # projection, so pin it to the coordinator's source value.
    assert (
        load_script("pending").PAUSE_MALFORMED
        == load_script("agent_common").PAUSE_MALFORMED
    )


def test_pause_projection_is_deterministic(tmp_path):
    # No clock anywhere in the derivation: two reads of the same tree are
    # byte-identical, which is what the freshness gate depends on.
    _init(tmp_path)
    _pause(tmp_path, 'reason = "draining"\nsince = "2026-07-29"\n')
    assert _block(tmp_path) == _block(tmp_path)


# --- the read model and its siting (WI-483 slice 3) -------------------------
#
# Everything here asserts on the read model directly.  The one public facade
# compatibility contract belongs with the HTML family in test_gen_trajectory:
# core collection must not import the dashboard merely to reach these names.


def test_the_typed_model_kinds_every_pending_item(tmp_path):
    # `kind` is a FIELD, so a caller filtering by source never parses prose.
    pending = load_script("pending")
    _init(tmp_path)
    _write_srs(tmp_path, 'SR-007,New need,SN-001,"r","x","a",,C,Test,Drafted,3,\n')
    _pause(tmp_path, 'reason = "draining"\n')
    items = pending.pending_items(tmp_path)
    assert [i.kind for i in items] == [pending.SPINE, pending.PAUSE]
    assert all(i.line for i in items)


def test_owner_cards_is_pending_items_minus_the_pause(tmp_path):
    # The dispatcher's drained-queue arm: a paused station has its own earlier
    # exit, so the pause must never inflate the approvals-waiting count — and
    # the exclusion is DECLARED in the read model, not re-derived at the banner.
    pending = load_script("pending")
    _init(tmp_path)
    _write_srs(tmp_path, 'SR-007,New need,SN-001,"r","x","a",,C,Test,Drafted,3,\n')
    _pause(tmp_path, 'reason = "draining"\n')
    assert len(pending.pending_items(tmp_path)) == 2
    cards = pending.owner_cards(tmp_path)
    assert [c.kind for c in cards] == [pending.SPINE]


def test_the_block_renders_exactly_the_model(tmp_path):
    # One derivation, one rendering: every item's line appears in the block, so
    # the banner's count and the owner surface can never disagree.
    pending = load_script("pending")
    _init(tmp_path)
    _write_srs(tmp_path, 'SR-007,New need,SN-001,"r","x","a",,C,Test,Drafted,3,\n')
    block = pending.pending_block(tmp_path)
    for item in pending.pending_items(tmp_path):
        assert item.line in block


def test_the_dispatcher_reads_the_model_not_the_render_facade(tmp_path):
    # THE EDGE, asserted at the behaviour rather than only in the import
    # census: the banner's card count is the read model's `owner_cards`, so a
    # future rewrite cannot go back to two private names in a render module
    # without this failing.
    drv = load_script("dispatch")
    pending = load_script("pending")
    _init(
        tmp_path,
        [("queued", "WI-900", "blocked-one", 'blockref = "docs/x.md"\n', "")],
    )
    _pause(tmp_path, 'reason = "draining"\n')
    assert drv._pending_cards(tmp_path) == pending.owner_cards(tmp_path)


def test_the_owner_surface_reads_the_model_not_the_render_facade(tmp_path):
    # The other documented bad edge: gen_open_items reused `pending_block` by
    # importing the ~1,000-line facade. Same text, one module down.
    goi = load_script("gen_open_items")
    pending = load_script("pending")
    _init(tmp_path)
    assert goi.pending_block_text(tmp_path) == pending.pending_block(tmp_path)
