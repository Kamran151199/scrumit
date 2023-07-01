# Scrumit

## Description

Scrumit is a utility package that converts raw text to scrum user stories

## Requirements

- Python 3.10+

## Installation

```bash
pip install scrumit
```

## Usage

### CLI

#### Sample run
```bash
scrumit -s ./conversation.sample -d software -o ./output.sample
```

#### Help
```bash
scrumit --help
```


### Python
```python
import openai
from promptify import OpenAI, Prompter

from scrumit.config import settings
from scrumit.entity.scrumit import Input
from scrumit.paraphraser.backends import ParaphraserOpenAI
from scrumit.recognizer.backends import RecognizerOpenAI
from scrumit.scrumer import Scrumer


def main():
    openai.api_key = settings.openai_api_key
    model = OpenAI(settings.openai_api_key)

    # recognizer
    prompter = Prompter(model)
    recognizer = RecognizerOpenAI(model, prompter)

    # paraphraser
    client = openai.Completion
    paraphraser = ParaphraserOpenAI(client)

    # scrumit
    scrumer = Scrumer(recognizer, paraphraser)
    conversation = Input(
        text="""
            Hey, have you heard about the latest bug fixes in the dating app, MatchMate?
            Oh, yes! They just released an update with some significant bug fixes. What specifically are you interested in?
            Well, I've been experiencing some issues with the matching algorithm. It doesn't seem to be working properly.
            Good news! The latest update addresses that. They've made improvements to the algorithm to ensure better matching accuracy. It should now provide more relevant matches based on your preferences and interests.
            That's great to hear! I was also encountering a problem where the app would crash randomly. Has that been fixed too?
            Absolutely! The developers have identified the cause of those crashes and implemented a fix. You should no longer experience any unexpected app shutdowns. They've also optimized the app's performance overall, making it more stable and responsive.
            That's a relief. Another issue I had was with the chat feature. Sometimes messages would get delayed or not show up at all.
            Yes, they've made significant improvements to the chat functionality. The messaging system has been optimized to ensure faster and more reliable delivery of messages. You should now experience smoother conversations with minimal delays or missing messages.
            Perfect! I've also noticed some minor UI glitches in the app. Are those taken care of too?
            Indeed! The developers have addressed various UI glitches reported by users. They've refined the interface to provide a more polished and visually appealing experience. The app should now look more cohesive and consistent across different devices.
            That's fantastic news! It seems like they've really been listening to user feedback and actively working on improving the app.
            Absolutely, user feedback is crucial, and the developers at MatchMate have been actively engaged with their user community. They've been working diligently to identify and fix any reported issues, ensuring a better overall experience for everyone.
            That's reassuring. I'm looking forward to updating the app and trying out all these bug fixes. Thanks for the information!
            You're welcome! Enjoy the updated MatchMate experience, and I hope you have some amazing connections on the app. Let me know if you have any other questions!
            """,
        domain="software",
    )
    outputs = scrumer.convert(conversation)
    print(outputs)


if __name__ == "__main__":
    main()

```

## Output

```
Output(stories=[UserStory(task='The matching algorithm should provide more relevant matches based on user preferences and interests.', story='"As a user, I want the matching algorithm to provide more relevant matches based on my preferences and interests so that I get accurate results."'), UserStory(task='The app should no longer experience any unexpected app shutdowns.', story='"As a user I want to be able to use the app without any unexpected app shutdowns so I can have a reliable experience."'), UserStory(task='The messaging system should be optimized to ensure faster and more reliable delivery of messages.', story='Paraphrase: "As a user I want to be able to have a messaging system that is optimized for faster and more reliable delivery of messages so I can communicate efficiently."'), UserStory(task='The interface should be refined to provide a more polished and visually appealing experience.', story='"As a user I want the interface to be refined to provide a more polished and visually appealing experience so I have a better user experience."'), UserStory(task='The developers should actively engage with their user community and identify and fix any reported issues.', story='Scrum Story: "As a user I want the developers to actively engage with the user community and to identify and fix any issues I report so I can continue to have an enjoyable experience using the product."')])
```
