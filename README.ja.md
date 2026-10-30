# dds_frame

DDSネイティブの通信フレーム。ROS 2を必要とせず、DDSのRequest/Reply型RPCとPublish/Subscribe型配信をPythonから利用します。初期実装はCycloneDDS Pythonを使用します。

> **開発初期版 (0.1.0)**: API・ワイヤ形式はまだ安定していません。実機制御や安全系への導入前に、ネットワーク、QoS、タイムアウト、異常系の検証が必要です。

## 導入

```bash
pip install dds-frame
```

Python依存パッケージは通常の`pip install`で導入します。CycloneDDSのネイティブ実行環境・ネットワーク設定については環境ごとの確認が必要です。

## RPC（別プロセスで起動）

サーバー:

```python
from dds_frame import DeviceServer

class Counter:
    def __init__(self):
        self.value = 0
    def increment(self, amount=1):
        self.value += amount
        return self.value
    def read(self):
        return self.value

with DeviceServer("counter", Counter()) as server:
    server.serve_forever()
```

クライアント:

```python
from dds_frame import DeviceClient

with DeviceClient("counter") as client:
    print(client.call("increment", 2))
    print(client.call("read"))
```

## Publish/Subscribe

```python
from dds_frame import Publisher, Subscriber

with Publisher("counter/state") as pub:
    pub.publish({"value": 1})

with Subscriber("counter/state") as sub:
    sample = sub.receive(timeout=3.0)
    print(sample)
```

PublisherとSubscriberは別プロセスで動作させてください。受信側のDiscovery完了前に送信したデータは既定のVOLATILE QoSでは失われ得ます。

## 設計上の境界

- デバイスクラスにDDSの型・Publisher・Subscriberを要求しません。
- `DeviceServer`がデバイスオブジェクトを呼び出し、通信例外とデバイス例外を分離します。
- RPCは要求と応答の相関IDを使用します。Pub/SubはRPCの代替ではなく独立した通信モデルです。
- ROS 2のTopic/Service/Actionへの直接接続は**この版では未対応**です。DDS利用だけではROS 2互換になりません。
- ネットワーク越しの認証・暗号化、任意の公開メソッドの実行制限は実運用時に設計が必要です。信頼できるネットワーク内での評価を想定しています。

詳しくは[設計文書](docs/design.md)、[API](docs/reference/api.md)、[互換性](docs/compatibility.md)を参照してください。

## 開発

```bash
python -m pip install -e .
python -m pip install pytest mkdocs-material
pytest
mkdocs serve
```

ライセンス: Apache-2.0
