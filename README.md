# dds_frame

[English](README.md) | [日本語](README.ja.md)

A small DDS communication frame alongside `grpc_frame` and `ese774_frame`. It does not replace the SUSANOO architecture or impose a uniform device API. Device classes are independent of transport.

- Transparent RPC with `DeviceServer`, `DeviceClient`, and `AsyncDeviceClient`.
- Native DDS pub/sub with `Publisher` and `Subscriber`, independent of RPC.

```bash
python -m pip install .
```

Run examples as documented in [examples/README.md](examples/README.md). Design constraints: [docs/ja/design.md](docs/ja/design.md).

**Status:** Syntax-checked; end-to-end DDS runtime tests have not been completed. The wire IDL is not ROS 2 compatible. Strict exactly-once execution is not guaranteed.
