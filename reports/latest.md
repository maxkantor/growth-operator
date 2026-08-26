# Daily Growth Report

Generated: 2026-08-26 12:44 UTC

> Public-site evidence only. Revenue, signup, activation, and checkout conclusions require connected analytics.

## Portfolio scorecard

| Product | HTTP | SEO health | Sitemap URLs | Current decision | Today's action |
| --- | ---: | ---: | ---: | --- | --- |
| [AIWorkoutNow](https://aiworkoutnow.com) | 200 | 86/100 | 42 | focus | Improve the primary landing-page CTA and run one tracked offer experiment for qualified visitors. |
| [DoctorAIBolit](https://doctoraibolit.com) | 200 | 86/100 | 49 | maintain | Maintain reliability and collect conversion evidence; do not increase acquisition spend yet. |
| [GetTrainMate](https://gettrainmate.com) | 200 | 86/100 | 74 | validate | Test one narrow customer segment with a specific outcome-focused landing page before adding features. |
| [HybridRace Workouts](https://www.hybridraceworkouts.com) | 200 | 86/100 | 21 | focus | Improve the primary landing-page CTA and run one tracked offer experiment for qualified visitors. |
| [LuckyNumbersLab](https://luckynumberslab.com) | 200 | 86/100 | 236 | focus | Improve the primary landing-page CTA and run one tracked offer experiment for qualified visitors. |
| [JobCompassAI](https://jobcompassai.com) | 200 | 71/100 | 2 | validate | Fix homepage search metadata and canonical URL; verify the change in Search Console. |
| [YouTubeBoosterAI](https://youtubeboosterai.com) | 200 | 71/100 | 40 | validate | Fix homepage search metadata and canonical URL; verify the change in Search Console. |
| [AnxietyChatAI](https://anxietychatai.com) | 200 | 43/100 | 0 | maintain | Fix homepage search metadata and canonical URL; verify the change in Search Console. |
| [LoveBehaviorTranslator](https://lovebehaviortranslator.com) | 200 | 29/100 | 0 | validate | Fix homepage search metadata and canonical URL; verify the change in Search Console. |

## Highest-priority acquisition queue

1. **AIWorkoutNow:** Improve the primary landing-page CTA and run one tracked offer experiment for qualified visitors.
2. **HybridRace Workouts:** Improve the primary landing-page CTA and run one tracked offer experiment for qualified visitors.
3. **LuckyNumbersLab:** Improve the primary landing-page CTA and run one tracked offer experiment for qualified visitors.

## Today's measurable experiments

### HybridRace Workouts — hybrid-guide-cta

- **Funnel:** SEO visitor to activation
- **Hypothesis:** Athletes reading training guides will try the generator when the CTA promises an immediate race-specific workout.
- **Action:** Add a reusable CTA after the first useful section of every training guide: ‘Training for a hybrid race? Generate 3 race-paced workouts free — no credit card.’ Link to /generate with utm_source=training_guides&utm_campaign=guide_activation.
- **Primary metric:** guide_generate_click / guide_view
- **Success target:** >= 5% after 200 guide sessions
- **Guardrail:** Guide engagement time must not fall by more than 10%
- **Duration:** 14 days
- **Cash cost:** $0
- **Stop rule:** Stop or rewrite if CTR is below 2% after 200 sessions

### AIWorkoutNow — workout-hero-activation

- **Funnel:** Landing page to first workout
- **Hypothesis:** Visitors will start more workouts when the hero promises speed and removes signup anxiety.
- **Action:** Test hero copy: ‘Your workout for today—in 30 seconds.’ Supporting line: ‘Choose your goal, equipment, and time. Get 3 personalized workouts free. No signup or credit card.’ Primary CTA: ‘Generate My Free Workout.’ Scroll directly to the generator and tag source=hero.
- **Primary metric:** hero_generate_click / landing_view and workout_generated_success / hero_generate_click
- **Success target:** Hero CTR >= 8%; completion >= 60% after 300 landing views
- **Guardrail:** Bounce rate must not increase by more than 10%
- **Duration:** 14 days
- **Cash cost:** $0
- **Stop rule:** Revert if hero CTR is below baseline after 300 views

### LuckyNumbersLab — lottery-stats-to-generator

- **Funnel:** Organic traffic to product use
- **Hypothesis:** Visitors on statistics pages will use the product when the CTA continues their current analysis rather than promising prediction accuracy.
- **Action:** Add a contextual CTA to Powerball, Mega Millions, hot-number, overdue-number, and best-picks pages: ‘Use this draw history in the generator.’ Preselect the current lottery and link with utm_campaign=stats_to_generator.
- **Primary metric:** stats_generate_click / stats_page_view and numbers_generated
- **Success target:** CTR >= 4% after 500 organic sessions
- **Guardrail:** Keep entertainment-only and no-guarantee language visible
- **Duration:** 14 days
- **Cash cost:** $0
- **Stop rule:** Rewrite if CTR is below 1.5% after 500 sessions


## Failures and missing fundamentals

- **AIWorkoutNow:** h1
- **DoctorAIBolit:** h1
- **GetTrainMate:** h1
- **HybridRace Workouts:** h1
- **LuckyNumbersLab:** h1
- **JobCompassAI:** description, h1
- **YouTubeBoosterAI:** title, description
- **AnxietyChatAI:** title, h1, robots, sitemap
- **LoveBehaviorTranslator:** title, description, h1, robots, sitemap

## Metrics required for revenue decisions

Connect landing_view → primary_cta_click → signup_complete → activation → checkout_start → purchase → repeat_use.
Do not claim customer growth until purchase events are verified against Stripe.
