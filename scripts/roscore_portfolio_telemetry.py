#!/usr/bin/env python3
"""Build current GitHub portfolio telemetry for Ross using only Python stdlib."""
from __future__ import annotations

import io
import json
import os
import sys
import urllib.request
import zipfile
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

def api_bytes(url: str):
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required")
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "roscore-portfolio-telemetry",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read()

def age_days(iso: str | None):
    if not iso:
        return None
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return round((datetime.now(timezone.utc) - dt).total_seconds() / 86400, 2)

def latest_director_health(repo: str, workflow_runs: list[dict]):
    health_runs = [r for r in workflow_runs if r.get("name") == "Rosscore Director Health"]
    if not health_runs:
        return None
    run = health_runs[0]
    if run.get("status") != "completed" or run.get("conclusion") != "success":
        return {
            "status": run.get("status"),
            "conclusion": run.get("conclusion"),
            "run_id": run.get("id"),
            "head_sha": run.get("head_sha"),
        }
    artifacts = api(f"/repos/{repo}/actions/runs/{run['id']}/artifacts?per_page=20").get("artifacts", [])
    artifact = next(
        (a for a in artifacts
         if a.get("name", "").startswith("roscore-director-health-") and not a.get("expired")),
        None,
    )
    if not artifact:
        return {"status": "missing_artifact", "run_id": run.get("id"), "head_sha": run.get("head_sha")}
    raw = api_bytes(artifact["archive_download_url"])
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        member = next((n for n in zf.namelist() if n.endswith("roscore-director-health.json")), None)
        if not member:
            return {"status": "invalid_artifact", "run_id": run.get("id")}
        report = json.loads(zf.read(member).decode("utf-8"))
    return {
        "status": "ready",
        "run_id": run.get("id"),
        "run_url": run.get("html_url"),
        "report_commit": report.get("commit"),
        "readiness": report.get("readiness"),
        "risk_flags": report.get("risk_flags", []),
        "generated_at_utc": report.get("generated_at_utc"),
        "changed_files": report.get("changed_files", [])[:50],
    }

def collect(project):
    repo = project["repository"]
    metadata = api(f"/repos/{repo}")
    runs = api(f"/repos/{repo}/actions/runs?per_page=20")
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
        "director_health": latest_director_health(repo, workflow_runs),
        "health_flags": [],
    }

def main():
    control = json.loads(CONTROL.read_text(encoding="utf-8"))
    telemetry = {
        "schema_version": "1.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "company": control["company"],
        "company_director": control["company_director"],
        "source": "GitHub API current repository state + post-commit director health artifacts",
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
            dh = item.get("director_health")
            if not dh:
                flags.append("NO_DIRECTOR_HEALTH_REPORT")
            elif dh.get("status") != "ready":
                flags.append("DIRECTOR_HEALTH_NOT_READY")
            elif dh.get("report_commit") and dh.get("report_commit") != item.get("latest_ci", {}).get("head_sha"):
                flags.append("DIRECTOR_REPORT_COMMIT_MISMATCH")
            for rf in (dh or {}).get("risk_flags", []):
                flags.append(f"DIRECTOR_{rf}")
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
        "| Project | Director | Push age | CI | Director report | Flags |",
        "|---|---|---:|---|---|---|",
    ]
    for p in telemetry["projects"]:
        age = "—" if p.get("days_since_push") is None else f"{p['days_since_push']:.1f}d"
        ci = "—" if not p.get("latest_ci") else str(p["latest_ci"].get("conclusion") or p["latest_ci"].get("status"))
        flags = ", ".join(p.get("health_flags", [])) or "OK"
        dh = p.get("director_health") or {}
        report = dh.get("readiness") or dh.get("status") or "—"
        lines.append(f"| {p['name']} | {p.get('alias') or '—'} | {age} | {ci} | {report} | {flags} |")
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
