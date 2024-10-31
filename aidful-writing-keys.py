import yaml
import pyperclip
import requests
from pynput import keyboard
import time
import signal
import sys

kboard = keyboard.Controller()
is_processing = False
hotkey_listener = None

def signal_handler(sig, frame):
    print("\nShutting down gracefully...")
    if hotkey_listener:
        hotkey_listener.stop()
    sys.exit(0)

def read_config():
    with open('config.yml', 'r') as file:
        return yaml.safe_load(file)

config = read_config()

def on_hotkey(action):
    """
    Handles the hotkey press event to perform text processing.

    This function is triggered when the user presses the configured hotkey. It performs the following steps:
    1. Simulates Ctrl+C to copy the currently selected text.
    2. Retrieves the copied text from the clipboard.
    3. Sends the text to a language model for processing.
    4. Copies the processed text back to the clipboard.
    5. Simulates Ctrl+V to paste the processed text.

    Notes:
    1. If no text selected, the current content of the clipboard is processed and pasted at the cursor position.
    2. For many key combinations the initial script hang because this function was
    called multiple times. This is now prevented with the global is_processing variable.
    """
    global is_processing
    if is_processing:
        #print("is_processing triggered")
        return # Prevents double execution
    is_processing = True

    try:
        # Add everything selectable to the clipboard
        with kboard.pressed(keyboard.Key.ctrl):
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
    global hotkey_listener
    signal.signal(signal.SIGINT, signal_handler)

    hotkeys = {}
    for action in config['actions']:
        hotkeys[action['key']] = lambda action=action: on_hotkey(action)

    hotkey_listener = keyboard.GlobalHotKeys(hotkeys)
    with hotkey_listener as h:
        print("aidful-key app is running:")
        for action in config['actions']:
            print(f"Press {action['key']} to {action['def']} using {action['llm']}")
        print("Press <ctrl>+c in this terminal to exit")
        h.join()

if __name__ == "__main__":
    main()
