# Product-Led Scout Workflow

Use this workflow when you want WaveScout to start from a product thesis before researching creators.

## Use Product Text

```bash
python scripts/plan_creator_scout.py --product-text "An AI workspace that connects your apps so you can ask questions across your stack and turn answers into workflows." --out artifacts/scout_plan.md
```

This creates both:

- `artifacts/scout_plan.md`
- `artifacts/scout_plan.json`

## Use Product URL In Dry-Run

```bash
python scripts/plan_creator_scout.py --product-url "https://example.com" --out artifacts/scout_plan.md
```

URL-only mode does not fetch by default. Add product text for full offline analysis.

## Add Owned TikTok Handle

```bash
python scripts/plan_creator_scout.py --product-text "..." --owned-tiktok "@exampleapp" --out artifacts/scout_plan.md
```

This includes an owned profile section without live TikTok calls.

## Add Owned Content And Comments Manually

Use CSV or JSON files exported from manual research:

```bash
python scripts/plan_creator_scout.py --product-text "..." --owned-tiktok "@exampleapp" --owned-content data/owned_content.csv --owned-comments data/owned_comments.csv --out artifacts/scout_plan.md
```

## Run Discovery Dry-Run

```bash
python scripts/run_discovery_dryrun.py --plan artifacts/scout_plan.json --limit 25 --out artifacts/discovery_dryrun.md
```

This shows what would be searched if compliant providers are connected later. It makes no external calls.

## Move From Scout Plan To Real Creator Import

1. Review the scout plan and discovery dry-run.
2. Research candidate creators manually or with future approved providers.
3. Fill the creator/content/comment CSV templates.
4. Run the real creator import workflow.
5. Build Creator Intelligence Packets for qualified candidates.
6. Human-review any proposal before manual outreach.

