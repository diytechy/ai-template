+++
id = "WI-174"
title = "check_docs multi-backtick inline code-span strip - a quoted markdown-link example uses a double-backtick span (the label holds backticks) but INLINE_CODE_RE only matched single-backtick spans so the run mis-split and leaked a phantom empty-text broken link; discovered running WI-171 (it reddened the meta commit bar via the 093/094 review docs that quote WI-173's link fix)"
workstream = "scripts"
needs = ["WI-013"]
buildtier = "quick"
order = 173
+++

## Deliverable

INLINE_CODE_RE matches an N-backtick opener only at a run boundary and closes only on an exactly-N non-adjacent run; parse_doc strips spans across the whole unfenced document while preserving embedded newlines and finding line numbers. This removes quoted-link false positives without allowing a longer closer to hide a real link. Regression coverage includes same-line real links, unequal runs, and multiline spans.
