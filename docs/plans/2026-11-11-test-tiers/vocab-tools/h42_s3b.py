EDITS = [
    ("project-trajectory/scripts/kitlib/spine.py", '        "priority",\n        "verification",\n        "status",', '        "priority",\n        "verification_method",\n        "status",'),
    ("project-trajectory/scripts/spine_carrier.py", '"verification": "VerificationMethod",', '"verification_method": "VerificationMethod",'),
    ("tests/test_spine_rules.py", 'str(r.get("verification") or "").strip() not in LLR_EXEMPT_METHODS', 'str(r.get("verification_method") or "").strip() not in LLR_EXEMPT_METHODS'),
]
