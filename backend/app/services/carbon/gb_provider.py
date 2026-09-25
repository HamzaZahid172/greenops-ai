import httpx

from app.core.config import settings

from app.schemas.carbon import (
    CarbonCurrentResponse,
    CarbonForecastResponse,
    CarbonIntensityPoint,
)

from app.services.carbon.base import (
    CarbonProvider,
    CarbonProviderError,
)


class GBCarbonIntensityProvider(CarbonProvider):

    provider_name = "NESO Carbon Intensity API"
    region_name = "Great Britain"
    unit = "gCO2/kWh"

    @staticmethod
    def _normalize_point(
        raw_point: dict,
    ) -> CarbonIntensityPoint:

        intensity = raw_point["intensity"]

        return CarbonIntensityPoint(
            from_time=raw_point["from"],
            to_time=raw_point["to"],
            forecast=intensity["forecast"],
            actual=intensity.get("actual"),
            index=intensity["index"],
        )

    async def get_current(
        self,
    ) -> CarbonCurrentResponse:

        url = (
            f"{settings.carbon_api_base_url}"
            "/intensity"
        )

        try:
            async with httpx.AsyncClient(
                timeout=10.0,
            ) as client:

                response = await client.get(url)

                response.raise_for_status()

                payload = response.json()

                raw_point = payload["data"][0]

                point = self._normalize_point(
                    raw_point,
                )

        except (
            httpx.HTTPError,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
        ) as exc:

            raise CarbonProviderError(
                "Unable to retrieve current carbon intensity."
            ) from exc

        return CarbonCurrentResponse(
            provider=self.provider_name,
            region=self.region_name,
            unit=self.unit,
            intensity=point,
        )

    async def get_forecast(
        self,
    ) -> CarbonForecastResponse:

        current = await self.get_current()

        start_time = (
            current.intensity.from_time
            .strftime("%Y-%m-%dT%H:%MZ")
        )

        url = (
            f"{settings.carbon_api_base_url}"
            f"/intensity/{start_time}/fw24h"
        )

        try:
            async with httpx.AsyncClient(
                timeout=10.0,
            ) as client:

                response = await client.get(url)

                response.raise_for_status()

                payload = response.json()

                points = [
                    self._normalize_point(item)
                    for item in payload["data"]
                ]

        except (
            httpx.HTTPError,
            KeyError,
            TypeError,
            ValueError,
        ) as exc:

            raise CarbonProviderError(
                "Unable to retrieve carbon forecast."
            ) from exc

        return CarbonForecastResponse(
            provider=self.provider_name,
            region=self.region_name,
            unit=self.unit,
            points=points,
        )