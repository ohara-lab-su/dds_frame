"""デバイスRPCとは独立したDDS Publish/Subscribe。"""
from collections import deque
import time
import uuid
from .codec import dumps, loads
from .transport import participant, reader, writer
from .wire import FrameMessage

class Publisher:
    def __init__(self, topic: str, *, domain_id: int = 0):
        self._dp = participant(domain_id)
        self._writer = writer(self._dp, f'dds_frame/pubsub/{topic}')
        self._id = uuid.uuid4().hex
    def publish(self, value):
        self._writer.write(FrameMessage('', self._id, '', list(dumps(value)), '', ''))
    def close(self):
        self._writer = self._dp = None
    def __enter__(self): return self
    def __exit__(self, *_): self.close()

class Subscriber:
    def __init__(self, topic: str, *, domain_id: int = 0):
        self._dp = participant(domain_id)
        self._reader = reader(self._dp, f'dds_frame/pubsub/{topic}')
        self._buffer = deque()
    def receive(self, *, timeout: float | None = None):
        if timeout is not None and timeout < 0:
            raise ValueError('timeout must be non-negative')
        deadline = None if timeout is None else time.monotonic() + timeout
        while True:
            if self._buffer:
                sample = self._buffer.popleft()
                # DDSのインスタンス状態変更などに伴う無効サンプルはデータを持たない。
                if not isinstance(sample, FrameMessage):
                    continue
                return loads(bytes(sample.payload))
            self._buffer.extend(self._reader.take())
            if self._buffer:
                continue
            if deadline is not None and time.monotonic() >= deadline:
                raise TimeoutError('DDS subscriber timeout')
            time.sleep(0.01)
    def close(self):
        self._reader = self._dp = None
    def __enter__(self): return self
    def __exit__(self, *_): self.close()
