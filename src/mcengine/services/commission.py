# """Commission calculation Monte Carlo simulation logic.

# Based on: https://pbpython.com/monte-carlo.html
# """
import time

import numpy as np
from typing import Any


def run_commission_simulation(request: dict[str, Any]) -> dict[str, Any]:
    started_at = time.time()
    all_stats: list[tuple[float, float, float]] = []

    for _ in range(request["num_simulations"]):
        # TODO: Add multiprocessing for this
        stats = run_single_simulation(
            num_reps=request["num_reps"],
            pct_to_target_mean=request["pct_to_target_mean"],
            pct_to_target_std=request["pct_to_target_std"],
            sales_target_values=request["sales_target_values"],
            sales_target_probabilities=request["sales_target_probabilities"],
        )
        all_stats.append(stats)

    # Extract columns
    total_sales = [stats[0] for stats in all_stats]
    total_commissions = [stats[1] for stats in all_stats]
    total_targets = [stats[2] for stats in all_stats]

    # Calculate statistics
    commissions_array = np.array(total_commissions)
    sales_array = np.array(total_sales)

    return {
        "num_reps": request["num_reps"],
        "num_simulations": request["num_simulations"],
        "mean_total_sales": float(sales_array.mean()),
        "mean_total_commissions": float(commissions_array.mean()),
        "mean_total_targets": float(np.array(total_targets).mean()),
        "std_total_sales": float(sales_array.std()),
        "std_total_commissions": float(commissions_array.std()),
        "min_total_commissions": float(commissions_array.min()),
        "max_total_commissions": float(commissions_array.max()),
        "p25_commissions": float(np.percentile(commissions_array, 25)),
        "p50_commissions": float(np.percentile(commissions_array, 50)),
        "p75_commissions": float(np.percentile(commissions_array, 75)),
        "started_at": started_at,
        "completed_at": time.time()
    }


def run_single_simulation(
    num_reps: int,
    pct_to_target_mean: float,
    pct_to_target_std: float,
    sales_target_values: list[float],
    sales_target_probabilities: list[float],
) -> tuple[float, float, float]:
    """
    Run a single Monte Carlo simulation iteration.

    Returns:
        Tuple of (total_sales, total_commissions, total_targets)
    """
    # Generate random percent to target values (normal distribution)
    pct_to_target = np.random.normal(
        pct_to_target_mean, pct_to_target_std, num_reps
    ).round(2)

    # Generate random sales targets (weighted choice)
    sales_targets = np.random.choice(
        sales_target_values, size=num_reps, p=sales_target_probabilities
    )

    # Calculate actual sales
    sales = pct_to_target * sales_targets

    # Calculate commission rates and amounts
    commission_rates = np.array([calc_commission_rate(pct) for pct in pct_to_target])
    commission_amounts = commission_rates * sales

    # Sum totals
    total_sales = float(sales.sum())
    total_commissions = float(commission_amounts.sum())
    total_targets = float(sales_targets.sum())

    return total_sales, total_commissions, total_targets


def calc_commission_rate(pct_to_target: float) -> float:
    """
    Calculate commission rate based on percent to target.

    Commission tiers:
    - < 90%: 1%
    - 90-99%: 2%
    - 99-100%: 3%
    - > 100%: 4%
    """
    if pct_to_target < 0.90:
        return 0.01
    if pct_to_target < 0.99:
        return 0.02
    if pct_to_target <= 1.00:
        return 0.03
    return 0.04