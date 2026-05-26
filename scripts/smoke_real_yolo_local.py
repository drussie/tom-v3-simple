from __future__ import annotations

import argparse
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tom_v3_storage.db_models import Base

from apps.worker.config import settings
from apps.worker.services.real_yolo_smoke import run_real_yolo_local_smoke


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run or plan the optional TOM v3 real-YOLO local smoke path."
    )
    parser.add_argument("--source-path")
    parser.add_argument("--weights-path")
    parser.add_argument("--model-name", default="local-yolo-smoke")
    parser.add_argument("--model-version", default="local-v0")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--frame-sample-rate", type=int, default=30)
    parser.add_argument("--max-frames", type=int, default=3)
    parser.add_argument("--output-root", default=".data/artifacts")
    parser.add_argument("--allowed-root", action="append", dest="allowed_roots")
    parser.add_argument(
        "--copy-to-storage",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument(
        "--run-tracklets",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "--output-debug-artifact",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--skip-create-db", action="store_true")
    args = parser.parse_args()

    connect_args = {}
    if settings.database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    engine = create_engine(settings.database_url, connect_args=connect_args, future=True)
    if not args.skip_create_db:
        Base.metadata.create_all(engine)
    session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
        future=True,
    )
    with session_factory() as session:
        result = run_real_yolo_local_smoke(
            session=session,
            source_path=args.source_path,
            weights_path=args.weights_path,
            model_name=args.model_name,
            model_version=args.model_version,
            device=args.device,
            frame_sample_rate=args.frame_sample_rate,
            max_frames=args.max_frames,
            output_root=args.output_root,
            allowed_roots=args.allowed_roots,
            copy_to_storage=args.copy_to_storage,
            run_tracklets=args.run_tracklets,
            output_debug_artifact=args.output_debug_artifact,
            plan_only=args.plan_only,
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result.get("status") == "failed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
