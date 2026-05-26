from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest
from tom_v3_model_adapters import yolo_runtime
from tom_v3_model_adapters.yolo_runtime import (
    YoloDeviceUnavailable,
    probe_yolo_runtime,
    resolve_yolo_device,
)


def fake_torch(cuda_available: bool = False, mps_available: bool = False) -> SimpleNamespace:
    return SimpleNamespace(
        __version__="2.test",
        cuda=SimpleNamespace(is_available=lambda: cuda_available),
        backends=SimpleNamespace(
            mps=SimpleNamespace(is_available=lambda: mps_available),
        ),
    )


def test_base_worker_cli_imports_without_yolo_runtime() -> None:
    import apps.worker.cli as worker_cli

    assert worker_cli.main is not None


def test_runtime_probe_reports_missing_optional_dependencies(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def missing_import(name: str) -> None:
        raise ImportError(f"missing {name}")

    monkeypatch.setattr(yolo_runtime.importlib, "import_module", missing_import)

    result = probe_yolo_runtime()

    assert result["status"] == "unavailable"
    assert result["ultralytics_available"] is False
    assert result["torch_available"] is False
    assert result["opencv_available"] is False
    assert result["resolved_device"] == "cpu"
    assert result["missing_packages"] == [
        "ultralytics",
        "torch",
        "opencv-python-headless",
    ]
    assert "pip install -r requirements-yolo.txt" in result["install_hint"]


def test_runtime_probe_reports_versions_when_runtime_is_mocked(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    torch_module = fake_torch(cuda_available=True)

    def fake_import(name: str) -> SimpleNamespace:
        if name == "ultralytics":
            return SimpleNamespace(__version__="8.test")
        if name == "torch":
            return torch_module
        if name == "cv2":
            return SimpleNamespace(__version__="4.test")
        raise ImportError(name)

    monkeypatch.setattr(yolo_runtime.importlib, "import_module", fake_import)

    result = probe_yolo_runtime()

    assert result["status"] == "ok"
    assert result["ultralytics_version"] == "8.test"
    assert result["torch_version"] == "2.test"
    assert result["opencv_version"] == "4.test"
    assert result["resolved_device"] == "cuda:0"
    assert result["cuda_available"] is True


def test_device_resolver_auto_prefers_cuda() -> None:
    result = resolve_yolo_device(torch_module=fake_torch(cuda_available=True, mps_available=True))

    assert result.resolved_device == "cuda:0"
    assert result.cuda_available is True


def test_device_resolver_auto_uses_mps_when_allowed() -> None:
    result = resolve_yolo_device(torch_module=fake_torch(cuda_available=False, mps_available=True))

    assert result.resolved_device == "mps"
    assert result.mps_available is True


def test_device_resolver_auto_falls_back_to_cpu() -> None:
    result = resolve_yolo_device(torch_module=fake_torch())

    assert result.resolved_device == "cpu"


def test_device_resolver_explicit_cpu_always_succeeds_without_torch() -> None:
    result = resolve_yolo_device(requested_device="cpu", torch_module=None)

    assert result.resolved_device == "cpu"


def test_device_resolver_explicit_mps_fails_when_unavailable() -> None:
    with pytest.raises(YoloDeviceUnavailable, match="MPS"):
        resolve_yolo_device(requested_device="mps", torch_module=fake_torch())


def test_device_resolver_explicit_cuda_fails_when_unavailable() -> None:
    with pytest.raises(YoloDeviceUnavailable, match="CUDA"):
        resolve_yolo_device(requested_device="cuda", torch_module=fake_torch())


def test_gitignore_protects_model_assets_and_weights() -> None:
    gitignore = Path(".gitignore").read_text()

    for pattern in ["model_assets/", "weights/", "*.pt", "*.pth", "*.onnx", "*.engine"]:
        assert pattern in gitignore
