# TikTok Growth Workflow Demo

The demo runs fully offline using local JSON data.

## Run The Demo

```bash
python scripts/demo_tiktok_growth_workflow.py
```

Expected output:

- PASS safety summary
- top 3 demo creators
- rejected creators
- generated artifact path

## Scout A Wave

```bash
python scripts/scout_wave.py --wave "Talk to your apps" --product "An AI workspace that connects your apps so you can ask questions across your stack and turn answers into workflows" --top 3
```

## Build One Packet

```bash
python scripts/build_creator_packet.py --creator-handle @agentbuilderdaily --wave "Talk to your apps" --format markdown
```

## Reading The Creator Score

Scores combine trend fit, audience fit, comment intent, creator clarity, product demo fit, commercial priority, and risk penalties. Reach is only a small signal.

## Inspecting Markdown Artifacts

The demo always writes the main review artifact:

```text
artifacts/demo_creator_intelligence_packet.md
```

Set `WAVESCOUT_EXPORT_ARTIFACTS=true` before running the demo to also write per-creator packet markdown and outreach JSON under `artifacts/creator_packets/`.

## Notion Dry-Run

Notion sync returns a payload without writing anything by default. Missing database IDs are reported as part of the dry-run result and do not fail the workflow.

## Run All Checks

```bash
python scripts/run_all_tests.py
```
