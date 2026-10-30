"""DDS Participant/Topic生成の共通処理。"""
from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic
from cyclonedds.pub import DataWriter
from cyclonedds.sub import DataReader
from .wire import FrameMessage


def participant(domain_id: int):
    return DomainParticipant(domain_id)


def writer(dp, name: str):
    return DataWriter(dp, Topic(dp, name, FrameMessage))


def reader(dp, name: str):
    return DataReader(dp, Topic(dp, name, FrameMessage))
