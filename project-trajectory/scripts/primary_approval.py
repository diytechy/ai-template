"""Read-only authority projection for one held primary approval turn.

The primary coordinator owns the lock, review engine and writes.  This module
owns the one content question between them: whether the reviewed ``## Approval``
payload can produce a narrow Status/snapshot plan.  It never stages or writes.
"""

import hashlib
import re
import tomllib

import acceptance_record as record
import agent_common
import baseline_snapshot as snapshot
import score_reviews
import intake
from kitlib import adjudication
import spine_carrier
from kitlib import git as kitgit
from kitlib import verdict as kverdict

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_CLASSES = frozenset({"approve", "equivalent", "return", "uncertain", "meaning"})
_STATES = frozenset({"approved-change", "below-approval-rider"})
_IMPACT = frozenset({"amend", "retain", "regenerate", "history-unchanged"})


def _refusal(message):
    return None, "primary approval: REFUSED — " + message


def _git(root, args):
    return kitgit.git_out(root, args)


def _blob_at(root, rev, path):
    value = _git(root, ["rev-parse", "{}:{}".format(rev, path)])
    return value.strip() if value else None


def _payload_text(root, candidate, path):
    return _git(root, ["show", "{}:{}".format(candidate, path)])


def _fenced_approval(text):
    """The sole TOML block immediately following an ``## Approval`` heading."""
    match = re.search(
        r"(?m)^## Approval\s*$\n(?:\s*\n)*```toml\s*\n(.*?)^```\s*$", text, re.S
    )
    if not match:
        return None
    if len(re.findall(r"(?m)^## Approval\s*$", text)) != 1:
        return None
    return match.group(1)


def parse_approval_payload(text):
    """Parse the fixed Approval TOML carrier, returning ``(dict, refusal)``.

    This is deliberately stricter than a convenience TOML read: payload types
    are the authority boundary, so later projection code never guesses what a
    string, list, or blob-shaped value meant.
    """
    block = _fenced_approval(text)
    if block is None:
        return None, "the queued spec has no single fenced `## Approval` TOML block"
    try:
        data = tomllib.loads(block)
    except tomllib.TOMLDecodeError as exc:
        return None, "`## Approval` is not valid TOML: {}".format(exc)
    required = {"version", "turn", "base", "proposal", "decision"}
    if set(data) - {
        "version",
        "turn",
        "base",
        "proposal",
        "decision",
        "absorption",
        "impact",
    }:
        return None, "`## Approval` has unknown top-level keys"
    if not required <= set(data) or data.get("version") != 1:
        return (
            None,
            "`## Approval` requires version=1, turn, base, proposal and decisions",
        )
    if (
        not isinstance(data["turn"], str)
        or not isinstance(data["base"], str)
        or not isinstance(data["proposal"], str)
    ):
        return None, "turn, base and proposal must be strings"
    if not _HEX40.fullmatch(data["base"]) or not _HEX64.fullmatch(data["proposal"]):
        return (
            None,
            "base must be 40-hex and proposal must be the 64-hex verdict tree identity",
        )
    for key in ("decision", "absorption", "impact"):
        if key in data and not isinstance(data[key], list):
            return None, "`{}` must be an array of tables".format(key)
    return data, None


def _turn_refusal(turn):
    keys = {
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
    if not isinstance(turn, dict) or set(turn) != keys:
        return "turn has an unexpected fixed-key shape"
    scalar_keys = keys - {"version", "scope", "registry_blobs", "approved_blobs"}
    if turn["version"] != 1 or not all(
        isinstance(turn[k], str) and turn[k] for k in scalar_keys
    ):
        return "turn has missing scalar bindings"
    if not _HEX40.fullmatch(turn["base"]) or not _HEX40.fullmatch(
        turn["proposal_spec_blob"]
    ):
        return "turn base and proposal_spec_blob must be 40-hex"
    if not isinstance(turn["scope"], list) or not all(
        isinstance(x, str) and x for x in turn["scope"]
    ):
        return "turn scope must be a non-empty typed row-id list"
    if len(set(turn["scope"])) != len(turn["scope"]):
        return "turn scope contains duplicate row ids"
    for key in ("registry_blobs", "approved_blobs"):
        values = turn[key]
        if not isinstance(values, dict) or not all(
            isinstance(p, str) and isinstance(v, str) and _HEX40.fullmatch(v)
            for p, v in values.items()
        ):
            return "turn {} must map registry paths to 40-hex blobs".format(key)
    return None


def approval_scope(turn, brief=""):
    """Rows that may receive Approval decisions for this typed primary brief.

    The turn scope remains the immutable subject scope.  Consolidation owns a
    different typed carrier and therefore has no registry-cell decision scope;
    every ordinary primary brief keeps the full turn scope.
    """
    return [] if brief == "consolidate" else list(turn["scope"])


def _columns(registry):
    if spine_carrier.stem(registry) == spine_carrier.stem(snapshot.NEEDS_REL):
        return ["SN-ID"]
    columns = {
        col
        for path, col in record.APPROVAL_ACT_CSVS + snapshot.SNAPSHOT_TIERS
        if spine_carrier.stem(path) == spine_carrier.stem(registry)
    }
    if not columns:
        raise ValueError("unknown approval registry " + registry)
    return sorted(columns)


def registry_rows(root, blob, registry):
    """All tiers in a carrier, including the three external-registry tables."""
    text = _git(root, ["cat-file", "-p", blob])
    if text is None:
        raise ValueError("cannot read registry blob " + str(blob))
    if registry.endswith(".md"):
        return {
            n["id"]: {spine_carrier.SPINE_COLUMN.get(k, k): v for k, v in n.items()}
            for n in spine_carrier.needs_from_text(text)
        }
    rows = {}
    for col in _columns(registry):
        rows.update(spine_carrier.rows_from_text(text, col, _suffix(registry)) or {})
    return {rid: row for rid, row in rows.items() if not rid.endswith("-000")}


def _cell_blob(root, blob, registry, row, cell):
    return registry_rows(root, blob, registry).get(row, {}).get(cell)


def _suffix(path):
    return ".toml" if path.endswith(".toml") else ".csv"


def _id_column(registry):
    return _columns(registry)[0]


def _decision_rows(payload, scope):
    decisions = payload.get("decision", [])
    rows = []
    for item in decisions:
        if not isinstance(item, dict):
            return None, "decision is not a table"
        need = {"registry", "row", "classification", "before", "after", "evidence"}
        if set(item) != need:
            return None, "decision {} has an unexpected key set".format(
                item.get("row", "?")
            )
        if (
            not isinstance(item["registry"], str)
            or not isinstance(item["row"], str)
            or not isinstance(item["classification"], str)
            or item["classification"] not in _CLASSES
        ):
            return None, "decision has an invalid registry, row or classification"
        if item["row"] not in scope:
            return None, "decision {} is outside the turn scope".format(item["row"])
        if (
            not isinstance(item["before"], dict)
            or not isinstance(item["after"], dict)
            or set(item["before"]) != set(item["after"])
        ):
            return (
                None,
                "decision {} must bind identical before/after cell sets".format(
                    item["row"]
                ),
            )
        if not item["before"] or not all(
            isinstance(c, str) and isinstance(v, str) and _HEX40.fullmatch(v)
            for m in (item["before"], item["after"])
            for c, v in m.items()
        ):
            return None, "decision {} has invalid cell blob identities".format(
                item["row"]
            )
        if (
            not isinstance(item["evidence"], list)
            or not item["evidence"]
            or not all(isinstance(x, str) for x in item["evidence"])
        ):
            return None, "decision {} has no evidence refs".format(item["row"])
        rows.append(item)
    if {item["row"] for item in rows} != set(scope) or len(rows) != len(scope):
        return None, "decisions must name every scoped row exactly once"
    return rows, None


def _log_metadata(text):
    metadata = {}
    for line in (text or "").splitlines():
        if not line.startswith("#") or line.startswith("# ---"):
            break
        key, sep, value = line[1:].strip().partition(":")
        if sep:
            metadata[key.strip()] = value.strip()
    return metadata


def _judgment_commit(root, candidate, path):
    value = _git(root, ["log", "-1", "--format=%H", candidate, "--", path])
    value = value.strip() if value else ""
    return value if _HEX40.fullmatch(value) else None


def _latest_judgment(records, chronology):
    if not records:
        return []
    ranked = [
        (chronology.get(meta.get("_logged_commit", ""), -1), meta, text)
        for meta, text in records
    ]
    if any(rank < 0 for rank, _meta, _text in ranked):
        return []
    ranked.sort(key=lambda item: item[0], reverse=True)
    if len(ranked) > 1 and ranked[0][0] == ranked[1][0]:
        return []
    return [(ranked[0][1], ranked[0][2])]


def _judgment_record(root, candidate, turn, brief, path, want):
    if not path.startswith("docs/iteration/") or not path.endswith(".log"):
        return None, False
    meta = _log_metadata(_payload_text(root, candidate, path))
    if (meta.get("phase"), meta.get("wi"), meta.get("primary-turn")) != (
        "ADJUDICATE",
        turn["wi"],
        turn["turn"],
    ):
        return None, False
    judged = meta.get("candidate", "")
    artifact = meta.get("judgment", "")
    if not _HEX40.fullmatch(judged) or not artifact.startswith("docs/reviews/"):
        return None, False
    if _git(root, ["merge-base", "--is-ancestor", judged, candidate]) is None:
        return None, False
    if kverdict.tree_identity(root, judged) != want:
        return None, False
    text = _payload_text(root, judged, artifact)
    if text is None or adjudication.verdict_text_refusal(
        brief or "primary", text, artifact, scope=turn["scope"]
    ):
        return None, False
    if _blob_at(root, judged, artifact) != _blob_at(root, candidate, artifact):
        return None, False
    if meta.get("base") != turn["base"][:12]:
        return None, False
    commit = _judgment_commit(root, candidate, path)
    if commit is None:
        return None, True
    meta["_logged_commit"] = commit
    return (meta, text), False


def _judgment_records(root, candidate, turn, brief):
    """Actual coordinator logs joining a typed judgment to this exact proposal."""
    paths = kverdict.branch_paths(root, candidate, turn["base"])
    records = []
    commits = (_git(root, ["rev-list", candidate]) or "").splitlines()
    chronology = {commit: len(commits) - index for index, commit in enumerate(commits)}
    want = kverdict.tree_identity(root, candidate)
    for path in paths or ():
        record, malformed = _judgment_record(root, candidate, turn, brief, path, want)
        if malformed:
            return []
        if record:
            records.append(record)
    return _latest_judgment(records, chronology)


def _evidence_refusal(root, candidate, refs, judgments=None):
    for ref in refs:
        if not isinstance(ref, str) or not _HEX40.fullmatch(ref):
            return "evidence ref must be an immutable judgment commit"
        if _git(root, ["merge-base", "--is-ancestor", ref, candidate]) is None:
            return "evidence ref {!r} is not committed for this candidate".format(ref)
        paths = _git(root, ["diff-tree", "--no-commit-id", "--name-only", "-r", ref])
        written = set((paths or "").splitlines())
        if judgments is not None and not any(
            meta["judgment"] in written
            and _blob_at(root, ref, meta["judgment"])
            == _blob_at(root, candidate, meta["judgment"])
            for meta, _text in judgments
        ):
            return "evidence ref {!r} has no typed judgment bound to this turn and candidate".format(
                ref
            )
    return None


def _machine_author(judgments):
    if len(judgments) != 1:
        return None
    meta = judgments[0][0]
    model = meta.get("model", "")
    invocation = meta.get("invocation-id", "")
    if not model or not invocation:
        return None
    fields = [
        meta.get(k, "")
        for k in ("provider", "roster-row", "model", "session-id", "invocation-id")
    ]
    digest = hashlib.sha256("\0".join(fields).encode()).hexdigest()[:32]
    return {
        "name": "AI adjudicator {}".format(meta["model"]),
        "email": "adjudicate+{}@automation.invalid".format(digest),
    }


def _review_refusal(root, candidate, turn, spec_text):
    """Use the same declared review phases and successor classes as the engine."""
    try:
        meta, _body = agent_common.parse_spec_frontmatter(spec_text, turn["spec"])
        required = int(
            agent_common.declared_policy(root / "docs", "review-policy", "0")
        )
    except (ValueError, TypeError) as exc:
        return "cannot resolve primary review policy: {}".format(exc)
    drafts, why = intake.parse_dispositions(spec_text, turn["spec"])
    if why:
        return why
    if required < 1 or not agent_common.adjudication_review_owed(
        root / "docs", meta.get("brief", ""), [intake.draft_kind(d) for d in drafts]
    ):
        return None
    want = kverdict.tree_identity(root, candidate)
    entries = kverdict.branch_entries(
        root, candidate, turn["base"], want, score_reviews.parse_verdict
    )
    if entries is None or kverdict.phases_owed(entries, required):
        return "candidate lacks its required independent review phases"
    latest, flipped = score_reviews.latest_phase_verdicts(entries, required)
    if not latest or any(word != "APPROVE" for word in latest.values()):
        return "candidate lacks independent APPROVE review at its bound tree"
    if flipped:
        return "candidate review reran until approve"
    return None


def absorption_census(root, turn, candidate, accepted):
    """Actual copied population from bound snapshots to the proposed live rows."""
    census = {}
    registries = {registry for registry, _rid in accepted}
    for registry in sorted(registries):
        old_blob = turn["approved_blobs"].get(snapshot.SNAPSHOT_DIR + "/" + registry)
        new_blob = _blob_at(root, candidate, registry)
        if not old_blob or not new_blob:
            raise ValueError(
                "{} needs an explicit initial signing before automatic publication".format(
                    registry
                )
            )
        old = registry_rows(root, old_blob, registry)
        new = registry_rows(root, new_blob, registry)
        for rid in sorted(set(old) | set(new)):
            before, after = old.get(rid, {}), new.get(rid, {})
            if snapshot._claims_approval(before):
                if not after:
                    raise ValueError(
                        "approved row {} was removed from its carrier".format(rid)
                    )
                id_col = next(
                    (k for k in before if k.endswith("-ID")), _id_column(registry)
                )
                changed = record.split_changed_cells(registry, id_col, before, after)[
                    "approved"
                ]
                state = "approved-change"
            elif (registry, rid) not in accepted and not snapshot._claims_approval(
                after
            ):
                changed = {
                    k: (before.get(k), after.get(k))
                    for k in set(before) | set(after)
                    if not k.endswith("-ID") and before.get(k) != after.get(k)
                }
                state = "below-approval-rider"
            else:
                continue
            if changed:
                census[(registry, rid)] = {
                    "state": state,
                    "cells": {
                        cell: {"before": old_blob, "after": new_blob}
                        for cell in changed
                    },
                }
    return census


def _absorption_refusal(root, turn, candidate, payload, decisions, judgments):
    accepted = {
        (d["registry"], d["row"]): d
        for d in decisions
        if d["classification"] in {"approve", "equivalent", "meaning"}
    }
    if not accepted:
        return None
    try:
        expected = absorption_census(root, turn, candidate, accepted)
    except (ValueError, KeyError) as exc:
        return str(exc)
    seen = {}
    for item in payload.get("absorption", []):
        why = _absorption_shape(item)
        if why:
            return why
        key = (item["registry"], item["row"])
        if key in seen:
            return "duplicate absorption for {}".format(item["row"])
        seen[key] = item
        why = _evidence_refusal(root, candidate, [item["judgment"]], judgments)
        if why:
            return why
        if (
            key not in expected
            or {k: item[k] for k in ("state", "cells")} != expected[key]
        ):
            return "absorption {} cells/state do not equal the exact whole-file census".format(
                item["row"]
            )
        if item["state"] == "approved-change" and key not in accepted:
            return "approved-cell absorption {} has no accepted scoped decision".format(
                item["row"]
            )
    if set(seen) != set(expected):
        return "whole-file absorption ledger omits changed approved cells or Drafted riders"
    return None


def _current_turn_record(root, base, path):
    """Exclude only new decision evidence; prior historical uses stay in scope."""
    if not kverdict.is_record_path(path):
        return False
    history = _git(root, ["log", "--format=%H", base, "--", path])
    if history is None:
        raise ValueError("cannot establish impact path history: " + path)
    return not history.strip()


def impact_census(root, candidate, turn, ids):
    """Every tracked ID/path use; the selected spec binds its immutable proposal."""
    pairs = {}
    for rid in sorted(ids):
        found = _git(
            root,
            [
                "grep",
                "-l",
                "-z",
                "-w",
                "-F",
                "-e",
                rid,
                candidate,
                "--",
                ".",
                ":(exclude)OWNER_SCRATCHPAD.md",
                ":(glob,exclude)**/OWNER_SCRATCHPAD.md",
            ],
        )
        if found is None:
            raise ValueError("cannot census tracked uses of {}".format(rid))
        for hit in found.split("\0"):
            if not hit:
                continue
            _rev, _colon, path = hit.partition(":")
            if _current_turn_record(root, turn["base"], path):
                continue
            blob = (
                turn["proposal_spec_blob"]
                if path == turn["spec"]
                else _blob_at(root, candidate, path)
            )
            if not blob:
                raise ValueError("cannot bind impact source {}".format(path))
            pairs[(rid, path)] = blob
    return pairs


def _impact_path_class(path):
    snapshot_path = snapshot.SNAPSHOT_DIR.rstrip("/") + "/"
    if path.startswith(snapshot_path):
        return "live-snapshot"
    if (
        path.startswith(("docs/archive/", "docs/handbacks/"))
        or kverdict.is_record_path(path)
        or path == "docs/log.md"
    ):
        return "historical"
    return "live"


def _impact_disposition_refusal(path, disposition):
    kind = _impact_path_class(path)
    if kind == "live-snapshot":
        return (
            None
            if disposition in {"amend", "regenerate"}
            else "snapshot impact must use amend or regenerate"
        )
    if (kind == "historical") != (disposition == "history-unchanged"):
        return "impact disposition must preserve historical uses and judge live uses separately"
    return None


def _impact_refusal(root, candidate, turn, payload, decisions, judgments=None):
    if not any(item["classification"] == "meaning" for item in decisions):
        return None
    impacts = payload.get("impact", [])
    if not impacts:
        return "meaning decision requires a complete tracked ID-use impact census"
    seen, why = _impact_shape(impacts)
    if why:
        return why
    try:
        expected = impact_census(
            root,
            candidate,
            turn,
            {item["row"] for item in decisions if item["classification"] == "meaning"},
        )
    except ValueError as exc:
        return str(exc)
    if seen != set(expected):
        return "impact entries do not equal the complete tracked ID/path census (missing {}, extra {})".format(
            len(set(expected) - seen), len(seen - set(expected))
        )
    for item in impacts:
        why = _evidence_refusal(root, candidate, item["evidence"], judgments)
        if why:
            return why
        pair = (item["id"], item["path"])
        if item["source_blob"] != expected[pair]:
            return "impact source blob changed for {} {}".format(*pair)
        why = _impact_disposition_refusal(item["path"], item["disposition"])
        if why:
            return why
    return None


def _decision_binding_refusal(root, turn, candidate, decisions, judgments):
    for decision in decisions:
        registry = decision["registry"]
        if registry not in turn["registry_blobs"]:
            return "decision {} names a registry outside the bound turn".format(
                decision["row"]
            )
        why = _evidence_refusal(root, candidate, decision["evidence"], judgments)
        if why:
            return why
        for cell, before_blob in decision["before"].items():
            after_blob = decision["after"][cell]
            if after_blob != _blob_at(root, candidate, registry):
                return "decision {} after identity is not the candidate registry blob".format(
                    decision["row"]
                )
            allowed_before = {
                turn["registry_blobs"][registry],
                turn["approved_blobs"].get(snapshot.SNAPSHOT_DIR + "/" + registry),
            }
            if before_blob not in allowed_before:
                return "decision {} before identity is not a bound live or approved blob".format(
                    decision["row"]
                )
            try:
                before = _cell_blob(
                    root, before_blob, decision["registry"], decision["row"], cell
                )
                after = _cell_blob(
                    root, after_blob, decision["registry"], decision["row"], cell
                )
            except ValueError as exc:
                return str(exc)
            if before is None or after is None:
                return "decision {} does not resolve its {} cell identities".format(
                    decision["row"], cell
                )
    return None


def approval_projection(root, turn, candidate="HEAD", require_provenance=True):
    """Return a stage-only approval plan or an actionable refusal string.

    The plan has no filesystem effects.  ``return`` and ``uncertain`` are the
    existing finite-release path: they report observations but stage neither a
    Status nor a snapshot.
    """
    context, why = _projection_context(root, turn, candidate, require_provenance)
    if why:
        return _refusal(why)
    payload, decisions, judgments = context
    why = _decision_binding_refusal(root, turn, candidate, decisions, judgments)
    if why:
        return _refusal(why)
    why = _absorption_refusal(root, turn, candidate, payload, decisions, judgments)
    if why:
        return _refusal(why)
    why = _impact_refusal(root, candidate, turn, payload, decisions, judgments)
    if why:
        return _refusal(why)
    return _effects(root, candidate, decisions, judgments, require_provenance)


def _effects(root, candidate, decisions, judgments, require_provenance):
    classifications = {d["classification"] for d in decisions}
    author = _machine_author(judgments) if require_provenance else None
    judgment = judgments[0][0].get("judgment") if judgments else None
    if require_provenance and author is None:
        return _refusal(
            "no unique committed ADJUDICATE judgment and route/session identity bind this candidate"
        )
    if classifications <= {"return", "uncertain"}:
        return (
            {
                "outcome": "return",
                "statuses": {},
                "approves": {},
                "author": author,
                "judgment": judgment,
                "findings": [
                    "{}: {}".format(d["row"], d["classification"]) for d in decisions
                ],
            },
            None,
        )
    if classifications - {"approve", "equivalent", "meaning"}:
        return _refusal(
            "only accepted first-approval or equivalent decisions may publish; meaning requires its later complete-scope reanchor"
        )
    if judgments and any(
        re.search(r"(?m)^\s*OUTCOME:\s*RETURN\b", body) for _meta, body in judgments
    ):
        return _refusal("a RETURN judgment cannot authorize accepted approval cells")
    statuses, why = _status_projection(root, candidate, decisions)
    if why:
        return _refusal(why)
    approves = {d["registry"]: d["evidence"][0] for d in decisions}
    return (
        {
            "outcome": "publish",
            "statuses": statuses,
            "approves": approves,
            "author": author,
            "judgment": judgment,
            "findings": [],
        },
        None,
    )


def _projection_context(root, turn, candidate, require_provenance):
    why = _candidate_refusal(root, turn, candidate)
    if why:
        return None, why
    text = _payload_text(root, candidate, turn["spec"])
    if text is None:
        return _refusal("cannot read the bound queued spec at candidate")
    if require_provenance:
        why = _review_refusal(root, candidate, turn, text)
        if why:
            return _refusal(why)
    payload, why = parse_approval_payload(text)
    if why:
        return _refusal(why)
    proposal = kverdict.tree_identity(root, turn["base"])
    if (
        payload["turn"] != turn["turn"]
        or payload["base"] != turn["base"]
        or payload["proposal"] != proposal
    ):
        return _refusal("payload turn/base/proposal does not bind the pending turn")
    if _blob_at(root, turn["base"], turn["spec"]) != turn["proposal_spec_blob"]:
        return _refusal("initial queued spec blob no longer matches the turn")
    try:
        meta, _body = agent_common.parse_spec_frontmatter(text, turn["spec"])
    except ValueError as exc:
        return _refusal(str(exc))
    decisions, why = _decision_rows(
        payload, approval_scope(turn, meta.get("brief", ""))
    )
    if why:
        return _refusal(why)
    judgments = (
        _judgment_records(root, candidate, turn, meta.get("brief", ""))
        if require_provenance
        else None
    )
    return (payload, decisions, judgments), None


def _absorption_shape(item):
    if not isinstance(item, dict) or set(item) != {
        "registry",
        "row",
        "cells",
        "judgment",
        "state",
    }:
        return "absorption has an unexpected key set"
    if not isinstance(item["registry"], str) or not isinstance(item["row"], str):
        return "absorption registry and row must be strings"
    if item["judgment"] == "UNJUDGED":
        return "UNJUDGED whole-file absorption blocks publication; RETURN with a scoped continuation"
    return None


def _impact_shape(impacts):
    seen = set()
    for item in impacts:
        if not isinstance(item, dict) or set(item) != {
            "id",
            "path",
            "source_blob",
            "disposition",
            "evidence",
        }:
            return None, "impact has an unexpected key set"
        key = (item["id"], item["path"])
        if not all(isinstance(x, str) and x for x in key) or key in seen:
            return None, "impact census has a duplicate or invalid ID/path pair"
        seen.add(key)
        if (
            not isinstance(item["source_blob"], str)
            or not _HEX40.fullmatch(item["source_blob"])
            or not isinstance(item["disposition"], str)
            or item["disposition"] not in _IMPACT
        ):
            return None, "impact {} has invalid source blob or disposition".format(
                item["id"]
            )
        if (
            not isinstance(item["evidence"], list)
            or not all(isinstance(ref, str) and ref for ref in item["evidence"])
            or not item["evidence"]
        ):
            return None, "impact {} lacks evidence".format(item["id"])
    return seen, None


def _status_projection(root, candidate, decisions):
    statuses = {}
    for d in decisions:
        try:
            live = _cell_blob(
                root,
                _blob_at(root, candidate, d["registry"]),
                d["registry"],
                d["row"],
                "Status",
            )
        except ValueError as exc:
            return None, (str(exc))
        if agent_common.human_approves_spine(
            root / "docs", spine_carrier.stem(d["registry"])
        ):
            return None, (
                "{} is human-held; automation must surface it to the manual primary signer".format(
                    d["registry"]
                )
            )
        if d["classification"] == "approve":
            if live != "Drafted":
                return None, (
                    "approve decision {} must start at Status=Drafted".format(d["row"])
                )
            statuses.setdefault(d["registry"], {})[d["row"]] = "Approved"
        elif live != "Approved":
            return None, (
                "{} decision {} must retain Status=Approved".format(
                    d["classification"], d["row"]
                )
            )
    return statuses, None


def _candidate_refusal(root, turn, candidate):
    why = _turn_refusal(turn)
    if why:
        return why
    if _git(root, ["rev-parse", "--verify", candidate + "^{commit}"]) is None:
        return "candidate is not a commit"
    if _git(root, ["merge-base", "--is-ancestor", turn["base"], candidate]) is None:
        return "candidate does not descend from the bound primary base"
    return None
