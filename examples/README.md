# examples の実行方法

`dds_frame` のサンプルです。すべてプロジェクトのルートディレクトリから実行します。

## 準備

```bash
python -m pip install .
```

## 1. 透過型 RPC

RPC は、サーバー側にある制御クラスのメソッドをクライアントから呼び出し、その戻り値を取得する通信です。

`counter_device.py` は DDS に依存しない制御クラスです。`counter_server.py` がそのインスタンスを公開し、クライアントは
`counter.increment(2)` や `counter.read()` を直接呼び出します。

ターミナル1（サーバーを起動し、そのまま稼働させる）：

```bash
python examples/counter_server.py
```

ターミナル2（同期クライアント）：

```bash
python examples/counter_client.py
```

正常時の出力例：

```text
2
2
```

非同期クライアントも試す場合（サーバーは起動したまま）：

```bash
python examples/async_counter_client.py
```

`Counter` の値はサーバーの起動中保持されます。同期クライアントを実行した後に非同期クライアントを実行すると、加算結果は `4`
になります。サーバーは `Ctrl+C` で終了します。

## 2. Pub/Sub の意味

Pub/Sub（Publish/Subscribe）は、 **Publisher が Topic にデータを発行し、
同じ Topic を購読する Subscriber がそのデータを受信する**通信方式です。

RPC は特定の操作を要求して結果を待つのに対し、
Pub/Sub は相手を個別指定せずにデータを配信します。例えば、計測装置の測定値や装置状態を、監視画面・記録プログラム・解析プログラムへ同時に届ける用途に適しています。

```text
Publisher（publisher.py）
    │ publish({"value": 0}) など
    ▼
Topic: counter/state
    ├── Subscriber（subscriber.py）
    └── 同じ Topic を購読する別の Subscriber
```

**Topic 名が一致することが必要です。** このサンプルでは両方とも `counter/state` を使用します。DDS の Domain ID や QoS
などの通信条件も適合する必要があります。

この Pub/Sub サンプルは RPC の `Counter` 制御クラスとは独立しています。`publisher.py` が 0〜9 の値を生成して配信します。RPC
の `increment()` が自動的に配信されるわけではありません。

## 3. Pub/Sub の実行方法

ターミナル1（Subscriber を先に起動）：

```bash
python examples/subscriber.py
```

ターミナル2（Publisher を起動）：

```bash
python examples/publisher.py
```

Publisher は `{"value": 0}` から `{"value": 9}` までを1秒間隔で送信し、終了します。Subscriber は受信したデータを表示し、受信待ちを継続します。終了は
`Ctrl+C` です。

Subscriber 側の表示例：

```text
{'value': 0}
{'value': 1}
{'value': 2}
...
{'value': 9}
```

DDS は通信開始時に Discovery（通信相手の発見と条件照合）を行います。接続が成立する前に発行されたデータは受信できない場合があります。表示例は全件受信を保証するものではありません。

複数の Subscriber を確認する場合は、別のターミナルでも `python examples/subscriber.py` を実行してから Publisher
を起動します。それぞれの Subscriber が同じ Topic のデータを受信できます。

## 4. インスタンス生成と終了処理

すべてのサンプルでインスタンスを明示的に生成し、`finally` 節で `close()` を呼び出します。非同期クライアントでは
`await close()` を呼び出します。`with` / `async with` によるインスタンス管理は使用しません。

## 5. 検証状況

このサンプルはコードの構文検査を実施していますが、CycloneDDS を使用した実通信は未検証です。実行結果は想定例です。
