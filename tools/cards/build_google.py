"""Google catch-up posts (off-days: Mon 23, Wed 25, Mon 30 Nov, Wed 2 Dec) and week 7 updates
for Meta and Google (3 and 4 Dec). Report images are the website samples (made-up brands)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from vizz_cards import card, showcase

R = os.path.join(HERE, "..", "..", "posts") + "/"
S = os.path.join(HERE, "samples") + "/"

# ---- MON 23 NOV · Free Competitor Ad Check, now on Google
p = R + "2026-11-23-google-check/23nov-google-check-%d.jpg"
showcase(p % 1, "navy", "NOW ON GOOGLE TOO",
         ["Who's on your own", "name on Google?"], coral_last="We check, free.",
         shot=[S + "competitor-ad-check-google-1-scorecard.jpg", S + "competitor-ad-check-google-2-gaps.jpg"],
         caption="Sample Google check for a made-up brand")
card(p % 2, "cream", "FREE COMPETITOR AD CHECK",
     ["Meta, Google"], coral_last="or both. Free.",
     items=["Every ad Google lists for you", "You vs up to 3 rivals",
            "Searches run 3 times a day", "3 gaps and 3 tests in 48 hours"],
     closing=["No card, no account access:", "vizzads.com/competitor-ad-check"])

# ---- WED 25 NOV · Ad Creative Analysis, Google
p = R + "2026-11-25-google-analysis/25nov-google-analysis-%d.jpg"
showcase(p % 1, "cream", "AD CREATIVE ANALYSIS · GOOGLE",
         ["Every Google ad,"], coral_last="read and counted.",
         shot=S + "hi_aca-1.jpg", crop=(0.04, 0.03, 0.96, 0.62),
         caption="Sample Google analysis for a made-up brand")
card(p % 2, "navy", "WHAT'S IN IT",
     ["Every live ad,"], coral_last="every finding counted.",
     items=["Who's seen on your name", "Your homepage vs your ads",
            "Shopping and Google video ads", "A work list, in order"],
     closing=["Meta, Google or both:", "vizzads.com/ad-creative-analysis"])

# ---- MON 30 NOV · Ad Account Deep Audit, Google
p = R + "2026-11-30-google-deep-audit/30nov-google-deep-audit-%d.jpg"
showcase(p % 1, "navy", "AD ACCOUNT DEEP AUDIT · GOOGLE",
         ["How much of your", "Performance Max is"], coral_last="your own name?",
         shot=S + "hi_da-05.jpg", crop=(0.04, 0.03, 0.96, 0.50),
         caption="Sample Google audit for a made-up brand")
card(p % 2, "cream", "THE GOOGLE DEEP AUDIT",
     ["Each campaign judged"], coral_last="on its own job.",
     items=["Your name and Performance Max", "Category searches and video",
            "A set-up check, red to green", "A 90-day plan and 3 tests"],
     closing=["Read-only access.", "Meta, Google or both."])

# ---- WED 2 DEC · How we know the outside read is right (results of the build)
p = R + "2026-12-02-google-checked/02dec-google-checked-%d.jpg"
card(p % 1, "cream", "HOW WE KNOW IT'S RIGHT",
     ["We checked our", "outside read against"], coral_last="a real account.",
     head_size=74,
     body=["Every launch and stop date we", "read from Google's public data",
           "matched the account to the day."],
     closing=["Then we built it", "into the free check."])
card(p % 2, "navy", "WHAT WE LEARNED",
     ["One search"], coral_last="proves nothing.",
     items=["Dates matched to the day", "Every search run 3 times",
            "Ad blocker off for every check", "Performance Max, seen in public"],
     closing=["Free, on Meta or Google:", "vizzads.com/competitor-ad-check"])

# ---- THU 3 DEC · slide 2 now says Meta, Google or both (cream first unchanged)
p = R + "2026-12-03-free-first-step/03dec-free-first-step-%d.jpg"
card(p % 1, "cream", "WHAT'S NEW",
     ["We rebuilt our", "website around"], coral_last="one free first step.",
     head_size=74,
     body=["Before you pay us anything,", "you see where your rivals' ads",
           "are ahead, on Meta or Google."],
     closing=["Three steps.", "The first one is free."])
card(p % 2, "navy", "START HERE",
     ["Three steps,"], coral_last="free first.",
     items=["Free Competitor Ad Check", "Ad Creative Analysis", "Ad Account Deep Audit"],
     body=["Meta, Google or both.", "Start outside your account."],
     closing=["Start free, in 48 hours:", "vizzads.com/competitor-ad-check"])

# ---- FRI 4 DEC · Inside a free check, Meta and Google (navy first unchanged)
p = R + "2026-12-04-inside-the-check/04dec-inside-the-check-%d.jpg"
showcase(p % 1, "navy", "INSIDE A FREE CHECK",
         ["Meta and Google,"], coral_last="one free check.",
         shot=[S + "competitor-ad-check-both-cover.jpg", S + "competitor-ad-check-google-2-gaps.jpg"],
         caption="Sample check for a made-up brand")
card(p % 2, "cream", "WHAT IT FOUND",
     ["Real brand,"], coral_last="real gaps.",
     items=["Meta: Christmas, 7 of 175", "Meta: delivery, 0 of 175",
            "Google: 7 new ads vs 57+", "Google: 9 video ads vs 26+"],
     body=["A UK homeware brand we tested,", "name withheld."],
     closing=["Get yours free in 48 hours:", "vizzads.com/competitor-ad-check"])
