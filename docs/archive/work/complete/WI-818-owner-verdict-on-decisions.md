+++
id = "WI-818"
title = "The owner's verdict on a delegated decision: confirmed or overruled, and an overrule is acted on"
workstream = "process"
specref = ""
sr_refs = ["SR-225"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

A delegated-decisions entry's `reviewed` key retires for `owner = "confirmed" | "overruled"` (absent: not yet seen); `migrate_decisions.py` rewrites a record's statements in place, keeping comments, line endings and every unrelated byte, and refuses an unparseable record (a forced migration, migrated here). Overruled entries leave the review queue for their own heading in `open-items.html`, each with the work items that cite it. The ruling-sync step refuses, at the pre-commit hook and on each lane commit in the merge slot, a commit that newly overrules an entry unless the same diff files or amends a queued or active work item citing `docs/decisions/<run>.toml#D-NNN`; a record in the commit's tree that does not parse refuses, path lists are read NUL-delimited without loss, and a path that is not UTF-8 refuses where a sync reads it (D-014). A run name carrying `#` or a character git refuses has no record (`record_path` raises; the merge refuses it when a record is owed), so a citation parses one way; `/` still becomes `-`, and `a/b` and `a-b` sharing one file is a stated residue filed as an owner item. To stay under the 1000-SLOC threshold the overrule sync moved to `kitlib/decisions.py` and the path and blob readers to `kitlib/git.py` (D-012). Rows: LLR-303, LLR-304, TC-319 and TC-320 approved; SR-225, LLR-283, LLR-284, TC-293, TC-294 and TC-313 re-attested (act seq 36; verdicts 001 to 003 and `dispute-1-ruling.md`, which upheld Sol's round-4 MAJOR and accepted D-001, D-004, D-005 and D-014). Codex 6.1 Sol: five rounds, the last SOUND. Decisions: `docs/decisions/wi-818.toml`.

## Context

Filed by hand by the coordinator on 2026-10-04 at the owner's direction. Marking
eleven high-risk delegated decisions in session, the owner said: "I wouldn't expect
decisions to carry approval since they are already a selected direction. They are
either confirmed by the user or overruled (or empty / ignored)." Asked whether to
file the change as a row: "Yes that sounds appropriate".

Today a delegated-decisions entry carries one key, `reviewed`
(`kitlib/decisions.py`, WI-790; SR-225, LLR-283, IF-255). It answers only "seen or
not": an owner who disagrees with a decision has no way to say so, and "reviewed"
does not record which way the owner went. Any value outside the boolean vocabulary,
`"confirmed"` included, is a format finding and keeps the entry in the queue.

The change gives the owner's verdict its own key and makes an overrule actionable:

- one key, `owner`, with two values, `confirmed` and `overruled`; absent means not
  yet seen. The `reviewed` key retires: it is migrated, never read beside the new
  key;
- an overrule states the direction instead in the entry's `review` note;
- an overrule is coupled to work at the commit, as OI-102 Q3 coupled a ruled open
  item to its citing row: the commit that marks an entry overruled must, in the
  same commit, file or amend a work item that cites that entry. No history walk,
  no marker convention. A new row is not always needed (owner, 2026-10-04): a
  decision scoped to a queued work item is overruled by amending that row's prose
  to the new direction and citing the entry from it, with nothing minted.

Who sets the key stays a convention (the owner, or an agent at the owner's stated
direction, recorded in the note): git cannot tell the owner's commit from an
agent's without a marker convention, which the owner has ruled out.

WI-808 (one landing per lane) also amends SR-225: it moves WHERE the record is
checked (every landing); this row changes WHAT an entry records. Neither needs the
other; whichever lands second amends SR-225 on top of the first.

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

## Done-when

- `owner = "confirmed"` and `owner = "overruled"` are the only recognized values;
  an absent key reads as not yet seen; any other value, and the retired `reviewed`
  key, is a format finding and reads as not yet seen.
- An `overruled` entry with a blank `review` note is a format finding.
- The commit that sets an entry `overruled` is refused, at the pre-commit hook and
  again by the merge slot on each lane commit against its parent, unless the same
  commit files or amends a queued or active work item whose spec cites that entry
  (the citation form, e.g. `docs/decisions/<run>.toml#D-NNN`, is fixed by this
  row's build). Amending the existing queued row the decision is scoped to
  satisfies it: an overrule never requires a new row to be minted.
- The owner surface lists entries not yet seen under "Decisions to review" (high
  risk first, as today) and overruled entries under their own heading with the
  citing work item, so an overrule never disappears silently.
- A migrator rewrites `reviewed = true` to `owner = "confirmed"` (keeping each
  note) and drops `reviewed = false`; this repo's records are migrated with it.
- `decisions.template.toml`, the decisions note handed to delegated sessions, and
  the `session-protocol` skill's wording are updated.
- SR-225, LLR-283 and IF-255 are amended and pass adjudication of each row, on
  whichever adjudication path is the one path when this row lands.
- Tests: each value; an unknown value; the retired key; an overrule with no note;
  an overrule with no citing work item refused at commit and at the merge slot; an
  overrule filed with a new citing row passing; an overrule that amends the
  existing queued row it is scoped to passing, with no row minted; the migrator on a fixture record.
- The row's test bar: its affected modules' tests plus the smoke tier at `-n 2`.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit. A forced migration, flagged as
  such: adopters run the migrator at their next resync (the owner accepted the same
  shape for WI-788's Q-1).
