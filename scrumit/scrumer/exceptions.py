"""
This module contains the exceptions for the scrumit service.
"""


class ScrumitException(Exception):
    """
    This class implements the exception for the scrumit service.
    """

    def __init__(self, message: str):
        """
        This method initializes the exception.

        :param message: The message of the exception.
        """
        super().__init__(message)
        self.message = message
