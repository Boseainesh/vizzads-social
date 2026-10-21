"""Post to a LinkedIn personal profile (Share on LinkedIn, w_member_social).

Environment:
  LINKEDIN_TOKEN      Member access token (GitHub secret). Lasts 60 days, then needs renewing.
  LINKEDIN_ORG_URN    Optional, e.g. urn:li:organization:12345. When set, "@Vizz Ads" in the
                      post text becomes a real tag of the company page.
  LINKEDIN_VERSION    Optional YYYYMM API version. Default: newest accepted, found automatically.
"""
import json
import os
import urllib.error
import urllib.request
from datetime import date

TOKEN = os.environ.get("LINKEDIN_TOKEN", "")
ORG_URN = os.environ.get("LINKEDIN_ORG_URN", "").strip()
MENTION_NAME = "Vizz Ads"
RESERVED = set("|{}@[]()<>#\\*_~")
_version = os.environ.get("LINKEDIN_VERSION", "").strip() or None


def _candidate_versions():
    if _version:
        yield _version
        return
    y, m = date.today().year, date.today().month
    for _ in range(14):
        yield f"{y}{m:02d}"
        m -= 1
        if m == 0:
            y, m = y - 1, 12


def _request(method, url, body=None, raw=None, rest=True, version=None):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode()
    if raw is not None:
        headers["Content-Type"] = "application/octet-stream"
        data = raw
    if rest:
        headers["LinkedIn-Version"] = version
        headers["X-Restli-Protocol-Version"] = "2.0.0"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=120) as r:
        text = r.read().decode() or "{}"
        return r.status, dict(r.headers), json.loads(text) if text.strip().startswith("{") else {}


def rest(method, path, body=None):
    """Call a /rest endpoint, stepping back through API versions until one is accepted."""
    global _version
    last = None
    for v in _candidate_versions():
        try:
            out = _request(method, f"https://api.linkedin.com/rest/{path}", body=body, version=v)
            _version = v
            return out
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")
            if e.code == 426 or "VERSION" in msg.upper():
                last = msg
                continue
            raise RuntimeError(f"LinkedIn {method} {path} failed: {e.code} {msg}") from None
    raise RuntimeError(f"No accepted LinkedIn API version: {last}")


def member_urn():
    try:
        _, _, me = _request("GET", "https://api.linkedin.com/v2/userinfo", rest=False)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"LinkedIn token rejected ({e.code}). It may have expired: renew it.") from None
    return f"urn:li:person:{me['sub']}", me.get("name")


def escape(text):
    """Escape LinkedIn 'little text' reserved characters; turn @Vizz Ads into a page tag."""
    out = "".join("\\" + c if c in RESERVED else c for c in text)
    if ORG_URN:
        out = out.replace("\\@" + MENTION_NAME, f"@[{MENTION_NAME}]({ORG_URN})")
    return out


def upload_image(owner, path):
    _, _, init = rest("POST", "images?action=initializeUpload",
                      {"initializeUploadRequest": {"owner": owner}})
    up_url, image_urn = init["value"]["uploadUrl"], init["value"]["image"]
    with open(path, "rb") as f:
        _request("PUT", up_url, raw=f.read(), rest=False)
    return image_urn


def post(text, image_paths, alt=""):
    owner, _ = member_urn()
    images = [upload_image(owner, p) for p in image_paths]
    body = {
        "author": owner,
        "commentary": escape(text),
        "visibility": "PUBLIC",
        "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [],
                         "thirdPartyDistributionChannels": []},
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    if len(images) == 1:
        body["content"] = {"media": {"id": images[0], "altText": alt[:4086]}}
    elif len(images) > 1:
        body["content"] = {"multiImage": {"images": [{"id": i, "altText": alt[:4086]} for i in images[:20]]}}
    _, headers, _ = rest("POST", "posts", body)
    return headers.get("x-restli-id") or headers.get("X-RestLi-Id") or "posted"


def check():
    urn, name = member_urn()
    print(f"LinkedIn token works for: {name} ({urn})")
    print(f"Page tag: {'on, ' + ORG_URN if ORG_URN else 'off (LINKEDIN_ORG_URN not set)'}")
    print("Reminder: LinkedIn tokens last 60 days from when they were created.")
