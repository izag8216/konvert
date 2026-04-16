[![header](https://capsule-render.vercel.app/api?type=cylinder&color=0:0D1117,100:1a1a2e&fontColor=3FB950&height=220&section=header&text=konvert&fontSize=48&fontAlignY=40&desc=Universal%20Data%20Format%20Converter&descSize=16&descAlignY=55)](https://github.com/izag8216/konvert)

![Python](https://img.shields.io/badge/python-3.10%2B-3FB950?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-0D1117?style=flat)
![Tests](https://img.shields.io/badge/tests-116%20passing-3FB950?style=flat)
![Coverage](https://img.shields.io/badge/coverage-81%25-3FB950?style=flat)

[English](./README.md)

# konvert

**ユニバーサルデータフォーマット変換CLI**

JSON、YAML、TOML、CSV、XML、INI、.env間の相互変換を行う、設定不要のパイプフレンドリーなコマンドラインツール。Python 3.10+。

## 特徴

- **設定不要** -- 入力ファイルとターゲットフォーマットを指定するだけ
- **7フォーマット** -- JSON, YAML, TOML, CSV, XML, INI, .env（42種のフォーマットペア）
- **自動検出** -- ファイル拡張子とコンテンツから入力フォーマットを自動検出
- **パイプ対応** -- 標準入力/標準出力でパイプラインに組み込み可能
- **バッチモード** -- ディレクトリ内のファイルを一括変換
- **インプレース変換** -- コピーを作成せずにファイルを変換
- **スキーマ検出** -- 変換せずにデータ構造を確認
- **コメント保持** -- TOMLのコメントはtomlkit経由でラウンドトリップ可能

## インストール

```bash
git clone https://github.com/izag8216/konvert.git
cd konvert
pip install -e .
```

Python 3.10+が必要です。

## 使い方

### 基本的な変換

```bash
# JSONからYAMLへ
konvert config.json yaml

# YAMLからTOMLへ
konvert settings.yaml toml

# JSONからXMLへ
konvert data.json xml
```

### パイプモード

```bash
# 標準入力から標準出力へ
cat config.json | konvert - yaml

# 他のツールとチェーン
curl -s https://api.example.com/data | konvert - yaml
```

### オプション付き

```bash
# 整形出力
konvert config.json yaml --pretty

# 入力フォーマットを明示指定
konvert data.yaml json -f yaml

# ファイルに出力
konvert config.json yaml -o output.yaml
```

### インプレース変換

```bash
# ファイルを変換して元ファイルを置き換え
konvert config.yaml --to json --in-place
# config.jsonを作成、config.yamlを削除
```

### バッチ変換

```bash
# ディレクトリ内の全ファイルを変換
konvert ./configs --to yaml --batch
```

### スキーマ検出

```bash
konvert config.json --schema
```

出力:
```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "version": { "type": "string" }
  }
}
```

## 対応フォーマット

| フォーマット | 拡張子 | 入力 | 出力 | 備考 |
|------------|--------|------|------|------|
| JSON | `.json` | yes | yes | ネスト構造対応 |
| YAML | `.yaml`, `.yml` | yes | yes | PyYAMLベース |
| TOML | `.toml` | yes | yes | tomlkitでコメント保持 |
| CSV | `.csv` | yes | yes | 1行目をヘッダーとして扱う |
| XML | `.xml` | yes | yes | 複数キーのdictは自動ラップ |
| INI | `.ini`, `.cfg`, `.conf` | yes | yes | セクションベース |
| .env | `.env` | yes | yes | KEY=VALUE形式 |

## 開発

```bash
pip install -e ".[dev]"
pytest tests/ -v --cov=konvert
```

## コントリビュート

1. リポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. テストを記述
4. 全テストが通ることを確認 (`pytest`)
5. 80%以上のカバレッジを維持
6. プルリクエストを開く

## ライセンス

MIT License -- 詳細は[LICENSE](./LICENSE)を参照。

## 作者

**izag8216** -- [GitHub](https://github.com/izag8216)
