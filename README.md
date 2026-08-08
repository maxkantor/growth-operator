# Growth Operator

Automated, evidence-first growth monitoring for Max Kantor's product portfolio.

## What it does

- Checks every configured production site daily.
- Verifies HTTP health, titles, descriptions, canonical tags, headings, robots.txt, and sitemaps.
- Produces a portfolio scorecard and one prioritized acquisition action per product.
- Commits the latest report to `reports/latest.md`.
- Opens a GitHub issue when a production site is unavailable.

This first version is deliberately read-only toward production systems. It does not spend money, send bulk outreach, invent customer evidence, or deploy changes to product repositories.

## Run locally

```bash
python3 src/growth_operator.py
python3 -m unittest discover -s tests
```

## Run automatically

The `Daily Growth Operator` workflow runs daily and can also be launched from the Actions tab with **Run workflow**.

## Next integrations

Add these only as encrypted GitHub Actions secrets or federated credentials—never commit them:

- GA4 service-account access
- Google Search Console access
- Stripe restricted read key
- PostHog or Mixpanel read key
- Optional LLM API key for richer experiment generation

Production writes should use separate least-privilege credentials, allowlisted repositories, tests, and rollback rules.
