+++
id = "WI-381"
title = "DESIGN DRAFT (docs/concurrency-v2.md §2) - do not claim until that doc is settled. Make the spine barrier real: a spine-class WI must WAIT for all lanes to return to the station (no open claims), then run as the ONLY thing touching trunk, and ALL spine WIs admit together as one batch so N spine changes cost one re-attest window and one owner sitting rather than N. Spine work takes priority so it drains rather than starving behind ordinary work. Note this is largely making an existing declaration TRUE rather than new machinery: schedule.py already classifies spine|gate|attestation -> serial-whole-project and protected -> protected-serial, but _disposition() still returns ready for those rows and the only enforcement is integrate.py's blunt claims-ordinary-only refusal - a hard stop, not a wait. Also covers the mid-flight case: a WI that discovers it needs spine work must either finish what it can and queue a spine WI for the rest, or report that it cannot complete - never do the spine work inline (which is what WI-280 did under an honest-at-filing ordinary class). Open: whether the batch is admitted by the dispatcher (which can wait) or a claim rung (which can only refuse)."
workstream = "scripts"
specref = "docs/concurrency-v2.md"
buildtier = "medium"
safety_class = "ordinary"
+++
