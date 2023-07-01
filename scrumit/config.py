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
        env_prefix = "SCRUMIT_"

    openai_api_key: str = Field(
        None, env="OPENAI_API_KEY", description="Openai API key. Required if using OpenAI backend."
    )
    recognizer_examples_json: str = Field(
        None,
        env="EXAMPLES_JSON",
        description="Path to the examples JSON file."
        "This file contains the examples of"
        "how the tasks should be recognized."
        "It could help to polish the results of"
        "the NER to your specific domain/use-case.",
    )
    paraphraser_examples_json: str = Field(
        None,
        env="PARAPHRASER_EXAMPLES_JSON",
        description="Path to the examples JSON file."
        "This file contains the examples of"
        "how the tasks should be paraphrased."
        "It could help to polish the results of"
        "the paraphraser to your specific domain/use-case.",
    )
    default_recognizer_examples_json: str = os.path.join(BASE_DIR, "default_recognizer_examples.json")
    default_paraphraser_examples_json: str = os.path.join(BASE_DIR, "default_paraphraser_examples.json")

    default_paraphraser_prompt_template_wo_ex: str = Field(
        'Paraphrase the following text into a scrum story:\n"%s" \n\n',
        description="Default prompt template for the paraphraser when used without examples.",
    )
    default_paraphraser_prompt_template_w_ex = Field(
        "Paraphrase the following text into a scrum story " 'like this examples:\n%s \n\n Original text: "%s"\n',
        description="Default prompt template for the paraphraser when used with examples.",
    )
    paraphraser_prompt_template_w_ex: str = Field(
        None,
        env="PARAPHRASER_PROMPT_TEMPLATE_W_EX",
        description="Prompt template for the paraphraser when used with examples.",
    )
    paraphraser_prompt_template_wo_ex: str = Field(
        None,
        env="PARAPHRASER_PROMPT_TEMPLATE_WO_EX",
        description="Prompt template for the paraphraser when used without examples.",
    )


settings = Config()
