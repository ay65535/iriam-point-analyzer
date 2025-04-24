import cv2
import numpy as np


class ImageProcessor:
    """画像の前処理を行うクラス"""

    @staticmethod
    def preprocess_image(
        image_path: str, output_path: str = None, method: str = "basic"
    ) -> np.ndarray:
        """
        画像の前処理を行う

        Args:
            image_path: 入力画像のパス
            output_path: 出力画像のパス（Noneの場合は保存しない）
            method: 前処理方法 ('basic', 'adaptive', 'otsu')

        Returns:
            前処理された画像（NumPy配列）

        Raises:
            ValueError: 未知の前処理方法が指定された場合
        """
        # 画像を読み込む
        image = cv2.imread(image_path)

        # グレースケール変換（全メソッド共通）
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if method == "basic":
            # コントラスト調整
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)

            # ノイズ除去
            denoised = cv2.fastNlMeansDenoising(enhanced, h=10)

            # 二値化（閾値処理）
            _, result = cv2.threshold(denoised, 150, 255, cv2.THRESH_BINARY)

        elif method == "adaptive":
            # ガウシアンブラー
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # 適応的閾値処理
            result = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )

        elif method == "otsu":
            # ガウシアンブラー
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Otsuの二値化
            _, result = cv2.threshold(
                blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )

        else:
            raise ValueError(f"Unknown method: {method}")

        # 結果を保存
        if output_path:
            cv2.imwrite(output_path, result)

        return result
