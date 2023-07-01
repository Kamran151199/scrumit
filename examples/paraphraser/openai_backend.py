"""
This module contains the examples for Paraphraser service using OpenAI backend.
"""

import openai

from scrumit.config import settings
from scrumit.entity.paraphraser import ParaphraserInput
from scrumit.paraphraser.backends import ParaphraserOpenAI


def main():
    """
    This method is the entry point for the script.
    """

    if not settings.openai_api_key:
        raise ValueError("OpenAI API key must be provided to use OpenAI backend.")
    openai.api_key = settings.openai_api_key

    paraphraser = ParaphraserOpenAI(openai.Completion)
    inp = ParaphraserInput(
        text="Newly submitted comments should appear without needing a page refresh in the comment section."
    )
    out = paraphraser.paraphrase(inp)

    print(f'Input: "{inp.text}"\n' f'Output: "{out.user_story}"\n')


if __name__ == "__main__":
    main()
