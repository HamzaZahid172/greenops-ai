import time

import httpx

from app.core.config import settings

from app.observability.metrics import (
    AI_ERRORS_TOTAL,
    AI_GENERATION_DURATION_SECONDS,
)

from app.services.ai.base import (
    AIProvider,
    AIProviderError,
)


class OllamaProvider(AIProvider):

    async def generate(
        self,
        prompt: str,
    ) -> str:

        url = (
            f"{settings.ollama_base_url}"
            "/api/generate"
        )

        payload = {
            "model": settings.ollama_model,
            "prompt": prompt,
            "stream": False,
        }

        started = time.perf_counter()

        try:
            async with httpx.AsyncClient(
                timeout=60.0,
            ) as client:

                response = await client.post(
                    url,
                    json=payload,
                )

                response.raise_for_status()

                data = response.json()

        except (
            httpx.HTTPError,
            ValueError,
        ) as exc:

            AI_ERRORS_TOTAL.labels(
                provider="ollama",
                operation="generate",
            ).inc()

            raise AIProviderError(
                "Ollama AI provider unavailable."
            ) from exc

        finally:
            duration = (
                time.perf_counter()
                - started
            )

            AI_GENERATION_DURATION_SECONDS.labels(
                provider="ollama",
                model=settings.ollama_model,
            ).observe(duration)


        generated_text = (
            data.get("response", "")
            .strip()
        )

        if not generated_text:

            AI_ERRORS_TOTAL.labels(
                provider="ollama",
                operation="empty_response",
            ).inc()

            raise AIProviderError(
                "AI provider returned "
                "an empty response."
            )

        return generated_text