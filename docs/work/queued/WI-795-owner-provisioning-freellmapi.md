+++
id = "WI-795"
title = "Owner provisioning: the FreeLLMAPI endpoint and pinned models"
workstream = "process"
specref = "docs/requirements/open-items.toml#OI-105"
needs = ["OI-105"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04, as the queued placeholder that
puts OI-105 on the owner's surface: an open item is filed together with the
queued row that cites it. The owner moved WI-788's checkpoint question Q-4 into
its own item: the FreeLLMAPI router is not running yet, so the route row and its
one live call wait for it, while S788-routes builds everything that needs no
endpoint.

The ruling of OI-105 writes this row's Done-when in the same commit, as the rule
for citing rows requires: once the endpoint and pinned ids are named, the
FreeLLMAPI route row ships (only with a one-model chain per pinned id) and its
one live call is recorded.
