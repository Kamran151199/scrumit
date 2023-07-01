"""
This module contains the base class for the scrumit application.
"""
import abc

from scrumit.entity import scrumit as entities


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
