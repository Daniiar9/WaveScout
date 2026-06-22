# Discovery Provider Layer

The provider layer standardizes how WaveScout plans future discovery without doing unsafe work.

## Providers

- `manual_import`: reads human-provided imported creator JSON.
- `dry_run_search`: generates search payloads only.
- `exa_placeholder`: future external provider placeholder.
- `serp_placeholder`: future external provider placeholder.
- `tiktok_research_placeholder`: future official TikTok Research API placeholder.
- `owned_account_placeholder`: uses owned handle/imported content only.

## Provider Safety Contract

Every provider returns:

- `external_calls=false` by default
- `live_mode=false` by default
- `dry_run=true` by default
- provider status
- safety status

No provider makes live external calls in this pass.

## Candidate Flow

Provider result -> normalized candidate -> dedupe -> initial ranking -> enrichment with imported content/comments -> Creator Intelligence Packet.

