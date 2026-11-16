from enum import Enum

from app.constants.paths import DATA_DIR


class VendorType(Enum):
    """Occupations in the GameAssets vendor settings."""

    BLACKSMITH = "Blacksmith"
    CARPENTER = "Carpenter"
    COOK = "Cook"
    FARMER = "Farmer"
    HUNTER = "Hunter"
    JEWLER = "Jewler"
    TAILOR = "Tailor"
    BREEDER = "Breeder"
    WARRIOR = "Warrior"


mapping_vendor_type_to_path_assets = {VendorType.BLACKSMITH: f"{DATA_DIR}/characters/blacksmith.json"}
