+++
id = "WI-618"
title = "Record retired spine rows as structured fragments in docs/log.d/retired/, amending D-4 (S4)"
workstream = "scripts"
specref = ""
buildtier = "medium"
priority = 2
safety_class = "ordinary"
+++

## Deliverable

Built by one builder in three commits with three Codex Sol rounds (wave-5
arbitration rulings 48 and 50), SOUND at 63ef10c1.

- **D-4** in `docs/repo-lock.md` names the retirement fragments as the
  structured home.
- **A deletion writes its fragment in the same commit.** `retire.py <ID>
  --reason ... [--successor] [--date]` cuts the SN, SR, LLR or TC row as text
  and accepts the cut only if the file then parses to the old document minus
  exactly that row. It writes `docs/log.d/retired/<ID>.md` (TOML front matter
  with id, date, successor and reason, and nothing after the fence), and
  checks everything before it writes anything. A test drives
  `trunk_step.py --compile-log` over a fragment and shows it stays.
- **The census of ids spent before the record began** is
  `docs/log.d/retired/before-the-record.toml`. `--seed` writes it once,
  `--exclude` keeps ids reserved by lanes still building out of it, and
  `--replace` rewrites only a census that has not landed. The coordinator
  regenerated it on trunk at this merge with WI-620's reserved ids excluded.
- **The two warn-first checks**: a spent id with neither a record nor a
  place in the census; and a record changed or removed after it landed,
  read from git blobs. The second is reported as "append-only status
  unverifiable" where a shallow clone cannot see the landing.
- **The dashboard renderer**: a Retired tab once a record exists. The
  deleting commit is read from git, and `gen_trajectory --check` accepts
  "unknown" only where the checkout cannot resolve it.
- **The template** gains the `orphans-allow` line, and RESYNC_PACK has its
  entry. **PROCESS.md** says the fragments are for lookup, not browsing
  (+260 bytes, watched).

New Drafted rows: SR-226 (a labelled derived requirement on SN-010,
MAINTAINER lens), LLR-286, LLR-287, TC-299, TC-300, IF-257 (the record and
census files) and IF-258 (`retire.py`'s command arm). IF-102's `requestors`
gained `scripts/retire` (a traced cell).

## Context

Ruled by the owner 2026-09-23 on a condition: fragments are for lookup, not
browsing, stated in PROCESS.md and not in AGENTS (sister plan S4, §1.4). The home
was revised 2026-09-24 to `docs/log.d/retired/`, because `trunk_step.py` folds
and deletes every top-level `docs/log.d/*.md` and its glob does not recurse.

D-4 says a superseded row is deleted and its history lives in git and the log;
a structured record is a third home, so this is an amendment. The shape: id,
date, successor if any, reason, written in the same commit as the deletion. No
self-referential hash: the dashboard resolves the deleting commit from git at
render time and shows *unknown* in a shallow or squashed clone. Append-only by
check, warn-first: a fragment edited after it lands, and a spent id with no
fragment from the day the rule starts.

## Done-when

- D-4 in `docs/repo-lock.md` names the retirement fragments as the structured
  home.
- A deletion writes its fragment under `docs/log.d/retired/` in the same
  commit, and a test drives `trunk_step.py --compile-log` over one and shows it
  stays.
- The two warn-first checks and the dashboard renderer exist; the template
  gains the `orphans-allow` line and `RESYNC_PACK.md` an entry.
- PROCESS.md says the fragments are for lookup, not browsing.
