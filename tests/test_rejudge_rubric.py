"""The observation rubric-reference advisory (TC-307), without git or scaffolds."""

from conftest import load_script

trajectory = load_script("check_trajectory")


def test_missing_observation_rubric_warns():
    findings = trajectory.observation_rubric_findings(
        [
            {"TC-ID": "TC-001", "Automated": "No"},
            {"TC-ID": "TC-002", "Automated": "No", "Rubric": "docs/rubrics/example.md"},
            {"TC-ID": "TC-003", "Automated": "Yes"},
            {"TC-ID": "TC-000", "Automated": "No"},
        ]
    )
    assert len(findings) == 1
    assert "TC-001" in findings[0] and "rubric" in findings[0].lower()
