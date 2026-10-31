# RPC

サーバー: `python examples/counter_server.py`、別プロセスでクライアント: `python examples/counter_client.py`。

`DeviceClient.call(method, *args, timeout=None, **kwargs)`で呼び出します。サーバーは`DeviceServer(name, device, allowed_methods={...})`で許可した公開メソッドのみを実行できます。

返り値・引数はMessagePack対応型を使用してください。通信タイムアウトは`RequestTimeout`、デバイス側例外は`RemoteError`です。サーバー側の例外クラス自体は転送しません。

RPCはDDS標準のServiceではなく、独自のRequest/Response Topicを用いるプロトコルです。複数サーバーを同名で動かさないでください。


透過型呼び出し / Transparent call: `client.increment(2)`。
