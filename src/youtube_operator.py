#!/usr/bin/env python3
import json
import os
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "youtube.json"
REPORT = ROOT / "reports" / "youtube-latest.md"
STATE = ROOT / "reports" / "youtube-state.json"
DRAFTS = ROOT / "reports" / "youtube-comment-drafts.json"
API_ROOT = "https://www.googleapis.com/youtube/v3"
USER_AGENT = "MaxKantorGrowthOperator/1.0 (+https://github.com/maxkantor/growth-operator)"


def api_get(resource, params, api_key, timeout=15):
    query = urllib.parse.urlencode({**params, "key": api_key})
    request = urllib.request.Request(
        f"{API_ROOT}/{resource}?{query}", headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def load_state(path=STATE):
    if not path.exists():
        return {"known_video_ids": [], "comment_ids": [], "videos": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("known_video_ids", [])
    data.setdefault("comment_ids", [])
    data.setdefault("videos", {})
    return data


def fetch_channel(api_key, channel_id, max_videos=250):
    channel = api_get(
        "channels",
        {"part": "snippet,contentDetails,statistics", "id": channel_id},
        api_key,
    )["items"][0]
    uploads_id = channel["contentDetails"]["relatedPlaylists"]["uploads"]
    ids = []
    page_token = ""
    while len(ids) < max_videos:
        params = {
            "part": "snippet,contentDetails",
            "playlistId": uploads_id,
            "maxResults": min(50, max_videos - len(ids)),
        }
        if page_token:
            params["pageToken"] = page_token
        playlist = api_get("playlistItems", params, api_key)
        ids.extend(item["contentDetails"]["videoId"] for item in playlist.get("items", []))
        page_token = playlist.get("nextPageToken", "")
        if not page_token:
            break
    if not ids:
        return channel, []
    by_id = {}
    for start in range(0, len(ids), 50):
        details = api_get(
            "videos",
            {"part": "snippet,statistics,contentDetails", "id": ",".join(ids[start:start + 50])},
            api_key,
        )
        by_id.update({item["id"]: item for item in details.get("items", [])})
    return channel, [by_id[video_id] for video_id in ids if video_id in by_id]


def fetch_comments(api_key, video_id, max_results=25):
    try:
        payload = api_get(
            "commentThreads",
            {
                "part": "snippet",
                "videoId": video_id,
                "order": "time",
                "textFormat": "plainText",
                "maxResults": max_results,
            },
            api_key,
        )
    except Exception as exc:
        return [], f"{type(exc).__name__}: {exc}"
    comments = []
    for item in payload.get("items", []):
        snippet = item["snippet"]["topLevelComment"]["snippet"]
        comments.append(
            {
                "id": item["snippet"]["topLevelComment"]["id"],
                "author": snippet.get("authorDisplayName", "Viewer"),
                "text": snippet.get("textDisplay", "").strip(),
                "published_at": snippet.get("publishedAt", ""),
                "reply_count": item["snippet"].get("totalReplyCount", 0),
            }
        )
    return comments, ""


def clean_title(title):
    return re.sub(r"\s*\|.*$", "", title).strip()


def draft_package(video):
    title = video["snippet"]["title"]
    topic = clean_title(title)
    url = f"https://youtu.be/{video['id']}"
    return {
        "video_id": video["id"],
        "video_title": title,
        "video_url": url,
        "published_at": video["snippet"].get("publishedAt", ""),
        "status": "draft",
        "pinned_comment_en": (
            f"What would you change or add when making {topic}? "
            "Share your version below—I read every comment."
        ),
        "pinned_comment_ru": (
            f"А как бы вы приготовили {topic}? Что изменили или добавили бы? "
            "Поделитесь своим вариантом в комментариях — я читаю каждый ответ."
        ),
        "community_post_en": (
            f"New recipe: {topic}. Watch the full process and tell me which step "
            f"you would try first: {url}"
        ),
        "community_post_ru": (
            f"Новый рецепт: {topic}. Посмотрите весь процесс и напишите, какой "
            f"этап попробуете первым: {url}"
        ),
        "social_share": f"I just published {topic}. Full recipe: {url}",
        "short_hook": f"Show the final result first, then one decisive technique from {topic}.",
    }


def reply_draft(comment):
    text = comment["text"].lower()
    if "?" in comment["text"]:
        en = "Thanks for the question. I’ll answer with the exact detail after reviewing this step."
        ru = "Спасибо за вопрос. Я уточню этот этап и отвечу с точными деталями."
    elif any(word in text for word in ("thank", "great", "love", "вкус", "спасибо", "класс")):
        en = "Thank you! Which recipe would you like to see next?"
        ru = "Спасибо! Какой рецепт вы хотели бы увидеть следующим?"
    else:
        en = "Thanks for watching and sharing your experience. How do you make this dish at home?"
        ru = "Спасибо за просмотр и ваш опыт! А как вы готовите это блюдо дома?"
    return {"en": en, "ru": ru}


def recommendation(current, previous):
    current_views = int(current.get("viewCount", 0))
    previous_views = int(previous.get("viewCount", 0)) if previous else 0
    delta = current_views - previous_views
    if previous and delta <= 0:
        return "No new public views since the last run; review title/thumbnail fit and distribution before changing metadata."
    comments = int(current.get("commentCount", 0))
    if current_views >= 100 and comments == 0:
        return "Views are arriving without comments; use the topic-specific pinned question and reply quickly to genuine viewers."
    return "Continue collecting public-view and comment data; use YouTube Studio for CTR, retention, impressions, and watch time."


def render(channel, videos, new_video_ids, new_comments, drafts, previous, now, error=""):
    lines = [
        "# YouTube Engagement Drafts",
        "",
        f"Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "> Drafts only. This automation never likes, comments, views, subscribes, or switches accounts.",
        "",
    ]
    if error:
        return "\n".join(lines + ["## Setup required", "", error, ""])
    stats = channel.get("statistics", {})
    lines += [
        "## Channel snapshot",
        "",
        f"- **Channel:** {channel['snippet']['title']}",
        f"- **Subscribers:** {stats.get('subscriberCount', 'hidden')}",
        f"- **Views:** {stats.get('viewCount', 'unknown')}",
        f"- **Videos:** {stats.get('videoCount', 'unknown')}",
        "",
        "## New uploads",
        "",
    ]
    if not new_video_ids:
        lines.append("No new upload detected since the last successful run.")
    for video in videos:
        if video["id"] not in new_video_ids:
            continue
        package = drafts[video["id"]]
        lines += [
            f"### [{video['snippet']['title']}](https://youtu.be/{video['id']})",
            "",
            "**Pinned comment — English**",
            "",
            package["pinned_comment_en"],
            "",
            "**Закреплённый комментарий — Русский**",
            "",
            package["pinned_comment_ru"],
            "",
            "**Community post — English**",
            "",
            package["community_post_en"],
            "",
            "**Пост сообщества — Русский**",
            "",
            package["community_post_ru"],
            "",
            f"**External share:** {package['social_share']}",
            "",
            f"**Short hook:** {package['short_hook']}",
            "",
        ]
    lines += ["", "## New genuine comments and reply drafts", ""]
    if not new_comments:
        lines.append("No new top-level viewer comments detected.")
    for item in new_comments:
        reply = reply_draft(item)
        lines += [
            f"### {item['author']} on [{item['video_title']}](https://youtu.be/{item['video_id']})",
            "",
            f"> {item['text']}",
            "",
            f"- **English draft:** {reply['en']}",
            f"- **Русский черновик:** {reply['ru']}",
            "",
        ]
    lines += ["", "## Public-metric recommendations", ""]
    for video in videos:
        stats = video.get("statistics", {})
        prior = previous.get("videos", {}).get(video["id"], {}).get("statistics", {})
        lines.append(
            f"- **{video['snippet']['title']}** — views {stats.get('viewCount', '0')}, "
            f"likes {stats.get('likeCount', 'hidden')}, comments {stats.get('commentCount', '0')}: "
            f"{recommendation(stats, prior)}"
        )
    lines += [
        "",
        "> YouTube Data API public statistics do not include impressions, CTR, audience retention, or public watch hours. Review those in YouTube Studio or add an authorized YouTube Analytics integration later.",
        "",
    ]
    return "\n".join(lines)


def merge_drafts(videos, existing):
    previous = {item["video_id"]: item for item in existing.get("drafts", [])}
    drafts = []
    for video in videos:
        generated = draft_package(video)
        old = previous.get(video["id"], {})
        generated["status"] = old.get("status", "draft")
        generated["review_notes"] = old.get("review_notes", "")
        drafts.append(generated)
    return {"drafts": drafts}


def run(api_key, config, previous, existing_drafts, now):
    channel, videos = fetch_channel(api_key, config["channel_id"], config["max_videos"])
    known = set(previous["known_video_ids"])
    known_comments = set(previous["comment_ids"])
    first_run = not previous.get("last_run") and not known
    new_video_ids = (
        [videos[0]["id"]] if first_run and videos else
        [video["id"] for video in videos if video["id"] not in known]
    )
    backlog = merge_drafts(videos, existing_drafts)
    drafts = {item["video_id"]: item for item in backlog["drafts"] if item["video_id"] in new_video_ids}
    observed_comment_ids = set(known_comments)
    new_comments = []
    for video in videos[:5]:
        comments, _ = fetch_comments(api_key, video["id"], config["max_comments_per_video"])
        for comment in comments:
            observed_comment_ids.add(comment["id"])
            if not first_run and comment["id"] not in known_comments:
                new_comments.append({**comment, "video_id": video["id"], "video_title": video["snippet"]["title"]})
    state = {
        "last_run": now.isoformat(),
        "known_video_ids": [video["id"] for video in videos],
        "comment_ids": sorted(observed_comment_ids)[-500:],
        "videos": {
            video["id"]: {
                "title": video["snippet"]["title"],
                "published_at": video["snippet"]["publishedAt"],
                "statistics": video.get("statistics", {}),
            }
            for video in videos
        },
    }
    report = render(channel, videos, new_video_ids, new_comments, drafts, previous, now)
    backlog["generated_at"] = now.isoformat()
    return report, state, backlog


def main():
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    previous = load_state()
    existing_drafts = json.loads(DRAFTS.read_text(encoding="utf-8")) if DRAFTS.exists() else {"drafts": []}
    now = datetime.now(timezone.utc)
    api_key = os.environ.get("YOUTUBE_API_KEY", "").strip()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    if not api_key:
        REPORT.write_text(
            render({}, [], [], [], {}, previous, now, "Add the `YOUTUBE_API_KEY` repository secret to enable read-only YouTube monitoring."),
            encoding="utf-8",
        )
        print("YOUTUBE_API_KEY is not configured; wrote setup report.")
        return 0
    report, state, drafts = run(api_key, config, previous, existing_drafts, now)
    REPORT.write_text(report, encoding="utf-8")
    STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    DRAFTS.write_text(json.dumps(drafts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT}, {STATE}, and {DRAFTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
