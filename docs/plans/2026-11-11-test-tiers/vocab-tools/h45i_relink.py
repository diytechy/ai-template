"""HANDOFF 10.5 pass 4: re-base the links nine records hold into the moved record.

check_docs validates links in history too ("a dead link in the history still
misleads a future reader, and the archival flow re-bases links once at archive
time"). Only the link target changes; the records' words stay as written.
Goes in the record-move commit, with the move that breaks them.
"""

EDITS = [
    ('docs/log.d/2026-09-06-oi85-owner-ruling.md',
     '](../archive/last_approved/docs/requirements/stakeholder-needs.toml)',
     '](../archive/last_accepted/docs/requirements/stakeholder-needs.toml)', 1),
    ('docs/reviews/2026-09-27-wave4/sol-wi675.md',
     '](../../../docs/archive/last_approved/acts.toml)',
     '](../../../docs/archive/last_accepted/acts.toml)', 1),
    ('docs/reviews/2026-09-27-wave4/sol-wi675.md',
     '](../../../docs/archive/last_approved/docs/requirements/low-level-requirements.toml)',
     '](../../../docs/archive/last_accepted/docs/requirements/low-level-requirements.toml)', 1),
    ('docs/reviews/2026-09-27-wave4/sol-wi675.md',
     '](../../../docs/archive/last_approved/docs/test/test-cases.toml)',
     '](../../../docs/archive/last_accepted/docs/test/test-cases.toml)', 1),
    ('docs/reviews/2026-09-27-wave5/sol-batchb-fix.md',
     '](../../../docs/archive/last_approved/acts.toml)',
     '](../../../docs/archive/last_accepted/acts.toml)', 1),
    ('docs/reviews/2026-09-27-wave5/sol-batchb-fix2.md',
     '](../../../docs/archive/last_approved/acts.toml)',
     '](../../../docs/archive/last_accepted/acts.toml)', 2),
    ('docs/reviews/2026-09-27-wave5/sol-batchd-fix2.md',
     '](../../../docs/archive/last_approved/README.md)',
     '](../../../docs/archive/last_accepted/README.md)', 1),
    ('docs/reviews/2026-09-27-wave5/sol-batchd-fix2.md',
     '](../../../docs/archive/last_approved/acts.toml)',
     '](../../../docs/archive/last_accepted/acts.toml)', 3),
    ('docs/reviews/2026-09-27-wave5/sol-batchd.md',
     '](../../../docs/archive/last_approved/README.md)',
     '](../../../docs/archive/last_accepted/README.md)', 1),
    ('docs/reviews/2026-09-27-wave5/sol-batchd.md',
     '](../../../docs/archive/last_approved/acts.toml)',
     '](../../../docs/archive/last_accepted/acts.toml)', 1),
    ('docs/reviews/2026-09-27-wave5/sol-batche.md',
     '](../../../docs/archive/last_approved/acts.toml)',
     '](../../../docs/archive/last_accepted/acts.toml)', 1),
    ('docs/reviews/2026-09-27-wave5/sol-batchf-fix.md',
     '](../../../docs/archive/last_approved/acts.toml)',
     '](../../../docs/archive/last_accepted/acts.toml)', 3),
    ('docs/reviews/2026-09-27-wave5/sol-batchf.md',
     '](../../../docs/archive/last_approved/acts.toml)',
     '](../../../docs/archive/last_accepted/acts.toml)', 3),
]
