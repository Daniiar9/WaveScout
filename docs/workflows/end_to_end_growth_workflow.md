# End-to-End Growth Workflow

## Run The Engine

```bash
python scripts/run_growth_engine.py --product-text "An AI workspace that connects your apps so you can ask questions across your stack and turn answers into workflows." --owned-tiktok "@demoapp" --out artifacts/growth_brief.md --json-out artifacts/growth_brief.json
```

## Run With A Provider Gate

```bash
python scripts/run_growth_engine.py --product-text "An AI workspace that connects your apps so you can ask questions across your stack and turn answers into workflows." --discovery-provider exa --out artifacts/growth_brief.md --json-out artifacts/growth_brief.json
```

This produces safe provider payloads and blocked live-mode status unless explicit live gates are configured.

## Check TikTok Gates

```bash
python scripts/tiktok_oauth_setup.py --scopes "user.info.basic,video.list" --dry-run
python scripts/tiktok_owned_account_check.py --dry-run
python scripts/tiktok_research_discovery_check.py --dry-run
```

## Add Imported Creator Data

```bash
python scripts/run_growth_engine.py --product-text "..." --imported-creators data/imported_creators.json --imported-content data/imported_content_samples.json --imported-comments data/imported_comments.json
```

## Enrich Discovery Candidates

```bash
python scripts/enrich_candidates_from_import.py --candidates artifacts/discovery_candidates.json --creators data/imported_creators.json --content data/imported_content_samples.json --comments data/imported_comments.json --product-text "..."
```

## Review

Open the Growth Brief, inspect the candidate shortlist, and only manually contact creators after human approval.

## Intentionally Not Automated

- TikTok scraping.
- Browser automation.
- TikTok DMs.
- Message sending.
- Live posting.
- Content Posting API publishing.
- Live Notion writes by default.
