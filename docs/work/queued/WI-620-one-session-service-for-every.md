+++
id = "WI-620"
title = "One session service for every model call (act, keep, record), writing the adopted OTel usage schema (S7, S8)"
workstream = "unattended"
needs = ["~WI-605", "~WI-606"]
specref = "docs/plans/2026-09-23-owner-notes-spine-sessions-and-tests.md#31-a-common-session-service-note-1"
buildtier = "strong"
priority = 3
safety_class = "ordinary"
+++

## Context

Ruled by the owner: S7 (2026-09-23, option (a): "refactor as much as possible
to reduce individual or custom code components") and S8 (2026-09-24), sister
plan §3.1 and §3.2.

- **act:** a role differs only in data (brief, route, tier, tool set), never in
  its own launch code.
- **keep:** resume by id, keep warm, reset. WI-551 lands through this
  operation, so its keep-warm ping is an ordinary recorded call.
- **record:** one writer replaces the loop's in-line logging and
  `invoke_and_persist`. It writes S8's schema: OTel GenAI usage names pinned to
  a commit, inclusive input, fresh input derived, raw usage verbatim, provider
  and CLI columns, billed tokens apart from context occupancy; exporters are
  optional.
- **provider differences** live in one adapter per provider (argument
  building, output and usage parsing). Claude's two parse defects
  (`reasoning-tokens`, `reported-model`; review pack C2) are fixed in its
  adapter.

WI-606 first captures raw codex and opencode usage; WI-605 fixes occupancy.
The loop's C901 pin (`tests/test_complexity_ratchet.py`) still applies:
decompose, don't re-stamp. It is large; slice it at claim if needed.

## Done-when

- Every model call goes through the service; no role or provider keeps its own
  launch or logging path (grep evidence of the removed paths, and the SLOC
  removed).
- The record step writes the S8 schema for Claude, codex and opencode, pinned
  to a named OTel commit, with raw usage verbatim; a fixture test per provider.
- Claude's `reasoning-tokens` and `reported-model` defects are fixed in its
  adapter.
- The service exposes the keep operation WI-551 lands through.
- The C901 pin and the module-size ratchet hold without re-stamping.
