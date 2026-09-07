# TEMPLATE: CRM Routing, Handoff & SLAs
### The operator instantiates this for Part 2 after the landing page.

**How to use:** the routing framework below is stable; per run, the operator fills in the segments and geos that actually appeared in Part 1 and points the table at them. Fill it in per run as `references/workflow.md` Step 5 describes. Always explain the reasoning (especially the SLA math), not just the table.

## Why speed is the design driver (state this)

Response time is the biggest lever on inbound conversion and it decays in minutes: a lead contacted within 5 minutes is 21x more likely to qualify than at 30 minutes (MIT / Lead Response Management); within 1 hour, 60x vs 24 hours (HBR); 78% of buyers purchase from the first responder. So the whole system exists to get a human (or an instant-booking flow) on a high-fit, high-intent lead inside 5 minutes during business hours.

## Lead score = Fit x Intent (reuse Part 1 fit)

- **Fit** = the Part 1 tier (A/B/C/D/DQ) + strategic flag. Do not recompute from scratch; the whole point is one continuous score.
- **Intent** = the inbound behavior. High = demo / threat-report request (the landing page's primary CTA). Medium = content download. Low = newsletter / single visit.

Priority = matrix of the two: Fit A/B + High intent = P1 Hot; enterprise = Strategic; partial = P2; weak = nurture; DQ = suppress.

## Decision table (fill segment/geo from the run)

| Priority | Fit + Intent | Segment | Geo | Route to | First-touch SLA |
|---|---|---|---|---|---|
| Strategic | enterprise | Security/IT Leader | any | Enterprise AE + SE | 1 business hour |
| P1 Hot | A/B + High | `<top segment>` | primary geo | Segment pod AE + SDR | 5 min (biz hrs) |
| P1 Hot | A/B + High | any | other geos | Follow-the-sun / regional | 5 min in-region, else next biz hr |
| P2 Warm | A/B + Med, or C + High | any | any | SDR queue | 15-60 min |
| P3 Nurture | C/D + Low | any | any | Marketing automation | automated |
| Suppress | Disqualified | student/competitor/free-email/sub-100 | any | No routing / CI list | n/a |

Reasoning to give: geo sets the pod and the SLA clock (primary geo is wherever the run's density is; for the AegisAI sample that was North America at ~90%). Enterprise gets a longer SLA because it is a bigger, multi-stakeholder deal, not because it is less important.

## Handoff flow (what fires on submit)

Capture -> dedupe against existing accounts -> enrich + verify -> score fit + capture intent -> decision table assigns owner + SLA -> alert (Slack + owner + mobile for P1) and offer instant booking -> SLA timer with escalation -> log disposition back to scoring. A Mermaid diagram of this is in the worked example.

## Automation, alerting, SLAs, ownership
P1: auto-assign, instant-booking link, Slack `#sales-hot` + DM + mobile push, 5-min SLA, escalate at 10 min, reassign at 15. Strategic: `#sales-enterprise`, 1-hr SLA. Ownership is explicit so nothing sits unactioned. The connectors that make this real (CRM, router, Slack, Chili Piper) are the production next steps.
