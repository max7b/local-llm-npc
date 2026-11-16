import json
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, ValidationError
from pydantic.alias_generators import to_pascal

from app.core.logger import LOGGING

if TYPE_CHECKING:
    from pathlib import Path


class BaseModelAlias(BaseModel):
    """Base model that reads the PascalCase JSON keys into snake_case fields."""

    model_config = ConfigDict(alias_generator=to_pascal)


class ItemRequirements(BaseModelAlias):
    """Item tags that decide which items a vendor can sell."""

    require_tags: list[str]
    ignore_tags: list[str]


class ExtensionRarityDropChance(BaseModelAlias):
    """Drop chance for each rarity tier, as given in the vendor settings file."""

    legendary: float
    epic: float
    rare: float
    uncommon: float


class VendorRule(BaseModelAlias):
    """Vendor rules for one occupation."""

    item_requirements: ItemRequirements
    item_probability: float
    extension_rarity_to_drop_chance: ExtensionRarityDropChance


class VendorSettings(BaseModelAlias):
    """Root of the GameAssets vendor settings file."""

    default_vendor_money: int
    vendor_money_scaling_by_level: float
    sell_price_multiplicator: float
    vendor_tag_to_item_map: dict[str, VendorRule]
    vendor_to_level_mapping: dict[str, list[str]]


def load_vendor_settings(path: str | Path) -> VendorSettings:
    """Load and validate the GameAssets vendor settings file.

    Args:
        path (str | Path): Path to the vendor settings JSON file.

    Returns:
        VendorSettings: The validated settings.
    """
    with open(path) as vendor_path:
        vendor_settings_json = json.load(vendor_path)

    try:
        vendor_settings = VendorSettings.model_validate(vendor_settings_json)
    except ValidationError as e:
        LOGGING.error(e)
        raise

    return vendor_settings
