import time
from dds_frame import Publisher


def main():
    publisher = Publisher("counter/state")
    try:
        for value in range(10):
            publisher.publish({"value": value})
            time.sleep(1)
    finally:
        publisher.close()


if __name__ == "__main__":
    main()
