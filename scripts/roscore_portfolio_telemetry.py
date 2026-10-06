#!/usr/bin/env python3
"""Build current GitHub portfolio telemetry for Ross using only Python stdlib."""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "roscore-control.json"
OUT = ROOT / "telemetry"

def api(path: str):
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required")
    req = urllib.request.Request(
        "https://api.github.com" + path,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "roscore-portfolio-telemetry",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)

def age_days(iso: str | None):
    if not iso:
        return None
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return round((datetime.now(timezone.utc) - dt).total_seconds() / 86400, 2)

def collect(project):
    repo = project["repository"]
    metadata = api(f"/repos/{repo}")
    runs = api(f"/repos/{repo}/actions/runs?per_page=10")
    tree = api(f"/repos/{repo}/git/trees/{metadata['default_branch']}?recursive=1")
    workflow_runs = runs.get("workflow_runs", [])
    latest = workflow_runs[0] if workflow_runs else None
    success = sum(1 for r in workflow_runs if r.get("conclusion") == "success")
    completed = sum(1 for r in workflow_runs if r.get("status") == "completed")
    paths = {item.get("path") for item in tree.get("tree", [])}
    expected = {"manifest": project.get("manifest"), "agent_contract": project.get("agent_contract")}
    missing_contracts = [k for k, p in expected.items() if p and p not in paths]
    return {
        "name": project["name"],
        "alias": project.get("alias"),
        "repository": repo,
        "visibility": metadata.get("visibility"),
        "archived": metadata.get("archived"),
        "default_branch": metadata.get("default_branch"),
        "pushed_at": metadata.get("pushed_at"),
        "days_since_push": age_days(metadata.get("pushed_at")),
        "open_issues": metadata.get("open_issues_count"),
        "stars": metadata.get("stargazers_count"),
        "forks": metadata.get("forks_count"),
        "has_issues": metadata.get("has_issues"),
        "has_actions": metadata.get("has_actions"),
        "latest_ci": None if not latest else {
            "name": latest.get("name"),
            "status": latest.get("status"),
            "conclusion": latest.get("conclusion"),
            "created_at": latest.get("created_at"),
            "updated_at": latest.get("updated_at"),
            "html_url": latest.get("html_url"),
        },
        "ci_last_10": {
            "completed": completed,
            "successful": success,
            "success_rate": round(success / completed, 3) if completed else None,
        },
        "control_contracts_missing": missing_contracts,
        "control_contracts_present": not missing_contracts,
        "health_flags": [],
    }

def main():
    control = json.loads(CONTROL.read_text(encoding="utf-8"))
    telemetry = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "company": control["company"],
        "company_director": control["company_director"],
        "source": "GitHub API current repository state",
        "projects": [],
    }
    errors = []
    blocked = []
    for project in control["projects"]:
        if project.get("authority") == "inactive-empty":
            telemetry["projects"].append({
                "name": project["name"],
                "alias": project.get("alias"),
                "repository": project["repository"],
                "lifecycle": project.get("lifecycle"),
                "status": "inactive-empty",
                "health_flags": ["INACTIVE_PROJECT"],
            })
            continue
        try:
            item = collect(project)
            flags = item["health_flags"]
            if item["archived"]:
                flags.append("ARCHIVED")
            if item["days_since_push"] is not None and item["days_since_push"] > 30:
                flags.append("STALE_30D")
            if item["latest_ci"] and item["latest_ci"]["conclusion"] not in (None, "success", "skipped", "neutral"):
                flags.append("LATEST_CI_NOT_GREEN")
            if item["latest_ci"] is None:
                flags.append("NO_CI_RUN_OBSERVED")
            if item["control_contracts_missing"]:
                flags.append("CONTROL_CONTRACT_MISSING")
            telemetry["projects"].append(item)
        except Exception as exc:
            message = str(exc)
            access_blocked = "HTTP Error 404" in message or "HTTP Error 403" in message
            if access_blocked:
                blocked.append(project["name"])
            telemetry["projects"].append({
                "name": project["name"],
                "alias": project.get("alias"),
                "repository": project["repository"],
                "health_flags": ["ACCESS_BLOCKED"] if access_blocked else ["TELEMETRY_ERROR"],
                "error": message,
            })
            if not access_blocked:
                errors.append(f"{project['name']}: {exc}")

    OUT.mkdir(exist_ok=True)
    (OUT / "latest.json").write_text(json.dumps(telemetry, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Ross Portfolio Telemetry",
        "",
        f"Generated: {telemetry['generated_at']}",
        "",
        "| Project | Director | Push age | CI | Flags |",
        "|---|---|---:|---|---|",
    ]
    for p in telemetry["projects"]:
        age = "—" if p.get("days_since_push") is None else f"{p['days_since_push']:.1f}d"
        ci = "—" if not p.get("latest_ci") else str(p["latest_ci"].get("conclusion") or p["latest_ci"].get("status"))
        flags = ", ".join(p.get("health_flags", [])) or "OK"
        lines.append(f"| {p['name']} | {p.get('alias') or '—'} | {age} | {ci} | {flags} |")
    (OUT / "latest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    if errors:
        print("Telemetry completed with errors:")
        print("\n".join(errors))
        return 1
    print("Ross portfolio telemetry: PASS")
    print(f"Projects observed: {len(telemetry['projects'])}")
    print(f"Access-blocked projects: {len(blocked)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
