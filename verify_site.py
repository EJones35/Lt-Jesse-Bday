"""Verify EVERY page of the Jesse site against the final rosters.

The 27 Sep miss: crew.html was updated and verified, missions.html was never
looked at, and it was wrong on seven lines. A verifier that only checks the page
you edited cannot catch the page you forgot. So this one walks all four.
"""
import html
import os
import re
import sys

ROOT = r"C:\Users\ethan\Coding\HTML\Me\Lt Jesse Birthday Mission"

# ---- the rosters, exactly as Ethan dictated them on 27 Sep 2026 ----
M1 = [
    ("Captain",            "Lt Jesse"),
    ("Helm",               "Cadet Holly"),
    ("Weapons (Beams)",    "Sub Lt Gathers"),
    ("Weapons (Missiles)", "Lt Raven"),
    ("Science - Navigation", "Sub Lt Gary"),
    ("Radar",              "Lt. Cmdr Sarah 'Walter' Wheels"),
    ("Comms",              "Lt May"),
    ("Power Management",   "Ens Mike M"),
    ("Damage Control",     "Ensign Duco"),
    ("Dock and Drone",     "Coral"),
    ("Shuttle XO",         'Cadet Jones "CadetGPT"'),
    ("Shuttle Helm",       "Lt Ryan"),
    ("Shuttle Generalist", "Lt. Blaze Starburst"),
    ("Shuttle Engineer",   'Lt Cmdr Memes "Mrs Starburst" Starburst'),
]
M2_TAK = [
    ("Captain",           'Lt Jesse "Copycat"'),
    ("First Officer",     'Cadet Jones "CadetGPT"'),
    ("Helm",              "Lt Cmdr Freddie (Beth)"),
    ("Weapons (Beams)",   'Sub Lt Nat "Gathers"'),
    ("Weapons (Missiles)", "Ensign Duco"),
    ("Power Management",  "Lt Casper Bartholin (Chief Engineer)"),
    ("Damage Control",    "Ensign Mike M"),
    ("Drone Operator",    "Coral"),
    ("Navigation",        "Lt May"),
    ("Comms",             "Lt Grim"),
    ("Radar",             "Sub Lt Heather"),
    ("Shuttle Helm",      "Lt Ed Davies"),
    ("Shuttle Generalist", "Lt Blaze Starburst"),
    ("Shuttle Engineer",  'Lt Cmdr Memes "Mrs Starburst" Starburst'),
]

fails, checks = [], 0

def check(label, ok, detail=""):
    global checks
    checks += 1
    if not ok:
        fails.append(f"{label} :: {detail}")

def read(name):
    return open(os.path.join(ROOT, name), encoding="utf-8").read()

def mission_block(src, which):
    # Stop at the next <h2> or at the section close, whichever comes first.
    m = re.search(r"<h2>Mission %s</h2>(.*?)(?=<h2>|</section>)" % which, src, re.S)
    return m.group(1) if m else ""

def field(block, label):
    m = re.search(r"<strong>%s:\s*</strong>([^<]*)" % re.escape(label), block)
    return html.unescape(m.group(1)).strip() if m else None

def section(block, heading):
    # $ anchors the end of the block, so the LAST subsection in a card still
    # resolves instead of failing to find a terminator.
    m = re.search(r"<h3>%s</h3>(.*?)(?=<h3>|$)" % re.escape(heading), block, re.S)
    return m.group(1) if m else ""

# ============================ missions.html ============================
mis = read("missions.html")
b1 = mission_block(mis, "1")
b2 = mission_block(mis, "2")
check("missions.html: Mission 1 block found", bool(b1))
check("missions.html: Mission 2 block found", bool(b2))

c1 = section(b1, "Crew")
c2 = section(b2, "Takanami Crew")
hav = section(b2, "Havock Crew")
check("missions.html: Mission 1 Crew found", bool(c1))
check("missions.html: Mission 2 Takanami Crew found", bool(c2))
check("missions.html: Mission 2 Havock Crew found", bool(hav))

for label, want in M1:
    got = field(c1, label)
    check(f"missions M1 {label}", got == want, f"page has {got!r}, roster says {want!r}")

for label, want in M2_TAK:
    got = field(c2, label)
    check(f"missions M2 Takanami {label}", got == want, f"page has {got!r}, roster says {want!r}")

# The Havock roster is NOT final - Robyn has not posted it. Assert we did not
# invent anything there, and that the two rows which are known stay put.
check("missions Havock Captain still Oz", field(hav, "Captain") == "Commander Oz", field(hav, "Captain"))
check("missions Havock Helm still Holly", field(hav, "Helm") == "Cadet Holly", field(hav, "Helm"))

# ============================ crew.html ============================
cr = read("crew.html")
cards = re.findall(r'<section class="general-card">(.*?)</section>', cr, re.S)

def card_fields(card):
    out = {}
    for m in re.finditer(r"<strong>([^<]+):\s*</strong>([^<]*)", card):
        out[m.group(1).strip()] = html.unescape(m.group(2)).strip()
    return out

def key_for(card):
    f = card_fields(card)
    h = re.search(r"<h2>(.*?)</h2>", card, re.S)
    h2 = html.unescape(re.sub(r"<[^>]+>", "", h.group(1))).strip() if h else ""
    m = re.search(r"Mike\s+([MWF])$", h2)
    if m:
        return "Mike " + m.group(1)
    nm = f.get("Name")
    if nm and nm.startswith("Memes"):
        return "Memes (Mrs Starburst)"
    return nm

people = {}
for c in cards:
    k = key_for(c)
    if k:
        people.setdefault(k, []).append(card_fields(c))

RANK = {"Robyn": "Lieutenant", "Nat": "Sub Lieutenant", "Topher": "Lieutenant",
        "Raven": "Lieutenant", "Ethan": "Cadet", "Holly": "Cadet",
        "Gary": "Sub Lieutenant", "Mike M": "Ensign", "Beth": "Lieutenant Commander",
        "Heather": "Sub Lieutenant", "Sarah": "Lieutenant Commander", "May": "Lieutenant",
        "Duco": "Ensign", "Ed": "Lieutenant", "Blaze": "Lieutenant",
        "Memes (Mrs Starburst)": "Lieutenant Commander", "Casper": "Lieutenant",
        "Ryan": "Lieutenant"}
for person, want in RANK.items():
    got = people.get(person)
    if not got:
        check(f"crew.html {person} present", False, "no card")
        continue
    check(f"crew.html rank {person}", got[0].get("Rank") == want,
          f"page has {got[0].get('Rank')!r}, Ethan says {want!r}")

coral = people.get("Coral", [{}])[0]
check("crew.html Coral rank not invented", coral.get("Rank") == "Not given", coral.get("Rank"))

check("crew.html: 28 crew cards + flight controllers", len(cards) == 29, f"{len(cards)} sections")

# ============================ comments.html ============================
cm = read("comments.html")
for who, want in [("Lt Cmdr Ward", "Lt Cmdr Ward"), ("Lt Grim", "Lt Grim"),
                  ("Sub Lt Smith", "Sub Lt Smith")]:
    check(f"comments.html carries '{want}'", want in cm, "missing")
check("comments.html no stale 'Ensign Grim'", "Ensign Grim" not in cm, "still Ensign Grim")

# ============================ structural ============================
for name, tail in (("index.html", "</html>"), ("crew.html", "</html>"),
                   ("missions.html", "</html>"), ("comments.html", "</html>"),
                   ("js/script.js", ";"), ("css/style.css", "}")):
    s = read(name)
    check(f"{name} closes", s.rstrip().endswith(tail), f"does not end with {tail!r}")
    check(f"{name} no em dash", "\u2014" not in s, "U+2014 present")
    check(f"{name} no BOM", not s.startswith("\ufeff"), "BOM present")

# no [To be decided] left on the Takanami or Mission 1 - those are final
check("missions.html no [To be decided] on M1 crew", "[To be decided]" not in c1, "still present")
check("missions.html no [To be decided] on M2 Takanami", "[To be decided]" not in c2, "still present")

print(f"{checks} checks across 5 files")
if fails:
    print(f"RESULT: {len(fails)} FAILURE(S)")
    for f in fails:
        print("   - " + f)
    sys.exit(1)
print("RESULT: every page matches the final rosters")
