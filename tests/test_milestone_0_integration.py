from scripts.smoke_synthetic_viewer_data import run_smoke


def test_milestone_0_synthetic_viewer_smoke(tmp_path) -> None:
    database_url = f"sqlite+pysqlite:///{tmp_path / 'milestone_0_smoke.db'}"
    result = run_smoke(database_url)

    assert result["ok"] is True
    assert all(result["checks"].values())
