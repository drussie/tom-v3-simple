from sqlalchemy.orm import Session
from tom_v3_observations.synthetic import BASELINE_SCENARIO_NAME, create_synthetic_run

from apps.worker.scenarios.baseline_tennis_clip import build_scenario


def seed_synthetic_run(
    session: Session,
    scenario_name: str = BASELINE_SCENARIO_NAME,
    source_uri: str | None = None,
    run_name: str | None = None,
    reuse_media: bool = False,
) -> dict[str, object]:
    if scenario_name != BASELINE_SCENARIO_NAME:
        raise ValueError(f"unknown synthetic scenario: {scenario_name}")
    scenario = build_scenario(source_uri=source_uri, run_name=run_name)
    return create_synthetic_run(session=session, scenario=scenario, reuse_media=reuse_media)
