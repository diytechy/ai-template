# Approval contract schema and launch timing — authoring record

Status: authoring only. This record grants no approval and changes no live
requirement, test, snapshot, or runtime source.

The reviewed design carrier was corrected in two representational places after
implementation exposed ambiguity:

- The minimum `[[decision]]` shape now includes its required `registry` path and
  states that each `before`/`after` cell value is the registry blob identity
  containing that cell.
- Each `[[absorption]].cells` value now has the implemented nested
  `{ before = <registry blob>, after = <registry blob> }` shape.
- The WI-605 migration text now separates the already recorded supervisor
  holder transfer from selection. The repair commit leaves WI-605 queued. After
  the repair is frozen and the pause-removal launch commit lands, the supported
  dispatcher creates `turn.toml`; consequently its immutable `turn.base` is
  that actual clean launch base, never the earlier repair commit.

No decision classification, authority, scope, census, review, publication, or
migration meaning changed. The corrected design carrier SHA-256 is
`b2c434dda6ae490fbbf137c1e8052faf408c9bede7ddb156d539902909ae5793`.
Independent review is still required.
