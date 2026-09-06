"""The first old-kit re-sync test: scaffold at an OLDER kit commit, sync forward.

WHY THIS EXISTS (OI-27, defect 3). Every other scaffold test in this suite
bootstraps a repo from kit HEAD. Not one of them scaffolds an *old* kit state and
brings it forward, which is the only thing a real adopter ever does — and the
field record names three distinct re-sync breakages, each caught downstream by a
human rather than by this suite. This module builds the missing shape: extract a
pinned older commit of THIS repo's own history, bootstrap a scaffold from it, run
the re-sync procedure the kit documents today, and require the result to be a
green harness. That procedure's home moved at OI-27's ruling — from ADOPTING.md
§6 to `project-trajectory/RESYNC_PACK.md` §1, which is where the mechanical steps
below are now written; §6 keeps the framing and points there.

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
    ones. The rest of the procedure — the pack's §2 deviation review and its §3
    per-change entries — is prose an operator executes by hand, and SR-036
    declares that judgment deliberately non-mechanized
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
    step of the procedure is the one step this fixture cannot perform, and
    does not.

  The OI-27 re-sync pack HAS landed (`project-trajectory/RESYNC_PACK.md`), and
  this module is its baseline: the pack re-homed the procedure without changing
  the mechanical steps, so the same assertions still hold, and any future claim
  the pack makes about carrying an old repo forward has to be re-measured HERE —
  a change to the pack's §1 that this module does not reflect is a claim asserted
  in prose. `tests/test_resync_pack.py` holds the pack's shape; this one holds
  what the procedure actually does to a repo.
"""

import collections
import hashlib
import io
import shutil
import subprocess
import tarfile
import tomllib

import pytest
from conftest import ROOT, SCRIPTS, run_py, skip_without_env_gates

# --- The pin -----------------------------------------------------------------
# WHY THIS COMMIT, recorded so the next person can re-pin deliberately rather
# than by taste:
#   1. AGE. 2026-07-22, three weeks before this WI. The range to HEAD crosses
#      real, documented kit change — the concurrency restructure's Phase 5
#      dispatcher deletion, the `drive.py` -> `dispatch.py`/`lane.py` split, the
#      WI-registry CSV -> spec-folder flip, the spine's CSV -> TOML carrier move,
#      and `check_dupes.py`'s removal. Those are exactly the entries
#      RESYNC_PACK.md §3 carries, so the test crosses migrations rather
#      than a quiet week.
#   2. IT IS A CLEAN CLOSE POINT on the trunk's first-parent history (a "mark
#      done + registry/dashboard close" commit), not a mid-claim state, so the
#      scaffold it produces is a coherent kit rather than a half-landed one.
#   3. ITS GREEN IS NOT VACUOUS. Measured while choosing: re-syncing forward from
#      this commit leaves a harness that runs four real steps and passes. Reaching
#      further back (e.g. `main`'s tip, 2026-06-28) produces a scaffold whose
#      surviving old `check.py` prints "No checks defined for gate DevStg-Reqs" and exits
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


def _adopter_git(root, *args):
    """Run Git in a temporary adopter and return stdout, failing verbosely."""
    proc = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


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
    """Scaffold from the pinned old kit, then run the documented steps forward.

    Module-scoped: the chain is four bootstraps' worth of subprocesses and every
    test in this file interrogates the SAME run, which is also what makes the
    assertions comparable (they describe one re-sync, not four).

    The steps below are exactly what RESYNC_PACK.md §1 documents TODAY, in
    its order, and nothing else — no repair the pack does not tell an adopter
    to perform. That restraint is the point: if the documented procedure is
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

    # (b) The pack's §1.3 step 2: re-run the CURRENT kit's bootstrap in place.
    plain = run_py([SCRIPTS / "bootstrap.py", "--dest", "."], cwd=repo)
    assert plain.returncode == 0, plain.stdout + plain.stderr

    # (c) Pack §2.2 "Regenerate, never raw-copy": the process docs are generated from
    # the recorded docs/kit-profile, so taking the new ones means deleting them
    # and re-running — the ONE documented way a re-sync updates a file it has.
    for rel in PROCESS_DOCS:
        (repo / rel).unlink()
    regen = run_py([SCRIPTS / "bootstrap.py", "--dest", "."], cwd=repo)
    assert regen.returncode == 0, regen.stdout + regen.stderr
    after = _digests(repo, PROCESS_DOCS)

    # (d) Pack §1.3 step 6: refresh materialized per-agent skill copies.
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
    # The bar is passed in the RETIRED vocabulary, deliberately. The re-synced
    # repo still carries its OLD check.py — that is this module's whole premise,
    # stated in the docstring above — and that binary knows only the retired
    # tags. Passing the canonical `DevStg-Reqs` here would test the CURRENT kit's
    # argparse against a scaffold that does not have it, and would hide the thing
    # worth pinning: OI-21's conversion did not break a re-synced adopter whose
    # harness predates it. When re-sync becomes overwrite-capable for check.py,
    # this reverts to the canonical name and the alias path is proven by
    # tests/test_check_harness.py instead.
    retired_bar = "G1"  # check_vocab: allow
    proc = run_py(["scripts/check.py", "--gate", retired_bar], cwd=resync.repo)
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
    """The delete-then-re-run recipe (pack §2.2) is the one documented path by which a
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
    retired. Everything else in the pack is an operator's hand-work, which SR-036
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
    #    the pack's "delete your old scripts/<x>.py" entries are load-bearing.
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


def test_force_resync_installs_current_checkers_and_the_tree_cannot_false_green(
    resync, tmp_path
):
    """The OTHER half of the procedure — the wholesale overwrite — with --force.

    The add-only leg above proves the DOCUMENTED DEFAULT and pins its known
    dishonest green (the surviving old checkers approve a tree the current kit
    refuses). This leg proves the overwrite path: after `bootstrap.py --force`
    plus the documented `--migrate-config`, the tree's checkers ARE current —
    so whatever they report is the CURRENT kit's honest verdict on a
    July-era scaffold, and the one outcome this test forbids is a green that
    hides un-run migrations (SN-008 one level up, the adversarial round's
    point). Either the current harness runs green with substance, or it
    refuses LOUDLY naming what a re-sync still owes — both are honest; silence
    is the defect.
    """
    repo = tmp_path / "force-resynced"
    shutil.copytree(resync.pristine, repo)
    forced = run_py([SCRIPTS / "bootstrap.py", "--dest", ".", "--force"], cwd=repo)
    assert forced.returncode == 0, forced.stdout + forced.stderr
    migrated = run_py(
        [SCRIPTS / "bootstrap.py", "--dest", ".", "--migrate-config"], cwd=repo
    )
    assert migrated.returncode == 0, migrated.stdout + migrated.stderr

    # The overwritten checkers must BE the current kit's, byte-for-byte —
    # otherwise this leg proves nothing about the current verdict.
    for rel in ("scripts/check.py", "scripts/trace.py"):
        assert (repo / rel).read_bytes() == (SCRIPTS.parent / rel).read_bytes(), (
            "--force left a stale kit-owned checker in place: " + rel
        )

    verdict = run_py(["scripts/trace.py", "--strict-integrity"], cwd=repo)
    out = verdict.stdout + verdict.stderr
    if verdict.returncode == 0:
        # Honest green: the current integrity floor really passed — require
        # substance so a vacuous pass cannot slip through as approval.
        assert "orphans=0" in out or "integrity=0" in out, (
            "green with no substance is the false green this test exists "
            "to refuse:\n" + out
        )
    else:
        # Honest red: the refusal must NAME what is owed, so the operator
        # is routed to the migration rather than left with a bare exit code.
        assert out.strip(), "a silent nonzero teaches nothing:\n" + out


def test_fresh_node_scaffold_generates_its_required_prompt_catalog(tmp_path):
    """The Node profile ships the generator its mandatory freshness step needs."""
    repo = tmp_path / "fresh-node-adopter"
    scaffold = run_py(
        [SCRIPTS / "bootstrap.py", "--dest", repo, "--stack", "node"], cwd=tmp_path
    )
    assert scaffold.returncode == 0, scaffold.stdout + scaffold.stderr
    assert (repo / "scripts/gen_prompt_catalog.py").is_file()
    catalog = run_py(["scripts/gen_prompt_catalog.py", "--check"], cwd=repo)
    assert catalog.returncode == 0, catalog.stdout + catalog.stderr
    harness = run_py(
        ["scripts/check.py", "--stage", "DevStg-Needs", "--tier", "smoke"], cwd=repo
    )
    assert harness.returncode == 0, harness.stdout + harness.stderr
    assert "PASS  prompt-catalog" in harness.stdout


def test_node_adopter_upgrade_preserves_populated_owner_content(resync, tmp_path):
    """A populated non-Python adopter survives the documented target re-sync.

    This is deliberately a copy of the archived old-kit scaffold, not a fresh
    current fixture: the target bootstrap must encounter an adopter's existing
    README, legacy SN/SR carriers, application, Node harness configuration and
    recorded history.  It adds the current hats carrier as owner-authored text
    before the first target run, then proves that neither the initial add-only
    re-sync, the profile-driven process-doc regeneration, nor ``--sync``
    replaces any of those records.

    A second copy follows the full documented overwrite, then explicitly merges
    the owner-controlled application, README, hats, stack config, work record,
    and history before it migrates the carriers and policy file.
    """
    repo = tmp_path / "node-adopter-upgrade"
    shutil.copytree(resync.pristine, repo)

    owner_content = {
        "README.md": """# Signal Triage\n\n## Vision\n\n**PROJECT-VISION:** Dispatch teams shall see a trustworthy incident timeline\nfrom browser-collected signals without losing the source or confidence of an\nevent.\n\n## What it does\n\n- **Incident timeline** — responders inspect the ordered browser signals (SN-701).\n\n## Migration record\n\n[Source-confidence note](docs/adopter-notes.md)\n""",
        "docs/requirements/hats.toml": """[hat.DATA-PROVENANCE]\napplies_when = 'tags contains "telemetry"'\nasks = "Can a responder distinguish reported events from inferred events?"\nlistens_for = "A timeline that makes uncertain or derived events appear authoritative."\n""",
        "src/timeline.js": """export function label(event) {\n  return `${event.source}: ${event.message}`;\n}\n""",
        "test/timeline.test.js": """import assert from "node:assert/strict";\nimport test from "node:test";\n\nimport { label } from "../src/timeline.js";\n\ntest("labels an event with its source", () => {\n  assert.equal(\n    label({ source: "sensor", message: "threshold crossed" }),\n    "sensor: threshold crossed"\n  );\n});\n""",
        "package.json": """{\n  "name": "signal-triage",\n  "private": true,\n  "type": "module",\n  "scripts": {"test": "node --test"}\n}\n""",
        "docs/stack.ini": """[paths]\nsrc = src\ntests = test\n\n[product]\nformat = npx --no-install prettier --check {src} {tests}\nlint = npx --no-install eslint {src} {tests}\ntest = node --test\n\n[tiers]\nsmoke = test/smoke\nfull =\nrelease =\nall =\n\n[coverage]\nthreshold = 0\nargs =\n\n[arch-map]\nmode = files\n""",
    }
    for rel, text in owner_content.items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    project_owned_note = "docs/adopter-notes.md"
    (repo / project_owned_note).write_text(
        "# Source-confidence migration note\n\n"
        "The incident label fulfills [SR-701](requirements/system-requirements.csv).\n",
        encoding="utf-8",
    )
    unfinished = "docs/work/draft/WI-701-source-confidence.md"
    (repo / unfinished).parent.mkdir(parents=True, exist_ok=True)
    (repo / unfinished).write_text(
        "+++\n"
        'id = "WI-701"\n'
        'title = "Preserve source-confidence review"\n'
        'workstream = "adopter"\n'
        'sr_refs = ["SR-701"]\n'
        'safety_class = "ordinary"\n'
        "+++\n\n"
        "## Deliverable\n",
        encoding="utf-8",
    )

    # These are the older kit's actual carrier formats, populated rather than
    # replaced with target templates. A resync must preserve their records and
    # leave their conversion to the explicit migration review.
    legacy_sn = repo / "docs/requirements/stakeholder-needs.md"
    legacy_sn.write_text(
        legacy_sn.read_text(encoding="utf-8").replace(
            "\n## Edge-case expectations",
            "\n| SN-701 | Responders need each event's source and confidence. | "
            "Wrong triage costs time. | M | A timeline labels source and confidence. |\n"
            "\n## Edge-case expectations",
        ),
        encoding="utf-8",
    )
    legacy_sr = repo / "docs/requirements/system-requirements.csv"
    legacy_sr.write_text(
        legacy_sr.read_text(encoding="utf-8")
        + '\nSR-701,Label incident provenance,SN-701,"The system shall retain an '
        'event source and confidence.","Responders must distinguish evidence '
        'from inference.","A test reads both fields.",,M,Test,Drafted,,telemetry\n',
        encoding="utf-8",
    )
    history = repo / "docs/log.md"
    history.write_text(
        history.read_text(encoding="utf-8")
        + "\n## 2026-09-06 — source-confidence decision\n\n"
        "The owner retained source and confidence in incident evidence.\n",
        encoding="utf-8",
    )
    _adopter_git(repo, "init", "-q")
    _adopter_git(repo, "config", "user.email", "adopter@example.invalid")
    _adopter_git(repo, "config", "user.name", "Temporary Adopter")
    _adopter_git(repo, "add", "-A")
    _adopter_git(repo, "commit", "-qm", "adopter: record incident evidence")
    initial_commit = _adopter_git(repo, "rev-parse", "HEAD").strip()
    preserved = _digests(
        repo,
        tuple(owner_content)
        + (
            "docs/requirements/stakeholder-needs.md",
            "docs/requirements/system-requirements.csv",
            "docs/log.md",
            project_owned_note,
            unfinished,
        ),
    )

    # The first current-kit run is the documented one-time profile declaration
    # for an older adopter. Its target stack is Node, but it must not overwrite
    # the adopter's selected toolchain or any other existing content.
    initial = run_py(
        [SCRIPTS / "bootstrap.py", "--dest", ".", "--stack", "node"], cwd=repo
    )
    assert initial.returncode == 0, initial.stdout + initial.stderr
    assert "stack=node" in (repo / "docs/kit-profile").read_text(encoding="utf-8")

    # RESYNC_PACK's documented regeneration route takes only generated process
    # documents. The recorded Node profile must be used when flags are omitted.
    for rel in PROCESS_DOCS:
        path = repo / rel
        if path.exists():
            path.unlink()
    regenerate = run_py([SCRIPTS / "bootstrap.py", "--dest", "."], cwd=repo)
    assert regenerate.returncode == 0, regenerate.stdout + regenerate.stderr
    sync = run_py([SCRIPTS / "bootstrap.py", "--dest", ".", "--sync"], cwd=repo)
    assert sync.returncode == 0, sync.stdout + sync.stderr

    assert _digests(repo, preserved) == preserved
    assert (repo / "docs/process.md").is_file()
    assert (repo / "docs/process-options.md").is_file()
    assert "mode = files" in (repo / "docs/stack.ini").read_text(encoding="utf-8")
    # The historic Python artefact is intentionally not silently removed by a
    # Node-profile re-sync; current bootstrap only skips creating a new one.
    assert (repo / "pytest.ini").is_file()

    _adopter_git(repo, "add", "-A")
    _adopter_git(repo, "commit", "-qm", "resync: record Node profile")

    # The migration is deliberately on a copy. Take the complete current kit
    # mapping first, then restore the owner-controlled records before converting
    # carriers. This is the documented overwrite plus intentional owner merge,
    # rather than a script-only update that leaves stale kit documents behind.
    # This leg does NOT test preservation: the byte-restore below is the test's
    # own operator step. What it proves is that the documented overwrite plus
    # carrier conversion leaves the restored files alone and lands a green
    # current harness. The add-only leg above is the preservation oracle.
    supported = tmp_path / "node-adopter-supported"
    shutil.copytree(repo, supported)
    forced = run_py(
        [SCRIPTS / "bootstrap.py", "--dest", ".", "--force", "--stack", "node"],
        cwd=supported,
    )
    assert forced.returncode == 0, forced.stdout + forced.stderr
    restored = tuple(owner_content) + (
        "docs/requirements/stakeholder-needs.md",
        "docs/requirements/system-requirements.csv",
        "docs/log.md",
        project_owned_note,
        unfinished,
    )
    for rel in restored:
        (supported / rel).write_bytes((repo / rel).read_bytes())
    assert (supported / unfinished).read_bytes() == (repo / unfinished).read_bytes()

    # The note is project-owned. Its legacy carrier link therefore survives the
    # overwrite and is retargeted explicitly by the operator after conversion.
    note = supported / project_owned_note
    assert "requirements/system-requirements.csv" in note.read_text(encoding="utf-8")
    catalogue = run_py(["scripts/gen_prompt_catalog.py"], cwd=supported)
    assert catalogue.returncode == 0, catalogue.stdout + catalogue.stderr

    checked = run_py(
        ["scripts/migrate_carrier.py", "--root", ".", "--check"], cwd=supported
    )
    assert checked.returncode == 0, checked.stdout + checked.stderr
    migrated = run_py(["scripts/migrate_carrier.py", "--root", "."], cwd=supported)
    assert migrated.returncode == 0, migrated.stdout + migrated.stderr
    converted = []
    for line in migrated.stdout.splitlines():
        if line.startswith("migrate_carrier: ") and " -> " in line:
            converted.append(line.removeprefix("migrate_carrier: ").split(" -> ", 1)[0])
    assert converted, migrated.stdout + migrated.stderr
    _adopter_git(supported, "add", "-A")
    _adopter_git(supported, "rm", "-q", *converted, "pytest.ini")

    # A legacy policy is deliberately introduced only on the migration copy so
    # this focused arm proves the explicit CLI conversion itself, rather than
    # relying on the earlier full bootstrap pass that also invokes it.
    (supported / "docs/review-policy").write_text("2\n", encoding="utf-8")
    config = run_py(
        [SCRIPTS / "bootstrap.py", "--dest", ".", "--migrate-config"], cwd=supported
    )
    assert config.returncode == 0, config.stdout + config.stderr
    assert not (supported / "docs/review-policy").exists()
    assert (
        tomllib.loads((supported / "docs/process.toml").read_text(encoding="utf-8"))[
            "policies"
        ]["review_rounds"]
        == 2
    )

    needs = tomllib.loads(
        (supported / "docs/requirements/stakeholder-needs.toml").read_text(
            encoding="utf-8"
        )
    )["need"]
    requirements = tomllib.loads(
        (supported / "docs/requirements/system-requirements.toml").read_text(
            encoding="utf-8"
        )
    )["requirement"]
    assert needs["SN-701"]["status"] == "Approved"
    assert (
        needs["SN-701"]["need"] == "Responders need each event's source and confidence."
    )
    assert requirements["SR-701"]["sn_refs"] == ["SN-701"]
    assert requirements["SR-701"]["status"] == "Drafted"
    assert _digests(supported, tuple(owner_content) + ("docs/log.md",)) == _digests(
        repo, tuple(owner_content) + ("docs/log.md",)
    )
    note.write_text(
        note.read_text(encoding="utf-8").replace(
            "requirements/system-requirements.csv",
            "requirements/system-requirements.toml",
        ),
        encoding="utf-8",
    )
    assert "requirements/system-requirements.toml" in note.read_text(encoding="utf-8")

    watermark = run_py(["scripts/trace.py", "--bump-ids"], cwd=supported)
    assert watermark.returncode == 0, watermark.stdout + watermark.stderr

    # The preserved application's own test is the one step that needs Node; a
    # box without it must still drive every kit-side assertion below rather
    # than skipping the whole leg (the kit half is what this module is for).
    node, npm = shutil.which("node"), shutil.which("npm")
    product_ran = False
    if node and npm:
        product = subprocess.run(
            [npm, "test"], cwd=supported, capture_output=True, text=True
        )
        assert product.returncode == 0, product.stdout + product.stderr
        product_ran = True

    _adopter_git(supported, "commit", "-m", "resync: migrate carrier")
    final_commit = _adopter_git(supported, "rev-parse", "HEAD").strip()
    _adopter_git(supported, "merge-base", "--is-ancestor", initial_commit, final_commit)
    assert "PROJECT-VISION:" in _adopter_git(
        supported, "show", initial_commit + ":README.md"
    )
    assert "source-confidence decision" in _adopter_git(
        supported, "show", initial_commit + ":docs/log.md"
    )

    integrity = run_py(["scripts/trace.py", "--strict-integrity"], cwd=supported)
    assert integrity.returncode == 0, integrity.stdout + integrity.stderr
    harness = run_py(
        ["scripts/check.py", "--stage", "DevStg-Needs", "--tier", "smoke"],
        cwd=supported,
    )
    harness_output = harness.stdout + harness.stderr
    assert harness.returncode == 0, harness_output
    assert "PASS  registry-integrity" in harness_output
    assert "PASS  doc-navigability" in harness_output
    assert "PASS  prompt-catalog" in harness_output

    docs = run_py(["scripts/check_docs.py", "--root", "."], cwd=supported)
    docs_output = docs.stdout + docs.stderr
    assert docs.returncode == 0, docs_output
    if not product_ran:
        pytest.skip(
            "Node/npm unavailable; kit assertions ran, the preserved application test did not"
        )
