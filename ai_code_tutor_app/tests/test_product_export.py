from __future__ import annotations

import json
import zipfile
from io import BytesIO

from curriculum import LESSONS
from product_export import backup_zip_bytes, certificate_markdown, learning_transcript_markdown, progress_backup_payload, unwrap_progress_import
from progress import default_progress, mark_lesson_complete, record_gym_session
from study_plan import DAILY_PLAN


def test_backup_payload_import_unwraps_progress():
    progress = {"completed_lessons": ["one"]}
    wrapped = progress_backup_payload("Ava", "ava", progress)
    assert unwrap_progress_import(wrapped) == progress
    assert unwrap_progress_import(progress) == progress
    assert unwrap_progress_import({"hello": "world"}) is None


def test_transcript_certificate_and_zip_include_learning_goal():
    progress = default_progress([lesson.id for lesson in LESSONS], profile_name="Ava")
    mark_lesson_complete(progress, LESSONS[0].id)
    record_gym_session(progress, 1, "30 min daily", "Saved", "I learned print and error reading.", lesson_id=LESSONS[0].id)

    transcript = learning_transcript_markdown("Ava", progress, LESSONS, DAILY_PLAN)
    certificate = certificate_markdown("Ava", progress, LESSONS)
    assert "Learning Transcript" in transcript
    assert "Completed lessons" in transcript
    assert "Graduation Certificate" in certificate
    assert "not an accredited credential" in certificate

    zip_bytes = backup_zip_bytes("Ava", "ava", progress, LESSONS, DAILY_PLAN)
    with zipfile.ZipFile(BytesIO(zip_bytes)) as zf:
        names = set(zf.namelist())
        assert {"progress_backup.json", "learning_transcript.md", "graduation_certificate.md", "README.txt"}.issubset(names)
        backup = json.loads(zf.read("progress_backup.json").decode("utf-8"))
        assert backup["kind"] == "private_learning_backup"
        assert backup["progress"]["profile_name"] == "Ava"
