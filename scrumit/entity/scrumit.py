"""
This module contains the entities for the
Scrumit application (composite of the Recognizer and Paraphraser services).
"""

from pydantic import BaseModel
from pydantic.fields import Field


class Input(BaseModel):
    """
    This class contains the input for the scrumit application.
    """

    text: str = Field(..., description="Input text to be converted to user stories.")


class UserStory(BaseModel):
    """
    This class contains the user story for the scrumit application.
    """

    original_text: str = Field(..., description="Original text - excerpt from the input text.")
    story: str = Field(..., description="User story text.")


class Output(BaseModel):
    """
    This class contains the output for the scrumit application.
    """

    stories: list[UserStory] = Field(..., description="List of user stories.")
