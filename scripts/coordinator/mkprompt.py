"""mkprompt.py <template> <out> KEY=VALUE ... — fill @KEY@ slots in a prompt template.

Refuses (exit 2) when a slot in the template is left unfilled, so a review never
launches with a literal `@SHA@` in it. `@LANE_SLUG@` defaults to LANE with `/`
replaced by `-`. `@WTROOT@` (the checkout's sibling `.wt` folder) and `@PY@`
(the checkout's venv Python) default to the paths `layout.py` derives, so no
template names a machine.
"""

import re
import sys

from layout import PYTHON, WTROOT


def main(argv):
    template, out, pairs = argv[0], argv[1], argv[2:]
    values = dict(p.split("=", 1) for p in pairs)
    if "LANE" in values:
        values.setdefault("LANE_SLUG", values["LANE"].replace("/", "-"))
    values.setdefault("WTROOT", WTROOT.as_posix())
    values.setdefault("PY", PYTHON.as_posix())
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
