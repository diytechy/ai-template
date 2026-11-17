"""HANDOFF 10.7 item 1 (4.5.5, 4.5.7, 9.10's leftover), by line (hline.py),
after r47e_checks_rows.py: the rows whose "bar" was not a run of checks.

- A field of the passed-checks trailer (`bar=`, now `checks=`): "a known
  check set", "another check set", "the `checks` field".
- The work-item key of 4.5.2: TC-148's method, TC-? (the draft key).
- A threshold (4.5.7): "standard", "threshold".
- A stage (4.5.5): "stage".
- Reverted: the retired bar axis and its spellings, a glyph ("a bracket, a
  bar or a check mark"), and the migrator's own mapping (`bar` to
  `checks_stage`), which names the earlier key on purpose.
"""

L = "docs/requirements/low-level-requirements.toml"
S = "docs/requirements/system-requirements.toml"
N = "docs/requirements/stakeholder-needs.toml"
I = "docs/requirements/interfaces.toml"
T = "docs/test/test-cases.toml"

LINES = [
    # --- reverts
    (L, 541, "CHECKS/gate axis", "BAR/gate axis"),
    (L, 3833, "as checks to checks_stage", "as bar to checks_stage"),
    (L, 2819, "a bracket, a check run or", "a bracket, a bar or"),
    (L, 1624, "stage-to-checks crossing", "stage-to-bar crossing"),
    (L, 1973, "it carries a CHECKS", "it carries a BAR"),
    (T, 1395, "rather than capping a check run", "rather than capping a bar"),
    (T, 1934, "G-tag and a check run spelling", "G-tag and a bar spelling"),
    (T, 1956, "the checks vocabulary", "the bar vocabulary"),
    (T, 2843, "bracket, checks or check mark", "bracket, bar or check mark"),
    # --- the trailer's field
    (L, 2226, "first parent and checks are in that set", "first parent and its `checks` field is in that set"),
    (L, 2226, "A trailer without checks are not read.", "A trailer without a `checks` field is not read."),
    (L, 3580, "another checks, another test set", "another check set, another test set"),
    (L, 3580, "is another-checks refusal", "is an another-check-set refusal"),
    (L, 3580, "both checks values", "both check-set values"),
    (S, 1913, "names another checks or test set", "names another check set or test set"),
    (T, 2231, "a known checks, and", "a known check set, and"),
    (T, 2231, "missing or unknown checks,", "missing or unknown check set,"),
    (T, 3796, "another checks, and", "another check set, and"),
    (T, 3798, "another-checks and test-set refusals", "another-check-set and test-set refusals"),
    # --- the work-item key (4.5.2)
    (T, 1450, "A declared checks reaches the gate check as its gate", "A declared checks_stage reaches the gate check as its stage"),
    (T, 1450, "an undeclared checks pass no gate", "an undeclared checks_stage passes no stage"),
    (T, 1461, "a bad checks value", "a bad checks_stage value"),
    # --- a threshold (4.5.7)
    (L, 575, "whose checks becomes operational", "whose standard becomes operational"),
    (L, 1144, "the whole checks", "the whole standard"),
    (L, 1660, "deliberately high checks", "deliberately high threshold"),
    (L, 1661, "similarity checks", "similarity threshold"),
    (L, 1588, "refresh's checks directives", "refresh's check directives"),
    (S, 13, "only when its checks are met", "only when its standard is met"),
    (S, 258, "so the checks are a reviewed argument", "so the standard is a reviewed argument"),
    (S, 358, "an accessibility checks left unstated silently reads as no checks at all", "an accessibility standard left unstated silently reads as no standard at all"),
    (S, 373, "uniformity checks", "uniformity standard"),
    (S, 374, "joins the checks by existing", "joins the standard by existing"),
    (S, 388, "The checks are therefore", "The standard is therefore"),
    (N, 131, "mechanical checks are met", "mechanical standard is met"),
    (N, 143, "a check run nothing can check", "a standard nothing can check"),
    (N, 192, "the checks are **argument", "the standard is **argument"),
    (I, 332, "coverage below the checks", "coverage below the minimum"),
    # --- a stage (4.5.5)
    (L, 1769, "at EVERY checks", "at EVERY stage"),
    (L, 1769, "lowest checks", "lowest stage"),
    (S, 7, "enforce their checks", "enforce their stage's checks"),
    (S, 8, "Invoked for a check run, the harness runs that checks' declared steps", "Invoked for a stage, the harness runs that stage's declared steps"),
    (S, 770, "requirements checks on", "requirements stage on"),
    (S, 770, "release checks", "release stage"),
    (S, 1063, "release checks", "release stage"),
    (S, 1091, "gating a check run on it", "gating a stage on it"),
    (T, 151, "including the checks the step is wired at", "including the stage the step is wired at"),
    # --- the stack file's retired section, in a Drafted interface row
    (I, 497, "readability, checks, step:NAME", "readability, check-suites, step:NAME"),
]
