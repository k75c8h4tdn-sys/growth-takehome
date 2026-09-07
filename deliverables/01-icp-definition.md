# ICP Definition & Defense
### AegisAI Outbound Targeting Engine, Part 1

**One-line ICP:** A security or IT leader (Director and above) at a 201-10,000 employee organization in a regulated or high-phishing-risk sector, running Microsoft 365 or Google Workspace, in North America.

This document defines that profile, then defends and refines it against the actual 2,000-contact list. All figures come from `02-scored-contacts.csv` (reproducible via `../skill/scripts/score_contacts.py`).

---

## 1. Starting hypothesis vs. the data

The brief's hypothesis: *"security and IT leaders at 100 to 10,000 employee orgs on M365 or Workspace."*

Verdict: **directionally right, refined in five ways.** The persona and size guesses hold up. The data also reveals two dimensions the hypothesis was silent on (geography and industry) and one trap it would have walked into (30% of the list are non-buyers).

| # | Refinement | Evidence from the list |
|---|---|---|
| 1 | **Split "security and IT leaders" into two segments; they buy differently.** | 563 Security Leaders and 607 IT Leaders (58.5% combined). Security owns email security explicitly; IT owns it *by default* in the mid-market orgs that have no CISO. |
| 2 | **Keep 201-10,000 as the core; treat 10,001+ as a separate AE-led motion; floor out the smallest companies (below 50).** | 72.9% (1,457) are in the 201-10,000 band. 15% (299) are 10,001+ (above the stated ceiling). 6.1% (122) are below 50 employees (the 1-10 and 11-50 bands). |
| 3 | **M365/Workspace is a real criterion but must be enriched, not assumed.** | The raw file has no tech-stack field. Where headlines mention it, only M365, Azure, and Workspace appear (144 / 144 / 154). None contradict the platform assumption, but ~85% are unknown until enriched. |
| 4 | **Add geography: run North America first.** (Hypothesis was silent on geo.) | ~91% North America (1,736 US + 94 Canada + US metro labels). International is a thin, mostly English-speaking tail (UK & Ireland, ANZ, plus scattered APAC/EMEA/LATAM). |
| 5 | **Add industry prioritization.** (Hypothesis was silent on sector.) | The list is dense in exactly the sectors that buy email security fastest: Banking (181), Healthcare (172), SaaS (156), Aerospace & Defense (82), Fintech (69). Compliance posture is everywhere: SOC 2 (209), ISO 27001 (197), HIPAA (177). |

---

## 2. Firmographics

**Company size.** Core band is **201-10,000 employees** (72.9% of the list). This is the mid-market sweet spot: large enough to have a real attack surface, a security or IT owner, and budget, but not so large that the sale turns into a 9-month enterprise committee. AegisAI's "deploy by API in 5 minutes, no MX changes" motion is tailor-made for teams that want protection without a professional-services project.

- **201-10,000 (core):** primary volume motion.
- **10,001+ (299):** a separate, AE-led motion, not the mid-market sequence. But 200 of these 299 are disqualified non-buyers, so the real enterprise targets are the **99 non-disqualified contacts**, and all 99 are flagged `strategic_account` and routed to an AE. Bigger attack surface and ACV, but a longer multi-stakeholder cycle.
- **Under 50 (122, floor):** score at the floor and cannot reach the priority tiers. Rarely a dedicated security owner or budget. (The 51-200 "straddle" band, 21 contacts, is treated as partial since only the 100-200 slice is in the hypothesis.)
- **Unknown size (101):** hold for enrichment before spending SDR time.

**Industry.** Prioritize by risk and propensity to buy:

- **Lead (High):** Finance (Banking, Fintech, Financial Services, Investment Banking, Asset Management, Insurance/InsurTech ≈ 361 contacts), Healthcare & Life Sciences (Healthcare, Medical Devices, Biotech, Pharma ≈ 259), SaaS/Tech, Aerospace & Defense (82). Regulated, heavily phished, wire-fraud exposed, and already compliance-driven (the SOC 2 / HIPAA signals confirm it).
- **Deprioritize (Low):** Cybersecurity firms (106): likely to build in-house or are competitors. IT Services / Consulting (122): a channel and partner motion, not an end-buyer cold-outbound motion. Nonprofit: budget-constrained.

**Geography.** North America first. Copy, timezones, SLAs, and compliance framing (SOC 2, HIPAA) should assume a US/Canada buyer. A small English-speaking international tier (UK & Ireland, ANZ) can run the same sequence with timezone-shifted send times.

---

## 3. Target personas

| Segment | Who | Why they are the buyer | Count |
|---|---|---|---:|
| **Security Leader** (primary) | CISO, Global/Deputy CISO, VP/Head/Director of Information Security, VP Cyber Security, Sr. Director Cybersecurity | Email security is their explicit mandate and budget line. They feel BEC and phishing risk personally. | 563 |
| **IT Leader** (primary) | CIO, Chief Digital & Information Officer, SVP/VP/Director of IT, Head of IT | In mid-market orgs without a CISO, IT owns email security by default. They value the 5-minute, no-MX-change deploy. | 607 |
| **Tech Exec** (secondary) | CTO, Chief Product & Technology Officer | The de-facto security owner at smaller/tech-first companies. Secondary weight; often not the day-to-day owner in larger orgs. | 83 |

The message differs by segment. Security Leaders respond to detection efficacy, zero-day/BEC coverage, false-positive reduction, and SOC workload. IT Leaders and Tech Execs respond to speed of deployment, no rip-and-replace, and low operational overhead. This split drives the email branching (Part 1) and the landing-page variants (Part 2).

---

## 4. Disqualifiers (who to suppress, and why)

**30.1% of the list (603 contacts) are not buyers** and are hard-suppressed. Catching these is the core judgment test; the list is deliberately seeded with look-alikes.

| Disqualifier | Count | Rationale |
|---|---:|---|
| Junior / support IC | 209 | Tier 1 Support, Help Desk, Desktop Support, Interns. Users of email, not buyers of email security. |
| Wrong function | 187 | CFO, CRO, VP Sales, CHRO, Head of Talent. No ownership of the problem. |
| Academic / student | 106 | Professors, researchers, students, and **"Aspiring CISO \| Bootcamp Graduate"** (a title-keyword trap: has "CISO," is not one). |
| Solo / independent consultant | 52 | One-person shops below the size floor with no org to protect. |
| Retired / former | 49 | "Retired CIO," **"Former CISO \| Board Advisor."** No current buying authority. |

The classifier reads the full title and checks disqualifiers before leader keywords, so it separates a real CISO from an *aspiring* or *former* one. Verified: zero genuine senior buyers were suppressed.

Two soft cases are kept but down-weighted rather than cut: **Founders/Owners** (72) score on the size gate (legit at a 300-person SaaS, noise at a 5-person shop), and ambiguous **Other** leaders like VP Engineering (72) land in nurture, not priority.

---

## 5. Segmentation output (how this becomes a ranked list)

Applying the ICP as a weighted score (see `02-scoring-logic.md`) tiers every contact by the GTM action it deserves:

| Tier | Definition | Count | % | What happens |
|---|---|---:|---:|---|
| **A - Priority** | Right persona + senior + right size + good sector | 570 | 28.5% | Full 5-touch personalized sequence |
| **B - Strong** | Solid fit, one weaker dimension | 581 | 29.1% | Sequence, lighter personalization |
| **C - Nurture** | Partial fit | 113 | 5.7% | Marketing nurture |
| **D - Low** | Weak fit, non-DQ | 133 | 6.7% | Suppress, re-enrich |
| **Disqualified** | Non-buyer | 603 | 30.1% | Hard suppress |

**Bottom line: a raw list of 2,000 becomes 1,151 genuinely addressable contacts (57.5%), with 570 priority (Tier A) targets. Across all tiers, 233 accounts are pulled to an AE-led 1:1 motion (99 enterprise + 134 near-perfect-fit at score >= 97); the rest run the automated sequences.** Tier A skews exactly as the ICP predicts: ~94% North America, top sectors SaaS / Banking / Healthcare / Aerospace & Defense, and roughly half already showing a supported-platform signal in their headline.

The `segment` label ("Security Leader," "IT Leader," "Tech Exec") is the thread that runs through the rest of the system: it drives the email sequence branching, the landing-page persona variant, and the CRM routing table. Same segments, end to end.
