#!/usr/bin/env python3
"""WI-997's equivalence checker: the seed commit against its parent.

Unshipped tooling, separate from the seed so the seed never judges itself:

    python docs/plans/WI-997/check_seed.py --seed-commit <sha> --scratch <dir>
        [--out <file>]

`--seed-commit` repeats, oldest first, when a re-run adds a commit. Every result
is taken at the seed commits and their parents, never the tip, so the output
holds for as long as those commits do. It collects in a throwaway clone under
`--scratch`, and writes only there and to `--out`. The kit code it reads is the
clone's, at the last seed commit. Exit 0 when all four results hold.
"""

import argparse
import ast
import hashlib
import importlib
import os
import random
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TC_REGISTRY = "docs/test/test-cases.toml"
SAMPLE_SEED = 997
SAMPLE_SIZE = 40
SHOWN_DIFFERENCES = 20
DOCSTRING_OWNERS = (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


def git(repo, *args):
    """A git command's stdout as bytes; a failure is raised."""
    command = ("git", "-C", str(repo)) + args
    return subprocess.run(command, check=True, capture_output=True).stdout


def full_sha(repo, rev):
    """`rev` as a full commit id."""
    return git(repo, "rev-parse", rev + "^{commit}").decode("ascii").strip()


def without_docstrings(source):
    """`source`'s `ast.dump` with every docstring removed."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, DOCSTRING_OWNERS):
            if ast.get_docstring(node, clean=False) is not None:
                node.body = node.body[1:]
    return ast.dump(tree)


def changed_files(repo, commit, tests_dir):
    """The paths `commit` changes under the tests root."""
    out = git(
        repo,
        "diff-tree",
        "-r",
        "--no-commit-id",
        "--name-only",
        "--no-renames",
        commit + "^",
        commit,
        "--",
        tests_dir,
    )
    return out.decode("utf-8").split()


def ast_results(repo, commits, tests_dir):
    """`(lines, ok)`: each changed file's stripped AST against its commit's parent."""
    files, differing = set(), []
    for commit in commits:
        for rel in changed_files(repo, commit, tests_dir):
            files.add(rel)
            old = git(repo, "show", "{}^:{}".format(commit, rel))
            new = git(repo, "show", "{}:{}".format(commit, rel))
            if without_docstrings(old) != without_docstrings(new):
                differing.append(rel)
    lines = [
        "files changed: {}".format(len(files)),
        "AST differences: {}".format(len(differing)),
    ]
    lines.extend("  differs: " + rel for rel in sorted(differing))
    return lines, bool(files) and not differing


def collected_ids(clone, rev):
    """The sorted node ids pytest collects with `clone` checked out at `rev`."""
    git(clone, "checkout", "--quiet", "--detach", rev)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
    run = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q"]
        + ["-p", "no:cacheprovider"],
        cwd=clone,
        env=env,
        capture_output=True,
        encoding="utf-8",
    )
    if run.returncode != 0:
        raise SystemExit("collection failed at {}:\n{}".format(rev, run.stdout))
    return sorted(line for line in run.stdout.splitlines() if "::" in line)


def digest(ids):
    """The sha256 of the sorted ids, one per line."""
    return hashlib.sha256("\n".join(ids).encode("utf-8")).hexdigest()


def id_results(before, after):
    """`(lines, ok)` for the two sorted id lists."""
    lines = [
        "before: {} ids, sha256 {}".format(len(before), digest(before)),
        "after: {} ids, sha256 {}".format(len(after), digest(after)),
    ]
    return lines, bool(before) and before == after


def load_kit(clone):
    """The clone's reader modules, imported once it holds the last seed commit."""
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(clone / "project-trajectory" / "scripts"))
    names = ("check_trajectory", "gen_arch_map", "spine_carrier", "kitlib.spine")
    return [importlib.import_module(name) for name in names]


def evidence_parts(rows, prefix, spine):
    """`{TC id: {reduced node: [part as the cell names it]}}` under the tests root."""
    parts = {}
    for row in rows:
        mine = parts.setdefault(row["TC-ID"], {})
        for path, node in spine.evidence_items(row.get("Evidence")):
            if path.startswith(prefix):
                reduced = path
                written = path
                if node:
                    reduced = "{}::{}".format(path, node.split("[", 1)[0])
                    written = "{}::{}".format(path, node)
                mine.setdefault(reduced, []).append(written)
    return parts


def differences(parts, tags):
    """`(missing, extra)`: `(TC, node)` pairs a tag lacks, and pairs no part names."""
    missing, extra = [], []
    for tc in sorted(parts):
        named, tagged = set(parts[tc]), set(tags.get(tc, ()))
        missing.extend((tc, node) for node in sorted(named - tagged))
        extra.extend((tc, node) for node in sorted(tagged - named))
    return missing, extra


def tags_by_node(tags):
    """`{node: [TC id]}` inverted from the reader's `{TC id: [node]}`."""
    sites = {}
    for tc, nodes in tags.items():
        for node in nodes:
            sites.setdefault(node, []).append(tc)
    return sites


def tag_results(parts, tags, findings):
    """`(lines, ok)` for the tags against the reduced parts of every live case."""
    missing, extra = differences(parts, tags)
    pairs = sum(len(nodes) for nodes in parts.values())
    lines = [
        "live test cases: {}".format(len(parts)),
        "tags: {}".format(len(tags_by_node(tags))),
        "test-case and node pairs: {}".format(pairs),
        "reader findings: {}".format(len(findings)),
        "missing: {}".format(len(missing)),
        "extra: {}".format(len(extra)),
    ]
    shown = (missing + extra)[:SHOWN_DIFFERENCES]
    lines.extend("  differs: {} {}".format(tc, node) for tc, node in shown)
    lines.extend(
        "  finding: {file}:{line}: {shape}: {detail}".format(**finding)
        for finding in findings[:SHOWN_DIFFERENCES]
    )
    return lines, bool(pairs) and not (findings or missing or extra)


def complexity_results(clone):
    """`(lines, ok)` from the armed compare against the stamped baseline."""
    script = clone / "project-trajectory" / "scripts" / "check_complexity.py"
    run = subprocess.run(
        [sys.executable, str(script), "--root", str(clone), "--mode", "enforce"],
        capture_output=True,
        encoding="utf-8",
        env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1"),
    )
    lines = run.stdout.strip().splitlines()
    return lines, run.returncode == 0 and "unchanged from baseline" in run.stdout


def sample_lines(parts, tags):
    """The seeded random sample of tags, one line per tag: file, target, ids, and
    the evidence parts each id's tag answers."""
    sites = tags_by_node(tags)
    drawn = random.Random(SAMPLE_SEED).sample(
        sorted(sites), min(SAMPLE_SIZE, len(sites))
    )
    lines = []
    for node in drawn:
        path, _sep, target = node.partition("::")
        ids = sorted(sites[node])
        answers = [
            "{}: {}".format(tc, "; ".join(parts.get(tc, {}).get(node, ["(no part)"])))
            for tc in ids
        ]
        lines.append(
            "{} | {} | {} | {}".format(
                path, target or "(module)", ", ".join(ids), " | ".join(answers)
            )
        )
    return lines


def command_line(commits):
    """The line a reader re-runs, `<scratch>` and `<file>` literal so runs compare."""
    seeds = " ".join("--seed-commit " + commit for commit in commits)
    return "python docs/plans/WI-997/check_seed.py {} --scratch <scratch> --out <file>".format(
        seeds
    )


def section(title, lines):
    """One titled block of the report."""
    return [title] + lines + [""]


def report(clone, commits):
    """`(text, ok)`: the four results and the sample, from the throwaway clone."""
    before = collected_ids(clone, commits[0] + "^")
    after = collected_ids(clone, commits[-1])
    check_trajectory, gen_arch_map, spine_carrier, spine = load_kit(clone)
    tests_dir = check_trajectory._tests_dir(clone)
    prefix = Path(tests_dir.replace("\\", "/")).as_posix().rstrip("/") + "/"
    rows = spine_carrier.load(clone / TC_REGISTRY, "TC-ID", False)
    live = {row["TC-ID"] for row in rows}
    tags, findings = gen_arch_map.read_test_tags(clone, tests_dir, live)
    parts = evidence_parts(rows, prefix, spine)

    ast_lines, ast_ok = ast_results(clone, commits, tests_dir)
    id_lines, id_ok = id_results(before, after)
    tag_lines, tag_ok = tag_results(parts, tags, findings)
    complexity_lines, complexity_ok = complexity_results(clone)
    ok = ast_ok and id_ok and tag_ok and complexity_ok

    out = section("WI-997 seed evidence", ["command: " + command_line(commits)])
    out += section("1. AST, docstrings stripped, against the parent", ast_lines)
    out += section("2. Collected test ids, sorted", id_lines)
    out += section("3. Tags against reduced evidence parts", tag_lines)
    out += section("4. check_complexity", complexity_lines)
    out += section(
        "Sample: file | target | ids | the evidence parts each id answers",
        sample_lines(parts, tags),
    )
    out.append("result: {}".format("PASS" if ok else "FAIL"))
    return "\n".join(out) + "\n", ok


def make_writable(function, path, _exc):
    """`shutil.rmtree`'s retry for git's read-only object files on Windows."""
    os.chmod(path, stat.S_IWRITE)
    function(path)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed-commit", action="append", required=True)
    parser.add_argument("--scratch", required=True, type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)

    commits = [full_sha(ROOT, commit) for commit in args.seed_commit]
    args.scratch.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="check-seed-", dir=args.scratch)).resolve()
    clone = work / "clone"
    try:
        subprocess.run(
            ["git", "clone", "--quiet", "--no-checkout", str(ROOT), str(clone)],
            check=True,
        )
        text, ok = report(clone, commits)
    finally:
        shutil.rmtree(work, onerror=make_writable)
    data = text.encode("utf-8")
    if args.out is not None:
        args.out.write_bytes(data)
    sys.stdout.buffer.write(data)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
