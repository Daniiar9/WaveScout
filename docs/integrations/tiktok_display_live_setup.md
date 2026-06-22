# TikTok Display API Live Gate

The TikTok Display API path is for an authenticated owned account only.

It is not for scraping public TikTok pages, fetching arbitrary creator profiles, comments, or sending messages.

## Supported Intent

- read authorized account metadata
- list authorized account videos
- convert authorized video metadata into owned-account analysis inputs
- analyze owned-account themes, hooks, formats, and content gaps

## Required Scopes

- `user.info.basic`
- `video.list`

## Dry-Run Command

```bash
python scripts/tiktok_owned_account_check.py --dry-run
```

## Live-Gated Command

```bash
python scripts/tiktok_owned_account_check.py --allow-tiktok-live --out artifacts/owned_tiktok_profile.md
```

Live mode blocks unless all are true:

- `WAVESCOUT_ALLOW_TIKTOK_LIVE=true`
- explicit CLI flag is passed
- `TIKTOK_ACCESS_TOKEN` exists locally
- required scopes are configured
- capability checker passes

The current pass still returns a blocked status instead of making a live HTTP call.
