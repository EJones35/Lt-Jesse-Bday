"""Verify crew.html against the final rosters Ethan gave on 27 Sep 2026.

Parses the rendered DOM facts out of the HTML and asserts each one. This is the
'measure, do not count' rule: an edit that lands in the wrong card still parses,
still renders, and still looks fine - only comparing it to the source rosters
catches that.
"""
import html
import re
import sys

PATH = r"C:\Users\ethan\Coding\HTML\Me\Lt Jesse Birthday Mission\crew.html"
src = open(PATH, encoding="utf-8").read()

CARDS = re.findall(r"<section class=\"general-card\">(.*?)</section>", src, re.S)

def fields(card):
    out = {}
    for m in re.finditer(r"<strong>([^<]+):\s*</strong>([^<]*)", card):
        out[m.group(1).strip()] = html.unescape(m.group(2)).strip()
    h = re.search(r"<h2>(.*?)</h2>", card, re.S)
    out["_h2"] = html.unescape(re.sub(r"<[^>]+>", "", h.group(1))).strip() if h else ""
    out["_img"] = bool(re.search(r"<img\b", card))
    return out

def key_for(f):
    """Identify a card uniquely. The Name field is not unique - three separate
    people are called Mike - so the h2 heading is the reliable key."""
    h2 = f.get("_h2", "")
    m = re.search(r"Mike\s+([MWF])$", h2)
    if m:
        return "Mike " + m.group(1)
    nm = f.get("Name")
    if nm and nm.startswith("Memes"):
        return "Memes (Mrs Starburst)"
    return nm

people = {}
for c in CARDS:
    f = fields(c)
    k = key_for(f)
    if k:
        people.setdefault(k, []).append(f)

# ---- the rosters, exactly as Ethan gave them ----
M1 = {
    "Captain": ("Robyn", "Captain"),
    "Helm": ("Holly", "Helm"),
    "Beams": ("Nat", "Weapons (Beams)"),
    "Missiles": ("Raven", "Weapons (Missiles)"),
    "Navigation": ("Gary", "Navigation"),
    "Radar": ("Sarah", "Radar"),
    "Comms": ("May", "Comms"),
    "Power Management": ("Mike M", "Power Management"),
    "Damage Control": ("Duco", "Damage Control"),
    "Dock and Drone": ("Coral", "Dock and Drone"),
    "Shuttle XO": ("Ethan", "Shuttle XO"),
    "Shuttle Helm": ("Ryan", "Shuttle Helm"),
    "Shuttle Generalist": ("Blaze", "Shuttle Generalist"),
    "Shuttle Engineer": ("Memes (Mrs Starburst)", "Shuttle Engineer"),
}
M2_TAKANAMI = {
    "Captain": ("Robyn", "Captain"),
    "First Officer": ("Ethan", "First Officer"),
    "Helm": ("Beth", "Helm"),
    "Beams": ("Nat", "Weapons (Beams)"),
    "Missiles": ("Duco", "Weapons (Missiles)"),
    "Power Management": ("Casper", "Power Management"),
    "Damage Control": ("Mike M", "Damage Control"),
    "Drone Operator": ("Coral", "Drone Operator"),
    "Navigation": ("May", "Navigation"),
    "Comms": ("Topher", "Comms"),
    "Radar": ("Heather", "Radar"),
    "Shuttle Helm": ("Ed", "Shuttle Helm"),
    "Shuttle Engineer": ("Memes (Mrs Starburst)", "Shuttle Engineer"),
    "Shuttle Generalist": ("Blaze", "Shuttle Generalist"),
}
RANK = {
    "Robyn": "Lieutenant", "Nat": "Sub Lieutenant", "Topher": "Lieutenant",
    "Raven": "Lieutenant", "Ethan": "Cadet", "Holly": "Cadet",
    "Gary": "Sub Lieutenant", "Mike M": "Ensign", "Beth": "Lieutenant Commander",
    "Heather": "Sub Lieutenant", "Sarah": "Lieutenant Commander", "May": "Lieutenant",
    "Duco": "Ensign", "Ed": "Lieutenant", "Blaze": "Lieutenant",
    "Memes (Mrs Starburst)": "Lieutenant Commander", "Casper": "Lieutenant",
    "Ryan": "Lieutenant",
}

fails, checks = [], 0

def check(label, ok, detail=""):
    global checks
    checks += 1
    if not ok:
        fails.append(f"{label} :: {detail}")

# every Mission 1 role must be on the page, on the right person
for role, (person, want) in M1.items():
    got = people.get(person)
    check(f"M1 {role} -> {person} present", bool(got), "no card with that Name")
    if not got:
        continue
    have = got[0].get("Mission 1 Role", "")
    check(f"M1 {person} role", have == want, f"page has {have!r}, roster says {want!r}")

# every Mission 2 Takanami role
for role, (person, want) in M2_TAKANAMI.items():
    got = people.get(person)
    check(f"M2 {role} -> {person} present", bool(got), "no card with that Name")
    if not got:
        continue
    have = got[0].get("Mission 2 Role", "")
    ship = got[0].get("Mission 2 Ship", "")
    check(f"M2 {person} role", have == want, f"page has {have!r}, roster says {want!r}")
    check(f"M2 {person} ship is Takanami", ship == "Takanami", f"page has {ship!r}")

# ranks
for person, want in RANK.items():
    got = people.get(person)
    if not got:
        continue
    have = got[0].get("Rank", "")
    check(f"rank {person}", have == want, f"page has {have!r}, Ethan says {want!r}")

# nothing invented: Coral has no rank in Ethan's list
coral = people.get("Coral", [{}])[0]
check("Coral rank not invented", coral.get("Rank") == "Not given", coral.get("Rank"))

# no [UNKNOWN] on anyone on the FINAL Mission 1 roster. Havock-only crew are
# excluded on purpose: Robyn has not posted that roster, so [UNKNOWN] is the
# correct state for them and changing it would be inventing a fact.
m1_people = {p for p, _ in M1.values()}
for person, cards in people.items():
    if person not in m1_people:
        continue
    for c in cards:
        if c.get("Mission 1 Role") == "[UNKNOWN]":
            check(f"no stale [UNKNOWN] on {person}", False, "still [UNKNOWN]")

# structure intact
check("28 crew cards + flight controllers", len(CARDS) == 29, f"{len(CARDS)} sections")
check("no em dashes", "\u2014" not in src, "U+2014 present")
check("no BOM", not src.startswith("\ufeff"), "BOM present")
check("html closes", src.rstrip().endswith("</html>"), "truncated")

print(f"{checks} checks run on {len(CARDS)} sections / {len(people)} named people")
if fails:
    print(f"RESULT: {len(fails)} FAILURE(S)")
    for f in fails:
        print("   - " + f)
    sys.exit(1)
print("RESULT: crew page matches the final rosters")
