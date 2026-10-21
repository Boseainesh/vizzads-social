# vizzads-social

Scheduled posting for the Vizz Ads Instagram account and Facebook page.

**How it works:** `queue.json` lists each post (UK time, images, caption). Every 30 minutes a GitHub Action posts anything that is due and marked `ready`, then marks it `posted`.

**Settings this needs (Settings → Secrets and variables → Actions):**

- Secret `META_PAGE_TOKEN`: the Facebook Page access token (never commit it).
- Variable `IG_USER_ID`: the Instagram professional account ID.
- Variable `FB_PAGE_ID`: the Facebook Page ID.

**To test:** Actions → Publish social posts → Run workflow, with "Dry run" ticked.

Images must be JPEG. X is posted by hand.
