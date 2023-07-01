import openai


def paraphrase_to_scrum_story(text):
    # Set up OpenAI API credentials
    openai.api_key = "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"

    # Define the prompt
    prompt = f'Paraphrase the following text into a scrum story:\n"{text}"\n\n'

    # Generate paraphrased scrum story using GPT-3
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=prompt, max_tokens=32, temperature=1, n=1, stop=None
    )

    # Extract the generated scrum story from the API response
    paraphrased_story = response.choices[0].text.strip()

    return paraphrased_story


# Example usage
input_text = "The button should be working in the header page."
paraphrased_story = paraphrase_to_scrum_story(input_text)
print(paraphrased_story)
