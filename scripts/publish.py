"""Publish due posts from queue.json to Instagram and a Facebook Page via Meta's Graph API,
and to a LinkedIn personal profile (see linkedin.py; queue entries need "linkedin_text").

Runs on a schedule in GitHub Actions. Uses only the Python standard library.

Environment:
  META_PAGE_TOKEN  Page access token (GitHub secret) with instagram_content_publish,
                   instagram_basic, pages_manage_posts, pages_read_engagement.
  IG_USER_ID       Instagram professional account ID.
  FB_PAGE_ID       Facebook Page ID.
  GRAPH_VERSION    Optional, default v23.0.
  RAW_BASE         Public base URL for repo files (raw.githubusercontent.com/...).
  DRY_RUN          "1" to print what would happen without posting.
  ONLY_ID          Optional: post only this queue id, regardless of its time (for tests).
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "queue.json")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
UK = ZoneInfo("Europe/London")
VER = os.environ.get("GRAPH_VERSION", "v23.0")
API = f"https://graph.facebook.com/{VER}"
TOKEN = os.environ.get("META_PAGE_TOKEN", "")
IG = os.environ.get("IG_USER_ID", "")
PAGE = os.environ.get("FB_PAGE_ID", "")
RAW = os.environ.get("RAW_BASE", "").rstrip("/")
DRY = os.environ.get("DRY_RUN") == "1"
ONLY = os.environ.get("ONLY_ID", "").strip()


def call(method, path, **params):
    params["access_token"] = TOKEN
    data = urllib.parse.urlencode(params).encode()
    url = f"{API}/{path}"
    if method == "GET":
        req = urllib.request.Request(url + "?" + data.decode())
    else:
        req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"{method} {path} failed: {e.code} {body}") from None


def wait_ready(container_id):
    for _ in range(30):
        status = call("GET", container_id, fields="status_code").get("status_code")
        if status == "FINISHED":
            return
        if status in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"container {container_id} status {status}")
        time.sleep(5)
    raise RuntimeError(f"container {container_id} not ready in time")


def post_instagram(urls, caption):
    if len(urls) == 1:
        c = call("POST", f"{IG}/media", image_url=urls[0], caption=caption)["id"]
    else:
        kids = []
        for u in urls:
            kid = call("POST", f"{IG}/media", image_url=u, is_carousel_item="true")["id"]
            wait_ready(kid)
            kids.append(kid)
        c = call("POST", f"{IG}/media", media_type="CAROUSEL",
                 children=",".join(kids), caption=caption)["id"]
    wait_ready(c)
    return call("POST", f"{IG}/media_publish", creation_id=c)["id"]


def post_facebook(urls, caption):
    if len(urls) == 1:
        return call("POST", f"{PAGE}/photos", url=urls[0], caption=caption)["id"]
    ids = [call("POST", f"{PAGE}/photos", url=u, published="false")["id"] for u in urls]
    attached = json.dumps([{"media_fbid": i} for i in ids])
    return call("POST", f"{PAGE}/feed", message=caption, attached_media=attached)["id"]


def main():
    with open(QUEUE) as f:
        q = json.load(f)
    now = datetime.now(UK)
    changed, failed = False, False

    for p in q["posts"]:
        if ONLY:
            if p["id"] != ONLY:
                continue
        else:
            if p.get("status") != "ready":
                continue
            due = datetime.strptime(p["when"], "%Y-%m-%d %H:%M").replace(tzinfo=UK)
            if due > now:
                continue

        urls = [f"{RAW}/{img}" for img in p["images"]]
        done = p.setdefault("posted", {})
        print(f"== {p['id']} ({len(urls)} image(s))")

        for platform in p["platforms"]:
            if platform in done:
                print(f"   {platform}: already posted ({done[platform]})")
                continue
            if DRY:
                print(f"   {platform}: DRY RUN, would post {len(urls)} image(s)")
                continue
            try:
                if platform == "instagram":
                    rid = post_instagram(urls, p["caption"])
                elif platform == "facebook":
                    rid = post_facebook(urls, p.get("facebook_caption", p["caption"]))
                elif platform == "linkedin":
                    import linkedin
                    imgs = p.get("linkedin_images", p["images"])
                    paths = [os.path.join(ROOT, i) for i in imgs]
                    rid = linkedin.post(p["linkedin_text"], paths, p.get("alt", ""))
                else:
                    print(f"   {platform}: unknown platform, skipped")
                    continue
                done[platform] = rid
                changed = True
                print(f"   {platform}: posted, id {rid}")
            except Exception as e:  # keep going with the other platform
                failed = True
                print(f"   {platform}: FAILED: {e}")

        if not DRY and all(pl in done for pl in p["platforms"]):
            p["status"] = "posted"
            p["posted_at"] = now.strftime("%Y-%m-%d %H:%M")
            changed = True

    if changed:
        with open(QUEUE, "w") as f:
            json.dump(q, f, indent=2, ensure_ascii=False)
            f.write("\n")
    sys.exit(1 if failed else 0)


def check():
    """Read-only test: confirms the tokens work and says whether they expire. Posts nothing."""
    if os.environ.get("LINKEDIN_TOKEN"):
        import linkedin
        try:
            linkedin.check()
        except Exception as e:
            print(f"LinkedIn check FAILED: {e}")
    else:
        print("LinkedIn: no LINKEDIN_TOKEN secret set yet")
    me = call("GET", "me", fields="id,name")
    print(f"Token belongs to: {me.get('name')} ({me.get('id')})")
    info = call("GET", "debug_token", input_token=TOKEN).get("data", {})
    exp = info.get("expires_at")
    print(f"Token type: {info.get('type')}  valid: {info.get('is_valid')}")
    print("Expires: never" if exp == 0 else f"Expires at (unix): {exp}")
    print(f"Permissions: {', '.join(sorted(info.get('scopes', [])))}")
    ig = call("GET", IG, fields="username")
    print(f"Instagram account reachable: @{ig.get('username')}")
    limit = call("GET", f"{IG}/content_publishing_limit", fields="quota_usage,config")
    print(f"Publishing quota: {limit}")


if __name__ == "__main__":
    if os.environ.get("CHECK") == "1":
        check()
        sys.exit(0)
    for name, val in (("META_PAGE_TOKEN", TOKEN), ("IG_USER_ID", IG), ("FB_PAGE_ID", PAGE), ("RAW_BASE", RAW)):
        if not val and not DRY:
            sys.exit(f"Missing {name}")
    main()
