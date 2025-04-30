"""定数データを管理するモジュール"""

import json
from pathlib import Path


def _load_name_table():
    """設定ファイルから名前テーブルを読み込む"""
    base_path = Path(__file__).parent.parent.parent
    config_dir = base_path / "config" / "private"
    config_path = config_dir / "name_data.json"
    if not config_path.exists():
        err_msg = f"名前データファイルが見つかりません: {config_path}"
        raise FileNotFoundError(err_msg)

    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 名前テーブルを返す
    return data["name_table"]


def _load_error_patterns():
    """設定ファイルから誤認識パターンを読み込む"""
    base_path = Path(__file__).parent.parent.parent
    config_dir = base_path / "config" / "private"
    config_path = config_dir / "error_patterns.json"
    if not config_path.exists():
        err_msg = f"誤認識パターンファイルが見つかりません: {config_path}"
        raise FileNotFoundError(err_msg)

    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 誤認識パターンを返す
    return data["error_patterns"]


# namae列-name列対応テーブル（設定ファイルから読み込み）
NAME_TABLE = _load_name_table()

# 誤認識パターンの定義（設定ファイルから読み込み）
ERROR_PATTERNS = _load_error_patterns()
