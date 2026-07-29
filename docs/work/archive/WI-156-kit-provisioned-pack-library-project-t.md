+++
id = "WI-156"
title = "Kit-provisioned pack library - project-trajectory/knowledge/ + opt-in scaffold wiring + staged research-pack import (6 packs)"
workstream = "scripts"
needs = ["WI-152"]
order = 155
+++

## Deliverable

Added a six-pack curated library under project-trajectory/knowledge with domains frontmatter: web (UI/design systems, rendering, model inference) and hardware (perception, kinematics, simulation/robot learning). bootstrap.py --domain explicitly opts into the matching three packs, copies them write-once into docs/knowledge, and extends the pack index without duplicate rows; omitted/any/game/data domains install none. --force deliberately refreshes selected packs. README kit inventory and 2 integration tests cover opt-in/default behavior, indexing, domain metadata, write-once preservation, and forced refresh.
