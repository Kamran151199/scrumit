"""
This module contains the implementation of the Paraphraser class for the scrumit application using OpenAI backend.
"""
from typing import Type  # noqa: TYP001

from openai import Completion, error as openai_error
from pydantic.tools import parse_file_as

from scrumit.config import settings
from scrumit.entity import paraphraser as entities
from scrumit.paraphraser import base, exceptions


class ParaphraserOpenAI(base.ParaphraserBase):
    """
    This class implements the Paraphraser class.

    It paraphrases the input text to a scrum user-story.
    """

    def __init__(
        self,
        client: Type[Completion],
        include_default_examples: bool = True,
        include_global_examples: bool = False,
        examples: list[entities.ParaphraserExample] = None,
        template_wo_ex: str = None,
        template_w_ex: str = None,
        **kwargs,
    ):
        """
        This method initializes the Paraphraser application.
        This version uses the OpenAI API.

        :param client: The OpenAI client to use.
        :param include_default_examples: Whether to include the default examples or not.
        :param include_global_examples: Whether to include the global user-defined examples or not.
        :param examples: The user-defined examples in the current session.
        examples in the current session with the global ones or not.
        :param template_wo_ex: The template to use when there are no examples.
        Will override the default or global-defined templates if provided
        :param template_w_ex: The template to use when there are examples.
        Will override the default or global-defined templates if provided
        """

        self.client = client
        self.default_examples: list[entities.ParaphraserExample] = []
        self.ud_examples: list[entities.ParaphraserExample] = examples or []

        self.include_default_examples = include_default_examples
        self.include_global_examples = include_global_examples

        self.template_wo_ex = (
            settings.default_paraphraser_prompt_template_wo_ex
            if not settings.paraphraser_prompt_template_wo_ex
            else settings.paraphraser_prompt_template_wo_ex
        )
        self.template_w_ex = (
            settings.default_paraphraser_prompt_template_w_ex
            if not settings.paraphraser_prompt_template_w_ex
            else settings.paraphraser_prompt_template_w_ex
        )

        if template_wo_ex:
            self.template_wo_ex = template_wo_ex
        if template_w_ex:
            self.template_w_ex = template_w_ex

    def paraphrase(self, inp: entities.ParaphraserInput, **kwargs) -> entities.ParaphraserOutput:
        """
        This method paraphrases the input text to the output text.

        :param inp: The input text to paraphrase.
        :return: The paraphrased output text (user story in our case).

        :keyword max_tokens: The maximum number of tokens to generate.
        :keyword temperature: What sampling temperature to use.
        :keyword stop: One or more tokens where generation is stopped.
        :keyword engine: The engine to use for the API request.
        :keyword n: Number of completions to generate for each prompt.
        :keyword input_examples_only: Whether to use only the input examples or session configured ones.
        """

        input_examples_only = kwargs.get("input_examples_only", False)
        examples = inp.examples if input_examples_only else self.get_examples(inp.examples)
        prompt = self.get_prompt(inp, examples)

        try:
            response = self.client.create(
                engine=kwargs.get("engine", "text-davinci-003"),
                prompt=prompt,
                max_tokens=kwargs.get("max_tokens", 60),
                temperature=kwargs.get("temperature", 1),
                n=kwargs.get("n", 1),
                stop=kwargs.get("stop", None),
            )
        except openai_error.OpenAIError as err:
            raise exceptions.ParaphraserModelError(str(err))
        if response and getattr(response, "choices", None):
            paraphrased_story = response.choices[0].text.strip()
            return entities.ParaphraserOutput(user_story=paraphrased_story)
        raise exceptions.ParaphraserModelError("No response from the OpenAI API.")

    def get_examples(self, input_examples: list[entities.ParaphraserExample]) -> list[entities.ParaphraserExample]:
        """
        This method returns the examples to use for the current session.

        :param input_examples: The examples to use for the current input text.
        :return: The examples to use for the current session [list of ParaphraserExample].
        """
        if self.include_default_examples:
            try:
                self.default_examples += parse_file_as(
                    list[entities.ParaphraserExample], settings.default_paraphraser_examples_json
                )
            # TODO: Specify exception
            except Exception as exc:
                raise exceptions.ParaphraserException("Error while parsing the default examples file: %s" % str(exc))
        if settings.paraphraser_examples_json and self.include_global_examples:
            try:
                self.ud_examples += parse_file_as(list[entities.ParaphraserExample], settings.paraphraser_examples_json)
            # TODO: Specify exception
            except Exception as exc:
                raise exceptions.ParaphraserSerializationException(
                    "Error while parsing the global examples file: %s" % str(exc)
                )
        return input_examples + self.default_examples + self.ud_examples

    @staticmethod
    def get_examples_as_str(examples: list[entities.ParaphraserExample]) -> str:
        """
        This method returns the examples as a string.

        :param examples: The list of examples [list of ParaphraserExample].
        :return: The examples as a string.
        """
        return "\n".join(
            [
                f'Example #{index}: {ex.original_text}\n"{ex.paraphrased_text}"\n'
                for index, ex in enumerate(examples, start=1)
            ]
        )

    def get_prompt(self, inp: entities.ParaphraserInput, examples: list[entities.ParaphraserExample]) -> str:
        """
        This method returns the prompt to use for the current session.
        :param inp: The input text to paraphrase.
        :param examples: The examples to use for the current session.
        :return: The prompt to use for the current session.
        """
        if examples:
            return self.template_w_ex % (self.get_examples_as_str(examples), inp.text)
        return self.template_wo_ex % inp.text
