+++
id = "WI-362"
title = "backlog_staleness's 'any reviewed edit re-affirms' promise is FALSE for a Title edit (measured at the Phase 5 fixture conversion). The Title drives the spec FILENAME, so re-titling a WI renames its file, and _path_commit_time(row_history=True)'s `--follow --diff-filter=AM` pair — the exact flags Phase 2b measured in to keep a pure STATUS move from resetting the clock — filters the rename commit out even when it also changed content: the row keeps its pre-edit commit time and the amended-SR warn persists after a genuine re-affirmation. Same-path content edits re-date correctly. A downstream author re-titling a WI to re-affirm gets a warn that will not clear. Candidate fixes to MEASURE (this clock has been wrong in both directions already — the 2b four-way flag test is the precedent): treat an R<score> record whose content ALSO changed as a re-date (rename detection with content-delta discrimination), or document that re-affirmation touches frontmatter/body, never the Title, and say so in the warn text. Whatever lands must extend tests/test_wi_folder_loaders.py's staleness mutation proofs with the rename+content case in both directions."
workstream = "scripts"
buildtier = "medium"
priority = 2
safety_class = "ordinary"
order = 362
+++

## Deliverable

DONE 2026-07-29 in the owner-NARROWED form (no rename detection): the staleness warns share BACKLOG_REAFFIRM_HINT naming the WI's own docs/work/ spec file and the rename blind spot; the blind spot is PINNED both directions (a retitle+content edit does not re-date; a same-path edit does). Bonus measured corrections: _path_commit_time's docstring claimed rename+edit re-dates — measured FALSE (R064 is filtered; only a big rewrite reads as A and re-dates), now stated correctly; a fixture that modeled an impossible re-affirmation fixed; the review then caught the hint pointing at 'the spec' (readers would edit the SpecRef target, which can NEVER clear the warn) — reworded to the file the clock actually reads.
