from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CreatorProposal:
    creator_id: str
    subject_or_opening: str = ""
    dm_draft: str = ""
    email_draft: str = ""
    collaboration_angle: str = ""
    why_this_creator: str = ""
    suggested_video_angle: str = ""
    compensation_note_placeholder: str = "Compensation or product access details to be reviewed by a human."
    approval_required: bool = True
    send_allowed: bool = False
    do_not_send_reason: str = ""

