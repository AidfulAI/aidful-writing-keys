import yaml
import pyperclip
import requests
from pynput import keyboard
import time

kboard = keyboard.Controller()
is_processing = False


def read_config():
    with open('config.yml', 'r') as file:
        return yaml.safe_load(file)

config = read_config()

def on_hotkey(action):
    """
    Handles the hotkey press event to perform text processing.

    This function is triggered when the user presses the configured hotkey. It performs the following steps:
    1. Simulates Ctrl+A and Ctrl+C to select and copy the text.
    2. Retrieves the copied text from the clipboard.
    3. Sends the text to a language model for processing.
    4. Copies the processed text back to the clipboard.
    5. Simulates Ctrl+V to paste the processed text.

    Notes:
    1. There's an unexpected behavior when splitting Ctrl+A and Ctrl+C into separate
    'with' statements, causing the function to execute twice.
    2. For many key combinations the initial script hang because this function was
    called multiple times. This is no prevented with the global is_processing variable.
    """
    global is_processing
    if is_processing:
        #print("is_processing triggered")
        return # Prevents double execution
    is_processing = True

    try:
        # Add everything selectable to the clipboard
        with kboard.pressed(keyboard.Key.ctrl):
            kboard.press('a')
            kboard.release('a')
            kboard.press('c')
            kboard.release('c')

        # Give some time to update the clipboard content
        time.sleep(0.01)

        # Get text from clipboard
        text = pyperclip.paste()

        # Send text to LLM for processing
        processed_text = process_text(text, action)

        # Put processed text back in clipboard
        pyperclip.copy(processed_text)

        # Replace the current text by pasting the content back in the active window
        with kboard.pressed(keyboard.Key.ctrl):
            kboard.press('a') # Ensure that the current text is selected
            kboard.release('a')
            kboard.press('v')
            kboard.release('v')
    finally:
        is_processing = False

def process_text(text, action):
    """
    Processes the given text using the Ollama API based on the specified action.

    This function sends the input text to a language model via the Ollama API
    for processing according to the action's configuration.

    Args:
        text (str): The input text to be processed.
        action (dict): The action configuration from the YAML file.

    Returns:
        str: The processed text if the API call is successful, or an error message if it fails.

    Raises:
        No exceptions are raised directly, but errors in the API call are returned as strings.
    """
    api_url = "http://localhost:11434/api/generate"
    data = {
        "model": action['llm'],
        "prompt": f"{action['ask']}\n\n{text}\n\n",
        "stream": False
    }
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        return response.json()['response'].strip()
    else:
        return(f"Error calling Ollama: {response.status_code}, {response.text}")

def main():
    hotkeys = {}
    for action in config['actions']:
        hotkeys[action['key']] = lambda action=action: on_hotkey(action)

    with keyboard.GlobalHotKeys(hotkeys) as h:
        print("aidful-key app is running:")
        for action in config['actions']:
            print(f"Press {action['key']} to {action['def']} using {action['llm']}")
        h.join()

if __name__ == "__main__":
    main()
