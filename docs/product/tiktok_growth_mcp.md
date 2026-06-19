# TikTok Creator-Led Growth MCP

WaveScout is a creator-led growth intelligence system for AI and startup products. It is not TikTok scraping, DM automation, or a mass outreach system.

## Thesis

More creators is not the goal. Qualified creators are the goal.

A qualified creator is someone whose content matches the trend wave, whose audience resembles the buyer or user, whose comments show curiosity or intent, whose style can explain the product credibly, whose risk is manageable, and whose product angle feels native to their content.

## Why More Signals Are Not Enough

Follower count, category labels, and generic AI keywords can produce noisy creator lists. WaveScout prioritizes evidence that a creator can credibly carry a specific product angle:

- trend-wave relevance
- audience and buyer fit
- comment intent quality
- creator clarity and trust
- product demo fit
- risk and forced-angle penalties

## V5 Vision

V0 is offline and demoable. V5 can add official platform APIs, richer performance feedback, more robust Notion workflows, and agentic review loops while preserving safety defaults.

## Trend Wave Loop

1. Define or import a TrendWave.
2. Add example keywords, hashtags, adjacent topics, and creator handles.
3. Rank creators against the wave.
4. Revisit wave confidence as performance evidence appears.

## Creator Intelligence Loop

1. Import creators manually.
2. Import content and comment samples manually.
3. Analyze content style, audience, and comments.
4. Score creator-market-product fit.
5. Build a CreatorIntelligencePacket.

## Outreach Packet Loop

1. Generate a content angle.
2. Draft a creator-specific proposal.
3. Build a Notion-ready OutreachPacket.
4. Require human review before any manual outreach.

## Safety Model

WaveScout defaults to offline mode. It does not scrape TikTok, bypass login, bypass rate limits, solve CAPTCHAs, automate DMs, mass-message creators, send proposals, or use browser automation for TikTok.

Outreach is always draft-only in V0:

- `send_allowed=false`
- `approval_required=true`

## MCP Tools

The MCP surface exposes safe local tools for listing waves, importing manual data, analyzing comments, inferring audience, scoring creators, generating content angles, drafting proposals, building packets, dry-running Notion sync, and running WaveScout rankings.

## Notion Sync

Notion sync is dry-run by default. If database IDs are missing, the system returns the payload and a clear message instead of failing. Live writes are intentionally not implemented in V0.

## Intentionally Not Automated

- TikTok scraping
- TikTok API calls
- browser automation for TikTok
- TikTok DMs
- proposal sending
- mass outreach
- secret storage or printing

