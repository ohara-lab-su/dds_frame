# 公開API

- `DeviceServer(name, device, domain_id=0, allowed_methods=None)`：制御クラスを公開します。
- `DeviceClient(name, domain_id=0, timeout=5)`：制御クラスと同名のメソッドを同期呼び出しします。
- `AsyncDeviceClient(name, ...)`：`await client.method(...)`で呼び出します。
- `Publisher(topic, domain_id=0)`：Topicにデータを配信します。
- `Subscriber(topic, domain_id=0)`：Topicからデータを受信します。

制御クラス固有のAPIはフレームにはありません。
