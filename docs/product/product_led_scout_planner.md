# Product-Led Scout Planner

Manual creator finding does not scale because it starts with platform wandering instead of a product thesis. WaveScout now starts from the product and produces a scout plan before humans spend time researching creators.

## Workflow

Product URL or product text -> Product Intelligence Brief -> Trend Wave Map -> Creator Search Strategy -> optional owned TikTok account analysis -> Scout Run Plan -> discovery adapter dry-run -> creator candidates -> Creator Intelligence Packets -> outreach/content recommendations.

## Product Intelligence Brief

The brief extracts the category, target users, buyers, use cases, pains, value props, trend keywords, and creator-relevant angles.

## Trend Wave Map

The trend map identifies primary waves, adjacent waves, rejected waves, hashtags, search keywords, creator archetypes, and why the trend matters now.

## Creator Search Strategy

The strategy turns the product and waves into:

- creator archetypes
- discovery queries
- hashtag targets
- comment patterns
- qualification criteria
- rejection criteria
- outreach angles

## Owned TikTok Account Analysis

Owned account analysis is dry-run/manual-import only. It can summarize imported content samples and comments to identify brand voice, hooks, content gaps, creator collab opportunities, and angles creators can remix.

## Discovery Adapters

V0 includes dry-run adapters:

- manual import
- search provider placeholder
- official TikTok Research API placeholder

No adapter scrapes TikTok or makes external calls by default.

## Safety Model

- no external calls by default
- no product fetch unless separately implemented and explicitly allowed
- no TikTok scraping
- no browser automation
- no TikTok DM/send
- no unsafe live API calls

## Example Command

```bash
python scripts/plan_creator_scout.py --product-text "An AI workspace that connects your apps so you can ask questions across your stack and turn answers into workflows." --owned-tiktok "@demoapp" --out artifacts/scout_plan.md
```

