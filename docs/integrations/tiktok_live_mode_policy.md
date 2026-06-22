# TikTok Live Mode Policy

WaveScout is offline and dry-run first.

## Never Allowed

- TikTok scraping.
- Browser automation for TikTok.
- Login, rate-limit, or CAPTCHA bypass.
- Auto-DM.
- Mass messaging.
- Automatic outreach sending.

## Live Call Requirements

Live calls require:

- `TIKTOK_OFFICIAL_API_ENABLED=true`
- specific API family flag enabled
- `WAVESCOUT_ALLOW_EXTERNAL_CALLS=true`
- required credentials
- required scopes
- explicit live confirmation flag
- separate implementation review
- human approval for public-facing actions

## Posting Policy

Content posting requires approved scope, user authorization, explicit confirmation, and human review. It is not part of creator scouting.

## Current Pass

This readiness pack implements dry-run wrappers and capability gates only. It does not implement live HTTP calls.

