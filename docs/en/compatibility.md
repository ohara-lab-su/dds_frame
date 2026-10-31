# ROS 2 interoperability

ROS 2 uses an RMW abstraction, often backed by DDS. Native DDS topics do not automatically match ROS 2 topics, services or actions: names, IDL type identifiers, encodings and QoS must be compatible. This package does not implement ROS 2 message interoperability.
