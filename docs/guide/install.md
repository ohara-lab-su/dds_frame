# インストール

```bash
python -m pip install dds-frame
```

開発時は`python -m pip install -e .`。Pythonパッケージの依存は`pyproject.toml`の標準`dependencies`に記載し、optional dependenciesは使いません。

ネイティブCycloneDDSライブラリの導入状況はOS・配布wheelに依存します。インストール後は`python -c "import cyclonedds; import dds_frame"`で確認してください。

送受信プロセスは同じDDS Domain IDを指定してください。異なるマシンではDiscoveryのためのネットワーク設定も必要です。
