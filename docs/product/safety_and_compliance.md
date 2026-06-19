# Safety And Compliance

WaveScout V0 is offline, demo-first, and manual-import only.

## Prohibited In V0

- no TikTok scraping
- no login bypass
- no rate-limit bypass
- no CAPTCHA bypass
- no browser automation for TikTok
- no TikTok DM automation
- no mass-message workflows
- no automatic proposal sending
- no secret printing
- no `.env` changes

## Default Configuration

- `WAVESCOUT_OFFLINE_MODE=true`
- `WAVESCOUT_DEMO_MODE=true`
- `WAVESCOUT_ALLOW_EXTERNAL_CALLS=false`
- `NOTION_SYNC_CONFIRM=false`
- `TIKTOK_OFFICIAL_API_ENABLED=false`

## Outreach Rules

Every proposal is draft-only:

- `send_allowed=false`
- `approval_required=true`

Humans must review the packet, proposal, evidence, risks, and missing data before doing any manual outreach.

## Manual Import By Default

V0 supports demo data, manual creator imports, manual content imports, manual comment imports, and string-only TikTok URL parsing. URL parsing does not fetch pages.

## Official API Placeholder

The official TikTok adapter is a placeholder only. Future API work should use approved official APIs, explicit configuration, and a fresh safety review.

