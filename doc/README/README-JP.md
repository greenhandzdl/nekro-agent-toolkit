# 日本語ユーザーマニュアル

<p align="center">
	<img src="../icons/nekro-agent-toolkit-icons.png" alt="Nekro Agent Toolkit吉祥物">
</p>

Nekro Agent Toolkit は、Nekro Agent および関連サービスをデプロイ、バックアップ、復元するためのオールインワンツールであり、Docker 環境での自動化をサポートします。

## 🌐 他の言語へのリンク

| [Read in English](README-EN.md) | [اقرأ باللغة العربية](README-AR.md) | [Lire en français](README-FR.md) | [Читать на русском](README-RU.md) | [Leer en español](README-ES.md) | [日本語で読む](README-JP.md) |

## ✨ 主な機能

- ワンクリックで Nekro Agent のインストール、アップグレード、バックアップ、復元
- インテリジェントな検出と多言語サポート
- Docker ボリュームの自動バックアップと復元をサポート

## 🚀 クイックスタート

### インストール

```bash
pip install nekro-agent-toolkit
# またはソースから実行
git clone https://github.com/your-repo/nekro-agent-toolkit.git
cd nekro-agent-toolkit
```

### よく使うコマンド

```bash
# インストール/アップグレード/バックアップ/復元
nekro-agent-toolkit -i [PATH]
nekro-agent-toolkit -u [PATH]
nekro-agent-toolkit -b [DATA_DIR] BACKUP_DIR
nekro-agent-toolkit -r BACKUP_FILE [DATA_DIR]
```

### uv を使用した依存関係の管理（推奨）

このプロジェクトは現在、`uv` を使用して依存関係を管理し、再現可能なロックファイル `uv.lock` を生成することをサポートしています。

## 追加情報

- システム要件: Python 3.6+、Docker、Docker Compose
- ライセンス: [LICENSE](../LICENSE) を参照