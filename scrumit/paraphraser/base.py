"""
This module contains the base Paraphraser (abstract/interface) class for the scrumit application.

Paraphraser is implementation of Text Summarization.
"""

import abc

from scrumit.entity import paraphraser as entities


class ParaphraserBase(abc.ABC):
    """
    This is an abstract class for the Paraphraser class.
    """

    @abc.abstractmethod
    def paraphrase(self, inp: entities.ParaphraserInput, **kwargs) -> entities.ParaphraserOutput:
        """
        This method paraphrases the input text to the output text.
        """
        ...
