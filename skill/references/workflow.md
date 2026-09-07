# Workflow (open only after the user has chosen their input)

You reach this file after Step 0 (explain + ask own-CSV-or-example) and after the user has answered. You now have an input CSV: either the user's file, or `data/example-contacts.csv`. Run the steps below one at a time, explaining what and why at each step, and gating with a single question between steps.

The connected flow you are building:
**CSV -> enrich, score, rank -> persona landing pages -> email sequence whose CTA links each prospect to their persona's landing page -> send -> prospect clicks, sees a matched page, books -> CRM routing + SLAs.**

## Execution mode (portable)
Prefer running the engine for exact, reproducible scores:
`python3 scripts/score_contacts.py --in <THE_CHOSEN_CSV> --out <run>/01-scored-contacts.csv --top 20`
It auto-detects columns, so any header works. If the environment cannot run Python, score by reasoning from `references/scoring-rubric.md` (identical weights) and say which mode you used. Save every output to the user's working folder, never into the skill directory.

## Step 1 - Enrich, score, rank (Part 1)
Run the engine on the chosen CSV. Then:
- Explain the methodology and why: five weighted parts, Persona 35, Seniority 20, Size 20, Industry 15, Signal 10; persona leads because a perfect company is useless if the contact cannot buy; hard disqualifiers (retired, students, wrong-function, junior, solo consultants) override the score.
- Show the top ~15-20 ranked contacts as a table, and save the full scored file.
- Report the run's numbers: tier distribution, addressable (A+B), disqualified count and reasons, and the top segment.
- Spot-check out loud that no genuine buyer was suppressed (show two or three disqualified examples so the judgment is visible).
- Name the top segment(s); they set the personas for the next steps.
Then ask one question: "Want me to build the landing page(s) for the top persona(s), then the emails that link to them?" Wait.

## Step 2 - Persona landing page(s) (built before the emails, so the emails can link to them)
From `assets/landing-page-template.html`, build a page for each top persona in this run (usually Security Leader and/or IT Leader), defaulting each to its persona via `?segment=`. Explain: the page adapts its hero, pain points, and proof to the persona, and its form lets the prospect book a meeting (the demo / 14-day threat report). Save each page and note the per-persona URL you will use in the emails (e.g. `.../lp?segment=security`). If hosting is not wired up, say the URL is a placeholder to fill once the page is deployed (a named next step). Then ask one question: "Ready for the email sequence that links to these pages?" Wait.

## Step 3 - Email sequence that links to the landing pages
From `assets/email-sequence-template.md` and `references/aegisai-voice.md`, write the sequence for the top tier, branched by segment. The CTA in each email links to that persona's landing page (the `?segment=` URL from Step 2), set as `{{landing_url}}`. Explain the reasoning: who it targets (Tier A, minus strategic accounts that go to an AE), why the 14-day-threat-report offer, why 3-5 touches, and the click-through: prospect clicks, sees a page written for their persona, books a meeting. Save it. Then ask one question: "Want to see how this goes live (send) and what happens after they book?" Wait.

## Step 4 - Send + what happens after they book (the seams, named honestly as next steps)
Explain, briefly:
- Send: today the sequence is drafted to a file; in production the top tier flows into the sequencer (Outreach/Apollo/Salesloft) and this becomes one-click enroll/send, after address verification (NeverBounce/ZeroBounce).
- Landing pages: hosted at a real URL so the email links resolve.
- When they book: the form feeds CRM routing.
Then ask one question: "Want the CRM routing + SLAs for the meetings these generate?" Wait.

## Step 5 - CRM routing + SLAs, then wrap
From `assets/routing-template.md`, produce routing for this run: fit x intent scoring, a decision table filled with the segments and geo this list actually contained, the handoff flow, and the SLAs. Explain the reasoning, especially the 5-minute first-touch SLA (speed-to-lead: a lead worked within 5 minutes is far likelier to qualify). Save it.

Wrap up: summarize what you produced and where it saved, and state the loop in one sentence: their CSV became a scored list, whose top personas got landing pages, whose links went into a matched email sequence, that routes booked meetings to sales, one connected flow. Offer to re-run on another CSV, change a weight, or go deeper on any step.

## Definitions
- Top tier = Tier A (fit score >= 90); the email sequence targets it.
- Top segment / persona = the segment (Security Leader / IT Leader / Tech Exec) with the most Tier A contacts; it sets the landing page and the email track.
- Strategic = enterprise-sized (10,001+) or score >= 97, flagged independent of tier; pulled from automation to an AE for 1:1.
