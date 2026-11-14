from app.constants.paths import DATA_DIR
from app.content.game_assets.vendor import load_vendor_settings

path_vendor_setting = f"{DATA_DIR}/game_assets/vendor.json"


def test_load_full_json_game_assets_works():
    vendor_setting = load_vendor_settings(path=path_vendor_setting)
    assert vendor_setting.vendor_money_scaling_by_level == 0.1
    assert vendor_setting.sell_price_multiplicator == 0.33
    assert vendor_setting.default_vendor_money == 500
