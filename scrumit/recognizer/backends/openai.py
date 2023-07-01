"""
This module contains the Recognizer class for the scrumit application using OpenAI backend.

Recognizer is implementation of NER (Named Entity Recognition) using OpenAI API.
It is used to recognize entities (tasks) in the input text and convert them to the output text (user stories).
"""
import ast
from typing import Any

from promptify import Prompter
from pydantic import parse_file_as

from scrumit.config import settings
from scrumit.entity import recognizer as entities
from scrumit.recognizer import base, exceptions


class RecognizerOpenAI(base.RecognizerBase):
    """
    This is an implementation of the Recognizer class.

    This version uses the Promtify package with OpenAI's GPT-3 model.
    """

    def __init__(
        self,
        model: Any,
        prompter: Prompter,
        template: str = "ner.jinja",
        include_default_examples: bool = True,
        examples: list[entities.RecognizerExample] = None,
        combine_ud_examples: bool = True,
    ):
        """
        This method initializes the Recognizer application.

        :param model: The OpenAI model to use.
        :param prompter: The Prompter to use.
        :param template: The template to use.
        :param include_default_examples: Whether to include default examples or not.
        :param examples: The examples to use in the current session.
        :param combine_ud_examples: Whether to combine the global user-defined examples
        with the current session examples or not.
        """
        self.model = model
        self.prompter = prompter
        self.template = template
        self.default_examples: list[entities.RecognizerExample] = []
        self.ud_examples: list[entities.RecognizerExample] = examples or []
        self.include_default_examples = include_default_examples
        self.combine_ud_examples = combine_ud_examples

    def recognize(self, text: entities.RecognizerInput, **kwargs) -> entities.RecognizerOutput:
        """
        This method recognizes entities (tasks) in the input text and converts them to the output text (user stories).
        """

        results: list[entities.RecognizerTask] = []
        examples = self.get_examples(text.examples)

        prompter_examples = [
            [
                example.raw,
                [
                    {
                        "Task": example.task,
                        "Persona": example.persona,
                        "Deadline": example.deadline,
                    }
                ],
            ]
            for example in examples
        ]

        output = self.prompter.fit(
            template_name=self.template,
            domain=text.domain,
            text_input=text.text,
            labels=["Task", "Persona", "Deadline"],
            examples=prompter_examples,
        )
        output_text = ast.literal_eval(output["text"])
        if not output_text or not isinstance(output_text, list):
            return entities.RecognizerOutput(tasks=results)

        recognized_entities = output_text[0] if len(output_text) > 0 else []
        for re in recognized_entities:
            if re.get("Task") is not None:
                results.append(
                    entities.RecognizerTask(
                        description=re.get("Task"),
                        persona=re.get("Persona"),
                        deadline=re.get("Deadline"),
                    )
                )
        return entities.RecognizerOutput(tasks=results)

    def get_examples(self, input_examples: list[entities.RecognizerExample]) -> list[entities.RecognizerExample]:
        """
        This method returns the examples used in the current session.

        :param input_examples: The examples provided for individual recognizer input.
        """

        # Default examples provided in package
        if self.include_default_examples:
            try:
                self.default_examples = parse_file_as(
                    list[entities.RecognizerExample], settings.default_recognizer_examples_json
                )
            # TODO: Specify exception
            except Exception as exc:
                raise exceptions.RecognizerException(message=f"Failed to parse default examples JSON: {exc}")

        # User-defined global examples.
        if settings.recognizer_examples_json and self.combine_ud_examples:
            try:
                self.ud_examples += parse_file_as(list[entities.RecognizerExample], settings.recognizer_examples_json)
            # TODO: Specify exception
            except Exception as exc:
                exceptions.RecognizerSerializerException(message=f"Failed to parse examples JSON: {exc}")
        return input_examples + self.default_examples + self.ud_examples
