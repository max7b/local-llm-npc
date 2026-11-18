from typing import TYPE_CHECKING

import pytest
from fastapi.testclient import TestClient

from app.api import talk
from app.main import app

if TYPE_CHECKING:
    from pathlib import Path

    from app.content.characters.character import Character

client = TestClient(app)


@pytest.mark.llamacpp
def test_npc_gives_their_name_properly(default_character, monkeypatch, tmp_path):
    character_name = default_character.name

    def patch_load_character(path: str | Path) -> Character:
        return default_character

    monkeypatch.setattr(talk, "load_character", patch_load_character)
    monkeypatch.setattr(talk, "PATH_STORED_CONVERSATIONS", tmp_path)

    response = client.post(
        "/talk/",
        json={
            "vendor_type": "Blacksmith",
            "query": "What is your name?",
        },
    )

    assert isinstance(response.json(), str)
    assert character_name in response.json()
