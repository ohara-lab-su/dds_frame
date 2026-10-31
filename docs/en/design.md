# Architecture

The DDS DomainParticipant is the transport-level peer. Request/reply and pub/sub are layered over DDS topics. A device object must remain transport independent. DDS discovery is not arbitrary multi-hop routing.


## Current limitations

This initial implementation uses native CycloneDDS participants and provides synchronous RPC and pub/sub. It does not implement DDS routing, automatic cross-domain bridging, ROS 2 Service/Action interoperability, or OMG DDS-RPC. Exactly one RPC server per device name is assumed. Public methods must be explicitly allowlisted. Discovery is asynchronous; requests sent before endpoint matching may be lost under volatile QoS. MessagePack payloads are opaque bytes rather than fully typed DDS data models.
