"""
This module contains the exceptions for the recognizer service.
"""


class RecognizerException(Exception):
    """
    Default exception for the recognizer service.
    """

    def __init__(self, message: str = "Recognizer crashed due to unexpected error", *args):
        """
        This method initializes the exception.

        :param message: The message for the exception.
        :param args: The arguments for the exception.
        """
        self.message = message
        super().__init__(message, *args)


class RecognizerSerializerException(RecognizerException):
    """
    Exception for the recognizer service when the serializer fails.
    """

    def __init__(self, message: str = "Serialization failed.", *args):
        """
        This method initializes the exception.

        :param message: The message for the exception.
        :param args: The arguments for the exception.
        """
        self.message = message
        super().__init__(message, *args)
