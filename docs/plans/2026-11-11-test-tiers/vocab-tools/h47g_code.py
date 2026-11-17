"""HANDOFF 10.7 item 1 (4.5.5, 4.5.7, 9.10's leftover), by line (hline.py):
the scripts and tests the phrase map left to a reader, after r47e_checks_*.

Kept as written, each naming the retired bar axis as retired: check.py's
lines on the MIN over rows and the retired tags (586-589, 742-744, 850, 873,
1339-1440, 1471, 2604-2608), check_trajectory.py 1038-1070, trace_text.py's
quoted message, the retired-axis tests (test_check_harness 139-140 and 574,
test_acceptance_level 1243-1246, test_traj_render 164). A visual bar (the
tab bar, check.py's progress bar, the dashboard legend's bars) and a
placeholder (`Bar.stall_verdict`) stay too.

Decision (f): the dashboard's "rung bar" is the glossary's **gate checks**
("the full gate for a stage ... Formerly the 'gate bar'; gate checks is
kept"). test_traj_panels had listed "gate checks" as the deleted axis's name
spelled the new way; the glossary has since kept the term for the full gate,
so the test now asserts it and keeps "gate bar" and "rung bar" out.
"""

S = "project-trajectory/scripts/"
CK = S + "check.py"
T = "tests/"

LINES = [
    # --- check.py: running checks, and a stage where the comment means one
    (CK, 55, "the full bar applies", "the full checks apply"),
    (CK, 57, "and then bars", "and then checks"),
    (CK, 596, "requirements bar has", "requirements stage has"),
    (CK, 604, "# bar has no excuse", "# stage has no excuse"),
    (CK, 746, "AT EVERY BAR", "AT EVERY STAGE"),
    (CK, 749, "the LOWEST bar", "the LOWEST stage"),
    (CK, 763, "At every bar", "At every stage"),
    (CK, 764, "the LOWEST bar", "the LOWEST stage"),
    (CK, 1070, "whose derived bar sits at", "whose derived stage sits at"),
    (CK, 1168, "So the bar now vouches", "So the checks now vouch"),
    (CK, 1173, "AT EVERY BAR", "AT EVERY STAGE"),
    (CK, 1192, "AT EVERY BAR", "AT EVERY STAGE"),
    (CK, 1211, "at every bar", "at every stage"),
    (CK, 1214, "station refresh's bar runs", "station refresh's checks run"),
    (CK, 1239, "at every bar", "at every stage"),
    (CK, 1670, "and bars the result", "and checks the result"),
    (CK, 1673, "the mechanical bar possible", "the mechanical checks possible"),
    (CK, 1754, "while the bar — hook floor and CI alike — refuses.", "while the checks — hook floor and CI alike — refuse."),
    (CK, 1854, "so the bar vouches", "so the checks vouch"),
    (CK, 2279, "its STRICT bar.", "its STRICT checks."),
    (CK, 2298, "STRICT bar applies.", "STRICT checks apply."),
    (CK, 2413, "every commit of a branch is a bar that is not being run.", "every commit of a branch skips the checks."),
    (CK, 2630, "(the hook's sensor bar)", "(the hook's sensor checks)"),
    (CK, 2655, "the station refresh's bar (integrate.py refresh)", "the station refresh's checks (integrate.py refresh)"),
    # --- a threshold
    (S + "check_trajectory.py", 1583, "A lower bar turns", "A lower threshold turns"),
    (S + "coherence.py", 412, "status bar applies", "status rule applies"),
    (S + "coherence.py", 420, "so the bar stands down", "so the rule stands down"),
    (S + "coherence.py", 434, "cleared a bar that asks", "cleared a rule that asks"),
    (S + "coherence.py", 439, "stands the bar down", "stands the rule down"),
    (S + "agent_policy.py", 135, "coverage bar", "coverage minimum"),
    (S + "agent_policy.py", 140, "disarm a bar the repo", "disarm a minimum the repo"),
    (S + "agent_policy.py", 158, "the strictest bar", "the strictest minimum"),
    (S + "agent_policy.py", 159, "reads as a bar that", "reads as a minimum that"),
    (S + "agent_policy.py", 433, "every bar but", "every gate but"),
    (S + "agent_policy.py", 872, "the declared bar", "the declared checks"),
    (S + "gen_arch_map.py", 68, "the bar lives", "the minimum lives"),
    (S + "gen_arch_map.py", 121, "backlink_coverage_min` bar", "backlink_coverage_min` minimum"),
    (S + "gen_arch_map.py", 165, "backlink_coverage_min` bar", "backlink_coverage_min` minimum"),
    (S + "gen_arch_map.py", 2169, "what bar the adopter meant", "what minimum the adopter meant"),
    (S + "gen_arch_map.py", 2222, "the bar\"", "the minimum\""),
    (S + "gen_arch_map.py", 2226, "earns the bar.", "earns the minimum."),
    (S + "gen_arch_map.py", 2604, "The bar is docs/process.toml", "The minimum is docs/process.toml"),
    (S + "trajectory_arch.py", 801, "derived bar down", "derived stage down"),
    (S + "check_test_first.py", 194, "That checks registries", "That excludes registries"),
    # --- tests
    (T + "test_traj_panels.py", 242, 'the surviving sense of "bar")', 'the surviving sense of "bar", now "checks")'),
    (T + "test_traj_panels.py", 245, "Slices → phase → the check bars", "Slices → phase → the checks"),
    (T + "test_traj_panels.py", 257, "states the two bars", "states the two sets of checks"),
    (T + "test_traj_panels.py", 258, '# "rung bar", not "gate bar": the dashboard', '# "gate checks", the glossary\'s term, not "rung bar" or "gate bar": the dashboard'),
    (T + "test_traj_panels.py", 263, '# "gate checks" is that deleted name as the bar-to-checks rename would', '# "rung bar" was the dashboard\'s word until the glossary named the full gate'),
    (T + "test_traj_panels.py", 265, '"rung bar" in text', '"gate checks" in text'),
    (T + "test_traj_panels.py", 266, '("gate bar", "gate checks")', '("gate bar", "rung bar")'),
    (T + "test_traj_panels.py", 523, "# the bar)", "# the checks)"),
    (T + "test_traj_panels.py", 641, '"ff trunk to the barred tree"', '"ff trunk to the barred tree" (now "checked")'),
    (T + "test_traj_panels.py", 648, "advance trunk to the barred tree", "advance trunk to the checked tree"),
    (T + "test_traj_panels.py", 650, "advance trunk to the barred tree", "advance trunk to the checked tree"),
    (T + "test_traj_panels.py", 651, "advance trunk to the barred tree…", "advance trunk to the checked tree…"),
    (T + "test_shipped_tier.py", 6, "carries a far lower bar.", "carries a far lower standard."),
    (T + "test_shipped_tier.py", 17, "the shipped bar.", "the shipped standard."),
    (T + "test_shipped_tier.py", 21, "because the bar is about what", "because the standard is about what"),
    (T + "test_shipped_tier.py", 54, "drift away from this bar.", "drift away from this standard."),
    (T + "test_shipped_tier.py", 89, "the shipped bar demanded", "the shipped standard demanded"),
    (T + "test_shipped_tier.py", 93, "invisible to the bar it is", "invisible to the standard it is"),
    (T + "test_shipped_tier.py", 135, "fail the shipped bar,", "fail the shipped standard,"),
    (T + "test_shipped_tier.py", 155, "carries the higher bar", "carries the higher standard"),
    (T + "test_shipped_tier.py", 167, "The real bar:", "The real standard:"),
    (T + "test_shipped_tier.py", 173, "shipped-tier bar of", "shipped-tier standard of"),
    (T + "test_shipped_tier.py", 179, "this bar would silently", "this standard would silently"),
    (T + "test_shipped_tier.py", 189, "or this bar has gone blind", "or this standard has gone blind"),
    (T + "test_shipped_tier.py", 231, "The bar is a bar, not a ban:", "The standard is a standard, not a ban:"),
    (T + "test_rule_sync.py", 352, "below the top bar", "below the top stage"),
    (T + "test_rule_sync.py", 375, "--require-verified bar's", "--require-verified check's"),
    (T + "test_rule_sync.py", 1068, "coverage BAR, a percentage", "coverage MINIMUM, a percentage"),
    (T + "test_rule_sync.py", 1102, "because the bar came down", "because the minimum came down"),
    (T + "test_rule_sync.py", 1116, "told the bar is off", "told the minimum is off"),
    (T + "test_rule_sync.py", 1133, "what bar the adopter meant", "what minimum the adopter meant"),
    (T + "test_rule_sync.py", 1162, "the backlink bar above", "the backlink minimum above"),
    (T + "test_check_harness.py", 773, '"the bar must REFUSE', '"the checks must REFUSE'),
    (T + "test_check_harness.py", 782, "the same bar goes green.", "the same checks go green."),
    (T + "test_gen_arch_map.py", 733, "must not invent a bar.", "must not invent a minimum."),
    (T + "test_acceptance_level.py", 222, "the states a bar-advance", "the states a stage advance"),
    (T + "test_acceptance_level.py", 225, "self-accept the final bar.", "self-accept the final stage."),
    (T + "test_acceptance_level.py", 701, "while the bar", "while the checks"),
    (T + "test_old_kit_resync.py", 93, "A test whose bar can be met", "A test whose standard can be met"),
    (T + "test_old_kit_resync.py", 256, "The bar is passed in the RETIRED vocabulary", "The stage is passed in the RETIRED vocabulary"),
    (T + "test_traj_render.py", 533, "so the bar is the strict one", "so the stage is the strict one"),
    (T + "test_traj_render.py", 535, "so the bar is", "so the stage is"),
    # --- tests the rules made wrong or left half-done
    (T + "test_check_smoke_budget.py", 481, 'ROUTES = ["commit", "review"]', 'ROUTES = ["by-hand", "record-checks"]'),
    (T + "test_check_smoke_budget.py", 491, 'if route == "review":', 'if route == "record-checks":'),
    (T + "test_check_smoke_budget.py", 503, 'parametrize("bar", ROUTES)', 'parametrize("route", ROUTES)'),
    (T + "test_check_smoke_budget.py", 522, 'parametrize("bar", ROUTES)', 'parametrize("route", ROUTES)'),
    (T + "test_integrate_record_checks.py", 4, "names the `review` checks and", "names `checks=commit` and"),
    (T + "test_passed_checks.py", 167, "The checks set is closed: a check run outside it", "The check-set field is closed: a set outside it"),
]
