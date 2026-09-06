"""gen_trajectory.py --status — the docs/status.md derived snapshot (WI-277:
split verbatim from tests/test_gen_trajectory.py along the WI-280 production
seams; this module's subject is `traj_status.py`).

The snapshot PROJECTS already-derived facts (`derive_stage.py`'s recorded
`docs/stage` record, the open-items registry) into a marked block in
docs/status.md: the splice and its ordering, the volatile-git-state exclusion,
the --check freshness gate, the vacuous / minimal-record / unreadable-stage
arms, and the forward-only guard's scope.
"""

from conftest import SCRIPTS, run_py
from traj_fixtures import gen, make_repo, write_stage


# --- the docs/status.md derived snapshot (WI-202, --status) --------------------

# The fields of the recorded `docs/stage` record the snapshot PROJECTS (never
# recomputes). WI-498 slice 5 retired `docs/gate` and its `# basis:` comment
# line, so the projected facts are now named key=value fields; the file itself
# is rendered by the carrier's own writer (`traj_fixtures.write_stage`).
#
# `drafted` is deliberately PLURAL here. The singular arm (`drafted = 1`)
# currently renders "(1 drafts)": `kitlib.stage.parse` coerces the field to an
# int while `traj_status.status_block` picks the suffix by comparing it against
# the STRING "1". That is a product defect, reported rather than papered over —
# and asserting the wrong wording here to make a fixture pass would have made
# this test the thing that keeps it.
STAGE_FIELDS = {
    "stage": "DevStg-Tests",
    "phase": 2,
    "per-phase": {"1": "DevStg-Impl", "2": "DevStg-Tests"},
    "per-phase-live": {"1": "DevStg-Impl", "2": "DevStg-Tests"},
    "drafted": 3,
}

# One-line field vs Recommendation fallback; OI-3's field soft-wraps two lines,
# and its Decision carries a volatile git-state that must NOT reach the snapshot.
# WI-322: briefs are ROWS of the open-items registry, not markdown sections.
# Declared out of id order on purpose — the projection sorts numerically — and
# OI-2 carries no OneLine, so the first-sentence-of-Recommendation fallback is
# exercised too.
OPEN_ITEMS_HEADER = (
    "OI-ID,Title,Status,Raised,OneLine,Decision,BlastRadius,Options,"
    "Recommendation,WI-Refs,RuledDate,RulingRef\n"
)

OPEN_ITEMS = OPEN_ITEMS_HEADER + (
    'OI-2,the second decision,pending,,,"whether to flip the flag.",,,'
    '"keep it off until phase 3. A later sitting revisits.",,,\n'
    "OI-1,the first decision,pending,,"
    '"push — the branch is remote-tracked, so the unpushed commits are pure '
    'durability risk (the merge is a separate sitting).",'
    '"origin exists, ahead 9 commits at check — verify at read time.",,,,,,\n'
)

STATUS_MARKED = (
    "# Status\n\n## Current State\n\n"
    "<!-- BEGIN GENERATED STATUS -->\n"
    "<!-- END GENERATED STATUS -->\n\n"
    "- **Next action:** hand-authored intent stays here.\n\n"
    "## Scope\n\n- **Goal:** the thing.\n"
)


def make_status_repo(
    root, status=STATUS_MARKED, open_items=OPEN_ITEMS, stage=STAGE_FIELDS
):
    """`stage` is either a field mapping (rendered through the carrier's own
    writer) or a raw string written to `docs/stage` verbatim — the second form is
    how the degraded arms plant a record this kit did not write."""
    make_repo(root)
    if isinstance(stage, str):
        (root / "docs" / "stage").write_text(stage, encoding="utf-8")
    else:
        fields = dict(stage)
        write_stage(root, fields.pop("stage"), **fields)
    if open_items is not None:
        (root / "docs" / "requirements").mkdir(parents=True, exist_ok=True)
        (root / "docs" / "requirements" / "open-items.csv").write_text(
            open_items, encoding="utf-8"
        )
    if status is not None:
        (root / "docs" / "status.md").write_text(status, encoding="utf-8")
    return root


def status_text(root):
    return (root / "docs" / "status.md").read_text(encoding="utf-8")


def block_of(root):
    t = status_text(root)
    return t.split("<!-- BEGIN GENERATED STATUS -->", 1)[1].split(
        "<!-- END GENERATED STATUS -->", 1
    )[0]


def test_status_splices_derived_facts(tmp_path):
    make_status_repo(tmp_path)
    proc = gen(tmp_path, "--status")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    block = block_of(tmp_path)
    # The derived STAGE comes from the recorded `docs/stage` record, the spine
    # counts from the registries (WI-498 slice 5: `docs/gate`'s `# basis:` line
    # carried both, and the counts fast path retired with it). The bar axis's
    # ceiling marker — "(Release: pending harness driver)", rendered from
    # `spine_rules.bar_label` — retired with the axis: nothing derives
    # DevStg-Release any more, so there is no withheld top value to announce.
    # The position and the description are BOTH projected: the position off the
    # record's own `stage-ord`, the sentence off `kitlib.ladder.STAGE_DESC`.
    # `DevStg-Tests` is the SIXTH rung and reads "stage 6 of 8" — the record
    # keeps `stage-ord` 0-based because that is the index comparisons want, and
    # the renderer adds the one, which is why this pin is on the SENTENCE rather
    # than on the field.
    assert (
        "**In stage:** **DevStg-Tests** (stage 6 of 8, test-case definition in "
        "work)" in block
    )
    assert "the rung this repo is IN, derived over its settled spine" in block
    assert "per-phase `1=DevStg-Impl;2=DevStg-Tests`" in block and "phase=2" in block
    assert "SN=1 SR=2 LLR=3 TC=4" in block and "(3 drafts)" in block
    # the hand-authored intent + Scope stay OUTSIDE the markers, untouched
    after = status_text(tmp_path).split("<!-- END GENERATED STATUS -->", 1)[1]
    assert "hand-authored intent stays here" in after and "## Scope" in after


def test_status_cli_does_not_load_dashboard_renderers(tmp_path):
    make_status_repo(tmp_path)
    script = str(SCRIPTS / "gen_trajectory.py")
    denied = {
        "traj_context",
        "traj_graph",
        "traj_panels",
        "traj_render",
        "traj_views",
    }
    probe = """
import runpy
import sys

denied = {denied!r}

class DenyDashboardImports:
    def find_spec(self, fullname, path=None, target=None):
        if fullname.partition(".")[0] in denied:
            raise AssertionError("status loaded dashboard module " + fullname)
        return None

sys.meta_path.insert(0, DenyDashboardImports())
sys.argv = [{script!r}, "--root", {root!r}, "--status"]
try:
    runpy.run_path({script!r}, run_name="__main__")
except SystemExit as exc:
    if exc.code:
        raise
else:
    raise AssertionError("gen_trajectory did not exit through its CLI boundary")

loaded = denied.intersection(sys.modules)
if loaded:
    raise AssertionError("status retained dashboard modules: " + repr(sorted(loaded)))
""".format(denied=denied, script=script, root=str(tmp_path))

    proc = run_py(["-c", probe], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "**In stage:** **DevStg-Tests**" in block_of(tmp_path)


def test_status_open_items_projection_and_ordering(tmp_path):
    make_status_repo(tmp_path)
    assert gen(tmp_path, "--status").returncode == 0
    block = block_of(tmp_path)
    # id-order (OI-1 before OI-2) regardless of file order
    assert block.index("**OI-1**") < block.index("**OI-2**")
    # OI-1: the explicit One-line field, soft-wrapped lines joined into one bullet
    assert (
        "**OI-1** — push — the branch is remote-tracked, so the unpushed commits "
        "are pure durability risk (the merge is a separate sitting)." in block
    )
    # OI-2: no One-line field -> the FIRST sentence of Recommendation, not the rest
    assert "**OI-2** — keep it off until phase 3." in block
    assert "A later sitting revisits" not in block


def test_status_does_not_bake_volatile_git_state(tmp_path):
    # Done-when 4: an item's live git state (OI-1's "ahead 9 commits") lives in the
    # brief's Decision field, never the stamped snapshot.
    make_status_repo(tmp_path)
    assert gen(tmp_path, "--status").returncode == 0
    assert "ahead 9 commits" not in block_of(tmp_path)


def test_status_check_fresh_and_stale(tmp_path):
    make_status_repo(tmp_path)
    assert gen(tmp_path, "--status").returncode == 0
    fresh = gen(tmp_path, "--status", "--check")
    assert fresh.returncode == 0 and "up to date" in fresh.stdout
    # an open-items edit stales the block (caught at commit, not first in CI)
    oi = tmp_path / "docs" / "requirements" / "open-items.csv"
    oi.write_text(
        oi.read_text(encoding="utf-8")
        + "OI-5,a new ask,pending,,decide soon.,,,,,,,\n",
        encoding="utf-8",
    )
    stale = gen(tmp_path, "--status", "--check")
    assert stale.returncode == 1 and "STALE" in stale.stderr
    # regenerating restores freshness and now projects OI-5
    assert gen(tmp_path, "--status").returncode == 0
    assert gen(tmp_path, "--status", "--check").returncode == 0
    assert "**OI-5** — decide soon." in block_of(tmp_path)


def test_status_vacuous_without_markers_or_file(tmp_path):
    # Opt-in posture: a status.md without the marker pair is left untouched and
    # --check passes vacuously; an absent status.md is likewise a clean no-op.
    make_status_repo(tmp_path, status="# Status\n\n## Scope\n\n- Goal\n")
    before = status_text(tmp_path)
    proc = gen(tmp_path, "--status")
    assert proc.returncode == 0 and "no GENERATED STATUS markers" in proc.stdout
    assert status_text(tmp_path) == before  # untouched
    assert gen(tmp_path, "--status", "--check").returncode == 0
    (tmp_path / "docs" / "status.md").unlink()
    assert gen(tmp_path, "--status", "--check").returncode == 0


def test_status_renders_a_degraded_stage_record(tmp_path):
    # RE-KEYED FROM "legacy gate without basis falls back to counts" (WI-498
    # slice 5). The old subject — a hand-set `docs/gate` whose `# basis:` line is
    # missing, so the cached counts are unavailable — retired with the file AND
    # with the cached-counts fast path (the registry count is the only arm now).
    # The concern that OUTLIVES it is degradation: the snapshot must still render
    # something honest when the derived carrier is thin or unreadable, and must
    # never invent a rung. Both shapes the new carrier admits are driven.
    #
    # (a) A MINIMAL record — a `stage` and nothing else. The rung renders, the
    # position degrades to the bare word "stage" rather than a guessed ordinal,
    # no per-phase/draft detail is claimed, and the counts come off the
    # registries (SN=1 SR=2 LLR=3 TC=4 in the fixture spine).
    thin = tmp_path / "thin"
    thin.mkdir()
    make_status_repo(thin, stage="stage = DevStg-Reqs\n")
    assert gen(thin, "--status").returncode == 0
    block = block_of(thin)
    assert (
        "**In stage:** **DevStg-Reqs** (stage, requirement definition in work)" in block
    )
    assert "SN=1 SR=2 LLR=3 TC=4" in block
    assert "per-phase" not in block and "draft" not in block

    # (b) A file this kit did not write — no `stage` field at all. The bullet
    # names NO stage and says where the value should come from, instead of
    # degrading toward a plausible-looking one; the spine line is unaffected.
    unreadable = tmp_path / "unreadable"
    unreadable.mkdir()
    make_status_repo(unreadable, stage="# a hand-written file, no record here\n")
    assert gen(unreadable, "--status").returncode == 0
    block = block_of(unreadable)
    assert "**Stage:** not derived — no readable `docs/stage`." in block
    assert "DevStg-" not in block
    assert "SN=1 SR=2 LLR=3 TC=4" in block


def test_status_forward_only_guard_is_scoped_to_the_generated_block(tmp_path):
    # The WI-200 handoff, re-scoped by repo-review 2026-07-21 H-5: the marker
    # exempts ONLY the spliced block (its freshness is the status-map step's
    # job); the hand-authored remainder of a hybrid status.md stays policed —
    # the old whole-file stand-down left it enforced by nothing, and this
    # repo's own status.md promptly accreted done-WI prose. Uses an all-done
    # registry so no other --strict rule fires (R-A wants a Deliverable iff
    # done; R-E wants a SpecRef on OPEN rows only).
    coherent = (
        "WI-001,Bootstrap,scripts,SR-001,,done,the adder\n"
        "WI-002,Harness,scripts,SR-001,WI-001,done,harness green\n"
    )
    make_repo(tmp_path, coherent)
    fields = dict(STAGE_FIELDS)
    write_stage(tmp_path, fields.pop("stage"), **fields)
    # 1) A clean hand region beside the generated block: --strict is clean
    # (whatever done ids the BLOCK itself carries are the splice's business).
    (tmp_path / "docs" / "status.md").write_text(STATUS_MARKED, encoding="utf-8")
    assert gen(tmp_path, "--status").returncode == 0
    marked = run_py(
        [SCRIPTS / "check_trajectory.py", "--root", tmp_path, "--strict"], cwd=tmp_path
    )
    assert marked.returncode == 0, marked.stdout + marked.stderr
    assert "forward-only" not in (marked.stdout + marked.stderr)
    # 2) A done id accreting in the HAND region of the same marked file: a
    # finding, ERROR under --strict (this was silently clean before H-5).
    (tmp_path / "docs" / "status.md").write_text(
        STATUS_MARKED.replace(
            "hand-authored intent stays here.",
            "WI-001 shipped the adder (a done id in prose).",
        ),
        encoding="utf-8",
    )
    assert gen(tmp_path, "--status").returncode == 0
    hand = run_py(
        [SCRIPTS / "check_trajectory.py", "--root", tmp_path, "--strict"], cwd=tmp_path
    )
    assert hand.returncode == 1, hand.stdout + hand.stderr
    assert "forward-only" in hand.stderr and "WI-001" in hand.stderr
    # 3) Markers stripped entirely: the rule polices the whole file (unchanged).
    stripped = (
        status_text(tmp_path)
        .replace("<!-- BEGIN GENERATED STATUS -->", "")
        .replace("<!-- END GENERATED STATUS -->", "")
    )
    (tmp_path / "docs" / "status.md").write_text(stripped, encoding="utf-8")
    rearmed = run_py(
        [SCRIPTS / "check_trajectory.py", "--root", tmp_path, "--strict"], cwd=tmp_path
    )
    assert rearmed.returncode == 1 and "forward-only" in rearmed.stderr
