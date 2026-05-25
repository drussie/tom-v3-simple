from tom_v3_observations.synthetic import SyntheticScenario, baseline_tennis_clip_scenario


def build_scenario(
    source_uri: str | None = None,
    run_name: str | None = None,
) -> SyntheticScenario:
    return baseline_tennis_clip_scenario(source_uri=source_uri, run_name=run_name)
