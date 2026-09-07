"""Atomic, turn-bound primary adjudication publication.

Contracts: IF-180

Contract IF-180: carrier_candidate(root, rev) -> candidate commit or None;
    verdict_reader exposes the shared verdict API bound to that query.
    The exact commit must carry the immutable turn and pass the completion
    verifier's full reconstruction, parent, receipt and author checks. Missing
    or invalid proof returns None; callers retain the unmapped identity and
    therefore owe review. Successful proofs are cached only in this process.
    Replay may create temporary checkouts and run their bar;
    the query imports no objects and changes no primary ref, index or working tree. This is
    a read-only identity query, never permission to reset away the publication.
"""

from __future__ import annotations

import inspect
import json
import re
import subprocess
import sys
import tempfile
from functools import partial
from pathlib import Path

from kitlib import verdict

import baseline_snapshot
import intake
import primary_approval
import primary_close
import primary_turn
import publication_verify

TRAILER = "Primary-Publication-Turn: "
# A Git commit and the serialized immutable turn completely identify a replay.
# Cache only successful proofs in this process; restart audits them again.
_VERIFIED_PUBLICATIONS = set()


def _git(root, *args, check=True):
    p = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if check and p.returncode:
        raise RuntimeError((p.stdout or "") + (p.stderr or ""))
    return p.stdout.strip()


def _project(root, turn, candidate, tier="all", harness_root=None):
    primary_turn.validate_candidate(root, turn, candidate)
    plan, refusal = primary_approval.approval_projection(root, turn, candidate)
    if refusal:
        return None, None, refusal
    refusal = _apply_approval(root, candidate, plan)
    if refusal:
        return None, None, refusal
    closed, drafts, refusal = primary_close.stage_primary_adjudication(
        root, turn["spec"], judgment_path=plan["judgment"]
    )
    if refusal:
        return None, None, refusal
    minted, refusal = intake.stage_mint(
        root, drafts, "primary adjudication {}".format(turn["wi"])
    )
    if refusal:
        return None, None, refusal
    step = next(
        (
            Path(root) / rel
            for rel in (
                "scripts/trunk_step.py",
                "project-trajectory/scripts/trunk_step.py",
            )
            if (Path(root) / rel).is_file()
        ),
        None,
    )
    if step is None:
        return None, None, "trunk_step.py is absent from the candidate"
    p = subprocess.run(
        [sys.executable, str(step), "--root", ".", "--regen"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if p.returncode:
        return None, None, "regeneration failed: " + (p.stdout + p.stderr)[-2000:]
    _git(root, "add", "-A")
    product_bar = _outside_adjudication_scope(root)
    if product_bar:
        green, _out, why = publication_verify.run_bar(
            Path(root), Path(harness_root or root), tier
        )
        if not green:
            return None, None, why
        _git(root, "add", "-A")
    plan["verification"] = {
        "mode": "product-bar" if product_bar else "scope-no-product-bar",
        "paths": _git(root, "diff", "--cached", "--name-only").splitlines(),
        "result": "pass",
    }
    return closed, plan, None


def _apply_approval(root, candidate, plan):
    statuses = plan.get("statuses") or {}
    for rel, rows in statuses.items():
        live = Path(root) / rel
        refusal = intake._rewrite_toml_statuses(live, rel, list(rows))
        if refusal:
            return refusal
    if statuses or plan.get("approves"):
        # Snapshot prose carries a date. Bind it to the reviewed candidate's
        # commit date so completion replay tomorrow derives identical bytes.
        publication_day = _git(root, "show", "-s", "--format=%cs", candidate)
        clock = baseline_snapshot._today
        try:
            baseline_snapshot._today = lambda: publication_day
            approves = plan.get("approves") or {}
            baseline_snapshot.copy_live(root, approves=approves, exact_rels=approves)
        except SystemExit as exc:
            return "snapshot copy refused: {}".format(exc)
        finally:
            baseline_snapshot._today = clock
    return None


def _outside_adjudication_scope(root):
    changed = _git(root, "diff", "--cached", "--name-only").splitlines()
    allowed = (
        list(publication_verify.ADJUDICATION_SURFACES)
        + [baseline_snapshot.SNAPSHOT_DIR + "/", "docs/id-watermark"]
        + publication_verify.generated_paths(Path(root))
    )
    return not all(
        any(
            p == a.rstrip("/") or (a.endswith("/") and p.startswith(a)) for a in allowed
        )
        for p in changed
    )


def derive_tree(root, turn, candidate="HEAD", tier="all", *, import_objects=True):
    """Independently replay the exact publication and return its tree and plan."""
    root = Path(root).resolve()
    try:
        cand = _git(root, "rev-parse", candidate)
        with tempfile.TemporaryDirectory(prefix="primary-publication-") as td:
            scratch = Path(td) / "repo"
            _git(root, "clone", "--shared", "--no-checkout", str(root), str(scratch))
            _git(scratch, "checkout", "--detach", cand)
            closed, plan, refusal = _project(scratch, turn, cand, tier, root)
            if refusal:
                return None, None, None, refusal
            tree = _git(scratch, "write-tree")
            if import_objects:
                # Import newly-written blobs/tree before the disposable object store
                # disappears. A temporary commit makes the object closure fetchable;
                # no primary ref is advanced.
                carrier = _git(
                    scratch, "commit-tree", tree, "-p", cand, "-m", "projection carrier"
                )
                _git(root, "fetch", "--no-tags", str(scratch), carrier)
        return tree, closed, plan, None
    except (KeyError, OSError, RuntimeError, ValueError) as exc:
        return None, None, None, str(exc)


def _subject(turn):
    return "adjudicate: {} primary publication".format(turn["wi"])


def publish(root, turn, candidate="HEAD", tier="all"):
    """Replay, verify and atomically commit one publication; lock is caller-held."""
    root = Path(root).resolve()
    cand = None
    installed = False
    try:
        cand = _git(root, "rev-parse", candidate)
        if cand != _git(root, "rev-parse", "HEAD") or _git(
            root, "status", "--porcelain"
        ):
            return None, "primary is not clean at the exact candidate"
        primary_turn.validate(root, turn, cand)
        tree, closed, plan, refusal = derive_tree(root, turn, cand, tier)
        if refusal:
            return None, refusal
        _git(root, "read-tree", "--reset", "-u", tree)
        installed = True
        if _git(root, "write-tree") != tree:
            raise ValueError("installed projection differs from verified tree")
        author = (plan or {}).get("author") or {}
        if not author:
            raise ValueError("publication has no verified adjudicator author")
        env = dict(
            __import__("os").environ,
            GIT_AUTHOR_NAME=author["name"],
            GIT_AUTHOR_EMAIL=author["email"],
        )
        msg = "{}\n\n{}{}\nPublication-Candidate: {}\nPublication-Tree: {}".format(
            _subject(turn), TRAILER, turn["turn"], cand, tree
        )
        msg += "\nPublication-Verification: " + json.dumps(
            plan["verification"], sort_keys=True
        )
        p = subprocess.run(
            ["git", "-C", str(root), "commit", "-m", msg],
            env=env,
            capture_output=True,
            text=True,
        )
        if p.returncode:
            _git(root, "reset", "--hard", cand)
            installed = False
            return None, "publication commit failed: " + (p.stdout + p.stderr)[-2000:]
        if _git(root, "rev-parse", "HEAD^{tree}") != tree:
            raise ValueError("publication commit tree differs from the verified tree")
        return closed, None
    except (KeyError, OSError, RuntimeError, ValueError) as exc:
        if installed and cand:
            try:
                _git(root, "reset", "--hard", cand)
            except RuntimeError as restore:
                return None, "{}; primary restore failed: {}".format(exc, restore)
        return None, str(exc)


def publication_commit(root, turn):
    """Verified reachable publication carrier for a durable turn, else None."""
    token = TRAILER + str(turn.get("turn", ""))
    out = _git(
        root, "log", "--format=%H", "--fixed-strings", "--grep=" + token, check=False
    )
    return next(
        (rev for rev in out.splitlines() if _verified_candidate(root, turn, rev)), None
    )


def _verified_candidate(root, turn, rev):
    """One exact carrier proof shared by completion and governing identity."""
    token = TRAILER + str(turn.get("turn", ""))
    proof = (str(Path(root).resolve()), rev, json.dumps(turn, sort_keys=True))
    if proof in _VERIFIED_PUBLICATIONS:
        return _git(root, "rev-parse", rev + "^1")
    body = _git(root, "show", "-s", "--format=%B", rev)
    if body.partition("\n")[0] != _subject(turn):
        return None
    if [line for line in body.splitlines() if line.startswith(TRAILER)] != [token]:
        return None
    tree = _git(root, "show", "-s", "--format=%T", rev)
    match = re.search(r"(?m)^Publication-Candidate: ([0-9a-f]{40})$", body)
    if not match:
        return None
    if _git(root, "show", "-s", "--format=%P", rev) != match.group(1):
        return None
    expected, _closed, plan, refusal = derive_tree(
        root, turn, match.group(1), import_objects=False
    )
    if refusal or expected != tree:
        return None
    receipt = "Publication-Verification: " + json.dumps(
        plan["verification"], sort_keys=True
    )
    if receipt not in body.splitlines():
        return None
    author = _git(root, "show", "-s", "--format=%an%x00%ae", rev).split("\0")
    wanted = (plan or {}).get("author") or {}
    if not wanted or author != [wanted.get("name"), wanted.get("email")]:
        return None
    spec = Path(str(turn.get("spec", ""))).name
    homes = ("docs/work/complete/" + spec, "docs/archive/work/complete/" + spec)
    if any(
        _git(root, "ls-tree", "-r", "--name-only", rev, "--", home) for home in homes
    ):
        _VERIFIED_PUBLICATIONS.add(proof)
        return _git(root, "rev-parse", rev + "^1")
    return None


def carrier_candidate(root, rev):
    """Read-only mapping of this exact verified publication, never a reset peel."""
    try:
        rev, body = _git(root, "show", "-s", "--format=%H%x00%B", rev).split("\0", 1)
        matches = re.findall(
            r"(?m)^Primary-Publication-Turn: (WI-[0-9]+-[0-9a-f]{40})$", body
        )
        if len(matches) != 1:
            return None
        path = primary_turn.RECORDS + "/" + matches[0] + "/turn.toml"
        turn = primary_turn.parse_record(_git(root, "show", rev + ":" + path), path)
        return _verified_candidate(root, turn, rev)
    except (KeyError, OSError, RuntimeError, ValueError, TypeError):
        return None


def completed(root, turn):
    return publication_commit(root, turn) is not None


def pending(root):
    """One unfinished committed selection, or None; malformed/duplicate refuses."""
    root = Path(root)
    found = []
    for path in sorted((root / primary_turn.RECORDS).glob("*/turn.toml")):
        turn = primary_turn._read_record(root, path)
        if not completed(root, turn):
            found.append(turn)
    if len(found) > 1:
        raise ValueError(
            "multiple unfinished primary adjudications: "
            + ", ".join(turn["wi"] for turn in found)
        )
    return found[0] if found else None


def writer_refusal(root):
    """A durable pending turn owns the primary writer even between processes."""
    try:
        turn = pending(root)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return "primary adjudication selection is unreadable: {}".format(exc)
    if turn:
        return "primary adjudication {} is pending; resume it before another writer".format(
            turn["wi"]
        )
    return None


class _CarrierReader:
    """Bind one verifier into the shared algorithm without reversing imports."""

    def __getattr__(self, name):
        value = getattr(verdict, name)
        if (
            inspect.isfunction(value)
            and "carrier" in inspect.signature(value).parameters
        ):
            return partial(value, carrier=carrier_candidate)
        return value


verdict_reader = _CarrierReader()
