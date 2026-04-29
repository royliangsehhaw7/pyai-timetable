from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from pydantic_ai.providers.google import GoogleProvider

from pydantic_ai.models.openai import OpenAIChatModel, OpenAIChatModelSettings
from pydantic_ai.providers.openai import OpenAIProvider

class LLMFactory():
    def __init__(self, model_name: str, api_key: str):
        self._model_name = model_name
        self._api_key = api_key

    def get_gemini_model(self, model_name: str, api_key: str):
        model = GoogleModel(
            model_name = model_name,
            provider = GoogleProvider(
                api_key=api_key
            ),
            settings=GoogleModelSettings(
                temperature=0,
                max_tokens = 4096
            )
        )

        return model

    def get_openrouter_model(self, model_name: str, api_key: str):
        model = OpenAIChatModel(
            model_name = model_name,
            provider = OpenAIProvider(
                api_key=api_key,
                base_url  = ""
            ),
            settings = OpenAIChatModelSettings(
                temperature=0,
                max_tokens = 4096
            )
        )
        
        return model