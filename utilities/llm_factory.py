from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from pydantic_ai.providers.google import GoogleProvider

from pydantic_ai.models.openai import OpenAIChatModel, OpenAIChatModelSettings
from pydantic_ai.providers.openai import OpenAIProvider


class LLMFactory:
    def __init__(self, model_name: str, api_key: str, provider: str):
        self._model_name = model_name
        self._api_key = api_key
        self._provider = provider.lower()

    def create(self):
        if self._provider == "gemini":
            return self._create_gemini()
        elif self._provider == "openrouter":
            return self._create_openrouter()
        elif self._provider == "huggingface":
            return self._create_huggingface()
        else:
            raise ValueError(f"Unsupported provider: {self._provider}")

    # ---------------- GEMINI
    def _create_gemini(self):
        return GoogleModel(
            model_name=self._model_name,
            provider=GoogleProvider(api_key=self._api_key),
            settings=GoogleModelSettings(
                temperature=0,
                max_tokens=4096
            )
        )

    # ---------------- OPENROUTER
    def _create_openrouter(self):
        return OpenAIChatModel(
            model_name=self._model_name,
            provider=OpenAIProvider(
                api_key=self._api_key,
                base_url="https://openrouter.ai/api/v1"
            ),
            settings=OpenAIChatModelSettings(
                temperature=0,
                max_tokens=4096
            )
        )

    # ---------------- HUGGING FACE
    def _create_huggingface(self):
        return OpenAIChatModel(
            model_name=self._model_name,
            provider=OpenAIProvider(
                api_key=self._api_key,
                # ***** 
                # IMPORTANT: DO NOT USE base_url FOR HF
                # we are using native HF models *****
                # base_url="https://api-inference.huggingface.co/v1"
            ),
            settings=OpenAIChatModelSettings(
                temperature=0,
                max_tokens=4096
            )
        )