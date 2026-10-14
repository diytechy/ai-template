+++
id = "WI-910"
title = "The full suite is green on macOS: the run.command fixture runs an executable run.sh, and the dispatch lane-worktree flake is explained"
workstream = "process"
sr_refs = ["SR-046", "SR-032"]
specref = "docs/specs/WI-910.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 2
needs = ["WI-909"]
+++

## Context

Filed by hand on 2026-10-13 at the owner's direction: "drill through to see
if there is anything else related to Mac failures, and make a single WI to
cover that scope". WI-909 fixed the first Mac failure (the hooks' probe did not
parse under bash 3.2). This row holds what the drill found after it: how the
drill ran, its two findings and why they went unseen are its spec of record,
`docs/specs/WI-910.md`.

## Done-when

- The `run.command` cases pass on macOS and Linux: the fixture gives the
  copied launchers their exec bit, as bootstrap does. Whether to also track
  `run.template.sh`/`.command` as `100755` is decided and recorded either way.
- Finding 2 is either reproduced and fixed at its cause, or recorded as not
  reproducible with the attempts named. If the suspect holds, git's failure
  surfaces as the refusal's reason instead of reading as "no holder".
- The full unfiltered suite is green on the Mac, with the command, revision
  and result recorded. The CI macOS and Linux jobs' state on the branch tip is
  checked and recorded.
- The finding that the suite's recent full runs could not see a POSIX-only
  failure is carried to the owner as a question: whether the full suite should
  also run on a POSIX box before phase close, beyond CI.
