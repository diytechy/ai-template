+++
id = "WI-660"
title = "Choose the needs carrier from the file, not by sniffing its text, in draft_ids_from_text"
workstream = "scripts"
specref = ""
buildtier = "quick"
safety_class = "ordinary"
priority = 5
+++

## Deliverable

`spine_carrier.draft_ids_from_text(text, carrier)` takes the needs carrier
from its caller (the file's suffix) and no longer sniffs the text. `.toml`
reads the TOML status field and `.md` scans the headings. Any other carrier,
and a `.toml` text that does not parse, raises `ValueError`.
`draft_ids_or_refuse(path, text)` turns that error into a refusal naming the
file, and both production callers, `spine_rules.load_spine` and
`trace.load_registries`, go through it. A malformed needs file therefore
refuses rather than deriving a higher stage.

- **Evidence:** `tests/test_spine_carrier.py` covers the comment-only TOML
  file (no drafts), the markdown file that happens to parse as TOML, and the
  unparseable and unknown-carrier refusals. `tests/test_spine_rules.py`
  covers the refusal through `load_spine` and `load_registries`. Each was red
  first, then green.
- **Review:** in the first round Sol held that the unparseable-TOML fallback
  was still a text guess, and one the stage path does not catch. The
  coordinator ruled for Sol (arbitration ruling 6). The fix round was SOUND.
- **Twin:** `needs_from_text` keeps the same sniff. It is filed as **WI-671**.

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
