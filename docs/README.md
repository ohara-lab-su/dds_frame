# docs/README.md — 文書の構成と設計判断

本ディレクトリはGitHub Pages（MkDocs Material）のソースです。`mkdocs.yml`の`nav`に対応します。

## 作成時の合意事項

1. `dds_frame`はROS 2に依存しないDDSネイティブのフレームとする。ROS 2はDDSそのものではない。
2. 既存の`grpc_frame`・`ese774_frame`と並列の通信方式として扱う。デバイスクラスは通信方式から独立させる。
3. RPC（透過的なメソッド呼び出し）とPub/Sub（1対多の状態配信）を両方扱うが、意味論を混同しない。
4. ROS 2との相互運用は将来の検討対象。DDS採用のみではTopic、Service、Actionの互換性は成立しない。
5. 最初の実装はCycloneDDS Pythonを使用する。Fast DDS等への抽象化は必要性を検証してから行う。
6. Pythonパッケージの依存は通常の`pip install`で解決する。`optional-dependencies`は用いない。
7. 設計説明と運用ドキュメントは日本語を基本とする。

## ドキュメント更新時の注意

未実装のROS 2対応を実装済みと書かないこと。DDSネイティブ互換とROS 2互換は分けて記述すること。実装にないQoS設定、DDS Security、動的API公開、async APIを宣伝しないこと。デバイスクラスに通信責務を移さないこと。

詳細は`design.md`、`compatibility.md`、`reference/api.md`を参照。


## 分散通信とルーティング

DDSのParticipantは対等な通信主体であり、固定されたclient/server役割はありません。Server間通信も双方がDataWriter/DataReaderを持つことで成立します。ただしDDSのDiscoveryは任意の多段経路の自動ルーティングを意味しません。ネットワークやDomainを跨ぐ場合はDDS Router/Bridge等を別途検討します。

## 既存フレームとの責務分離

デバイスクラスはDDS、Topic、Publisher、Subscriberを認識しません。フレームが通信処理を担当します。既存のgrpc_frame/ese774_frameの動的メソッド公開、プロパティ、DeviceProxy、型スタブとのAPI整合は未検証であり、現時点で互換性を主張しません。
