from __future__ import annotations

from tom_v3_model_adapters.detection import YoloDetectionAdapter
from tom_v3_model_adapters.yolo_normalization import (
    build_detection_adapter_result_from_normalized,
    normalize_yolo_frame_result,
    normalize_yolo_results,
)
from tom_v3_model_adapters.yolo_weights import default_yolo_class_mapping


def base_frame_result(boxes: list[dict[str, object]]) -> dict[str, object]:
    return {
        "frame_number": 120,
        "timestamp_ms": 4000,
        "image_width": 1920,
        "image_height": 1080,
        "boxes": boxes,
    }


def test_sports_ball_maps_to_ball_detection() -> None:
    result = normalize_yolo_frame_result(
        base_frame_result(
            [
                {
                    "xyxy": [100.0, 200.0, 140.0, 240.0],
                    "confidence": 0.91,
                    "class_id": 32,
                    "class_name": "sports ball",
                    "source_result_index": 0,
                }
            ]
        )
    )

    detection = result.detections[0]
    assert detection.observation_type == "ball_detection"
    assert detection.target_label == "ball"
    assert detection.class_id == 32
    assert detection.class_label == "sports ball"


def test_person_maps_to_player_detection_unknown_player() -> None:
    result = normalize_yolo_frame_result(
        base_frame_result(
            [
                {
                    "xyxy": [500.0, 150.0, 700.0, 900.0],
                    "confidence": 0.87,
                    "class_id": 0,
                    "class_name": "person",
                }
            ]
        )
    )

    detection = result.detections[0]
    assert detection.observation_type == "player_detection"
    assert detection.target_label == "player_unknown"


def test_near_and_far_player_only_appear_from_explicit_mappings() -> None:
    result = normalize_yolo_frame_result(
        base_frame_result(
            [
                {
                    "xyxy": [100.0, 100.0, 200.0, 500.0],
                    "confidence": 0.75,
                    "class_id": 10,
                    "class_name": "near_player",
                },
                {
                    "xyxy": [300.0, 120.0, 380.0, 420.0],
                    "confidence": 0.73,
                    "class_id": 11,
                    "class_name": "far_player",
                },
            ]
        )
    )

    assert [detection.target_label for detection in result.detections] == [
        "near_player",
        "far_player",
    ]


def test_mapping_by_class_id_works() -> None:
    class_mapping = {
        "custom_ball": {
            "source_class_names": [],
            "source_class_ids": [99],
            "target_observation_type": "ball_detection",
            "target_label": "ball",
        }
    }

    result = normalize_yolo_frame_result(
        base_frame_result(
            [
                {
                    "xyxy": [10.0, 20.0, 30.0, 60.0],
                    "confidence": 0.9,
                    "class_id": 99,
                    "class_name": "custom object",
                }
            ]
        ),
        class_mapping=class_mapping,
    )

    assert result.mapped_detection_count == 1
    assert result.detections[0].observation_type == "ball_detection"


def test_class_name_matching_is_case_insensitive_and_normalized() -> None:
    result = normalize_yolo_frame_result(
        base_frame_result(
            [
                {
                    "xyxy": [10.0, 20.0, 30.0, 60.0],
                    "confidence": 0.9,
                    "class_id": 1,
                    "class_name": "Sports_Ball",
                }
            ]
        )
    )

    assert result.mapped_detection_count == 1
    assert result.detections[0].target_label == "ball"


def test_unmapped_class_is_counted_but_not_emitted() -> None:
    result = normalize_yolo_frame_result(
        base_frame_result(
            [
                {
                    "xyxy": [10.0, 20.0, 30.0, 60.0],
                    "confidence": 0.9,
                    "class_id": 13,
                    "class_name": "chair",
                }
            ]
        )
    )

    assert result.detections == []
    assert result.unmapped_detection_count == 1
    assert result.unmapped_classes == [
        {"class_id": 13, "class_name": "chair", "source_result_index": 0}
    ]


def test_xyxy_converts_to_bbox_and_center() -> None:
    result = normalize_yolo_frame_result(
        base_frame_result(
            [
                {
                    "xyxy": [100.0, 200.0, 140.0, 240.0],
                    "confidence": 0.91,
                    "class_id": 32,
                    "class_name": "sports ball",
                }
            ]
        )
    )

    detection = result.detections[0]
    assert detection.bbox == {"x": 100.0, "y": 200.0, "width": 40.0, "height": 40.0}
    assert detection.center == {"x": 120.0, "y": 220.0}


def test_invalid_bbox_is_skipped_with_warning() -> None:
    result = normalize_yolo_frame_result(
        base_frame_result(
            [
                {
                    "xyxy": [140.0, 240.0, 100.0, 200.0],
                    "confidence": 0.91,
                    "class_id": 32,
                    "class_name": "sports ball",
                }
            ]
        )
    )

    assert result.detections == []
    assert result.warnings[0]["warning_type"] == "invalid_bbox"


def test_non_numeric_confidence_is_skipped_with_warning() -> None:
    result = normalize_yolo_frame_result(
        base_frame_result(
            [
                {
                    "xyxy": [100.0, 200.0, 140.0, 240.0],
                    "confidence": "not-a-number",
                    "class_id": 32,
                    "class_name": "sports ball",
                }
            ]
        )
    )

    assert result.detections == []
    assert result.warnings[0]["warning_type"] == "invalid_confidence"


def test_out_of_range_confidence_warns_but_keeps_detection() -> None:
    result = normalize_yolo_frame_result(
        base_frame_result(
            [
                {
                    "xyxy": [100.0, 200.0, 140.0, 240.0],
                    "confidence": 1.2,
                    "class_id": 32,
                    "class_name": "sports ball",
                }
            ]
        )
    )

    assert result.mapped_detection_count == 1
    assert result.warnings[0]["warning_type"] == "confidence_out_of_range"


def test_normalization_summary_counts_input_mapped_and_unmapped() -> None:
    result = normalize_yolo_frame_result(
        base_frame_result(
            [
                {
                    "xyxy": [100.0, 200.0, 140.0, 240.0],
                    "confidence": 0.91,
                    "class_id": 32,
                    "class_name": "sports ball",
                },
                {
                    "xyxy": [10.0, 20.0, 30.0, 60.0],
                    "confidence": 0.9,
                    "class_id": 13,
                    "class_name": "chair",
                },
            ]
        )
    )

    assert result.input_box_count == 2
    assert result.mapped_detection_count == 1
    assert result.unmapped_detection_count == 1


def test_normalized_payload_includes_frame_time_and_runtime_metadata() -> None:
    result = normalize_yolo_frame_result(
        base_frame_result(
            [
                {
                    "xyxy": [100.0, 200.0, 140.0, 240.0],
                    "confidence": 0.91,
                    "class_id": 32,
                    "class_name": "sports ball",
                    "source_result_index": 7,
                }
            ]
        ),
        model_registry_id="model-1",
        runtime_config_id="config-1",
        inference_metadata={"imgsz": 640, "conf": 0.25, "iou": 0.7, "device": "cpu"},
    )

    detection = result.detections[0]
    assert detection.frame_number == 120
    assert detection.timestamp_ms == 4000
    assert detection.frame_time_owner == "media_indexing"
    assert detection.source_runtime == "ultralytics_yolo"
    assert detection.metadata["model_registry_id"] == "model-1"
    assert detection.metadata["runtime_config_id"] == "config-1"
    assert detection.metadata["inference"]["device"] == "cpu"
    assert detection.source_result_index == 7


def test_adapter_result_conversion_matches_detection_contract() -> None:
    normalized = normalize_yolo_frame_result(
        base_frame_result(
            [
                {
                    "xyxy": [100.0, 200.0, 140.0, 240.0],
                    "confidence": 0.91,
                    "class_id": 32,
                    "class_name": "sports ball",
                }
            ]
        )
    )

    result = build_detection_adapter_result_from_normalized(normalized)

    assert result.adapter_name == "ultralytics-yolo-detection-normalizer"
    assert result.detections[0].label == "ball"
    assert result.detections[0].bbox.as_dict() == {
        "x": 100.0,
        "y": 200.0,
        "width": 40.0,
        "height": 40.0,
    }


def test_yolo_adapter_skeleton_can_normalize_fake_frame_results() -> None:
    adapter = YoloDetectionAdapter(model_path="model_assets/yolo/fake.pt", device="cpu")

    normalized = adapter.normalize_frame_result(
        base_frame_result(
            [
                {
                    "xyxy": [500.0, 150.0, 700.0, 900.0],
                    "confidence": 0.87,
                    "class_id": 0,
                    "class_name": "person",
                }
            ]
        ),
        class_mapping=default_yolo_class_mapping(),
    )
    adapter_result = adapter.build_adapter_result_from_normalized(normalized)

    assert normalized.mapped_detection_count == 1
    assert adapter_result.detections[0].label == "player_unknown"


def test_multiple_frame_results_aggregate_counts() -> None:
    result = normalize_yolo_results(
        [
            base_frame_result(
                [
                    {
                        "xyxy": [100.0, 200.0, 140.0, 240.0],
                        "confidence": 0.91,
                        "class_id": 32,
                        "class_name": "sports ball",
                    }
                ]
            ),
            {
                "frame_number": 121,
                "timestamp_ms": 4033,
                "boxes": [
                    {
                        "xyxy": [10.0, 20.0, 30.0, 60.0],
                        "confidence": 0.9,
                        "class_id": 13,
                        "class_name": "chair",
                    }
                ],
            },
        ]
    )

    assert result.input_box_count == 2
    assert result.mapped_detection_count == 1
    assert result.unmapped_detection_count == 1
