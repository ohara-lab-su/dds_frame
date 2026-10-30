from dds_frame import DeviceClient

if __name__ == "__main__":
    with DeviceClient("counter", timeout=10.0) as client:
        print(client.call("increment", 2))
        print(client.call("read"))
