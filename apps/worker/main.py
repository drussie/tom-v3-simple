from sqlalchemy.orm import Session
from tom_v3_observations.synthetic import (
    BASELINE_SCENARIO_NAME,
    create_synthetic_run,
    verify_synthetic_run,
)


def seed_baseline_synthetic_run(
    session: Session,
    source_uri: str | None = None,
    run_name: str | None = None,
    reuse_media: bool = False,
) -> dict[str, object]:
    return create_synthetic_run(
        session=session,
        scenario=BASELINE_SCENARIO_NAME,
        source_uri=source_uri,
        run_name=run_name,
        reuse_media=reuse_media,
    )


def verify_seeded_run(session: Session, run_id: str) -> dict[str, object]:
    return verify_synthetic_run(session, run_id)
