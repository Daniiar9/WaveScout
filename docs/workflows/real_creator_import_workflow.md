# Real Creator Import Workflow

This workflow is for manually researched creator data. It is offline by default and does not scrape TikTok, call TikTok APIs, automate browsing, send DMs, or send proposals.

## 1. Copy CSV Templates

```bash
copy templates\creators_template.csv data\local_creators.csv
copy templates\content_samples_template.csv data\local_content_samples.csv
copy templates\comments_template.csv data\local_comments.csv
```

## 2. Fill 20 Creators

Add 20 manually researched candidate creators to `data/local_creators.csv`.

Capture handle, profile URL, bio, rough follower count, average views, categories, hashtags, region, language, and public contact if available.

## 3. Add 3-5 Content Samples Per Creator

Fill `data/local_content_samples.csv` with recent relevant videos. Include a short manual summary of what the video shows. Prefer videos that overlap with the trend wave.

## 4. Add 10-30 Comments Per Creator

Fill `data/local_comments.csv` with manually sampled comments. Prioritize comments that ask questions, mention tools, share use cases, show pain, request tutorials, or express skepticism.

## 5. Run Import Scripts

```bash
python scripts/import_creators_csv.py --input data/local_creators.csv --out data/imported_creators.json
python scripts/import_content_samples_csv.py --input data/local_content_samples.csv --out data/imported_content_samples.json
python scripts/import_comments_csv.py --input data/local_comments.csv --out data/imported_comments.json
```

## 6. Score Imported Creators

```bash
python scripts/score_imported_creators.py --creators data/imported_creators.json --content data/imported_content_samples.json --comments data/imported_comments.json --wave "Talk to your apps" --product "An AI workspace that connects your apps so you can ask questions across your stack and turn answers into workflows" --top 5 --out artifacts/imported_creator_rankings.md
```

## 7. Export Creator Packets

```bash
python scripts/export_creator_packets.py --creators data/imported_creators.json --content data/imported_content_samples.json --comments data/imported_comments.json --wave "Talk to your apps" --product "An AI workspace that connects your apps so you can ask questions across your stack and turn answers into workflows" --out-dir artifacts/creator_packets --top 10
```

## 8. Review Top 5 Packets

Open the ranking artifact and top creator packets. Check the fit score, comment intelligence, audience profile, best angle, proposal draft, risks, missing data, and outreach decision.

## 9. Manually Contact Only After Human Approval

WaveScout creates drafts only. Do not send automatically. Confirm:

- `send_allowed=false`
- `approval_required=true`
- `external_calls=false`
- `tiktok_dm=false`

## 10. Optionally Sync To Notion Later

Notion sync is dry-run by default. Live writes should only be added after a separate review and explicit confirmation configuration.

