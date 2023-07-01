"""
This module contains the main class for the scrumit application.
"""

import abc

from scrumit.entity import scrumit as entities
from scrumit.paraphraser.base import ParaphraserBase
from scrumit.recognizer.base import RecognizerBase


class ScrumitBase(abc.ABC):
    """
    This is an abstract class for the scrumit application.
    """

    @abc.abstractmethod
    def convert(self, text: entities.Input) -> entities.Output:
        """
        This method converts the input text to the output text.
        """
        ...


class Scrumit(ScrumitBase):
    """
    This class is the main class for the scrumit application.
    """

    def __init__(
        self,
        recognizer: RecognizerBase,
        paraphraser: ParaphraserBase,
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

    def convert(self, text: entities.Input) -> entities.Output:
        """
        This method converts the input text to the output text.
        """
        ...
