import dotenv
from autogen import LLMConfig
from pydantic import Field, AliasChoices, computed_field
from pydantic_settings import BaseSettings

dotenv.load_dotenv()


class Config(BaseSettings):
    model: str = Field(
        ...,
        description="The model to use for LLM requests.",
        validation_alias=AliasChoices("MODEL", "model", "OPENAI_MODEL", "AZURE_OPENAI_MODEL"),
        frozen=False,
        deprecated=False,
    )
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

    @computed_field
    @property
    def llm_config(self) -> LLMConfig:
        if self.api_type == "azure":
            llm_config = LLMConfig(
                model=self.model,
                api_key=self.api_key,
                base_url=self.base_url,
                api_version="2025-04-01-preview",
                api_type=self.api_type,
                default_headers={"X-User-Id": "srv_dvc_tma001"},
            )
        elif self.api_type == "openai":
            llm_config = LLMConfig(
                model=self.model,
                api_key=self.api_key,
                base_url=self.base_url,
                api_type=self.api_type,
            )
        else:
            raise ValueError(f"Unsupported API type: {self.api_type}")
        return llm_config
