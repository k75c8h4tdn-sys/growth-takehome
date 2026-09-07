#!/usr/bin/env python3
"""
AegisAI Growth Operator  --  Part 1 Scoring Engine (portable, any list)
=======================================================================

Turns ANY inbound contact list into an enriched, ranked, tiered list.

It auto-detects columns, so it does not care whether the header says
"Job Title" or "title" or "role". It fills the fields the raw file lacks
by deriving them from what is present, applies a transparent weighted
0-100 fit score, hard-suppresses non-buyers, and tiers the rest by GTM action.

USAGE
    python3 score_contacts.py                          # ../data/example-contacts.csv (or pass --in/--out)
    python3 score_contacts.py --in mylist.csv --out scored.csv
    python3 score_contacts.py --in mylist.csv --top 25 # also print the top 25

WHY A SCRIPT AND A RUBRIC
    This is the exact, reproducible path. When code cannot run, the agent
    scores the same way by reasoning from references/scoring-rubric.md, which
    documents these identical weights. Same model, two execution modes.

Only the Python standard library is used.
"""

import argparse, csv, os, re, sys
from collections import Counter

# --------------------------------------------------------------------------- #
# SCORING WEIGHTS  --  the whole model in one place (sums to 100)              #
# Mirror any change here into references/scoring-rubric.md so the reasoning        #
# fallback stays in sync.                                                      #
# --------------------------------------------------------------------------- #
WEIGHTS = {"persona": 35, "seniority": 20, "size": 20, "industry": 15, "signal": 10}
assert sum(WEIGHTS.values()) == 100

PERSONA_SCORE = {
    "security_leader": 1.00, "it_leader": 0.92, "tech_exec": 0.70,
    "it_practitioner": 0.42, "founder_owner": 0.45, "other": 0.15,
    "disqualified": 0.00,
}
SENIORITY_SCORE = {"c_level": 1.00, "vp": 0.85, "head_dir": 0.72,
                   "manager": 0.40, "ic": 0.12, "unknown": 0.30}
SIZE_SCORE = {"core": 1.00, "enterprise": 0.70, "straddle": 0.60,
              "below": 0.15, "unknown": 0.40}
INDUSTRY_SCORE = {"high": 1.00, "medium": 0.60, "low": 0.27, "unknown": 0.40}

INDUSTRY_HIGH = ["banking", "financial services", "fintech", "investment banking",
    "asset management", "insurance", "insurtech", "healthcare", "medical devices",
    "biotech", "pharmaceutical", "life sciences", "aerospace", "defense",
    "r&d / defense", "saas", "technology / saas", "technology", "hr tech",
    "edtech", "data / analytics", "telecommunications", "telecom"]
INDUSTRY_LOW = ["cybersecurity", "it services", "consulting", "nonprofit"]

# --------------------------------------------------------------------------- #
# TIER THRESHOLDS  (map to a GTM action, not a forced curve)                   #
# --------------------------------------------------------------------------- #
def tier_for(score):
    if score >= 90: return "A"   # Priority  -> full 5-touch personalized sequence
    if score >= 78: return "B"   # Strong    -> sequence, templated personalization
    if score >= 60: return "C"   # Nurture   -> marketing nurture
    return "D"                    # Low       -> suppress, re-enrich

def is_strategic(score, size_cat):
    return size_cat == "enterprise" or score >= 97

# --------------------------------------------------------------------------- #
# COLUMN AUTO-MAPPING  --  works on any header                                 #
# --------------------------------------------------------------------------- #
SYNONYMS = {
    "first_name":  ["first name", "firstname", "first", "given name", "fname"],
    "last_name":   ["last name", "lastname", "last", "surname", "family name", "lname"],
    "full_name":   ["full name", "fullname", "name", "contact name", "contact"],
    "job_title":   ["job title", "jobtitle", "title", "role", "position", "job role"],
    "company":     ["company name", "company", "organization", "organisation",
                    "account", "employer", "org"],
    "industry":    ["industry", "sector", "vertical"],
    "company_size":["company size", "companysize", "size", "employees",
                    "employee count", "headcount", "num employees", "# employees",
                    "company headcount", "staff"],
    "location":    ["location", "country", "geo", "region", "city", "state", "address"],
    "headline":    ["headline", "bio", "summary", "about", "description"],
    "email":       ["enriched email", "work email", "email address", "email", "e-mail"],
}

def map_columns(fieldnames):
    """Return {canonical_field: actual_header_or_None}. Longer synonyms win."""
    lower = {fn.lower().strip(): fn for fn in fieldnames}
    mapping = {}
    for field, syns in SYNONYMS.items():
        found = None
        # exact match first, then substring, preferring longer synonym strings
        for syn in sorted(syns, key=len, reverse=True):
            if syn in lower:
                found = lower[syn]; break
        if not found:
            for syn in sorted(syns, key=len, reverse=True):
                for lc, orig in lower.items():
                    if syn in lc:
                        found = orig; break
                if found: break
        mapping[field] = found
    # don't let job_title and headline collapse onto the same column
    if mapping["job_title"] and mapping["job_title"] == mapping.get("headline"):
        mapping["headline"] = None
    return mapping

def val(row, mapping, field):
    col = mapping.get(field)
    return (row.get(col, "") or "").strip() if col else ""

# --------------------------------------------------------------------------- #
# TITLE CLASSIFIER  (DQ first, then leaders)                                   #
# --------------------------------------------------------------------------- #
DQ_PATTERNS = {
    "retired":        [r"\bretired\b", r"\bemeritus\b", r"\bformer\b"],
    "academic":       [r"\bprofessor\b", r"\blecturer\b", r"\bresearcher\b",
                       r"\bstudent\b", r"\bmba candidate\b", r"\bph\.?d\b",
                       r"\bgraduate\b", r"\bfaculty\b", r"\baspiring\b", r"\bbootcamp\b"],
    "wrong_function": [r"human resources", r"\bchro\b", r"chief people",
                       r"talent acquisition", r"\bhr\b", r"\bsales\b",
                       r"account executive", r"\bae\b", r"business development",
                       r"\bbdr\b", r"\bsdr\b", r"revenue officer", r"\bcro\b",
                       r"\bmarketing\b", r"chief financial", r"\bcfo\b",
                       r"financial officer", r"\baccounting\b",
                       r"jefe de informaci.n financiera"],
    "junior_ic":      [r"tier [123]", r"help ?desk", r"desktop support",
                       r"support engineer", r"support specialist", r"service desk",
                       r"\bintern\b", r"\bapprentice\b", r"\bjunior\b", r"\bjr\.?\b",
                       r"\bcoordinator\b", r"\btechnician\b"],
    "solo_consultant":[r"\bindependent\b", r"\bfreelance\b", r"principal consultant",
                       r"sole proprietor"],
}
LEADER_KEYWORDS = ["chief", "ciso", "cio", "cto", "vp", "svp", "evp",
                   "head of", "director", "vice president"]

def classify_title(title):
    s = (title or "").lower().strip()
    if not s: return "other", None
    has_leader = any(k in s for k in LEADER_KEYWORDS)
    for reason, pats in DQ_PATTERNS.items():
        for p in pats:
            if re.search(p, s):
                if reason in ("junior_ic", "solo_consultant") and has_leader \
                        and any(x in s for x in ["security", "information", "cyber", "technology"]):
                    continue
                return "disqualified", reason
    sec = any(x in s for x in ["ciso", "chief information security",
              "information security", "cyber security", "cybersecurity", "chief security"])
    if sec or (("security" in s) and has_leader):
        return "security_leader", None
    it = any(x in s for x in ["chief information officer", "cio", "chief digital",
             "chief technology & information", "chief technical & information",
             "information technology", "head of it", "director of it", "it director",
             "vp of it", "vp, it"])
    if it and (has_leader or "head of it" in s):
        return "it_leader", None
    if any(x in s for x in ["chief technology officer", "cto",
            "chief product & technology", "chief technical officer"]):
        return "tech_exec", None
    if any(x in s for x in ["security manager", "it manager", "security engineer",
            "systems administrator", "network administrator", "sysadmin",
            "infrastructure", "security architect", "it operations", "grc",
            "governance, risk"]):
        return "it_practitioner", None
    if any(x in s for x in ["founder", "owner", "managing partner"]):
        return "founder_owner", None
    return "other", None

def classify_seniority(title):
    s = (title or "").lower()
    if any(x in s for x in ["chief", "ciso", "cio", "cto", "cpo", "cdo"]) or re.search(r"\bc[a-z]?o\b", s):
        return "c_level"
    if any(x in s for x in ["svp", "evp", "senior vice president", "executive vice president"]):
        return "vp"
    if "vp" in s or "vice president" in s: return "vp"
    if any(x in s for x in ["head of", "director"]): return "head_dir"
    if "manager" in s or "lead" in s: return "manager"
    if any(x in s for x in ["engineer", "administrator", "analyst", "specialist",
            "coordinator", "consultant", "technician", "support"]):
        return "ic"
    return "unknown"

# --------------------------------------------------------------------------- #
# COMPANY SIZE  --  handles bands ("201-500") AND raw numbers ("850")          #
# --------------------------------------------------------------------------- #
BAND_MAP = {"1-10": "below", "11-50": "below", "51-200": "straddle",
            "201-500": "core", "501-1,000": "core", "501-1000": "core",
            "1,001-5,000": "core", "1001-5000": "core",
            "5,001-10,000": "core", "5001-10000": "core", "10,001+": "enterprise",
            "10001+": "enterprise"}

def size_from_number(n):
    if n < 51: return "below"
    if n <= 200: return "straddle"
    if n <= 10000: return "core"
    return "enterprise"

def classify_size(size):
    s = (size or "").strip()
    if not s: return "unknown"
    key = s.replace(" ", "")
    if s in BAND_MAP: return BAND_MAP[s]
    if key in BAND_MAP: return BAND_MAP[key]
    # pull the first integer out of things like "850", "~1,200 employees", "500-1000"
    m = re.search(r"(\d[\d,]*)", s)
    if m:
        try: return size_from_number(int(m.group(1).replace(",", "")))
        except ValueError: pass
    return "unknown"

# --------------------------------------------------------------------------- #
# REGION / SIGNALS / INDUSTRY / EMAIL                                          #
# --------------------------------------------------------------------------- #
NA = ["united states", "usa", "u.s.", "canada", "metropolitan area", "new york city",
      "chicago area", "san francisco", "bay area", "los angeles", "greater "]
UKI = ["united kingdom", "u.k.", "england", "scotland", "wales", "ireland"]
ANZ = ["australia", "new zealand"]
def classify_region(loc):
    s = (loc or "").lower()
    if not s: return "Unknown"
    if any(x in s for x in NA): return "North America"
    if any(x in s for x in UKI): return "UK & Ireland"
    if any(x in s for x in ANZ): return "ANZ"
    if any(x in s for x in ["united arab emirates","saudi","germany","france","spain",
            "netherlands","sweden","nigeria","kenya","south africa","poland",
            "switzerland","italy"]): return "EMEA"
    if any(x in s for x in ["mexico","brazil","panama","colombia","chile","argentina","peru"]):
        return "LATAM"
    if any(x in s for x in ["india","singapore","philippines","japan","china",
            "hong kong","indonesia","malaysia","vietnam","korea"]): return "APAC"
    return "Other"

def classify_platform(h):
    s = (h or "").lower()
    ws = ("google workspace" in s) or ("gsuite" in s) or ("g suite" in s)
    ms = ("microsoft 365" in s) or ("m365" in s) or ("office 365" in s) or ("azure" in s)
    if ws and ms: return "Both"
    if ws: return "Google Workspace"
    if ms: return "Microsoft 365"
    return "Unknown"

def has_compliance_signal(h):
    s = (h or "").lower()
    return any(x in s for x in ["iso 27001","soc 2","soc2","hipaa","pci","compliance","gdpr","fedramp"])

def classify_industry(ind):
    s = (ind or "").lower().strip()
    if not s: return "unknown"
    if any(x in s for x in INDUSTRY_LOW):  return "low"
    if any(x in s for x in INDUSTRY_HIGH): return "high"
    return "medium"

def enrich_email(first, last, full, company):
    if (not first or not last) and full:
        parts = full.split()
        if len(parts) >= 2: first, last = parts[0], parts[-1]
    if not (first and last and company): return "", "missing_data"
    slug = re.sub(r"\b(the|inc|inc\.|llc|ltd|ltd\.|corp|corporation|company|co|co\.|group|plc|sa|ag|gmbh|holdings)\b", "", company.lower())
    slug = re.sub(r"[^a-z0-9]", "", slug)
    if not slug: return "", "missing_data"
    return f"{first.lower()}.{last.lower()}@{slug}.com", "unverified_guess"

# --------------------------------------------------------------------------- #
# SCORE ONE ROW                                                                #
# --------------------------------------------------------------------------- #
SEGMENT = {"security_leader":"Security Leader","it_leader":"IT Leader",
           "tech_exec":"Tech Exec","it_practitioner":"IT Practitioner",
           "founder_owner":"Founder/Owner","other":"Other","disqualified":"Disqualified"}

def score_row(row, mapping):
    title = val(row, mapping, "job_title")
    persona, dq_reason = classify_title(title)
    seniority = classify_seniority(title)
    size_cat  = classify_size(val(row, mapping, "company_size"))
    region    = classify_region(val(row, mapping, "location"))
    ind_tier  = classify_industry(val(row, mapping, "industry"))
    platform  = classify_platform(val(row, mapping, "headline"))
    compliance = has_compliance_signal(val(row, mapping, "headline"))

    p_persona   = WEIGHTS["persona"]   * PERSONA_SCORE[persona]
    p_seniority = WEIGHTS["seniority"] * SENIORITY_SCORE[seniority]
    p_size      = WEIGHTS["size"]      * SIZE_SCORE[size_cat]
    p_industry  = WEIGHTS["industry"]  * INDUSTRY_SCORE[ind_tier]
    sig = 0.0
    if platform in ("Microsoft 365", "Google Workspace", "Both"): sig += 7
    if compliance: sig += 3
    p_signal = min(WEIGHTS["signal"], sig)

    score = round(p_persona + p_seniority + p_size + p_industry + p_signal, 1)
    disqualified = persona == "disqualified"
    if disqualified:
        tier, strategic = "Disqualified", False
    else:
        tier = tier_for(score)
        if size_cat == "below" and tier in ("A", "B"): tier = "C"
        # Strategic = the enterprise (10,001+) motion OR a near-perfect-fit contact.
        # NOT gated on Tier A: a Tier B enterprise account still deserves the
        # AE-led motion, not the mid-market sequence. These are pulled OUT of the
        # automated sequence and handed to an AE (see routing + email templates).
        strategic = is_strategic(score, size_cat)

    email, email_status = enrich_email(val(row, mapping, "first_name"),
                                       val(row, mapping, "last_name"),
                                       val(row, mapping, "full_name"),
                                       val(row, mapping, "company"))
    return {
        "segment": SEGMENT[persona], "persona": persona, "seniority": seniority,
        "size_band": size_cat, "region": region, "industry_tier": ind_tier,
        "platform_signal": platform, "compliance_signal": "yes" if compliance else "no",
        "enriched_email_guess": email, "email_status": email_status,
        "score_persona": round(p_persona,1), "score_seniority": round(p_seniority,1),
        "score_size": round(p_size,1), "score_industry": round(p_industry,1),
        "score_signal": round(p_signal,1), "fit_score": score, "tier": tier,
        "strategic_account": "yes" if strategic else "no",
        "disqualified_reason": dq_reason or "",
    }

# --------------------------------------------------------------------------- #
# MAIN                                                                         #
# --------------------------------------------------------------------------- #
def find_default_input(here):
    cand = os.path.join(here, "..", "data", "example-contacts.csv")
    if os.path.exists(cand): return cand
    ddir = os.path.join(here, "..", "data")
    if os.path.isdir(ddir):
        csvs = [f for f in os.listdir(ddir) if f.lower().endswith(".csv")]
        if csvs: return os.path.join(ddir, sorted(csvs)[0])
    return cand

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--in",  dest="infile", default=find_default_input(here))
    ap.add_argument("--out", dest="outfile",
                    default=os.path.join(here, "..", "output", "scored_contacts.csv"))
    ap.add_argument("--top", type=int, default=0, help="also print the top N")
    args = ap.parse_args()

    if not os.path.exists(args.infile):
        sys.exit(f"Input not found: {args.infile}")
    with open(args.infile, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit("Input file has no rows.")

    mapping = map_columns(list(rows[0].keys()))
    print("COLUMN MAPPING (auto-detected):")
    for field in ["job_title","company","company_size","industry","location","headline","first_name","last_name","email"]:
        print(f"  {field:13s} <- {mapping.get(field) or '(none, will degrade gracefully)'}")
    if not mapping.get("job_title"):
        print("\nWARNING: no job-title column found. Persona scoring will be weak.\n")

    for r in rows:
        r.update(score_row(r, mapping))
    rows.sort(key=lambda r: (r["tier"] == "Disqualified", -r["fit_score"]))
    for i, r in enumerate(rows, 1): r["rank"] = i

    os.makedirs(os.path.dirname(os.path.abspath(args.outfile)), exist_ok=True)
    with open(args.outfile, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    n = len(rows)
    tiers = Counter(r["tier"] for r in rows)
    print(f"\nScored {n} contacts -> {os.path.relpath(args.outfile, here)}\n")
    print("TIER DISTRIBUTION")
    for t in ["A","B","C","D","Disqualified"]:
        c = tiers.get(t,0); print(f"  Tier {t:<12} {c:>5}  ({100*c/n:4.1f}%)")
    a_b = sum(1 for r in rows if r["tier"] in ("A","B"))
    strat = sum(1 for r in rows if r["strategic_account"]=="yes")
    print(f"\nAddressable (A+B): {a_b} ({100*a_b/n:.1f}%) | Strategic (all tiers, AE 1:1): {strat}")
    print("\nSEGMENT DISTRIBUTION")
    for seg,c in Counter(r["segment"] for r in rows).most_common():
        print(f"  {seg:<16} {c:>5}")
    dq = Counter(r["disqualified_reason"] for r in rows if r["tier"]=="Disqualified")
    if dq:
        print("\nDISQUALIFIED REASONS")
        for p,c in dq.most_common(): print(f"  {p:<16} {c:>5}")
    if args.top:
        print(f"\nTOP {args.top}:")
        jt = mapping.get("job_title"); co = mapping.get("company")
        for r in rows[:args.top]:
            print(f"  #{r['rank']:<4} {r['fit_score']:>5}  {r['tier']}  "
                  f"{(r.get(jt,'') if jt else '')[:34]:34s} {(r.get(co,'') if co else '')[:22]}")

if __name__ == "__main__":
    main()
