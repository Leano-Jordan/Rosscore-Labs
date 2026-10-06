# Ross Portfolio Telemetry

## What it measures

Ross polls every active repository for:

- repository availability and visibility;
- default branch;
- last push age;
- archived state;
- GitHub Actions availability;
- latest Actions result;
- recent Actions success rate;
- required Director/manifest contract presence;
- machine-detectable health flags.

The report is written to `telemetry/latest.json` and `telemetry/latest.md`.

## Schedule

The telemetry workflow runs:

- on control-plane changes;
- every 6 hours;
- manually through GitHub Actions.

## Private repository boundary

GitHub's default `GITHUB_TOKEN` is scoped to the repository running the workflow. It cannot automatically read Rosscore's private sibling repositories.

Current private portfolio repositories therefore appear as **ACCESS_BLOCKED** until a dedicated credential is configured:

`ROSCORE_TELEMETRY_TOKEN`

Use a least-privilege GitHub credential that can read the required private repositories. Do not place a personal access token in source files or workflow YAML.

The workflow already prefers `ROSCORE_TELEMETRY_TOKEN` and falls back to the local repository's `GITHUB_TOKEN`.

Until that secret exists, partial telemetry is considered a **known limitation**, not a false green.

## Control rule

Ross must never claim full portfolio telemetry when one or more repositories are access-blocked.

Evidence states:

- **OBSERVED** — current telemetry was collected;
- **ACCESS_BLOCKED** — collection was attempted but GitHub permissions prevented observation;
- **UNKNOWN** — no valid observation exists;
- **VERIFIED** — the relevant telemetry evidence passed its expected check.

## Design rationale

This is deliberately read-only with respect to portfolio repositories. The telemetry workflow writes only its own snapshot into Rosscore Labs.

It does not modify Zazu, Swift Order, GnuGuard or the website repositories.

