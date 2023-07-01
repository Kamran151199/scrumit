"""
This module contains the custom exceptions for the Paraphraser service.
"""


class ParaphraserException(Exception):
    """
    Default exception for the Paraphraser service.
    """

    def __init__(self, message: str = "Something went wrong.", *args):
        """
        This method initializes the ParaphraserException class.

        :param message: The message to display.
        """
        self.message = message
        super().__init__(message, *args)


class ParaphraserModelError(ParaphraserException):
    """
    Exception for the Paraphraser service when the model behind it fails.
    """

    def __init__(self, message: str = "Model behind the Paraphraser service failed.", *args):
        """
        This method initializes the ParaphraserModelError class.

        :param message: The message to display.
        """
        self.message = message
        super().__init__(message, *args)


class ParaphraserSerializationException(ParaphraserException):
    """
    Exception for the Paraphraser service when the serialization fails.
    """

    def __init__(self, message: str = "Serialization failed.", *args):
        """
        This method initializes the ParaphraserSerializationException class.

        :param message: The message to display.
        """
        self.message = message
        super().__init__(message, *args)
