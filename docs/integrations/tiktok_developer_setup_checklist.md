# TikTok Developer Setup Checklist

1. Create a TikTok developer app.
2. Configure the redirect URI.
3. Request only the scopes required for the approved use case.
4. Add OAuth/login flow as a separate reviewed feature.
5. Store credentials only in local environment variables.
6. Run the capability checker.
7. Test dry-run adapters.
8. Only enable live mode after approval.

## Local Placeholder Variables

Use `.env.example` as a reference. Do not commit real secrets.

## Dry-Run Commands

```bash
python scripts/check_tiktok_capabilities.py
python scripts/build_tiktok_oauth_url.py --scopes "user.info.basic,video.list"
```

The OAuth helper does not open a browser, exchange tokens, or store tokens.

