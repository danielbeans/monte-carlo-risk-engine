import pytest

from mcengine.services import commission


@pytest.mark.parametrize(
    "request_data,expected_reps,expected_sims",
    [
        (
            {
                "num_reps": 5,
                "num_simulations": 10,
                "pct_to_target_mean": 1.0,
                "pct_to_target_std": 0.1,
                "sales_target_values": [75_000, 100_000, 200_000],
                "sales_target_probabilities": [0.3, 0.4, 0.3],
            },
            5,
            10,
        ),
        (
            {
                "num_reps": 10,
                "num_simulations": 100,
                "pct_to_target_mean": 1.0,
                "pct_to_target_std": 0.1,
                "sales_target_values": [100_000],
                "sales_target_probabilities": [1.0],
            },
            10,
            100,
        ),
        (
            {
                "num_reps": 20,
                "num_simulations": 50,
                "pct_to_target_mean": 0.95,
                "pct_to_target_std": 0.15,
                "sales_target_values": [50_000, 150_000, 250_000],
                "sales_target_probabilities": [0.5, 0.3, 0.2],
            },
            20,
            50,
        ),
    ],
)
def test_run_commission_simulation_basic(
    request_data: dict, expected_reps: int, expected_sims: int
) -> None:
    result = commission.run_commission_simulation(request_data)
    
    assert result["num_reps"] == expected_reps
    assert result["num_simulations"] == expected_sims
    assert "mean_total_sales" in result
    assert "mean_total_commissions" in result
    assert "mean_total_targets" in result
    assert "std_total_sales" in result
    assert "std_total_commissions" in result
    assert "min_total_commissions" in result
    assert "max_total_commissions" in result
    assert "p25_commissions" in result
    assert "p50_commissions" in result
    assert "p75_commissions" in result
    assert "started_at" in result
    assert "completed_at" in result
    assert result["completed_at"] >= result["started_at"]
    assert isinstance(result["mean_total_sales"], float)
    assert isinstance(result["mean_total_commissions"], float)


def test_run_commission_simulation_statistics() -> None:
    request = {
        "num_reps": 10,
        "num_simulations": 100,
        "pct_to_target_mean": 1.0,
        "pct_to_target_std": 0.1,
        "sales_target_values": [100_000],
        "sales_target_probabilities": [1.0],
    }
    
    result = commission.run_commission_simulation(request)
    
    assert result["mean_total_commissions"] >= 0
    assert result["min_total_commissions"] <= result["mean_total_commissions"]
    assert result["max_total_commissions"] >= result["mean_total_commissions"]
    assert result["p25_commissions"] <= result["p50_commissions"]
    assert result["p50_commissions"] <= result["p75_commissions"]


@pytest.mark.parametrize(
    "num_reps,pct_to_target_mean,pct_to_target_std,sales_target_values,sales_target_probabilities",
    [
        (5, 1.0, 0.1, [75_000, 100_000], [0.5, 0.5]),
        (10, 1.0, 0.05, [100_000], [1.0]),
    ],
)
def test_run_single_simulation(
    num_reps: int,
    pct_to_target_mean: float,
    pct_to_target_std: float,
    sales_target_values: list[float],
    sales_target_probabilities: list[float],
) -> None:
    result = commission.run_single_simulation(
        num_reps=num_reps,
        pct_to_target_mean=pct_to_target_mean,
        pct_to_target_std=pct_to_target_std,
        sales_target_values=sales_target_values,
        sales_target_probabilities=sales_target_probabilities,
    )
    
    assert isinstance(result, tuple)
    assert len(result) == 3
    total_sales, total_commissions, total_targets = result
    assert isinstance(total_sales, float)
    assert isinstance(total_commissions, float)
    assert isinstance(total_targets, float)
    assert total_sales >= 0
    assert total_commissions >= 0
    assert total_targets >= 0
    



@pytest.mark.parametrize(
    "pct_to_target,expected_rate",
    [
        # Below 90%
        (0.85, 0.01),
        (0.89, 0.01),
        (0.899, 0.01),
        # 90-99%
        (0.90, 0.02),
        (0.95, 0.02),
        (0.98, 0.02),
        (0.989, 0.02),
        # 99-100%
        (0.99, 0.03),
        (1.00, 0.03),
        # Above 100%
        (1.001, 0.04),
        (1.01, 0.04),
        (1.10, 0.04),
        (1.50, 0.04),
    ],
)
def test_calc_commission_rate(pct_to_target: float, expected_rate: float) -> None:
    assert commission.calc_commission_rate(pct_to_target) == expected_rate
