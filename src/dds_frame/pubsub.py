"""DDSネイティブのPublish/Subscribe。"""
import time
import uuid
from .codec import dumps, loads
from .transport import participant, reader, writer
from .wire import FrameMessage


class Publisher:
    def __init__(self, topic: str, *, domain_id: int = 0):
        self._dp = participant(domain_id)
        self._writer = writer(self._dp, f"dds_frame/pubsub/{topic}")
        self._id = uuid.uuid4().hex

    def publish(self, value):
        self._writer.write(FrameMessage("", self._id, "", list(dumps(value)), "", ""))

    def close(self):
        self._writer = None
        self._dp = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


class Subscriber:
    def __init__(self, topic: str, *, domain_id: int = 0):
        self._dp = participant(domain_id)
        self._reader = reader(self._dp, f"dds_frame/pubsub/{topic}")

    def receive(self, *, timeout: float | None = None):
        """次のデータを返す。期限切れはTimeoutError。"""
        deadline = None if timeout is None else time.monotonic() + timeout
        while deadline is None or time.monotonic() < deadline:
            samples = self._reader.take()
            if samples:
                return loads(bytes(samples[0].payload))
            time.sleep(0.005)
        raise TimeoutError("DDS subscriber timeout")

    def close(self):
        self._reader = None
        self._dp = None

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
