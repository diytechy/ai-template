+++
id = "WI-354"
title = "A WI's SpecRef anchor is never validated, so a row can cite a heading that does not exist. check_trajectory's R-E resolves a SpecRef by splitting on '#' and testing only that the PATH exists (check_trajectory.py:1113-1130); the fragment is discarded unread. Found 2026-07-28 closing WI-326, whose row had cited 'docs/log.md#2026-07-26--wi-326-a-green-that-hid-47-tests' since it was filed - a truncated slug matching no heading in that file. Nothing surfaced it for two days; it surfaced only because the close wrote the same anchor into a markdown LINK, where check_docs rejected it immediately. So the identical reference is enforced in one home and unchecked in the other, which is the WI-308 doc-refs class one registry over: a citation whose target moved or was never there reads as traceable and is not. Fix: have R-E resolve the fragment too when the path is a markdown file - slugify the file's ATX headings the same way check_docs already does and reuse that, do not write a second slugifier - and report the WI id, the ref, and the nearest matching heading, because a wrong anchor is nearly always a stale or truncated one rather than an invented one. Guard with a row citing a real file and a bogus anchor, asserting it is caught, plus its twin citing a real anchor asserting it is not; run the new check over the live registry before landing, since more rows than WI-326 may be wrong."
workstream = "scripts"
buildtier = "quick"
priority = 1
safety_class = "ordinary"
order = 351
+++

## Deliverable

R-E now resolves the ANCHOR half of a doc#anchor SpecRef, not just the path: specref_findings() reuses check_docs.parse_doc for the anchor set (one slugifier, so a reference cannot pass as a SpecRef and fail as a link) and reports the nearest heading, prefix-first so a TRUNCATED slug names its full form. Lazy sibling import degrades to path-only rather than breaking the shipped hook. Extracted from ssot_findings to stay under the C901 limit. Live registry measured clean (6 anchored rows, re-derived at close); the test that pinned "anchor ignored by R-E" became the positive case.
