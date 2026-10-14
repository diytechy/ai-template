"""toml_merge3.py <branch> <path>... [--out-dir DIR]

Three-way merge of TOML registries TABLE BY TABLE, never line by line.

Git's line merge aligns identical `status`/`phase` tails across rows two
sides added, so keeping both hunks can strip a row's tail. This splits each
version (merge base, HEAD, <branch>) into a preamble plus `[kind.ID]` blocks
(a block runs from its header to the next header) and merges per block:

- a block changed on one side only takes that side;
- a block both sides changed identically takes it;
- a block both sides changed differently is a CONFLICT (exit 1, nothing written);
- a block added on one side is kept; added on both differently is a CONFLICT;
- a block deleted on one side and unchanged on the other is dropped.

Order: HEAD's blocks in HEAD's order, then branch-only blocks in branch order
(trunk's first). The preamble merges the same way as one block. Writes the
merged file over <path> in the working tree (or under --out-dir), LF bytes as
read from git.
"""

import os
import re
import subprocess
import sys

HEADER = re.compile(r"^\[[A-Za-z_]+\.[A-Za-z]+-\d+\]\s*$", re.M)


def show(rev, path):
    r = subprocess.run(
        ["git", "show", f"{rev}:{path}"], capture_output=True, check=False
    )
    return r.stdout.decode("utf-8") if r.returncode == 0 else None


def split(text):
    if text is None:
        return "", {}, []
    starts = [m.start() for m in HEADER.finditer(text)]
    pre = text[: starts[0]] if starts else text
    blocks, order = {}, []
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(text)
        chunk = text[s:e]
        key = chunk.split("\n", 1)[0].strip()
        if key in blocks:
            raise SystemExit(f"duplicate table {key}")
        blocks[key] = chunk
        order.append(key)
    return pre, blocks, order


def pick(name, base, ours, theirs, conflicts):
    if ours == theirs:
        return ours
    if ours == base:
        return theirs
    if theirs == base:
        return ours
    conflicts.append(name)
    return ours


def norm_tail(chunk):
    return chunk if chunk is None or chunk.endswith("\n") else chunk + "\n"


def merge(branch, path):
    base_rev = subprocess.run(
        ["git", "merge-base", "HEAD", branch], capture_output=True, text=True,
        check=True,
    ).stdout.strip()
    bp, bb, _ = split(show(base_rev, path))
    op, ob, oo = split(show("HEAD", path))
    tp, tb, to = split(show(branch, path))
    conflicts = []
    out = [pick("<preamble>", bp, op, tp, conflicts)]
    keys = oo + [k for k in to if k not in ob]
    for k in keys:
        b, o, t = bb.get(k), ob.get(k), tb.get(k)
        got = pick(k, b, o, t, conflicts)
        if got is not None:
            out.append(norm_tail(got))
    return "".join(out), conflicts


def main(argv):
    out_dir = None
    if "--out-dir" in argv:
        i = argv.index("--out-dir")
        out_dir = argv[i + 1]
        del argv[i : i + 2]
    branch, paths = argv[0], argv[1:]
    bad = 0
    for path in paths:
        text, conflicts = merge(branch, path)
        if conflicts:
            print(f"{path}: CONFLICT in {', '.join(conflicts)}")
            bad = 1
            continue
        dest = os.path.join(out_dir, path) if out_dir else path
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
        with open(dest, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        print(f"{path}: merged -> {dest}")
    return bad


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
