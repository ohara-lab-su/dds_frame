"""DDS実機不要のRPC経路テスト（通信はインメモリに差し替える）。"""
from collections import defaultdict, deque
from unittest.mock import patch
from dds_frame.client import DeviceClient
from dds_frame.server import DeviceServer


class Counter:
    def __init__(self):
        self.value = 0
    def increment(self, amount=1):
        self.value += amount
        return self.value
    def read(self):
        return self.value


class Endpoint:
    def __init__(self, name, queues, on_write=None):
        self.name, self.queues, self.on_write = name, queues, on_write
    def write(self, message):
        self.queues[self.name].append(message)
        if self.on_write:
            self.on_write()
    def take(self):
        items = list(self.queues[self.name]); self.queues[self.name].clear()
        return items


def test_transparent_call_and_deduplication():
    queues = defaultdict(deque)
    server_holder = []
    def writer(dp, name):
        callback = server_holder[0].serve_once if name.endswith('/request') and server_holder else None
        return Endpoint(name, queues, callback)
    def reader(dp, name):
        return Endpoint(name, queues)
    with patch('dds_frame.server.participant', return_value=object()), \
         patch('dds_frame.server.reader', side_effect=reader), \
         patch('dds_frame.server.writer', side_effect=writer), \
         patch('dds_frame.client.participant', return_value=object()), \
         patch('dds_frame.client.reader', side_effect=reader), \
         patch('dds_frame.client.writer', side_effect=writer):
        device = Counter()
        server = DeviceServer('counter', device)
        server_holder.append(server)
        client = DeviceClient('counter', timeout=1)
        assert client.increment(2) == 2
        assert client.read() == 2
        assert device.value == 2
        client.close(); server.close()
