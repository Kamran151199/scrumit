"""
This module contains the entities for the Paraphraser service.
"""

from pydantic import BaseModel
from pydantic.fields import Field


class ParaphraserInput(BaseModel):
    """
    This class contains the input for the scrumit application.
    """

    text: str = Field(..., description="Input text to be converted to user stories.")


class ParaphraserOutput(BaseModel):
    """
    This class contains the output for the scrumit application.
    """

    user_story: str = Field(..., description="Paraphrased output text (user story in our case).")
