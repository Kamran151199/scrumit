"""
This module contains the entities for the Recognizer service.
"""

from pydantic import BaseModel, Field


class RecognizerExample(BaseModel):
    """
    This class contains the output for the scrumit application.
    """

    task: str = Field(..., description="Task to be recognized.", alias="Task")
    persona: str = Field("user", description="Persona of the task", alias="Persona")
    deadline: str = Field(None, description="Deadline of the task. When will the task be done.", alias="Deadline")
    raw: str = Field(..., description="Raw text of the task.")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "task": "Fixing the 3d-party login",
                "persona": "user",
                "deadline": "27th of May",
                "raw": "Hey, the 3d-party login is broken. "
                "Please fix it by 27th of May else users will not be able to login.",
            }
        }


class RecognizerInput(BaseModel):
    """
    This class contains the input for the scrumit application.
    """

    text: str = Field(..., description="Input text to be converted to user stories.")
    domain: str = Field(..., description="Domain of the input text. Used for NER to properly identify the entities.")
    examples: list[RecognizerExample] = Field(
        default_factory=list, description="List of examples of the recognized entities (tasks in our case)."
    )


class RecognizerTask(BaseModel):
    """
    This class contains the output for the scrumit application.
    """

    description: str = Field(..., description="Description of the task.", alias="Task")
    persona: str = Field("user", description="Persona of the task. For whom the task should be done.", alias="Persona")
    deadline: str = Field(None, description="Deadline of the task. When will the task be done.", alias="Deadline")

    class Config:
        allow_population_by_field_name = True


class RecognizerOutput(BaseModel):
    """
    This class contains the output for the scrumit application.
    """

    tasks: list[RecognizerTask] = Field(
        default_factory=list, description="List of recognized entities (tasks in our case)."
    )
