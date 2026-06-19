# Creator Intelligence Packet

The CreatorIntelligencePacket is the central WaveScout artifact. It turns a trend wave and a creator candidate into a reviewable decision packet.

## Definition

A packet answers:

- Why this creator?
- Why this trend?
- What do they post about?
- Who seems to be in their audience?
- What are people asking in the comments?
- Is there buyer or user intent?
- What angle fits this creator?
- What should we avoid saying?
- Should we contact them?
- What proposal should we send?
- What is the next safe action?

## Fields

- TrendWave
- CreatorCandidate
- content summary
- AudienceProfile
- comment intelligence summary
- CreatorFitScore
- recommended ContentAngle
- CreatorProposal
- risks
- missing data
- evidence
- next safe action
- approval required
- send allowed

## Scoring Logic

The deterministic score uses:

- topical relevance: 20
- audience relevance: 25
- comment intent quality: 20
- creator trust and clarity: 15
- product demo fit: 10
- commercial priority: 10
- risk penalty: up to -20

Follower count is deliberately limited. A micro-creator can score high when the topic, audience, comments, and content format all match.

## Comment Intelligence

Comments are evaluated for intent, not vanity engagement. Implementation-level questions matter more than hype. Tool mentions, tutorial requests, use cases, objections, and pain points improve the quality signal.

## Audience Fit

Audience fit estimates likely segments such as founders, builders, RevOps/operators, agency owners, developers, SMB owners, AI tourists, students, and irrelevant/general audiences.

## Qualified Creator Standard

A qualified creator has:

- native topic fit
- credible content format
- relevant audience
- high-intent comments
- manageable risk
- a product angle that does not feel forced

## Example Outcome

High fit creators receive a draft-only proposal and a recommended content angle. Low fit or reject creators receive a do-not-send reason and a next action such as import more evidence or archive.

