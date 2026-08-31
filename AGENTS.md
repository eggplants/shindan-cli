# shindan-cli — Agent Instructions

[診断メーカー](https://shindanmaker.com) の診断結果を取得する Python 製 CLI + ライブラリ。

## 必須コマンド

```bash
mise run pytest        # テスト実行
mise run pytest-cov    # カバレッジ付きテスト
mise run ruff          # Lint + フォーマット確認
mise run ty            # 型チェック
mise run build         # パッケージビルド
```

> `mise run` の代わりに `uv run <tool>` でも実行可能。

## アーキテクチャ

```
shindan_cli/
  main.py         - CLI エントリーポイント (argparse)
  shindan.py      - メインロジック・診断タイプ判別・ShindanError 定義
  get_results.py  - 診断タイプ別の HTTP POST + スクレイピング処理
  interactive.py  - AI/分岐診断における対話型入力処理
  models.py       - TypedDict によるデータモデル定義
  constants.py    - URL・HTTPヘッダー・パラメータ名の定数定義
```

## コード規約

- **全ファイル**: `from __future__ import annotations` + 型ヒント必須
- **HTTP**: `curl_cffi`（`_http.create_session()` 経由。Cloudflare は TLS/HTTP2 フィンガープリントを見るため、`requests` 等の素の HTTP クライアントは使わない）
- **非同期**: 使用しない（同期処理のみ）
- **Lint**: Ruff（`pyproject.toml` で設定済み）。変更後は `mise run ruff` を通すこと
- **型チェック**: `ty`（`mise run ty`）で確認

## テスト

- `tests/test_cli.py`: CLI 引数・標準出力のテスト
- `tests/test_shindan.py`: スクレイピング・API 統合テスト（実通信あり）
- 対話型入力は `monkeypatch` で `input` をシミュレート

## 注意事項

- **HTML セレクタの脆弱性**: `get_results.py` / `interactive.py` のセレクタは診断メーカーの HTML 構造に依存。サイト変更で壊れる可能性がある
- **AI 診断の SSE**: `get_result_by_ai` は SSE 形式のレスポンスを正規表現でパース（`get_results.py` 参照）
- **CSRF トークン**: 診断ページはキャッシュ配信で `_token` / `meta[name=csrf-token]` が空。`GET /csrf-token` から取得して埋める（`shindan.py`）
- **AI 診断**: Cloudflare Turnstile で保護されており、スクリプトからは `encrypted_exec_key` を取得できない（`test_ai` は xfail）
- **CI からの実通信**: GitHub Actions の IP は Cloudflare に 403 で弾かれる。`tests/conftest.py` が 403 をスキップに変換する
- **マジックパラメータ**: `_token`、`rbr` 等のパラメータ名は診断メーカー側の仕様に依存
- **Python バージョン**: `>=3.10` 必須（`pyproject.toml` 参照）
