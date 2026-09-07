"""Exclusive primary adjudication: immutable selection, existing engine, one publication.

The queued spec and committed review evidence are the work in progress. There
is no claim branch or phase journal. Only a verified publication completes a
selection; an interrupted selection precedes every later admission.
"""

from __future__ import annotations

import copy
from pathlib import Path

import agent_common as ac
import baseline_snapshot
from kitlib import spine

import primary_turn
import primary_publication
import primary_approval
import integrate

RECORDS = primary_turn.RECORDS
record_path = primary_turn.record_path
_required_git = primary_turn._required_git
registry_blobs = primary_turn.registry_blobs
_primary_identity = primary_turn._primary_identity
_read_record = primary_turn._read_record
validate = primary_turn.validate
validate_candidate = primary_turn.validate_candidate


def pending(root):
    return primary_publication.pending(root)


def writer_refusal(root):
    return primary_publication.writer_refusal(root)


def completion_refusal(root, worker):
    """A committed WI trailer cannot complete an unpublishable primary ruling."""
    turn = worker.get("primary_turn")
    if not turn:
        return None
    try:
        validate(root, turn)
        _plan, refusal = primary_approval.approval_projection(root, turn)
        return refusal
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return str(exc)


def begin(root, wi):
    """Commit one selection while both station locks are held, without claiming."""
    root = Path(root)
    if writer_refusal(root):
        raise ValueError(writer_refusal(root))
    if ac.working_tree_dirty(root):
        raise ValueError("selecting primary adjudication requires a clean checkout")
    identity, branch = _primary_identity(root)
    spec = integrate._queued_spec(root, wi)
    meta = integrate._spec_frontmatter(spec)
    if meta.get("safety_class") != "adjudication":
        raise ValueError("{} is not an adjudication".format(wi))
    if meta.get("brief") in ("amendment", "first-approval") and not meta.get(
        "adjudicates"
    ):
        raise ValueError(
            "{} needs its exact typed Adjudicates scope before selection".format(wi)
        )
    base = _required_git(root, "rev-parse", "HEAD")
    rel = spec.relative_to(root).as_posix()
    turn = dict(
        version=1,
        turn="{}-{}".format(wi, base),
        wi=wi,
        base=base,
        primary_branch=branch,
        primary_root=identity,
        spec=rel,
        proposal_spec_blob=_required_git(root, "rev-parse", base + ":" + rel),
        scope=meta.get("adjudicates") or [],
        registry_blobs=registry_blobs(root, base),
        approved_blobs=registry_blobs(root, base, baseline_snapshot.SNAPSHOT_DIR + "/"),
    )
    text = spine.toml_fields((k, v) for k, v in turn.items() if not isinstance(v, dict))
    for key in ("registry_blobs", "approved_blobs"):
        text += "\n[{}]\n".format(key) + spine.toml_fields(
            (spine.toml_string(k), v) for k, v in turn[key].items()
        )
    path = root / record_path(turn)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(text)
    _required_git(root, "add", "--", record_path(turn))
    _required_git(
        root,
        "commit",
        "-m",
        "adjudicate: select {} for exclusive primary judgment".format(wi),
    )
    return turn


def run(root, args, session, *, wi=None, turn=None, tier="all"):
    """Run the existing engine in process while holding the integration slot."""
    refusal = integrate._slot(root, primary_turn=True)
    if refusal:
        print("adjudicate: " + refusal)
        return ac.EXIT_PREFLIGHT
    try:
        turn = turn or begin(root, wi)
        validate(root, turn)
        assigned = copy.copy(args)
        assigned.wi, assigned.base = turn["wi"], turn["base"]
        assigned.train = turn["primary_branch"]
        assigned.worktree, assigned.root = None, str(root)
        code = session(assigned, primary_turn=turn)
        if code != ac.EXIT_DONE:
            return code
        validate(root, turn)
        closed, refusal = primary_publication.publish(root, turn, tier=tier)
        if refusal:
            raise ValueError(refusal)
        if closed != [turn["wi"]]:
            raise ValueError("publication did not close the selected WI")
        return ac.EXIT_DONE
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("adjudicate: {} (selection retained for resume)".format(exc))
        return ac.EXIT_PREFLIGHT
    finally:
        ac.release_lock(Path(root) / "out" / "integrate.lock")


def session_binding(root, worker, plan, candidate):
    """Coordinator-authored join from this invocation to its committed ruling."""
    if not worker.get("primary_turn") or plan["phase"] != "ADJUDICATE":
        return {}
    return {
        "primary-turn": worker["primary_turn"]["turn"],
        "judgment": Path(plan["verdict_path"]).relative_to(root).as_posix(),
        "candidate": candidate,
    }
