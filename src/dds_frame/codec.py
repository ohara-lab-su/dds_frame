"""通信メッセージのシリアライズ。pickleは使用しない。"""
import msgpack


def dumps(value) -> bytes:
    """msgpackでエンコードする。対応型は基本的なJSON相当型とbytes。"""
    return msgpack.packb(value, use_bin_type=True)


def loads(data: bytes):
    """msgpackでデコードする。"""
    return msgpack.unpackb(data, raw=False, strict_map_key=False)
