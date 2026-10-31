from dds_frame import DeviceClient


def main():
    counter = DeviceClient("counter", timeout=10.0)
    try:
        print(counter.increment(2))
        print(counter.read())
    finally:
        counter.close()


if __name__ == "__main__":
    main()
