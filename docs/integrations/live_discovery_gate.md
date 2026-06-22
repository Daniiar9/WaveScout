# Live Discovery Gate

WaveScout can prepare provider discovery requests while keeping live external calls off by default.

The gate exists so future provider integrations can be reviewed without changing the core safety model.

## Default Safety

- `dry_run=true`
- `external_calls=false`
- `tiktok_live_calls=false`
- `tiktok_scraping=false`
- `browser_automation=false`
- `tiktok_dm_send=false`
- `live_post=false`
- `send_allowed=false`
- `approval_required=true`
- `human_review_required=true`

## Live External Discovery Requirements

Live search-style discovery requires all of the following:

- `WAVESCOUT_ALLOW_EXTERNAL_CALLS=true`
- an explicit CLI or MCP allow flag
- provider credential present, such as `EXA_API_KEY` or `SERP_API_KEY`
- provider capability and schema reviewed

If any requirement is missing, WaveScout returns a blocked response and a dry-run payload preview.

## Providers

- `dry_run_search`: local payload generation only.
- `exa`: optional live-gated search provider; no live call by default.
- `serp`: optional live-gated search provider; no live call by default.
- `manual`: human imported candidates.
- `tiktok_research`: official TikTok Research API gate, blocked unless approved and configured.

The current pass does not scrape TikTok pages, does not use browser automation, and does not bypass rate limits.

## Example

```bash
python scripts/run_growth_engine.py --product-text "..." --discovery-provider exa --out artifacts/growth_brief.md --json-out artifacts/growth_brief.json
```

This generates Exa-style dry-run payloads and records the provider as blocked for live external use.
