from dds_frame.codec import dumps, loads


def test_roundtrip():
    value = {"args": [1, "abc", True, None, b"data"], "kwargs": {"a": 2}}
    assert loads(dumps(value)) == value
