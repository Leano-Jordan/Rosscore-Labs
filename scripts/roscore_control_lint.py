#!/usr/bin/env python3
"""Deterministic guard for the Rosscore Labs company control plane."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "roscore-control.json"
AGENTS = ROOT / "AGENTS.md"
REGISTRY = ROOT / "docs" / "ROSCOR_LABS_PROJECT_REGISTRY.md"
DOCTRINE = ROOT / "docs" / "ROSCOR_LABS_AGENT_OPERATING_DOCTRINE.md"
TELEMETRY = ROOT / "scripts" / "roscore_portfolio_telemetry.py"
TELEMETRY_WORKFLOW = ROOT / ".github" / "workflows" / "roscore-portfolio-telemetry.yml"

REQUIRED_PROJECTS = {
    "Zazu EMP": ("Jarvis", "Leano-Jordan/ZazuEMP", "commercial-readiness", "initial product"),
    "Swift Order": ("Swifty", "Leano-Jordan/store-ordering-system", "release-hardening", "initial product"),
    "GnuGuard": ("Gnu", "Leano-Jordan/GnuGuard", "product-candidate", "software asset / product candidate"),
    "Leano ITC Website": ("ITC", "Leano-Jordan/leano-itc-website", "commercial-asset", "service website asset"),
    "Maggie's Hair & Beauty": ("Mags", "Leano-Jordan/maggies-hair-beauty", "commercial-asset", "reusable salon website asset"),
    "Catering Website Template": ("Cater", "Leano-Jordan/catering-website-template", "commercial-asset", "reusable catering template asset"),
}
ERRORS: list[str] = []

def fail(message: str) -> None:
    ERRORS.append(message)

def require_file(path: Path) -> None:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")

def main() -> int:
    for path in (CONTROL, AGENTS, REGISTRY, DOCTRINE, TELEMETRY, TELEMETRY_WORKFLOW):
        require_file(path)
    if ERRORS:
        return report()
    try:
        control = json.loads(CONTROL.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"roscore-control.json is invalid JSON: {exc}")
        return report()

    agents = AGENTS.read_text(encoding="utf-8")
    registry = REGISTRY.read_text(encoding="utf-8")
    doctrine = DOCTRINE.read_text(encoding="utf-8")

    if control.get("company_director") != "Ross":
        fail("company_director must be Ross")
    if "Company Director: **Jarvis**" in agents or "Company Director: **Jarvis**" in registry:
        fail("stale Jarvis company-director identity detected")
    if "Company Director: **Ross**" not in agents:
        fail("AGENTS.md does not declare Ross as company Director")
    if "Name: **Ross**" not in registry:
        fail("project registry does not declare Ross as company Director")

    projects = control.get("projects")
    if not isinstance(projects, list):
        fail("projects must be a list")
        return report()
    seen_repos: set[str] = set()
    seen_aliases: set[str] = set()
    for name, (alias, repository, lifecycle, strategic_role) in REQUIRED_PROJECTS.items():
        matches = [p for p in projects if p.get("name") == name]
        if len(matches) != 1:
            fail(f"control manifest must contain exactly one project entry for {name}")
            continue
        project = matches[0]
        if project.get("alias") != alias:
            fail(f"{name}: expected alias {alias!r}, found {project.get('alias')!r}")
        if project.get("repository") != repository:
            fail(f"{name}: expected repository {repository}, found {project.get('repository')}")
        expected_meta = {"lifecycle": lifecycle, "strategic_role": strategic_role, "write_boundary": "repository only"}
        for field, expected in expected_meta.items():
            if project.get(field) != expected:
                fail(f"{name}: expected {field}={expected!r}, found {project.get(field)!r}")
        if repository in seen_repos:
            fail(f"duplicate repository mapping: {repository}")
        seen_repos.add(repository)
        if alias in seen_aliases:
            fail(f"duplicate project alias: {alias}")
        seen_aliases.add(alias)
    friday = [p for p in projects if p.get("name") == "FRIDAY AI 6.7 Pro Refined"]
    if len(friday) != 1 or friday[0].get("alias") is not None or friday[0].get("authority") != "inactive-empty":
        fail("FRIDAY must remain explicitly inactive-empty with no Director")

    for project, marker in [
        ("Zazu EMP", "route to **Jarvis**"),
        ("Swift Order", "route to **Swifty**"),
        ("GnuGuard", "route to **Gnu**"),
        ("Leano ITC Website", "route to **ITC**"),
        ("Maggie's Hair & Beauty", "route to **Mags**"),
        ("Catering Website Template", "route to **Cater**"),
    ]:
        if marker not in agents:
            fail(f"company routing missing for {project}: {marker}")
    if "OBSERVED" not in doctrine or "UNKNOWN" not in doctrine or "BLOCKED" not in doctrine:
        fail("doctrine must preserve explicit evidence-state language")
    for marker in [
        "silently import another project's",
        "Never let a multi-project request become an implicit multi-repository write",
        "Never claim evidence that was not actually observed",
    ]:
        if marker not in doctrine:
            fail(f"doctrine lost critical control rule: {marker!r}")
    return report()

def report() -> int:
    if ERRORS:
        print("ROSCORE CONTROL LINT: FAIL")
        for error in ERRORS:
            print(f"- {error}")
        return 1
    print("ROSCORE CONTROL LINT: PASS")
    print("Company Director: Ross")
    print("Projects checked: 6 active + 1 inactive")
    print("Identity firewall: PASS")
    print("Routing uniqueness: PASS")
    print("Evidence doctrine: PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
