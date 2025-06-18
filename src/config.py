from pydantic import Field, AliasChoices
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    api_type: str = Field(
        default="openai",
        description="The type of API to use for LLM requests. Options: 'openai', 'azure', etc.",
        validation_alias=AliasChoices("API_TYPE", "api_type"),
        frozen=False,
        deprecated=False,
    )
    base_url: str = Field(
        default="https://api.openai.com/v1",
        description="Base URL for the LLM API.",
        validation_alias=AliasChoices(
            "BASE_URL", "base_url", "OPENAI_BASE_URL", "AZURE_ENDPOINT_URL"
        ),
        frozen=False,
        deprecated=False,
    )
    api_key: str = Field(
        ...,
        description="API key for authenticating with the LLM service.",
        validation_alias=AliasChoices(
            "API_KEY", "api_key", "OPENAI_API_KEY", "AZURE_OPENAI_API_KEY"
        ),
        frozen=False,
        deprecated=False,
    )
