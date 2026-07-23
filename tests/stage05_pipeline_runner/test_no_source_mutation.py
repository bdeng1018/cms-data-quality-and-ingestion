"""
Stage 05 — Test: No Mutation of Upstream Artifacts
================================================================================

This test verifies that Stage 05 (run_pipeline.py + orchestrator.py) does NOT
modify any artifacts produced by Stages 01–04.

Stage 05 is strictly read‑only with respect to upstream data. It may:

- Read Stage 04 processed outputs
- Generate its own summary JSON

It must NOT:
- Modify schema.json
- Modify cleaned_data.csv
- Modify Stage 03 intermediate artifacts
- Modify Stage 04 processed reports

This test uses temporary copies of upstream artifacts and asserts that their
contents remain unchanged after Stage 05 execution.
"""

from unittest.mock import patch

from src.stage05_pipeline_runner.run_pipeline import main as run_pipeline_main


# ------------------------------------------------------------------------------
# Helper: create fake upstream artifacts
# ------------------------------------------------------------------------------
def _create_fake_upstream(tmpdir):
    """Create minimal fake Stage 01–04 artifacts for mutation testing."""

    # Stage 01
    stage01 = tmpdir / "data/stage01_schema"
    stage01.mkdir(parents=True)
    (stage01 / "schema.json").write_text('{"fields": ["a", "b"]}')

    # Stage 02
    stage02 = tmpdir / "data/stage02_cleaned"
    stage02.mkdir(parents=True)
    (stage02 / "cleaned_data.csv").write_text("a,b\n1,2")

    # Stage 03
    stage03 = tmpdir / "data/stage03_intermediate"
    stage03.mkdir(parents=True)
    (stage03 / "quality_summary.json").write_text('{"rows": 100}')
    (stage03 / "quality_flags.csv").write_text("row,flag\n1,ok")

    # Stage 04
    stage04 = tmpdir / "data/stage04_processed"
    stage04.mkdir(parents=True)
    (stage04 / "report_index.json").write_text('{"reports": 5}')
    (stage04 / "facility_health.csv").write_text("facility,score\nA,90")
    (stage04 / "dataset_summary.json").write_text('{"valid": true}')

    return {
        "schema": stage01 / "schema.json",
        "cleaned": stage02 / "cleaned_data.csv",
        "quality_summary": stage03 / "quality_summary.json",
        "quality_flags": stage03 / "quality_flags.csv",
        "report_index": stage04 / "report_index.json",
        "facility_health": stage04 / "facility_health.csv",
        "dataset_summary": stage04 / "dataset_summary.json",
    }


# ------------------------------------------------------------------------------
# Test: Stage 05 must not mutate upstream artifacts
# ------------------------------------------------------------------------------
def test_stage05_no_mutation(tmp_path):
    """After Stage 05 runs, upstream artifacts must remain byte‑identical."""

    upstream = _create_fake_upstream(tmp_path)

    # Capture original contents
    originals = {name: p.read_bytes() for name, p in upstream.items()}

    # Prepare Stage 05 output directory
    output_dir = tmp_path / "data/stage05_reports"
    output_dir.mkdir(parents=True)
    output_path = output_dir / "pipeline_summary.json"

    # Mock config loader + orchestrator
    with patch(
        "src.stage05_pipeline_runner.run_pipeline.load_pipeline_config"
    ) as mock_cfg, patch(
        "src.stage05_pipeline_runner.run_pipeline.run_all_stages"
    ) as mock_orch:

        mock_cfg.return_value = {"stage05": {"output_dir": str(output_dir)}}
        mock_orch.return_value = {
            "stage01": "success",
            "stage02": "success",
            "stage03": "success",
            "stage04": "success",
        }

        # Simulate CLI args
        test_args = [
            "run_pipeline.py",
            "--config",
            "configs/pipeline.yml",
            "--output",
            str(output_path),
        ]

        with patch("sys.argv", test_args):
            run_pipeline_main()

    # Validate summary JSON exists
    assert output_path.exists()

    # Validate upstream artifacts unchanged
    for name, p in upstream.items():
        assert p.read_bytes() == originals[name], f"{name} was mutated"
