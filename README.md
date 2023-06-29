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

```python
from scrumit import Scrumit

scrumit = Scrumit(openai_api_key="YOUR_API_KEY")
output = scrumit.convert(
    "So, guys there should be a button that allows users to generate a scrum user story from raw text")
print(output.story)
```

## Output

```bash
As a user, I want to be able to generate a scrum user story from raw text
```

