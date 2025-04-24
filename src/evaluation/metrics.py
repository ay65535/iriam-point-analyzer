"""
OCR結果の評価に関する機能を提供するモジュール
"""

import yaml
from pathlib import Path


class TextEvaluator:
    """テキスト評価を行うクラス"""

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        テキストを正規化（日付フォーマットの統一など）

        Args:
            text: 正規化する文字列

        Returns:
            正規化された文字列
        """
        # 年月日表記を/表記に変換
        text = text.replace("年", "/").replace("月", "/").replace("日", "")
        # 空白を正規化
        text = " ".join(text.split())
        return text

    @staticmethod
    def compare(extracted: list[str], expected: list[str]) -> float:
        """
        抽出されたテキストと期待されるテキストを比較して精度を計算

        Args:
            extracted: 抽出されたテキスト行のリスト
            expected: 期待されるテキスト行のリスト

        Returns:
            一致率（パーセント）
        """
        matched = sum(1 for line in expected if line in extracted)
        accuracy = matched / len(expected) * 100
        return accuracy

    @staticmethod
    def compare_normalized(extracted: list[str], expected: list[str]) -> float:
        """
        正規化したテキストで比較

        Args:
            extracted: 抽出されたテキスト行のリスト
            expected: 期待されるテキスト行のリスト

        Returns:
            正規化後の一致率（パーセント）
        """
        normalized_extracted = [
            TextEvaluator.normalize_text(line) for line in extracted
        ]
        normalized_expected = [TextEvaluator.normalize_text(line) for line in expected]

        matched = 0
        for exp_line in normalized_expected:
            for ext_line in normalized_extracted:
                if exp_line in ext_line or ext_line in exp_line:
                    matched += 1
                    break

        accuracy = matched / len(normalized_expected) * 100
        return accuracy

    @staticmethod
    def load_expected() -> list[str]:
        """
        期待される正解データを返す

        Returns:
            期待されるテキスト行のリスト

        Raises:
            FileNotFoundError: 正解データファイルが見つからない場合
            yaml.YAMLError: YAMLファイルのパース時にエラーが発生した場合
        """
        config_path = (
            Path(__file__).parent.parent.parent / "config" / "expected_data.yaml"
        )

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data["expected_texts"]
        except FileNotFoundError:
            raise FileNotFoundError(
                f"正解データファイルが見つかりません: {config_path}"
            )
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"正解データファイルの読み込みに失敗しました: {e}")
