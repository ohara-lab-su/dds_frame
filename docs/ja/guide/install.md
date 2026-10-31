# インストール

Python 3.10以上を使用します。標準のインストール方法は次のとおりです。

```bash
python -m pip install .
```

`pyproject.toml` の標準依存関係に `cyclonedds>=11.0.1,<12` と `msgpack>=1.0,<2` を記載しています。CycloneDDSの対応wheelが利用可能な環境ではネイティブライブラリの個別導入は不要です。

対応wheelがないプラットフォームではソースビルドが必要になる場合があります。DDS SecurityおよびIceoryx共有メモリ通信は通常のwheelに含まれません。

```bash
python -c "import cyclonedds, dds_frame; print(dds_frame.__version__)"
python -m pytest -q
```

`requirements.txt` は `-e .` として `pyproject.toml` の依存関係を参照します。
