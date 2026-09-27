+++
id = "WI-663"
title = "Fix the invalid noqa directive ruff reports in the stage-ladder test"
workstream = "tests"
specref = "tests/test_stage_ladder.py"
buildtier = "quick"
safety_class = "ordinary"
priority = 6
+++

## Context

`ruff check tests/test_stage_ladder.py` warns: "Invalid `# noqa` directive
on tests/test_stage_ladder.py:41: expected `:` followed by a comma-separated
list of codes". Line 41 is a comment that mentions a "`# noqa`-style
exemption" in prose, which ruff parses as a directive.

IN SCOPE: reword the comment so ruff stops reading it as a directive, without
changing its meaning.

## Done-when

- `ruff check tests/test_stage_ladder.py` prints no warning, and the commit
  bar passes.
