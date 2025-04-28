# IRIAM Point Analyzer

画像からOCRを使用してポイント情報を抽出し、CSVファイルとして出力するPythonプロジェクトです。

## プロジェクト概要

このプロジェクトは、画像ファイルから特定のポイント情報を抽出し、構造化されたデータとして保存することを目的としています。

### 処理フロー

1. 指定されたディレクトリから画像ファイル（PNG）を読み込み
2. Tesseract OCRを使用してテキストを抽出
3. 抽出したテキストから必要な情報（日付、ポイント、名前等）を構造化
4. 結果をCSVファイルとして出力

## 必要要件

- Python 3.13以上
- Tesseract OCR（macOSの場合はHomebrewでインストール）
- 以下のPythonパッケージ：
  - pytesseract >= 0.3.13
  - Pillow >= 11.2.1
  - fuzzywuzzy >= 0.18.0
  - python-Levenshtein >= 0.27.1

## インストール

1. リポジトリをクローン：

   ```bash
   git clone [リポジトリURL]
   cd iriam-point-analyzing
   ```

2. uvを使用して仮想環境を作成：

   ```bash
   uv venv
   ```

3. 依存パッケージをインストール：

   ```bash
   uv sync
   ```

4. Tesseract OCRのインストール（macOS）：

   ```bash
   brew install tesseract
   ```

## 名前データの設定

このプロジェクトを実行するには、`config/private/name_data.json` ファイルが必要です。このファイルには、英語名と日本語名のペアをリスト形式で持つ `name_table` キーが含まれています。

1. サンプルファイルをコピーして設定ファイルを作成：

   ```bash
   cp config/private/name_data.json.sample config/private/name_data.json
   ```

2. `name_data.json` の設定内容：

   ```json
   {
     "name_table": [
       ["english_name_1", "日本語名1"],
       ["english_name_2", "日本語名2"],
       ["another_english_name", "別の日本語名"]
     ]
   }
   ```

   - `name_table`: 英語名と日本語名のペアのリスト。各要素は [英語名, 日本語名] の形式で指定します。

## 使い方

1. 画像ファイルを `img/` ディレクトリに配置

2. スクリプトを実行：

   ```bash
   python src/main.py
   ```

3. 処理結果は `output.csv` に出力されます。出力されるデータ形式：
   - date: 日付
   - pt: ポイント値
   - name: 名前（英字）
   - namae: 名前（日本語）

## テストの実行

プロジェクトのテストを実行するには以下のコマンドを使用します：

```bash
uv add --dev pytest  # テスト用の依存パッケージをインストール
pytest tests/  # テストの実行
```

## エラー対応

- 画像ディレクトリが存在しない場合はエラーメッセージが表示されます
- OCRの精度が低い場合は、画像の品質を確認してください
- Tesseractが正しくインストールされていることを確認してください
