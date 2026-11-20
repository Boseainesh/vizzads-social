"""Vizz Ads week 7 creatives (1-4 Dec 2026). Two slides each, opposite colours.
First slides: Tue 1 navy, Thu 3 cream, Fri 4 navy (27 Nov was cream-first)."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from vizz_cards import card

R = "/home/claude/vizzads-social/posts/"

# ---- TUE 1 DEC · Build series 6 · Creative Engine (navy first, question close)
p = R + "2026-12-01-creative-engine/01dec-creative-engine-%d.jpg"
card(p % 1, "navy", "WHAT WE BUILT · 06",
     ["AI makes", "the picture."], coral_last="We write the words.",
     body=["Every ad picture starts as a", "checked brief. The words go on",
           "afterwards, in the brand's", "own fonts."],
     closing=["So the words can change", "without a new picture."])
card(p % 2, "cream", "THE CREATIVE ENGINE",
     ["Picture first,"], coral_last="words second.",
     items=["A checked brief per picture", "AI makes it, with no text",
            "Words set in the brand's fonts", "Every word read back"],
     closing=["What slows down your", "new ads the most?"])

# ---- THU 3 DEC · Website rebuilt around the free first step (cream first, free check close)
p = R + "2026-12-03-free-first-step/03dec-free-first-step-%d.jpg"
card(p % 1, "cream", "WHAT'S NEW",
     ["We rebuilt our", "website around"], coral_last="one free first step.",
     head_size=74,
     body=["Before you pay us anything,", "you see where your rivals'",
           "ads are ahead of yours."],
     closing=["Three steps.", "The first one is free."])
card(p % 2, "navy", "START HERE",
     ["Three steps,"], coral_last="free first.",
     items=["Free Competitor Ad Check", "Ad Creative Analysis", "Ad Account Deep Audit"],
     body=["Start outside your account.", "Go inside only when it's worth it."],
     closing=["Start free, in 48 hours:", "vizzads.com/competitor-ad-check"])

# ---- FRI 4 DEC · Inside a Free Competitor Ad Check, made-up brand (navy first, free check close)
p = R + "2026-12-04-inside-the-check/04dec-inside-the-check-%d.jpg"
card(p % 1, "navy", "INSIDE A FREE CHECK",
     ["3 of 3 rivals", "sell Christmas."], coral_last="Our sample brand: 0.",
     body=["A sample check for Oakhollow", "Home, a made-up homeware", "brand, against three rivals."],
     closing=["Here's what else", "it found."])
card(p % 2, "cream", "THE THREE GAPS",
     ["Three gaps,"], coral_last="three tests.",
     items=["No holiday ads at all", "Product on white, not at home", "Free delivery in no ads"],
     body=["Each gap counted from public", "ads, and one test to close it."],
     closing=["Get yours free in 48 hours:", "vizzads.com/competitor-ad-check"])
