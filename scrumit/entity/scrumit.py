"""
This module contains the entities for the
Scrumit application (composite of the Recognizer and Paraphraser services).
"""

from pydantic import BaseModel
from pydantic.fields import Field

from scrumit.entity import paraphraser as paraphraser_entities, recognizer as recognizer_entities


class Input(BaseModel):
    """
    This class contains the input for the scrumit application.
    """

    text: str = Field(..., description="Input text to be converted to user stories.")
    domain: str = Field(..., description="Domain of the input text. Used for NER to properly identify the entities.")
    ner_examples: list[recognizer_entities.RecognizerExample] = Field(
        default_factory=list, description="List of examples of the recognized entities (conversations -> tasks)."
    )
    paraphraser_examples: list[paraphraser_entities.ParaphraserExample] = Field(
        default_factory=list, description="List of examples of the paraphrased entities (tasks -> user-stories)."
    )


class UserStory(BaseModel):
    """
    This class contains the user story for the scrumit application.
    """

    task: str = Field(..., description="Original text - excerpt from the input text.")
    story: str = Field(..., description="User story text.")


class Output(BaseModel):
    """
    This class contains the output for the scrumit application.
    """

    stories: list[UserStory] = Field(..., description="List of user stories.")
