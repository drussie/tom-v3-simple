from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tom_v3_model_adapters.yolo_runtime import (
    YoloWeightsUnavailable,
    try_import_yolo_runtime,
)

ALLOWED_YOLO_WEIGHT_SUFFIXES = {".pt", ".pth", ".onnx", ".engine"}
DEFAULT_YOLO_ALLOWED_ROOTS = (Path("model_assets/yolo"), Path("weights/yolo"))
TARGET_OBSERVATION_TYPES = {"ball_detection", "player_detection"}
TARGET_LABELS = {"ball", "player_unknown", "near_player", "far_player"}


@dataclass(frozen=True)
class YoloWeightsValidationResult:
    weights_path: str
    resolved_path: str
    exists: bool
    is_file: bool
    suffix: str | None
    size_bytes: int | None
    sha256: str | None
    required_sha256: str | None
    sha256_matches: bool | None
    status: str
    message: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "weights_path": self.weights_path,
            "resolved_path": self.resolved_path,
            "exists": self.exists,
            "is_file": self.is_file,
            "suffix": self.suffix,
            "size_bytes": self.size_bytes,
            "sha256": self.sha256,
            "required_sha256": self.required_sha256,
            "sha256_matches": self.sha256_matches,
            "status": self.status,
            "message": self.message,
        }


class YoloWeightsValidationError(YoloWeightsUnavailable):
    def __init__(self, result: YoloWeightsValidationResult) -> None:
        super().__init__(result.message)
        self.result = result


class YoloClassMappingError(ValueError):
    pass


def validate_yolo_weights(
    weights_path: str | Path,
    allowed_roots: Sequence[str | Path] | None = None,
    required_sha256: str | None = None,
    raise_on_error: bool = True,
) -> YoloWeightsValidationResult:
    original_path = str(weights_path)
    path = Path(weights_path).expanduser()
    resolved_path = path.resolve(strict=False)
    suffix = resolved_path.suffix.lower() or None

    if allowed_roots is not None and not _is_within_allowed_roots(resolved_path, allowed_roots):
        return _result_or_raise(
            YoloWeightsValidationResult(
                weights_path=original_path,
                resolved_path=str(resolved_path),
                exists=resolved_path.exists(),
                is_file=resolved_path.is_file(),
                suffix=suffix,
                size_bytes=None,
                sha256=None,
                required_sha256=required_sha256,
                sha256_matches=None,
                status="invalid_path",
                message=(
                    "YOLO weights path resolves outside the allowed roots. "
                    "Use model_assets/yolo or weights/yolo, or pass an explicit allowed root."
                ),
            ),
            raise_on_error,
        )

    if not resolved_path.exists():
        return _result_or_raise(
            YoloWeightsValidationResult(
                weights_path=original_path,
                resolved_path=str(resolved_path),
                exists=False,
                is_file=False,
                suffix=suffix,
                size_bytes=None,
                sha256=None,
                required_sha256=required_sha256,
                sha256_matches=None,
                status="missing",
                message=f"YOLO weights file does not exist: {resolved_path}",
            ),
            raise_on_error,
        )

    if not resolved_path.is_file():
        return _invalid_path(
            original_path,
            resolved_path,
            suffix,
            required_sha256,
            "YOLO weights path must point to a file, not a directory.",
            raise_on_error,
        )

    if suffix not in ALLOWED_YOLO_WEIGHT_SUFFIXES:
        return _invalid_path(
            original_path,
            resolved_path,
            suffix,
            required_sha256,
            "YOLO weights file suffix is unsupported. Use .pt, .pth, .onnx, or .engine.",
            raise_on_error,
        )

    size_bytes = resolved_path.stat().st_size
    if size_bytes <= 0:
        return _invalid_path(
            original_path,
            resolved_path,
            suffix,
            required_sha256,
            "YOLO weights file is empty.",
            raise_on_error,
        )

    sha256 = _sha256_file(resolved_path)
    sha256_matches = None
    if required_sha256 is not None:
        sha256_matches = sha256.lower() == required_sha256.lower()
        if not sha256_matches:
            return _result_or_raise(
                YoloWeightsValidationResult(
                    weights_path=original_path,
                    resolved_path=str(resolved_path),
                    exists=True,
                    is_file=True,
                    suffix=suffix,
                    size_bytes=size_bytes,
                    sha256=sha256,
                    required_sha256=required_sha256,
                    sha256_matches=False,
                    status="checksum_mismatch",
                    message=(
                        "YOLO weights checksum mismatch: "
                        f"expected {required_sha256}, calculated {sha256}."
                    ),
                ),
                raise_on_error,
            )

    return YoloWeightsValidationResult(
        weights_path=original_path,
        resolved_path=str(resolved_path),
        exists=True,
        is_file=True,
        suffix=suffix,
        size_bytes=size_bytes,
        sha256=sha256,
        required_sha256=required_sha256,
        sha256_matches=sha256_matches,
        status="ok",
        message="YOLO weights file validated.",
    )


def default_yolo_class_mapping() -> dict[str, dict[str, Any]]:
    return {
        "ball": {
            "source_class_names": ["sports ball", "tennis ball", "ball"],
            "source_class_ids": [],
            "target_observation_type": "ball_detection",
            "target_label": "ball",
        },
        "player": {
            "source_class_names": ["person", "player"],
            "source_class_ids": [],
            "target_observation_type": "player_detection",
            "target_label": "player_unknown",
        },
        "near_player": {
            "source_class_names": ["near_player"],
            "source_class_ids": [],
            "target_observation_type": "player_detection",
            "target_label": "near_player",
        },
        "far_player": {
            "source_class_names": ["far_player"],
            "source_class_ids": [],
            "target_observation_type": "player_detection",
            "target_label": "far_player",
        },
    }


def validate_yolo_class_mapping(
    class_mapping: Mapping[str, Any] | None = None,
) -> dict[str, dict[str, Any]]:
    mapping = dict(class_mapping or default_yolo_class_mapping())
    if not mapping:
        raise YoloClassMappingError("YOLO class mapping must include at least one entry.")

    normalized: dict[str, dict[str, Any]] = {}
    for mapping_name, entry_value in mapping.items():
        if not isinstance(entry_value, Mapping):
            raise YoloClassMappingError(f"class mapping entry must be an object: {mapping_name}")
        source_class_names = [str(name) for name in entry_value.get("source_class_names", [])]
        source_class_ids = [int(class_id) for class_id in entry_value.get("source_class_ids", [])]
        target_observation_type = str(entry_value.get("target_observation_type", ""))
        target_label = str(entry_value.get("target_label", ""))

        if target_observation_type not in TARGET_OBSERVATION_TYPES:
            raise YoloClassMappingError(
                f"invalid target_observation_type for {mapping_name}: {target_observation_type}"
            )
        if target_label not in TARGET_LABELS:
            raise YoloClassMappingError(
                f"invalid target_label for {mapping_name}: {target_label}"
            )
        if not source_class_names and not source_class_ids:
            raise YoloClassMappingError(
                "class mapping entry requires source_class_names or "
                f"source_class_ids: {mapping_name}"
            )

        normalized[str(mapping_name)] = {
            "source_class_names": source_class_names,
            "source_class_ids": source_class_ids,
            "target_observation_type": target_observation_type,
            "target_label": target_label,
        }
    return normalized


def probe_yolo_model_metadata(weights_path: str | Path, device: str = "cpu") -> dict[str, Any]:
    runtime_imports = try_import_yolo_runtime()
    if runtime_imports.ultralytics is None:
        return {
            "status": "unavailable",
            "message": "Ultralytics runtime is unavailable; model metadata probe skipped.",
            "missing_packages": list(runtime_imports.missing_packages),
            "device": device,
        }

    try:
        yolo_factory = runtime_imports.ultralytics.YOLO
        model = yolo_factory(str(weights_path))
        names = _normalize_model_names(getattr(model, "names", None))
        return {
            "status": "ok",
            "device": device,
            "model_class": model.__class__.__name__,
            "task": getattr(model, "task", None),
            "class_names": names,
            "number_of_classes": len(names) if names is not None else None,
            "ultralytics_version": _module_version(runtime_imports.ultralytics),
            "torch_version": _module_version(runtime_imports.torch),
        }
    except Exception as exc:
        return {
            "status": "error",
            "message": f"YOLO model metadata probe failed: {exc}",
            "device": device,
        }


def _invalid_path(
    original_path: str,
    resolved_path: Path,
    suffix: str | None,
    required_sha256: str | None,
    message: str,
    raise_on_error: bool,
) -> YoloWeightsValidationResult:
    size_bytes = resolved_path.stat().st_size if resolved_path.is_file() else None
    return _result_or_raise(
        YoloWeightsValidationResult(
            weights_path=original_path,
            resolved_path=str(resolved_path),
            exists=resolved_path.exists(),
            is_file=resolved_path.is_file(),
            suffix=suffix,
            size_bytes=size_bytes,
            sha256=None,
            required_sha256=required_sha256,
            sha256_matches=None,
            status="invalid_path",
            message=message,
        ),
        raise_on_error,
    )


def _result_or_raise(
    result: YoloWeightsValidationResult,
    raise_on_error: bool,
) -> YoloWeightsValidationResult:
    if raise_on_error and result.status != "ok":
        raise YoloWeightsValidationError(result)
    return result


def _is_within_allowed_roots(path: Path, allowed_roots: Sequence[str | Path]) -> bool:
    resolved_roots = [Path(root).expanduser().resolve(strict=False) for root in allowed_roots]
    return any(path == root or root in path.parents for root in resolved_roots)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _normalize_model_names(names: Any) -> list[str] | None:
    if names is None:
        return None
    if isinstance(names, Mapping):
        return [str(name) for _, name in sorted(names.items(), key=lambda item: int(item[0]))]
    if isinstance(names, list | tuple):
        return [str(name) for name in names]
    return [str(names)]


def _module_version(module: Any | None) -> str | None:
    if module is None:
        return None
    version = getattr(module, "__version__", None)
    return str(version) if version is not None else None
