# Agent Briefing - the walkthrough for this repo
### Read this, and you can explain and defend the entire AegisAI take-home.

This file replaces a Loom video. It is written to brief an AI agent (Claude or similar) so a reviewer can *talk to the repo*: ask it to walk through the work, drill into any decision, and challenge the judgment. It is equally readable as a plain narrative if you'd rather just read it top to bottom.

---

## How to use this (for the reviewer)

1. Open Claude (or your model of choice) with this repository available (attach the folder, or paste this file plus any file you want to probe).
2. Paste the priming prompt below.
3. Ask anything: *"walk me through it,"* *"defend the ICP,"* *"why is Tier A 28% of the list,"* *"show me the weakest part."*

**Priming prompt to paste:**
> You are the expert on the AegisAI Operations & Growth take-home contained in this repository. `deliverables/06-walkthrough-agent-briefing.md` is your briefing. Ground every answer in the actual files and cite them by path. When you state a number, it should match `deliverables/02-scored-contacts.csv` / `deliverables/02-scoring-logic.md`. If a question isn't covered, reason from the documented logic and say explicitly when you're extrapolating. Start by giving me the 60-second summary, then ask what I'd like to go deeper on.

---

## Agent operating instructions

- **Be specific and cite files.** Every claim maps to a file. Point the reviewer there.
- **Numbers are fixed and reproducible.** They come from `score_contacts.py`. If asked, offer to re-run it. Do not invent figures.
- **Defend judgment, don't just describe.** The reviewer is grading reasoning. For any choice, give the rationale and the trade-off considered.
- **Be honest about seams.** The work has documented limitations (enrichment stubs, unverified emails, no true intent data outbound). Name them plainly; it is a strength, not a weakness.
- **Stay in AegisAI's world.** Email security, agentic AI, M365/Workspace, SEG replacement, BEC/zero-day. Voice is confident and defender-to-defender.

---

## 60-second summary

The brief: turn a list of 2,000 to 3,000 contacts into a pipeline, with an outbound targeting engine (Part 1) and an inbound conversion path (Part 2).

What was built, end to end (the write-ups live in `deliverables/`, the engine in `skill/scripts/`):
- **An ICP**, defended and refined against the actual 2,000-row list (`01-icp-definition.md`).
- **A scoring engine** that enriches every contact and assigns a transparent 0-100 fit score, then ranks and tiers them (`skill/scripts/score_contacts.py`, output `02-scored-contacts.csv`). Output: 2,000 becomes **1,151 addressable** contacts, **570 priority (Tier A)**, **233 pulled to an AE 1:1 motion**, and **603 disqualified**.
- **A 5-touch email sequence** for the top tier, branched by segment, in AegisAI's real voice, anchored on their real 14-day-threat-report offer (`03-email-sequence.md`).
- **A live, persona-adaptive landing page** with a lead form that simulates routing on submit (`04-landing-page.html`).
- **CRM routing logic**: fit x intent scoring, a decision table, a handoff flow, and speed-based SLAs (`05-routing-logic.md`).

The spine of the whole thing: a single `segment` label, created in Part 1, reused in Parts 1 and 2, so a contact flows from raw row to routed lead as one system.

---

## Repo map (what to open for what question)

| If the reviewer asks about... | Open |
|---|---|
| Who we target and why | `deliverables/01-icp-definition.md` |
| How scoring works, weights, disqualifiers | `deliverables/02-scoring-logic.md` |
| The code / reproducibility | `skill/scripts/score_contacts.py` |
| The actual ranked contacts | `deliverables/02-scored-contacts.csv` |
| The outbound copy | `deliverables/03-email-sequence.md` |
| The conversion page | `deliverables/04-landing-page.html` |
| What happens after a lead converts | `deliverables/05-routing-logic.md` |

---

## Decision log (the "why" behind every choice)

**1. Split "security and IT leaders" into two segments.** The brief lumped them. The data shows 563 security leaders and 607 IT leaders, and they buy differently: security owns email security explicitly (angle = detection, BEC, false positives), while IT owns it by default in orgs without a CISO (angle = 5-minute deploy, no MX changes, less to manage). One message for both would underperform, so the email sequence and landing page each branch on this.

**2. Keep 201-10,000 as core, but treat 10,001+ as a separate AE-led motion and floor out the smallest.** 72.9% of the list sits in 201-10,000. 15% (299) are 10,001+, above the brief's ceiling; of those, 200 are disqualified non-buyers and the 99 real contacts all get a `strategic_account` flag and route to an AE, not the mid-market sequence. And 6.1% (122) under 50 employees score at the floor. This is the clearest example of refining the hypothesis instead of accepting it. (Note: the strategic flag is decoupled from tier on purpose, so a Tier B or C enterprise contact still gets the enterprise motion; 233 accounts are flagged in total.)

**3. Suppress 30% of the list.** The list is seeded with look-alikes: junior support (209), wrong-function execs like CFO/CRO/CHRO (187), academics and students including "Aspiring CISO | Bootcamp Graduate" (106), solo consultants (52), and "Retired CIO" / "Former CISO" (49). The classifier checks disqualifiers before leader keywords and reads the whole title, so it tells a real CISO from an aspiring or former one. Verified: zero genuine buyers were suppressed. Catching these is the core judgment test.

**4. Weight persona highest (35 of 100).** A perfect-size company in a perfect industry is worthless if the contact can't buy. Persona, then seniority (authority), then size (need + ACV), then industry (propensity), then a small signal component from headline platform/compliance mentions. Weights are the honest ranking of what predicts a winnable deal, and they all live in one `WEIGHTS` dict so they're auditable.

**5. Tier by GTM action, not a forced curve.** This is a curated leader list, so scores legitimately compress high (median 87). Forcing a bell curve would be dishonest. Instead each cutoff maps to what a rep/system does: A (>=90) full sequence, B (78-89) lighter sequence, C (60-77) nurture, D (<60) suppress. That's why Tier A is ~28% and not a token 5%: the list really is that good.

**6. Anchor outbound on the 14-day threat report, not "book a demo."** AegisAI's real low-friction offer: connect read-only by API, get a report of what your current filter missed. For skeptical security buyers, proof beats a pitch, so it leads every touch and is the landing page's primary CTA.

**7. Make the landing page a system, not a brochure.** The persona toggle ties to Part 1 segments, the emails deep-link `?segment=`, and the form runs the routing decision on submit so a reviewer can *see* the Part 1 to Part 2 handoff happen.

**8. Design SLAs around the speed-to-lead data.** 5 minutes vs 30 makes a lead 21x more likely to qualify. So P1 hot leads get a 5-minute first-touch SLA with auto-escalation, and strategic accounts get 1 hour (bigger, multi-stakeholder). Ownership is explicit so nothing sits unactioned.

---

## Numbers cheat-sheet (memorize; all reproducible)

- **Input:** 2,000 contacts, 11 columns; `Enriched Email` was 100% empty.
- **Disqualified:** 603 (30.1%) - junior 209, wrong-function 187, academic 106, solo 52, retired 49.
- **Tiers:** A 570 (28.5%), B 581 (29.1%), C 113 (5.7%), D 133 (6.7%), DQ 603 (30.1%).
- **Addressable (A+B):** 1,151 (57.5%). **Strategic (AE 1:1, all tiers):** 233 = 99 non-DQ enterprise + 134 near-perfect (score >= 97).
- **Segments:** IT Leader 607, Security Leader 563, Tech Exec 83, Founder/Owner 72, Other 72, DQ 603.
- **Company size:** core 201-10,000 = 1,457 (72.9%); enterprise 10,001+ = 299 (15%); under-50 floor = 122 (6.1%); 51-200 = 21; missing = 101.
- **Geo:** ~91% North America (US 1,736, Canada 94); thin international tail.
- **Weights:** Persona 35 / Seniority 20 / Size 20 / Industry 15 / Signal 10. Tier cutoffs A>=90, B 78-89, C 60-77, D<60.
- **Tier A profile:** 94% North America; top sectors SaaS, Banking, Healthcare, Aerospace & Defense; ~half show a supported-platform signal.
- **SLA basis:** 5 min = 21x more likely to qualify vs 30 min (MIT/LRM); 1 hr = 60x vs 24 hr (HBR); 78% buy from first responder.

---

## Suggested walkthrough script (about 7 minutes)

1. **Frame (30s).** "The job was raw list to routed lead. I built it as one system, and the spine is a single segment label that carries from scoring through outreach to routing."
2. **ICP (90s).** Open `icp-definition.md`. The brief's hypothesis was directionally right; I refined it five ways (split personas, size floor + enterprise motion, geo, industry, and suppressing the 30% who aren't buyers). Show the disqualifier table and the "Aspiring/Former CISO" catch.
3. **Scoring (2m).** Open `scoring_logic.md`, then the `WEIGHTS` dict in `score_contacts.py`. Explain why persona is weighted highest and why tiers map to actions. Offer to re-run the script live.
4. **Scored list (30s).** Open `scored_contacts.csv`, sort by `fit_score`: real CISOs at Banking/Healthcare/SaaS on top, disqualified at the bottom.
5. **Email (60s).** Open `sequence.md`. Show the segment branching and the 14-day-report anchor. Note claims are all real, one CTA per email.
6. **Landing page (60s).** Open `index.html`, toggle Security vs IT (or `?segment=it`), submit the form, show the routing readout.
7. **Routing (60s).** Open `routing-logic.md`. Fit x intent matrix, the decision table, and the 5-minute SLA tied to the speed-to-lead data. Close on the through-line.

---

## Anticipated questions (with strong answers)

**Judgment**

*Q: Why is almost 60% of the list "addressable"? Isn't that too generous?*
Because the list is pre-curated to security/IT leaders, so genuine fit compresses high. I chose not to fake a curve. What I did instead: suppress 30% hard, and within the addressable base, concentrate effort with the strategic flag (233 accounts pulled to AE 1:1) and the Tier A/B split so reps aren't told "everyone is priority."

*Q: You disqualified a "Chief Revenue Officer" and kept a "Director of IT." Defend that.*
The CRO doesn't own or budget email security; the Director of IT does, especially in a mid-market org without a CISO. Persona and function, not seniority alone, decide fit. A CFO or CHRO is senior and still a hard disqualifier.

*Q: Isn't 10,001+ inside the brief's "up to 10,000"? Why keep them?*
Strictly they're above the stated ceiling. The data has 299, but 200 are disqualified non-buyers, so the real enterprise targets are 99, and I route all 99 to a different (AE-led, longer) motion rather than the mid-market sequence. That's the refine-the-hypothesis move the brief invited, and the code flags them regardless of tier so a Tier B enterprise contact still gets the enterprise motion.

**Systems thinking**

*Q: Show me that this is one system, not six deliverables.*
The `segment` field is created in `score_contacts.py`, stored in the CSV, used to branch `sequence.md`, used to switch the persona in `index.html` (with `?segment=` deep-links from the emails), and used as a routing dimension in `routing-logic.md`. Same label, five files. Fit tier does the same job across scoring and routing.

*Q: How does an outbound contact become an inbound lead without losing context?*
The email links to the landing page with its segment; the page pre-selects that persona; on conversion the routing re-uses the same fit engine and adds intent. Nothing is re-derived from scratch.

**Execution**

*Q: Is the scoring real or hand-waved?*
Real and reproducible: `python3 score_contacts.py` regenerates the CSV and every number in the docs from the standard library alone. Happy to run it now and change a weight to show the tiers move.

*Q: Does the landing page actually work?*
Yes, it's self-contained HTML. The persona toggle and deep-link work, the form validates, and on submit it runs the routing decision client-side and shows the readout. No backend, by design, for a take-home.

**Craft**

*Q: How do you know the email voice matches AegisAI?*
It's built from their live site: the SEG-replacement angle, "reason like an analyst," "no MX changes," ">90% fewer false positives," "22% more attacks caught," the Battery Ventures Series A, the ex-Google founder story, and the real 14-day-report offer. Every claim is one they actually make.

**Resourcefulness**

*Q: Where did AI help, and where did you make the calls?*
AI did the profiling, the engine, the copy drafting, and the page. The judgment calls (weights, disqualifier logic, tier philosophy, the strategic-account carve-out, anchoring on the threat report) are documented decisions, not model defaults. And this very briefing is an AI-native alternative to a Loom, which fits a company selling agentic AI.

**Tough / adversarial**

*Q: What's the weakest part of this?*
Platform fit is inferred from headlines, which only ~15% of contacts fill in. It's the lowest-weighted component for exactly that reason. In production I'd replace it with an MX/tech-stack lookup, which would make it far stronger and let me raise its weight.

*Q: The emails are unverified guesses. Isn't that a problem?*
Yes, which is why they're flagged `unverified_guess` and the sequence explicitly forbids sending to them until verified. The raw file's email column was 100% empty, so this is the exact gap a real enrichment + verification step (Apollo + NeverBounce) fills before anything sends.

*Q: If you had two more days?*
Real enrichment/verification via API; A/B subject-line variants with a test plan; an account-level rollup (score companies, not just contacts) for ABM; and wiring the landing-page form to a real CRM sandbox with the routing rules live.

---

## Honest limitations

1. Platform/intent signals for outbound are proxies from sparse headline text, not verified tech-stack or behavioral data.
2. Emails are pattern guesses, unverified, and must not be mailed as-is.
3. Scoring is contact-level; ABM would want an account-level rollup.
4. The landing page has no backend; routing is simulated client-side to illustrate the logic.
5. Score compression is inherent to a pre-curated list; tiers would be re-baselined against a colder, larger universe.

Every one of these is a deliberate, documented trade-off for a 4-6 hour scope, and each has a clear production upgrade path noted above.
