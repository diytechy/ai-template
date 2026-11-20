## 2026-11-19 — WI-1009: docs/open-items.html lists no delegated decision; the operator reads them in their record files

Deferred open items: none.

Built on the maintenance branch `maint/wi-1009`, cut from `refactor_again` at
`6a78f63a7`, outside the lane workflow at the operator's direction: no claim,
no lane review rounds, commit hooks on. The parent session reviews and merges.

- **The ruling.** The scope critique left the surface open among a page of
  its own (a), a terminal listing (b) and the record files themselves (c).
  The operator chose (c): "I thought there was already a decisions.toml
  file? ... I think that would be the preferable location. No html / more
  formally generated report needs to be here." A second ruling the same day
  (B5) had the code and tests that served only the section cut with it.
- **The page.** "Decisions to review" is gone, with its cards, its overruled
  heading and the work items it showed beside each overrule. The page went
  from 2,001,004 bytes to 77,757. One part of the section was a check, not a
  listing: each record's format findings. Nothing else reports them across
  all records whatever the dial (the merge slot reads only a closing lane's
  own record, and only under a recording dial), so they stay on the page, in
  a notice closing section 3, shown only when a record carries one. Today it
  names four: three blank `alternative` cells in `wi-798.toml` and a missing
  `review` in `wi-880.toml`.
- **The status line.** `docs/status.md` now reads "Delegated decisions not yet
  seen: 1141 — docs/decisions/", linking the directory, where it linked the
  removed anchor. It is kept because nothing else counts the unseen entries
  across 132 files.
- **The rows.** SR-225 says each run's record is the listing the operator
  reads, an entry there with no verdict being not yet seen, and keeps every
  check it promised. LLR-118, LLR-283, TC-123 and TC-293 follow. All five stay
  `Accepted` and owe the operator a re-accept: the page's acceptance section
  now carries 7 SR chains, up from 5. IF-074 and IF-164 (Drafted) follow too.
  DA-020 reads true as it stands. No id minted.
- **Shipped.** The template's header and `PROCESS_OPTIONS.md` send the
  operator to the record files; the RESYNC entry forces nothing and migrates
  nothing.
- **Left.** `kitlib.decisions.review_queue` still orders its lists and returns
  overruled entries and a confirmed count that nothing renders; its call
  contract is IF-256's, and WI-1004 works in that file. The 1,141 unseen
  entries are the operator's to read or mark.
