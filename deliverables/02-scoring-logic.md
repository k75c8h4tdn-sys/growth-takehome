# Scoring Logic & Weights

How `score_contacts.py` turns 2,000 raw contacts into an enriched, ranked, tiered list. Everything here is implemented in code, and every weight lives in the `WEIGHTS` dict at the top of the script so it is auditable and tunable.

## The model in one line

`fit_score` is a 0-100 weighted sum of five components. Hard disqualifiers override the score and suppress the contact entirely.

```
fit_score = Persona(35) + Seniority(20) + Size(20) + Industry(15) + Signal(10)
```

## Why these five components, and these weights

The buyer for API-based email security is a person (does this role own the problem?) inside a company (is it the right size and sector?) reachable on a supported platform. The weights rank those questions by how strongly each predicts a real, winnable deal.

| Component | Weight | What it measures | Why it is weighted this way |
|---|---:|---|---|
| **Persona** | 35 | Does this role own or champion email security? | The single biggest predictor. A perfect-size company is worthless if the contact is in HR. Highest weight. |
| **Seniority** | 20 | Budget and decision authority. | AegisAI is a platform purchase. A CISO signs; an analyst cannot. |
| **Company size** | 20 | Employees vs the ICP band (201-10,000 core). | Drives both need (bigger attack surface) and ACV. Below ~100 employees rarely has budget or a dedicated security owner. |
| **Industry** | 15 | Sector risk and propensity to buy. | Regulated / high-phishing sectors (finance, healthcare, defense, SaaS) buy faster and renew. |
| **Signal** | 10 | Headline proxy for platform fit + compliance pressure. | The only near-"intent" signal in the raw data. Kept small because the headline field is sparse and noisy. |

### Persona sub-scores (share of the 35 points)
Security Leader 1.00 (CISO, VP/Head/Dir Information Security, Cyber), IT Leader 0.92 (CIO, VP/Dir IT, Head of IT, Chief Digital & Information), Tech Exec 0.70 (CTO, Chief Product & Technology), IT Practitioner 0.42 (Security/IT Manager, Sysadmin, Security Engineer), Founder/Owner 0.45 (size gate does the rest), Other 0.15, Disqualified 0.00.

Security leaders rank just above IT leaders because email security is their explicit mandate; IT leaders own it by default in orgs without a dedicated security function, which is most of the mid-market.

### Seniority sub-scores (share of 20)
C-level 1.00, VP/SVP 0.85, Head/Director 0.72, Manager 0.40, IC 0.12, Unknown 0.30.

### Company-size sub-scores (share of 20)
Core (201-10,000) 1.00, Enterprise (10,001+) 0.70, Straddle (51-200) 0.60, Below floor (1-50) 0.15, Unknown 0.40.

Enterprise scores below core on purpose. Those accounts are valuable but need a different (longer, multi-stakeholder) motion, so they should not crowd the mid-market sequence. They are re-surfaced separately via the `strategic_account` flag.

### Industry sub-scores (share of 15)
High 1.00, Medium 0.60, Low 0.27, Unknown 0.40. High = banking, financial services, fintech, insurance, healthcare, medical devices, biotech, pharma, aerospace & defense, SaaS, and other tech. Low = cybersecurity (build-it-themselves / competitor risk), IT services & consulting (a channel, not the end buyer), and nonprofit (budget).

### Signal sub-score (max 10)
+7 if the headline names a supported platform (Microsoft 365, Google Workspace, or Azure as an M365 proxy); +3 if it shows compliance posture (ISO 27001, SOC 2, HIPAA, PCI, "compliance"). Capped at 10.

## Hard disqualifiers (override the score, suppress the contact)

These contacts can never be the buyer, so they are removed from outbound regardless of company or score. **603 of 2,000 (30.1%)** were suppressed:

| Reason | Count | Examples caught |
|---|---:|---|
| Junior / support IC | 209 | Tier 1 Support Engineer, Help Desk Analyst, Security Operations Intern |
| Wrong function | 187 | CFO, CRO, VP Sales, CHRO, Head of Talent |
| Academic / student | 106 | Professor, Graduate Researcher, "Aspiring CISO \| Bootcamp Graduate" |
| Solo / independent consultant | 52 | Independent IT Consultant, Principal Consultant |
| Retired / former | 49 | Retired CIO, "Former CISO \| Board Advisor" |

The classifier checks disqualifiers **before** leader titles and reads the full title string, so it correctly separates a real CISO from an *aspiring* or *former* one. A guard prevents a genuine senior title (e.g. a Security Director whose headline mentions a "junior" program) from being suppressed by a stray keyword.

## Tiers map to a GTM action, not a bell curve

This is a hand-curated list of security and IT leaders, so fit scores legitimately compress toward the top (non-DQ median 87). Forcing an artificial curve would be dishonest. Instead each cutoff maps to something a rep or a system actually does:

| Tier | Score | Count | % | Action / channel |
|---|---|---:|---:|---|
| **A - Priority** | ≥ 90 | 570 | 28.5% | Full 5-touch personalized sequence, SDR-owned |
| **B - Strong** | 78-89 | 581 | 29.1% | Sequence, templated personalization |
| **C - Nurture** | 60-77 | 113 | 5.7% | Marketing nurture, no SDR capacity spent |
| **D - Low** | < 60 | 133 | 6.7% | Suppress from active outbound, re-enrich later |
| **Disqualified** | n/a | 603 | 30.1% | Hard suppress |

**Addressable top-of-funnel (A+B): 1,151 contacts (57.5%).** Separately, a `strategic_account` flag (independent of tier) marks **233** accounts for an AE-led 1:1 motion instead of the automated sequence: the **99** non-disqualified enterprise contacts (10,001+, a different sales motion) plus the **134** near-perfect-fit mid-market contacts (score >= 97). Of those 233, 147 are Tier A, 66 Tier B, and 20 Tier C/D enterprise; all are pulled from the automated sequence.

## Worked examples

- **100/100** Chief Information Security Officer, Banking, 501-1,000, headline cites SOC 2: Persona 35 + Seniority 20 + Size 20 + Industry 15 + Signal 10. Tier A, strategic-eligible.
- **~84** CISO, medium-tier industry, core size, no headline signal: 35 + 20 + 20 + 9 + 0. Tier B.
- **~70** Director of IT, 10,001+, medium industry, no signal: 32.2 + 14.4 + 14 + 9 + 0. Tier C by fit score, but `strategic_account = yes` because it is enterprise, so it is deliberately routed to an AE, not the mid-market sequence. (This is the point of decoupling the strategic flag from tier: a big account with a middling individual contact still deserves the enterprise motion.)
- **0 / suppressed** "Retired CIO": disqualified before scoring.

## Enrichment (what the raw file did not contain)

The raw list has no employee count number, no tech stack, and the `Enriched Email` column is **100% empty**. The script derives what the existing fields support: `persona`, `seniority`, `size_band`, `region`, `platform_signal`, and `compliance_signal`. Email is a **pattern-based guess** (`first.last@companyslug.com`) flagged `email_status = unverified_guess`.

In production this step is an API call, not string parsing: Apollo / Clearbit / ZoomInfo to fill firmographics, verified email, and real tech stack (e.g. detected MX = Google vs Microsoft, which would replace the headline platform proxy and could move into the Signal weight), then NeverBounce / ZeroBounce to confirm deliverability before any address enters a sequence.

## Known limitations (honest seams)

1. **Platform is inferred from headlines**, which only ~15% of contacts fill in. A real MX/tech-stack lookup would make the Signal component far stronger and could raise its weight.
2. **No true intent data** in an outbound list. Intent (site visits, content downloads, G2 activity) is layered in Part 2, where fit + intent together drive routing.
3. **Score compression** is real, not a bug: the list is pre-filtered to leaders. Tiers are therefore action-based cutoffs, and would be re-baselined against a colder, larger list.
4. **Email guesses are unverified** and must not be mailed as-is.

## Reproduce

```
cd skill
python3 scripts/score_contacts.py --in data/example-contacts.csv --out /tmp/scored.csv
```
Output: a scored CSV (all raw columns + enrichment + component scores + fit_score + tier + segment + strategic flag), plus the summary above printed to stdout. The committed copy of this run is `02-scored-contacts.csv` in this folder.
