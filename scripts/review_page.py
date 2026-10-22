"""Build the 'Post approvals' review page from queue.json.

Usage: python3 scripts/review_page.py OUT.html [--days 14]
Shows every post due in the next N days (default 14) that isn't posted yet, with
images (embedded) and the exact text for each platform, plus its approval code.
"""
import base64
import html
import io
import json
import os
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UK = ZoneInfo("Europe/London")
PLATFORM = {"linkedin": "LinkedIn", "instagram": "Instagram", "facebook": "Facebook", "x": "X"}


def thumb(path, w=360):
    im = Image.open(os.path.join(ROOT, path)).convert("RGB")
    im = im.resize((w, int(im.height * w / im.width)))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=78)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def esc(t):
    return html.escape(t).replace("\n", "<br>")


def block(label, text, copy=False, note=""):
    btn = '<button class="copy" type="button">Copy</button>' if copy else ""
    n = f'<p class="note">{esc(note)}</p>' if note else ""
    return (f'<div class="text"><div class="text-head"><span class="label">{label}</span>{btn}</div>'
            f'<p class="body">{esc(text)}</p>{n}</div>')


def card(p):
    when = datetime.strptime(p["when"], "%Y-%m-%d %H:%M")
    status = p.get("status", "awaiting_approval")
    pill = {"awaiting_approval": ("Awaiting approval", "wait"), "approved": ("Approved", "ok"),
            "posted": ("Posted", "done")}.get(status, (status, "wait"))
    auto = [PLATFORM[x] for x in p["platforms"]]
    chips = "".join(f'<span class="chip auto">{a} · auto</span>' for a in auto)
    if p.get("x_text") or p.get("x_thread"):
        chips += '<span class="chip manual">X · you post</span>'
    imgs = "".join(f'<img src="{thumb(i)}" alt="Slide {n}" loading="lazy">'
                   for n, i in enumerate(p["images"], 1))
    strip = f'<div class="strip">{imgs}</div>' if imgs else '<p class="note">Text only, no image.</p>'
    texts = ""
    if "linkedin_text" in p:
        texts += block("LinkedIn · your profile", p["linkedin_text"],
                       note='"@Vizz Ads" becomes a tag of the company page.')
        if p.get("page_reshare"):
            texts += block("Vizz Ads page reshare · you, at midday", p["page_reshare"], copy=True)
    if "caption" in p:
        texts += block("Instagram caption", p["caption"])
        if p.get("facebook_caption"):
            texts += '<p class="note">Facebook gets the same caption without the hashtags.</p>'
    if p.get("x_text"):
        texts += block("X · post by hand", p["x_text"], copy=True,
                       note="Attach slide 1. Put vizzads.com in a reply, not the post.")
    for i, t in enumerate(p.get("x_thread", []), 1):
        texts += block(f"X thread · post {i} of {len(p['x_thread'])}", t, copy=True)
    if p.get("x_note"):
        texts += f'<p class="note">{esc(p["x_note"])}</p>'
    return f"""
<article class="post" id="{p['code']}">
  <header class="post-head">
    <div class="when"><span class="day">{when:%a %-d %b}</span><span class="time">{when:%H:%M}</span></div>
    <div class="meta"><span class="code">{p['code']}</span><span class="pill {pill[1]}">{pill[0]}</span></div>
  </header>
  <div class="chips">{chips}</div>
  {strip}
  <div class="texts">{texts}</div>
</article>"""


def main(out, days=14):
    q = json.load(open(os.path.join(ROOT, "queue.json")))
    now = datetime.now(UK).replace(tzinfo=None)
    until = now + timedelta(days=days)
    posts = [p for p in q["posts"] if p.get("status") != "posted"
             and datetime.strptime(p["when"], "%Y-%m-%d %H:%M") <= until]
    posts.sort(key=lambda p: p["when"])
    waiting = sum(p.get("status") == "awaiting_approval" for p in posts)
    weeks = {}
    for p in posts:
        d = datetime.strptime(p["when"], "%Y-%m-%d %H:%M")
        monday = d - timedelta(days=d.weekday())
        weeks.setdefault(monday, []).append(p)
    body = ""
    for monday, ps in weeks.items():
        body += (f'<section class="week"><h2>Week of {monday:%-d %b}</h2>'
                 + "".join(card(p) for p in ps) + "</section>")
    stamp = datetime.now(UK).strftime("%-d %b %Y, %H:%M")
    page = TEMPLATE.replace("{{BODY}}", body).replace("{{WAITING}}", str(waiting)) \
        .replace("{{TOTAL}}", str(len(posts))).replace("{{STAMP}}", stamp)
    open(out, "w").write(page)
    print(f"wrote {out}: {len(posts)} posts, {waiting} awaiting approval")


TEMPLATE = """<title>Vizz Ads Post Approvals</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap">
<style>
/* Layout: one narrow column of post cards grouped by week, review-queue style. */
:root{
  --navy:#0B132B; --coral:#E1785B; --cream:#F3F0DD;
  --bg:#F7F5EC; --surface:#FFFFFF; --fg:#0B132B; --muted:#5B6278; --line:#E3E0D0;
  --ok:#2F7D4F; --wait:#B4561F; --done:#5B6278;
  --display:"Outfit", "Helvetica Neue", Arial, sans-serif;
  --body:"Outfit", "Helvetica Neue", Arial, sans-serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#0B132B; --surface:#131C38; --fg:#F3F0DD; --muted:#A7ACBE; --line:#253052;
  --ok:#6CC08F; --wait:#F0A07F; --done:#A7ACBE; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0B132B; --surface:#131C38; --fg:#F3F0DD; --muted:#A7ACBE; --line:#253052;
  --ok:#6CC08F; --wait:#F0A07F; --done:#A7ACBE; color-scheme:dark}
body{background:var(--bg);color:var(--fg);font-family:var(--body);font-size:15px;line-height:1.5}
.wrap{max-width:760px;margin:0 auto;padding-block:32px 64px;
  padding-left:max(16px, env(safe-area-inset-left, 0px));padding-right:max(16px, env(safe-area-inset-right, 0px));
  display:grid;gap:32px}
.top h1{font-family:var(--display);font-weight:700;font-size:30px;margin:0;text-wrap:balance}
.top h1 .vizz{color:var(--coral)}
.top p{margin:6px 0 0;color:var(--muted)}
.how{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px 18px;display:grid;gap:6px}
.how strong{font-weight:600}
.how code{font-family:ui-monospace, Menlo, monospace;font-size:13px;background:var(--bg);padding:1px 6px;border-radius:4px}
.count{font-variant-numeric:tabular-nums;color:var(--wait);font-weight:600}
.week{display:grid;gap:16px}
.week h2{font-family:var(--display);font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--coral);margin:0}
.post{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:18px;display:grid;gap:14px;min-width:0}
.post-head{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap}
.when{display:flex;gap:10px;align-items:baseline}
.day{font-family:var(--display);font-weight:700;font-size:20px}
.time{color:var(--muted);font-variant-numeric:tabular-nums}
.meta{display:flex;gap:8px;align-items:center}
.code{font-family:ui-monospace, Menlo, monospace;font-size:13px;font-weight:600;border:1px solid var(--line);padding:2px 8px;border-radius:6px}
.pill{font-size:12px;font-weight:600;padding:3px 10px;border-radius:999px;border:1px solid currentColor}
.pill.wait{color:var(--wait)} .pill.ok{color:var(--ok)} .pill.done{color:var(--done)}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font-size:12px;padding:2px 9px;border-radius:999px;background:var(--bg);color:var(--muted)}
.chip.manual{color:var(--coral);font-weight:600}
.strip{display:flex;gap:8px;overflow-x:auto;padding-bottom:4px}
.strip img{width:150px;flex:0 0 auto;border-radius:4px;border:1px solid var(--line);aspect-ratio:4/5;object-fit:cover}
.texts{display:grid;gap:12px;min-width:0}
.text{border-top:1px solid var(--line);padding-top:10px;min-width:0}
.text-head{display:flex;justify-content:space-between;align-items:center;gap:8px}
.label{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:600}
.body{margin:6px 0 0;max-width:65ch;overflow-wrap:anywhere}
.note{margin:4px 0 0;font-size:13px;color:var(--muted)}
.copy{font:inherit;font-size:12px;font-weight:600;color:var(--fg);background:transparent;border:1px solid var(--line);border-radius:6px;padding:3px 10px;cursor:pointer}
.copy:hover{border-color:var(--coral)} .copy:focus-visible{outline:2px solid var(--coral);outline-offset:2px}
.stamp{font-size:12px;color:var(--muted)}
</style>
<div class="wrap">
  <div class="top">
    <h1><span class="vizz">Vizz</span>Ads post approvals</h1>
    <p><span class="count">{{WAITING}}</span> of {{TOTAL}} posts in the next two weeks are waiting for your approval.</p>
  </div>
  <div class="how">
    <span><strong>Nothing posts until you approve it.</strong> Reply in the chat with:</span>
    <span><code>approve all</code> · <code>approve 22-LI 23-IGFB</code> · or say what to change, e.g. <code>27-IGFB: shorter caption</code></span>
    <span class="stamp">Each code covers that post on every platform shown, including your X copy. Updated {{STAMP}}.</span>
  </div>
  {{BODY}}
</div>
<script>
document.querySelectorAll('.copy').forEach(function(b){
  b.addEventListener('click', function(){
    var t = b.closest('.text').querySelector('.body').innerText;
    var done = function(){ b.textContent = 'Copied'; setTimeout(function(){ b.textContent = 'Copy'; }, 1500); };
    try { navigator.clipboard.writeText(t).then(done, function(){ sel(b); }); } catch(e){ sel(b); }
  });
});
function sel(b){ var r=document.createRange(); r.selectNodeContents(b.closest('.text').querySelector('.body'));
  var s=window.getSelection(); s.removeAllRanges(); s.addRange(r); b.textContent='Selected'; }
</script>
"""

if __name__ == "__main__":
    out = sys.argv[1]
    days = int(sys.argv[sys.argv.index("--days") + 1]) if "--days" in sys.argv else 14
    main(out, days)
