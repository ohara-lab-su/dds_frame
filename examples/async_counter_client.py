import asyncio
from dds_frame import AsyncDeviceClient


async def main():
    counter = AsyncDeviceClient("counter", timeout=10.0)
    try:
        print(await counter.increment(2))
        print(await counter.read())
    finally:
        await counter.close()


if __name__ == "__main__":
    asyncio.run(main())
