import pyperclip
import requests
from pynput import keyboard
import clipman
import time

kboard = keyboard.Controller()
clipman.init()

def on_hotkey():
    """
    Handles the hotkey press event to perform text correction.

    This function is triggered when the user presses Ctrl+Shift+C. It performs the following steps:
    1. Simulates Ctrl+A and Ctrl+C to select and copy the text.
    2. Retrieves the copied text from the clipboard.
    3. Sends the text to a language model for correction.
    4. Copies the corrected text back to the clipboard.
    5. Simulates Ctrl+V to paste the corrected text.

    Note: There's an unexpected behavior when splitting Ctrl+A and Ctrl+C into separate
    'with' statements, causing the function to execute twice. This is currently under investigation.
    """

    # -------------------------------------------------------------------------
    # Unexpected behavior: Splitting Ctrl+A and Ctrl+C into separate 'with'
    # statements causes the print statement to execute twice. Investigate why.
    # For now, keeping them in a single 'with' statement as a workaround.
    # -------------------------------------------------------------------------
    with kboard.pressed(keyboard.Key.ctrl):
        kboard.press('a')
        kboard.release('a')
        kboard.press('c')
        kboard.release('c')

    time.sleep(0.01)

    # Get text from clipboard
    text = clipman.get()
    print(text)

    # Send text to LLM for correction
    corrected_text = correct_text(text)

    # Put corrected text back in clipboard
    pyperclip.copy(corrected_text)
    print(corrected_text)

    with kboard.pressed(keyboard.Key.ctrl):
        kboard.press('v')
        kboard.release('v')

def correct_text(text):
    """
    Corrects the spelling and grammar of the given text using the Ollama API.

    This function sends the input text to a language model (phi3.5:3.8b) via the Ollama API
    for spelling and grammar correction. It constructs a prompt that instructs the model
    to return the corrected text without any additional explanations.

    Args:
        text (str): The input text to be corrected.

    Returns:
        str: The corrected text if the API call is successful, or an error message if it fails.

    Raises:
        No exceptions are raised directly, but errors in the API call are returned as strings.
    """
    api_url = "http://localhost:11434/api/generate"
    data = {
        "model": "phi3.5:3.8b",
        "prompt": f"Reply only with exactly the same text as entered below, but correct the spelling and grammar. Do not add any explanation of what you correct:\n\n{text}\n\n",
        "stream": False
    }
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        return response.json()['response'].strip()
    else:
        return(f"Error calling Ollama: {response.status_code}, {response.text}")

def main():
    with keyboard.GlobalHotKeys({'<ctrl>+<shift>+c': on_hotkey}) as h:
        print("Text correction app is running. Press Ctrl+Shift+C to correct text.")
        h.join()

if __name__ == "__main__":
    main()
