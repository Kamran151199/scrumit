"""
This module contains the Recognizer class for the scrumit application.

Recognizer is implementation of NER (Named Entity Recognition) using OpenAI API.
It is used to recognize entities (tasks) in the input text and convert them to the output text (user stories).
"""
import ast
from typing import Any

from promptify import Prompter
from pydantic import parse_file_as

from scrumit.config import settings
from scrumit.entity import recognizer as entities
from scrumit.recognizer.base import RecognizerBase


class Recognizer(RecognizerBase):
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
    ):
        """
        This method initializes the Recognizer application.

        :param model: The OpenAI model to use.
        :param prompter: The Prompter to use.
        :param template: The template to use.
        :param include_default_examples: Whether to include default examples or not.
        """
        self.model = model
        self.prompter = prompter
        self.template = template
        self.default_examples = []  # Default examples provided in package
        self.ud_examples = []  # User-defined examples

        if include_default_examples:
            self.default_examples = parse_file_as(list[entities.RecognizerExample], settings.default_examples_json)

        if settings.examples_json:
            self.ud_examples = parse_file_as(list[entities.RecognizerExample], settings.examples_json)

    def recognize(self, text: entities.RecognizerInput) -> entities.RecognizerOutput:
        """
        This method recognizes entities (tasks) in the input text and converts them to the output text (user stories).
        """

        results: list[entities.RecognizerTask] = []
        examples = text.examples + self.default_examples + self.ud_examples
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
