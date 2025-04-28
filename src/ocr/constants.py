"""定数データを管理するモジュール"""

import json
from pathlib import Path


def _load_name_table():
    """設定ファイルから名前テーブルを読み込む"""
    config_path = (
        Path(__file__).parent.parent.parent / "config" / "private" / "name_data.json"
    )
    if not config_path.exists():
        raise FileNotFoundError(f"名前データファイルが見つかりません: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["name_table"]


# namae列-name列対応テーブル（設定ファイルから読み込み）
NAME_TABLE = _load_name_table()

# 誤認識パターンの定義
ERROR_PATTERNS = [
    r"\(ののは\)",  # (ののは)
    r"較只仙?",  # 較只, 較只仙
    r"較叶[人公]?",  # 較叶人, 較叶公
    r"較夫人",  # 較夫人
    r"較只",  # 較只 (単独)
    r"圏ふ",  # 圏ふ
    r"言信",  # 言信
    r"刀彩言",  # 刀彩言
    r"基栓",  # 基栓
    r"箇査",  # 箇査
    r"ミ=ゴ",  # ミ=ゴ
    r"ヤヤ多?",  # ヤヤ, ヤヤ多
    r"ヤシ",  # ヤシ
    r"私ののは",  # 私ののは
    r"を$",  # 末尾の「を」
    r"の8$",  # 末尾の「の8」
    r"@潮$",  # 末尾の「@潮」
]
