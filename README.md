# iriam-point-analyzer

日本語スクリーンショットからテキストを抽出するOCRツール

## 機能

- 画像からの日本語テキスト抽出（EasyOCR/Tesseract対応）
- 複数の画像前処理オプション（basic/adaptive/otsu）
- バッチ処理による複数画像の一括処理
- テキスト抽出結果の精度評価
- 設定ファイルによるパラメータ管理

## インストール

```bash
# 依存パッケージのインストール
uv sync
```

## 使い方

```bash
# 基本的な使用方法
python main.py path/to/image.png

# OCRエンジンの指定
python main.py path/to/image.png --engine easyocr  # または tesseract

# 前処理方法の指定
python main.py path/to/image.png --preprocess basic  # none/basic/adaptive/otsu
```

## 設定

主な設定は各エンジンのデフォルト値を使用します：

- EasyOCR: 日本語と英語に対応
- Tesseract: 日本語対応（`jpn.traineddata`が必要）

詳細な設定が必要な場合は、各エンジンのソースコードで設定可能です：
- `src/ocr/easyocr_engine.py`
- `src/ocr/tesseract_engine.py`

## プロジェクト構造

```plaintext
.
├── config/            # 設定ファイル
├── data/              # 入力データ
│   └── img/           # 画像ファイル
├── results/           # 出力結果
├── src/               # ソースコード
│   ├── config/        # 設定ローダー
│   ├── ocr/           # OCRエンジン
│   ├── preprocessing/ # 画像前処理
│   ├── evaluation/    # 精度評価
│   └── utils/         # ユーティリティ
└── tests/             # テストコード
```
