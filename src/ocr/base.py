"""
OCRエンジンの基本インターフェースを定義するモジュール
"""

from abc import ABC, abstractmethod
from typing import List


class OCREngine(ABC):
    """OCRエンジンの基本クラス"""

    @abstractmethod
    def extract_text(self, image_path: str, preprocessed_path: str = None) -> List[str]:
        """
        画像からテキストを抽出する

        Args:
            image_path: 入力画像のパス
            preprocessed_path: 前処理済み画像の保存パス（オプション）

        Returns:
            抽出されたテキスト行のリスト

        Raises:
            RuntimeError: テキスト抽出に失敗した場合
        """
        pass
