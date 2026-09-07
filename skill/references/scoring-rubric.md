# Scoring Rubric (the reasoning fallback)
### How to score by hand when code cannot run.

`score_contacts.py` is the exact path. When the environment cannot execute Python, apply THIS rubric by reasoning: the weights are identical, so the logic is the same, only the executor changes. On a large list, score every contact if you can; if not, score a representative sample and say so. Always explain the "why," not just the number.

## The formula

`fit_score = Persona(35) + Seniority(20) + Size(20) + Industry(15) + Signal(10)` = 0-100.

Why this ranking: the buyer is a **person** (does this role own email security?) at a **company** (right size and sector?) reachable on a **supported platform**. Persona is weighted highest because a perfect company is worthless if the contact cannot buy.

## Components

**Persona (35)** - fraction of 35: Security Leader 1.00, IT Leader 0.92, Tech Exec 0.70, IT Practitioner 0.42, Founder/Owner 0.45, Other 0.15, Disqualified 0.00. (Security just above IT: email security is security's explicit mandate; IT owns it by default in orgs without a CISO.)

**Seniority (20)** - C-level 1.00, VP/SVP 0.85, Head/Director 0.72, Manager 0.40, IC 0.12, Unknown 0.30. (Proxy for budget and signing authority.)

**Company size (20)** - Core 201-10,000 = 1.00, Enterprise 10,001+ = 0.70, Straddle 51-200 = 0.60, Below 1-50 = 0.15, Unknown 0.40. (Enterprise scores below core on purpose so it does not crowd the mid-market sequence; it is re-surfaced via the strategic flag.)

**Industry (15)** - High 1.00, Medium 0.60, Low 0.27, Unknown 0.40. High = finance, healthcare/life-sciences, aerospace & defense, SaaS/tech, telecom. Low = cybersecurity (DIY/competitor), IT services/consulting (channel), nonprofit (budget).

**Signal (10)** - +7 if the headline/enrichment shows a supported platform (Microsoft 365, Google Workspace, or Azure as an M365 proxy); +3 for compliance posture (ISO 27001, SOC 2, HIPAA, PCI, "compliance"). Capped at 10. Kept small because this data is sparse and noisy; a real MX/tech-stack lookup would justify a higher weight.

## Hard disqualifiers (override the score to Disqualified)

Retired/former, academic/student ("aspiring," "bootcamp graduate"), wrong-function execs (CFO, CRO, sales, HR, marketing), junior/support IC, solo/independent consultants. **Check these before leader keywords and read the full title** so a real CISO is kept but an aspiring/former one is cut.

## Tiers (map to a GTM action)

A (>=90) full 5-touch sequence; B (78-89) sequence, lighter personalization; C (60-77) marketing nurture; D (<60) suppress, re-enrich; Disqualified = hard suppress. Plus `strategic_account` (enterprise-sized or score >=97) = pull for 1:1 AE.

Why action-based cutoffs and not a forced curve: a curated leader list legitimately compresses high (median ~87). Faking a bell curve would be dishonest; instead each cutoff is something a rep or system actually does. On a colder, larger list, re-baseline these cutoffs.

## After scoring, always report

The tier distribution, the addressable count (A+B), the top segments, the disqualified reasons, and a spot-check confirming no genuine buyer was suppressed. Show the reasoning behind the weights, not just the ranked list.
