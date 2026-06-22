# TikTok OAuth Setup

WaveScout includes a TikTok OAuth URL helper for manual setup.

It does not open a browser, exchange tokens, print tokens, or store tokens by default.

## Command

```bash
python scripts/tiktok_oauth_setup.py --scopes "user.info.basic,video.list" --dry-run
```

The command prints:

- authorization URL
- redirect URI
- requested scopes
- safety status
- next manual step

## Local Configuration

```text
TIKTOK_CLIENT_KEY=
TIKTOK_CLIENT_SECRET=
TIKTOK_REDIRECT_URI=
TIKTOK_ACCESS_TOKEN=
TIKTOK_REFRESH_TOKEN=
TIKTOK_OPEN_ID=
TIKTOK_SCOPES=
```

Use `TIKTOK_SCOPES` for currently approved scopes. `TIKTOK_APPROVED_SCOPES` remains supported for older local setups.

## Token Policy

Tokens must not be committed or printed. If local token storage is added later, it must use an ignored path such as:

```text
data/local_tokens/tiktok_token.json
```

The current pass keeps token exchange blocked pending a separate audited HTTP implementation.
