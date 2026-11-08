## 2026-11-08 — WI-1000: the shipped registry templates and ID vocabulary are scanned for language-specific tokens

Deferred open items: none.

A new in-process test scans the shipped registry templates, the work-item
scaffold, the id-watermark template and the ID vocabulary's declarations for a
declared token set, under the spec's closed matching rule, with the kit's own
script names exempt (coordinator-2026-11-08 D-004, for the owner to confirm or
overrule). The profile permutation test now runs the strict schema tier too,
and TC-165's evidence names both tests.

- Headless leg 39 critiqued the row (round 1 CHANGES-REQUESTED, round 2
  confirming APPROVE), claimed it, built it, and ran three counted rounds. Round
  1's MAJOR (wildcard and backslash paths slipped through) and round 2's MAJOR
  (the fix made an extension end only at a separator, so Markdown emphasis or
  a link anchor hid a path) were fixed with regression tests that fail on the
  pre-fix scan; round 3, in convergence stance, raised one MINOR. No row text
  changed, so no sitting or act was owed (wi-1000 D-001, D-007).
- Follow-ups, not built here (wi-1000 D-003, D-007): a digit or underscore
  suffix (`python3`, `pip3`, `python_requires`) defeats the word boundary; on
  an unmodified scaffold the schema tier sweeps no real row, so TC-165's
  schema half cannot fail as worded; upper-case extensions and kit-script
  names are not pinned by a case.
