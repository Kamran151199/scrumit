"""
This module contains the main class for the scrumit application.
"""

from scrumit.entity import paraphraser as paraphraser_entities, recognizer as recognizer_entities, scrumit as entities
from scrumit.paraphraser import base as paraphraser_base, exceptions as paraphraser_exceptions
from scrumit.recognizer import base as recognizer_base, exceptions as recognizer_exceptions
from scrumit.scrumer import base, exceptions as exceptions


class Scrumer(base.ScrumerBase):
    """
    This class is the main class for the scrumit application.
    """

    def __init__(
        self,
        recognizer: recognizer_base.RecognizerBase,
        paraphraser: paraphraser_base.ParaphraserBase,
    ):
        """
        This method initializes the scrumit application.

        :param recognizer: The recognizer to use.
        It is used to recognize entities (tasks) in the input text.
        :param paraphraser: The paraphraser to use.
        It is used to paraphrase the recognized entities (tasks) to the output text (user stories).
        """
        self.recognizer = recognizer
        self.paraphraser = paraphraser

    def convert(self, inp: entities.Input) -> entities.Output:
        """
        This method converts the input text (conversation trascript) to the output text (user stories).
        """

        user_stories: list[entities.UserStory] = []
        try:
            ner_output = self.recognizer.recognize(
                recognizer_entities.RecognizerInput(text=inp.text, domain=inp.domain, examples=inp.ner_examples)
            )
        except recognizer_exceptions.RecognizerException as e:
            raise exceptions.ScrumitException(f"Could not recognize entities: {e.message}")
        for task in ner_output.tasks:
            try:
                paraphrased = self.paraphraser.paraphrase(
                    paraphraser_entities.ParaphraserInput(text=task.description, examples=inp.paraphraser_examples)
                )
                user_stories.append(entities.UserStory(task=task.description, story=paraphrased.user_story))
            except paraphraser_exceptions.ParaphraserException as e:
                raise exceptions.ScrumitException(
                    f"Could not paraphrase the task {task.description}. Reason: {e.message}"
                )
        return entities.Output(stories=user_stories)
