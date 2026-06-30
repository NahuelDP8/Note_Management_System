from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.schemas.note_schema import NoteCreate
from app.services.notes_service import NotesService


class FakeNotesRepository:
    def __init__(self, note=None):
        self.note = note
        self.created_payload = None
        self.updated_payload = None

    def get_by_id_and_user(self, db, note_id, user_id):
        return self.note

    def create(self, db, title, content, user_id, categories):
        self.created_payload = {
            "title": title,
            "content": content,
            "user_id": user_id,
            "categories": categories,
        }
        return SimpleNamespace(id=1, **self.created_payload)

    def update(self, db, *, note, **values):
        self.updated_payload = values
        for key, value in values.items():
            if value is not None:
                setattr(note, key, value)
        return note


class FakeCategoryRepository:
    def __init__(self, categories):
        self.categories = categories

    def get_by_id(self, db, category_id):
        return self.categories.get(category_id)

    def get_visible_by_id(self, db, category_id, user_id):
        category = self.categories.get(category_id)
        if not category:
            return None

        category_user_id = getattr(category, "user_id", None)
        if category_user_id is None or category_user_id == user_id:
            return category

        return None


def build_service(note=None, categories=None):
    service = NotesService()
    service.repo = FakeNotesRepository(note=note)
    service.category_repo = FakeCategoryRepository(categories or {})
    return service


def test_create_note_attaches_existing_categories():
    category = SimpleNamespace(id=1, name="work", user_id=None)
    service = build_service(categories={1: category})

    note = service.create_note(
        db=None,
        user_id=10,
        data=NoteCreate(
            title="Architecture notes",
            content="Keep it simple",
            category_ids=[1],
        ),
    )

    assert note.title == "Architecture notes"
    assert service.repo.created_payload["user_id"] == 10
    assert service.repo.created_payload["categories"] == [category]


def test_create_note_rejects_missing_category():
    service = build_service(categories={})

    with pytest.raises(HTTPException) as exc:
        service.create_note(
            db=None,
            user_id=10,
            data=NoteCreate(title="Missing category", category_ids=[99]),
        )

    assert exc.value.status_code == 404


def test_create_note_rejects_category_from_another_user():
    category = SimpleNamespace(id=1, name="private", user_id=99)
    service = build_service(categories={1: category})

    with pytest.raises(HTTPException) as exc:
        service.create_note(
            db=None,
            user_id=10,
            data=NoteCreate(title="Wrong category", category_ids=[1]),
        )

    assert exc.value.status_code == 404


def test_archive_note_rejects_note_from_another_user():
    service = build_service(note=None)

    with pytest.raises(HTTPException) as exc:
        service.archive_note(db=None, note_id=1, user_id=10)

    assert exc.value.status_code == 404


def test_archive_note_sets_archived_flag():
    note = SimpleNamespace(id=1, is_archived=False)
    service = build_service(note=note)

    archived = service.archive_note(db=None, note_id=1, user_id=10)

    assert archived.is_archived is True
    assert service.repo.updated_payload["is_archived"] is True
