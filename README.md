# Growth Operator

Automated, evidence-first growth monitoring for Max Kantor's product portfolio.

## What it does

- Checks every configured production site daily.
- Verifies HTTP health, titles, descriptions, canonical tags, headings, robots.txt, and sitemaps.
- Produces a portfolio scorecard and one prioritized acquisition action per product.
- Commits the latest report to `reports/latest.md`.
- Opens a GitHub issue when a production site is unavailable.
- Detects new Max Kantor Cooking uploads and new genuine viewer comments.
- Produces bilingual pinned-comment, Community-post, social-share, Short-hook, and creator-reply drafts in `reports/youtube-latest.md`.
- Maintains one bilingual draft per existing and future video in `reports/youtube-comment-drafts.json`, preserving `draft`, `reviewed`, or `posted` status.

This first version is deliberately read-only toward production systems. It does not spend money, send bulk outreach, invent customer evidence, or deploy changes to product repositories.

## Run locally

```bash
python3 src/growth_operator.py
YOUTUBE_API_KEY=your_read_only_key python3 src/youtube_operator.py
python3 -m unittest discover -s tests
```

## Run automatically

The `Daily Growth Operator` workflow runs daily and can also be launched from the Actions tab with **Run workflow**.

Add a repository secret named `YOUTUBE_API_KEY` to enable read-only YouTube Data API monitoring. Restrict the Google Cloud key to the YouTube Data API and never commit it. The workflow creates drafts and recommendations only; it does not post comments, add likes, create views, subscribe, or switch accounts.

## Next integrations

Add these only as encrypted GitHub Actions secrets or federated credentials—never commit them:

- GA4 service-account access
- Google Search Console access
- Stripe restricted read key
- PostHog or Mixpanel read key
- Optional LLM API key for richer experiment generation

Production writes should use separate least-privilege credentials, allowlisted repositories, tests, and rollback rules.
