# Manual Creator Research

WaveScout V0 expects humans to research creators manually, then import structured creator, content, and comment samples. It does not scrape TikTok, automate browsing, or send messages.

## Research Standard

Use this baseline when validating whether WaveScout can take 20 real TikTok creators and surface the 5 worth contacting:

- 20 candidate creators.
- 3-5 recent relevant videos per creator.
- 10-30 comments sampled per creator.
- Focus on comments that ask questions, mention tools, share use cases, show pain, request tutorials, or express skepticism.

## How To Find Creators Manually

Search TikTok by trend and adjacent topics such as AI agents, AI workspace, SaaS automation, RevOps, Notion workflows, Slack workflows, CRM automation, founder tools, no-code automation, and AI tool reviews.

Look for creators whose recent content already overlaps with the wave. Do not add creators only because they are large or broadly mention AI.

## What To Capture

For each creator, capture:

- handle and profile URL
- display name and bio
- rough follower count, average views, and average likes
- categories and hashtags used
- contact field if publicly listed
- region/language when obvious
- notes about credibility, risk, or positioning

For each content sample, capture:

- video URL
- caption or title
- transcript summary or manual summary
- hashtags and topics
- format such as demo, tutorial, teardown, comparison, or hot take
- views, likes, comment count, posted date, and notes

For comments, capture the comment text and optional notes. Use only manual samples relevant to evaluating audience quality.

## High-Intent Comments

High-intent comments include:

- "Can this connect to Notion?"
- "Does it work with Slack?"
- "I need this for my CRM."
- "Can you make a tutorial?"
- "How would this work for a small agency?"
- "Is this real or just a demo?"

These comments show implementation curiosity, tool demand, workflow pain, use cases, tutorial demand, or useful skepticism.

## Low-Quality Hype

Low-quality comments include:

- "first"
- "AI is crazy"
- "bro what"
- "follow me"
- "chatgpt changed my life"

These can indicate awareness, but they should not drive creator qualification by themselves.

## Avoid Overvaluing Follower Count

Follower count is only a small signal. A smaller creator with clear demos and implementation-level comments can be more valuable than a large creator with shallow AI hype.

Prioritize:

- content-wave match
- audience buyer/user match
- comment intent
- creator clarity and trust
- natural product angle
- manageable risk

## Qualification Standard

A qualified creator is someone where:

- content matches the wave
- audience matches the buyer/user
- comments show real curiosity, pain, or intent
- creator can explain the product credibly
- risk is manageable
- product angle feels native to their content

## Using The CSV Templates

Copy the templates before editing them:

```bash
copy templates\creators_template.csv data\local_creators.csv
copy templates\content_samples_template.csv data\local_content_samples.csv
copy templates\comments_template.csv data\local_comments.csv
```

Fill your copied files with manually researched data. Keep categories, hashtags, and topics separated by commas or semicolons.

## Running WaveScout After Research

```bash
python scripts/import_creators_csv.py --input data/local_creators.csv --out data/imported_creators.json
python scripts/import_content_samples_csv.py --input data/local_content_samples.csv --out data/imported_content_samples.json
python scripts/import_comments_csv.py --input data/local_comments.csv --out data/imported_comments.json
python scripts/score_imported_creators.py --top 5 --out artifacts/imported_creator_rankings.md
python scripts/export_creator_packets.py --top 10 --out-dir artifacts/creator_packets
```

Review the top packets manually. Contact only after human approval.

