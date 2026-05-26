from __future__ import annotations

import importlib
import sys
from dataclasses import dataclass
from types import ModuleType
from typing import Any

YOLO_RUNTIME_INSTALL_HINT = (
    "Install the optional YOLO runtime in a separate environment, for example: "
    "pip install -r requirements-yolo.txt. Torch may require a platform-specific "
    "install command for CUDA or MPS support."
)


class YoloRuntimeUnavailable(RuntimeError):
    pass


class YoloDeviceUnavailable(RuntimeError):
    pass


class YoloWeightsUnavailable(RuntimeError):
    pass


@dataclass(frozen=True)
class ResolvedYoloDevice:
    requested_device: str
    resolved_device: str
    cuda_available: bool
    mps_available: bool
    reason: str


@dataclass(frozen=True)
class YoloRuntimeImportResult:
    ultralytics: ModuleType | Any | None
    torch: ModuleType | Any | None
    cv2: ModuleType | Any | None
    missing_packages: tuple[str, ...]
    import_errors: dict[str, str]

    @property
    def ultralytics_available(self) -> bool:
        return self.ultralytics is not None

    @property
    def torch_available(self) -> bool:
        return self.torch is not None

    @property
    def opencv_available(self) -> bool:
        return self.cv2 is not None


def try_import_yolo_runtime() -> YoloRuntimeImportResult:
    imports: dict[str, ModuleType | Any | None] = {}
    missing_packages: list[str] = []
    import_errors: dict[str, str] = {}
    module_specs = {
        "ultralytics": "ultralytics",
        "torch": "torch",
        "cv2": "opencv-python-headless",
    }

    for module_name, package_name in module_specs.items():
        try:
            imports[module_name] = importlib.import_module(module_name)
        except ImportError as exc:
            imports[module_name] = None
            missing_packages.append(package_name)
            import_errors[module_name] = str(exc)

    return YoloRuntimeImportResult(
        ultralytics=imports["ultralytics"],
        torch=imports["torch"],
        cv2=imports["cv2"],
        missing_packages=tuple(missing_packages),
        import_errors=import_errors,
    )


def resolve_yolo_device(
    requested_device: str = "auto",
    allow_mps: bool = True,
    torch_module: Any | None = None,
) -> ResolvedYoloDevice:
    normalized = _normalize_requested_device(requested_device)
    cuda_available = _cuda_available(torch_module)
    mps_available = _mps_available(torch_module)

    if normalized == "cpu":
        return ResolvedYoloDevice(
            requested_device=requested_device,
            resolved_device="cpu",
            cuda_available=cuda_available,
            mps_available=mps_available,
            reason="explicit cpu request",
        )

    if normalized == "auto":
        if cuda_available:
            return ResolvedYoloDevice(
                requested_device=requested_device,
                resolved_device="cuda:0",
                cuda_available=True,
                mps_available=mps_available,
                reason="auto selected cuda:0 because torch reports CUDA availability",
            )
        if allow_mps and mps_available:
            return ResolvedYoloDevice(
                requested_device=requested_device,
                resolved_device="mps",
                cuda_available=False,
                mps_available=True,
                reason="auto selected mps because torch reports MPS availability",
            )
        return ResolvedYoloDevice(
            requested_device=requested_device,
            resolved_device="cpu",
            cuda_available=cuda_available,
            mps_available=mps_available,
            reason="auto fell back to cpu",
        )

    if normalized == "mps":
        if torch_module is None:
            raise YoloDeviceUnavailable(
                "MPS was requested, but torch is not available. "
                f"{YOLO_RUNTIME_INSTALL_HINT}"
            )
        if not allow_mps:
            raise YoloDeviceUnavailable("MPS was requested, but MPS is disabled by --no-mps.")
        if not mps_available:
            raise YoloDeviceUnavailable("MPS was requested, but torch reports MPS is unavailable.")
        return ResolvedYoloDevice(
            requested_device=requested_device,
            resolved_device="mps",
            cuda_available=cuda_available,
            mps_available=True,
            reason="explicit mps request",
        )

    if normalized.startswith("cuda"):
        if torch_module is None:
            raise YoloDeviceUnavailable(
                "CUDA was requested, but torch is not available. "
                f"{YOLO_RUNTIME_INSTALL_HINT}"
            )
        if not cuda_available:
            raise YoloDeviceUnavailable(
                "CUDA was requested, but torch reports CUDA is unavailable."
            )
        return ResolvedYoloDevice(
            requested_device=requested_device,
            resolved_device=normalized,
            cuda_available=True,
            mps_available=mps_available,
            reason=f"explicit {normalized} request",
        )

    raise YoloDeviceUnavailable(
        "Unsupported YOLO device request. Use auto, cpu, mps, cuda, cuda:0, or 0."
    )


def probe_yolo_runtime(requested_device: str = "auto", allow_mps: bool = True) -> dict[str, Any]:
    runtime_imports = try_import_yolo_runtime()
    messages: list[str] = []
    device_error: str | None = None
    resolved_device: ResolvedYoloDevice | None = None

    try:
        resolved_device = resolve_yolo_device(
            requested_device=requested_device,
            allow_mps=allow_mps,
            torch_module=runtime_imports.torch,
        )
    except YoloDeviceUnavailable as exc:
        device_error = str(exc)
        messages.append(device_error)

    if runtime_imports.missing_packages:
        messages.append(YOLO_RUNTIME_INSTALL_HINT)

    status = "ok"
    if runtime_imports.missing_packages or device_error:
        status = "unavailable"

    return {
        "python_version": sys.version.split()[0],
        "ultralytics_available": runtime_imports.ultralytics_available,
        "ultralytics_version": _module_version(runtime_imports.ultralytics),
        "torch_available": runtime_imports.torch_available,
        "torch_version": _module_version(runtime_imports.torch),
        "opencv_available": runtime_imports.opencv_available,
        "opencv_version": _module_version(runtime_imports.cv2),
        "cuda_available": _cuda_available(runtime_imports.torch),
        "mps_available": _mps_available(runtime_imports.torch),
        "requested_device": requested_device,
        "resolved_device": resolved_device.resolved_device if resolved_device else None,
        "device_resolution_reason": resolved_device.reason if resolved_device else None,
        "allow_mps": allow_mps,
        "status": status,
        "missing_packages": list(runtime_imports.missing_packages),
        "import_errors": runtime_imports.import_errors,
        "device_error": device_error,
        "messages": messages,
        "install_hint": YOLO_RUNTIME_INSTALL_HINT,
    }


def _normalize_requested_device(requested_device: str | None) -> str:
    normalized = (requested_device or "auto").strip().lower()
    if normalized == "0":
        return "cuda:0"
    if normalized == "cuda":
        return "cuda:0"
    return normalized


def _cuda_available(torch_module: Any | None) -> bool:
    try:
        return bool(torch_module is not None and torch_module.cuda.is_available())
    except AttributeError:
        return False


def _mps_available(torch_module: Any | None) -> bool:
    try:
        return bool(torch_module is not None and torch_module.backends.mps.is_available())
    except AttributeError:
        return False


def _module_version(module: Any | None) -> str | None:
    if module is None:
        return None
    version = getattr(module, "__version__", None)
    return str(version) if version is not None else None
