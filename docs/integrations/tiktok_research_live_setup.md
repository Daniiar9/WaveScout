# TikTok Research API Live Gate

The TikTok Research API path is capability-gated and approval-dependent.

WaveScout does not assume access. It produces dry-run query payloads and blocked responses until approval, scopes, and live flags are confirmed.

## Required Scope

- `research.data.basic`

## Dry-Run Command

```bash
python scripts/tiktok_research_discovery_check.py --dry-run
```

## Live-Gated Command

```bash
python scripts/tiktok_research_discovery_check.py --allow-tiktok-live --query "AI workflow automation" --out artifacts/tiktok_research_discovery.md
```

## Blocked Response Includes

- blocked status
- blocked reason
- required approval/scopes
- dry-run request payloads
- safe next actions

## Exclusions

- no TikTok scraping
- no browser automation
- no login bypass
- no comments query unless capability exists
- no DMs
- no posting
