# dds_frame

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/ohara-lab-su/dds_frame/blob/main/README.md)
[![ja](https://img.shields.io/badge/lang-ja-blue.svg)](https://github.com/ohara-lab-su/dds_frame/blob/main/README.ja.md)

[![GitHub](https://img.shields.io/badge/GitHub-ohara--lab--su%2Fdds_frame-181717?logo=github)](https://github.com/ohara-lab-su/dds_frame/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Documentation-222222?logo=githubpages&logoColor=white)](https://ohara-lab-su.github.io/dds_frame/ja/)
[![Ohara Lab](https://img.shields.io/badge/Ohara%20Lab-Home-4B5563?logo=homeassistant&logoColor=white)](https://ohara-lab-su.github.io/index.html)


> **テスト段階（実運用非推奨）**
>
> 基本機能について最低限のテストは実施していますが、網羅的な検証は完了していません。
> 実際の運用条件における信頼性は確認できておらず、現時点では実用フェーズに達していません。

既存のPython制御クラスを通信方式から独立させたまま、DDSで公開するための軽量な通信フレームです。`ese774_frame`、`grpc_frame`
と並ぶ独立した選択肢であり、SUSANOO全体をDDSに置き換えるものではありません。

- 透過型RPC：既存の制御クラスを`DeviceServer`に渡し、`DeviceClient`から元のメソッド名で呼び出します。
- DDS Pub/Sub：`Publisher`と`Subscriber`で、RPCとは独立した一対多・多対多のデータ配信を行います。
- 制御クラスのAPIを統一・再定義しません。通信の知識を制御クラスに持ち込みません。

```bash
python -m pip install .
```

実行方法：[examples/README.md](examples/README.md)

設計と制約：[docs/ja/design.md](docs/ja/design.md)

**既知の制約：** QoS設定の公開、ROS 2との相互運用、デバイス専用`.pyi`生成、厳密なexactly-once実行保証は提供していません。
