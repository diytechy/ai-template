"""Record the test evidence — the harness driver that makes `DevStg-Release`
reachable (WI-500).

    python scripts/record_test_evidence.py [--tier full] [--root .]
    python scripts/record_test_evidence.py --check      # does the record hold?
    python scripts/record_test_evidence.py --dry-run    # what would be written

WHAT THIS IS. `DevStg-Release` is the rung a repo earns when every declared test
case PASSES. That is a claim about a harness run, and OI-30 D2 rules that no
Status cell and no hand-written file may ever be its source — so until this
driver existed the rung was returned by nothing, deliberately (WI-498 slice 3).
This script is the only sanctioned producer: it RUNS the declared bar itself,
through the documented harness entry point, and writes `docs/test/evidence` only
if that run exits 0. There is no flag that writes the record without running the
suite, and none that records a failure: a failing run leaves the previous state
untouched and says so.

WHY IT WRAPS `check.py` INSTEAD OF BEING A CHECK STEP. The evidence is a verdict
ABOUT the whole harness run, so it can only be written by something that outlives
that run — a step inside the plan would be recording a verdict it is itself part
of. Wrapping is also what keeps the definition of "the declared bar" in ONE home:
this driver names no test command, it names a TIER declared in `docs/stack.ini`
and lets `check.py` expand it, exactly as CI does.

THE TIER RULE. Only a whole-suite tier may carry the claim
(`kitlib.evidence.WHOLE_SUITE_TIERS`); `smoke` is a declared SUBSET, so a record
naming it would be a weaker sentence in the same field. Refused here at the
writer AND again at the reader, because the file is committed state and a
consumer must not have to trust its writer.

WHY THE RECORD IS COMMITTED, AND WHY CI DOES NOT WRITE IT. The rung is a
statement the repository makes about itself, so its evidence has to be reviewable
history like every other approving act in this kit — a value in a run log
evaporates, and a hosted runner committing back would need write credentials, a
bot identity, and a lane no reviewer signs. So the human (or the agent under the
usual gates) runs this, reads the record, and commits it. CI's half needs no new
machinery: because the record is a declared stage input and the stage fingerprint
covers the source surface it binds to, a stale record already reds
`derive_stage --check` wherever that step runs.

STALENESS IS NOT THIS SCRIPT'S JOB TO FORGIVE. `--check` reports the verdict and
exits nonzero when the committed record does not hold. The fix is to re-run the
suite or delete the record — never to edit the binding.

Python 3.11+, stdlib only; Windows + POSIX.
"""

import argparse
import datetime
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from kitlib import config as kitconfig  # noqa: E402
from kitlib import evidence as kitevidence  # noqa: E402
from kitlib import git as kitgit  # noqa: E402
from kitlib import stage as kitstage  # noqa: E402

DEFAULT_TIER = "full"


def harness_command(root, tier):
    """The harness invocation this driver runs, as an argv list.

    THE DOCUMENTED ENTRY POINT, NOT A TEST COMMAND. `check.py --tier <t>` is what
    the guide, the hooks and the shipped CI all invoke; naming pytest here would
    mint a second definition of passing, which is the drift SR-151/SR-152 exist to
    forbid.

    The harness is this script's own SIBLING, not `<root>/scripts/check.py`: in a
    scaffold those are the same file, and in the kit's own meta-repo (scripts one
    level down, root one level up) only the sibling reading is right."""
    return [sys.executable, str(harness_path()), "--tier", tier]


def harness_path():
    """The harness this driver drives. Split from the argv builder so `main` can
    check that it EXISTS without having to parse an argv a test may have
    substituted — the presence check is about the shipped kit, not about whatever
    command is being run."""
    return Path(__file__).resolve().parent / "check.py"


def _command_text(root, argv):
    """The invocation as the record should quote it — repo-relative and
    interpreter-agnostic, so the same run on Windows and POSIX writes the same
    line and the record does not change because someone's venv moved."""
    parts = ["python"]
    for item in argv[1:]:
        text = str(item)
        try:
            text = Path(text).resolve().relative_to(Path(root).resolve()).as_posix()
        except (ValueError, OSError):
            pass
        parts.append(text)
    return " ".join(parts)


def build_record(root, tier, command_text):
    """The record for a green run on the tree at `root`."""
    return {
        "outcome": kitevidence.PASS,
        "tier": tier,
        "command": command_text,
        "revision": (
            kitgit.git_out(root, ["rev-parse", "--short", "HEAD"]) or ""
        ).strip()
        or "no-git",
        "binding": kitstage.evidence_binding(root, memo=None),
    }


def _refuse_without_a_surface(root):
    """The one precondition. A binding over an EMPTY source surface would be a
    digest of nothing — it would match forever and bind to nothing, which is worse
    than no record at all, so an undeclared or empty `[paths]` is refused by name.

    THE COUNT IS COMPARED AGAINST ONE, not zero: `docs/stack.ini` folds itself in
    (it declares the bar), so a surface that resolved to nothing at all still
    hashes one file. Testing for "non-empty" would have accepted exactly the state
    this refuses."""
    if kitevidence.source_paths(root) and len(kitevidence.source_files(root)) > 1:
        return None
    return (
        "record_test_evidence: REFUSED — {} declares no [paths] src/tests surface "
        "with any files in it, so the evidence could not be bound to anything. "
        "Declare the product source and test paths there first.".format(
            kitevidence.STACK_FILE
        )
    )


def main(argv=None):
    kitconfig.utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    ap.add_argument(
        "--tier",
        default=DEFAULT_TIER,
        help="the declared whole-suite tier to run (default: {}); one of {}".format(
            DEFAULT_TIER, ", ".join(kitevidence.WHOLE_SUITE_TIERS)
        ),
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="report whether the committed record still holds; exit 1 if not",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="print the record a green run would write; run nothing, write nothing",
    )
    args = ap.parse_args(argv)
    root = Path(args.root)

    if args.check:
        holds, reason = kitstage.evidence_verdict(root, memo=None)
        print(
            "record_test_evidence: {} — {}".format("HOLDS" if holds else "NO", reason)
        )
        return 0 if holds else 1

    if args.tier not in kitevidence.WHOLE_SUITE_TIERS:
        print(
            "record_test_evidence: REFUSED — tier {!r} is not a whole-suite tier "
            "({}). A partial tier cannot carry the claim that EVERY declared test "
            "case passed.".format(args.tier, ", ".join(kitevidence.WHOLE_SUITE_TIERS)),
            file=sys.stderr,
        )
        return 2

    refusal = _refuse_without_a_surface(root)
    if refusal:
        print(refusal, file=sys.stderr)
        return 2

    argv_cmd = harness_command(root, args.tier)
    command_text = _command_text(root, argv_cmd)

    if args.dry_run:
        print("record_test_evidence: would run: {}".format(command_text))
        print(kitevidence.field_block(build_record(root, args.tier, command_text)))
        return 0

    if not harness_path().exists():
        print(
            "record_test_evidence: {} is missing — re-sync the kit scripts".format(
                harness_path().name
            ),
            file=sys.stderr,
        )
        return 2

    print("record_test_evidence: running {}".format(command_text))
    proc = subprocess.run(argv_cmd, cwd=str(root))
    if proc.returncode != 0:
        print(
            "record_test_evidence: the harness exited {} — NOTHING WRITTEN. The "
            "record only ever states a pass, so a red run leaves the committed "
            "state exactly as it was.".format(proc.returncode),
            file=sys.stderr,
        )
        return 1

    # THE BINDING IS COMPUTED AFTER THE RUN, deliberately: it must describe the
    # tree the suite actually executed against, and an edit made DURING the run
    # then shows up as a record that does not hold rather than as one that
    # silently claims the pre-edit tree. `memo=None` skips the digest memo — this
    # process hashes each file once and a stale memo entry here would be a
    # falsified claim.
    record = build_record(root, args.tier, command_text)
    path = root / kitevidence.EVIDENCE_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        kitevidence.render(record, datetime.date.today().isoformat()),
        encoding="utf-8",
        newline="\n",
    )
    print(
        "record_test_evidence: wrote {} (tier {}, binding {}).\n"
        "  Regenerate docs/stage (python scripts/derive_stage.py) and commit both.".format(
            kitevidence.EVIDENCE_FILE, args.tier, record["binding"]
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
