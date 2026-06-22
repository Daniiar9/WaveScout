# TikTok Connector Readiness

This pack prepares WaveScout for future official TikTok API work without adding live TikTok automation.

## What This Adds

- Official API capability map.
- OAuth/app setup checklist.
- Config placeholders.
- Dry-run official API adapters.
- Capability checker CLI.
- MCP tools for capability inspection and dry-run previews.
- Tests proving no external calls are made by default.

## What This Does Not Add

- No scraping.
- No browser automation.
- No TikTok DM automation.
- No message sending.
- No live API calls by default.
- No token exchange.
- No `.env` changes.

## Official API Categories

- Display API: authorized user profile and video metadata.
- Research API: approved public video/comment research use cases.
- Content Posting API: authorized posting only, not creator scouting.
- DM automation: blocked and not supported by WaveScout.

## Config Flags

- `TIKTOK_OFFICIAL_API_ENABLED=false`
- `TIKTOK_DISPLAY_API_ENABLED=false`
- `TIKTOK_RESEARCH_API_ENABLED=false`
- `TIKTOK_CONTENT_POSTING_API_ENABLED=false`
- `WAVESCOUT_ALLOW_EXTERNAL_CALLS=false`
- `TIKTOK_LIVE_DISPLAY_CONFIRM=false`
- `TIKTOK_LIVE_RESEARCH_CONFIRM=false`
- `TIKTOK_LIVE_POST_CONFIRM=false`

Credentials and tokens are placeholders only and should live in local environment variables.

## Safety Gates

No external TikTok request can be considered until all are true:

- official API enabled
- external calls allowed
- required credentials exist
- required scopes are present
- explicit live confirmation is set
- a separate live implementation has been reviewed

This readiness pass still returns dry-run responses and does not implement live HTTP.

## Run Capability Check

```bash
python scripts/check_tiktok_capabilities.py
```

This writes:

```text
artifacts/tiktok_capability_report.md
```

## Fit With WaveScout

WaveScout remains a quality-first creator intelligence system. Future official API work can support authorized metadata or approved research workflows, but outreach stays human-approved and draft-only.

