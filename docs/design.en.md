# Architecture

The DDS DomainParticipant is the transport-level peer. Request/reply and pub/sub are layered over DDS topics. A device object must remain transport independent. DDS discovery is not arbitrary multi-hop routing.
