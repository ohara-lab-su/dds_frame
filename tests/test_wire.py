from dds_frame.wire import FrameMessage


def test_message_fields():
    message = FrameMessage("a", "b", "read", [1, 2], "", "")
    assert message.request_id == "a"
    assert bytes(message.payload) == b"\x01\x02"
