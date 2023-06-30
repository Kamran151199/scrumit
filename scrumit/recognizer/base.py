"""
This module contains the base Recognizer (abstract/interface) class for the scrumit application.

Recognizer is implementation of NER (Named Entity Recognition) using OpenAI API.
It is used to recognize entities (tasks) in the input text and convert them to the output text (user stories).
"""

import abc

from scrumit.entity import recognizer as entities


class RecognizerBase(abc.ABC):
    """
    This is an abstract class for the Recognizer class.
    """

    @abc.abstractmethod
    def recognize(self, text: entities.RecognizerInput) -> entities.RecognizerOutput:
        """
        This method recognizes entities (tasks) in the input text and converts them to the output text (user stories).
        """
        ...
