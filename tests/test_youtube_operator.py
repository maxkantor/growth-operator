import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "youtube_operator.py"
SPEC = importlib.util.spec_from_file_location("youtube_operator", MODULE_PATH)
youtube_operator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(youtube_operator)


class YouTubeOperatorTests(unittest.TestCase):
    def test_draft_package_is_bilingual_and_links_video(self):
        video = {
            "id": "abc123",
            "snippet": {"title": "Chkmeruli | Чкмерули"},
        }
        draft = youtube_operator.draft_package(video)
        self.assertIn("Chkmeruli", draft["pinned_comment_en"])
        self.assertIn("А как", draft["pinned_comment_ru"])
        self.assertIn("https://youtu.be/abc123", draft["community_post_en"])

    def test_reply_draft_treats_question_as_needing_review(self):
        reply = youtube_operator.reply_draft({"text": "Can I use chicken thighs?"})
        self.assertIn("exact detail", reply["en"])
        self.assertIn("точными", reply["ru"])

    def test_recommendation_does_not_claim_private_analytics(self):
        message = youtube_operator.recommendation(
            {"viewCount": "100", "commentCount": "0"},
            {"viewCount": "90", "commentCount": "0"},
        )
        self.assertIn("pinned question", message)

    def test_merge_drafts_preserves_manual_status(self):
        videos = [{"id": "abc123", "snippet": {"title": "Soup", "publishedAt": "2026-01-01"}}]
        existing = {"drafts": [{"video_id": "abc123", "status": "posted", "review_notes": "Used EN"}]}
        merged = youtube_operator.merge_drafts(videos, existing)
        self.assertEqual(merged["drafts"][0]["status"], "posted")
        self.assertEqual(merged["drafts"][0]["review_notes"], "Used EN")


if __name__ == "__main__":
    unittest.main()
