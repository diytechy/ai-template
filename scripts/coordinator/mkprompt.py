"""mkprompt.py <template> <out> KEY=VALUE ... — fill @KEY@ slots in a prompt template.

Refuses (exit 2) when a slot in the template is left unfilled, so a review never
launches with a literal `@SHA@` in it. `@LANE_SLUG@` defaults to LANE with `/`
replaced by `-`. `@WTROOT@` (the checkout's sibling `.wt` folder) and `@PY@`
(the checkout's venv Python) default to the paths `layout.py` derives, so no
template names a machine.

`HATS` is computed, not substituted: `none` for a turn that adds no SR under a
need and amends no need, which fills the stated no-round line; otherwise the
`;`-joined SN ids of every need the round's sitting reaches (each need the
turn amends, each need a new SR sits under and each need an SR it amends
names), which fills the questions of that decomposition round's applicable
hats, computed by the kit from the lane worktree (`<WTROOT>/<LANE_SLUG>`): its hats roster, its needs and the work
item `WI`, each named need widened by the work item's tags; the work item's own
SR-Refs and SpecRef add no parent, as in the round's sitting. A value naming no
need, an unknown work item or a roster that cannot be read refuses (exit 2).
"""

import re
import sys
from pathlib import Path

from layout import PYTHON, REPO, WTROOT

sys.path.insert(0, str(REPO / "project-trajectory" / "scripts"))
import consolidate  # noqa: E402
import plan_briefs  # noqa: E402

NO_ROUND = "none"


def hats_block(values):
    """`(block, None)`: the perspectives block the `HATS` value asks for, or
    `(None, reason)`."""
    hats = values["HATS"].strip()
    if hats == NO_ROUND:
        return plan_briefs.NOT_A_ROUND, None
    needs = tuple(n.strip() for n in hats.split(";") if n.strip())
    if not needs:
        return None, "names no need: give {!r} or the SN ids".format(NO_ROUND)
    lane = Path(values["WTROOT"]) / values["LANE_SLUG"]
    rows = {r.get("WI-ID"): r for r in consolidate.read_rows(lane)}
    row = rows.get(values.get("WI", ""))
    if row is None:
        return None, "no work item {!r} under {}".format(values.get("WI", ""), lane)
    # The round's questions without the sitting's verdict instruction: the
    # template asks the author for each hat's outcome in its final message.
    try:
        return plan_briefs.round_questions(lane, row, needs=needs), None
    except plan_briefs.HatsError as exc:
        return None, str(exc)


def main(argv):
    template, out, pairs = argv[0], argv[1], argv[2:]
    values = dict(p.split("=", 1) for p in pairs)
    if "LANE" in values:
        values.setdefault("LANE_SLUG", values["LANE"].replace("/", "-"))
    values.setdefault("WTROOT", WTROOT.as_posix())
    values.setdefault("PY", PYTHON.as_posix())
    if "HATS" in values:
        block, why = hats_block(values)
        if block is None:
            print("mkprompt: HATS: " + why, file=sys.stderr)
            return 2
        values["HATS"] = block
    text = open(template, encoding="utf-8").read()
    for key, value in values.items():
        text = text.replace("@{}@".format(key), value)
    left = sorted(set(re.findall(r"@([A-Z_]+)@", text)))
    if left:
        print("mkprompt: unfilled slot(s): " + ", ".join(left), file=sys.stderr)
        return 2
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("mkprompt: wrote " + out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
