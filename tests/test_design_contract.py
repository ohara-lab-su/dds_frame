"""制御クラスと通信の分離に関する回帰テスト。"""
from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]

def test_device_class_has_no_transport_dependency():
    tree = ast.parse((ROOT / 'examples/counter_device.py').read_text())
    assert not any(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(tree))

def test_client_has_dynamic_dispatch():
    tree = ast.parse((ROOT / 'src/dds_frame/client.py').read_text())
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'DeviceClient')
    assert any(isinstance(n, ast.FunctionDef) and n.name == '__getattr__' for n in cls.body)

def test_pubsub_does_not_depend_on_rpc():
    tree = ast.parse((ROOT / 'src/dds_frame/pubsub.py').read_text())
    assert not any(isinstance(n, ast.ImportFrom) and n.module in ('client','server') for n in tree.body)
