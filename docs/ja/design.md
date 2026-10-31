# 設計方針・DDSとROS 2の関係

## 目的

`dds_frame`は`grpc_frame`や`ese774_frame`と並ぶ独立した通信フレームです。デバイスクラスには通信技術の知識を持ち込まず、フレーム側が通信とリモート呼び出しを担当します。特定のデバイスのAPIや例外型をDDSの型定義に固定しません。

## ROS 2とDDSは同一ではない

ROS 2は`rclpy`/`rclcpp`、`rcl`、`rmw`などからなるフレームワークです。`rmw`の下位でFast DDSやCyclone DDSを使う構成が一般的ですが、ZenohなどDDS以外のバックエンドもあります。DDSはROS 2なしで使える独立したOMG標準です。

```text
ROS 2 Node -> rclpy/rclcpp -> rcl -> rmw -> DDS implementation
Python Application -> dds_frame -> CycloneDDS Python -> DDS implementation
```

`dds_frame`を`rclpy`ベースにするとROS 2のノード実装に依存します。本パッケージではその依存を避け、DDSネイティブの通信フレームとします。将来ROS 2にネイティブ対応する必要がある場合は、別途`ros2_frame`や明示的なブリッジを検討します。

## RPCとPub/Subは別の通信意味論

RPCは`method + args + kwargs`を要求し、相関IDで結果を返します。Pub/SubはTopicへのデータ配信であり、呼び出しと結果の一対一対応を要求しません。状態値をSubscriber側にキャッシュする設計と、毎回デバイスに問い合わせる設計は同じではありません。

## ワイヤ形式

`FrameMessage`はDDS IDL型です。ペイロードはMessagePackでエンコードします。これは`dds_frame`独自の規約であり、標準DDS-RPCでもROS 2のメッセージでもありません。異言語実装は同じIDL型とMessagePack形式、Topic規約を実装する必要があります。

RPC Topic: `dds_frame/<device>/request`, `dds_frame/<device>/response`。Pub/Sub Topic: `dds_frame/pubsub/<topic>`。

## デバイスとの責務分離

`DeviceServer`が受信、デコード、メソッド呼び出し、結果・エラーの返信を担当します。デバイスクラスにはDDSの継承、Publisherの保持、DDSの例外型、通信状態管理を要求しません。デバイス側のエラーはワイヤ上の`error_type`と`error_message`に変換し、クライアント側で`RemoteError`として復元します。任意の元例外クラスを無条件に再生成することはしません。

## この版で未対応の事項

- ROS 2 Topic/Service/Actionへの直接互換
- DDS-RPC標準への準拠
- 複数サーバーへの単一要求の排他配送（DDSのPub/Subは通常全購読者に届く）
- 認証・認可・暗号化、複雑なデータ型の汎用シリアライズ
- QoSの詳細な設定、非同期API、型スタブの自動生成
- 動的Discoveryに基づくサービス一覧・スキーマ配信

将来の互換性検討ではROS 2のTopic名の`rt/`マッピング、IDL型名と型ハッシュ、XCDR表現、QoS、Serviceの要求応答規約を別々に検証します。DDS実装を同じにするだけではROS 2互換にはなりません。


## 現在の実装範囲と制約

本版はCycloneDDS 11系のDDS Participantを使う同期RPCおよびPub/Subの初期実装です。DDSルーティング機能、異なるDomain間の自動中継、ROS 2のService/Action互換、DDS-RPC標準への準拠は実装していません。

RPCはデバイス名に対応する要求・応答Topicを使用します。同一デバイス名で複数サーバーを起動すると、要求が複数サーバーで実行され得るため、**同一デバイス名につきサーバーは1プロセス**を前提とします。複数クライアントの要求を並列に処理する保証もありません。

公開メソッドは`allowed_methods`で明示します。デバイスクラス自身にDDS固有のAPIを要求しません。

DDSのDiscoveryは非同期です。初回の書き込みがReaderとのマッチング前に行われると、デフォルトのVOLATILE QoSでは失われ得ます。初回RPCではタイムアウトを考慮し、運用前に接続確立とQoSの検証が必要です。

MsgPackで符号化した任意のPython値をDDS IDLのバイト列に格納する方式は、DDSの型付きデータ空間を完全には活用しません。将来の型付きTopic対応とROS 2相互運用は別の設計課題です。
