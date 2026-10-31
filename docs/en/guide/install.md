# Installation

Use Python 3.10 or later.

```bash
python -m pip install .
```

Runtime dependencies are managed exclusively by `pyproject.toml`: `cyclonedds>=11.0.1,<12` and `msgpack>=1.0,<2`. Prebuilt CycloneDDS wheels include the native runtime on supported platforms. DDS Security and Iceoryx shared-memory support are not included in those wheels.

```bash
python -c "import cyclonedds, dds_frame; print(dds_frame.__version__)"
python -m pytest -q
```
