# aidful-writing-keys

A Python application that provides customizable keyboard shortcuts for AI-powered text processing using local language models through Ollama.

## Description

The application allows you to enhance your writing workflow by processing selected text through language models with simple keyboard shortcuts. Whether you want to fix errors, translate, or transform text in other ways, you can do it quickly without leaving your current application.

## Prerequisites

- Python 3.x
- [Ollama](https://ollama.ai/) installed and running locally

## Installation

1. Clone this repository
2. Create a virtual environment (this isolates the project's dependencies from your system Python installation and will be used by the startup script):
```bash
python -m venv .venv
```
3. Activate the virtual environment:
- Linux (and also macOS, but untested):
```bash
source .venv/bin/activate
```
- Windows:
```bash
.venv\Scripts\activate
```
4. Install required packages:
```bash
pip install -r requirements.txt
```
5. Configure your hotkeys and actions in `config.yml`

## Usage

1. Start Ollama on your system
2. Activate the virtual environment (see Installation section above)
3. Run the script:
```bash
python aidful-writing-keys.py
```
4. Select text in any application
5. Press your configured hotkey to process the text
6. The processed text will automatically replace your selection

## Autostart
- Linux: adapt and add `run-aidful-writing-key.sh` to your autostart applications. This will activate the .venv and run the application.

## Configuration

Edit `config.yml` to customize your hotkeys and actions. Example configuration:

```yaml
actions:
  - def: fix text
    key: <ctrl>+<alt>+q
    llm: gemma2:2b
    ask: "Reply only with exactly the same text as entered below, but correct the spelling and grammar. Do not add any explanation of what you correct:"

  - def: rewrite formal
    key: <ctrl>+<alt>+w
    llm: gemma2:2b
    ask: "Rewrite the following very formal and polite. No explanations or note:"

  - def: translate to German
    key: <ctrl>+<alt>+e
    llm: gemma2:2b
    ask: "Translate the following text to German. Only provide the translation, no explanations or note:"
```

## Features

- Global hotkeys that work in any application
- Customizable language model selection
- Configurable text processing instructions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Ollama](https://ollama.ai/)
