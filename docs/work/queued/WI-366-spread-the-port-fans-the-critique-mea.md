+++
id = "WI-366"
title = "Spread the port fans the WI-323 advisory critique measured FUSED (docs/reviews/WI-323-CRITIQUE.md, pixel-measured 2026-07-29): strokes leaving a shared port should reach >= 8 CSS px separation within ~15 CSS px of the port. Two named sites on the Roadmap DAG at 1680px: right of the unphased block's port (two edges at 2.5-3 CSS px pitch for ~55 CSS px of descent - reads as one thick line; was 3.5-5.5px and diverging BEFORE) and right of block 1's port (a NEW 25 CSS px fused stretch the WI-323 lane stack introduced - two edges render as one from y~378 to the port). The critic also found the How-SW emitter's new lanes at 8 CSS px pitch where the roadmap's floor is 10, plus a pre-existing 4.5px SW pair - unify the floor. The implementer's note stands: fan offsets are computed by the caller BEFORE routing, so corridor-aware fans need a two-phase pass - but the critic's ask is narrower (stagger departure offsets near the port), so measure whether the narrow form suffices before building the rewrite. Perceptual clause: no crossing-count proxy (standing rule); judged by before/after shots + the periodic advisory critique."
workstream = "dashboard"
specref = "docs/reviews/WI-323-CRITIQUE.md"
buildtier = "medium"
priority = 2
safety_class = "ordinary"
+++
