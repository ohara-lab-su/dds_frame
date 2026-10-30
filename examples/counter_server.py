from dds_frame import DeviceServer


class Counter:
    def __init__(self):
        self.value = 0

    def increment(self, amount=1):
        self.value += amount
        return self.value

    def read(self):
        return self.value


if __name__ == "__main__":
    with DeviceServer("counter", Counter(), allowed_methods={"increment", "read"}) as server:
        print("DDS counter server running")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
