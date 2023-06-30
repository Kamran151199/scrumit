"""
This module contains the configuration class for the scrumit application.
"""
import os
from pathlib import Path

from pydantic import BaseSettings
from pydantic.fields import Field

BASE_DIR = Path(__file__).resolve().parent


class Config(BaseSettings):
    """
    This class contains the configuration for the scrumit application.
    """

    class Config:
        env_file_encoding = "utf-8"

    openai_api_key: str = Field(..., env="OPENAI_API_KEY", description="Openai API key")
    examples_json: str = Field(
        None,
        env="SCRUMIT_EXAMPLES_JSON",
        description="Path to the examples JSON file."
        "This file contains the examples of"
        "how the tasks should be recognized."
        "It could help to polish the results of"
        "the NER to your specific domain/use-case.",
    )
    default_examples_json: str = os.path.join(BASE_DIR, "default_examples.json")


settings = Config()
