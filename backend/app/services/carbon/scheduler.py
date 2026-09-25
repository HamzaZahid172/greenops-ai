import math

from app.schemas.carbon import CarbonIntensityPoint

from app.schemas.scheduler import (
    CarbonScheduleResponse,
    ScheduleWindow,
)


def _average_intensity(
    points: list[CarbonIntensityPoint],
) -> float:

    values = [
        point.forecast
        for point in points
    ]

    return sum(values) / len(values)


def find_best_carbon_window(
    workload_name: str,
    forecast_points: list[CarbonIntensityPoint],
    runtime_minutes: int,
    max_delay_hours: int,
) -> CarbonScheduleResponse:

    if not forecast_points:
        raise ValueError(
            "Carbon forecast is empty."
        )

    slot_minutes = 30

    required_slots = math.ceil(
        runtime_minutes / slot_minutes
    )

    maximum_start_slots = (
        max_delay_hours * 60
    ) // slot_minutes

    if len(forecast_points) < required_slots:
        raise ValueError(
            "Not enough forecast data "
            "for requested runtime."
        )

    current_points = forecast_points[
        :required_slots
    ]

    current_average = _average_intensity(
        current_points
    )

    current_window = ScheduleWindow(
        start_time=current_points[0].from_time,
        end_time=current_points[-1].to_time,
        average_intensity=round(
            current_average,
            2,
        ),
    )

    best_points = current_points

    max_start_index = min(
        maximum_start_slots,
        len(forecast_points)
        - required_slots,
    )

    for start_index in range(
        max_start_index + 1
    ):

        candidate = forecast_points[
            start_index:
            start_index + required_slots
        ]

        candidate_average = (
            _average_intensity(candidate)
        )

        best_average = (
            _average_intensity(best_points)
        )

        if candidate_average < best_average:
            best_points = candidate

    recommended_average = (
        _average_intensity(best_points)
    )

    recommended_window = ScheduleWindow(
        start_time=best_points[0].from_time,
        end_time=best_points[-1].to_time,
        average_intensity=round(
            recommended_average,
            2,
        ),
    )

    if current_average == 0:
        reduction_percent = 0.0
    else:
        reduction_percent = (
            (
                current_average
                - recommended_average
            )
            / current_average
            * 100
        )

    reduction_percent = round(
        max(0, reduction_percent),
        2,
    )

    optimization_available = (
        recommended_window.start_time
        != current_window.start_time
        and reduction_percent > 0
    )

    if optimization_available:
        message = (
            "A lower-carbon execution window "
            "is available within the allowed "
            "delay period."
        )
    else:
        message = (
            "The current execution window is "
            "already the best option within "
            "the allowed delay period."
        )

    return CarbonScheduleResponse(
        workload_name=workload_name,
        current_window=current_window,
        recommended_window=recommended_window,
        reduction_percent=reduction_percent,
        optimization_available=(
            optimization_available
        ),
        message=message,
    )