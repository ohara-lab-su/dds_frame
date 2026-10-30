# API一覧

| クラス | 主要API | 用途 |
| --- | --- | --- |
| `DeviceServer` | `serve_once()`, `serve_forever()`, `stop()`, `dispatch()` | RPCサーバー |
| `DeviceClient` | `call(method, *args, timeout=None, **kwargs)` | 同期RPCクライアント |
| `Publisher` | `publish(value)` | データ配信 |
| `Subscriber` | `receive(timeout=None)` | データ受信 |
| `RequestTimeout` | 例外 | 応答期限切れ |
| `RemoteError` | `type_name`属性 | サーバー側例外 |

各クラスはコンテキストマネージャーをサポートします。すべて`domain_id=0`を既定値として受け取ります。

ワイヤ形式は`dds_frame.wire.FrameMessage`。`request_id`, `sender_id`, `method`, `payload`, `error_type`, `error_message`を持ちます。公開APIとワイヤ形式は0.1系では変更される可能性があります。
