"""Tests for the canvas integration."""
from datetime import UTC, datetime, timedelta

from homeassistant.components.instructure.canvas_api import ISO_DATETIME_FORMAT

# Save data
ANNOUNCEMENTS_KEY: str = "announcements"
ASSIGNMENTS_KEY: str = "assignments"
CONVERSATIONS_KEY: str = "conversations"
GRADES_KEY: str = "grades"
QUICK_LINKS_KEY: str = "quick_links"
ANNOUNCEMENT_ENTITY_CONSTANT = 1
ASSIGNMENT_ENTITY_CONSTANT = 2
CONVERSATION_ENTITY_CONSTANT = 3
GRADES_ENTITY_CONSTANT = 4

MOCK_ASSIGNMENTS = {
    "assignment-1": {
        "id": 1,
        "name": "Test Assignment",
        "due_at": "2023-12-07T10:00:00Z",
        "html_url": "https://canvas.example.com/assignments/1",
    }
}

MOCK_TWO_ASSIGNMENTS = {
    "assignment-1": {
        "id": 1,
        "name": "Test Assignment 1",
        "due_at": (datetime.now(UTC) + timedelta(days=5)).strftime(ISO_DATETIME_FORMAT),
        "html_url": "https://canvas.example.com/assignments/1",
    },
    "assignment-2": {
        "id": 2,
        "name": "Test Assignment 2",
        "due_at": (datetime.now(UTC) + timedelta(days=16)).strftime(
            ISO_DATETIME_FORMAT
        ),
        "html_url": "https://canvas.example.com/assignments/2",
    },
}
MOCK_ANNOUNCEMENTS = {
    "announcement-1": {
        "id": 1,
        "title": "Test Announcement",
        "read_state": "unread",
        "html_url": "https://canvas.example.com/announcements/1",
        "posted_at": "2023-12-01T09:00:00Z",
    }
}
MOCK_CONVERSATIONS = {
    "conversation-1": {
        "id": 1,
        "subject": "Test Conversation",
        "workflow_state": "unread",
        "context_name": "Test Course",
        "participants": [{"name": "Test Sender"}],
        "last_message": "This is a test message.",
        "last_message_at": "2023-12-05T15:30:00Z",
    }
}
MOCK_GRADES = {
    "grade-1": {
        "id": 1,
        "assignment_id": "assignment-1",
        "grade": "A",
        "score": 95,
        "submission_type": "online_text_entry",
    }
}

COURSES = {
    "id": 470664,
    "sis_course_id": None,
    "uuid": "XkZmHn8JQWp9sLxPZDv4AeTzYHwV4RmFJQa2bXc6",
    "integration_id": None,
    "sis_import_id": 45,
    "name": "Advanced Python Programming",
    "course_code": "PYTHONADV01",
    "original_name": "Advanced-Python-Programming-2023",
    "workflow_state": "available",
    "account_id": 91260,
    "root_account_id": 91260,
    "enrollment_term_id": 45,
    "grading_periods": None,
    "grading_standard_id": 35,
    "grade_passback_setting": "nightly_sync",
    "created_at": "2023-01-15T00:00:00-06:00",
    "start_at": "2023-02-01T00:00:00-06:00",
    "end_at": "2023-05-01T00:00:00-06:00",
    "locale": "en",
    "enrollments": None,
    "total_students": 45,
    "calendar": None,
    "default_view": "feed",
    "syllabus_body": "<p>Advanced topics in Python programming</p>",
    "needs_grading_count": 10,
    "term": None,
    "course_progress": None,
    "apply_assignment_group_weights": True,
    "permissions": {"create_discussion_topic": True, "create_announcement": True},
    "is_public": True,
    "is_public_to_auth_users": False,
    "public_syllabus": True,
    "public_syllabus_to_auth": False,
    "public_description": "Dive deep into advanced Python concepts and libraries.",
    "storage_quota_mb": 10,
    "storage_quota_used_mb": 3,
    "hide_final_grades": False,
    "license": "Creative Commons",
    "allow_student_assignment_edits": True,
    "allow_wiki_comments": True,
    "allow_student_forum_attachments": True,
    "open_enrollment": True,
    "self_enrollment": True,
    "restrict_enrollments_to_course_dates": True,
    "course_format": "online",
    "access_restricted_by_date": False,
    "time_zone": "Europe/Stockholm",
    "blueprint": False,
    "blueprint_restrictions": {
        "content": False,
        "points": False,
        "due_dates": True,
        "availability_dates": True,
    },
    "blueprint_restrictions_by_object_type": {
        "assignment": {"content": False, "points": False},
        "wiki_page": {"content": False},
    },
    "template": False,
}

ASSIGNMENT = {
    "id": 4,
    "name": "some assignment",
    "description": "<p>Do the following:</p>...",
    "created_at": "2012-07-01T23:59:00-06:00",
    "updated_at": "2012-07-01T23:59:00-06:00",
    "due_at": "2024-07-01T23:59:00-06:00",
    "lock_at": "2012-07-01T23:59:00-06:00",
    "unlock_at": "2012-07-01T23:59:00-06:00",
    "has_overrides": True,
    "all_dates": None,
    "course_id": 123,
    "html_url": "https://...",
    "submissions_download_url": "https://example.com/courses/:course_id/assignments/:id/submissions?zip=1",
    "assignment_group_id": 2,
    "due_date_required": True,
    "allowed_extensions": ["docx", "ppt"],
    "max_name_length": 15,
    "turnitin_enabled": True,
    "vericite_enabled": True,
    "turnitin_settings": None,
    "grade_group_students_individually": False,
    "external_tool_tag_attributes": None,
    "peer_reviews": False,
    "automatic_peer_reviews": False,
    "peer_review_count": 0,
    "peer_reviews_assign_at": "2012-07-01T23:59:00-06:00",
    "intra_group_peer_reviews": False,
    "group_category_id": 1,
    "needs_grading_count": 17,
    "needs_grading_count_by_section": [
        {"section_id": "123456", "needs_grading_count": 5},
        {"section_id": "654321", "needs_grading_count": 0},
    ],
    "position": 1,
    "post_to_sis": True,
    "integration_id": "12341234",
    "integration_data": {"5678": "0954"},
    "points_possible": 12.0,
    "submission_types": ["online_text_entry"],
    "has_submitted_submissions": True,
    "grading_type": "points",
    "grading_standard_id": None,
    "published": True,
    "unpublishable": False,
    "only_visible_to_overrides": False,
    "locked_for_user": False,
    "lock_info": None,
    "lock_explanation": "This assignment is locked until September 1 at 12:00am",
    "quiz_id": 620,
    "anonymous_submissions": False,
    "discussion_topic": None,
    "freeze_on_copy": False,
    "frozen": False,
    "frozen_attributes": ["title"],
    "submission": None,
    "use_rubric_for_grading": True,
    "rubric_settings": {"points_possible": "12"},
    "rubric": None,
    "assignment_visibility": [137, 381, 572],
    "overrides": None,
    "omit_from_final_grade": True,
    "hide_in_gradebook": True,
    "moderated_grading": True,
    "grader_count": 3,
    "final_grader_id": 3,
    "grader_comments_visible_to_graders": True,
    "graders_anonymous_to_graders": True,
    "grader_names_visible_to_final_grader": True,
    "anonymous_grading": True,
    "allowed_attempts": 2,
    "post_manually": True,
    "score_statistics": None,
    "can_submit": True,
    "ab_guid": ["ABCD", "EFGH"],
    "annotatable_attachment_id": None,
    "anonymize_students": False,
    "require_lockdown_browser": False,
    "important_dates": False,
    "muted": False,
    "anonymous_peer_reviews": False,
    "anonymous_instructor_annotations": False,
    "graded_submissions_exist": False,
    "is_quiz_assignment": False,
    "in_closed_grading_period": False,
    "can_duplicate": False,
    "original_course_id": 4,
    "original_assignment_id": 4,
    "original_lti_resource_link_id": 4,
    "original_assignment_name": "some assignment",
    "original_quiz_id": 4,
    "workflow_state": "unpublished",
}
