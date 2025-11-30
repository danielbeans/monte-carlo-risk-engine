"""
! TODO:
    - Test that the result is cached in Redis and saved to PostgreSQL
"""

import json
from unittest import mock

import pytest
import pytest_mock

from mcengine.tasks import commission

def test_process_commission_simulation(
    mocker: pytest_mock.MockerFixture,
) -> None:
    job_id = "test-job-id"
    request = {
        "num_reps": 10,
        "num_simulations": 100,
        "pct_to_target_mean": 1.0,
        "pct_to_target_std": 0.1,
        "sales_target_values": [75_000, 100_000],
        "sales_target_probabilities": [0.5, 0.5],
    }
    
    expected_result = {
        "num_reps": 10,
        "num_simulations": 100,
        "mean_total_sales": 1000000.0,
        "mean_total_commissions": 20000.0,
        "mean_total_targets": 1000000.0,
        "std_total_sales": 50000.0,
        "std_total_commissions": 2000.0,
        "min_total_commissions": 15000.0,
        "max_total_commissions": 25000.0,
        "p25_commissions": 18000.0,
        "p50_commissions": 20000.0,
        "p75_commissions": 22000.0,
        "started_at": 1234567890.0,
        "completed_at": 1234567900.0,
    }
    
    mock_run_simulation = mocker.patch.object(commission.services.commission, "run_commission_simulation")
    mock_run_simulation.return_value = expected_result

    result = commission.process_commission_simulation(job_id, request)
    
    assert result == expected_result
    mock_run_simulation.assert_called_once_with(request)
