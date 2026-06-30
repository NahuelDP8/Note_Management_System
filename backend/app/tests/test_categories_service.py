from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.schemas.category_schema import CategoryCreate
from app.services.categories_service import CategoriesService


class FakeCategoryRepository:
    def __init__(self, categories=None, existing=None):
        self.categories = categories or []
        self.existing = existing
        self.created_payload = None

    def get_all_visible(self, db, user_id):
        return self.categories

    def get_visible_by_name(self, db, name, user_id):
        return self.existing

    def create(self, db, name, user_id=None):
        self.created_payload = {"name": name, "user_id": user_id}
        return SimpleNamespace(id=1, name=name, user_id=user_id)


def build_service(repo):
    service = CategoriesService()
    service.repo = repo
    return service


def test_create_category_rejects_existing_visible_name():
    repo = FakeCategoryRepository(
        existing=SimpleNamespace(id=1, name="Trabajo", user_id=None)
    )
    service = build_service(repo)

    with pytest.raises(HTTPException) as exc:
        service.create_category(
            db=None,
            user_id=10,
            data=CategoryCreate(name="trabajo"),
        )

    assert exc.value.status_code == 409


def test_create_category_assigns_current_user():
    repo = FakeCategoryRepository()
    service = build_service(repo)

    category = service.create_category(
        db=None,
        user_id=10,
        data=CategoryCreate(name="  Proyecto   Nuevo  "),
    )

    assert category.name == "Proyecto Nuevo"
    assert repo.created_payload == {
        "name": "Proyecto Nuevo",
        "user_id": 10,
    }


def test_list_categories_removes_duplicate_names_preferring_global():
    global_category = SimpleNamespace(id=1, name="Trabajo", user_id=None)
    user_category = SimpleNamespace(id=2, name="trabajo", user_id=10)
    repo = FakeCategoryRepository(categories=[user_category, global_category])
    service = build_service(repo)

    categories = service.list_categories(db=None, user_id=10)

    assert categories == [global_category]
