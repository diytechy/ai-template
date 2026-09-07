"""Immutable primary-turn Git bindings; no session engine or publication writer."""

import re
import tomllib
from pathlib import Path

import agent_common as ac
import baseline_snapshot
from check_docs import blank_fenced
from kitlib import git as kgit
from kitlib import verdict

RECORDS = "docs/reviews/primary"
_TURN = re.compile(r"WI-[0-9]+-[0-9a-f]{40}\Z")
_FIELDS = {
    "version",
    "turn",
    "wi",
    "base",
    "primary_branch",
    "primary_root",
    "proposal_spec_blob",
    "scope",
    "registry_blobs",
    "approved_blobs",
    "spec",
}


def record_path(turn):
    return "{}/{}/turn.toml".format(RECORDS, turn["turn"])


def _required_git(root, *args):
    value = kgit.git_out(root, args)
    if value is None:
        raise ValueError("cannot read primary Git binding: {}".format(" ".join(args)))
    return value.strip()


def registry_blobs(root, rev, prefix=""):
    """Exact carrier objects at a revision, including absent-file identity."""
    paths = [prefix + rel for rel in baseline_snapshot.SNAPSHOTTED]
    paths += [str(Path(p).with_suffix(".csv")) for p in paths]
    paths.append(prefix + str(Path(baseline_snapshot.NEEDS_REL).with_suffix(".md")))
    listing = _required_git(root, "ls-tree", "-r", rev, "--", *paths)
    return {
        path: meta.split()[2]
        for line in listing.splitlines()
        for meta, path in [line.split("\t", 1)]
    }


def _primary_identity(root):
    primary = kgit.primary_worktree_root(root)
    if primary is None or kgit.is_linked_worktree(root) or not primary.samefile(root):
        raise ValueError("adjudication needs the designated primary checkout")
    branch = _required_git(root, "symbolic-ref", "--quiet", "--short", "HEAD")
    if not branch:
        raise ValueError("primary adjudication cannot run at detached HEAD")
    return str(Path(root).resolve()), branch


def _definition(text):
    """The immutable proposal with its two judgment sections removed."""
    kept, judgment = [], False
    for raw, visible in zip(text.splitlines(keepends=True), blank_fenced(text)):
        if visible.startswith("## "):
            judgment = visible.strip() in ("## Approval", "## Dispositions")
        if not judgment:
            kept.append(raw)
    return "".join(kept).rstrip() + "\n"


def _read_record(root, path):
    return parse_record(
        path.read_text(encoding="utf-8"), path.relative_to(root).as_posix()
    )


def parse_record(text, path):
    """Parse one selection, whether read from the checkout or a Git carrier."""
    data = tomllib.loads(text)
    if set(data) != _FIELDS or data.get("version") != 1:
        raise ValueError("{}: invalid primary selection schema".format(path))
    if not isinstance(data["turn"], str) or not _TURN.fullmatch(data["turn"]):
        raise ValueError("{}: invalid turn identity".format(path))
    if data["turn"] != "{}-{}".format(data["wi"], data["base"]):
        raise ValueError("{}: turn does not bind its WI and base".format(path))
    if path != record_path(data):
        raise ValueError("{}: selection is in the wrong home".format(path))
    return data


def validate(root, turn, candidate="HEAD"):
    """Re-resolve original proposal bindings and the permitted judgment delta."""
    identity, branch = _primary_identity(root)
    if (identity, branch) != (turn["primary_root"], turn["primary_branch"]):
        raise ValueError("primary root or branch changed since selection")
    if ac.working_tree_dirty(root):
        raise ValueError(
            "primary adjudication has uncommitted residue; reconcile it first"
        )
    return validate_candidate(root, turn, candidate)


def validate_candidate(root, turn, candidate):
    """Portable Git proof, also checked by the disposable publication replay."""
    base = turn["base"]
    _required_git(root, "merge-base", "--is-ancestor", base, candidate)
    path = record_path(turn)
    if tomllib.loads(_required_git(root, "show", candidate + ":" + path)) != turn:
        raise ValueError("publication selection differs from its committed turn")
    origin = _required_git(
        root, "log", "--diff-filter=A", "--format=%H", candidate, "--", path
    )
    if not origin or "\n" in origin:
        raise ValueError("selection has no unique committed origin")
    if _required_git(root, "show", "-s", "--format=%P", origin) != base:
        raise ValueError(
            "selection origin is not the first commit after its bound base"
        )
    if _required_git(root, "rev-parse", origin + ":" + path) != _required_git(
        root, "rev-parse", candidate + ":" + path
    ):
        raise ValueError("immutable primary selection was changed")
    for prefix, key in (
        ("", "registry_blobs"),
        (baseline_snapshot.SNAPSHOT_DIR + "/", "approved_blobs"),
    ):
        if (
            registry_blobs(root, base, prefix) != turn[key]
            or registry_blobs(root, candidate, prefix) != turn[key]
        ):
            raise ValueError("{} changed during judgment".format(key))
    _validate_proposal(root, turn, candidate)
    spec = turn["spec"]
    changed = _required_git(
        root, "diff", "--name-only", "--no-renames", base, candidate
    )
    extra = [
        p for p in changed.splitlines() if p != spec and not verdict.is_record_path(p)
    ]
    if extra:
        raise ValueError("primary judgment changed unowned paths: " + ", ".join(extra))
    return None


def _validate_proposal(root, turn, candidate):
    base = turn["base"]
    spec = turn["spec"]
    if (
        not spec.startswith("docs/work/queued/")
        or "/" in spec[len("docs/work/queued/") :]
    ):
        raise ValueError("selection does not name one queued spec")
    if (
        _required_git(root, "rev-parse", base + ":" + spec)
        != turn["proposal_spec_blob"]
    ):
        raise ValueError("initial queued proposal identity does not match")
    before = _required_git(root, "show", base + ":" + spec)
    after = _required_git(root, "show", candidate + ":" + spec)
    meta, _body = ac.parse_spec_frontmatter(before, spec)
    if (meta.get("id"), meta.get("safety_class"), meta.get("adjudicates") or []) != (
        turn["wi"],
        "adjudication",
        turn["scope"],
    ):
        raise ValueError(
            "turn WI, role or scope does not equal the original queued proposal"
        )
    if _definition(before) != _definition(after):
        raise ValueError("judgment changed the proposal outside Approval/Dispositions")
