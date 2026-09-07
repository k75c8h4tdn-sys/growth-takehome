# ICP Reference (operational)
### The rules the operator applies when it enriches and scores a list.

This is the short, operational version the operator applies. On each run it re-derives the evidence for the specific list while keeping these rules.

**One-line ICP:** a security or IT leader (Director and above) at a 201-10,000 employee company in a regulated or high-phishing-risk sector, on Microsoft 365 or Google Workspace, in North America.

## Firmographics (and why)

- **Company size: 201-10,000 core.** Big enough to have a real attack surface, a security/IT owner, and budget; small enough that the sale is not a 9-month enterprise committee. AegisAI's 5-minute API deploy is built for this band.
  - **10,001+**: do not discard. High ACV, but a longer multi-stakeholder motion, so flag `strategic_account` and route to an AE, not the mid-market sequence.
  - **Under ~100**: suppress. Rarely a dedicated owner or budget.
- **Industry priority:** lead with regulated / heavily-phished sectors (finance, healthcare & life sciences, aerospace & defense, SaaS/tech). These buy faster and renew. Deprioritize cybersecurity firms (build-it-themselves / competitor risk) and IT-services/consulting (a channel, not the end buyer).
- **Geography:** North America first (copy, timezones, SLAs, SOC 2 / HIPAA framing assume a US/Canada buyer). Reasoning: it is where the density and the staffed sales coverage are.

## Personas (who is the buyer, and why)

- **Security Leader (primary):** CISO, Global/Deputy CISO, VP/Head/Director of Information Security, VP Cyber Security. Email security is their explicit mandate and budget.
- **IT Leader (primary):** CIO, Chief Digital & Information Officer, SVP/VP/Director of IT, Head of IT. In mid-market orgs without a CISO, IT owns email security by default.
- **Tech Exec (secondary):** CTO, Chief Product & Technology Officer. The de-facto owner at smaller/tech-first companies; secondary because they are often not the day-to-day owner in larger orgs.

## Disqualifiers (who to suppress, and why)

Hard-suppress. These can never be the buyer, and lists are usually seeded with look-alikes:

- **Junior / support IC** (Tier 1, help desk, desktop support, interns): users of email, not buyers of email security.
- **Wrong function** (CFO, CRO, VP Sales, CHRO, Head of Talent): no ownership of the problem.
- **Academic / student** (professors, researchers, students, "aspiring," "bootcamp graduate"): no buying authority.
- **Solo / independent consultant**: below the size floor, no org to protect.
- **Retired / former** ("Retired CIO," "Former CISO"): no current authority.

Rule that matters: check disqualifiers BEFORE leader keywords, and read the whole title, so a real CISO is kept but an *aspiring* or *former* one is cut. Verify after each run that no genuine senior buyer was suppressed.
