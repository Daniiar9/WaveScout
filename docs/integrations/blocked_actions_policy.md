# Blocked Actions Policy

WaveScout is a creator-led growth intelligence tool, not an outbound automation or posting system.

The following actions are blocked in this pass:

- TikTok scraping
- browser automation
- login, CAPTCHA, or rate-limit bypass
- TikTok DM automation
- message sending
- live content posting or publishing
- automatic outreach
- automatic Notion writes by default

## Content Posting

TikTok Content Posting remains intentionally unsupported:

```text
live_post=false
content_posting_supported=false
blocked_reason="WaveScout does not post content or automate publishing in this pass."
```

## Outreach

WaveScout may draft proposals and packets, but it must keep:

```text
send_allowed=false
approval_required=true
human_review_required=true
```

Any future send or publish capability requires a separate product, safety, and implementation review.
