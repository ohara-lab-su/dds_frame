"""通信フレームの例外。"""
class FrameError(Exception):
    """通信フレーム内で発生したエラー。"""

class RequestTimeout(FrameError, TimeoutError):
    """RPC応答が期限までに到着しなかった。"""

class RemoteError(FrameError):
    """リモートデバイス側で発生した例外。"""
    def __init__(self, type_name: str, message: str):
        self.type_name = type_name
        super().__init__(f"{type_name}: {message}")
