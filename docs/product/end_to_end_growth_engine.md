# End-to-End Growth Engine

The WaveScout Growth Engine connects the V0/V5-shaped loop in one safe dry-run workflow:

Product -> Trend -> Safe Provider Discovery -> Candidate Shortlist -> Enrichment Needed -> Comment/Audience Intelligence -> Fit Score -> Content Angle -> Proposal Draft -> Notion Pipeline -> Feedback Later.

## Full Workflow

1. Product text or product URL placeholder.
2. Product Intelligence Brief.
3. Trend Wave Map.
4. Creator Search Strategy.
5. Live-gated Discovery Provider Layer.
6. Discovery candidate normalization, dedupe, and initial ranking.
7. Creator scoring when imported content/comments exist.
8. Creator Intelligence Packets.
9. Outreach/content recommendations.
10. Notion dry-run pipeline.
11. Feedback loop placeholder.
12. Final Growth Brief.

## Dry-Run By Default

The engine does not scrape TikTok, automate a browser, send DMs, send messages, live-post content, or write to Notion by default.

Search providers such as `exa` and `serp` are optional and live-gated. TikTok Display API is scoped to authenticated owned-account analysis only. TikTok Research API is blocked unless capability approval, scopes, and explicit live flags exist. TikTok Content Posting remains blocked.

All outreach artifacts include:

- `send_allowed=false`
- `approval_required=true`
- `human_review_required=true`

## Missing Data Handling

If no candidates are available, the engine still returns discovery queries and next safe actions. If imported creators lack content/comments, the brief marks them as needing enrichment.

## Command

```bash
python scripts/run_growth_engine.py --product-text "An AI workspace that connects your apps so you can ask questions across your stack and turn answers into workflows." --owned-tiktok "@demoapp" --out artifacts/growth_brief.md --json-out artifacts/growth_brief.json
```

Provider dry-run:

```bash
python scripts/run_growth_engine.py --product-text "An AI workspace that connects your apps so you can ask questions across your stack and turn answers into workflows." --discovery-provider exa --out artifacts/growth_brief.md --json-out artifacts/growth_brief.json
```

The Growth Brief includes Live Discovery Status, Provider Capability Status, Owned TikTok Live Status, TikTok Research Status, Blocked Actions, and Safety Status.
