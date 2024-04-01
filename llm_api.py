import openai

# Replace "your_openai_api_key_here" with your actual OpenAI API key
openai.api_key = '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'

def process_with_gpt4(input_text):
    """
    Sends input text to GPT-4 and returns the response.
    """
    response = openai.Completion.create(
        engine="text-davinci-003", # or "gpt-4" if available for your account
        prompt=input_text,
        temperature=0.7,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text.strip()

# Example usage with the output from the Selenium script
selenium_output = "This is the data collected from the webpage."
processed_output = process_with_gpt4(selenium_output)

print("Processed Output:", processed_output)
