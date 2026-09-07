# TEMPLATE: Outbound Email Sequence
### The operator fills this in for the top tier discovered in Part 1.

**How to use:** after Part 1, the top segment is whichever of Security Leader / IT Leader has the most Tier A contacts. Generate the sequence for that segment using AegisAI's voice (`references/aegisai-voice.md`).

**Explain the reasoning when you output this.** State: who it targets, why this offer, why this many touches, and why the branching. Do not just paste emails.

---

## Design reasoning (say this out loud when you present it)

- **Who:** Tier A only (full sequence). Tier B gets a compressed 3-touch cut (touches 1, 3, 5). Tier C is marketing nurture. D and Disqualified get nothing. Reasoning: concentrate rep effort where fit is highest.
- **The offer, every touch:** the **14-day threat report** (read-only API, analysts report what got through). Reasoning: for skeptical security buyers, proof beats a pitch, and it is low-commitment.
- **Why 3-5 touches:** enough to earn a reply across channels without becoming spam; each touch changes the angle rather than repeating.
- **Why branch by segment:** Security buys on catch-rate and risk; IT/Tech buys on deployment speed and low overhead. Same product, different trigger.
- **Emails link to the landing page:** every CTA points to `{{landing_url}}`, the page matched to this contact's persona, where they book a meeting. That link is what joins Part 1 to Part 2: one click from inbox, to a page written for their persona, to a booked meeting.

## Personalization variables (and the rule)

`{{first_name}}`, `{{company}}`, `{{title}}`, `{{industry}}`, `{{segment}}`, `{{platform}}` (M365 or Workspace), `{{peer_logo}}` (approved customer or a recognizable name in `{{industry}}`), `{{trigger}}` (optional event), `{{sender_name}}`, `{{report_link}}`, `{{landing_url}}` (the landing page matched to this contact's persona, e.g. `.../lp?segment=security`).

**Rule:** never send with an unresolved `{{first_name}}`, `{{company}}`, or an `unverified_guess` email. Verify deliverability first. If a token cannot resolve, drop the line, never send a raw `{{token}}`.

## Cadence (Tier A, ~15 business days)

Day 1 Email T1 · Day 2 LinkedIn connect · Day 3 Email T2 (reply on thread) · Day 6 Email T3 · Day 9 Email T4 · Day 14 Email T5. Each email = one idea, one CTA, ~60-120 words, plain text.

---

## Touch skeletons (fill per segment; example copy is Security Leader)

**T1 - Problem + offer.** Subject: `what {{company}}'s filter is letting through`
> AI made spear-phishing and BEC cheap to run at scale, and rule-based filters were not built for attacks with no payload and no known-bad domain. AegisAI puts an agent on every inbox that reasons like an analyst. Teams like {{peer_logo}} catch ~22% more attacks with up to 90% fewer false positives. See what your filter is missing and book a 14-day threat report (read-only API, no MX changes): {{landing_url}}

**T2 - How it works + proof** (reply on thread). Subject: `re: ...`
> No rules, no tuning, no rip-and-replace. Deploys via the {{platform}} API in minutes, can run in monitoring mode first, and every verdict ships with the agent's reasoning. Built by the team behind Google Safe Browsing and reCAPTCHA; $36M Series A from Battery Ventures.

**T3 - Angle shift (segment pain).** Security: false positives / SOC workload. IT: operational overhead / no MX change.
> (Security) Legacy filters bury analysts in false positives. AegisAI cuts those up to 90%, auto-triages, and hands over real incidents with IOCs attached.

**T4 - Value, soft CTA.** Subject: `what AI phishing looks like now`
> Share the State of AI Phishing report (real blocked attacks). One link. No hard ask.

**T5 - Breakup.** Subject: `should I close this out?`
> Give them an easy out; restate the report is read-only and five minutes. Ask: send the steps, or circle back next quarter?

## Branching by segment (swap the emphasis, keep the offer)

- **Security Leader:** T1/T3 lead with detection, BEC/zero-day, false positives, SOC load.
- **IT Leader / Tech Exec:** T1 subject `{{company}} email security without the MX change`; lead with 5-minute API deploy, no MX changes, less to manage, consolidation.
- **Strategic (enterprise or score >=97):** pull from automation, AE writes a 1:1 first touch referencing a specific `{{trigger}}`, offers an executive threat briefing.

## Guardrails
Every claim real (from the voice pack). One CTA per email, and it is the persona landing page (`{{landing_url}}`), so the click always lands on a page matched to them. Keep to one link per email; plain text otherwise. CAN-SPAM / GDPR footer with real unsubscribe that feeds the suppression list.
