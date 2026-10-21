# vizzads-social

Scheduled posting for the Vizz Ads Instagram account, Facebook page and Ainesh's LinkedIn profile.

**How it works:** `queue.json` lists each post (UK time, images, caption). Every 30 minutes a GitHub Action posts anything that is due and marked `ready`, then marks it `posted`.

**Settings this needs (Settings → Secrets and variables → Actions):**

- Secret `META_PAGE_TOKEN`: the Facebook Page access token (never commit it).
- Secret `LINKEDIN_TOKEN`: LinkedIn member token for Ainesh's profile. **Expires every 60 days**: generate a new one in the LinkedIn developer portal (app "Vizz Ads Social Publisher" → Auth → OAuth 2.0 tools) and replace the secret.

The Instagram account ID and Facebook Page ID are set in the workflow file (they are not secret).

**To test:** Actions → Publish social posts → Run workflow, with "Dry run" ticked.

LinkedIn posts need a `linkedin_text` field in the queue entry (write "@Vizz Ads" to tag the page) and `linkedin` in `platforms`; `linkedin_images` optionally overrides the images.

Images must be JPEG. X is posted by hand.
