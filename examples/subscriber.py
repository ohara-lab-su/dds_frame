from dds_frame import Subscriber


def main():
    subscriber = Subscriber("counter/state")
    try:
        while True:
            print(subscriber.receive())
    except KeyboardInterrupt:
        pass
    finally:
        subscriber.close()


if __name__ == "__main__":
    main()
