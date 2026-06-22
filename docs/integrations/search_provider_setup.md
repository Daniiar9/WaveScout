# Search Provider Setup

Search providers are optional discovery adapters for public creator, profile, or video URLs.

They do not replace manual review. They only help source candidate URLs for enrichment.

## Environment Placeholders

```text
WAVESCOUT_ALLOW_EXTERNAL_CALLS=false
EXA_API_KEY=
SERP_API_KEY=
```

Do not commit real keys. Keep credentials in local environment variables only.

## Dry-Run Command

```bash
python scripts/run_growth_engine.py --product-text "..." --discovery-provider exa --out artifacts/growth_brief.md --json-out artifacts/growth_brief.json
```

## Live-Gated Command

```bash
python scripts/run_growth_engine.py --product-text "..." --discovery-provider exa --allow-external-discovery --out artifacts/growth_brief.md --json-out artifacts/growth_brief.json
```

Live mode still blocks unless `WAVESCOUT_ALLOW_EXTERNAL_CALLS=true`, the provider key is configured, and the provider schema has been reviewed.

## Safety Notes

- No TikTok scraping.
- No browser automation.
- No login or CAPTCHA bypass.
- No DMs or message sending.
- No posting.
- Human review remains required before outreach.
