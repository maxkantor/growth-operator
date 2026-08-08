# Daily Growth Delivery Operating Plan

## Objective

Produce verified paid-customer growth across Max Kantor's product portfolio through one small, measurable, reversible delivery each day.

Paid customers are a target, not a guarantee. Report revenue only when verified against Stripe or another authoritative transaction source.

## Initial focus products

1. HybridRace Workouts — `maxkantor/GoHyrox`
2. AIWorkoutNow — `maxkantor/AIWorkoutNow`
3. LuckyNumbersLab — `maxkantor/lucky-numbers-lab`

Continue monitoring the rest of the portfolio, but do not split implementation effort across more products until these three have usable funnel evidence.

## Daily incremental-delivery loop

1. Read `reports/latest.md`, `reports/today.json`, open growth issues, open PRs, recent workflow results, and this plan.
2. Resume unfinished work before selecting a new experiment.
3. Select exactly one unimplemented experiment for one product.
4. Confirm the current baseline events and identify the smallest safe code change.
5. Create an `agent/growth-<product>-<experiment>` branch in the product repository.
6. Implement one cohesive change, including analytics events and tests.
7. Run the repository's relevant tests, lint, and build.
8. Open a draft PR with hypothesis, changes, metric, target, guardrail, rollback, and validation results.
9. If all required checks pass and the change is within the auto-deploy boundary, mark the PR ready, merge it, and verify production health.
10. Record commit, PR, deployment, production URL, baseline, and next evaluation date in the daily report and issue.
11. Do not start another product change in the same daily run.

## Auto-deploy boundary

Automatic merge and deployment are allowed only for small, reversible changes to:

- Landing-page copy and CTA placement
- Internal links and UTM parameters
- Existing analytics event instrumentation
- SEO metadata and structured content
- Non-sensitive UI presentation
- Experiment configuration with an immediate rollback path

Do not automatically merge or deploy changes involving:

- Payments, prices, refunds, Stripe configuration, or entitlements
- Authentication, authorization, secrets, IAM, infrastructure, or databases
- Medical or mental-health safety behavior or claims
- Lottery probability, winning, or financial claims
- Bulk email, scraped contacts, unsolicited outreach, or ad spend
- Destructive migrations, data deletion, or broad dependency upgrades

When a selected experiment crosses a boundary, prepare a draft PR or issue and select the next safe implementation on the following run.

## Release gates

Deployment requires:

- Relevant tests, lint, and production build passing
- No secrets in the diff
- No unrelated files
- Existing repository CI passing
- Clear rollback commit or flag
- Production homepage and changed route returning HTTP 2xx/3xx after deployment
- Analytics events retaining non-sensitive parameters only

If any gate fails, do not merge or deploy. Record the blocker and keep the work resumable.

## Experiment rules

Every change must state:

- Customer and funnel hypothesis
- Baseline or “baseline unavailable”
- Primary metric
- Success target
- Guardrail metric
- Minimum sample or duration
- Stop/continue rule
- Rollback method

Never report success from clicks alone when the objective is paid customers. Use verified purchase events as the revenue outcome.

## Current experiment order

Rotate one experiment daily across:

1. HybridRace Workouts
2. AIWorkoutNow
3. LuckyNumbersLab

Within each product, complete the oldest unimplemented experiment from `config/playbooks.json`. Do not create duplicate PRs or issues for an experiment already open or deployed.

## Standing constraints

- Zero ad spend until conversion tracking and verified purchase attribution work.
- No invented users, testimonials, revenue, rankings, or conversion results.
- No spam or automated bulk outreach.
- Prefer durable customer learning over content volume.
- Keep changes small enough to review, revert, and attribute.
