import time
from typing import Self

import pydantic

from mcengine.schemas.core import BaseRequest, BaseResponse


class CommissionSimulationRequest(BaseRequest):
    num_reps: int = pydantic.Field(
        ..., gt=0, description="Number of sales representatives"
    )
    num_simulations: int = pydantic.Field(
        default=1000, gt=0, le=100000, description="Number of Monte Carlo simulations to run"
    )
    # Percent to target distribution parameters
    pct_to_target_mean: float = pydantic.Field(
        default=1.0, description="Mean of percent to target (1.0 = 100%)"
    )
    pct_to_target_std: float = pydantic.Field(
        default=0.1, gt=0, description="Standard deviation of percent to target"
    )
    # Sales target distribution
    sales_target_values: list[float] = pydantic.Field(
        default=[75_000, 100_000, 200_000, 300_000, 400_000, 500_000],
        description="Possible sales target values",
    )
    sales_target_probabilities: list[float] = pydantic.Field(
        default=[0.3, 0.3, 0.2, 0.1, 0.05, 0.05],
        description="Probabilities for each sales target value (must sum to 1.0)",
    )

    @pydantic.model_validator(mode="after")
    def validate_probabilities(self) -> Self:
        total = sum(self.sales_target_probabilities)
        if not 0.99 <= total <= 1.01:
            raise ValueError(f"Probabilities must sum to 1.0, got {total}")
        if len(self.sales_target_probabilities) != len(self.sales_target_values):
            raise ValueError(
                "Number of probabilities must match number of sales target values"
            )
        return self


class CommissionSimulationResponse(BaseResponse):
    job_id: str = pydantic.Field(..., description="Unique job identifier")

class CommissionSimulationResultResponse(BaseResponse):
    num_reps: int = pydantic.Field(..., description="Number of sales representatives")
    num_simulations: int = pydantic.Field(..., description="Number of simulations run")
    # Statistics across all simulations
    mean_total_sales: float = pydantic.Field(
        ..., description="Mean total sales across simulations"
    )
    mean_total_commissions: float = pydantic.Field(
        ..., description="Mean total commissions across simulations"
    )
    mean_total_targets: float = pydantic.Field(
        ..., description="Mean total targets across simulations"
    )
    std_total_sales: float = pydantic.Field(
        ..., description="Standard deviation of total sales"
    )
    std_total_commissions: float = pydantic.Field(
        ..., description="Standard deviation of total commissions"
    )
    min_total_commissions: float = pydantic.Field(
        ..., description="Minimum total commissions observed"
    )
    max_total_commissions: float = pydantic.Field(
        ..., description="Maximum total commissions observed"
    )
    # Percentiles
    p25_commissions: float = pydantic.Field(
        ..., description="25th percentile of commissions"
    )
    p50_commissions: float = pydantic.Field(
        ..., description="50th percentile (median) of commissions"
    )
    p75_commissions: float = pydantic.Field(
        ..., description="75th percentile of commissions"
    )
    created_at: float = pydantic.Field(
        default_factory=time.time,
        description="Simulation creation time (Unix timestamp)",
    )
    started_at: float = pydantic.Field(
        ..., description="Simulation start time (Unix timestamp)"
    )
    completed_at: float = pydantic.Field(
        ..., description="Simulation completion time (Unix timestamp)"
    )