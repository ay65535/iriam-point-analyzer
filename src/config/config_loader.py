import os
import yaml


def load_config(path: str = "config/settings.yaml") -> dict:
    """
    設定ファイルを読み込み、辞書として返す。
    Args:
        path: 設定ファイルのパス
    Returns:
        設定内容を含む辞書
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"設定ファイルが見つかりません: {path}")
    with open(path, encoding="utf-8") as f:
        settings = yaml.safe_load(f)
    return settings
