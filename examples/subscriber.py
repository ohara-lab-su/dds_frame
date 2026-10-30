from dds_frame import Subscriber

if __name__ == "__main__":
    with Subscriber("counter/state") as sub:
        while True:
            print(sub.receive())
