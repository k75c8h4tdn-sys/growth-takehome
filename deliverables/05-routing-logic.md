# CRM Routing, Handoff & SLAs
### AegisAI Inbound Conversion Path, Part 2

What happens the moment a lead converts on the landing page: how it is scored, routed, alerted, and handed to sales, and the SLAs that keep it fast. The `segment` and `fit tier` used here are the exact ones produced in Part 1, so a lead flows through one continuous system from raw list to booked meeting.

---

## 1. Why speed is the whole game

The single biggest lever on inbound conversion is response time, and it decays in minutes:

- Contacting a lead within **5 minutes** makes it ~**21x** more likely to qualify than at 30 minutes, and ~100x more likely to connect (Lead Response Management / Oldroyd, the widely-cited "MIT" study).
- Responding within **1 hour** vs. 24 hours makes qualifying far more likely (Harvard Business Review, "The Short Life of Online Sales Leads," 2011, reports ~60x).
- ~**78%** of buyers pick the vendor that responds first, and most B2B teams still take many hours to reply (InsideSales/Xant and Drift benchmarks).

*(These are widely-cited studies spanning ~2007-2021. I treat them as directional, not gospel: the point is that minutes matter, so the SLA design optimizes for speed-to-first-touch.)*

So the design goal is simple: for a high-fit, high-intent lead, a human (or an instant-booking flow) engages inside **5 minutes** during business hours. Everything below exists to make that reliable.

---

## 2. Lead score = Fit x Intent

Routing is driven by two axes, not one.

**Fit** is inherited from the Part 1 scoring engine (persona, seniority, company size, industry, platform). On conversion we re-run enrichment and land the lead in the same tiers: **A / B / C / D / Disqualified**, plus the **Strategic (enterprise)** flag for 10,001+ orgs.

**Intent** is the behavioral signal the inbound moment gives us:

| Intent | Signals |
|---|---|
| **High** | Requested a demo or the 14-day threat report, pricing page, repeat visits in a short window |
| **Medium** | Downloaded the State of AI Phishing report or other gated content, webinar signup |
| **Low** | Newsletter only, single blog visit, no clear buying action |

A demo/threat-report form fill (the landing page's primary CTA) is **High intent by definition**, which is why an inbound conversion is treated more urgently than the same person hit cold in Part 1.

**Priority matrix (Fit x Intent):**

| | High intent | Medium intent | Low intent |
|---|---|---|---|
| **Fit A** | **P1 Hot** | P2 | P3 |
| **Fit B** | **P1 Hot** | P2 | P3 |
| **Fit C** | P2 | P3 | P3 |
| **Fit D** | P3 | P3 | Nurture |
| **Disqualified** | Review / suppress | Suppress | Suppress |

---

## 3. Routing decision table

Owner, SLA, and alerting by segment, fit, intent, and geo. This is the table the CRM (HubSpot/Salesforce + a router like LeanData or a workflow) executes on lead creation.

| Priority | Fit + Intent | Segment | Geo | Route to | First-touch SLA | Alert |
|---|---|---|---|---|---|---|
| **Strategic** | enterprise (10,001+), any high/med intent | Security or IT Leader | Any | Enterprise AE **+** Sales Engineer, named-account owner if the account already exists | **1 business hour** | `#sales-enterprise`, DM to AE + SE |
| **P1 Hot** | A/B + High | Security Leader | NA | Security-pod AE + SDR (round-robin) | **5 min** (biz hrs) | `#sales-hot`, DM + mobile push, instant-booking offered on confirmation |
| **P1 Hot** | A/B + High | IT / Tech | NA | IT-pod AE + SDR (round-robin) | **5 min** (biz hrs) | `#sales-hot`, DM + mobile push |
| **P1 Hot** | A/B + High | Any | EMEA / ANZ / APAC | Regional pod, else follow-the-sun SDR | **5 min in-region biz hrs**, else next business hour | `#sales-hot-intl` |
| **P2 Warm** | A/B + Medium, or C + High | Any | Any | SDR queue (segment-matched) | **15-60 min** | `#sales-sdr` |
| **P3 Nurture** | C/D + Low/Med, or D + High | Any | Any | Marketing automation, no rep | Automated, revisit when intent rises | none (scored, logged) |
| **Suppress / Review** | Disqualified | Student, competitor, job seeker, free-email domain, sub-100 employees | Any | No routing. Competitor to CI list; others to nurture or hard suppression | n/a | none |

**Geo notes.** Geo sets both the pod and the SLA clock. Since ~90% of the addressable base is North America (Part 1), NA is the primary staffed pod. International hot leads use follow-the-sun coverage or an after-hours auto-responder with a self-serve booking link so the clock effectively starts at next-business-hour without losing the lead.

---

## 4. The handoff flow (what fires on submit)

```mermaid
flowchart TD
    A[Lead converts on landing page] --> B[Create/update Lead in CRM]
    B --> C{Dedupe: known account or contact?}
    C -- Yes --> C1[Attach to existing account, route to current owner]
    C -- No --> D[Enrich: Apollo/Clearbit firmographics, verify email, detect MX/platform]
    C1 --> E
    D --> E[Score FIT reusing Part 1 engine + capture INTENT from form action]
    E --> F{Decision table: segment x fit x intent x geo}
    F -->|Strategic (enterprise)| G[Enterprise AE + SE, SLA 1 hr]
    F -->|P1 Hot| H[Segment/geo pod AE + SDR, SLA 5 min]
    F -->|P2 Warm| I[SDR queue, SLA 15-60 min]
    F -->|P3 Nurture| J[Marketing automation, no rep]
    F -->|Disqualified| K[Suppress / CI list / nurture]
    G --> L[Alert + start SLA clock]
    H --> L
    I --> L
    L --> M{First touch within SLA?}
    M -- Yes --> N[Log disposition -> feeds scoring]
    M -- No --> O[Escalate: manager ping, then round-robin reassign]
    O --> N
    J --> N
```

Step by step:

1. **Capture.** Form submit creates or updates a Lead. (The prototype landing page runs this decision client-side on submit to visualize it; production POSTs to the CRM/router.)
2. **Dedupe.** Match on email domain and company against existing accounts so an inbound lead on an owned account goes straight to that account's owner, not a round-robin.
3. **Enrich.** Fill firmographics, verify the email is deliverable, and detect the real email platform (MX = Microsoft vs Google), which confirms the Part 1 platform signal.
4. **Score.** Re-run the Part 1 fit score, attach the intent level from the conversion action.
5. **Route.** Apply the decision table: assign owner (round-robin within the segment + geo pod, respecting capacity and dedupe) or send to nurture.
6. **Alert + book.** Fire the alerts below and, for P1, surface an instant-booking calendar on the confirmation screen so the prospect can self-serve a meeting before a rep even calls.
7. **Enforce SLA.** Start the timer; escalate on breach.
8. **Close the loop.** Rep logs disposition (connected, qualified, disqualified, bad-fit); dispositions feed back to tune fit weights and suppression lists.

---

## 5. Automation, alerting & SLAs (speed and ownership)

| Priority | Automation | Alerting | First-touch SLA | Escalation if breached |
|---|---|---|---|---|
| **Strategic (enterprise)** | Auto-create opportunity, notify named AE + SE, draft exec-briefing invite | `#sales-enterprise` + DM to AE and SE | 1 business hour | Ping AE manager at 60 min; reassign at 2 hrs |
| **P1 Hot** | Auto-assign, instant-booking link on confirmation page, pre-drafted first email | `#sales-hot` + owner DM + mobile push | 5 min (business hours) | Manager ping at 10 min; auto round-robin reassign at 15 min |
| **P2 Warm** | Enroll in segment-matched SDR sequence, task created | `#sales-sdr` | 15-60 min | Reassign next business hour |
| **P3 Nurture** | Enroll in marketing nurture; raise to P2 automatically if intent rises | none (dashboard only) | n/a | n/a |
| **Off-hours (any)** | Auto-reply with booking link; SLA clock starts next business hour | queued to on-call channel | next business hour (5 min for P1 once open) | standard |

**Ownership model.** Marketing owns the lead until it is routed. The assigned **SDR/AE owns first touch and the SLA**; a sales manager owns escalations and reassignment. RevOps owns the routing rules, the SLA definitions, and the weekly report. Nothing sits unowned: an unactioned P1 auto-reassigns rather than going stale.

**What we measure (weekly):** median speed-to-lead, SLA attainment % by priority, MQL to SQL conversion by segment and fit tier, meetings booked, and disposition mix. These both prove the system works and feed the Part 1 weights (e.g. if Fit-A leads disqualify often on a dimension, re-weight it).

---

## 6. Guardrails

- **Dedupe first**, always, so inbound never pulls an owned account into round-robin.
- **Suppression** honors every opt-out from the Part 1 sequences and all unsubscribe requests, instantly.
- **Competitors and free-email/personal domains** are filtered out of sales routing (competitors flagged to competitive intel; personal domains sent to nurture pending a work email).
- **Data handling** matches AegisAI's own posture: minimal PII, SOC 2 Type II, and no lead data shared with external AI labs. Enrichment providers are contracted processors only.
