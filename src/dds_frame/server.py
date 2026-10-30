"""デバイスオブジェクトを公開するRPCサーバー。"""
import time
from .codec import dumps, loads
from .transport import participant, reader, writer
from .wire import FrameMessage


class DeviceServer:
    """DDSの通信処理とデバイスオブジェクトを分離する。"""

    def __init__(self, name: str, device, *, domain_id: int = 0, allowed_methods=None):
        self.name = name
        self.device = device
        self.allowed_methods = set(allowed_methods) if allowed_methods is not None else None
        self._dp = participant(domain_id)
        self._req = reader(self._dp, f"dds_frame/{name}/request")
        self._res = writer(self._dp, f"dds_frame/{name}/response")
        self._running = False

    def dispatch(self, method: str, args: list, kwargs: dict):
        """通信非依存のデバイス呼び出し。"""
        if method.startswith("_") or (self.allowed_methods is not None and method not in self.allowed_methods):
            raise AttributeError(f"method not published: {method}")
        fn = getattr(self.device, method)
        if not callable(fn):
            raise TypeError(f"not callable: {method}")
        return fn(*args, **kwargs)

    def serve_once(self) -> int:
        """到着済み要求を処理し、処理件数を返す。"""
        count = 0
        for sample in self._req.take():
            count += 1
            try:
                call = loads(bytes(sample.payload))
                result = self.dispatch(sample.method, call["args"], call["kwargs"])
                reply = FrameMessage(sample.request_id, sample.sender_id, sample.method, list(dumps(result)), "", "")
            except Exception as exc:
                reply = FrameMessage(sample.request_id, sample.sender_id, sample.method, [], type(exc).__name__, str(exc))
            self._res.write(reply)
        return count

    def serve_forever(self, *, poll_interval: float = 0.01):
        self._running = True
        while self._running:
            if not self.serve_once():
                time.sleep(poll_interval)

    def stop(self):
        self._running = False

    def close(self):
        self.stop()
        self._req = None
        self._res = None
        self._dp = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
