"""テキスト処理関連の関数を提供するモジュール"""

from typing import List, TypedDict, Tuple
import json
import re
from pathlib import Path
from fuzzywuzzy import process
from .constants import NAME_TABLE, ERROR_PATTERNS


class NameMapping(TypedDict):
    """名前の英語表記と日本語表記のマッピングを表す型です。

    Attributes:
        english (str): 英語表記の名前
        japanese (str): 日本語表記の名前
    """

    english: str
    japanese: str


class NormalizationRule(TypedDict, total=False):
    """名前の正規化ルールを表す型です。

    Attributes:
        keywords (List[str], optional): 正規化を適用するキーワードのリスト
        pattern (str, optional): 正規化に使用する正規表現パターン
        replacement (str, optional): 正規表現での置換文字列
        normalized_name (str, optional): 正規化後の名前
    """

    keywords: List[str]
    pattern: str
    replacement: str
    normalized_name: str


class SpecialNameMapping(TypedDict):
    """特別な名前のマッピングルールを表す型です。

    Attributes:
        default_empty (NameMapping): 空文字列に対するデフォルトのマッピング
        koguma_polaris_keywords (List[str]): こぐまポラリス判定用のキーワードリスト
        koguma_polaris_mapping (NameMapping): こぐまポラリス用の名前マッピング
    """

    default_empty: NameMapping
    koguma_polaris_keywords: List[str]
    koguma_polaris_mapping: NameMapping


class SensitiveData(TypedDict):
    """設定ファイルから読み込む機密データの構造を表す型です。

    Attributes:
        name_normalization_rules (List[NormalizationRule]): 名前の正規化ルールのリスト
        special_name_mapping (SpecialNameMapping): 特別な名前のマッピングルール
    """

    name_normalization_rules: List[NormalizationRule]
    special_name_mapping: SpecialNameMapping


# sensitive_data.jsonの読み込み
config_dir = Path(__file__).parent.parent.parent / "config" / "private"
config_path = config_dir / "sensitive_data.json"
with open(config_path, encoding="utf-8") as f:
    sensitive_data: SensitiveData = json.load(f)

# name_mapping辞書の作成
name_mapping = {name_jp: name_eng for name_eng, name_jp in NAME_TABLE}

__all__ = ["normalize_text_for_name", "get_name_from_table"]


def normalize_text_for_name(raw_name: str) -> str:
    """名前文字列を正規化する。

    絵文字や特殊文字を可能な限り除去し、空白トリムし、
    全角/半角のゆらぎを統一する。

    Args:
        raw_name: 正規化する名前文字列

    Returns:
        str: 正規化された名前文字列
    """
    # キーワードによる正規化
    # キーワードベースのルールを適用
    for rule in sensitive_data["name_normalization_rules"]:
        keywords = rule.get("keywords")
        if keywords and any(keyword in raw_name for keyword in keywords):
            return str(rule["normalized_name"])

    # 全角スペースを半角に統一
    cleaned = raw_name.replace("　", " ")

    # 絵文字・記号等の除外(広めのUnicode範囲で除外)
    cleaned = re.sub(r"[^\wぁ-んァ-ヶ一-龠々ー～\s]+", "", cleaned)

    # 特定の誤認識パターンを除去
    for pattern in ERROR_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned)

    # 複数の空白を1つに統一
    cleaned = re.sub(r"\s+", " ", cleaned)

    # 明らかな誤認識を修正
    for rule in sensitive_data["name_normalization_rules"]:
        if "pattern" in rule:
            cleaned = re.sub(rule["pattern"], rule["replacement"], cleaned)

    # 全角英数字を半角へ変換
    zen_chars = (
        "０１２３４５６７８９"
        "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
        "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"
    )
    han_chars = "0123456789" "abcdefghijklmnopqrstuvwxyz" "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # 文字列から文字列へのマッピングで変換テーブルを作成
    trans_table = str.maketrans(zen_chars, han_chars)
    cleaned = cleaned.translate(trans_table)

    # 余分な空白を削除
    return cleaned.strip()


def get_name_from_table(namae: str) -> Tuple[str, str]:
    """
    namaeを正規化してテーブルとの一致例を探す。
    一致しなければfuzzywuzzy.process.extractOneで近似名を推測し、該当するものがあれば置換する。

    Args:
        namae: マッピングする名前文字列

    Returns:
        (name列の英語, namae(最終正規化)) のタプル
    """
    # まず正規化
    normed = normalize_text_for_name(namae)

    # 空文字列チェック
    if not normed:
        default = sensitive_data["special_name_mapping"]["default_empty"]
        return default["english"], default["japanese"]

    # 完全一致があればそれを返す
    if normed in name_mapping:
        return name_mapping[normed], normed

    # 特別な変換ルール
    special_mapping = sensitive_data["special_name_mapping"]
    keywords = special_mapping["koguma_polaris_keywords"]
    if any(word in normed for word in keywords):
        mapping = special_mapping["koguma_polaris_mapping"]
        return mapping["english"], mapping["japanese"]

    # fuzzywuzzyで近いものを探す
    candidates = list(name_mapping.keys())
    match_result: Tuple[str, int] | None = process.extractOne(normed, candidates)

    # スコアが60以上の場合のみマッピングを使用
    if match_result and match_result[1] >= 60:
        close_jp = match_result[0]
        if close_jp in name_mapping:
            return name_mapping[close_jp], close_jp

    # 近似候補が全く見つからない場合は元の名前を返す
    return namae, namae
