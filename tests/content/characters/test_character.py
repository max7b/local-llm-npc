from app.constants.paths import DATA_DIR
from app.content.characters.character import load_character
from app.content.game_assets.vendor import VendorType

path_character_blacksmith = f"{DATA_DIR}/characters/blacksmith.json"


def test_load_json_blacksmith_character_works():
    character = load_character(path=path_character_blacksmith)
    assert character.name == "Dammon"
    assert character.occupation == VendorType.BLACKSMITH
