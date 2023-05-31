"""
CoverletterMe is an open source tool that writes coverletter for you using ChatGPT

How to use: 
Run python CoverletterMe.py in terminal/console

If the window freezes after entering remarks, it's because ChatGPT is taking
the time to generate your coverletter, please wait patiently.
"""

import openai
from tkinter import messagebox
from helperfunctions import get_completion, get_api_key, get_prompt


def main():
    # Connect to OpenAI using user API
    openai.api_key = get_api_key()

    # Get response using prompt
    prompt = get_prompt()
    response = get_completion(prompt)

    # Save response in text file
    with open("your_new_cover_letter.txt", "w") as f:
        f.write(response)

    messagebox.showinfo("CoverletterMe", "New cover letter successfully saved in your_new_cover_letter.txt")


if __name__ == "__main__":
    main()