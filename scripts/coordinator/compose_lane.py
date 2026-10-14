"""compose_lane.py — compose an in-lane adjudication brief (wave-10 recipe).

Run FROM THE LANE ROOT with the repo venv:

    python C:/Projects/ai-template.wt/coordinator-tools/compose_lane.py \
        WI-NNN <brief> "<ID;ID;...>" "<SR;SR>" <verdict-path> <out.md>

<brief> is the adjudication kind the merge would mint (`amendment` or
`first-approval`); the row is the lane's own work-item row with `Brief`,
`Adjudicates` and `SR-Refs` overridden, exactly as the coordinator composed
WI-688's and WI-787's briefs. The kit's own `adjudicate_brief.compose` fills
it, so the adjudicator reads the brief the merge's mint would hand a sitting.
"""

import sys
from pathlib import Path

sys.path.insert(0, "project-trajectory/scripts")
import adjudicate_brief  # noqa: E402
import consolidate  # noqa: E402


def main(argv):
    wi, brief, scope, srs, verdict, out = argv
    root = Path(".").resolve()
    rows = {r["WI-ID"]: r for r in consolidate.read_rows(root)}
    if wi not in rows:
        print("compose_lane: no row {} under {}".format(wi, root))
        return 2
    row = dict(rows[wi])
    row["Brief"] = brief
    row["Adjudicates"] = scope
    row["SR-Refs"] = srs
    body, why = adjudicate_brief.compose(root, row, verdict)
    if body is None:
        print("compose_lane: REFUSED: {}".format(why))
        return 1
    Path(out).write_text(body, encoding="utf-8", newline="\n")
    print("compose_lane: {} {} -> {} ({} chars)".format(wi, brief, out, len(body)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
