# TikTok API Capability Matrix

| Capability | Official API | Required scopes | Default status | Can use for WaveScout? | Notes |
|---|---|---|---|---|---|
| display_user_info | Display API | user.info.basic | dry_run_only | Future authorized metadata only | Authorized account/profile metadata. |
| display_list_videos | Display API | video.list | dry_run_only | Future authorized creator/account review | Authorized user recent/public videos. |
| display_query_videos | Display API | video.list | dry_run_only | Future selected-video review | Authorized user selected videos. |
| research_query_videos | Research API | research.data.basic | blocked | Future approved trend/creator discovery | Only where approved by official Research API access. |
| research_query_comments | Research API | research.data.basic | blocked | Future approved comment intelligence | Endpoint is a placeholder until official details are reviewed. |
| content_direct_post | Content Posting API | video.publish | blocked | No for creator scouting | Authorized posting only; requires user auth, audit, and human approval. |
| tiktok_dm_send | None | None | blocked | No | WaveScout does not automate TikTok DMs. |

## Scope Notes

Display API:

- `user.info.basic`
- `video.list`
- profile/video metadata for authorized user

Research API:

- `research.data.basic`
- public video/comment research where approved
- useful for future trend/creator discovery

Content Posting API:

- `video.publish`
- authorized posting only
- audit/private-viewing constraints may apply
- not part of creator scouting

DM automation:

- blocked
- not supported

