# Daily Growth Report

Generated: 2026-08-15 12:31 UTC

> Public-site evidence only. Revenue, signup, activation, and checkout conclusions require connected analytics.

## Portfolio scorecard

| Product | HTTP | SEO health | Sitemap URLs | Current decision | Today's action |
| --- | ---: | ---: | ---: | --- | --- |
| [AIWorkoutNow](https://aiworkoutnow.com) | 200 | 86/100 | 42 | focus | Improve the primary landing-page CTA and run one tracked offer experiment for qualified visitors. |
| [DoctorAIBolit](https://doctoraibolit.com) | 200 | 86/100 | 49 | maintain | Maintain reliability and collect conversion evidence; do not increase acquisition spend yet. |
| [GetTrainMate](https://gettrainmate.com) | 200 | 86/100 | 65 | validate | Test one narrow customer segment with a specific outcome-focused landing page before adding features. |
| [HybridRace Workouts](https://www.hybridraceworkouts.com) | 200 | 86/100 | 21 | focus | Improve the primary landing-page CTA and run one tracked offer experiment for qualified visitors. |
| [JobCompassAI](https://jobcompassai.com) | 200 | 86/100 | 96 | validate | Test one narrow customer segment with a specific outcome-focused landing page before adding features. |
| [LuckyNumbersLab](https://luckynumberslab.com) | 200 | 86/100 | 234 | focus | Improve the primary landing-page CTA and run one tracked offer experiment for qualified visitors. |
| [YouTubeBoosterAI](https://youtubeboosterai.com) | 200 | 57/100 | 40 | validate | Fix homepage search metadata and canonical URL; verify the change in Search Console. |
| [AnxietyChatAI](https://anxietychatai.com) | 200 | 43/100 | 0 | maintain | Fix homepage search metadata and canonical URL; verify the change in Search Console. |
| [LoveBehaviorTranslator](https://lovebehaviortranslator.com) | 200 | 29/100 | 0 | validate | Fix homepage search metadata and canonical URL; verify the change in Search Console. |

## Highest-priority acquisition queue

1. **AIWorkoutNow:** Improve the primary landing-page CTA and run one tracked offer experiment for qualified visitors.
2. **HybridRace Workouts:** Improve the primary landing-page CTA and run one tracked offer experiment for qualified visitors.
3. **LuckyNumbersLab:** Improve the primary landing-page CTA and run one tracked offer experiment for qualified visitors.

## Today's measurable experiments

### HybridRace Workouts — hybrid-paywall-offer

- **Funnel:** Paywall to purchase
- **Hypothesis:** A concrete recommended plan will reduce choice friction after free workouts are consumed.
- **Action:** At the workout limit, lead with the Athlete offer: ‘Keep training: 50 race-paced workouts for $5.99 once.’ Keep Unlimited $9.99 as the secondary comparison and show ‘No subscription’ beside both CTAs.
- **Primary metric:** checkout_start / unlock_wall_view
- **Success target:** >= 8% and verified purchase rate >= 2%
- **Guardrail:** Refund/contact complaints must not increase
- **Duration:** 14 days or 300 paywall views
- **Cash cost:** $0
- **Stop rule:** Revert if checkout-start rate is below the existing baseline after 300 views

### AIWorkoutNow — workout-result-upgrade

- **Funnel:** Activation to pricing
- **Hypothesis:** Users who receive a useful first workout are more receptive to a paid plan than cold homepage visitors.
- **Action:** Below the first generated workout, add: ‘Want your next week planned too?’ Show one recommended paid option, its exact one-time price, and a ‘See Plans’ CTA. Track generated_result_upgrade_click with workout type and source.
- **Primary metric:** generated_result_upgrade_click / workout_generated_success
- **Success target:** >= 6% after 200 successful workouts
- **Guardrail:** Workout save/print usage must not decrease
- **Duration:** 14 days
- **Cash cost:** $0
- **Stop rule:** Remove if CTR is below 2% after 200 generated workouts

### LuckyNumbersLab — lottery-upgrade-value

- **Funnel:** Free use to checkout
- **Hypothesis:** Users will pay when credits are framed around saved analysis and convenience, not better odds.
- **Action:** At the free-credit limit, test: ‘Continue your analysis and save your number history.’ Show Starter $3.99 and Popular $9.99, clearly labeled one-time. Do not imply that payment improves winning probability.
- **Primary metric:** checkout_started / credit_limit_view and checkout_completed / checkout_started
- **Success target:** Checkout start >= 7%; completion >= 35%
- **Guardrail:** No increase in gambling-responsibility complaints or misleading-claim feedback
- **Duration:** 14 days or 300 limit views
- **Cash cost:** $0
- **Stop rule:** Revert if verified purchase conversion declines after 300 views


## Failures and missing fundamentals

- **AIWorkoutNow:** h1
- **DoctorAIBolit:** h1
- **GetTrainMate:** h1
- **HybridRace Workouts:** h1
- **JobCompassAI:** h1
- **LuckyNumbersLab:** h1
- **YouTubeBoosterAI:** title, description, canonical
- **AnxietyChatAI:** title, h1, robots, sitemap
- **LoveBehaviorTranslator:** title, description, h1, robots, sitemap

## Metrics required for revenue decisions

Connect landing_view → primary_cta_click → signup_complete → activation → checkout_start → purchase → repeat_use.
Do not claim customer growth until purchase events are verified against Stripe.
