#!/usr/bin/env python3
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "sites.json"
REPORT = ROOT / "reports" / "latest.md"
USER_AGENT = "MaxKantorGrowthOperator/1.0 (+https://github.com/maxkantor/growth-operator)"


def fetch(url, timeout=8):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.status, response.geturl(), response.read(2_000_000).decode(charset, "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, url, ""
    except Exception as exc:
        return 0, url, f"ERROR: {type(exc).__name__}: {exc}"


def first_match(pattern, text):
    match = re.search(pattern, text, re.I | re.S)
    if not match:
        return ""
    return html.unescape(re.sub(r"\s+", " ", match.group(1))).strip()


def analyze(site):
    status, final_url, body = fetch(site["url"])
    title = first_match(r"<title[^>]*>(.*?)</title>", body)
    description = first_match(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', body)
    if not description:
        description = first_match(r'<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']description["\']', body)
    canonical = first_match(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']', body)
    h1 = first_match(r"<h1[^>]*>(.*?)</h1>", body)
    robots_status, _, robots = fetch(urljoin(site["url"] + "/", "robots.txt"))
    sitemap_status, _, sitemap = fetch(urljoin(site["url"] + "/", "sitemap.xml"))
    sitemap_urls = len(re.findall(r"<loc>", sitemap, re.I)) if sitemap_status == 200 else 0

    checks = {
        "healthy": 200 <= status < 400,
        "title": 20 <= len(title) <= 65,
        "description": 70 <= len(description) <= 170,
        "canonical": bool(canonical),
        "h1": bool(h1),
        "robots": robots_status == 200 and "user-agent" in robots.lower(),
        "sitemap": sitemap_status == 200 and sitemap_urls > 0,
    }
    score = round(100 * sum(checks.values()) / len(checks))
    missing = [name for name, passed in checks.items() if not passed]
    action = choose_action(site, status, missing, sitemap_urls)
    return {
        **site,
        "status": status,
        "final_url": final_url,
        "title": title,
        "description": description,
        "h1": re.sub(r"<[^>]+>", "", h1),
        "sitemap_urls": sitemap_urls,
        "score": score,
        "missing": missing,
        "action": action,
    }


def choose_action(site, status, missing, sitemap_urls):
    if not 200 <= status < 400:
        return "Restore production availability before sending traffic."
    if "title" in missing or "description" in missing or "canonical" in missing:
        return "Fix homepage search metadata and canonical URL; verify the change in Search Console."
    if sitemap_urls < 10:
        return "Publish one high-intent landing page answering a specific customer problem and add it to the sitemap."
    if site["decision"] == "focus":
        return "Improve the primary landing-page CTA and run one tracked offer experiment for qualified visitors."
    if site["decision"] == "validate":
        return "Test one narrow customer segment with a specific outcome-focused landing page before adding features."
    return "Maintain reliability and collect conversion evidence; do not increase acquisition spend yet."


def render(results):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    ordered = sorted(results, key=lambda item: (item["status"] == 0, -item["score"], item["name"]))
    lines = [
        "# Daily Growth Report",
        "",
        f"Generated: {now}",
        "",
        "> Public-site evidence only. Revenue, signup, activation, and checkout conclusions require connected analytics.",
        "",
        "## Portfolio scorecard",
        "",
        "| Product | HTTP | SEO health | Sitemap URLs | Current decision | Today's action |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for item in ordered:
        lines.append(
            f'| [{item["name"]}]({item["url"]}) | {item["status"] or "DOWN"} | '
            f'{item["score"]}/100 | {item["sitemap_urls"]} | {item["decision"]} | {item["action"]} |'
        )
    focus = [item for item in ordered if item["decision"] == "focus" and 200 <= item["status"] < 400]
    lines += ["", "## Highest-priority acquisition queue", ""]
    for index, item in enumerate(focus[:3], 1):
        lines.append(f'{index}. **{item["name"]}:** {item["action"]}')
    lines += ["", "## Failures and missing fundamentals", ""]
    failures = [item for item in ordered if item["status"] == 0 or item["missing"]]
    if not failures:
        lines.append("No public-site failures detected.")
    for item in failures:
        details = ", ".join(item["missing"]) or "unreachable"
        lines.append(f'- **{item["name"]}:** {details}')
    lines += [
        "",
        "## Metrics required for revenue decisions",
        "",
        "Connect landing_view → primary_cta_click → signup_complete → activation → checkout_start → purchase → repeat_use.",
        "Do not claim customer growth until purchase events are verified against Stripe.",
        "",
    ]
    return "\n".join(lines)


def main():
    sites = json.loads(CONFIG.read_text(encoding="utf-8"))
    results = []
    with ThreadPoolExecutor(max_workers=min(6, len(sites))) as executor:
        futures = {executor.submit(analyze, site): site for site in sites}
        for future in as_completed(futures):
            results.append(future.result())
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(render(results), encoding="utf-8")
    print(f"Wrote {REPORT}")
    if any(item["status"] == 0 or item["status"] >= 500 for item in results):
        print("One or more production sites are unavailable.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
