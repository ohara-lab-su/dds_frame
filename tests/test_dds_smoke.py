"""実際のCycloneDDSランタイムを使った最小スモークテスト。"""
from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic
from dds_frame.wire import FrameMessage

def test_domain_participant_and_topic():
    participant = DomainParticipant(0)
    topic = Topic(participant, "dds_frame_test_smoke", FrameMessage)
    assert topic is not None
