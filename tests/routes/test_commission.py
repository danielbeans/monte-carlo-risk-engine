"""
! TODO:
    - Add redis_rq service mock called once with the correct arguments
"""

import json
from unittest import mock

import pytest
import pytest_mock
import rq.job
from fastapi import status
from fastapi import testclient

from mcengine.db import redis_rq

@pytest.fixture
def sample_commission_request() -> dict:
    return {
        "num_reps": 10,
        "num_simulations": 100,
        "pct_to_target_mean": 1.0,
        "pct_to_target_std": 0.1,
        "sales_target_values": [75_000, 100_000, 200_000],
        "sales_target_probabilities": [0.3, 0.4, 0.3],
    }


@pytest.fixture
def sample_commission_result() -> dict:
    return {
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


def test_enqueue_commission_simulation(
    client: testclient.TestClient,
    sample_commission_request: dict,
    mocker: pytest_mock.MockerFixture,
) -> None:
    redis_rq_service = mocker.patch.object(redis_rq, "RedisRQService")
    response = client.post("/commission/simulate", json=sample_commission_request)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "job_id" in data
    assert isinstance(data["job_id"], str)


def test_enqueue_commission_simulation__invalid_num_reps_negative(
    client: testclient.TestClient,
) -> None:
    invalid_request = {
        "num_reps": -1,
        "num_simulations": 100,
    }
    
    response = client.post("/commission/simulate", json=invalid_request)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_enqueue_commission_simulation__probabilities_sum_not_1(
    client: testclient.TestClient,
) -> None:
    invalid_request = {
        "num_reps": 10,
        "num_simulations": 100,
        "sales_target_values": [75_000, 100_000],
        "sales_target_probabilities": [0.3, 0.5],  # Sums to 0.8, not 1.0
    }
    
    response = client.post("/commission/simulate", json=invalid_request)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
