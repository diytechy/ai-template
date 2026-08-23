+++
id = "WI-241"
title = "Harden REVIEWER_PROMPT with the three field-proven adversarial clauses + the code-review-adversarial rubric (owner directive 2026-07-19)"
workstream = "unattended"
sr_refs = ["SR-154"]
buildtier = "medium"
safety_class = "ordinary"
order = 238
+++

## Deliverable

Three adversarial clauses (drive-the-real-paths, severity-ordered failure classes, verdict discipline) added to REVIEWER_PROMPT (2096->2695 bytes, load-bearing bones byte-unchanged); docs/rubrics/code-review-adversarial.md (anchors R1-R5) reachable via log.md; test_reviewer_prompt_carries_adversarial_clauses asserts the clauses + unchanged redaction/verdict lines on the deployed prompt.
