import os
import cv2


def preprocess_image(image_path: str, output_path: str, method: str = "basic") -> None:
    """
    画像の前処理を行い、結果を保存する。
    Args:
        image_path: 入力画像のパス
        output_path: 出力画像のパス
        method: 前処理方法 ('basic', 'adaptive', 'otsu')
    """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"画像が見つかりません: {image_path}")

    if method == "basic":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        denoised = cv2.fastNlMeansDenoising(enhanced, h=10)
        _, result = cv2.threshold(denoised, 150, 255, cv2.THRESH_BINARY)

    elif method == "adaptive":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        result = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

    elif method == "otsu":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, result = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    else:
        raise ValueError(f"Unknown preprocessing method: {method}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, result)


def preprocess(
    image_path: str, method: str, tmp_folder: str = "data/img/preprocessed"
) -> str:
    """
    前処理を行い、前処理後の画像パスを返す。
    Args:
        image_path: 元画像のパス
        method: 前処理方法 ('basic','adaptive','otsu','none')
        tmp_folder: 前処理画像を保存するフォルダ
    Returns:
        保存した画像のパス、method=='none' なら元パスを返す
    """
    if method == "none":
        return image_path
    base, ext = os.path.splitext(os.path.basename(image_path))
    os.makedirs(tmp_folder, exist_ok=True)
    out_path = os.path.join(tmp_folder, f"{base}_{method}{ext}")
    preprocess_image(image_path, out_path, method)
    return out_path
