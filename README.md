# AegisAI Growth Operator

The AegisAI Operations & Growth take-home, delivered two ways: a **runnable skill** that performs the whole exercise on any contact list, and a **complete example run** you can read right now.

## What's here

- **`deliverables/`** - a full example run on a 2,000-contact list. Start here to see the work: the ICP (`01`), the scored and ranked list + scoring logic (`02`), the email sequence (`03`), the live landing page (`04`), the CRM routing and SLAs (`05`), a walkthrough (`06`), and production next steps (`07`).
- **`skill/`** - the installable Claude skill that produces all of the above on a new list. `skill/SKILL.md` is the entry point; on start it explains itself and asks whether to use your CSV or the built-in example, then walks the flow one step at a time, explaining its reasoning.
- **`aegisai-growth-operator.skill`** - the packaged skill. Download it, click "Save skill" to install, then run it in a new chat.

## The flow it runs

CSV -> enrich, score, rank -> persona landing pages -> an email sequence whose CTA links each prospect to their persona's landing page (where they book a meeting) -> send -> CRM routing + SLAs. A single `segment` label, created during scoring, threads through all of it, so a contact flows from raw row to routed lead as one connected system.

The example run turns 2,000 raw contacts into 1,151 addressable (Tier A 570 / Tier B 581), 233 strategic accounts routed to an AE, and 603 disqualified non-buyers, all reproducible from the engine.

## Run it

**As a skill (recommended):** install `aegisai-growth-operator.skill`, open a new chat, and say "run the AegisAI growth operator." It explains itself and asks whether to use your own CSV or the built-in example, then proceeds one step at a time.

**The engine directly:**
```
cd skill
python3 scripts/score_contacts.py --in data/example-contacts.csv --out /tmp/scored.csv
```
Standard library only. It auto-detects columns, so any contact CSV works.

## Notes

Built with AI assistance. The bundled contact data is synthetic sample data. Email addresses the engine generates are unverified pattern guesses and must be verified before any real send (see `deliverables/07-next-steps-and-integrations.md`).
