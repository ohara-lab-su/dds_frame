"""同期RPCクライアント。"""
import threading
import time
import uuid
from .codec import dumps, loads
from .errors import RemoteError, RequestTimeout
from .transport import participant, reader, writer
from .wire import FrameMessage


class DeviceClient:
    """1クライアントにつき1つの返信購読を使用する。"""

    def __init__(self, name: str, *, domain_id: int = 0, timeout: float = 5.0):
        self.name = name
        self.timeout = timeout
        self.sender_id = uuid.uuid4().hex
        self._dp = participant(domain_id)
        self._req = writer(self._dp, f"dds_frame/{name}/request")
        self._res = reader(self._dp, f"dds_frame/{name}/response")
        self._lock = threading.Lock()
        self._pending = {}

    def call(self, method: str, *args, timeout: float | None = None, **kwargs):
        """指定メソッドをリモート実行する。同期呼び出しはロックで直列化。"""
        request_id = uuid.uuid4().hex
        payload = dumps({"args": list(args), "kwargs": kwargs})
        message = FrameMessage(request_id, self.sender_id, method, list(payload), "", "")
        limit = time.monotonic() + (self.timeout if timeout is None else timeout)
        with self._lock:
            self._req.write(message)
            while time.monotonic() < limit:
                cached = self._pending.pop(request_id, None)
                if cached is not None:
                    return self._decode(cached)
                for sample in self._res.take():
                    if sample.sender_id != self.sender_id:
                        continue
                    if sample.request_id == request_id:
                        return self._decode(sample)
                    self._pending[sample.request_id] = sample
                time.sleep(0.005)
        raise RequestTimeout(f"{self.name}.{method}: timeout")

    @staticmethod
    def _decode(sample):
        if sample.error_type:
            raise RemoteError(sample.error_type, sample.error_message)
        return loads(bytes(sample.payload))

    def close(self):
        """DDSエンティティを解放する。"""
        self._res = None
        self._req = None
        self._dp = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
