"""The first old-kit re-sync test: scaffold at an OLDER kit commit, sync forward.

WHY THIS EXISTS (OI-27, defect 3). Every other scaffold test in this suite
bootstraps a repo from kit HEAD. Not one of them scaffolds an *old* kit state and
brings it forward, which is the only thing a real adopter ever does — and the
field record names three distinct re-sync breakages, each caught downstream by a
human rather than by this suite. This module builds the missing shape: extract a
pinned older commit of THIS repo's own history, bootstrap a scaffold from it, run
the re-sync procedure ADOPTING.md §6 documents today, and require the result to
be a green harness.

WHAT IT HONESTLY COVERS
  - The documented procedure RUNS, end to end, across a real three-week kit
    range, on a scaffold built by a genuinely older bootstrap — not a mock.
  - The scaffold that comes out the far side passes the kit's own harness
    (`check.py` at its gate, `trace.py --strict`), and passes it NON-vacuously:
    an old `check.py` that no longer recognises the repo prints "No checks
    defined" and would otherwise hand us a false green, so that is asserted
    against explicitly.
  - The re-stamp works: `docs/kit-version` moves from the old kit's label to the
    current kit's SHA, which is what makes the NEXT re-sync a diff.
  - The one documented recipe that updates an existing file — delete
    `docs/process.md` + `docs/process-options.md`, re-run bootstrap — really does
    refresh them from the current masters.

WHAT IT DOES NOT COVER, stated plainly because the gap is the point
  - **Syncing forward is ADD-ONLY today.** A `bootstrap.py --dest .` re-run is
    write-once: it creates files the repo lacks and updates NOTHING it already
    has, and it never deletes a script the kit has since retired. So this test
    does not show that an old scaffold ends up EQUAL to a fresh one — it shows
    the opposite, and pins it (`test_documented_resync_is_add_only_today`). After
    the documented run, most kit-owned scripts in the scaffold are still the old
    ones. The rest of §6 — "overwrite freely", "re-apply your dials", the
    per-change migration recipes — is prose an operator executes by hand, and
    SR-036 declares that judgment deliberately non-mechanized
    (`verification = "Inspection"`). None of that half is exercised here.
  - Consequently a GREEN here means "the documented mechanical steps leave a
    repo whose OWN harness passes", not "the repo is now on the current kit".
    Those are different claims and this file only makes the first — and the
    distinction is not academic: the measured result is that the re-synced
    scaffold ends up carrying its spine registries under BOTH carriers, a state
    the current kit hard-REFUSES, and it still reports green because the
    checker that would refuse it is one of the stale files
    (`test_the_green_holds_only_because_the_old_checkers_survived`). Read that
    test before trusting the headline one.
  - It exercises ONE range (the pin below), not every range; a migration recipe
    that only applies to some other range is untested by construction.
  - The extracted old kit is not a git checkout, so the old scaffold is stamped
    `unknown (kit not a git checkout)` — the tarball-adopter shape. That is
    faithful to a real adoption route, but it means the "diff your recorded SHA"
    step of §6 is the one step this fixture cannot perform, and does not.

  When the OI-27 re-sync pack lands, THIS is its baseline: the pack's procedure
  replaces the steps below and the same assertions must still hold, so any claim
  it makes about carrying an old repo forward is measured rather than asserted in
  prose.
"""

import collections
import hashlib
import io
import shutil
import subprocess
import tarfile

import pytest
from conftest import ROOT, SCRIPTS, run_py, skip_without_env_gates

# --- The pin -----------------------------------------------------------------
# WHY THIS COMMIT, recorded so the next person can re-pin deliberately rather
# than by taste:
#   1. AGE. 2026-07-22, three weeks before this WI. The range to HEAD crosses
#      real, documented kit change — the concurrency restructure's Phase 5
#      dispatcher deletion, the `drive.py` -> `dispatch.py`/`lane.py` split, the
#      WI-registry CSV -> spec-folder flip, the spine's CSV -> TOML carrier move,
#      and `check_dupes.py`'s removal. Those are exactly the recipes ADOPTING.md
#      §6 carries, so the test crosses recipes rather than a quiet week.
#   2. IT IS A CLEAN CLOSE POINT on the trunk's first-parent history (a "mark
#      done + registry/dashboard close" commit), not a mid-claim state, so the
#      scaffold it produces is a coherent kit rather than a half-landed one.
#   3. ITS GREEN IS NOT VACUOUS. Measured while choosing: re-syncing forward from
#      this commit leaves a harness that runs four real steps and passes. Reaching
#      further back (e.g. `main`'s tip, 2026-06-28) produces a scaffold whose
#      surviving old `check.py` prints "No checks defined for gate G1" and exits
#      0 — a green that means nothing. A test whose bar can be met vacuously is
#      worse than no test, so the pin stops on the near side of that line and
#      `test_old_kit_scaffold_syncs_forward_to_a_green_harness` asserts against
#      the vacuous shape directly.
# Re-pinning is expected as the kit ages; keep the three criteria, not the SHA.
PINNED_OLD_KIT_SHA = "fd5916b976dc3d77ff11a2d2d6bc4a7fa924641d"
PINNED_OLD_KIT_DATE = "2026-07-22"

PROCESS_DOCS = ("docs/process.md", "docs/process-options.md")


ResyncRun = collections.namedtuple(
    "ResyncRun",
    "old_kit pristine repo old_stamp plain_out process_before process_after",
)


def _git(args, **kw):
    """Run git at this repo's root, capturing bytes (never text: `git archive`
    emits a tar stream)."""
    return subprocess.run(
        ["git"] + list(args), cwd=str(ROOT), capture_output=True, **kw
    )


def _old_kit_unavailable():
    """A named reason the pinned kit state cannot be reached, or None.

    Probed rather than assumed: a shallow CI clone, a source tarball, or a
    machine with no git all reach this module, and every one of them is an
    ENVIRONMENT fact, not a defect in the branch under test. Skipping with the
    reason spelled out is the honest verdict there; failing would report the
    checkout depth as a bug.
    """
    if _git(["rev-parse", "--is-inside-work-tree"]).returncode != 0:
        return "no git work tree at the repo root (source export?)"
    if _git(["cat-file", "-e", PINNED_OLD_KIT_SHA + "^{commit}"]).returncode != 0:
        shallow = _git(["rev-parse", "--is-shallow-repository"]).stdout.strip()
        depth = " (shallow clone — fetch full history)" if shallow == b"true" else ""
        return (
            "pinned old kit commit {} ({}) is not in this checkout's history{}".format(
                PINNED_OLD_KIT_SHA[:8], PINNED_OLD_KIT_DATE, depth
            )
        )
    return None


def _extract_old_kit(dest):
    """Materialize `project-trajectory/` as of the pinned commit under `dest`.

    `git archive` (not a worktree or a checkout) on purpose: it reads straight
    from the object database, so it cannot disturb the working tree this suite is
    running in, needs no cleanup that could fail under a Windows file lock, and
    works the same on both platforms. The tar stream is expanded through stdlib
    `tarfile` rather than a `tar` binary, which Windows runners may not have.
    """
    proc = _git(["archive", "--format=tar", PINNED_OLD_KIT_SHA, "project-trajectory"])
    assert proc.returncode == 0, proc.stderr.decode("utf-8", "replace")
    with tarfile.open(fileobj=io.BytesIO(proc.stdout)) as tar:
        try:
            tar.extractall(path=str(dest), filter="data")
        except TypeError:  # `filter` arrives in 3.11.4; older 3.11 patch levels
            tar.extractall(path=str(dest))
    old_kit = dest / "project-trajectory"
    assert (old_kit / "scripts" / "bootstrap.py").exists(), (
        "the pinned kit state has no scripts/bootstrap.py — re-pin"
    )
    return old_kit


def _digests(root, rels):
    """sha256 per relative path (None when absent) — the before/after probe for
    "did the documented step actually change this file?"."""
    out = {}
    for rel in rels:
        p = root / rel
        out[rel] = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
    return out


@pytest.fixture(scope="module")
def resync(tmp_path_factory):
    """Scaffold from the pinned old kit, then run §6's documented steps forward.

    Module-scoped: the chain is four bootstraps' worth of subprocesses and every
    test in this file interrogates the SAME run, which is also what makes the
    assertions comparable (they describe one re-sync, not four).

    The steps below are exactly what ADOPTING.md §6 documents TODAY, in its
    order, and nothing else — no repair the guide does not tell an adopter to
    perform. That restraint is the point: if the documented procedure is
    insufficient, this test must show it, not paper over it.
    """
    skip_without_env_gates("git")
    reason = _old_kit_unavailable()
    if reason:
        pytest.skip("old-kit re-sync unavailable: " + reason)

    base = tmp_path_factory.mktemp("oldkit")
    old_kit = _extract_old_kit(base / "kit")

    # (a) An adopter's repo, scaffolded by the OLD kit's own bootstrap.
    pristine = base / "adopter-at-old-kit"
    pristine.mkdir()
    proc = run_py([old_kit / "scripts" / "bootstrap.py", "--dest", pristine], cwd=base)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    stamp_file = pristine / "docs" / "kit-version"
    old_stamp = stamp_file.read_text(encoding="utf-8") if stamp_file.exists() else ""

    # Keep `pristine` untouched as the before-image; the re-sync runs on a copy.
    repo = base / "adopter-resynced"
    shutil.copytree(pristine, repo)
    before = _digests(repo, PROCESS_DOCS)

    # (b) §6's mechanical step: re-run the CURRENT kit's bootstrap in place.
    plain = run_py([SCRIPTS / "bootstrap.py", "--dest", "."], cwd=repo)
    assert plain.returncode == 0, plain.stdout + plain.stderr

    # (c) §6 "Regenerate, never raw-copy": the process docs are generated from
    # the recorded docs/kit-profile, so taking the new ones means deleting them
    # and re-running — the ONE documented way a re-sync updates a file it has.
    for rel in PROCESS_DOCS:
        (repo / rel).unlink()
    regen = run_py([SCRIPTS / "bootstrap.py", "--dest", "."], cwd=repo)
    assert regen.returncode == 0, regen.stdout + regen.stderr
    after = _digests(repo, PROCESS_DOCS)

    # (d) §6: refresh any materialized per-agent skill copies from source.
    # Vacuous on a scaffold with no agent dir, which is the default — run it
    # anyway, because "vacuous but exits 0" is itself the documented contract.
    sync = run_py([SCRIPTS / "bootstrap.py", "--dest", ".", "--sync"], cwd=repo)
    assert sync.returncode == 0, sync.stdout + sync.stderr

    return ResyncRun(
        old_kit=old_kit,
        pristine=pristine,
        repo=repo,
        old_stamp=old_stamp,
        plain_out=plain.stdout + plain.stderr,
        process_before=before,
        process_after=after,
    )


def test_old_kit_scaffold_syncs_forward_to_a_green_harness(resync):
    """The headline claim: old scaffold + documented re-sync => green harness.

    Green is checked for SUBSTANCE as well as exit code. A re-synced repo still
    carries its OLD `check.py`, and an old enough one no longer recognises the
    repo it is standing in and reports "No checks defined for gate <G>" at exit
    0. That is the false green this whole class of test exists to catch, so the
    assertions below require the harness to have actually run steps and passed
    them.
    """
    proc = run_py(["scripts/check.py", "--gate", "G1"], cwd=resync.repo)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert "RESULT: PASS" in out, out
    assert "No checks defined" not in out, (
        "the re-synced scaffold's harness ran NO steps — this green is vacuous, "
        "which means the pin is too old for the surviving check.py:\n" + out
    )
    passed = [ln for ln in out.splitlines() if ln.strip().startswith("PASS ")]
    assert len(passed) >= 3, "expected a substantive harness plan, got:\n" + out

    # ...and the traceability spine the kit ships is intact on the far side.
    trace = run_py(["scripts/trace.py", "--strict"], cwd=resync.repo)
    assert trace.returncode == 0, trace.stdout + trace.stderr
    assert "orphans=0" in trace.stdout


def test_resync_restamps_the_kit_version_anchor(resync):
    """The stamp moves to the current kit, which is what makes the NEXT re-sync
    a diff instead of a guess. `docs/kit-version` is a generated stamp, so it is
    the one kit-owned file a plain re-run always rewrites."""
    stamp = (resync.repo / "docs" / "kit-version").read_text(encoding="utf-8")
    head = _git(["rev-parse", "--short", "HEAD"]).stdout.decode().strip()
    assert head and head in stamp, (
        "re-sync must re-stamp docs/kit-version to the current kit:\n" + stamp
    )
    assert stamp != resync.old_stamp

    # The old scaffold's own stamp is the tarball shape (the extracted kit is not
    # a git checkout) — recorded here because it is the honest limitation named in
    # this module's docstring, and because OI-27 defect 1 made that path warn.
    if resync.old_stamp:
        assert "unknown (kit not a git checkout)" in resync.old_stamp


def test_documented_regenerate_recipe_refreshes_the_process_docs(resync):
    """§6's delete-then-re-run recipe is the one documented path by which a
    re-sync UPDATES a file the repo already had. If it silently no-ops, an
    adopter's process docs stay frozen at their adoption date while the guide
    says otherwise."""
    for rel in PROCESS_DOCS:
        assert resync.process_before[rel], rel + " missing from the old scaffold"
        assert resync.process_after[rel], rel + " not regenerated"
        assert resync.process_after[rel] != resync.process_before[rel], (
            rel + " was NOT refreshed by the documented regenerate recipe — the "
            "adopter would keep the old kit's process docs while believing they "
            "took the new ones"
        )
    # Regenerated from the masters, not raw-copied: no kit-only marker leaks.
    text = (resync.repo / "docs" / "process.md").read_text(encoding="utf-8")
    assert "kit-only" not in text


def test_documented_resync_is_add_only_today(resync):
    """The GAP, pinned as behaviour rather than left as prose.

    `bootstrap.py` is write-once. So the documented mechanical re-sync ADDS the
    files a repo lacks and updates none it has, and deletes nothing the kit has
    retired. Everything else in §6 is an operator's hand-work, which SR-036
    declares deliberately non-mechanized. This test asserts that state exactly —
    so that when the OI-27 re-sync pack changes it, the change is visible here as
    a failure to be re-baselined rather than an unnoticed silent shift.
    """
    old_scripts = {p.name: p.read_bytes() for p in resync.pristine.glob("scripts/*.py")}
    new_scripts = {p.name: p.read_bytes() for p in SCRIPTS.glob("*.py")}
    got = {p.name: p.read_bytes() for p in resync.repo.glob("scripts/*.py")}

    # 1. ADDED: files the old kit never shipped do arrive. (The half that works.)
    added = sorted(n for n in got if n not in old_scripts)
    assert added, "a re-sync across three weeks of kit change added no script"
    assert "created:" in resync.plain_out

    # 2. NOT UPDATED: a kit-owned script that CHANGED in the range stays old.
    stale = sorted(
        n
        for n, body in old_scripts.items()
        if n in new_scripts and new_scripts[n] != body and got.get(n) == body
    )
    changed_in_range = sorted(
        n
        for n, body in old_scripts.items()
        if n in new_scripts and new_scripts[n] != body
    )
    assert changed_in_range, (
        "no kit-owned script changed between the pinned commit and HEAD — the "
        "pin is too close to HEAD to test anything; re-pin further back"
    )
    assert stale == changed_in_range, (
        "the documented re-sync updated a kit-owned script in place. That is a "
        "GOOD change, but this test pins the add-only contract — re-baseline it "
        "(and this module's docstring) deliberately. Updated: {}".format(
            sorted(set(changed_in_range) - set(stale))
        )
    )

    # 3. NOT DELETED: a script the current kit RETIRED survives the re-sync, so
    #    §6's "delete your old scripts/<x>.py" recipes are load-bearing hand-work.
    retired = sorted(n for n in old_scripts if n not in new_scripts)
    assert retired, "the pinned range retired no script — re-pin to cross one"
    assert all(n in got for n in retired), (
        "a retired script vanished on its own; the re-sync now deletes, which "
        "contradicts the write-once contract this test pins: " + str(retired)
    )


def test_the_green_holds_only_because_the_old_checkers_survived(resync):
    """The sharpest thing this module measures, and the reason it exists.

    Add-only has a consequence beyond "some files are stale". Because the
    re-sync ADDS the current kit's registry files without REMOVING the old kit's,
    the scaffold ends up carrying the same registry under BOTH carriers — the
    exact dual-home state the kit hard-REFUSES (`spine_carrier.resolve` raises
    on it, by the same rule `--migrate-config` applies to the policy dials).

    And it reports green anyway, because the checker that would refuse it is one
    of the kit-owned scripts the re-sync did not update: the repo is still being
    judged by the OLD `trace.py`, which predates the carrier and cannot see the
    problem. Run the CURRENT kit's `trace.py` against the very same tree and it
    exits nonzero.

    That is SN-008's dishonest green one level up — not a skipped check, but a
    check that no longer matches the repo it is checking — and it is a MEASURED
    fact about the documented procedure, not a hypothesis. Pinned here so the
    OI-27 re-sync pack has a concrete thing to fix and a way to prove it did.
    """
    csv_home = resync.repo / "docs" / "requirements" / "system-requirements.csv"
    toml_home = resync.repo / "docs" / "requirements" / "system-requirements.toml"
    assert csv_home.is_file() and toml_home.is_file(), (
        "expected the re-sync to leave BOTH carriers live; if it no longer "
        "does, the add-only contract changed — re-baseline this module"
    )

    # The repo's own (old) harness: green.
    own = run_py(["scripts/trace.py", "--strict"], cwd=resync.repo)
    assert own.returncode == 0, own.stdout + own.stderr

    # The current kit's identical check, same tree: refused.
    current = run_py([SCRIPTS / "trace.py", "--strict"], cwd=resync.repo)
    assert current.returncode != 0, (
        "the current trace.py accepted a dual-carrier tree — the refusal this "
        "test relies on has moved:\n" + current.stdout + current.stderr
    )
    assert "BOTH carriers" in current.stdout + current.stderr
