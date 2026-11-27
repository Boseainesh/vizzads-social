"""Week 8 (8-11 Dec 2026), Meta and Google, green & pink brand colours.
Instagram first slides: Tue 8 light (cream), Thu 10 dark (navy), Fri 11 light (cream)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from vizz_cards import card, showcase

R = os.path.join(HERE, "..", "..", "posts") + "/"
S = os.path.join(HERE, "samples") + "/"

# ---- TUE 8 DEC · How we use AI, and where a person still makes the call (light first, question close)
p = R + "2026-12-08-ai-and-people/08dec-ai-and-people-%d.jpg"
card(p % 1, "cream", "HOW WE USE AI",
     ["AI does the reading."], coral_last="A person makes the call.",
     head_size=72,
     body=["AI reads every live ad and runs", "every search, on Meta and Google.",
           "A person checks each finding", "before anything reaches you."],
     closing=["Fast where it's safe,", "careful where it counts."])
card(p % 2, "navy", "WHO DOES WHAT",
     ["AI reads,"], coral_last="people decide.",
     items=["Every live ad, read", "Every search, run 3 times", "Every report, fact-checked",
            "Every call, made by a person"],
     closing=["Where would you trust AI", "with your ads?"])

# ---- THU 10 DEC · The Ad Creative Analysis, Meta and Google (dark first, Analysis page close)
p = R + "2026-12-10-creative-analysis/10dec-creative-analysis-%d.jpg"
showcase(p % 1, "navy", "AD CREATIVE ANALYSIS",
         ["Every ad you're running,"], coral_last="read and counted.",
         shot=[S + "ad-creative-analysis-1-findings-v4.jpg", S + "ad-creative-analysis-google-1-findings-v3.jpg"],
         caption="Sample Meta and Google reports for a made-up brand")
card(p % 2, "cream", "WHAT YOU GET",
     ["One report per"], coral_last="platform.",
     items=["Every live ad, read and counted", "Your homepage vs your ads",
            "Your rivals, side by side", "A work list, in order"],
     closing=["Meta, Google or both:", "vizzads.com/ad-creative-analysis"])

# ---- FRI 11 DEC · Three gaps we see most often (light first, free check close, boost candidate)
p = R + "2026-12-11-three-gaps/11dec-three-gaps-%d.jpg"
card(p % 1, "cream", "WHAT WE SEE MOST",
     ["3 gaps we find"], coral_last="again and again.",
     items=["Your best claim isn't in your ads", "Rivals on your own name",
            "Too few new ads"],
     body=["On Meta and on Google,", "across the brands we've read."],
     closing=["Each one is", "fixable this week."])
card(p % 2, "navy", "FREE COMPETITOR AD CHECK",
     ["Which one"], coral_last="is yours?",
     body=["We read your live ads next to", "up to three rivals', and send",
           "the three biggest gaps with", "a test to close each one."],
     closing=["Free, in 48 hours:", "vizzads.com/competitor-ad-check"], gradient=True)
