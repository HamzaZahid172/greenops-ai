from abc import ABC, abstractmethod

from app.schemas.carbon import (
    CarbonCurrentResponse,
    CarbonForecastResponse,
)


class CarbonProviderError(RuntimeError):
    pass


class CarbonProvider(ABC):

    @abstractmethod
    async def get_current(
        self,
    ) -> CarbonCurrentResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_forecast(
        self,
    ) -> CarbonForecastResponse:
        raise NotImplementedError