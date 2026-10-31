"""制御クラスを通信フレームに依存させないDDS RPCサーバー。"""
from collections import OrderedDict
import inspect
import time
from .codec import dumps, loads
from .transport import participant, reader, writer
from .wire import FrameMessage

class DeviceServer:
    def __init__(self, name: str, device, *, domain_id: int = 0,
                 allowed_methods=None, cache_size: int = 4096):
        if cache_size < 1:
            raise ValueError('cache_size must be positive')
        self.name, self.device = name, device
        # デバイスAPIの仕様・実装は制御クラスが保持する。
        self.allowed_methods = (
            {n for n, m in inspect.getmembers(device) if not n.startswith('_') and callable(m)}
            if allowed_methods is None else set(allowed_methods)
        )
        if any(n.startswith('_') or not callable(getattr(device, n, None)) for n in self.allowed_methods):
            raise ValueError('allowed_methods contains a non-public or non-callable member')
        self._dp = participant(domain_id)
        self._req = reader(self._dp, f'dds_frame/{name}/request')
        self._res = writer(self._dp, f'dds_frame/{name}/response')
        self._cache = OrderedDict()
        self._cache_size = cache_size
        self._running = False

    def dispatch(self, method: str, args: list, kwargs: dict):
        if method.startswith('_') or method not in self.allowed_methods:
            raise AttributeError(f'method not published: {method}')
        return getattr(self.device, method)(*args, **kwargs)

    def serve_once(self):
        count = 0
        for sample in self._req.take():
            if not isinstance(sample, FrameMessage):
                continue
            count += 1
            key = (sample.sender_id, sample.request_id)
            reply = self._cache.get(key)
            if reply is None:
                try:
                    call = loads(bytes(sample.payload))
                    result = self.dispatch(sample.method, call['args'], call['kwargs'])
                    reply = FrameMessage(sample.request_id, sample.sender_id, sample.method,
                                         list(dumps(result)), '', '')
                except Exception as exc:
                    reply = FrameMessage(sample.request_id, sample.sender_id, sample.method,
                                         [], type(exc).__name__, str(exc))
                self._cache[key] = reply
                if len(self._cache) > self._cache_size:
                    self._cache.popitem(last=False)
            else:
                self._cache.move_to_end(key)
            self._res.write(reply)
        return count

    def serve_forever(self, *, poll_interval: float = 0.01):
        self._running = True
        while self._running:
            if not self.serve_once():
                time.sleep(poll_interval)

    def stop(self): self._running = False
    def close(self):
        self.stop()
        self._req = self._res = self._dp = None
    def __enter__(self): return self
    def __exit__(self, *_): self.close()
