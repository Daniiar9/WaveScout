# WaveScout

WaveScout is an offline creator-led growth intelligence system for AI and startup products.

It is designed to turn a trend wave into a qualified creator shortlist, then into a creator intelligence packet, content angle, proposal draft, and Notion-ready dry-run outreach payload.

## Core Thesis

More creators is not the goal. Qualified creators are the goal.

A qualified creator is not just someone who talks about AI. A qualified creator has trend fit, buyer or user audience fit, comment-level intent, a credible content style, manageable risk, and a product angle that feels native to their work.

## What WaveScout Does

- Tracks offline/demo TrendWave records.
- Imports creator, content, and comment samples manually.
- Scores creator-market-product fit with deterministic heuristics.
- Turns comments into audience and buyer-intent intelligence.
- Infers likely audience segments.
- Generates ranked content angles.
- Drafts creator-specific proposals for human review.
- Builds CreatorIntelligencePacket and OutreachPacket artifacts.
- Produces Notion dry-run payloads.
- Exposes safe MCP-style tools.

## What WaveScout Does Not Do

- No TikTok scraping.
- No browser automation for TikTok.
- No login, rate-limit, or CAPTCHA bypass.
- No TikTok DM automation.
- No mass messaging.
- No automatic proposal sending.
- No live TikTok API calls in V0.
- No secret printing.
- No `.env` changes.

## Safety Model

V0 defaults are offline and demo-first:

- `WAVESCOUT_OFFLINE_MODE=true`
- `WAVESCOUT_DEMO_MODE=true`
- `WAVESCOUT_ALLOW_EXTERNAL_CALLS=false`
- `NOTION_SYNC_CONFIRM=false`
- `TIKTOK_OFFICIAL_API_ENABLED=false`

All outreach is draft-only:

- `send_allowed=false`
- `approval_required=true`

## Run The Demo

```bash
python scripts/demo_tiktok_growth_workflow.py
```

The demo prints a concise PASS summary and exports:

```text
artifacts/demo_creator_intelligence_packet.md
```

## Example Output

```text
WaveScout Demo: PASS
External calls: false
Notion write: false
TikTok DM/send: false

Top creators:
1. @agentbuilderdaily - 94 high
2. @aistackreview - 90 high
3. @vibecodesam - 81 high

Rejected:
@genericchatgpttips - 13 reject
@randomfitnesscreator - 0 reject
```

## Run Tests

```bash
python scripts/run_all_tests.py
```

The runner executes the demo workflow, all smoke tests, and compile checks.

You can also run individual checks:

```bash
python scripts/test_creator_scoring.py
python scripts/test_comment_intelligence.py
python scripts/test_audience_analysis.py
python scripts/test_notion_sync_dryrun.py
python scripts/test_mcp_tools_import.py
python -m compileall app scripts
```

## MCP Tools Overview

WaveScout exposes local safe tools for:

- listing and creating trend waves
- manually importing creators, content, and comments
- scoring creators for a wave
- analyzing comments
- inferring audience profiles
- generating content angles
- generating proposal drafts
- building creator intelligence packets
- building outreach packets
- dry-running Notion sync
- running a wave scout ranking

The MCP server uses FastMCP if it is installed. Without FastMCP, the tool functions still import and run directly.

## Real Creator Import Workflow

Use the CSV templates in [templates](templates) and follow [docs/workflows/real_creator_import_workflow.md](docs/workflows/real_creator_import_workflow.md) to manually research 20 creators, import the data, score them, and export one packet per qualified creator.

Key commands:

```bash
python scripts/import_creators_csv.py --input data/local_creators.csv --out data/imported_creators.json
python scripts/import_content_samples_csv.py --input data/local_content_samples.csv --out data/imported_content_samples.json
python scripts/import_comments_csv.py --input data/local_comments.csv --out data/imported_comments.json
python scripts/score_imported_creators.py --top 5 --out artifacts/imported_creator_rankings.md
python scripts/export_creator_packets.py --top 10 --out-dir artifacts/creator_packets
```

## TikTok Connector Readiness

WaveScout includes official TikTok API readiness checks without enabling live calls by default. The readiness layer maps Display API, Research API, and Content Posting API capabilities, checks required scopes/config flags, and exposes dry-run adapters for future approved integration work.

It does not add scraping, browser automation, TikTok DM automation, message sending, token exchange, or live API calls.

Run:

```bash
python scripts/check_tiktok_capabilities.py
```

This writes `artifacts/tiktok_capability_report.md` and reports:

- external calls: false
- TikTok scraping: false
- TikTok DM/send: false
- live post allowed: false

Future OAuth/scopes work should start with:

```bash
python scripts/build_tiktok_oauth_url.py --scopes "user.info.basic,video.list"
```

The OAuth helper prints setup guidance only. It does not open a browser, exchange tokens, or store tokens.

## Product-Led Scout Planner

WaveScout can now start from product text or a product URL placeholder and generate a creator hunting strategy before manual research begins.

```bash
python scripts/plan_creator_scout.py --product-text "An AI workspace that connects your apps so you can ask questions across your stack and turn answers into workflows." --owned-tiktok "@demoapp" --out artifacts/scout_plan.md
python scripts/run_discovery_dryrun.py --limit 25 --out artifacts/discovery_dryrun.md
```

The planner exports a Product Intelligence Brief, Trend Wave Map, Creator Search Strategy, optional owned TikTok analysis, dry-run discovery payloads, and next safe actions. It does not scrape TikTok, fetch TikTok live, automate browsing, send DMs, or send messages.

See [docs/product/product_led_scout_planner.md](docs/product/product_led_scout_planner.md) and [docs/workflows/product_led_scout_workflow.md](docs/workflows/product_led_scout_workflow.md).

## Project Layout

```text
app/
  adapters/   offline and placeholder adapters
  mcp/        MCP tool registry and optional server
  models/     dataclass model layer
  services/   scoring, analysis, packet, and sync logic
data/         checked-in demo data
docs/         product and demo documentation
scripts/      CLI workflows and smoke tests
artifacts/    generated local demo exports, ignored by git
```

## Future Roadmap

See [docs/product/roadmap.md](docs/product/roadmap.md).

The direction is a creator-led GTM operating system: trend -> creator -> content -> outreach -> performance -> learning, still human-approved and never spam automation.
