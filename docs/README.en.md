# Design notes

DDS is a data-centric distributed middleware. Its peers are DomainParticipants; a participant can be both a writer and reader. Peer-to-peer and server-to-server communication are possible. Discovery is not general-purpose multi-hop routing. ROS 2 compatibility requires compatible topic names, IDL types and QoS. Device classes must not depend on transport details.
