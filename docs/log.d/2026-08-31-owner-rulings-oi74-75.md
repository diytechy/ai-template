## 2026-08-31 — the owner rules OI-74 (the pure-TOML per-run decisions record, review state in place) and OI-75 ((b), the decision_recording dial)

Deferred open items: none — the two rows this entry names are both ruled by
it, and no other row is pending.

Both rulings were made in session, the owner's words recorded verbatim; each
row's `one_line` and `decision` cells carry the ruling at their head (the
OI-67 convention). The evidence base is
[../knowledge/decision-routing.md](../knowledge/decision-routing.md).

### OI-74 — RULED: (a) as amended — pure TOML, review state changed in place, no second record

The owner, on the recommended markdown-plus-frontmatter hybrid: *"All the
other registries are toml, what makes it misrable to author and read? ... It
just seems strange to maintain so many different formats. And if it was toml,
the state could just change (and no machinery needs to check it, it can be up
to the user to make whatever string note they want so some eventual (if ever)
mechanized collator of all decisions could skip any that already has some
review entry. I would pref that over yet another record that needs to be
joined."*

What is ruled. The run stays the unit — every delegated run closes with one
record — but the artifact is a PURE-TOML file, one per run (conflict-free the
way `log.d` fragments are), entries as tables with REQUIRED keys (`decided`,
`alternative`, `reversal_cost`, `why_not_escalated`) plus `review = ""`. An
empty `review` is unreviewed; any owner-written string marks it reviewed,
with semantics the owner's own. The file is edited in place and is NOT
immutable; there is no separate approval record, no join, and no review-state
checker — an eventual collator, if ever built, skips entries whose `review`
is non-empty. The high-risk hoist, the overturn-mints-a-WI rule, the
all-altitudes coverage, and the record-is-not-an-exit framing (OI-70/OI-73
remain the only exits) all stand from the brief. The driver's hybrid-format
argument was conceded on the owner's evidence: the open-items registry itself
authors long prose in TOML.

### OI-75 — RULED: (b), the named-mode dial now

The owner: *"Hmmm, this is the interesting dial. I would say 2."* — option
(b), over the recommendation's defer-and-measure.

What is ruled. One `[attestation]` key: `decision_recording = "off" |
"record" | "escalate-first"`. `off` — no recording obligation; the template's
shipped value. `record` — a delegated run's close OWES the OI-74 record, the
way a partial close owes its handback report; this repo's value.
`escalate-first` — beyond recording, sessions prefer the OI-70/OI-73 exits
over deciding. Single line, closed alphabet, IF-037 grep-parity, structural
template-vs-repo parity under the dogfood-sync test. The routing doctrine
rides with it: route on action fields and counts, never model
self-confidence as a primary (confidence and panel dissent may only promote
scrutiny, never demote it); disclosure is structural via the required entry
keys; the dial allocates the owner's workload and never moves the safety
boundary — the escalate class binds at every setting.

What the two rulings commission: `WI-557` — the record format and its
per-run naming, the close-time obligation under the dial, the dial itself in
`process.toml` and its template, and the doctrine text where delegated
sessions read it. One row; the rulings are executed there.
