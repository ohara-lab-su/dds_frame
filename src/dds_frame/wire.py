"""DDSワイヤ型。独自形式でありROS 2メッセージ型とは互換ではない。"""
from dataclasses import dataclass
from cyclonedds.idl import IdlStruct
from cyclonedds.idl.types import sequence, uint8


@dataclass
class FrameMessage(IdlStruct, typename="dds_frame::FrameMessage"):
    request_id: str
    sender_id: str
    method: str
    payload: sequence[uint8]
    error_type: str
    error_message: str
