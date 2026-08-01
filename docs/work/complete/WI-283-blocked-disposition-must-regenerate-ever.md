+++
id = "WI-283"
title = "Blocked-disposition must regenerate every floor-checked artifact - live 2026-07-23 failure: flipping a row to Status=blocked feeds the generated pending owner-actions projection, blocked_disposition regenerates the snapshot but not that projection, so its own commit fails the status-map floor deterministically (train 3-g3-WI-273-b45e parked state=error) and the coordinator never reaches its SR-084 critique obligation; single-home the regen list with the floor's checked set"
workstream = "scripts"
buildtier = "medium"
priority = 1
safety_class = "ordinary"
order = 280
+++

## Deliverable

Integrated from train p0-g3-WI-283-87ef @ b7efec7: WI-283: blocked-disposition regenerates every floor-checked artifact
