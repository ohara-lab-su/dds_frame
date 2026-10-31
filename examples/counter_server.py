from dds_frame import DeviceServer
from counter_device import Counter


def main():
    device = Counter()
    server = DeviceServer("counter", device)
    try:
        print("DDS counter server running", flush=True)
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        server.close()


if __name__ == "__main__":
    main()
