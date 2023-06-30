"""
This module contains the main class for the scrumit application.
"""

import abc

import config
from entity import scrumit as entities


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

    def __init__(self, config: config.Config):
        """
        This method initializes the scrumit application.

        :param config: The configuration for the scrumit application.
        """
        self.config = config

    def convert(self, text: entities.Input) -> entities.Output:
        """
        This method converts the input text to the output text.
        """
        ...
