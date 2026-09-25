from abc import ABC, abstractmethod


class AIProviderError(RuntimeError):
    pass


class AIProvider(ABC):

    @abstractmethod
    async def generate(
        self,
        prompt: str,
    ) -> str:
        raise NotImplementedError