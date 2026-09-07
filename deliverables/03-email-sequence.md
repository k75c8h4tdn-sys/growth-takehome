# Outbound Email Sequence
### Top tier (Tier A), branched by segment, in AegisAI's voice

> **Production note (future integration):** today this is drafted to a file. In-seat, the top tier would flow into the sequencer (Outreach/Apollo/Salesloft) and this becomes a one-click "Enroll / Send" button, with addresses verified first. See `07-next-steps-and-integrations.md`.

**Who gets this:** the top tier. Of the 570 Tier A contacts, 147 are Strategic (enterprise or near-perfect fit) and are pulled out to an AE for 1:1 treatment, leaving **423 in the automated top-tier sequence: 253 Security Leaders and 170 IT Leaders.** Tier B (581, which also gets 66 strategic pulled to AE) receives the compressed 3-touch version (Touches 1, 3, 5). Tier C is marketing nurture. Tier D and Disqualified get nothing. (Tech Execs top out at Tier B, max score 89.5, so they enter via the Tier B cut, not the top tier.)

**The offer that anchors every touch:** the **14-day threat report**, AegisAI's real low-friction entry point. Connect by API, read-only, no MX changes, and their analysts report what got through the prospect's current filter. It is proof, not a pitch, which is why it converts skeptical security buyers.

**Where every CTA points (Part 1 to Part 2, connected):** each email's CTA links to the prospect's **persona landing page** (`{{landing_url}}`, the `?segment=` deep link into `04-landing-page.html`). One click takes them from the inbox to a page written for their persona, where they enter their details and book the meeting. Same `segment` label, all the way through.

**Voice:** confident, specific, defender-to-defender. Short sentences. No buzzword salad, no "hope this finds you well." Every claim is one AegisAI actually makes: ~22% more attacks caught, up to 90% fewer false positives, 5-minute API deploy, no MX changes, agents that reason like an analyst, founded by the team behind Google Safe Browsing and reCAPTCHA.

---

## Personalization variables

| Token | Source | Fallback if missing |
|---|---|---|
| `{{first_name}}` | list | "there" (but suppress send if name missing for Tier A) |
| `{{company}}` | list | required, no send without it |
| `{{title}}` | list | "your team" |
| `{{industry}}` | list / enrichment | "your sector" |
| `{{segment}}` | scored list (Security Leader / IT Leader / Tech Exec) | routes to IT Leader copy |
| `{{platform}}` | enrichment (M365 or Google Workspace) | "your Microsoft 365 or Google Workspace tenant" |
| `{{peer_logo}}` | approved reference customers only (Mesh, Lokker, LangChain, Stelliant, Spacetil, all public on aegisai.ai) or a recognizable name in `{{industry}}` | drop the sentence rather than guess |
| `{{trigger}}` *(optional)* | recent funding, sector breach, hiring for security roles | omit the line |
| `{{landing_url}}` | the persona landing page, deep-linked (e.g. `.../lp?segment=security`) | required; it is the CTA in every email |
| `{{sender_name}}`, `{{calendly_link}}`, `{{report_link}}` | rep config | required |

**Rule:** never send a Tier A email with an unresolved `{{first_name}}`, `{{company}}`, or an `unverified_guess` email address. Verify deliverability first (see scoring_logic.md).

## Cadence (Tier A, ~15 business days, multi-channel)

| Day | Channel | Touch |
|---|---|---|
| 1 | Email | 1 - Problem + threat-report offer |
| 2 | LinkedIn | connection request (no pitch) |
| 3 | Email | 2 - How it works + proof (reply on thread) |
| 6 | Email | 3 - Angle shift (segment-specific pain) |
| 7 | LinkedIn | comment / light touch |
| 9 | Email | 4 - Value content, soft CTA |
| 14 | Email | 5 - Breakup |

Branching by score: **Tier A (non-strategic)** = all 5 emails. **Tier B (non-strategic)** = Touches 1, 3, 5 only. **Strategic (233 accounts total across tiers: 99 enterprise + 134 near-perfect fit)** = pulled out of automation and given to an AE for a 1:1 version (guidance at the end).

---

## TRACK A - Security Leader (253 automated Tier A contacts)
*Angle: detection efficacy, BEC/zero-day coverage, false positives, SOC workload.*

### Touch 1 - Email (Day 1)
**Subject:** what {{company}}'s filter is letting through
**Preview:** a 14-day, read-only look. no MX changes.

Hi {{first_name}},

AI made spear-phishing and BEC cheap to run at scale, and the rule-based filters most teams still run weren't built for attacks with no payload and no known-bad domain.

AegisAI puts an autonomous agent on every inbox that reasons like an analyst instead of matching a rule. Teams like {{peer_logo}} see it catch ~22% more attacks with up to 90% fewer false positives.

See what {{company}}'s filter is missing and book a 14-day threat report (read-only API, no MX changes): {{landing_url}}

Open to it?
{{sender_name}}

### Touch 2 - Email (Day 3, reply on thread)
**Subject:** re: what {{company}}'s filter is letting through

{{first_name}}, quick note on the how:

No rules to write, no tuning, no rip-and-replace. AegisAI deploys through the {{platform}} API in minutes and can run in monitoring mode first, so you see verdicts before it ever touches mail flow. Every decision ships with the agent's reasoning, so it's not a black box for your SOC.

The founding team built Google Safe Browsing and reCAPTCHA, and just raised a $36M Series A from Battery Ventures to go after AI-driven email attacks.

15 minutes this week to see it against {{company}}'s real traffic?

### Touch 3 - Email (Day 6)
**Subject:** fewer false positives, fewer 2am escalations

{{first_name}}, the reason security teams actually switch isn't just catch rate:

Legacy filters bury analysts in false positives. AegisAI cuts those up to 90%, auto-triages the noise, and hands your team real incidents with IOCs already attached. Less alert fatigue, more time on work that matters.

If BEC and payload-less or QR-based phishing are on your {{industry}} risk register this year, the 14-day report is the fastest way to quantify the gap. Want me to set it up?

### Touch 4 - Email (Day 9, value-add)
**Subject:** what AI phishing actually looks like now

{{first_name}}, not a pitch, just useful:

We built our State of AI Phishing report from real attacks AegisAI blocked across Microsoft 365 and Google Workspace tenants. The adversary-in-the-middle and vendor-impersonation examples are worth a scan for any {{industry}} security team.

{{report_link}}

Whenever the timing's right, the 14-day analysis on {{company}} is a five-minute setup.

### Touch 5 - Email (Day 14, breakup)
**Subject:** should I close this out?

{{first_name}}, I won't keep cluttering your inbox.

If email security isn't a priority this quarter, no problem, I'll stop here. If it is, the 14-day threat report is read-only, takes five minutes to start, and you'll know exactly what your current filter is missing.

Want the connection steps, or should I check back next quarter?
{{sender_name}}

---

## TRACK B - IT Leader (170 automated Tier A contacts; Tech Execs enter via Tier B)
*Angle: deployment speed, no MX changes, low operational overhead, consolidation. Same cadence and offer; swap the subject lines and the value emphasis. Tech Execs (max score 89.5) are not in Tier A, so they receive this track's copy through the compressed Tier B sequence.*

**Touch 1 - Subject:** {{company}} email security without the MX change
> Opening swap: "Most email security upgrades mean a gateway migration and a change window. AegisAI deploys through the {{platform}} API in about five minutes, no MX changes, no downtime, and can start in monitoring mode."
> Keep the 14-day threat-report CTA.

**Touch 2 - Subject:** re: without the MX change
> Emphasize: no rules to maintain, no tuning, one less console for your team to babysit; agents adapt on their own. Same Battery Ventures / ex-Google credibility line.

**Touch 3 - Subject:** less email security to manage, not more
> Angle: operational overhead and cost. "up to 90% fewer false positives means fewer tickets and less time your team spends triaging what the filter got wrong." Consolidation over legacy SEG.

**Touch 4 - Subject:** what AI phishing looks like now
> Same State of AI Phishing content touch (segment-neutral).

**Touch 5 - Subject:** should I close this out?
> Same breakup, framed around deployment being a five-minute lift whenever they're ready.

---

## Strategic variant (233 accounts, AE-owned, not automated)
The 233 strategic accounts (99 enterprise at 10,001+, plus 134 near-perfect-fit mid-market at score >= 97) are pulled out of the sequencer. The AE sends a genuinely 1:1 first touch that references a specific, verifiable detail (a recent breach in their sub-sector, a `{{trigger}}` event, or their public compliance posture), offers an **executive threat briefing** alongside the 14-day report, and, for 10,001+ orgs, frames a phased rollout by business unit. Fall back to Track A/B copy only if the AE has no specific hook.

---

## Guardrails baked into the copy
- **Every claim is real** and matches AegisAI's public messaging. No invented stats.
- **One CTA per email**, and it is low-friction (a read-only report), not "book a 30-min demo" on touch 1.
- **Deliverability:** plain text, no images or tracking-heavy HTML on cold touches, one link max and only from Touch 4. Warmed domain, verified addresses only.
- **Compliance:** CAN-SPAM / GDPR footer with a real unsubscribe; honor opt-outs instantly (feeds the suppression list in routing-logic.md).
- **Personalization degrades gracefully:** if a token can't be resolved, the line is dropped, never sent with a broken `{{token}}`.
