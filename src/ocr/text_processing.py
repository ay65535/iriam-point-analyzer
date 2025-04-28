"""テキスト処理関連の関数を提供するモジュール"""

import re
from fuzzywuzzy import process
from .constants import NAME_TABLE, ERROR_PATTERNS

# name_mapping辞書の作成
name_mapping = {name_jp: name_eng for name_eng, name_jp in NAME_TABLE}

__all__ = ["normalize_text_for_name", "get_name_from_table"]


def normalize_text_for_name(raw_name: str) -> str:
    """
    名前文字列を正規化：絵文字や特殊文字を可能な限り除去し、空白トリムし、
    全角/半角のゆらぎを統一する

    Args:
        raw_name: 正規化する名前文字列

    Returns:
        正規化された名前文字列
    """
    # 絵文字・記号等の除外(広めのUnicode範囲で除外)
    cleaned = re.sub(r"[^\wぁ-んァ-ヶ一-龠々ー～\s]+", "", raw_name)

    # 特定の誤認識パターンを除去
    for pattern in ERROR_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned)

    # 全角英数字を半角へ変換
    zen_chars = (
        "０１２３４５６７８９"
        "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
        "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"
    )
    han_chars = (
        "0123456789"
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )

    # 文字列から文字列へのマッピングで変換テーブルを作成
    trans_table = str.maketrans(zen_chars, han_chars)
    cleaned = cleaned.translate(trans_table)

    # 余分な空白を削除
    return cleaned.strip()


def get_name_from_table(namae: str) -> tuple[str, str]:
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

    # 完全一致があればそれを返す
    if normed in name_mapping:
        return name_mapping[normed], normed

    # fuzzywuzzyで近いものを探す
    candidates = list(name_mapping.keys())
    match_result: tuple[str, int] | None = process.extractOne(
        normed, candidates
    )
    if match_result and match_result[1] >= 70:
        close_jp = match_result[0]
        return name_mapping[close_jp], close_jp

    # 近似候補が全く見つからない場合は元の名前を返す(マッピングなし)
    return normed, normed
