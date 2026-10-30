import time
from dds_frame import Publisher

if __name__ == "__main__":
    with Publisher("counter/state") as pub:
        for value in range(10):
            pub.publish({"value": value})
            time.sleep(1)
