"""27 Nov (Black Friday day) — rebuilt 26 Nov from the published images (the week 6 script was lost)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from vizz_cards import card
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "posts", "2026-11-27-black-friday-day")
HS = [int(a) for a in sys.argv[2:4]] if len(sys.argv) > 3 else [78, 84]
p = OUT + "/27nov-black-friday-day-%d.jpg"
card(p % 1, "cream", "BLACK FRIDAY",
     ["It's Black Friday."], coral_last="Check these today.", head_size=HS[0],
     items=["Ads still running?", "Tracking still working?", "Stock still there?"],
     closing=["Five minutes,", "three times a day."])
card(p % 2, "navy", "AND THEN",
     ["Leave the rest"], coral_last="alone.", head_size=HS[1],
     body=["Don't pause your winners.", "Don't launch new ideas today.", "Keep some budget for", "Cyber Monday."],
     closing=["Good luck today."])
