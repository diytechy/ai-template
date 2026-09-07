"""Typed adjudication verdict grammar shared by composition and evidence readers."""

import re

VERDICT_GRAMMAR = {
    "amendment": ("VERDICT", ("MEANING", "CLARITY"), ("rows",)),
    "first-approval": ("OUTCOME", ("APPROVE", "RETURN"), ("rows",)),
    "disposition": ("OUTCOME", ("COMPLETE", "PARTIAL", "CANCELLED"), ("successors",)),
    # The CONSOLIDATION grammar (restructure plan §1.2). Its first three
    # alternatives are the retired `conflict` grammar verbatim; the fourth is
    # the exit that brief lacked, and `absorbs` is the counter that makes it
    # readable — a verdict saying CONSOLIDATE without naming what it absorbed
    # is a judgement the close cannot enact. BOTH counters are required on
    # EVERY alternative, `-` being the honest "none": a counter that appears
    # only on the alternative that uses it lets a session omit it and still
    # parse, which is the silent half-verdict `verdict_refusal` exists to
    # refuse.
    #
    # BOTH ARE `;`-JOINED LISTS AND BOTH ARE RECONCILED. `absorbs=` restates the
    # `## Dispositions` draft's `supersedes`, `needs=` the WAITERS of the
    # `## Consolidation` block's `edges` - and `consolidate.reconcile_refusal`
    # refuses the close on any divergence. `needs=` was spelled singular here
    # and in the template while `edges` was already a list, so a conformant
    # two-edge verdict was refused with no way to write one that passed; the
    # grammar, the brief and the check are ONE fact now (review round 3).
    "consolidate": (
        "OUTCOME",
        ("QUEUE", "QUEUE-WITH-EDGE", "RETURN-TO-DRAFT", "CONSOLIDATE"),
        ("needs", "absorbs"),
    ),
    "red-tc": ("OUTCOME", ("DRAFTED", "NEEDS-JUDGEMENT"), ("cases", "drafts")),
    "primary": ("OUTCOME", ("REVIEWED", "RETURN"), ()),
}


def verdict_text_refusal(brief, text, verdict_path, scope=None):
    """The same grammar for a committed blob and a live verdict artifact."""
    keyword, labels, counters = VERDICT_GRAMMAR.get(brief, (None, (), ()))
    if keyword is None:
        return "unknown brief {!r} — no verdict grammar".format(brief)
    matched = re.search(r"^\s*{}:\s*(\S+)(.*)$".format(keyword), text, re.M)
    if matched is None:
        return "{} carries no `{}:` machine line".format(verdict_path, keyword)
    label, rest = matched.group(1).strip(), matched.group(2)
    if label not in labels:
        return "{} says `{}: {}` — not one of {}".format(
            verdict_path, keyword, label, "|".join(labels)
        )
    missing = [c for c in counters if not re.search(r"\b{}\s*=\s*\S+".format(c), rest)]
    if missing:
        return "{} says `{}: {}` but omits {}".format(
            verdict_path, keyword, label, ", ".join(missing)
        )
    if scope is not None and "rows" in counters:
        count = re.search(r"\brows\s*=\s*(\S+)", rest).group(1)
        if count != str(len(scope)):
            return "{} row count does not equal the selected Adjudicates scope".format(
                verdict_path
            )
    return None
