# Publish/Subscribe

先に`python examples/subscriber.py`を起動し、別プロセスで`python examples/publisher.py`を起動します。

`Publisher(topic).publish(value)`で配信し、`Subscriber(topic).receive(timeout=...)`で受信します。Topic名は`dds_frame/pubsub/`を接頭辞としてDDSに登録します。

初期実装ではDDS QoSの詳細設定を公開していません。遅れて参加したSubscriberに過去のサンプルが届く保証はありません。リアルタイム制御への利用ではDeadline、Reliability、Durabilityなどの明示的な設計が必要です。
