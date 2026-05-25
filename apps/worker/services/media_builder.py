from sqlalchemy.orm import Session
from tom_v3_observations.synthetic import SyntheticScenario, seed_synthetic_run


def seed_media_backed_scenario(
    session: Session,
    scenario: SyntheticScenario,
    reuse_media: bool = False,
) -> dict[str, object]:
    return seed_synthetic_run(session=session, scenario=scenario, reuse_media=reuse_media)
