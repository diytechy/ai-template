+++
id = "WI-@F@"
title = "Choose the needs carrier from the file, not by sniffing its text, in draft_ids_from_text"
workstream = "scripts"
specref = "project-trajectory/scripts/spine_carrier.py"
buildtier = "quick"
safety_class = "ordinary"
priority = 5
+++

## Context

`spine_carrier.draft_ids_from_text` decides between the TOML and markdown
needs carriers by trying a TOML parse and looking for the need table's name
in the text. The needs loader already takes the carrier from the file's
suffix, after a comment-only TOML needs file read as markdown and a need id in
a comment joined the need universe. This function still sniffs, so the same
misreading remains possible on its path.

IN SCOPE: pass the carrier (or the path) in from its callers and remove the
content sniff; a test pins a comment-only TOML file with an id in a comment.

## Done-when

- `draft_ids_from_text`'s carrier comes from its caller, and no text-based
  carrier guess remains on that path.
- The comment-only TOML test passes, and the commit bar passes.
