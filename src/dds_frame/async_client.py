"""同期RPCとは独立したasyncio側の呼び出し窓口。"""
import asyncio
from .client import DeviceClient

class AsyncDeviceClient:
    """非同期クライアント。同期DDS呼び出しをワーカースレッドで実行する。"""
    def __init__(self, name: str, **kwargs):
        self._client = DeviceClient(name, **kwargs)

    def __getattr__(self, method):
        if method.startswith('_'):
            raise AttributeError(method)
        async def invoke(*args, **kwargs):
            return await self.call(method, *args, **kwargs)
        return invoke

    async def call(self, method, *args, **kwargs):
        return await asyncio.to_thread(self._client.call, method, *args, **kwargs)

    async def close(self):
        await asyncio.to_thread(self._client.close)

    async def __aenter__(self): return self
    async def __aexit__(self, *_): await self.close()
