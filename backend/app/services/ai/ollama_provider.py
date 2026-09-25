import httpx

from app.core.config import settings

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

            raise AIProviderError(
                "Ollama AI provider unavailable."
            ) from exc


        generated_text = (
            data.get("response", "")
            .strip()
        )

        if not generated_text:
            raise AIProviderError(
                "AI provider returned "
                "an empty response."
            )


        return generated_text