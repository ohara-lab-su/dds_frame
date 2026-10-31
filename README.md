# dds_frame

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/ohara-lab-su/dds_frame/blob/main/README.md)
[![ja](https://img.shields.io/badge/lang-ja-blue.svg)](https://github.com/ohara-lab-su/dds_frame/blob/main/README.ja.md)

[![GitHub](https://img.shields.io/badge/GitHub-ohara--lab--su%2Fdds_frame-181717?logo=github)](https://github.com/ohara-lab-su/dds_frame/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Documentation-222222?logo=githubpages&logoColor=white)](https://ohara-lab-su.github.io/dds_frame/en/)
[![Ohara Lab](https://img.shields.io/badge/Ohara%20Lab-Home-4B5563?logo=homeassistant&logoColor=white)](https://ohara-lab-su.github.io/index.en.html)


> **TESTING PHASE — NOT PRODUCTION READY.** Only minimal tests have been performed. Basic DDS Pub/Sub message reception
> has been observed, but an `InvalidSample` reception error was reported and the subsequent fix has not been verified by
> an end-to-end test. RPC and other runtime scenarios are not comprehensively validated. Do not assume operational
> reliability.

A small DDS communication frame alongside `grpc_frame` and `ese774_frame`. It does not replace the SUSANOO architecture
or impose a uniform device API. Device classes are independent of transport.

- Transparent RPC with `DeviceServer`, `DeviceClient`, and `AsyncDeviceClient`.
- Native DDS pub/sub with `Publisher` and `Subscriber`, independent of RPC.

```bash
python -m pip install .
```

Run examples as documented in [examples/README.md](examples/README.md). Design
constraints: [docs/ja/design.md](docs/ja/design.md).

**Known limitations:** The wire IDL is not ROS 2 compatible. Strict exactly-once execution is not guaranteed. QoS
configuration and generated device-specific `.pyi` stubs are not yet provided.
