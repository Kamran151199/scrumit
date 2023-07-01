"""
This module contains the entities for the Paraphraser service.
"""

from pydantic import BaseModel
from pydantic.fields import Field


class ParaphraserExample(BaseModel):
    """
    This class contains the example for the Paraphraser service.
    """

    original_text: str = Field(..., description="Original text - excerpt from the input text.")
    paraphrased_text: str = Field(..., description="Paraphrased text - converted user story.")


class ParaphraserInput(BaseModel):
    """
    This class contains the input for the scrumit application.
    """

    text: str = Field(..., description="Input text to be converted to user stories.")
    examples: list[ParaphraserExample] = Field(
        default_factory=list, description="List of examples of the paraphrased entities (tasks -> user-stories)."
    )


class ParaphraserOutput(BaseModel):
    """
    This class contains the output for the scrumit application.
    """

    user_story: str = Field(..., description="Paraphrased output text (user story in our case).")
