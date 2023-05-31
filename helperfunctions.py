"""
Helper functions that handle user input for CoverletterMe
"""

import openai
import tkinter as tk
from tkinter import filedialog, messagebox
import docx
import pickle


def get_completion(prompt, model="gpt-3.5-turbo"):
    """
    Function that gets response from ChatGPT 3.5 

    Input:
    prompt - prompt for ChatGPT
    model - ChatGPT version to use

    Output:
    response - output from ChatGPT
    """
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def get_api_key():
    """
    Function that prompts user to input ChatGPT API, cache the result

    Output:
    key - ChatGPT API key formatted in string
    """

    api_key = get_cached_file("API_key")
    
    if api_key is None:
        root = tk.Tk()
        root.withdraw()
        api_key = tk.simpledialog.askstring("API key", 
                                            "Enter your OpenAI API key. If you don't have it, please go to https://platform.openai.com/account/api-keys")
        # Cache the docx_string using pickle
        with open("API_key.pkl", "wb") as f:
            pickle.dump(api_key, f)
    
    return api_key


def select_docx_file(filename):
    """
    Prompts user to select a .docx file 

    Input:
    filename - string indexing the type of the file selected 

    Output:
    docx_string - content in the .docx file, formatted as a string
    """

    messagebox.showinfo(filename, f"Please select your current {filename}")

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Word Document", "*.docx")])

    if file_path:
        # Read the input text as a string using the docx package
        doc = docx.Document(file_path)
        paragraphs = [p.text for p in doc.paragraphs]
        docx_string = "\n".join(paragraphs)

        # Cache the input text string using pickle
        with open(f"""{filename.replace(" ", "_")}.pkl""", "wb") as f:
            pickle.dump(docx_string, f)
    else:
        messagebox.showwarning(filename, f"No file selected. No {filename} cached.")
        docx_string = get_cached_file(filename)
    
    return docx_string


def enter_docx_file(filename):
    """
    Prompts user to manually enter some text

    Input:
    filename - string indexing the type of the text requested

    Output:
    docx_string - user input, formatted as a string
    """

    root = tk.Tk()
    root.withdraw()
    docx_string = tk.simpledialog.askstring(filename, f"Enter your {filename}:")
    
    if docx_string:
        # Cache the docx_string using pickle
        with open(f"""{filename.replace(" ", "_")}.pkl""", "wb") as f:
            pickle.dump(docx_string, f)
    else:
        messagebox.showwarning(filename, f"No {filename} entered. No {filename} cached.")
        docx_string = get_cached_file(filename)

    return docx_string


def get_cached_file(filename):
    """
    Retrieves cached file stored in a pickle

    Input:
    filename - string indexing the type of the file selected 

    Output:
    docx_string - content in the .docx file, formatted as a string. 
                  or None if said file doesn't exist
    """

    try:
        with open(f"""{filename.replace(" ", "_")}.pkl""", "rb") as f:
            docx_string = pickle.load(f)
        return docx_string
    except FileNotFoundError:
        return None
    

def get_resume():
    """
    Prompt user to select a file containing resume, cache the result

    Output:
    resume - content in the resume file, formatted as string
    """

    # Check if there is a pickled file for resume
    resume = get_cached_file("Resume")

    if resume is not None:
        # Ask the user if they wish to use the existing resume
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askyesno("Resume", "Do you want to use the existing resume?")

        if not result:
            # Prompt the user to select a .docx file using GUI
            resume = select_docx_file("Resume")
    else:
        # Prompt the user to select a .docx file using GUI
        resume = select_docx_file("Resume")
    
    return resume


def get_coverletter():
    """
    Prompt user to select a file containing cover letter, cache the result

    Output:
    cover_letter - content in the coverletter file, formatted as string
    """
     
    # Check if there is a pickled file for cover
    cover_letter = get_cached_file("Cover Letter")

    if cover_letter is not None:
        # Ask the user if they wish to use the existing cover letter
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askyesno("Cover Letter", "Do you want to use the existing cover letter?")

        if not result:
            # Prompt the user to select a .docx file using GUI
            cover_letter = select_docx_file("Cover letter")
    else:
        # Prompt the user to select a .docx file using GUI
        cover_letter = select_docx_file("Cover letter")

    return cover_letter


def get_job_description():
    """
    Prompt user to select a file containing job description, cache the result

    Output:
    description - content in user input, formatted as string
    """
     
    # Check if there is a pickled file for job description
    description = get_cached_file("Job description")

    if description is not None:
        # Ask the user if they wish to use the existing job description
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askyesno("Job description", "Do you want to use the existing job description?")

        if not result:
            # Prompt the user to select a .docx file using GUI
            description = enter_docx_file("Job description")
    else:
        # Prompt the user to select a .docx file using GUI
        description = enter_docx_file("Job description")
    
    return description


def get_remarks():
    """
    Prompt user to select a file containing addition prompt, cache the result

    Output:
    remarks - content in user input, formatted as string
    """
     
    # Check if there is a pickled file for additional prompt
    remarks = get_cached_file("Additional prompt")

    if remarks is not None:
        # Ask the user if they wish to use the existing remarks
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askyesno("Additional prompt", "Do you want to change existing additional prompt?")

        if not result:
            # Prompt the user to select a .docx file using GUI
            remarks = enter_docx_file("Additional prompt")
    else:
        # Prompt the user to select a .docx file using GUI
        remarks = enter_docx_file("Additional prompt")
    
    return remarks


def get_prompt():
    """
    Helper function to generate ChatGPT prompt

    Output:
    prompt used to get ChatGPT generated coverletter
    """
    resume = get_resume()
    reference_coverletter = get_coverletter()
    description = get_job_description()
    remarks = get_remarks()
    prompt = f"""
    Perform the following actions: 
    1 - Summarize the requirements for the following job \
    description delimited by triple backticks.
    Job description: ```{description}```

    2 - Extract skills and experience relevant to the job \
    description from the resume delimited by triple backticks, \
    extract skills and experiences from the job description.
    Resume: ```{resume}```

    3 - Summarize relevant information from the following \
    coverletter deliminated by triple backticks.
    Reference coverletter: ```{reference_coverletter}```

    4 - Output a coverletter for the summarized job description in a \
    professional and conversational tone. Format your response to be \
    consistent with the reference cover letter.

    The is intended for hiring manager, so it should focus on matching \
    qualifications from the summarized resume and the cover letter to the \
    job description provided. 

    Qualification should be presented using the "show, don't tell" technique. 
        
    Try to establish a relationship between my experiences and the job. 

    Keep in mind that {remarks}.
    """

    return prompt