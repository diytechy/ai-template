"""HANDOFF 10.6, the glossary (hand-only): the "commit checks" entry rewritten
for `integrate.py record-checks`, and the failed-checks record added from
4.5.1's draft (D16), with its header spellings beside the passed-checks
record's grammar.
"""

G = "project-trajectory/GLOSSARY.md"

EDITS = [
    (G,
     "The [required checks](#required-checks) for a commit a lane attests.\n"
     "`integrate.py attest` runs the named [check suite](#check-suite), then the\n"
     "row's derived review tests, and records the green in the commit. Formerly the\n"
     "\"commit bar\" and the \"review bar\", two words for one thing; **commit checks**\n"
     "is kept. The attestation's recorded name is still `review` (the trailer reads\n"
     "`Bar-Green: ... bar=review`).\n",
     "The [required checks](#required-checks) for a commit a lane builds.\n"
     "`integrate.py record-checks --checks commit` runs the named\n"
     "[check suite](#check-suite), then the row's derived review tests, and when\n"
     "both pass commits the lane's staged work carrying a\n"
     "[passed-checks record](#passed-checks-record) with `checks=commit`. When they\n"
     "fail, the loop writes a [failed-checks record](#failed-checks-record).\n"
     "Formerly the \"commit bar\" and the \"review bar\", two words for one thing;\n"
     "**commit checks** is kept.\n"),
    (G,
     "**passed-checks record** is kept, and a trailer in the earlier form is not\n"
     "read.\n"
     "\n"
     "### gate checks\n",
     "**passed-checks record** is kept, and a trailer in the earlier form is not\n"
     "read.\n"
     "\n"
     "### failed-checks record\n"
     "\n"
     "The two header lines a build's session log carries when its\n"
     "[commit checks](#commit-checks) failed: the build commit they refused and a\n"
     "one-line summary, written `# checks-failed: <sha>` and\n"
     "`# checks-summary: <line>`. The\n"
     "[commit-check failure cap](#commit-check-failure-cap) counts these since the\n"
     "last [passed-checks record](#passed-checks-record). Formerly the \"red\n"
     "record\", written `# bar-red:` and `# bar-summary:`; **failed-checks record**\n"
     "is kept, and headers in the earlier form are not read.\n"
     "\n"
     "### gate checks\n"),
]
