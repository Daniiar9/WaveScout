# End-to-End Growth Workflow

## Run The Engine

```bash
python scripts/run_growth_engine.py --product-text "An AI workspace that connects your apps so you can ask questions across your stack and turn answers into workflows." --owned-tiktok "@demoapp" --out artifacts/growth_brief.md --json-out artifacts/growth_brief.json
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
- Live Notion writes by default.

