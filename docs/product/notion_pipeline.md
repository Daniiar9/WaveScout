# Notion Pipeline

WaveScout builds Notion-ready payloads without writing to Notion by default.

## Payload Groups

- Trend Waves.
- Creator Candidates.
- Creator Intelligence Packets.
- Outreach Packets.
- Growth Brief.

## Dry-Run Status

The pipeline payload includes:

- `dry_run=true`
- `notion_write=false`
- `send_allowed=false`
- `approval_required=true`
- `human_review_required=true`

Live Notion writes require a separate confirmation path and are not part of the default growth engine.

