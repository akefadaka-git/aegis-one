#!/usr/bin/env python3
"""Structural validation for the AEGIS ONE architecture baseline."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "docs/architecture/A2-BASELINE.md": [
        "# AEGIS ONE",
        "## 1. Purpose and scope",
        "## 3. Deployment profiles",
        "## 5. Android capability boundaries",
        "## 7. Owner Decision Register constraints",
        "## 9. Stage gates and non-authorizations",
        "## 11. Acceptance evidence required",
        "ODR-017",
        "ODR-023",
        "ODR-032",
        "ODR-045",
        "ODR-012",
        "ODR-016",
        "ODR-036",
        "ODR-038",
    ],
    "docs/governance/OWNER-DECISION-REGISTER.md": [
        "AEGIS-A2-ODR-001",
        "version 1.1",
        "version 1.3",
        "ODR-017",
        "ODR-023",
        "ODR-032",
        "ODR-045",
        "ODR-012",
        "ODR-016",
        "ODR-036",
        "ODR-038",
    ],
}


def main() -> int:
    errors: list[str] = []
    for relative, required_terms in REQUIRED.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"Missing required document: {relative}")
            continue
        content = path.read_text(encoding="utf-8")
        if not content.endswith("\n"):
            errors.append(f"{relative}: missing final newline")
        for term in required_terms:
            if term not in content:
                errors.append(f"{relative}: required marker missing: {term}")
    if errors:
        print("DOCUMENTATION VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("DOCUMENTATION VALIDATION: PASS")
    print(f"Validated {len(REQUIRED)} documents and all required governance markers.")
    print("This checks document structure only; it is not security or implementation verification.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
