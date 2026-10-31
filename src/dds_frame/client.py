"""DDS経由で任意のPython制御オブジェクトを操作する透過クライアント。"""
import threading
import time
import uuid
from .codec import dumps, loads
from .errors import RemoteError, RequestTimeout
from .transport import participant, reader, writer
from .wire import FrameMessage

class DeviceClient:
    """デバイス固有のAPIを定義しない同期プロキシ。"""
    def __init__(self, name: str, *, domain_id: int = 0, timeout: float = 5.0,
                 retry_interval: float = 0.25):
        if timeout <= 0 or retry_interval <= 0:
            raise ValueError("timeout and retry_interval must be positive")
        self.name, self.timeout, self.retry_interval = name, timeout, retry_interval
        self.sender_id = uuid.uuid4().hex
        self._dp = participant(domain_id)
        self._req = writer(self._dp, f"dds_frame/{name}/request")
        self._res = reader(self._dp, f"dds_frame/{name}/response")
        self._lock = threading.RLock()
        self._closed = False

    def __getattr__(self, method):
        if method.startswith('_'):
            raise AttributeError(method)
        def invoke(*args, **kwargs):
            return self.call(method, *args, **kwargs)
        invoke.__name__ = method
        return invoke

    def call(self, method: str, *args, timeout: float | None = None, **kwargs):
        if self._closed:
            raise RuntimeError("DeviceClient is closed")
        if not method or method.startswith('_'):
            raise AttributeError(method)
        duration = self.timeout if timeout is None else timeout
        if duration <= 0:
            raise ValueError("timeout must be positive")
        request_id = uuid.uuid4().hex
        message = FrameMessage(request_id, self.sender_id, method,
                               list(dumps({'args': args, 'kwargs': kwargs})), '', '')
        deadline = time.monotonic() + duration
        next_send = 0.0
        # 1インスタンス内の受信応答の取り違えを防止するため直列化する。
        with self._lock:
            while time.monotonic() < deadline:
                now = time.monotonic()
                if now >= next_send:
                    self._req.write(message)
                    next_send = now + self.retry_interval
                for sample in self._res.take():
                    if not isinstance(sample, FrameMessage):
                        continue
                    if sample.sender_id != self.sender_id or sample.request_id != request_id:
                        continue
                    if sample.error_type:
                        raise RemoteError(sample.error_type, sample.error_message)
                    return loads(bytes(sample.payload))
                time.sleep(min(0.01, max(0.0, deadline - time.monotonic())))
        raise RequestTimeout(f"{self.name}.{method}: timeout; remote execution status unknown")

    def close(self):
        with self._lock:
            self._closed = True
            self._res = None
            self._req = None
            self._dp = None

    def __enter__(self): return self
    def __exit__(self, *_): self.close()
