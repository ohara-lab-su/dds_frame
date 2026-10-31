# dds_frame

[English](README.md) | [日本語](README.ja.md)

既存のPython制御クラスを通信方式から独立させたまま、
DDSで公開するための軽量な通信フレームです。`ese774_frame`、`grpc_frame` と並ぶ独立した選択肢であり、SUSANOO全体をDDSに置き換えるものではありません。

- 透過型RPC：既存の制御クラスを`DeviceServer`に渡し、`DeviceClient`から元のメソッド名で呼び出します。
- DDS Pub/Sub：`Publisher`と`Subscriber`で、RPCとは独立した一対多・多対多のデータ配信を行います。
- 制御クラスのAPIを統一・再定義しません。通信の知識を制御クラスに持ち込みません。

```bash
python -m pip install .
```

実行方法：[examples/README.md](examples/README.md)

設計と制約：[docs/ja/design.md](docs/ja/design.md)

**検証状況：** Python構文検査のみ。CycloneDDSランタイムを使った実通信テストは未実施です。QoS公開・ROS
2相互運用・型スタブ生成・厳密なexactly-once保証は提供していません。
