from sqlalchemy.orm import Session
from tom_v3_observations.synthetic import BASELINE_SCENARIO_NAME

from apps.worker.pipelines.synthetic_seed import seed_synthetic_run


def build_synthetic_run(
    session: Session,
    scenario_name: str = BASELINE_SCENARIO_NAME,
    source_uri: str | None = None,
    run_name: str | None = None,
    reuse_media: bool = False,
) -> dict[str, object]:
    return seed_synthetic_run(
        session=session,
        scenario_name=scenario_name,
        source_uri=source_uri,
        run_name=run_name,
        reuse_media=reuse_media,
    )
