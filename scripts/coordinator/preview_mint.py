"""preview_mint.py — what would the merge of this lane mint? (S11 plan §3 step 2)

Run FROM THE LANE ROOT with the repo venv:

    python "$TOOLS/preview_mint.py" <before> [<after>]

<before> is the trunk commit the lane forked from (its merge-base with trunk);
<after> defaults to HEAD. It calls the kit's own draft builders,
`intake._amendment_drafts` and `intake._first_approval_drafts`, which mint
nothing, and prints each draft's brief, scope and SR refs: the in-lane
adjudication scope, exactly what a sitting would receive.
"""

import sys
from pathlib import Path

sys.path.insert(0, "project-trajectory/scripts")
import intake  # noqa: E402


def main(argv):
    before = argv[0]
    after = argv[1] if len(argv) > 1 else "HEAD"
    root = Path(".").resolve()
    drafts = intake._amendment_drafts(root, before, after) + intake._first_approval_drafts(
        root, before, after
    )
    if not drafts:
        print("preview_mint: nothing would be minted")
        return 0
    for d in drafts:
        print("brief={} adjudicates={} sr_refs={} specref={}".format(
            d.get("brief"), ";".join(d.get("adjudicates") or []),
            ";".join(d.get("sr_refs") or []), d.get("specref")))
        print("  title: " + d.get("title", ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
