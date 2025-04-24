import os
from typing import List


def list_images(folder: str) -> List[str]:
    """
    ディレクトリ内の画像ファイル一覧を取得
    """
    if not os.path.isdir(folder):
        raise NotADirectoryError(f"フォルダが見つかりません: {folder}")
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]


def save_text(output_folder: str, image_path: str, lines: List[str]) -> str:
    """
    テキスト行をファイルに保存し、保存先パスを返す
    """
    os.makedirs(output_folder, exist_ok=True)
    base = os.path.splitext(os.path.basename(image_path))[0]
    out_file = os.path.join(output_folder, f"{base}.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    return out_file
