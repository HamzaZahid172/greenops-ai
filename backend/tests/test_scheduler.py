from datetime import (
    UTC,
    datetime,
    timedelta,
)

from app.schemas.carbon import (
    CarbonIntensityPoint,
)

from app.services.carbon.scheduler import (
    find_best_carbon_window,
)


def build_forecast(
    values: list[int],
):
    start = datetime(
        2026,
        9,
        25,
        18,
        0,
        tzinfo=UTC,
    )

    points = []

    for index, value in enumerate(values):

        from_time = (
            start
            + timedelta(
                minutes=index * 30
            )
        )

        to_time = (
            from_time
            + timedelta(minutes=30)
        )

        points.append(
            CarbonIntensityPoint(
                from_time=from_time,
                to_time=to_time,
                forecast=value,
                actual=None,
                index="moderate",
            )
        )

    return points


def test_scheduler_finds_lower_carbon_window():

    forecast = build_forecast(
        [
            220,
            210,
            200,
            190,
            160,
            140,
            100,
            90,
            80,
            85,
        ]
    )

    result = find_best_carbon_window(
        workload_name="Batch Job",
        forecast_points=forecast,
        runtime_minutes=60,
        max_delay_hours=4,
    )

    assert (
        result.optimization_available
        is True
    )

    assert (
        result.recommended_window
        .average_intensity
        <
        result.current_window
        .average_intensity
    )

    assert result.reduction_percent > 0


def test_scheduler_keeps_current_window_when_best():

    forecast = build_forecast(
        [
            80,
            90,
            120,
            150,
            180,
            200,
        ]
    )

    result = find_best_carbon_window(
        workload_name="Batch Job",
        forecast_points=forecast,
        runtime_minutes=60,
        max_delay_hours=2,
    )

    assert (
        result.optimization_available
        is False
    )

    assert result.reduction_percent == 0